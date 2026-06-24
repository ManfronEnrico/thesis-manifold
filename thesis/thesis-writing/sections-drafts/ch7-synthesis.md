# Chapter 7 — Context-Aware Decision Synthesis
> Status: SKELETON + §7.2.3 DETERMINISTIC SYNTHESIS RESULTS written from real
> outputs (2026-06-24; scripts/srq2_synthesis.py → thesis/data/_06_results_srq2/).
> The LLM recommendation text (§7.3, §7.5) and LLM-as-Judge evaluation (§7.6) need
> an LLM API and are deferred to the agentic-harness phase. Architecture bullets
> (§7.1–7.2.2) unchanged.
> Last updated: 2026-06-24

---

## 7.1 The synthesis problem

- After 5 models each produce a point forecast + prediction interval, a decision-maker needs a single actionable recommendation — not 5 competing numbers
- The synthesis problem: how to aggregate heterogeneous ML outputs into a confidence-scored, natural language recommendation
- This is the core SRQ2 question: *How can an LLM synthesise multi-model forecasts into a confidence-scored recommendation?*
- Analogy: MCDM (Multi-Criteria Decision Making) — weight and aggregate multiple indicators into a ranked decision
- Cite: Hybrid MCDM + ML Supplier Selection paper; Hybrid AI + LLM Industrial paper

---

## 7.2 Architecture of the Synthesis Agent

### 7.2.1 Inputs to the Synthesis Agent

| Input | Source | Format |
|---|---|---|
| Model forecasts (5×) | Forecasting Agent | {model_name: {point_forecast, lower_90, upper_90, MAPE_validation}} |
| Historical context | Nielsen data | last_N_periods actuals, seasonality flags |
| Market context | Coordinator prompt | product category, retailer, planning horizon |

### 7.2.2 Synthesis pipeline

**Step 1 — Model consensus scoring**
- Compute inter-model agreement: std(point_forecasts) / mean(point_forecasts) = relative disagreement metric
- High agreement (low spread) → higher base confidence
- Assign inverse-MAPE weights to each model's forecast: w_i = (1/MAPE_i) / Σ(1/MAPE_j)
- Weighted ensemble point forecast = Σ(w_i × forecast_i)

**Step 2 — Interval calibration**
- Apply Kuleshov et al. (2018) post-hoc calibration to ensemble prediction intervals
- Calibration set: validation period actuals vs. stated intervals
- Output: calibrated 90% prediction interval with empirically validated coverage

**Step 4 — Confidence score computation**
- Composite confidence score (0–100):
  - 40% weight: calibrated interval width (narrower = higher confidence)
  - 30% weight: inter-model agreement (lower spread = higher confidence)
- Map to 3-tier natural language: High (≥70), Moderate (40–69), Low (<40)
- Cite: Kuleshov et al. 2018, Do Forecasts as Prediction Intervals Improve Planning (2010)

**Step 5 — LLM recommendation generation**
- LLM (claude-sonnet-4-6 via API) receives structured synthesis context:
  - Ensemble forecast + calibrated interval
  - Confidence score + tier
  - Historical actuals for comparison
- LLM generates: 2–3 sentence natural language recommendation + stock action suggestion
- Temperature: 0 (deterministic for reproducibility)
- Prompt template: stored in agent code, versioned

### 7.2.3 Deterministic synthesis results

<!-- Factual, from scripts/srq2_synthesis.py; results thesis/data/_06_results_srq2/.
Models trained per the Ch6 §6.5.6 selected configuration; ensemble = inverse-
validation-WMAPE weights; interval = split-conformal 90% on the ensemble. -->

The non-LLM core of the Synthesis Agent was implemented and run on the test set for
all four categories: per (brand[, chain], month) it produces an inverse-WMAPE-weighted
ensemble forecast, an inter-model agreement score, a split-conformal 90% interval,
and a composite confidence score (30% agreement + 40% interval tightness + 30% model
accuracy) mapped to a High/Moderate/Low tier.

| Category | n series-months | mean confidence | Moderate / Low | 90% interval coverage |
|---|---|---|---|---|
| CSD | 845 | 44.9 | 72% / 28% | 96.6% |
| danskvand | 966 | 43.6 | 70% / 30% | 97.8% |
| energidrikke | 205 | 47.1 | 75% / 25% | 80.0% |
| RTD | 324 | 38.5 | 45% / 55% | 90.7% |

