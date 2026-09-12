---
name: book-scan-log
description: STATE - Section-by-section record of the full Hyndman & Athanasopoulos (2021) scan. Written BEFORE looking at the repo, so the standard is derived from the source rather than reverse-engineered from what was built.
pid: P0055
created: 2026_09_13-00_00
updated: 2026_09_13-00_00
status: in_progress
---

# The book scan — 41 sections, read end to end

## Method, and why the order matters

**Sections are read first, in full. The repo is not consulted until the standard
is written.**

That ordering is the whole point. The previous analysis anchored on what the
code does and then asked whether the book permitted it, which is how a
post-hoc justification gets mistaken for a methodology. The prose in Chapters 4
and 5 describes what was built; it is evidence of what the thesis *claims*, not
evidence of what forecasting practice *requires*. The book arrived after the
methodology was already committed.

**Two standards are recorded per finding:**

1. **Unconstrained** — what the source says best practice is, with no regard to
   this panel, this timeline or this codebase.
2. **Feasible** — what is achievable here, and the named gap between the two.

The gap between them is the limitations section, written for free.

## Scope decision (Brian, 2026-09-12)

| | |
|---|---|
| **In scope** | Feature engineering, data assessment, and the prediction methodology feeding the matrix |
| **Out of scope by decision** | The model roster. The same 4-5 families stay, because changing them touches already-cited and reviewed sources |
| **Recorded but not acted on** | Model-specification findings (ARIMA order, missing ETS, combination). Logged for the limitations section; **not** dropped |

**Note on the exclusion.** Model-specification findings are recorded because the
code-as-action arms in the funded run used exponential smoothing and seasonal
ARIMA on *every single run* and performed far better. That is evidence the
roster matters, even though the roster is not being changed here.

## Verdict vocabulary

| Verdict | Meaning |
|---|---|
| **CONFIRMS** | The source supports what was done. Keep, and now it has a real citation |
| **REFINES** | Broadly right, but the source specifies something sharper |
| **CONTRADICTS** | The source says otherwise. A defect |
| **SILENT** | The source does not address it. Our choice stands on its own reasoning |
| **NEW** | The source requires something not present at all |

---

# Section findings

## §2.3 Time series patterns — **the organising principle**

**Read 2026-09-13.** Bearing: **high**, and it sets the frame for everything.

The decisive sentence:

> "When choosing a forecasting method, we will first need to **identify the time
> series patterns in the data**, and then **choose a method that is able to
> capture the patterns properly**."

**Pattern identification drives method choice.** That is the opposite ordering
from a pipeline that fixes a model roster and then describes the data.

Definitions that constrain what may be claimed:

- **Trend** — long-term increase or decrease, *need not be linear*.
- **Seasonal** — "always of a **fixed and known period**", tied to the calendar.
  One series may carry more than one seasonal pattern.
- **Cyclic** — rises and falls **not** of fixed frequency, "usually at least
  2 years" in duration.

**Consequence for a 39-46 month panel:** a cyclic claim is unsupportable at this
length — two cycles minimum would consume the entire panel. Any non-seasonal
fluctuation must be called what it is, and not dressed up as a cycle.

**Standard (unconstrained):** identify trend, seasonality and cyclicity per
series *first*; select methods that can represent what was found.

**Standard (feasible):** the identification step is cheap and mostly already
performed. What is missing is the *link* from identification to method choice.

---

## §2.8 Autocorrelation — **a concrete, checkable defect candidate**

**Read 2026-09-13.** Bearing: **high**.

The ACF is defined explicitly, and two diagnostic readings are given:

> "When data have a trend, the autocorrelations for small lags tend to be large
> and positive… the ACF of a trended time series tends to have positive values
> that **slowly decrease** as the lags increase."

> "When data are seasonal, the autocorrelations will be **larger for the
> seasonal lags (at multiples of the seasonal period)** than for other lags."

### ⚠ FLAG — the lag set may be misaligned with the seasonal period

For **monthly** data the seasonal period is **m = 12**, so seasonal lags fall at
12, 24, 36. The thesis lag set is **1, 2, 3, 4, 8, 13** with rolling windows at
4 and 13.

**13 is not a multiple of 12.** If 13 was chosen as "the annual lag", the source
says the annual lag is 12. The thesis reports the pooled brand-demeaned lag-13
autocorrelation as **mildly negative** (−0.16), and describes it as "a mild
negative annual carry" — which is exactly what you would expect from probing one
month *past* the seasonal peak rather than at it.

**To check against the repo later:** is 13 justified by the Nielsen 4-4-5
calendar (where a "year" may not be 12 periods), or was it chosen without a
seasonal-period argument? **If 4-4-5 justifies it, this is CONFIRMS and the
justification must appear in the prose. If not, it is CONTRADICTS and the lag
set is probing the wrong lag.**

This is the single most actionable feature-engineering finding so far, and it is
exactly the kind of thing a title-only analysis could not have found.

**Standard (unconstrained):** lag selection is driven by the measured ACF and by
the seasonal period, with seasonal lags at multiples of m.

**Standard (feasible):** fully feasible. Computing the ACF at 12 as well as 13
costs nothing and settles the question empirically.

---

## §4.3 STL features — read earlier this session

Bearing: **high**. Gives directly implementable per-series features with exact
formulae:

- **Trend strength** `F_T = max(0, 1 − Var(R_t)/Var(T_t + R_t))`
- **Seasonal strength** `F_S = max(0, 1 − Var(R_t)/Var(S_t + R_t))`

Both bounded 0-1. Also `seasonal_peak_year`, `seasonal_trough_year`,
`spikiness`, `linearity`, `curvature`, `stl_e_acf1`, `stl_e_acf10`.

Stated use case is **exactly** this panel's shape: "when you have a large
collection of time series, and you need to find the series with the most trend
or the most seasonality."

**Standard (unconstrained):** STL-derived features are standard practice for
characterising a collection of series.
**Standard (feasible):** fully feasible; must be computed within the
time-safety boundary (train+val only, shifted by the horizon).

---

## §5.4 Residual diagnostics — read earlier this session

Bearing: **high**, and it supplies the **test that gates the whole plan**.

Required properties of innovation residuals:

1. **Uncorrelated.** "If there are correlations between innovation residuals,
   then there is **information left in the residuals which should be used in
   computing forecasts**."
2. **Zero mean**, else the forecasts are biased (and the fix is trivial: add the
   mean).

Useful but not required: constant variance, normality. "Sometimes applying a
**Box-Cox transformation** may assist with these properties."

Formal test: **Ljung-Box**, `Q* = T(T+2) Σ (T−k)^−1 r_k²`, with
**ℓ = 2m for seasonal data** (so ℓ = 24 monthly), capped at ℓ = T/5 when that is
smaller. At T ≈ 39, **T/5 ≈ 8**, so the cap binds and ℓ = 8.

