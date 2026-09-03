---
title: "Position: Stop Anthropomorphizing Intermediate Tokens as Reasoning/Thinking Traces!"
source: "https://arxiv.org/abs/2504.09762"
publication: "Proceedings of the 43rd International Conference on Machine Learning (ICML 2026), PMLR 306"
date_read: "2026-09-03"
primary_domain: "AI Safety & Evaluation"
tags:
  - anthropomorphism
  - LLMs
  - AI safety
  - transparency and accountability
  - assurance
scholarly_signal: "cs.AI"
key_insight: "Intermediate-token visibility is not assurance: when traces are not causally tied to outcomes, governance must attach trust to verifiable decisions and external commitments rather than plausible-looking model monologues."
---

# Paper Review

## Review

This position paper argues that the unfiltered intermediate tokens emitted before a model's answer should not be treated as human-interpretable reasoning or thinking traces. Its case is cumulative rather than based on one experiment. The authors distinguish answer correctness from trace validity, then assemble evidence showing that models can retain or improve task performance when trained on semantically incorrect, swapped, truncated, or otherwise irrelevant derivational traces. Their maze experiments make the claim especially concrete: formally checkable A* traces can become invalid while final-answer accuracy remains high, and reinforcement learning can improve solutions without repairing trace semantics. The paper also challenges the use of token length as a proxy for problem difficulty and cites human-subject evidence that showing traces or trace summaries can increase trust even when answers are wrong.

The governance implication is larger than a terminology dispute. If intermediate tokens are not causally reliable evidence of how a model reached an outcome, exposing them does not create meaningful transparency and can instead manufacture confidence. This shifts assurance away from narrative visibility and toward verifiable outputs, external checks, and, in agentic systems, the semantically consequential commitments made through tool calls and other actions. Section 6.2 is therefore especially important: it separates internal intermediate tokens from externalized actions whose effects require governance, auditability, and control.

The paper is an advocacy position, so its central limitation is that it establishes a strong presumption against trace-based trust rather than a universal impossibility theorem. A defender of chain-of-thought monitoring could argue that imperfect traces may still carry useful statistical signals for detecting some classes of misbehavior. The critique survives in governance terms because a monitorable correlation is not equivalent to an accountable causal record. The paper would be more operationally useful if it specified assurance criteria for when trace-derived signals may be used as supplementary evidence without being mistaken for provenance, explanation, or authority.

## Key Insight

Intermediate-token visibility is not assurance: when traces are not causally tied to outcomes, governance must attach trust to verifiable decisions and external commitments rather than plausible-looking model monologues.
