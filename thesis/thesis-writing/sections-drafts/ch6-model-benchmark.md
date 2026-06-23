# Chapter 6 — Model Benchmark & Selection
> Status: SKELETON + §6.5 RESULTS DRAFTED [PENDING APPROVAL] — 2026-06-23. Tabular
> models (Ridge/LightGBM/XGBoost + SeasonalNaive) benchmarked on the corrected DVH
> EXCL. HD matrices (WMAPE/median MAPE; results in thesis/data/_05_results_srq1/).
> ARIMA/Prophet, RAM/latency, and calibration coverage are NOT yet run (§6.5.3).
> Rest of chapter still bullets. Prose pending human approval.
> Last updated: 2026-06-23

---

## 6.1 Rationale for model selection

- Five models chosen to span the model family spectrum: statistical time-series (ARIMA, Prophet), gradient boosting (LightGBM, XGBoost), regularised linear (Ridge Regression)
- Selection criteria: (a) established empirical performance on retail/FMCG data; (b) fit within ≤8GB RAM sequential execution budget; (c) interpretability sufficient for SRQ4 evaluation; (d) diversity of inductive bias for ensemble robustness
- Cite: Xu et al. 2024 (LightGBM in supply chain), ML-Based FMCG Demand Forecasting 2024 (Springer), Applying ML in Retail 2024 (MDPI)
- NOT included (and why): LSTM/deep learning — RAM footprint incompatible with ≤8GB constraint; too slow for iterative HPO under time budget; cite Edge AI paper for constraint justification

---

## 6.2 Model descriptions

### 6.2.1 ARIMA
- Classical univariate time-series; Box-Jenkins framework
- Role: statistical baseline — represents "best traditional forecasting" for SRQ4 comparison
- Parameters: p, d, q determined via AIC minimisation; auto_arima (pmdarima) for grid search within RAM budget
- RAM: ~5–20MB; negligible
- Limitation: assumes stationarity; no exogenous variables by default (can extend to ARIMAX)

### 6.2.2 Prophet (Meta)
- Additive decomposition: trend + seasonality + holidays
- Role: handles Danish holiday calendar and seasonal CSD demand patterns explicitly
- Parameters: changepoint_prior_scale, seasonality_mode; auto-tuned via cross-validation
- RAM: ~50–100MB; acceptable
- Advantage: built-in uncertainty intervals (posterior sampling) — directly usable for SRQ2 confidence scoring

### 6.2.3 LightGBM
- Gradient boosting with leaf-wise tree growth; GOSS sampling for speed
- Role: primary ML model — expected best accuracy based on domain literature
- Features: lag features, rolling statistics, promotional flags
- RAM: ~100–300MB depending on feature set; acceptable
- HPO: Optuna Bayesian search, ≤50 trials to stay within time/RAM budget

### 6.2.4 XGBoost
- Gradient boosting with level-wise growth; regularisation via L1/L2
- Role: ML alternative — different regularisation strategy may outperform LightGBM on sparse SKU data
- Same feature set as LightGBM for fair comparison
- RAM: ~150–400MB; acceptable
- HPO: same Optuna protocol as LightGBM

### 6.2.5 Ridge Regression
- L2-regularised linear regression
- Role: linear baseline — establishes whether nonlinear ML models add value over linear extrapolation with features
- Features: same engineered features as boosting models
- RAM: ~5–15MB; negligible
- Advantage: fastest training; useful for memory-constrained execution profiling

---

## 6.3 Experimental setup

### 6.3.1 Data split
- Temporal train/validation/test split (no random shuffling — preserves time series integrity)
- Training: [earliest date] to [split_date_1]; Validation: [split_date_1] to [split_date_2]; Test: [split_date_2] to [latest date]
- Specific dates to be determined once Nielsen data access obtained
- Rolling-window cross-validation for hyperparameter selection (Prophet: built-in; LightGBM/XGBoost: custom)

### 6.3.2 Feature engineering
- Lag features: t-1, t-2, t-4, t-8, t-52 weeks (seasonal lag)
- Rolling statistics: 4-week, 8-week, 13-week rolling mean/std
- Calendar: week of year, month, quarter, Danish public holidays
- Promotional: price discount flag, display/feature flag (if available in Nielsen data)

### 6.3.3 Execution protocol
- Sequential model execution: load → fit → predict → unload → gc.collect()
- Memory profiling: tracemalloc at each stage; peak RAM recorded per model
- All models share identical feature sets for controlled comparison

---

## 6.4 Evaluation metrics

| Metric | Formula | Rationale |
|---|---|---|
| MAPE | mean(|y - ŷ| / y) × 100 | Standard retail forecasting metric; scale-independent; cite Xu 2024 |
| RMSE | √(mean((y - ŷ)²)) | Penalises large errors; relevant for stock-out risk |
| MAE | mean(|y - ŷ|) | Robust to outliers; complements MAPE |
| Coverage (90% PI) | % of actuals within predicted interval | Calibration metric for SRQ2; cite Kuleshov et al. 2018 |
| Peak RAM (MB) | tracemalloc peak_memory | Operational constraint metric — unique to thesis |
| Inference latency (ms) | wall-clock time for prediction | Agent responsiveness metric |

- Target MAPE: ≤15% (industry benchmark for retail demand forecasting — cite ML-Based FMCG 2024)
- Calibration target: ≥85% empirical coverage for stated 90% prediction intervals

---

## 6.5 Results

### 6.5.1 Tabular-model benchmark `[PENDING APPROVAL]`

