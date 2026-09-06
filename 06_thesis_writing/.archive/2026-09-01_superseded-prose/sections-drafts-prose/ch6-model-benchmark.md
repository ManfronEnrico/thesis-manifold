# Chapter 6 — Model Benchmark & Selection
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
| Exclude zero-actual rows | Median APE and MAPE only | Mathematical — APE is undefined there |
| *(nothing else)* | — | — |

**WMAPE and MASE are computed on every row.** Both are defined at zero actuals, so
neither requires an exclusion, and none is applied.

Irregular series are handled by **categorisation rather than removal** — see §6.4.4.

> **The one exclusion is not attributed to a source, and must not be.** Hyndman &
> Koehler (2006, p. 683) explicitly call excluding zero windows "an artificial solution
> that is impossible to apply in practical situations", recommending zero-stable metrics
> such as MASE instead — which is precisely why MASE is reported here. Dropping
> zero-actual rows from *percentage* statistics is unavoidable because the quantity does
> not exist; extending that exclusion to metrics that are well defined would be the
> practice they criticise.

### 6.4.3 Targets

- **Accuracy target: none imported from the literature.** Earlier drafts carried a
  ≤15% WMAPE target attributed to Ceran et al. (2024). Source-level verification
  (2026-08-25) found **no such benchmark in that paper**: the authors explicitly reject
  MAPE because their panel contains too many zero-demand observations for a percentage
  error to be well defined, and report WRMSSE, RMSE and MAE instead. The target is
  therefore withdrawn, and **no claim that an external accuracy target is met or
  approached should be written anywhere in the thesis**
- **What replaces it: the simple benchmarks of §6.2.0**, scored on this thesis's own
  test rows (§6.5.2). This is the stricter test and needs no cross-study metric
  alignment — a target borrowed from a daily product-store study with a 15-day horizon
  was never comparable to brand × month at H=3 in any case
- **Calibration target: ≥85% empirical coverage** for a nominal 90% interval —
  **and interval width must be reported alongside**, since an arbitrarily wide interval
  attains perfect coverage while carrying no decision-relevant information

---

### 6.4.4 Demand-pattern categorisation

Brand-level demand on this panel ranges from steady weekly sellers to series with long
gaps and highly variable order sizes. Reporting a single pooled accuracy figure across
that range obscures more than it conveys, and thresholding the difficult series away
would reproduce exactly the practice the metric literature objects to.

Each brand is therefore classified using the scheme of Syntetos, Boylan and Croston
(2005, p. 495), on two measured quantities with **derived** cut-offs:

- **p** — average inter-demand interval (periods per non-zero demand)
- **CV²** — squared coefficient of variation of **non-zero** demand sizes

| | CV² ≤ 0.49 | CV² > 0.49 |
|---|---|---|
| **p ≤ 1.32** | smooth | erratic |
| **p > 1.32** | intermittent | lumpy |

The thresholds are not tuned to this data: they mark where the relative accuracy
ordering of Croston's method, the Syntetos–Boylan Approximation and simple exponential
smoothing changes. Classification uses **train and validation periods only** — deriving
classes from test rows and then reporting test accuracy per class would leak.

Resulting distribution (230 brands):

| Category | smooth | erratic | intermittent | lumpy |
|---|---:|---:|---:|---:|
| CSD | 44 | 32 | 5 | 14 |
| RTD | 32 | 20 | 2 | 8 |
| energidrikke | 16 | 18 | 2 | 8 |
| danskvand | 16 | 9 | 3 | 1 |

**This categorises; it does not exclude.** Accuracy is reported per class, so weak
performance on lumpy series appears as a stated limitation rather than as an absence.
That is the response Syntetos and Boylan's own work recommends — their contribution is
estimators for such series, not advice to discard them.

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
stat_baselines.csv, mase.csv, pooled_summary.md, pooled_perbrand_summary.md,
demand_classes.md, calibration.csv, profiling.csv, stability.csv. The previous
version of this section was stale in both its numbers and its structure: it
reported pre-tuning values and carried a `brand x chain` column for a grain that
DEC-GRAIN and P0035 removed from code, paths and results. It was replaced rather
than patched. Every figure below is traceable to a named file. -->

All results are on the locked **brand × month** grain (DEC-GRAIN). The alternative
`brand × chain` representation, and the granularity comparison built on it, were
removed from the project by P0035 and no longer appear in this chapter.

