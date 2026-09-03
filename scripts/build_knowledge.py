#!/usr/bin/env python3
"""Generate Archive as Knowledge Infrastructure discovery pages.

Knowledge pages are a first-class section of the Digital Governance Paper Notes
site. They deliberately reuse the core discovery site's visual language and
navigation rather than presenting a separate microsite.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "knowledge"
FACETS = ROOT / "knowledge" / "governance-facets.yml"
META = ROOT / "knowledge" / "review-metadata.yml"
REL = ROOT / "knowledge" / "relationships.yml"
SYNTH = ROOT / "collections" / "syntheses"


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def review_title(path: str) -> str:
    text = (ROOT / path).read_text(encoding="utf-8")
    match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', text, re.M)
    return match.group(1).strip() if match else Path(path).stem


def relative_prefix(page_path: str) -> str:
    depth = max(0, len(Path(page_path).parts) - 1)
    return "../" * depth


def review_site_url(path: str, prefix: str) -> str:
    name = Path(path).name
    match = re.match(r"^(\d{4})-\d{2}-\d{2}__(.+)__v\d+\.md$", name)
    if not match:
        return prefix
    year, slug = match.groups()
    return f"{prefix}reviews/{year}/{slug}/"


def page(title: str, body: str, page_path: str, description: str = "") -> str:
    prefix = relative_prefix(page_path)
    desc = description or "Cross-paper governance discovery, relationships and synthesis from Digital Governance Paper Notes."
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
        <a href="{prefix}knowledge/" aria-current="page">Knowledge</a>
      </nav>
    </div>
  </header>
  <main id="main" class="container">
    <div class="breadcrumbs"><a href="{prefix}">Home</a> · <a href="{prefix}knowledge/">Knowledge</a></div>
    {body}
  </main>
  <footer class="site-footer">
    <div class="container">Digital Governance Paper Notes · Governance-first research reviews and cumulative knowledge infrastructure.</div>
  </footer>
</body>
</html>
"""


def md_basic(text: str) -> str:
    text = re.sub(r"(?ms)^---\n.*?\n---\n", "", text, count=1)
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        line = block.strip()
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("- "):
            items = "".join(f"<li>{html.escape(x[2:])}</li>" for x in line.splitlines() if x.startswith("- "))
            out.append(f"<ul>{items}</ul>")
        else:
            escaped = html.escape(" ".join(x.strip() for x in line.splitlines()))
            escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
            escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
            out.append(f"<p>{escaped}</p>")
    return "\n".join(out)


