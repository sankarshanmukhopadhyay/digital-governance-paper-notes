---
title: "AI for Justice: Ethical, Fair and Robust Adoption in India's Courts"
source: "https://www.digitalfutureslab.in/publications/ai-for-justice-ethical-fair-and-robust-adoption-in-india-s-courts"
publication: "DAKSH & Digital Futures Lab / UNDP"
date_read: "2026-03-23"
primary_domain: "Public Sector Digital Strategy"
tags:
  - AI governance
  - judicial systems
  - India
  - public sector
  - fairness and bias
  - rights-based frameworks
  - risk assessment
  - institutional readiness
  - transparency and accountability
  - regulatory frameworks
  - public administration
  - state capacity
scholarly_signal: "cs.CY"
key_insight: "AI adoption in courts should be structured around a rights-based, multi-stage assessment framework (institutional readiness, risk at use-case level, technical vendor assessment, and ongoing monitoring) grounded in judicial legitimacy rather than efficiency gains, because courts are unique institutional contexts where AI's opacity, potential for bias, and procedural implications threaten not just individual fairness but systemic judicial legitimacy."
---

# Paper Review

## Review

This UNDP-commissioned report from DAKSH and Digital Futures Lab articulates a governance framework for AI adoption in India's courts, grounded in institutional realities, rights-based principles, and extensive stakeholder consultation. The report addresses a critical gap: while courts have digitized substantially (eCourts project), AI adoption remains ad hoc, poorly documented, and vulnerable to vendor-driven pilot creep without structured safeguards.

The problem framing is incisive. AI in judicial contexts differs fundamentally from other sectors because courts are custodians of legitimacy and impartiality—qualities that cannot be "optimized" away. The report identifies distinct sources of harm arising not merely from model training (bias, hallucination) but from the procedural and institutional context: translation vs. judgment drafting carry different legitimacy implications; sensitive case types (sexual violence, child welfare) require heightened privacy protections; and litigant vulnerability (illiteracy, language barriers, legal knowledge asymmetry) amplifies the stakes of system errors. These institutional specificities are often overlooked in generic AI governance frameworks.

The report catalogs current AI use (translation, transcription, case summarization) and identifies how deployment has unfolded: through individual champions (judges or court administrators), with minimal documentation, often via "shadow" experimental use. This champion-dependency creates fragility—when judicial officers transfer or retire, institutional knowledge and AI initiatives often lapse. The absence of dedicated technical cadres, use-case registries, or centralized procurement creates both transparency and quality control gaps.

The proposed framework comprises four sequential assessments. Institutional Readiness examines whether courts have the human resources, infrastructure, compliance capacity, and organizational readiness to responsibly integrate AI. Risk Assessment identifies potential harms at the use-case level (e.g., translation's risk profile differs from case filtering). Technical Assessment evaluates vendor capabilities, data governance, model transparency, security posture, and audit trails. Ongoing Assessment monitors real-world performance and emergent harms post-deployment. This sequencing is sound: readiness must precede adoption, and harm monitoring must continue throughout system lifetime.

The rights-based framing is the report's conceptual strength. Rather than adopting a binary high-risk/low-risk classification (common in regulatory frameworks like the EU AI Act), the report grounds assessment in fundamental principles: access to justice, fairness, due process, privacy, judicial independence. This reorientation matters because it makes visible the ways AI can undermine courts without creating obvious "harms" in conventional metrics. A system that is 95% accurate in case categorization but systematically mislassifies minority litigants' cases (e.g., religious minority property disputes) creates no individual "failure" flagged by accuracy metrics yet erodes systemic fairness.

The report provides concrete guidance: 10 safeguards (domain expert consultation, public disclosure of AI use and vendors, human-in-the-loop, mandatory validation, data minimization, opt-out mechanisms, complaint redress, cybersecurity oversight, bias audits, audit logs). Contractual clauses for vendor agreements and guidance for judicial officers using generative AI operationalize these principles. The specificity—e.g., requiring that vendors provide datasheets documenting dataset structure, limitations, and known biases—reflects understanding of what institutional actors need to verify vendor claims.

Limitations merit acknowledgment. First, the framework is prescriptive but not coercive. It provides assessment templates and guidance but does not specify enforcement mechanisms or consequences for non-compliance. If a high court judges its own institutional readiness as adequate without meaningful validation, or if it adopts a tool without completing a risk assessment, the framework provides no institutional brake. The report acknowledges this gap (recommending "complementary measures" including technical cadres and sandboxing frameworks) but does not resolve it.

Second, the framework assumes capacity that many courts lack. Completing institutional readiness, risk, and technical assessments requires expertise in data governance, fairness auditing, cybersecurity, and legal-technical translation. Many Indian courts operate with constrained administrative capacity; the burden of assessment could itself become a barrier, particularly for smaller courts. The report does not adequately address how assessment capacity could be built, whether through centralized auditing entities or through capacity transfer.

Third, the rights-based framework, while conceptually sound, remains somewhat abstract when applied to live deployment trade-offs. For instance, if translation AI improves access to justice by enabling multilingual case materials but introduces small systematic biases against minority languages, how should courts weigh access against fairness? The framework identifies the tension but does not provide decision procedures for resolving it. Courts will ultimately face these trade-offs without clear guidance.

Fourth, the report does not grapple with the political economy of AI adoption in courts. Institutional readiness assessments themselves can become regulatory theater if driven by enthusiasm for AI rather than genuine risk assessment. Similarly, the recommendation for "public disclosure of AI uses and vendors" assumes that transparency alone will drive accountability—a questionable assumption in institutional contexts where press attention is limited and civil society capacity to monitor courts varies.

Fifth, the framework's applicability to emerging agentic AI systems is limited. The report focuses on task-specific tools (translation, summarization) where outputs are directly integrated into human decision-making. Agentic systems that autonomously triage cases, draft orders, or escalate decisions operate under different failure modes (autonomous misbehavior, constraint violation, authority creep). The report provides a foundation but would need extension to address this evolution.

For the Indian context specifically, the report's identification of institutional realities is invaluable: the champion-dependency problem, the gap between digitization and AI readiness, the coordination challenges between Supreme Court, High Courts, and state judiciaries. However, the report underestimates how federal coordination challenges complicate adoption. If the framework recommends centralized oversight (e.g., through a national technical cadre), it must address which institution creates and governs that cadre—the Supreme Court? The Department of Justice? The negotiation itself may freeze adoption while institutional authority is clarified.

The report's comparison of global approaches (cautionary, neutral, enthusiastic) is descriptive but does not recommend which stance India should adopt. For a judicial system contending with case backlogs and access-to-justice deficits, cautionary approaches may seem like obstacles to efficiency. Yet the report implicitly argues for caution by grounding recommendations in rights. This tension is worth surfacing explicitly: genuine efficiency gains from AI must be weighed against legitimacy risks, and efficiency alone is not a sufficient justification for adoption.

## Key Insight

The report's core insight is institutional: courts are not ordinary organizations and AI governance in courts must be grounded in judicial legitimacy and rights-based principles rather than efficiency metrics, because AI failures in courts undermine not just individual fairness but systemic trust in the judiciary itself—requiring governance frameworks that make this implication visible and actionable at the institutional level.
