---
title: "The Five-Layer Trust Stack for Agent-to-Agent Coordination: A Compositional Architecture for Verifiable, Auditable, and Deception-Resistant Autonomous Agent Interactions"
source: "https://doi.org/10.21079/11681/50507"
publication: "U.S. Army Engineer Research and Development Center, Geospatial Research Laboratory, ERDC/GRL SR-26-1, September 2026"
date_read: "2026-10-07"
primary_domain: "AI Governance"
tags:
  - "AI agents"
  - "agentic systems"
  - "authorization"
  - "delegated authority"
  - "assurance"
key_insight: "Cryptographic identity, scoped delegation, policy checks, signed commitments, and tamper-evident logs can make agent interactions more answerable, but they do not make an issuer legitimate or a recorded commitment substantively correct."
doi: "10.21079/11681/50507"
paper_type: "other"
paper_version: "ERDC/GRL SR-26-1"
review_status: "current"
---

# Paper Review

## Review

Michael G. R. Lewis’s ERDC special report proposes a compositional trust architecture for agent-to-agent coordination in federal and defense environments. It frames the problem as machine-speed deception: agents may impersonate principals, inflate delegated authority, exploit policy gaps, repudiate commitments, or evade audit. The response is a five-layer stack, with a Layer 0 governance foundation: identity, authority, policy, commitment, and audit/dispute, anchored by human policy authorship, monitoring, intervention, and accountability. The report maps these functions to existing capabilities such as ICAM, verifiable credentials, capability-based delegation, policy-as-code, signed transaction records, and tamper-evident logs. It also sketches failure semantics, disconnected operation, example scenarios, and four threat cases.

Its contribution is architectural separation. Identity answers who an agent is associated with; authority constrains what it may do; policy evaluates whether an action is allowed in context; commitments preserve what parties signed; audit supports reconstruction and escalation. This helps prevent the common collapse of agent identity into authorization and distinguishes an invalid delegation from a validly identified agent attempting a prohibited action. Layer 0 is also a valuable reminder that technical controls need named human authorities for policy lifecycle, credential issuance and revocation, intervention, and post-incident accountability. The report explicitly presents itself as a structured thought exercise to inform future architecture decisions, not as a validated prescription.

That scope matters when assessing the report’s deception-resistance and performance claims. The red-team section describes how four representative attacks might be mitigated, but reports no implemented prototype, adversarial exercise, or measured outcome. The stated per-layer and aggregate latencies are estimates, not results from a specified test environment. They establish a set of design hypotheses and useful questions for implementation; they do not demonstrate that the composition resists deception or meets machine-speed requirements under operational load. A fair defense is that the report is intentionally exploratory and its examples are illustrative. That resolves any criticism that it lacks field validation as a contribution defect, but it does not support treating the stack as assurance evidence or a ready-made control baseline.

The institutional boundary remains the hardest part. A signature can establish that a key signed a credential or commitment; it cannot establish that the issuer had legitimate authority, that the policy reflects valid institutional direction, or that the recorded delivery fulfilled the real-world obligation. The stack recognizes this distinction in Layer 0, but the governance layer is described as doctrine, structure, and tooling rather than specified decision rights. Who approves policy changes, under what mandate, with what review or appeal? Who arbitrates disputes across organizations that do not share a trust anchor? The report identifies mutual trust negotiation as unresolved, alongside policy synthesis, assumption drift, and behavioral baselines. These are central governance dependencies, not peripheral implementation details.

Disconnected operation makes lifecycle control especially consequential. Pre-issued credentials, delegation tokens, and cached policy bundles allow local work to continue, but revocation and policy changes may not reach a disconnected node until synchronization resumes. The report correctly treats token and policy lifetimes as security parameters; it does not specify how acceptable stale-authority windows are determined, who bears their risk, or how conflicting local logs and decisions are reconciled. Tamper evidence can preserve records, yet audit logs also need access controls, retention rules, privacy protections, and an accountable route from anomaly detection to remedy. Detection and attribution do not themselves constrain an authorized agent acting maliciously within scope.

The report makes agent coordination more governable by giving architects a vocabulary for authority, policy, commitments, and failure. Its value is as a design framework and implementation agenda. Operational assurance would require prototypes and adversarial tests, explicit trust-anchor and revocation semantics for connected and DIL settings, policy change control, independent dispute handling, and evidence that intervention works within defined time bounds. Until those are specified and tested, the stack is a promising account of where controls belong, not proof that an interaction is trustworthy.

## Key Insight

Cryptographic identity, scoped delegation, policy checks, signed commitments, and tamper-evident logs can make agent interactions more answerable, but they do not make an issuer legitimate or a recorded commitment substantively correct.
