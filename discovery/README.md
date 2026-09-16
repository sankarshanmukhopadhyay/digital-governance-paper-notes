# Paper Radar

Paper Radar is the discovery and editorial-triage layer for Digital Governance Paper Notes. It finds recent scholarly work that may fit the repository, records why a paper was surfaced, and produces a candidate ledger and human-readable report.

It is not a publication authority. A `candidate` state means that the paper crossed transparent discovery thresholds. It does not mean the paper has been accepted into the review queue.

## Pipeline

1. Discover recent metadata from arXiv, Crossref and OpenAlex.
2. Normalise DOI, arXiv identifiers, titles and URLs.
3. Deduplicate records observed through multiple sources.
4. Compare canonical identifiers and titles with published reviews.
5. Record query matches, governance signals and exclusions.
6. Classify each result as `candidate`, `needs_judgment`, `deferred`, or `published` when already represented.
7. Write `data/paper-candidates.json` and a dated Markdown report under `reports/radar/`.
8. Require editorial judgment before creating a review issue.

## Configuration

`discovery/radar.json` is the inspectable discovery policy. Themes define broad search surfaces. `governance_signals` provide positive evidence that a work speaks to authority, accountability, legitimacy, institutional control or adjacent governance mechanisms. `exclusion_signals` suppress recurring false positives.

The score is diagnostic. It exists to explain why a record was surfaced and to reduce the review burden. It must not be treated as a quality score, importance ranking, or automatic admission decision.

## States

- `candidate`: enough evidence to merit editorial consideration.
- `needs_judgment`: plausible fit with weaker or ambiguous evidence.
- `deferred`: discovered but below the current triage threshold.
- `published`: already represented in the review corpus.

Queue lifecycle states such as `queued`, `reviewing`, and `published` belong to the editorial workflow after admission. Paper Radar does not move a candidate into that lifecycle on its own.

## Operation

Run locally:

```bash
python -m unittest discover -s tests -p 'test_paper_radar.py'
python scripts/paper_radar.py
```

The `Paper Radar` GitHub Actions workflow runs weekly on Monday and can also be run manually. Its report is rendered in the Actions job summary and the ledger/report are retained as workflow artifacts. Generated radar outputs are operational evidence, not canonical editorial content.

## Admission to the review queue

Before opening a review issue, inspect the paper itself or authoritative metadata and answer:

- Does it materially align with a controlled repository domain?
- Does it make a governance, institutional, infrastructure, power, legitimacy, rights, accountability, or control question legible?
- Is it sufficiently distinct from existing reviews to add cumulative knowledge?
- Is there enough source material to support the full review operating procedure?

If admitted, create the normal paper-review issue with title, authors, stable source URL, discovery provenance, proposed domain, and an explicit admission rationale. From that point the canonical paper-review operating procedure applies.

## Trustworthiness rules

- A source failure is retained in `source_errors`; a total source failure causes the run to fail rather than reporting an empty clean result.
- Existing papers are not surfaced as fresh candidates when canonical DOI/arXiv identifiers or sufficiently close titles match the corpus.
- Missing evidence is not interpreted as evidence of irrelevance.
- Relevance score and editorial authority are separate.
- Configuration changes are reviewable repository changes and should travel through the normal PR path.
