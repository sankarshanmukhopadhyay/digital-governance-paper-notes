---
title: "Authorization Architectures for Tool-Using AI Agents"
source: "https://arxiv.org/abs/2609.15906v1"
publication: "arXiv preprint; Rakesh Kumar Surapani, Pradeep Kumar Dolabehera Kakitapelli, Arun Morampudi, Praveena Padi"
date_read: "2026-10-06"
primary_domain: "AI Governance"
tags: ["AI agents", "authorization", "delegation", "accountability", "deployment controls", "evidence"]
scholarly_signal: "cs.CR"
key_insight: "Independent enforcement can constrain an agent's actions, but accountable delegation also requires evidence that the enforced scope was legitimately granted and a remedy for people harmed by its exercise."
published: "2026-09-14"
doi: "10.48550/arXiv.2609.15906"
peer_review_status: "preprint"
paper_type: "preprint"
paper_version: "arXiv v1"
review_status: "current"
---

# Paper Review

## Review

Surapani and colleagues organize agent authorization around the moment a proposed tool call becomes an external effect. Their structured narrative review retains 89 sources from approximately 180 candidates and derives seven requirements: attributable principal chains, explicit delegation, monotonic attenuation, aggregation bounds, task-sensitive temporal validity, independent runtime enforcement and tamper-resistant audit. Its contribution is an integrated assessment framework, not a new access-control primitive or a validated deployment specification.

The separation of delegation and information-provenance graphs in Section 2.3 is consequential. A credential can preserve who delegated while untrusted content determines what the delegate attempts. Treating prompt injection as authority borrowing therefore relocates control from detecting suspicious language to independently checking the action, arguments and influencing sources. Section 8.5's denied calendar-to-salary-to-email sequence demonstrates why a guard with workflow context and a resource boundary that blocks bypass must compose. This is a worked architectural trace, not an executed experiment.

The evidence discipline is useful: Tables 5–6 distinguish coverage within a mechanism's declared scope, evidence maturity and deployment scope. Operational token infrastructure does not become evidence of task-aware authorization merely because it is mature. The authors also distinguish key-holder signatures from proof of human intent in Section 7.3. Their absence claims remain bounded to the searched corpus. The supplied PDF references supplementary screening and cell-level coding tables that are not included in it; those materials were not available for this review, limiting independent reproduction of the ratings. The illustrative cross-organizational configuration is likewise a specified arrangement, not evidence that every federated implementation lacks the controls rated absent.

One deployment recommendation undermines the framework's own logic. Section 8.3 allows minimal single-agent systems to prioritize identity, enforcement and audit while treating explicit delegation, aggregation bounds and temporal validity as progressive hardening. A short chain reduces multi-hop attenuation complexity; it does not remove the need to distinguish an authorized read from an unauthorized send, terminate a cancelled task, or constrain inference across multiple sources. The authors' reasonable counterargument is proportional implementation cost. That supports simpler representations and controls, not postponing the authority semantics needed to decide whether enforcement is correct.

The human-principal hierarchy also needs institutional qualification. Section 2.3 groups users and data subjects as the source of legitimate authority, although a requesting employee, an affected person and an organization exercising a statutory power have different entitlements. Section 8.6 recognizes contestability, and Section 9.3 explicitly identifies liability and issuer trust as open problems. These acknowledgments prevent a claim that the paper ignores governance. Nevertheless, reconstructable logs are evidence for contestation, not an adjudicator, a duty to respond or a remedy. Signed delegation cannot make an unauthorized institutional grant legitimate, nor transfer the operator's responsibilities to the requesting user.

Read alongside Authority Continuity Across Agentic Trajectories in this archive, the survey supplies candidate enforcement locations and evaluation requirements for the next-action boundary; it does not demonstrate that their composition preserves authority under changing context. My judgment is that R1–R7 are a useful procurement and assurance question set, provided coverage ratings are not treated as certification. Operational confidence would require replayable tests of scope synthesis, bypass paths, revocation races and cumulative information use, reporting legitimate task completion, false denials and enforcement latency together. Institutional confidence additionally requires named policy owners, trusted sources for decision attributes, evidence-access rules and a correction or redress path available to affected people.

## Key Insight

Independent enforcement can constrain an agent's actions, but accountable delegation also requires evidence that the enforced scope was legitimately granted and a remedy for people harmed by its exercise.
