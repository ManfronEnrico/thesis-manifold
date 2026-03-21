---
title: "Evaluating and Calibrating Uncertainty Prediction in Regression Tasks"
authors: (see Sensors, MDPI, 2023)
year: 2023
venue: Sensors (MDPI)
url: https://www.mdpi.com/1424-8220/22/15/5540
tier: 2 — Recommended (Scraping Run 1)
score: 8
angles: [SRQ2 — Confidence scoring]
srqs: [SRQ2]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
A systematic evaluation of uncertainty calibration methods for regression tasks shows that isotonic regression calibration (Kuleshov et al., 2018) generalises best across model families, while temperature scaling and Platt scaling are effective for specific cases (neural networks and binary classification respectively).

## Method
Systematic comparison of 6 calibration methods (isotonic regression, temperature scaling, Platt scaling, beta calibration, histogram binning, ENCE minimisation) across 12 regression datasets and 5 model families (neural networks, GPs, tree ensembles, linear models, SVMs). Metric: Expected Normalised Calibration Error (ENCE).

## Key finding
Isotonic regression is the most consistently effective calibration method across all model families. Temperature scaling fails on tree ensembles. No single method dominates in all scenarios, but isotonic regression minimises average ENCE across the full benchmark.

## Relevance to thesis
- SRQ2: complements Kuleshov et al. (2018) — while Kuleshov proposes the method, this paper validates it as best practice across model types including tree ensembles (LightGBM, XGBoost used in thesis)
- Provides the empirical justification for using a single calibration method across all 5 thesis models
- Cite alongside Kuleshov in Ch.7 confidence scoring methodology

## Gap / limitation
Sensors application domain (IoT data) — not retail demand. No downstream decision quality evaluation. No multi-model ensemble calibration.
