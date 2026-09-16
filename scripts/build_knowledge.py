#!/usr/bin/env python3
"""Generate evidence-backed Knowledge Layer discovery pages."""
from __future__ import annotations
import html, re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "knowledge"
K = ROOT / "knowledge"
SYNTH = ROOT / "collections" / "syntheses"

def load(path): return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
def title(path):
    text=(ROOT/path).read_text(encoding="utf-8")
    m=re.search(r'^title:\s*["\']?(.*?)["\']?\s*$',text,re.M)
    return m.group(1).strip() if m else Path(path).stem
def prefix(page_path): return "../" * max(0,len(Path(page_path).parts)-1)
def review_url(path,pfx):
    m=re.match(r"^(\d{4})-\d{2}-\d{2}__(.+)__v\d+\.md$",Path(path).name)
    return f"{pfx}reviews/{m.group(1)}/{m.group(2)}/" if m else pfx
def shell(page_title,body,page_path,desc=""):
    p=prefix(page_path); d=desc or "Evidence-backed synthesis and cross-paper governance discovery."
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(page_title)} | Digital Governance Paper Notes</title><meta name="description" content="{html.escape(d,quote=True)}"><link rel="stylesheet" href="{p}assets/site.css"></head><body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="container header-inner"><a class="site-title" href="{p}">Digital Governance Paper Notes</a><nav aria-label="Primary navigation"><a href="{p}#recent">Recent</a><a href="{p}domains/">Domains</a><a href="{p}collections/">Collections</a><a href="{p}archive/">Archive</a><a href="{p}knowledge/" aria-current="page">Knowledge</a></nav></div></header><main id="main" class="container"><div class="breadcrumbs"><a href="{p}">Home</a> · <a href="{p}knowledge/">Knowledge</a></div>{body}</main><footer class="site-footer"><div class="container">Digital Governance Paper Notes · Governance-first research reviews and cumulative knowledge infrastructure.</div></footer></body></html>'''
def source_links(paths,pfx):
    return "".join(f"<li><a href='{review_url(x,pfx)}'>{html.escape(title(x))}</a></li>" for x in paths)
def cards(items,kind,page_path):
    p=prefix(page_path); out=[]
    for x in items:
        heading=x.get("title",x.get("id","Untitled")); claim=x.get("claim",x.get("gap","")); rationale=x.get("rationale",x.get("why_it_matters",""))
        out.append(f"<article class='review-card'><div class='eyebrow'>{html.escape(kind)}</div><h3>{html.escape(heading)}</h3><p>{html.escape(claim)}</p><p>{html.escape(rationale)}</p><details><summary>Evidence base</summary><ul>{source_links(x.get('source_reviews') or [],p)}</ul></details></article>")
    return "".join(out)
def md_basic(text):
    text=re.sub(r"(?ms)^---\n.*?\n---\n","",text,count=1); out=[]
    for b in re.split(r"\n\s*\n",text.strip()):
        s=b.strip()
        if s.startswith("# "): continue
        if s.startswith("## "): out.append(f"<h2>{html.escape(s[3:])}</h2>")
        elif s.startswith("### "): out.append(f"<h3>{html.escape(s[4:])}</h3>")
        elif s.startswith("- "): out.append("<ul>"+"".join(f"<li>{html.escape(y[2:])}</li>" for y in s.splitlines() if y.startswith('- '))+"</ul>")
        else: out.append(f"<p>{html.escape(' '.join(y.strip() for y in s.splitlines()))}</p>")
    return "\n".join(out)

def main():
    facets=load(K/"governance-facets.yml").get("facets") or {}; meta=load(K/"review-metadata.yml").get("reviews") or {}; rel=load(K/"relationships.yml").get("relationships") or []
    findings=load(K/"findings.yml").get("findings") or []; gaps=load(K/"gaps.yml").get("gaps") or []; synth=sorted(SYNTH.glob("*.md")); DOCS.mkdir(parents=True,exist_ok=True)
    counts={f:0 for f in facets}
    for item in meta.values():
        for f in item.get("governance_facets") or []: counts[f]=counts.get(f,0)+1
    theme_cards="".join(f"<article class='collection-card'><div class='count'>{counts.get(f,0)} enriched reviews</div><h3><a href='facets/{f}/'>{html.escape(f.replace('-',' ').title())}</a></h3><p>{html.escape(str(spec.get('description','')))}</p></article>" for f,spec in facets.items())
    body=f'''<section class="page-header"><div class="eyebrow">Archive as Knowledge Infrastructure</div><h1>What the review archive collectively tells us.</h1><p>The Knowledge layer connects canonical reviews into evidence-backed themes, editorial relationships, recurring findings and unresolved research gaps. It does not replace the reviews or infer consensus automatically.</p><div class="hero-actions"><a class="button" href="findings/">Explore findings</a><a class="button secondary" href="gaps/">Explore gaps</a></div><div class="metrics"><span><strong>{len(meta)}</strong> enriched reviews</span><span><strong>{len(rel)}</strong> curated connections</span><span><strong>{len(findings)}</strong> findings</span><span><strong>{len(gaps)}</strong> open gaps</span></div></section>
