#!/usr/bin/env python3
"""Build discovery and knowledge pages through one shared site shell."""
from __future__ import annotations

import argparse
import sys

import build_index
import build_knowledge
from site_shell import relative_prefix, render_page

KNOWLEDGE_DESCRIPTION = (
    "Cross-paper governance discovery, relationships and synthesis from Digital Governance Paper Notes."
)
KNOWLEDGE_FOOTER = (
    "Digital Governance Paper Notes · Governance-first research reviews and cumulative knowledge infrastructure."
)


def review_page_shell(title: str, body: str, path: str, description: str = "") -> str:
    return render_page(title, body, path, description)


def knowledge_page_shell(title: str, body: str, page_path: str, description: str = "") -> str:
    prefix = relative_prefix(page_path)
    breadcrumbs = (
        f'<div class="breadcrumbs"><a href="{prefix}">Home</a> · '
        f'<a href="{prefix}knowledge/">Knowledge</a></div>'
    )
    return render_page(
        title,
        body,
        page_path,
        description or KNOWLEDGE_DESCRIPTION,
        breadcrumbs=breadcrumbs,
        footer=KNOWLEDGE_FOOTER,
    )


def configure_shared_shell() -> None:
    """Make both existing generators use the canonical shell before rendering."""
    build_index.relative_prefix = relative_prefix
    build_index.page_shell = review_page_shell
    build_knowledge.relative_prefix = relative_prefix
    build_knowledge.page = knowledge_page_shell


def run_index(check: bool = False) -> int:
    original = sys.argv[:]
    try:
        sys.argv = ["build_index.py"] + (["--check"] if check else [])
        return build_index.main()
    finally:
        sys.argv = original


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the complete generated discovery site.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify review-site generated output using the shared shell without rebuilding knowledge pages.",
    )
    args = parser.parse_args()
    configure_shared_shell()
    result = run_index(check=args.check)
    if result != 0 or args.check:
        return result
    return build_knowledge.main()


if __name__ == "__main__":
    raise SystemExit(main())
