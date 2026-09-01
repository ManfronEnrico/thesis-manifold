<!-- PROSE STRIPPED 2026-09-01 (P0044).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-01_18-50/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 6 — Model Benchmark & Selection

> **P0044 OPEN (2026-09-01): RAM figure needs reconciling.** This file states an
> 8 GB budget. That number is a project assumption, not a sourced one -- Ng (2017)
> argues memory is the binding design variable, not that SMEs get 8 GB. Manifold's
> production Prometheus E2B template is provisioned at a **measured 4096 MB**
> (`fxe7gzkqjupdhbx4uvpr`, verified live 2026-09-01). Prefer the measured figure.
> All results hold under the tighter bound (serving 36.8 MB, refit ~37 MB).
> See `plans/P0044_2026-09-01_17-10_resource-measurement-and-retrain-arms/findings.md` F22-F23.

> **Status: §6.1–6.5 REVISED 2026-08-23** against the source-verified citation
> register (P0041) and the current results on disk. §6.5 was **rewritten, not patched**:
> its previous tables reported pre-tuning values and carried a `brand × chain` column for
> a grain that DEC-GRAIN/P0035 removed from code, paths and results. Every figure in
> §6.5 is now traceable to a named file in `04_thesis_results/srq1/`.
>
> **Resolved 2026-08-25:** the ≤15% accuracy target has been **withdrawn**. Source-level
> verification found no such benchmark in the cited paper — Ceran et al. explicitly
> *reject* MAPE for zero-inflation and report WRMSSE instead (§6.4.3).
> **Open:** `fig4_ram_budget` is stale (§6.5.6).
>
> **Every citation in §6.1–6.4 is `VERIFIED` in the register** unless explicitly marked
> otherwise. Do not add a citation here that has not been source-checked.
> Last updated: 2026-08-23

---

## 6.1 Rationale for model selection

- **Five model families span the inductive-bias spectrum**: classical statistical
- **Selection criteria**: (a) established empirical performance on retail/FMCG panels;
- **The benchmark rung is required, not decorative.** Hyndman & Athanasopoulos (2021,
- **Empirical weight for that requirement** comes from M4: of six pure machine-learning
- **NOT included, and why**: deep sequence models (LSTM/N-BEATS) — RAM footprint

> **A caution carried from M4 into Chapter 9.** M4's headline is often compressed to
> "machine learning failed". That is not what it found. The competition was **won by a
> hybrid** — Smyl's exponential-smoothing/RNN, 9.4% better than the combination
> benchmark — with a seven-method statistical combination second (Makridakis et al.,
> 2018, p. 803). The finding is that *pure* ML underperformed while *combinations* won,
> which is an argument for the ensemble scenario rather than against modelling.

---

## 6.2 Model descriptions

### 6.2.0 Simple benchmarks

| Method | Forecast for horizon *h* |
|---|---|
| Mean | ŷ(T+h) = ȳ |
| Naive | ŷ(T+h) = y(T) |
| Seasonal naive | ŷ(T+h) = y(T+h−m(k+1)), with *m* the seasonal period and *k* = ⌊(h−1)/m⌋ |
| Drift | ŷ(T+h) = y(T) + h · (y(T) − y(1)) / (T−1) |

- **Seasonal naive is the decisive one for this panel.** Monthly beverage demand has

### 6.2.1 ARIMA
- Classical univariate time-series model in the Box–Jenkins framework
- Role: statistical baseline representing established traditional forecasting
- **Implementation: `statsmodels` `SARIMAX(order=(1,1,1))` on log sales, fitted per
- RAM: ~0.5 MB measured; negligible
- Limitation: assumes stationarity; univariate, so no promotional or calendar inputs

### 6.2.2 Prophet (Meta)
- Additive decomposable model, **y(t) = g(t) + s(t) + h(t) + ε** — trend, seasonality,
- Designed for forecasting at scale by analysts with domain rather than statistical
- **No holiday calendar is supplied in this thesis**, and none of the multi-seasonality
- RAM: ~50–100 MB; acceptable

> **On Prophet's poor performance here — the wording matters.** Taylor & Letham do
> **not** state that Prophet is unsuitable for monthly data, and they do not show that
> it produces flat forecasts. Neither claim may be attributed to them. The defensible
> argument is mechanical: at month grain weekly seasonality does not exist, holiday
> windows collapse, and yearly seasonality reduces to roughly twelve points that the
> tabular models already capture through `month`, `quarter` and `lag_13`. What remains
> is a piecewise trend plus a coarse annual term estimated on ~30 observations.
> **Prophet is being applied outside the regime its design targets — a limitation of
> this application, not a documented defect of the method.**

### 6.2.3 LightGBM
- Gradient boosting with leaf-wise tree growth and GOSS sampling
- Role: primary ML candidate
- RAM: ~18.7 MB measured
- HPO: Optuna TPE, **100 trials**, 4-fold expanding-window CV (§6.3.4)

### 6.2.4 XGBoost
- Gradient boosting with level-wise growth and L1/L2 regularisation
- Role: ML alternative with a different regularisation strategy
- Identical feature set to LightGBM for a controlled comparison
- RAM: ~0.2 MB measured
- HPO: identical protocol

### 6.2.5 Ridge regression
- L2-regularised linear regression: minimises the penalised residual sum of squares,
- Role: linear baseline — establishes whether non-linear models earn their complexity
- RAM: ~1.5 MB measured

> **Do not overstate Ridge's status.** *The Elements of Statistical Learning* contains
> no normative rule making ridge a baseline every tabular model must beat; its merit is
> conditional on the data-generating process. It is a foundational benchmark for
> regularised linear models, and that is the claim to make.

> **A specification issue specific to this panel.** The feature matrix was engineered
> for trees: the lag and rolling columns are in raw units while the target is
> `log1p(sales_units)`. Trees are unaffected — they are "invariant under (strictly
> monotone) transformations of the individual predictors" (Hastie et al., 2009, p. 307)
> — but a linear model fitting log(y) on raw-unit lags asserts an additive relationship
> where the true one is multiplicative. Ridge is therefore fitted on logged features.
> **Note the boundary precisely: the invariance is to transforming the predictors, not
> the target.** Logging the target changes leaf means and boosting gradients, so it
> affects LightGBM too.

