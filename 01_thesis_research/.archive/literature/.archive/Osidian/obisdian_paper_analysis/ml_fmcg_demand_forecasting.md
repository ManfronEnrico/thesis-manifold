---
title: "Machine Learning-Based Demand Forecasting for an FMCG Retailer"
authors: (see Springer LNCS 2024)
year: 2024
venue: Springer LNCS (Lecture Notes in Computer Science)
url: https://link.springer.com/chapter/10.1007/978-3-031-67192-0_11
tier: 2 — Recommended (Scraping Run 1)
score: 9
angles: [SRQ1 — Retail forecasting]
srqs: [SRQ1, SRQ4]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
Applying ML forecasting (gradient boosting, neural networks) to a real FMCG retailer's demand data consistently outperforms classical statistical baselines (ARIMA, exponential smoothing) across SKU categories, establishing ML-based forecasting as operationally viable in retail CPG contexts.

## Method
Real FMCG retailer dataset: multiple product categories, weekly sales data. Benchmark comparison: ARIMA, ETS vs. LightGBM, XGBoost, LSTM. Evaluation metrics: MAPE, RMSE, MAE. Feature engineering includes promotional flags, seasonal indicators, price variables.

## Key finding
LightGBM achieves best overall performance across categories, with 15–25% MAPE reduction over ARIMA baselines. Neural network models (LSTM) competitive on high-volume SKUs but less robust on low-volume/intermittent demand.

## Relevance to thesis
- **SRQ1 primary domain reference**: closest match to thesis empirical context (FMCG retailer, real operational data, same model family)
- Validates the thesis model selection (LightGBM, XGBoost as primary ML candidates, ARIMA as baseline)
- SRQ4: provides magnitude benchmark — thesis should aim to demonstrate comparable or better gains over descriptive BI baselines
- Justifies the 5-model ensemble approach (no single model dominates across all SKU types)

## Gap / limitation
Single-retailer context. No multi-agent orchestration. No RAM/compute constraints reported. Consumer signal enrichment not attempted. No confidence scoring or recommendation output — purely predictive accuracy focus.
