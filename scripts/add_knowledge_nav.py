#!/usr/bin/env python3
"""Add the Knowledge entry to generated discovery-site navigation.

This is a bounded post-generation step until the primary discovery generator and
knowledge generator share a common site-shell module. It preserves the relative
prefix used by each generated page and is idempotent.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

ARCHIVE_LINK = re.compile(r'(<a href="(?P<prefix>(?:\.\./)*)archive/">Archive</a>)')


def main() -> None:
    changed = 0
    for path in DOCS.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if ">Knowledge</a>" in text:
            continue

        def replacement(match: re.Match[str]) -> str:
            prefix = match.group("prefix")
            return f'{match.group(1)}\n        <a href="{prefix}knowledge/">Knowledge</a>'

        updated, count = ARCHIVE_LINK.subn(replacement, text, count=1)
        if count:
            path.write_text(updated, encoding="utf-8")
            changed += 1

    print(f"Knowledge navigation added to {changed} generated page(s).")


if __name__ == "__main__":
    main()