### 6.5.1 Tabular-model benchmark

Both gradient-boosted models were tuned with Optuna (TPE, 100 trials) against an
expanding-window cross-validation objective, then scored once on the untouched
test split. Because WMAPE and median APE are minimised by different functionals
(§6.4.1), each model was tuned **twice** — once per objective — and both results
are reported. `cv_metrics.csv`.

**Tuned for WMAPE:**

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

**The two objectives select different models and produce different rankings.**
Tuning for median APE improves that metric and degrades WMAPE, as the theory in
§6.4.1 predicts: absolute-error loss is minimised by the median, while a pointwise
percentage error is minimised by a lower functional. On energidrikke the effect is
large — LightGBM tuned for medMAPE reaches 29.8% test WMAPE against 16.5% when
tuned for WMAPE. **A single "best model" number is therefore meaningless without
naming the objective it was tuned against**, which is why both are carried here.

**Validation-to-test movement is substantial and is not hidden.** energidrikke
tunes to 10.6% in cross-validation and lands at 13.0–16.5% on test; RTD moves the
other way on LightGBM. The gap is consistent with the selection bias documented in
§6.3.5 — this protocol is not nested, so the cross-validation figure is an
optimistically biased estimate of generalisation, to an unquantifiable degree
(Cawley & Talbot, 2010).

### 6.5.2 The simple benchmarks, and where they win

The four benchmarks of §6.2.0 were run on the same test rows. `stat_baselines.csv`.

| Category | Naive | Seasonal naive | Drift | Ridge | ARIMA | Prophet | Best tuned ML |
|---|---:|---:|---:|---:|---:|---:|---:|
| CSD | 42.9% | 19.2% | 47.7% | 19.4% | 21.8% | 105.7% | **14.5%** |
| danskvand | 32.5% | 35.9% | 32.0% | **10.9%** | 33.5% | 19.5% | 20.5% |
| energidrikke | 18.9% | 23.8% | 17.7% | 18.3% | 19.4% | 972.4% | **13.0%** |
| RTD | 89.3% | **27.3%** | 95.9% | 40.5% | 53.3% | 66.8% | 31.8% |

**Two categories are not won by the tuned models, and this is the most important
result in the section.**

- **On RTD, seasonal naive beats every tuned configuration** — 27.3% against
  31.8–36.1%. The most irregular category is the one where a method with no
  parameters wins.
- **On danskvand, a plain Ridge regression reaches 10.9%**, roughly half the tuned
  gradient-boosted error. danskvand is also the smallest panel (29 series, 174 test
  rows), where a high-capacity model has least to learn from.

This is precisely the outcome the benchmark rung exists to detect. Hyndman and
Athanasopoulos (2021, §5.2) recommend the simple methods as a standard against which
any new method must justify itself; here they are not a formality but a live
constraint, and reporting a headline ML number without them would have concealed
that the thesis's approach is beaten outright on half the categories.

**Prophet is applied outside its design regime and its numbers should not be read
as a defect of the method.** Taylor and Letham (2018) target daily business series
with multiple seasonalities and holiday effects; at month grain, weekly seasonality
does not exist, no holiday calendar is supplied, and yearly seasonality reduces to
about twelve observations. Fitting a linear trend on log-transformed short series
lets the trend extrapolate to extreme values on back-transformation, producing the
105.7% and 972.4% figures. **This is a limitation of the application, not of
Prophet**, and is reported as such.

**Ridge requires clipping to be reportable.** Unclipped, its energidrikke WMAPE is
2.8×10¹³ and its RTD WMAPE 2459%, because back-transformed linear extrapolation
diverges. The clipped variant is what appears above; the raw values are retained in
`stat_baselines.csv` because the instability is itself informative about linear
models on this panel.

### 6.5.3 Scaled error (MASE)

WMAPE compares models within a category but says nothing about whether a category is
forecastable at all. MASE answers that directly: below 1 beats the in-sample naive
forecast. `mase.csv`.

| Category | Naive MASE | Seasonal-naive MASE | Naive median ASE |
|---|---:|---:|---:|
| CSD | 0.95 | 1.63 | 0.39 |
| danskvand | 0.99 | 1.60 | 0.52 |
| energidrikke | 0.67 | 2.02 | 0.05 |
| RTD | **6.54** | 14.02 | 0.18 |

