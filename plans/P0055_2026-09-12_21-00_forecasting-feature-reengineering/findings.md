---
name: p0055-findings
description: STATE - What is actually missing from the feature set, verified against the code rather than assumed; where the premise needed narrowing; and four things the session brief did not account for.
pid: P0055
created: 2026_09_12-21_00
updated: 2026_09_12-21_00
---

# P0055 — Findings

## F1 — The premise needs narrowing, and the narrower version is stronger

**The brief said forecasting-based features were not incorporated. That is too
strong as stated, and an examiner would catch it.**

Chapter 4 already carries, with citations:

- **Log transformation** of the target and volume inputs, justified by measured
  skewness (4.1–5.1 raw, none above 0.25 transformed) and cited to Hyndman &
  Athanasopoulos (2021).
- **Stationarity testing** — ADF per category, p = 0.77 in level, below 0.001
  after first differencing; CSD declared difference-stationary.
- **Differencing** for the statistical baselines, cited as the conventional
  treatment for a unit root.
- **Autocorrelation analysis** at lags 1, 3 and 13, reported both per-brand and
  pooled-brand-demeaned.
- A **holiday ablation** (helped in 6 of 9 combinations) and a
  **weighted-distribution test** that was run and rejected on measurement.

**The accurate claim is different and sharper:** the diagnostics were performed
in Chapter 4 but **largely did not reach the feature matrix**. The model sees
18 columns:

| Group | Columns |
|---|---|
| Lags | lag_1, lag_2, lag_3, lag_4, lag_8, lag_13 |
| Rolling | rolling_mean_4, rolling_std_4, rolling_mean_13 |
| Calendar | month, quarter, peak_month |
| Promo | promo_intensity |
| Holiday | days_in_month, n_holidays, non_holiday_days |
| Intermittency | zero_run_flag, zero_run_length |

**There is no STL decomposition feature, no ACF-derived feature, no Box-Cox and
no differenced-target option.** Verified: the matrix has 54 columns, the
`FEATURES` literal has 18, and `resolve()` returns exactly 18 on CSD. There is
no literal-vs-matrix drift — the 18 are the deliberate set.

### ⚠ CORRECTED 2026-09-12 (higher-effort re-analysis) — do not write the broad version

An earlier draft of this finding said *"the diagnostics informed the prose but
not the matrix."* **That is still too broad, and Chapter 4 would refute it.**

§4.2.2 explicitly defends uniform treatment:

> "A logarithmic transformation is applied uniformly to the target and to the
> volume-valued inputs **rather than selected per brand**… Uniform treatment is
> preferred to per-series selection because the tests that would drive such a
> selection **have limited power at forty-six observations**, and because a
> transformation applied unevenly across brands would make the feature
> semantics inconsistent within the panel."

That is a considered argument, already made, and the ADF artefact's own notes
carry the same low-power caveat. **Uniform log1p is a defended design choice,
not an oversight, and the plan must not attack it.**

**The real, narrow, citable defect is the sentence after it.** §4.2.2 continues:

> "Non-stationarity in the mean is handled by differencing for the statistical
> baselines, which is the conventional treatment for a series carrying a unit
> root."

**That is false for RTD**, whose own Table 3 in the same chapter reports
`p = 0.000, stationary in level`. The chapter contradicts itself two sections
apart. P0051 F5 found this on 2026-09-08 and it is still in the prose.

> **Write it as: three global design choices (uniform `log1p`, lag features in
> place of explicit differencing, and a fixed ARIMA `d=1`) are defensible on the
> low-power argument, but the prose currently presents the third as
> data-selected when it is a fixed specification — and says so in a sentence
> that is wrong for one of the four categories.**

---

## F2 — The defensible gap list, each with its source section

Read directly from the split PDFs, not inferred from titles.

| Gap | Source | What it licenses |
|---|---|---|
| **STL strength features** — trend strength `F_T`, seasonal strength `F_S` | §4.3 | Both defined explicitly as `max(0, 1 − Var(R)/Var(T+R))` and the seasonal analogue. Also `seasonal_peak_year`, `spikiness`, `linearity`, `curvature`, `stl_e_acf1`, `stl_e_acf10`. Directly usable as per-brand features |
| **Residual diagnostics / Ljung-Box** | §5.4 | "If there are correlations between innovation residuals, then there is information left in the residuals which should be used in computing forecasts." Gives a *test* for whether the feature set is leaving signal on the table |
| **Forecast combination** | §13.4 | "Combining multiple forecasts leads to increased forecast accuracy… using a simple average has proven hard to beat." Their worked example beats every component on RMSE, MAE **and** Winkler score |
| **ETS / exponential smoothing** | §8.6, §9.10 | Already admitted as missing in Ch5 |
| **Seasonal ARIMA** | §9.9 | Ch5 admits the fitted ARIMA carries no seasonal order on a strongly seasonal monthly panel |
| **Transformation-based bounds** | §13.3 | Ch5 applies post-hoc clipping and already flags this as a departure |