**Critical caveat the source states plainly:** these checks show "whether a
method is using all of the available information, but it is **not a good way to
select a forecasting method**." So Ljung-Box gates *whether features are
missing*, not *which model wins*.

**Standard (unconstrained):** residual diagnostics are run on every fitted model.
**Standard (feasible):** cheap, no retrain needed, and answers whether the
current feature set leaves signal unexploited.

---

## §13.4 Forecast combinations — read earlier this session

Bearing: **high for the limitations section; OUT OF SCOPE by decision.**

> "Combining multiple forecasts leads to increased forecast accuracy. In many
> cases one can make dramatic performance improvements by simply averaging the
> forecasts." (Clemen 1989, quoted)

> "using a simple average has proven hard to beat" (Wang et al. 2023)

Worked example: the combination beats **every** component on RMSE, MAE **and**
the Winkler interval score.

**Scope note (Brian):** the benchmark selects the single best model to serve, so
combination is not adopted now — but it is explicitly reconsidered *after* the
feature engineering improves, and it is recorded here for the limitations and
future-work sections.

---


## §3.1 Transformations and adjustments — **answers Ch4's justification directly**

**Read 2026-09-13.** Bearing: **very high**. This is the transformation authority.

### Box-Cox, with the parameter CHOSEN not assumed

The family is given explicitly:

```
w_t = log(y_t)                        if lambda = 0
w_t = (sign(y_t)|y_t|^lambda - 1)/lambda   otherwise
```

> "A good value of lambda is one which makes the **size of the seasonal
> variation about the same across the whole series**, as that makes the
> forecasting model simpler."

And critically:

> "The **guerrero** feature (Guerrero, 1993) can be used to **choose a value of
> lambda for you**."

### ⚠ This reframes Chapter 4's low-power argument

Ch4 defends uniform `log1p` because "the tests that would drive such a selection
have limited power at forty-six observations." **The source does not select a
transformation by hypothesis test — it estimates a parameter.** Guerrero is an
estimator, not a test, so the low-power objection does not apply to it.

**This does not necessarily overturn the choice.** `lambda = 0` IS the log
transform. If Guerrero returns lambda near 0 across brands, the uniform log is
**vindicated empirically** rather than merely asserted — which is a strictly
stronger position than the current prose holds.

**Cheap, decisive check:** run Guerrero per brand, report the distribution of
lambda. Three outcomes, all publishable:
- clustered near 0 -> uniform log confirmed, with a real citation
- clustered elsewhere -> uniform log is wrong, and the right power is measured
- widely dispersed -> per-series selection is unstable, which is itself the
  low-power argument **measured instead of assumed**

### Calendar adjustment — a distinct operation the repo does not perform

> "if you are studying the total monthly sales in a retail store, there will be
> variation between the months simply because of the different numbers of
> trading days in each month… It is easy to remove this variation by computing
> **average sales per trading day** in each month, rather than total sales."

**The repo has `days_in_month` and `n_holidays` as FEATURES.** The source
proposes them as an **adjustment to the target**. A model can in principle learn
the adjustment from the feature, but the source's route removes a known source
of variation before modelling rather than asking the model to discover it.

**NEW — not present in any form.** Trading-day adjustment (`days_in_month`
minus holidays is already computed as `non_holiday_days`) is directly available.

**Standard (unconstrained):** estimate lambda; adjust for known calendar
variation before modelling.
**Standard (feasible):** both fully feasible and cheap. Guerrero needs a
library function or a short implementation; the calendar adjustment is a
division by an existing column.

---

## §3.2 Time series components — **names the assumption the log transform hides**

**Read 2026-09-13.** Bearing: **medium-high**.

Additive `y = S + T + R` versus multiplicative `y = S x T x R`. The decision
rule:

> "The additive decomposition is the most appropriate if the magnitude of the
> seasonal fluctuations… **does not vary with the level** of the series. When
> the variation… appears to be **proportional to the level**, then a
> multiplicative decomposition is more appropriate. **Multiplicative
> decompositions are common with economic time series.**"

And the equivalence that matters here:

> "y = S x T x R **is equivalent to** log y = log S + log T + log R"

**Consequence:** the repo's uniform `log1p` is implicitly a **multiplicative
seasonality assumption**. That is very likely correct for retail beverage
demand, and the source says multiplicative is common for economic series — but
the thesis nowhere states that this is what the transform commits it to.

**Verdict: CONFIRMS the choice, REFINES the justification.** The log is
defensible; the reason given in the prose is incomplete.

Also supplied: seasonally adjusted data as `y - S` (additive) or `y / S`
(multiplicative), and the warning that seasonally adjusted series retain the
remainder so "downturns or upturns can be misleading" — use the trend-cycle
component for turning points.

---

## §4.2 ACF features — **the most directly implementable feature set so far**

**Read 2026-09-13.** Bearing: **very high**. Core of the re-engineering.

`feat_acf()` returns six or seven features, named explicitly:

| Feature | What it is |
|---|---|
| `acf1` | first autocorrelation, original data |
| `acf10` | **sum of squares of the first ten** autocorrelations |
| `diff1_acf1` | first autocorrelation of the **differenced** series |
| `diff1_acf10` | sum of squares of first ten, differenced |
| `diff2_acf1` | first autocorrelation, **twice** differenced |
| `diff2_acf10` | sum of squares of first ten, twice differenced |
| `season_acf1` | **autocorrelation at the first seasonal lag** — returned for seasonal data |

The rationale for the summary form:

> "the sum of the first ten squared autocorrelation coefficients is a useful
> summary of **how much autocorrelation there is in a series, regardless of
> lag**."

### Seasonal differencing is introduced as a distinct operation

> "compute **seasonal differences**… If we had monthly data, we would compute
> the difference between **consecutive Januaries, consecutive Februaries**, and
> so on. This enables us to look at how the series is changing **between years,
> rather than between months**."

**The repo has no differenced columns at all** — not first, not seasonal. And
`season_acf1` is precisely the diagnostic that would settle the lag-12-versus-13
question flagged under §2.8.

**Verdict: NEW.** None of these seven features exists in the matrix.

**Standard (unconstrained):** ACF-derived features, computed on original,
differenced and seasonally differenced series, are standard series
characterisation.
**Standard (feasible):** fully feasible and cheap — they are summary statistics
over a window, computed within the time-safety boundary. **`acf10` and
`season_acf1` are the two highest-value single additions identified so far.**

---


## §9.1 Stationarity and differencing — **the most consequential section so far**

**Read 2026-09-13.** Bearing: **very high**. Four separate findings.

### 1. The book uses KPSS, not ADF — and the null is REVERSED

> "A number of unit root tests are available, which are based on different
> assumptions and **may lead to conflicting answers**. In our analysis, we use
> the **Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test**… In this test, the
> **null hypothesis is that the data are stationary**… small p-values (e.g.,
> less than 0.05) suggest that **differencing is required**."

