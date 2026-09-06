---
title: "Innovative machine learning approaches for complexity in economic forecasting and SME growth: A comprehensive review"
authors: [Nguyen, Thi Thanh Huyen, et al.]
year: 2025
venue: International Journal of Innovation Studies, Vol. 9, No. 1
url: https://www.sciencedirect.com/science/article/pii/S2949948825000010
tier: 2 — High Relevance
score: 7
srqs: [SRQ1]
---

## Core argument
This comprehensive review surveys machine learning approaches applied to economic forecasting in resource-constrained business environments, with a focus on SME growth prediction. The paper argues that traditional econometric methods are insufficient for capturing the non-linear, high-dimensional complexity of modern economic signals, and systematically evaluates the performance and computational cost trade-offs of gradient boosting methods, neural networks, hybrid models, and ensemble approaches across forecasting horizons and data regimes.

## Method
A systematic literature review methodology covers 120+ papers on ML-based economic forecasting published between 2015 and 2024. Papers are categorised by model type, forecasting horizon, data volume, evaluation metric, and computational requirements. Findings are synthesised into a comparative table of accuracy vs computational cost across model families.

## Key finding
Gradient boosting methods (LightGBM, XGBoost) consistently deliver the best accuracy-to-computational-cost ratio across short-to-medium forecasting horizons (1–12 months) in economic contexts, outperforming deep learning approaches when training data is limited (fewer than 500 observations) — a condition directly relevant to monthly retail scanner data with ~36 periods.

## Key quote
> "For SME-scale economic forecasting with limited historical data, gradient boosting methods offer the optimal balance between predictive accuracy and computational efficiency, consistently outperforming both classical econometric models and deep learning architectures."

## Relevance to thesis
- [SRQ1]: The review directly supports the thesis's model selection rationale for Phase 4 — the finding that LightGBM/XGBoost dominates under limited training data and moderate computational budgets justifies their inclusion in the benchmark alongside ARIMA and Prophet.
- [SRQ1]: The paper's treatment of forecasting accuracy vs computational cost as a dual evaluation criterion provides academic grounding for the thesis's RAM-profiling requirement in the model benchmark.

## Gap / limitation
The review is aggregated across diverse economic contexts (GDP growth, credit risk, commodity prices) rather than FMCG retail scanner data specifically. There is no treatment of multi-agent orchestration, LLM synthesis of forecasts, or consumer survey data enrichment (SRQ3). The paper does not address the 8GB RAM constraint or cloud deployment architecture, and does not evaluate models within an end-to-end decision-support pipeline.
