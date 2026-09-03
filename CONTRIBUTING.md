# Contributing

## Who maintains this repository

This repository is maintained by a single curator. Reviews reflect one practitioner's reading and judgment, not institutional consensus.

The repository is maintained with assistance from AI/LLM systems. See [`AI-USAGE.md`](AI-USAGE.md) for the disclosure, permitted assistance, source-grounding requirements, and the boundary between machine assistance and human editorial responsibility.

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

Copy the template from `templates/review-template.md`. The canonical review fields remain required except `scholarly_signal`, which applies only to arXiv papers or other preprints that carry an arXiv subject classification.

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

Archive as Knowledge Infrastructure adds optional fields for provenance, review state, and governance discovery. Omit an optional field rather than guess its value. The canonical semantics are defined in `knowledge/schema.yml`.

```yaml
published: "YYYY-MM-DD"          # optional
# doi: null                      # null = checked and none identified; omission = not yet enriched
peer_review_status: "preprint"   # optional controlled value
paper_type: "preprint"           # optional controlled value
paper_version: "arXiv v1"        # optional source-version label
review_status: "current"         # current | corrected | superseded
governance_facets: ["authority", "delegation"]
```

Historical reviews do not need speculative backfill. `knowledge/review-metadata.yml` provides a curated migration surface for older reviews when enrichment is reliable.

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

Exit code is non-zero if any error-level finding exists. CI runs this on every pull request and blocks the merge on errors. Warnings cover bounded repository heuristics such as tag count outside 3-6, body length outside the expected band, filename/`date_read` mismatches, duplicate-paper signals, and tags not found in the controlled vocabulary. Prose judgment remains a human editorial responsibility described in `editorial-standards.md`.

The linter retains `--strict-schema` as an experimental preview for legacy provenance migration. The live Archive as Knowledge Infrastructure semantics are now documented in `knowledge/schema.yml`, not inferred from the editorial principles.

### Knowledge-layer validation

Changes under `knowledge/`, `collections/syntheses/`, or optional knowledge metadata should also pass:

```bash
python scripts/knowledge_lint.py
```

This validates controlled governance facets, review references, relationship types and rationales, review-state values, and synthesis traceability. It checks structure and referential integrity rather than deciding whether an editorial interpretation is correct.

Governance facets are defined in `knowledge/governance-facets.yml`. A facet indicates substantive treatment of a governance mechanism or institutional tension. It must not be assigned by keyword occurrence alone. AI/LLM systems may propose candidate facets or relationships, but canonical assignments require human editorial acceptance under `AI-USAGE.md`.

Curated review relationships live in `knowledge/relationships.yml`. Relationship edges are editorial claims and therefore require an explicit rationale. Generated semantic similarity is not sufficient for a canonical edge.

### Collection synthesis

Collection-level synthesis lives under `collections/syntheses/`. A synthesis must identify its constituent `source_reviews`, carry a `last_reviewed` date and status, and include a `## Traceability` section. Synthesis may be produced with AI/LLM assistance, but it remains a human-edited analytical artifact. Claims should remain traceable to constituent reviews and, through them, to the underlying papers.

### Corrections and supersession

The reader-facing policy for paper versions, substantive review corrections, supersession, withdrawal and retraction is documented in `knowledge/history-policy.md`. Do not silently rewrite analysis when the evidentiary basis changes materially. Use a new review version when the paper or interpretation changes enough to make the earlier analytical object materially different.

### Rebuilding generated files

Build the normal discovery site and then the knowledge layer:

```bash
python scripts/build_index.py
python scripts/build_knowledge.py
```

To verify the normal generated review site without writing:

```bash
python scripts/build_index.py --check
```

CI runs `editorial_lint.py`, `knowledge_lint.py`, `build_index.py`, `build_knowledge.py`, and the reproducibility check on pull requests. GitHub Pages independently rebuilds both discovery layers from canonical source files before deployment.

### What to commit

Commit canonical review files and other hand-authored or human-accepted source changes. Generated discovery files are automation-owned unless a generated diff is deliberately included for review. Canonical knowledge sources are the files under `knowledge/`, `collections/syntheses/`, and any accepted optional metadata in review front matter. Generated Pages artifacts are discovery surfaces and must not become accidental sources of truth.
