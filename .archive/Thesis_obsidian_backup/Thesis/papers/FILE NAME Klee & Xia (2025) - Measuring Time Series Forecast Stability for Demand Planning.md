

---
aliases:
learning_text_title: "Measuring Time Series Forecast Stability for Demand Planning"
learning_text_venue: KDD '25 Workshop on "AI for Supply Chain: Today and Future" @ 31st ACM SIGKDD
learning_text_doi: 10.1145/XXXXXX.XXXXXX
learning_text_apa7: "Klee, S., & Xia, Y. (2025). Measuring time series forecast stability for demand planning. In *Proceedings of the 1st Workshop on "AI for Supply Chain: Today and Future" @ 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2 (KDD '25)*. ACM. https://doi.org/10.1145/XXXXXX.XXXXXX"
learning_list_authors:
  - Klee, S.
  - Xia, Y.
learning_list_topic:
  - Forecast Stability
  - Model-Induced Stochasticity
  - Coefficient of Variation
  - Ensemble Forecasting
  - Demand Planning
  - Deep Learning Forecasting
learning_list_srq:
  - SRQ1
learning_list_chapter:
  - Ch.3
  - Ch.6
learning_number_release_year: 2025
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

Using coefficient of variation across ten random-seed runs on M5 and Favorita retail datasets, Klee & Xia demonstrate that model-induced stochasticity is a critical and underexplored dimension of production forecasting system design — ensemble models reduce normalised output variance to <5% compared to 10–20% for individual deep learning models, at no meaningful accuracy cost on M5 data.

## Core Ideas
- Forecast accuracy alone is an insufficient criterion for production deployment — model-induced stochasticity (variance attributable solely to random seed, with fixed inputs and hyperparameters) causes demand planners to lose trust and require excessive human intervention, even when global accuracy metrics are acceptable
- Coefficient of variation (CV) across R repeated runs on a fixed dataset provides a normalised, model-comparable stability metric that separates model-induced variance from cycle-to-cycle change caused by new training data
- Ensemble models (AutoGluon stacked ensemble of 12 models) substantially outperform individual deep learning models on stability — median CV <5% vs up to ~80% for TiDE on individual series — because deterministic sub-models (e.g., ARIMA, ETS) anchor the ensemble output
- The accuracy–stability trade-off is dataset-dependent: on M5 the ensemble dominates on both dimensions; on Favorita, tuned individual models (Chronos) achieve better accuracy at the cost of stability — planners must set explicit risk tolerance thresholds

## Methods
- M5 Walmart retail dataset (product-level aggregation) and Favorita Ecuadorian grocery dataset (product-level aggregation)
- AutoGluon TimeSeries Library v1.2.0 — six model families: DeepAR, TFT, PatchTST, TiDE, Chronos (zero-shot + fine-tuned), AutoGluon best-quality stacked ensemble
- Stability: CV computed across 10 runs with varying random seed, fixed inputs, fixed hyperparameters
- Accuracy: RMSE over backtesting test window; CV of RMSE distributions reported per model

## Key findings — cite these
- At least 10% of time series forecast by individual deep learning models show ≥10% normalised variance (CV); in some cases approaching 20% — attributable solely to random seed variation
- AutoGluon ensemble reduces median CV to <5% on both datasets, outperforming all individual deep learning models on stability
- On M5: ensemble is simultaneously more accurate (lower RMSE) and more stable — no trade-off
- On Favorita: ensemble is more stable but less accurate than tuned Chronos models — trade-off exists and is dataset-dependent
- Deterministic local models (e.g., statistical baselines included in the ensemble) are a key driver of ensemble stability, not just accuracy averaging

## Direct quotes — copy verbatim, include page/section
> "A signal whose global accuracy is acceptable but highly variable frustrates planners who ultimately make purchasing decisions across different planning horizons based on different vendor lead times." (Section 1)

> "At least 10% of the time series forecast by deep learning models can see at least 10%, and in some cases nearly 20%, normalized variance, even when trained on the same set of inputs. In contrast, the AutoGluon ensemble mitigates that variance to less than 5%." (Section 3)

