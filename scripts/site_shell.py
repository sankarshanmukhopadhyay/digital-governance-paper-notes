#!/usr/bin/env python3
"""Shared HTML shell for all generated discovery surfaces."""
from __future__ import annotations

import html
from pathlib import Path

DEFAULT_DESCRIPTION = "Governance-first reviews of research on digital institutions, infrastructure and power."
DEFAULT_FOOTER = "A static, governance-first research index generated from repository metadata."


def relative_prefix(path: str) -> str:
    depth = max(0, len(Path(path).parts) - 1)
    return "../" * depth


def _nav_link(prefix: str, href: str, label: str, active: bool = False) -> str:
    current = ' aria-current="page"' if active else ""
    return f'<a href="{prefix}{href}"{current}>{label}</a>'


def render_page(
    title: str,
    body: str,
    path: str,
    description: str = "",
    *,
    breadcrumbs: str = "",
    footer: str = DEFAULT_FOOTER,
) -> str:
    """Render the canonical discovery-site document shell.

    Relative links are derived from the generated output path. The active primary
    navigation item is inferred from the first path segment so every generated
    surface gets the same navigation semantics without post-processing.
    """
    prefix = relative_prefix(path)
    top = Path(path).parts[0] if Path(path).parts else ""
    nav = "\n        ".join(
        [
            _nav_link(prefix, "#recent", "Recent"),
            _nav_link(prefix, "domains/", "Domains", top == "domains"),
            _nav_link(prefix, "collections/", "Collections", top == "collections"),
            _nav_link(prefix, "archive/", "Archive", top == "archive"),
            _nav_link(prefix, "knowledge/", "Knowledge", top == "knowledge"),
        ]
    )
    desc = description or DEFAULT_DESCRIPTION
    crumb_html = f"\n    {breadcrumbs}" if breadcrumbs else ""
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
        {nav}
      </nav>
    </div>
  </header>
  <main id="main" class="container">{crumb_html}
    {body}
  </main>
  <footer class="site-footer"><div class="container">{html.escape(footer)}</div></footer>
</body>
</html>
"""
