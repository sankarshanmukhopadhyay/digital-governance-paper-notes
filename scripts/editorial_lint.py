#!/usr/bin/env python3
"""Editorial lint for Digital Governance Paper Notes.

Enforces machine-verifiable repository conventions documented in
CONTRIBUTING.md, templates/review-template.md, and taxonomy/domains.yml:
front matter completeness, taxonomy conformance, file naming, explicit
style prohibitions, key_insight consistency, body length bounds, and
duplicate-paper detection.

The linter deliberately does not attempt substantive editorial judgments
such as claim traceability, steelmanning, comparative positioning, vague
agency, or the quality of governance analysis. Those remain human review
responsibilities described in editorial-standards.md.

Usage:
    python scripts/editorial_lint.py                  # lint all reviews, human-readable report
    python scripts/editorial_lint.py --json            # machine-readable report
    python scripts/editorial_lint.py --strict-schema    # preview experimental provenance
                                                          # fields that are not yet part of the
                                                          # live schema or normal CI gate.
    python scripts/editorial_lint.py path/to/one.md     # lint a single file

Exit code is 1 if any ERROR-level finding exists, 0 otherwise. WARNING-level
findings never fail the run unless --strict is also passed.
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_GLOB = str(REPO_ROOT / "reviews" / "**" / "*.md")
TAXONOMY_PATH = REPO_ROOT / "taxonomy" / "domains.yml"

# ---------------------------------------------------------------------------
# Rule configuration
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = [
    "title", "source", "publication", "date_read", "primary_domain", "tags", "key_insight",
]
OPTIONAL_FIELDS = ["scholarly_signal"]

# Experimental provenance fields for a possible future schema migration.
# These are documented in CONTRIBUTING.md, are not part of the live schema,
# and are reported only under --strict-schema.
PROPOSED_FIELDS = ["published", "doi", "affiliation", "peer_review_status", "paper_type"]

FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})__([a-z0-9-]+)__v(\d+)\.md$")

MIN_TAGS, MAX_TAGS = 3, 6

# Char-count band. Wide by design: the archive currently runs ~2,700-3,400
# chars against a template that nominally targets ~2,000. This flags true
# outliers (near-empty stubs, runaway drafts) without re-litigating the
# template-length question, which is an editorial decision, not a lint rule.
MIN_CHARS, MAX_CHARS = 1200, 6000

EM_DASH_CHARS = ["\u2014", "\u2013\u2013"]  # em dash; doubled en dash used as a stand-in

# Phrase -> note. Matched case-insensitively as whole-word/phrase boundaries.
# Keep this list deliberately small and high-precision: arguable prose choices
# belong to human editorial review, not lexical lint heuristics.
BANNED_PHRASES = {
    r"it is worth noting": "hedge phrase",
    r"\bimportantly\b": "hedge phrase",
    r"\bin conclusion\b": "hedge phrase",
    r"this paper makes a significant contribution": "empty praise",
    r"\bdelves into\b": "filler verb",
    r"\bnavigates\b": "filler verb",
    r"\bunpacks\b": "filler verb",
    r"sheds light on": "filler phrase",
    r"a nuanced approach": "filler phrase",
    r"\brobust\b": "banned adjective",
}

@dataclass
class Finding:
    level: str  # "ERROR" | "WARNING"
    rule: str
    message: str
    line: Optional[int] = None


@dataclass
class FileReport:
    path: str
    findings: List[Finding] = field(default_factory=list)

    def add(self, level: str, rule: str, message: str, line: Optional[int] = None) -> None:
        self.findings.append(Finding(level, rule, message, line))

    @property
    def errors(self) -> List[Finding]:
        return [f for f in self.findings if f.level == "ERROR"]

    @property
    def warnings(self) -> List[Finding]:
        return [f for f in self.findings if f.level == "WARNING"]


def load_taxonomy() -> Tuple[List[str], List[str]]:
    data = yaml.safe_load(TAXONOMY_PATH.read_text(encoding="utf-8"))
    return data.get("primary_domains", []), data.get("secondary_topics", [])


def split_front_matter(text: str) -> Tuple[Optional[dict], str, int]:
    """Return (front_matter_dict_or_None, body_text, body_start_line)."""
    if not text.startswith("---"):
        return None, text, 1
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text, 1
    raw_fm, body = parts[1], parts[2]
    try:
        fm = yaml.safe_load(raw_fm) or {}
    except yaml.YAMLError:
        fm = None
    body_start_line = raw_fm.count("\n") + 3  # two "---" lines plus 1-index
    return fm, body.lstrip("\n"), body_start_line


def check_filename(path: Path, fm: dict, report: FileReport) -> None:
    m = FILENAME_RE.match(path.name)
    if not m:
        report.add("ERROR", "filename", f"'{path.name}' does not match YYYY-MM-DD__slug__vN.md")
        return
    date_in_name = m.group(1)
    date_read = str(fm.get("date_read", "")) if fm else ""
    if date_read and date_in_name != date_read:
        report.add(
            "WARNING", "filename-date-mismatch",
            f"filename date {date_in_name} != date_read {date_read}",
        )


def check_required_fields(fm: Optional[dict], report: FileReport) -> None:
    if fm is None:
        report.add("ERROR", "front-matter", "missing or unparsable YAML front matter")
        return
    for f in REQUIRED_FIELDS:
        if f not in fm or fm[f] in (None, "", [], {}):
            report.add("ERROR", "required-field", f"missing or empty required field: {f}")


def check_strict_schema(fm: Optional[dict], report: FileReport) -> None:
    if fm is None:
        return
    for f in PROPOSED_FIELDS:
        if f not in fm or fm[f] in (None, "", [], {}):
            report.add(
                "WARNING", "proposed-field-missing",
                f"provenance field not yet present: {f} (Phase 2 schema migration)",
            )


def check_taxonomy(fm: Optional[dict], primary_domains: List[str], secondary_topics: List[str],
                    report: FileReport) -> None:
    if fm is None:
        return
    domain = fm.get("primary_domain")
    if domain and domain not in primary_domains:
        report.add("ERROR", "taxonomy-domain", f"primary_domain '{domain}' not in taxonomy/domains.yml")

    tags = fm.get("tags") or []
    if not isinstance(tags, list):
        report.add("ERROR", "tags-type", "tags field is not a list")
        tags = []
    if not (MIN_TAGS <= len(tags) <= MAX_TAGS):
        report.add("WARNING", "tag-count", f"{len(tags)} tags, expected {MIN_TAGS}-{MAX_TAGS}")
    for t in tags:
        if t not in secondary_topics and t != domain:
            report.add("WARNING", "tag-not-in-taxonomy", f"tag '{t}' not found in taxonomy/domains.yml")


def check_key_insight_duplication(fm: Optional[dict], body: str, report: FileReport) -> None:
    if not fm:
        return
    ki = (fm.get("key_insight") or "").strip()
    if not ki:
        return
    # Body already has its own "## Key Insight" section that legitimately
    # repeats the front-matter field per CONTRIBUTING.md ("keep them
    # identical"). Only flag if it ALSO appears verbatim inside the
    # "## Review" section, which would be true duplication.
    review_section = body.split("## Key Insight")[0]
    normalized_body = re.sub(r"\s+", " ", review_section).lower()
    normalized_ki = re.sub(r"\s+", " ", ki).lower()
    if normalized_ki and normalized_ki in normalized_body:
        report.add(
            "WARNING", "key-insight-duplicated",
            "key_insight text also appears verbatim inside the Review section",
        )


def check_key_insight_identity(fm: Optional[dict], body: str, report: FileReport) -> None:
    """CONTRIBUTING.md: the front-matter key_insight and the body's
    '## Key Insight' section must be identical, not paraphrases of each other."""
    if not fm:
        return
    ki = (fm.get("key_insight") or "").strip()
    if not ki or "## Key Insight" not in body:
        return
    def normalize(s: str) -> str:
        s = re.sub(r"\s+", " ", s).strip()
        # YAML double-quoted scalars need an escaped straight quote; body
        # prose renders curly quotes. Normalize both to a single form so a
        # typographic difference isn't reported as a content mismatch.
        s = s.replace('\\"', '"')
        for a, b in (("\u201c", '"'), ("\u201d", '"'), ("\u2018", "'"), ("\u2019", "'")):
            s = s.replace(a, b)
        return s

    body_ki = normalize(body.split("## Key Insight", 1)[1])
    normalized_fm = normalize(ki)
    if body_ki != normalized_fm:
        report.add(
            "ERROR", "key-insight-mismatch",
            "front-matter key_insight and body '## Key Insight' text differ; CONTRIBUTING.md requires them identical",
        )


def check_char_count(body: str, report: FileReport) -> None:
    review_only = body.split("## Key Insight")[0]
    n = len(review_only.strip())
    if n < MIN_CHARS or n > MAX_CHARS:
        report.add("WARNING", "length", f"review body is {n} chars, outside {MIN_CHARS}-{MAX_CHARS} band")


def check_em_dash(body: str, report: FileReport) -> None:
    for i, line in enumerate(body.splitlines(), start=1):
        for ch in EM_DASH_CHARS:
            if ch in line:
                report.add("ERROR", "em-dash", "em dash present", line=i)


def check_banned_phrases(body: str, report: FileReport) -> None:
    for i, line in enumerate(body.splitlines(), start=1):
        for pattern, note in BANNED_PHRASES.items():
            if re.search(pattern, line, re.IGNORECASE):
                report.add("ERROR", "banned-phrase", f"'{pattern}' ({note})", line=i)


def lint_file(path: Path, primary_domains: List[str], secondary_topics: List[str],
              strict_schema: bool) -> FileReport:
    report = FileReport(path=str(path.relative_to(REPO_ROOT)))
    text = path.read_text(encoding="utf-8")
    fm, body, _ = split_front_matter(text)

    check_filename(path, fm or {}, report)
    check_required_fields(fm, report)
    if strict_schema:
        check_strict_schema(fm, report)
    check_taxonomy(fm, primary_domains, secondary_topics, report)
    check_key_insight_duplication(fm, body, report)
    check_key_insight_identity(fm, body, report)
    check_char_count(body, report)
    check_em_dash(body, report)
    check_banned_phrases(body, report)
    return report


def check_duplicates(paths: List[Path]) -> List[Finding]:
    seen_titles: Dict[str, str] = {}
    seen_sources: Dict[str, str] = {}
    findings: List[Finding] = []
    for p in paths:
        fm, _, _ = split_front_matter(p.read_text(encoding="utf-8"))
        if not fm:
            continue
        title = re.sub(r"\s+", " ", str(fm.get("title", "")).strip().lower())
        source = str(fm.get("source", "")).strip().lower()
        rel = str(p.relative_to(REPO_ROOT))
        if title:
            if title in seen_titles and seen_titles[title] != rel:
                findings.append(Finding(
                    "WARNING", "duplicate-title",
                    f"title also used in {seen_titles[title]}",
                ))
            else:
                seen_titles[title] = rel
        if source:
            if source in seen_sources and seen_sources[source] != rel:
                findings.append(Finding(
                    "WARNING", "duplicate-source",
                    f"source also used in {seen_sources[source]}",
                ))
            else:
                seen_sources[source] = rel
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="Editorial lint for review files.")
    ap.add_argument("paths", nargs="*", help="Specific review files to lint (default: all)")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON report")
    ap.add_argument("--strict-schema", action="store_true",
                     help="Preview missing experimental provenance fields (warnings)")
    ap.add_argument("--strict", action="store_true",
                     help="Treat warnings as failing the run too")
    args = ap.parse_args()

    primary_domains, secondary_topics = load_taxonomy()

    if args.paths:
        paths = [Path(p).resolve() for p in args.paths]
    else:
        paths = sorted(Path(p) for p in glob.glob(REVIEWS_GLOB, recursive=True))

    reports = [lint_file(p, primary_domains, secondary_topics, args.strict_schema) for p in paths]

    dup_findings = check_duplicates(paths)
    if dup_findings:
        dup_report = FileReport(path="(cross-file)", findings=dup_findings)
        reports.append(dup_report)

    total_errors = sum(len(r.errors) for r in reports)
    total_warnings = sum(len(r.warnings) for r in reports)

    if args.json:
        payload = [
            {
                "path": r.path,
                "findings": [
                    {"level": f.level, "rule": f.rule, "message": f.message, "line": f.line}
                    for f in r.findings
                ],
            }
            for r in reports if r.findings
        ]
        print(json.dumps({
            "files_checked": len(paths),
            "errors": total_errors,
            "warnings": total_warnings,
            "reports": payload,
        }, indent=2))
    else:
        for r in reports:
            if not r.findings:
                continue
            print(f"\n{r.path}")
            for f in sorted(r.findings, key=lambda x: (x.level != "ERROR", x.line or 0)):
                loc = f":{f.line}" if f.line else ""
                print(f"  [{f.level}] {f.rule}{loc}: {f.message}")
        print(f"\n{len(paths)} files checked, {total_errors} errors, {total_warnings} warnings")

    if total_errors > 0:
        return 1
    if args.strict and total_warnings > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
