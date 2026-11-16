---
title: "Pause Is Not Recovery: Containment, Revocation, Rollback, Recovery, and Fresh Readmission in Recursive AI R&D"
source: "https://doi.org/10.5281/zenodo.23032977"
publication: "The Second Waters - Structural Paper Series, Paper 06; The Second Waters (2026)"
date_read: "2026-11-16"
primary_domain: "Trust Infrastructure"
tags: ["authority", "authorization", "resilience", "assurance", "evidence", "AI risk management"]
key_insight: "Paper 06 establishes durable revocation and fresh readmission as recovery invariants, but its linear lifecycle is not yet a sufficient conformance model for concurrent restrictions and partitioned authority; implementers should preserve the invariants without adopting the state sequence literally."
published: "2026-09-29"
doi: "10.5281/zenodo.23032977"
peer_review_status: "working-paper"
paper_type: "working-paper"
paper_version: "Final Publication Edition v2.1"
review_status: "current"
---

# Paper Review

## Review

*Pause Is Not Recovery* addresses a genuine authority-restoration failure: an incident response can stop execution and restore software while unknowingly reviving credentials or policy state invalidated after the checkpoint. The paper's core requirements are precise enough to retain as design invariants. Revocation must survive restore, incident history must remain append-preserving, a recovered candidate must be technically verified, and privileged readmission must be separately authorized under current policy. The typed distinctions among evidence, verifier verdict, authorization and commit in Sections 17–18 prevent a successful integrity check from silently becoming operational permission.

Sections 34–38 translate those distinctions into testable recovery behavior. A pre-revocation snapshot must not validate an old credential; a candidate cannot infer current authority from its historical identity; uncertainty remains explicit in the recovery bundle; and readmission progresses through restricted scopes with measurable exit conditions. Sections 39 and 42 address another material failure: a compromised monitor cannot be the sole witness that both the recovered workload and the monitor itself are safe. These are more than broad recommendations to improve oversight. They identify specific transitions that a control plane must reject.

The paper also supplies minimum requirements R1–R10 and negative tests, but it does not report execution of those tests against a reference system. Its scenarios illustrate permissible operation, not measured robustness. The editorial distinction is therefore between a useful set of invariants and a complete conformance specification. That boundary becomes clear when examining the paper's canonical state progression.

The sequence ACTIVE, RESTRICTED, PAUSED, QUARANTINED, REVOKED, RECOVERY_CANDIDATE, RECOVERY_VERIFIED, READMISSION_PENDING and READMITTED is a useful narrative of an incident lifecycle. It is not sufficient as a single state variable. Revocation describes an authority relation, quarantine an operational isolation condition, and verification an evidentiary result. Those conditions can overlap and apply to different objects or generations. A service may remain quarantined while one delegation is revoked and a separate component is reconstructed. Treating every label as a mutually exclusive global phase would undermine the paper's own requirement for narrow containment and unaffected-work continuity. A realistic conformance model needs orthogonal state or equivalent scoped relations and explicit guards on consequential transitions.

The same issue appears across providers. Sections 19, 22 and 25 require fresh epochs, policy digests and fail-closed behavior, but leave open what constitutes sufficiently current authority when services have divergent revocation views or cannot contact their authority source. It is possible to require denial during uncertainty, yet doing so at every boundary may strand legitimate recovery. The trade-off is not an argument against revocation precedence. It requires a declared consistency and availability contract: which protected actions cannot proceed on stale state, where delegated caches are prohibited, and how recovery can resume once agreement is restored. Without it, two implementations could satisfy the same descriptive rule while producing materially different authority outcomes.

A related limit concerns effects outside the restored system. Rollback preserves historical evidence of prior actions but cannot reverse external disclosures, transfers or decisions already committed. Compensating obligations and redress may be necessary even when the internal state machine reports a clean readmission. The paper does not claim to solve those obligations. They delimit what its term 'recovery' can establish.

This paper is best read alongside the archive's *Security of the Security*. That work secures the independence of verification and commit; Paper 06 addresses how those boundaries survive a destructive lifecycle event. Its distinctive advance is the insistence that trusted re-entry is a new governed decision, not a successful restart. My editorial position is to preserve the durable-revocation, history and fresh-readmission invariants as implementation requirements, but not to promote the proposed linear state sequence to a normative conformance profile without concurrent-state semantics and partition tests. An implementation showing correct authority behavior under snapshot replay, mixed quarantine scopes, provider disagreement and verifier compromise would substantively change that assessment.

## Key Insight

Paper 06 establishes durable revocation and fresh readmission as recovery invariants, but its linear lifecycle is not yet a sufficient conformance model for concurrent restrictions and partitioned authority; implementers should preserve the invariants without adopting the state sequence literally.