| | ADF (what the repo uses) | KPSS (what the book uses) |
|---|---|---|
| Null | non-stationary | **stationary** |
| Failing to reject means | inconclusive | evidence of stationarity |

**This matters precisely because the panel is short.** With ADF, low power means
non-rejection is uninformative — and the repo's own ADF artefact says exactly
that in its notes ("a non-rejection should be read as inconclusive"). KPSS puts
the burden the other way, so a short series does not automatically default to
"assume a unit root".

### 2. Differencing order is DETERMINED, not assumed

- `unitroot_ndiffs()` — "a **sequence of KPSS tests** to determine the
  appropriate number of first differences".
- `unitroot_nsdiffs()` — "uses the **measure of seasonal strength introduced in
  Section 4.3**… **No seasonal differences are suggested if F_S < 0.64**,
  otherwise one seasonal difference is suggested."

**That is a directly implementable rule**, and it links §4.3's `F_S` to a
concrete decision with a stated threshold.

### 3. The source condemns over-differencing in its own words

> "**Beware that applying more differences than required will induce false
> dynamics or autocorrelations that do not really exist** in the time series.
> Therefore, **do as few differences as necessary** to obtain a stationary
> series."

**This is the authority behind P0051 F2.** That finding measured 27 of 79 brands
testing as already stationary in raw form while a blanket `d=1` is applied to
all of them. The book says that induces artefacts. **CONTRADICTS.**

### 4. Only two difference types are interpretable

> "First differences are the change between one observation and the next.
> Seasonal differences are the change between one year to the next. **Other lags
> are unlikely to make much interpretable sense and should be avoided.**"

Order also matters: "if the data have a strong seasonal pattern, we **recommend
that seasonal differencing be done first**, because the resulting series will
sometimes be stationary and there will be no need for a further first
difference."

**Standard (unconstrained):** KPSS-driven `ndiffs`/`nsdiffs` per series;
seasonal difference first; minimum necessary differencing.
**Standard (feasible):** fully feasible. `statsmodels` has KPSS. The `F_S < 0.64`
rule needs STL, which §4.3 already requires.

---

## §13.7 Very long and very short time series — **undercuts a thesis argument**

**Read 2026-09-13.** Bearing: **high**, and partly uncomfortable.

> "Some textbooks provide **rules-of-thumb giving minimum sample sizes**… These
> are **misleading and unsubstantiated in theory or practice**… There is, for
> example, **no justification for the magic number of 30** often given as a
> minimum for ARIMA modelling. The only theoretical limit is that we need more
> observations than there are parameters."

**Check against the repo:** the pipeline derives a `MIN_PERIODS` retention rule.
If that threshold is justified by a rule-of-thumb rather than by parameter count
and noise, the book explicitly rejects that reasoning. **This needs checking, and
it may require rewording rather than re-engineering.**

The recommended alternative for short series:

> "**The AICc is particularly useful here**, because it is a proxy for the
> one-step forecast out-of-sample MSE. Choosing the model with the minimum AICc
> allows both the number of parameters and the amount of noise to be taken into
> account."

And the empirical result on 152 short M3 series: 21 got zero-parameter models,
86 one parameter, 31 two, 13 three, **only 1 got four**. Short series select
simple models.

Also relevant to the tree models:

> "**ETS models are designed to handle this situation** by allowing the trend and
> seasonal terms to evolve over time. **ARIMA models with differencing have a
> similar property. But dynamic regression models do not allow any evolution of
> model components.**"

Lag-feature tree models are closer to dynamic regression than to ETS. **Recorded
for the limitations section** — the roster is out of scope by decision.

---

## §13.9 Outliers and missing values — **a concrete rule the repo lacks**

**Read 2026-09-13.** Bearing: **medium-high**.

**Outlier detection, stated as a procedure:**

1. Apply **`STL()` with `robust=TRUE`** (use `period=1` where there is little
   seasonality).
2. Outliers "should show up in the **remainder** series".
3. Flag remainders beyond **3 IQRs** from the central 50%: "**This is the rule we
   prefer to use**" — stricter than the conventional 1.5 IQR, giving ~1 in
   500,000 under normality.

**The caution is as important as the rule:**

> "**Simply replacing outliers without thinking about why they have occurred is
> a dangerous practice.** They may provide useful information about the process
> that produced the data."

**Missing values:** the book distinguishes *informative* missingness (a closed
store, where the following day rebounds — handle with dummy variables) from
*random* missingness. And on tooling: naive/benchmark methods and ARIMA tolerate
missing values, **but `ETS()` and `STL()` do not**.

**That last point is a practical constraint on any STL-derived feature**: the
panel has genuine zero-runs and gaps, so STL needs a gap policy before
`F_T`/`F_S` can be computed per brand.

**Standard (unconstrained):** robust-STL outlier detection at 3 IQR, with
reasoned treatment rather than automatic replacement.
**Standard (feasible):** feasible, but requires deciding a gap policy for STL
first. **The intermittency flags the repo already has are the right input to
that decision.**

---

## §4.1 Some simple statistics — thin

**Read 2026-09-13.** Bearing: **low**.

Any numerical summary is a feature: mean, min, max, and the five-number summary
via `quantile()`. Nothing here the repo needs that it does not already have in
its EDA tables.

**Verdict: SILENT.** Recorded for completeness; no action.

---


## §5.8 Evaluating point forecast accuracy — **one checkable implementation defect**

**Read 2026-09-13.** Bearing: **very high**.

### ⚠ MASE uses the SEASONAL naive denominator on seasonal data

For a **seasonal** series the scaled error is defined against the **seasonal**
naive benchmark:

```
q_j = e_j / [ 1/(T-m) * SUM_{t=m+1..T} |y_t - y_{t-m}| ]
```

and only "we set **m = 1** for non-seasonal data."

**For a monthly seasonal panel, m = 12.** If the repo computes MASE with the
non-seasonal denominator on a panel it elsewhere calls strongly seasonal, every
reported MASE is scaled against the wrong benchmark.

**There is a symptom already in the prose.** Ch5 records that "seasonal naive
scores worse than naive on MASE in every category while winning on WMAPE for
RTD", and attributes it to the two metrics weighting differently. **That is
exactly what a mis-set `m` would produce** — seasonal naive is guaranteed a
MASE near 1 when scaled against *its own* benchmark, so it scoring worse than
naive is a red flag rather than a curiosity.

**CHECK THIS IN THE REPO.** It is a small code question with a large
consequence for a reported table.

### The rest CONFIRMS current practice

