---
title: "Critique of Agent Model"
source: "https://arxiv.org/abs/2606.23991"
source_url: "https://arxiv.org/abs/2606.23991"
publication: "arXiv"
date: "2026-06-22"
date_read: "2026-08-03"
issue_url: "https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/issues/61"
primary_domain: "AI Governance"
domain: "AI Governance"
tags:
  - AI agents
  - agentic systems
  - AI safety
  - alignment and safety
  - accountability
  - delegation
scholarly_signal: "cs.AI"
key_insight: "The paper correctly identifies that advanced agents redistribute control by internalising goals, identity, deliberation, and learning, but it mistakes architectural visibility for governability: an inspectable module is not an accountable institution unless authority, constraint, revocation, evidence, and redress are executable around it."
---

# Paper Review

## Review

The paper distinguishes agentic systems, whose competence is assembled through tools and workflows, from agentive systems, whose goals, identity, planning, self-regulation, learning, and coordination are maintained internally. Its Goal-Identity-Configurator architecture turns that distinction into a proposed model: persistent objectives are decomposed into subgoals, identity evolves from experience, a configurator selects between reactive action and world-model-based planning, and learning continues through real and simulated interaction. The separation of the agent model, which selects action, from the world model, which predicts consequences, is useful because it preserves different training signals and clarifies whether failure arose from prediction, evaluation, planning, or execution.

This is also an allocation of decision rights. External scaffolding leaves workflow designers visibly responsible for task boundaries, tool access, update schedules, and escalation. GIC moves those choices into learned components that can revise goals, self-understanding, reasoning effort, and training activity during operation. The paper calls this internalisation genuine agency. From a governance perspective, it is delegated authority becoming adaptive, persistent, and partially self-administered. The relevant question is not only whether the model acts more autonomously, but who may grant that autonomy, which decisions remain non-delegable, and how affected parties can contest the consequences.

The survey is synthetic rather than systematic, and GIC remains conceptual. No complete implementation, ablation study, benchmark comparison, or open-world deployment evidence is presented. The four theorems establish conditional advantages, but their premises carry much of the conclusion. Identity revision helps when revisions reliably move toward a value-maximising self-model; world-model planning cannot degrade a policy when prediction error is bounded and planning is used above a correctly calibrated margin; simulated experience helps when the simulator is sufficiently faithful; and the MPC result assumes reward and cost are perfectly aligned. They do not show that the required bounds, value functions, update monotonicity, or alignment conditions can be established in consequential environments.

The central governance gap appears in the treatment of identity. The paper defines identity broadly enough to include capabilities, constraints, relationships, values, loyalties, and moral commitments, then allows it to evolve rapidly without retraining. Identity therefore becomes a mutable policy layer, not simply a self-description. Yet the architecture does not specify protected identity invariants, authorised evidence sources, approval thresholds for consequential changes, rollback procedures, version histories, or who may challenge a self-model that has drifted. Endogenous identity may improve adaptation while weakening the stability of delegated authority.

The safety argument overclaims what modularity can deliver. The paper reduces harmful behaviour to goal misspecification or component imperfection and argues that sufficiently trained components drive harm toward zero unless the human-supplied terminal goal is wrong. This excludes institutional failure: ambiguous authority, conflicting principals, unlawful instructions, legitimate refusal, cumulative externalities, adversarial governance, and harms imposed on people who never supplied the goal. A terminal goal may remain textually fixed while decomposition, identity, world modelling, reward estimation, and self-directed learning alter its operational meaning. Persistent goals still create principal-agent problems.

Layered outputs can improve observability, but observability is not accountability. Inspecting a subgoal does not establish that a reviewer has time, competence, authority, or evidence to stop it. Audit logs do not provide revocation. Component attribution does not determine liability. Human oversight is invoked without specifying intervention latency, safe-state transitions, escalation, or what happens when learning has already changed the system. The claim that agentive systems remain under human control therefore lacks an operational control model.

The PEG framework measures performance, efficiency, and growth, but omits governance outcomes. Evaluation should also cover mandate fidelity, authority-boundary compliance, reversibility, shutdown reliability, identity drift, policy-change traceability, uncertainty calibration, incident containment, and remedy. Multi-agent coordination is treated as an emergent capability, although emergent organisation can create coalitions and informal authority that no single component audit captures.

GIC should be extended with a governance plane external to the learning loop. Terminal goals need signed provenance, scope, duration, precedence, and revocation semantics. Goal decomposition and identity evolution need protected constraints, versioned change records, independent policy checks, and thresholds that trigger approval or safe suspension. The configurator should route to mandatory escalation, refusal, and containment states that it cannot rewrite through learning. World-model uncertainty must become enforceable deployment limits rather than advisory confidence. Incident evidence should support reconstruction, attribution, correction, and appeal by affected parties.

The paper makes agency more architecturally legible, but it does not make autonomous authority legitimate. Its contribution is to show where control would move inside a more agentive system. The unresolved task is to build the institutional machinery that constrains that movement before persistence, self-modification, and self-directed learning turn delegated capability into unreviewable power.
## Key Insight

The paper correctly identifies that advanced agents redistribute control by internalising goals, identity, deliberation, and learning, but it mistakes architectural visibility for governability: an inspectable module is not an accountable institution unless authority, constraint, revocation, evidence, and redress are executable around it.
