---
name: 2026-08-19_preprocessing-pipeline-handover-enrico
description: HANDOVER - The CSD notebook is retired and replaced by a shared 7-step pipeline running all four categories; how to regenerate it locally, what changed in the numbers, and where to pick up
category: reference
applies-to: [02_thesis_data, 03_thesis_modelling, 04_thesis_results]
triggers: [handover, regenerate eda, run pipeline, enrico]
created: 2026_08_19-01_30
updated: 2026_08_19-01_30
---

# Handover — preprocessing pipeline rebuilt (2026-08-18/19)

**For:** Enrico
**From:** Brian
**Covers:** 29 commits, `6057557` → `634415b`

---

## TL;DR

The CSD notebook is **retired**. In its place there is one shared pipeline that runs
**all four categories** from a single codebase, at two forecast horizons.

Three things changed that affect numbers you may already have quoted:

1. **The train/val/test split was wrong** and is now fixed (test was 29.5% of rows,
   should be ~15%).
2. **Prediction intervals were 4.4× too narrow** — they were calibrated against data
   the model had already seen.
3. **Two features were reading the month they were supposed to predict** and have been
   removed from model inputs.

Any figure produced before 2026-08-18 should be re-derived.

---

## 1. How to regenerate the EDA pipeline on your machine

### 1.1 The data is NOT in git — this is the part that will trip you up

`.gitignore` excludes `*.parquet` and `*.jsonl`. A fresh clone gives you **all the
code and none of the data**, and the pipeline will fail at step 0 with a missing-cache
error.

You need the **converted parquet views**, not the raw export:

| Tree | Size | Do you need it? |
|------|-----:|-----------------|
| `02_thesis_data/_00_raw/nielsen/` | **38 GB** | **No** — only if re-converting from source |
| `02_thesis_data/_01_converted/nielsen/parquet_nielsen/*/views/` | **1.3 GB** | **Yes** — this is what the pipeline reads |

Copy just the `views/` folders (CSD 735 MB, Energidrikke 266 MB, RTD 153 MB,
Danskvand 75 MB) into the same relative paths. Each category needs its four view
files: facts, `dim_product`, `dim_period`, `dim_market`.

If you ever do need to rebuild from raw:

```bash
python 02_thesis_data/_01_converted/nielsen/jsonl_to_parquet_script/run_all_conversions.py
```

It is idempotent (skip-if-newer), so it is safe to re-run.

### 1.2 Dependencies

```bash
pip install -r requirements.txt
```

**I added four packages on 2026-08-19** that were missing: `scikit-learn`, `xgboost`,
`lightgbm`, `prophet`. Without them the preprocessing pipeline runs but the modelling
layer silently degrades — `srq1_benchmark` printed `ERR` for every ML row because the
import error was swallowed into the results table rather than raised, and Prophet
reported `n_series=0` with `nan` metrics.

If you cloned before that commit, re-install.

### 1.3 Run it

Everything lives in **one folder**:
`02_thesis_data/_02_preprocessing/nielsen/_shared_modules/`

```bash
cd 02_thesis_data/_02_preprocessing/nielsen/_shared_modules

# one category, one horizon, steps 0-6
python run_preprocessing.py --category CSD --horizon 3

# everything: 4 categories x 2 horizons
python run_preprocessing.py --all-categories --horizons 1,3
```

Runtimes on Brian's machine: CSD ≈ 70s end to end; a full sweep of all four
categories at both horizons ≈ 3 minutes. **No warehouse connection needed** — step 0
validates the local parquet cache; nothing calls Nielsen.

Useful flags:

| Flag | Why |
|------|-----|
| `--skip-shared` | skip steps 0-2 (horizon-independent) when iterating on the contract |
| `--from-step N --to-step M` | re-run a slice, e.g. `--from-step 6 --to-step 6` to rewrite outputs only |
| `--no-plots` | step 2 computes tables without rendering figures |
| `--horizons 1,3` | runs both; steps 0-2 execute once and are skipped for the second |

Steps 0-2 do not depend on the horizon, so a second horizon costs seconds rather than
minutes (Danskvand: 25.4s for H=1, then 2.0s for H=3).

