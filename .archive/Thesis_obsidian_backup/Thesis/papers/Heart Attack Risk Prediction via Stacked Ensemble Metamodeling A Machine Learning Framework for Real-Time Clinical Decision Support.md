

authors: Nava-Martinez, B.N., Hernandez-Hernandez, S.S., Rodriguez-Ramirez, D.A., Martinez-Rodriguez, J.L., Rios-Alvarado, A.B., Diaz-Manriquez, A., Martinez-Angulo, J.R., & Guerrero-Melendez, T.Y.

year: 2025

venue: Informatics (MDPI), Vol. 12, No. 4, Article 110

doi: 10.3390/informatics12040110

apa7: >

  Nava-Martinez, B.N., et al. (2025). Heart attack risk prediction via stacked

  ensemble metamodeling: A machine learning framework for real-time clinical

  decision support. *Informatics*, *12*(4), 110.

  https://doi.org/10.3390/informatics12040110

read_date: 2026-03-17

read_depth: full

---

  

## In one sentence

  

A stacked ensemble metamodel combining six supervised base learners (SVM, MLP, LR, KNN, DT, NB) through stacking and voting strategies achieves 90.2–98.9% accuracy on three independent clinical datasets for heart attack risk prediction, deploying as a lightweight web interface with color-coded outputs designed for clinicians without data science backgrounds — validating the stacked ensemble + actionable output pattern for resource-constrained real-time decision support.

  

## Method

  

Three independent physico-clinical datasets. Full pipeline: integrity verification → winsorization + log transformation → ANOVA F-score feature selection → exhaustive cross-validated grid search (hyperparameter tuning) → six base learners (SVM, MLP, LR, KNN, DT, NB) evaluated individually → six stacking and voting metamodel configurations trained on base learner predictions → underperforming base models eliminated → top configuration deployed as a lightweight web application. Output: color-coded risk label + probability pie chart.

  

## Key findings — cite these

  

- Stacked ensemble metamodels achieve **90.2% to 98.9% accuracy** across three independent clinical datasets — outperforming prior state-of-the-art single-model approaches

- **Eliminating underperforming base learners before stacking** improves final metamodel performance — selective ensemble construction outperforms brute-force inclusion

- Stacking consistently outperforms voting when base learner diversity is high (SVM + MLP + LR + KNN + DT + NB cover fundamentally different inductive biases)

- Lightweight deployment with real-time prediction is achievable without GPU infrastructure

- ANOVA F-score is the recommended feature selection method for limited clinical datasets

  

## Direct quotes — copy verbatim, include page/section

  

> "Implementing such tools in clinical settings faces significant hurdles: inconsistent data quality and availability, complex preprocessing requirements, the need for artificial intelligence expertise, and challenges in translating technical outputs into actionable clinical insights for medical personnel." (Section 1)

  

> "To achieve real-world impact, these solutions must prioritize accessibility, interpretability, and seamless integration into existing medical workflows." (Section 1)

  

> "By strategically combining the strongest predictors and eliminating underperforming base models, our final ensemble achieved accuracies ranging from 90.2% to 98.9%." (Section 7)

  

## Where this goes in my thesis

  

- **Ch.2, Section 2.2**: Supporting reference for stacked ensemble architecture in real-time decision support — the clinical deployment analogue (resource-constrained environment + non-technical end users + actionable output) directly parallels the thesis's Synthesis Agent design for retail analysts

- **Ch.5 (Framework Design)**: The base-learner diversity principle (SVM + MLP + LR + KNN + DT + NB covering different inductive biases) supports combining ARIMA, Prophet, LightGBM, and Ridge — four structurally different forecasting approaches; cite to justify model family diversity over multiple variants of the same family

- **Ch.6 (Evaluation — SRQ1)**: The paper's experimental protocol (evaluate each base learner independently, then evaluate ensemble configurations) is the exact benchmarking structure the thesis should follow; cite as precedent

  

## What this paper does NOT cover (gap it leaves)

  

The framework stacks classification models for binary risk prediction on static tabular data; it does not address time-series forecasting ensembles, probabilistic prediction intervals requiring calibration, LLM-based synthesis of heterogeneous model outputs into natural language recommendations, RAM-constrained sequential model execution, or the integration of external consumer survey signals into a weighted confidence score.

  

## My critical assessment

  

Demonstrates the effectiveness of stacked ensemble metamodels combining diverse base learners for high-accuracy predictions in resource-constrained, real-time settings  
  

Shows that selective inclusion of base learners improves ensemble performance — supporting the thesis’s rationale for weighting and pruning models in the Synthesis Agent  
  

Provides a practical analogue for deploying ML outputs to non-technical users via interpretable, actionable outputs (color-coded labels + probability charts), directly relevant to retail analyst workflows  
  

Validates base-learner diversity principle, justifying combining structurally different forecasting models (ARIMA, Prophet, LightGBM, Ridge) rather than multiple variants of the same family  
  

Limitations for the thesis context:  
  

- Focuses on static tabular data for classification; does not address time-series forecasting  
      
    
- Does not handle probabilistic output calibration or LLM-based synthesis of multiple model outputs into natural language recommendations  
      
    
- No treatment of RAM-constrained sequential model execution or external signal integration  
      
    

Overall, the paper provides a strong empirical precedent for the thesis’s ensemble design, evaluation protocol, and actionable output principle, while leaving domain-specific adaptations (time-series, LLM synthesis, confidence scoring) for the thesis to address

  
**