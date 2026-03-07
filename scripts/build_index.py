#!/usr/bin/env python3
"""Build or check generated navigation files for the review archive.

Outputs:
- index.md
- docs/index.md
- README.md recent reviews block

Conventions:
- Reviews live under reviews/YYYY/*.md
- Review files should use the canonical template in templates/review-template.md
"""
from __future__ import annotations

import argparse
import glob
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_GLOB = str(REPO_ROOT / "reviews" / "**" / "*.md")
INDEX_PATH = REPO_ROOT / "index.md"
DOCS_INDEX_PATH = REPO_ROOT / "docs" / "index.md"
README_PATH = REPO_ROOT / "README.md"
README_START = "<!-- RECENT_REVIEWS:START -->"
README_END = "<!-- RECENT_REVIEWS:END -->"

@dataclass(frozen=True)
class ReviewRecord:
    date: str
    title: str
    publication: str
    domain: str
    source: str
    review_path: str


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


def parse_front_matter(md_text: str) -> Dict[str, str]:
    """Parse simple YAML-style front matter.

    Supports files where front matter starts at the top or immediately after a
    leading heading like '# Paper Review'.
    """
    text = md_text.lstrip("\ufeff\n\r\t ")
    m = re.search(r"(?ms)^---\s*\n(.*?)\n---\s*", text)
    if not m:
        return {}

    block = m.group(1).splitlines()
    data: Dict[str, str] = {}
    for line in block:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        data[key] = _strip_quotes(val)
    return data


def load_reviews() -> List[ReviewRecord]:
    records: List[ReviewRecord] = []
    for path_str in glob.glob(REVIEWS_GLOB, recursive=True):
        path = Path(path_str)
        txt = path.read_text(encoding="utf-8")
        fm = parse_front_matter(txt)
        title = fm.get("title", "").strip() or path.stem
        source = fm.get("source", "").strip()
        date = fm.get("date_read", "").strip() or "1970-01-01"
        domain = fm.get("primary_domain", "").strip() or "Uncategorized"
        publication = fm.get("publication", "").strip()

        # legacy fallbacks
        if not source:
            m = re.search(r"\*\*Source URL:\*\*\s*\n?(\S+)", txt)
            source = m.group(1).strip() if m else ""
        if title == path.stem:
            m = re.search(r"\*\*Title:\*\*\s*(.+)", txt)
            if m:
                title = m.group(1).strip()
        if date == "1970-01-01":
            m = re.search(r"\*\*Date Read:\*\*\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", txt)
            if m:
                date = m.group(1)

        review_path = path.relative_to(REPO_ROOT).as_posix()
        records.append(ReviewRecord(date=date, title=title, publication=publication, domain=domain, source=source, review_path=review_path))

    records.sort(key=lambda r: (r.date, r.title.lower()), reverse=True)
    return records


def render_index(records: List[ReviewRecord], link_prefix: str = "") -> str:
    lines = [
        "# Paper Review Index",
        "",
        "A generated index of review notes in this repository.",
        "",
        "| Date | Paper | Publication | Domain | Review | Source |",
        "|------|-------|-------------|--------|--------|--------|",
    ]
    for r in records:
        review_link = f"{link_prefix}{r.review_path}"
        publication = r.publication or "—"
        source_link = f"[Source]({r.source})" if r.source else "—"
        lines.append(f"| {r.date} | {r.title} | {publication} | {r.domain} | [Review]({review_link}) | {source_link} |")
    lines.append("")
    return "\n".join(lines)


def render_recent_reviews(records: List[ReviewRecord], count: int = 8) -> str:
    lines = [README_START, ""]
    for r in records[:count]:
        pub = f" — *{r.publication}*" if r.publication else ""
        lines.append(f"- **{r.date}** — [{r.title}]({r.review_path}){pub}")
    lines.extend(["", README_END])
    return "\n".join(lines)


def update_readme(readme_text: str, recent_block: str) -> str:
    pattern = re.compile(re.escape(README_START) + r".*?" + re.escape(README_END), re.DOTALL)
    if pattern.search(readme_text):
        return pattern.sub(recent_block, readme_text)
    if not readme_text.endswith("\n"):
        readme_text += "\n"
    return readme_text + "\n## Recent Reviews\n\n" + recent_block + "\n"


def compute_outputs(records: List[ReviewRecord]) -> Dict[Path, str]:
    readme_current = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else "# Digital Governance Paper Notes\n"
    recent_block = render_recent_reviews(records)
    return {
        INDEX_PATH: render_index(records),
        DOCS_INDEX_PATH: render_index(records, link_prefix="../"),
        README_PATH: update_readme(readme_current, recent_block),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Fail if generated files are not up to date.")
    args = ap.parse_args()

    records = load_reviews()
    outputs = compute_outputs(records)

    mismatches: List[Path] = []
    for path, new_text in outputs.items():
        old_text = path.read_text(encoding="utf-8") if path.exists() else ""
        if old_text != new_text:
            mismatches.append(path)

    if args.check:
        if mismatches:
            for path in mismatches:
                print(f"Out of date: {path.relative_to(REPO_ROOT)}")
            print("Run: python scripts/build_index.py")
            return 2
        print("Generated files are up to date.")
        return 0

    for path, new_text in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_text, encoding="utf-8")
        print(f"Wrote {path.relative_to(REPO_ROOT)}")
    print(f"Indexed {len(records)} review files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
