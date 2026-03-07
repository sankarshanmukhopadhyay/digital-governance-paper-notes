---
title: "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"
source: "https://arxiv.org/abs/2602.11988"
publication: "arXiv"
date_read: "2026-03-07"
primary_domain: "AI Agents / Software Engineering"
tags: ["AI agents", "coding agents", "benchmarks", "developer tooling", "context engineering"]
key_insight: "Automatically generated repository context files often degrade coding-agent performance because they introduce additional constraints without improving task-relevant understanding."
---

# Paper Review

## Review

This paper evaluates whether repository-level context files such as AGENTS.md actually improve the effectiveness of coding agents. While such files are widely recommended by agent developers, the authors show through controlled evaluation that automatically generated context files often reduce task success rates while increasing cost.

The study introduces AGENTBENCH, a benchmark derived from real GitHub repositories that already include developer-written context files. Across multiple coding agents and models, the authors compare three settings: no context file, LLM-generated context files, and developer-provided files.

The results are surprising. LLM-generated context files generally reduce success rates and increase inference costs by more than 20%. Developer-written context files slightly improve performance but still increase operational cost due to additional exploration and testing steps triggered by the instructions in the files.

Trace analysis reveals that coding agents reliably follow the instructions present in context files, leading to more repository exploration, additional testing, and greater use of project-specific tooling. However, these instructions do not meaningfully help agents locate relevant code faster. In effect, the added guidance often introduces unnecessary constraints rather than improving task understanding.

The work highlights an emerging design tension in agentic systems: more context does not necessarily produce better outcomes. In many cases, models already possess sufficient prior knowledge about common development tooling and repository structure, making large context documents redundant.

Overall, the paper provides valuable empirical evidence against a rapidly spreading engineering practice. Its main contribution is demonstrating that concise, minimal guidance may be more effective than extensive automatically generated documentation when designing environments for coding agents.

## Key Insight

More repository context does not necessarily improve coding agent performance; excessive automatically generated guidance can increase cost and reduce task success.
