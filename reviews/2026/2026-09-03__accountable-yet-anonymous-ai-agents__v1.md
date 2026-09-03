---
title: "Accountable yet Anonymous AI Agents: Split-Knowledge Binding in China’s National Agent-Identity Layer"
source: "https://arxiv.org/abs/2607.23207"
publication: "arXiv preprint (v1)"
date_read: "2026-09-03"
primary_domain: "Digital Identity"
tags: ["AI agents", "accountability", "authority", "governance-by-design", "trust assurance"]
scholarly_signal: "cs.CY"
key_insight: "Split-knowledge identity can make an agent traceable without making its principal visible to business actors, but traceability becomes legitimate accountability only when tracing, revocation, delegated authority, and redress are independently governable."
---

# Paper Review

## Review

He, Shan, Luo, and Wang describe a pre-launch Chinese national identity layer for AI agents that separates association from disclosure. MPS retains the mapping from a pairwise reference to verified identity, while SIC retains the reference-to-agent linkage. Applications receive proof that an agent is bound to a verified principal without learning who that principal is. Re-identification requires a legal authority to compel both institutions separately. The authors correctly characterize this as institutional split knowledge rather than cryptographic threshold anonymity and explicitly acknowledge that a coordinated state can reconstruct identity.

The paper's durable design contribution is the "accountability surface": deployments choose which calls or messages leave attributable evidence, making attribution granularity and the point at which revocation takes effect explicit infrastructure decisions. Its threat model also treats state over-reach, straw principals, cross-agent profiling, harmed counterparties, biometric exclusion, and registry-level revocation as governance risks rather than peripheral security concerns. The architecture therefore moves beyond a simple identity credential by specifying how action-to-agent evidence and agent-to-principal tracing can be composed after harm.

The unresolved issue is that identity attribution is not authority. A retained presentation plus an agent-to-principal trace can establish which bound agent produced an action, but cannot establish that the principal authorized that specific action, that the delegation remained valid, or that the agent acted inside its permitted scope. The paper itself concedes that a definite bound principal need not be the responsible party in straw-principal cases. That concession prevents a simplistic identity-equals-liability reading, but it leaves a broader architectural gap: governance-grade accountability needs a chain from principal through current delegation and action-specific authority to the agent act and surviving evidence.

The same distinction applies institutionally. Business actors are structurally denied principal identity, but tracing and pseudonymous revocation remain state powers gated mainly by procedure. The paper openly leaves subject notification, unified end-to-end audit, parts of blocklisting governance, and revocation appeal unresolved. Since its proportionality framework says escrow is defensible only where institutional oversight credibly constrains those powers, post-launch evidence about rejected tracing requests, revocation review, restoration, biometric failure, disputed bindings, and service-gateway dependence will matter as much as adoption counts.

The paper therefore makes a useful intervention against the assumption that accountable agents must be continuously identifiable to platforms and counterparties. Its deeper governance proposition is more precise: privacy can be improved by redistributing who is allowed to resolve identity, but legitimate accountability still depends on separately governing authority, tracing, revocation, evidence, and redress.

## Key Insight

Split-knowledge identity can make an agent traceable without making its principal visible to business actors, but traceability becomes legitimate accountability only when tracing, revocation, delegated authority, and redress are independently governable.
