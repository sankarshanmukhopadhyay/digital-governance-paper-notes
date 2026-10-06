---
title: "From Intent to Execution Grant: An Execution-Boundary Conformance Profile for High-Risk AI Actions"
source: "https://arxiv.org/abs/2609.11596v1"
publication: "arXiv preprint; Mengting Wu, Lin Wang, Yong Zhang, Jiang Deng"
date_read: "2026-10-06"
primary_domain: "Trust Infrastructure"
tags: ["authorization", "authority", "assurance", "provenance", "deployment controls", "interoperability"]
scholarly_signal: "cs.CR"
key_insight: "A verified permission record becomes dependable execution authority only when current validation, grant consumption and the protected effect share an enforceable boundary whose policy owners remain accountable."
published: "2026-09-10"
doi: "10.48550/arXiv.2609.11596"
peer_review_status: "preprint"
paper_type: "preprint"
paper_version: "arXiv v1"
review_status: "current"
---

# Paper Review

## Review

Wu and colleagues specify EBL-Core as a semantic conformance profile for the transition from an AI-proposed action to executable authority. One fully materialized candidate is bound to structured intent, Root and Operational Policies, evidence obligations, context, time and a verifiable decision derivation. The Execution Release Contract records this adjudication but carries no authority itself. A verified ALLOW contract may support a separate Execution Grant, which must pass current validation when redeemed. An earlier approval cannot authorize a substituted recipient, changed policy version or altered decision-relevant evidence.

Sections 3–5 make several governance requirements operational. Operational rules cannot weaken root constraints or reinterpret their evidence obligations; only obligation-relative VALID evidence discharges a positive requirement. UNKNOWN, MISSING, EXPIRED and CONFLICT are distinct refusal states. Determinism depends on a closed input bundle rather than undeclared clocks or lookups. Validation, the transition from ISSUED to CONSUMED and the protected effect must share a logical linearization point. Revocation prevents execution when it wins that ordering, but cannot undo an already consumed grant. L2 is the minimum full execution-release conformance level; decision compatibility alone does not qualify.

Section 6 supplies bounded executable evidence. The financial-transfer artifact reports 34 static vectors, 15 lifecycle checks, 100 trials of 32 concurrent redemptions and 100 revoke-redeem races. I reran the ancillary validation package and reproduced the passing corpus and lifecycle results, with one successful redemption and protected test effect per concurrency trial. Revocation won all 100 races in this rerun, which therefore did not exercise both race orderings. The verifier reconstructs decisions without calling the adjudicator, but shares canonicalization and commitment primitives; neither the authors nor these results establish independently developed interoperability. Formal propositions remain proof sketches rather than mechanized correspondence with the implementation.

The material deployment boundary is the effect transaction. An in-memory lock can serialize a protected callback; it does not show that a remote payment, durable grant state and crash recovery preserve the same commitment boundary. The authors explicitly acknowledge this limitation and require linearization, so it would be unfair to accuse the profile of accepting a check-then-execute race. That counterargument resolves a specification criticism, not the missing deployment evidence. At-most-once redemption also cannot by itself establish completed external execution or recovery after an ambiguous failure. Fault injection across effect, state persistence, restart and retry would determine whether an adapter satisfies the contract rather than merely claiming it.

Compared with Authorization Architectures for Tool-Using AI Agents and Authority Continuity Across Agentic Trajectories in this archive, EBL-Core supplies a more precise contract for one execution boundary. Its novelty is mandatory composition and conformance semantics, not a new authorization primitive or proof that Cedar, Rego or capability systems cannot encode the requirements. Cross-domain coverage and independent adapters remain proposed evaluation stages.

My governance judgment is that this is a useful executable specification for procurement and integration testing, not a certificate of trustworthy deployment. Evidence validity does not establish truth, trusted structured intent does not establish human understanding, and root-policy non-weakening does not constrain an authorized replacement of the root. The institutional implication is that discretion moves upstream to intent authorities, evidence resolvers, policy owners and grant issuers. Those actors need named responsibilities and correction or redress procedures outside the core profile. Independently developed parsers and verifiers, durable distributed effect tests and a documented authority topology would materially strengthen operational confidence while keeping compliance distinct from legitimacy.

## Key Insight

A verified permission record becomes dependable execution authority only when current validation, grant consumption and the protected effect share an enforceable boundary whose policy owners remain accountable.
