# Editorial Standards for Digital Governance Paper Notes

## Purpose

This document sets the rules by which a review earns publication in the repository. It is written against the actual content of the 68 published reviews, not against an idealized version of the archive. The current reviews are stylistically disciplined and analytically confident, but confidence is not the same property as rigor. A reader from a journal editorial board, a regulator's research office, or a think tank would ask three questions the current pipeline does not systematically answer: where in the paper does this claim live, what would make this claim false, and how does this paper's argument sit against the five adjacent papers already in the archive. The rules below are organized to close those three gaps without abandoning the voice the repository has built.

## 1. Provenance and Metadata Integrity

A review is only as trustworthy as its paper trail. The current front matter tracks `date_read` but not the paper's own publication date, and has no `doi` or institutional-affiliation field at all. This is a real gap: a claim about "the current state of AI regulatory capacity" means something different if the paper is from 2021 than from 2026, and the reader has no way to check without leaving the review.

- Every review records the paper's original publication or preprint date, separately from the date the reviewer read it. If the paper does not state one, the review says so explicitly rather than omitting the field.
- Every review records the author's institutional affiliation and, where it is material to the argument, states it in the body (a paper on platform liability written by platform in-house counsel is a different evidentiary object than the same paper written by an independent academic, even if the arguments are identical).
- Preprint status, working-paper status, and peer-review status are distinguished explicitly. A preprint gets a visible flag in the front matter and a sentence in the body noting that claims have not cleared review.
- `source_url` must resolve to the paper itself or its canonical landing page, not a search result, a paywall gateway that immediately 404s, or a cached mirror. If only a paywalled abstract is accessible, the review says so at the top of the analysis, not buried in a footnote.
- A `doi` field is populated whenever one exists. Its absence is recorded as `null`, not silently dropped, so a missing DOI reads as "checked, none found" rather than "not checked."

## 2. Evidentiary Traceability

This is the largest gap in the current archive. Reviews assert strong claims about what a paper argues, gets wrong, or fails to see, but almost none of them anchor a claim to a specific location in the source text — a section, a figure, a stated methodology, a quoted (and properly minimal) phrase. A reader cannot verify the review against the paper without re-reading the whole paper, which defeats the purpose of a review.

- Every substantive claim about what the paper argues or fails to argue should be locatable. Not every sentence needs a citation, but the review as a whole should make clear which section, framework, or claim in the paper is being evaluated at each point, using the paper's own terms rather than the reviewer's restatement of them.
- Reviewer inference must be marked as inference. There is a difference between "the paper states that voluntary frameworks are sufficient" and "the paper's silence on enforcement implies it assumes voluntary compliance will hold." The second is a legitimate governance critique, but it has to be flagged as the reviewer's read, not folded into the paper's claims as if the paper said it.
- Where a paper makes an empirical claim (a statistic, a benchmark result, a survey finding), the review states the evidentiary basis the paper gives for it and whether that basis is adequate to the claim's strength. A paper that draws a general governance conclusion from a single case study should be called out for exactly that, not just labeled "weak" without saying why.
- Quoted material follows the same minimal-quotation discipline as any other written output: quotes are rare, short, and used only where the paper's exact language is itself the evidence (a definitional claim, an unusually strong or unusually hedged assertion). Everything else is paraphrase in the reviewer's own words.

## 3. Analytical Completeness by Paper Type

The system prompt's governance checklist (control, contestability, enforceability, beneficiary population, failure modes, novelty) is well built for papers that propose a governance mechanism or system design. It does not fit every paper in the archive equally well. "The Mythology of Conscious AI" is a philosophical essay, not a design proposal, and forcing an enforcement-and-redress analysis onto it produces a review that gestures at the checklist rather than genuinely applying it. The fix is a triage step, not a weaker checklist.

- Before drafting, the review classifies the paper into one of a small number of types: mechanism/design proposal, empirical study, policy or regulatory report, conceptual/theoretical argument, survey or literature review, or advocacy/position paper. This classification appears in the front matter or the opening line of the analysis.
- The full governance checklist (who controls, under what conditions control transfers, enforcement, redress, beneficiary population, failure modes) is mandatory in full for mechanism/design proposals and policy/regulatory reports, since those are papers making implementable claims.
- For conceptual, philosophical, or advocacy papers, the review substitutes an adapted checklist: what governance-relevant premise does the argument depend on, what institutional actor would this argument, if accepted, empower or weaken, and what does the argument's framing make it easy to avoid discussing. This keeps the governance lens without manufacturing an enforcement analysis for a paper that was never making an enforcement claim.
- For empirical studies, the checklist adds a specific requirement: does the sample, method, or dataset support the scope of the governance conclusion drawn from it. This is the single most common failure mode in adjacent literatures (a narrow technical result generalized into a broad policy recommendation) and the current reviews do not consistently check for it.