---

## 6.3 Experimental setup

### 6.3.1 Grain and data split
- **Grain: brand × month** (DEC-GRAIN). The chain and region grains were evaluated and
- Temporal train/validation/test split, no shuffling
- Horizon **H = 3** months
- Test-set sizes: CSD 665 rows, RTD 372, energidrikke 308, danskvand 174

### 6.3.2 Feature engineering
- **Lags**: t−1, t−2, t−3, t−4, t−8, t−13 months
- **Rolling statistics**: 4-month and 13-month mean; 4-month standard deviation
- **Calendar**: `month`, `quarter`, and a binary `peak_month` flag derived from the
- **Promotional**: `promo_intensity` (promotional share of units, clipped to [0,1],
- Missing lag values for short histories are left as NaN (handled natively by the tree

> **The cost of omitting `promo_intensity` from cross-category comparisons was
> measured, not inferred.** Refitting with and without the feature on the two categories
> that carry it: CSD +0.30 pp (XGBoost) and +0.27 pp (LightGBM) WMAPE; energidrikke
> +1.44 pp (XGBoost) but **−1.36 pp (LightGBM)**. Dropping it improves 5 of 8
> model × category × metric combinations. **A SHAP ranking would not have supported this
> conclusion** — attribution measures what a fitted model used, whereas selecting on
> individual relevance is "usually suboptimal for building a predictor" (Guyon &
> Elisseeff, 2003, p. 1158). The two questions are distinct and only the refit answers
> the second.

### 6.3.3 Execution protocol
- Sequential execution: load → fit → predict → unload → `gc.collect()`
- Memory profiling via `tracemalloc` at each stage; peak RAM recorded per model
- Fixed seed (42) throughout; seed sensitivity is measured separately (§6.5)

### 6.3.4 Validation scheme

> **The justification must be conditional, and it is stated that way deliberately.**
> Standard K-fold cross-validation is **not** universally invalid for time series:
> Bergmeir, Hyndman and Koo (2018, Theorem 1) prove it is valid for purely
> autoregressive models with uncorrelated errors, and it is more data-efficient than
> out-of-sample splitting on stationary series. The argument here rests on this panel's
> properties rather than on a general rule: monthly brand-level beverage demand is
> trended, seasonal and non-stationary, and under non-stationarity methods preserving
> temporal order give substantially more accurate estimates of generalisation loss
> (Cerqueira et al., 2020). **Nor is the expanding window mathematically mandatory** —
> a sliding window trades differently, discarding old data to adapt to structural
> breaks (Tashman, 2000, p. 441). It is a reasoned choice, not a requirement.

### 6.3.5 Hyperparameter optimisation

> **Two attributions kept separate**: Bergstra et al. (2011) for the mathematics of TPE,
> Akiba et al. (2019) for the software. The Optuna paper does not formulate TPE — it
> attributes the algorithm to Bergstra.

> A limitation worth stating: sequential model-based optimisation **can underperform
> random search** when the surrogate model is misspecified (Bergstra et al., 2011), and
> random search was not run as a control here.

---

## 6.4 Evaluation metrics

| Metric | Definition | Rationale |
|---|---|---|
| **WMAPE** | Σ\|y−ŷ\| / Σ\|y\| × 100 | Primary. Volume-weighted, defined at zero actuals, and consistent for the median (see below) |
| **Median APE** | median(\|y−ŷ\|/y) over y > 0 | Robust per-series view; undefined where y = 0 |
| **MASE** | mean(\|y−ŷ\|) / in-sample MAE of the naive forecast, per series | Scale-free, defined at zero, and absolutely interpretable: < 1 beats a naive forecast |
| Coverage (80 / 90% PI) | share of actuals inside the interval | Calibration signal for SRQ2 |
| Median relative interval width | interval width ÷ actual | Reported **beside** coverage — see below |
| Peak RAM (MB) | `tracemalloc` peak | The operational constraint |
| Inference latency (ms) | wall-clock prediction time | Agent responsiveness |

### 6.4.1 Why WMAPE is the primary metric

- absolute-error loss is minimised by the **median** (p. 746);
- pointwise absolute *percentage* error is minimised by the **(−1)-median** — a density
- WMAPE aggregates absolute errors *before* dividing by total volume, so minimising it

> One step is ours rather than Gneiting's: he does not use the term WMAPE. The bridge is
> algebraic — Σ\|yₜ\| is constant across candidate models on a fixed evaluation sample,
> so minimising WMAPE is minimising Σ\|error\|.

### 6.4.2 Scorability, and what is excluded from what

| Rule | Applies to | Basis |
|---|---|---|
| Exclude zero-actual rows | Median APE and MAPE only | Mathematical — APE is undefined there |
| *(nothing else)* | — | — |

> **The one exclusion is not attributed to a source, and must not be.** Hyndman &
> Koehler (2006, p. 683) explicitly call excluding zero windows "an artificial solution
> that is impossible to apply in practical situations", recommending zero-stable metrics
> such as MASE instead — which is precisely why MASE is reported here. Dropping
> zero-actual rows from *percentage* statistics is unavoidable because the quantity does
> not exist; extending that exclusion to metrics that are well defined would be the
> practice they criticise.

### 6.4.3 Targets

- **Accuracy target: none imported from the literature.** Earlier drafts carried a
- **What replaces it: the simple benchmarks of §6.2.0**, scored on this thesis's own
- **Calibration target: ≥85% empirical coverage** for a nominal 90% interval —

---

### 6.4.4 Demand-pattern categorisation

- **p** — average inter-demand interval (periods per non-zero demand)
- **CV²** — squared coefficient of variation of **non-zero** demand sizes

| | CV² ≤ 0.49 | CV² > 0.49 |
|---|---|---|
| **p ≤ 1.32** | smooth | erratic |
| **p > 1.32** | intermittent | lumpy |

| Category | smooth | erratic | intermittent | lumpy |
|---|---:|---:|---:|---:|
| CSD | 44 | 32 | 5 | 14 |
| RTD | 32 | 20 | 2 | 8 |
| energidrikke | 16 | 18 | 2 | 8 |
| danskvand | 16 | 9 | 3 | 1 |

> **An earlier version of this analysis used a volume floor of one unit per month**, a
> threshold chosen by judgement to keep near-empty series from dominating per-brand
> comparisons. Measuring it against the categorisation showed it was a poor instrument:
> it removed **8 smooth brands** — well-behaved series that merely happen to be small,
> exactly what a forecasting study should retain — while leaving **21 lumpy or
> intermittent brands** above the line. Volume and regularity are different properties,
> and only the second is what the guard was for.

> **A caveat on transfer.** These cut-offs were derived for Croston-type estimators
> under specific assumptions (α = 0.15, lead time 1), not for gradient boosting on a
> brand-month panel. They are used here as a principled and citable partition of demand
> patterns, not as a claim that the same accuracy ordering holds for these models —
> which is itself a question the per-class results can address.

## 6.5 Results

<!-- REWRITTEN 2026-08-23 against the current results on disk: cv_metrics.csv,

### 6.5.1 Tabular-model benchmark

| Category | Model | CV WMAPE | Test WMAPE | Test medMAPE | n test |
|---|---|---:|---:|---:|---:|
| CSD | LightGBM | 17.0% | **14.5%** | 33.2% | 665 |
| CSD | XGBoost | 16.1% | 15.2% | 31.8% | 665 |
| danskvand | LightGBM | 17.9% | **20.5%** | 38.6% | 174 |
| danskvand | XGBoost | 17.1% | 20.9% | 35.8% | 174 |
| energidrikke | LightGBM | 10.6% | 16.5% | 34.7% | 308 |
| energidrikke | XGBoost | 10.6% | **13.0%** | 32.3% | 308 |
| RTD | LightGBM | 27.9% | **31.8%** | 38.1% | 372 |
| RTD | XGBoost | 28.0% | 36.1% | 32.8% | 372 |

### 6.5.2 The simple benchmarks, and where they win

| Category | Naive | Seasonal naive | Drift | Ridge | ARIMA | Prophet | Best tuned ML |
|---|---:|---:|---:|---:|---:|---:|---:|
| CSD | 42.9% | 19.2% | 47.7% | 19.4% | 21.8% | 105.7% | **14.5%** |
| danskvand | 32.5% | 35.9% | 32.0% | **10.9%** | 33.5% | 19.5% | 20.5% |
| energidrikke | 18.9% | 23.8% | 17.7% | 18.3% | 19.4% | 972.4% | **13.0%** |
| RTD | 89.3% | **27.3%** | 95.9% | 40.5% | 53.3% | 66.8% | 31.8% |

- **On RTD, seasonal naive beats every tuned configuration** — 27.3% against
- **On danskvand, a plain Ridge regression reaches 10.9%**, roughly half the tuned

### 6.5.3 Scaled error (MASE)

| Category | Naive MASE | Seasonal-naive MASE | Naive median ASE |
|---|---:|---:|---:|
| CSD | 0.95 | 1.63 | 0.39 |
| danskvand | 0.99 | 1.60 | 0.52 |
| energidrikke | 0.67 | 2.02 | 0.05 |
| RTD | **6.54** | 14.02 | 0.18 |

### 6.5.4 Pooled versus per-category training

| Category | LightGBM pooled → per-cat | XGBoost pooled → per-cat |
|---|---|---|
| CSD | 17.5% → 16.3% (per-cat better by 1.2 pp) | 16.6% → 15.3% (per-cat by 1.3) |
| danskvand | 21.4% → 23.7% (**pooling wins 2.2 pp**) | 18.9% → 21.5% (**pooling wins 2.5**) |
| energidrikke | 12.1% → 13.7% (**pooling wins 1.6**) | 12.5% → 13.9% (**pooling wins 1.4**) |
| RTD | 35.8% → 35.1% (per-cat by 0.7) | 37.0% → 35.5% (per-cat by 1.5) |

### 6.5.5 Results by demand pattern

### 6.5.6 Operational profile

> **The RAM figure in `fig4_ram_budget` is hardcoded and contradicts this table.**
> The figure is not cited above and requires regeneration before use.

### 6.5.7 Prediction-interval calibration

| Category | Nominal | Empirical coverage | Median relative width | n calib |
|---|---:|---:|---:|---:|
| CSD | 90% | 89.6% | 3.3× | 665 |
| RTD | 90% | 89.0% | 3.1× | 372 |
| danskvand | 90% | 87.4% | **16.8×** | 174 |
| energidrikke | 90% | 93.5% | **8.9×** | 264 |
| CSD | 80% | 78.6% | 1.9× | 665 |
| RTD | 80% | 76.1% | 1.7× | 372 |
| danskvand | 80% | 70.7% | 3.5× | 174 |
| energidrikke | 80% | 82.5% | 3.3× | 264 |

> **What the guarantee does and does not cover.** Split conformal provides
> **marginal** coverage — an average over cells, not a promise about any individual
> brand-month (Lei et al., 2018, Remark 3) — and it assumes **exchangeability**, which
> monthly brand demand violates. Barber et al. (2023) show unweighted split conformal
> can lose coverage materially under temporal drift, bounding the loss rather than
> eliminating it. **The coverage figures above are therefore an empirical measurement
> under known-violated assumptions, not a theoretical entitlement** — which is precisely
> why they are measured on a held-out test period instead of assumed.

### 6.5.8 Remaining gaps

- **The ≤15% accuracy target has been withdrawn, not scored.** Verification found the
- The tuning protocol is not nested, so every cross-validation figure above is
- ARIMA and Prophet use a fixed specification per series rather than a per-series
- `fig4_ram_budget` is stale and contradicts §6.5.6.

---

### 6.5.9 Forecast stability across seeds

| Category | Model | median CV | p90 CV | WMAPE mean | WMAPE sd |
|---|---|---:|---:|---:|---:|
| CSD | LightGBM | 0.112 | 0.295 | 15.4% | 0.65 |
| CSD | XGBoost | 0.123 | 0.422 | 15.1% | 0.59 |
| danskvand | LightGBM | 0.119 | 0.687 | 20.8% | 0.69 |
| danskvand | XGBoost | 0.124 | 0.539 | 21.8% | 1.04 |
| energidrikke | LightGBM | 0.174 | 0.634 | 14.1% | 1.18 |
| energidrikke | XGBoost | 0.174 | 0.730 | 13.9% | 0.79 |
| RTD | LightGBM | 0.125 | 0.397 | 33.5% | 1.64 |
| RTD | XGBoost | 0.104 | 0.400 | 35.1% | 0.92 |

| Category | Winner per seed | |
|---|---|---|
| CSD | XGBoost, XGBoost, LightGBM, XGBoost, LightGBM | **flips** |
| danskvand | LightGBM ×3, XGBoost, LightGBM | **flips** |
| energidrikke | LightGBM, LightGBM, XGBoost, LightGBM, LightGBM | **flips** |
| RTD | XGBoost, XGBoost, LightGBM, LightGBM, LightGBM | **flips** |

> **This is a limitation the thesis discovers about itself, and reporting it is the
> point.** Cawley and Talbot (2010) show that selecting on a noisy criterion produces
> apparent differences of a magnitude comparable to genuine differences between learning
> algorithms. That is exactly what a single-seed model comparison risks, and measuring
> the seed sensitivity is what distinguishes a reported selection from an artefact.

---

## 6.6 Model selection decision

- **The choice between LightGBM and XGBoost is not supported by this data.** A
- **The defensible claim is that the two are statistically indistinguishable here**, the
- **What the benchmark does support** is the gap between *families*: both gradient
- **The served model carries its own track record.** The forecast tool returns the
- **Metric disagreement is surfaced, not hidden.** Where WMAPE and median APE rank
- **Ensemble combination is evaluated as a separate scenario**, not folded into this

> **`brand × chain` is not a selectable dimension.** Any residual text implying a
> per-category *granularity* choice is obsolete — DEC-GRAIN fixed the grain at
> brand × month and P0035 removed the alternative from code, paths and results.

---

## 6.7 Connection to SRQs

| SRQ | How Ch.6 addresses it |
|---|---|
| SRQ1 | Direct answer: which models work best for retail CSD forecasting within ≤8GB RAM |
| SRQ2 | Prediction intervals + calibration coverage provide the raw confidence signal for SRQ2 |
| SRQ3 | Not addressed here; integration readiness is addressed in Ch3 and Ch5 |
| SRQ4 | Supplies the trained models and their measured accuracy to the scenario ladder; the models benchmarked here are what distinguishes the model-equipped scenarios from the data-only ones |

---

## Outstanding decisions

- ~~Exact train/validation/test dates pending Nielsen access~~ → data in hand; splits
- ~~HPO trial budget: 50 trials, may reduce under RAM pressure~~ → **100 trials**, and
- ~~Whether to add a 6th model~~ → four simple benchmarks added instead, which is the

- ~~Which metric the ≤15% benchmark refers to.~~ **Closed 2026-08-25**: the benchmark is
- **Whether ARIMA should be order-searched.** The fixed SARIMAX(1,1,1) is a floor for
- **Whether the ensemble scenario runs**, which determines whether §6.6's combination

---

## OPEN: MODEL-TRAINING PROSE MUST BE RE-CHECKED (P0044, 2026-09-01)

The served artefact changed on 2026-09-01. Every claim in this chapter about
*which model is served* and *what it costs* was written against the previous
configuration and needs verifying against the current one.

### What changed and why

- **Hyperparameters.** `train_and_persist.py` now reads `cv_params.json`
  (100 trials, 4-fold expanding-window CV, dual objective) instead of
  `tuned_params.json` (30 trials, ONE validation split, wMAPE only). The CV
  script was written specifically to fix the older design and its output had
  been consumed by nothing for two weeks (P0044 F27).
- **Selection was biased.** `best_model_for()` ranked candidates on
  `test_wmape` -- the held-out test set -- so the served model was chosen using
  the data this chapter then reports it against. Now selects on `cv_score`
  (expanding-window validation), so test is genuinely held out (F29).
- **RTD flipped: XGBoost -> LightGBM.** The other three categories keep XGBoost.

### Checks required in this chapter

| # | Check | Status |
|---|---|---|
| 1 | Any sentence naming the served model per category -- RTD is now LightGBM | TODO |
| 2 | The profiling table in §6.5 -- regenerated 2026-09-01, and the memory column now measures **process RSS**, not tracemalloc | TODO |
| 3 | The `fig4_ram_budget` figure -- already flagged stale; now also wrong on the RAM instrument | TODO |
| 4 | Any statement that the served config is "tuned" -- must say tuned **how** (30-trial vs CV), since both files exist | TODO |
| 5 | Selection-on-test: if the chapter describes the selection protocol, it must describe the CORRECTED one, and the bias should be disclosed as a fixed defect | TODO |

**The CV tables themselves are unaffected** -- they derive from `cv_metrics.csv`,
which did not change. Only claims about the *served artefact* need revisiting.

### Already correct -- do not "fix"

Line ~269 reports RTD LightGBM 27.9% vs XGBoost 28.0% in CV, and line ~358
already records RTD's selection as **"flips"** across seeds. The chapter had
identified RTD as the unstable category before the change; the flip is
consistent with what it already says.

### Memory instrument correction (F1)

The previous profiling table used `tracemalloc`, which sees only Python-level
allocations and reported **XGBoost at 0.1 MB** -- less than Ridge, and below the
3.7 MB the same model pickles to. LightGBM and XGBoost allocate in C++. Measured
by process RSS in isolated subprocesses:

| model | tracemalloc | **RSS** | pickled |
|---|---|---|---|
| Ridge | 5.5 MB | 5.4 MB | 0.0 MB |
| LightGBM | 23.0 MB | **36.8 MB** | 7.64 MB |
| XGBoost | **0.1 MB** | **26.6 MB** | 3.70 MB |
| ARIMA | 0.3 MB | 2.2 MB | n/a |

Any prose quoting the old figures, or claiming models fit in "tens of MB on
Python allocations", must be rewritten. The constraint claim survives easily:
36.8 MB is ~0.9% of the measured 4 GB sandbox.

### On-demand retraining (F28, F31) -- if this chapter or Ch9 discusses it

- refit on stored params: **2.93 s, 35.0 MB**
- re-tune, 100 trials x 4-fold CV, single cutoff: **417 s** -- **142x**
- Do **not** claim re-tuning is less accurate. Retracted (F21): varying only the
  Optuna seed on identical data moves test wMAPE by 3.97pp.
- 7-month parameter drift: **inconclusive** (F31). Mean gap -0.04pp; the
  +0.414 pp/month slope is carried by two opposite outliers on seven points and
  must not be cited.
- Defensible design: refit per query, re-tune on a schedule. State that the
  cadence was not empirically optimised.
