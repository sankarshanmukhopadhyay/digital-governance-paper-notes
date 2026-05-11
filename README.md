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

- **AI Governance** (20)
- **AI Safety & Evaluation** (5)
- **Digital Public Infrastructure** (7)
- **Public Sector Digital Strategy** (2)
- **Digital Identity** (3)
- **Trust Infrastructure** (2)
- **Privacy & Data Protection** (2)
- **Cybersecurity & Resilience** (1)
- **Law, Regulation & Liability** (7)
- **Platform Governance & Internet Governance** (1)
- **Socio-technical Systems** (6)
- **Inclusion, Rights & Development** (1)
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

- **2026-05-11** — [AI Governance at the Frontier: Unpacking Foundational Assumptions](reviews/2026/2026-05-11__ai-governance-at-the-frontier__v1.md) — *Center for Security and Emerging Technology*
- **2026-05-09** — [Governing Artificial Intelligence in India: Data Sourcing, Synthetic Content, and Technological Sovereignty](reviews/2026/2026-03-30__governing-artificial-intelligence-in-india__v1.md) — *Kautilya School of Public Policy Working Paper #3*
- **2026-05-06** — [Future of Jobs in the Age of AI: Emerging Roles, New Opportunities](reviews/2026/2026-05-06__future-of-jobs-in-the-age-of-ai__v1.md) — *DeepTech4Bharat Foundation and Center of Policy Research and Governance*
- **2026-05-06** — [Building Digital Foundations in Small Island Digital States 2.0](reviews/2026/2026-05-06__building-digital-foundations-in-small-island-digital-states-2-0__v1.md) — *United Nations Development Programme*
- **2026-05-06** — [Building a Human Resilience Infrastructure for the AI Age](reviews/2026/2026-04-01__building-human-resilience-infrastructure-ai-age__v1.md) — *Imagining the Digital Future Center, Elon University*
- **2026-05-05** — [Self-Sovereign Identity and the Future of Digital Trust: From India to the World](reviews/2026/2026-04-16__self-sovereign-identity-future-digital-trust__v1.md) — *Data Security Council of India / Digi Yatra Foundation / National Centre of Excellence*
- **2026-05-04** — [DPI@2047 for Viksit Bharat: A Strategic Roadmap to Enable Non-linear Inclusive Socio-economic Growth](reviews/2026/2026-05-04__dpi-2047-for-viksit-bharat__v1.md) — *NITI Aayog / NITI Frontier Tech Hub*
- **2026-05-04** — [AI Agents Under EU Law: A Compliance Architecture for AI Providers](reviews/2026/2026-04-07__ai-agents-under-eu-law-a-compliance-architecture-for-ai-providers__v1.md) — *arXiv working paper*

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
