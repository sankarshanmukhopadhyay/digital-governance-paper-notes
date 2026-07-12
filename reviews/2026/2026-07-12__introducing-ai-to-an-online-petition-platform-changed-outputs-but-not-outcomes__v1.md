---
title: "Introducing AI to an Online Petition Platform Changed Outputs but not Outcomes"
source: "https://arxiv.org/abs/2511.13949"
source_url: "https://arxiv.org/abs/2511.13949"
publication: "arXiv"
date: "2026-02-16"
date_read: "2026-07-12"
issue_url: "https://github.com/sankarshanmukhopadhyay/digital-governance-paper-notes/issues/56"
primary_domain: "Platform Governance & Internet Governance"
domain: "Platform Governance & Internet Governance"
tags:
  - generative AI
  - AI adoption
  - digital policy
  - governance-by-design
  - legitimacy
  - public-interest technology
  - transparency and accountability
  - inclusion, rights & development
scholarly_signal: "cs.CY"
key_insight: "Embedding generative AI into a civic platform did not merely assist users with prose. It standardized the language of participation while leaving participation and petition effectiveness unimproved, showing that interface defaults can centralize expressive power without producing corresponding public value."
---

# Paper Review

## Review

Introducing AI to an Online Petition Platform Changed Outputs but not Outcomes examines the 2023 integration of an AI drafting tool into Change.org. Using 1.5 million petitions and a staggered geographic rollout, the authors estimate the causal effect of access to the tool. Petitions became longer, more lexically varied, more complex, and more similar to one another. Human raters also judged a sample of post-launch petitions to be better written and more persuasive. Yet petition production did not increase, comment engagement did not improve, and the likelihood of reaching ten signatures declined. The platform changed the visible form of civic expression without demonstrating a corresponding improvement in civic mobilization.

This result matters because the AI feature is not simply a writing aid. Once embedded in the petition-creation flow, it becomes an institutional interface that mediates who speaks, how claims are framed, and what a legitimate public appeal is expected to sound like. A shared model, backend prompt, and default workflow exercise editorial power at scale. The platform is therefore not only lowering the cost of producing text. It is redistributing expressive decision rights from petition writers toward the platform operator and its model provider.

The paper provides unusually credible evidence for that shift. Its difference-in-differences design exploits a ten-week period in which the United States, Great Britain, and Canada had full access while Australia did not. The authors test parallel trends, run placebo and synthetic-control analyses, examine alternative outcome thresholds, and confirm the main pattern among repeat petition writers. This is materially stronger than studies that infer AI use from generic detectors or self-report. The estimates show a 45 percent increase in median petition length, a 19 percent increase in grade level, and a 9 percent increase in semantic similarity. The negative result is equally important: stylistic improvement did not translate into more signatures or comments.

The governance implication is not that better writing is useless. It is that civic efficacy is relational rather than lexical. Petitions succeed through specificity, organizer commitment, community recognition, circulation, and the willingness of others to treat the claim as authentic. AI can reproduce the surface characteristics of historically successful petitions while weakening the scarcity value of those characteristics. Once polished prose becomes cheap and ubiquitous, polish ceases to signal effort, knowledge, or commitment. The paper captures this transition in its finding that writing quality and persuasiveness became weaker, and sometimes negative, predictors of outcomes after AI access.

Homogenization should be read as a legitimacy problem, not merely a diversity metric. A civic platform depends on signals that a petition originates in a particular experience, constituency, and demand. When the platform channels many users through the same model and prompt, local vocabulary, dialect, urgency, and issue-specific detail can be replaced by a generic administrative register. The observed rise of terms such as “implement” and “establish,” alongside reduced title concreteness and a shift toward American English, indicates that the system is defining a preferred grammar of public participation. That can make petitions look institutionally polished while making the people and communities behind them less legible.

The paper is appropriately cautious about mechanism. It proposes three explanations for the absence of improved outcomes: weak substantive improvement, reader suspicion of AI, and reduced author ownership or effort. The third is institutionally consequential because petition success depends heavily on off-platform promotion. If automatic drafting reduces the cognitive and emotional investment required to formulate a claim, authors may be less likely to circulate, defend, and sustain it. The study cannot test this because it lacks sharing, editing, promotion, and author-perception data. The mechanism therefore remains plausible rather than established.

The treatment is access to AI, not verified use, which limits individual-level interpretation. The authors build a high-performing classifier and estimate substantial uptake, but exposure, use, and degree of reliance remain distinct. A user who lightly edits a suggestion is grouped with one who publishes a near-complete generated draft. Future evaluation should capture prompt inputs, draft provenance, edit distance, revision time, author choice, and whether a human-only route was available. These are not incidental product analytics. They identify where control moved and whether meaningful authorship was preserved.

The outcome model also remains narrow. Ten signatures and one comment are defensible indicators that a petition got off the ground, but they are not measures of political effect. They do not establish whether a petition reached a decision-maker, shaped media coverage, built an organization, changed policy, or produced a declared victory. Nor do they isolate other platform controls such as ranking, recommendation, notifications, paid promotion, moderation, or home-page placement. The paper demonstrates that AI did not improve the selected engagement metrics. It cannot establish that AI had no effect on civic outcomes in the wider institutional sense.

A further gap concerns the platform operator's incentives. The paper notes that Change.org deepened AI integration even though the observed launch did not increase participation or effectiveness. By early 2026, some users were routed from the home page directly into an AI-assisted creation flow without an equivalent human-only path. That product decision deserves explicit governance scrutiny. A platform may value faster onboarding, standardized content, lower support costs, data capture, or strategic alignment with AI investment even when users gain no measurable civic benefit. The divergence between platform value and public value is central to the case.

Operational governance should therefore move beyond generic transparency notices. Civic platforms that introduce generative AI should define measurable public-interest objectives before deployment, preserve an accessible human-only path, document the model and prompt changes that can alter public expression, and evaluate effects on specificity, linguistic diversity, author ownership, distribution, and real-world petition outcomes. Rollouts should include independent audits, time-bounded review points, and rollback criteria. Users need visibility into how much text was generated, meaningful control over revision, and a way to contest or report distortions. A feature that changes the language of civic participation without improving civic efficacy should not become the default merely because it makes content production faster.

The paper's broader contribution is to separate output quality from institutional performance. Generative AI can make each artifact appear more competent while making the platform as a whole more uniform and no more effective. That distinction should shape AI procurement and deployment far beyond petition sites. Public-facing systems should not treat improved fluency as evidence of improved service, inclusion, legitimacy, or outcomes. When AI is embedded into an interface, the relevant question is not whether it produces better text. It is whether the new allocation of control produces demonstrable public value without eroding authenticity, pluralism, and user agency.

## Key Insight

Embedding generative AI into a civic platform did not merely assist users with prose. It standardized the language of participation while leaving participation and petition effectiveness unimproved, showing that interface defaults can centralize expressive power without producing corresponding public value.
