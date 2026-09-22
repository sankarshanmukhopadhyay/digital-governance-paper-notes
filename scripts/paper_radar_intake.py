#!/usr/bin/env python3
"""Create or resurface GitHub issue intake records from a Paper Radar ledger."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import paper_radar as radar  # noqa: E402

USER_AGENT = "digital-governance-paper-notes-paper-radar-intake/0.1"
LIFECYCLE_LABELS = {
    "radar:candidate",
    "radar:needs-judgment",
    "review:backlog",
    "review:in-progress",
    "review:published",
    "disposition:deferred",
    "disposition:declined",
}


def github_json(url: str, token: str, method: str = "GET", payload: dict | None = None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        body = response.read().decode("utf-8")
        return json.loads(body) if body else {}


def load_all_issues(repo: str, token: str) -> list[dict]:
    issues = []
    for page in range(1, 6):
        url = f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={page}"
        data = github_json(url, token)
        if not isinstance(data, list) or not data:
            break
        issues.extend(issue for issue in data if not issue.get("pull_request"))
        if len(data) < 100:
            break
    return issues


def item_keys(item: dict) -> set[str]:
    keys = radar.identity_keys(item)
    keys.update(item.get("alternate_identifiers") or [])
    return keys


def issue_keys(issue: dict) -> set[str]:
    title = radar.issue_paper_title(issue.get("title") or "")
    keys, _ = radar.extract_refs(issue.get("body") or "", title)
    return keys


def same_issue_item(issue: dict, item: dict) -> bool:
    if item_keys(item) & issue_keys(issue):
        return True
    a = radar.norm(radar.issue_paper_title(issue.get("title") or ""))
    b = radar.norm(item.get("title") or "")
    return bool(a and b and (a == b or (min(len(a), len(b)) >= 28 and (a in b or b in a))))


def select_items(payload: dict) -> list[dict]:
    return [
        item for item in payload.get("items", [])
        if item.get("state") in {"candidate", "needs_judgment"} and not item.get("already_represented")
    ]


def intake_label(item: dict, cfg: dict) -> str:
    intake = cfg.get("issue_intake") or {}
    if item.get("state") == "candidate":
        return intake.get("candidate_label", "radar:candidate")
    return intake.get("judgment_label", "radar:needs-judgment")


def issue_title(item: dict) -> str:
    theme = item.get("theme") or "paper"
    return f"radar({theme}): {item.get('title', '').strip()}"


def issue_body(item: dict, generated_at: str) -> str:
    identifiers = []
    if item.get("doi"):
        identifiers.append(f"- DOI: {item['doi']}")
    if item.get("arxiv_id"):
        identifiers.append(f"- arXiv: {item['arxiv_id']}")
    identifier_block = "\n".join(identifiers) if identifiers else "- Identifier: not resolved"

    return f"""## Paper

**{item.get('title', '').strip()}**

- Source: {item.get('url') or 'not resolved'}
- Publication/source: {item.get('publication') or item.get('source_system') or 'not resolved'}
{identifier_block}

## Paper Radar provenance

- Radar state: `{item.get('state')}`
- Theme: `{item.get('theme')}`
- Score: {item.get('score')}
- Freshness status: `{item.get('freshness_status', 'unknown')}`
- Earliest known publication/public-release date: {item.get('earliest_known_publication_at') or 'unknown'}
- Discovered in run: {generated_at}

## Editorial decision

This issue is an intake object, not an admission decision.

- add `review:backlog` to admit the paper to the review programme
- add `disposition:deferred` to defer it; the issue will close and may resurface after the configured reconsideration window
- add `disposition:declined` to decline it; the issue will close
- `review:in-progress` marks active review work
- `review:published` is terminal and closes the issue as completed
"""


def desired_labels(existing: dict, new_state_label: str) -> list[str]:
    current = {x.get("name", "") for x in existing.get("labels", []) if isinstance(x, dict)}
    current -= LIFECYCLE_LABELS
    current.add(new_state_label)
    return sorted(x for x in current if x)


def create_issue(repo: str, token: str, item: dict, cfg: dict, generated_at: str):
    intake = cfg.get("issue_intake") or {}
    payload = {
        "title": issue_title(item),
        "body": issue_body(item, generated_at),
        "labels": [intake_label(item, cfg)],
    }
    assignees = intake.get("assignees") or []
    if assignees:
        payload["assignees"] = assignees
    return github_json(f"https://api.github.com/repos/{repo}/issues", token, "POST", payload)


def resurface_deferred(repo: str, token: str, issue: dict, item: dict, cfg: dict):
    label = intake_label(item, cfg)
    payload = {
        "state": "open",
        "labels": desired_labels(issue, label),
    }
    updated = github_json(
        f"https://api.github.com/repos/{repo}/issues/{issue['number']}",
        token,
        "PATCH",
        payload,
    )
    github_json(
        f"https://api.github.com/repos/{repo}/issues/{issue['number']}/comments",
        token,
        "POST",
        {
            "body": (
                "Paper Radar resurfaced this deferred paper after the configured "
                "reconsideration window. It has returned to editorial triage; no review "
                "admission decision has been made automatically."
            )
        },
    )
    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="discovery/radar.json")
    parser.add_argument("--ledger", default="data/paper-candidates.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cfg = json.loads((ROOT / args.config).read_text(encoding="utf-8"))
    intake = cfg.get("issue_intake") or {}
    if not intake.get("enabled", False):
        print("Paper Radar issue intake is disabled")
        return 0

    payload = json.loads((ROOT / args.ledger).read_text(encoding="utf-8"))
    selected = select_items(payload)
    if args.dry_run:
        for item in selected:
            print(f"{intake_label(item, cfg)}\t{item.get('title')}")
        return 0

    token = os.environ.get("GITHUB_TOKEN")
    repo = cfg.get("repository")
    if not token or not repo:
        raise SystemExit("GITHUB_TOKEN and repository configuration are required")

    today = dt.datetime.now(dt.timezone.utc).date()
    existing = load_all_issues(repo, token)
    created = resurfaced = skipped = 0

    for item in selected:
        matches = [issue for issue in existing if same_issue_item(issue, item)]
        suppressing = [issue for issue in matches if radar.issue_should_suppress(issue, cfg, today)]
        if suppressing:
            skipped += 1
            continue

        deferred = [
            issue for issue in matches
            if "disposition:deferred" in radar.issue_label_names(issue)
        ]
        if deferred:
            updated = resurface_deferred(repo, token, deferred[0], item, cfg)
            existing = [updated if x.get("number") == updated.get("number") else x for x in existing]
            resurfaced += 1
            continue

        created_issue = create_issue(repo, token, item, cfg, payload.get("generated_at", "unknown"))
        existing.append(created_issue)
        created += 1

    print(f"Paper Radar intake: created={created}, resurfaced={resurfaced}, skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
