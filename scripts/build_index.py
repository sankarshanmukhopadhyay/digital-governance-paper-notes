#!/usr/bin/env python3
"""Generate and validate the Digital Governance Paper Notes discovery site.

The site is intentionally static. Every page is derived from review front matter,
the domain taxonomy and curated collection rules, so adding a paper only requires
adding a valid review file and running this script.
"""
from __future__ import annotations

import argparse
import glob
import html
import json
import re
import shutil
import textwrap
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_GLOB = str(REPO_ROOT / "reviews" / "**" / "*.md")
INDEX_PATH = REPO_ROOT / "index.md"
ROOT_HTML_PATH = REPO_ROOT / "index.html"
README_PATH = REPO_ROOT / "README.md"
DOCS_ROOT = REPO_ROOT / "docs"
TAXONOMY_PATH = REPO_ROOT / "taxonomy" / "domains.yml"
COLLECTIONS_PATH = REPO_ROOT / "collections" / "collections.json"
MANIFEST_PATH = DOCS_ROOT / ".generated-files.txt"
README_START = "<!-- RECENT_REVIEWS:START -->"
README_END = "<!-- RECENT_REVIEWS:END -->"

REQUIRED_FRONT_MATTER_FIELDS = [
    "title", "source", "publication", "date_read", "primary_domain", "tags", "key_insight"
]

DOMAIN_DESCRIPTIONS = {
    "AI Governance": "Institutional authority, accountability, deployment controls and the allocation of AI-related risk.",
    "AI Safety & Evaluation": "Evaluation regimes, assurance evidence, model behaviour and the limits of technical safety claims.",
    "Digital Public Infrastructure": "Shared digital rails, public purpose, state capacity and the governance of essential infrastructure.",
    "Digital Public Goods": "Open digital components, stewardship, reuse and the institutional conditions that sustain public value.",
    "Public Sector Digital Strategy": "Government technology strategy, procurement, capability and public-sector transformation.",
    "Digital Identity": "Identity systems, recognition, inclusion and the allocation of rights through digital credentials.",
    "Trust Infrastructure": "Registries, attestations, assurance and the infrastructure through which trust claims become actionable.",
    "Standards, Protocols & Interoperability": "Technical coordination mechanisms and the governance choices embedded in interoperability.",
    "Privacy & Data Protection": "Data rights, surveillance, anonymisation and institutional duties over personal information.",
    "Cybersecurity & Resilience": "Adversarial risk, operational continuity and the capacity to withstand or recover from failure.",
    "Law, Regulation & Liability": "Legal authority, enforceability, liability allocation and pathways to remedy.",
    "Platform Governance & Internet Governance": "Control over platforms, networks, online institutions and their rule-making power.",
    "Socio-technical Systems": "How technology, incentives and institutions jointly redistribute control, labour and legitimacy.",
    "Inclusion, Rights & Development": "Distributional effects, participation, access, dignity and development outcomes.",
    "State Capacity & Administrative Systems": "Administrative capability, institutional memory and the machinery of public authority.",
    "Economic & Market Infrastructure": "Market rules, transaction systems, labour arrangements and the infrastructure of economic coordination.",
}


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
    slug: str
    tags: Tuple[str, ...] = field(default_factory=tuple)
    scholarly_signal: str = ""
    key_insight: str = ""
    markdown_body: str = ""

    @property
    def year(self) -> str:
        return self.date[:4]

    @property
    def html_path(self) -> str:
        return f"reviews/{self.year}/{self.slug}/index.html"

    @property
    def html_url(self) -> str:
        return f"reviews/{self.year}/{self.slug}/"


@dataclass(frozen=True)
class Collection:
    title: str
    slug: str
    description: str
    domains: Tuple[str, ...] = ()
    any_tags: Tuple[str, ...] = ()
    all_tags: Tuple[str, ...] = ()
    max_items: int = 12


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in {'"', "'"}:
        return v[1:-1]
    return v


def _clean_scalar(value: str) -> str:
    return _strip_quotes(textwrap.dedent(value).strip())


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


def _derive_slug_from_path(path: Path) -> str:
    match = re.match(r"^\d{4}-\d{2}-\d{2}__(.+)__v\d+\.md$", path.name)
    return match.group(1) if match else path.stem


def parse_simple_yaml_lists(yaml_text: str) -> Dict[str, List[str]]:
    data: Dict[str, List[str]] = {}
    current_key = None
    for raw in yaml_text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key = re.match(r"^([A-Za-z0-9_]+)\s*:\s*$", stripped)
        if key:
            current_key = key.group(1)
            data.setdefault(current_key, [])
            continue
        item = re.match(r"^\s*-\s+(.*)$", raw)
        if item and current_key:
            data[current_key].append(_strip_quotes(item.group(1).strip()))
    return data


