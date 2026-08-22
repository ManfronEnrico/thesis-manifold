# Chapter 6 — Model Benchmark & Selection
> **Status: §6.1–6.4 REVISED 2026-08-23** against the source-verified citation register
> (P0041) and the current results on disk. §6.5 accuracy tables are **STALE** — every
> figure predates the 2026-08 CV-tuning work and the `brand × chain` grain was removed
> by DEC-GRAIN/P0035, so those tables are structurally obsolete, not merely out of date.
> Rewriting §6.5 is tracked separately.
>
> **Every citation in §6.1–6.4 is `VERIFIED` in the register** unless explicitly marked
> otherwise. Do not add a citation here that has not been source-checked.
> Last updated: 2026-08-23

---

## 6.1 Rationale for model selection

- **Five model families span the inductive-bias spectrum**: classical statistical
  (ARIMA, Prophet), gradient boosting (LightGBM, XGBoost), regularised linear (Ridge),
  plus four parameter-free benchmarks (mean, naive, seasonal-naive, drift)
- **Selection criteria**: (a) established empirical performance on retail/FMCG panels;
  (b) fit within the ≤8 GB sequential RAM budget; (c) interpretability sufficient for
  the SRQ4 scenario comparison; (d) diversity of inductive bias
- **The benchmark rung is required, not decorative.** Hyndman & Athanasopoulos (2021,
  §5.2) define the four simple methods as benchmarks against which "any forecasting
  methods we develop will be compared … to ensure that the new method is better than
  these simple alternatives". A forecasting result reported without them is
  unbenchmarked
- **Empirical weight for that requirement** comes from M4: of six pure machine-learning
  entries, none beat the statistical combination benchmark and only one beat Naïve2
  (Makridakis et al., 2018, p. 803)
- **NOT included, and why**: deep sequence models (LSTM/N-BEATS) — RAM footprint
  incompatible with the ≤8 GB constraint, and infeasible under the HPO time budget on
  ~30 monthly observations per series

> **A caution carried from M4 into Chapter 9.** M4's headline is often compressed to
> "machine learning failed". That is not what it found. The competition was **won by a
> hybrid** — Smyl's exponential-smoothing/RNN, 9.4% better than the combination
> benchmark — with a seven-method statistical combination second (Makridakis et al.,
> 2018, p. 803). The finding is that *pure* ML underperformed while *combinations* won,
> which is an argument for the ensemble scenario rather than against modelling.

---

## 6.2 Model descriptions

### 6.2.0 Simple benchmarks

Four parameter-free methods, defined as in Hyndman & Athanasopoulos (2021, §5.2):

| Method | Forecast for horizon *h* |
|---|---|
| Mean | ŷ(T+h) = ȳ |
| Naive | ŷ(T+h) = y(T) |
| Seasonal naive | ŷ(T+h) = y(T+h−m(k+1)), with *m* the seasonal period and *k* = ⌊(h−1)/m⌋ |
| Drift | ŷ(T+h) = y(T) + h · (y(T) − y(1)) / (T−1) |

- **Seasonal naive is the decisive one for this panel.** Monthly beverage demand has
  strong annual seasonality, which seasonal naive exploits with zero parameters. It is
  the direct test of whether a tuned model has learned seasonality or merely fitted it

### 6.2.1 ARIMA
- Classical univariate time-series model in the Box–Jenkins framework
- Role: statistical baseline representing established traditional forecasting
- **Implementation: `statsmodels` `SARIMAX(order=(1,1,1))` on log sales, fitted per
  brand.** A fixed order, not a search — `pmdarima`/`auto_arima` was unavailable in the
  environment. **This is a stated limitation**: ARIMA is not order-optimised, so its
  numbers are a floor for the family rather than its best achievable performance
- RAM: ~0.5 MB measured; negligible
- Limitation: assumes stationarity; univariate, so no promotional or calendar inputs

