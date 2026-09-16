---
title: "People Are Not Just Their Countries. Disentangling Social Determinants of LLM Value Alignment Across Europe"
source: "https://arxiv.org/abs/2608.07367"
publication: "arXiv; accepted at AIES 2026"
date_read: "2026-09-16"
primary_domain: "Socio-technical Systems"
tags: ["behavioral alignment", "fairness and bias", "legitimacy", "LLMs"]
scholarly_signal: "cs.AI"
key_insight: "Measuring which populations an LLM resembles is evidence about representational distribution, not a mandate for whose values the system should implement; moving from country averages to demographic granularity makes the legitimacy of the alignment target more, not less, important."
published: "2026-08-07"
peer_review_status: "accepted"
paper_type: "conference paper"
paper_version: "v1"
review_status: "current"
---

# Paper Review

## Review

This paper challenges a common unit of analysis in LLM value-alignment research: the country. Using Wave 11 of the European Social Survey, the authors compare 10 commercial LLMs with 50,116 respondents across 29 European countries and Israel. They analyze 47 value- and opinion-related questions, including a 21-item Portrait Values Questionnaire subset, and examine alignment against 15 socio-demographic variables as well as country of residence. Model calls are repeated and aggregated, while individual-level analyses use linear and gradient-boosted models; inverse-propensity weighting is used to test whether national differences can be explained by measured demographic composition.

The central empirical result is that country remains informative but is not sufficient. Education, income, occupation and religion show substantial alignment differences, and country-level and socio-demographic factors contribute complementary explanatory power. The relative importance also changes with the question set: broad opinion questions preserve more geographic signal than the narrower PVQ subset. This is an important correction to governance narratives that treat national averages as adequate proxies for populations.

The deeper governance issue is that representational measurement and legitimate alignment are different problems. The paper can identify which groups are closer to model outputs, but empirical similarity cannot determine whose values a general-purpose system ought to privilege. A country average embeds an aggregation rule; a demographic slice embeds classification choices; an individual alignment target raises questions about personalization, inference and unequal treatment. Increasing granularity therefore does not remove the political choice. It relocates it into the selection of groups, survey questions, weighting rules and deployment objectives.

Several limits appropriately bound interpretation. All prompts are in English, Likert-style survey responses are imperfect proxies for values, majority aggregation suppresses some model-output variability, and observed socio-demographic categories cannot exhaust the identities or contexts that shape opinion. The analysis is European and should not be generalized to other populations without evidence. Nor does lower measured alignment itself establish harm. Harm depends on what the system is doing, whose interests are affected and whether outputs exercise consequential authority.

For governance practice, the paper suggests that alignment evaluation should publish its reference population, aggregation and weighting rules, question-selection rationale, uncertainty, subgroup disparities and intended decision context. Where alignment metrics influence deployment or tuning, institutions also need a contestable process for deciding which differences warrant intervention. The key shift is from asking whether a model is "aligned with Europe" to asking who defined the represented public, for what purpose, under what authority, and with what recourse for those systematically distant from the chosen target.

## Key Insight

Measuring which populations an LLM resembles is evidence about representational distribution, not a mandate for whose values the system should implement; moving from country averages to demographic granularity makes the legitimacy of the alignment target more, not less, important.