<!-- DRAFT pending human approval. All numbers are factual, from the committed,
reproducible benchmark (scripts/srq1_benchmark.py + srq1_benchmark_tuned.py,
seed=42) on the corrected DVH EXCL. HD matrices. Results: thesis/data/
_05_results_srq1/. Figures: _05_results_srq1/figures/. ARIMA/Prophet, RAM/latency,
and calibration coverage are NOT yet run — flagged under §6.5.3 gaps. -->

The tabular models (Ridge, LightGBM, XGBoost) plus a SeasonalNaive baseline were
benchmarked on both dataset granularities under the DVH EXCL. HD scope. The
reported metrics are **WMAPE** (volume-weighted — the operationally meaningful
error) and **median per-series MAPE** (robust to low-volume series). Plain mean
MAPE is *not* reported: on the low-volume categories it diverges to absurd values
because a handful of near-zero-actual test rows blow up the percentage denominator
— a known MAPE pathology, and itself a finding about metric choice for this panel.

**Headline (tuned XGBoost, test set, WMAPE):**

| Category | brand × month (_03) | brand × chain (_04) | SeasonalNaive (chain) |
|---|---|---|---|
| CSD | **16.5%** | 20.8% | 39.9% |
| danskvand | 23.8% | **22.0%** | 37.7% |
| energidrikke | **11.4%** | 13.9% | 31.9% |
| RTD | **31.0%** | 38.8% | 58.8% |

XGBoost is the best model in all eight (category × granularity) cells; LightGBM is
a close second; both clearly beat Ridge and SeasonalNaive. Optuna tuning (TPE, 30
trials, validation WMAPE objective) improved WMAPE by roughly 2–4 pp over untuned
defaults. See `fig1_model_ladder.png` (every model beats the naive baseline) and
`fig3_forecast_overlay.png` (top CSD brand, actual vs forecast).

### 6.5.2 Granularity finding `[PENDING APPROVAL]`

Disaggregating to a retail-chain dimension multiplies training rows ~6× but does
**not** uniformly improve accuracy — the gain is category-dependent: brand×month
wins for CSD, energidrikke and RTD (less noise per series), while brand×chain wins
for danskvand. This refutes a naïve "more rows is always better" assumption and is
explained by the signal-to-noise trade-off of finer granularity (see
`fig2_granularity.png`). energidrikke reaches **11.4% WMAPE**, near the ≤15%
industry target.

### 6.5.3 Statistical baselines and the SRQ4 comparison `[PENDING APPROVAL]`

<!-- DRAFT pending approval. Numbers factual, from scripts/srq1_baselines_stat.py;
results _05_results_srq1/stat_baselines.{csv,md}. -->

ARIMA (statsmodels SARIMAX(1,1,1) on log sales) and Prophet were fitted per brand
as univariate traditional baselines. ARIMA test WMAPE: CSD 24.2%, danskvand 33.4%,
energidrikke 15.7%, RTD 48.2%. The SRQ4 question — does the ML approach beat
traditional forecasting — resolves in favour of the gradient-boosted models in
three of four categories:

| Category | Best ML (tuned XGBoost) | ARIMA | Prophet | SRQ4 verdict |
|---|---|---|---|---|
| CSD | **16.5%** | 24.2% | unstable* | ML wins (+7.7 pp) |
| danskvand | 22.0% | 33.4% | **16.9%** | Prophet wins |
| energidrikke | **11.4%** | 15.7% | unstable* | ML wins (+4.3 pp) |
| RTD | **31.0%** | 48.2% | 45.4% | ML wins (+17.2 pp) |

*Prophet WMAPE diverges for CSD and energidrikke: fitting a linear trend on
log-transformed short monthly series lets the trend extrapolate to extreme values
on back-transformation. Prophet is therefore unreliable on this panel and ARIMA is
treated as the primary traditional baseline; the danskvand result (Prophet 16.9%)
is the one category where an additive-seasonality model is competitive.

### 6.5.4 Not yet run (honest gaps)
- **Peak RAM / inference latency** profiling (§6.4) — pending; needed for the
  ≤8 GB operational claim.
- **Calibration / prediction-interval coverage** (§6.4) — pending; the SRQ2
  confidence signal.
- Mean-MAPE is intentionally omitted (degenerate on low-volume series); WMAPE and
  median per-series MAPE are the reported metrics throughout.

---

## 6.6 Model selection decision

- Winning model selected as primary for Synthesis Agent input
- Ensemble weighting rationale: inverse-MAPE weighting or stacking (cite Model Averaging + Double ML — Ahrens et al. 2024)
- Fallback hierarchy: if primary model fails in production → secondary model activated automatically
- All 5 model outputs forwarded to Synthesis Agent (not just winner) — multi-model confidence scoring requires all signals

---

## 6.7 Connection to SRQs

| SRQ | How Ch.6 addresses it |
|---|---|
| SRQ1 | Direct answer: which models work best for retail CSD forecasting within ≤8GB RAM |
| SRQ2 | Prediction intervals + calibration coverage provide the raw confidence signal for SRQ2 |
| SRQ3 | Not addressed here; integration readiness is addressed in Ch3 and Ch5 |
| SRQ4 | MAPE/RMSE of best ML model vs ARIMA baseline establishes the predictive vs descriptive gain |

---

## Outstanding decisions

- Exact train/validation/test dates: pending Nielsen data access
- Whether to include ARIMAX (ARIMA + exogenous) or keep vanilla ARIMA as baseline
- HPO trial budget: 50 trials target, may reduce if RAM pressure observed
- Whether to include a 6th model (e.g. Theta, TBATS) to strengthen SRQ1 coverage
