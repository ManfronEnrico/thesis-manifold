---
name: 2026-08-19_preprocessing-pipeline-handover-enrico
description: HANDOVER - The CSD notebook is retired and replaced by a shared 7-step pipeline running all four categories; how to regenerate it locally, what changed in the numbers, and where to pick up
category: reference
applies-to: [02_thesis_data, 03_thesis_modelling, 04_thesis_results]
triggers: [handover, regenerate eda, run pipeline, enrico]
created: 2026_08_19-01_30
updated: 2026_08_19-02_35
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

**Before you regenerate anything**: pull the raw data fresh (section 1.1). No data
comes through git, and the latest month should be **2026-07** — if your run ends
earlier, the pull did not refresh and every downstream number will be wrong.

---

## 1. How to regenerate the EDA pipeline on your machine

### 1.1 Start from the warehouse, not from a copied folder

**Nothing data-related comes through git.** `.gitignore` excludes `*.parquet`,
`*.jsonl` and `*.csv`, so a fresh clone gives you all the code and none of the data.
Copying folders between machines would work as a plain file transfer, but do not do
that here — you would inherit whatever staleness Brian's machine has.

**Run the full chain yourself**, so you know your data is current. The latest month
should be **2026-07**; anything ending earlier means the pull did not refresh.

#### Step A — credentials (you should already have these)

The pull reads `RU_*` credentials from a **`.env` at the repo root** —
`RU_SERVER_STRING`, `RU_DATABASE`, `RU_CLIENT_ID`, `RU_TENANT_ID`,
`RU_CLIENT_SECRET`. You have pulled before, so this is almost certainly already in
place; it is listed only so a failure here is immediately recognisable rather than
mysterious.

Note it is a **different** `.env` from `03_thesis_modelling/.env`, which holds the LLM
keys for SRQ4. Two files, two purposes.

Also needs `pyodbc` with an ODBC driver, plus `azure-identity`.

#### Step B — pull the raw JSONL (excluding Totalbeer)

```bash
python 02_thesis_data/_00_raw/nielsen/scripts/save_all_datasets.py --only CSD Danskvand Energidrikke RTD --parallel
```

**Views + metadata only** — that is the default, and it is the complete input for
everything downstream. The pipeline reads only the views and never touches the raw
source tables. `--parallel` opens one connection per category (~3 min rather than
~15).

**Do not pass `--download-raw`.** It adds ~2 hours pulling source tables that nothing
in the pipeline consumes. The flag exists as an escape hatch for settling a data
question below view level, not as a routine option; the script's docstring now says so
explicitly.

**Totalbeer is excluded on purpose** — out of scope for the thesis, dropped from the
prose on compute-constraint grounds (P0034).

#### Step C — convert JSONL to parquet (same exclusion)

```bash
python 02_thesis_data/_01_converted/nielsen/jsonl_to_parquet_script/run_all_conversions.py --only CSD Danskvand Energidrikke RTD
```

Idempotent (skip-if-newer), so it is safe to re-run. Conversion only makes sense
**after** step B — converting stale JSONL just produces stale parquet.

Result: ~1.3 GB of parquet views under
`02_thesis_data/_01_converted/nielsen/parquet_nielsen/{Category}/views/`, four files
per category (facts, `dim_product`, `dim_period`, `dim_market`).

> **Note on `MANIFEST.json`**: the copy on Brian's machine is timestamped 2026-06-30
> and its `output_dir` still points at the pre-restructure `thesis/data/...` path, so
> it predates both the re-pull and the P0028 restructure. Treat it as unreliable
> provenance — your own pull is the authority on how current your data is.

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

SRQ4 — **the thesis premise** — needs two API keys. Put them in
`03_thesis_modelling/.env` (the repo-root `.env` also works; the harness checks the
modelling one first, then falls back):

```
ANTHROPIC_API_KEY=...
E2B_API_KEY=...
```

E2B is a disposable cloud sandbox where System B's self-written code executes. System A
does not need it; that asymmetry is the experiment.

**Check for a value, not a key name.** Brian's repo-root `.env` contains the line
`ANTHROPIC_API_KEY=` with nothing after it — a placeholder that greps like a working
credential. If yours from building System B looks the same, the harness will fail
authentication rather than start. The loader now skips empty values so the error names
the missing key instead of failing obscurely.

`E2B_API_KEY` is the one genuinely new thing to obtain. It is free-tier for a workload
this size.

**On the LLM choice (DEC-VENDOR)** — if your Anthropic key is real, running
`--demo` as-is is the fastest path to a first result, and worth doing before changing
anything.

**Already fixed on Brian's side (commit `63c8a6c`)**, so you should not hit these:
the harness used to raise `FileNotFoundError` on import when `.env` was absent; it
pointed at a stale `forecast_service.py` path left over from the P0028 train-vs-serve
split; and `anthropic` / `e2b-code-interpreter` were missing from `requirements.txt`.
Re-run `pip install -r requirements.txt` to pick up the two SDKs.

System A's forecasting core is verified working without any credentials —
`_eval_forecast("CSD", "HARBOE")` returns a forecast with a 90% interval — so what
remains genuinely is credentials alone.

The open question is whether Claude should be the **reported** model. The harness
hardcodes `claude-sonnet-4-6` (line 36) and **no justification is recorded anywhere in
the thesis** — a reviewer asking "why this model?" currently has no answer. Brian
leans toward GPT on ecological-validity grounds: it is what most firms actually deploy,
so a finding that holds there generalises better to the thesis' own recommendation.

Worth noting the premise is about **model availability**, not about any vendor. If the
effect only holds for one, it is a vendor finding rather than a thesis — so a full run
on one model plus a smaller cross-check on the other is the stronger design.

Cost does not separate them at this scale: roughly **$7 on Claude vs $4 on GPT** for 50
runs per system. Budget governs *how many runs* are affordable — a sample-size
decision for the methodology — not which vendor to use.

Two practical notes if the vendor does change: the harness is written against
Anthropic's API shape, so the two call sites need an adapter; and
`PRICE_IN_PER_M` / `PRICE_OUT_PER_M` must be updated, since every reported cost figure
is computed from them.

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
