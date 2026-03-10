---
title: "Gene name errors: Lessons not learned"
source: "https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008984"
publication: "PLOS Computational Biology"
date_read: "2026-03-10"
primary_domain: "Socio-technical Systems"
tags:
  - evidence
  - reproducibility
  - public-interest technology
  - evaluations
  - developer tooling
  - public administration
scholarly_signal: "cs.CY"
key_insight: "A decade of documented warnings and nomenclature reforms have not reduced the rate of spreadsheet-induced gene name corruption in published genomics research, demonstrating that knowledge dissemination alone cannot change entrenched data practices — only structural interventions at the software, journal, and training levels can."
---

# Paper Review

## Review

Abeysooriya et al. conduct a large-scale longitudinal audit of supplementary Excel files published in PubMed Central between 2014 and 2020, asking whether the well-publicised 2016 report on spreadsheet-induced gene name corruption had any lasting effect on researcher behaviour. The answer is unambiguous: it did not.

Screening 166,139 genomics articles and manually verifying 5,136 suspect files, the authors confirm gene name errors in 30.9% of publications containing supplementary Excel gene lists (3,436 of 11,117) — substantially above the 19.6% reported in 2016. The proportion of affected articles remained essentially flat across all seven years, ruling out any secular improvement. The elevated headline figure reflects both a wider sample (all of PMC rather than 18 selected journals) and an improved scanner that now detects five-digit internal date serial numbers, which account for roughly 15.7% of confirmed errors in the sampled subset.

The paper also identifies locale-dependent error modes — gene symbols misread as dates because of Italian, Spanish, Dutch, or Finnish month names — extending the known taxonomy of how spreadsheet internationalisation interacts with biological nomenclature. A counterintuitive finding is a statistically significant positive correlation between journal impact factor and error rate: Cell, Nature, PNAS, and EBioMedicine all exceed 40% affected. The most plausible explanation — unverified in this paper — is that high-impact journals require authors to deposit raw source data, inflating the surface area for errors rather than indicating lower scientific quality.

The central governance-relevant finding is that neither HGNC gene symbol reforms, nor open-source remediation tools (Truke, EscapeExcel, HGNChelper), nor prior publication of the problem have bent the error-rate curve. This generalises beyond genomics: it is a case study in the limits of awareness-based interventions for changing embedded data-handling practices. The paper's prescription — migrate to Python/R notebooks, use LibreOffice when spreadsheets are unavoidable, share genomic data as flat text — is technically sound but underestimates the structural barriers of training, legacy workflows, and journal submission conventions that make behaviour change slow even when intent is present.

For public-sector and research-infrastructure contexts, the implication is that mandating open data deposition without simultaneously mandating format standards and tooling support creates a reproducibility illusion: data are visible but silently corrupted. Journals, funders, and infrastructure operators bear co-responsibility alongside individual researchers.

## Key Insight

A decade of documented warnings and nomenclature reforms have not reduced the rate of spreadsheet-induced gene name corruption in published genomics research, demonstrating that knowledge dissemination alone cannot change entrenched data practices — only structural interventions at the software, journal, and training levels can.
