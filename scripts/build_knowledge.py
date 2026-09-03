#!/usr/bin/env python3
"""Generate static Archive as Knowledge Infrastructure discovery pages."""
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
    m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', text, re.M)
    return m.group(1).strip() if m else Path(path).stem


def page(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title><style>body{{font-family:system-ui,sans-serif;max-width:980px;margin:40px auto;padding:0 20px;line-height:1.55}}nav{{margin-bottom:24px}}code{{background:#f3f3f3;padding:2px 4px}}.meta{{color:#555}}li{{margin:.45rem 0}}a{{color:inherit}}</style></head><body><nav><a href='../../'>Digital Governance Paper Notes</a> · <a href='../'>Knowledge Infrastructure</a></nav><h1>{html.escape(title)}</h1>{body}</body></html>"""


def md_basic(text: str) -> str:
    text = re.sub(r"(?ms)^---\n.*?\n---\n", "", text, count=1)
    out=[]
    for block in re.split(r"\n\s*\n", text.strip()):
        line=block.strip()
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("- "):
            items="".join(f"<li>{html.escape(x[2:])}</li>" for x in line.splitlines() if x.startswith("- "))
            out.append(f"<ul>{items}</ul>")
        else:
            escaped=html.escape(" ".join(x.strip() for x in line.splitlines()))
            escaped=re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
            escaped=re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
            out.append(f"<p>{escaped}</p>")
    return "\n".join(out)


def main() -> int:
    facets = load_yaml(FACETS).get("facets") or {}
    metadata = load_yaml(META).get("reviews") or {}
    relationships = load_yaml(REL).get("relationships") or []
    DOCS.mkdir(parents=True, exist_ok=True)

    facet_counts={f:0 for f in facets}
    for item in metadata.values():
        for f in item.get("governance_facets") or []:
            facet_counts[f]=facet_counts.get(f,0)+1

    syntheses=sorted(SYNTH.glob("*.md"))
    body="<p>This layer connects reviews across provenance, governance facets, relationships, synthesis and review history. Canonical analytical judgment remains in repository source files; these pages are generated discovery surfaces.</p>"
    body+="<h2>Governance facets</h2><ul>"+"".join(f"<li><a href='facets/{html.escape(f)}/'>{html.escape(f)}</a> ({facet_counts.get(f,0)})</li>" for f in facets)+"</ul>"
    body+="<h2>Relationships</h2><p><a href='relationships/'>Browse curated review relationships</a>.</p>"
    body+="<h2>Collection syntheses</h2><ul>"+"".join(f"<li><a href='synthesis/{p.stem}/'>{html.escape(p.stem.replace('-', ' ').title())}</a></li>" for p in syntheses)+"</ul>"
    body+="<h2>Policies</h2><ul><li><a href='https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/blob/main/AI-USAGE.md'>AI Usage</a></li><li><a href='https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/blob/main/knowledge/history-policy.md'>Corrections and supersession</a></li></ul>"
    (DOCS/"index.html").write_text(page("Archive as Knowledge Infrastructure", body), encoding="utf-8")

    for facet, spec in facets.items():
        target=DOCS/"facets"/facet
        target.mkdir(parents=True, exist_ok=True)
        matches=[p for p,item in metadata.items() if facet in (item.get("governance_facets") or [])]
        b=f"<p>{html.escape(str(spec.get('description','')))}</p><ul>"+"".join(f"<li>{html.escape(review_title(p))}<br><span class='meta'><code>{html.escape(p)}</code></span></li>" for p in matches)+"</ul>"
        (target/"index.html").write_text(page(f"Governance facet: {facet}", b), encoding="utf-8")

    rel_dir=DOCS/"relationships"; rel_dir.mkdir(parents=True, exist_ok=True)
    rb="<ul>"+"".join(f"<li><strong>{html.escape(review_title(e['from']))}</strong> <code>{html.escape(e['type'])}</code> <strong>{html.escape(review_title(e['to']))}</strong><br>{html.escape(e.get('rationale',''))}</li>" for e in relationships)+"</ul>"
    (rel_dir/"index.html").write_text(page("Curated review relationships", rb), encoding="utf-8")

    for src in syntheses:
        target=DOCS/"synthesis"/src.stem; target.mkdir(parents=True, exist_ok=True)
        (target/"index.html").write_text(page(src.stem.replace('-', ' ').title(), md_basic(src.read_text(encoding="utf-8"))), encoding="utf-8")

    print(f"Generated knowledge pages: {len(facets)} facets, {len(relationships)} relationships, {len(syntheses)} syntheses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
