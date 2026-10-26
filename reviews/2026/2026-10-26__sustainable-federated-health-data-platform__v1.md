---
title: "A sustainable platform for federated health data access, AI innovation, and regulatory acceptance in alignment with the European Health Data Space principles"
source: "https://doi.org/10.12688/openreseurope.23459.4"
publication: "Open Research Europe 2026, 6:181 (version 4, 6 October 2026)"
date_read: "2026-10-26"
primary_domain: "Privacy & Data Protection"
tags: ["digital sovereignty", "interoperability", "governance-by-design", "regulatory frameworks", "AI governance", "assurance"]
key_insight: "Federated health infrastructure preserves local custody of patient data, but legitimate secondary use still depends on independently reviewable access authority, cross-border policy reconciliation, and evidence of acceptable analytical outcomes."
published: "2026-10-06"
doi: "10.12688/openreseurope.23459.4"
peer_review_status: "peer-reviewed"
paper_type: "other"
paper_version: "v4; 1 approved, 1 approved with reservations"
review_status: "current"
governance_facets: ["authority", "gatekeeping", "accountability", "auditability", "dependency", "institutional-capacity"]
---

# Paper Review

## Review

Boutsma and colleagues describe IDERHA, a European public-private initiative to build a disease-agnostic, federated health-data research infrastructure aligned with European Health Data Space (EHDS) principles. The Open Letter is an architectural and governance prospectus, not a report of demonstrated clinical benefit or regulatory acceptance. Its lung-cancer studies provide a bounded initial setting for developing risk prediction from electronic health records and imaging, rather than evidence that such models are already clinically validated. The fourth version, published in October 2026, incorporates substantive peer-review clarifications about semantic mapping, clinical decision support, federated-learning limitations, and institutional authority.

The design moves computation to secure processing environments at participating data holders. Its central node authenticates users, supports dataset discovery through DCAT-AP metadata, and initiates analyses; local nodes evaluate requests, grant permits, enforce their own use conditions, and retain patient-level data. Figure 3 makes this separation visible: a central AI manager coordinates algorithms and model weights while local institutions retain data. IDERHA combines OMOP common-data-model mapping with clinical expert review, provenance-aware extraction and transformation, OHDSI quality tooling, and study-specific readiness assessments. The detailed mapping workflow is a meaningful improvement over treating common schemas as proof of semantic equivalence. Its stated design also draws on GA4GH, IDSA/EDC, DICOM, FHIR, and other standards rather than presenting federation as a proprietary protocol.

The governance consequence is more qualified than the phrase 'data sovereignty' can suggest. Local custody and local permit decisions are substantive limits on central extraction, and the authors explicitly state that the Integrated Data Access Governance Council (IDAGC) advises on policy rather than deciding individual access requests. Yet central orchestration, metadata visibility, acceptable analysis workflows, model-update aggregation, and interoperability profiles can still determine who participates and which research questions become feasible. Differences in national permissions may be accommodated by changing analyses or excluding nodes, but that creates selection effects that can compromise the portability and representativeness of the resulting evidence. The paper recognizes heterogeneous data and non-identical local constraints without establishing an auditable method for assessing how exclusions affect regulatory conclusions.

Several risk boundaries deserve precision. Keeping raw clinical records and DICOM images local reduces transfer exposure but does not by itself eliminate leakage through aggregates or model updates, nor does it validate the legality of each secondary use. Likewise, OMOP conformance and a living Data Management Plan make data transformations and compliance assertions more inspectable without establishing clinical validity, an adequate legal basis, or approval by a health technology assessment or medicines regulator. The revised account appropriately separates predictive machine learning from generative AI in clinical workflows, requires intended-use validation, and keeps clinical responsibility within applicable institutional and regulatory arrangements. It does not provide completed cross-site performance, privacy-attack, authorization-revocation, audit, or regulator-acceptance evidence.

The strongest counterargument is one of genre and maturity: an Open Letter can establish an architecture and operational research agenda without functioning as an implementation audit. That objection is justified. The paper specifies more real machinery than a generic aspiration to share health data, including node-level enforcement and version-controlled mapping decisions. But its claim to a sustainable pan-European model remains contingent. Next evidence should include a replayable access-decision and withdrawal trace spanning the central and local nodes, procedures for legal disagreement and contested permissions, quantified mapping and cohort-concordance results, privacy and model-update leakage tests, and a documented regulatory review of a particular real-world-evidence submission. Sustainability also requires named long-term operators, financing, accountability, and exit/portability arrangements. IDERHA establishes a plausible federated operating architecture; its decisive outstanding question is whether distributed data custody can coexist with legitimate, consistent, and contestable federation-wide governance.

## Key Insight

Federated health infrastructure preserves local custody of patient data, but legitimate secondary use still depends on independently reviewable access authority, cross-border policy reconciliation, and evidence of acceptable analytical outcomes.
