---
title: "Agentic Substrate: What an AI System Must Provide to Execute Autonomous Tasks Under Governance Constraints"
source: "https://nonsequitur.tech/white-papers/agentic-substrate/"
publication: "Justin H. Kuiper, Non Sequitur Publishing (2026); v1.0-preprint, cover revised 2026-09-15"
date_read: "2026-11-24"
primary_domain: "AI Governance"
tags: ["AI agents", "authorization", "delegated authority", "deployment controls", "assurance", "context engineering"]
key_insight: "An agentic substrate can bound the operations an agent invokes without bounding the consequences those operations produce; a defensible blast-radius contract must govern cumulative exposure, continuing authority and downstream effects beyond the originating execution."
doi: "10.5281/zenodo.19869291"
peer_review_status: "preprint"
paper_type: "preprint"
paper_version: "v1.0-preprint"
review_status: "current"
governance_facets: ["authority", "delegation", "enforcement", "auditability", "dependency"]
---

# Paper Review

## Review

Kuiper's contribution is to locate the enforceability of agent governance in the infrastructure mediating execution rather than in an agent's willingness to comply. Section 6.1 translates the Skipjack Protocol into five substrate contracts: unavoidable admission interception, independently captured execution evidence, context manifest continuity, scoped credentials and structural partition isolation. These contracts provide useful criteria for selecting or composing agent runtimes. The supplied v1.0-preprint identifies the DOI above as its original publication and states that its September 15 cover revision leaves the manuscript unchanged. Issue #140 records a different Zenodo DOI, 10.5281/zenodo.22771316; the relationship between those deposits and the original publication date could not be independently verified. This review concerns the supplied manuscript.

The design synthesis is particularly useful where Section 2 treats memory, reasoning and tool access as governance surfaces. Episodic memory distinguishes operator-ratified positions from inference and tool-derived information; semantic memory associates operative knowledge with acknowledged policy versions. Section 2.3 requires renewed admission for material changes to a plan and prevents self-correction from redefining its mandate. Section 4 complements this with refusal paths outside the executor's discretion and substrate-observed evidence rather than relying on the agent's account of compliance. The reported four-pool K3s deployment illustrates feasibility, but the paper explicitly defers comparative evaluation and formal interface verification. It establishes architectural requirements, not independently demonstrated conformance.

The decisive claim is the blast-radius contract in Section 5.6. Its proposed bound comprises the capabilities admitted by an envelope within the credential lifetime. Process isolation, capability tokens, sandboxing and credential mediation are appropriate mechanisms for limiting operational reach. They do not establish a maximum consequential harm without a model of effects beyond that reach. An authorized disclosure may be irreversible; an authorized external transaction may create an obligation that persists after credentials expire; a queued operation may execute after its originating task closes. Concurrent or repeated individually permitted operations may exhaust an aggregate budget that no per-call scope check represents. These are counterexamples to interpreting a capability inventory as a harm bound, not observations of failures in the reported deployment.

The strongest defence is that the author describes the theorem as a contract rather than an empirical claim, expressly excludes some underlying infrastructure failures and recognizes compositional harm. That is appropriate scope discipline. However, it leaves the operational contract incomplete on its own terms: bounding the set of invocations does not establish the consequences reachable through them. Quantitative or qualitative effect limits, downstream execution assumptions, cumulative exposure and explicit residual risks would be needed before an operator could responsibly authorize against the proposed bound.

Continuing authority is another necessary condition. Section 7, vector 5 explicitly leaves early token revocation, propagation latency and recovery open. The per-action checks and immutable manifests are useful, but checking an unchanged envelope does not determine whether the mandate it represents remains effective. Withdrawal of delegation, conflicting policy versions and delayed execution require fresh applicability checks at the point of commitment. Token expiry at task completion cannot substitute for this property.

Section 3 identifies authority implications of orchestration topology, yet logical role separation should not be equated with institutional independence. A single executor can be subject to an independent policy enforcement point; several role-typed executors may share one controlling administrator. Distributed execution need not imply peer authorization by consensus. Centralized orchestration is a defensible design default within Skipjack, not a universal governance requirement. Its concentration of admission, routing and evidence control makes administrative independence a separate assessment question.

The same qualification applies to evidence and hosting. Section 4.3 usefully separates substrate-witnessed records from agent self-reporting, but a checksum and append-only channel do not establish completeness or independent replay when the substrate controls observation and storage. Section 4.7's local open-source deployment increases inspectability and control in the described environment; it does not prove that remote inference cannot be separated from a locally governed execution boundary. The relevant property is the enforceable trust boundary, not hosting location alone.

Compared with the archive's *Authority Continuity Across Agentic Trajectories*, Kuiper supplies candidate enforcement locations for reassessing authority before action. *Governance Laundering* supplies a complementary test for independently reconstructable authorization evidence, and *Swarms of Agentic AI* locates containment in reachable states rather than predictable behaviour. The present paper's contribution is the integration of runtime security primitives into agent governance contracts, not a new security theorem.

Adopt the five contracts as substrate selection and design requirements. Do not treat the reported deployment, the evidence-channel schema or the isolation inventory as proof of conformance or a maximum harm bound. A bounded conformance suite testing mid-execution revocation, cumulative scope violations, delayed external commitments and independently reconstructable authorization decisions would materially change the assessment. Until then, the blast-radius contract is credible as an operational reach constraint under declared assumptions, not as an established bound on consequential harm.

## Key Insight

An agentic substrate can bound the operations an agent invokes without bounding the consequences those operations produce; a defensible blast-radius contract must govern cumulative exposure, continuing authority and downstream effects beyond the originating execution.