### 6.2.2 Prophet (Meta)
- Additive decomposable model, **y(t) = g(t) + s(t) + h(t) + ε** — trend, seasonality,
  holidays (Taylor & Letham, 2018, p. 38, Eq. 1)
- Designed for forecasting at scale by analysts with domain rather than statistical
  expertise, targeting "piecewise trends, multiple seasonality, floating holidays"
  (pp. 37–38)
- **No holiday calendar is supplied in this thesis**, and none of the multi-seasonality
  machinery applies at month grain
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
  equivalently RSS subject to Σβ² ≤ t (Hastie et al., 2009, pp. 61–62, Eq. 3.41–3.42)
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
  dropped; they are reported as a limitation and future work, not as a live dimension
- Temporal train/validation/test split, no shuffling
- Horizon **H = 3** months
- Test-set sizes: CSD 665 rows, RTD 372, energidrikke 308, danskvand 174

### 6.3.2 Feature engineering
- **Lags**: t−1, t−2, t−3, t−4, t−8, t−13 months
- **Rolling statistics**: 4-month and 13-month mean; 4-month standard deviation
- **Calendar**: `month`, `quarter`, and a binary `peak_month` flag derived from the
  category's own seasonal profile (months whose mean units exceed the category mean by
  more than 10%). **No holiday calendar is used** — the flag is measured from the sales
  distribution, not from calendar dates
- **Promotional**: `promo_intensity` (promotional share of units, clipped to [0,1],
  lagged one period). **Available for CSD and energidrikke only** — Nielsen reports no
  promotional measure for danskvand or RTD, so the feature is omitted rather than
  zero-filled, since a constant zero would assert that no promotion ran
- Missing lag values for short histories are left as NaN (handled natively by the tree
  models); Ridge receives a zero-fill at fit time

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

Hyperparameters are selected by **4-fold expanding-window (rolling-origin)
cross-validation**, splitting on distinct **periods** rather than rows — the rows are
brand-months, so a row-wise split would place the same month in training and validation
for different brands. The training window grows forward and validation is the block
immediately following it, so no model ever sees a period later than the one it predicts.
The test split is untouched throughout.

Rolling-origin evaluation successively advances the forecast origin instead of relying
on a single split, which is vulnerable to "corruption by occurrences unique to that
origin" (Tashman, 2000, p. 439). Because each fold refits from scratch, this is
**recalibration** rather than mere updating — Tashman's preferred procedure (p. 440).

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

Optuna's TPE sampler, **100 trials** per model × category × objective. TPE models the
configuration density conditional on performance, splitting observed trials into
densities *l(x)* below and *g(x)* above a quantile threshold (Bergstra et al., 2011,
p. 2549). Optuna supplies the define-by-run interface, sampling and pruning
infrastructure (Akiba et al., 2019, p. 2623).

> **Two attributions kept separate**: Bergstra et al. (2011) for the mathematics of TPE,
> Akiba et al. (2019) for the software. The Optuna paper does not formulate TPE — it
> attributes the algorithm to Bergstra.

**The trial budget is justified empirically, not by convention.** No trial-count
convention exists in the HPO literature; the requirement scales with search-space
dimensionality. The tuner therefore records the running best CV score per trial and
reports the trial after which improvement becomes negligible. Measured plateaus range
from 3 to 87 trials with a median near 16, so 100 trials comfortably contains the
converged region for every configuration.

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

**Plain mean MAPE is not reported.** It is undefined against a zero actual and
diverges to meaningless magnitudes near zero — on this panel it reaches 10¹³ — because
percentage errors are "infinite or undefined if Yₜ = 0 … and have an extremely skewed
distribution when any value of Yₜ is close to zero" (Hyndman & Koehler, 2006, p. 683).

### 6.4.1 Why WMAPE is the primary metric

The choice is not conventional but theoretical. A scoring function determines *which
functional of the predictive distribution* an optimal forecast reports (Gneiting, 2011):