**RTD's mean MASE of 6.54 against a median ASE of 0.18 is a distributional finding,
not an accuracy one.** The typical RTD series is forecast *better* than naive; the
mean is carried by a small number of cells with very large scaled errors. Reporting
only the mean would describe RTD as catastrophically unforecastable, and only the
median would conceal that a few series are. **Both are reported for this reason.**

Seasonal naive scores worse than naive on MASE in every category while winning on
WMAPE for RTD — the two metrics weight differently (volume versus per-series
scale), and the disagreement is surfaced rather than resolved by picking one.

### 6.5.4 Pooled versus per-category training

Whether one model trained across all four categories beats four category-specific
models is SRQ1's central design question. Both arms use the same 12-feature
intersection, the same tuning protocol, and are scored on identical test rows, so
they differ only in which rows they were trained on. `pooled_summary.md`.

| Category | LightGBM pooled → per-cat | XGBoost pooled → per-cat |
|---|---|---|
| CSD | 17.5% → 16.3% (per-cat better by 1.2 pp) | 16.6% → 15.3% (per-cat by 1.3) |
| danskvand | 21.4% → 23.7% (**pooling wins 2.2 pp**) | 18.9% → 21.5% (**pooling wins 2.5**) |
| energidrikke | 12.1% → 13.7% (**pooling wins 1.6**) | 12.5% → 13.9% (**pooling wins 1.4**) |
| RTD | 35.8% → 35.1% (per-cat by 0.7) | 37.0% → 35.5% (per-cat by 1.5) |

**The answer is conditional, and the condition is data volume.** Pooling wins on the
two smallest panels (danskvand 174 test rows, energidrikke 308) and loses on the two
largest (CSD 665, RTD 372). This is the expected transfer-learning trade-off: a small
category borrows strength from the others, while a large one is diluted by them. The
pattern holds for both model families, which is what makes it a finding rather than
noise — though §6.5.9 shows the magnitudes here sit within seed noise, so the
*direction* is the claim, not the pp values.

**Per-brand, the aggregate conceals wide disagreement.** Broken out by demand class
(`pooled_perbrand_summary.md`), pooling helps between 44% and 64% of brands depending
on class and model — close to a coin flip everywhere. The aggregate deltas above are
small differences between two distributions that overlap heavily.

### 6.5.5 Results by demand pattern

Using the Syntetos–Boylan–Croston partition of §6.4.4, the 230 brands divide into
108 smooth, 79 erratic, 12 intermittent and 31 lumpy. **Nothing is excluded**;
irregular series are reported rather than filtered.

**The most informative fact here is an absence: 15 of the 31 lumpy brands have no
test signal at all** — their entire test window is zero. Pooling deltas for the
lumpy class are computed on the 16 that remain, and any per-brand percentage
statistic for the other 15 would be undefined. This is a property of the data that a
volume threshold would have hidden by removing the brands quietly; the categorisation
makes it visible and countable.

For the classes with signal, pooling win-rates run 46–55% (smooth), 51–64% (erratic)
and 44–56% (intermittent). **No demand class shows a decisive pooling effect.**

### 6.5.6 Operational profile

Peak RAM on the largest matrix is in single-digit megabytes for every model —
Ridge 5.5, LightGBM 8.0, XGBoost 0.1, ARIMA 0.3 MB — against the 8 GB sequential
budget of SRQ1. **The memory constraint is non-binding by three orders of magnitude
at this data scale**, which is a real answer to the research question and not a
missing measurement: the constraint that motivated the question does not bite here.

Latency is likewise immaterial: XGBoost fits in 0.97 s and predicts in 9.3 ms;
LightGBM fits in 2.04 s and predicts in 15.9 ms. `profiling.csv`.

> **The RAM figure in `fig4_ram_budget` is hardcoded and contradicts this table.**
> The figure is not cited above and requires regeneration before use.

### 6.5.7 Prediction-interval calibration

A split-conformal wrapper on the tuned model, calibrated on validation residuals in
log space, gives the following on the untouched test split. `calibration.csv`.

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

The half-width is the ⌈(n+1)(1−α)⌉/n empirical quantile of the calibration
residuals — Algorithm 2 of Lei et al. (2018) — not the nominal (1−α) quantile.
The finite-sample correction is what supports the distribution-free guarantee at
finite *n*.

