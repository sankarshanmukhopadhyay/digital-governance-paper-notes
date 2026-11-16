---
title: "Security of The Model Context Protocol Ecosystem: Emerging Threats, Empirical Attack Evidence, Trust and Authorization Failures, Supply-Chain Risks, And Defensive Strategies"
source: "https://doi.org/10.64388/IREV10I3-1723420"
publication: "Iconic Research and Engineering Journals, vol. 10, no. 3, pp. 3266-3314 (2026); Khalid D. Muhammed and David Chinonso Anih"
date_read: "2026-11-16"
primary_domain: "Trust Infrastructure"
tags: ["authorization", "delegation", "provenance", "adversarial evaluation", "evidence", "dependencies"]
key_insight: "MCP security depends on independently enforcing action authority and information-flow constraints across tool composition; authenticating components and verifying their provenance do not establish that a particular operation is authorized."
published: "2026-09-29"
doi: "10.64388/IREV10I3-1723420"
paper_type: "research-article"
review_status: "current"
---

# Paper Review

## Review

Muhammed and Anih analyze MCP security through a boundary conventional component checks cannot resolve: whether a model-selected sequence of tools is authorized to produce its eventual external effects. Their threat mapping covers the host, client, model, server, authorization service, downstream API and software supply chain. Treating tool metadata as an input to execution decisions explains why poisoning and shadowing can alter selection before invocation (Sections 2.2–2.3). Section 3.3 identifies a distinct compositional failure: permission to read through one tool does not authorize release through another.

The operational proposition is to enforce constraints outside model reasoning. Sections 2.5 and 3.5 separate provenance, credential audience and scope, action-level authorization, isolation, data-flow restrictions, egress control and revalidation after change. Each establishes a different property. A software signature can establish origin and integrity, not legitimate authority. A valid token does not establish that the current task authorizes all operations within its technical reach. Figure 3 maps authorization-code theft, audience confusion, token passthrough and excessive scope; Figure 4 shows sensitive information crossing tool boundaries despite individually plausible actions. Cached metadata, mutable tool versions and asynchronous tasks make execution-time reassessment material (Sections 2.2.6 and 3.5.14).

This is a narrative technical synthesis, not a newly executed benchmark, systematic meta-analysis or validated deployment. The tables combine protocol reasoning, controlled attacks and software-supply-chain observations. The authors appropriately caution that reported selection-hijacking and payload-execution rates depend on tested configurations (Section 3.1.5), so they are not deployment-wide prevalence estimates. More seriously, multiple citations do not identify the studies credited in the text. MCP lifecycle claims cite [28], whose bibliography entry concerns Dependabot; remote-server findings cite [29], listed as an AI security-operations survey; tool-selection results cite [30], listed as a prompt-injection defense study; and the MCP-versus-function-calling comparison cites [42], listed as an IoT cybersecurity survey. Benchmark identifiers are also inconsistent between the tables and reference list. Those defects obstruct independent verification of specific empirical claims; they do not demonstrate that the underlying results are false.

The authors' best response is that their core control separation does not depend on any single experiment. Confused-deputy reasoning, audience restrictions, isolation and information-flow enforcement have independent security rationales. This preserves the conceptual synthesis but does not validate its quantitative comparisons or show that the recommended defenses work together. Table 5 grades defense evidence, yet the publication provides no composite conformance profile or executed end-to-end evaluation. Risk-adaptive review remains a proposal whose effects on false denials, latency, approval burden and legitimate task completion require measurement.

Relative to this archive's reviews of *Authorization Architectures for Tool-Using AI Agents* and *Authority Continuity Across Agentic Trajectories*, the distinct contribution is lifecycle coverage of metadata, server distribution and supply-chain change, rather than a new delegation model. Before using the paper as an assurance reference, the cited studies should be reconciled with their actual bibliographic records. An operational test should specify who owns the policy, which evidence determines authority, and what happens on revoked access, changed metadata, invalid token audience, unauthorized cross-tool release and deferred execution. Replayable traces should measure prohibited effects alongside task success, false refusal and enforcement latency. The paper is useful for identifying control locations, but cannot yet establish comparative defensive efficacy or an implementable MCP security profile.

## Key Insight

MCP security depends on independently enforcing action authority and information-flow constraints across tool composition; authenticating components and verifying their provenance do not establish that a particular operation is authorized.
