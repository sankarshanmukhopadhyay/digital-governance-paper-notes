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

- **AI Governance** (17)
- **AI Safety & Evaluation** (5)
- **Digital Public Infrastructure** (5)
- **Public Sector Digital Strategy** (2)
- **Digital Identity** (2)
- **Trust Infrastructure** (2)
- **Privacy & Data Protection** (2)
- **Cybersecurity & Resilience** (1)
- **Law, Regulation & Liability** (6)
- **Platform Governance & Internet Governance** (1)
- **Socio-technical Systems** (3)
- **State Capacity & Administrative Systems** (1)
- **Economic & Market Infrastructure** (2)

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

- **2026-04-27** — [Institutional Memory, Narrative Integrity, and the Future of Democratic Resilience](reviews/2026/2026-04-27__institutional-memory-narrative-integrity-democratic-resilience__v1.md) — *Centre for International Governance Innovation*
- **2026-04-16** — [Mapping India’s Data Centres: Aspirations, Realities and Futures](reviews/2026/2026-04-16__mapping-indias-data-centres-aspirations-realities-and-futures__v1.md) — *Digital Futures Lab*
- **2026-04-16** — [AI Index Report 2026](reviews/2026/2026-04-16__ai-index-report-2026__v1.md) — *Stanford Institute for Human-Centered Artificial Intelligence (HAI)*
- **2026-04-14** — [AI Governance, Safety and Infrastructure](reviews/2026/2026-04-14__ai-governance-safety-and-infrastructure__v1.md) — *Global Network Initiative and Centre for Communication Governance, National Law University Delhi*
- **2026-04-06** — [Syntelos: Trust Through Attestation and Policy](reviews/2026/2026-04-06__syntelos-trust-through-attestation-and-policy__v1.md) — *Author webpage / paper draft*
- **2026-04-06** — [CUBE: A Standard for Unifying Agent Benchmarks](reviews/2026/2026-04-06__cube-a-standard-for-unifying-agent-benchmarks__v1.md) — *arXiv*
- **2026-04-06** — [Cryptographic Runtime Governance for Autonomous AI Systems: The Aegis Architecture for Verifiable Policy Enforcement](reviews/2026/2026-04-06__cryptographic-runtime-governance-for-autonomous-ai-systems-the-aegis-architecture-for-verifiable-policy-enforcement__v1.md) — *arXiv*
- **2026-04-06** — [A Cryptographic Framework for Proof of Personhood](reviews/2026/2026-04-06__a-cryptographic-framework-for-proof-of-personhood__v1.md) — *Reference page for IACR ePrint paper*

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
