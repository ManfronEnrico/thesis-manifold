---
aliases:
learning_text_title: "The M4 Competition: 100,000 time series and 61 forecasting methods"
learning_text_venue: International Journal of Forecasting
learning_text_doi: 10.1016/j.ijforecast.2019.04.014
learning_text_apa7: "Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2020). The M4 competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, *36*(1), 54–74. https://doi.org/10.1016/j.ijforecast.2019.04.014"
learning_list_authors:
  - Makridakis, S.
  - Spiliotis, E.
  - Assimakopoulos, V.
learning_list_topic:
  - Forecasting Benchmarks
  - Time Series Forecasting
  - Model Combination
  - Ensemble Forecasting
  - Prediction Intervals
  - Machine Learning vs. Statistical Methods
  - Hybrid Forecasting
learning_list_srq:
  - SRQ1
  - SRQ2
  - SRQ3
learning_list_chapter:
  - Ch.2
  - Ch.3
  - Ch.6
learning_number_release_year: 2020
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

Across 100,000 time series and 61 forecasting methods, the M4 Competition establishes that pure ML methods consistently underperform statistical benchmarks on real-world time series, that combining multiple methods outperforms single best model selection, and that hybrid approaches blending statistical structure with ML combination weights achieve the highest accuracy — while prediction intervals are a non-negotiable complement to point forecasts for sound decision-making.

## Core Ideas
- Pure ML methods failed to meet expectations in M4 — all submitted ML methods were less accurate than the Comb benchmark (simple combination of statistical models), and only one outperformed Naïve2; this is not because ML is inherently inferior but because it lacks the inductive biases (trend, seasonality, regime) that statistical models encode explicitly, making it sample-inefficient on the time series lengths typical in practice
- Combining forecasting methods consistently outperforms single best model selection — random errors cancel, overfitting to series-specific noise is reduced; the best M4 methods were all combination or hybrid approaches, not single models
- The winning innovation was not the choice of base models but the combination mechanism — Smyl's hybrid blended exponential smoothing and ML into one model; Montero-Manso et al. used ML to estimate optimal combination weights across methods; both exploited cross-series information to forecast individual series more accurately
- Prediction intervals are a "two indispensable forecasting tasks" requirement alongside point forecasts — most methods in M4 produced overnarrow PIs that underestimate uncertainty, and point forecasts alone are insufficient and potentially dangerous for decision-making in inventory and risk management contexts
- The M4 explicitly publishes accuracy vs. computational time (Fig. 2) — directly enabling practitioners to select methods against a cost/accuracy frontier, which is precisely the trade-off framing of SRQ1

## Methods
- 100,000 time series covering yearly, quarterly, monthly, weekly, daily, and hourly frequencies across macro, micro, finance, industry, demographic, and other domains
- 49 submitted methods + 12 benchmark/standard methods = 61 total
- Point forecast evaluation: sMAPE, MASE, OWA (Overall Weighted Average combining sMAPE and MASE)
- Prediction interval evaluation: Mean Scaled Interval Score (MSIS)
- Computational time for each method measured and reported against accuracy
- International Journal of Forecasting, 2020 — top-tier forecasting journal; among the most cited forecasting papers of the decade

## Key findings — cite these
- All pure ML methods submitted to M4 were less accurate than the Comb benchmark; only one outperformed the Naïve2 simple baseline
- The top-performing method was Smyl's hybrid (exponential smoothing + ML), achieving the largest accuracy gain over Comb; it combined statistical structure (ETS) with ML-learned corrections
- Combining consistently outperforms single models — confirmed across both point forecasts and prediction intervals; optimal combination weighting (ML-estimated) is more effective than simple averaging
- Most M4 methods underestimated uncertainty (produced overnarrow prediction intervals) — only the top two PI methods achieved accurate interval coverage
- A simple Comb (equal-weight average of Theta, DSES, Holt, Damped, ARIMA, ETS) beat all pure ML submissions — establishing a strong, accessible statistical baseline

## Direct quotes — copy verbatim, include page/section
> "All ML methods submitted were less accurate than the Comb benchmark, and only one was more accurate than the Naïve2." (Section 5, p. 70)

> "What we have been calling PFs are insufficient and often dangerous to utilize for decision making on their own without using their complement, the PIs, to specify the uncertainty around the PFs clearly and unambiguously." (Section 5, p. 71)

> "Combining several forecasting models/methods cancels random errors, generally resulting in more accurate forecasts." (Section 5, p. 72)

> "The element that distinguished the most accurate methods from the rest was the way in which they combined the PFs of the individual methods being utilized." (Section 5, p. 71)

> "One thing that remains to be determined is the possible improvement in PF and PI performances that can be achieved by expanding time series forecasting to include explanatory/exogenous variables." (Section 5, p. 73)

