---
title: "Applying ML in Retail Demand Prediction — Tree Ensembles vs LSTM"
authors: (see Applied Sciences, MDPI, 2024)
year: 2024
venue: Applied Sciences (MDPI)
url: https://www.mdpi.com/2076-3417/13/19/11112
tier: 2 — Recommended (Scraping Run 1)
score: 8
angles: [SRQ1 — Retail forecasting]
srqs: [SRQ1]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
A direct comparative benchmark of gradient boosting tree ensembles vs. LSTM neural networks for retail demand forecasting shows that tree ensembles consistently match or outperform LSTM on real retail data, while requiring substantially less compute and being easier to interpret.

## Method
Empirical benchmark on real retail dataset: LightGBM, XGBoost, Random Forest vs. LSTM and GRU. Evaluation: MAPE, MAE, RMSE. Feature engineering includes lag features, rolling windows, calendar, and promotional indicators. HPO via grid search.

## Key finding
LightGBM achieves lowest average MAPE across all SKU categories tested. LSTM competitive only on high-volume, low-volatility SKUs. Tree ensembles train 10–50× faster and require ~5× less memory than equivalent LSTM models.

## Relevance to thesis
- SRQ1: directly justifies the thesis model selection — tree ensembles (LightGBM, XGBoost) over deep learning within RAM and compute constraints
- Provides the "apples-to-apples" benchmark citation: why LSTM is excluded from the 5-model ensemble
- Citable for SRQ1 model selection justification in Ch.6

## Gap / limitation
Single retail context. No RAM profiling reported (only training time). No consumer signal enrichment. No confidence scoring or recommendation output.
