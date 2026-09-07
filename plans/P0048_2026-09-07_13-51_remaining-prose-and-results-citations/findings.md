---
pid: P0048
created: 2026-09-07 16:40:00
updated: 2026-09-07 16:40:00
---

# P0048 — Findings

Every finding below was measured in-session, not inferred. Each carries the command
or file that reproduces it, because the session that found them is not recoverable.

---

## F1 — The forecast horizon never reaches feature construction (**critical**)

`engineer_features()` in
`01_SRQ1_Model_Training/01_thesis_data/_02_preprocessing/nielsen/_shared_modules/engineer_features.py`
has **no `horizon` parameter**, and `step_4_engineer_features.py` passes none. Lags
are built as `g[target_col].shift(lag)`, so `lag_1` is month *t−1* at every horizon.

At a genuine 3-month horizon, forecasting *t* from origin *t−3*, `lag_1` must be
*t−3*.

**Reproduce:** merge the two CSD matrices on `brand × period_year × period_month`.
Across all 4,370 shared rows, `sales_units`, `lag_1`, `lag_3`, `lag_13` are identical.
The sole difference between h1 and h3 is `min_periods` (15 vs 17), dropping 11 brands
and 506 rows.

`grep -n "horizon" engineer_features.py` returns **only comment lines** — the word
never appears in executable code.

