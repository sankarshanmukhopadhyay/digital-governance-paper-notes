---
title: "Credential Disclosure in (EU) Digital Identity Wallets: Privacy Risks and Practical Mitigations"
source: "https://arxiv.org/abs/2606.06354"
publication: "arXiv"
date_read: "2026-09-16"
primary_domain: "Privacy & Data Protection"
tags: ["digital public infrastructure", "digital policy", "governance-by-design", "risk assessment", "authorization"]
scholarly_signal: "cs.CR"
key_insight: "Selective disclosure does not produce privacy by itself when the verifier can request excessive evidence and the holder must repeatedly judge whether disclosure is legitimate."
published: "2026-06-04"
doi: "10.48550/arXiv.2606.06354"
peer_review_status: "preprint"
paper_type: "preprint"
paper_version: "arXiv v1"
review_status: "current"
governance_facets: ["authority", "accountability"]
---

# Paper Review

## Review

Zingg and colleagues examine a governance problem often hidden by the cryptographic framing of digital identity wallets: even when a wallet can disclose credentials securely and selectively, users still have to decide whether a verifier is entitled to receive the requested evidence. Their large-scale study, reported as involving 1,035 users and 27 experts, finds consequential oversharing, including roughly one fifth of users disclosing official identification to news websites. Their Credential Assistant uses expert recommendations and user opinions to intervene at disclosure time, reducing reported disclosure mistakes from about 15 percent to about 7 percent.

The result changes where the privacy problem should be located. Wallet architectures commonly treat holder control as protection because the user approves disclosure. The study shows why consent at the interface cannot carry the full governance burden. A technically valid request can still be excessive, and a user's willingness to approve it does not establish the verifier's legitimate need for the credential. The residual error after assistance reinforces the point: better advice improves decisions but does not convert repeated individual judgment into enforceable data minimization.

The empirical design gives this argument operational weight by comparing user choices with expert judgments across credential and website scenarios. Its governance limit follows from the same design. "Appropriate" disclosure depends on contextual purpose, law, service requirements and institutional authority. An expert-derived recommendation can help a holder, but it cannot itself establish a verifier's entitlement. The study is also a simulated disclosure environment, and its reported user sample cannot by itself establish behaviour across the full and heterogeneous population that will encounter EUDI Wallet deployments.

For wallet governance, the next step is therefore not only a better warning layer. High-risk disclosures need request-side constraints: purpose and verifier authorization that can be evaluated by the wallet, enforceable minimization rules, auditable exceptions, and mechanisms for challenge and redress. The paper provides evidence that privacy cannot be delegated entirely to the person holding the wallet.

## Key Insight

Selective disclosure does not produce privacy by itself when the verifier can request excessive evidence and the holder must repeatedly judge whether disclosure is legitimate.
