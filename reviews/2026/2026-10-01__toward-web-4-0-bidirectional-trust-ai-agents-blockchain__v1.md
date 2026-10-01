---
title: "Toward Web 4.0: bidirectional trust between AI agents and blockchain"
source: "https://doi.org/10.55092/blockchain20260008"
publication: "Blockchain"
date_read: "2026-10-01"
primary_domain: "AI Governance"
tags: ["AI agents", "AI governance", "delegation", "authorization", "mechanism design", "trust assurance"]
scholarly_signal: "cs.CR"
key_insight: "Verifiable agent infrastructure can make identity, delegation, execution, and evidence machine-checkable without settling who is entitled to govern, whose preferences should count, or how affected parties can contest automated authority."
published: "2026-09-22"
doi: "10.55092/blockchain20260008"
peer_review_status: "peer-reviewed"
paper_type: "survey"
review_status: "current"
governance_facets: ["authority", "delegation", "legitimacy", "accountability", "dependency"]
---

# Paper Review

## Review

Yunfeng Xia and co-authors offer a Systematization of Knowledge for autonomous AI agents operating on and within blockchain systems. Their organizing move is to treat the relationship as bidirectional: blockchain provides agents with identity, delegated permission, intent execution, and economic infrastructure, while agents may in turn participate in blockchain security, consensus, and governance. The paper formalizes this through the Agent-Blockchain Interaction Model (ABIM), evaluates 70 EIPs/ERCs, 127 academic papers, and 20 industry projects, and maps the ecosystem across verifiability, trust minimality, expressiveness, composability, and maturity. The resulting picture is less a story of mature decentralized agency than of interdependent infrastructure gaps.

The paper contributes useful structure by making several distinct governance problems legible as different classes of system requirement. Identity uniqueness and permission enforcement are treated as protocol invariants; verifiable computation, security detection, and validator correctness as assurance bounds; intent faithfulness, economic incentives, and governance influence as mechanism-design objectives. This distinction matters because it prevents every failure from being treated as a cryptographic problem. The ABIM dependency chain also exposes how upstream deficits propagate. The authors show, for example, that bounded AI influence in governance presupposes reliable agent identity and Sybil resistance, while validator verifiability and intent faithfulness ultimately depend on stronger verification of probabilistic model outputs.

The survey methodology is broad but disciplined. The corpus was assembled across academic databases, Ethereum standards, and industry sources, with inclusion criteria requiring work at the intersection of agents and blockchain and a substantive mechanism, analysis, measurement, or systematization contribution. Standards statuses were rechecked in July 2026, and the paper explicitly separates academic evidence from industry documentation. The main limitation is not corpus quality but the comparability of what is being compared. A formal property, a standards-process state, an industry deployment, and a governance mechanism are not equivalent evidentiary objects. The authors acknowledge this in part, but the five-dimensional framework can still make unlike forms of maturity and assurance appear commensurable.

From a governance perspective, the paper is most useful when it shows that technical verifiability does not close institutional questions. Its treatment of permission and delegation recognizes that an agent can be cryptographically constrained yet still operate under policies whose legitimacy is external to the protocol. Its governance section identifies concentration, low participation, delegation monopolies, legal accountability gaps, and the possibility that AI voting power could distort collective outcomes. Yet the formal model resolves this mainly through a proposed bounded-influence condition, where AI voting power should not exceed a threshold. That is a control objective, not a theory of legitimate participation. It leaves unresolved who classifies an actor as AI, who sets the threshold, whose interests the bound protects, how delegated human preferences should be interpreted, and how an affected community can challenge the rule itself.

A similar boundary appears in the paper's account of identity. The authors correctly identify Sybil-resistant agent identity as an upstream bottleneck, but uniqueness is not the same as accountability or authority. A system can reliably distinguish agents without establishing which human or institution is answerable for them, whether delegation remains valid over time, or whether downstream counterparties may reject the asserted authority. The same issue recurs in verifiable computation. zkML, opML, and TEEs can strengthen evidence that a computation occurred as claimed, but they do not establish that the computation was authorized, lawful, normatively acceptable, or contestable. The paper does not collapse these concepts, but its "trust infrastructure" framing risks encouraging readers to treat assurance of execution as a broader solution to governance than it actually is.

The paper's own evidence supports a sharper institutional conclusion: agent infrastructure is currently ahead in execution capability and behind in governance closure. No ABIM property is fully satisfied by a deployed system; delegation and intent standards are immature; AI participation in consensus and governance remains largely experimental; and the open problems at the governance layer depend on unresolved identity, verification, and mechanism-design questions. A stronger next step would be to extend ABIM with explicit authority provenance, revocation state, accountability assignment, contestation, and redress objects, then test whether those properties survive cross-agent delegation and cross-chain execution. That would convert the framework from a security-centered trust model into a more complete governance model for autonomous action.

## Key Insight

Verifiable agent infrastructure can make identity, delegation, execution, and evidence machine-checkable without settling who is entitled to govern, whose preferences should count, or how affected parties can contest automated authority.
