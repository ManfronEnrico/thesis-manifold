---
title: "DSS4EX: A Decision Support System framework to explore Artificial Intelligence pipelines with an application in time series forecasting"
authors: [Carmona-Blanco, David, et al.]
year: 2025
venue: Expert Systems with Applications, Vol. 272, Article 125721
url: https://www.sciencedirect.com/science/article/pii/S0957417425000430
tier: 2 — High Relevance
score: 7
srqs: [SRQ4]
---

## Core argument
DSS4EX proposes a modular decision support system (DSS) framework that wraps AI forecasting pipelines — including classical time-series models and deep learning approaches — in an interactive, explainable interface. The paper argues that the gap between raw AI/ML forecasting outputs and actionable managerial decisions requires a structured DSS layer that makes model comparisons, uncertainty estimates, and feature contributions interpretable to non-expert users. DSS4EX positions explainability and pipeline exploration (comparing multiple models interactively) as first-class design requirements.

## Method
A prototype DSS is implemented using a time-series forecasting application on real business data; the framework supports pipeline composition (data preprocessing, model selection, hyperparameter tuning), model comparison dashboards, and SHAP-based explainability outputs. User evaluation is conducted with domain experts to assess usability and decision quality improvement.

## Key finding
DSS4EX users achieved statistically significantly better decision quality scores compared to users relying on raw model outputs alone, and reported substantially higher confidence in their forecasting-based decisions; explainability features (SHAP visualisations) were identified as the most valued component.

## Key quote
> "DSS4EX bridges the gap between AI pipeline outputs and managerial decision-making by providing an interactive, explainable layer that makes model comparisons and uncertainty estimates accessible to business users."

## Relevance to thesis
- [SRQ4]: Directly addresses the thesis's central SRQ4 comparison — DSS4EX explicitly contrasts AI-augmented decision support against unaugmented (descriptive) analytics, providing both a methodological template and empirical evidence for the value of moving from descriptive to predictive BI.
- [SRQ4]: The explainability-first design philosophy aligns with the thesis framework's requirement that the Synthesis Agent produce confidence-scored, natural-language recommendations interpretable by Manifold's analyst clients.
- [SRQ2]: The pipeline composition and model comparison modules are structurally analogous to the thesis's multi-agent architecture where the Forecasting Agent benchmarks multiple models and the Synthesis Agent selects and integrates outputs.

## Gap / limitation
DSS4EX is a monolithic application framework rather than a multi-agent system — there is no LLM orchestration, no agent-based coordination, and no treatment of RAM or computational constraints. The paper does not address FMCG retail specifically, and its explainability approach (SHAP) is model-agnostic but not integrated with natural-language generation. The multi-agent synthesis of heterogeneous model outputs into a single recommendation — a core thesis contribution — is absent.