**Verdict: a bug, not a simplification.** Step 3's docstring states the intent
explicitly ("The primary reported horizon is 3 months... Both are real runs, so
`--horizon` is a CLI argument"), and the surrounding plumbing is deliberate:
`min_periods = warmup + horizon + 1`, `n_origins = n_test − horizon + 1`, plus a
contract that hard-fails if the filename horizon disagrees with the body. Nobody
documents a design that precisely and then intentionally omits its implementation.

**Fix:** lags become `shift(lag + h − 1)`; rolling windows shift identically. One
function. Everything downstream of it is already correct.

---

## F2 — The published SRQ1 results are the h3 file, and there are no H1 results

Every SRQ1 script hardcodes `_feature_matrix_h3.parquet` inline. `grep -rn "_h1"` over
`01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/*.py` returns
**nothing**. No horizon CLI flag exists (only `--trials`, `--grain`, `--grains`).

Confirmed by row count. `summary.md` reports CSD `n_train 1805, n_test 665,
n_series 95`. After `dropna(subset=["log_sales_units","lag_1","lag_13"])`:

| matrix | train | test | series |
|---|---|---|---|
| h1 | 2014 | 742 | 106 |
| **h3** | **1805** | **665** | **95** |

Combined with F1: **the thesis reports one-month-ahead accuracy while describing a
three-month horizon.** Benchmarking "both horizons" today would produce two nearly
identical result sets differing only by brand coverage — which would not support the
1-month vs 3-month storyline, and a reader comparing them would notice.

**19 scripts need the hardcoded `_h3` parameterised** before both horizons can run.

---

## F3 — The feature count is 13, not 14; `weighted_distribution` is not a model input

`srq1_benchmark.py::FEATURES` has 13 entries and does **not** contain
`weighted_distribution`. Confirmed against the trained artefacts at
`05_thesis_results/srq1_model_performance/models/<cat>/metadata.json`:

| category | n features |
|---|---|
| CSD | 13 |
| energidrikke | 13 |
| danskvand | **12** |
| RTD | **12** |

Promo-zero categories omit `promo_intensity` rather than zero-filling — a constant-zero
column would assert "no promotion ran", which the data does not support
(DEC-DISCOVER-COLUMNS). So the feature set genuinely differs across categories, and
cross-category comparison must account for a difference in available *information*,
not just values.

**The thesis is wrong, not the code.** Ch4 §4.3 asserts `weighted_distribution` "**is**
the fourteenth input feature".

**Resolves discrepancy 2 in the holiday note**: post-enrichment the count is **16**,
not 17.

---

## F4 — The split is proportional and recomputed, not locked or pre-registered

`resolve_split_cutoffs()` derives **70 % / 15 % / remainder** over distinct periods
(`DEFAULT_TRAIN_FRAC = 0.70`, `DEFAULT_VAL_FRAC = 0.15`).

The code comment records why fixed dates were abandoned: they had drifted to a
24–27 % test share against an intended 15 %, because every refreshed month lands in
whichever split is the remainder.

Current boundaries, from the 8 step-3 contracts (identical at both horizons):

| Category | Periods | Train | Val | Test | Train end | Val end |
|---|---|---|---|---|---|---|
| CSD | 46 | 32 | 7 | 7 | 2025-05 | 2025-12 |
| Danskvand | 41 | 29 | 6 | 6 | 2025-07 | 2026-01 |
| Energidrikke | 43 | 30 | 6 | 7 | 2025-06 | 2025-12 |
| RTD | 41 | 29 | 6 | 6 | 2025-07 | 2026-01 |

**The panel has grown** — CSD is 46 periods, not the 42 the thesis states.

Ch4 §4.4 is wrong on all counts, and **Brian's own Word threads already say so**: 183
("Dynamic Train/Test/Val sets based on percentage cutoff"), 185 ("Not locked"), 187,
191 ("All test windows end in March 2026" — they end 2026-07). All eight threads
(183–191) are closable by one section replace.

**Side effect:** training windows are now 29–32 months, so the "~24-period ARIMA
minimum; danskvand and RTD at 23 are marginally below" caveat is obsolete. The
staged prose **drops** that claim rather than sourcing it, which closes threads 184
and 189 by removing what they objected to.

---

## F5 — SRQ4 can evaluate at H3 with ground truth retained

`_brand_history()` in `04_SRQ4_Scenario_Experiment/scenario_setup/srq4_experiment.py`
is well built: it returns the target month **explicitly** (so Scenario A cannot anchor
on wall-clock time and score a different month than B and C), and `_assert_no_leakage`
hard-fails if the target appears in the history handed to an agent.

Measured today: last fit month **2025-12** → target **2026-01** = a **1-month** gap at
both h1 and h3, because it takes `test.iloc[0]`.

There are **7 held-out test months** (2026-01 … 2026-07) with actuals present.
Evaluating at 3 months requires selecting `test.iloc[2]` and ending the supplied
history 3 months before target. The leakage assertion already covers the wider gap.

**Brian's requirement — verify against held-out real values for every scenario — is
satisfiable at H3.**

---

## F6 — MIN_PERIODS is derived, which retracts a stated limitation

`min_periods = warmup + horizon + 1` → **15 at H1, 17 at H3**
(`derive_lag_structure()`). A brand-month is usable only once its lag features are
defined, so a shorter series yields no usable observation under the specification.

The thesis states MIN_PERIODS = 30 and concedes it as "EDA-driven, not theory-first"
— a limitation. It is now *derived*, so that concession can be **retracted**, not
merely renumbered. Worth writing deliberately.

A third live value (40, in the old notebook) was removed 2026-08-18 for the same
reason.

---

## F7 — Ch8 accuracy numbers are stale twice over

Ch8 §8.2 states "Test WMAPE: CSD 16.5%, danskvand 22.0%, energidrikke 11.4%
(≈ the ≤15% industry target), RTD 31.0%".

Current `tuned_summary.md` (tuned XGBoost): CSD **15.0**, danskvand **20.9**,
energidrikke **13.1**, RTD **36.0**. RTD moved materially worse.

So the numbers are wrong against current output *and* they describe a horizon the
pipeline does not implement (F1). Both need the re-run.

Note also the "≤15% industry target" phrasing — P0041 recorded that target as
**unsourced and withdrawn** from Ch6/Ch9/Ch10. It appears to survive here.

---

## F8 — Chapter 8's design subsections are still bullets with stale placeholders

Ch8 splits cleanly: every **Results** subsection is real prose with real numbers,
while every **design** subsection is unconverted bullets — Benchmark design, Metrics,
Baselines, LLM-as-Judge protocol, Calibration check, RAM profiling, Latency profiling,
Failure mode analysis.

Some carry placeholders that were never filled: `[N] SKUs × 28 retailers × [T] weeks`.
The weekly framing also contradicts the brand × month grain locked since DEC-GRAIN.

Ch7 (1,189 w), Ch8 (1,339 w) and Ch9 (1,194 w) are the thin chapters. Ch4 is in better
shape than expected — genuine prose throughout — but its numbers are stale (F3, F4).

---

## Cross-cutting: the results folder is almost entirely uncited

`05_thesis_results/` holds ~317 files:

- **26 appendix tables**, export-ready, regenerated 2026-09-07 by `export_appendix.py`
- **44 SRQ1 tables** (`srq1_model_performance/tables/`)
- **per category: 31 EDA tables + 8 plots** — seasonal decomposition, ACF/PACF, ECDF,
  correlation heatmaps, promo intensity

The thesis cites **2 figures total** (`table-of-figures.md`). Chapter 4 cites none of
the EDA plots.

Also visible in `table-of-tables.md`: **Table 10 is captioned "NO IDEA"**, and Tables
9 and 12 carry typos ("Exclud", "adn"). Cosmetic, but they are in the document.
