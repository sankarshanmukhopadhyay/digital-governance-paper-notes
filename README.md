# Digital Governance Paper Notes

A curated archive of governance-first reviews of research papers, policy reports, essays, and institutional publications on AI governance, digital public infrastructure, public-interest technology, digital identity, and adjacent governance questions.

**Site:** [sankarshanmukhopadhyay.github.io/digital-governance-paper-notes](https://sankarshanmukhopadhyay.github.io/digital-governance-paper-notes/) 

**Index:** [index.md](index.md)

**Editorial standards:** [editorial-standards.md](editorial-standards.md)

**Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## About

These are working notes from a single reader. Each review extracts the governance claim a paper makes or implies, assesses it against a fixed set of questions (who controls the system, under what conditions that control can be contested, whether the proposed mechanisms are enforceable and by whom), and closes with one durable insight worth carrying into future work.

The archive has a running editorial preoccupation: when does a governance claim become operationally credible? Maturity frameworks, sovereignty postures, and open-ecosystem visions are evaluated here against whether they specify enforceable controls, testable design choices, and mechanisms that could actually fail, rather than against how well they affirm good intentions. That bias is deliberate and it shows in the reviews.

The current set skews toward India, South Asia, and APAC contexts because that is where the reading started. That is a temporary feature of the backlog, not a limitation of scope. The archive covers globally published work that aligns to the taxonomy below.

To suggest a paper for review, open an issue and assign it to the maintainer. See [CONTRIBUTING.md](CONTRIBUTING.md) for what to include.

---

## Editorial standards

Every review is written against a fixed governance checklist and a fixed style discipline, documented in full in [editorial-standards.md](editorial-standards.md). In short:

- **Governance-first, not summary.** A review states what the paper argues and, for mechanism or design proposals and policy/regulatory reports, evaluates control, contestability, enforcement, redress, the assumed beneficiary population, and unaddressed failure modes. Conceptual, philosophical, and advocacy papers get an adapted version of the same lens rather than a forced fit.
- **Traceable claims.** What the review says the paper argues should be locatable in the paper. Reviewer inference is distinguished from the paper's own claims rather than folded into them.
- **A steelman before a critique.** Every substantive critique engages the strongest available counter-argument before making its case.
- **No em dashes, no hedge phrases, no empty praise.** "Robust," "leverage" as a verb, "delves into," "sheds light on," and similar filler are off-limits; see the full banned-phrase list in [editorial-standards.md](editorial-standards.md).
- **`key_insight` is load-bearing.** It must be specific to the paper, present in the front matter, and identical to the body's `## Key Insight` section.

A subset of these rules is enforced mechanically. Run the linter before opening a pull request:

```bash
python scripts/editorial_lint.py
```

It checks front matter completeness, taxonomy conformance, file naming, em dashes, the banned-phrase list, `key_insight` identity between front matter and body, body length, and duplicate papers across the archive. CI runs it on every pull request and blocks the merge on errors; warnings (tag count outside 3-6, `ecosystem` used as a possible non-biological metaphor, length-band outliers) are reported but left to editorial judgment. What the linter can and cannot verify, and why some checks are warnings rather than hard gates, is documented in [editorial-standards.md](editorial-standards.md).

---

## Scope

### Taxonomy Snapshot

<!-- TAXONOMY_SUMMARY:START -->

- **AI Governance** (20)
- **AI Safety & Evaluation** (8)
- **Digital Public Infrastructure** (8)
- **Public Sector Digital Strategy** (2)
- **Digital Identity** (4)
- **Trust Infrastructure** (2)
- **Standards, Protocols & Interoperability** (1)
- **Privacy & Data Protection** (2)
- **Cybersecurity & Resilience** (1)
- **Law, Regulation & Liability** (9)
- **Platform Governance & Internet Governance** (2)
- **Socio-technical Systems** (8)
- **Inclusion, Rights & Development** (2)
- **State Capacity & Administrative Systems** (1)
- **Economic & Market Infrastructure** (4)

<!-- TAXONOMY_SUMMARY:END -->

This snapshot regenerates automatically from `taxonomy/domains.yml` and the reviews in `reviews/`; don't hand-edit the block between the markers above.

Core areas include:

- AI governance and institutional capacity
- Digital public infrastructure, DPGs, and public-sector transformation
- Digital identity, trust infrastructure, and interoperability
- Internet governance, privacy, cybersecurity, and standards
- Socio-technical systems and governance theory

The full controlled vocabulary, including secondary topic tags and arXiv scholarly-signal codes, lives in [`taxonomy/domains.yml`](taxonomy/domains.yml). Adding a domain or tag not yet in that file means updating it in the same commit as the review that needs it.

---

## Repository Structure

```text
reviews/YYYY/                 canonical review files, one per paper
index.md                      generated root index
docs/                         generated GitHub Pages site (index.html, per-domain and per-collection pages)
templates/review-template.md  canonical front matter and body template
taxonomy/domains.yml           controlled vocabulary: domains, tags, scholarly signals
collections/collections.json  curated cross-cutting collections
scripts/build_index.py         rebuilds index.md, docs/, and the README's generated sections
scripts/editorial_lint.py      Tier 1 editorial checks (style, schema, taxonomy, duplication)
editorial-standards.md         the full editorial rulebook, including what is and isn't automated
CONTRIBUTING.md                how to suggest a paper and how the maintainer writes a review
.github/workflows/             CI: lint + index staleness check, index rebuild, Pages deploy
```

---

## Review File Convention

New reviews use the canonical path format:

```text
reviews/YYYY/YYYY-MM-DD__slug__v1.md
```

The date is when the review was finished, not the paper's publication date. Version increments (`v2`, `v3`) are used only for substantive post-publication revisions to the analysis, not formatting fixes.

Each review follows [`templates/review-template.md`](templates/review-template.md): required front matter, then a `## Review` section of roughly 2,000-6,000 characters depending on how much the paper is actually arguing, then a `## Key Insight` section that must match the front matter `key_insight` field exactly.

Required front matter:

```yaml
---
title: ""
source: ""
publication: ""
date_read: "YYYY-MM-DD"
primary_domain: ""
tags: []
scholarly_signal: ""    # optional; arXiv/preprint subject classification only
key_insight: ""
---
```

`primary_domain` and every entry in `tags` must come from [`taxonomy/domains.yml`](taxonomy/domains.yml). `scholarly_signal` is the only optional field; every other field is required and checked by `editorial_lint.py`.

---

## Automation

The repository maintains itself with minimal manual overhead:

- On pull requests and pushes, CI installs dependencies, runs `editorial_lint.py`, and checks whether generated files are stale. A lint error or a stale index blocks the merge.
- On pushes to `main` that touch `reviews/`, the taxonomy, or the indexing logic, CI rebuilds `index.md` and `docs/` and auto-commits the result.
- GitHub Pages publishes from the generated `docs/` directory via GitHub Actions.

To run everything locally before opening a pull request:

```bash
python scripts/editorial_lint.py      # style, schema, and taxonomy checks
python scripts/build_index.py          # rebuild index.md, docs/, and this README's generated sections
python scripts/build_index.py --check  # verify nothing is stale
```

Commit the review file together with any regenerated files in a single commit.

---

## Recent Reviews

<!-- RECENT_REVIEWS:START -->

- **2026-08-06** — [Taking Scale Seriously in Technology Law](reviews/2026/2026-08-06__taking-scale-seriously-in-technology-law__v1.md) — *Wake Forest Law Review, Vol. 61 (2026), pp. 393-433*
- **2026-08-03** — [Critique of Agent Model](reviews/2026/2026-08-03__critique-of-agent-model__v1.md) — *arXiv*
- **2026-07-28** — [Targeted Report on Regulatory Challenges from Decentralised Finance](reviews/2026/2026-07-28__targeted-report-on-regulatory-challenges-from-decentralised-finance__v1.md) — *Financial Action Task Force (FATF)*
- **2026-07-25** — [The AI Amplifier Effect: Defining Human-AI Intimacy and Romantic Relationships with Conversational AI](reviews/2026/2026-07-25__the-ai-amplifier-effect-defining-human-ai-intimacy-and-romantic-relationships-with-conversational-ai__v1.md) — *arXiv*
- **2026-07-24** — [The Unintended Consequences of Large Language Models as a Labor-Augmenting Technology in Science](reviews/2026/2026-07-19__the-unintended-consequences-of-large-language-models-as-a-labor-augmenting-technology-in-science__v1.md) — *arXiv*
- **2026-07-12** — [‘God has helped us, and so will AI’: How the Terrorist Group Boko Haram Uses Frontier AI](reviews/2026/2026-07-12__god-has-helped-us-and-so-will-ai__v1.md) — *Cambridge Programme on AI Science & Policy, University of Cambridge*
- **2026-07-12** — [Introducing AI to an Online Petition Platform Changed Outputs but not Outcomes](reviews/2026/2026-07-12__introducing-ai-to-an-online-petition-platform-changed-outputs-but-not-outcomes__v1.md) — *arXiv*
- **2026-06-27** — [Strategic Identity Asymmetry: Why Digital Infrastructure Governance Fails Where Technology Succeeds in Brazil, Nigeria, and the Philippines](reviews/2026/2026-06-27__strategic-identity-asymmetry__v1.md) — *SSRN*

<!-- RECENT_REVIEWS:END -->

This list regenerates automatically from the most recently read reviews; don't hand-edit the block between the markers above. See [index.md](index.md) for the full archive, browsable by domain and by collection.

---

## Contributing

To suggest a paper for review, open an issue and assign it to the maintainer, including the title, author(s), a direct link, and a sentence on why it fits the taxonomy. To write a review, follow the conventions above and in [CONTRIBUTING.md](CONTRIBUTING.md), then run `editorial_lint.py` and `build_index.py` before opening a pull request.

---

## License

See [`LICENSE`](LICENSE).
