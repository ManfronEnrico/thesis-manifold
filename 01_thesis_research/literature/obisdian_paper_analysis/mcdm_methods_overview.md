---
title: "Overview of Existing Multi-Criteria Decision-Making (MCDM) Methods Used in Industrial Environments"
authors: [Pelissari, Renata, et al.]
year: 2025
venue: Technologies (MDPI), Vol. 13, No. 10, Article 444
url: https://www.mdpi.com/2227-7080/13/10/444
tier: 2 — High Relevance
score: 7
srqs: [SRQ2]
---

## Core argument
This review paper systematically surveys MCDM methods applied in industrial settings, cataloguing techniques such as AHP (Analytic Hierarchy Process), TOPSIS, VIKOR, PROMETHEE, and ELECTRE across manufacturing, supply chain, and operations management domains. The paper argues that MCDM is underutilised as a synthesis layer in AI-augmented decision systems, and that selecting the right MCDM method requires matching its properties (compensatory vs non-compensatory, cardinal vs ordinal) to the decision context and the nature of the criteria being aggregated.

## Method
A structured literature review methodology is applied, systematically searching and categorising papers using MCDM methods in industrial contexts. Papers are classified by method type, application domain, number of criteria, and decision context, yielding a taxonomy of MCDM usage patterns.

## Key finding
AHP and TOPSIS together account for over 60% of MCDM applications in industrial environments; hybrid MCDM-ML combinations are an emerging trend, particularly for supplier selection and quality control, but remain rare in analytics and forecasting synthesis contexts.

## Key quote
> "The choice of MCDM method should be driven by the nature of the decision problem, the type and number of criteria, and the acceptable level of compensatory trade-offs — a selection that remains ad hoc in most industrial applications."

## Relevance to thesis
- [SRQ2]: Directly informs the Synthesis Agent design — the thesis framework must aggregate multiple forecasting model outputs (ARIMA, Prophet, LightGBM) using a principled multi-criteria synthesis layer, and this paper provides the methodological vocabulary and selection criteria for choosing between AHP, TOPSIS, or VIKOR as the aggregation mechanism.
- [SRQ2]: The hybrid MCDM-ML trend identified in the review validates the thesis's architectural choice to combine ML forecasting with a structured decision synthesis layer rather than relying on a single model output.

## Gap / limitation
The review does not address MCDM integration with LLM orchestrators or multi-agent AI systems — all reviewed applications involve human decision-makers applying MCDM manually or with classical DSS tools. There is no treatment of automated, LLM-driven criteria weighting, no FMCG retail context, and no evaluation of MCDM methods under computational resource constraints. The synthesis of probabilistic ML outputs into MCDM criteria remains unaddressed.