**Coverage alone is the wrong success criterion, and this table shows why.** An
arbitrarily wide interval attains perfect coverage while carrying no decision-relevant
information. danskvand meets its 90% coverage target only with intervals spanning
roughly seventeen times the quantity being forecast, which no planner can act on.
**For danskvand and energidrikke, width — not coverage — is the binding constraint,
and both are reported as limitations rather than averaged into a "well-calibrated"
claim.** At the 80% level danskvand additionally undercovers, at 70.7%.

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
  benchmark does not exist in the cited source (§6.4.3). Accuracy is therefore assessed
  against the simple benchmarks of §6.5.2 alone, on which two of four categories are
  beaten outright.
- The tuning protocol is not nested, so every cross-validation figure above is
  optimistically biased by an unquantified amount (§6.3.5).
- ARIMA and Prophet use a fixed specification per series rather than a per-series
  order search, on cost grounds. Their figures are a competent baseline, not the
  best attainable from those families.
- `fig4_ram_budget` is stale and contradicts §6.5.6.

---


### 6.5.9 Forecast stability across seeds

Chapter 2 motivates evaluating the modelling substrate on accuracy, computational
efficiency **and stability**, and SRQ1's scope names stability as its fourth axis. This
section supplies that measurement, which had not previously been made.

Stability is measured as the **coefficient of variation of the forecast for each
(brand, month) cell across five random seeds**, with data, splits, features and protocol
held identical. Only the seed varies, driving Optuna's sampler and the models' own
stochastic elements.

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

**Two findings, and both matter more than the accuracy tables suggest.**

**First, aggregate stability flatters the system by roughly three times.** Aggregate
WMAPE moves by about 4.7% of its own level across seeds, while the *typical individual
forecast* moves by about 13%, and the ninetieth-percentile cell by 30–73%. Per-cell
movements partly cancel within a volume-weighted sum, so a planner reading one brand's
number experiences considerably more run-to-run variability than a headline metric
implies. **Both figures are therefore reported**; quoting only the aggregate would
understate instability threefold.

**Second, and more consequentially for this chapter: the winning model changes with the
seed in every category.**

| Category | Winner per seed | |
|---|---|---|
| CSD | XGBoost, XGBoost, LightGBM, XGBoost, LightGBM | **flips** |
| danskvand | LightGBM ×3, XGBoost, LightGBM | **flips** |
| energidrikke | LightGBM, LightGBM, XGBoost, LightGBM, LightGBM | **flips** |
| RTD | XGBoost, XGBoost, LightGBM, LightGBM, LightGBM | **flips** |

Every input is identical; only the random seed differs. **A per-category statement of
which gradient-boosting model is best is therefore not a finding** — it reports the
outcome of one seed. §6.6 states the conclusion this supports instead.

> **This is a limitation the thesis discovers about itself, and reporting it is the
> point.** Cawley and Talbot (2010) show that selecting on a noisy criterion produces
> apparent differences of a magnitude comparable to genuine differences between learning
> algorithms. That is exactly what a single-seed model comparison risks, and measuring
> the seed sensitivity is what distinguishes a reported selection from an artefact.

---

## 6.6 Model selection decision

- **The choice between LightGBM and XGBoost is not supported by this data.** A
  five-seed sweep with every input held identical shows **the winning model changes with
  the seed in all four categories** (§6.5.7). Naming a winner per category would be
  reporting one seed's outcome as a finding
- **The defensible claim is that the two are statistically indistinguishable here**, the
  between-seed spread exceeding the between-model difference. This is a weaker headline
  but a true one, and it is useful: a practitioner deciding what to deploy can choose on
  operational grounds — training time, memory, tooling — rather than accuracy
- **What the benchmark does support** is the gap between *families*: both gradient
  boosters clearly beat Ridge and ARIMA on most categories, and clearly lose to seasonal
  naive on RTD. Those differences exceed the seed noise; the LightGBM-vs-XGBoost one
  does not
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

- ~~Which metric the ≤15% benchmark refers to.~~ **Closed 2026-08-25**: the benchmark is
  not in the cited source at all; the target is withdrawn (§6.4.3)
- **Whether ARIMA should be order-searched.** The fixed SARIMAX(1,1,1) is a floor for
  the family, not its best performance, and the baseline comparison is weaker for it
- **Whether the ensemble scenario runs**, which determines whether §6.6's combination
  paragraph describes a result or a deferred option
