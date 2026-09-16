# Paper Radar

Paper Radar is the discovery and editorial-triage layer for Digital Governance Paper Notes. It finds recent scholarly work that may fit the repository, records why a paper was surfaced, and produces a candidate ledger and human-readable report.

It is not a publication authority. A `candidate` state means that the paper crossed transparent discovery thresholds. It does not mean the paper has been accepted into the review queue.

## Pipeline

1. Discover recent metadata from arXiv, Crossref and OpenAlex.
2. Normalise DOI, arXiv identifiers, titles and URLs.
3. Deduplicate records observed through multiple sources, including records that share a DOI while using different title renderings.
4. Reconcile source-specific freshness evidence before making any publication-date claim.
5. Compare canonical identifiers and titles with published reviews and open review issues.
6. Require at least one domain-specific theme anchor before a record can become a candidate or judgment case.
7. Record theme anchors, query matches, governance signals and exclusions.
8. Classify each result as `candidate`, `needs_judgment`, `deferred`, or `represented` when already reviewed or queued.
9. Write `data/paper-candidates.json` and a dated Markdown report under `reports/radar/`.
10. Require editorial judgment before creating a review issue.

## Configuration

`discovery/radar.json` is the inspectable discovery policy. Themes define broad search surfaces and explicit domain anchors. A theme anchor is evidence that the work is actually about the relevant technical or institutional domain rather than merely containing generic words such as “governance” or “infrastructure”. `governance_signals` provide additional evidence that a work speaks to authority, accountability, legitimacy, institutional control or adjacent governance mechanisms. `exclusion_signals` suppress recurring false positives.

The score is diagnostic. It exists to explain why a record was surfaced and to reduce the review burden. It must not be treated as a quality score, importance ranking, or automatic admission decision.

## States

- `candidate`: enough discovery evidence to merit editorial consideration.
- `needs_judgment`: plausible fit with weaker or ambiguous evidence, including materially conflicting freshness evidence.
- `deferred`: discovered but below the current triage threshold or missing a required domain anchor.
- `represented`: already present in the review corpus or current open review queue.

Queue lifecycle states such as `queued`, `reviewing`, and `published` belong to the editorial workflow after admission. Paper Radar does not move a candidate into that lifecycle on its own.

## Freshness provenance

Freshness is an evidentiary claim, not a single metadata field. A repository deposit, index update, or metadata registration date may be newer than the underlying intellectual object.

Paper Radar therefore preserves source-specific temporal evidence in each reconciled candidate record. The ledger distinguishes the discovery timestamp from source dates and retains source date semantics for Crossref, OpenAlex, arXiv, and future adapters. Reconciled records expose `earliest_known_publication_at`, `freshness_status`, `freshness_dates`, and the underlying `source_records` used to derive them.

The report uses `Published` only where publication semantics are verified. Otherwise it reports `Source date` with the source and date semantics. If two matched source records imply publication or public-release dates more than 31 days apart, the freshness state is `conflicting`; a `candidate` is automatically downgraded to `needs_judgment` until the temporal discrepancy is editorially resolved.

This rule prevents a recent repository or index deposit from being silently treated as evidence that the paper itself is newly published.

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
- Is it sufficiently distinct from existing reviews and queued work to add cumulative knowledge?
- Is there enough source material to support the full review operating procedure?
- Is its apparent freshness supported by the provenance record, or does it require temporal reconciliation first?

If admitted, create the normal paper-review issue with title, authors, stable source URL, discovery provenance, proposed domain, and an explicit admission rationale. From that point the canonical paper-review operating procedure applies.

## Trustworthiness rules

- A source failure is retained in `source_errors`; a total source failure causes the run to fail rather than reporting an empty clean result.
- Future-dated metadata is not admitted into the current radar window.
- Existing or already-queued papers are not surfaced as fresh candidates when canonical DOI/arXiv identifiers or sufficiently close titles match.
- Source-specific publication, deposit, index, update, and observed dates are retained where available rather than collapsed into one field.
- A recent source deposit is not silently described as a recent publication.
- Materially conflicting freshness evidence requires judgment before admission.
- Generic governance vocabulary cannot satisfy a theme without a domain-specific anchor.
- Missing evidence is not interpreted as evidence of irrelevance.
- Relevance score and editorial authority are separate.
- Configuration changes are reviewable repository changes and should travel through the normal PR path.
