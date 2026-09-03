# Contributing

## Who maintains this repository

This repository is maintained by a single curator. Reviews reflect one practitioner's reading and judgment, not institutional consensus.

## Suggesting a paper for review

If you have a paper, report, or essay you would like to see reviewed, open an issue and assign it to the maintainer. It will be triaged into the reading backlog. There is no guarantee of turnaround time.

Please include in the issue:
- Title and author(s)
- A direct link to the paper or a stable URL
- A sentence on why it fits the scope (AI governance, digital public infrastructure, public-interest technology, and adjacent areas — see the taxonomy for the full domain list)

The archive covers globally published work. Papers with a regional focus (South Asia, APAC, Global South, OECD contexts, etc.) are all in scope as long as they speak to the taxonomy.

## Writing a review (for the maintainer)

### File naming

Reviews live under `reviews/YYYY/` and follow this convention:

```
YYYY-MM-DD__paper-slug__v1.md
```

Use the date you finished the review, not the paper's publication date. The slug should be a lowercase, hyphen-separated short title — enough to be identifiable in a file list.

### Front matter

Copy the template from `templates/review-template.md`. All fields are required except `scholarly_signal`, which applies only to arXiv papers or other preprints that carry an arXiv subject classification.

```yaml
---
title: ""
source: ""
publication: ""
date_read: "YYYY-MM-DD"
primary_domain: ""
tags: []
scholarly_signal: ""       # optional; e.g. cs.AI, cs.CY
key_insight: ""
---
```

`primary_domain` and `tags` must use values from `taxonomy/domains.yml`. If you need a new domain or tag, update the taxonomy file in the same commit.

### Review body

The review body should contain two sections, in this order:

```markdown
# Paper Review

## Review

<up to ~2000 characters: main argument, what the paper does well, its limitations, why it matters for practitioners>

## Key Insight

<one sentence that captures the single most durable takeaway>
```

The key insight line is also stored in the front matter `key_insight` field — keep them identical.

### Editorial lint

Before rebuilding the index, run the repository linter. It checks machine-verifiable contribution rules: front matter completeness, taxonomy conformance, file naming, the em dash and a deliberately small high-precision banned-phrase list, `key_insight` identity between front matter and the body's `## Key Insight` section, body length, and duplicate papers across the archive:

```bash
python scripts/editorial_lint.py
```

Exit code is non-zero if any error-level finding exists. CI runs this on every pull request and blocks the merge on errors. Warnings cover bounded repository heuristics such as tag count outside 3-6, body length outside the expected band, filename/`date_read` mismatches, duplicate-paper signals, and tags not found in the controlled vocabulary. The linter intentionally does not flag words such as `ecosystem` or attempt to infer whether `leverage` is stylistically weak; those are prose judgments for a human reviewer. CI then builds the generated discovery site in the runner and verifies that a second `--check` pass is clean. Review PRs therefore do not need to carry generated index or Pages files merely to satisfy CI. The intellectual standards for reading and critique are described separately in `editorial-standards.md`; this file and the repository tooling remain the source of truth for contribution mechanics and automated checks.

To see a single file's findings:

```bash
python scripts/editorial_lint.py reviews/2026/2026-03-05__some-review__v1.md
```

The linter also retains an explicitly experimental schema preview for possible future provenance fields: `published`, `doi`, `affiliation`, `peer_review_status`, and `paper_type`. These fields are not part of the live template and do not participate in normal CI. Use the preview only to inspect the impact of a future schema decision:

```bash
python scripts/editorial_lint.py --strict-schema
```

### Rebuilding generated files

After writing or editing a review, rebuild the generated index files locally before committing:

```bash
python scripts/build_index.py
```

To verify without writing:

```bash
python scripts/build_index.py --check
```

CI will also rebuild generated files automatically on push to `main` if `reviews/` or `scripts/build_index.py` changed. You only need to run locally if you want to preview changes before pushing.

### What to commit

Commit the review file and any hand-authored source changes. Generated discovery files are automation-owned: pull-request CI builds them ephemerally to validate generation, `rebuild-index.yml` refreshes and persists them on `main`, and the Pages workflow builds its deployment artifact directly from the merged review sources. If you deliberately ran the generator locally and want the generated diff reviewed in the same PR, it is still acceptable to commit those files together, but it is no longer required for a review-only change.
