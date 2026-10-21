---
title: "Compliant with Local Controls, Collectively Discriminatory: A Governance Architecture for Multi-Agent AI in Regulated Finance"
source: "https://arxiv.org/abs/2609.27994"
publication: "arXiv"
date_read: "2026-10-21"
primary_domain: "AI Governance"
tags: ["AI agents", "AI governance", "fairness and bias", "authorization", "assurance", "accountability"]
scholarly_signal: "cs.MA"
key_insight: "Local compliance is not a compositional property: when institutional outcomes emerge from coupled agents, governance must attach observability, revocable authority, containment, and accountability to the population and workflow, not only to each component."
published: "2026-09-23"
doi: "10.48550/arXiv.2609.27994"
peer_review_status: "preprint"
paper_type: "preprint"
paper_version: "arXiv v1"
review_status: "current"
governance_facets: ["authority", "accountability", "revocation", "enforcement", "auditability", "institutional-capacity"]
---

# Paper Review

## Review

This paper identifies a structural governance failure in agentic finance: controls that are valid for each model or agent do not necessarily compose into acceptable institutional outcomes. The authors call this constitutional non-compositionality and use it to justify ARIA, a population-level governance architecture spanning policy specification, population assurance, bounded decision authority, runtime enforcement, adaptive policy learning, and preservation of human oversight competence. The contribution is not a claim that ARIA has been validated in production. It is a reference architecture and falsifiable research agenda intended to make multi-agent governance observable, revocable, auditable, and attributable.

The paper turns that proposition into an institutional control design rather than leaving it at the level of alignment theory. A minimal counterexample shows that every component can pass a local equal-treatment check while aggregate approval patterns violate a portfolio-level disparity constraint. Two simulations then illustrate the mechanism: shared-signal and measurement-quality coupling can produce thin-file exclusion despite zero local-control violations, while an observed-versus-expected distributional monitor can provide earlier warning than a prohibited-outcome monitor in a deliberately constructed drift regime. The authors are careful about the evidentiary boundary. These are mechanism demonstrations, not production estimates, and the proposed M2 indicator is explicitly support-dependent.

ARIA's most consequential move is to separate technical capability from governed authority. Its bounded-decision-authority model makes execution conditional on a context-specific authority profile, while runtime policy decision and enforcement points can downgrade, sandbox, or suspend action when population-level signals deteriorate. This moves governance closer to the workflow where institutional harm can actually emerge. The accompanying RACI allocation and named audit artifacts also make a useful distinction between having controls and being able to prove that those controls were exercised.

The architecture nevertheless concentrates substantial governance power in the institutions that define the constitutional core, calibrate expected behavior, set alarm thresholds, approve authority changes, and decide when containment is justified. The paper recognizes this by calling for stakeholder input, pre-registered amendments, independent validation, and regulatory access, but it does not fully specify how affected customers contest those choices or obtain redress when population-level controls still produce an adverse decision. This is more significant than the absence of production validation, because the authors explicitly frame validation as future work. A more material unresolved question is who has legitimate authority over the reference distributions and thresholds that turn M2 and containment into enforceable institutional policy.

The paper also correctly identifies two second-order risks: compliance theater and repurposing of monitoring infrastructure for worker or customer surveillance. Those risks follow directly from the architecture. Population observability can improve accountability, but it can also centralize evidence production and expand institutional visibility. The governance burden therefore shifts rather than disappears. ARIA would need independent scrutiny of reference models, amendment procedures, containment decisions, and customer-impact evidence to prevent runtime governance from becoming a technically sophisticated form of self-certification.

As a research architecture, ARIA materially advances the discussion because it makes collective AI governance testable. Its proposed validation program names measurable outcomes including violation rate, duration, overshoot, containment latency, mediated-action coverage, false containment, utility loss, policy regression, and oversight competence. If those measures fail to improve relative to simpler controls, the architecture is explicitly revisable. That falsifiability is important. The paper establishes that component assurance is insufficient for coupled agent populations and supplies a concrete institutional design for testing the alternative. It does not yet establish that ARIA is the right supervisory architecture for finance, but it defines what evidence would be required to make that stronger claim.

## Key Insight

Local compliance is not a compositional property: when institutional outcomes emerge from coupled agents, governance must attach observability, revocable authority, containment, and accountability to the population and workflow, not only to each component.
