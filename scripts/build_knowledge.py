#!/usr/bin/env python3
"""Generate evidence-backed Knowledge Layer discovery pages."""
from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "knowledge"
K = ROOT / "knowledge"
SYNTH = ROOT / "collections" / "syntheses"
REVIEWS = ROOT / "reviews"
COLLECTIONS = ROOT / "collections" / "collections.json"


def load(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


def relative_prefix(page_path):
    return "../" * max(0, len(Path(page_path).parts) - 1)


def page(page_title, body, page_path, desc=""):
    p = relative_prefix(page_path)
    d = desc or "Evidence-backed synthesis and cross-paper governance discovery."
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(page_title)} | Digital Governance Paper Notes</title><meta name="description" content="{html.escape(d, quote=True)}"><link rel="stylesheet" href="{p}assets/site.css"></head><body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="container header-inner"><a class="site-title" href="{p}">Digital Governance Paper Notes</a><nav aria-label="Primary navigation"><a href="{p}#recent">Recent</a><a href="{p}domains/">Domains</a><a href="{p}collections/">Collections</a><a href="{p}archive/">Archive</a><a href="{p}knowledge/" aria-current="page">Knowledge</a></nav></div></header><main id="main" class="container"><div class="breadcrumbs"><a href="{p}">Home</a> · <a href="{p}knowledge/">Knowledge</a></div>{body}</main><footer class="site-footer"><div class="container">Digital Governance Paper Notes · Governance-first research reviews and cumulative knowledge infrastructure.</div></footer></body></html>"""


def front_matter(path):
    text = path.read_text(encoding="utf-8").lstrip("\ufeff")
    m = re.match(r"(?ms)^---\s*\n(.*?)\n---\s*", text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def review_url(path, pfx):
    m = re.match(r"^(\d{4})-\d{2}-\d{2}__(.+)__v\d+\.md$", Path(path).name)
    return f"{pfx}reviews/{m.group(1)}/{m.group(2)}/" if m else pfx


def load_reviews():
    reviews = {}
    for path in sorted(REVIEWS.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        fm = front_matter(path)
        reviews[rel] = {
            "title": str(fm.get("title", path.stem)),
            "domain": str(fm.get("primary_domain", "")),
            "tags": list(fm.get("tags") or []),
            "key_insight": str(fm.get("key_insight", "")),
            "date_read": str(fm.get("date_read", "")),
            "governance_facets": list(fm.get("governance_facets") or []),
            "review_status": str(fm.get("review_status", "current")),
        }

    legacy = load(K / "review-metadata.yml").get("reviews") or {}
    for rel, override in legacy.items():
        if rel not in reviews:
            continue
        merged = reviews[rel]
        for key, value in override.items():
            if key == "governance_facets":
                merged[key] = list(dict.fromkeys((merged.get(key) or []) + (value or [])))
            elif not merged.get(key):
                merged[key] = value
    return reviews


def load_syntheses():
    out = []
    for path in sorted(SYNTH.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = front_matter(path)
        out.append({
            "slug": path.stem,
            "path": path,
            "title": str(fm.get("title", path.stem.replace("-", " ").title())),
            "collection": str(fm.get("collection", "")),
            "last_reviewed": str(fm.get("last_reviewed", "")),
            "status": str(fm.get("status", "current")),
            "source_reviews": list(fm.get("source_reviews") or []),
            "text": text,
        })
    return out


def title(path, reviews):
    return reviews.get(path, {}).get("title") or Path(path).stem


def inline_md(text):
    escaped = html.escape(str(text))
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)


def tag_row(items):
    values = [str(x) for x in items if x]
    if not values:
        return ""
    return "<div class='tag-row'>" + "".join(f"<span class='tag'>{html.escape(v.replace('-', ' ').title())}</span>" for v in values) + "</div>"


def source_links(paths, pfx, reviews, with_insight=False):
    bits = []
    for path in paths:
        meta = reviews.get(path, {})
        insight = meta.get("key_insight", "")
        extra = f"<div class='publication'>{html.escape(insight)}</div>" if with_insight and insight else ""
        bits.append(f"<li><a href='{review_url(path, pfx)}'>{html.escape(title(path, reviews))}</a>{extra}</li>")
    return "".join(bits)


def knowledge_card(item, kind, page_path, reviews):
    p = relative_prefix(page_path)
    heading = item.get("title", item.get("id", "Untitled"))
    claim = item.get("claim", item.get("gap", ""))
    rationale = item.get("rationale", item.get("why_it_matters", ""))
    sources = item.get("source_reviews") or []
    facets = item.get("facets") or []
    return (
        "<article class='review-card'>"
        f"<div class='eyebrow'>{html.escape(kind)} · {len(sources)} source review{'s' if len(sources) != 1 else ''}</div>"
        f"<h3>{html.escape(str(heading))}</h3>"
        f"<p>{html.escape(str(claim))}</p>"
        f"<p>{html.escape(str(rationale))}</p>"
        f"{tag_row(facets)}"
        f"<details><summary>Evidence base</summary><ul>{source_links(sources, p, reviews, True)}</ul></details>"
        "</article>"
    )


def review_card(path, meta, page_path):
    p = relative_prefix(page_path)
    facets = meta.get("governance_facets") or []
    eyebrow = " · ".join(x for x in [meta.get("date_read", ""), meta.get("domain", "")] if x)
    insight = meta.get("key_insight", "")
    return (
        "<article class='review-card'>"
        f"<div class='eyebrow'>{html.escape(eyebrow)}</div>"
        f"<h3><a href='{review_url(path, p)}'>{html.escape(meta.get('title', Path(path).stem))}</a></h3>"
        f"<p>{html.escape(insight)}</p>"
        f"{tag_row(facets)}"
        f"<div class='card-actions'><a href='{review_url(path, p)}'>Read review</a></div>"
        "</article>"
    )


def md_basic(text):
    text = re.sub(r"(?ms)^---\n.*?\n---\n", "", text, count=1)
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        s = block.strip()
        if s.startswith("# "):
            continue
        if s.startswith("## "):
            out.append(f"<h2>{html.escape(s[3:])}</h2>")
        elif s.startswith("### "):
            out.append(f"<h3>{html.escape(s[4:])}</h3>")
        elif s.startswith("- "):
            out.append("<ul>" + "".join(f"<li>{inline_md(y[2:])}</li>" for y in s.splitlines() if y.startswith("- ")) + "</ul>")
        else:
            out.append(f"<p>{inline_md(' '.join(y.strip() for y in s.splitlines()))}</p>")
    return "\n".join(out)


def overlap_items(items, review_paths):
    paths = set(review_paths)
    return [item for item in items if paths.intersection(item.get("source_reviews") or [])]


def synthesis_card(item, page_path):
    p = relative_prefix(page_path)
    count = len(item.get("source_reviews") or [])
    return (
        "<article class='collection-card'>"
        f"<div class='eyebrow'>Collection synthesis · {count} reviews</div>"
        f"<h3><a href='{p}knowledge/synthesis/{html.escape(item['slug'])}/'>{html.escape(item['title'])}</a></h3>"
        f"<p>Last substantively reviewed {html.escape(item.get('last_reviewed', ''))}.</p>"
        f"<div class='card-actions'><a href='{p}knowledge/synthesis/{html.escape(item['slug'])}/'>Read synthesis</a></div>"
        "</article>"
    )


def main():
    facets = load(K / "governance-facets.yml").get("facets") or {}
    relationships = load(K / "relationships.yml").get("relationships") or []
    findings = load(K / "findings.yml").get("findings") or []
    gaps = load(K / "gaps.yml").get("gaps") or []
    reviews = load_reviews()
    syntheses = load_syntheses()
    collections = json.loads(COLLECTIONS.read_text(encoding="utf-8")).get("collections", []) if COLLECTIONS.exists() else []

    DOCS.mkdir(parents=True, exist_ok=True)
    mapped = {path: meta for path, meta in reviews.items() if meta.get("governance_facets")}
    counts = Counter()
    for meta in mapped.values():
        counts.update(meta.get("governance_facets") or [])

    sorted_themes = sorted(facets.items(), key=lambda pair: (-counts.get(pair[0], 0), pair[0]))
    theme_cards = "".join(
        f"<article class='collection-card'><div class='count'>{counts.get(fid,0)} mapped review{'s' if counts.get(fid,0) != 1 else ''}</div>"
        f"<h3><a href='facets/{fid}/'>{html.escape(fid.replace('-', ' ').title())}</a></h3>"
        f"<p>{html.escape(str(spec.get('description','')))}</p></article>"
        for fid, spec in sorted_themes
    )

    recent_mapped = sorted(mapped.items(), key=lambda x: (x[1].get("date_read", ""), x[1].get("title", "")), reverse=True)[:6]
    synth_cards = "".join(synthesis_card(s, "knowledge/index.html") for s in syntheses)

    body = f"""