**§5.4 is the highest-value cheap item.** A Ljung-Box test on residuals is a few
lines, needs no retrain to compute, and either confirms the feature set is
adequate or proves it is not — which is a *result* either way.

---

## F3 — The agents already do what the pipeline does not, and this is measured

From the v6 run traces (14 B and F runs):

- **Every single run** fitted exponential smoothing **and** a seasonal ARIMA —
  the exact two families Ch5 records as absent.
- Most added STL decomposition; several added Ridge, Huber, OLS or WLS.
- **12 of 14 runs** used explicit combination language ("ensemble", "blend",
  "median of", "simple average").
- One earlier run fitted an **18-order SARIMA grid** selected on AIC in a single
  session.

This is not an anecdote; it is the measured behaviour of the comparator. It also
means the gap list in F2 is not academic — it is the list of things the agent is
doing and the pipeline is not.

---

## F4 — Chapters 8 and 9 are NOT written, and Chapter 7 has three stale numbers

**The brief assumed Ch8 prose documents the missing forecasting features. It
does not — Chapter 8 is a skeleton.** Verified against the 2026-09-12 22:28
snapshot:

- Ch8 is **1,384 words** and carries placeholders: `[N] SKUs × 28 retailers ×
  [T] weeks`, a **weekly** grain contradicting the monthly panel, and `GPT-4o`
  as judge.
- Its §8.2.4 results quote **pre-v6 per-category WMAPE** (CSD 16.5%, etc.) — the
  SRQ1 benchmark, not the SRQ4 experiment.
- Ch9 is **1,233 words** and §9.1.4 states the code-as-action baseline "was
  *not* executed: it requires a secure execution sandbox (E2B) that is not
  configured." **That is now false** — it ran 63 times.

**Chapter 7** pins latency/token/cost to `smoke/runs.csv` (2026-09-11), which
the 63-run set supersedes. The argument holds; three numbers do not.

**Implication for tonight:** the writing session cannot "analyse what was
written into Ch8 prose about this", because it was never written. The relevant
admissions live in **Chapter 5**, which does state both the ETS omission and the
non-seasonal ARIMA plainly and well.

---

## F5 — P0051 is the EVIDENTIARY SPINE of this plan, not a subset of it

### ⚠ CORRECTED 2026-09-12 — an earlier draft had this backwards

The first version of this finding said *"fold P0051 into this plan."* **That
inverts the quality ordering and was wrong.** P0051 was read in full afterwards.
It is not half of P0055; it is a **better-evidenced statement of the core
defect** than anything P0055 wrote independently, and P0055 should cite it
rather than absorb it.

What P0051 establishes, measured 2026-09-08 by two independent repo-wide
searches plus an exhaustive `grep -ril "adfuller\|adf_"` covering `worktrees/`:

| | Finding | Why it matters here |
|---|---|---|
| **F1** | The per-brand ADF `recommendation` column has **zero consumers**, across **three pipeline generations** | Not half-finished wiring — a long-standing reporting artefact |
| **F2** | **27 of 79 brands test `raw`** (already stationary). The blanket `d=1` **over-differences them** | The single strongest fact in this area. It is a *correctness* problem, not a missing-feature problem |
| **F3** | Four hardcoded sites, with line numbers: global `log1p`, no differenced columns, fixed `SARIMAX(1,1,1)`, Ridge's hardcoded volume tuple | Tells you exactly where to intervene |
| **F4** | `derive_log_transform()` computes `supported`, then returns the config constant | The verdict is interpolated into a provenance string and discarded |
| **F5** | Two Ch4 prose claims overstate; the RTD differencing sentence is wrong | This is the prose defect, already located and worded |
| **F6** | A code comment asserts the ADF csv is consumed. Nothing reads it | One-line fix, independent |
| **F7** | `p_diff` is computed but **never used in the decision rule** — `log1p+diff` is an else-branch fallback | The column is less informative than its name |

**Re-verified live on 2026-09-12** at
`step_2_eda_descriptive.py:543-553`: `p_diff` is computed on line 543 and does
not appear in the rule on lines 549-553. F7 stands.

**Action: P0051 stays open and is read FIRST.** P0055 inherits its findings as
evidence and adds the forecasting-literature layer on top. Its `superseded_by`
marker and fold banner, written earlier in this session, are being removed.

---

## F6 — Retraining is cheaper than the brief assumes

The HPC is not the bottleneck. Measured 2026-09-10, job `j-12387709`: **six
stages in 18.3 minutes**, including two 5-minute tuning stages. The full suite is
**22 stages**, most of which are seconds.

