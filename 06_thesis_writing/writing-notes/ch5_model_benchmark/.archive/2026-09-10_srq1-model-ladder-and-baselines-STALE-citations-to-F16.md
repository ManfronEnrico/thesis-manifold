---
name: srq1-model-ladder-and-baselines
description: RULE - Why the SRQ1 model ladder contains the models it does, with the academic justification for each benchmark and the argument for narrowing to two tabular models.
category: reference
applies-to: [srq1, methodology, ch5, ch6]
triggers: [writing the SRQ1 methodology, justifying model selection, defending the baseline set]
created: 2026_08_22-12_00
updated: 2026_08_22-16_00
---

# SRQ1 — the model ladder and why each rung is there

Written for the methodology chapter. Every model in the comparison needs a reason
for being there; this is that reason, per model.

## The ladder

Ordered simplest → most complex. **Each rung must justify its added complexity
against the rung above it** — that ordering is itself the argument.

| Rung | Model | What it isolates |
|------|-------|------------------|
| 1 | Naive | the minimum any forecast must beat |
| 2 | Seasonal-naive | whether the model learned *seasonality* or just level |
| 3 | Drift | whether the model learned *trend* |
| 4 | Ridge | whether feature engineering alone suffices |
| 5 | ARIMA / Prophet | the classical time-series comparison |
| 6 | LightGBM / XGBoost | the tabular ML arm this thesis deploys |

## The academic justification — this is the standard set, not a choice

**The three simple benchmarks are convention, not decoration.** Verified at source
2026-08-23 (BM-01, BM-02, both Supported).

Hyndman & Athanasopoulos (*Forecasting: Principles and Practice*, 3rd ed., §5.2)
define mean, naive, seasonal-naive and drift as the four standard benchmarks. The
**verified** wording is:

> "Some forecasting methods are extremely simple and surprisingly effective. We will
> use four simple forecasting methods as benchmarks throughout this book." … "any
> forecasting methods we develop will be compared to these simple methods to ensure
> that the new method is better than these simple alternatives."

