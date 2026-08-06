---
title: "Position: LLMs Can't Jump"
source: "https://openreview.net/forum?id=klU4737opt"
source_url: "https://openreview.net/forum?id=klU4737opt"
publication: "ICML 2026"
date: "2026-01-27"
date_read: "2026-08-06"
issue_url: "https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/issues/63"
primary_domain: "AI Safety & Evaluation"
domain: "AI Safety & Evaluation"
tags:
  - AI benchmarks
  - capability
  - LLMs
  - philosophy of AI
  - foundation models
  - epistemic integrity
scholarly_signal: "cs.AI"
key_insight: "The inability to generate new premises is not only a model-capability gap; it is a governance boundary for institutions that delegate scientific agenda-setting to AI. World models may expand the space of machine-generated hypotheses, but without rules for evidentiary status, validation, attribution, and contestability they also concentrate authority over what counts as a plausible explanation."
---

# Paper Review

## Review

Tom Zahavy separates scientific discovery into induction, deduction, and abduction. Large language models compress patterns and increasingly execute formal derivations, but the paper argues that they cannot perform the abductive jump from experience to new explanatory premises. Einstein's route to General Relativity is used as the case study. Newtonian gravity had little empirical error to optimise against, while the equivalence principle emerged from a physically grounded thought experiment rather than from a large observational dataset or a deduction from settled axioms.

The paper usefully shifts capability analysis from whether a model can solve a stated problem to whether it can decide that the prevailing problem formulation is wrong. This distinction matters institutionally. A system that searches within supplied objectives leaves agenda-setting, ontology selection, and premise formation elsewhere. Claims of an autonomous AI scientist therefore conceal a continuing allocation of decision rights to whoever defines the simulation, selects admissible variables, sets novelty criteria, and decides which anomalies deserve attention.

The historical reconstruction divides Einstein's work into ideation, consolidation, and mathematical validation. It then maps these stages onto Peirce's inference categories and argues that manipulative abduction, grounded in counterfactual physical simulation, generated the equivalence principle. Interactive world models are proposed as the missing substrate because they could let an agent intervene in a simulated environment rather than merely predict likely pixels or tokens.

This is a position argument, not an empirical demonstration that LLMs are structurally incapable of abduction. General Relativity is one exceptional discovery and cannot establish a universal boundary between human and machine inference. The paper also moves between several claims that require separate tests: present LLMs lack sensory grounding; text-only systems cannot generate genuinely new axioms; action-controllable world models can supply the missing mechanism; and abductive novelty can be distinguished from rare recombination. No benchmark, operational definition, or falsification protocol connects these claims. ARC-style sparse inference is acknowledged but dismissed as lacking embodied manipulation, leaving the decisive category boundary conceptually asserted rather than measured.

The prescription also relocates rather than resolves the governance problem. A world model is not neutral sensory access. Its physics, action space, resolution, exclusions, and reward structure determine which counterfactuals can be imagined. The operator of the simulation therefore acquires upstream control over machine hypothesis formation. If a small number of laboratories own the models, compute, scientific corpora, and experimental interfaces, they may become private governors of scientific possibility, deciding which representations are available before any formal proof or external validation begins.

The paper does not specify how a machine-generated axiom should acquire evidentiary standing. Novelty, explanatory compression, simulation consistency, and predictive success are different tests. Nor does it address attribution when a hypothesis is jointly produced by researchers, model developers, training data, and simulation designers. False but compelling hypotheses could redirect funding and laboratory capacity long before decisive evidence exists. Scientific governance therefore needs staged validation, provenance records, independent replication, conflict disclosure, revocation of unsupported claims, and routes for excluded communities or disciplines to contest the model's ontology.

The durable contribution is the separation of premise generation from downstream reasoning. That separation should constrain procurement and policy claims about automated discovery. Institutions should not treat fluent hypothesis production as autonomous scientific judgment, and they should not treat embodiment as a sufficient remedy. The relevant assurance question is who controls the world in which the system learns to imagine, who validates the resulting premises, and who can interrupt their conversion into research priorities, capital allocation, or public policy.

## Key Insight

The inability to generate new premises is not only a model-capability gap; it is a governance boundary for institutions that delegate scientific agenda-setting to AI. World models may expand the space of machine-generated hypotheses, but without rules for evidentiary status, validation, attribution, and contestability they also concentrate authority over what counts as a plausible explanation.
