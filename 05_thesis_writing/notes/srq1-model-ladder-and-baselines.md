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

**The three simple benchmarks are convention, not decoration.** Hyndman &
Athanasopoulos (*Forecasting: Principles and Practice*, 3rd ed., §5.2) define
naive, seasonal-naive, drift and mean as *the* standard benchmark methods, stating
that these "are the best we can do" for many series and that any forecasting method
should be compared against them. The M-competitions (Makridakis, Spiliotis &
Assimakopoulos 2018, 2020) score every entrant against naive and seasonal-naive as
the reference point, and the M4 paper's central finding — that many sophisticated
methods fail to beat simple benchmarks — is precisely why their omission is
conspicuous.

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

**This is the M4 finding (Makridakis et al. 2018) reproduced on this dataset**, and
reporting it is not optional: it is the first thing an examiner checks and the
reason the benchmark set is standard. Three readings, all of which belong in the
prose:

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
   result.** Prophet is designed for daily/sub-daily series with multiple
   seasonalities and holiday effects; on ~30 monthly observations per brand it is
   outside its design range. Say so — it is a more honest account than "Prophet is
   bad," and it strengthens rather than weakens the case for the tabular approach.

## Related

- `srq1-pooled-vs-per-category.md` — the pooled/specialised result
- `04_thesis_results/srq1/stat_baselines.md` — the baseline table
- `04_thesis_results/srq1/tuned_summary.md` — the tabular arm
- `plans/P0040_2026-08-20_prometheus-scenarios-d-e/findings.md` — F52–F63
