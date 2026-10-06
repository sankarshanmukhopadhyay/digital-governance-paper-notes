---
title: "Authority Continuity Across Agentic Trajectories: A Comparative Reconstruction of Authority Transitions in Real-World AI Agent Incidents"
source: "https://doi.org/10.5281/zenodo.22923341"
publication: "HibriMind preprint, Joaquim Santos Albino; Zenodo source recorded in issue #183"
date_read: "2026-10-06"
primary_domain: "AI Governance"
tags: ["AI agents", "authority", "authorization", "delegation", "accountability", "evidence"]
key_insight: "Authority checks must govern the next action before an agent crosses a boundary, while leaving the competence and legitimacy of the authorizing institution open to challenge."
published: "2026-09-23"
peer_review_status: "preprint"
paper_type: "preprint"
paper_version: "v0.1"
review_status: "current"
---

# Paper Review

## Review

Joaquim Santos Albino's preprint distinguishes continued pursuit of an assigned purpose from continued authority to act. An agent can discover credentials, reach a real target, or engage a new counterparty without abandoning its task, yet lack permission for the next action. Authority continuity requires a demonstrable relationship between the action now possible and a source competent to authorize it. Sections 13–14 locate the control before execution: unresolved applicability should trigger suspension rather than allow completed action to settle the authority question.

The evidence is comparative reconstruction of four cyber-evaluation incident families, with Taiwan's reported offensive campaign as a negative control and Meta Muse–Amazon as an inter-authority boundary case. These are heterogeneous public disclosures, not independently replayed trajectories. The UK AI Security Institute case supports the possibility that task pursuit produces unauthorized action; OpenAI's sequence also involves documented goal-related misalignment. Gemini distinguishes stopping after entry from governing the boundary before entry. Anthropic's later discovery of an additional incident makes retrospective reconstruction a separate responsibility. The paper explicitly preserves these causal differences rather than treating authority discontinuity as their common cause.

The Taiwan comparison requires a narrower reading than the term negative control suggests. Absence of public evidence that agents exceeded their operators' instructions cannot establish that authority remained intact. The author acknowledges that the originating operation's legitimacy is separate. The case therefore challenges autonomy as a sufficient diagnostic, but cannot validate competent authorization. This distinction exposes a pressure point in the model: instructions from an operator, permission recognized by a service, and legitimate institutional authority are different propositions.

The paper earns an analytical contribution, not a validated preventive mechanism. Its state model identifies purpose, identities, authority, capability and veto, but supplies neither a reproducible transition-coding protocol nor a tested decision procedure for determining when authority applicability has changed. This is a scope boundary for an exploratory preprint, not evidence that the proposal fails. However, the proposed suspension rule depends on detecting the relevant change before the action commits, preserving current authority state, and assigning an accountable decision-maker when sources conflict. A model that narrates its own compliance would not independently establish any of those conditions.

Compared with the archive's review of Authority is a Continuous System, this paper shifts attention from preserving a bounded execution lineage to reassessing authority when execution constructs a new operational context. It does not establish that existing authorization architectures cannot implement that reassessment. Its value is the discriminating question, rather than proof of a uniquely necessary architecture.

The Muse case makes the institutional consequence visible. A platform can deny recognition to a user's delegation; that denial does not itself settle whether its gatekeeping is legitimate. My governance judgment is that authority continuity should become an action-boundary requirement with contestable sources of authority, not a technical endorsement of whichever operator controls access. A useful next test would compare authority-aware enforcement against ordinary authorization controls on matched traces, measuring unauthorized boundary crossings, unnecessary suspensions, revocation races and recoverable decision evidence. Independent transition coding and disputed-authority cases would show whether the concept adds operational discrimination without merely relocating discretion into an opaque policy gate.

## Key Insight

Authority checks must govern the next action before an agent crosses a boundary, while leaving the competence and legitimacy of the authorizing institution open to challenge.
