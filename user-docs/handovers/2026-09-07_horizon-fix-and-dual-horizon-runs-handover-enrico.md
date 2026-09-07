---
name: 2026-09-07_horizon-fix-and-dual-horizon-runs-handover-enrico
description: HANDOVER - The h1/h3 matrices were the same one-month task; fixed across three layers. SRQ1 now runs at both horizons from one value.
category: reference
applies-to: [01_SRQ1_Model_Training, 02_SRQ2_Tool_Interface, 04_SRQ4_Scenario_Experiment, 05_thesis_results]
triggers: [running SRQ1, adding a training script, reading a feature matrix, scoring a scenario, reporting a horizon]
created: 2026_09_07-20_50
updated: 2026_09_07-20_50
---

# Handover — the horizon fix, and running both horizons

## 1. What was wrong

`--horizon` reached the filenames, the contracts, `min_periods` and the split
geometry — everything except the features themselves. `engineer_features()` never
received it, so lags were `shift(lag)` at both horizons and **the h1 and h3
matrices were byte-identical in every lag column**.

Published results came from the `_h3` file. So the thesis reported one-month
accuracy while describing three-month. That is a validity problem, not a
reproducibility one.

**It was three defects, not one**, and each would have survived a fix to the
others:

| Layer | Was |
|---|---|
| Features (`engineer_features.py`) | lags `shift(lag)` regardless of horizon |
| Scoring (`srq4_experiment.py`) | scored `test.iloc[0]` = cutoff+1, *whatever matrix it read* |
| Serving (`forecast_tool.py`) | called with no month, defaulting to the first test month |

The scoring layer is the one worth understanding. It is **independent of the
feature bug**: even with correct H=3 features, scoring the first held-out month
measures a one-month-ahead task. A fix confined to `engineer_features()` would
have produced correct-looking matrices, a passing pipeline, and the same wrong
number.

## 2. What to do differently when adding code

**Never write a horizon literal.** Import it:

```python
from _horizon import HORIZON, matrix_path, results_root

OUT = _SRQ1Out(results_root())            # not THESIS_RESULTS_SRQ1_DIR
fm  = pd.read_parquet(matrix_path(cat, slug))   # not f"..._h3.parquet"
```

`srq1/_horizon.py` resolves `SRQ1_HORIZON` (default 3) into **both** the input
matrix and the output directory. One value, so the two cannot describe different
horizons — which is exactly how this defect arose.

**The layout is asymmetric on purpose:**

| Horizon | Reads | Writes |
|---|---|---|
| 3 (primary) | `*_feature_matrix_h3.parquet` | `06_model_benchmark/{tables,figures,models}/` |
| 1 (secondary) | `*_feature_matrix_h1.parquet` | `06_model_benchmark/h1/{...}/` |

H=3 keeps the unsuffixed paths because `forecast_tool.py`, the SRQ4 harness, the
appendix exporter and the figure generators all read them. Moving the primary
horizon would break every one of them to gain nothing. The consequence that
matters: **an H=1 run cannot overwrite an H=3 result.**

**Feature columns keep their H=1 meaning.** `lag_1` is "the most recent
observation available to the forecaster" at every horizon — at H=3 it is
`shift(3)`. Renaming it to `lag_3` would make one column name mean different
things in different matrices, and every downstream `FEATURES` list is written
against these names.

## 3. Enforced vs. remembered

**Enforced by code** — these fail loudly:

- `horizon` is a *required* keyword of `engineer_features()`; omitting it is a
  `TypeError`, and `horizon < 1` raises.
- Step 4 reads the horizon from the **contract**, not from `--horizon`, so
  `min_periods` and the feature offset are provably derived from one value.
- `_assert_no_leakage` requires the gap between history-end and scored month to
  **equal** `HORIZON`. Understating it is a leak; overstating it silently makes
  the task harder than reported. Confirmed to fire on a forged 1-month gap.
- `verify_setup.py` asserts `months_ahead == HORIZON` end to end.
- `SRQ1_HORIZON` rejects unsupported values rather than defaulting.

