---
title: "Building a National Digital Trust Architecture for India: From Digital Identity and Data Exchange to Federated Institutional Trust"
source: "https://doi.org/10.5281/zenodo.22840405"
publication: "Zenodo"
date_read: "2026-09-26"
primary_domain: "Trust Infrastructure"
tags: ["trust registries", "trust assurance", "authority", "authorization", "digital public infrastructure", "India"]
key_insight: "The paper's central contribution is to separate technical verification from institutional reliance and make trust an explicit governance decision over issuer authority, purpose, status, relying-party authority, liability, and redress."
published: "2026-09-19"
doi: "10.5281/zenodo.22840405"
peer_review_status: "working-paper"
paper_type: "working-paper"
paper_version: "Final Version, September 2026"
review_status: "current"
governance_facets: ["authority", "accountability", "redress", "revocation"]
---

# Paper Review

## Review

Nair proposes a national trust layer for India that sits above existing identity, credential and data-exchange systems rather than replacing them. The paper's most important move is conceptual: it separates identity, credential, assertion, trust and authorisation, then treats successful cryptographic verification as necessary but insufficient for institutional reliance. A relying institution must also determine whether the issuer was authorised to make the assertion, whether the assertion remains valid, whether the intended purpose is permitted, whether the relying institution itself has authority to act, and where liability sits if the assertion is wrong.

The proposed six-layer architecture operationalises that distinction through institutional assertions, a federated Trust Exchange, a Trusted Issuer Registry and a governance layer spanning purpose limitation, auditability, liability, redress, privacy and security. The registry is deliberately conceived as a federation of existing sector directories rather than a new national source of personal data. That design preserves sectoral authority while creating a common trust query surface. The explicit Trust Decision is the paper's strongest governance mechanism because it records not only provenance and status but also purpose, relying-party authority and responsibility before a service action occurs.

The paper is careful about concentration risk. It proposes sector-signed registry entries, public change logs, appeal rights for suspension, last-known-good operation during outages, holder-mediated presentation by default, no universal identifier, and correction paths with interim protection against wrongful denial. These controls make legitimacy, revocation and redress part of the infrastructure rather than post-hoc policy language.

The limits are equally clear. The architecture is conceptual and unimplemented. It does not yet establish the legal instrument, registry operator, cross-sector liability doctrine, cost model, formal security model or evidence that reuse will improve fraud, cost or processing outcomes. Its safe-harbour proposal for relying institutions requires explicit legal authority, and the interaction between sectoral regimes and the Digital Personal Data Protection framework remains unresolved. The implementation plan appropriately treats these as pilot questions rather than presumed benefits.

For practitioners, the durable contribution is a governance model in which trust is neither a signature nor a credential property. It is a recorded institutional decision grounded in authority, scope, purpose, current status and accountable reliance.

## Key Insight

The paper's central contribution is to separate technical verification from institutional reliance and make trust an explicit governance decision over issuer authority, purpose, status, relying-party authority, liability, and redress.
