---
title: "Authority Propagation Models: PoP vs PoC and the Confused Deputy Problem"
source: "https://zenodo.org/records/17833000"
publication: "Zenodo"
date_read: "2026-09-07"
primary_domain: "Trust Infrastructure"
tags: ["authority", "authorization", "provenance", "delegated authority", "delegation"]
key_insight: "Provenance-bounded execution can prevent downstream privilege expansion, but continuity of authority does not establish the legitimacy of the authority at the origin."
published: "2025-12-01"
review_status: "current"
---

# Paper Review

## Review

Gallo formalizes a distinction between possession-based authorization and provenance-bounded execution. The PIC model represents execution as a causal chain in which each hop may exercise only a subset of the authority available at the origin. From that monotonicity constraint, the paper proves an origin-bounded safety property and argues that the classical confused deputy condition becomes non-formulable because no downstream principal can acquire a privilege absent from the origin.

The governance contribution is the relocation of authority from an artifact held by an actor to a property of execution lineage. Delegation becomes materially different from token transfer. A credential or bearer object may prove possession, but possession alone cannot explain why downstream action remains within the originator's authority. PIC instead demands a verifiable causal chain and irreversible loss of authority once a privilege is removed.

The formal result is narrower than the paper's broad claim about artifact-based delegation. The proof establishes safety under monotonicity and origin-bounded assumptions. It does not show that every JWT, capability, or cryptographic delegation system implements possession semantics without contextual attenuation, audience restriction, policy evaluation, or invocation-specific binding. The strongest defense is that the paper contrasts semantic models rather than surveying implementations. That resolves the need for exhaustive coverage, but not the universal phrasing.

PIC also does not establish legitimacy. It can prove that an action descends from an origin without showing that the origin was entitled to authorize it, how authority is revoked during execution, or how disputed provenance supports redress. Its practical value is making one class of authority expansion structurally impossible, not completing governance of delegated action.

## Key Insight

Provenance-bounded execution can prevent downstream privilege expansion, but continuity of authority does not establish the legitimacy of the authority at the origin.
