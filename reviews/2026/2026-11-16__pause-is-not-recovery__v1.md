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
review_status: "superseded"
---

# Paper Review

## Review

*Pause Is Not Recovery* treats incident response in recursive AI research as changes in operational state and authority, not a reversible shutdown command. Revocation must survive snapshots, caches and successor generations. A restored service can be technically functional without permission to resume protected operations. Sections 17–18 distinguish evidence, verification verdict, authorization and commit through typed objects and operation-specific authority edges.

The contribution is clearest where restoration could resurrect an old capability. Sections 34–38 require current revocation state to override saved credentials, fresh generation or authority epochs after recovery, and staged readmission with evidence-bound transitions. Recovery bundles retain unresolved findings as UNKNOWN rather than treating missing evidence as success. Sections 39 and 42 address compromised monitors and verifiers: the recovery bootstrap must not depend solely on the same mutable security layer. Tests can reject stale credentials, erased lineage and direct candidate-to-production transitions.

This is an implementation-neutral structural proposal, not an evaluated deployment. The minimum profile R1–R10, conformance tiers, red-team matrix and drill metrics define candidate tests; the paper reports no executed suite, measured control latency or independently verified recovery. Section 30's scenarios are worked illustrations. Operational assurance would require reproducible fixtures across restoration and failover, including proof that protected effects remain unreachable when verification is compromised or unavailable.

One specification ambiguity concerns the canonical progression from ACTIVE through PAUSED, QUARANTINED and REVOKED to RECOVERY_VERIFIED and READMITTED. Operational restriction, revocation and recovery-candidate status can coexist at different scopes. Revocation is durable authority state, not only a sequential workflow phase. A linear machine therefore needs orthogonal state dimensions and explicit guards for partial revocation, concurrent quarantine and staged restoration. This supports the paper's failure-locality requirement.

Revocation precedence also depends on a consistent authority source across providers and network partitions. Sections 19, 22 and 25 require epoch freshness and fail-closed protected operations, but do not define a consistency contract for unavailable or conflicting revocation views. Nor can rollback undo external effects already committed before pause. The paper requires preserving their history, but does not specify corresponding compensation duties or redress for external counterparties.

The institutional boundary is appropriately placed after technical recovery. Approval is bound to state and incident, and a verifier verdict does not authorize resumed activity. Yet the paper does not establish who may order suspension or readmission, resolve competing authorities or review erroneous restrictions. These become necessary if conformance is presented as governance adequacy. Authentic evidence establishes what was decided, not whether the deciding authority was legitimate.

Compared with this archive's *Security of the Security*, which addresses independence of monitoring, verification and commit, Paper 06 applies those separations to the aftermath of failure. Recovery and fresh permission demand distinct evidence. The next test should restore pre-revocation snapshots, replay stale tokens, compromise a verifier, partition the epoch service and attempt unauthorized readmission across provider boundaries. Results should report rejection, evidence continuity, unaffected-service availability, false restrictions and decision latency. The paper establishes a testable recovery-control architecture, not demonstrated safe readmission.

## Key Insight

Recovery is governable only when revoked authority cannot return through restored state and readmission is a separately evidenced decision under current policy, not an automatic consequence of technical recovery.
