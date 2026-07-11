---
title: "Sales forecasting for retail stores using hybrid neural networks with sales-affecting variables"
authors: (see PLOS ONE, PMC, 2024)
year: 2024
venue: PLOS ONE (PMC)
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC12453866/
tier: 2 — Recommended (Scraping Run 1)
score: 8
angles: [SRQ1 — Retail forecasting]
srqs: [SRQ1]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
Hybrid CNN-LSTM neural networks incorporating sales-affecting exogenous variables (promotions, weather, holidays) achieve MAPE of 4.16% on retail store-level sales forecasting, substantially outperforming pure time-series approaches.

## Method
CNN-LSTM hybrid architecture on real retail store sales data (~3 years, weekly). Exogenous variables: promotional events, Danish-equivalent holidays, weather data, competitor pricing. Ablation study on variable contribution.

## Key finding
4.16% MAPE achieved with full feature set. Promotional variables account for the largest single accuracy improvement (~35% MAPE reduction). Hybrid CNN-LSTM outperforms pure LSTM by 12% and pure CNN by 18%.

## Relevance to thesis
- SRQ1: provides the state-of-the-art benchmark for the thesis to compare against — 4.16% MAPE is the aspirational ceiling (acknowledging deep learning is excluded from the thesis for RAM reasons)
- Ablation result (promotional variables matter most) validates the thesis feature engineering plan (promo_flag as a priority feature)
- Cite in Ch.6 as the external benchmark: "thesis ensemble achieves X% MAPE, vs. 4.16% reported by [citation] using unconstrained deep learning"

## Gap / limitation
CNN-LSTM requires significantly more RAM than any of the 5 thesis models — excluded from thesis on architectural grounds (not RAM-compatible). No confidence scoring or synthesis layer.