<section class="page-header">
  <div class="eyebrow">Archive as Knowledge Infrastructure</div>
  <h1>What the archive is learning across papers.</h1>
  <p>This section turns individual reviews into reader pathways through recurring governance mechanisms, curated connections, cross-paper findings, unresolved gaps and human-edited syntheses. Generated pages organize accepted evidence; they do not manufacture consensus.</p>
  <div class="hero-actions"><a class="button" href="findings/">Start with findings</a><a class="button secondary" href="synthesis/">Read syntheses</a></div>
  <div class="metrics"><span><strong>{len(reviews)}</strong> canonical reviews</span><span><strong>{len(mapped)}</strong> knowledge-mapped reviews</span><span><strong>{len(relationships)}</strong> curated connections</span><span><strong>{len(findings)}</strong> findings</span><span><strong>{len(gaps)}</strong> open gaps</span><span><strong>{len(syntheses)}</strong> syntheses</span></div>
</section>
<section>
  <div class="section-heading"><div><div class="eyebrow">Reader paths</div><h2>Choose the question you want the archive to answer</h2></div></div>
  <div class="card-grid collection-grid">
    <article class="collection-card"><h3><a href="findings/">What is recurring?</a></h3><p>Cross-paper propositions with an explicit evidence base.</p></article>
    <article class="collection-card"><h3><a href="synthesis/">What does a body of work add up to?</a></h3><p>Human-edited collection syntheses that accumulate analysis across reviews.</p></article>
    <article class="collection-card"><h3><a href="#themes">Which governance mechanism matters?</a></h3><p>Authority, legitimacy, accountability, revocation, redress and other recurring mechanisms.</p></article>
    <article class="collection-card"><h3><a href="relationships/">Which papers materially connect?</a></h3><p>Curated relationships with reasons, not automated similarity links.</p></article>
    <article class="collection-card"><h3><a href="gaps/">What remains unresolved?</a></h3><p>Research and institutional questions repeatedly exposed by the archive.</p></article>
  </div>