| Claim | Verdict |
|---|---|
| MAPE undefined at zero actuals, extreme near zero | **CONFIRMS** the thesis's exclusion rule |
| Percentage errors need a **meaningful zero** (ratio scale) | **CONFIRMS** — unit sales qualify |
| **sMAPE should not be used** — "Hyndman & Koehler (2006) recommend that the sMAPE not be used" | **CONFIRMS** its absence |
| Minimising **MAE -> median** forecasts; **RMSE -> mean** forecasts | **REFINES**: the tuning objective determines which functional is estimated |
| Test set "**at least as large as the maximum forecast horizon**", typically ~20% | Check against the 70/15/15 split at H=3 |
| "A model which fits the training data well will not necessarily forecast well" | **CONFIRMS** the train/test discipline |

---

## §5.10 Time series cross-validation — **CONFIRMS, with one deviation worth naming**

**Read 2026-09-13.** Bearing: **high**.

The procedure is "evaluation on a **rolling forecasting origin**", training sets
containing only prior observations, accuracy averaged over test sets — and it
explicitly supports **multi-step** errors where "one-step forecasts may not be
as relevant", which is this thesis's H=3 case.

**CONFIRMS** the repo's expanding-window, period-level, order-preserving CV.

**The one deviation:** the book says "A good way to choose the best forecasting
model is to find the model with the **smallest RMSE** computed using time series
cross-validation." The repo tunes on **WMAPE**.

**This is a defensible deviation and arguably better than the book's single
recommendation** — the repo tunes *twice*, once per objective, because "WMAPE
and median APE are minimised by different functionals". §5.8 supplies the
theory for exactly that (MAE->median, RMSE->mean). **Say so explicitly**: the
deviation is principled, not an oversight.

Also confirmed by their Figure 5.24: forecast error **increases with horizon**,
which is why an H=3 result must never be compared against an H=1 figure.

---

## §13.3 Ensuring forecasts stay within limits — **confirms the clipping defect**

**Read 2026-09-13.** Bearing: **high**. Model-side, but already admitted in Ch5.

> "To impose a positivity constraint, we can simply **work on the log scale**."

For a bounded interval, a **scaled logit**:
`y = log((x−a)/(b−x))`, inverted by `x = (b−a)e^y/(1+e^y) + a`.

And the property that matters:

> "The **bias-adjustment is automatically applied** here, and the prediction
> intervals from these transformations have the **same coverage probability** as
> on the transformed scale, because **quantiles are preserved under
> monotonically increasing transformations**."

**Post-hoc clipping is nowhere endorsed.** Ch5 already reports its upper bound
as "a departure from that preference". **The book confirms the departure is
real**, and names the principled alternative.

**Out of scope by decision** (model-side), but this is a strong limitations
paragraph with an exact citation.

---


## §5.2 Some simple forecasting methods — **CONFIRMS the benchmark rung, pins m = 12**

**Read 2026-09-13.** Bearing: **high**.

The four benchmarks are mean, naive, seasonal naive, drift. Seasonal naive:

```
y_hat(T+h|T) = y(T+h-m(k+1)),  m = seasonal period, k = int((h-1)/m)
```

> "with **monthly data**, the forecast for all future February values is equal
> to the last observed February value."

**This is the third independent confirmation that m = 12 for monthly data**
(with §2.8 and §9.1). It reinforces the lag-13 flag.

And the sentence Ch5 already quotes, now verified in full:

> "any forecasting methods we develop will be compared to these simple methods
> to ensure that the new method is better than these simple alternatives. **If
> not, the new method is not worth considering.**"

**CONFIRMS** the benchmark design, and **CONFIRMS** that seasonal naive beating
tuned models on RTD is a finding to report rather than an embarrassment.

---

## §5.9 Evaluating distributional forecast accuracy — **resolves the thesis's open question**

**Read 2026-09-13.** Bearing: **very high**. This is the interval-evaluation
answer the thesis currently lacks.

### The Winkler score — width and coverage in ONE number

```
W = (u - l) + (2/alpha)(l - y)   if y < l
    (u - l)                       if l <= y <= u
    (u - l) + (2/alpha)(y - u)   if y > u
```

> "For observations that fall within the interval, the Winkler score is simply
> the **length of the interval**. Thus, **low scores are associated with narrow
> intervals**. However, if the observation falls outside the interval, the
> penalty applies, with the penalty **proportional to how far** the observation
> is outside."

**The thesis reports coverage and relative width separately and treats the
trade-off as unresolved** (`interval-width-a-tested-negative-result.md`). The
Winkler score is exactly the measure that resolves it, and it is one line to
compute from bounds already stored.

### Also supplied

| Measure | Definition | Use |
|---|---|---|
| **Quantile / pinball** | `Q = 2(1-p)(f-y)` if `y<f`, else `2p(y-f)` | per-quantile; equals absolute error at p = 0.5 |
| **CRPS** | average of quantile scores over all p | whole-distribution accuracy |
| **Skill score** | `(CRPS_bench - CRPS_model)/CRPS_bench` | scale-free cross-series comparison |

### Two cautions that bear on this panel

1. "it is important that the **test set is large enough** to allow reliable
   calculation of the error measure, **especially in the denominator**. For
   that reason, **MASE or RMSSE are often preferable** scale-free measures."
   **CONFIRMS** the thesis's use of MASE over skill scores at this sample size.
2. "**When the data are seasonal, the benchmark used is the seasonal naive
   method** rather than the naive method." **The m = 12 question again**, now
   affecting any skill score too.

**Standard (unconstrained):** report a Winkler score alongside coverage.
**Standard (feasible):** trivially feasible — the 90% bounds are already
persisted. **Highest-value single addition to the evaluation layer.**

---

## §5.6 Forecasting using transformations — **the exact mechanism behind the medians finding**

**Read 2026-09-13.** Bearing: **high**. SRQ2-relevant.

> "the back-transformed point forecast **will not be the mean** of the forecast
> distribution. In fact, it will usually be the **median**… For example, you may
> wish to add up sales forecasts from various regions to form a forecast for the
> whole country. **But medians do not add up, whereas means do.**"

Bias-adjusted mean, for `lambda = 0`:

```
y_hat = exp(w_hat) * [1 + sigma^2 / 2]
```

> "The larger the forecast variance, the bigger the difference between the mean
> and the median."

**Consequence for this repo:** predictions are made in log space and inverted
with `expm1`, so **every served point forecast is a median, not a mean**. That
is acceptable for a single brand-month, but it means **brand forecasts must not
be summed to a category total** without bias adjustment.

P0048's index already records this as "an SRQ2 item". **§5.6 is the citation and
the formula.**

Also: "the prediction interval is first computed on the transformed scale, and
the end points are back-transformed… This approach **preserves the probability
coverage**" — which **CONFIRMS** the repo's split-conformal interval being
formed in log space and exponentiated.

---

## §13.8 Forecasting on training and test sets — **the repo's design is right, and should say so**

**Read 2026-09-13.** Bearing: **medium-high**.