def main() -> int:
    facets = load_yaml(FACETS).get("facets") or {}
    metadata = load_yaml(META).get("reviews") or {}
    relationships = load_yaml(REL).get("relationships") or []
    DOCS.mkdir(parents=True, exist_ok=True)

    facet_counts = {facet: 0 for facet in facets}
    for item in metadata.values():
        for facet in item.get("governance_facets") or []:
            facet_counts[facet] = facet_counts.get(facet, 0) + 1

    syntheses = sorted(SYNTH.glob("*.md"))

    facet_cards = "".join(
        f"<article class='collection-card'><div class='count'>{facet_counts.get(facet, 0)} reviews</div>"
        f"<h3><a href='facets/{html.escape(facet)}/'>{html.escape(facet.replace('-', ' ').title())}</a></h3>"
        f"<p>{html.escape(str(spec.get('description', '')))}</p><a href='facets/{html.escape(facet)}/'>Explore facet</a></article>"
        for facet, spec in facets.items()
    )
    synthesis_cards = "".join(
        f"<article class='collection-card'><div class='eyebrow'>Cross-paper synthesis</div>"
        f"<h3><a href='synthesis/{p.stem}/'>{html.escape(p.stem.replace('-', ' ').title())}</a></h3>"
        f"<p>Human-edited synthesis with traceability to constituent reviews and source papers.</p>"
        f"<a href='synthesis/{p.stem}/'>Read synthesis</a></article>"
        for p in syntheses
    )

    body = f"""
<section class="page-header">
  <div class="eyebrow">Archive as Knowledge Infrastructure</div>
  <h1>Knowledge across the review archive.</h1>
  <p>This layer connects individual reviews across recurring governance mechanisms, curated relationships, synthesis and review history. Canonical analytical judgment remains in repository source files; these pages are generated discovery surfaces.</p>
  <div class="hero-actions"><a class="button" href="#facets">Explore governance facets</a><a class="button secondary" href="relationships/">Review relationships</a></div>
  <div class="metrics"><span><strong>{len(metadata)}</strong> enriched reviews</span><span><strong>{len(relationships)}</strong> curated relationships</span><span><strong>{len(syntheses)}</strong> syntheses</span></div>
</section>
<section id="facets">
  <div class="section-heading"><div><div class="eyebrow">Recurring mechanisms</div><h2>Governance facets</h2></div></div>
  <div class="card-grid collection-grid">{facet_cards}</div>
</section>
<section>
  <div class="section-heading"><div><div class="eyebrow">Cumulative analysis</div><h2>Collection syntheses</h2></div></div>
  <div class="card-grid collection-grid">{synthesis_cards or '<p class="note">No collection syntheses have been published yet.</p>'}</div>
</section>
<section>
  <div class="section-heading"><div><div class="eyebrow">Editorial infrastructure</div><h2>Relationships, provenance and correction</h2></div></div>
  <div class="card-grid collection-grid">
    <article class="collection-card"><h3><a href="relationships/">Curated review relationships</a></h3><p>Trace where papers extend, challenge, operationalize or otherwise materially relate to one another.</p><a href="relationships/">Browse relationships</a></article>
    <article class="collection-card"><h3><a href="https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/blob/main/knowledge/history-policy.md">Corrections and supersession</a></h3><p>Reader-facing semantics for changing papers, corrected reviews, supersession, withdrawal and retraction.</p><a href="https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/blob/main/knowledge/history-policy.md">Read policy</a></article>
    <article class="collection-card"><h3><a href="https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/blob/main/AI-USAGE.md">AI usage and editorial authority</a></h3><p>How AI-assisted extraction, enrichment and synthesis remain subordinate to source grounding and human editorial judgment.</p><a href="https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/blob/main/AI-USAGE.md">Read disclosure</a></article>
  </div>
</section>
"""
    (DOCS / "index.html").write_text(
        page("Knowledge Infrastructure", body, "knowledge/index.html"), encoding="utf-8"
    )

    for facet, spec in facets.items():
        target = DOCS / "facets" / facet
        target.mkdir(parents=True, exist_ok=True)
        page_path = f"knowledge/facets/{facet}/index.html"
        prefix = relative_prefix(page_path)
        matches = [path for path, item in metadata.items() if facet in (item.get("governance_facets") or [])]
        cards = "".join(
            f"<article class='review-card'><div class='eyebrow'>Governance facet</div>"
            f"<h3><a href='{review_site_url(path, prefix)}'>{html.escape(review_title(path))}</a></h3>"
            f"<div class='publication'><code>{html.escape(path)}</code></div>"
            f"<div class='card-actions'><a href='{review_site_url(path, prefix)}'>Read review</a></div></article>"
            for path in matches
        )
        facet_body = f"""
<section class="page-header">
  <div class="eyebrow">Governance facet</div>
  <h1>{html.escape(facet.replace('-', ' ').title())}</h1>
  <p>{html.escape(str(spec.get('description', '')))}</p>
</section>
<section><div class="card-grid review-grid">{cards or '<p class="note">No enriched reviews currently carry this facet.</p>'}</div></section>
"""
        (target / "index.html").write_text(
            page(f"Governance facet: {facet}", facet_body, page_path), encoding="utf-8"
        )

    rel_dir = DOCS / "relationships"
    rel_dir.mkdir(parents=True, exist_ok=True)
    rel_path = "knowledge/relationships/index.html"
    rel_prefix = relative_prefix(rel_path)
    relationship_cards = "".join(
        f"<article class='review-card'><div class='eyebrow'>{html.escape(entry['type'].replace('-', ' '))}</div>"
        f"<h3><a href='{review_site_url(entry['from'], rel_prefix)}'>{html.escape(review_title(entry['from']))}</a> → "
        f"<a href='{review_site_url(entry['to'], rel_prefix)}'>{html.escape(review_title(entry['to']))}</a></h3>"
        f"<p>{html.escape(entry.get('rationale', ''))}</p></article>"
        for entry in relationships
    )
    rel_body = f"""
<section class="page-header">
  <div class="eyebrow">Cross-paper structure</div>
  <h1>Curated review relationships</h1>
  <p>Relationships are editorial claims rather than automatically inferred similarity. Each edge is retained with a rationale and points back to the canonical review surfaces.</p>
</section>
<section><div class="card-grid review-grid">{relationship_cards or '<p class="note">No curated relationships are currently published.</p>'}</div></section>
"""
    (rel_dir / "index.html").write_text(
        page("Curated review relationships", rel_body, rel_path), encoding="utf-8"
    )

    for src in syntheses:
        target = DOCS / "synthesis" / src.stem
        target.mkdir(parents=True, exist_ok=True)
        synth_path = f"knowledge/synthesis/{src.stem}/index.html"
        synth_body = f"""
<section class="page-header">
  <div class="eyebrow">Collection synthesis</div>
  <h1>{html.escape(src.stem.replace('-', ' ').title())}</h1>
  <p>A human-edited synthesis across multiple reviews, retained with traceability to its constituent analytical sources.</p>
</section>
<article class="review-page prose">{md_basic(src.read_text(encoding='utf-8'))}</article>
"""
        (target / "index.html").write_text(
            page(src.stem.replace('-', ' ').title(), synth_body, synth_path), encoding="utf-8"
        )

    print(
        f"Generated knowledge pages: {len(facets)} facets, {len(relationships)} relationships, {len(syntheses)} syntheses"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