**Remembered only** — no guard exists:

- Nothing stops a new script writing `_h3` as a literal. If you add one, import
  from `_horizon`.
- Nothing stops a new past-derived feature forgetting the `_h` offset. The six
  existing blocks share one named variable so the omission is visible; keep it
  that way.

## 4. Near-misses worth knowing

**A soft-failing read of a misplaced path is now the dominant defect class here.**
Three instances, all silent:

- **F21** — `forecast_tool.py` read its track record from the results root instead
  of `tables/`. Inside `try/except`, so it served forecasts with the
  `historical_*` fields simply **absent** — the very evidence Scenario C exists
  to carry — while logs looked normal.
- **F25** — `train_and_persist.py` read its five model-selection inputs from the
  root too. Guarded by `is_file()`, so **model selection fell through to a
  hardcoded `"XGBoost"` default and never consulted the CV study**, beneath a long
  comment explaining why selecting on `cv_score` rather than `test_wmape` matters.
  The default was wrong for all four categories.
- **F22's serving default** — the tool's "first test month" fallback.

If you add a guarded read, ask what happens when the file is missing. "Returns
something plausible" is the failure mode to design out.

**Two more, caught only by explicit checks:** an import inserted *after* its first
use (compiled fine, would have raised `NameError` at runtime), and an import
spliced into the middle of an existing comment referencing an undefined variable.
`py_compile` catches neither. An import-before-use scan does.

## 5. Open, and not mine to close

- **The two-horizon run is part-done.** Resume with:

  ```bash
  python 01_SRQ1_Model_Training/02_thesis_modelling/model_training/run_both_horizons.py --resume
  ```

  Done: `benchmark` (both horizons), `benchmark_cv` + `benchmark_tuned` (H=3
  only). Remaining: 4 stages at H=3, 7 at H=1. CV took 56 min; tuned 3 min; the
  rest are minutes.

- **RTD improves at the longer horizon** (31.9 % → 28.4 % WMAPE) while the other
  three degrade as expected. **This is not survivorship** — that hypothesis was
  tested and failed: the 10 brands H=3 drops carry 0.3 % of test volume, and
  WMAPE is volume-weighted. It needs confirming against the tuned and CV numbers
  before it is written up. See findings F26.

- **Best model changes with horizon** (H=1 XGBoost for three categories; H=3
  LightGBM for three). Expected, but it means **model choice must be reported per
  horizon**, not once.

- **The delivered A/B/C ladder** (2026-08-19: C 13.8 % vs B 17.3 %) was scored at
  **one month ahead**. It does not get relabelled — it gets re-run, or reported
  honestly as H=1. The direction should survive; the magnitudes will not.

- **DEC-VENDOR is still open.** The harness pins `gpt-5.5-2026-04-23`; what is
  missing is the written justification. Decide on ecological validity — at ~$7 vs
  ~$4 for 50 runs, cost is not the deciding factor.

## 6. Settled — do not reopen without new information

**Training does not move to a VPS, and the feature matrices stay gitignored.**
Both were considered to escape memory kills; both were wrong:

- The suite uses **282 MB** (CV) / **247 MB** (tuned), measured while running. It
  was never memory-hungry — `XGB_N_JOBS=1` keeps per-fit memory low.
- The kills came from **two suites running concurrently**: a `nohup` launch whose
  wrapper had returned, so it looked finished, was still alive when a second run
  started.
- The matrices are **4.5 MB total**, so GitHub limits were never the obstacle.
  They stay ignored because of the **Nielsen confidentiality agreement with
  Manifold AI** — brand-level monthly sales for named Danish brands is the
  confidential data itself, merely transformed. A VPS would mean syncing exactly
  that to another host.

## Related

- `plans/P0049_2026-09-07_17-50_finalizing-experiments/findings.md` — F23–F27
- `plans/P0049_.../progress.md` — stage-by-stage run state
- `01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/_horizon.py`
- `.claude/rules/repo-tier-structure.md` — where scripts belong
