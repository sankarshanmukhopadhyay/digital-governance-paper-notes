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

Commit your review file. The CI pipeline (`rebuild-index.yml`) handles regenerating `index.md`, `docs/index.html`, and the README recent-reviews block, and auto-commits those changes. If you ran the build script locally, commit the generated files together with the review in a single commit.
