---
title: "Interaction Creates Dynamical AI Behavior Absent in Isolation"
source: "https://arxiv.org/abs/2608.07457"
publication: "arXiv"
date_read: "2026-09-16"
primary_domain: "AI Safety & Evaluation"
tags: ["AI agents", "agentic systems", "assurance", "coordination"]
scholarly_signal: "cs.AI"
key_insight: "If interaction topology and message history can create behavior absent in isolated agents, assurance cannot stop at the model boundary: the relationship, protocol and composition become part of the governed system."
published: "2026-08-07"
peer_review_status: "preprint"
paper_type: "preprint"
paper_version: "v1"
review_status: "current"
---

# Paper Review

## Review

This paper presents a deliberately minimal experiment in which two parameter-identical 124-million-parameter GPT-2 agents exchange generated text under no interaction, one-way interaction in either direction, and mutual interaction. Across 200-round runs at two decoding temperatures, the authors find that the receiving or "subordinate" agent can move into a behavioral state not exhibited by either isolated agent, while reversing communication direction reverses which agent changes. Under mutual listening both agents move toward the altered state. Pre-recorded messages can reproduce much of the effect, and changing message order can change behavior. A three-state kinetic model is offered to explain the interaction as an information-driven dynamical system.

The governance significance is compositional. Conventional assurance often treats a model or agent as the evaluation object and then assumes that sufficiently characterized components remain sufficiently characterized after deployment. This experiment shows why that assumption needs testing. The same parameters and decoding settings do not determine behavior once another agent's output becomes part of the retained context. Directionality, ordering, interaction history and communication topology become control parameters. In an operational multi-agent system, the governed object may therefore need to include the relationship and protocol, not merely the participating models.

The paper does not establish that contemporary production agents will exhibit the same dynamics. GPT-2 is a small, pre-instruction-tuning base model, the experiment uses a specific archived classifier and low-temperature setup, and the authors explicitly frame the work as a minimal system suited to studying dynamics. Those limits matter. The governance inference should be narrower: isolated-agent evidence is not sufficient by construction to establish composition safety when interaction itself is a causal variable.

That narrower finding is still consequential. Multi-agent assurance should record who can send context to whom, whether communication is reciprocal, what history is retained, what transformations or filters intervene, and which relationship states authorize continued exchange. Monitoring should detect composition-level state changes rather than only component failures. Revocation must be capable of terminating a relationship or communication edge, and incident evidence must preserve interaction history well enough to reconstruct how an otherwise acceptable component entered an unacceptable state.

The paper's next operational step would be to test whether the effect survives across instruction-tuned models, heterogeneous agents, tool-using workflows and bounded protocols, then define negative tests for topology, ordering and retained-context changes. That would turn an intriguing dynamical result into evidence usable by multi-agent governance and assurance systems.

## Key Insight

If interaction topology and message history can create behavior absent in isolated agents, assurance cannot stop at the model boundary: the relationship, protocol and composition become part of the governed system.
