---
name: 2026-09-01_srq1-tuning-and-ram-handover-enrico
description: HANDOVER - SRQ1 tuning/selection defects fixed, RAM instrument corrected, refit-vs-retune measured
category: reference
applies-to: [03_thesis_modelling, 04_thesis_results, 05_thesis_writing]
triggers: [resuming SRQ1 work, reviewing served models, writing Ch6, running SRQ4 blocks]
created: 2026_09_01-21_30
updated: 2026_09_01-21_30
---

# Handover - SRQ1 tuning, memory measurement, and the retrain question

**For:** Enrico
**From:** Brian (session 2026-09-01)
**Plan:** `plans/P0044_2026-09-01_17-10_resource-measurement-and-retrain-arms/`

Three defects were found and fixed in the SRQ1 pipeline, and several claims that
had been asserted are now measured. **Two of the fixes change the served
artefact**, so anything citing a served model may need revisiting.

---

## 1. The served models were trained on the weaker of two tunings

`srq1_benchmark_cv.py` was written to fix three documented weaknesses in
`srq1_benchmark_tuned.py` - 30 trials, a single validation split, and a
wMAPE-only objective. It ran on 2026-08-24, produced better parameters with a
convergence curve, and wrote them to `cv_params.json`.

**Nothing ever read that file.** `train_and_persist.py` kept reading
`tuned_params.json` (2026-08-19). Every served model, and the profiling table,
was built on the tuning the project itself had called under-powered.

The divergence is not cosmetic - CSD/LightGBM: `n_estimators` 1192 vs 374,
`num_leaves` 63 vs 120.

It went unnoticed because the two scripts write different filenames and nothing
consumed the newer one, so no test failed and no error surfaced.

**Fixed:** training now reads `cv_params.json`, with `tuned_params.json` retained
as a fallback so a missing entry degrades rather than crashes.

## 2. Model selection was reading the test set (more serious)

`best_model_for()` ranked candidates by `test_wmape`:

```python
r = t.sort_values("test_wmape").iloc[0]   # the HELD-OUT TEST SET
```

The served model was therefore chosen using the same data the thesis reports its
performance against. That optimistically biases every downstream number.

**Fixed:** selection now uses `cv_score` (expanding-window validation), which
never touches test.

**One model changed:**

| category | before | after |
|---|---|---|
| CSD | XGBoost | XGBoost |
| danskvand | XGBoost | XGBoost |
| energidrikke | XGBoost | XGBoost |
| **RTD** | **XGBoost** | **LightGBM** |

Models re-persisted 2026-09-01. **SRQ4 is unaffected** - all runs to date are
CSD-only, so RTD was never exercised. Ch6 had already flagged RTD selection as
unstable ("flips" across seeds), so this is consistent with the chapter.

## 3. The RAM numbers were measured with an instrument that could not see them

`srq1_profiling.py` used `tracemalloc`, which counts **Python-level allocations
only**. LightGBM and XGBoost build their ensembles in C++.

| model | tracemalloc | **RSS (correct)** | pickled |
|---|---|---|---|
| Ridge | 5.5 MB | 5.4 MB | 0.0 MB |
| LightGBM | 23.0 MB | **36.8 MB** | 7.64 MB |
| XGBoost | **0.1 MB** | **26.6 MB** | 3.70 MB |

XGBoost was understated **266x**. The 0.1 MB figure was impossible on its face -
below Ridge, and below the 3.7 MB the same model serialises to.