| Step | Cost |
|---|---|
| Re-engineer features + rebuild matrices | local, minutes |
| Full HPC retrain | ~1–2 hours, bounded |
| Re-run SRQ4 (63 runs) | **~$20, ~1 hour** |
| Regenerate figures/tables (P0050) | minutes, any order |

**The schedule risk is the prose, not the compute.** Chapters 4, 5 and 8 all
describe the feature set, and Ch8/Ch9 are unwritten regardless.

---

## F7 — The claim to test, not assume

The brief states that even after re-engineering, the code-as-action arms will
likely stay ahead because they fit **brand-filtered** data while the pipeline
fits pooled or per-category data.

**That is plausible and probably right, but it is currently an assumption.** It
is also the single cheapest experiment available:

> Fit the existing pipeline **per brand** on the same three brands and
> re-compare. One training run, not fifty.

If the gap closes, the headline finding is about **grain**, not about agency —
and that changes what the thesis claims. If it holds, the claim is *measured*
rather than argued, which is strictly stronger. **Do this before writing the
limitation.**

Note the counter-evidence already in the literature review: M5 found
cross-learning (one model across many series) **outperformed** series-by-series
training at lower cost. So per-brand fitting is the approach M5 found *worse* at
scale — which makes "brand-filtered data advantages the agent" a claim about
**short single-brand series specifically**, not a general one.

---

## F8 — Three provably-broken sites, verified live 2026-09-12. FIX THESE BEFORE ADDING ANYTHING

Added by the higher-effort re-analysis. **This finding reorders Phase 2.** An
earlier draft proposed adding STL and ACF features first; that builds on a
pipeline whose differencing is wrong for roughly a third of brands.

| # | Site | State | Source |
|---|---|---|---|
| **1** | `step_2_eda_descriptive.py:543-553` | `p_diff` computed, **never in the decision rule**; `log1p+diff` is the else-branch. Example from the CSD artefact: `TUBORG SQUASH` has `p_diff = 0.471` — differencing plainly failed — and is still labelled `log1p+diff` | P0051 F7 |
| **2** | `srq1/srq1_baselines_stat.py:283` | `SARIMAX(y, order=(1,1,1))`, **no seasonal order**, on a strongly seasonal monthly panel. The module's own docstring (line 26) says *"no pmdarima"*. `auto_arima` is never called anywhere | §9.9, §9.6; Ch5 already admits it |
| **3** | `step_3_derive_params.py`, `derive_log_transform()` | Computes `supported`, records `adf_stationary_at_5pct`, then `return LOG_TRANSFORM_TARGET` — the config constant | P0051 F4 |

**Site 3 has improved since P0051 described it** — it now runs an ADF test and
records `adf_pvalue_log` and `adf_stationary_at_5pct` in provenance, and its
docstring is honest that the config carries the default. The structural point
still stands: the computed verdict does not drive the return value.

**Also confirmed:** there is no contract JSON exposing ADF to a consumer. The
engineered directory holds only `*_manifest_h*.json` and `*_split_dates_h*.json`.
So P0051's "no consumers" finding holds **structurally**, not merely by grep.

### Why this ordering matters

Site 2 is the highest-value single fix in the plan, and it is **already admitted
in Chapter 5** — so fixing it converts a stated limitation into a result, with
no new prose argument required. Sites 1 and 3 are cheap correctness repairs that
make any subsequent feature work trustworthy.

**A defensible outcome is to fix these three, retrain, and add no new features
at all.** That alone would answer the brief's intent.


---

## F9 - MASE uses the NON-SEASONAL denominator on a seasonal panel (CONFIRMED IN CODE)

**Source:** Hyndman & Athanasopoulos (2021) 5.8. **Site:**
`srq1/srq1_benchmark_cv.py:184-203`, consumed by `srq1_mase.py:158`.

The book defines MASE with a **seasonal** naive denominator when the series is
seasonal:

```
q_j = e_j / [ 1/(T-m) * SUM |y_t - y_{t-m}| ]      with m = 12 for monthly
```

The repo computes (line 200):

```python
d = float(np.mean(np.abs(np.diff(y))))
```

`np.diff` with no arguments is the **first difference**, i.e. `|y_t - y_{t-1}|`.
**That is m = 1** - the non-seasonal denominator - on a panel the repo's own
docstring (`srq1_baselines_stat.py:29-31`) describes as *"monthly beverage demand
with strong annual seasonality."*

### Why this matters more than a scaling constant

Every model is scaled against **the one-step naive error**. That flatters
naive-1 by construction and penalises any method whose skill is seasonal.

**It explains an anomaly the thesis already observed and could not account for:
seasonal naive scoring WORSE than naive on MASE in every category.** With an
m = 1 denominator that is the expected outcome, not a finding about the data.