> "Ensemble models are more stable than individual deep learning models while also achieving comparable or better accuracy." (Abstract)

> "Business planners would need to understand their tolerance for risk and variance in forecast outputs as a trade-off against accuracy." (Section 3)

## SRQ Mapping
- **SRQ1** (forecasting accuracy vs. computational efficiency): Directly relevant — introduces forecast stability (CV) as a third model selection criterion alongside accuracy and memory footprint; the thesis benchmark table in Ch.6 should include stability alongside MAPE/RMSE and RAM usage
- **SRQ2** (multi-agent coordination and recommendations): Indirectly relevant — the finding that ensemble aggregation improves stability supports the synthesis layer design, where aggregating multiple model outputs reduces recommendation volatility
- **SRQ3** (contextual information improving AI capabilities): N/A
- **SRQ4** (predictive AI vs. descriptive BI): N/A

## Where this goes in our thesis
- **Ch.6, Section 6.X (Model Evaluation Criteria)**: Cite when justifying the multi-dimensional benchmark framework — stability (CV across seeds) should be documented alongside MAPE/RMSE and memory profiling as a production-readiness criterion, even if our deterministic models (ARIMA, Prophet, Ridge) are inherently stable
- **Ch.3 (Methodology)**: Cite as precedent for framing model selection as a multi-criteria decision — accuracy, computational efficiency, AND stability — justifying why a single metric (MAPE) is insufficient
- **Ch.5 (Framework Design)**: Cite when arguing that lightweight, largely deterministic models (ARIMA, Prophet, LightGBM) are preferred over deep learning alternatives in a production SME context — stability under RAM constraints is an additional justification beyond computational cost

## What this paper does NOT cover (gap it leaves)

The paper studies only deep learning models under stochasticity, leaving the regime of lightweight deterministic or near-deterministic models (ARIMA, Prophet, Ridge, LightGBM) entirely unstudied — the thesis fills this gap by benchmarking exactly these models under an explicit RAM constraint, where deterministic model behaviour is a design feature rather than a limitation.

## Strength
- Amazon Web Services authorship and KDD venue provides strong industrial credibility and signals direct production deployment motivation
- CV methodology is simple, reproducible, and directly applicable to the thesis benchmark design — no specialised tooling required beyond re-running models with different seeds
- Retail datasets (M5 Walmart, Favorita grocery) directly analogous to the Nielsen CSD retail context

## Weaknesses
- Workshop paper (6 pages) — limited statistical depth; no confidence intervals on CV estimates; 10 runs may be insufficient for tail behaviour characterisation
- Model set is exclusively deep learning — ARIMA, Prophet, LightGBM, XGBoost, Ridge are absent, making direct comparison with the thesis model set impossible
- Favorita results (ensemble underperforms on accuracy) introduce ambiguity that weakens the ensemble recommendation without a clear resolution

## My critical assessment


# Manual Assessment
---

- **Strengths:** Provides a rigorous and well-validated framework for uncertainty quantification using prediction intervals (QRF) combined with explainability (SHAP), demonstrating how uncertainty can be made actionable in decision-support contexts; strong alignment with the “predict-then-optimize” paradigm.
- **Weaknesses:** Focuses on a single-model setup in a manufacturing process monitoring context, limiting generalisability to retail time-series forecasting; does not consider ensemble methods, LLM-based synthesis, or computational constraints.
- **Relevance to thesis:** Directly informs your Synthesis Agent design by justifying the need for **explicit uncertainty representation (confidence scoring)** and providing a conceptual template for explaining why recommendations carry different confidence levels.
- **Gap addressed by your work:** Does not address **aggregation of uncertainty across multiple forecasting models, integration into multi-agent LLM systems, or deployment under ≤8 GB RAM constraints**; your thesis extends this by operationalising uncertainty-aware decision support in a **multi-model, resource-constrained retail forecasting pipeline**.
---

# Additional References
## Parent Note Reference
- [[2026 - Project Note - CMT - CBS Master Thesis - MSc. Data Science]]
## Note References
-
## Link References
-
## Physical References
+
## Other References
-
