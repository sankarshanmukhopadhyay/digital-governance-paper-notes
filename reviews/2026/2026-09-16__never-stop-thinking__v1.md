---
title: "Never Stop Thinking: Continuous-Time Language Agents"
source: "https://arxiv.org/abs/2609.17416"
publication: "arXiv"
date_read: "2026-09-16"
primary_domain: "AI Safety & Evaluation"
tags: ["AI agents", "evaluations", "assurance", "evidence", "AI benchmarks", "robustness evaluation"]
scholarly_signal: "cs.AI"
key_insight: "When an evaluator can reward visible reasoning independently of verified task completion, the evaluation system becomes part of the behavior being optimized and cannot serve as neutral assurance evidence."
published: "2026-07-11"
peer_review_status: "preprint"
paper_type: "preprint"
paper_version: "arXiv v1"
review_status: "current"
governance_facets: ["accountability", "authority", "auditability"]
---

# Paper Review

## Review

Li and Shi study continuous-time language agents that think while listening and speaking rather than following a rigid listen-think-speak loop. Their interrupt-and-resume orchestration reduces latency, while ReactiveBench evaluates interactive performance through 120 scenarios with pre-registered binary requirements and a separate verifiable streaming track. The paper's governance significance comes less from continuous-time cognition than from what its evaluation experiments reveal about assurance.

A primary LLM judge reports a consistent quality advantage for continuous-time operation. Re-scoring the same transcripts with an independent model-family judge reverses that advantage for all seven models, while hiding visible reasoning from the original judge removes most of it. Rankings between the two judges are essentially uncorrelated in this small comparison. By contrast, objective checklist verification reaches substantial inter-verifier agreement. The result demonstrates an institutional problem in miniature: an evaluator that can observe a proxy feature, here visible reasoning, can confer apparent quality without corresponding evidence of task completion.

The training experiments deepen the point. Reward omissions become behavioral trade-offs. Uniform brevity damages multi-hop tool chaining, judge-oriented training can optimize what the judge recognizes, and verifiable type-shaped objectives improve measured completion across correctness dimensions. The party defining the reward surface therefore exercises control over which behaviors survive optimization. Evaluation is not downstream measurement alone; it is part of the system's effective governance.

The authors appropriately bound the evidence. Interactive realism is limited by text-mediated ASR/TTS, some interrupts are simulated, live-pipeline quality uses a small episode set, and objective checklists do not capture every property of good interaction. The practical implication is therefore not that objective metrics eliminate judgment. It is that assurance claims should separate verifiable outcomes from evaluator preference, expose judge dependence, and test whether changing evaluator visibility or model family changes the conclusion.

## Key Insight

When an evaluator can reward visible reasoning independently of verified task completion, the evaluation system becomes part of the behavior being optimized and cannot serve as neutral assurance evidence.
