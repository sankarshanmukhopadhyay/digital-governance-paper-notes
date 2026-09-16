---
title: "Designing Loyalty: AI Agents and Conflicts of Interest"
source: "https://hai.stanford.edu/policy/designing-loyalty-ai-agents-and-conflicts-of-interest"
publication: "Stanford Institute for Human-Centered Artificial Intelligence (HAI)"
date_read: "2026-09-16"
primary_domain: "AI Governance"
tags: ["AI agents", "delegation", "accountability", "authority", "governance-by-design"]
key_insight: "A duty of loyalty becomes governable only when delegated authority, conflicts of interest, execution boundaries, revocation, and evidence of action can be made observable and enforceable at the point an agent acts."
published: "2026-08-25"
peer_review_status: "other"
paper_type: "report"
review_status: "current"
governance_facets: ["authority", "delegation", "accountability"]
---

# Paper Review

## Review

Smith, Wu, and King identify a structural problem that becomes unavoidable once AI systems move from recommending actions to executing them: the entity presented to a user as an agent may operate inside commercial incentives controlled by developers and deployers whose interests diverge from the user's. The brief proposes treating developers and deployers as fiduciaries in high-stakes consumer settings, with a duty of loyalty bounded by the delegated task. It translates that duty into disclosure of material commercial relationships, restrictions on self-preferencing, purpose limitation for data acquired through delegation, and affirmative consent before specified high-stakes actions.

The governance contribution goes beyond fiduciary language. The authors connect legal obligation to infrastructure: task-scoped and revocable agent credentials, verification of user identity, controlling entity and authorization scope, data minimization, incident reporting, and regulatory registration. This matters because interoperability protocols can otherwise become de facto governance by defining what systems permit while leaving authorization, consent and commercial-use constraints to implementers.

The unresolved issue is execution. A legal duty can establish who owes an obligation and create liability after breach, but it does not by itself determine whether a particular action is admissible before execution. "Best interests" also remains context-dependent, especially where price, convenience, privacy and user preference conflict. The proposal therefore depends on an institutional bridge from fiduciary obligation to machine-verifiable delegation, conflict disclosure, policy enforcement, evidence retention and revocation. The brief recognizes much of this infrastructure but does not specify a complete enforcement architecture or redress lifecycle.

Its durable implication is that agent governance cannot stop at identity or provenance. Knowing which agent acted and which company controls it supports attribution, not legitimacy. A governed agent relationship must also establish whose authority the agent exercises, the permitted task and duration, which conflicting incentives are disallowed, how authority can be withdrawn, and what evidence allows a user or regulator to challenge what happened.

## Key Insight

A duty of loyalty becomes governable only when delegated authority, conflicts of interest, execution boundaries, revocation, and evidence of action can be made observable and enforceable at the point an agent acts.
