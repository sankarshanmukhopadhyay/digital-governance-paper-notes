# Digital Governance Paper Notes

A curated archive of governance-first reviews of research papers, policy reports, essays, and institutional publications on AI governance, digital public infrastructure, public-interest technology, digital identity, and adjacent governance questions.

**Site:** [sankarshanmukhopadhyay.github.io/digital-governance-paper-notes](https://sankarshanmukhopadhyay.github.io/digital-governance-paper-notes/)

**Knowledge infrastructure:** [sankarshanmukhopadhyay.github.io/digital-governance-paper-notes/knowledge/](https://sankarshanmukhopadhyay.github.io/digital-governance-paper-notes/knowledge/)

**Index:** [index.md](index.md) · **Editorial principles:** [editorial-standards.md](editorial-standards.md) · **AI usage:** [AI-USAGE.md](AI-USAGE.md) · **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## About

These are working notes from a single reader. Reviews ask what a paper actually establishes, what evidence carries the argument, what assumptions bear institutional weight, and how a proposed system redistributes authority, control, dependency, legitimacy and responsibility.

The archive's recurring concern is operational credibility. Governance claims are examined for whether authority, enforcement, revocation, evidence, contestability and redress become implementable rather than remaining principles. That lens is applied only where the paper's mechanism makes those questions material; the paper is read on its own terms first.

The repository is maintained with assistance from AI/LLM systems. The disclosure and responsibility boundary are documented in [AI-USAGE.md](AI-USAGE.md). AI assistance may support extraction, enrichment, comparative retrieval, synthesis and repository work, but canonical editorial judgment remains the responsibility of the human maintainer.

---

## Archive as Knowledge Infrastructure

The archive now has a second layer above individual reviews. It is designed to make accumulated governance knowledge explicit without converting editorial judgment into opaque scores or automatic classifications. Collections organize what to read; the Knowledge layer records accepted cross-paper propositions, material relationships, evidence-backed gaps and synthesis judgments.

- **Provenance and paper state:** optional metadata can record publication state, paper type, source version and review status without forcing speculative backfill.
- **Review relationships:** curated edges record when reviews relate to, extend, challenge or supersede one another. Every canonical edge requires a rationale.
- **Governance facets:** a bounded vocabulary exposes recurring mechanisms such as authority, legitimacy, redress, revocation, delegation, gatekeeping and institutional capacity. Facets are discovery aids, not quality grades.
- **Collection synthesis:** human-edited synthesis artifacts accumulate findings across reviews while retaining traceability to constituent reviews and underlying papers.
- **History and correction:** correction, supersession, withdrawal and review-version semantics are reader-facing rather than hidden only in git history.

Canonical definitions live under [`knowledge/`](knowledge/), collection syntheses under [`collections/syntheses/`](collections/syntheses/), and generated discovery pages under `/knowledge/` on GitHub Pages.

---

## Editorial principles

The archive's human-facing editorial approach is described in [editorial-standards.md](editorial-standards.md). Its central commitments are to read papers on their own terms, distinguish evidence from inference, follow decision rights, separate capability and provenance from authority and legitimacy, surface consequential assumptions, examine contestability and redress where the mechanism makes them material, and pressure-test criticism against the strongest reasonable response.

Repository mechanics remain separate. File naming, front matter, optional knowledge metadata, taxonomy, linting, synthesis traceability and generated outputs are documented in [CONTRIBUTING.md](CONTRIBUTING.md), the review template and repository scripts.

Before opening a pull request, run:

```bash
python scripts/editorial_lint.py
python scripts/knowledge_lint.py
```

---

## Scope

### Taxonomy and live domain counts

The canonical domain taxonomy is defined in [`taxonomy/domains.yml`](taxonomy/domains.yml). Current review counts by domain are generated directly from canonical review metadata and published on the [Domains](https://sankarshanmukhopadhyay.github.io/digital-governance-paper-notes/domains/) page.

The README deliberately does not duplicate live counts. This keeps the protected `main` branch free of generated summary commits while ensuring that the public discovery surface is rebuilt from canonical reviews on every Pages deployment.

The full controlled vocabulary, including secondary topic tags and arXiv scholarly-signal codes, lives in [`taxonomy/domains.yml`](taxonomy/domains.yml). The separate governance-facet vocabulary lives in [`knowledge/governance-facets.yml`](knowledge/governance-facets.yml).

---

## Repository Structure

```text
reviews/YYYY/                   canonical review files, one per paper
collections/collections.json    curated cross-cutting collection rules
collections/syntheses/          human-edited cumulative collection analysis
knowledge/schema.yml            additive knowledge-layer schema semantics
knowledge/review-metadata.yml   curated migration metadata for existing reviews
knowledge/governance-facets.yml bounded governance discovery vocabulary
knowledge/relationships.yml     curated relationships between reviews
knowledge/history-policy.md     corrections and supersession semantics
AI-USAGE.md                     disclosure and responsibility model for AI/LLM assistance
templates/review-template.md    canonical review template
scripts/editorial_lint.py       machine-verifiable review contribution checks
scripts/knowledge_lint.py       knowledge-layer integrity and traceability checks
scripts/build_index.py          normal review/index site generator
scripts/build_knowledge.py      knowledge discovery page generator
docs/                           generated GitHub Pages artifact
editorial-standards.md          human-facing editorial principles
CONTRIBUTING.md                 contribution and repository mechanics
.github/workflows/              CI and Pages deployment
```

---

## Review File Convention

New reviews use:

```text
reviews/YYYY/YYYY-MM-DD__slug__v1.md
```

The canonical fields remain `title`, `source`, `publication`, `date_read`, `primary_domain`, `tags`, and `key_insight`; `scholarly_signal` is optional. Archive as Knowledge Infrastructure adds optional provenance, version, review-state and governance-facet fields. Omit unavailable optional metadata rather than guessing it. See [`knowledge/schema.yml`](knowledge/schema.yml) for semantics.

Version increments (`v2`, `v3`) are reserved for substantive post-publication revisions to the analytical object. Reader-facing correction and supersession rules are in [`knowledge/history-policy.md`](knowledge/history-policy.md).

---

## Automation

On pull requests and pushes, CI runs the editorial and knowledge-layer validators, builds the normal discovery site, builds the knowledge discovery surfaces, and verifies reproducibility of the core review generator. GitHub Pages rebuilds both layers from canonical source files before deployment.

To run locally:

```bash
python scripts/editorial_lint.py
python scripts/knowledge_lint.py
python scripts/build_index.py
python scripts/build_knowledge.py
python scripts/build_index.py --check
```

Generated Pages files are deployment artifacts, not independent sources of truth.

---

## Recent Reviews

The current review stream is generated directly from canonical review metadata. See [Recent reviews](https://sankarshanmukhopadhyay.github.io/digital-governance-paper-notes/#recent) for the latest publications, or the [full archive](https://sankarshanmukhopadhyay.github.io/digital-governance-paper-notes/archive/) for chronological browsing.

Keeping this list on the generated site rather than duplicating it in the README prevents the repository landing page from becoming stale between protected-branch updates.

---

## Contributing

To suggest a paper for review, open an issue and assign it to the maintainer, including the title, author(s), a direct link, and a sentence on why it fits the taxonomy. Contribution mechanics, AI-assisted work rules and knowledge-layer conventions are in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

See [`LICENSE`](LICENSE).
