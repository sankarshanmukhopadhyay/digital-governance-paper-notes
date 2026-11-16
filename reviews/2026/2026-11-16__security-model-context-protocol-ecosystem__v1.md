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

Muhammed and Anih synthesize MCP security research around a boundary that conventional component checks cannot settle: whether a model-selected sequence of individually available tools is authorized to produce its eventual external effects. Their security model spans host, client, model, server, authorization service, downstream API and software distribution. The treatment of tool metadata as an input to execution decisions, rather than inert documentation, explains why poisoning and tool shadowing can alter tool selection before invocation (Sections 2.2–2.3). The cross-tool exfiltration examples in Section 3.3 add a separate failure mode: permission to read information through one tool does not authorize its release through another.

The defensible architectural conclusion is to locate enforceable controls outside model reasoning. Sections 2.5 and 3.5 distinguish server provenance, credential audience and scope, per-action policy, execution isolation, data-flow restrictions, egress controls and lifecycle revalidation. These controls answer different questions. A signed software artifact identifies an origin and detects change; it does not establish that the publisher is entitled to perform an action. A valid token permits access under its defined conditions; it does not prove that the user's current task authorizes every operation reachable through the token. Figure 3 illustrates authorization-code, token-audience, token-passthrough and excessive-scope boundaries. Figure 4 shows why enforcing only individual tool permissions leaves composite data release unresolved. The analysis also correctly treats cached tool descriptions, version changes and deferred tasks as reasons to reassess authorization at execution time (Sections 2.2.6 and 3.5.14).

This is a narrative, evidence-informed technical review, not an original benchmark, systematic meta-analysis or implementation evaluation. Its tables aggregate heterogeneous experimental results, protocol analysis and software-supply-chain observations. The authors appropriately caution that reported tool-selection hijacking and payload execution rates depend on evaluated models, clients and attacks (Section 3.1.5). These numbers cannot establish deployment-wide incident probabilities. More consequentially, the bibliography contains material cross-reference errors: the MCP lifecycle discussion cites [28], whose reference entry is a Dependabot study; malicious remote-server findings are attributed to [29], listed as a survey of AI-augmented security operations; tool-selection results cite [30], listed as a prompt-injection defense comparison; and the comparative MCP/function-calling result cites [42], listed as an IoT cybersecurity survey. Section 2 and Table 4 also use citation identifiers inconsistently for benchmark evidence. These mismatches impair independent verification of several highlighted empirical propositions. They require correction and source-level reconciliation, not an assumption that the underlying experiments are false.

The strongest defense of the synthesis is that its architectural distinctions do not depend on any one benchmark figure: confused-deputy reasoning, token audience restrictions, information-flow controls and software isolation have independent security rationales. That response preserves the conceptual contribution. It does not substantiate the paper's comparative prevalence claims or establish that its proposed controls have been evaluated together. Table 5 labels defense evidence by maturity, but the article offers no unified experimental protocol, operational conformance profile or reproduced full-system control assessment. Its risk-adaptive scheme is a deployment recommendation whose false-denial, latency and usability trade-offs remain to be measured, not a demonstrated security outcome.

Compared with the archive's reviews of *Authorization Architectures for Tool-Using AI Agents* and *Authority Continuity Across Agentic Trajectories*, this article broadens the scope to server distribution, metadata and supply-chain lifecycle rather than supplying a new theory of delegation. Its added practical value is an inventory of enforcement locations and failure paths. A credible operational follow-up would reconcile each study against its bibliography; define the responsible policy authority and evidence source for each action decision; and test cross-tool releases, token-audience rejection, post-approval metadata change, revoked permissions and deferred execution in replayable traces. Such tests should report unauthorized effects alongside legitimate task completion, false refusals and enforcement latency. Until then the paper is a useful control-mapping synthesis, not verified comparative evidence or a validated MCP security profile.

## Key Insight

MCP security depends on independently enforcing action authority and information-flow constraints across tool composition; authenticating components and verifying their provenance do not establish that a particular operation is authorized.
