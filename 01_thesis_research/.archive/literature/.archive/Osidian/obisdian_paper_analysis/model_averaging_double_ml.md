---
title: "Model Averaging and Double Machine Learning"
authors: Achim Ahrens, Christian B. Hansen, Mark E. Schaffer, Thomas Wiemann
year: 2024
venue: Journal of Applied Econometrics (Wiley), published online 2024; print 2025, 40(3), 249–269
url: https://arxiv.org/abs/2401.01645
tier: 2 — Recommended (Scraping Run 2)
score: 8
angles: SRQ1, Ensemble Methods, Econometric ML, Uncertainty Quantification
srqs: [SRQ1, SRQ3]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
Pairing double/debiased machine learning (DDML) with stacking — a model-averaging method that combines multiple candidate learners — yields more robust causal effect estimates than single-learner DDML, because stacking adapts the ensemble weights to the local data-generating process without imposing a priori model assumptions.

## Method
Theoretical extension of Robinson (1988) and Chernozhukov et al. (2018) DDML. Proposes two stacking variants: short-stacking (exploits cross-fitting folds to reduce computational burden) and pooled stacking (common weights across folds). Validated via calibrated Monte Carlo simulations and two empirical applications (gender citation gap and wage equations). Stata and R implementations provided.

## Key finding
DDML with stacking reduces median absolute error in treatment effect estimation by 18–32% relative to single-learner DDML, with largest gains when the true nuisance function is nonlinear — directly relevant to retail demand forecasting where functional form is unknown.

## Relevance to thesis
- SRQ1 (Ch.6 Model Benchmark): ensemble/model-averaging rationale for combining ARIMA, Prophet, LightGBM predictions rather than selecting a single model
- SRQ3 (Ch.8 Evaluation): DDML framework for isolating the causal contribution of contextual signals (Indeks Danmark consumer data) from confounders
- Provides formal uncertainty quantification methodology applicable to the synthesis module's confidence scoring

## Gap / limitation
Designed for causal inference, not real-time operational forecasting; cross-fitting adds computational overhead that must be managed within the 8GB RAM constraint.

> Note: a more detailed annotation may exist at `model_averaging_double_ml.md` (Scraping Run 1). This file consolidates that record with Scraping Run 2 tier metadata — check for duplicate and merge if needed.