### 1.4 What you get, and where

| Output | Location |
|--------|----------|
| EDA plots, tables, console logs | `nielsen/{Category}/pipeline_step_outputs/` |
| Feature matrix, split dates, manifest | `_03_engineered/bymonth/{Category}/*_h{N}.*` |

Everything is horizon-suffixed (`_h1`, `_h3`). If you see a file without a suffix it is
pre-2026-08-18 and stale.

### 1.5 Sanity check

A clean run ends with `All 8 run(s) completed.` and exit code 0. Split geometry should
match:

| Category | train/val/test | brands | features |
|----------|----------------|-------:|---------:|
| CSD | 32/7/7 | 95 | 31 |
| Danskvand | 29/6/6 | 29 | 23 |
| Energidrikke | 30/6/7 | 44 | 31 |
| RTD | 29/6/6 | 62 | 30 |

Feature counts differ **on purpose**: Nielsen does not report promotion for Danskvand
or RTD, so `promo_intensity` is omitted for those categories rather than zero-filled.
A constant-zero column would assert "no promotion ran", which the data does not
support and a model would learn from.

---

## 2. What changed, and why it matters for numbers you may hold

### 2.1 The split was broken (`888e192`)

The old notebook used hardcoded cutoff dates that never moved as data accumulated:

| | train | val | test |
|--|------:|----:|-----:|
| notebook | 1,450 | 348 | **754 (29.5%)** |
| pipeline | 3,040 | 665 | **665 (15.2%)** |

The test set was more than double its intended size. Cutoffs are now derived
proportionally per category and recorded in the contract.

### 2.2 Prediction intervals were 4.4× too narrow (`634415b`)

`build_service` fitted on **all** data (train+val+test) and then measured its error on
the **test** rows — rows the model had already seen. The residuals were in-sample, so
the interval measured how well the model recalled its training data, not how well it
generalises.

| | a 10,000-unit forecast |
|--|---|
| old | [7,604 … 13,151] |
| **honest** | **[3,002 … 33,309]** |

Now: fit on train, calibrate on val, leave test alone.

**Consequence worth discussing**: all 230 served forecasts now report `Low` confidence,
and the median 90% interval spans **3× the forecast**. That is the real uncertainty of
monthly brand-level demand on 29-46 months of history. It should be reported openly —
it also gives System B a fairer comparison in SRQ4.

### 2.3 Features that read the future (`5cbf76c`, `9498ffb`)

Two separate cases, both found by testing rather than reading:

- **`zero_run_flag` / `zero_run_length`** were computed from `sales_units` at time *t* —
  the value being forecast. Verified 100.00% identical to `(sales_units == 0)`. It was
  invisible in the notebook because that matrix had **zero** zero-rows; the current
  parent-scope matrix has 588 (13.5%). Restored in lagged form.
- **`sales_value` / `sales_liters`** are the same month's trading in kroner and litres.
  They sat in the manifest's feature list. Adding them improves CSD WMAPE 17.20% →
  15.02% — a 2.2pp gain bought by reading the month being predicted. Now excluded via
  `CONTEMPORANEOUS_COLS`.

### 2.4 `holiday_month` → `peak_month` (`2fea7a0`)

The feature never consulted a holiday calendar; it flags months with above-average
sales. Evidence contradicted the holiday reading in 3 of 4 categories (CSD peaks at
quarter-ends — trade loading; Danskvand in summer — weather). The old name is also how
a wrong constant `{1,4,6,10,12}` survived review: read as "peak months for soft
drinks", January is obviously wrong at −26.6%.

**This touched Ch1 and Ch4 prose**, which stated a holiday data source that does not
exist.

### 2.5 `weighted_dist` dropped from model inputs (`f4779a7`)

**Not** because it leaks — it was tested and cleared (it is structural and nearly
static, corr(t, t−1) = 0.976). Dropped because it does not improve accuracy: worse in
**3 of 4** categories. The column stays in the matrix for EDA.

### 2.6 Metric reporting (`5f2e9b7`)

- **`mean MAPE` dropped** from the benchmark table. It read 10¹²–10¹⁵ % for every
  model *including SeasonalNaive*, because MAPE divides by the actual and 13.8% of CSD
  test rows are exactly zero. Still in `metrics.csv` as evidence.