def load_taxonomy() -> Taxonomy:
    parsed = parse_simple_yaml_lists(TAXONOMY_PATH.read_text(encoding="utf-8"))
    return Taxonomy(
        tuple(parsed.get("primary_domains", [])),
        tuple(parsed.get("secondary_topics", [])),
        tuple(parsed.get("scholarly_signals", [])),
    )


def load_collections() -> List[Collection]:
    if not COLLECTIONS_PATH.exists():
        return []
    raw = json.loads(COLLECTIONS_PATH.read_text(encoding="utf-8"))
    collections: List[Collection] = []
    seen: set[str] = set()
    for item in raw.get("collections", []):
        slug = str(item.get("slug", "")).strip()
        title = str(item.get("title", "")).strip()
        description = str(item.get("description", "")).strip()
        if not slug or not title or not description:
            raise SystemExit("Collection entries require title, slug and description")
        if slug in seen or slug != _slugify(slug):
            raise SystemExit(f"Invalid or duplicate collection slug: {slug}")
        seen.add(slug)
        collections.append(Collection(
            title=title,
            slug=slug,
            description=description,
            domains=tuple(item.get("domains", [])),
            any_tags=tuple(item.get("any_tags", [])),
            all_tags=tuple(item.get("all_tags", [])),
            max_items=int(item.get("max_items", 12)),
        ))
    return collections