> "the comparisons on the test data use **different forecast horizons**… The
> forecast variance usually increases with the forecast horizon, so if we are
> simply averaging the absolute or squared errors from the test set, we are
> **combining results with different variances**."

**The repo scores a SINGLE month at exactly H=3** (`test.iloc[HORIZON-1]`),
which sidesteps this problem entirely. **That is a deliberate strength and the
prose should claim it**, citing §13.8 — at present it is justified only as
"the horizon contract".

The section also describes one-step errors on test data via `refit()` without
re-estimation, as a way to compare one-step forecasts fairly. Not needed here,
but it confirms that mixing horizons in one average is a recognised defect.

---


## §7.4 Some useful predictors — **THE richest feature section in the book**

**Read 2026-09-13.** Bearing: **highest of the entire scan so far.** Four
predictor families, none of which the repo has.

### 1. Fourier terms — the single highest-value addition identified

```
x1 = sin(2*pi*t/m),  x2 = cos(2*pi*t/m),
x3 = sin(4*pi*t/m),  x4 = cos(4*pi*t/m),  ...    K <= m/2
```

> "If we have monthly seasonality, and we use the first 11 of these predictor
> variables, then we will get **exactly the same forecasts as using 11 dummy
> variables**. With Fourier terms, we often need **fewer predictors** than with
> dummy variables."

**The repo encodes seasonality as three integers: `month`, `quarter`,
`peak_month`.** An integer `month` asserts that December (12) is eleven units
from January (1), which is false on a cycle. **Fourier terms encode the annual
cycle continuously and correctly in 4-6 columns**, and K is tunable.

**NEW.** Nothing equivalent exists. Cheap, time-safe (deterministic from the
date), and directly compatible with the tree and linear models already in the
roster.

### 2. Trading days — the repo does the weaker of the two sanctioned options

> "The number of trading days in a month can vary considerably and can have a
> **substantial effect on sales data**. To allow for this, the number of trading
> days in each month can be **included as a predictor**."

§3.1 offered the *adjustment* route (divide by trading days); §7.4 offers the
*predictor* route. **Both are sanctioned.** The repo does the predictor route
already (`days_in_month`, `non_holiday_days`) but has never said which route it
chose or why. **CONFIRMS with a citation, and closes a prose gap.**

### 3. Intervention variables — absent, and the panel needs them

| Type | Shape | Use here |
|---|---|---|
| **Spike** | 1 in one period, 0 elsewhere | one-off outlier; equivalent to a dummy for an outlier |
| **Step** | 0 before, 1 from intervention onward | **a brand delisting or a permanent range change** |
| **Piecewise trend** | trend that bends at a point | a slope change |

**NEW.** The panel has brands entering and leaving; none of this is modelled.
Also the direct alternative to deleting an outlier: "**Rather than omit the
outlier, a dummy variable removes its effect.**"

### 4. Distributed lags — applicable to promotion

> "since the effect of advertising can last beyond the actual campaign, we need
> to include **lagged values**… x1 = advertising for previous month, x2 = two
> months previously…"

The repo carries `promo_intensity` at a single shift. **Multiple promo lags are
sanctioned and absent.**

### 5. The dummy-variable trap — a guard if seasonal dummies are ever added

> "for **monthly data, use 11 dummy variables**… The general rule is to use one
> fewer dummy variables than categories."

---

## §5.3 Fitted values and residuals — **makes the Ljung-Box gate precise**

**Read 2026-09-13.** Bearing: **high**, and it corrects how the §5.4 gate must
be implemented.

> "If a transformation has been used in the model, then it is often useful to
> look at residuals **on the transformed scale**. We call these **innovation
> residuals**… suppose we modelled the logarithms of the data, `w = log(y)`.
> Then the innovation residuals are given by `w - w_hat` whereas the regular
> residuals are given by `y - y_hat`."

**The repo models `log1p(sales_units)`. So the Ljung-Box gate must run on
log-scale residuals, not on back-transformed ones.** Getting this wrong would
test the wrong series.

And the caution that decides which residuals to use:

> "fitted values are **often not true forecasts** because any parameters
> involved… are estimated using **all available observations**, including future
> observations."

**So the gate must use cross-validation residuals, not in-sample fitted
residuals.** §5.10 supplies the rolling-origin machinery for exactly that.

> "If patterns are observable in the innovation residuals, **the model can
> probably be improved**."

---

## §2.4 Seasonal plots — identification, with one useful property

**Read 2026-09-13.** Bearing: **medium**.

> "A seasonal plot allows the underlying seasonal pattern to be seen more
> clearly, and is **especially useful in identifying years in which the pattern
> changes**."

On a four-year panel, a changing seasonal pattern is a real risk and this is the
diagnostic for it. The `period` argument also handles **multiple seasonal
periods**, which matters if the Nielsen 4-4-5 calendar induces a second cycle.

**CONFIRMS** the repo's per-category seasonal profiling; **REFINES** it by
asking whether the profile is *stable across years* rather than only averaged.

---

## ⚠ §5.5 Distributional forecasts and prediction intervals — **FILE IS EMPTY**

**Attempted 2026-09-13.** The PDF
`...Chapter_5.5_Distributional_forecasts_and_prediction_intervalspdf.pdf`
is **zero bytes** and cannot be read. Note the malformed filename ("intervalspdf").

**This is a real gap, not a skip.** §5.5 is the definitional section for
prediction intervals and forecast distributions, and it is cited by §5.4 and
§5.9. It is listed **Essential** in the earlier analysis.

**Action:** re-export or re-download that section before the standard is
finalised. Its likely content (interval construction from the forecast
distribution, the multi-step widening rule, and the caution that intervals from
a normality assumption may be wrong) is partly recoverable from §5.4 and §5.9,
**but it must not be cited without being read.**

---


## §7.5 Selecting predictors — **challenges how the repo selects features**

**Read 2026-09-13.** Bearing: **high**.

### Two approaches named INVALID

> "A common approach that is **not recommended** is to plot the forecast
> variable against a particular predictor and if there is no noticeable
> relationship, drop that predictor… **This is invalid.**"

> "Another common approach which is **also invalid** is to do a multiple linear
> regression on all the predictors and **disregard all variables whose p-values
> are greater than 0.05**… statistical significance does not always indicate
> predictive value."

**The repo's weighted-distribution rejection SURVIVES this** — it was rejected
because measured error rose in three of four categories, which is a predictive
criterion, not a scatterplot or a p-value. **CONFIRMS that decision.**

### What the source recommends instead

Five measures: adjusted R-squared, CV (leave-one-out), AIC, AICc, BIC.

```
AIC  = T log(SSE/T) + 2(k+2)
AICc = AIC + 2(k+2)(k+3)/(T-k-3)
BIC  = T log(SSE/T) + (k+2) log(T)
```

> "we recommend that one of the **AICc, AIC, or CV** statistics be used, each of
> which has **forecasting as their objective**… In most of the examples in this
> book, we use the **AICc**."

