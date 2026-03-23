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

- **AI Governance** (14)
- **AI Safety & Evaluation** (4)
- **Digital Public Infrastructure** (5)
- **Public Sector Digital Strategy** (3)
- **Digital Identity** (1)
- **Trust Infrastructure** (1)
- **Privacy & Data Protection** (2)
- **Cybersecurity & Resilience** (1)
- **Law, Regulation & Liability** (5)
- **Socio-technical Systems** (2)
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

- **2026-03-23** — [The Comprehension-Gated Agent Economy: A Robustness-First Architecture for AI Economic Agency](reviews/2026/2026-03-23__comprehension-gated-agent-economy-robustness-first-ai-economic-agency__v1.md) — *arXiv*
- **2026-03-23** — [Nomotic AI: The Governance Counterpart to Agentic AI](reviews/2026/2026-03-23__nomotic-ai-governance-counterpart-to-agentic-ai__v1.md) — *SSRN (Independent Researcher)*
- **2026-03-23** — [AI for Justice: Ethical, Fair and Robust Adoption in India's Courts](reviews/2026/2026-03-23__ai-for-justice-ethical-fair-and-robust-adoption-in-indias-courts__v1.md) — *DAKSH & Digital Futures Lab / UNDP*
- **2026-03-23** — [AI for Justice: Ethical, Fair and Robust Adoption in India's Courts](reviews/2026/2026-03-23__ai-for-justice-ethical-fair-robust-adoption-indias-courts__v1.md) — *DAKSH & Digital Futures Lab / UNDP*
- **2026-03-18** — [Large-scale online deanonymization with LLMs](reviews/2026/2026-03-18__large-scale-online-deanonymization-with-llms__v1.md) — *arXiv*
- **2026-03-17** — [Sandboxes for DPI: Co-creating the blocks of digital trust](reviews/2026/2026-03-17__sandboxes-for-dpi-co-creating-the-blocks-of-digital-trust__v1.md) — *Datasphere Initiative*
- **2026-03-17** — [Distributed Legal Infrastructure for a Trustworthy Agentic Web](reviews/2026/2026-03-17__distributed-legal-infrastructure-for-a-trustworthy-agentic-web__v1.md) — *arXiv*
- **2026-03-17** — [AI Innovation, Effective Anonymization & the DPDP Act](reviews/2026/2026-03-17__ai-innovation-effective-anonymization-the-dpdp-act__v1.md) — *Open Loop*

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