</section>
<section>
  <div class="section-heading"><div><div class="eyebrow">Cumulative analysis</div><h2>Start with a synthesis</h2></div><a href="synthesis/">All syntheses</a></div>
  <div class="card-grid collection-grid">{synth_cards or "<p class='note'>No syntheses published yet.</p>"}</div>
</section>
<section>
  <div class="section-heading"><div><div class="eyebrow">Emerging propositions</div><h2>What the archive is beginning to establish</h2></div><a href="findings/">All findings</a></div>
  <div class="card-grid review-grid">{''.join(knowledge_card(x,'Cross-paper finding','knowledge/index.html',reviews) for x in findings[:4])}</div>
</section>
<section id="themes">
  <div class="section-heading"><div><div class="eyebrow">Recurring mechanisms</div><h2>Governance themes</h2></div></div>
  <div class="card-grid collection-grid">{theme_cards}</div>
</section>
<section>
  <div class="section-heading"><div><div class="eyebrow">Recent evidence</div><h2>Recently mapped reviews</h2></div></div>
  <div class="card-grid review-grid">{''.join(review_card(path,meta,'knowledge/index.html') for path,meta in recent_mapped)}</div>
</section>
<section>
  <div class="section-heading"><div><div class="eyebrow">Research agenda</div><h2>What remains unresolved</h2></div><a href="gaps/">All gaps</a></div>
  <div class="card-grid review-grid">{''.join(knowledge_card(x,'Open governance gap','knowledge/index.html',reviews) for x in gaps[:4])}</div>
