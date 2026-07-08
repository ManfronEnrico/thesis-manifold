---
name: Framework Architecture (System A/B Design)
description: System A/B separation, agent roles, data flow, LangGraph state, core architectural rules
updated: 2026-04-15
---

# Framework Architecture

> Phase B — designed by Coordinator (architect persona)
> Status: DRAFT — awaiting human approval

---

## Design Principles

Every decision below is justified against two constraints:
1. **≤8GB RAM** — total system memory budget
2. **Actionable output** — every component must contribute to the managerial recommendation

---

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        COORDINATOR                          │
│                  (LangGraph orchestration)                  │
└──────┬──────────┬────────────────┬──────────────┬───────────┘
       │          │                │              │
       ▼          ▼                ▼              ▼
  ┌─────────┐ ┌─────────┐  ┌──────────────┐ ┌──────────────┐
  │  Data   │ │Forecast-│  │  Synthesis   │ │  Validation  │
  │ Loader  │ │  ing    │  │   Agent      │ │    Agent     │
  │  Agent  │ │  Agent  │  │  (SRQ2+3)   │ │   (SRQ4)    │
  └────┬────┘ └────┬────┘  └──────┬───────┘ └──────┬───────┘
       │           │              │                 │
       ▼           ▼              ▼                 ▼
  Nielsen CSV  Model        Confidence-        Evaluation
  + Indeks DK  Ensemble     scored reco.       Report
  features     outputs      in natural lang.
```

---

## Agent Roles & Responsibilities

### Coordinator
- **Framework**: LangGraph StateGraph
- **Role**: Orchestrates all agents, manages state, routes outputs
- **Memory**: Stateful graph — passes context between agents
- **RAM estimate**: ~100MB (graph state + routing logic)
- **Justification**: LangGraph chosen over custom orchestration for built-in state management, conditional edges, and human-in-the-loop support

### Data Loader Agent
- **Role**: Loads, validates, and preprocesses datasets; builds feature matrix
- **Inputs**: Nielsen CSV (or SQL query result) + Indeks Danmark consumer segments
- **Outputs**: Clean feature matrix (brand × retailer × period), consumer context vectors
- **Key tasks**:
  - Enforce brand × DVH EXCL. HD granularity
  - Build Indeks Danmark consumer segments (clustering on behavioral variables)
  - Join consumer segments to retailer-level demand signals (SRQ3 feature enrichment)
  - Validate data quality, flag missing periods
- **RAM estimate**: ~1.5–2GB (Nielsen facts + Indeks Danmark 20k×6364 float64 ≈ 970MB)
- **Justification**: Load once, pass references — avoid redundant copies

### Forecasting Agent
- **Role**: Runs model benchmark, selects best model(s), generates predictions
- **Inputs**: Clean feature matrix from Data Loader
- **Outputs**: Predictions per brand×retailer×period, memory profile per model, accuracy metrics
- **Model candidates**: ARIMA, Prophet, LightGBM, XGBoost, Ridge Regression
- **RAM estimate per model**:
  - Ridge Regression: ~50MB
  - ARIMA (per series): ~20MB × N series
  - Prophet: ~200–400MB
  - LightGBM/XGBoost: ~200–500MB depending on depth
- **Justification**: Models run sequentially (not in parallel) to stay within 8GB budget
- **Output format**: Structured dict `{model_name: {predictions, MAPE, RMSE, memory_mb}}`

### Synthesis Agent (SRQ2 + SRQ3)
- **Role**: Aggregates multi-model predictions + consumer context → confidence-scored recommendation
- **Inputs**: Forecasting Agent outputs + Indeks Danmark consumer signals
- **Outputs**: Natural language managerial recommendation with confidence score + uncertainty range
- **Design**:
  1. **Ensemble weighting**: weighted average of model predictions (weights ∝ inverse MAPE)
  2. **Contextual adjustment**: modify forecast signal using consumer sentiment/segment shift from Indeks Danmark
  3. **Confidence scoring**: based on model agreement (std dev across models) + data coverage
  4. **LLM layer**: Claude/GPT generates natural language recommendation from structured inputs
- **RAM estimate**: ~500MB (LLM API call — no local model needed)
- **Justification**: LLM called via API (no local inference) to stay within RAM budget

### Validation Agent (SRQ4)
- **Role**: Evaluates framework performance against descriptive analytics baseline
- **Inputs**: All agent outputs, baseline definition
- **Outputs**: 3-level validation report
- **Validation levels**:
  1. **ML accuracy**: MAPE, RMSE, directional accuracy per model per series
  2. **Recommendation quality**: Hit rate, LLM-as-judge rubric (relevance, actionability, confidence calibration)
  3. **Agent behaviour**: latency, memory footprint, error rate
- **Baseline**: Manifold AI Colleagues current descriptive output OR last-period extrapolation if unavailable

---

## Memory Budget

| Component | Estimated RAM |
|---|---|
| Nielsen data (facts table, full load) | ~500MB–1GB |
| Indeks Danmark (20k × 6364 float64) | ~970MB |
| Active ML model (one at a time) | ~200–500MB |
| LangGraph state | ~100MB |
| Python runtime + libraries | ~500MB |
| LLM API layer | ~100MB |
| Buffer | ~1–1.5GB |
| **Total estimate** | **~3.5–4.5GB** |

**Verdict**: Within 8GB budget with ~3–4GB headroom. Sequential model execution is the key design choice that makes this feasible.

---

## Tech Stack Justification

| Choice | Alternative | Why this one |
|---|---|---|
| LangGraph | Custom orchestrator, AutoGen | Built-in state management, human-in-the-loop, conditional edges; widely cited in literature |
| PydanticAI | LangChain agents | Type-safe agent I/O, cleaner validation, lower overhead |
| LightGBM + XGBoost | Deep learning (LSTM, Transformer) | 10–100× lower RAM; competitive accuracy on tabular retail data |
| Prophet | Neural Prophet, DeepAR | Low memory, interpretable seasonality components; suitable for ~36 periods |
| ARIMA | SARIMA, SARIMAX | Baseline univariate; low memory; well-established in retail forecasting |
| Ridge Regression | Lasso, ElasticNet | Simplest linear baseline; near-zero memory; interpretable |
| LLM via API | Local LLM (Llama, Mistral) | Avoids 4–8GB local model weight; stays within RAM budget |

---

## Data Flow

```
Nielsen CSV / SQL
      │
      ▼
Data Loader Agent
  ├── validate & clean
  ├── build time series (brand × retailer × period)
  └── enrich with Indeks Danmark segments
      │
      ▼
Forecasting Agent
  ├── ARIMA       → {predictions, MAPE, RAM}
  ├── Prophet     → {predictions, MAPE, RAM}
  ├── LightGBM    → {predictions, MAPE, RAM}
  ├── XGBoost     → {predictions, MAPE, RAM}
  └── Ridge       → {predictions, MAPE, RAM}
      │
      ▼
Synthesis Agent
  ├── ensemble weighting
  ├── contextual adjustment (Indeks Danmark signals)
  ├── confidence scoring
  └── LLM → natural language recommendation
      │
      ▼
Validation Agent
  ├── Level 1: ML accuracy metrics
  ├── Level 2: recommendation quality
  └── Level 3: agent behaviour + memory profile
      │
      ▼
  Final Report → Coordinator → Human
```

---