### The internal contradiction that proves it

| Site | Seasonal period used |
|---|---|
| `run_seasonal_naive` (`srq1_baselines_stat.py:167`) | `hist[-12]` - **m = 12, correct** |
| `mase_denominator` (`srq1_benchmark_cv.py:200`) | `np.diff(y)` - **m = 1, wrong** |

The same script scores a lag-12 benchmark with a lag-1 denominator.

**Fix:** one line - a lag-12 difference, with the documented fallback to m = 1
for series shorter than 13 observations. Affects `mase.csv` / `mase.md` only; no
retrain required. **Independently shippable.**

---

## F10 - The lag set contains no multiple of 12, and one comment states the error

**Source:** five independent confirmations in the scan - 2.8, 5.2, 7.4, 9.9, 2.7.
**Site:** `_shared_modules/engineer_features.py:33`.

```python
DEFAULT_LAGS: tuple[int, ...] = (1, 2, 3, 4, 8, 13)
DEFAULT_ROLLING_WINDOWS: tuple[int, ...] = (4, 13)
```

**No element is a multiple of 12.** The book is unambiguous that for monthly data
the informative seasonal lags are **12 and 24** (2.7: "strongly positive at lags
4 and 8" for quarterly m = 4; 9.9: seasonal spikes read at lags 12, 24, 36).

### The naming convention is NOT the bug - read it carefully

`engineer_features.py:516` applies `shift(lag + _h)` where `_h = horizon - 1`,
and the column keeps the **nominal** name. This is deliberate and documented
(lines 508-514): the name is stable across horizons so a cross-horizon comparison
can line the columns up. So `lag_13` really does mean 13 months back.

**The defect is the choice of 13, and one comment says so out loud:**

> `training_report.py:180` - `"lag_13": "same month last year"`

**Same month last year is 12 months back, not 13.** The comment describes the
feature the model should have and does not have.

### The repo already knows the right answer elsewhere

`run_seasonal_naive` uses `hist[-12]`, and the archived
`registry_and_forecasting.ipynb:1418` reads `row_df["lag_12"]` for its seasonal
naive. **The correct lag existed in an earlier generation and was lost.**

**Cost of the error:** the models get a lag one month out of phase with the
annual cycle, AND `train_and_persist.py:229` drops rows on
`dropna(subset=[..., "lag_13"])`, so the off-by-one also costs one extra row of
warm-up history per brand on an already short panel.

**Fix:** `(1, 2, 3, 4, 8, 13)` -> include **12** (and 24 where history allows);
same for the rolling window 13 -> 12. **Requires a matrix rebuild and retrain.**

---

## F11 - Two model-side checks: one defect confirmed, one CLEARED

**Site:** `srq1/srq1_baselines_stat.py`.

### CONFIRMED DEFECT - ARIMA (restates F8 with the source attached)

```python
m = SARIMAX(y, order=(1, 1, 1), enforce_stationarity=False,
            enforce_invertibility=False)      # line 283
```

9.7 gives the procedure this replaces in full: **d by repeated KPSS tests**, then
**p, q, c by minimising AICc** over a stepwise search. 9.9 adds
`unitroot_nsdiffs` for the seasonal D. Three defects in one line:

1. no seasonal `(P,D,Q,12)` on seasonal monthly data
2. fixed orders, no information criterion anywhere in the repo
3. **`enforce_stationarity=False`** disables the guard 9.7 says `ARIMA()`
   *always* applies: "The `ARIMA()` function will **never** return a model with
   inverse roots outside the unit circle... such models will be potentially
   problematic."

### CLEARED - Prophet is correctly configured

12.2 warns that "the seasonal term **must have the period fully specified** for
quarterly and monthly data, as the default values assume the data are observed at
least daily." **Checked (line 293):**

```python
m = Prophet(yearly_seasonality=True, weekly_seasonality=False,
            daily_seasonality=False)
```

Annual seasonality on by name, both sub-monthly seasonalities off by name.
Nothing relies on a daily-tuned default. **No action.** Recorded so the check is
not silently repeated.

Worth noting for Ch5: Prophet's seasonality **is Fourier terms** (order 10
annually by default). The project already runs a model with a continuous seasonal
representation while feeding its ML models three calendar integers.


---

## F10a - AMENDMENT: the repo's OWN PROVENANCE FIELD says lag-12

**Found after F10 was written. This is the strongest single piece of evidence in
the plan, and it is entirely internal - the book is not needed to make the case.**

**Site:** `_shared_modules/step_3_derive_params.py:211-216`, inside
`derive_lag_structure()`, whose docstring says provenance "is what lets the
contract answer *why this value* without anyone reading this file, and it is what
shows a reviewer whether a number was measured or decided."

