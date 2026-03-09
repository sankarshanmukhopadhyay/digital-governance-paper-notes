#!/usr/bin/env python3
"""Build or check generated navigation files for the review archive.

Outputs:
- index.md
- docs/index.html
- README.md recent reviews block

Conventions:
- Reviews live under reviews/YYYY/*.md
- Review files should use canonical YAML front matter at the top of the file
- Review files should use the canonical template in templates/review-template.md
- Taxonomy is defined in taxonomy/domains.yml
"""
from __future__ import annotations

import argparse
import glob
import html
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple


REPO_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_GLOB = str(REPO_ROOT / "reviews" / "**" / "*.md")
INDEX_PATH = REPO_ROOT / "index.md"
DOCS_HTML_PATH = REPO_ROOT / "docs" / "index.html"
README_PATH = REPO_ROOT / "README.md"
TAXONOMY_PATH = REPO_ROOT / "taxonomy" / "domains.yml"

README_START = "<!-- RECENT_REVIEWS:START -->"
README_END = "<!-- RECENT_REVIEWS:END -->"

GITHUB_REPO_BLOB_BASE = (
    "https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/blob/main/"
)

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
class Taxonomy:
    primary_domains: Tuple[str, ...] = ()
    secondary_topics: Tuple[str, ...] = ()
    scholarly_signals: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ReviewRecord:
    date: str
    title: str
    publication: str
    domain: str
    source: str
    review_path: str
    tags: Tuple[str, ...] = field(default_factory=tuple)
    scholarly_signal: str = ""
    key_insight: str = ""


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


