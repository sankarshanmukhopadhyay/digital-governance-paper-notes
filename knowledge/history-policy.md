# Review History, Corrections and Supersession

Digital Governance Paper Notes preserves analytical history while making material changes visible to readers. Git history is necessary but is not sufficient as the reader-facing correction mechanism.

## Paper state and review state

A change in the underlying paper is distinct from a change in the reviewer's interpretation. Optional review metadata therefore separates `paper_version` from `review_status`.

`paper_version` identifies the source version actually reviewed when a stable version label exists. `review_status` describes the status of the repository review: `current`, `corrected`, or `superseded`.

## When to correct in place

Formatting repairs, link repairs, spelling fixes and metadata corrections that do not alter the analysis may be committed without incrementing the review filename version.

A substantive factual correction that preserves the basic analytical object may update the review in place if the correction is clearly noted in the review or associated repository history. `review_status: corrected` may be used when the correction materially affects how the review should be read.

## When to create a new review version

Create a new `__vN.md` review when the paper changes materially or when the analysis is substantively reconsidered. The prior review remains part of the archive and should be marked `superseded` where practical. The newer review should identify the source version it evaluates.

A new paper release does not automatically invalidate an earlier review. The editorial question is whether the evidentiary basis or argument changed enough to make the earlier analysis materially stale.

## Retraction, withdrawal and errata

A withdrawal, retraction or material erratum should be surfaced visibly rather than silently deleting the review. The archive may retain the historical review because it records what was evaluated at the time, but generated discovery surfaces should identify that the underlying source state changed.

## AI-assisted comparison

AI/LLM systems may assist version comparison, change detection and candidate materiality assessment. They do not determine whether a change is institutionally or analytically material. That decision remains a human editorial judgment and should be traceable through the repository's issue/PR history.

## Stable URLs

Historical review URLs should remain stable where practical. Supersession should redirect reader attention through visible metadata and related-review links rather than deleting prior analytical records.
