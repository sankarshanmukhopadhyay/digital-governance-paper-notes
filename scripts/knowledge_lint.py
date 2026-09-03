#!/usr/bin/env python3
"""Validate Archive as Knowledge Infrastructure source files."""
from __future__ import annotations

import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
FACETS = ROOT / "knowledge" / "governance-facets.yml"
SCHEMA = ROOT / "knowledge" / "schema.yml"
META = ROOT / "knowledge" / "review-metadata.yml"
REL = ROOT / "knowledge" / "relationships.yml"
SYNTH = ROOT / "collections" / "syntheses"


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def main() -> int:
    errors: list[str] = []
    facet_doc = load(FACETS)
    schema = load(SCHEMA)
    metadata = load(META)
    relationships = load(REL)

    facets = set((facet_doc.get("facets") or {}).keys())
    relation_types = set(schema.get("relationship_types") or [])
    review_meta = metadata.get("reviews") or {}

    for review_path, item in review_meta.items():
        p = ROOT / review_path
        if not p.exists():
            errors.append(f"metadata references missing review: {review_path}")
            continue
        for facet in item.get("governance_facets") or []:
            if facet not in facets:
                errors.append(f"{review_path}: unknown governance facet '{facet}'")
        status = item.get("review_status", "current")
        if status not in {"current", "corrected", "superseded"}:
            errors.append(f"{review_path}: invalid review_status '{status}'")

    for edge in relationships.get("relationships") or []:
        src = str(edge.get("from", ""))
        dst = str(edge.get("to", ""))
        typ = str(edge.get("type", ""))
        rationale = str(edge.get("rationale", "")).strip()
        if typ not in relation_types:
            errors.append(f"relationship {src} -> {dst}: unknown type '{typ}'")
        if src == dst:
            errors.append(f"relationship self-link is invalid: {src}")
        for endpoint in (src, dst):
            if not endpoint or not (ROOT / endpoint).exists():
                errors.append(f"relationship references missing review: {endpoint}")
        if not rationale:
            errors.append(f"relationship {src} -> {dst}: rationale is required")

    for path in sorted(SYNTH.glob("*.md")):
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
        for review_path in fm.get("source_reviews") or []:
            if not (ROOT / review_path).exists():
                errors.append(f"{path.relative_to(ROOT)}: missing source review {review_path}")
        if "## Traceability" not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing Traceability section")

    if errors:
        print("Knowledge-layer validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Knowledge layer valid: {len(review_meta)} enriched reviews, {len(relationships.get('relationships') or [])} relationships, {len(facets)} facets, {len(list(SYNTH.glob('*.md')))} syntheses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
