---
title: "A machine learning approach to consumer behavior in supermarket analytics"
authors: (see Computers & Industrial Engineering, ScienceDirect, 2025)
year: 2025
venue: Computers & Industrial Engineering (ScienceDirect)
url: https://www.sciencedirect.com/science/article/pii/S2772662225000566
tier: 2 — Recommended (Scraping Run 1)
score: 8
angles: [SRQ3 — Consumer signals]
srqs: [SRQ3]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
ML analysis of consumer purchasing behaviour in supermarket transaction data reveals that consumer segment characteristics (demographics, lifestyle, basket composition) are predictive of product-level demand patterns, supporting consumer-enriched demand forecasting.

## Method
Transaction-level supermarket data + consumer demographic data. Clustering (k-means) to derive consumer segments. ML classification and regression to predict purchase propensity and basket size per segment. Evaluated on loyalty card data across 4 supermarket chains.

## Key finding
Consumer segment membership improves demand prediction accuracy by 8–14% (MAPE reduction) compared to transaction-only models. Segment-level demand indices are more stable predictors than individual transaction histories.

## Relevance to thesis
- SRQ3: directly supports the Indeks Danmark integration design — consumer segments derived from survey data are predictive of retail demand
- Provides methodological precedent for PCA + k-means → consumer segment → demand index pipeline
- Validates the retailer-level segment mapping approach used in the thesis

## Gap / limitation
Uses loyalty card transaction data (richer than survey data). Does not address multi-agent orchestration, RAM constraints, or confidence scoring. Supermarket analytics context differs from the thesis's CSD-specific panel data.
