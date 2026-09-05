# Comments — Experimental Evaluation

Extracted 2026-09-05 from `MSc. Data Science - 175888 and 176171 - Master Thesis.docx`.
23 comment(s) in 23 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [360](#c360) | Experimental Evaluation | FORMATTING |  | FORMATTING: Could use a subtitle for the chapter... |
| [362](#c362) | Evaluation overview | VERIFY, PROSE |  | VERIFY, PROSE... |
| [365](#c365) | Benchmark design | VERIFY, PROSE |  | VERIFY, PROSE... |
| [367](#c367) | Metrics | VERIFY, PROSE |  | VERIFY, PROSE... |
| [369](#c369) | Baselines | VERIFY, PROSE |  | VERIFY, PROSE... |
| [371](#c371) | Results | VERIFY |  | VERIFY... |
| [374](#c374) | LLM-as-Judge protocol | VERIFY, OUTDATED |  | OUTDATED, VERIFY... |
| [376](#c376) | Calibration check | VERIFY, SOURCE, PROSE |  | VERIFY, PROSE, SOURCE... |
| [378](#c378) | SRQ4 baseline - code-as-action agent (Prometh | METACOMMENT, ACADEMIC |  | METACOMMENT, ACADEMIC: Seems like a meta comment... |
| [379](#c379) | SRQ4 baseline - code-as-action agent (Prometh | VERIFY |  | VERIFY... |
| [381](#c381) | Results | VERIFY, OUTDATED |  | OUTDATED, VERIFY: LLM as judge, trial number not up tom date... |
| [383](#c383) | Results | OUTDATED, INCORRECT |  | OUTDATED, INCORRECT: LLM judge... |
| [384](#c384) | Results | OUTDATED |  | OUTDATED... |
| [387](#c387) | RAM profiling | VERIFY, PROSE, OUTDATED |  | VERIFY, OUTDATED, PROSE... |
| [389](#c389) | Latency profiling | VERIFY, PROSE, OUTDATED |  | VERIFY, OUTDATED, PROSE... |
| [391](#c391) | Failure mode analysis | VERIFY, PROSE, OUTDATED |  | VERIFY, OUTDATED, PROSE... |
| [393](#c393) | Results | VERIFY, METACOMMENT, OUTDATED |  | METACOMMENT, VERIFY, OUTDATED... |
| [395](#c395) | Threats to validity | PROSE, CONTEXT |  | PROSE Only a header with table, no context and prose... |
| [396](#c396) | Threats to validity | OUTDATED |  | OUTDATED... |
| [398](#c398) | Threats to validity | VERIFY, NAMING, OUTDATED |  | NAMING, VERIFY, OUTDATED... |
| [400](#c400) | Connection to SRQs | PROSE, CONTEXT |  | PROSE Only a header with table, no context and prose... |
| [402](#c402) | Connection to SRQs | VERIFY, NAMING |  | NAMING, VERIFY... |
| [403](#c403) | Outstanding decisions | VERIFY, METACOMMENT |  | METACOMMENT, VERIFY... |

---

<a id="c360"></a>

## [360] Brian Rohde -- Experimental Evaluation  `FORMATTING`

- **Section:** Experimental Evaluation
- **Date:** 2026-09-05T18:53:00
- **On:** “COULD USE A SUBTITLE”

FORMATTING: Could use a subtitle for the chapter

<a id="c362"></a>

## [362] Brian Rohde -- Experimental Evaluation  `VERIFY * PROSE`

- **Section:** Experimental Evaluation > Evaluation overview
- **Date:** 2026-09-05T16:51:00
- **On:** “Three-level evaluation framework (3-level is the thesis’s core methodological contribution to evaluation design for AI artefacts): Level 1 - ML accuracy: are the forecasting models accurate? (SRQ1)Level 2 - Recommendation quality: does the synthesis produce actionable, calibrated outputs? (SRQ2)Level 3 - Agent behaviour: does the system operate within computational constraints? (SRQ1 + SRQ2)Cite: AI-Based DSR Framework 2024 (evaluation dimensions for AI artefacts); Pathways for Design Research on AI 2024 (INFORMS ISR)”

VERIFY, PROSE

<a id="c365"></a>

## [365] Brian Rohde -- Experimental Evaluation  `VERIFY * PROSE`

- **Section:** Experimental Evaluation > Level 1 - ML accuracy evaluation (SRQ1) > Benchmark design
- **Date:** 2026-09-05T16:52:00
- **On:** “Dataset: Nielsen CSD panel data, [N] SKUs × 28 retailers × [T] weeksStratification: evaluate separately by product category (regular CSD, diet, energy) and retailer tier (major chain, discount, convenience)Test period: hold-out test set, [T_test] weeks (minimum 13 weeks - one quarter)”

VERIFY, PROSE

<a id="c367"></a>

## [367] Brian Rohde -- Experimental Evaluation  `VERIFY * PROSE`

- **Section:** Experimental Evaluation > Level 1 - ML accuracy evaluation (SRQ1) > Metrics
- **Date:** 2026-09-05T16:52:00
- **On:** “MAPE, RMSE, MAE (see Ch.6 definitions)Directional accuracy: % of weeks where model correctly predicts direction of change (increase/decrease/flat)Statistical significance: Diebold-Mariano test for pairwise model comparison”

VERIFY, PROSE

<a id="c369"></a>

## [369] Brian Rohde -- Experimental Evaluation  `VERIFY * PROSE`

- **Section:** Experimental Evaluation > Level 1 - ML accuracy evaluation (SRQ1) > Baselines
- **Date:** 2026-09-05T16:52:00
- **On:** “ARIMA: best-in-class statistical baselineNaïve seasonal: last year’s same week (simple but competitive in seasonal FMCG data)Manifold descriptive baseline: descriptive analytics output from current Manifold AI tool (SRQ4 - requires access to baseline outputs)”

VERIFY, PROSE

<a id="c371"></a>

## [371] Brian Rohde -- Experimental Evaluation  `VERIFY`

- **Section:** Experimental Evaluation > Level 1 - ML accuracy evaluation (SRQ1) > Results
- **Date:** 2026-09-05T17:37:00
- **On:** “On the selected per-category configuration (Ch6 §6.5.6), tuned XGBoost is the best model in every category. Test WMAPE: CSD 16.5%, danskvand 22.0%, energidrikke 11.4% (≈ the ≤15% industry target), RTD 31.0%. Against the traditional baselines, the ML model beats ARIMA (CSD 24.2%, danskvand 33.4%, energidrikke 15.7%, RTD 48.2%) in three of four categories; for danskvand an additive Prophet model (16.9%) is competitive. Every model beats the SeasonalNaive baseline (e.g. CSD 39.9%, RTD 58.8%), confirming genuine learned skill rather than trend persistence. SHAP attributes the forecasts chiefly to lag_1 (last-month sales) and weighted_distribution (shelf availability) across all categories.”

VERIFY

<a id="c374"></a>

## [374] Brian Rohde -- Experimental Evaluation  `VERIFY * OUTDATED`

- **Section:** Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > LLM-as-Judge protocol
- **Date:** 2026-09-05T17:37:00
- **On:** “LLM-as-Judge protocolEvaluator: GPT-4o (independent LLM - not the same model as the Synthesis Agent to avoid self-evaluation bias)Sample: N=50 randomly selected product×retailer×week recommendations from test periodDimensions (Likert 1–5): Accuracy: is the forecast number consistent with the stated confidence?Calibration quality: does the recommendation correctly communicate uncertainty?Actionability: does the recommendation give the category manager a clear action?Relevance: is the provided context used appropriately?Clarity: is the recommendation written clearly and concisely?Cite: ANAH evaluation framework; Humans vs. LLMs (IJF 2024)”

OUTDATED, VERIFY

<a id="c376"></a>

## [376] Brian Rohde -- Experimental Evaluation  `VERIFY * SOURCE * PROSE`

- **Section:** Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > Calibration check
- **Date:** 2026-09-05T17:39:00
- **On:** “Calibration checkCompare stated 90% prediction intervals to actual outcomes in test setCompute empirical coverage rate: should be 85–95% for well-calibrated outputsPlot calibration curve (stated vs. empirical coverage across quantiles)Cite: Kuleshov et al. 2018; Evaluating and Calibrating Uncertainty 2023 (MDPI Sensors)”

VERIFY, PROSE, SOURCE

<a id="c378"></a>

## [378] Brian Rohde -- Experimental Evaluation  `METACOMMENT * ACADEMIC`

- **Section:** Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst
- **Date:** 2026-09-05T17:40:00
- **On:** “SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst”

METACOMMENT, ACADEMIC:


Seems like a meta comment

<a id="c379"></a>

## [379] Brian Rohde -- Experimental Evaluation  `VERIFY`

- **Section:** Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst
- **Date:** 2026-09-05T17:40:00
- **On:** “The SRQ4 baseline is not a human analyst (that comparison is out of scope - infeasible within the project timeline). It is the production code-as-action agent, Prometheus (the Manifold/Royal Unibrew Graph Engine): a LangGraph + PydanticAI agent whose coder writes and executes SQL/Python in an E2B sandbox in an investigate-and-verify loop to answer a data/forecasting brief. SRQ4 therefore compares the dedicated-model integration (this thesis: an LLM that delegates forecasting to pre-trained XGBoost models exposed as a structured tool) against the code-as-action baseline (Prometheus: an LLM that writes its own forecasting code), on correctness, consistency, replicability, cost and latency over a common prompt set. Both run on the same Nielsen categories (CSD, danskvand, energidrikke, RTD); execution is local + sandbox, with no human-in-the-loop baseline.”

VERIFY

<a id="c381"></a>

## [381] Brian Rohde -- Experimental Evaluation  `VERIFY * OUTDATED`

- **Section:** Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > Results
- **Date:** 2026-09-05T17:42:00
- **On:** “On N=50 stratified test cases, GPT-4o (LLM-as-Judge, independent model family) scored the Synthesis-Agent recommendation against a rule-based template baseline on five Likert(1–5) dimensions:”

OUTDATED, VERIFY:


LLM as judge, trial number not up tom date

<a id="c383"></a>

## [383] Brian Rohde -- Experimental Evaluation  `OUTDATED * INCORRECT`

- **Section:** Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > Results
- **Date:** 2026-09-05T17:44:00
- **On:** “Table 21 - LLM Judge Scoring Likert Scale Results”

OUTDATED, INCORRECT:


LLM judge

<a id="c384"></a>

## [384] Brian Rohde -- Experimental Evaluation  `OUTDATED`

- **Section:** Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > Results
- **Date:** 2026-09-05T17:44:00
- **On:** “The LLM synthesis clearly adds value on actionability (4.00 vs 2.14), relevance (4.00 vs 3.28), clarity (4.34 vs 3.46) and calibration (3.74 vs 3.46) - answering the SRQ2 “does the LLM add value over a template?” question affirmatively on four of five dimensions. The baseline edges out the LLM only on accuracy (3.42 vs 2.96): the template merely restates the forecast number, so it cannot contradict its inputs, whereas the LLM’s added interpretation occasionally drifts from a strict reading of the numbers - a precision/usefulness trade-off worth stating. Interval calibration is empirically validated separately (§8.3.2 / Ch6 §6.5.4: ensemble conformal coverage 80–98% against the 90% nominal). The human-analyst comparison (§8.3.3) requires a Manifold team member and is not run here; the SRQ4 code-as-action comparator requires an execution sandbox (E2B key not configured) and is deferred.”

OUTDATED

<a id="c387"></a>

## [387] Brian Rohde -- Experimental Evaluation  `VERIFY * PROSE * OUTDATED`

- **Section:** Experimental Evaluation > Level 3 - Agent behaviour evaluation (SRQ1 + SRQ2) > RAM profiling
- **Date:** 2026-09-05T17:44:00
- **On:** “Tool: tracemalloc (Python standard library)Protocol: profile each agent component separately, then full pipeline end-to-endMeasurement: peak RAM per component, peak total pipeline RAMTarget: total peak ≤4GB (hard constraint)Report: memory profile table per component (Forecasting Agent × 5 models, Synthesis Agent, Coordinator)”

VERIFY, OUTDATED, PROSE

<a id="c389"></a>

## [389] Brian Rohde -- Experimental Evaluation  `VERIFY * PROSE * OUTDATED`

- **Section:** Experimental Evaluation > Level 3 - Agent behaviour evaluation (SRQ1 + SRQ2) > Latency profiling
- **Date:** 2026-09-05T17:45:00
- **On:** “Wall-clock time for full pipeline: data load → feature engineering → model training → prediction → synthesis → recommendationTarget: end-to-end ≤5 minutes for single SKU×retailer×week forecast (reasonable for a category manager’s tool)Separate training latency from inference latency (training once, inference per request)”

VERIFY, OUTDATED, PROSE

<a id="c391"></a>

## [391] Brian Rohde -- Experimental Evaluation  `VERIFY * PROSE * OUTDATED`

- **Section:** Experimental Evaluation > Level 3 - Agent behaviour evaluation (SRQ1 + SRQ2) > Failure mode analysis
- **Date:** 2026-09-05T17:45:00
- **On:** “Deliberately trigger: API timeout (synthesis), memory pressure (all models loaded simultaneously), missing data (incomplete Nielsen week)Document agent recovery behaviour: does the Coordinator handle gracefully? Does the system fall back to the next-best model?”

VERIFY, OUTDATED, PROSE

<a id="c393"></a>

## [393] Brian Rohde -- Experimental Evaluation  `VERIFY * METACOMMENT * OUTDATED`

- **Section:** Experimental Evaluation > Level 3 - Agent behaviour evaluation (SRQ1 + SRQ2) > Results
- **Date:** 2026-09-05T17:46:00
- **On:** “Peak RAM (tracemalloc) is in the tens of MB for every model - Ridge 1.5, LightGBM 18.7, XGBoost 0.2, ARIMA 0.5 MB - i.e. three orders of magnitude below the 8 GB ceiling; the constraint is non-binding at this data scale (a different result from the hypothesised 4–6 GB, because the corrected matrices are far smaller than the all-markets ones). Training latency is seconds, not minutes (XGBoost ~1.7 s, LightGBM ~7.7 s with its tuned n_estimators); inference is ~16 ms for XGBoost. The Synthesis Agent adds only structured arithmetic plus, optionally, one LLM API call (~1–3 s, no local RAM). The end-to-end pipeline therefore runs comfortably within the operational budget. Note: tracemalloc captures Python-level allocations; native LightGBM/XGBoost C++ buffers are additional but small at this scale.(Failure-mode analysis §8.4.3 - API timeout / fallback - is part of the agentic harness evaluation and is run with the LLM-dependent layer.)”

METACOMMENT, VERIFY, OUTDATED

<a id="c395"></a>

## [395] Brian Rohde -- Experimental Evaluation  `PROSE * CONTEXT`

- **Section:** Experimental Evaluation > Threats to validity
- **Date:** 2026-09-05T17:48:00
- **On:** “Threats to validity”

PROSE


Only a header with table, no context and prose

<a id="c396"></a>

## [396] Brian Rohde -- Experimental Evaluation  `OUTDATED`

- **Section:** Experimental Evaluation > Threats to validity
- **Date:** 2026-09-05T17:47:00
- **On:** “LLM-as-Judge self-consistency | Internal validity | Use GPT-4o (different model family) as judge; evaluate inter-rater agreement with human judge on 10% sample”

OUTDATED

<a id="c398"></a>

## [398] Brian Rohde -- Experimental Evaluation  `VERIFY * NAMING * OUTDATED`

- **Section:** Experimental Evaluation > Threats to validity
- **Date:** 2026-09-05T17:47:00
- **On:** “Table 22 - Threats to Validity”

NAMING, VERIFY, OUTDATED

<a id="c400"></a>

## [400] Brian Rohde -- Experimental Evaluation  `PROSE * CONTEXT`

- **Section:** Experimental Evaluation > Connection to SRQs
- **Date:** 2026-09-05T17:48:00
- **On:** “Connection to SRQs”

PROSE


Only a header with table, no context and prose

<a id="c402"></a>

## [402] Brian Rohde -- Experimental Evaluation  `VERIFY * NAMING`

- **Section:** Experimental Evaluation > Connection to SRQs
- **Date:** 2026-09-05T17:50:00
- **On:** “Table 23 - Chapter 8: Results Connection to SRQs”

NAMING, VERIFY

<a id="c403"></a>

## [403] Brian Rohde -- Experimental Evaluation  `VERIFY * METACOMMENT`

- **Section:** Experimental Evaluation > Outstanding decisions
- **Date:** 2026-09-05T19:32:00
- **On:** “decisions”

METACOMMENT, VERIFY
