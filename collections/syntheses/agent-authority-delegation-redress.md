---
title: "Agent authority, delegation and redress"
collection: "agent-authority-delegation-redress"
last_reviewed: "2026-09-03"
status: "current"
source_reviews:
  - reviews/2026/2026-03-05__ai-agents-and-the-next-layer-of-india-s-digital__v1.md
  - reviews/2026/2026-08-03__critique-of-agent-model__v1.md
  - reviews/2026/2026-09-03__accountable-yet-anonymous-ai-agents__v1.md
---

# Collection Synthesis

Across these reviews, a consistent governance boundary appears: **agent capability is not equivalent to agent authority, and attribution is not equivalent to legitimate accountability**.

The March review of *AI Agents and the Next Layer of India's Digital Infrastructure* identifies the infrastructure problem early. If software agents transact or negotiate for people and institutions, identity binding alone is insufficient. Delegated authority needs scope, duration and revocation, and agent ecosystems need discovery, trust and assurance mechanisms capable of surviving fraud, mandate escalation and concentrated infrastructure dependencies.

The August review of *Critique of Agent Model* makes the same problem visible inside the agent architecture itself. Moving goals, identity, planning and learning from external workflow scaffolding into adaptive components redistributes decision rights. Architectural observability may expose where a decision formed, but it does not establish who authorised that decision, which boundaries the agent may not rewrite, whether authority can be revoked, or how an affected party obtains correction and remedy. The proposed governance requirement therefore shifts from monitoring autonomy to constraining mutable delegated authority.

The September review of *Accountable yet Anonymous AI Agents* adds a more concrete identity and accountability architecture. Split-knowledge binding can make actions traceable to an agent and, under legal process, to a principal without routinely disclosing principal identity to business actors. But the review shows why provenance and attribution remain distinct from legitimacy: a trace can identify a bound principal without proving that the principal authorised the specific action, that delegation remained current, or that tracing and revocation powers themselves are governed legitimately.

Taken together, the reviews suggest a reusable institutional model for consequential agents. A governance-grade agent system needs at least four separable layers: **principal and agent binding; current and action-specific authority; enforceable capability boundaries and revocation; and surviving evidence capable of supporting contest, correction and redress**. Collapsing those layers creates recurring category errors. Identity is treated as authority, logging as accountability, observability as control, and technical revocation as legitimate institutional remedy.

The unresolved research problem is therefore not simply how to make agents more autonomous or more attributable. It is how to preserve a verifiable chain from principal mandate to action-specific authority while ensuring that neither the agent nor the infrastructure operator can silently enlarge that mandate, and while giving affected parties a practical route to challenge or reverse harmful acts. Future reviews in this collection should test whether proposed agent architectures implement that chain or merely assume it.

## Traceability

This synthesis is a human-edited analytical artifact produced with AI/LLM assistance under `AI-USAGE.md`. Its claims should be read through the three constituent reviews listed in front matter and, through them, against the underlying papers.