## SRQ Mapping
- **SRQ1** (forecasting accuracy vs. computational efficiency): Directly and foundationally relevant — M4 is the standard large-scale empirical benchmark for forecasting model selection; the finding that pure ML underperforms statistical methods justifies including ARIMA and Prophet alongside LightGBM/XGBoost in the thesis benchmark; the Fig. 2 accuracy vs. computation trade-off is the direct methodological precedent for the thesis's multi-metric benchmark table (MAPE × RAM × runtime)
- **SRQ2** (multi-agent coordination and recommendations): Directly relevant — the consistent empirical superiority of combining over single model selection is the foundational evidence for the synthesis module's multi-model aggregation design; the thesis's synthesis layer is precisely an implementation of the M4 finding that optimal combination weighting outperforms best single model selection
- **SRQ3** (contextual information improving AI capabilities): Indirectly but importantly relevant — M4 explicitly identifies the inclusion of exogenous/explanatory variables as the next open frontier for forecasting competitions; this directly frames SRQ3's contribution (Indeks Danmark consumer survey signals as exogenous enrichment) as a natural extension of the M4 research agenda
- **SRQ4** (predictive AI vs. descriptive BI): N/A

## Where this goes in our thesis
- **Ch.2, Section 2.X (Forecasting Methods — Empirical Evidence)**: Cite as the authoritative empirical benchmark establishing the ML-vs-statistical performance hierarchy — the thesis model selection (including both statistical and ML models) is directly motivated by M4 findings
- **Ch.3, Section 3.X (Methodology — Model Selection Rationale)**: Cite when justifying why the thesis benchmark includes both ARIMA/Prophet (statistical) and LightGBM/XGBoost (ML) — the M4 result shows pure ML is insufficient, hybrid/combination approaches are the evidence-based choice
- **Ch.6, Section 6.X (Model Benchmark Design)**: Cite when framing the accuracy vs. computational time trade-off as the primary evaluation axis — M4's Fig. 2 is the methodological precedent for this framing
- **Ch.7, Section 7.X (Synthesis Module)**: Cite as empirical justification for multi-model combination in the synthesis layer — M4 shows combination consistently beats single best model selection

## What this paper does NOT cover (gap it leaves)

M4 evaluates generic univariate time series methods without exogenous variables, without memory/RAM constraints, and without an LLM synthesis layer that converts combined forecasts into natural-language managerial recommendations — the thesis fills all three gaps simultaneously, positioning itself as an applied extension of the M4 agenda to a resource-constrained, context-enriched, decision-support setting.

## Strength
- International Journal of Forecasting (ABS 3), 100,000 series — the definitive empirical foundation for time series forecasting model selection; citing M4 for model choice justification is expected and academically necessary in any forecasting thesis
- The explicit computational time vs. accuracy trade-off documentation is directly usable as a methodological template for SRQ1
- The exogenous variable gap (Section 5, last paragraph) is a citable research gap that directly motivates SRQ3

## Weaknesses
- M4 series are predominantly yearly/quarterly/monthly from macro, finance, and industry domains — CSD retail weekly/monthly scanner data has higher seasonality complexity and promotional spikes not well represented in M4
- Does not include newer deep learning methods (Chronos, PatchTST, N-BEATS post-M4) — the ML performance gap has narrowed since 2020, particularly for global models trained across many series simultaneously (see M5 Competition, 2022)
- Combination benchmarks (Comb) use equal-weight averaging of statistical models — does not directly address how to combine heterogeneous ML and statistical models with different uncertainty characterisations, which is the specific synthesis challenge of this thesis

## My critical assessment

Makridakis et al. (2020) are central to this thesis as they provide large-scale empirical evidence that robust forecasting performance arises from combining heterogeneous models rather than relying on single-method optimization. This directly motivates the thesis’ multi-agent architecture, where multiple deterministic ML and statistical forecasts are treated as complementary inputs to a synthesis layer rather than competing alternatives. The paper’s key contribution—showing that hybrid and ensemble approaches outperform both pure ML and pure statistical methods, and that prediction intervals are essential for decision-making—underpins the thesis’ emphasis on uncertainty-aware, confidence-scored outputs. However, the M4 competition remains focused on predictive accuracy benchmarking and does not address how forecasts are operationalized into actionable decisions or how different model outputs are semantically integrated. It also excludes exogenous data and reasoning mechanisms, leaving the transition from forecast generation to decision support unresolved. The thesis extends this work by embedding model combination within a validated, LLM-driven decision-support pipeline that integrates contextual signals and explicitly addresses reliability under practical constraints.
# Manual Assessment
---


---

# Additional References
## Parent Note Reference
- [[2026 - Project Note - CMT - CBS Master Thesis - MSc. Data Science]]
## Note References
-
## Link References
- https://doi.org/10.1016/j.ijforecast.2019.04.014
## Physical References
+
## Other References
-
