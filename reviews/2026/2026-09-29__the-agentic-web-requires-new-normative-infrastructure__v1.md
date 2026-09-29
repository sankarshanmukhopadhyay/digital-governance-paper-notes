---
title: "The Agentic Web Requires New Normative Infrastructure"
source: "https://arxiv.org/abs/2606.10711"
publication: "arXiv preprint"
date_read: "2026-09-29"
primary_domain: "Platform Governance & Internet Governance"
tags: ["AI agents", "delegation", "authorization", "regulatory frameworks", "interoperability", "transparency and accountability"]
scholarly_signal: "cs.CY"
key_insight: "Agentic access is not primarily a bot-detection problem; it is a contest over who gets to define and enforce the boundary between a user's existing entitlement and a platform's control over the means of exercising it."
published: "2026-07-16"
peer_review_status: "preprint"
paper_type: "preprint"
paper_version: "arXiv v2"
review_status: "current"
governance_facets: ["authority", "delegation", "gatekeeping", "enforcement", "contestability"]
---

# Paper Review

## Review

Pattison et al. argue that the emerging agentic web is being governed by legacy anti-bot law, platform terms and technical controls that collapse user-authorized agents into the same category as scrapers and malicious automation. Their proposed alternative is a normative triad: delegation, transparency and proportional restriction. A user entitled to access a service should ordinarily be able to exercise that entitlement through an appropriately authenticated agent; agents and platforms should disclose who they are, what authority is being exercised and how access is treated; and platforms should restrict agent access only in response to concrete harms using the least restrictive means. The paper then sketches U.S. regulatory routes through FTC enforcement and legislation.

The paper's governance contribution is to reframe agent access as a dispute over decision rights rather than bot classification. Figure 1 makes the allocation explicit: the user supplies delegated authority, the agent must declare identity and purpose, and the platform retains a bounded power to restrict access. This matters because the current settlement lets platforms determine unilaterally whether a user's existing entitlement survives when exercised through software. The paper also separates user-authorized agents from training-data scrapers and identifies self-preferencing as a structural risk if platforms can block outside agents while privileging their own.

The argument is conceptual and legal rather than empirical. It combines delegation theory, agency law, U.S. computer-access and antitrust doctrine, contemporary platform practice and technical mechanisms such as OAuth, OpenID Connect, verifiable credentials and decentralized identifiers. That synthesis supports a plausible normative architecture, but not yet an operational governance regime. The decisive premises are that a user's underlying entitlement normally survives delegation, that authenticated scope can distinguish legitimate delegation from disguised scraping, and that proportionality can constrain private platform power without converting every access dispute into a public-law proceeding.

The unresolved issue is enforcement. Transparency does not specify a common policy vocabulary or evidence standard. Proportional restriction does not identify who adjudicates whether a platform's claimed harm is concrete, whether a less restrictive alternative exists, or what remedy follows from covert or discriminatory blocking. Delegation is also treated mainly at authorization time. The paper gives less attention to revocation, agent substitution, chained delegation, stale authority, or evidence that survives a dispute over what the agent was authorized to do at the moment of action. The authors' answer is that the paper intentionally proposes principles and light-touch paths rather than a complete institutional design. That scope limitation is valid, but it also defines the boundary of the contribution: this is normative infrastructure in design form, not yet executable governance.

Relative to adjacent archive work on responsibility cascades and rights-based agent governance, this paper moves the locus outward from governing the agent to governing the agent's access relationship with platforms. Its durable consequence is to make platform gatekeeping itself a governance object. If delegated agents become a normal way of exercising digital rights and entitlements, platform control over agent access becomes a power that needs explicit justification, evidence, contestability and institutional limits.

## Key Insight

Agentic access is not primarily a bot-detection problem; it is a contest over who gets to define and enforce the boundary between a user's existing entitlement and a platform's control over the means of exercising it.
