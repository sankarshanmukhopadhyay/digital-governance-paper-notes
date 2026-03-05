---
title: "Exhaustibility Is Not an Optimization. It Is a First-Class Invariant"
source: "https://medium.com/@paul_15561/exhaustibility-is-not-an-optimization-it-is-a-first-class-invariant-c3a19008077e"
publication: "Medium (Paul Knowles)"
date_read: "2026-03-05"
primary_domain: "Trust Infrastructure"
tags: ["Agentic AI", "Authorization", "Delegation", "Provenance", "Digital Identity", "Governance-by-Design"]
---
# Paper Review

## Review

Agentic AI approaches are exposing a design assumption embedded in most digital identity systems: authority is persistent. Once a credential, role, or API token is issued, systems assume that permission remains valid until it expires or is revoked.

Paul Knowles’ essay, *Exhaustibility Is Not an Optimization. It Is a First-Class Invariant*, challenges that assumption directly.

Traditional authorization asks: **does this identity have permission?** But when software agents act continuously and autonomously, that becomes insufficient. The governance question becomes: **should this specific action produce an effect right now?**

In other words, the unit of governance shifts from *identity* to *effect*.

That shift aligns with an emerging pattern across trust infrastructure and agent identity work: identity alone cannot stabilize digital systems. What matters is the chain that links **who acted**, **under what mandate**, and **which outcome** was produced.

Nicola Gallo’s *Provenance Identity Continuity (PIC)* framework pushes in a similar direction, treating identity not as a static credential but as a continuous provenance trail that binds actors, actions, and artifacts across time.

Exhaustible authority fits neatly into this direction of travel. Instead of persistent permission, authority becomes **consumable and action-bound**. Each action must instantiate its mandate, satisfy constraints, and leave a verifiable trace when the effect occurs.

Seen this way, agent governance is less about stronger authentication and more about governing the moment an action changes the world: **executable governance**.

Persistent permissions were designed for human workflows. Autonomous systems require something else: authority that expires at the moment it is exercised, and provenance that survives afterward.

Identity establishes *who*. Exhaustibility governs *what may happen now*. Provenance ensures we can understand *what actually happened*. That triad is emerging as a practical control surface for agentic systems.

## Key Insight

For agentic systems, governance must shift from persistent identity-based permission to action-bound, exhaustible authority that produces verifiable provenance at the moment an effect occurs.