<section><div class="section-heading"><div><div class="eyebrow">Reader paths</div><h2>Themes · Connections · Findings · Gaps</h2></div></div><div class="card-grid collection-grid"><article class="collection-card"><h3><a href="#themes">Themes</a></h3><p>Recurring governance mechanisms such as authority, delegation, revocation, legitimacy, redress and enforcement.</p></article><article class="collection-card"><h3><a href="relationships/">Connections</a></h3><p>Human-curated claims about how reviews extend, challenge or otherwise materially relate to one another.</p></article><article class="collection-card"><h3><a href="findings/">Findings</a></h3><p>Cross-paper propositions retained with an explicit evidence base.</p></article><article class="collection-card"><h3><a href="gaps/">Gaps</a></h3><p>Institutional questions that multiple reviews expose but do not resolve.</p></article></div></section>
<section><div class="section-heading"><div><div class="eyebrow">Emerging propositions</div><h2>What the archive is beginning to establish</h2></div><a href="findings/">All findings</a></div><div class="card-grid review-grid">{cards(findings[:3],'Cross-paper finding','knowledge/index.html')}</div></section>
<section id="themes"><div class="section-heading"><div><div class="eyebrow">Recurring mechanisms</div><h2>Governance themes</h2></div></div><div class="card-grid collection-grid">{theme_cards}</div></section>
<section><div class="section-heading"><div><div class="eyebrow">Research agenda</div><h2>What remains unresolved</h2></div><a href="gaps/">All gaps</a></div><div class="card-grid review-grid">{cards(gaps[:3],'Open governance gap','knowledge/index.html')}</div></section>'''
    (DOCS/"index.html").write_text(shell("Knowledge Map",body,"knowledge/index.html"),encoding="utf-8")
    for f,spec in facets.items():
        d=DOCS/"facets"/f; d.mkdir(parents=True,exist_ok=True); pp=f"knowledge/facets/{f}/index.html"; p=prefix(pp); matches=[x for x,item in meta.items() if f in (item.get('governance_facets') or [])]
        rc="".join(f"<article class='review-card'><h3><a href='{review_url(x,p)}'>{html.escape(title(x))}</a></h3><div class='card-actions'><a href='{review_url(x,p)}'>Read review</a></div></article>" for x in matches)
        b=f"<section class='page-header'><div class='eyebrow'>Governance theme</div><h1>{html.escape(f.replace('-',' ').title())}</h1><p>{html.escape(str(spec.get('description','')))}</p></section><section><div class='card-grid review-grid'>{rc or '<p class=note>No enriched reviews currently carry this theme.</p>'}</div></section>"
        (d/"index.html").write_text(shell(f"Governance theme: {f}",b,pp),encoding="utf-8")
    rd=DOCS/"relationships"; rd.mkdir(parents=True,exist_ok=True); pp="knowledge/relationships/index.html"; p=prefix(pp)
    rc="".join(f"<article class='review-card'><div class='eyebrow'>{html.escape(e['type'].replace('-',' '))}</div><h3><a href='{review_url(e['from'],p)}'>{html.escape(title(e['from']))}</a> → <a href='{review_url(e['to'],p)}'>{html.escape(title(e['to']))}</a></h3><p>{html.escape(e.get('rationale',''))}</p></article>" for e in rel)
    (rd/"index.html").write_text(shell("Curated review relationships",f"<section class='page-header'><div class='eyebrow'>Connections</div><h1>Curated review relationships</h1><p>Every edge is an editorial claim with a rationale, not an automatically inferred similarity.</p></section><section><div class='card-grid review-grid'>{rc}</div></section>",pp),encoding="utf-8")
    for slug,items,label,intro in [("findings",findings,"Cross-paper finding","Propositions synthesized from multiple canonical reviews. Each finding exposes its evidence base and remains revisable as the archive grows."),("gaps",gaps,"Open governance gap","Questions the archive repeatedly exposes but does not yet resolve. Gaps are research agenda items, not claims that no answer exists elsewhere.")]:
        d=DOCS/slug; d.mkdir(parents=True,exist_ok=True); pp=f"knowledge/{slug}/index.html"; b=f"<section class='page-header'><div class='eyebrow'>{label}</div><h1>{slug.title()}</h1><p>{intro}</p></section><section><div class='card-grid review-grid'>{cards(items,label,pp)}</div></section>"; (d/"index.html").write_text(shell(slug.title(),b,pp),encoding="utf-8")
    for src in synth:
        d=DOCS/"synthesis"/src.stem; d.mkdir(parents=True,exist_ok=True); pp=f"knowledge/synthesis/{src.stem}/index.html"; b=f"<section class='page-header'><div class='eyebrow'>Collection synthesis</div><h1>{html.escape(src.stem.replace('-',' ').title())}</h1></section><article class='review-page prose'>{md_basic(src.read_text(encoding='utf-8'))}</article>"; (d/"index.html").write_text(shell(src.stem.replace('-',' ').title(),b,pp),encoding="utf-8")
    print(f"Generated knowledge pages: {len(facets)} themes, {len(rel)} relationships, {len(findings)} findings, {len(gaps)} gaps, {len(synth)} syntheses")
    return 0
if __name__ == "__main__": raise SystemExit(main())
