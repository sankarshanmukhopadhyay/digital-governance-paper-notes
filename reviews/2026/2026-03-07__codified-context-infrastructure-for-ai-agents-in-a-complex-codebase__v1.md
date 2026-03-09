---
title: "Codified Context: Infrastructure for AI Agents in a Complex Codebase"
source: "https://arxiv.org/abs/2602.20478"
publication: "arXiv"
date_read: "2026-03-07"
primary_domain: "AI Governance"
tags:
  - AI agents
  - agentic systems
  - context engineering
  - coding agents
  - governance-by-design
  - developer tooling
  - coordination
  - workflows
scholarly_signal: "cs.SE"
key_insight: "Persistent, machine-readable project context functions as a governance layer for AI coding agents, but the paper shows this through a single-project experience report rather than a comparative evaluation."
---

# Paper Review

## Review

This paper argues that AI coding agents fail less when project knowledge is treated as infrastructure rather than as ad hoc prompt text. In a 108,256-line distributed C# system developed across 283 sessions, the author builds a three-tier “codified context” stack: a hot-memory constitution loaded into every session, 19 specialist agents invoked for domain-specific tasks, and a cold-memory knowledge base of 34 subsystem documents retrieved on demand. The central contribution is practical and timely. It shows that agent performance in large codebases depends not only on model capability but on how conventions, constraints, failure modes, and routing logic are codified for repeated reuse.

The paper is strongest when it reframes documentation as an operational control layer. That framing matters beyond software engineering. Public sector AI systems, DPI components, and safety-critical administrative tools all face the same problem: models are stateless, institutions are not. In that sense, the paper offers a useful governance-by-design lesson. Stable behavior comes from structured context, explicit rules, and disciplined update practices, not from hoping the model “remembers.”

That said, the evidence base is narrow. This is a single-author, single-project experience report with observational case studies, not a controlled evaluation. The quantitative material is descriptive rather than causal. Reported counts for prompts, agent turns, retrieval calls, and infrastructure growth help establish scale, but they do not isolate whether the architecture improved quality, speed, cost, or safety compared with simpler baselines. The strongest claims therefore remain plausible but under-tested.

There is also a translation gap between coding-agent performance and public-interest governance. The paper hints at transferability to broader agentic systems, yet it does not develop concrete implications for accountability, auditability, public procurement, or regulatory assurance. That is a missed opportunity. A sharper discussion could connect the three-tier architecture to policy controls such as change management, evidence trails, human override, and risk-tiered deployment.

Overall, this is a worthwhile and original practice paper. It is not a definitive evaluation, but it is a credible early blueprint for how persistent context can become an institutional memory layer for AI agents. For AI governance and DPI practitioners, the big idea is simple: memory is not magic; it is architecture.


## Key Insight

Persistent, machine-readable project context can act as a governance layer for AI coding agents, but the paper demonstrates this through a single-project experience report rather than a comparative evaluation.
