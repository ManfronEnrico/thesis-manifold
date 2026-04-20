# Chapter 5 — Framework Design
> Thesis Writing Agent output — BULLET POINTS ONLY (no prose)
> Last updated: 2026-03-14
> Status: DRAFT — requires human approval before prose writing

---

## 5.1 Design Objectives

- Objective 1: Deliver reliable sales forecasts at brand × retailer granularity within ≤8GB RAM
- Objective 2: Integrate heterogeneous data signals (sales history + consumer context) into a unified decision output
- Objective 3: Generate confidence-scored, natural language managerial recommendations
- Objective 4: Enable comparison with descriptive analytics baseline (SRQ4)
- Design constraint: every architectural choice must be justified against the 8GB RAM budget
- Design philosophy: modularity — each agent is independently replaceable; system is extensible

---

## 5.2 Architectural Overview

- Framework: multi-agent system orchestrated by LangGraph StateGraph
- 5 operational agents + Coordinator (orchestrator):
  1. **Coordinator** — orchestrates workflow, manages state, triggers human approval points
  2. **Data Loader Agent** — ingests and preprocesses Nielsen + Indeks Danmark data
  3. **Forecasting Agent** — benchmarks and runs predictive models (SRQ1)
  4. **Synthesis Agent** — aggregates predictions + consumer context → recommendation (SRQ2, SRQ3)
  5. **Validation Agent** — evaluates framework against baseline (SRQ4)
- Communication: agents pass structured outputs via LangGraph state graph (typed with PydanticAI)
- Human-in-the-loop: Coordinator requests approval at phase transitions

---

## 5.3 Coordinator

- Technology: LangGraph StateGraph with conditional edges
- Responsibilities:
  - Defines execution order and conditions (data loaded → forecast → synthesise → validate)
  - Passes state between agents (avoids redundant data copies → RAM savings)
  - Implements human approval checkpoints
  - Handles error routing (agent failure → notify → await instruction)
- State schema (PydanticAI typed):
  - `data_status`: loading state + quality flags
  - `forecast_outputs`: model predictions + accuracy metrics per model
  - `synthesis_output`: recommendation + confidence score
  - `validation_output`: 3-level evaluation results
- RAM estimate: ~100MB (graph state + routing logic)

---

## 5.4 Data Loader Agent

- Responsibilities:
  - Load Nielsen facts table (CSV or SQL query result)
  - Validate: check for missing periods, null sales values, period range completeness
  - Build time series: pivot to brand × retailer × period matrix
  - Build feature matrix: lag features (t-1, t-2, t-3, t-12), rolling averages (3m, 6m), promo ratio, distribution delta
  - Load Indeks Danmark: apply PCA + k-means to build consumer segments
  - Map consumer segments to retailers: output segment-affinity vector per retailer
  - Pass feature matrix + consumer vectors to state
- Key design decision: **load once, reference by pointer** — avoid copies in memory
- RAM estimate: ~1.5–2GB (Nielsen facts ~0.5–1GB + Indeks Danmark ~970MB; freed after feature extraction)

---

## 5.5 Forecasting Agent

- Responsibilities:
  - Receive feature matrix from Data Loader
  - Run 5 models **sequentially** (critical RAM management decision):
    1. Ridge Regression — simple linear baseline (~50MB)
    2. ARIMA — univariate time series per product series (~20MB × N series)
    3. Prophet — additive decomposition model (~200–400MB)
    4. LightGBM — gradient boosting on feature matrix (~200–500MB)
    5. XGBoost — gradient boosting comparator (~200–500MB)
  - For each model: record predictions, MAPE, RMSE, directional accuracy, peak RAM usage
  - Select best model(s) by MAPE/RAM Pareto frontier
  - Pass structured output: `{model: {predictions, metrics, memory_mb}}`
- Key design decision: **sequential execution** — model loaded, run, unloaded before next loaded
- Justification: parallel execution would require ~1.5GB simultaneously; sequential keeps peak RAM ≤500MB for model layer
- RAM estimate: max ~500MB at any point during forecasting

---

