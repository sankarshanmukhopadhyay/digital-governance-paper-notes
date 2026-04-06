---
title: "Syntelos: Trust Through Attestation and Policy"
source: "https://dhh1128.github.io/papers/syntelos.html"
publication: "Author webpage / paper draft"
date_read: "2026-04-06"
primary_domain: "Trust Infrastructure"
tags:
  - "AI agents"
  - "agentic systems"
  - "decentralisation"
  - "delegation"
  - "accountability"
  - "authority"
  - "authorization"
  - "governance-by-design"
  - "interoperability"
  - "legitimacy"
scholarly_signal: ""
key_insight: "Syntelos reframes trust as a runtime evaluation of attestations against policy, but leaves unresolved the governance of that policy layer, where real authority over system behavior resides."
---

# Paper Review

## Review

This paper proposes Syntelos as a trust architecture for distributed systems built around attestations, policy evaluation, and decentralized coordination. Its central move is to shift trust away from static identity and toward verifiable claims about capability, relationship, and authorization. That is the right direction. In distributed systems, and especially in agentic ones, the important question is rarely who an actor is in the abstract. It is what they are allowed to do, under what constraints, and on whose authority.

The paper is strongest when it treats trust as a runtime evaluation problem rather than a registration problem. Attestations are presented not as decorative metadata but as inputs into active decision-making. That makes the architecture more realistic than many identity-first trust models, which often assume that once an actor is named or authenticated the governance question has largely been solved. Syntelos instead recognizes that trust has to be computed in context, against policy, and in relation to changing conditions. That aligns with where distributed systems and delegated machine action are heading.

Its other strong feature is composability. By allowing multiple attestations to be assembled and evaluated against policy, the system offers a plausible route to more granular trust decisions across heterogeneous participants. This is valuable because modern systems increasingly require layered trust rather than binary admission. A participant may be recognized for one function, constrained for another, and disallowed from a third. Attestation-plus-policy is a better fit for that reality than monolithic identity assertions.

The paper’s main weakness is that it is clearer on proof than on governance. It explains how trust claims can be assembled and evaluated, but it is less precise about who controls the policy layer, how policy changes propagate, and how conflicts over authority are resolved. That is not a side issue. Once trust is defined as policy evaluation, the policy layer becomes the control plane. Whoever sets those rules determines the practical distribution of power in the system. The paper gestures toward decentralization, but decentralization of attestations does not automatically produce decentralization of rule-setting.

Revocation and lifecycle governance also appear underdeveloped. Trustworthy systems need more than valid attestations. They need mechanisms for withdrawal, expiry, dispute, and redress. If an actor’s authority changes, if an issuer is compromised, or if a delegation chain is found to be invalid, the architecture has to support operational rollback rather than merely retrospective diagnosis. Without that, trust becomes sticky in exactly the wrong way.

There is also an interoperability problem sitting just beneath the surface. The paper assumes that attestations can be composed across domains, but cross-domain composition depends on more than syntax. It requires governance over semantics, schema evolution, and evaluation criteria. Different institutions do not simply disagree on format. They disagree on what counts as valid authority, sufficient evidence, and legitimate action. A trust architecture that does not make those disagreements operational risks pushing them out of view rather than resolving them.

Overall, this is a useful architectural paper because it moves the discussion beyond static identity and toward delegated, contextual, policy-mediated trust. But its decisive unresolved issue is legitimacy at execution time. The interesting question is not whether attestations can be verified. It is who gets to shape the policies that interpret them, who may revoke or override them, and how affected participants can challenge those decisions when they are wrong.

## Key Insight

Syntelos reframes trust as a runtime evaluation of attestations against policy, but leaves unresolved the governance of that policy layer, where real authority over system behavior resides.