</section>
"""
    (DOCS / "index.html").write_text(page("Knowledge Map", body, "knowledge/index.html"), encoding="utf-8")

    for fid, spec in facets.items():
        d = DOCS / "facets" / fid
        d.mkdir(parents=True, exist_ok=True)
        pp = f"knowledge/facets/{fid}/index.html"
        matches = [(path, meta) for path, meta in mapped.items() if fid in (meta.get("governance_facets") or [])]
        matches.sort(key=lambda x: (x[1].get("date_read", ""), x[1].get("title", "")), reverse=True)
        related_findings = [x for x in findings if fid in (x.get("facets") or [])]
        related_gaps = [x for x in gaps if fid in (x.get("facets") or [])]
        match_paths = {x[0] for x in matches}
        related_edges = [e for e in relationships if e.get("from") in match_paths or e.get("to") in match_paths]
        edge_html = "".join(
            f"<article class='review-card'><div class='eyebrow'>{html.escape(str(e['type']).replace('_',' ').replace('-',' '))}</div>"
            f"<h3><a href='{review_url(e['from'],relative_prefix(pp))}'>{html.escape(title(e['from'],reviews))}</a> → <a href='{review_url(e['to'],relative_prefix(pp))}'>{html.escape(title(e['to'],reviews))}</a></h3>"
            f"<p>{html.escape(str(e.get('rationale','')))}</p></article>"
            for e in related_edges[:8]
        )
        b = f"""