- **medMAPE is now the headline** for the statistical baselines; WMAPE is retained with
  a caption. WMAPE is unbounded, so one diverged series sets the category figure — CSD
  Prophet's was 60% a single brand.
- **`log`/`expm1` mismatch fixed** in both baselines: they fitted with `np.log()` and
  inverted with `np.expm1()`, which do not pair.

---

## 3. Current results

`04_thesis_results/srq1/` — XGBoost wins every category:

| Category | best | WMAPE | naive | medMAPE |
|----------|------|------:|------:|--------:|
| CSD | XGBoost | 17.1% | 34.9% | 36.3% |
| Danskvand | XGBoost | 32.6% | 44.0% | 46.2% |
| Energidrikke | XGBoost | 14.9% | 30.6% | 43.9% |
| RTD | XGBoost | 31.8% | 54.8% | 28.6% |

Re-run with:

```bash
python 03_thesis_modelling/model_training/srq1_benchmark.py
python 03_thesis_modelling/model_training/srq1_baselines_stat.py
```

---

## 4. Where to pick up

### The one blocker

`03_thesis_modelling/.env` is missing. SRQ4 — **the thesis premise** — cannot run
without it:

```
ANTHROPIC_API_KEY=...
E2B_API_KEY=...
```

E2B is a disposable cloud sandbox where System B's self-written code executes. System A
does not need it; that asymmetry is the experiment.

**Open question for you and Brian**: the harness is currently hardcoded to
`claude-sonnet-4-6` and **no justification is recorded anywhere**. Brian favours GPT on
the grounds that it is what firms actually deploy — a genuine ecological-validity
argument. Note that "cheaper and weaker makes our result look better" is *not* a
defensible reason and should not appear in the write-up. The harness is written against
Anthropic's API shape, so a GPT run needs a small adapter for the two call sites.

### Suggested order

1. Add `.env`, run `python 03_thesis_modelling/model_training/srq4_experiment.py --demo`
   — one brand through both systems. This tells you whether the remaining schedule is
   realistic, and what one run costs.
2. Add the System B failure taxonomy (`ok` / `code_error` / `no_forecast` / `timeout` /
   `implausible`) **before** any real runs, or you re-run everything to add it. Failures
   are a result: "code-as-action failed 12% of the time" is stronger than a small
   accuracy gap.
3. Fix the scope in writing — brands, prompts, repeats — and do not change it after
   seeing results. Agreed: **CSD primary** (most brands, so the most statistical
   weight), one other category as a robustness check.
4. Run, log everything, keep raw responses.
5. Analyse against the pre-stated claims.
6. Only then resume `P0034` chapter reconciliation, with final numbers.

### A framing worth considering

System A's honest pitch is no longer "more accurate" — the intervals are wide. It is
**a number, plus calibrated uncertainty, plus provenance**. System B can produce a
number; it cannot produce the other two, since self-written code has no recorded
lineage. That argument survives System B occasionally winning on accuracy, which a
pure accuracy claim would not.

---

## 5. Plan status

| Plan | Status |
|------|--------|
| P0037 serving interface | **active — the critical path** |
| P0034 chapter reconciliation | paused until numbers are final |
| P0026, P0029, P0031, P0032, P0033, P0035, P0036, P0038 | closed → `plans/.archive/` |

Full detail in `plans/.archive/P0038_*/findings.md` (F59-F80) and
`plans/P0037_*/findings.md` (F10-F13).

---

## 6. Known limitations to carry into the write-up

- **Cross-brand heterogeneity is not quantified** per category (P0031 task 3). The
  pipeline treats every category's brand panel as equally poolable; if one category's
  brands are far more heterogeneous, a pooled model fits it worse and nothing in the
  artifacts says so.
- **The four categories do not share a feature space** (31/23/31/30). State this
  wherever results are compared across categories.
- **Prophet diverges** on individual series: one CSD brand was forecast at 101M against
  301k actual, driven by an unbounded linear trend fitted in log space. Reported via
  medMAPE rather than tuned away, so the baseline is not handicapped.
