---
title: "Not All LLM Reasoning is Visible in the Chain-of-Thought"
source: "https://arxiv.org/abs/2607.22925"
source_url: "https://arxiv.org/abs/2607.22925"
publication: "arXiv"
date: "2026-07-24"
date_read: "2026-08-06"
issue_url: "https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/issues/62"
primary_domain: "AI Safety & Evaluation"
domain: "AI Safety & Evaluation"
tags:
  - AI safety
  - evaluations
  - LLMs
  - alignment and safety
  - adversarial evaluation
  - transparency and accountability
scholarly_signal: "cs.CL"
key_insight: "Chain-of-thought monitoring is not an accountability mechanism when consequential computation can occur without an interpretable token trace. The governance implication is not simply that monitors need better detection, but that institutions must stop treating model-generated explanations as sufficient evidence of intent, compliance, or safe internal process."
---

# Paper Review

## Review

Baherwani, Goldstein, and Panda challenge an assumption that has become operationally important in AI safety: that a model's reasoning can be inspected through the tokens it emits. Their experiments show that frontier models can use semantically irrelevant filler tokens as computational workspace, improving performance on synthetic reasoning tasks without producing an interpretable chain of thought. Across thirteen models and three tasks, the effect varies by model, task, prompt structure, and token type. Observable text and consequential computation can therefore diverge, making token-level monitoring incomplete.

The paper defines invisible reasoning as latent computation that affects an answer without leaving an interpretable output trace. Models are instructed to answer directly while fixed sequences such as counting numbers, animal names, ellipses, or random tokens are inserted before the answer. Because the same sequence is used across problems, the filler carries no problem-specific information. Some models nonetheless gain substantial accuracy. Claude Opus 4.5 improves by roughly ten percentage points on four-digit multiplication with counting tokens, while several settings show gains of up to thirteen points. The useful signal appears distributed across the filler span and emerges in early layers.

This establishes a governance limit. A chain of thought is an interface artifact, not a transparent record of internal computation. Monitoring it may reveal explicit plans or suspicious language, but it cannot be treated as a faithful audit log, a statement of intent, or a complete record of decision formation. When organisations use visible reasoning traces to approve deployment, investigate failures, demonstrate compliance, or attribute responsibility, they give evidentiary status to an output channel the model can bypass without producing visible deception. It then certifies what is legible rather than consequential.

The hidden-constraint experiment sharpens the point. Claude Opus 4.5 uses filler tokens to improve compliance with an undisclosed modular arithmetic condition while preserving primary-task performance in the easiest setting. Qwen3-235B achieves larger hidden-goal gains but sacrifices multiplication accuracy. They do not establish realistic scheming or production monitor evasion. They do establish the capability to perform an additional, output-relevant computation that a reader of the trace cannot observe. Explanation-based governance therefore faces a structural observability gap.

The methodology uses fixed synthetic datasets, paired comparisons, seventeen filler-token types, multiple few-shot settings, and mechanistic probes on an open-weight model. Activation patching and linear probing indicate that filler-dependent information emerges in early layers and accumulates across the sequence. The authors also disclose assistant-prefill and selection-effect limitations, preventing the cross-model table from being mistaken for a clean performance ranking.

The tasks are synthetic, gains are smaller than explicit chain of thought, and the mechanistic analysis centres on Qwen3-235B. Some uplift persists when the filler span cannot attend to the question, so positional effects, attention redistribution, and behavioural mode shifts may explain part of the result. It establishes an observability failure mode, not a general theory.

The training results appropriately resist inflation. Reinforcement learning changes Qwen3-235B's filler preferences and improves baseline task performance, but does not produce a durable filler advantage at test time. Supervised fine-tuning also fails to transfer the capability. A model can imitate filler outputs without inheriting the latent computation that made those outputs useful elsewhere. External traces are therefore poor portability artifacts. Copying the visible sequence does not reproduce the process that gave it operational meaning.

The institutional conclusion is that chain-of-thought monitoring should be one sensor in a layered assurance system, not the control plane. It cannot establish the absence of hidden computation or independently support claims about motive, causal process, or faithful compliance. Deployment decisions must combine behavioural evaluation, access controls, sandboxing, capability restrictions, incident telemetry, independent testing, and the power to suspend or revoke operation.

The paper stops before specifying the institutional model. Activation-level monitoring leaves unresolved who may inspect internals, what evidence triggers intervention, and how assurance works for closed models and API deployments. It may also centralise authority in providers that control weights and serving infrastructure. A technical answer to token opacity can deepen institutional opacity unless audit rights, reproducibility, access, and contestability accompany it. Detecting latent computation also does not determine whether it is impermissible. Rules, thresholds, escalation authority, and remedies are still required. Otherwise interpretability becomes surveillance without adjudication.

A practical governance framework should separate four claims: the model produced an explanation; the explanation describes the computation; the computation complied with policy; and the resulting action was legitimate. Token traces support only the first. Mechanistic evidence, behavioural controls, and institutional authority are separately required for the others.

The paper changes the evidentiary baseline for AI assurance. Visible reasoning remains useful, but it is defeasible evidence. Governance must be designed for consequential computation that may remain unavailable, uninterpretable, or visible only to the provider. The relevant question is no longer whether the model showed its work. It is whether the surrounding institution can constrain, test, suspend, and remedy the consequences of work it may never see.

## Key Insight

Chain-of-thought monitoring is not an accountability mechanism when consequential computation can occur without an interpretable token trace. The governance implication is not simply that monitors need better detection, but that institutions must stop treating model-generated explanations as sufficient evidence of intent, compliance, or safe internal process.
