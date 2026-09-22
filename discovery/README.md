# Paper Radar

Paper Radar is the discovery and editorial-triage layer for Digital Governance Paper Notes. It finds recent scholarly work that may fit the repository, records why a paper was surfaced, and produces a candidate ledger and human-readable report.

It is not a publication authority. A `candidate` state means that the paper crossed transparent discovery thresholds. It does not mean the paper has been accepted into the review queue.

## Pipeline

1. Discover recent metadata from arXiv, Crossref and OpenAlex.
2. Normalise DOI, arXiv identifiers, titles and URLs.
3. Deduplicate records observed through multiple sources, including records that share a DOI while using different title renderings.
4. Reconcile source-specific freshness evidence before making any publication-date claim.
5. Compare canonical identifiers and titles with published reviews and issue lifecycle history, including closed terminal dispositions.
6. Require at least one domain-specific theme anchor before a record can become a candidate or judgment case.
7. Record theme anchors, query matches, governance signals and exclusions.
8. Classify each result as `candidate`, `needs_judgment`, `deferred`, or `represented` when already reviewed or suppressed by issue state.
9. Write `data/paper-candidates.json` and a dated Markdown report under `reports/radar/` inside the workflow run only.
10. Create or resurface GitHub intake issues only for `candidate` and `needs_judgment` records.
11. Require human editorial action to move an intake issue into `review:backlog` or a terminal disposition.

## Configuration

`discovery/radar.json` is the inspectable discovery policy. Themes define broad search surfaces and explicit domain anchors. A theme anchor is evidence that the work is actually about the relevant technical or institutional domain rather than merely containing generic words such as “governance” or “infrastructure”. `governance_signals` provide additional evidence that a work speaks to authority, accountability, legitimacy, institutional control or adjacent governance mechanisms. `exclusion_signals` suppress recurring false positives.

The score is diagnostic. It exists to explain why a record was surfaced and to reduce the review burden. It must not be treated as a quality score, importance ranking, or automatic admission decision.

## States

- `candidate`: enough discovery evidence to merit editorial consideration.
- `needs_judgment`: plausible fit with weaker or ambiguous evidence, including materially conflicting freshness evidence.
- `deferred`: discovered but below the current triage threshold or missing a required domain anchor.
- `represented`: already present in the review corpus or current open review queue.

Radar states and editorial issue states are deliberately separate. Machine-level `deferred` records do not create issues. A Radar shortlist becomes an issue labelled `radar:candidate` or `radar:needs-judgment`. Human editorial action may then move it to `review:backlog`, `review:in-progress`, `disposition:deferred`, or `disposition:declined`. `review:published` is terminal.

Only one lifecycle label should be active at a time. The issue-lifecycle workflow removes superseded lifecycle labels automatically. `disposition:deferred` and `disposition:declined` close an issue as not planned; `review:published` closes it as completed. A deferred issue is suppressed for 90 days by default and may then be resurfaced by Radar into the same issue.

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

The `Paper Radar` GitHub Actions workflow runs weekly on Monday and can also be run manually. Its report is rendered in the Actions job summary and the ledger/report are retained as workflow artifacts. They are not committed to `main`, so the repository does not become an archive of machine-discovered or machine-deferred papers.

On scheduled or manually dispatched runs, the workflow converts only `candidate` and `needs_judgment` records into GitHub intake issues. Pull-request runs validate the same projection in dry-run mode and do not create issues.

## Admission to the review queue

Before opening a review issue, inspect the paper itself or authoritative metadata and answer:

- Does it materially align with a controlled repository domain?
- Does it make a governance, institutional, infrastructure, power, legitimacy, rights, accountability, or control question legible?
- Is it sufficiently distinct from existing reviews and queued work to add cumulative knowledge?
- Is there enough source material to support the full review operating procedure?
- Is its apparent freshness supported by the provenance record, or does it require temporal reconciliation first?

Admission is represented by changing the issue label to `review:backlog`. That transition removes the Radar triage label and establishes a human editorial decision that the paper belongs in the review programme. `review:in-progress` marks active work. The resulting review PR should close the issue in the normal issue/PR flow; `review:published` can also be applied as the terminal lifecycle label.

If the paper should not enter the backlog, use `disposition:deferred` or `disposition:declined`. These states close the issue so triage does not accumulate as a perpetually open queue.

## Trustworthiness rules

- A source failure is retained in `source_errors`; a total source failure causes the run to fail rather than reporting an empty clean result.
- Future-dated metadata is not admitted into the current radar window.
- Existing reviews, active intake issues, admitted review issues, published issues, declined issues, and recently deferred issues suppress duplicate fresh intake when canonical DOI/arXiv identifiers or sufficiently close titles match.
- Source-specific publication, deposit, index, update, and observed dates are retained where available rather than collapsed into one field.
- A recent source deposit is not silently described as a recent publication.
- Materially conflicting freshness evidence requires judgment before admission.
- Generic governance vocabulary cannot satisfy a theme without a domain-specific anchor.
- Missing evidence is not interpreted as evidence of irrelevance.
- Relevance score and editorial authority are separate.
- Configuration changes are reviewable repository changes and should travel through the normal PR path.
