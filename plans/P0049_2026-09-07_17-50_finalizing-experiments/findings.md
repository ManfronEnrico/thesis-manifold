---
name: p0049-findings
description: STATE - Findings from P0049. F23 records the horizon fix: what was broken, where, and how each layer was verified.
pid: P0049
created: 2026_09_07-18_55
updated: 2026_09_07-18_55
---

# P0049 — Findings

## F23 — The horizon defect was THREE defects, in three layers (2026-09-07)

P0048 found that `engineer_features()` never received the horizon. Checking the
scoring path before implementing showed that fixing it alone would have left the
experiment still measuring one month ahead. Three independent layers each
assumed H=1, and each would have silently survived a fix to the others.

| # | Layer | File | What was wrong |
|---|-------|------|----------------|
| 1 | Features | `_shared_modules/engineer_features.py` | Lags were `shift(lag)` at every horizon, so h1 and h3 matrices were byte-identical in every lag column |
| 2 | Scoring | `scenario_setup/srq4_experiment.py` | Scored `test.iloc[0]` — the first held-out month, i.e. cutoff+1 — whichever matrix was read |
| 3 | Serving | `02_SRQ2_Tool_Interface/forecast_tool.py` | Called without a month, defaulting to the first test month; Scenario C forecast month 1 while scored on month 3 |

**Layer 2 is the one that matters most for the finding's credibility.** It is
independent of the feature bug: even with correct H=3 features, scoring
`test.iloc[0]` measures a one-month-ahead task. A fix confined to
`engineer_features()` would have produced correct-looking matrices, a passing
pipeline, and the same wrong number.

### The fix

**Layer 1 — one offset, six feature blocks.** `horizon` is now a required
keyword argument. Every past-derived feature shifts by an extra `horizon - 1`:
lags to `shift(lag + h - 1)`, and the `shift(1)` features (rolling mean/std,
`promo_intensity`, `zero_run_flag`, `zero_run_length`) to `shift(1 + h - 1)`.
Named `_h` at the top of the function so the six blocks visibly share one offset.

At h=1 the offset is zero, so **every H=1 number ever published is unchanged** —
verified by equality against the old definition, not assumed.

