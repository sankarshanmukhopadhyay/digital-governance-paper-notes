---
title: "Agents of Chaos"
source: "https://arxiv.org/abs/2602.20021"
publication: "arXiv"
date_read: "2026-03-09"
primary_domain: "AI Safety & Evaluation"
tags: ["AI agents", "agentic systems", "AI safety", "AI risk management", "accountability", "authorization", "cyber risk", "deployment controls", "evaluations", "LLMs"]
scholarly_signal: "cs.AI"
key_insight: "The paper shows that once language models are wrapped in memory, tools, messaging, and delegated authority, the main governance problem is no longer just model error but insecure delegation across socio-technical systems."
---

# Paper Review

## Review

This paper is one of the more useful early warning studies on agentic AI because it tests agents in a messy, live environment rather than a sterile benchmark. The authors deploy OpenClaw-based agents with persistent memory, email, Discord, filesystem access and shell execution, then let twenty researchers probe them over two weeks. The result is a catalogue of concrete failures: non-owner compliance, sensitive-data disclosure, destructive local actions, denial of service, looping, identity spoofing, prompt injection through editable artifacts, and cross-agent propagation of unsafe behavior.

Its main contribution is not statistical proof of prevalence but empirical proof of existence. That matters. For governance, one counterexample is enough to show that current deployment patterns can produce security, privacy and accountability failures when authority is weakly specified. The strongest insight is that the dangerous layer is not the base model alone, but the integration of model, memory, tools, channels, and social context.

The methodology is appropriate for exploratory red teaming, but it is not yet robust enough to support comparative claims. The sample is small, the environment is custom, the cases are qualitative, and the authors openly acknowledge setup instability and human intervention. That limits reproducibility and makes it hard to separate model weakness from scaffold weakness or operator misconfiguration. The paper would be stronger with a clearer incident taxonomy, severity ranking, frequency accounting, and control conditions across models, permissions, and tool sets.

Even so, the paper has high practical value. It reframes agent safety as a public-interest governance problem: identity, authorization, stakeholder modeling, auditability, bounded autonomy, and liability. For DPI and public-sector systems, the lesson is stark. You cannot safely place agents into administrative or citizen-facing workflows if they cannot reliably distinguish owners from non-owners, instructions from data, or successful action from false completion. The paper is best read as a governance and assurance agenda for agent deployment, not merely as a collection of entertaining failure stories.

## Key Insight

The paper shows that once language models are wrapped in memory, tools, messaging, and delegated authority, the main governance problem is no longer just model error but insecure delegation across socio-technical systems.