- absolute-error loss is minimised by the **median** (p. 746);
- pointwise absolute *percentage* error is minimised by the **(−1)-median** — a density
  reweighted by y⁻¹ — which biases forecasts systematically downward (pp. 746, 752);
- WMAPE aggregates absolute errors *before* dividing by total volume, so minimising it
  over a fixed evaluation sample is equivalent to minimising MAE, and is therefore
  consistent for the **standard median**.

**This predicts, rather than merely describes, the WMAPE/median-APE divergence reported
throughout this chapter.** The two metrics estimate different functionals, so agreement
was never to be expected. It also explains why tuning against median APE costs 8–13 pp
of WMAPE while buying only 2–3 pp of median APE: that objective targets the
(−1)-median and underforecasts, which WMAPE penalises directly.

> One step is ours rather than Gneiting's: he does not use the term WMAPE. The bridge is
> algebraic — Σ\|yₜ\| is constant across candidate models on a fixed evaluation sample,
> so minimising WMAPE is minimising Σ\|error\|.

### 6.4.2 Scorability, and what is excluded from what

Between 14% and 29% of test rows per category have a zero actual, where APE is
undefined. Two distinct decisions follow, and they are **not** the same rule:

| Rule | Applies to | Basis |
|---|---|---|
| Exclude zero-actual rows | Median APE and MAPE only | Mathematical — APE is undefined |
| Volume floor of 1 unit/month | Per-brand WMAPE comparisons only | **Declared design choice** — see below |

WMAPE and MASE are computed on **all** rows; neither needs an exclusion.

The volume floor exists because per-brand WMAPE on brands averaging under one unit per
month produces deltas in the thousands of percentage points — division by an almost
empty denominator rather than evidence. It is stated with its row counts wherever
applied.

> **Neither exclusion is attributed to a source, and neither may be.** Hyndman & Koehler
> (2006, p. 683) explicitly call excluding zero windows "an artificial solution that is
> impossible to apply in practical situations", recommending zero-stable metrics such as
> MASE instead — which is why MASE is reported. Likewise Syntetos and Boylan (2005)
> propose specialised estimators for intermittent series rather than discarding them.
> **The literature objects to silent exclusion; a declared, quantified inclusion
> criterion is a different thing, and that is what these are.**

### 6.4.3 Targets

- **Accuracy target: ≤15% WMAPE**, taken from the retail demand-forecasting literature.
  ⚠️ **The source's metric is not yet verified.** If the cited benchmark refers to plain
  or median MAPE rather than WMAPE, this thesis meets it on no category. Until that is
  confirmed, no claim that the target is met should be written
- **Calibration target: ≥85% empirical coverage** for a nominal 90% interval —
  **and interval width must be reported alongside**, since an arbitrarily wide interval
  attains perfect coverage while carrying no decision-relevant information

---

## 6.5 Results

> ## ⚠️ EVERY NUMBER IN §6.5.1–§6.5.3 AND §6.5.6 IS STALE — DO NOT CITE
>
> These tables were produced before the 2026-08 tuning work and **contradict every
> current results file**. Two independent problems:
>
> 1. **The values are wrong.** Current best WMAPE per category (`cv_metrics.csv`,
>    100-trial CV-tuned) is **CSD 14.5%** (LightGBM), **energidrikke 13.0%** (XGBoost),
>    **danskvand 20.5%** (LightGBM), **RTD 31.8%** (LightGBM). The chapter claims 16.5 /
>    11.4 / 23.8 / 31.0 and attributes all four to XGBoost.
> 2. **The structure is obsolete.** The `brand × chain` column and the entire
>    granularity finding (§6.5.2, §6.5.6) refer to a grain **removed by DEC-GRAIN and
>    P0035**. This cannot be fixed by updating numbers — those tables have a column that
>    no longer exists.
>
> **Also missing entirely**: the four simple benchmarks (§6.2.0), the finding that
> **seasonal naive beats every tuned model on RTD** (27.3% vs 31.8–36.1%), the
> pooled-versus-per-category comparison, MASE, and the dual-objective result.
>
> §6.1–6.4 have been revised and are current. §6.5 requires a rewrite against
> `cv_metrics.csv`, `stat_baselines.csv`, `mase.csv`, `pooled_summary.md` and
> `stability.md`, not a patch.


