---
title: "Doot: The AI Agent for Every Indian Citizen"
source: "https://digidoot.in/Doot_WhitePaper.pdf"
publication: "DigiDoot / India AI Mission White Paper"
date_read: "2026-03-09"
primary_domain: "Digital Public Infrastructure"
tags:
  - AI agents
  - agentic systems
  - AI governance
  - digital public infrastructure
  - India
  - India Stack
  - trust assurance
  - interoperability
  - public infrastructure
  - governance-by-design
  - public administration
scholarly_signal: "cs.AI"
key_insight: "The next layer of digital public infrastructure may be citizen-owned AI agents that mediate interaction between individuals and complex administrative systems."
---

# Paper Review

## Review

The DOOT / Agent-One proposal attempts to solve a genuine constraint in agent systems. Persistent agents are difficult to operate reliably on mobile devices, yet many current agent designs quietly assume continuous execution. The architecture therefore separates the system into three layers: signal detection, identity routing, and machine-to-machine exchange. In effect the agent remains dormant until an incoming signal indicates that an obligation, notification, or institutional request requires attention. This decomposition is directionally sound. It reframes agents not primarily as conversational assistants but as infrastructure that monitors signals and activates when action is required.

The proposal becomes more complex when viewed through a governance lens. Once agents begin responding to institutional obligations the central question is no longer whether a signal can reach the device. The critical question becomes whether the signal is legitimate and whether the requested action should be allowed to influence the user. If agents are designed to wake, escalate, or trigger workflows in response to institutional signals, then authority verification becomes a foundational requirement. Without mechanisms such as verifiable institutional identity, trust registries, or provenance frameworks, the architecture risks turning personal agents into programmable compliance endpoints for any actor capable of generating a signal.

The signalling layer itself remains intentionally abstract in the proposal. While this abstraction allows experimentation across different communication channels, it also exposes an important trust gap. If early implementations depend on existing notification ecosystems without a defined authority model, the system inherits their weaknesses. Signals may be ambiguous, manipulated, or issued by actors whose mandate is unclear. When such signals are fed into automated agent behaviour on personal devices, even small uncertainties in authority can scale into systemic harms.

The architecture also implicitly introduces a policy engine into the personal device. Agents that interpret obligations must eventually decide when to notify, escalate, defer, or act. These decisions encode governance logic. Conflicting institutional requests, ambiguous obligations, or coercive signalling practices will inevitably appear once such systems operate at scale. Without defined safeguards, dispute resolution mechanisms, and transparency around decision rules, the architecture risks automating institutional power rather than responsibly mediating it.

The core idea behind obligation-driven agents is important and directionally correct. Future digital systems will likely shift from query-driven interaction toward systems that respond to verified obligations and commitments. However such systems cannot rely solely on technical architecture. They require an accompanying layer of governance infrastructure that establishes institutional legitimacy, signal provenance, and clear boundaries around automated action. Without these safeguards, the architecture risks amplifying authority without adequate mechanisms for accountability or harm prevention.

## Key Insight

Citizen-owned AI agents could become the next interface layer of digital public infrastructure, reshaping how individuals interact with governments and markets.