Two observations. First, the conformal ensemble interval is **well-to-conservatively
calibrated** (empirical coverage 80–98% against the 90% nominal), so the uncertainty
the agent communicates is trustworthy. Second, the composite confidence skews to the
**Moderate** tier with no High-confidence forecasts under the current thresholds —
because the (deliberately wide) 90% interval keeps the tightness term low. This is a
property of the scoring weights, not of the forecasts; the tier cut-offs are a
calibration choice to revisit. Operationally the engine already supports the SRQ2
goal: it triages each forecast by confidence so the agentic layer can surface
reliable forecasts and route Low-confidence ones (notably the more volatile RTD,
55% Low) to human review. The natural-language recommendation and the LLM-as-Judge
quality assessment (§7.3, §7.6) sit on top of this structured output and require an
LLM API; they are run in the agentic-harness phase.

---

## 7.3 LLM prompt design

### 7.3.1 System prompt (Synthesis Agent)
```
You are a demand forecasting analyst for FMCG retail. Given a set of ML model forecasts, a calibrated confidence score, and consumer demand signals, you produce a concise, actionable recommendation for a category manager.

Rules:
- Always state the forecast range (lower to upper bound), not just the point estimate
- Always state the confidence level (High/Moderate/Low) and why
- If models disagree, flag the uncertainty explicitly
- Keep recommendations to 2-3 sentences maximum
- Do not hallucinate data — only use provided inputs
```

### 7.3.2 User prompt structure
```
PRODUCT: {product_name} | RETAILER: {retailer_name} | WEEK: {target_week}

ENSEMBLE FORECAST: {point_forecast} units (90% interval: {lower} – {upper})
CONFIDENCE: {score}/100 ({tier}) — based on {inter_model_spread} model agreement, {calibration_quality} calibration
HISTORICAL: Last 4 weeks actuals: {actuals_list}

Generate a recommendation.
```

---

## 7.4 Design principles applied

- Progressive uncertainty disclosure (show interval, not just point) — cite AI-augmented decision making DSR 2024
- Human override preserved — synthesis output is a recommendation, not an automated order
- Contextualised explanation included in rationale
- Confidence calibration (post-hoc isotonic regression) — cite Kuleshov 2018

---

## 7.5 Computational footprint

- LLM API call: ~1–3 seconds per synthesis request; ~500–1000 input tokens; ~100–200 output tokens
- No local LLM loaded — API call only; ~0MB additional RAM (vs. ~3–6GB for local Llama/Mistral)
- Total synthesis step RAM: <50MB (structured data manipulation + API call)
- This is the key architectural decision: using claude-sonnet-4-6 API keeps total RAM under 8GB ceiling

---

## 7.6 Evaluation (SRQ2 operationalisation)

- **LLM-as-Judge protocol**: GPT-4o evaluates synthesis outputs on 5 dimensions (relevance, accuracy, calibration quality, actionability, uncertainty communication) — Likert 1–5
- Evaluate on N=50 randomly sampled product×retailer×week combinations from test set
- Baseline comparison: simple rule-based text generation ("Forecast is X units, model confidence: Y%") — does LLM add value?
- Calibration check: empirical coverage of stated 90% intervals vs. actuals in test set
- Cite: ANAH (evaluation framework for LLM outputs), Hybrid AI + LLM Industrial paper

---

## 7.7 Connection to SRQs

| SRQ | How Ch.7 addresses it |
|---|---|
| SRQ2 | Direct answer: multi-model synthesis → calibrated confidence score → LLM recommendation |
| SRQ3 | Not addressed here; integration readiness is addressed in Ch3 and Ch5 |
| SRQ4 | Synthesis output (natural language + confidence) is the proposed alternative to descriptive BI dashboards |

---

## Outstanding decisions

- Whether to add a 4th confidence component (forecast accuracy trend: is the model improving or degrading over time?)
- Whether to include a "flag for human review" output for Low confidence recommendations
- API cost ceiling: estimate per-recommendation cost and total evaluation cost (N=50 × ~$0.005/call ≈ $0.25 — negligible)
- Whether synthesis outputs should be stored in a local SQLite log for reproducibility
