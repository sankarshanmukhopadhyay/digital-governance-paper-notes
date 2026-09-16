#!/usr/bin/env python3
"""Validate Archive as Knowledge Infrastructure source files."""
from __future__ import annotations
import sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent.parent
K=ROOT/"knowledge"; SYNTH=ROOT/"collections"/"syntheses"
def load(p): return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
def main():
    errors=[]; facets=set((load(K/"governance-facets.yml").get("facets") or {}).keys()); schema=load(K/"schema.yml"); metadata=load(K/"review-metadata.yml"); relationships=load(K/"relationships.yml"); findings=load(K/"findings.yml").get("findings") or []; gaps=load(K/"gaps.yml").get("gaps") or []
    relation_types=set(schema.get("relationship_types") or []); review_meta=metadata.get("reviews") or {}
    for review_path,item in review_meta.items():
        if not (ROOT/review_path).exists(): errors.append(f"metadata references missing review: {review_path}")
        for facet in item.get("governance_facets") or []:
            if facet not in facets: errors.append(f"{review_path}: unknown governance facet '{facet}'")
        if item.get("review_status","current") not in {"current","corrected","superseded"}: errors.append(f"{review_path}: invalid review_status")
    for edge in relationships.get("relationships") or []:
        src=str(edge.get("from","")); dst=str(edge.get("to","")); typ=str(edge.get("type","")); rationale=str(edge.get("rationale","")).strip()
        if typ not in relation_types: errors.append(f"relationship {src} -> {dst}: unknown type '{typ}'")
        if src==dst: errors.append(f"relationship self-link is invalid: {src}")
        for endpoint in (src,dst):
            if not endpoint or not (ROOT/endpoint).exists(): errors.append(f"relationship references missing review: {endpoint}")
        if not rationale: errors.append(f"relationship {src} -> {dst}: rationale is required")
    for kind,items,required in (("finding",findings,("id","title","claim","rationale","source_reviews")),("gap",gaps,("id","title","gap","why_it_matters","source_reviews"))):
        ids=set()
        for item in items:
            ident=str(item.get("id","")).strip()
            if not ident: errors.append(f"{kind}: id is required")
            elif ident in ids: errors.append(f"{kind}: duplicate id '{ident}'")
            ids.add(ident)
            for field in required:
                if not item.get(field): errors.append(f"{kind} {ident or '<unknown>'}: missing {field}")
            sources=item.get("source_reviews") or []
            if kind=="finding" and len(sources)<2: errors.append(f"finding {ident}: cross-paper finding requires at least two source reviews")
            for review_path in sources:
                if not (ROOT/review_path).exists(): errors.append(f"{kind} {ident}: missing source review {review_path}")
    for path in sorted(SYNTH.glob("*.md")):
        text=path.read_text(encoding="utf-8")
        if not text.startswith("---\n"): errors.append(f"{path.relative_to(ROOT)}: missing YAML front matter"); continue
        try: _,raw,_=text.split("---",2); fm=yaml.safe_load(raw) or {}
        except Exception as exc: errors.append(f"{path.relative_to(ROOT)}: invalid front matter: {exc}"); continue
        for field in ("title","collection","last_reviewed","status","source_reviews"):
            if not fm.get(field): errors.append(f"{path.relative_to(ROOT)}: missing {field}")
        for review_path in fm.get("source_reviews") or []:
            if not (ROOT/review_path).exists(): errors.append(f"{path.relative_to(ROOT)}: missing source review {review_path}")
        if "## Traceability" not in text: errors.append(f"{path.relative_to(ROOT)}: missing Traceability section")
    if errors:
        print("Knowledge-layer validation failed:"); [print(f"- {e}") for e in errors]; return 1
    print(f"Knowledge layer valid: {len(review_meta)} enriched reviews, {len(relationships.get('relationships') or [])} relationships, {len(facets)} facets, {len(findings)} findings, {len(gaps)} gaps, {len(list(SYNTH.glob('*.md')))} syntheses"); return 0
if __name__=="__main__": sys.exit(main())
