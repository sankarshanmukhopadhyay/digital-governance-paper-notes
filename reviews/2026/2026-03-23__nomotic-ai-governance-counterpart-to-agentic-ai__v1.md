---
title: "Nomotic AI: The Governance Counterpart to Agentic AI"
source: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6069888"
publication: "SSRN (Independent Researcher)"
date_read: "2026-03-23"
primary_domain: "AI Governance"
tags:
  - AI governance
  - agentic systems
  - AI safety
  - authorization
  - accountability
  - governance-by-design
  - delegated authority
  - regulatory alignment
  - AI ethics
scholarly_signal: "cs.AI"
key_insight: "Agentic AI systems operating in production environments have exposed a fundamental governance gap: the distinction between what systems can do (capability) and what they should do (governance) remains uncaptured by existing vocabulary, requiring a new conceptual category that treats governance as co-equal with capability rather than as afterthought compliance."
---

# Paper Review

## Review

Hood introduces Nomotic AI, a conceptual framework positioned explicitly as the governance counterpart to agentic AI. The core contribution is terminological and architectural: recognizing that the discourse around agentic systems has become capability-centric while governance vocabulary remains underdeveloped, Hood proposes that "law" (from Greek nomos) should be as central to AI discourse as "action."

The paper's strength lies in its crisply articulated problem statement. Organizations deploying agentic systems are experiencing predictable failure modes (unauthorized actions, security vulnerabilities, compliance violations) not because the systems malfunctioned, but because governance boundaries were never explicit at design time. Hood argues compellingly that treating governance as a post-deployment compliance layer guarantees tension and reactive patching. The case for governance-as-architecture is well-supported by reference to EU AI Act risk-tiering and NIST frameworks, both of which mandate integrated governance from the beginning.

The formal contribution is a duality: agentic systems (perceive, reason, plan, act) paired with nomotic systems (govern, authorize, trust, evaluate). This framing dissolves a persistent confusion between intent (originating in user input) and authority (originating in governance rules). When a customer service agent with a $500 refund limit is asked to approve $2,000, the example clarifies that the failure is not in the agent's reasoning but in the authorization boundary.

Six core principles are presented: governance as architecture, pre-action authorization, explicit authority boundaries, verifiable trust, ethical justification, and accountable governance. The principles are broadly reasonable; governance structures should have owners, permissions should be explicit, trust should be earned rather than assumed; yet remain at a level of abstraction that invites critique. Pre-action authorization, for instance, is specified to allow implementation variation (synchronous or asynchronous, class-based or instance-level), which opens the question: at what level of operational specificity should Nomotic AI principles constrain implementation?

The paper does not provide implementation architectures, formal verification methods, or empirical validation of whether Nomotic AI frameworks reduce the failure modes claimed. The discussion of enforcement in distributed multi-agent systems acknowledges the gap but defers detailed mechanism design. The relationship to existing approaches (Constitutional AI as training-time alignment, runtime policy enforcement, delegated authority models) is acknowledged but not deeply analyzed. Hood claims synthesis of these approaches into a "holistic category," yet the novel architectural contribution beyond naming and reframing remains ambiguous.

A significant limitation is the assumption that governance can be static; that a set of rules established at design time will remain appropriate. The paper recognizes in passing that governance must be "evolvable," but does not grapple with how nomotic frameworks adapt when agentic capabilities or deployment contexts change. The board-level governance section gestures toward institutional design (who sets authority boundaries?) without resolving it.

For public sector and digital infrastructure contexts, the paper's framing is useful: governance must be designed into systems, not bolted on afterward. This aligns with DPI design principles (modular, interoperable, human-centered). However, the applicability to contexts where authority boundaries are contested, politically dynamic, or culturally variable is underexplored. In India's digital governance context, for instance, questions of whose authority counts and how boundaries adapt across federal-state coordination remain open.

The paper succeeds as conceptual framing: it elevates governance to co-equal standing with capability and provides vocabulary for that conversation. Whether "Nomotic AI" will gain traction in discourse remains an empirical question. The stronger contribution may be the principle-level guidance for enterprise governance rather than the neologism itself.

## Key Insight

Nomotic AI's core insight is architectural rather than technical: the governance gap in agentic AI systems persists not because governance is impossible but because governance is typically treated as a post-deployment compliance layer rather than as a design-time architectural decision that is co-equal with capability design.
