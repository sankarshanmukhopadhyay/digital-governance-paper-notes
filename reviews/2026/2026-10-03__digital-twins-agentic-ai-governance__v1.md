---
title: "Digital Twins and Agentic AI: Applications, Risks, and Governance Frameworks"
source: "https://doi.org/10.3390/fi18100501"
publication: "Future Internet 2026, 18, 501"
date_read: "2026-10-03"
primary_domain: "AI Governance"
tags: ["AI agents", "agentic systems", "AI risk management", "deployment controls", "assurance", "accountability"]
key_insight: "Digital twins turn agentic governance into a control-plane problem: autonomy should track consequence and reversibility, but oversight is meaningful only when humans possess actual authority, timely evidence, and workable mechanisms to intervene."
published: "2026-09-23"
doi: "10.3390/fi18100501"
peer_review_status: "peer-reviewed"
paper_type: "research-article"
review_status: "current"
governance_facets: ["authority", "accountability", "delegation", "enforcement", "auditability"]
---

# Paper Review

## Review

Alnoman et al. review the emerging intersection of digital twins and agentic AI, asking how autonomy, multi-agent coordination, risk, human control, and governance should be understood when software agents can act through persistent representations of physical or operational systems. The paper's main governance contribution is not a new technical architecture. It is a cross-domain synthesis that treats autonomy as context-dependent and links consequence severity, uncertainty, reversibility, time-to-harm, and intervention feasibility to progressively stronger control requirements. Its Tables 4 and 6 convert that proposition into a usable control model: bounded permissions, independent monitoring, explicit authorization, rollback, return-of-control, and shutdown become governance mechanisms rather than generic safety aspirations.

The review also makes two useful distinctions. First, it separates conceptual and simulation-based demonstrations from operational evidence, refusing to treat feasibility as proof of safe deployment. Second, it distinguishes regulations, risk-management frameworks, management-system standards, impact assessment, and implementation-oriented security guidance instead of presenting them as interchangeable governance layers. The mapping across NIST AI RMF, the EU AI Act, ISO/IEC 42001, ISO/IEC 23894, ISO/IEC 42005, and OWASP gives practitioners a clearer account of which institutional function each instrument can perform.

The evidence base remains the limiting factor. The authors explicitly note that much of the literature is conceptual or simulation-based, that validation practices are heterogeneous, and that the review does not apply a formal evidence-quality or risk-of-bias scoring method. The resulting framework therefore establishes a credible governance synthesis, not evidence that the proposed controls work reliably in high-consequence deployments. That boundary is especially important because human oversight is treated correctly as a capability, not merely an approval button: operators need competence, information, authority, access, and enough time to act. Yet those conditions are mostly specified as governance requirements rather than evaluated properties of deployed systems.

A deeper institutional gap appears around delegated authority. The paper assigns accountable roles and discusses orchestrators, tool privileges, policy constraints, monitoring, and human authorization, but it does not fully specify how authority is granted to an agent, narrowed across multi-agent chains, revoked, or proven at the moment of action. In a digital-twin environment, this is consequential because a technically valid action can still exceed the authority of the agent or orchestrator that issued it. Audit trails and tool-use traces can reconstruct what happened without establishing who was entitled to cause it. The strongest counterargument is that this is a structured literature review, not a protocol or authorization architecture, and the authors do not claim otherwise. That scope defense is valid. It fixes the contribution at the level of governance design principles rather than executable authority infrastructure.

Relative to adjacent archive work on agentic rights, responsibility cascades, and normative infrastructure, this paper contributes a more operational risk-to-control mapping for systems that can affect cyber-physical state. Its durable contribution is the insistence that autonomy must vary with consequence and reversibility, and that meaningful human control depends on practical intervention capacity. The next step is empirical: test autonomy-transition thresholds, delegated authorization, rollback, operator workload, and evidence continuity in real deployments, including cases where agents are replaced, permissions change during execution, or human intervention arrives too late.

## Key Insight

Digital twins turn agentic governance into a control-plane problem: autonomy should track consequence and reversibility, but oversight is meaningful only when humans possess actual authority, timely evidence, and workable mechanisms to intervene.