**An earlier draft of this note quoted them as saying these "are the best we can do"
for many series. That quote is not in §5.2** and has been removed — the actual text
says the opposite in emphasis ("sometimes one of these simple methods will be the
best forecasting method available; but in many cases, these methods will serve as
benchmarks"). Use the verified wording.

**Write the formulas out** (verified, §5.2), because a benchmark table is stronger
when the benchmark is defined rather than named:

| Method | Forecast |
|---|---|
| Mean | ŷ(T+h) = ȳ |
| Naive | ŷ(T+h) = y(T) |
| Seasonal naive | ŷ(T+h) = y(T+h−m(k+1)), m = seasonal period, k = ⌊(h−1)/m⌋ |
| Drift | ŷ(T+h) = y(T) + h·(y(T) − y(1))/(T−1) |

**M4 (Makridakis et al., 2018, p. 803)** supplies the empirical weight, and the
**precise** finding is worth quoting rather than paraphrasing: of six submitted pure
ML methods, **none** beat the statistical combination benchmark (Comb) and **only one**
beat Naïve2.

**Practical consequence for the defence:** a forecasting result reported without
these is treated as *unbenchmarked*. The first question an examiner asks is "is
this better than assuming next month equals last month?" If the thesis cannot
answer that in a table, the ML results have no floor to stand on.

**Seasonal-naive matters most for this data.** The panel is monthly beverage demand
with strong annual seasonality — exactly the structure seasonal-naive exploits with
zero parameters. It is the honest test of the claim "the model learned seasonality":
if a tuned gradient-boosting model cannot beat "same month last year," it has
learned noise. It costs nothing to compute, which makes its absence harder to
defend than its inclusion.

**Ridge is the less conventional inclusion, and it earns its place by isolating a
confound.** LightGBM beating ARIMA proves less than it appears to, because two
things differ at once: the tabular models have lag/rolling/calendar *features* that
ARIMA (univariate) does not, **and** they can model nonlinear interactions. Ridge
has the same 13 features and no interactions, so:

- **ARIMA → Ridge** = the *feature-engineering* premium
- **Ridge → GBM** = the *nonlinearity* premium

Without Ridge the thesis can only report a combined effect and attribute it to
whichever explanation it prefers. With Ridge, the attribution is measured. This is
the same one-variable-at-a-time discipline the SRQ4 scenario ladder uses, applied to
the modelling arm — worth pointing out explicitly, as it shows the design logic is
consistent across research questions.

Regularised linear models are also a standard tabular baseline in their own right
(Hastie, Tibshirani & Friedman, *ESL* ch. 3), so this is not an invented rung.

## The headline finding from adding these benchmarks

**Seasonal-naive beats every tuned model in the thesis on RTD**, and comes within
2–4pp on CSD. Measured 2026-08-22:

| Category | SeasonalNaive WMAPE | tuned GBM WMAPE | verdict |
|----------|--------------------:|----------------:|---------|
| CSD | 19.2% | 15.3–17.5% | GBM ahead 2–4pp |
| **RTD** | **27.3%** | **35.1–37.0%** | **seasonal-naive wins by ~8pp** |
| energidrikke | 23.8% | 12.1–13.9% | GBM ahead ~10pp |
| danskvand | 35.9% | 18.9–23.7% | GBM ahead ~12pp |

A zero-parameter benchmark — "same month last year" — beats 30-trial Optuna-tuned
XGBoost on RTD.

**This is consistent with the M4 finding, and must be worded as consistency rather
than reproduction (BM-05, verified 2026-08-23).**

M4 is 100,000 heterogeneous series across micro, macro, finance, industry and
demographic domains. **It contains no retail beverage category**, so it cannot and
does not establish anything about seasonal-naive versus ML *for this data*. Writing
"the M4 finding reproduced on this dataset" claims a validation M4 never performed.

**The defensible construction:**

> M4 established that pure machine-learning methods frequently fail to outperform
> simple statistical baselines (Makridakis et al., 2018, p. 803). Our RTD result —
> where seasonal-naive at 27.3% WMAPE beats every tuned model — is a concrete
> instance of that general pattern in a domain M4 did not cover.

**M4's other half matters too, and cuts the opposite way (BM-04).** The competition
was *won* by a **hybrid**: Smyl's exponential-smoothing/RNN, +9.4% over Comb; second
place was a combination of seven statistical methods with NN-derived weights. So M4
does not say "simple beats complex" — it says **pure ML underperformed while
combinations won**, which is an argument *for* `F_ensemble`, not against modelling.

Three readings, all of which belong in the prose:

1. **The advantage is conditional, not general.** Large on energidrikke and
   danskvand, marginal on CSD, negative on RTD. The thesis should claim a
   category-dependent advantage. This is a *more precise* claim than "ML wins",
   and precision is defensible where a general claim would not survive the table.
2. **RTD deserves a direct answer rather than a footnote.** Both arms sit near 35%
   WMAPE and the free benchmark beats them. Say plainly: RTD is the hardest
   category and the tabular approach does not help there. A stated limit reads as
   rigour; an unstated one that a reader finds reads as concealment.
3. **It corroborates the pooling result.** The categories where pooling helped
   (danskvand, energidrikke) are the same ones where ML most clearly beats
   seasonal-naive — those categories have learnable structure, RTD has less. Two
   independent analyses agreeing on which categories are tractable is worth stating
   explicitly.

### The same metric split appears again

On medMAPE seasonal-naive is poor (CSD 54.7%, RTD 89.4%, energidrikke 95.9%). Its
strength is confined to volume-weighted WMAPE, which means **seasonal-naive is
accurate on large brands and poor on typical ones** — structurally identical to the
pooled-vs-specialised finding.

Worth drawing together as a cross-cutting observation: **three separate analyses in
this thesis (pooling, per-brand, benchmarks) all found the same split between
volume-weighted and per-series accuracy.** That is a property of the data — a
handful of large brands carry most of the volume — and naming it once, early,
explains several later results at no extra cost.

It does not rescue RTD. WMAPE is the operational metric and RTD is where it loses.

## The Ridge arm — a specification bug worth reporting as methodology

Ridge was added to isolate nonlinearity from feature engineering. Getting it to work
uncovered a defect in the **feature matrix** that is worth a paragraph in the
methodology chapter, because it is a genuine and non-obvious limitation.

### The features are engineered for trees

`lag_1`, `lag_2`, `rolling_mean_4` etc. are in **raw units**. The target
`log_sales_units` is `log1p(sales_units)`. Fitting `log(y) ~ β·(raw lags)` asserts an
**additive** relationship where the true one is **multiplicative**.

**Trees are immune** — they split on rank order, so any monotone transform of a
feature is equivalent. LightGBM and XGBoost therefore perform well on exactly the
same columns, which is why the defect went unnoticed: no tree-based model could
have revealed it.

> **Verified at source, and cite it (TREE-03, Supported).** Hastie, Tibshirani &
> Friedman, *ESL* 2nd ed., p. 307: trees "are invariant under (strictly monotone)
> transformations of the individual predictors. As a result, scaling and/or more
> general transformations are not an issue". The extension to boosted ensembles
> (TREE-04) is Supported-by-inference: ensembles are built from rank-split trees, so
> the property propagates.
>
> **Do not let this drift one word further.** The invariance is to transforming the
> **predictors**. It does **NOT** hold for transforming the **target** — a
> neighbouring claim that is false (TREE-05, Contradicted). Leaf values are
> arithmetic means and 𝔼[log Y] ≠ log 𝔼[Y], and in boosting the target transform
> changes the loss and hence every pseudo-residual. **Logging the target affects
> LightGBM too**; what distinguishes Ridge here is the *mismatch* between raw-unit
> features and a logged target, not immunity to the log itself.

Diagnostic evidence, CSD:

| | log-space RMSE | WMAPE | medMAPE |
|---|---:|---:|---:|
| raw features | 3.92 | 1705% | 99.6% |
| **logged features** | **0.93** | **22.6%** | **29.5%** |

The decisive observation was that **log-space RMSE stayed at ~3.92 across seven
orders of magnitude of the regularisation parameter** (1e-4 to 1e3). No amount of
shrinkage fixes a wrong functional form. A medMAPE pinned at 99.6% meant the model
was predicting near-zero for essentially every brand.

**What to write:** the engineered feature matrix encodes an unstated modelling
assumption — that the learner is tree-based. Any future linear or neural model on
this matrix inherits the same trap. Stating this is more valuable than hiding it: it
is a concrete, measured instance of a design decision propagating silently into
downstream work.

### Which Ridge figures to cite — the answer is per-category

Both clipped and unclipped figures are published (DEC-RIDGE-BOTH). Publishing both
**refuted** an earlier assumption that the bound was propping up the good results:

| Category | unclipped | clipped | difference | clips |
|----------|----------:|--------:|-----------:|------:|
| CSD | 19.9% | 19.4% | 0.5pp | 59/665 |
| **danskvand** | **10.9%** | **10.9%** | **none** | 9/174 |
| energidrikke | 2.8×10¹³% | 18.3% | catastrophic | 46/308 |
| RTD | 2458.9% | 40.5% | catastrophic | 44/372 |

**On CSD and danskvand the bound is demonstrably inert** — the clipped and unclipped
figures agree, so those numbers describe Ridge itself. danskvand's 10.9% genuinely
beats every tuned GBM (18.9–23.7%), and that should be reported rather than
explained away.

**On energidrikke and RTD the method fails outright.** 2.8×10¹³% is not an accuracy
figure; it is a model that collapsed on at least one series and had the failure
amplified by `expm1`. Report the unclipped values there as *evidence of failure at
this sample size*, and state that the clipped variants are shown for completeness
only and are not comparable to the other models.

**The finding to write:** per-brand Ridge is legitimate on two categories and
unusable on two, with a mechanical explanation — at ~24 rows against 13 features the
design matrix is near-singular, so whether the fit extrapolates sanely depends on
how well-conditioned that category happens to be. That is a more useful statement
than either "Ridge works" or "Ridge is broken".

**A methodological point worth one sentence:** a clip *count* does not establish that
clipping changed a *result*. Only comparing bounded and unbounded output does. This
project initially inferred contamination from the clip rate alone and was wrong for
two of four categories.

**For the nonlinearity-premium argument, keep citing the pooled Ridge**
(`ridge_pooled.csv`, 21.5–25.1% within category), which is well-conditioned
everywhere and matches the GBMs' fitting regime. On that basis the nonlinearity
premium is roughly 5–8pp WMAPE on three of four categories.

### Fitting regime must be labelled in the results table

Not every model can be run every way, and the table should say so rather than
implying a uniform design.

| Method | Per-brand | Pooled | Why |
|--------|:---------:|:------:|-----|
| Naive, Seasonal-naive, Drift | ✓ | — | defined on *this* series' own history; a pooled version does not exist |
| ARIMA, Prophet | ✓ | — | univariate by construction: one series in, one series out |
| Ridge, LightGBM, XGBoost | ✓ | ✓ | take a feature table, so either regime is well-defined |

**This matters for interpretation:** the tabular models are fitted across all brands
in a category while ARIMA and Prophet are fitted per brand, so "GBM beats ARIMA"
conflates the *method* with *how much data each model saw*. The pooled Ridge row is
what separates them. Say this explicitly — an examiner comparing a pooled model
against per-series baselines will otherwise ask.

## Why the comparison narrows to two ML models — this must be in the write-up

**The narrowing is evidence-based and the evidence is on disk.** The comparison did
not begin with LightGBM and XGBoost; it began with a wider set, and the classical
methods lost decisively:

| Category | ARIMA medMAPE | Prophet medMAPE | Prophet WMAPE | tuned GBM WMAPE |
|----------|--------------:|----------------:|--------------:|----------------:|
| CSD | 58.5% | 63.1% | 105.7% | ~15–17% |
| danskvand | 48.4% | 37.1% | 19.5% | ~19–24% |
| energidrikke | 70.1% | 112.5% | **975.6%** | ~12–14% |
| RTD | 66.0% | 88.8% | 66.8% | ~35–37% |

Source: `04_thesis_results/srq1/stat_baselines.csv` and `tuned_metrics.csv`.

**State the narrowing explicitly rather than presenting two models as if they were
the only candidates considered.** The defensible phrasing:

> Six model families were evaluated. The classical univariate methods (ARIMA,
> Prophet) and the simple benchmarks were outperformed by a wide margin in every
> category, so the tuned comparison was carried forward on the two gradient-boosting
> implementations. The full baseline results are reported rather than discarded, so
> the narrowing is auditable.

A reader who sees only LightGBM and XGBoost assumes convenience. A reader who sees
the baseline table sees a decision with evidence behind it. **Report the losing
models' numbers** — that is what converts a narrowing into a finding.

### Two caveats on the baseline numbers themselves

1. **Prefer medMAPE over WMAPE for the per-series statistical baselines.** WMAPE is
   volume-weighted and unbounded above, so a single diverged series sets the
   category figure — CSD Prophet's WMAPE is 60% attributable to one brand (P0038
   F72), and energidrikke Prophet's 975.6% is not a meaningful accuracy statement.
   Reporting that number without the caveat invites a fair objection.
