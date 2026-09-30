---
title: "Governance Laundering: A Taxonomy of Failure Modes in AI Compliance Architectures"
source: "https://doi.org/10.5281/zenodo.22902565"
publication: "FERZ, Inc. research report"
date_read: "2026-10-01"
primary_domain: "AI Governance"
tags: ["AI governance", "assurance", "authorization", "evidence", "procurement", "reproducibility"]
key_insight: "Governance evidence becomes institutionally meaningful only when it can reconstruct a decision, prove that authorization preceded execution, and preserve the authority and action context that made the decision legitimate."
published: "2026-09-01"
doi: "10.5281/zenodo.22902565"
peer_review_status: "institutional-publication"
paper_type: "policy-report"
paper_version: "v1.2"
review_status: "current"
governance_facets: ["authority", "enforcement", "auditability", "provenance", "dependency"]
---

# Paper Review

## Review

Edward Meyman’s report defines “governance laundering” as the condition in which an organization can present persuasive governance artifacts while lacking the architectural properties needed to support the assurance those artifacts imply. Its central move is to distinguish governance artifacts from governance evidence: logs, dashboards, attestations, certificates and anchored hashes record that governance-related activity occurred, while evidence must let an independent third party reconstruct a specific policy verdict from version-pinned inputs, policy, evaluator state and trace. The report then maps seven structural failure families to seven requirements: enforcement, independence, completeness, non-delegability, pre-execution authorization, continuity between verdict and action, and semantic stability.

The contribution is unusually operational. The Expanded Anti-Laundering Protocol turns the taxonomy into seven tests covering exportability, offline replay, state completeness, fail-closed behavior, mutation detection, pre-execution dependency and custody continuity. The report is careful about assurance boundaries: an Evidence-Grade result applies only to the declared scope and does not establish non-bypassability, governing authority or input provenance. Those are recorded separately. This distinction matters because it prevents replayability from being mistaken for legitimacy. The paper also correctly treats monitoring and authorization as different institutional functions: post-hoc detection may produce useful evidence, but it does not prove that an action was permitted before execution.

The methodology is conceptual and architectural rather than empirical. Failure modes are derived from the proposed evidence-grade requirements, then illustrated through worked examples and an a priori susceptibility map across product categories. This makes the framework testable as a procurement and audit instrument, but it does not establish how frequently the failure modes occur in deployed systems or whether the seven-family taxonomy is complete. The paper itself acknowledges both limits. Its susceptibility map is therefore best read as a design-risk hypothesis, not a market measurement.

A more consequential governance limitation sits around authority. FM-4 correctly distinguishes valid delegation from unsupported reliance on upstream safety mechanisms, and the supplemental authority assessment asks who governs each action and what delegation exists. Yet the report still treats authority primarily as something to be established evidentially, not as something whose legitimacy may itself be contested. A perfectly replayable and fail-closed system can still enforce an illegitimate, discriminatory or procedurally defective policy. The strongest counterargument is that the report deliberately scopes itself to evidence-grade authorization rather than normative legitimacy, and it explicitly avoids claiming that an EALP grade establishes legal compliance. That response is persuasive as a scope defense, but it also fixes the boundary of the framework: EALP can establish that a governance rule was applied faithfully, not that the rule or governing institution was entitled to decide.

Relative to adjacent work in this archive on decision ownership, responsibility cascades and normative infrastructure for agentic systems, this report contributes a sharper evidentiary test for whether governance claims survive independent reconstruction. Its most reusable proposition is that governance should be judged by the properties of the authorization boundary and the evidence it leaves behind, not by the sophistication of dashboards or policies surrounding it. The next step should be empirical deployment: apply EALP across real governance products, publish negative and ambiguous cases, test inter-rater consistency, and examine whether organizations can preserve both replayability and contestable authority under adversarial conditions.

## Key Insight

Governance evidence becomes institutionally meaningful only when it can reconstruct a decision, prove that authorization preceded execution, and preserve the authority and action context that made the decision legitimate.
