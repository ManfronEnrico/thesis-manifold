---
title: "Demand Forecasting Methods and the Potential of ML in the FMCG Retail Industry"
authors: (see Springer Book Chapter, 2023)
year: 2023
venue: Springer Book Chapter
url: https://link.springer.com/chapter/10.1007/978-3-658-39072-3_8
tier: 2 — Recommended (Scraping Run 1)
score: 8
angles: [SRQ1 — Retail forecasting]
srqs: [SRQ1]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
Comprehensive review of demand forecasting methods applicable to FMCG retail, concluding that ML-based approaches (particularly gradient boosting) outperform classical statistical methods when feature-rich data is available, while classical methods remain competitive in sparse or intermittent demand scenarios.

## Method
Systematic literature review + empirical comparison of: ARIMA/ETS (statistical), Random Forest, XGBoost, LightGBM, LSTM (ML/DL). Evaluated on FMCG retail datasets across multiple product categories. Assessment criteria: MAPE, MAE, computational cost, interpretability.

## Key finding
No single method dominates across all product categories. Gradient boosting excels on regular-demand SKUs; ARIMA competitive on low-volume intermittent SKUs; ensemble approaches (averaging statistical + ML) most robust across categories.

## Relevance to thesis
- SRQ1: establishes the domain-specific model selection rationale — why ARIMA is included as a baseline (robust for low-volume SKUs) AND why LightGBM/XGBoost are the ML candidates
- Ch.2 literature review: provides the FMCG forecasting context and state-of-the-art benchmark
- Justifies the 5-model ensemble strategy: different models are optimal for different demand regimes

## Gap / limitation
Review context — no RAM/compute profiling. No multi-agent orchestration or consumer signal enrichment. No confidence scoring.
