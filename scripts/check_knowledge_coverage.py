#!/usr/bin/env python3
"""Ensure Knowledge discovery covers every current archive review exactly once.

Curated facets/findings/syntheses are intentionally partial and are not
conflated with complete source review discovery.
"""
from __future__ import annotations

from pathlib import Path

import build_index
import build_knowledge

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    published = build_index.load_reviews(build_index.load_taxonomy())
    knowledge = build_knowledge.load_reviews()
    current = {
        path for path, meta in knowledge.items()
        if meta.get("review_status") != "superseded"
    }
    published_paths = {record.review_path for record in published}
    if published_paths != current:
        raise SystemExit(
            "Knowledge and archive review sets differ: "
            f"missing in archive={sorted(current - published_paths)}; "
            f"missing in knowledge={sorted(published_paths - current)}"
        )

    urls = [record.html_url for record in published]
    if len(urls) != len(set(urls)):
        raise SystemExit("Multiple current reviews would write to the same public review URL")

    directory = ROOT / "docs" / "knowledge" / "reviews" / "index.html"
    if not directory.exists():
        raise SystemExit("Knowledge full-review directory is missing")
    page = directory.read_text(encoding="utf-8")
    for url in urls:
        target = f"href='../../{url}'"
        if page.count(target) != 1:
            raise SystemExit(f"Knowledge directory must link current review exactly once: {target}")

    superseded = len(knowledge) - len(current)
    print(
        f"Knowledge coverage verified: {len(published)} current reviews, "
        f"{superseded} historical versions excluded, {len(set(urls))} unique public review URLs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
