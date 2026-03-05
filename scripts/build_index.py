#!/usr/bin/env python3
"""
Build (or check) the top-level index.md from review markdown files.

Conventions:
- Reviews live under reviews/YYYY/*.md
- Each review SHOULD start with YAML-like front matter between '---' lines.
  Required keys:
    - title
    - source
    - date_read (YYYY-MM-DD)
    - primary_domain

This script is intentionally dependency-free (stdlib only).
"""
from __future__ import annotations

import argparse
import glob
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REVIEWS_GLOB = os.path.join(REPO_ROOT, "reviews", "**", "*.md")
INDEX_PATH = os.path.join(REPO_ROOT, "index.md")

@dataclass(frozen=True)
class ReviewRecord:
    date: str
    title: str
    domain: str
    link: str
    path: str

def _strip_quotes(v: str) -> str:
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v

def parse_front_matter(md_text: str) -> Dict[str, str]:
    """
    Parse a minimal YAML-ish front matter. We only need simple scalars.
    """
    md_text = md_text.lstrip()
    if not md_text.startswith("---\n"):
        return {}
    parts = md_text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    block = parts[0].splitlines()[1:]  # skip first ---
    data: Dict[str, str] = {}
    for line in block:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # key: value
        m = re.match(r"^([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        data[key] = _strip_quotes(val)
    return data

def load_reviews() -> List[ReviewRecord]:
    records: List[ReviewRecord] = []
    for path in glob.glob(REVIEWS_GLOB, recursive=True):
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        fm = parse_front_matter(txt)
        title = fm.get("title", "").strip()
        link = fm.get("source", "").strip()
        date = fm.get("date_read", "").strip()
        domain = fm.get("primary_domain", "").strip()

        # fallback: try to extract from body in legacy template form
        if not title:
            m = re.search(r"\*\*Title:\*\*\s*(.+)", txt)
            title = m.group(1).strip() if m else os.path.basename(path)
        if not link:
            m = re.search(r"\*\*Source URL:\*\*\s*\n?(\S+)", txt)
            link = m.group(1).strip() if m else ""
        if not date:
            m = re.search(r"\*\*Date Read:\*\*\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", txt)
            date = m.group(1) if m else "1970-01-01"
        if not domain:
            domain = "Uncategorized"

        records.append(ReviewRecord(date=date, title=title, domain=domain, link=link, path=path))

    # sort newest first, then title
    records.sort(key=lambda r: (r.date, r.title.lower()), reverse=True)
    return records

def render_index(records: List[ReviewRecord]) -> str:
    lines = [
        "# Paper Review Index",
        "",
        "| Date | Paper | Domain | Link |",
        "|------|------|--------|------|",
    ]
    for r in records:
        lines.append(f"| {r.date} | {r.title} | {r.domain} | {r.link} |")
    lines.append("")
    return "\n".join(lines)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Fail if index.md is not up to date.")
    args = ap.parse_args()

    records = load_reviews()
    new_index = render_index(records)

    old_index = ""
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            old_index = f.read()

    if args.check:
        if old_index != new_index:
            print("index.md is out of date. Run: python scripts/build_index.py")
            return 2
        print("index.md is up to date.")
        return 0

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(new_index)
    print(f"Wrote {INDEX_PATH} ({len(records)} entries).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
