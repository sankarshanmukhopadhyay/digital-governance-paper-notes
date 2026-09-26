#!/usr/bin/env python3
"""Validate Archive as Knowledge Infrastructure source files."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

from build_index import parse_front_matter

ROOT = Path(__file__).resolve().parent.parent
K = ROOT / "knowledge"
SYNTH = ROOT / "collections" / "syntheses"
REVIEWS = ROOT / "reviews"
COLLECTIONS = ROOT / "collections" / "collections.json"


def load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def main():
    errors = []
    facets = set((load(K / "governance-facets.yml").get("facets") or {}).keys())
    schema = load(K / "schema.yml")
    metadata = load(K / "review-metadata.yml")
    relationships = load(K / "relationships.yml")
    findings = load(K / "findings.yml").get("findings") or []
    gaps = load(K / "gaps.yml").get("gaps") or []
    relation_types = set(schema.get("relationship_types") or [])
    review_meta = metadata.get("reviews") or {}
    collections = json.loads(COLLECTIONS.read_text(encoding="utf-8")).get("collections", []) if COLLECTIONS.exists() else []
    collection_slugs = {str(x.get("slug")) for x in collections}

    all_reviews = {}
    mapped = set()
    for path in sorted(REVIEWS.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        fm = parse_front_matter(path.read_text(encoding="utf-8"))
        all_reviews[rel] = fm
        for facet in fm.get("governance_facets") or []:
            if facet not in facets:
                errors.append(f"{rel}: unknown governance facet '{facet}'")
            else:
                mapped.add(rel)
        if fm.get("review_status", "current") not in {"current", "corrected", "superseded"}:
            errors.append(f"{rel}: invalid review_status")

    for review_path, item in review_meta.items():
        if review_path not in all_reviews:
            errors.append(f"metadata references missing review: {review_path}")
        for facet in item.get("governance_facets") or []:
            if facet not in facets:
                errors.append(f"{review_path}: unknown governance facet '{facet}'")
            else:
                mapped.add(review_path)
        if item.get("review_status", "current") not in {"current", "corrected", "superseded"}:
            errors.append(f"{review_path}: invalid review_status")

    seen_edges = set()
    for edge in relationships.get("relationships") or []:
        src = str(edge.get("from", ""))
        dst = str(edge.get("to", ""))
        typ = str(edge.get("type", ""))
        rationale = str(edge.get("rationale", "")).strip()
        key = (src, typ, dst)
        if key in seen_edges:
            errors.append(f"duplicate relationship: {src} {typ} {dst}")
        seen_edges.add(key)
        if typ not in relation_types:
            errors.append(f"relationship {src} -> {dst}: unknown type '{typ}'")
        if src == dst:
            errors.append(f"relationship self-link is invalid: {src}")
        for endpoint in (src, dst):
            if not endpoint or endpoint not in all_reviews:
                errors.append(f"relationship references missing review: {endpoint}")
        if not rationale:
            errors.append(f"relationship {src} -> {dst}: rationale is required")

    for kind, items, required in (
        ("finding", findings, ("id", "title", "claim", "rationale", "source_reviews")),
        ("gap", gaps, ("id", "title", "gap", "why_it_matters", "source_reviews")),
    ):
        ids = set()
        for item in items:
            ident = str(item.get("id", "")).strip()
            if not ident:
                errors.append(f"{kind}: id is required")
            elif ident in ids:
                errors.append(f"{kind}: duplicate id '{ident}'")
            ids.add(ident)
            for field in required:
                if not item.get(field):
                    errors.append(f"{kind} {ident or '<unknown>'}: missing {field}")
            sources = item.get("source_reviews") or []
            if kind == "finding" and len(sources) < 2:
                errors.append(f"finding {ident}: cross-paper finding requires at least two source reviews")
            if len(sources) != len(set(sources)):
                errors.append(f"{kind} {ident}: duplicate source review")
            for review_path in sources:
                if review_path not in all_reviews:
                    errors.append(f"{kind} {ident}: missing source review {review_path}")
            for facet in item.get("facets") or []:
                if facet not in facets:
                    errors.append(f"{kind} {ident}: unknown governance facet '{facet}'")

    synthesis_count = 0
    for path in sorted(SYNTH.glob("*.md")):
        synthesis_count += 1
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"{path.relative_to(ROOT)}: missing YAML front matter")
            continue
        try:
            _, raw, _ = text.split("---", 2)
            fm = yaml.safe_load(raw) or {}
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid front matter: {exc}")
            continue
        for field in ("title", "collection", "last_reviewed", "status", "source_reviews"):
            if not fm.get(field):
                errors.append(f"{path.relative_to(ROOT)}: missing {field}")
        if fm.get("collection") and fm.get("collection") not in collection_slugs:
            errors.append(f"{path.relative_to(ROOT)}: unknown collection '{fm.get('collection')}'")
        sources = fm.get("source_reviews") or []
        if len(sources) != len(set(sources)):
            errors.append(f"{path.relative_to(ROOT)}: duplicate source review")
        for review_path in sources:
            if review_path not in all_reviews:
                errors.append(f"{path.relative_to(ROOT)}: missing source review {review_path}")
        if "## Traceability" not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing Traceability section")

    if errors:
        print("Knowledge-layer validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Knowledge layer valid: {len(all_reviews)} reviews, {len(mapped)} knowledge-mapped reviews, "
        f"{len(relationships.get('relationships') or [])} relationships, {len(facets)} facets, "
        f"{len(findings)} findings, {len(gaps)} gaps, {synthesis_count} syntheses"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
