---
title: "Large-scale online deanonymization with LLMs"
source: "https://arxiv.org/abs/2602.16800"
publication: "arXiv"
date_read: "2026-03-18"
primary_domain: "Privacy & Data Protection"
tags:
  - LLMs
  - AI safety
  - cyber risk
  - evaluations
  - evidence
  - AI governance
  - deployment controls
  - accountability
scholarly_signal: "cs.CR"
key_insight: "LLMs do not need to exceed human investigative capability to collapse pseudonymity at scale — they only need to reduce its cost, and that cost reduction is now sufficient to make large-scale deanonymization a routine, automatable threat."
---

# Paper Review

## Review

This paper delivers a result that the privacy community has been dreading but lacked rigorous quantification for: LLMs make pseudonymity on the open internet practically indefensible against a moderately resourced adversary.

The core contribution is a modular four-stage pipeline — Extract, Search, Reason, Calibrate — that decomposes deanonymization into steps where LLMs add measurable, ablatable value over classical baselines. Against the Netflix Prize attack as a structured-data comparator, the LLM pipeline is not marginally better; it is categorically better. The baseline achieves near-zero recall at 99% precision on every dataset. The full LLM pipeline achieves 45% recall on LinkedIn–Hacker News matching and 38% on temporally-split Reddit profiles at the same precision threshold. That gap is not a tuning artefact — it reflects that unstructured text was simply intractable for classical methods and is now tractable.

The experimental design is careful about a hard problem: ground-truth deanonymization labels require either that users have already exposed their identity (biasing toward low-privacy-consciousness profiles) or that profiles be synthetically split (introducing intra-person similarity that real alt-accounts may not share). The authors are transparent about both biases and argue persuasively that false positive rates — the metric that governs harm in real attacks — transfer across settings regardless of recall overestimation. The Anthropic Interviewer demonstration (9 scientists re-identified from partially redacted transcripts) makes the agentic threat concrete without requiring exotic tooling.

The governance implications are stated clearly and are correct. Classical frameworks — k-anonymity, differential privacy — were designed for structured databases and offer no protection here. LLM-based text sanitization exists but is known to leave semantic residue. Rate-limiting API access and detecting bulk scraping are cited as partial mitigations but the authors are honest that splitting an attack into summarisation, embedding, and ranking tasks makes it difficult to distinguish from legitimate use. The practical conclusion is uncomfortable: platforms that make pseudonymous user content accessible at scale should assume that content is linkable to real identities, and users posting under pseudonyms should not assume otherwise.

The paper's main analytical limitation is that its strongest Calibrate step (Swiss-system tournament sorting) is explicitly a batch attack — it requires a large co-present query set to function and cannot deanonymize a single individual efficiently. The per-user agentic attack is demonstrated but not rigorously benchmarked at scale. These are two different threat models that warrant cleaner separation in the framing.

## Key Insight

LLMs do not need to exceed human investigative capability to collapse pseudonymity at scale — they only need to reduce its cost, and that cost reduction is now sufficient to make large-scale deanonymization a routine, automatable threat.