Column names keep their H=1 meaning (`lag_1` = "most recent observation
available to the forecaster"). Renaming to `lag_3` at H=3 would make one column
name mean different things in different matrices, and every downstream `FEATURES`
list is written against these names.

`horizon` is read from the CONTRACT in step 4, not from `run()`'s `--horizon`
argument, even though both are in scope. `load_contract()` already hard-fails if
they disagree, so taking it from the contract makes `min_periods` and the feature
offset provably derived from one value.

**Layer 2 — `HORIZON = 3` as a single module constant.** It selects the matrix
*and* picks the scored month (`test.iloc[HORIZON - 1]`), so the two cannot
disagree. Previously the horizon was a hardcoded `_h3` in three `read_parquet`
calls with no relationship to the scored offset.

The `HORIZON - 1` intervening months are withheld from `fit` as well — a
forecaster standing at the cutoff has not observed them either.

**Layer 3 — the harness passes the scored month explicitly**, and the payload
now carries `months_ahead`, computed from `trained_through`, so the horizon is
self-describing rather than inferred by the caller.

### A new assert, because the old one was too weak

`_assert_no_leakage` checked only that history ends *before* the target. At H=3
that also passes for a history ending one month before — a two-month-ahead
forecast reported as three. The gap is now an **equality** against `HORIZON`:
understating it is a leak, overstating it silently makes the task harder than
reported. Confirmed to fire on a forged 1-month gap.

`verify_setup.py`'s "all scenarios target the same month" check was passing
before **only because both sides were wrong in the same way**. It now calls the
tool the way production does and additionally asserts `months_ahead == HORIZON`.

### Verified

- Synthetic: `h3.lag_1 == shift(3)`, `h3.lag_3 == shift(5)`, h1 unchanged,
  `horizon=0` rejected, omitting `horizon` a `TypeError`
- Real data, all 4 categories: `lag_1` now differs across horizons, and
  `h3.lag_1 == h1.lag_3` exactly — the offset is precise, not merely different
- Sample (CSD brand 1724, July 2026): H=1 sees June, H=3 sees April
- SRQ4: 76 scorable CSD brands, history ends 2025-12, scored month 2026-03,
  gap assert passes for all
- Tool: default returns `months_ahead=1`; explicit target returns
  `months_ahead=3` and a different forecast — the bug made visible
- `verify_setup.py`: **10/10, no warnings**

### Eligibility narrowed, deliberately

`_eligible_brands` now requires at least `HORIZON` held-out months rather than
one. `_scorable_brands` still requires the WHOLE test window non-zero, though
only the scored month enters the APE denominator — the weaker rule would let the
eligible population change with the horizon, making H=1 and H=3 results measured
on different brand sets.

### What this invalidates

The delivered A/B/C ladder (2026-08-19, $4.92: C 13.8% vs B 17.3%) was scored at
**one month ahead**. It does not get relabelled — it gets re-run, or reported
honestly as H=1. The direction should survive; the magnitudes will not.

The persisted models are still trained on H=1 features (the tool's payload moved
from 4,535,742 to 4,338,324 purely from the matrix change). Retraining is the
next task; until it lands, Scenario C serves an H=1 model against H=3 features.

### The lesson

`--horizon` reached the filenames, the contract, `min_periods` and the split
geometry — everything except the features themselves. Step 3 had been deriving
`min_periods = warmup + horizon + 1` in anticipation of a shift that was never
applied, and `n_origins = n_test - horizon + 1` likewise. **The plumbing being
present is not evidence that it is connected.** Trace a parameter to the line
that consumes it, not to the last place it is mentioned.

---

## F24 — 13 live SRQ1 scripts hardcode `_h3`; none can produce H=1 (2026-09-07)

Found while confirming nothing else read the old matrix path. Every SRQ1
training/benchmark script opens `{slug}_feature_matrix_h3.parquet` as a literal:

`train_and_persist.py`, `training_report.py`, and under `model_training/srq1/`:
`srq1_benchmark.py`, `srq1_benchmark_cv.py`, `srq1_benchmark_tuned.py`,
`srq1_calibration.py`, `srq1_pooled.py`, `srq1_baselines_stat.py`,
`srq1_profiling.py`, `srq1_generate_shap_figures.py`,
`srq1_generate_performance_figures.py`. Also `verify_setup.py:153`,
`generate_architecture_diagrams.py:134`, and `forecast_tool.py:395`.

**Two consequences, opposite in sign:**

1. **Good:** they now read genuinely H=3 features with no change. Phase 2's
   retrain produces real three-month-ahead numbers as-is.
2. **Blocking for DEC-HORIZON:** none can produce H=1. "Benchmark both horizons"
   is not runnable until the horizon is a parameter in these scripts.

**Do not fix this by find-and-replace to `h1`.** That would swap which horizon is
unreachable. The scripts need the horizon as an argument (defaulting to 3, the
primary reported horizon) plus horizon-tagged output paths — otherwise an H=1 run
silently overwrites the H=3 results table.

Scope estimate: mechanical but not trivial — 13 files, and the output-path change
matters more than the input-path one.

**Decide before phase 2 starts**, since it changes what phase 2 is: H=3 only
(retrain now, defer H=1) or both horizons (parameterise first, then retrain
twice). H=3 alone is the thesis's primary reported horizon and unblocks the
funded runs sooner.

---

## F25 — `train_and_persist.py` selected its model from files that did not exist (2026-09-07)

Found while routing the SRQ1 scripts through the horizon (F24). Five reads
resolved to the results **tier root**, but every one of those files lives in
`tables/` or `models/`:

```
cvf = THESIS_RESULTS_SRQ1_DIR / "cv_metrics.csv"     # actually tables/
tf  = THESIS_RESULTS_SRQ1_DIR / "tuned_metrics.csv"  # actually tables/
mf  = THESIS_RESULTS_SRQ1_DIR / "metrics.csv"        # actually tables/
cvf = THESIS_RESULTS_SRQ1_DIR / "cv_params.json"     # actually models/
pf  = THESIS_RESULTS_SRQ1_DIR / "tuned_params.json"  # actually models/
```

Verified: no `.csv` exists at the tier root at all.

Every read is guarded by `if ...is_file()`, so nothing raised. **Model selection
fell through to its hardcoded `best = "XGBoost"` default and never consulted the
cross-validated study** — beneath a comment block explaining, at length, why
selecting on `cv_score` rather than `test_wmape` matters for keeping the test set
genuinely held out. The reasoning was sound; the code could not reach the data.

Same failure shape as F21 in `forecast_tool.py`: **a soft-failing read of a
misplaced path degrades into a silently weaker result rather than an error.**
That is now three occurrences of this one pattern (F21, F25, and the F22 scoring
default), which makes it the dominant defect class in this codebase.

Fixed by routing all five through `results_root()`, which resolves per horizon.

**Consequence for the numbers:** whichever model XGBoost happened not to be, the
served model was chosen by default rather than by CV. The H=3 benchmark run after
the fix reports `best=LightGBM` for CSD, energidrikke and RTD, and `Ridge` for
danskvand — so the default was wrong for all four categories.

---

## F26 — H=3 is measurably harder than H=1, as it should be (2026-09-07)

The first post-fix benchmark, both horizons, untuned:

| Category | H=1 WMAPE | H=3 WMAPE | Δ |
|---|---:|---:|---:|
| CSD | 18.1 % | 20.4 % | +2.3 pp |
| danskvand | 20.0 % | 30.4 % | +10.4 pp |
| energidrikke | 16.2 % | 17.3 % | +1.1 pp |
| RTD | 31.9 % | 28.4 % | **−3.5 pp** |

Three of four degrade at the longer horizon, which is the sanity check the plan
named: *"expect H3 to get worse after the fix; if it does not, the fix has not
taken effect."* It took effect.

**RTD improves, and it is not survivorship — that hypothesis was tested and
failed.** The obvious explanation is that H=3's stricter `min_periods`
(warmup + horizon + 1 = 17 vs 15) drops short, hard series, flattering the
aggregate. RTD loses the most brands of any category (72 -> 62, 14 %). But:

- Restricting the H=1 score to only the brands that survive into H=3 moves the
  naive baseline by **0.1 pp** (54.9 -> 54.8). The population change is not the
  driver.
- The 10 dropped brands carry **0.3 % of test volume**. WMAPE is volume-weighted,
  so they cannot move it regardless of how badly they forecast (their naive
  WMAPE is 89.6 % against 54.8 % for those retained).
- The test windows are **identical** across horizons (RTD: 2026-02 .. 2026-07,
  n=432 vs 372 rows over the same months), so it is not a shifted evaluation
  period either.

What is left is the naive baseline itself: RTD's seasonal-naive WMAPE goes
**up** with the horizon (54.9 % -> 78.1 %) while the model's goes down. At H=3
the lag structure available to the model (`lag_1` = t-3) happens to suit RTD's
series better than the year-ago comparison does. **This is a real result, not an
artefact — but it is a single untuned run, and it should be confirmed against the
tuned and CV numbers before it is written up.** Report the horizon comparison
per category; do not summarise it as one direction.

Best model also changes with horizon (H=1 XGBoost for three categories; H=3
LightGBM for three). Expected — the horizon changes the task — but it means
**model choice must be reported per horizon**, not once.

---

## F27 — The suite was never memory-hungry; it was running twice (2026-09-07)

Two background runs were killed by the harness for low memory, at ~91 % RAM on a
16 GB machine. The obvious reading — that the SRQ1 suite is too heavy for this
box, so it needs a VPS or a smaller job — is wrong on the measurements.

**Measured while the CV stage ran: 282 MB.** The tuned stage: 210 MB. `XGB_N_JOBS
= 1` (DEC-DETERMINISM) already holds per-fit memory down, so the reproducibility
fix incidentally made the suite cheap to run.

The actual cause was **two full suites running concurrently**: a `nohup` launch
whose wrapper had returned (so it looked finished) was still alive when a second
run started. Both were writing the same output files. Six orphaned processes were
terminated; none remained afterwards.

Terminating them freed almost nothing (1.3 -> 1.4 GB), which is the tell: the
pressure is **other applications** — Word 424 MB, VS Code 527 MB, several Claude
sessions, and `MemCompression` at 1.27 GB indicating Windows was already
compressing pages. The training was a bystander.

**Two operational lessons:**

1. **A returned `nohup` wrapper does not mean the job finished.** Check for live
   processes by cmdline before starting another run. Windows adds intermediate
   shims, so one job legitimately shows as a 4-5 process chain
   (nohup -> runner -> subprocess wrapper -> worker); count the *workers*, not
   the processes.
2. **`--resume` now exists on `run_both_horizons.py`** so a kill costs one stage
   rather than the suite. A stage counts as done only if its artefact was written
   *after the current run began* — a stale table from an earlier run never counts,
   which is the same silent-staleness trap as F21 and F25.

### Rejected: committing the feature matrices, and the VPS

Both were considered for moving training off this machine. Both are wrong, and the
reasons are worth recording so they are not revisited:

- **Committing the parquets** — the matrices total **4.5 MB**, far inside GitHub's
  limits, so size was never the obstacle. The blanket `*.parquet` / `*.csv` rules
  exist for the **Nielsen confidentiality agreement with Manifold AI**. The
  matrices carry brand-level monthly sales for named Danish brands: that is the
  confidential data itself, merely transformed. **Not to be un-ignored.**
- **A VPS** — would mean syncing that same confidential data to another host to
  solve a problem that does not exist (282 MB).

The real fix is free: run one stage at a time, and close Word/VS Code windows while
the long stages run.

### Wall clock, measured

`benchmark` ~8 s per horizon. `benchmark_cv` **56 min** at H=3. The tuned and CV
stages dominate; everything else is minutes. Budget accordingly rather than
assuming the whole suite is long.