### 6.5.1 Tabular-model benchmark

<!-- Approved by Enrico 2026-06-24. All numbers are factual, from the committed,
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

### 6.5.2 Granularity finding

Disaggregating to a retail-chain dimension multiplies training rows ~6× but does
**not** uniformly improve accuracy — the gain is category-dependent: brand×month
wins for CSD, energidrikke and RTD (less noise per series), while brand×chain wins
for danskvand. This refutes a naïve "more rows is always better" assumption and is
explained by the signal-to-noise trade-off of finer granularity (see
`fig2_granularity.png`). energidrikke reaches **11.4% WMAPE**, near the ≤15%
industry target.

### 6.5.3 Statistical baselines and the SRQ4 comparison

<!-- Approved by Enrico 2026-06-24. Numbers factual, from scripts/srq1_baselines_stat.py;
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

### 6.5.4 Operational profile and calibration

<!-- Approved by Enrico 2026-06-24. Numbers from scripts/srq1_profiling.py and
srq1_calibration.py; results _05_results_srq1/profiling.* and calibration.*. -->

**Operational cost (≤8 GB claim).** Peak RAM (tracemalloc) on the largest matrix is
in the tens of MB for every model — Ridge 1.5, LightGBM 18.7, XGBoost 0.2, ARIMA
0.5 MB — i.e. orders of magnitude under the 8 GB sequential budget; the constraint
is non-binding at this data scale. Latency: XGBoost trains in ~1.7 s and predicts
in ~16 ms; LightGBM ~7.7 s (its tuned `n_estimators`); ARIMA is per-series.

**Prediction-interval calibration (SRQ2).** *(Revised 2026-08-23 — current.)*

A split-conformal wrapper on the tuned XGBoost, with the half-width calibrated on
validation residuals in log space, gives the following on the untouched test split:

| Category | Nominal | Empirical coverage | Median relative width |
|---|---|---:|---:|
| CSD | 90% | 89.6% | 3.3× |
| RTD | 90% | 89.0% | 3.1× |
| danskvand | 90% | 87.4% | **16.8×** |
| energidrikke | 90% | 93.5% | **8.9×** |

The interval half-width is the ⌈(n+1)(1−α)⌉/n empirical quantile of the calibration
residuals — Algorithm 2 of Lei et al. (2018) — not the nominal (1−α) quantile. The
finite-sample correction is what supports the distribution-free guarantee at finite *n*.

**Coverage alone is the wrong success criterion, and this table shows why.** An
arbitrarily wide interval attains perfect coverage while carrying no decision-relevant
information. danskvand meets its coverage target only with intervals spanning roughly
seventeen times the quantity being forecast, which no planner can act on. **For
danskvand and energidrikke, width — not coverage — is the binding constraint, and both
are reported as limitations rather than averaged into a "well-calibrated" claim.**

> **What the guarantee does and does not cover.** Split conformal provides
> **marginal** coverage — an average over cells, not a promise about any individual
> brand-month (Lei et al., 2018, Remark 3) — and it assumes **exchangeability**, which
> monthly brand demand violates. Barber et al. (2023) show unweighted split conformal
> can lose coverage materially under temporal drift, bounding the loss rather than
> eliminating it. **The coverage figures above are therefore an empirical measurement
> under known-violated assumptions, not a theoretical entitlement** — which is precisely
> why they are measured on a held-out test period instead of assumed.

