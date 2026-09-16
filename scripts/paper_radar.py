#!/usr/bin/env python3
"""Discover, score, deduplicate, reconcile freshness, and report governance-relevant papers."""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "digital-governance-paper-notes-paper-radar/0.2"


def fetch_json(url: str) -> dict | list:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def norm(s: str) -> str:
    s = html.unescape(s or "").lower()
    s = re.sub(r"https?://(dx\.)?doi\.org/", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def date_only(value: str | None) -> str:
    return (value or "")[:10]


def crossref_date(block: dict | None) -> str:
    parts = (block or {}).get("date-parts", [[None]])[0]
    if not parts or not parts[0]:
        return ""
    return "-".join(str(v).zfill(2) for v in parts)


def phrase_in_text(text: str, phrase: str) -> bool:
    return f" {norm(phrase)} " in f" {text} "


def canonical_key(item: dict) -> str:
    if item.get("doi"):
        return "doi:" + norm(item["doi"])
    if item.get("arxiv_id"):
        return "arxiv:" + item["arxiv_id"].lower()
    return "title:" + norm(item.get("title", ""))


def identity_keys(item: dict) -> set[str]:
    keys = {"title:" + norm(item.get("title", ""))}
    if item.get("doi"):
        keys.add("doi:" + norm(item["doi"]))
    if item.get("arxiv_id"):
        keys.add("arxiv:" + item["arxiv_id"].lower())
    return {k for k in keys if k.split(":", 1)[1]}


def extract_refs(text: str, title: str | None = None) -> tuple[set[str], list[str]]:
    keys, titles = set(), []
    if title:
        titles.append(norm(title))
        keys.add("title:" + norm(title))
    for doi in re.findall(r'(?:doi\.org/)?(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)', text, re.I):
        keys.add("doi:" + norm(doi.rstrip(".,)>]")))
    for aid in re.findall(r'arxiv(?:\.org/(?:abs|pdf)/|:)(\d{4}\.\d{4,5})', text, re.I):
        keys.add("arxiv:" + aid.lower())
    return keys, titles


def load_existing_reviews() -> tuple[set[str], list[str]]:
    keys, titles = set(), []
    for p in ROOT.glob("reviews/**/*.md"):
        text = p.read_text(encoding="utf-8")
        m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', text, re.M)
        title = m.group(1).strip() if m else None
        k, t = extract_refs(text, title)
        keys |= k
        titles += t
    return keys, titles


def issue_paper_title(issue_title: str) -> str:
    if ": " in issue_title and issue_title.startswith("review("):
        return issue_title.split(": ", 1)[1]
    return issue_title


def load_existing_issues(repo: str) -> tuple[set[str], list[str], list[str]]:
    keys, titles, errors = set(), [], []
    if not repo:
        return keys, titles, errors
    try:
        page = 1
        while page <= 3:
            url = f"https://api.github.com/repos/{repo}/issues?state=open&per_page=100&page={page}"
            data = fetch_json(url)
            if not isinstance(data, list) or not data:
                break
            for issue in data:
                if issue.get("pull_request"):
                    continue
                k, t = extract_refs(issue.get("body") or "", issue_paper_title(issue.get("title") or ""))
                keys |= k
                titles += t
            if len(data) < 100:
                break
            page += 1
    except Exception as e:
        errors.append(f"issue-queue lookup failed: {e}")
    return keys, titles, errors


def source_dates(**kwargs: str) -> dict:
    return {k: date_only(v) for k, v in kwargs.items() if date_only(v)}


def crossref(query: str, start: str, rows: int) -> list[dict]:
    params = urllib.parse.urlencode({
        "query.bibliographic": query,
        "filter": f"from-pub-date:{start}",
        "rows": rows,
        "select": "DOI,title,abstract,published,created,deposited,indexed,URL,publisher",
    })
    data = fetch_json("https://api.crossref.org/works?" + params)
    out = []
    for x in data.get("message", {}).get("items", []):
        title = " ".join(x.get("title", [])).strip()
        if not title:
            continue
        abstract = re.sub(r"<[^>]+>", " ", x.get("abstract", ""))
        out.append({
            "source_system": "crossref",
            "title": title,
            "abstract": abstract,
            "doi": x.get("DOI"),
            "url": x.get("URL"),
            "publication": x.get("publisher", ""),
            "source_date_semantics": "registered_publication_metadata",
            "source_dates": source_dates(
                published=crossref_date(x.get("published")),
                created=(x.get("created") or {}).get("date-time"),
                deposited=(x.get("deposited") or {}).get("date-time"),
                indexed=(x.get("indexed") or {}).get("date-time"),
            ),
        })
    return out


def openalex(query: str, start: str, rows: int) -> list[dict]:
    params = urllib.parse.urlencode({"search": query, "filter": f"from_publication_date:{start}", "per-page": rows})
    data = fetch_json("https://api.openalex.org/works?" + params)
    out = []
    for x in data.get("results", []):
        title = x.get("title") or ""
        if not title:
            continue
        words = [(i, w) for w, pos in (x.get("abstract_inverted_index") or {}).items() for i in pos]
        doi = (x.get("doi") or "").replace("https://doi.org/", "") or None
        out.append({
            "source_system": "openalex",
            "title": title,
            "abstract": " ".join(w for _, w in sorted(words)),
            "doi": doi,
            "url": (x.get("primary_location") or {}).get("landing_page_url") or x.get("id"),
            "publication": ((x.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
            "source_date_semantics": "index_publication_metadata",
            "source_dates": source_dates(
                published=x.get("publication_date"),
                indexed=x.get("updated_date"),
                observed=x.get("created_date"),
            ),
        })
    return out


def arxiv(query: str, rows: int) -> list[dict]:
    params = urllib.parse.urlencode({"search_query": "all:" + query, "start": 0, "max_results": rows, "sortBy": "submittedDate", "sortOrder": "descending"})
    root = ET.fromstring(fetch_text("https://export.arxiv.org/api/query?" + params))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in root.findall("a:entry", ns):
        url = e.findtext("a:id", "", ns)
        aid = url.rstrip("/").split("/")[-1].split("v")[0]
        out.append({
            "source_system": "arxiv",
            "title": " ".join(e.findtext("a:title", "", ns).split()),
            "abstract": " ".join(e.findtext("a:summary", "", ns).split()),
            "arxiv_id": aid,
            "url": url,
            "publication": "arXiv",
            "source_date_semantics": "repository_submission",
            "source_dates": source_dates(
                published=e.findtext("a:published", "", ns),
                updated=e.findtext("a:updated", "", ns),
            ),
        })
    return out


def source_record(item: dict) -> dict:
    return {
        "source_system": item.get("source_system"),
        "url": item.get("url"),
        "doi": item.get("doi"),
        "arxiv_id": item.get("arxiv_id"),
        "date_semantics": item.get("source_date_semantics", "unknown"),
        "dates": dict(item.get("source_dates") or {}),
    }


def freshness_evidence(records: list[dict]) -> tuple[str, str, list[str]]:
    published = []
    semantics = set()
    for record in records:
        semantics.add(record.get("date_semantics") or "unknown")
        value = date_only((record.get("dates") or {}).get("published"))
        if value:
            published.append(value)
    if not published:
        return "", "unknown", []
    unique = sorted(set(published))
    earliest = unique[0]
    if len(unique) == 1 and semantics <= {"registered_publication_metadata"}:
        return earliest, "verified", unique
    if len(unique) == 1:
        return earliest, "source_consistent", unique
    try:
        dates = [dt.date.fromisoformat(v) for v in unique]
        spread = (max(dates) - min(dates)).days
    except ValueError:
        spread = 9999
    if spread > 31:
        return earliest, "conflicting", unique
    return earliest, "source_consistent", unique


def apply_freshness(item: dict, records: list[dict]) -> dict:
    earliest, status, dates = freshness_evidence(records)
    item["source_records"] = records
    item["earliest_known_publication_at"] = earliest or None
    item["freshness_status"] = status
    item["freshness_dates"] = dates
    if status == "conflicting" and item.get("state") == "candidate":
        item["state"] = "needs_judgment"
        item["freshness_requires_judgment"] = True
    else:
        item["freshness_requires_judgment"] = False
    return item


def score(item: dict, cfg: dict, theme: str, query: str, existing_keys: set[str], existing_titles: list[str]) -> dict:
    title = norm(item.get("title", ""))
    text = norm((item.get("title") or "") + " " + (item.get("abstract") or ""))
    theme_cfg = next(t for t in cfg["themes"] if t["name"] == theme)
    anchors = [a for a in theme_cfg.get("anchors", []) if phrase_in_text(text, a)]
    signals = [s for s in cfg["governance_signals"] if phrase_in_text(text, s)]
    material = [s for s in cfg.get("material_governance_signals", []) if phrase_in_text(text, s)]
    title_signals = [s for s in cfg.get("candidate_title_signals", []) if phrase_in_text(title, s)]
    exclusions = [s for s in cfg["exclusion_signals"] if phrase_in_text(text, s)]
    qterms = [t for t in norm(query).split() if len(t) > 3]
    qmatches = sorted({t for t in qterms if phrase_in_text(text, t)})
    near_existing = any(title and (title == t or (len(title) > 28 and (title in t or t in title))) for t in existing_titles)
    exact_existing = bool(identity_keys(item) & existing_keys)
    points = min(4, len(signals)) + min(2, len(qmatches)) + min(2, len(anchors)) + cfg.get("source_weights", {}).get(item["source_system"], 0)
    if exclusions:
        points -= 4
    if exact_existing or near_existing:
        state = "represented"
    elif not anchors:
        state = "deferred"
    elif points >= cfg["candidate_threshold"] and len(material) >= 2 and title_signals:
        state = "candidate"
    elif points >= cfg["judgment_threshold"] and (material or title_signals):
        state = "needs_judgment"
    else:
        state = "deferred"
    item.update({
        "theme": theme,
        "matched_query": query,
        "theme_anchors": anchors,
        "governance_signals": signals,
        "material_governance_signals": material,
        "candidate_title_signals": title_signals,
        "query_matches": qmatches,
        "exclusion_signals": exclusions,
        "score": points,
        "state": state,
        "already_represented": bool(exact_existing or near_existing),
    })
    return item


def should_merge(a: dict, b: dict) -> bool:
    if identity_keys(a) & identity_keys(b):
        return True
    ta, tb = norm(a.get("title", "")), norm(b.get("title", ""))
    return bool(ta and tb and len(ta) >= 20 and ta == tb)


def merge_group(group: list[dict]) -> dict:
    best = max(group, key=lambda x: x.get("score", 0))
    out = dict(best)
    records = [source_record(x) for x in group]
    out["also_seen_in"] = sorted({x.get("source_system") for x in group if x.get("source_system")} - {out.get("source_system")})
    out["alternate_identifiers"] = sorted({k for x in group for k in identity_keys(x)} - identity_keys(out))
    out["matched_queries"] = sorted({x.get("matched_query") for x in group if x.get("matched_query")})
    out["theme_matches"] = sorted({x.get("theme") for x in group if x.get("theme")})
    return apply_freshness(out, records)


def dedupe(items: list[dict]) -> list[dict]:
    groups: list[list[dict]] = []
    for item in items:
        matches = [i for i, group in enumerate(groups) if any(should_merge(item, member) for member in group)]
        if not matches:
            groups.append([item])
            continue
        target = matches[0]
        groups[target].append(item)
        for idx in reversed(matches[1:]):
            groups[target].extend(groups.pop(idx))
    merged = [merge_group(group) for group in groups]
    return sorted(merged, key=lambda x: (x["state"] not in {"candidate", "needs_judgment"}, -x["score"], x["title"]))


def report_date_line(x: dict) -> str:
    status = x.get("freshness_status", "unknown")
    earliest = x.get("earliest_known_publication_at")
    records = x.get("source_records") or []
    if status == "verified" and earliest:
        return f"- Published: {earliest}"
    visible = []
    for record in records:
        source_date = (record.get("dates") or {}).get("published")
        if source_date:
            visible.append(f"{record.get('source_system')}={source_date} ({record.get('date_semantics')})")
    return f"- Source date: {'; '.join(visible) if visible else 'unknown'}"


def render(items: list[dict], run_date: str) -> str:
    states = ["candidate", "needs_judgment", "deferred", "represented"]
    counts = {s: sum(1 for x in items if x["state"] == s) for s in states}
    lines = [
        f"# Paper Radar — {run_date}", "",
        "This report is a discovery and editorial-triage surface. Scores are diagnostic and do not authorize queue admission.",
        "Freshness is provenance-sensitive: `Published` is used only for verified publication semantics; otherwise source-specific dates are shown.", "",
        "## Summary", "",
        f"- Candidate: {counts['candidate']}",
        f"- Needs judgment: {counts['needs_judgment']}",
        f"- Deferred: {counts['deferred']}",
        f"- Already represented or queued: {counts['represented']}", "",
        "## Candidate papers", "",
    ]
    selected = [x for x in items if x["state"] in {"candidate", "needs_judgment"} and not x["already_represented"]]
    if not selected:
        lines.append("No papers crossed the candidate/judgment thresholds in this run.")
    for x in selected:
        lines += [
            f"### {x['title']}", "",
            f"- State: `{x['state']}`",
            f"- Score: {x['score']}",
            f"- Theme: `{x['theme']}`",
            f"- Source: {x['source_system']}",
            report_date_line(x),
            f"- Freshness status: `{x.get('freshness_status', 'unknown')}`",
            f"- Earliest known publication/public-release date: {x.get('earliest_known_publication_at') or 'unknown'}",
            f"- URL: {x.get('url','')}",
            f"- Theme anchors: {', '.join(x['theme_anchors']) or 'none'}",
            f"- Material governance signals: {', '.join(x['material_governance_signals']) or 'none'}",
            f"- Governance signals: {', '.join(x['governance_signals']) or 'none'}",
            f"- Trigger query: `{x['matched_query']}`", "",
        ]
    return "\n".join(lines) + "\n"


def accept_record(item: dict, start: str, today_s: str) -> bool:
    dates = item.get("source_dates") or {}
    source_date = date_only(dates.get("published") or dates.get("indexed") or dates.get("observed"))
    return not source_date or start <= source_date <= today_s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="discovery/radar.json")
    ap.add_argument("--output", default="data/paper-candidates.json")
    ap.add_argument("--report", default=None)
    args = ap.parse_args()
    cfg = json.loads((ROOT / args.config).read_text(encoding="utf-8"))
    now = dt.datetime.now(dt.timezone.utc)
    today = now.date()
    today_s = today.isoformat()
    start = (today - dt.timedelta(days=cfg["lookback_days"])).isoformat()

    existing_keys, existing_titles = load_existing_reviews()
    issue_keys, issue_titles, issue_errors = load_existing_issues(cfg.get("repository", ""))
    existing_keys |= issue_keys
    existing_titles += issue_titles

    parallel_jobs, crossref_jobs = [], []
    for theme in cfg["themes"]:
        for query in theme["queries"]:
            parallel_jobs += [
                ("openalex", theme["name"], query, lambda q=query: openalex(q, start, cfg["max_per_source"])),
                ("arxiv", theme["name"], query, lambda q=query: arxiv(q, min(20, cfg["max_per_source"]))),
            ]
            crossref_jobs.append(("crossref", theme["name"], query, lambda q=query: crossref(q, start, cfg["max_per_source"])))

    found, errors = [], [{"source": "github-issues", "error": e} for e in issue_errors]

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fn): (name, theme, query) for name, theme, query, fn in parallel_jobs}
        for future in concurrent.futures.as_completed(futures):
            name, theme, query = futures[future]
            try:
                for item in future.result():
                    item["discovered_at"] = now.isoformat()
                    if accept_record(item, start, today_s):
                        found.append(score(item, cfg, theme, query, existing_keys, existing_titles))
            except Exception as e:
                errors.append({"source": name, "theme": theme, "query": query, "error": str(e)})

    for name, theme, query, fn in crossref_jobs:
        try:
            for item in fn():
                item["discovered_at"] = now.isoformat()
                if accept_record(item, start, today_s):
                    found.append(score(item, cfg, theme, query, existing_keys, existing_titles))
        except Exception as e:
            errors.append({"source": name, "theme": theme, "query": query, "error": str(e)})
        time.sleep(0.6)

    items = dedupe(found)
    payload = {
        "schema_version": 2,
        "generated_at": now.isoformat(),
        "lookback_start": start,
        "source_errors": errors,
        "items": items,
    }
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_path = ROOT / (args.report or f"reports/radar/{today_s}.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render(items, today_s), encoding="utf-8")
    print(f"wrote {len(items)} deduplicated records; {len(errors)} source errors")
    if errors and not found:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