<section class='page-header'><div class='eyebrow'>Governance theme · {len(matches)} mapped reviews</div><h1>{html.escape(fid.replace('-',' ').title())}</h1><p>{html.escape(str(spec.get('description','')))}</p></section>
<section><div class='section-heading'><div><div class='eyebrow'>Evidence</div><h2>Reviews that substantively treat this mechanism</h2></div></div><div class='card-grid review-grid'>{''.join(review_card(path,meta,pp) for path,meta in matches) or '<p class=note>No mapped reviews currently carry this theme.</p>'}</div></section>
<section><div class='section-heading'><div><div class='eyebrow'>Cross-paper knowledge</div><h2>Findings connected to this theme</h2></div></div><div class='card-grid review-grid'>{''.join(knowledge_card(x,'Cross-paper finding',pp,reviews) for x in related_findings) or '<p class=note>No curated finding currently uses this theme.</p>'}</div></section>
<section><div class='section-heading'><div><div class='eyebrow'>Research agenda</div><h2>Open gaps connected to this theme</h2></div></div><div class='card-grid review-grid'>{''.join(knowledge_card(x,'Open governance gap',pp,reviews) for x in related_gaps) or '<p class=note>No curated gap currently uses this theme.</p>'}</div></section>
<section><div class='section-heading'><div><div class='eyebrow'>Connections</div><h2>Material relationships among relevant reviews</h2></div></div><div class='card-grid review-grid'>{edge_html or '<p class=note>No curated relationship currently touches this theme.</p>'}</div></section>
"""
        (d / "index.html").write_text(page(f"Governance theme: {fid}", b, pp), encoding="utf-8")

    rd = DOCS / "relationships"
    rd.mkdir(parents=True, exist_ok=True)
    pp = "knowledge/relationships/index.html"
    pfx = relative_prefix(pp)
    degree = Counter()
    for e in relationships:
        degree[e.get("from")] += 1
        degree[e.get("to")] += 1
    hubs = [path for path, _ in degree.most_common(6)]
    hub_html = "".join(review_card(path, reviews.get(path, {}), pp) for path in hubs)
    rc = "".join(
        f"<article class='review-card'><div class='eyebrow'>{html.escape(str(e['type']).replace('_',' ').replace('-',' '))}</div><h3><a href='{review_url(e['from'],pfx)}'>{html.escape(title(e['from'],reviews))}</a> → <a href='{review_url(e['to'],pfx)}'>{html.escape(title(e['to'],reviews))}</a></h3><p>{html.escape(str(e.get('rationale','')))}</p></article>"
        for e in relationships
    )
    (rd / "index.html").write_text(page(
        "Curated review relationships",
        f"<section class='page-header'><div class='eyebrow'>Connections · {len(relationships)} editorial edges</div><h1>How reviews materially connect</h1><p>Every edge is an explicit editorial claim with a rationale. This page does not render automated semantic similarity as knowledge.</p></section><section><div class='section-heading'><div><div class='eyebrow'>Connection hubs</div><h2>Reviews participating in multiple curated relationships</h2></div></div><div class='card-grid review-grid'>{hub_html}</div></section><section><div class='section-heading'><div><div class='eyebrow'>All connections</div><h2>Curated relationship graph</h2></div></div><div class='card-grid review-grid'>{rc}</div></section>",
        pp,
    ), encoding="utf-8")

    for slug, items, label, intro in [
        ("findings", findings, "Cross-paper finding", "Propositions synthesized from multiple canonical reviews. Each finding exposes its evidence base and remains revisable as the archive grows."),
        ("gaps", gaps, "Open governance gap", "Questions the archive repeatedly exposes but does not yet resolve. Gaps are research agenda items, not claims that no answer exists elsewhere."),
    ]:
        d = DOCS / slug
        d.mkdir(parents=True, exist_ok=True)
        pp = f"knowledge/{slug}/index.html"
        b = f"<section class='page-header'><div class='eyebrow'>{label} · {len(items)}</div><h1>{slug.title()}</h1><p>{intro}</p></section><section><div class='card-grid review-grid'>{''.join(knowledge_card(x,label,pp,reviews) for x in items)}</div></section>"
        (d / "index.html").write_text(page(slug.title(), b, pp), encoding="utf-8")

    sd = DOCS / "synthesis"
    sd.mkdir(parents=True, exist_ok=True)
    pp = "knowledge/synthesis/index.html"
    collection_by_slug = {str(c.get("slug")): c for c in collections}
    synth_index = "".join(
        f"<article class='collection-card'><div class='eyebrow'>{html.escape(collection_by_slug.get(s['collection'],{}).get('title',s['collection']))} · {len(s['source_reviews'])} reviews</div><h3><a href='{relative_prefix(pp)}knowledge/synthesis/{html.escape(s['slug'])}/'>{html.escape(s['title'])}</a></h3><p>{html.escape(collection_by_slug.get(s['collection'],{}).get('description',''))}</p><div class='publication'>Last reviewed {html.escape(s['last_reviewed'])}</div></article>"
        for s in syntheses
    )
    (sd / "index.html").write_text(page(
        "Collection syntheses",
        f"<section class='page-header'><div class='eyebrow'>Cumulative analysis · {len(syntheses)} syntheses</div><h1>What bodies of reviewed work add up to</h1><p>Syntheses are human-edited analytical artifacts grounded in named canonical reviews. They accumulate findings across papers without turning generated text into a second source of truth.</p></section><section><div class='card-grid collection-grid'>{synth_index}</div></section>",
        pp,
    ), encoding="utf-8")

    for s in syntheses:
        d = sd / s["slug"]
        d.mkdir(parents=True, exist_ok=True)
        pp = f"knowledge/synthesis/{s['slug']}/index.html"
        related_f = overlap_items(findings, s["source_reviews"])
        related_g = overlap_items(gaps, s["source_reviews"])
        b = (
            f"<section class='page-header'><div class='eyebrow'>Collection synthesis · {len(s['source_reviews'])} source reviews</div><h1>{html.escape(s['title'])}</h1><p>Last substantively reviewed {html.escape(s['last_reviewed'])}. Claims below are grounded in the named source reviews.</p></section>"
            f"<article class='review-page prose'>{md_basic(s['text'])}</article>"
            f"<section><div class='section-heading'><div><div class='eyebrow'>Traceability</div><h2>Constituent reviews</h2></div></div><div class='card-grid review-grid'>{''.join(review_card(path,reviews.get(path,{}),pp) for path in s['source_reviews'])}</div></section>"
            f"<section><div class='section-heading'><div><div class='eyebrow'>Related knowledge</div><h2>Findings and gaps touching this synthesis</h2></div></div><div class='card-grid review-grid'>{''.join(knowledge_card(x,'Cross-paper finding',pp,reviews) for x in related_f[:4])}{''.join(knowledge_card(x,'Open governance gap',pp,reviews) for x in related_g[:4])}</div></section>"
        )
        (d / "index.html").write_text(page(s["title"], b, pp), encoding="utf-8")

    print(f"Generated knowledge pages: {len(facets)} themes, {len(mapped)} mapped reviews, {len(relationships)} relationships, {len(findings)} findings, {len(gaps)} gaps, {len(syntheses)} syntheses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
