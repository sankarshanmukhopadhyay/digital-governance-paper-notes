---
title: "Toward Risk Thresholds for AI-Enabled Cyber Threats"
source: "https://cltc.berkeley.edu/wp-content/uploads/2026/01/Toward_Risk_Thresholds_for_AI-Enabled_Cyber_Threats.pdf"
publication: "UC Berkeley Center for Long-Term Cybersecurity"
date_read: "2026-03-06"
primary_domain: "Cybersecurity"
tags: ["AI safety", "cyber risk", "thresholds", "bayesian networks", "decision triggers"]
---

# Paper Review

## Review

AI cyber “thresholds” today are mostly compliance theatre.

Every major frontier framework says some version of: “If the model meaningfully uplifts cyber offense, we will add safeguards.” The problem is that “meaningfully” is doing all the work. It is a vibes-based control with a PDF wrapper.

This CLTC paper lands a needed punch: thresholds cannot be a binary gate on a capability benchmark. Cyber risk is probabilistic, multi-factor, and adversarial. If your threshold does not model uncertainty, it is not a threshold. It is a press release.

The proposed move is pragmatic: use Bayesian Networks to turn hand-wavy threshold language into a measurable system. Nodes for capability, access, attacker skill, defenses, and deployment context. Edges that encode how these variables actually interact. Then update as evidence changes. This is how mature risk functions operate in other domains, and cyber is one of the few AI risk areas with enough telemetry to even attempt it.

But a probabilistic model is not governance unless you define what happens when the probability spikes.

A future iteration of this approach needs to be brutally explicit:

- What is the threshold output: probability of compromise, expected loss, or systemic impact?
- What is the baseline: human-only, open-weights, or criminal tooling markets?
- What action triggers are mandatory: gate deployment, restrict access, kill features, or notify regulators?

Otherwise we build beautiful Bayesian dashboards that let everyone feel quantified while nothing is actually constrained. Risk without decision rights is analytics cosplay.

## Key Insight

Cyber-risk thresholds become real governance only when probabilistic assessment is tied to explicit baselines, trigger points, and mandatory actions.
