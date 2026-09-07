---
title: "Authority is a Continuous System"
source: "https://zenodo.org/records/17860199"
publication: "Zenodo"
date_read: "2026-09-07"
primary_domain: "Trust Infrastructure"
tags: ["authority", "authorization", "governance-by-design", "delegated authority", "provenance"]
key_insight: "A continuity model can prevent downstream authority manufacture, but a governable system still needs explicit rules for how legitimate authority is created, revoked, disputed, and restarted."
published: "2025-12-08"
review_status: "current"
---

# Paper Review

## Review

This paper generalizes Provenance Identity Continuity into a theory of authority as a continuous property of execution rather than a transferable object. Authority states retain an immutable origin, monotonically shrinking operational scope, executor continuity, temporal validity, and contextual validity. A successor state exists only when all guardrails hold. The model extends this logic to sequential execution, forks, joins, governance policy decisions, and a definition of zero-trust compatibility.

The governance move is consequential. Continuity defines what is structurally possible, while a policy decision point may only restrict or terminate transitions. Governance therefore cannot create authority inside an execution chain. This separates authorization lineage from policy discretion and prevents a downstream policy engine from laundering newly introduced privilege into an apparently valid continuation. Forks and joins preserve the same non-expansion invariant.

The central limitation is legitimate authority creation. Institutions routinely create, renew, delegate, substitute, and revoke authority through governed acts. By defining governance as authority-reducing within a chain, the paper secures a strong safety property but pushes authority creation outside the model. The strongest response is that a new grant should establish a new execution origin. That preserves the invariant, but leaves a governance boundary unspecified: who may instantiate a new origin, under what evidence, with what revocation and dispute semantics, and how related origins are reconciled.

The zero-trust conclusion is also definition-dependent. The paper proves incompatibility where possession can rematerialize authority independently of current state. It does not establish that every practical system using proof of possession is non-zero-trust when possession is only one input to continuous authorization.

The durable contribution is an architectural invariant: downstream execution should be able to lose authority but not manufacture it.

## Key Insight

A continuity model can prevent downstream authority manufacture, but a governable system still needs explicit rules for how legitimate authority is created, revoked, disputed, and restarted.
