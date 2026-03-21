# Chapter 6 — Model Benchmark & Selection
> Status: BULLET POINT SKELETON — not prose yet
> Last updated: 2026-03-14

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
- Limitation: assumes stationarity; no exogenous variables by default (can extend to ARIMAX for consumer signals)

### 6.2.2 Prophet (Meta)
- Additive decomposition: trend + seasonality + holidays
- Role: handles Danish holiday calendar and seasonal CSD demand patterns explicitly
- Parameters: changepoint_prior_scale, seasonality_mode; auto-tuned via cross-validation
- RAM: ~50–100MB; acceptable
- Advantage: built-in uncertainty intervals (posterior sampling) — directly usable for SRQ2 confidence scoring

### 6.2.3 LightGBM
- Gradient boosting with leaf-wise tree growth; GOSS sampling for speed
- Role: primary ML model — expected best accuracy based on domain literature
- Features: lag features, rolling statistics, promotional flags, Indeks Danmark consumer signals (SRQ3)
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
- Consumer signals (SRQ3): Indeks Danmark-derived retailer-level demand indices (PCA + k-means output)

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

*(to be completed once data available)*

- Comparative results table: all 5 models × all 6 metrics
- Best model per SKU category analysis
- RAM profile table: peak RAM per model per data volume
- Calibration coverage curves (actual vs stated confidence level)
- Key finding hypothesis: LightGBM or XGBoost achieves lowest MAPE; ARIMA lowest RAM; Ridge fastest inference

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
| SRQ3 | Consumer signal features included in ML models; ablation test quantifies contribution |
| SRQ4 | MAPE/RMSE of best ML model vs ARIMA baseline establishes the predictive vs descriptive gain |

---

## Outstanding decisions

- Exact train/validation/test dates: pending Nielsen data access
- Whether to include ARIMAX (ARIMA + exogenous) or keep vanilla ARIMA as baseline
- HPO trial budget: 50 trials target, may reduce if RAM pressure observed
- Whether to include a 6th model (e.g. Theta, TBATS) to strengthen SRQ1 coverage
