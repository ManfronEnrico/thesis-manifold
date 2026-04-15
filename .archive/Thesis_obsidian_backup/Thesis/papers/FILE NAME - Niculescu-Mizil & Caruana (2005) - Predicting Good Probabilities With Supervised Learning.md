---
aliases:
learning_text_title: "Predicting Good Probabilities With Supervised Learning"
learning_text_venue: Proceedings of the 22nd International Conference on Machine Learning (ICML 2005)
learning_text_doi: 10.1145/1102351.1102430
learning_text_apa7: "Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. In *Proceedings of the 22nd International Conference on Machine Learning* (pp. 625–632). ACM. https://doi.org/10.1145/1102351.1102430"
learning_list_authors:
  - Niculescu-Mizil, A.
  - Caruana, R.
learning_list_topic:
  - Probability Calibration
  - Platt Scaling
  - Isotonic Regression
  - Confidence Scoring
  - Model Selection
  - Boosted Trees
  - Random Forest
learning_list_srq:
  - SRQ2
  - SRQ1
learning_list_chapter:
  - Ch.3
  - Ch.7
learning_number_release_year: 2005
note_list_type: Regular_Note
note_list_status: complete
note_list_relevance: High
note_list_read_depth: full
tags:
learning_date_read_date: 2026-03-22
cssclasses:
---

# AI Assessment
---
## In one sentence

Across ten supervised learning algorithms on eight classification benchmarks, Niculescu-Mizil & Caruana show that maximum margin methods (boosted trees, SVMs) and Naive Bayes produce systematically distorted probability outputs that require post-hoc calibration — either Platt Scaling for sigmoid-shaped distortions or Isotonic Regression for arbitrary monotonic distortions — after which boosted trees, random forests, and SVMs yield the best-calibrated probabilities.

## Core Ideas
- Raw probability outputs from ML models are not interchangeable as confidence scores — maximum margin methods (boosting, SVMs) compress predictions away from 0 and 1 (sigmoid distortion), while generative models (Naive Bayes) push them to extremes; treating these raw outputs as calibrated probabilities systematically misleads downstream decision-makers
- Platt Scaling (sigmoid transformation with parameters A, B fitted by maximum likelihood) is appropriate when the distortion is sigmoid-shaped and data is scarce — directly applicable to boosted tree and SVM outputs; Isotonic Regression (PAV algorithm) corrects any monotonic distortion but requires substantially more calibration data to avoid overfitting
- An independent calibration set is mandatory — calibrating on the training set introduces bias; the same holdout set can serve dual purpose for model selection and calibration
- After calibration, the ranking of models changes: bagged trees and neural nets are best pre-calibration; boosted trees, random forests, and SVMs are best post-calibration — model evaluation for production deployment must specify whether calibration is applied

## Methods
- Ten supervised learning algorithms evaluated: boosted trees, boosted stumps, SVMs, neural nets, bagged trees, Random Forest, Naive Bayes, decision trees, logistic regression, k-NN
- Eight binary classification benchmarks
- Calibration methods: Platt Scaling (sigmoid with MLE parameter fitting) and Isotonic Regression (PAV algorithm)
- Evaluation: log-loss (cross-entropy) and reliability diagrams; learning curve analysis for data requirements
- Cornell University, ICML 2005 — highly cited foundational work (~3,000+ citations)

## Key findings — cite these
- Maximum margin methods (boosted trees, SVMs) produce sigmoid-shaped distortions that are reliably correctable with Platt Scaling
- Naive Bayes produces the opposite distortion (probability mass pushed toward 0 and 1) — requires Isotonic Regression
- Bagged trees and neural nets are already well-calibrated pre-calibration — no systematic distortion
- After calibration, boosted trees, random forests, and SVMs produce the best-calibrated probabilities across benchmarks
- Isotonic Regression outperforms Platt Scaling when calibration data is abundant (>1,000 points); below this threshold, Platt Scaling is safer due to lower overfitting risk

## Direct quotes — copy verbatim, include page/section
> "Maximum margin methods such as boosted trees and boosted stumps push probability mass away from 0 and 1 yielding a characteristic sigmoid shaped distortion in the predicted probabilities." (Abstract)

> "After calibration boosted trees, random forests, and SVMs predict the best probabilities." (Abstract)

> "If we use the same data set that was used to train the model we want to calibrate, we introduce unwanted bias... So we need to use an independent calibration set in order to get good posterior probabilities." (Section 2.1)