**Fixed:** measures process RSS, sampled by a poller thread at 5 ms, in a
**separate subprocess per model** (RSS never returns to baseline in-process, so a
sequential loop charges each model with its predecessors' retained pages).
`tracemalloc` is kept as a second column so the correction is auditable.

Fit times also moved (XGBoost 0.97s -> 2.19s): `tracemalloc` slows what it
measures, and the old run shared one warm process.

---

## The RAM budget: use 4 GB, not 8 GB

The thesis asserts <=8 GB throughout. That number is **unsourced** - Ng (2017) is
cited beside it, but Ng argues memory is the binding design variable at terabyte
scale and states no SME budget.

Manifold's production E2B template is provisioned at a **measured 4096 MB**:

```
templateID=fxe7gzkqjupdhbx4uvpr   alias: prometheus   4096MB   private
```

Probed live - pandas, numpy, **pyodbc**, sqlalchemy, statsmodels, xgboost,
lightgbm, prophet, optuna, sklearn all present.

Brian's decision: **ground everything in the measured 4 GB.** All results hold a
fortiori (serving 36.8 MB ~ 0.9% of 4 GB). Draft chapters are flagged; the
rewrite is pending.

**Also added `PROMETHEUS_TEMPLATE_ID=prometheus` to `.env`.** It was absent, so
any code path reading it fell back to E2B's default base image - which has **no
pyodbc**, meaning warehouse queries would fail *inside* the sandbox rather than
at connection time.

---

## The retrain-on-demand question (measured)

Can the agent refit a model per query instead of serving a pre-trained one?

**Cost** - single cutoff, CSD/LightGBM:

| | time | peak RSS | ratio |
|---|---|---|---|
| refit on stored params | **2.93 s** | 35.0 MB | 1x |
| re-tune, 30 trials x 4-fold CV | 107.9 s | 86.6 MB | 37x |
| re-tune, 100 trials x 4-fold CV | **417.3 s** | 65.3 MB | **142x** |

So: **refit per query is viable; re-tuning per query is not.** 7 minutes vs 3
seconds.

**Data movement is not an obstacle.** `aggregate_brand_month_from_db()` pushes
aggregation into the warehouse query: `_00_raw/` is 38 GB, but the engineered CSD
matrix is **1.08 MB** - a ~47,000x reduction. The agent never downloads the
dataset.

**Two caveats, both important:**

1. **Parameter drift over 7 months is INCONCLUSIVE.** Mean gap between frozen and
   freshly-tuned params is -0.04pp. There is a +0.414 pp/month slope, but it is
   carried by two opposite outliers on seven points and **must not be cited**.
   The honest position: no detectable decay at this scale, untested at the
   multi-year horizon production faces. Recommended design is refit per query
   with a **scheduled** re-tune (quarterly), noting the cadence was not
   empirically optimised.
2. **Do NOT claim re-tuning is less accurate.** Varying only the Optuna seed on
   identical data moves test wMAPE by **3.97pp**, which swamps the ~0.3pp between
   arms. The justification for refit is **cost**, not accuracy.

**Scenario design:** C and E cannot simply "refit every time" - `forecast_demand()`
does not train at all; it loads a persisted model and reads a pre-computed
matrix. Refit should be a **separate rung (G)** changing one variable against C.
A previously-planned scenario F ("pre-trained served") was dropped as a duplicate
of C.

G needs three things built: a warehouse connection inside the sandbox,
re-derivation of the empirically-derived `peak_months`, and a redefinition of the
test-split guard - which currently refuses any month outside the fixed test
window, and a per-query refit moves that boundary.

---

## Writing surfaces changed

Prose now lives in **one** place. It previously existed twice - the OneDrive
`.docx` and `sections-drafts/*.md` at 76-97% similarity - agreeing only because
nobody had edited either since the export.

| surface | role |
|---|---|
| OneDrive `.docx` | **authoritative prose** |
| `05_thesis_writing/docx-exported-snapshots/` | read-only mirror, regenerated |
| `sections-drafts/*.md` | **bullets, status, provenance - no prose** |
| `sections-final/` | archived (all 6 files frozen 2026-07-11, 4 chapters never exported) |

Rule: `.claude/rules/writing-surface-authority.md`. Pre-strip prose is archived
under `05_thesis_writing/.archive/2026-09-01_superseded-prose/`.

The strip was **not** uniform: Ch6 kept 3,308 of 6,155 words because it carries
provenance the `.docx` never held (withdrawn <=15% target, citation verification
state). Each file was diffed against the snapshot first.

---

## What needs doing next

| # | Task | Blocked by |
|---|---|---|
| 1 | **Re-check Ch6 model-training prose** - notes in `sections-drafts/ch6-model-benchmark.md` | nothing |
| 2 | Ch1 rewrite on the 4 GB bound - notes in `sections-drafts/ch1-introduction.md` | nothing |
| 3 | Run P0042 blocks 1-3 (111 runs, ~$40) | API credit |
| 4 | Build scenario G | engineering above |
| 5 | Prune orphaned model files in `train_and_persist.py` | nothing |

**Do not run blocks 1-3 against the old models** - they were rebuilt on
2026-09-01 from unbiased selection.

## Reproducing any of this

```powershell
# profiling (free, ~1 min)
python 03_thesis_modelling/model_training/srq1/srq1_profiling.py

# re-persist served models (free, ~30 s)
python 03_thesis_modelling/model_training/train_and_persist.py
```

Results: `04_thesis_results/srq1/{profiling,refit_vs_retune,retune_single_cutoff,param_drift}.csv`
Full detail: `plans/P0044_.../findings.md` (F1-F33).