And on adjusted R-squared: "its tendency to select too many predictor variables
makes it **less suitable for forecasting**."

**The repo tunes on WMAPE and computes no information criterion.** §13.7 already
recommended AICc specifically for short series. **This is the second independent
recommendation of AICc in the scan.**

Also sanctioned: **backwards stepwise regression** ("start with all predictors,
remove one at a time, keep if it improves the measure"), and best-subsets where
feasible. Plus a warning the thesis should heed if it reports any p-values:

> "any procedure involving selecting predictors first will **invalidate the
> assumptions behind the p-values**."

---

## §10.6 Lagged predictors — **supersedes §7.4 on how many lags to carry**

**Read 2026-09-13.** Bearing: **high**, and it is a concrete procedure.

The distributed-lag model:

```
y_t = beta0 + gamma0*x_t + gamma1*x_{t-1} + ... + gammak*x_{t-k} + eta_t
```

> "The value of **k can be selected using the AICc**."

Their worked example fits lag0..lag3 on TV advertising and **selects lag1 on
AICc** — advertising in the current month and the previous month only. Note the
methodological care: "When comparing models, it is important that they all use
the **same training set**", so the first three months are excluded to make the
comparison fair.

**The repo carries `promo_intensity` at exactly one shift and has never
justified that number.** This section supplies both the model form and the
selection criterion. **Third independent appearance of AICc.**

**NEW.** Applies directly to promotion, and to any exogenous driver.

---

## §2.5 Seasonal subseries plots — identification, changes *within* a season

**Read 2026-09-13.** Bearing: **medium-low**. Same family as §2.4.

> "This form of plot enables the underlying seasonal pattern to be seen clearly,
> and also shows the **changes in seasonality over time**. It is especially
> useful in **identifying changes within particular seasons**."

Blue horizontal lines give the per-season mean. On a 4-year panel this is the
diagnostic for "is December's share drifting?", which a single averaged
peak-month set cannot show.

**REFINES** the repo's peak-month derivation: the set is computed from pooled
means and never checked for stability across years.

---


## §9.9 Seasonal ARIMA — **settles the question, 4th confirmation of m = 12**

**Read 2026-09-13.** Bearing: **very high** (model-side; out of scope by
decision, but Ch5 already admits the defect).

Notation: `ARIMA(p,d,q)(P,D,Q)_m`, "where **m = the seasonal period**". Their
**monthly** example uses **m = 12** throughout: seasonal differencing at lag 12,
seasonal ACF/PACF spikes read at **lags 12, 24, 36**.

> "In considering the appropriate seasonal orders… **restrict attention to the
> seasonal lags**."

### The full order-selection procedure, specified

> "The `ARIMA()` function uses **`unitroot_nsdiffs()` to determine D**… and
> **`unitroot_ndiffs()` to determine d**… The selection of the other model
> parameters (**p, q, P and Q**) are all determined by **minimising the AICc**."

**The repo's fixed `SARIMAX(order=(1,1,1))` with no seasonal part is the one
configuration this procedure never produces on seasonal monthly data.**

### A constraint that governs how any comparison is reported

> "When models are compared using **AICc** values, it is important that all
> models have the **same orders of differencing**. However, when comparing
> models using a **test set**, it does not matter how the forecasts were
> produced — **the comparisons are always valid**."

**The thesis compares on a test set**, so its cross-model comparisons are valid
even across differencing regimes. Worth stating explicitly.

### The honest closing line — a limitations sentence

> "Sometimes it is **not possible to find a model that passes all of the
> residual tests**. In practice, we would normally use the **best model we could
> find**, even if it did not pass all of the tests."

Also note their Ljung-Box call sets **`dof` to the number of fitted parameters**
(`lag=24, dof=4`), which the §5.4 gate must replicate.

---

## §9.6 Estimation and order selection — **AICc formula, and the d caveat again**

**Read 2026-09-13.** Bearing: **high**.

```
AIC  = -2 log(L) + 2(p+q+k+1)
AICc = AIC + 2(p+q+k+1)(p+q+k+2)/(T-p-q-k-2)
BIC  = AIC + [log(T) - 2](p+q+k+1)
```

> "Good models are obtained by minimising the AIC, AICc or BIC. **Our preference
> is to use the AICc.**"

And the caution that pairs with §9.1:

> "these information criteria tend **not to be good guides to selecting the
> appropriate order of differencing (d)**, but only for selecting the values of
> p and q. This is because the differencing **changes the data on which the
> likelihood is computed**, making the AIC values between models with different
> orders of differencing **not comparable**. So we need to use some other
> approach to choose d."

**That "other approach" is KPSS (§9.1).** The two sections interlock: KPSS picks
d and D; AICc picks p, q, P, Q. **Fourth independent recommendation of AICc.**

---

## §8.6 ETS estimation — **one constraint that blocks naive application here**

**Read 2026-09-13.** Bearing: **high** for the limitations section.

Selection is by information criterion over the (Error, Trend, Seasonal) space:

```
AIC  = -2 log(L) + 2k
AICc = AIC + 2k(k+1)/(T-k-1)
```

> "A great advantage of the ETS statistical framework is that **information
> criteria can be used for model selection**."

### ⚠ The constraint that matters for THIS panel

> "**Models with multiplicative errors** are useful when the data are strictly
> positive, but are **not numerically stable when the data contain zeros or
> negative values**. Therefore, multiplicative error models **will not be
> considered if the time series is not strictly positive**. In that case, **only
> the six fully additive models** will be applied."

**This panel has genuine zeros and zero-runs** — the repo has
`zero_run_flag`/`zero_run_length` precisely because of them. So on intermittent
brands, ETS is restricted to the six additive forms.

**That is a real, citable constraint on adding ETS — not a reason to avoid it.**
Three combinations (A,N,M), (A,A,M), (A,Ad,M) are excluded anyway for numerical
instability.

Also: for multiplicative-error models the innovation residuals are **not** the
regular residuals — same distinction §5.3 draws for transformations.

---

## §12.5 Bootstrapping and bagging — **reframes the combination question**

**Read 2026-09-13.** Bearing: **medium-high** for future work.

Procedure: transform if needed, **STL-decompose**, **block-bootstrap** the
remainder ("contiguous sections selected at random and joined together", because
the remainder may itself be autocorrelated), add back trend and seasonal, invert
the transform. Then fit a model to each simulated series and **average the
forecasts** — "bagging", for bootstrap aggregating.

> "**Bergmeir et al. (2016) show that, on average, bagging gives better forecasts
> than just applying `ETS()` directly.** Of course, it is slower because a lot
> more computation is required."

**This is a DIFFERENT kind of combination from §13.4.** §13.4 averages across
*model families*; §12.5 averages across *resampled versions of the same series*.
The second is available even when the roster is fixed at one family, so it is
**compatible with the out-of-scope decision on the model roster**.

**Requires STL**, which inherits §13.9's constraint that `STL()` does not accept
missing values — so the gap policy must be settled first.

---


## §9.10 ARIMA vs ETS — **AICc cannot compare across the two classes**

**Read 2026-09-13.** Bearing: **high**, and it sanctions the thesis design.

> "The AICc is useful for selecting between models **in the same class**…
> However, it **cannot be used to compare between ETS and ARIMA models**,
> because they are in different model classes, and the likelihood is computed in
> different ways."

So the selection procedure is two-level, and the thesis already does the second
level: **AICc within a family, test set or time-series CV across families.**

Their two worked comparisons split, which is itself the citable point:

| Series | Winner | Basis |
|---|---|---|
| Australian population (non-seasonal) | **ETS** (RMSE 0.077 vs 0.194) | time-series CV, `stretch_tsibble` |
| Quarterly cement (seasonal) | **ARIMA** (test RMSE 216 vs 222, MASE 1.27 vs 1.30) | train/test split |

> "Because the series is relatively long, we can afford to use a training and a
> test set **rather than time series cross-validation**. The advantage is that
> this is **much faster**."

**CONFIRMS the thesis's benchmark-by-held-out-test design** as the correct way to
compare heterogeneous model families — which is exactly what SRQ1 does across
statistical, ML and neural families. Worth citing directly.

Structural facts: all ETS models are non-stationary; the **six fully additive
ETS models** have exact ARIMA equivalents (Table 9.4 — e.g. ETS(A,N,A) =
ARIMA(0,1,m)(0,1,0)_m); the nine multiplicative-error and three
multiplicative-seasonal ETS models have **no ARIMA counterpart**. Since the
additive six are the only ones admissible on a non-strictly-positive panel
(§8.6), adding ETS here overlaps more with ARIMA than it would elsewhere —
a limitation worth stating rather than hiding.

---

## §11.1 Hierarchical and grouped series — **names the panel's real structure**

**Read 2026-09-13.** Bearing: **out of scope for P0055**, high for future work.

The panel is **exactly** the structure this chapter describes, and the thesis has
never named it:

| Book's term | This panel |
|---|---|
| Hierarchical (nested, `State / Region`) | **category / brand** — every brand belongs to one category |
| Grouped (crossed, `Gender * Legal * State`) | **brand × market** — market does not nest in brand |
| Mixed, `(State/Region) * Purpose` | **(category / brand) × market** |

> "for any time t, the observations at the **bottom level** of the hierarchy will
> **sum to the observations of the series above**."

Two direct implications the thesis should state:

1. **Forecasts at brand level do not automatically reconcile to a category
   total.** The thesis forecasts brands and never reconciles. That is a real,
   named, literature-recognised gap — not an oversight to hide.
2. **This is the correct frame for the pooled-vs-per-category-vs-per-brand
   question** (Phase 4). The book's vocabulary is grain-in-a-hierarchy, and
   reconciliation methods exist precisely for it.

> "some series showing strong trends or seasonality, some showing contrasting
> seasonality, while **some series appear to be just noise**."

That sentence describes the brand panel exactly, from an authoritative source,
and is quotable for the heterogeneity argument.

**NEW.** Record as future work; do not open it in P0055.

---

## §6.2 Judgmental forecasting, key principles — **speaks to SRQ4's framing, not its models**

**Read 2026-09-13.** Bearing: **high for Ch3/Ch9**, none for features.

This is the only section in the book that addresses **a human or agent producing
a forecast by judgment**, which is precisely what Scenarios A/B/F do. Five
principles, each mapping onto the experiment:

| Principle | Bearing on SRQ4 |
|---|---|
| "Set the forecasting task **clearly and concisely**… avoiding ambiguous and vague expressions" | **This is the v6 shared-composition argument.** The book independently justifies prompt consistency as a methodological control |
| "Implement a **systematic approach**… checklists of categories of information… identify what information is important and how this information is to be weighted" | the capability-note blocks are exactly this |
| "**Document and justify**… promotes consistency, as the same rules can be implemented repeatedly… leads to accountability, which can lead to **reduced bias**" | the auditability argument for the typed tool (SRQ2) |
| "**Systematically evaluate** forecasts… keep records of forecasts and use them to obtain feedback" | the run log |
| "**Segregate forecasters and users**" | the planner-vs-forecaster split in the scenario prompts |

And a distinction the discussion chapter should borrow outright:

> "management may decide to adjust a forecast upwards… **This type of adjustment
> should be part of setting goals or planning supply, rather than part of the
> forecasting process.** … **setting targets is different from producing
> forecasts, and the two should not be confused.**"

The PBS case study is the ready-made analogue: judgment **beat** a statistical
model alone for new listings ("using judgment for new listings and new policy
impacts gave better forecasts than using a statistical model alone"), *because*
it was structured and documented — while the unstructured policy-impact forecasts
were "heavily reliant on the work of one person" with "no formal review process".

**That is the thesis's own finding in miniature**: an agent given data and no
structure produces variable work; the same capability inside a documented,
evaluated procedure is useful. **CONFIRMS, from outside the ML literature.**

---

## §2.7 Lag plots — seasonality as positive relationships at multiples of m

**Read 2026-09-13.** Bearing: **low-medium**. Identification family.

`gg_lag` plots y_t against y_{t−k}.

> "The relationship is **strongly positive at lags 4 and 8**, reflecting the
> strong seasonality in the data. The **negative relationship** seen for lags 2
> and 6 occurs because **peaks (in Q4) are plotted against troughs (in Q2)**."

Quarterly, m = 4 → structure at 4 and 8. **Monthly, m = 12 → structure at 12 and
24 — not 13.** **Fifth independent confirmation of the lag-12 point**, and the
one that states the mechanism most plainly: the informative lags are integer
multiples of the seasonal period.

**REFINES** the repo's lag set `(1, 2, 3, 4, 8, 13)`: 8 is not a multiple of 12,
and 13 is one past it. On monthly data this section points at **12 and 24**.

---


## 12.2 Prophet -- the repo fits this model; one CHECK RESOLVED

**Read 2026-09-13.** Bearing: **HIGH -- direct hit on a model the repo uses.**

```
y_t = g(t) + s(t) + h(t) + eps_t
```

`g(t)` piecewise-linear trend with **automatically selected changepoints**;
`s(t)` seasonality; `h(t)` holiday effects as **simple dummy variables**;
estimated by a **Bayesian** approach.

### Finding 1 -- Prophet's seasonality IS Fourier terms

> "The seasonal component consists of **Fourier terms** of the relevant periods.
> By default, **order 10 is used for annual seasonality**."

**Independent reinforcement of 7.4's top recommendation.** The repo already
*runs* a model whose seasonal representation is Fourier terms, while feeding its
ML models three calendar integers. The mechanism is already in the project; it is
simply not available to the models that need it.

### Finding 2 -- the misconfiguration risk: CHECKED, NO DEFECT

The book warns:

> "the seasonal term **must have the period fully specified for quarterly and
> monthly data**, as the **default values assume the data are observed at least
> daily**."

**Verified against the repo -- the call is explicit and correct**
(`srq1_baselines_stat.py:293`):

```python
m = Prophet(yearly_seasonality=True, weekly_seasonality=False,
            daily_seasonality=False)
```

Annual seasonality is switched on by name; the two sub-monthly seasonalities are
switched off by name. Nothing is left to a daily-tuned default.
**No action. Recorded as a check that passed, not as a finding.**

### Finding 3 -- the book's verdict, useful for Ch5

> "Prophet has the advantage of being **much faster to estimate**... and it is
> **completely automated**. However, it **rarely gives better forecast accuracy
> than the alternative approaches**."

Both worked examples confirm it: on cement Prophet is **worst of three**
(MASE 1.47 vs ARIMA 1.27, ETS 1.30); on electricity it leaves "substantial
remaining autocorrelation in the residuals" and imposes a piecewise linear trend
the authors call "not really appropriate here."

**CONFIRMS** the thesis's treatment of Prophet as one benchmark among several --
and supplies a citation if Prophet underperforms here too.

---

## 11.3 Forecast reconciliation -- MinT, and one line about judgmental forecasts

**Read 2026-09-13.** Bearing: **out of scope, future work.** Continues 11.1.

`y_t = S b_t` (summing matrix); all coherent approaches are
`ytilde_h = S G yhat_h`. Bottom-up, top-down and middle-out are all just
particular `G` matrices.

> "no top-down method satisfies this constraint, so **all top-down approaches
> result in biased coherent forecasts**."

**MinT** (Wickramasuriya et al., 2019) finds the `G` minimising total forecast
variance. Four practical weightings: `ols`, `wls_var`, `wls_struct`,
`mint_cov` / `mint_shrink`.

Two details that would matter if this is ever attempted here:

- **`mint_shrink` for a wide, short panel**: "for cases where the number of
  bottom-level series **m is large compared to the length of the series T**, this
  is not a good estimator. Instead we use a **shrinkage estimator**." The panel is
  exactly that shape -- roughly 79 brands, 39 visible months.
- **`wls_struct` needs no residuals**, so it is "particularly useful... where the
  base forecasts are generated by **judgmental forecasting (Chapter 6)**."
  **That is the LLM scenarios.** If agent forecasts were ever reconciled to a
  category total, this is the named method for it.

> "particular aggregation levels or groupings may **reveal features of the
> data**... These features may be **completely hidden or not easily identifiable
> at other levels**."

**NEW, deferred.** Record as future work beside 11.1.

---

## 6.1 Beware of limitations -- the failure modes the scenarios can exhibit

**Read 2026-09-13.** Bearing: **high for Ch9's discussion of A/B/F behaviour.**

Four named failure modes of judgmental forecasting, each testable against the
run log:

| Failure | The source's words | Bearing |
|---|---|---|
| **Inconsistency** | "Unlike statistical forecasts, which can be generated by **the same mathematical formulas every time**, judgmental forecasts depend heavily on human cognition" | **This is run-to-run variance across repeats.** The thesis measures it directly |
| **Agenda / target contamination** | "Judgment can be clouded by personal or political agendas, where **targets and forecasts are not segregated**" | why the prompt separates planner from forecaster |
| **Optimism / wishful thinking** | "it would be highly unlikely that a team working towards launching a new product would forecast its failure" | a directional-bias check on agent forecasts |
| **Anchoring** | "subsequent forecasts tend to converge or be close to an **initial familiar reference point**... it is common to **take the last observed value** as a reference point... may lead to **conservatism and undervaluing new information**" | **directly testable** |

**The anchoring row is the most valuable thing in this section.** It predicts a
specific, measurable behaviour: an LLM given a history and asked for a forecast
may anchor on the final observed value, which is naive-1 in disguise. **The 63
logged runs can test this**, and either result is reportable.

The consistency contrast is the thesis's own framing stated by the authority: a
trained pipeline gives the same answer every time; an agent does not.

---

## 6.7 NOT READ -- the file contains 6.6 instead

**Checked 2026-09-13.** The file named
`..._Chapter_6.7_Judgmental_adjustments.pdf` contains **6.6 New product
forecasting** -- every page header reads "6.6 New product forecasting" and the
source URL is `otexts.com/fpp3/new-products.html`.

**So 6.7 was never captured.** It is a consequential gap: 6.7 covers **adjusting
a statistical forecast by judgment**, the closest section in the book to *an
agent revising a model's output* -- directly relevant to scenarios F and G.

### What the mis-filed 6.6 does contribute

Not nothing -- it is about forecasting with **no historical data**, the
cold-start case:

> "Judgmental forecasting is usually the only available method for new product
> forecasting, as **historical data are unavailable**."

> "having salespeople generate forecasts **violates the key principle of
> segregating forecasters and users**"

> "it is important to **thoroughly document the forecasts made, and the reasoning
> behind them**, in order to be able to **evaluate them when data become
> available**."

That last line is the audit-trail argument for SRQ2, again from outside ML.

**TO OBTAIN: 6.7**, from `otexts.com/fpp3/judgmental-adjustments.html`.

---

## 5.5 CONFIRMED UNREADABLE -- genuinely a zero-byte file

**Verified 2026-09-13** by `ls -la`: the file
`..._Chapter_5.5_Distributional_forecasts_and_prediction_intervalspdf.pdf`
(note the doubled extension) is **0 bytes**. Not a path error -- the file exists
and is empty. It is the **only** empty file of the 41.

**TO OBTAIN: 5.5**, from `otexts.com/fpp3/prediction-intervals.html`. Partially
recoverable from 5.9 (evaluating intervals), 5.6 (back-transformation) and 12.5
(which cites 5.5 for residual bootstrapping) -- but the multi-step interval
formulae and the Table 5.1 multipliers are not.

---

# SCAN COMPLETE -- 39 of 41 sections read

| | Count |
|---|---|
| PDFs on disk | **41** |
| Read end-to-end | **39** |
| Empty file (5.5) | 1 |
| Mis-filed (6.7 -- contains 6.6) | 1 |
| Bonus section gained (6.6, not on the original list) | +1 |

**Two sections to obtain before the derived standard is final: 5.5 and 6.7.**
Neither blocks the feature-engineering conclusions; they bear on interval
reporting and on judgmental adjustment respectively.

---

## Sections still to read

5.5 (EMPTY FILE) ·
6.1, 6.7 · 7.6 · 9.5, 9.7 ·
11.3 · 12.2

**6 remaining of 41**, one of which (5.5) is an unreadable file.
