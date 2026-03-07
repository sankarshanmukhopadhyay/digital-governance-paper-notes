#!/usr/bin/env python3
"""Build or check generated navigation files for the review archive.

Outputs:
- index.md
- docs/index.md
- docs/index.html
- README.md recent reviews block

Conventions:
- Reviews live under reviews/YYYY/*.md
- Review files should use canonical YAML front matter at the top of the file
- Review files should use the canonical template in templates/review-template.md
"""
from __future__ import annotations

import argparse
import glob
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_GLOB = str(REPO_ROOT / "reviews" / "**" / "*.md")
INDEX_PATH = REPO_ROOT / "index.md"
DOCS_INDEX_PATH = REPO_ROOT / "docs" / "index.md"
DOCS_HTML_PATH = REPO_ROOT / "docs" / "index.html"
README_PATH = REPO_ROOT / "README.md"
README_START = "<!-- RECENT_REVIEWS:START -->"
README_END = "<!-- RECENT_REVIEWS:END -->"
GITHUB_REPO_BLOB_BASE = "https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/blob/main/"
REQUIRED_FRONT_MATTER_FIELDS = [
    "title",
    "source",
    "publication",
    "date_read",
    "primary_domain",
    "tags",
    "key_insight",
]


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
    """Parse simple YAML-style front matter from the top of the file only."""
    text = md_text.lstrip("\ufeff")
    m = re.match(r"(?ms)^---\s*\n(.*?)\n---\s*", text)
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


def validate_review_file(path: Path, txt: str, fm: Dict[str, str]) -> List[str]:
    errors: List[str] = []
    text = txt.lstrip("\ufeff")
    if not re.match(r"(?ms)^---\s*\n.*?\n---\s*", text):
        errors.append("front matter must appear at the top of the file")
    for field in REQUIRED_FRONT_MATTER_FIELDS:
        if field not in fm:
            errors.append(f"missing front matter field: {field}")
    if "date_read" in fm and not re.match(r"^\d{4}-\d{2}-\d{2}$", fm["date_read"]):
        errors.append("date_read must use YYYY-MM-DD")
    if not re.search(r"(?m)^# Paper Review\s*$", txt):
        errors.append("missing '# Paper Review' heading")
    if not re.search(r"(?m)^## Review\s*$", txt):
        errors.append("missing '## Review' section")
    if not re.search(r"(?m)^## Key Insight\s*$", txt):
        errors.append("missing '## Key Insight' section")
    return errors


def load_reviews() -> List[ReviewRecord]:
    records: List[ReviewRecord] = []
    validation_errors: List[str] = []
    for path_str in glob.glob(REVIEWS_GLOB, recursive=True):
        path = Path(path_str)
        txt = path.read_text(encoding="utf-8")
        fm = parse_front_matter(txt)
        file_errors = validate_review_file(path, txt, fm)
        if file_errors:
            validation_errors.extend(f"{path.relative_to(REPO_ROOT)}: {err}" for err in file_errors)

        title = fm.get("title", "").strip() or path.stem
        source = fm.get("source", "").strip()
        date = fm.get("date_read", "").strip() or "1970-01-01"
        domain = fm.get("primary_domain", "").strip() or "Uncategorized"
        publication = fm.get("publication", "").strip()

        # legacy fallbacks for any old files that may still appear later
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
        records.append(
            ReviewRecord(
                date=date,
                title=title,
                publication=publication,
                domain=domain,
                source=source,
                review_path=review_path,
            )
        )

    if validation_errors:
        raise SystemExit("\n".join(["Review file validation failed:"] + validation_errors))

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
        lines.append(
            f"| {r.date} | {r.title} | {publication} | {r.domain} | [Review]({review_link}) | {source_link} |"
        )
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


def render_docs_html(records: List[ReviewRecord]) -> str:
    rows = []
    for r in records:
        source_html = (
            f'<a href="{html.escape(r.source, quote=True)}" target="_blank" rel="noopener noreferrer">Source</a>'
            if r.source else "—"
        )
        review_href = html.escape(GITHUB_REPO_BLOB_BASE + r.review_path, quote=True)
        rows.append(
            "<tr>"
            f"<td>{html.escape(r.date)}</td>"
            f"<td><a href=\"{review_href}\" target=\"_blank\" rel=\"noopener noreferrer\">{html.escape(r.title)}</a></td>"
            f"<td>{html.escape(r.publication or '—')}</td>"
            f"<td>{html.escape(r.domain)}</td>"
            f"<td>{source_html}</td>"
            "</tr>"
        )
    rows_html = "\n".join(rows)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Digital Governance Paper Notes</title>
  <meta name=\"description\" content=\"Practitioner-oriented review archive on AI governance, digital public infrastructure, and public-interest technology.\">
  <style>
    :root {{ color-scheme: light dark; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #0b1020; color: #e8ecf4; }}
    main {{ max-width: 1200px; margin: 0 auto; padding: 2rem 1rem 4rem; }}
    h1 {{ margin: 0 0 .5rem; font-size: 2rem; }}
    p {{ line-height: 1.6; color: #cfd7e6; }}
    a {{ color: #8cc8ff; }}
    .card {{ background: #121a2f; border: 1px solid #23304f; border-radius: 14px; padding: 1rem; margin-top: 1rem; overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 840px; }}
    th, td {{ text-align: left; padding: .75rem; border-bottom: 1px solid #23304f; vertical-align: top; }}
    th {{ font-size: .9rem; color: #9fb0cf; }}
    .meta {{ display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem; color: #9fb0cf; font-size: .95rem; }}
    .pill {{ background: #18233f; border: 1px solid #23304f; border-radius: 999px; padding: .35rem .75rem; }}
  </style>
</head>
<body>
  <main>
    <h1>Digital Governance Paper Notes</h1>
    <p>A curated archive of short, practitioner-oriented reviews covering AI governance, regulation, digital public infrastructure, digital identity, and adjacent socio-technical systems.</p>
    <div class=\"meta\">
      <span class=\"pill\">{len(records)} reviews indexed</span>
      <span class=\"pill\"><a href=\"https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes\" target=\"_blank\" rel=\"noopener noreferrer\">Repository</a></span>
      <span class=\"pill\"><a href=\"{html.escape((GITHUB_REPO_BLOB_BASE + 'index.md'), quote=True)}\" target=\"_blank\" rel=\"noopener noreferrer\">Markdown index</a></span>
    </div>
    <div class=\"card\">
      <table>
        <thead>
          <tr><th>Date</th><th>Paper</th><th>Publication</th><th>Domain</th><th>Source</th></tr>
        </thead>
        <tbody>
          {rows_html}
        </tbody>
      </table>
    </div>
  </main>
</body>
</html>
"""


def compute_outputs(records: List[ReviewRecord]) -> Dict[Path, str]:
    readme_current = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else "# Digital Governance Paper Notes\n"
    recent_block = render_recent_reviews(records)
    return {
        INDEX_PATH: render_index(records),
        DOCS_INDEX_PATH: render_index(records, link_prefix="../"),
        DOCS_HTML_PATH: render_docs_html(records),
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