## 4. Argumentative Rigor and the Steelman Requirement

A review that only identifies what is weak, without engaging what a sophisticated defender of the paper would say in response, is advocacy dressed as analysis. Reputable review venues expect the reviewer to have made the strongest case for the paper before making the case against it.

- Every "Weaknesses and Gaps" or "Governance Analysis" section must include at least one place where the review states the strongest available counter to its own critique, then explains why the critique survives it (or, where honest, concedes that it doesn't fully survive it). This is not hedging; it is the difference between a critique that has been pressure-tested and one that hasn't.
- Where the review disagrees with the paper's normative framing (whose interests should count, what counts as a legitimate exercise of authority), it states this as a disagreement, not as a factual correction. Conflating "the paper is wrong" with "the paper and I disagree about who should decide" is a category error the current reviews sometimes make, particularly in the sovereignty and open-ecosystem papers.
- Alternative readings of ambiguous passages are noted where the paper's own argument is genuinely underspecified, rather than the review picking the least charitable reading and critiquing that.

## 5. Comparative Positioning

The archive currently reviews each paper in isolation, even though many of the 68 entries cluster tightly (multiple AI governance maturity frameworks, multiple India/DPI papers, multiple sovereignty papers). A single-paper review that never says "this recombines a maturity-model structure already published in three prior frameworks in this archive" is missing information the reader needs to judge the novelty claim in "Novelty and Impact."

- Before finalizing the Novelty and Impact assessment, the reviewer checks the archive's own index for papers in the same or an adjacent domain and states explicitly whether the paper's central mechanism, framework, or claim has appeared before, in the archive or in the wider literature the reviewer is aware of.
- Where a genuine precedent exists, the review names it (paper title, not a vague "similar work exists") and states what, if anything, the new paper adds beyond that precedent.
- This does not require exhaustive literature review for every entry, but it does require the reviewer to have actually checked, not asserted "genuinely novel" or "incremental" as an unsupported label.

## 6. Style and Prose Discipline, Enforced Mechanically

The existing style rules (dense paragraphs, no em dashes, no hedge phrases, precise attribution of agency) are correct. The problem is that they are currently aspirational rather than enforced, and the archive shows drift as a result.

- A pre-commit or CI lint checks every review file for the banned phrase list and for the em-dash character before it can be merged. This is a five-line script; there is no reason this should be caught by a human reader after the fact.
- A character-count check on the review body flags files that fall well outside the stated target range, so length drift (currently ranging roughly 2,700 to 3,400 characters against a ~2,000-character template target) gets caught rather than silently normalized as the new target.
- Passive constructions that obscure agency ("mechanisms are described," "concerns have been raised") are treated as a specific, checkable failure: the review names who describes the mechanism and who raises the concern, because in governance writing the identity of the actor is usually the analytical point.

## 7. Reviewer Positionality and Correction Policy

The repository is explicit, correctly, that it reflects one reader's judgment, not institutional consensus. Reputable single-author review venues (a respected columnist, a named peer reviewer) handle this not by pretending to neutrality but by being transparent about their own vantage point and by having a visible mechanism for being wrong in public.

- Where a review's judgment turns on a contestable normative position (what counts as legitimate state control over a DPI stack, whether voluntary industry frameworks can ever be adequate), the review can take a position, but should signal that it is a position, not settled fact, consistent with the archive's own stated editorial preoccupation.
- A visible, dated correction log exists for substantive errors discovered after publication (misread claims, wrong attribution, factual errors in the paper's own reporting that the review repeated uncritically). This is distinct from the existing version-increment rule for "substantive post-publication revisions" — a correction log records what was wrong and when it was fixed, rather than only bumping a version number silently.
- If a paper is later retracted, corrected, or superseded by a revised version, the review is updated with a visible notice rather than left to stand as if the underlying paper were unchanged.

## 8. Pre-Publication Checklist

This extends, rather than replaces, the existing Repository Compliance Checklist. Before a review is merged:

- Paper type is classified and the correct variant of the governance checklist has been applied.
- Every claim attributed to the paper is traceable to a specific part of the paper; every inference is marked as the reviewer's own.
- At least one steelmanned counter-argument to the review's central critique appears and is addressed.
- The archive index has been checked for adjacent or precedent papers, and the novelty claim reflects that check.
- Publication date, institutional affiliation, and peer-review/preprint status are present in the front matter, with `null` recorded explicitly where information genuinely could not be found.
- The lint script has run clean for banned phrases, em dashes, and character-count range.
- Any prior review this paper's argument bears on (same author, same framework, revised edition) is cross-referenced.

None of this requires slowing the archive down into a formal peer-review process; it requires making explicit, checkable, and mechanically enforced what the current reviews are already trying to do by instinct. The gap between the archive's stated ambition and its current output is smaller than it looks. It is mostly a traceability and enforcement gap, not a judgment gap.
