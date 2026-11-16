---
title: "Security of The Model Context Protocol Ecosystem: Emerging Threats, Empirical Attack Evidence, Trust and Authorization Failures, Supply-Chain Risks, And Defensive Strategies"
source: "https://doi.org/10.64388/IREV10I3-1723420"
publication: "Iconic Research and Engineering Journals, vol. 10, no. 3, pp. 3266-3314 (2026); Khalid D. Muhammed and David Chinonso Anih"
date_read: "2026-11-16"
primary_domain: "Trust Infrastructure"
tags: ["authorization", "delegation", "provenance", "adversarial evaluation", "evidence", "dependencies"]
key_insight: "The MCP paper can inform threat-model coverage, but its misaligned citations prevent the reported attack results from serving as independently traceable assurance evidence; deployments still need operation-level authorization and cross-tool information-flow tests."
published: "2026-09-29"
doi: "10.64388/IREV10I3-1723420"
paper_type: "research-article"
review_status: "current"
governance_facets: [authority, delegation, enforcement, dependency]
---

# Paper Review

## Review

Muhammed and Anih offer a broad account of security boundaries in the Model Context Protocol (MCP) ecosystem. Its useful contribution is the identification of two connected but distinct attack surfaces. Tool descriptions influence a model's decision to invoke capabilities before execution, while individually permitted tools can be composed into an unauthorized information flow. A server may be authentic and its token valid without either fact establishing that a proposed composite operation is authorized. Sections 2.2–2.5 and 3.3–3.5 therefore supply a workable threat-model inventory spanning metadata, token audience and scope, egress, tool composition and changing dependencies.

That inventory is worth retaining, but the paper's claimed empirical synthesis does not meet the evidentiary standard needed for an assurance reference. It aggregates reported attack success, selection-hijacking observations and defensive techniques across heterogeneous studies without a reproducible review protocol. The limitations are not only heterogeneity and the absence of a new benchmark. Material cross-reference inconsistencies prevent several empirical propositions from being traced to the works cited. The text attributes MCP lifecycle claims to [28], whose reference entry addresses Dependabot; malicious-server observations to [29], listed as a broader AI security-operations survey; tool-selection findings to [30], listed as prompt-injection defense research; and an MCP-versus-function-calling comparison to [42], listed as an IoT cybersecurity survey. These are reference-level mismatches, not merely differences of terminology.

The correct conclusion is narrower than either endorsement or dismissal. The discrepancies do not establish that those attacks were not observed; they prevent the article, as published, from independently substantiating the attributed results. Nor does successful source reconciliation by itself demonstrate deployment prevalence: model, host, client and tool configurations determine what any reported attack rate measures. A security team should not import the review's quantitative comparisons into a risk register or procurement assurance claim before resolving the underlying references and measurement conditions.

The conceptual controls have a different evidentiary status. Restricting credential audience, checking permission at the consequential action boundary, separating data-read and data-release permissions, binding approval to task context, and applying egress restrictions respond to independently intelligible failure mechanisms. But the paper does not demonstrate that those controls form a jointly sufficient security profile. A tool signature establishes provenance and integrity; it cannot settle which principal has authority to initiate an operation, which external recipient may receive data, or whether an earlier delegation remains current. Nor can individual per-tool authorizations establish the permissibility of a cross-tool workflow.

The institutionally consequential question is where the host enforces that distinction. A model that chooses a tool is not the actor entitled to create permissions. A server claiming that a tool is safe is not an independent authority for its invocation. Tool descriptors and server manifests are inputs whose meaning must be constrained by current policy, rather than evidence that policy has already been satisfied. This is especially relevant to deferred execution and metadata changes: approval must refer to the actual proposed operation and its current scope, not a stale tool name.

Relative to the archive's reviews of *Authorization Architectures for Tool-Using AI Agents* and *Authority Continuity Across Agentic Trajectories*, the article adds coverage of MCP-specific discovery, metadata and supply-chain surfaces. It does not supply an alternative theory of delegation or an evaluated conformance class. The settled editorial disposition is to use the article to enumerate attack paths and control locations, not as evidence that an MCP defense performs at a stated rate. A meaningful change in that conclusion would require corrected source mapping and replayable tests of unauthorized cross-tool release, invalid token audience, changed descriptors and revoked or deferred operations.

## Key Insight

The MCP paper can inform threat-model coverage, but its misaligned citations prevent the reported attack results from serving as independently traceable assurance evidence; deployments still need operation-level authorization and cross-tool information-flow tests.