def _slugify_anchor(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def parse_simple_yaml_lists(yaml_text: str) -> Dict[str, List[str]]:
    """Parse a very small YAML subset for taxonomy/domains.yml.

    Supported shape:
      key:
        - item
        - item
    Comments and blank lines are ignored.
    """
    data: Dict[str, List[str]] = {}
    current_key = None

    for raw_line in yaml_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        key_match = re.match(r"^([A-Za-z0-9_]+)\s*:\s*$", stripped)
        if key_match:
            current_key = key_match.group(1)
            data.setdefault(current_key, [])
            continue

        item_match = re.match(r"^\s*-\s+(.*)$", line)
        if item_match and current_key:
            data[current_key].append(_strip_quotes(item_match.group(1).strip()))
            continue

    return data


def load_taxonomy() -> Taxonomy:
    if not TAXONOMY_PATH.exists():
        return Taxonomy()

    raw = TAXONOMY_PATH.read_text(encoding="utf-8")
    parsed = parse_simple_yaml_lists(raw)
    return Taxonomy(
        primary_domains=tuple(parsed.get("primary_domains", [])),
        secondary_topics=tuple(parsed.get("secondary_topics", [])),
        scholarly_signals=tuple(parsed.get("scholarly_signals", [])),
    )


def parse_front_matter(md_text: str) -> Dict[str, object]:
    """Parse YAML-style front matter from the top of the file only.

    Supports:
    - key: "value"
    - key: value
    - key:
        - item1
        - item2
    - key: [item1, item2]
    """
    text = md_text.lstrip("\ufeff")
    m = re.match(r"(?ms)^---\s*\n(.*?)\n---\s*", text)
    if not m:
        return {}

    block = m.group(1).splitlines()
    data: Dict[str, object] = {}
    current_list_key = None

    for raw_line in block:
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        list_item_match = re.match(r"^\s*-\s+(.*)$", line)
        if list_item_match and current_list_key:
            data.setdefault(current_list_key, [])
            assert isinstance(data[current_list_key], list)
            data[current_list_key].append(_strip_quotes(list_item_match.group(1).strip()))
            continue

        m_key = re.match(r"^([A-Za-z0-9_]+)\s*:\s*(.*)$", stripped)
        if not m_key:
            continue

        key, val = m_key.group(1), m_key.group(2)
        current_list_key = None

        if val == "":
            data[key] = []
            current_list_key = key
            continue

        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            if inner:
                parts = [_strip_quotes(part.strip()) for part in inner.split(",")]
                data[key] = [p for p in parts if p]
            else:
                data[key] = []
            continue

        data[key] = _strip_quotes(val)

    return data


def validate_review_file(path: Path, txt: str, fm: Dict[str, object], taxonomy: Taxonomy) -> List[str]:
    errors: List[str] = []
    text = txt.lstrip("\ufeff")

    if not re.match(r"(?ms)^---\s*\n.*?\n---\s*", text):
        errors.append("front matter must appear at the top of the file")

    for field in REQUIRED_FRONT_MATTER_FIELDS:
        if field not in fm:
            errors.append(f"missing front matter field: {field}")

    date_read = str(fm.get("date_read", "")).strip()
    if date_read and not re.match(r"^\d{4}-\d{2}-\d{2}$", date_read):
        errors.append("date_read must use YYYY-MM-DD")

    if not re.search(r"(?m)^# Paper Review\s*$", txt):
        errors.append("missing '# Paper Review' heading")
    if not re.search(r"(?m)^## Review\s*$", txt):
        errors.append("missing '## Review' section")
    if not re.search(r"(?m)^## Key Insight\s*$", txt):
        errors.append("missing '## Key Insight' section")

    primary_domain = str(fm.get("primary_domain", "")).strip()
    if taxonomy.primary_domains and primary_domain and primary_domain not in taxonomy.primary_domains:
        errors.append(f"primary_domain not in taxonomy: {primary_domain}")

    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [tags] if tags else []
    if not isinstance(tags, list):
        errors.append("tags must be a YAML list or inline list")
        tags = []

    invalid_tags = [tag for tag in tags if taxonomy.secondary_topics and tag not in taxonomy.secondary_topics]
    if invalid_tags:
        errors.append(f"tags not in taxonomy: {', '.join(invalid_tags)}")

    scholarly_signal = str(fm.get("scholarly_signal", "")).strip()
    if scholarly_signal and taxonomy.scholarly_signals and scholarly_signal not in taxonomy.scholarly_signals:
        errors.append(f"scholarly_signal not in taxonomy: {scholarly_signal}")

    return errors


def load_reviews(taxonomy: Taxonomy) -> List[ReviewRecord]:
    records: List[ReviewRecord] = []
    validation_errors: List[str] = []

    for path_str in glob.glob(REVIEWS_GLOB, recursive=True):
        path = Path(path_str)
        txt = path.read_text(encoding="utf-8")
        fm = parse_front_matter(txt)

        file_errors = validate_review_file(path, txt, fm, taxonomy)
        if file_errors:
            validation_errors.extend(f"{path.relative_to(REPO_ROOT)}: {err}" for err in file_errors)

        title = str(fm.get("title", "")).strip() or path.stem
        source = str(fm.get("source", "")).strip()
        date = str(fm.get("date_read", "")).strip() or "1970-01-01"
        domain = str(fm.get("primary_domain", "")).strip() or "Uncategorized"
        publication = str(fm.get("publication", "")).strip()
        scholarly_signal = str(fm.get("scholarly_signal", "")).strip()
        key_insight = str(fm.get("key_insight", "")).strip()

        tags_raw = fm.get("tags", [])
        if isinstance(tags_raw, str):
            tags = (tags_raw,) if tags_raw else ()
        elif isinstance(tags_raw, list):
            tags = tuple(str(tag).strip() for tag in tags_raw if str(tag).strip())
        else:
            tags = ()

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
        records.append(
            ReviewRecord(
                date=date,
                title=title,
                publication=publication,
                domain=domain,
                source=source,
                review_path=review_path,
                tags=tags,
                scholarly_signal=scholarly_signal,
                key_insight=key_insight,
            )
        )

    if validation_errors:
        raise SystemExit("\n".join(["Review file validation failed:"] + validation_errors))

    records.sort(key=lambda r: (r.date, r.title.lower()), reverse=True)
    return records


def group_by_domain(records: List[ReviewRecord], taxonomy: Taxonomy) -> List[Tuple[str, List[ReviewRecord]]]:
    grouped: Dict[str, List[ReviewRecord]] = defaultdict(list)
    for record in records:
        grouped[record.domain].append(record)

    ordered_domains = list(taxonomy.primary_domains)
    for domain in sorted(grouped.keys()):
        if domain not in ordered_domains:
            ordered_domains.append(domain)

    return [(domain, grouped[domain]) for domain in ordered_domains if grouped.get(domain)]


def render_domain_summary(records: List[ReviewRecord], taxonomy: Taxonomy) -> List[str]:
    grouped = group_by_domain(records, taxonomy)
    lines = ["## Browse by Domain", ""]
    for domain, items in grouped:
        anchor = _slugify_anchor(domain)
        lines.append(f"- [{domain}](#{anchor}) ({len(items)})")
    lines.append("")
    return lines


def render_grouped_sections(records: List[ReviewRecord], taxonomy: Taxonomy, link_prefix: str = "") -> List[str]:
    grouped = group_by_domain(records, taxonomy)
    lines: List[str] = ["## Reviews by Domain", ""]

    for domain, items in grouped:
        anchor = _slugify_anchor(domain)
        lines.append(f"## {domain}")
        lines.append(f"<a id=\"{anchor}\"></a>")
        lines.append("")
        for r in items:
            review_link = f"{link_prefix}{r.review_path}"
            publication = f" — *{r.publication}*" if r.publication else ""
            source = f" — [Source]({r.source})" if r.source else ""
            signal = f" — `{r.scholarly_signal}`" if r.scholarly_signal else ""
            lines.append(f"- **{r.date}** — [{r.title}]({review_link}){publication}{signal}{source}")
            if r.key_insight:
                lines.append(f"  - {r.key_insight}")
        lines.append("")

    return lines


def render_index(records: List[ReviewRecord], taxonomy: Taxonomy, link_prefix: str = "") -> str:
    lines = [
        "# Paper Review Index",
        "",
        "A generated index of review notes in this repository.",
        "",
    ]

    lines.extend(render_domain_summary(records, taxonomy))

    lines.extend(
        [
            "## Master Table",
            "",
            "| Date | Paper | Publication | Domain | Review | Source |",
            "|------|-------|-------------|--------|--------|--------|",
        ]
    )

    for r in records:
        review_link = f"{link_prefix}{r.review_path}"
        publication = r.publication or "—"
        source_link = f"[Source]({r.source})" if r.source else "—"
        lines.append(
            f"| {r.date} | {r.title} | {publication} | {r.domain} | [Review]({review_link}) | {source_link} |"
        )

    lines.append("")
    lines.extend(render_grouped_sections(records, taxonomy, link_prefix))
    return "\n".join(lines)


def render_recent_reviews(records: List[ReviewRecord], count: int = 8) -> str:
    lines = [README_START, ""]
    for r in records[:count]:
        pub = f" — *{r.publication}*" if r.publication else ""
        lines.append(f"- **{r.date}** — [{r.title}]({r.review_path}){pub}")
    lines.extend(["", README_END])
    return "\n".join(lines)


def update_readme(readme_text: str, recent_block: str, taxonomy: Taxonomy, records: List[ReviewRecord]) -> str:
    pattern = re.compile(re.escape(README_START) + r".*?" + re.escape(README_END), re.DOTALL)
    updated = (
        pattern.sub(recent_block, readme_text)
        if pattern.search(readme_text)
        else readme_text.rstrip() + "\n\n## Recent Reviews\n\n" + recent_block + "\n"
    )

    taxonomy_block_start = "<!-- TAXONOMY_SUMMARY:START -->"
    taxonomy_block_end = "<!-- TAXONOMY_SUMMARY:END -->"

    grouped = group_by_domain(records, taxonomy)
    taxonomy_lines = [taxonomy_block_start, ""]
    for domain, items in grouped:
        taxonomy_lines.append(f"- **{domain}** ({len(items)})")
    taxonomy_lines.extend(["", taxonomy_block_end])
    taxonomy_block = "\n".join(taxonomy_lines)

    taxonomy_pattern = re.compile(
        re.escape(taxonomy_block_start) + r".*?" + re.escape(taxonomy_block_end),
        re.DOTALL,
    )

    if taxonomy_pattern.search(updated):
        updated = taxonomy_pattern.sub(taxonomy_block, updated)
    else:
        insert_after = "## Scope"
        if insert_after in updated:
            updated = updated.replace(
                insert_after,
                insert_after + "\n\n### Taxonomy Snapshot\n\n" + taxonomy_block,
                1,
            )
        else:
            updated = updated.rstrip() + "\n\n## Taxonomy Snapshot\n\n" + taxonomy_block + "\n"

    return updated


def render_docs_html(records: List[ReviewRecord], taxonomy: Taxonomy) -> str:
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

    grouped = group_by_domain(records, taxonomy)
    domain_badges = "\n".join(
        f'<span class="pill">{html.escape(domain)} ({len(items)})</span>'
        for domain, items in grouped
    )

    rows_html = "\n".join(rows)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Digital Governance Paper Notes</title>
  <meta name="description" content="Practitioner-oriented review archive on AI governance, digital public infrastructure, and public-interest technology.">
  <style>
    :root {{ color-scheme: light dark; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #0b1020; color: #e8ecf4; }}
    main {{ max-width: 1200px; margin: 0 auto; padding: 2rem 1rem 4rem; }}
    h1 {{ margin: 0 0 .5rem; font-size: 2rem; }}
    h2 {{ margin-top: 2rem; }}
    p {{ line-height: 1.6; color: #cfd7e6; }}
    a {{ color: #8cc8ff; }}
    .card {{ background: #121a2f; border: 1px solid #23304f; border-radius: 14px; padding: 1rem; margin-top: 1rem; overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 840px; }}
    th, td {{ text-align: left; padding: .75rem; border-bottom: 1px solid #23304f; vertical-align: top; }}
    th {{ font-size: .9rem; color: #9fb0cf; }}
    .meta {{ display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem; color: #9fb0cf; font-size: .95rem; }}
    .pill {{ background: #18233f; border: 1px solid #23304f; border-radius: 999px; padding: .35rem .75rem; }}
    .domain-grid {{ display: flex; gap: .5rem; flex-wrap: wrap; margin-top: 1rem; }}
  </style>
</head>
<body>
  <main>
    <h1>Digital Governance Paper Notes</h1>
    <p>A curated archive of short, practitioner-oriented reviews covering AI governance, regulation, digital public infrastructure, digital identity, and adjacent socio-technical systems.</p>
    <div class="meta">
      <span class="pill">{len(records)} reviews indexed</span>
      <span class="pill"><a href="https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes" target="_blank" rel="noopener noreferrer">Repository</a></span>
      <span class="pill"><a href="{html.escape((GITHUB_REPO_BLOB_BASE + 'index.md'), quote=True)}" target="_blank" rel="noopener noreferrer">Markdown index</a></span>
    </div>
    <h2>Browse by Domain</h2>
    <div class="domain-grid">
      {domain_badges}
    </div>
    <div class="card">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Paper</th>
            <th>Publication</th>
            <th>Domain</th>
            <th>Source</th>
          </tr>
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


def write_or_check(path: Path, new_content: str, check: bool, out_of_date: List[str]) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if existing != new_content:
        if check:
            out_of_date.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(new_content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check whether generated files are up to date")
    args = parser.parse_args()

    taxonomy = load_taxonomy()
    records = load_reviews(taxonomy)

    root_index = render_index(records, taxonomy, link_prefix="")
    docs_html = render_docs_html(records, taxonomy)

    readme_existing = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""
    recent_block = render_recent_reviews(records)
    readme_updated = update_readme(readme_existing, recent_block, taxonomy, records)

    out_of_date: List[str] = []
    write_or_check(INDEX_PATH, root_index, args.check, out_of_date)
    write_or_check(DOCS_HTML_PATH, docs_html, args.check, out_of_date)
    write_or_check(README_PATH, readme_updated, args.check, out_of_date)

    if out_of_date:
        print("Generated files are stale:")
        for path in out_of_date:
            print(f"Out of date: {path}")
        print("Run: python scripts/build_index.py")
        return 2

    if args.check:
        print("Generated files are up to date.")
    else:
        print("Generated files rebuilt successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
