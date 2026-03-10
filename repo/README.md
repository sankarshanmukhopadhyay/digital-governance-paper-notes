# Digital Governance Paper Notes

A curated archive of short, practitioner-oriented reviews of research papers, policy reports, essays, and institutional publications on AI governance, digital public infrastructure, public-interest technology, digital identity, and adjacent governance questions.

**GitHub Pages site:** [sankarshanmukhopadhyay.github.io/digital-governance-paper-notes](https://sankarshanmukhopadhyay.github.io/digital-governance-paper-notes/) &nbsp;·&nbsp; **Repository index:** [index.md](index.md)

---

## About

These are working notes from a single reader. Each review extracts the main argument of a paper, assesses its strengths and limitations honestly, and captures one durable insight worth carrying into future work.

The collection has a running editorial preoccupation: when does a governance claim become operationally credible? Maturity frameworks, sovereignty postures, and open-ecosystem visions tend to be evaluated here against whether they specify enforceable controls, testable design choices, or mechanisms that could actually fail — rather than just affirming good intentions. That bias shows in the reviews.

The current set skews toward India, South Asia, and APAC contexts because that is where the reading started. That is a temporary feature of the backlog, not a limitation of scope. The archive will cover globally published work that aligns to the taxonomy.

If you want to suggest a paper for review, open an issue and assign it to the maintainer. See [CONTRIBUTING.md](CONTRIBUTING.md) for how that works.

---

## Scope

### Taxonomy Snapshot

<!-- TAXONOMY_SUMMARY:START -->

- **AI Governance** (10)
- **AI Safety & Evaluation** (3)
- **Digital Public Infrastructure** (3)
- **Public Sector Digital Strategy** (1)
- **Trust Infrastructure** (1)
- **Cybersecurity & Resilience** (1)
- **Law, Regulation & Liability** (4)
- **Socio-technical Systems** (1)
- **State Capacity & Administrative Systems** (1)

<!-- TAXONOMY_SUMMARY:END -->

Core areas include:

- AI governance and institutional capacity
- Digital public infrastructure, DPGs, and public-sector transformation
- Digital identity, trust infrastructure, and interoperability
- Internet governance, privacy, cybersecurity, and standards
- Socio-technical systems and governance theory

---

## Repository Structure

- `reviews/YYYY/` — canonical review files
- `index.md` — generated root index for the repository
- `docs/index.html` — generated GitHub Pages entrypoint
- `templates/` — review template
- `taxonomy/` — controlled vocabulary and domain scaffolding
- `scripts/` — repository maintenance utilities
- `.github/workflows/` — automation for index generation, Pages, and release packaging

---

## Review File Convention

New reviews should use the canonical path format:

```text
reviews/YYYY/YYYY-MM-DD__slug__v1.md
```

Each review should follow the template in `templates/review-template.md`.

Expected front matter:

```yaml
---
title: ""
source: ""
publication: ""
date_read: "YYYY-MM-DD"
primary_domain: ""
tags: []
scholarly_signal: ""    # optional
key_insight: ""
---
```

---

## Automation

The repository maintains itself with minimal manual overhead:

- On pull requests, CI checks whether generated files are stale.
- On pushes to `main` that modify `reviews/` or indexing logic, CI rebuilds the index and auto-commits generated changes.
- On version tags such as `v1.0.0`, CI creates a clean release ZIP artifact.
- GitHub Pages publishes from the generated `docs/` directory via GitHub Actions.

To rebuild locally:

```bash
python scripts/build_index.py
```

To verify locally:

```bash
python scripts/build_index.py --check
```

---

## Recent Reviews

<!-- RECENT_REVIEWS:START -->

- **2026-03-10** — [From Future of Work to Future of Workers: Addressing Asymptomatic AI Harms for Dignified Human-AI Interaction](reviews/2026/2026-03-10__future-of-work-to-future-of-workers-addressing-asymptomatic-ai-harms-for-dignified-human-ai-interaction__v1.md) — *arXiv*
- **2026-03-09** — [Strategy for Artificial Intelligence in Healthcare for India (SAHI)](reviews/2026/2026-03-09__strategy-for-artificial-intelligence-in-healthcare-for-india-sahi__v1.md) — *Ministry of Health and Family Welfare, Government of India*
- **2026-03-09** — [Doot: The AI Agent for Every Indian Citizen](reviews/2026/2026-03-09__doot-agent-one-architecture__v1.md) — *DigiDoot / India AI Mission White Paper*
- **2026-03-09** — [Agents of Chaos](reviews/2026/2026-03-09__agents-of-chaos__v1.md) — *arXiv*
- **2026-03-07** — [The Artificial in ‘Artificial Intelligence’: How Imagination Shapes AI Regulation](reviews/2026/2026-03-07__the-artificial-in-artificial-intelligence-how-imagination-shapes-ai-regulation__v1.md) — *SSRN*
- **2026-03-07** — [Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?](reviews/2026/2026-03-07__evaluating-agents-md-context-files-coding-agents__v1.md) — *arXiv*
- **2026-03-07** — [Digital Governance Stacks and the Infrastructure of Empires](reviews/2026/2026-03-07__digital-governance-stacks-and-the-infrastructure-of-empires__v1.md) — *Bot Populi*
- **2026-03-07** — [Codified Context: Infrastructure for AI Agents in a Complex Codebase](reviews/2026/2026-03-07__codified-context-infrastructure-for-ai-agents-in-a-complex-codebase__v1.md) — *arXiv*

<!-- RECENT_REVIEWS:END -->

---

## GitHub Pages Setup

In the repository settings, set **Pages** to deploy from **GitHub Actions**.

The generated site entrypoint is `docs/index.html` (built from review metadata for reliable Pages deployment).

---

## Contributing

To suggest a paper for review, open an issue and assign it to the maintainer. See [CONTRIBUTING.md](CONTRIBUTING.md) for full details.

---

## License

See [`LICENSE`](LICENSE).
