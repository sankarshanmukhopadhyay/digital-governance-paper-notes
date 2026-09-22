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

The archive now has a second layer above individual reviews. It is designed to make accumulated governance knowledge explicit without converting editorial judgment into opaque scores or automatic classifications.

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

### Taxonomy Snapshot

<!-- TAXONOMY_SUMMARY:START -->

- **AI Governance** (25)
- **AI Safety & Evaluation** (13)
- **Digital Public Infrastructure** (8)
- **Public Sector Digital Strategy** (2)
- **Digital Identity** (7)
- **Trust Infrastructure** (5)
- **Standards, Protocols & Interoperability** (1)
- **Privacy & Data Protection** (3)
- **Cybersecurity & Resilience** (1)
- **Law, Regulation & Liability** (10)
- **Platform Governance & Internet Governance** (2)
- **Socio-technical Systems** (9)
- **Inclusion, Rights & Development** (2)
- **State Capacity & Administrative Systems** (2)
- **Economic & Market Infrastructure** (5)

<!-- TAXONOMY_SUMMARY:END -->

This snapshot regenerates automatically from `taxonomy/domains.yml` and the reviews in `reviews/`; don't hand-edit the block between the markers above.

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

<!-- RECENT_REVIEWS:START -->

- **2026-09-22** — [Procedural fairness, accountability, and legitimacy in the AI-enabled state: evidence from China](reviews/2026/2026-09-22__procedural-fairness-accountability-legitimacy-ai-enabled-state__v1.md) — *Humanities and Social Sciences Communications (2026)*
- **2026-09-17** — [Multi-stakeholder transparency evaluation and dynamic accountability mechanisms for AI-assisted criminal sentencing](reviews/2026/2026-09-17__multi-stakeholder-transparency-dynamic-accountability-ai-sentencing__v1.md) — *Scientific Reports (2026)*
- **2026-09-16** — [Very Justified Envy](reviews/2026/2026-09-16__very-justified-envy__v1.md) — *arXiv*
- **2026-09-16** — [Verifiable Social Reasoning for LLM Assistants](reviews/2026/2026-09-16__verifiable-social-reasoning__v1.md) — *arXiv*
- **2026-09-16** — [Taxonomy-Driven Analysis of Open-Source AI Risk Mitigation Tools](reviews/2026/2026-09-16__taxonomy-driven-analysis-open-source-ai-risk-mitigation-tools__v1.md) — *arXiv*
- **2026-09-16** — [People Are Not Just Their Countries. Disentangling Social Determinants of LLM Value Alignment Across Europe](reviews/2026/2026-09-16__people-are-not-just-their-countries__v1.md) — *arXiv; accepted at AIES 2026*
- **2026-09-16** — [Never Stop Thinking: Continuous-Time Language Agents](reviews/2026/2026-09-16__never-stop-thinking__v1.md) — *arXiv*
- **2026-09-16** — [Interactive Memory Learning for Long-Term Conversations](reviews/2026/2026-09-16__interactive-memory-learning__v1.md) — *arXiv*

<!-- RECENT_REVIEWS:END -->

This list regenerates automatically from the most recently read reviews; don't hand-edit the block between the markers above. See [index.md](index.md) for the full archive.

---

## Contributing

To suggest a paper for review, open an issue and assign it to the maintainer, including the title, author(s), a direct link, and a sentence on why it fits the taxonomy. Contribution mechanics, AI-assisted work rules and knowledge-layer conventions are in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

See [`LICENSE`](LICENSE).
