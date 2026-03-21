---
title: "Heart Attack Risk Prediction via Stacked Ensemble Metamodeling: A Machine Learning Framework for Real-Time Clinical Decision Support"
authors: [Al-Masri, Anoud, et al.]
year: 2025
venue: Informatics (MDPI), Vol. 12, No. 4, Article 110
url: https://www.mdpi.com/2227-9709/12/4/110
tier: 2 — High Relevance
score: 7
srqs: [SRQ1]
---

## Core argument
This paper presents a stacked ensemble metamodeling framework for real-time heart attack risk prediction, combining multiple base classifiers (Logistic Regression, Random Forest, Gradient Boosting, SVM, k-NN) through a meta-learner in a two-tier stacking architecture. The paper argues that stacked ensembles consistently outperform individual models in clinical prediction tasks, and that the meta-learning layer provides a principled mechanism for combining model outputs under high uncertainty — mimicking the multi-model aggregation challenge faced by any decision-support system.

## Method
Multiple base ML classifiers are trained on a clinical dataset; their predictions are used as inputs to a meta-learner (Logistic Regression) trained via cross-validation. Model performance is evaluated on accuracy, AUC-ROC, precision, recall, and F1-score. Memory footprint and inference time are reported to demonstrate real-time suitability.

## Key finding
The stacked ensemble achieves 97.2% accuracy and 0.99 AUC-ROC on the heart attack prediction dataset, outperforming all individual base models by 2–8 percentage points, while maintaining sub-second inference time suitable for real-time clinical deployment.

## Key quote
> "Stacked ensemble metamodeling provides a robust mechanism for combining heterogeneous model predictions, consistently outperforming individual classifiers while remaining computationally feasible for real-time deployment."

## Relevance to thesis
- [SRQ1]: The stacked ensemble architecture is a direct candidate model for the thesis model benchmark (Phase 4 / SRQ1) — the two-tier stacking pattern can be evaluated against single models (ARIMA, Prophet, LightGBM) on the Nielsen CSD dataset to assess the accuracy-vs-memory trade-off.
- [SRQ1]: The paper's memory and inference time reporting methodology provides a template for the thesis's required RAM profiling of competing models.

## Gap / limitation
The study uses a classification problem (heart attack risk prediction) on a tabular clinical dataset — not a time-series demand forecasting problem. There is no treatment of temporal structure, seasonality, promotional effects, or the FMCG retail context. The paper does not address multi-agent coordination, LLM synthesis of model outputs, or the 8GB RAM constraint specific to cloud-based deployment. The meta-learner design is evaluated in isolation rather than as one component within a broader orchestrated analytics pipeline.