def parse_front_matter(md_text: str) -> Dict[str, object]:
    text = md_text.lstrip("\ufeff")
    match = re.match(r"(?ms)^---\s*\n(.*?)\n---\s*", text)
    if not match:
        return {}
    lines = match.group(1).splitlines()
    data: Dict[str, object] = {}
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        key_match = re.match(r"^([A-Za-z0-9_]+)\s*:\s*(.*)$", stripped)
        if not key_match:
            i += 1
            continue
        key, value = key_match.group(1), key_match.group(2)
        if value in {"|", ">"}:
            block: List[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                block.append(lines[i][2:] if lines[i].startswith("  ") else "")
                i += 1
            joined = "\n".join(block)
            data[key] = _clean_scalar(joined if value == "|" else re.sub(r"\n+", " ", joined))
            continue
        if value == "":
            items: List[str] = []
            j = i + 1
            while j < len(lines):
                item = re.match(r"^\s*-\s+(.*)$", lines[j])
                if item:
                    items.append(_strip_quotes(item.group(1).strip()))
                    j += 1
                    continue
                if not lines[j].strip():
                    j += 1
                    continue
                break
            data[key] = items
            i = j
            continue
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            parts: List[str] = []
            current: List[str] = []
            quote = None
            for ch in inner:
                if ch in {"\"", "'"}:
                    if quote is None:
                        quote = ch
                    elif quote == ch:
                        quote = None
                    current.append(ch)
                elif ch == "," and quote is None:
                    item = _strip_quotes("".join(current).strip())
                    if item:
                        parts.append(item)
                    current = []
                else:
                    current.append(ch)
            tail = _strip_quotes("".join(current).strip())
            if tail:
                parts.append(tail)
            data[key] = parts
        else:
            data[key] = _clean_scalar(value)
        i += 1
    return data


def strip_front_matter(text: str) -> str:
    return re.sub(r"(?ms)^---\s*\n.*?\n---\s*\n?", "", text.lstrip("\ufeff"), count=1)


def _extract_key_insight_from_body(text: str) -> str:
    match = re.search(r"(?ms)^## Key Insight\s*$\n+(.+?)(?:\n## |\Z)", text)
    return " ".join(line.strip() for line in match.group(1).splitlines() if line.strip()) if match else ""


def validate_review_file(path: Path, text: str, fm: Dict[str, object], taxonomy: Taxonomy) -> List[str]:
    errors: List[str] = []
    if not re.match(r"^\d{4}-\d{2}-\d{2}__[a-z0-9\-]+__v\d+\.md$", path.name):
        errors.append("invalid filename; expected YYYY-MM-DD__paper-slug__vN.md")
    for field in REQUIRED_FRONT_MATTER_FIELDS:
        if field not in fm:
            errors.append(f"missing front matter field: {field}")
    date = str(fm.get("date_read", "")).strip()
    if date and not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        errors.append("date_read must use YYYY-MM-DD")
    for heading in ("# Paper Review", "## Review", "## Key Insight"):
        if not re.search(rf"(?m)^{re.escape(heading)}\s*$", text):
            errors.append(f"missing '{heading}' heading")
    domain = str(fm.get("primary_domain", "")).strip()
    if taxonomy.primary_domains and domain not in taxonomy.primary_domains:
        errors.append(f"primary_domain not in taxonomy: {domain}")
    tags = fm.get("tags", [])
    if not isinstance(tags, list):
        errors.append("tags must be a YAML list or inline list")
        tags = []
    invalid = [str(tag) for tag in tags if taxonomy.secondary_topics and str(tag) not in taxonomy.secondary_topics]
    if invalid:
        errors.append(f"tags not in taxonomy: {', '.join(invalid)}")
    if not str(fm.get("key_insight", "")).strip() and not _extract_key_insight_from_body(text):
        errors.append("key insight must be present")
    return errors


def load_reviews(taxonomy: Taxonomy) -> List[ReviewRecord]:
    records: List[ReviewRecord] = []
    errors: List[str] = []
    for path_str in glob.glob(REVIEWS_GLOB, recursive=True):
        path = Path(path_str)
        text = path.read_text(encoding="utf-8")
        fm = parse_front_matter(text)
        errors.extend(f"{path.relative_to(REPO_ROOT)}: {e}" for e in validate_review_file(path, text, fm, taxonomy))
        tags_raw = fm.get("tags", [])
        tags = tuple(str(x).strip() for x in tags_raw) if isinstance(tags_raw, list) else ()
        records.append(ReviewRecord(
            date=str(fm.get("date_read", "1970-01-01")).strip(),
            title=str(fm.get("title", path.stem)).strip(),
            publication=str(fm.get("publication", "")).strip(),
            domain=str(fm.get("primary_domain", "Uncategorized")).strip(),
            source=str(fm.get("source", fm.get("source_url", ""))).strip(),
            review_path=path.relative_to(REPO_ROOT).as_posix(),
            slug=_derive_slug_from_path(path),
            tags=tags,
            scholarly_signal=str(fm.get("scholarly_signal", "")).strip(),
            key_insight=str(fm.get("key_insight", "")).strip() or _extract_key_insight_from_body(text),
            markdown_body=strip_front_matter(text),
        ))
    if errors:
        raise SystemExit("Review file validation failed:\n" + "\n".join(errors))
    records.sort(key=lambda r: (r.date, r.title.lower()), reverse=True)
    return records


def group_by_domain(records: Sequence[ReviewRecord], taxonomy: Taxonomy) -> List[Tuple[str, List[ReviewRecord]]]:
    grouped: Dict[str, List[ReviewRecord]] = defaultdict(list)
    for record in records:
        grouped[record.domain].append(record)
    ordered = list(taxonomy.primary_domains) + sorted(d for d in grouped if d not in taxonomy.primary_domains)
    return [(domain, grouped[domain]) for domain in ordered if grouped.get(domain)]


def collection_records(collection: Collection, records: Sequence[ReviewRecord]) -> List[ReviewRecord]:
    selected: List[ReviewRecord] = []
    for record in records:
        tags = set(record.tags)
        domain_match = not collection.domains or record.domain in collection.domains
        any_match = not collection.any_tags or bool(tags.intersection(collection.any_tags))
        all_match = set(collection.all_tags).issubset(tags)
        if domain_match and any_match and all_match:
            selected.append(record)
    return selected[:collection.max_items]


def relative_prefix(path: str) -> str:
    depth = max(0, len(Path(path).parts) - 1)
    return "../" * depth


def inline_md(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: List[str] = []
    paragraph: List[str] = []
    list_open = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append(f"<p>{inline_md(' '.join(x.strip() for x in paragraph))}</p>")
            paragraph = []

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush_paragraph()
            if list_open:
                out.append("</ul>")
                list_open = False
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            if list_open:
                out.append("</ul>")
                list_open = False
            level = len(heading.group(1))
            title = heading.group(2)
            if title == "Paper Review":
                continue
            out.append(f'<h{level} id="{_slugify(title)}">{inline_md(title)}</h{level}>')
            continue
        bullet = re.match(r"^\s*-\s+(.+)$", line)
        if bullet:
            flush_paragraph()
            if not list_open:
                out.append("<ul>")
                list_open = True
            out.append(f"<li>{inline_md(bullet.group(1))}</li>")
            continue
        if line.startswith(">"):
            flush_paragraph()
            out.append(f"<blockquote>{inline_md(line.lstrip('> ').strip())}</blockquote>")
            continue
        paragraph.append(line)
    flush_paragraph()
    if list_open:
        out.append("</ul>")
    return "\n".join(out)


def page_shell(title: str, body: str, path: str, description: str = "") -> str:
    prefix = relative_prefix(path)
    desc = description or "Governance-first reviews of research on digital institutions, infrastructure and power."
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | Digital Governance Paper Notes</title>
  <meta name="description" content="{html.escape(desc, quote=True)}">
  <link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="site-title" href="{prefix}">Digital Governance Paper Notes</a>
      <nav aria-label="Primary navigation">
        <a href="{prefix}#recent">Recent</a>
        <a href="{prefix}domains/">Domains</a>
        <a href="{prefix}collections/">Collections</a>
        <a href="{prefix}archive/">Archive</a>
      </nav>
    </div>
  </header>
  <main id="main" class="container">{body}</main>
  <footer class="site-footer"><div class="container">A static, governance-first research index generated from repository metadata.</div></footer>
</body>
</html>
"""



def external_source_html(source: str, label: str = "Original paper") -> str:
    source = source.strip()
    if re.match(r"^https?://", source):
        return f'<a href="{html.escape(source, quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(label)}</a>'
    return html.escape(source) if source else ""

def review_card(record: ReviewRecord, prefix: str = "") -> str:
    source = external_source_html(record.source)
    return f"""<article class="review-card">
  <div class="eyebrow">{html.escape(record.domain)} · {html.escape(record.date)}</div>
  <h3><a href="{prefix}{record.html_url}">{html.escape(record.title)}</a></h3>
  <div class="publication">{html.escape(record.publication or 'Publication not specified')}</div>
  <p>{html.escape(record.key_insight)}</p>
  <div class="card-actions"><a href="{prefix}{record.html_url}">Read review</a>{source and ' · ' + source}</div>
</article>"""


def render_home(records: List[ReviewRecord], taxonomy: Taxonomy, collections: List[Collection]) -> str:
    grouped = group_by_domain(records, taxonomy)
    latest_date = records[0].date if records else ""
    recent = "\n".join(review_card(r) for r in records[:8])
    domain_cards = "\n".join(
        f'''<article class="domain-card"><div class="count">{len(items)} reviews</div><h3><a href="domains/{_slugify(domain)}/">{html.escape(domain)}</a></h3><p>{html.escape(DOMAIN_DESCRIPTIONS.get(domain, 'Governance-focused reviews in this domain.'))}</p><a href="domains/{_slugify(domain)}/">Explore domain</a></article>'''
        for domain, items in grouped
    )
    collection_cards = []
    for collection in collections:
        count = len(collection_records(collection, records))
        if count:
            collection_cards.append(f'''<article class="collection-card"><div class="count">{count} selected reviews</div><h3><a href="collections/{collection.slug}/">{html.escape(collection.title)}</a></h3><p>{html.escape(collection.description)}</p><a href="collections/{collection.slug}/">Open collection</a></article>''')
    body = f"""
<section class="hero">
  <div class="eyebrow">Governance analysis, not literature summary</div>
  <h1>Research notes on how digital systems redistribute authority, legitimacy and control.</h1>
  <p class="lede">The archive reviews papers on AI, digital identity, public infrastructure, regulation and socio-technical systems. Each review extracts the institutional mechanism: who gains decision rights, which safeguards are operational, and where enforcement, revocation or redress remain absent.</p>
  <div class="hero-actions"><a class="button" href="#recent">Browse recent reviews</a><a class="button secondary" href="domains/">Explore domains</a><a class="button secondary" href="archive/">Complete archive</a></div>
  <div class="metrics"><span><strong>{len(records)}</strong> reviews</span><span><strong>{len(grouped)}</strong> domains</span><span>Updated <strong>{html.escape(latest_date)}</strong></span></div>
</section>
<section><div class="section-heading"><div><div class="eyebrow">Guided entry points</div><h2>Start with a governance question</h2></div><a href="collections/">View all collections</a></div><div class="card-grid collection-grid">{''.join(collection_cards[:6])}</div></section>
<section id="recent"><div class="section-heading"><div><div class="eyebrow">Latest additions</div><h2>Recent reviews</h2></div><a href="archive/">Browse the archive</a></div><div class="card-grid review-grid">{recent}</div></section>
<section><div class="section-heading"><div><div class="eyebrow">Repository taxonomy</div><h2>Explore by domain</h2></div><a href="domains/">Domain directory</a></div><div class="card-grid domain-grid">{domain_cards}</div></section>
"""
    return page_shell("Home", body, "index.html")


def render_domains_index(records: List[ReviewRecord], taxonomy: Taxonomy) -> str:
    cards = []
    for domain, items in group_by_domain(records, taxonomy):
        cards.append(f'''<article class="domain-card"><div class="count">{len(items)} reviews · latest {items[0].date}</div><h2><a href="{_slugify(domain)}/">{html.escape(domain)}</a></h2><p>{html.escape(DOMAIN_DESCRIPTIONS.get(domain, 'Governance-focused reviews in this domain.'))}</p><a href="{_slugify(domain)}/">Explore domain</a></article>''')
    body = f'<div class="page-header"><div class="eyebrow">Browse by subject</div><h1>Domain directory</h1><p>Domains classify the principal institutional field addressed by each paper. Collections provide cross-domain routes through recurring governance problems.</p></div><div class="card-grid domain-grid">{"".join(cards)}</div>'
    return page_shell("Domains", body, "domains/index.html")


def render_domain_page(domain: str, items: List[ReviewRecord], collections: List[Collection], records: List[ReviewRecord]) -> str:
    related = [c for c in collections if collection_records(c, items)]
    related_html = "".join(f'<a class="tag-link" href="../../collections/{c.slug}/">{html.escape(c.title)}</a>' for c in related[:5])
    cards = "\n".join(review_card(r, "../../") for r in items)
    path = f"domains/{_slugify(domain)}/index.html"
    body = f'''<div class="breadcrumbs"><a href="../../">Home</a> / <a href="../">Domains</a> / {html.escape(domain)}</div>
<div class="page-header"><div class="eyebrow">{len(items)} reviews</div><h1>{html.escape(domain)}</h1><p>{html.escape(DOMAIN_DESCRIPTIONS.get(domain, 'Governance-focused reviews in this domain.'))}</p>{related_html and '<div class="tag-row">Related collections: ' + related_html + '</div>'}</div>
<div class="card-grid review-grid">{cards}</div>'''
    return page_shell(domain, body, path)


def render_collections_index(collections: List[Collection], records: List[ReviewRecord]) -> str:
    cards = []
    for c in collections:
        count = len(collection_records(c, records))
        if count:
            cards.append(f'''<article class="collection-card"><div class="count">{count} selected reviews</div><h2><a href="{c.slug}/">{html.escape(c.title)}</a></h2><p>{html.escape(c.description)}</p><a href="{c.slug}/">Open collection</a></article>''')
    body = f'<div class="page-header"><div class="eyebrow">Curated pathways</div><h1>Governance collections</h1><p>Collections cut across the formal taxonomy. They group papers around recurring questions of authority, institutional capacity, enforcement, revocation, epistemic integrity and redress.</p></div><div class="card-grid collection-grid">{"".join(cards)}</div>'
    return page_shell("Collections", body, "collections/index.html")


def render_collection_page(collection: Collection, items: List[ReviewRecord]) -> str:
    cards = "\n".join(review_card(r, "../../") for r in items)
    path = f"collections/{collection.slug}/index.html"
    body = f'''<div class="breadcrumbs"><a href="../../">Home</a> / <a href="../">Collections</a> / {html.escape(collection.title)}</div>
<div class="page-header"><div class="eyebrow">{len(items)} selected reviews</div><h1>{html.escape(collection.title)}</h1><p>{html.escape(collection.description)}</p><p class="note">Membership is generated from controlled domain and topic rules, so future reviews appear automatically when their metadata matches this collection.</p></div>
<div class="card-grid review-grid">{cards}</div>'''
    return page_shell(collection.title, body, path)


def related_reviews(current: ReviewRecord, records: Sequence[ReviewRecord], limit: int = 4) -> List[ReviewRecord]:
    scored: List[Tuple[int, str, ReviewRecord]] = []
    current_tags = set(current.tags)
    for candidate in records:
        if candidate.review_path == current.review_path:
            continue
        score = (4 if candidate.domain == current.domain else 0) + len(current_tags.intersection(candidate.tags))
        if score:
            scored.append((score, candidate.date, candidate))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [x[2] for x in scored[:limit]]


def render_review_page(record: ReviewRecord, records: List[ReviewRecord], collections: List[Collection]) -> str:
    index = records.index(record)
    newer = records[index - 1] if index > 0 else None
    older = records[index + 1] if index + 1 < len(records) else None
    related = related_reviews(record, records)
    memberships = [c for c in collections if record in collection_records(c, records)]
    tags = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in record.tags)
    memberships_html = "".join(f'<a class="tag-link" href="../../../collections/{c.slug}/">{html.escape(c.title)}</a>' for c in memberships)
    related_html = "".join(review_card(r, "../../../") for r in related)
    prev_next = '<div class="prev-next">'
    prev_next += f'<a href="../../../{newer.html_url}"><span>Newer review</span>{html.escape(newer.title)}</a>' if newer else '<span></span>'
    prev_next += f'<a class="next" href="../../../{older.html_url}"><span>Older review</span>{html.escape(older.title)}</a>' if older else '<span></span>'
    prev_next += '</div>'
    source = external_source_html(record.source) or "Source unavailable"
    body = f'''<div class="breadcrumbs"><a href="../../../">Home</a> / <a href="../../../domains/">Domains</a> / <a href="../../../domains/{_slugify(record.domain)}/">{html.escape(record.domain)}</a></div>
<article class="review-page">
<header class="review-header"><div class="eyebrow">{html.escape(record.domain)} · {html.escape(record.date)}</div><h1>{html.escape(record.title)}</h1><div class="review-meta"><span>{html.escape(record.publication or 'Publication not specified')}</span><span>{source}</span><span><a href="https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/blob/main/{html.escape(record.review_path, quote=True)}">Markdown source</a></span></div><div class="tag-row">{tags}</div></header>
<section class="key-insight"><div class="eyebrow">Key Insight</div><p>{html.escape(record.key_insight)}</p></section>
<div class="prose">{markdown_to_html(record.markdown_body)}</div>
{memberships_html and '<section class="membership"><h2>Appears in these collections</h2><div class="tag-row">' + memberships_html + '</div></section>'}
{prev_next}
</article>
<section><div class="section-heading"><div><div class="eyebrow">Continue exploring</div><h2>Related reviews</h2></div><a href="../../../domains/{_slugify(record.domain)}/">More in {html.escape(record.domain)}</a></div><div class="card-grid review-grid">{related_html}</div></section>'''
    return page_shell(record.title, body, record.html_path, record.key_insight)


def render_archive(records: List[ReviewRecord]) -> str:
    years: Dict[str, List[ReviewRecord]] = defaultdict(list)
    for r in records:
        years[r.year].append(r)
    nav = "".join(f'<a class="tag-link" href="#{year}">{year} ({len(items)})</a>' for year, items in sorted(years.items(), reverse=True))
    sections = []
    for year, items in sorted(years.items(), reverse=True):
        rows = []
        for r in items:
            source = external_source_html(r.source, "Source") or "—"
            rows.append(f'<tr><td>{html.escape(r.date)}</td><td><a href="../{r.html_url}">{html.escape(r.title)}</a></td><td>{html.escape(r.publication or "—")}</td><td><a href="../domains/{_slugify(r.domain)}/">{html.escape(r.domain)}</a></td><td>{source}</td></tr>')
        sections.append(f'<section id="{year}"><h2>{year}</h2><div class="table-wrap"><table><thead><tr><th>Date</th><th>Paper</th><th>Publication</th><th>Domain</th><th>Source</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>')
    body = f'<div class="page-header"><div class="eyebrow">Complete chronological index</div><h1>Review archive</h1><p>The archive is retained for systematic scanning and auditability. Recent work, domains and curated collections provide the primary guided routes into the repository.</p><div class="tag-row">{nav}</div></div>{"".join(sections)}'
    return page_shell("Archive", body, "archive/index.html")


def render_root_redirect() -> str:
    return """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <meta http-equiv=\"refresh\" content=\"0; url=https://sankarshanmukhopadhyay.github.io/digital-governance-paper-notes/\">
  <link rel=\"canonical\" href=\"https://sankarshanmukhopadhyay.github.io/digital-governance-paper-notes/\">
  <title>Digital Governance Paper Notes</title>
</head>
<body>
  <p><a href=\"https://sankarshanmukhopadhyay.github.io/digital-governance-paper-notes/\">Open the Digital Governance Paper Notes site</a>.</p>
</body>
</html>
"""


def render_markdown_index(records: List[ReviewRecord], taxonomy: Taxonomy) -> str:
    lines = ["# Paper Review Index", "", "A generated repository-native index. The GitHub Pages site provides guided browsing by recency, domain and governance collection.", "", "## Browse by Domain", ""]
    for domain, items in group_by_domain(records, taxonomy):
        lines.append(f"- [{domain}](#{_slugify(domain)}) ({len(items)})")
    lines.extend(["", "## Reviews by Domain", ""])
    for domain, items in group_by_domain(records, taxonomy):
        lines.extend([f"### {domain}", f'<a id="{_slugify(domain)}"></a>', ""])
        for r in items:
            pub = f" — *{r.publication}*" if r.publication else ""
            src = f" — [Source]({r.source})" if r.source else ""
            lines.append(f"- **{r.date}** — [{r.title}]({r.review_path}){pub}{src}")
            lines.append(f"  - {r.key_insight}")
        lines.append("")
    return "\n".join(lines)


def render_recent_reviews(records: List[ReviewRecord], count: int = 8) -> str:
    lines = [README_START, ""]
    for r in records[:count]:
        pub = f" — *{r.publication}*" if r.publication else ""
        lines.append(f"- **{r.date}** — [{r.title}]({r.review_path}){pub}")
    lines.extend(["", README_END])
    return "\n".join(lines)


def update_readme(text: str, records: List[ReviewRecord], taxonomy: Taxonomy) -> str:
    recent = render_recent_reviews(records)
    pattern = re.compile(re.escape(README_START) + r".*?" + re.escape(README_END), re.DOTALL)
    updated = pattern.sub(recent, text) if pattern.search(text) else text.rstrip() + "\n\n## Recent Reviews\n\n" + recent + "\n"
    start, end = "<!-- TAXONOMY_SUMMARY:START -->", "<!-- TAXONOMY_SUMMARY:END -->"
    block = [start, ""] + [f"- **{d}** ({len(items)})" for d, items in group_by_domain(records, taxonomy)] + ["", end]
    taxonomy_block = "\n".join(block)
    tpattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    return tpattern.sub(taxonomy_block, updated) if tpattern.search(updated) else updated.rstrip() + "\n\n## Taxonomy Snapshot\n\n" + taxonomy_block + "\n"


SITE_CSS = r"""
:root{--bg:#f6f7f9;--surface:#fff;--text:#17202a;--muted:#5f6b78;--line:#dfe4ea;--accent:#0d5c63;--accent-dark:#073f45;--highlight:#f2e9d8;--max:1180px}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.65}a{color:var(--accent);text-underline-offset:3px}a:hover{color:var(--accent-dark)}.container{width:min(var(--max),calc(100% - 2rem));margin:auto}.skip-link{position:absolute;left:-9999px}.skip-link:focus{left:1rem;top:1rem;background:#fff;padding:.6rem;z-index:10}.site-header{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}.header-inner{min-height:64px;display:flex;align-items:center;justify-content:space-between;gap:1rem}.site-title{font-weight:750;text-decoration:none;color:var(--text)}nav{display:flex;gap:1.1rem;flex-wrap:wrap}nav a{text-decoration:none;font-size:.95rem}main{padding-bottom:4rem}.hero{padding:5rem 0 3.5rem;max-width:980px}.hero h1,.page-header h1,.review-header h1{font-family:Georgia,"Times New Roman",serif;line-height:1.08;letter-spacing:-.025em}.hero h1{font-size:clamp(2.4rem,6vw,4.8rem);margin:.4rem 0 1.2rem}.lede{font-size:1.2rem;color:var(--muted);max-width:850px}.eyebrow{text-transform:uppercase;letter-spacing:.09em;font-size:.76rem;font-weight:800;color:var(--accent)}.hero-actions{display:flex;gap:.8rem;flex-wrap:wrap;margin:1.8rem 0}.button{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;padding:.75rem 1rem;border-radius:8px;font-weight:700}.button:hover{color:#fff;background:var(--accent-dark)}.button.secondary{background:#fff;color:var(--accent);border:1px solid var(--line)}.metrics{display:flex;gap:1.5rem;flex-wrap:wrap;color:var(--muted);border-top:1px solid var(--line);padding-top:1rem}.metrics strong{color:var(--text)}section{margin:2.5rem 0}.section-heading{display:flex;justify-content:space-between;gap:1rem;align-items:end;margin-bottom:1rem}.section-heading h2,.page-header h1{margin:.2rem 0}.card-grid{display:grid;gap:1rem}.review-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.domain-grid,.collection-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.review-card,.domain-card,.collection-card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:1.25rem;box-shadow:0 1px 2px rgba(0,0,0,.03)}.review-card h3,.domain-card h2,.domain-card h3,.collection-card h2,.collection-card h3{line-height:1.25;margin:.5rem 0}.review-card h3 a,.domain-card h2 a,.domain-card h3 a,.collection-card h2 a,.collection-card h3 a{text-decoration:none;color:var(--text)}.review-card p,.domain-card p,.collection-card p{color:var(--muted)}.publication,.count{color:var(--muted);font-size:.9rem}.card-actions{font-weight:700;font-size:.92rem}.page-header{padding:3.5rem 0 1.5rem;max-width:900px}.page-header h1{font-size:clamp(2.2rem,5vw,4rem)}.page-header>p{font-size:1.12rem;color:var(--muted)}.breadcrumbs{padding-top:1.5rem;color:var(--muted);font-size:.9rem}.tag-row{display:flex;gap:.5rem;flex-wrap:wrap;align-items:center}.tag,.tag-link{display:inline-block;border:1px solid var(--line);background:#fff;border-radius:999px;padding:.25rem .65rem;font-size:.82rem;text-decoration:none}.note{border-left:3px solid var(--accent);padding-left:1rem}.review-page{max-width:860px;margin:0 auto}.review-header{padding:2rem 0}.review-header h1{font-size:clamp(2.2rem,5vw,4rem);margin:.4rem 0 1rem}.review-meta{display:flex;gap:1rem;flex-wrap:wrap;color:var(--muted);margin-bottom:1rem}.key-insight{background:var(--highlight);border-radius:12px;padding:1.4rem;margin:0 0 2rem}.key-insight p{font-family:Georgia,"Times New Roman",serif;font-size:1.35rem;line-height:1.5;margin:.4rem 0}.prose{font-family:Georgia,"Times New Roman",serif;font-size:1.08rem}.prose h2,.prose h3{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin-top:2.2rem}.prose p{margin:1.1rem 0}.prose blockquote{border-left:3px solid var(--accent);margin:1.5rem 0;padding-left:1rem;color:var(--muted)}.prev-next{display:grid;grid-template-columns:1fr 1fr;gap:1rem;border-top:1px solid var(--line);padding-top:1.5rem;margin-top:2.5rem}.prev-next a{background:#fff;border:1px solid var(--line);border-radius:8px;padding:1rem;text-decoration:none;font-weight:700}.prev-next a span{display:block;text-transform:uppercase;letter-spacing:.08em;font-size:.7rem;color:var(--muted);margin-bottom:.3rem}.prev-next .next{text-align:right}.membership{border-top:1px solid var(--line);padding-top:1rem}.table-wrap{overflow-x:auto;background:#fff;border:1px solid var(--line);border-radius:10px}table{border-collapse:collapse;width:100%;min-width:820px}th,td{text-align:left;padding:.8rem;border-bottom:1px solid var(--line);vertical-align:top}th{font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}.site-footer{border-top:1px solid var(--line);padding:2rem 0;color:var(--muted);background:#fff}@media(max-width:900px){.domain-grid,.collection-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:700px){.header-inner{align-items:flex-start;padding:.8rem 0;flex-direction:column}nav{gap:.8rem}.hero{padding:3rem 0}.review-grid,.domain-grid,.collection-grid{grid-template-columns:1fr}.section-heading{align-items:flex-start;flex-direction:column}.prev-next{grid-template-columns:1fr}.prev-next .next{text-align:left}}
"""


def build_outputs(records: List[ReviewRecord], taxonomy: Taxonomy, collections: List[Collection], readme: str) -> Dict[Path, str]:
    outputs: Dict[Path, str] = {
        INDEX_PATH: render_markdown_index(records, taxonomy),
        ROOT_HTML_PATH: render_root_redirect(),
        README_PATH: update_readme(readme, records, taxonomy),
        DOCS_ROOT / "index.html": render_home(records, taxonomy, collections),
        DOCS_ROOT / "assets" / "site.css": SITE_CSS.strip() + "\n",
        DOCS_ROOT / "domains" / "index.html": render_domains_index(records, taxonomy),
        DOCS_ROOT / "collections" / "index.html": render_collections_index(collections, records),
        DOCS_ROOT / "archive" / "index.html": render_archive(records),
        DOCS_ROOT / ".nojekyll": "",
    }
    for domain, items in group_by_domain(records, taxonomy):
        outputs[DOCS_ROOT / "domains" / _slugify(domain) / "index.html"] = render_domain_page(domain, items, collections, records)
    for collection in collections:
        items = collection_records(collection, records)
        if items:
            outputs[DOCS_ROOT / "collections" / collection.slug / "index.html"] = render_collection_page(collection, items)
    for record in records:
        outputs[DOCS_ROOT / record.html_path] = render_review_page(record, records, collections)
    manifest_entries = sorted(path.relative_to(REPO_ROOT).as_posix() for path in outputs if path != MANIFEST_PATH)
    outputs[MANIFEST_PATH] = "\n".join(manifest_entries) + "\n"
    return outputs


def clean_stale_generated(expected: Iterable[Path]) -> None:
    expected_set = {p.resolve() for p in expected}
    if MANIFEST_PATH.exists():
        for rel in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
            path = (REPO_ROOT / rel).resolve()
            if path not in expected_set and path.exists() and DOCS_ROOT.resolve() in path.parents:
                path.unlink()
    for directory in sorted((p for p in DOCS_ROOT.rglob("*") if p.is_dir()), reverse=True):
        if directory != DOCS_ROOT and not any(directory.iterdir()):
            directory.rmdir()


def write_or_check(outputs: Dict[Path, str], check: bool) -> int:
    stale: List[str] = []
    for path, content in outputs.items():
        existing = path.read_text(encoding="utf-8") if path.exists() else None
        if existing != content:
            if check:
                stale.append(path.relative_to(REPO_ROOT).as_posix())
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
    if check:
        expected_manifest = outputs[MANIFEST_PATH].splitlines()
        actual_manifest = MANIFEST_PATH.read_text(encoding="utf-8").splitlines() if MANIFEST_PATH.exists() else []
        if expected_manifest != actual_manifest and MANIFEST_PATH.relative_to(REPO_ROOT).as_posix() not in stale:
            stale.append(MANIFEST_PATH.relative_to(REPO_ROOT).as_posix())
        if stale:
            print("Generated files are stale:")
            for item in stale:
                print(f"Out of date: {item}")
            return 2
        print(f"Generated site is up to date ({len(outputs)-1} files).")
        return 0
    clean_stale_generated(outputs)
    print(f"Generated discovery site rebuilt successfully ({len(outputs)-1} files).")
    return 0


def lint_files(paths: Sequence[Path], taxonomy: Taxonomy) -> int:
    failed = False
    for path in paths:
        if not path.exists():
            print(f"ERROR  {path}: file not found")
            failed = True
            continue
        errors = validate_review_file(path, path.read_text(encoding="utf-8"), parse_front_matter(path.read_text(encoding="utf-8")), taxonomy)
        if errors:
            failed = True
            print(f"FAIL   {path}")
            for error in errors:
                print(f"       • {error}")
        else:
            print(f"OK     {path}")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build, check or lint the paper notes archive.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--lint", nargs="+")
    parser.add_argument("--print-generated", action="store_true")
    args = parser.parse_args()
    taxonomy = load_taxonomy()
    if args.lint:
        return lint_files([Path(x).resolve() for x in args.lint], taxonomy)
    records = load_reviews(taxonomy)
    collections = load_collections()
    if args.print_generated:
        outputs = build_outputs(records, taxonomy, collections, README_PATH.read_text(encoding="utf-8"))
        for path in sorted(outputs):
            print(path.relative_to(REPO_ROOT).as_posix())
        return 0
    outputs = build_outputs(records, taxonomy, collections, README_PATH.read_text(encoding="utf-8"))
    return write_or_check(outputs, args.check)


if __name__ == "__main__":
    raise SystemExit(main())