```python
provenance = {
    "lags": (
        "modelling decision; the lag-12 term is retained because the "
        "autocorrelation analysis (step 2, section 3.16) finds it "
        "significant across the majority of leading brands"
    ),
```

**The provenance documents a lag-12 term. The code it describes is
`DEFAULT_LAGS = (1, 2, 3, 4, 8, 13)`, which contains no 12.**

This text is written into every category's contract JSON. It cites a **measured**
result - an ACF analysis that found **lag 12** significant - as the justification
for a feature the pipeline does not build.

### Four independent in-repo confirmations that 12 is the intended value

| Site | Says |
|---|---|
| `step_3_derive_params.py:213` | provenance: **"the lag-12 term is retained"** |
| `srq1_baselines_stat.py:167` | `hist[-12]` - seasonal naive reads **12** months back |
| `training_report.py:180` | `lag_13` described as **"same month last year"** (which is 12) |
| archived `registry_and_forecasting.ipynb:1418` | `row_df["lag_12"]` for seasonal naive |

Plus five in the book (2.7, 2.8, 5.2, 7.4, 9.9). **The only place that says 13 is
the feature matrix itself.**

**This reframes the finding.** It is not "the literature prefers 12." It is: the
project measured 12, documented 12, benchmarks with 12 - and engineers 13.

---

## F10b - The warm-up arithmetic: fixing this ADMITS brands, adding lag 24 EXCLUDES them

**Site:** `step_3_derive_params.py:200-203`.

```python
warmup = max(max(lags), max(windows))     # currently 13
min_periods = warmup + horizon + 1        # 13 + 3 + 1 = 17 at H=3
```

`min_periods` is the brand-eligibility threshold - "a brand with fewer months
contributes zero usable training rows."

| Lag set | warm-up | `min_periods` at H=3 | Effect on brand count |
|---|---|---|---|
| current `(1,2,3,4,8,13)` | 13 | **17** | baseline |
| corrected `(1,2,3,4,8,12)` | 12 | **16** | **admits MORE brands** |
| extended `(1,2,3,4,8,12,24)` | 24 | **28** | **excludes many** on a 39-month panel |

**Two consequences for the plan:**

1. **The 13 -> 12 correction is strictly favourable.** It fixes the phase error
   *and* lowers the history requirement by one month. It does not trade accuracy
   against sample size - it improves both. `rolling_mean_13` -> `rolling_mean_12`
   likewise ("13-month mean (annual level)" - an annual level is 12 months).
2. **Lag 24 must NOT be added blindly.** 9.9 reads seasonal structure at 12, 24
   and 36, but on 39 visible months a 24-lag costs 28 months of warm-up. Any
   proposal to add it must report the brand count it would exclude **before** it
   is adopted. Fourier terms (7.4) give the annual cycle **without** consuming
   warm-up at all, which is a further argument for preferring them.

### A bonus for Ch6, not a complication

`ch6-CONSOLIDATED-pass.md:981` and `anticipated-assessor-questions.md:251` both
answer *"if the model needs thirteen months of lag depth, how does it answer
today?"* The corrected feature set needs **twelve**, so that argument gets
slightly easier, not harder. The prose will need the number changed.

---

## F10c - The defect has already reached the prose (Phase 5 scope)

Three places state the seasonal claim that the lag set does not support:

| Where | Text | Problem |
|---|---|---|
| `sections-drafts/data-assessment.md:293` | "`lag_1` ... `lag_13` \| Lagged `sales_units` (short, medium, **seasonal**)" | no lag in the set is a multiple of 12 |
| `sections-drafts/data-assessment.md:295` | "`rolling_mean_13` \| **Trailing annual average**" | an annual average is 12 months |
| `sections-drafts/model-benchmark.md:87` | Prophet defence: "yearly seasonality reduces to roughly twelve points that the tabular models **already capture through `month`, `quarter` and `lag_13`**" | the capture is off by one month |

The Ch5 snapshot carries the same table row, so the `.docx` has it too.

**Note the direction of the Prophet argument.** It currently says the tabular
models already capture annual seasonality, so Prophet adds nothing. If `lag_13`
is off-phase that defence is weaker than stated - and once corrected to `lag_12`
it becomes **stronger**. Fixing the feature improves the existing argument rather
than undermining it.


---

## F10d - THE MEASUREMENT VERIFIED: lag 12 is significant for 20 of 20 brands

F10a showed the *provenance* claims lag-12. This checks the **measurement behind
it**, in the shipped EDA tables at
`{Category}/pipeline_step_outputs/{cat}_eda_tables/step_2_16_acf_significant_lags.md`.

