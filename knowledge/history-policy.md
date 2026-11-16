# Review History, Corrections and Supersession

Digital Governance Paper Notes preserves analytical history while making material changes visible to readers. Git history preserves the full revision record. The active review directory and generated site present one current review per paper; a material supersession is recorded in the review version and the publication pull request.

## Paper state and review state

A change in the underlying paper is distinct from a change in the reviewer's interpretation. Optional review metadata therefore separates `paper_version` from `review_status`.

`paper_version` identifies the source version actually reviewed when a stable version label exists. `review_status` describes the status of the repository review: `current`, `corrected`, or `superseded`.

## When to correct in place

Formatting repairs, link repairs, spelling fixes and metadata corrections that do not alter the analysis may be committed without incrementing the review filename version.

A substantive factual correction that preserves the basic analytical object may update the review in place if the correction is clearly noted in the review or associated repository history. `review_status: corrected` may be used when the correction materially affects how the review should be read.

## When to create a new review version

Create a new `__vN.md` review when the paper changes materially or when the analysis is substantively reconsidered. Publish the new version as the sole active Markdown review for that paper. Remove the older `__vN.md` file from the active `reviews/` tree in the same PR, without rewriting or erasing its Git history. The PR must explain the substantive editorial change, allowing readers to retrieve the previous version from the repository's commit history. The newer review should identify the source paper version it evaluates when known.

A new paper release does not automatically invalidate an earlier review. The editorial question is whether the evidentiary basis or argument changed enough to make the earlier analysis materially stale.

## Retraction, withdrawal and errata

A withdrawal, retraction or material erratum should be surfaced visibly rather than silently deleting the review. The repository's Git history retains the historical review because it records what was evaluated at the time. The active review and generated discovery surfaces should identify any material change in the underlying source state.

## AI-assisted comparison

AI/LLM systems may assist version comparison, change detection and candidate materiality assessment. They do not determine whether a change is institutionally or analytically material. That decision remains a human editorial judgment and should be traceable through the repository's issue/PR history.

## Stable URLs

Public review URLs remain stable when the paper's review version changes. The current version replaces the previous version at that URL. The prior analytical record remains accessible through Git history and the supersession PR, rather than appearing as a second active archive entry.
