---
title: "Who Owns AI When It Breaks? The Convergence of AI Governance and Cybersecurity Accountability"
source: "https://doi.org/10.61643/c79060"
publication: "The Pinnacle: A Journal by Scholar-Practitioners, 4(2)"
date_read: "2026-09-24"
primary_domain: "AI Governance"
tags: ["AI governance", "accountability", "cyber risk", "AI risk management", "agentic systems"]
key_insight: "AI accountability becomes executable only when each consequential decision has a named owner and each control function has preauthorized authority to intervene before failure."
published: "2026-09-17"
doi: "10.61643/c79060"
paper_type: "research-article"
review_status: "current"
governance_facets: ["accountability", "authority", "enforcement", "institutional-capacity", "revocation"]
---

# Paper Review

## Review

Montgomery and Copeland treat AI failure as an authority-design problem rather than merely a model-risk problem. Their central distinction is between system ownership, responsibility for maintaining an AI capability, and decision ownership, accountability for interpreting, acting on, challenging, containing, or stopping its outputs. The paper argues that enterprise AI governance should remain cross-functional while every consequential decision retains one accountable owner. It identifies three recurring failures: capability without authority, inclusion without operational integration, and detection without execution.

The paper's main contribution is the AI Decision Authority Charter, a use-case-specific governance instrument that assigns business, technical, security, legal, privacy, and executive decision rights before deployment. The model gives the CISO bounded, preauthorized stop-work authority for defined security conditions, including unauthorized access, data exposure, compromised retrieval or model integrity, excessive agency, credential abuse, and loss of traceability. Return to service remains a separate decision requiring business authorization, technical readiness, and security concurrence. This separation between containment authority and final business disposition is institutionally important because it converts shared governance from committee participation into executable control.

The paper also challenges human-in-the-loop oversight when the human lacks evidence, time, an alternative path, or genuine authority to reject the system. Its escalation model therefore ties observable triggers to named decision owners, response deadlines, containment actions, and executive adjudication. For agentic AI, the argument becomes sharper: authority granted to an agent must be matched by the organization's capacity to observe, restrict, revoke, and recover from that authority.

The framework is operationally useful, but its evidence base is primarily synthesis, standards alignment, and illustrative cases rather than validation of the Charter in live organizations. Robodebt and SyRI demonstrate the consequences of diffuse authority, but they do not establish that singular decision ownership or bounded CISO authority will resolve cross-domain conflicts in practice. The next step should be implementation evidence: tabletop exercises, incident simulations, measurable intervention latency, tested revocation paths, and comparative results across organizations with different regulatory and operating models.

## Key Insight

AI accountability becomes executable only when each consequential decision has a named owner and each control function has preauthorized authority to intervene before failure.