Criterion (stated in each table): sample ACF exceeding
`+/- 1.96 / sqrt(n)`, "the standard criterion... (Box and Jenkins, 1970)",
computed on the **log-transformed** target - i.e. the form in which it is modelled.

| Category | n | Brand | Significant lags | 12? | 13? |
|---|---|---|---|:-:|:-:|
| CSD | 46 | HARBOE | `[1, 2, 3, 9, 12, 15]` | **Y** | N |
| CSD | 46 | COCA COLA | `[1..15]` | **Y** | Y |
| CSD | 46 | PEPSI | `[1..15]` | **Y** | Y |
| CSD | 46 | FAXE KONDI | `[3, 6, 9, 11, 12, 14, 15, 17, 18, 20, 21]` | **Y** | N |
| CSD | 46 | FANTA | `[3, 6, 9, 12, 15, 17, 18, 20, 21]` | **Y** | N |
| Energidrikke | 43 | RED BULL | `[3, 6, 9, 12, 15, 18]` | **Y** | N |
| Energidrikke | 43 | MONSTER ENERGY | `[1, 2, 3, 6, 9, 10, 12, 15, 18]` | **Y** | N |
| Energidrikke | 43 | FAXE KONDI BOOSTER | `[1, 2, 3, 4, 6, 9, 10, 11, 12, 15, 18]` | **Y** | N |
| Energidrikke | 43 | CULT | `[1..15]` | **Y** | Y |
| Energidrikke | 43 | STATE | `[1, 2, 3, 6, 9, 12, 18]` | **Y** | N |
| Danskvand | 41 | HARBOE | `[1, 2, 3, 4, 6, 9, 10, 11, 12, 13, 15]` | **Y** | Y |
| Danskvand | 41 | BLUE KELD | `[3, 12, 15]` | **Y** | N |
| Danskvand | 41 | FIRST PRICE | `[1, 2, 4..8, 10, 11, 12, 13, 16..19]` | **Y** | Y |
| Danskvand | 41 | AQUA D'OR | `[1, 2, 7, 11, 12, 13, 14, 15, 19]` | **Y** | Y |
| Danskvand | 41 | KILDEVAELD | `[1, 2, 4..8, 10..14, 16, 17, 18]` | **Y** | Y |
| RTD | 41 | BREEZER | `[6, 8, 12, 14]` | **Y** | N |
| RTD | 41 | SHAKER | `[6, 12, 13, 14, 15, 18]` | **Y** | Y |
| RTD | 41 | SMIRNOFF ICE/TWISTED | `[2, 6, 12, 13, 14, 16, 18]` | **Y** | Y |
| RTD | 41 | SOMERSBY | `[1, 4..8, 11, 12, 13, 16..19]` | **Y** | Y |
| RTD | 41 | MOKAI | `[1, 5, 6, 12, 13, 18, 19]` | **Y** | Y |

### The result

| | Brands |
|---|---|
| **Lag 12 significant** | **20 of 20 (100%)** |
| Lag 13 significant | 10 of 20 (50%) |
| Lag 13 significant **without** 12 also significant | **0 of 20** |

**Lag 12 is significant for every leading brand in every category. Lag 13 never
appears independently** - wherever it is significant, 12 is too, so it is reading
the shoulder of the annual peak rather than carrying its own signal.

In CSD, the flagship category, lag 13 is significant for **2 of 5** brands while
lag 12 is significant for **5 of 5**.

**HARBOE - one of the three brands in the SRQ4 experiment - is
`[1, 2, 3, 9, 12, 15]`: lag 12 significant, lag 13 NOT.**

### The complete chain, all internal

1. ACF measures **lag 12** significant for 20/20 brands
2. The EDA table states *"Significance at lag 12 indicates annual seasonality"*
3. The contract provenance states *"the lag-12 term is retained"*
4. All four manifests ship `lags: [1, 2, 3, 4, 8, 13]`

**The one lag that was actually measured is the one lag that did not reach the
feature matrix.** No appeal to the textbook is needed to establish this; the book
(five sections) merely explains *why* 12 is the right answer for monthly data.

### A second pattern the feature set also misses

Multiples of **3** recur across almost every brand (3, 6, 9, 12, 15, 18) -
quarterly structure. The lag set carries 1, 2, 3, 4, 8 and nothing at 6 or 9.
**Fourier terms (7.4) capture the annual cycle and its harmonics together**,
which is a further argument for preferring them to more individual lags,
especially given the warm-up cost established in F10b.

### One caveat to carry into the prose, stated by the table itself

> "The confidence band assumes a stationary series; where the stationarity tests
> are inconclusive, significance at long lags may reflect **trend rather than
> genuine seasonal dependence**."

This is the repo being careful, and it connects to P0051 F2 (27 of 79 brands
already stationary) and to 9.1's warning on over-differencing. It does not weaken
the 12-vs-13 finding - that comparison is between two adjacent lags under the
identical band - but it should be quoted rather than suppressed.

