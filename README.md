# Digital Governance Paper Notes

A curated archive of short, practitioner-oriented reviews of research papers, policy reports, essays, and institutional publications on AI governance, digital public infrastructure, public-interest technology, digital identity, and adjacent governance questions.

**Primary index:** [index.md](index.md)  
**GitHub Pages index:** [docs/index.md](docs/index.md)

---

## Scope

The repository focuses on concise review notes that extract the main argument of a paper, assess strengths and weaknesses, and capture one durable insight for future work.

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
- `docs/index.md` — generated index for GitHub Pages publishing
- `templates/` — review templates
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
---
```

---

## Automation

The repository is designed to maintain itself with minimal fiddly nonsense:

- On pull requests, CI checks whether generated files are stale.
- On pushes to `main` that modify `reviews/` or indexing logic, CI rebuilds the index and auto-commits generated changes.
- On version tags such as `v1.0.0`, CI creates a clean release ZIP artifact.
- GitHub Pages can publish from the generated `docs/` directory via GitHub Actions.

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

- **2026-03-07** — [The Artificial in ‘Artificial Intelligence’: How Imagination Shapes AI Regulation](reviews/2026/2026-03-07__the-artificial-in-artificial-intelligence-how-imagination-shapes-ai-regulation__v1.md) — *SSRN*
- **2026-03-07** — [Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?](reviews/2026/2026-03-07__evaluating-agents-md-context-files-coding-agents__v1.md) — *arXiv*
- **2026-03-07** — [Digital Governance Stacks and the Infrastructure of Empires](reviews/2026/2026-03-07__digital-governance-stacks-and-the-infrastructure-of-empires__v1.md) — *Bot Populi*
- **2026-03-07** — [Business Perspectives on Advancing AI](reviews/2026/2026-03-07__business-perspectives-on-advancing-ai__v1.md) — *Business at OECD*
- **2026-03-07** — [Advancing Open Source AI in India](reviews/2026/2026-03-07__advancing-open-source-ai-in-india__v1.md) — *Digital Futures Lab*
- **2026-03-06** — [Towards an Open, Resilient, Non-Aligned AI](reviews/2026/2026-03-06__towards-an-open-resilient-non-aligned-ai__v1.md) — *Geopolitique.eu*
- **2026-03-06** — [Toward Risk Thresholds for AI-Enabled Cyber Threats](reviews/2026/2026-03-06__toward-risk-thresholds-for-ai-enabled-cyber-threats__v1.md) — *UC Berkeley Center for Long-Term Cybersecurity*
- **2026-03-06** — [The Mythology of Conscious AI](reviews/2026/2026-03-06__the-mythology-of-conscious-ai__v1.md) — *Noema Magazine*

<!-- RECENT_REVIEWS:END -->

---

## GitHub Pages Setup

In the repository settings, set **Pages** to deploy from **GitHub Actions**.

The generated site entrypoint is `docs/index.html` (built from review metadata for reliable Pages deployment).

---

## License

See [`LICENSE`](LICENSE).