## 5.6 Synthesis Agent (SRQ2 + SRQ3)

- Responsibilities:
  - Receive multi-model predictions from Forecasting Agent
  - Receive consumer segment vectors from Data Loader
  - Step 1 — Ensemble weighting: compute weighted average prediction (weights ∝ inverse MAPE from Forecasting Agent)
  - Step 2 — Contextual adjustment (SRQ3): apply consumer segment signal to modify ensemble forecast
    - If consumer segment X shows declining affinity for retailer Y → downward adjustment
    - Adjustment magnitude is a learned/calibrated parameter
  - Step 3 — Confidence scoring:
    - Model agreement score: std dev across model predictions (lower = higher confidence)
    - Data coverage score: weighted distribution completeness
    - Combined confidence: weighted average → expressed as % confidence interval
  - Step 4 — LLM layer: structured inputs passed to Claude API (claude-sonnet-4-6)
    - Prompt includes: ensemble forecast, confidence score, consumer context summary, comparison with last period
    - Output: natural language recommendation (2–3 sentences) with explicit confidence qualifier
- Key design decision: **LLM via API** (not local) — avoids 4–8GB local model weight cost
- RAM estimate: ~100–200MB (API call + response buffer)

---

## 5.7 Validation Agent (SRQ4)

- Responsibilities:
  - Level 1 — ML accuracy: MAPE, RMSE, directional accuracy per model per series; compare across 5 models
  - Level 2 — Recommendation quality:
    - Hit rate: did the recommendation correctly predict direction of next-period sales?
    - LLM-as-judge: independent LLM evaluates recommendation on 3 dimensions (relevance, actionability, confidence calibration)
  - Level 3 — Agent behaviour: total pipeline latency, peak RAM per phase, error rate
  - SRQ4 comparison: framework metrics vs descriptive baseline (last-period extrapolation)
  - Output: structured validation report → `docs/tasks/validation_report.md`

---

## 5.8 Memory Budget Summary

| Component | Peak RAM | When |
|---|---|---|
| Python + libraries | ~500MB | Always |
| LangGraph state | ~100MB | Always |
| Nielsen data (raw load) | ~500MB–1GB | Phase: Data loading |
| Indeks Danmark (raw) | ~970MB | Phase: Data loading |
| Feature matrix (post-extraction) | ~200–300MB | Phases: Forecasting, Synthesis |
| Active ML model (one at a time) | ~500MB max | Phase: Forecasting |
| LLM API layer | ~100–200MB | Phase: Synthesis |
| **Worst-case peak** | **~3.5–4GB** | Data loading phase |
| **Normal operation** | **~1.5–2GB** | Forecasting + Synthesis |

**Verdict**: System stays well within 8GB budget. Data loading phase is peak; raw datasets can be freed after feature extraction.

---

## 5.9 Tech Stack Justification

| Choice | Rejected alternative | Reason |
|---|---|---|
| LangGraph | Custom orchestrator | State management, conditional edges, HITL, cited in literature |
| PydanticAI | LangChain agents | Type-safe I/O, lower overhead, cleaner validation |
| LightGBM + XGBoost | LSTM / Transformer | 10–100× lower RAM; competitive accuracy on tabular retail data; ~36 periods insufficient for deep learning |
| Prophet | Neural Prophet | Lower RAM; handles CSD seasonality; suitable for 36-period horizon |
| ARIMA | SARIMA | Univariate baseline; lowest RAM; well-established in retail lit |
| Ridge Regression | Lasso | Simplest baseline; interpretable coefficients; near-zero memory |
| Claude API (remote) | Local Llama/Mistral | Avoids 4–8GB model weights; stays within RAM budget |

---

## CBS Compliance Notes

- ✅ Design justified against research questions (SRQ1–4 each addressed)
- ✅ All design choices argued against the 8GB constraint
- ⚠️ Agent diagram must appear in this chapter (Mermaid → export as figure)
- ⚠️ Cite LangGraph and PydanticAI technical documentation as references
- ⚠️ Confirm with supervisor: is a system architecture chapter standard for this programme?