---

## F12 - Pre-existing prose drift in the same table Phase 5 must edit

Not caused by this plan, but it lands in the same place and should be fixed in
one pass rather than two.

`sections-drafts/data-assessment.md` states **`MIN_PERIODS = 30`** in four places
(lines 216, 242, 345, 348) and describes it as "the adopted filter... retains 77
brands". The code **derives** it: `warmup + horizon + 1` = **17** at H=3, and all
four shipped manifests carry `min_periods: 17`.

The draft already knows something is wrong - line 205 records *"Table 2
(parameters) has two wrong rows: MIN_PERIODS 30 and the 24/6/12 split"* and line
341 lists *"Stale numbers to correct here: MIN_PERIODS=30, 'CSD (42 periods, 77
brands)' -> 46 and 95."*

**Do not silently amend these.** Establish first whether 30 was a *separate
brand-retention filter* applied before feature engineering (the line 216 wording
"30 non-zero monthly observations" suggests it may have been) or simply a stale
figure. The two readings imply different corrections, and F10b changes
`min_periods` again. Flag to Brian rather than guess.


---

## F12 - RETRACTED. The draft already records the correct position.

**F12 claimed `sections-drafts/data-assessment.md` carries live drift because it
states `MIN_PERIODS = 30` in four places. That is wrong, and the correction was
fourteen lines above the region I read.**

`data-assessment.md:89-92` states it explicitly:

> "**Retention threshold is DERIVED, not chosen**: `min_periods = warmup +
> horizon + 1` = **15 at H1, 17 at H3**. The >=30 / >=40 thresholds are **gone** --
> three competing fixed values were removed 2026-08-18. This **retracts a
> limitation rather than restating one.** Evidence:
> `_shared_modules/engineer_features.py`. (thread 146)"

And line 93 carries the corrected retention:

> "**Brands retained: 95 / 29 / 44 / 62** (CSD / danskvand / energidrikke / RTD),
> **superseding 77 / 24 / 27 / 42**. Evidence: `*_manifest_h3.json`. (thread 143)"

So the `MIN_PERIODS = 30` occurrences at lines 216, 242, 345 and 348 are
**superseded text the ledger has already marked stale** - exactly what lines 205
and 341 record as "wrong rows" and "stale numbers to correct here". They are a
known, tracked editing task in the `.docx`, not an undiscovered defect.

**The claims ledger worked as designed.** My recommendation to "flag to Brian
rather than guess" was unnecessary; the file answered the question itself.

### What this corrects in F10b

F10b's arithmetic stands - `warmup + horizon + 1`, and the effect of changing the
lag set on brand eligibility is real. But the **baseline is 17 at H3 and 15 at
H1**, already correctly documented in both the code and the draft. F10b should
not be read as implying the current threshold is undocumented or wrong.

### The lesson for the Phase 5 prose pass

Read a draft's **status and correction blocks before its tables**. This file
interleaves superseded content with the notes retracting it, which is what a
claims ledger is *for*; treating any single region as current misreads it.


---

## F10e - The lag set is declared TWICE; both sites must move together

**Site 2:** `_shared_modules/pipeline_config.py:84-89`.

```python
# Features use up to lag-13 and rolling-13, so the first 13 rows per brand carry
# NaN features and must be excluded from training / evaluation.
MAX_LAG: int = 13                    # lags: (1, 2, 3, 4, 8, 13)
MAX_WINDOW: int = 13                 # rolling windows: (4, 13)
WARMUP_PERIODS: int = max(MAX_LAG, MAX_WINDOW)   # = 13
```

This **mirrors** `engineer_features.py:33` (`DEFAULT_LAGS`) rather than importing
it. So the lag structure is stated in two files that must agree, and the comment
here restates the tuple a third time.

**Any 13 -> 12 change must edit both**, or `WARMUP_PERIODS` and the features drift
apart silently - the exact class of failure `_features.py` was created to end
("Eleven live copies, and they had already drifted").

### The good news: the propagation is designed to work

```
# Because it is derived, it follows the lag structure automatically: MAX_LAG=6
# yields 9, MAX_LAG=3 yields 6. Do not hardcode a replacement.
MIN_PERIODS: int = WARMUP_PERIODS + FORECAST_HORIZON + 1   # = 15
```

`MIN_PERIODS` tracks the lag set by construction (DEC-MINPERIODS). So correcting
`MAX_LAG` to 12 moves `WARMUP_PERIODS` to 12 and `MIN_PERIODS` to 14 at H=1 /
16 at H=3, automatically and correctly - **which is the property F10b relies on.**

The `# = 15` and `# = 13` trailing comments are stale-able literals beside
computed values; they should be updated in the same edit.

