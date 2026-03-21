authors: Al-Karkhi, M.I., & Rządkowski, G.

year: 2025

venue: MethodsX (Elsevier)

doi: 10.1016/j.mex.2025.XXXXX

apa7: >

  Al-Karkhi, M.I., & Rządkowski, G. (2025). Innovative machine learning

  approaches for complexity in economic forecasting and SME growth: A

  comprehensive review. *MethodsX*.

  https://www.sciencedirect.com/science/article/pii/S2949948825000010

read_date: 2026-03-17

read_depth: full

---

  

## In one sentence

  

This review surveys ML methods applied to economic forecasting and SME growth prediction, concluding that ensemble methods and deep learning models achieve the largest accuracy gains while SHAP and LIME are the leading interpretability tools, and that real-time data integration, class imbalance, and feature selection remain the primary open challenges.

  

## Method

  

Structured literature review. Categorises studies by methodology (ensemble methods, deep learning, interpretability tools) and by regional focus. Compares existing surveys and identifies gaps. No original experiments — qualitative synthesis only. JEL codes: C53 (forecasting models), L26 (SMEs), O47 (economic growth).

  

## Key findings — cite these

  

- **Ensemble methods** (boosting, bagging, stacking) and **deep learning** (LSTM, ANN) consistently outperform traditional econometric models on business/SME forecasting accuracy

- **SHAP and LIME** are the dominant interpretability tools for ML-based economic forecasts — explicitly recommended for building stakeholder trust

- Key unresolved challenges: imbalanced data, real-time data fusion, robust feature selection

- Regional heterogeneity matters: ML models tuned for one economic context often fail to generalise cross-regionally

- Future direction explicitly advocated: **integrative models combining XAI with cross-regional data fusion**

  

## Direct quotes — copy verbatim, include page/section

  

> "The integration of ensemble methods and deep learning models has achieved significant improvements in prediction accuracy, while interpretability tools such as SHAP and LIME enhance transparency and user trust." (Abstract)

  

> "Forecasting business growth is a challenging endeavor due to the complexity and variability of economic indicators. Traditional economic models often fall short in capturing the multifaceted nature of these dynamics." (Introduction)

  

> "The findings underscore the potential of machine learning to transform economic forecasting, providing valuable insights for researchers, policymakers, and practitioners." (Conclusion)

  

## Where this goes in my thesis

  

- **Ch.2, Section 2.2**: Background citation establishing that ensemble ML methods are the state-of-the-art in business forecasting contexts — directly supports the model selection rationale for ARIMA + Prophet + LightGBM in SRQ1

- **Ch.2, Section 2.3**: The SHAP/LIME interpretability finding supports the thesis's design choice to generate natural language recommendations rather than raw model outputs — stakeholder trust via explainability is a validated requirement in this literature

- **Ch.9 (Limitations)**: The regional generalisation failure finding is directly applicable — the thesis's framework is calibrated to Danish CSD retail data and may not generalise to other markets; cite as establishing this as a known limitation in the ML-for-business-forecasting field, not specific to the thesis

  

## What this paper does NOT cover (gap it leaves)

  

The review covers batch ML forecasting with no computational resource constraints and no multi-agent orchestration; it does not address RAM-bounded sequential model execution, LLM-generated synthesis of heterogeneous model outputs, or the integration of consumer survey signals (Indeks Danmark) as external contextual variables into a unified confidence-scoring mechanism.

  

## My critical assessment  
Provides a useful high-level overview of ML approaches in economic forecasting, reinforcing the empirical advantage of ensemble methods  
  

Supports the thesis’s core design choices: use of multiple models and emphasis on explainability for stakeholder trust  
  

Validates the importance of interpretability (e.g., SHAP/LIME) in real-world decision-support systems  
  

However, as a qualitative literature review, it lacks empirical validation and does not provide actionable implementation guidance  
  

Does not address model integration strategies (e.g., weighting, aggregation logic) or system-level design  
  

Ignores key aspects central to the thesis: multi-agent orchestration, resource-constrained environments, and LLM-based synthesis of model outputs  
  

Therefore, valuable for background justification and positioning, but limited for the technical design and evaluation of the thesis framework

  
**