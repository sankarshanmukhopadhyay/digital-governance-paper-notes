---
title: "Pause Is Not Recovery: Containment, Revocation, Rollback, Recovery, and Fresh Readmission in Recursive AI R&D"
source: "https://doi.org/10.5281/zenodo.23032977"
publication: "The Second Waters - Structural Paper Series, Paper 06; The Second Waters (2026)"
date_read: "2026-11-16"
primary_domain: "Trust Infrastructure"
tags: ["authority", "authorization", "resilience", "assurance", "evidence", "AI risk management"]
key_insight: "Recovery is governable only when revoked authority cannot return through restored state and readmission is a separately evidenced decision under current policy, not an automatic consequence of technical recovery."
published: "2026-09-29"
doi: "10.5281/zenodo.23032977"
peer_review_status: "working-paper"
paper_type: "working-paper"
paper_version: "Final Publication Edition v2.1"
review_status: "current"
---

# Paper Review

## Review

*Pause Is Not Recovery* treats incident response in recursive AI research as a sequence of controlled changes in operational state and authority, rather than a reversible shutdown command. Its central requirement is that revocation outlive snapshots, restarts, caches and successor generations. A restored service may be technically functional but still lacks permission to resume protected operations. The paper links that rule to append-preserving incident history, separately verified recovery candidates, and fresh authorization for readmission. Sections 17–18 make the distinctions explicit through typed evidence, verdict, authorization and commit objects and operation-specific authority edges. This is more precise than treating a successful integrity check or human approval as sufficient for activation.

The contribution is strongest where restoration can resurrect an old capability. Sections 34–38 specify precedence of current revocation state over saved credentials, new generation or authority epochs after recovery, and staged re-entry with evidence-dependent transitions. The recovery bundle expressly records unresolved findings as UNKNOWN rather than treating missing evidence as success. Sections 39 and 42 also address recovery when monitors or verifiers were compromised: the bootstrap evidence must not depend entirely on the same mutable security layer. These requirements define observable failure cases, including stale credential acceptance after rollback, lost incident lineage and a direct candidate-to-production transition.

The paper is an implementation-neutral structural proposal, not an implementation report. Its minimum profile R1–R10, conformity tiers, red-team matrix and drill metrics are proposed acceptance criteria; it supplies no executed tests, measured latencies or independently verified demonstrations. The scenarios in Section 30 illustrate expected behavior rather than reported deployments. A conformity claim would require a running reference implementation, reproducible fixtures, negative tests across restoration and failover, and evidence that protected effects remained unreachable during compromised or unavailable verification.

A technical ambiguity concerns the presentation of incident states as one canonical progression from ACTIVE through PAUSED, QUARANTINED, REVOKED and RECOVERY_VERIFIED to READMITTED. Operational restrictions, revocation records and recovery-candidate status can coexist and have different scopes. Revocation is itself modeled as durable authority state, not merely a transient workflow phase. A single linear state machine therefore cannot fully express partial revocation, concurrent quarantine and staged restoration unless it is supplemented by orthogonal state dimensions and explicit transition guards. This matters for the paper's own commitment to failure locality: unrelated scopes should remain operational while affected authorities are independently invalidated.

The requirement that revocation dominate restoration is a necessary safety invariant, but enforcement across providers and partitions needs a defined authority-consistency contract. Sections 19, 22 and 25 require epoch freshness, current policy digests and fail-closed protected operations, yet do not specify how services obtain a sufficiently current revocation view when authority sources are unavailable or conflicting. This is an implementation dependency rather than a counterexample to the invariant. External actions already committed before pause also cannot be undone by internal rollback; the evidence and after-action sections recognize historical persistence, but the recovery model does not specify compensating obligations toward external counterparties.

The institutional boundary is correctly placed after technical verification. The publication distinguishes an authorization decision from a verifier verdict and requires approval tied to the recovered state and incident identifier. It does not determine who is competent to order suspension or readmission, how conflicting authorities are resolved, or what appeal and redress accompany prolonged restriction or an erroneous restart. Such questions are outside the technical conformance profile; they become material when the proposed controls are used as evidence of governance adequacy. Cryptographically intact evidence can establish what an authority decided, not whether that authority was legitimate.

Relative to this archive's *Security of the Security*, which examines separation of monitoring, verification and commit, Paper 06 applies the same non-substitution discipline to the aftermath of failure. Its distinct value is the insistence that operational recovery, trust reconstruction and renewed permission are separately evidenced transitions. The appropriate next test is a multi-provider recovery exercise that restores pre-revocation snapshots, injects stale permissions, compromises a verifier, partitions the epoch service and attempts an unauthorized readmission. Results should report rejection, lineage preservation, unaffected-service availability, false restrictions and decision latency. Until such results exist, the paper establishes a testable recovery-control design, not demonstrated safe readmission.

## Key Insight

Recovery is governable only when revoked authority cannot return through restored state and readmission is a separately evidenced decision under current policy, not an automatic consequence of technical recovery.
