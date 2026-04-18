---
title: "Accurate Uncertainties for Deep Learning Using Calibrated Regression"
authors: Volodymyr Kuleshov, Nathan Fenner, Stefano Ermon
year: 2018
venue: ICML 2018 (Proceedings of Machine Learning Research, Vol. 80)
url: https://proceedings.mlr.press/v80/kuleshov18a/kuleshov18a.pdf
tier: 2 — Recommended (Scraping Run 1)
score: 9
angles: [SRQ2 — Confidence scoring, Prediction Quality]
srqs: [SRQ2]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
Standard ML regression models produce miscalibrated prediction intervals — stated 90% intervals may contain the true value only 70% of the time. A post-hoc calibration procedure (isotonic regression on held-out data) reliably corrects this without retraining, producing statistically valid uncertainty estimates for any regression model.

## Method
Post-hoc calibration: (1) fit any base regression model; (2) on a held-out calibration set, compute empirical coverage at each confidence level; (3) use isotonic regression to learn a monotone mapping from stated to calibrated confidence levels. Evaluated on neural networks, GPs, and gradient boosting across UCI datasets and real-world applications (genomics, physical simulations).

## Key finding
Calibrated regression reduces calibration error (area between coverage curves) by 50–80% across all tested model families, with negligible impact on point prediction accuracy. Critically, calibration generalises across model architectures — the same procedure works for neural networks, tree ensembles, and linear models.

## Key quote
> "We propose a simple, general method for obtaining calibrated regression intervals from any model — including deep neural networks — by applying isotonic regression to empirical coverage on a held-out set."

## Relevance to thesis
- **SRQ2 primary reference**: the synthesis module's confidence score must be calibrated, not just a raw model output. This paper provides the foundational methodology.
- Post-hoc calibration is RAM-efficient (no retraining) — consistent with ≤8GB RAM constraint
- Works across all 5 thesis models (ARIMA, Prophet, LightGBM, XGBoost, Ridge) — single calibration protocol for the ensemble
- Directly cited in justifying why confidence intervals from the Synthesis Agent are statistically meaningful

## Gap / limitation
Deep learning focus — regression calibration for classical time-series models (ARIMA, Prophet) requires adaptation. Does not address multi-model aggregation or the translation of calibrated intervals into natural language confidence descriptors.