2. **Prophet's failure is partly a fit-to-purpose problem, not only an accuracy
   result.** On ~30 monthly observations per brand, Prophet's design advantages are
   largely unavailable. Say so — it is a more honest account than "Prophet is bad,"
   and it strengthens rather than weakens the case for the tabular approach.

   **Word this carefully (PRO-04/PRO-05, verified 2026-08-23).** Taylor & Letham
   (2018, *The American Statistician* 72(1), 37–45) **do not** state Prophet is
   unsuitable for monthly data, and they **do not** show it produces flat forecasts.
   Both are overstatements that a reader checking the source would catch.

   **The mechanical argument is available and is stronger anyway**, because it
   explains rather than asserts. Prophet is `y(t) = g(t) + s(t) + h(t) + ε` (p. 38),
   built for "piecewise trends, multiple seasonality, floating holidays" in
   high-frequency business series. On monthly data:

   - **weekly seasonality does not exist** — the Fourier machinery has nothing to fit;
   - **holiday windows collapse** — sub-daily/multi-day effects are invisible at
     month grain, and we supply no holiday calendar at all;
   - **yearly seasonality reduces to ~12 points**, which the tabular models capture
     directly through `month`, `quarter` and `lag_13`.

   What remains is a piecewise trend plus a coarse annual term, estimated on ~30
   observations. **So the honest claim is that we applied Prophet outside the regime
   its design targets** — a limitation of our application, not a defect the authors
   documented.

## Related

- `srq1-pooled-vs-per-category.md` — the pooled/specialised result
- `04_thesis_results/srq1/stat_baselines.md` — the baseline table
- `04_thesis_results/srq1/tuned_summary.md` — the tabular arm
- `plans/P0040_2026-08-20_prometheus-scenarios-d-e/findings.md` — F52–F63
