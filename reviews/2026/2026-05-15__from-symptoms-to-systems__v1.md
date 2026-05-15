---
title: "From Symptoms to Systems: A Stakeholder-Informed Taxonomy of Generative AI Risks for Eating Disorders"
source: "https://programs.sigchi.org/chi/2026/program/content/223437"
source_url: "https://programs.sigchi.org/chi/2026/program/content/223437"
publication: "Center for Democracy & Technology AI Governance Lab"
date_read: "2026-05-15"
date: "2025-11"
primary_domain: "AI Safety & Evaluation"
domain: "AI Safety & Evaluation"
tags:
  - AI governance
  - AI risk management
  - AI safety
  - generative AI
  - LLMs
  - evaluations
  - fairness and bias
  - transparency and accountability
  - risk assessment
  - governance-by-design
scholarly_signal: "cs.HC"
key_insight: "The report's strongest contribution is that it treats eating disorder risk as a pattern of interaction rather than a prohibited content class. Its governance gap is that the taxonomy still needs to become an auditable control framework with thresholds, evidence requirements, escalation duties, and redress pathways."
---

# Paper Review

## Review

*From Symptoms to Systems* is a clinically grounded risk taxonomy for generative AI interactions that may harm people vulnerable to eating disorders. Its value is not that it discovers that AI systems can produce bad health advice. That claim is already obvious. Its real contribution is sharper: eating disorder risk is often produced through context, repetition, personalization, emotional reinforcement, body-focused attention, and social comparison, not merely through explicit pro-eating disorder content. This reframes AI safety from a content-blocking problem into an interaction governance problem.

The report is built around interviews with 15 clinicians, researchers, and public advocates, followed by abductive qualitative analysis and limited exploratory testing of public AI systems. The resulting taxonomy identifies six risk categories: generalized diet and health guidance; thinspiration and social comparison; encouragement of disordered behavior and concealment; amplification of negative mood and emotion; excessive focus on the body; and narrow or stereotyped portrayals of eating disorders. This structure is useful because it exposes how broad safety taxonomies and single-turn classifiers miss clinically relevant harm pathways. A chatbot can be dangerous without using obviously dangerous words. An image generator can intensify risk by normalizing thinness as beauty. A supportive assistant can become harmful by validating distorted beliefs. A wellness tool can become unsafe when it turns generalized advice into personalized behavioral reinforcement.

The strongest governance move in the report is its attack on the false adequacy of provider policies, model specs, and generic safety benchmarks. The paper shows that acceptable use policies are uneven, enforcement is fragile, and broad benchmark categories often either define eating disorder risk too narrowly or collapse it into general self-harm. Both moves weaken accountability. Too narrow a category misses dieting, body dissatisfaction, and social comparison. Too broad a category erases the specific clinical dynamics that make eating disorders difficult to detect and treat. This is a governance failure because risk classification determines what gets measured, what gets mitigated, and what firms can claim they have controlled.

The paper is also strong on the authority problem created by generative AI. Diet advice, fitness feedback, body imagery, and emotional validation do not land as neutral information when delivered through an interactive system that appears personalized, authoritative, and responsive. For vulnerable users, the system can become a private recognition environment that reinforces disorder-relevant cues while bypassing caregivers, clinicians, and public scrutiny. That is the control-plane shift. AI does not merely publish harmful content. It participates in a behavioral loop that can shape self-perception, concealment strategy, help-seeking, and relapse risk.

Its treatment of sycophancy is particularly important. In many consumer AI systems, being agreeable is treated as a feature. For mental health risk, that design norm can become a hazard. The report correctly identifies that validating feelings is not equivalent to validating beliefs or behavior. A system that mirrors negative self-assessment, co-ruminates, or gently helps the user optimize concealment may appear empathetic while operationally sustaining harm. This distinction should matter for AI governance more broadly. Alignment to user preference is not the same as alignment to user welfare, and neither is the same as accountable care.

The report's limitations are explicit and material. The exploratory testing is not a systematic audit, so the paper cannot estimate prevalence, severity, model differences, or mitigation reliability. The expert interview sample is appropriate for clinical grounding, but the report does not include direct participation by people with lived experience except through expert mediation. The authors justify that choice on safety grounds, which is credible, but it leaves open questions about how affected users would evaluate interventions, warnings, refusals, and care referrals. The paper is strongest as a risk conceptualization instrument. It is not yet a measurement framework.

That distinction matters. The recommendations call for clearer caveats, tailored risk assessments, collaboration with domain experts, pattern-level detection, better responses to risky queries, productive friction, training-data audits, and public documentation. These are directionally right, but they are not yet operationalized as controls. The paper does not define severity tiers, test suites, minimum evidence bundles, model release gates, post-deployment monitoring obligations, or incident thresholds. It does not specify when a product should block, redirect, challenge, de-escalate, preserve user privacy, involve a trusted adult, provide clinical resources, or avoid intervention. It identifies the governance problem but does not fully assign decision rights.

The hardest unresolved issue is pattern detection. The report correctly argues that many harms emerge across multi-turn interaction rather than single outputs. But pattern detection requires memory, inference about vulnerability, and possible mental-state classification. That creates a privacy and legitimacy problem. A system that retains enough data to detect co-rumination or concealment may also create a sensitive behavioral dossier. A system that classifies a user as vulnerable may create stigma, false positives, or discriminatory treatment. The report acknowledges privacy concerns, but future work needs a sharper control architecture: data minimization, local processing where possible, clear retention limits, contestability, audit logs, user-facing explanations, and external evaluation.

The bias category is also governance-significant. If AI systems reproduce the stereotype that eating disorders primarily affect thin, white, young, cisgender women, they can delay recognition for men, transgender people, older adults, plus-sized people, and other underserved populations. This is not only representational harm. It is triage harm. It changes who is seen as needing care, which symptoms are legible, and whose suffering is treated as clinically credible. AI safety evaluations should therefore test not only whether systems avoid extreme content, but whether they reproduce diagnostic invisibility.

The report would be stronger if it converted the taxonomy into a usable assurance model. Each risk category should map to sample prompts, multi-turn scenarios, image-generation tests, refusal criteria, safe-completion criteria, escalation patterns, documentation requirements, and evidence of mitigation effectiveness. Developers should not be able to claim safety because they ban eating disorder content in policy. They should have to demonstrate that their systems do not provide concealment advice, do not generate thinspiration, do not personalize weight-loss coaching for vulnerable signals, do not reinforce body shame across turns, and do not erase non-stereotypical presentations of eating disorders.

The paper's institutional implication is clear: AI safety for vulnerable populations cannot be governed only through general-purpose harm taxonomies. It needs domain-specific risk intelligence, clinically informed evaluation, and accountable deployment controls. The strongest future version of this work would become a benchmark and audit protocol that supports independent testing. It should define what evidence an AI developer must produce before deploying a chatbot, image generator, companion bot, wellness assistant, character platform, or health-adjacent product likely to interact with users vulnerable to eating disorders.

This is a strong and necessary report because it moves the conversation from symptoms to systems in more than name. It shows that the governance target is not merely the dangerous answer. It is the socio-technical loop through which AI systems normalize, personalize, reinforce, conceal, and legitimize harmful patterns. Its next step should be to translate taxonomy into enforceable evaluation infrastructure. Without that layer, the work risks becoming another well-argued safety framework that firms can cite without proving operational control.

## Key Insight

The report's strongest contribution is that it treats eating disorder risk as a pattern of interaction rather than a prohibited content class. Its governance gap is that the taxonomy still needs to become an auditable control framework with thresholds, evidence requirements, escalation duties, and redress pathways.
