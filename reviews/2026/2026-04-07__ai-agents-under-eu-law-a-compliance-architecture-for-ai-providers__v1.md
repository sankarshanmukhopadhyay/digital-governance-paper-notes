---
title: "AI Agents Under EU Law: A Compliance Architecture for AI Providers"
source: "https://arxiv.org/abs/2604.04604"
source_url: "https://arxiv.org/abs/2604.04604"
publication: "arXiv working paper"
date: "2026-04-07"
date_read: "2026-05-04"
domain: "Law, Regulation & Liability"
primary_domain: "Law, Regulation & Liability"
tags:
  - "AI agents"
  - "AI governance"
  - "AI regulation"
  - "agentic systems"
  - "risk assessment"
  - "cyber risk"
  - "authority"
  - "accountability"
  - "deployment controls"
  - "regulatory alignment"
  - "transparency and accountability"
scholarly_signal: "cs.CY"
key_insight: "The paper’s strongest move is to relocate AI agent compliance from model classification to action inventory: what the agent can touch, change, disclose, delegate, or trigger is the real regulatory map. Its unresolved weakness is that it treats provider compliance architecture as the main control surface while leaving legitimacy, redress, and affected-party power underdeveloped."
---

# Paper Review

## Review

This paper is one of the more operationally useful attempts to translate the EU AI Act and adjacent EU digital regulation into a compliance architecture for AI agents. Its core claim is that agentic AI should not be governed primarily by architectural labels. The decisive object is the action surface: external tools, data flows, connected systems, affected persons, runtime memory, and the legal triggers activated by concrete operations. That is the right governance move. Agents redistribute decision rights not because they generate text, but because they invoke tools, alter records, send communications, rank people, move money, deploy code, and coordinate action chains with reduced human involvement.

The paper’s most important contribution is the external-action inventory. It shows why the same LLM-plus-tool-calling pattern can be low-risk in a research assistant, high-risk in recruitment, safety-critical in healthcare, and cyber-regulated in DevOps. This shifts compliance analysis from “what is the model?” to “what institutional authority has been delegated to the system?” That framing is materially stronger than a large share of AI governance writing because it treats governance as a runtime and value-chain problem rather than a documentation problem.

The paper is also valuable because it refuses to isolate the AI Act from the rest of the EU digital regulatory stack. It maps the AI Act against the GDPR, Cyber Resilience Act, Digital Services Act, Data Act, Data Governance Act, NIS2, DORA, sectoral regimes, and revised product liability rules. This matters because agent providers do not face one regulatory perimeter. They face regulatory stacking, where a single action can trigger data protection duties, cybersecurity obligations, platform accountability, sectoral supervision, and liability exposure at the same time. The paper’s twelve-step compliance sequence is useful precisely because it makes that stacking legible.

The strongest governance insight concerns runtime behavioral drift. The authors are right that a high-risk agent whose behavioral drift cannot be traced, bounded, or replayed cannot credibly satisfy essential requirements around oversight, logging, robustness, post-market monitoring, and conformity assessment. This is not a speculative legal concern. It is a control-plane failure. If the provider cannot show whether the deployed system remains within the assessed operating envelope, the conformity claim becomes structurally unverifiable.

The paper is also sharp on cybersecurity. It correctly rejects prompt-level restraint as a security control. For agents with tool access, privilege minimization has to live outside the generative model, at the API, identity, authorization, and execution layer. This is the right distinction. A model instruction saying “do not delete files” is not equivalent to an interface that never exposes delete capability. The same logic applies to human oversight. Oversight cannot be a performative checkbox if the system can act before authority is exercised or if the human reviewer is reduced to a liability sink after irreversible action.

The main weakness is that the paper is more mature on compliance architecture than on legitimacy architecture. It identifies affected persons, transparency obligations, and human oversight, but the deeper question remains underdeveloped: who gets a meaningful say when an agent’s action affects them, not merely when the provider documents the system? Compliance can make a provider legible to a regulator without making the system contestable by the people subject to its actions. The paper’s control surface is provider-centric. That is understandable for an AI provider compliance paper, but it leaves the institutional problem partially unresolved.

Redress is the clearest gap. The paper says a great deal about classification, standards, conformity assessment, logs, monitoring, and reporting. It says less about appeal, correction, revocation, remedy, and affected-party challenge. For agentic systems, this is not a secondary concern. The ability to reconstruct an action chain after harm is not the same as the ability to stop, challenge, reverse, or remedy an illegitimate action in time. The paper’s architecture needs a stronger redress layer tied to action-level receipts, accountable authority, and enforceable intervention rights.

There is also a risk of over-reliance on standards as the route from legal obligation to operational control. The paper repeatedly acknowledges that harmonised standards are incomplete, delayed, or not agent-specific enough. Yet its compliance architecture still leans heavily on future standards as the organizing path. That is defensible as a provider strategy, but it should be treated as a transitional governance assumption, not a stable end state. Standards can create presumption of conformity. They do not automatically create legitimacy, institutional accountability, or power-aware oversight.

The paper’s novelty lies less in any single legal interpretation and more in its systems integration. It connects agent categories, action inventories, regulatory triggers, harmonised standards, cybersecurity, human oversight, runtime drift, and adjacent EU instruments into one provider-facing operating model. Its practical impact could be high for legal, product, security, and governance teams trying to move beyond AI Act summaries into deployable compliance programs.

The recommended next step is to convert the paper’s action inventory into machine-readable governance artifacts: action ontologies, risk-tier bindings, authorization policies, oversight routing rules, decision receipts, drift thresholds, revocation paths, and redress workflows. That is where the paper’s argument becomes infrastructure. Without those artifacts, the compliance architecture remains an advanced checklist. With them, it becomes a control plane for agentic systems.

## Key Insight

The paper’s strongest move is to relocate AI agent compliance from model classification to action inventory: what the agent can touch, change, disclose, delegate, or trigger is the real regulatory map. Its unresolved weakness is that it treats provider compliance architecture as the main control surface while leaving legitimacy, redress, and affected-party power underdeveloped.
