---
title: "Designing Agent IDs"
source: "https://agent-id.org/docs/agent-ids-policy-memo-sash-2026-03-31.pdf"
publication: "Singapore AI Safety Hub (SASH) policy memo"
date_read: "2026-09-04"
primary_domain: "Digital Identity"
tags: ["AI agents", "authorization", "delegation", "accountability", "interoperability", "trust registries"]
key_insight: "An agent ID can make identity, provenance, and permission legible to a service, but it becomes governance infrastructure only when the authority behind those claims can be scoped, refreshed, revoked, contested, and independently trusted."
published: "2026-03-31"
peer_review_status: "institutional-publication"
paper_type: "policy-report"
review_status: "current"
governance_facets: ["authority", "delegation", "accountability", "gatekeeping", "dependency"]
---

# Paper Review

## Review

The Singapore AI Safety Hub memo treats an agent ID as a bundle of identifiers and metadata that can support authentication, authorization, incident prevention, accountability, and compatibility. Its comparative analysis of OAuth 2.0, OIDC, MCP, AP2, national digital IDs, Microsoft Entra, and MCP-I reaches an important architectural conclusion: no single existing identity mechanism is sufficient. Agent identity is more plausibly a layered composition of identity assurance, delegated authority, interaction semantics, registries, and domain-specific controls. The memo then maps market incentives and uses ten functional, technical, and governance questions to derive a stylized government-oriented design.

That framing correctly moves the problem beyond naming an agent. The service receiving an agent request becomes the actual decision point, while the ID supplies claims about who or what is acting, who deployed it, what it may do, and where additional evidence can be resolved. The memo also recognizes that registries, logging, disclosure rules, and incident-response endpoints become part of the trust architecture, and that private incentives may underprovide information needed for high-risk uses.

The central unresolved issue is lifecycle authority. A signed agent identifier, provider statement, deployer statement, OAuth token, or registry record can establish provenance or a permission claim, but none by itself establishes that authority is current, action-specific, legitimate, and still valid at execution time. The stylized design does not specify how delegation expires, how compromised or repurposed agents are suspended, how provider or deployer bindings are changed, how stale registry assertions are invalidated, or how a service should resolve conflicting claims. Revocation, dispute, restoration, and redress therefore remain outside the machinery that is supposed to make high-risk agent activity governable.

The memo is explicitly an option-space exercise rather than a finished standard, which is a fair response to some of these omissions. Even so, its own high-risk use case makes lifecycle governance non-optional. The proposal to favour broader access to ID information and distributed anchoring such as DNS also shifts power toward services, registry operators, and infrastructure resolvers without yet defining admission, update, appeal, or assurance rules for those actors. Compared with the archive's recent reviews of accountable-yet-anonymous agents and verifier-centric credential ecosystems, this memo usefully operates one layer upstream by asking what an agent ID should contain. Its next step should be to specify an executable authority lifecycle and test interoperability under revocation, compromise, conflicting registries, privacy constraints, and cross-domain policy changes.

## Key Insight

An agent ID can make identity, provenance, and permission legible to a service, but it becomes governance infrastructure only when the authority behind those claims can be scoped, refreshed, revoked, contested, and independently trusted.
