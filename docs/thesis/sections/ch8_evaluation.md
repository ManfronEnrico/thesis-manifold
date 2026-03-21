# Chapter 8 — Experimental Evaluation
> Status: BULLET POINT SKELETON — not prose yet
> Last updated: 2026-03-14

---

## 8.1 Evaluation overview

- Three-level evaluation framework (3-level is the thesis's core methodological contribution to evaluation design for AI artefacts):
  1. **Level 1 — ML accuracy**: are the forecasting models accurate? (SRQ1)
  2. **Level 2 — Recommendation quality**: does the synthesis produce actionable, calibrated outputs? (SRQ2)
  3. **Level 3 — Agent behaviour**: does the system operate within computational constraints? (SRQ1 + SRQ2)
- Cite: AI-Based DSR Framework 2024 (evaluation dimensions for AI artefacts); Pathways for Design Research on AI 2024 (INFORMS ISR)

---

## 8.2 Level 1 — ML accuracy evaluation (SRQ1)

### 8.2.1 Benchmark design
- Dataset: Nielsen CSD panel data, [N] SKUs × 28 retailers × [T] weeks
- Stratification: evaluate separately by product category (regular CSD, diet, energy) and retailer tier (major chain, discount, convenience)
- Test period: hold-out test set, [T_test] weeks (minimum 13 weeks — one quarter)

### 8.2.2 Metrics
- MAPE, RMSE, MAE (see Ch.6 definitions)
- Directional accuracy: % of weeks where model correctly predicts direction of change (increase/decrease/flat)
- Statistical significance: Diebold-Mariano test for pairwise model comparison

### 8.2.3 Baselines
- ARIMA: best-in-class statistical baseline
- Naïve seasonal: last year's same week (simple but competitive in seasonal FMCG data)
- Manifold descriptive baseline: descriptive analytics output from current Manifold AI tool (SRQ4 — requires access to baseline outputs)

### 8.2.4 SRQ3 ablation: consumer signal contribution
- Run LightGBM (best expected ML model) with and without Indeks Danmark features
- Report MAPE improvement attributable to consumer signals
- Cite: Customer Segmentation + Sales Prediction 2023; Cost-Aware 3PL Forecasting (Xu et al.) for contextual signal value

### 8.2.5 Expected results
*(to be filled once data available)*
- Hypothesis: LightGBM + consumer signals achieves MAPE ≤12%; pure ARIMA ≥20%; ensemble ≤15%
- Hypothesis: consumer signals provide ~5–10% MAPE improvement on retailers with strong Indeks Danmark alignment

---

## 8.3 Level 2 — Recommendation quality evaluation (SRQ2)

### 8.3.1 LLM-as-Judge protocol
- Evaluator: GPT-4o (independent LLM — not the same model as the Synthesis Agent to avoid self-evaluation bias)
- Sample: N=50 randomly selected product×retailer×week recommendations from test period
- Dimensions (Likert 1–5):
  1. **Accuracy**: is the forecast number consistent with the stated confidence?
  2. **Calibration quality**: does the recommendation correctly communicate uncertainty?
  3. **Actionability**: does the recommendation give the category manager a clear action?
  4. **Relevance**: is the consumer context used appropriately?
  5. **Clarity**: is the recommendation written clearly and concisely?
- Cite: ANAH evaluation framework; Humans vs. LLMs (IJF 2024)

### 8.3.2 Calibration check
- Compare stated 90% prediction intervals to actual outcomes in test set
- Compute empirical coverage rate: should be 85–95% for well-calibrated outputs
- Plot calibration curve (stated vs. empirical coverage across quantiles)
- Cite: Kuleshov et al. 2018; Evaluating and Calibrating Uncertainty 2023 (MDPI Sensors)

### 8.3.3 Human baseline comparison (SRQ4)
- Present N=20 product×retailer×week cases to a human analyst (Manifold AI team member or category manager)
- Human analyst produces their own recommendation using current descriptive BI tools
- LLM-as-Judge evaluates both human and AI recommendations on same 5 dimensions
- This provides the SRQ4 answer: does the AI multi-agent system match or exceed descriptive BI in recommendation quality?

### 8.3.4 Expected results
*(to be filled)*
- Hypothesis: AI synthesis scores ≥3.5/5 on all 5 dimensions
- Hypothesis: calibration coverage 85–93% (slightly conservative due to demand volatility)
- Hypothesis: AI system scores higher on calibration and range communication; human analyst scores higher on contextual nuance

---

## 8.4 Level 3 — Agent behaviour evaluation (SRQ1 + SRQ2)

### 8.4.1 RAM profiling
- Tool: tracemalloc (Python standard library)
- Protocol: profile each agent component separately, then full pipeline end-to-end
- Measurement: peak RAM per component, peak total pipeline RAM
- Target: total peak ≤8GB (hard constraint)
- Report: memory profile table per component (Forecasting Agent × 5 models, Synthesis Agent, Coordinator)

### 8.4.2 Latency profiling
- Wall-clock time for full pipeline: data load → feature engineering → model training → prediction → synthesis → recommendation
- Target: end-to-end ≤5 minutes for single SKU×retailer×week forecast (reasonable for a category manager's tool)
- Separate training latency from inference latency (training once, inference per request)

### 8.4.3 Failure mode analysis
- Deliberately trigger: API timeout (synthesis), memory pressure (all models loaded simultaneously), missing data (incomplete Nielsen week)
- Document agent recovery behaviour: does the Coordinator handle gracefully? Does the system fall back to the next-best model?

### 8.4.4 Expected results
*(to be filled)*
- Hypothesis: peak RAM 4–6GB (within constraint); LightGBM + feature set is the bottleneck
- Hypothesis: training latency ~10–20 min (one-time); inference latency ~30–90 seconds per request
- Hypothesis: API timeout handled gracefully; model failure falls back correctly

---

## 8.5 Threats to validity

| Threat | Type | Mitigation |
|---|---|---|
| Single company dataset | External validity | Discuss generalisability scope; document data characteristics |
| LLM-as-Judge self-consistency | Internal validity | Use GPT-4o (different model family) as judge; evaluate inter-rater agreement with human judge on 10% sample |
| Temporal leakage | Internal validity | Strict temporal train/test split; no future features in training set |
| Demand volatility in CSD | Construct validity | Report MAPE distribution not just mean; flag high-volatility SKUs separately |
| Access to Manifold descriptive baseline | External validity | If not available, substitute with published descriptive analytics benchmark or Naïve seasonal |

---

## 8.6 Connection to SRQs

| SRQ | Evaluation evidence |
|---|---|
| SRQ1 | Level 1: MAPE/RMSE/MAE vs. baselines; Level 3: RAM + latency within constraints |
| SRQ2 | Level 2: LLM-as-Judge scores; calibration coverage; Level 3: synthesis latency |
| SRQ3 | Level 1 ablation: MAPE with vs. without consumer signals |
| SRQ4 | Level 2 comparison: AI system vs. human descriptive baseline on recommendation quality |

---

## Outstanding decisions

- Whether N=50 is sufficient for LLM-as-Judge evaluation (statistical power consideration)
- Whether to include inter-rater reliability (Cohen's κ) between LLM judge and human judge
- Data access dependency: evaluation design complete, execution blocked until Nielsen access obtained
- Manifold descriptive baseline: need to discuss with Manifold AI team what form the current tool's outputs take