### 6.5.5 Remaining gaps
- ARIMA / Prophet are profiled per-series; a full per-series statistical sweep is
  not run for every brand (cost) — the reported baselines use the protocol in §6.5.3.
- Mean-MAPE and mean interval-width are omitted (degenerate on low-volume series);
  WMAPE, median per-series MAPE, and empirical coverage are the reported metrics.

### 6.5.6 Selected configuration per category

<!-- Approved by Enrico 2026-06-24. The thesis adopts the best (model × granularity)
configuration PER category rather than one global setting — consistent with the
specialised-models finding. Numbers from _05_results_srq1/tuned_summary.md. -->

Because the granularity gain is category-dependent (§6.5.2), the thesis does **not**
impose a single global representation. Instead it selects, for each category, the
(model × granularity) configuration with the lowest test WMAPE — a per-category
specialisation directly consistent with the SRQ1 finding that category-specific
models outperform a one-size-fits-all setup. The retained configurations are:

| Category | Selected model | Selected granularity | Test WMAPE |
|---|---|---|---|
| CSD | XGBoost | brand × month | **16.5%** |
| danskvand | XGBoost | brand × chain | **22.0%** |
| energidrikke | XGBoost | brand × month | **11.4%** |
| RTD | XGBoost | brand × month | **31.0%** |

XGBoost is the model of choice in every category; three categories forecast best at
the aggregated brand×month level, while danskvand benefits from the finer
brand×chain representation. Both matrix granularities are retained in the
repository (`_03`, `_04`) so each category is trained on its selected one; the
pipeline and feature set are identical across categories, so the comparison remains
controlled. This mixed-granularity selection is a deliberate methodological choice,
stated as such, not an inconsistency.

---

## 6.6 Model selection decision

- **Selection is per category.** No single model wins everywhere: LightGBM takes CSD,
  danskvand and RTD on WMAPE; XGBoost takes energidrikke. This is the expected outcome
  given that no single method dominates across demand patterns
- **The served model carries its own track record.** The forecast tool returns the
  selected model's measured accuracy (WMAPE and median APE), both simple baselines for
  that category, and a conformal interval — so the consuming agent receives the
  forecast's reliability alongside the forecast
- **Metric disagreement is surfaced, not hidden.** Where WMAPE and median APE rank
  models differently, the payload flags it rather than silently reporting one
- **Ensemble combination is evaluated as a separate scenario**, not folded into this
  chapter's selection. M4's evidence that combinations outperform single models
  (Makridakis et al., 2018) motivates it, and treating it as its own rung is what makes
  the contribution measurable rather than assumed

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

**Resolved since this list was written** — retained so the reasoning is traceable:

- ~~Exact train/validation/test dates pending Nielsen access~~ → data in hand; splits
  fixed, test sizes stated in §6.3.1
- ~~HPO trial budget: 50 trials, may reduce under RAM pressure~~ → **100 trials**, and
  RAM was never the binding constraint (peak in the tens of MB against an 8 GB budget)
- ~~Whether to add a 6th model~~ → four simple benchmarks added instead, which is the
  standard set and answers the "is it better than doing nothing" question directly

**Genuinely open:**

- **Which metric the ≤15% benchmark refers to.** If the source reports plain or median
  MAPE rather than WMAPE, no category meets the target. Blocks any claim in §6.4.3
- **Whether to replace the 1 unit/month volume floor with the Syntetos–Boylan–Croston
  demand quadrants** (p = 1.32, CV² = 0.49). This would substitute a citable
  categorisation for a threshold chosen by judgement, and would let accuracy be reported
  per demand pattern — a more informative result than a single pooled figure
- **Whether ARIMA should be order-searched.** The fixed SARIMAX(1,1,1) is a floor for
  the family, not its best performance, and the baseline comparison is weaker for it
- **Whether the ensemble scenario runs**, which determines whether §6.6's combination
  paragraph describes a result or a deferred option