### Measured evidence already in this file, worth reusing

> "Measured 2026-08-18 across all four categories: this threshold costs **0.0% of
> training rows** relative to imposing no threshold, because the brands it drops
> were each contributing zero. The previous hardcoded 40 cost 20.5% (CSD), 16.8%
> (Danskvand), 40.8% (Energidrikke) and 30.2% (RTD)."

Lowering the warm-up by one month can only **weakly increase** retention from a
baseline that already costs 0.0% of training rows. **The correction cannot lose
data.** That closes the last risk attached to F10.

### Complete fix list for the lag correction

| # | Site | Change |
|---|---|---|
| 1 | `engineer_features.py:33` | `DEFAULT_LAGS` 13 -> 12 |
| 2 | `engineer_features.py:34` | `DEFAULT_ROLLING_WINDOWS` 13 -> 12 |
| 3 | `pipeline_config.py:87-89` | `MAX_LAG`, `MAX_WINDOW`, and the two comments |
| 4 | `srq1/_features.py:57,61` | `lag_13` -> `lag_12`, `rolling_mean_13` -> `rolling_mean_12` |
| 5 | `train_and_persist.py:229` + `training_report.py:112,133,152,294` + `srq1_calibration.py:240` | `dropna(subset=[..., "lag_13"])` |
| 6 | `training_report.py:180,183` | the descriptions ("same month last year", "13-month mean") |
| 7 | prose (F10c) | three claims in two draft files + the `.docx` |

**Sites 1-6 are a mechanical rename plus two constants. Site 7 is Phase 5.**
Nothing here is architectural, and none of it touches the SRQ4 experiment.


---

## F10f - CORRECTION to F10e: the rename reaches SRQ2, and the site list was short

**F10e ended: "Nothing here is architectural, and none of it touches the SRQ4
experiment." The second half stands. The framing around it was wrong, and the
fix list was incomplete.**

### The omission

`02_SRQ2_Tool_Interface/forecast_tool.py:488`:

```python
d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"])
```

**`forecast_tool.py` is the typed tool the agent calls - the SRQ2 artefact.** The
rename therefore crosses an SRQ boundary that F10e's site list did not mention
and its closing sentence implied it stayed inside.

### The real scope: 20 live files, not 7 sites

A repo-wide search for `lag_13` / `rolling_mean_13` / `MAX_LAG` / `DEFAULT_LAGS`
returns **20 non-archived Python files**:

| Tier | Files |
|---|---|
| **01 preprocessing** | `engineer_features.py`, `pipeline_config.py`, `step_3_derive_params.py` |
| **01 modelling** | `_features.py`, `train_and_persist.py`, `training_report.py`, `srq1_benchmark.py`, `srq1_benchmark_cv.py`, `srq1_benchmark_tuned.py`, `srq1_calibration.py`, `srq1_pooled.py`, `srq1_ridge_pooled.py`, `srq1_ridge_cv.py`, `srq1_mase.py`, `srq1_profiling.py`, `srq1_feature_diagnostics.py`, `srq1_holiday_ablation.py`, `srq1_holiday_ablation_tuned.py`, `srq1_generate_performance_figures.py`, `srq1_generate_shap_figures.py` |
| **02 tool interface** | **`forecast_tool.py`** |

Most occurrences are the same `dropna(subset=[..., "lag_13"])` guard repeated
per script - the literal-duplication pattern `_features.py` was created to end,
surviving in the row-filter rather than the feature list.

### What this does and does not change

**Does not change:** the SRQ4 experiment harness, the prompt schema, the agent
input contract, or the leakage boundary. `forecast_tool.py` is touched at a
**row-filter literal**, not at its interface, payload shape or typed contract.
The 63 paid runs stay valid. **F10e's conclusion holds; its reasoning was
under-evidenced.**

**Does change:** the claim that this is confined to SRQ1. It is a
**cross-tier rename**, so it belongs in the plan as one atomic change touching
three tiers, not as a preprocessing tweak. If it is done, `forecast_tool.py`
must be re-verified against a rebuilt matrix, because a stale `lag_13` reference
there would make `dropna` silently drop **every** row (the column would no longer
exist -> KeyError, or worse, if a rename left both).

### The generalisable defect underneath

`dropna(subset=["log_sales_units", "lag_1", "lag_13"])` hardcodes **which lag is
the longest** in 20 places. It should ask the feature set:

```python
d = fm.dropna(subset=["log_sales_units", *_features.LAGS])
```

or guard on the resolved columns. Then a lag-set change propagates the way
`MIN_PERIODS` already does (F10e) instead of requiring 20 coordinated edits.
**Worth proposing as the actual fix**, since it removes this whole class of
error rather than moving it from 13 to 12.