> "Isotonic Regression is more prone to overfitting, and thus performs worse than Platt Scaling, when data is scarce." (Section 2.2)

## SRQ Mapping
- **SRQ1** (forecasting accuracy vs. computational efficiency): Relevant — probability calibration is a post-processing step that changes the model evaluation landscape; the thesis benchmark table should note whether calibration is applied, since LightGBM and XGBoost (boosting family) produce sigmoid-distorted probabilities that require Platt Scaling before confidence scores are meaningful
- **SRQ2** (multi-agent coordination and recommendations): Directly relevant — the synthesis module aggregates probability outputs from heterogeneous models into a confidence-scored managerial recommendation; without calibration, model confidence scores are not comparable across models and the aggregation is statistically unsound; Platt Scaling on LightGBM/XGBoost outputs is the theoretically grounded pre-processing step before synthesis
- **SRQ3** (contextual information improving AI capabilities): N/A
- **SRQ4** (predictive AI vs. descriptive BI): N/A

## Where this goes in our thesis
- **Ch.7, Section 7.X (Confidence Scoring Design)**: Cite as the foundational methodological justification for applying Platt Scaling to LightGBM/XGBoost probability outputs before feeding them into the synthesis layer — this is a ~20-year-old foundational result that legitimises the calibration step as standard practice, not an ad-hoc engineering choice
- **Ch.3, Section 3.X (Methodology — Calibration Pipeline)**: Cite when describing the data pipeline from ML model output to synthesis input — calibration is a mandatory intermediate step with a specific methodological basis, not an optional refinement
- **Ch.6 (Model Benchmark & Selection)**: Cite when reporting model probability quality alongside MAPE/RMSE — note that post-calibration performance ordering differs from pre-calibration, and that the thesis reports calibrated confidence scores

## What this paper does NOT cover (gap it leaves)

The paper addresses binary classification probability calibration in isolation — it does not address how calibrated outputs from multiple heterogeneous models (ARIMA point forecasts, LightGBM quantile estimates, Prophet intervals) are combined into a single confidence-scored recommendation under an LLM synthesis layer, which is the specific aggregation challenge of the thesis synthesis module.

## Strength
- Foundational ICML paper with ~3,000+ citations — citable as established methodological consensus, not emerging research
- Direct applicability to the thesis model stack: LightGBM and XGBoost are boosting-family methods whose raw probability outputs are known to be sigmoid-distorted per this paper, providing a theoretically grounded justification for Platt Scaling in the pipeline
- Practical guidance on calibration set size requirements (Isotonic Regression needs >1,000 points) directly constrains the thesis calibration design given limited Nielsen data

## Weaknesses
- 2005 paper — some findings may be superseded by model-specific calibration advances (e.g., gradient boosting frameworks like LightGBM have built-in calibration options not available in 2005)
- Binary classification only — extension to regression/quantile outputs (our primary use case for demand forecasting) requires additional methodological justification beyond this paper
- Eight benchmarks are not retail/FMCG domain — calibration behaviour in highly skewed, intermittent demand distributions may differ

## My critical assessment
Niculescu-Mizil and Caruana (2005) are directly relevant to this thesis as they establish that the probabilistic outputs of many supervised learning models are systematically miscalibrated, challenging the assumption that model scores can be used as reliable confidence measures in downstream decision-making. This insight underpins the thesis’ design choice to treat ML forecasts as _uncalibrated signals_ requiring transformation before entering the LLM-based synthesis layer. The work’s key contribution—demonstrating the effectiveness of post-hoc calibration methods such as Platt Scaling and Isotonic Regression—provides the methodological foundation for constructing comparable, confidence-scored inputs across heterogeneous models. However, the paper operates strictly within a single-model, binary classification setting and does not address how calibrated probabilities from multiple models can be aggregated into higher-level decisions. Nor does it consider integration with reasoning systems such as LLMs or the role of calibration within a broader validation framework. The thesis extends this line of work by embedding calibration within a multi-agent pipeline, where probabilistic outputs are not endpoints but intermediate representations feeding into constrained, interpretable decision support.

# Manual Assessment
---


---

# Additional References
## Parent Note Reference
- [[2026 - Project Note - CMT - CBS Master Thesis - MSc. Data Science]]
## Note References
-
## Link References
- https://doi.org/10.1145/1102351.1102430
## Physical References
+
## Other References
-
