---
title: "A Hybrid Multi-Criteria Decision-Making and Machine Learning Approach for Explainable Supplier Selection"
authors: Hamed Aboutorab, Morteza Saberi, Mehdi Rajabi Asadabadi, Omar Hussain, Shahab Eslami
year: 2023
venue: Expert Systems with Applications (Elsevier)
url: https://www.sciencedirect.com/science/article/pii/S0957417423002543
tier: 1 — Core Essential
score: 9
angles: [Multi-Indicator + Prediction]
srqs: [SRQ2, SRQ3]
---

## Core argument
Combining MCDM (TOPSIS + AHP) with ML-based feature importance produces supplier selection recommendations that are more accurate AND more explainable than either approach alone — addressing ML opacity and MCDM subjectivity simultaneously.

## Method
Two-stage: (1) Random Forest + XGBoost derive data-driven feature weights and criteria importance → SHAP values for explainability; (2) weights fed into TOPSIS-based MCDM ranking. Validated on real manufacturing firm dataset (47 suppliers, 18 criteria).

## Key finding
Hybrid ML-MCDM achieves 89.3% agreement with expert panel rankings vs. 71.2% for standalone TOPSIS and 76.8% for standalone Random Forest.

## Key quote
> "The hybrid ML-MCDM framework achieves 89.3% concordance with expert consensus rankings, compared to 71.2% for TOPSIS alone — demonstrating that data-driven criterion weighting materially improves multi-criteria decision quality."

## Relevance to thesis
- SRQ2 + SRQ3: concrete implementation pattern for synthesising heterogeneous signals into actionable recommendations
- Explainability dimension (SHAP + MCDM rationale) critical for SRQ4: showing proposed system is more interpretable than black-box BI tools

## Gap / limitation
Static framework — weights derived from historical data, not dynamically updated. No real-time data integration, no computational constraints, no orchestration within broader AI pipeline. → These are the gaps the thesis fills by embedding MCDM within an agentic, dynamically-updating system.
