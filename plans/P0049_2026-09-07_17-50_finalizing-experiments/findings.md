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

---

## F28 — The suite list was incomplete: 46 of 84 H=3 artefacts were pre-fix (2026-09-08)

Brian asked whether H=3 really only had "a few pieces left". It did not, and the
question is what exposed it.

`run_both_horizons.py` listed **8 stages**. The SRQ1 tree has **20 producers**.
Checking every artefact's mtime against the feature-matrix rebuild (2026-09-07
17:59) showed **46 of 84 H=3 artefacts (54 %) were built on pre-fix features** —
i.e. on the H1-mislabelled-as-H3 matrices.

The omitted producers were not minor:

| Omitted | Produces | Why it matters |
|---|---|---|
| `srq1_stability.py` | stability.csv + 2 | the seed-stability verdict §6.6 rests on |
| `srq1_holiday_ablation{,_tuned}.py` | 5 tables | the entire holiday-enrichment result |
| `srq1_feature_diagnostics.py` | VIF, permutation importance | the feature-selection justification |
| `srq1_pooled{,_perbrand}.py`, `srq1_ridge_{cv,pooled}.py` | 6 tables | pooled-vs-per-category comparison |
| `srq1_mase.py`, `srq1_demand_classes.py` | 4 tables | secondary metrics + segmentation |
| `training_report.py`, `srq1_export_enrichment_appendix.py` | report + appendix | what the thesis actually cites |

**Why they were left out was wrong reasoning, and it is worth naming.** The
original comment said stability was "40 fits; run deliberately", pooled was "a
separate modelling question", and the ablations were "answered already; rerun only
if features change". The first two are cost/scope arguments that say nothing about
correctness, and the third was **false at the moment it was written** — the
features had just changed. All three now run; only `srq1_profiling.py` stays out,
because it measures resource cost at `n_jobs=-1` and is horizon-insensitive by
design (DEC-DETERMINISM).

**The lesson.** A stage list is a claim about what the thesis reports, not a
convenience. The 8-stage list was assembled from the scripts I had touched, which
is a property of my session rather than of the deliverable. Deriving it from the
artefacts instead — every table under the results tier, mapped back to its producer
— is what found the gap.

**Generalisable check, cheap to repeat:** compare every artefact's mtime against
the mtime of the *input* it derives from. Anything older was built on different
data. This is the same staleness class as F21/F25, caught by timestamp rather than
by reading code.

Run now covers **20 stages x 2 horizons = 40 runs**.

---

## F29 — Today's runs used the WRONG PYTHON, with different library versions (2026-09-08)

Caught while terminating the two-horizon run: the process list showed
`pythoncore-3.14-64\python.exe`, not the project venv.

| | bare `python` | `.venv/Scripts/python.exe` |
|---|---|---|
| xgboost | **3.4.1** | 3.2.0 |
| lightgbm | **4.7.0** | 4.6.0 |
| scikit-learn | **1.9.0** | 1.8.0 |
| pandas | **2.3.3** | 3.0.1 |

Every SRQ1 script's own usage line names `.venv/Scripts/python.exe`, so the venv
is canonical and the bare interpreter was wrong.

**Why this matters more than it looks.** Gradient-boosting output is
version-sensitive: histogram binning, default hyperparameters and tie-breaking all
change between minor releases. So results from the two interpreters are **not
comparable**, and this directly undercuts DEC-DETERMINISM — pinning `XGB_N_JOBS=1`
(F18) makes a run reproducible *against the same library build* and nothing more.

**It failed silently.** Both interpreters import cleanly, run to completion, and
write plausible tables. Nothing in the output names the interpreter. This is the
same class as F21/F25/F28: **the failure mode is a wrong answer, not an error.**

**Affected:** every stage run today under the bare interpreter — H=3 `benchmark`,
`benchmark_cv`, `benchmark_tuned`, and the H=1 `benchmark`. All are being
regenerated by the venv-pinned run, so no stale numbers survive.

**Fixed** by `_interpreter()` in `run_both_horizons.py`, which resolves
`.venv/Scripts/python.exe` from the repo root and warns loudly if it is missing.
The convention is now the default rather than something to remember.

**Open question worth one check:** the committed results predating today were
presumably produced under the venv, but that was not verified — nothing records
which interpreter wrote a table. If cross-run comparability ever matters
(e.g. comparing a pre-fix baseline), record the interpreter and library versions
in the run log alongside the numbers.

---

## F30 — What the CV budget actually costs, and why H=1 was dropped (2026-09-08)

Brian asked whether 20 stages x 2 horizons x 100 trials was excessive, and whether
CV runs only on the winning model. The arithmetic, from `srq1_benchmark_cv.py`:

```
4 categories x 2 models (LightGBM, XGBoost) x 2 metrics (wmape, medmape)
  = 16 Optuna studies
16 studies x 100 trials x 4 expanding-window folds
  = 6,400 model fits per horizon
```

**CV runs on BOTH candidate models, not just the winner** -- that is what selects
the winner. It cannot be narrowed without removing the comparison SRQ1 reports.

**Decision (Brian, 2026-09-08): H=3 only.** H=3 is the decision-relevant horizon
-- a quarter is when marketing budgets are authorised -- so ~2 hours of the run
would have been spent on a horizon the thesis does not report. The infrastructure
survives: `--horizon 1` still works if an examiner asks for the comparison.

**Trial budget kept at 100.** The script's own convergence analysis found the last
25 trials contribute 0-7 % of total improvement and 0.00pp in three of eight
studies, so 100 is already documented as sufficient. Cutting to 50 would halve CV
again but weakens the answer to "did you tune adequately?" -- a poor trade for
~25 minutes.

---

## F31 — Holiday features never reached any model, and FEATURES had 11 drifting copies (2026-09-09)

Brian's commit `1065b08` asked why training uses 13 features when the matrix has
54. Most of that gap is correct; two parts of it were not.

### The 54 -> 13 gap, accounted for

| Group | n | Verdict |
|---|---:|---|
| Identifiers, split, target | 8 | correctly excluded |
| Nielsen measures at time *t* | ~28 | **correctly excluded -- including them leaks.** `sales_value`, `promo_units`, `weighted_dist`, the whole `baseline_*` family are contemporaneous and unknown at forecast time |
| Holiday: `days_in_month`, `n_holidays`, `non_holiday_days` | 3 | **defect** |
| Intermittency: `zero_run_flag`, `zero_run_length` | 2 | **defect** |
| Used | 13 | -> now 18 |

The ~28 exclusions are why the count drops so far, and that part is sound. This
is worth stating in the thesis: the matrix is wide because it carries the raw
Nielsen panel, not because 40 features were discarded on a whim.

### Defect 1 — the ablation measured a benefit the model could not receive

Holiday enrichment shipped 2026-08-18 (7/12 cells improved, mean -1.42pp) and
`srq1_holiday_ablation.py` reports it. But the three columns were **never added to
any `FEATURES` list**, so the benchmark, the CV, the tuning and the served model
all ran without them. The ablation was measuring something the production model
did not do.

**Retraining alone would NOT have fixed this** -- the correction Brian proposed,
and the reason it matters that it was checked. `available_features()` intersects
the hardcoded literal with the matrix columns:

```python
return [c for c in wanted if c in fm.columns]      # never ADDS a column
```

A column absent from the literal stays absent however many times you retrain. The
VPS run would have produced a holiday-free model and needed doing twice.

`zero_run_flag` / `zero_run_length` were the same: engineered and leakage-fixed in
P0038, then referenced by no training script at all.

### Defect 2 — eleven copies, already drifted

`FEATURES = [...]` existed as a literal in **11 live files**, and they no longer
agreed: `srq1_pooled.py` carried 12 items to everyone else's 13, missing
`promo_intensity`. So the pooled-vs-per-category comparison -- whose entire point
is holding everything but pooling constant -- ran on two different feature spaces
without saying so.

### The fix

`srq1/_features.py`, mirroring `_horizon.py`: one definition, grouped by what each
group contributes, with the leakage boundary stated (**adding a raw Nielsen column
here is a leak; shift it in `engineer_features()` first**). All 11 files now import
it. `LOG_SCALE_FEATURES` (2 copies) likewise.

`resolve()` keeps DEC-DISCOVER-COLUMNS: it intersects against the matrix, so a
category without promotion omits that column rather than raising, and a matrix
built without holiday enrichment simply does not see those three.

**`srq1_pooled.py` needed different treatment, not the same list.** Pooling trains
one model across all four categories, so it can only use columns every category
carries. That set is now COMPUTED by `_pooled_features()` (17: everything but
`promo_intensity`) and printed at run start, rather than being a literal that
cannot notice new columns.

### Verified

- 18 canonical features; per category: CSD 18/18, danskvand 17/18, energidrikke
  18/18, RTD 17/18 -- `promo_intensity` absent exactly where Nielsen has none
- All 11 scripts import and report 18; `srq1_pooled` reports 17 common
- `srq1_benchmark.py` runs end-to-end on the new set
- `verify_setup.py` 10/10, no warnings

### Effect on the numbers (untuned benchmark, H=3)

| Category | 13 features | 18 features |
|---|---:|---:|
| CSD | 20.4 % | **19.1 %** |
| danskvand | 30.4 % | **30.2 %** |
| energidrikke | 17.3 % | **17.8 %** |
| RTD | 28.4 % | **27.7 %** |

Three of four improve. Best-model selection also changes (CSD now Ridge). These
are untuned single runs -- **the real comparison comes from the VPS run**; they
are recorded here only as evidence the features are now reaching the models.

### The lesson, again

Same shape as F24 and F29: **the plumbing existed and nothing connected it.** The
columns were engineered, the ablation read them, the contract gated them — and no
model consumed them. Trace a value to the line that uses it, not to the last place
it is mentioned.

---

### Regression: this fix broke five sibling scripts (P0053 F3)

Recorded here because F31 caused it, and the three machines share these files.

The centralization touched 11 scripts. **Five siblings were not on that list** and
built their own "with holiday features" arm by appending the three holiday columns
to `FEATURES` — correct when FEATURES was 13, a duplicate-column error now that it
is 18. The HPC's full retrain surfaced all five.

A second, separate cause was mine alone: I made `srq1_pooled.FEATURES` an empty
list filled inside `main()`, and `srq1_ridge_pooled.py` / `srq1_pooled_perbrand.py`
do `from srq1_pooled import FEATURES` — so importers received `[]`.

Patched 2026-09-09 in `4b38c53`; **not yet run.** The authoritative record is
P0053 F3, since the VPS/HPC side found it. Do not maintain two versions of this.

**The generalisable lesson:** a "define it once" fix is only complete when every
consumer is found. I searched for the literal `FEATURES = [`, which found the 11
files that *declared* it and missed the 5 that *imported and extended* it. Grep
for the identifier, not the assignment.


---

## F32 — Casing sweep: the SRQ4 half was never fixed, and half the sample was gone (2026-09-09)

The HPC fixed `CATS` casing across the SRQ1 scripts (`9745bf3`). The sweep found
the same defect still live in **three** places it had not reached, all on the
experiment side:

| File | Was | Effect |
|---|---|---|
| `srq4_experiment.py` `CAT_FILE` | lowercase keys | `KeyError` on Danskvand/Energidrikke -- **two of four categories unusable** |
| `forecast_tool.py` `CATEGORIES` | lowercase keys | the key is passed to `get_category_engineered_bymonth_dir()`, so it is a path component |
| `export_appendix.py` | 4 lowercase category lists | tables now write `Danskvand`, so the lists matched nothing |

**Scorable brands went from 120 to 168** once all four categories resolved --
the funded-run sample was missing 40 % of its population.

### The join was fragile too, and that is the durable part

Fixing the spelling alone would have traded one silent failure for another: the
results tables on disk were written *before* the casing fix, so they carry
`danskvand` while the caller now says `Danskvand`. The track-record lookup joins
on the raw string, so `historical_wmape` came back `None` for Danskvand -- a
degraded payload, the F21 shape again, from a fix rather than a bug.

`_cat_key()` now case-folds both sides of the join, and `canonical_category()`
normalises caller input at the entry point. The second matters beyond casing:
**Scenario C's caller is an LLM choosing tool arguments from a prompt**, and
requiring it to reproduce "Energidrikke" exactly is a requirement it will
sometimes miss -- landing as `unknown_category` instead of a forecast.

### The harness logged the payload but never checked it

`run_scenario_c` recorded `tool_output` and carefully verified the LLM had queried
the right series (`args_match_request`) -- but never checked the answer was
complete. Scenario C could have run all 10 repeats serving forecasts with **no
`historical_*` fields** (the very evidence that distinguishes C from B), with
every run logged `outcome: ok`.

Added `_payload_complete()`, applied per tool call and promoted to the run trace,
so a degraded run is visible in the results table rather than found by reading
logs. `verify_setup.py` now uses the **same predicate**, so pre-flight and run
cannot disagree about what "complete" means -- and it now rejects
present-but-null fields, which the old key-existence check would have passed.

### Verified

All four categories, real brands, scored month: `status=ok`, `months_ahead=3`,
track record present, `_payload_complete=True`. `verify_setup.py` 10/10.

### The pattern, stated once

Four findings now share one shape (F21, F25, F31, F32): **an identifier mismatch
between two artefacts that never raises.** A missing directory, a misplaced file,
an absent column, a differently-spelled key -- each returns *less* rather than
failing. The defence is the same every time: normalise at the join, and assert
the result is complete rather than merely present.

---

## F33 — Traceability checked against ch2 §2.5; the prompt registry was missing (2026-09-09)

Read the literature review from snapshot `2026-09-09_16-05_prose-pass` to derive
what the experiment must record, rather than deciding it ourselves. §2.5 names
Dong et al. (2024) "AgentOps", whose taxonomy specifies the artefacts an agent
needs to be auditable:

> execution traces, tool-call spans, prompt and guardrail registries

Checked the harness against that list:

| Artefact | State |
|---|---|
| Execution traces | `_cache_response()` writes the full raw response per run |
| Tool-call spans | `tool_calls[]` records args, match-check, and now payload completeness |
| Guardrail registry | `_classify()` failure classes + the `--budget` cap |
| **Prompt registry** | **MISSING from the record** |

`prompts.schema_id()` already existed -- a SHA-256 over every prompt string sent
(question, three capability notes, exemplar, sentinel, tool schema), excluding
per-run substitutions. **The harness never called it.** So a results table could
not be tied to the prompt version that produced it, and two runs whose prompts
differed were indistinguishable afterwards. Now in `_trace()` as
`prompt_schema_id` (currently `v3-recommendation-oneshot+ff9b62a101f0`).

Same shape as every other finding here: the mechanism existed and nothing
connected it.

**Also load-bearing from §2.5, and now asserted by the smoke test:** the thesis
adopts split conformal prediction (Lei et al., 2018), whose guarantee is
*marginal* and whose exchangeability assumption temporal data violates (Barber et
al., 2023) -- which is why ch6 measures coverage empirically. That measurement is
only meaningful if the interval is well-formed, so the smoke test checks
`lo < forecast < hi` rather than merely that a field is present.

§2.3 sharpens why the interval alone is not the deliverable: Goodwin et al. (2010)
found that supplying intervals **degraded** decision quality against point
forecasts (correct cost-regime discrimination fell 84% -> 44%), while
Pathirannehelage et al. (2025) find communicated uncertainty is a precondition of
trust. The resolution the thesis adopts is that the interpretive step is the
contribution -- which is exactly what Scenario C's payload carries and B's does
not. That is the argument `_payload_complete()` protects.

---

## F34 — The smoke test, and what it is not (2026-09-09)

`scenario_setup/smoke_test.py`: one run per scenario, ~$1, before the ~$40 set.

`verify_setup.py` never sends a request, so it cannot see anything that appears
only when a scenario runs. The smoke test runs `--repeats 1` under a `--budget`
cap into a `smoke/` subfolder (never the results directory) and asserts nine
things, each traceable to a requirement rather than chosen for coverage:

- every scenario `outcome == ok`; one target month across all arms
- Scenario C at `months_ahead == HORIZON` with a complete payload
- the 90% interval ordered and containing the point forecast
- `prompt_schema_id`, a cached raw response per run, a tool-call span for C
- cost within 10x of the measured per-run estimates

**What it does NOT cover: scenarios D and E.** `SCENARIOS` holds A, B and C
only -- the Prometheus arms are **not implemented in the harness at all**, and
the E2B template they need is not built. This is stated in the module docstring
so nobody reads a passing smoke test as clearance for the full five-scenario
ladder.

That gap is larger than it looks. D->E is the second half of the thesis's central
comparison: B->C and D->E are **the same intervention on two different
orchestrators**, and agreement between them is a materially stronger claim than
either alone (INHERITED_CONTEXT §1). Only one half exists today.

---

## F35 — CORRECTION: the E2B template is built; D/E is not blocked (2026-09-10)

**I have repeatedly written that "the E2B template is unbuilt" and that scenario
D would run without statsmodels/prophet. That is wrong, and it is in P0049's
task_plan phase 5, its focus_detail, and the smoke test's docstring.**

Reading P0040 (archived) rather than restating from memory:

| Prerequisite | State | Evidence |
|---|---|---|
| E2B template `prometheus` | **BUILT 2026-08-21**, alias resolves | P0040 F42, id `fxe7gzkqjupdhbx4uvpr` |
| Template carries the libraries | **verified** — pyodbc, sqlalchemy, statsmodels, xgboost, prophet all present | F42 probe, against all five missing on the base image |
| Engine venv | **live today** — python 3.13.13, `e2b_code_interpreter` 2.0.0, `pydantic_ai` 1.73.0, both hard pins satisfied | F46, re-verified 2026-09-10 |
| Engine tool API | verified against the blueprint | F13 |
| RU warehouse credentials | verified live | F35 (P0040) |
| E2B cost | ~$0.0001/run, negligible | F38 |
| Engine reachable on this laptop | `Z:\_dev-ssd\prometheus\prometheus-graph-engine` | confirmed 2026-09-10 |

**What actually remains** is P0040 tasks 4-7, and it is a port, not a build:

1. **Launch the engine locally** (task 4, `in_progress`) — the environment is
   built and verified; it has simply never been started.
2. **Run `D_prometheus`** on the SRQ4 prompt with logging + cost capture (task 5).
3. **Port `forecast_demand` to the engine's tool API** (task 6) — drop the
   `chain` argument, repoint paths through `PATHS`.
4. **Register the tooled project, run `E_prometheus_model`** (task 7).

**The correction that matters for planning:** D/E was never blocked on
infrastructure. It is blocked on nobody having written `run_scenario_d` /
`run_scenario_e` — `SCENARIOS` still holds A, B and C, and a repo-wide search for
those names returns nothing. That is a smaller and better-understood job than
"build the template first", which I had been treating as the gate.

**Why I got it wrong:** P0049's `INHERITED_CONTEXT.md` §6 says "The E2B template
build is REQUIRED before D/E, not optional", written while it was still true. It
was built the next day and the inherited note was never updated. I then repeated
it from the plan rather than checking the finding it pointed at.

Same lesson as this plan's own opening: **a stated blocker is a claim with a
timestamp.** P0049 was created specifically because two of four inherited
blockers were stale on inspection; this is a third, and it was mine.

---

## F36 — Prometheus and the thesis read the SAME warehouse; D uses the snapshot (2026-09-10)

Brian asked whether Prometheus has access to the same database. **It does**, and
checking it settled a design question rather than merely confirming a detail.

`graph-engine/data_agents/projects/prometheus/data/data_connection_configuration.md`:

> Database: `Nielsen_clean` (Microsoft Fabric / SQL Server, T-SQL dialect).
> **Preferred path: the query tools.** `run_sql`, `inspect_schema`,
> `distinct_values`, `sample_rows` ...

The thesis pipeline reads the same place — `nielsen_connector.py` opens
`Nielsen_clean` on the same Fabric warehouse — and snapshotted it to JSONL on
**2026-06-30** (`_00_raw/nielsen/data_jsonl/MANIFEST.json`). Manifold AI supplied
both, so this is one data source with two access paths, not two sources.

### DEC-D-SNAPSHOT (Brian, 2026-09-10): D and E read the local snapshot, not the live warehouse

Confirmed explicitly. The reasoning is stronger than "hold a variable constant":

1. **It would otherwise be a second variable.** Scenario B gets the firm's history
   as a local CSV in a sandbox. If D queries the warehouse live, D->E and B->C
   differ in *engine* AND *data path*, and the agreement between the two ladders
   -- the design's strongest claim -- stops being attributable.
2. **It is a LEAKAGE risk, not only a confound.** The snapshot is from 2026-06-30;
   the warehouse is live. A live query could return months the snapshot does not
   have, including the held-out target month. Every leakage guard in the harness
   (`_assert_no_leakage`, the exact-horizon gap check) operates on the matrices,
   and **none of them can see a query the engine issues inside a sandbox.** D
   reading live data would bypass the whole guard layer silently.
3. **It keeps D reproducible in the one sense that matters.** D and E are not
   examiner-reproducible (Prometheus is proprietary), but they must at least be
   re-runnable by us. A live warehouse makes a re-run a different experiment.

**Implementation consequence:** the port must supply the same fitted history B
gets, and must NOT hand the engine warehouse credentials. Prometheus's own docs
say the query tools are the preferred path and `execute_code` is a fallback -- so
the tooled project has to be registered WITHOUT the SQL tools, or D silently gets
a capability B does not have.

That is a real difference from the shipped configuration and belongs in the
methodology: **D is Prometheus as it ships minus warehouse access**, because
matching B's data path is what makes D->E comparable to B->C.

---

## F37 — Why the engine runs locally even though E2B exists (2026-09-10)

Brian asked why step 1 is "launch the engine locally" when the project has E2B.
They are not alternatives; they are caller and callee.

| Component | Runs where | Does what |
|---|---|---|
| Graph engine (LangGraph) | **locally**, in `graph-engine/.venv` | orchestrates: decides actions, calls the LLM, registers tools |
| E2B sandbox | remote, per code action | executes the Python the coder agent writes |

The engine opens an E2B sandbox when it needs to run code; the `prometheus`
template exists so that sandbox carries statsmodels/prophet (P0040 F42). Nothing
runs the engine itself inside E2B.

Cost therefore splits: launching the engine is free, E2B is ~$0.0001/run
(F38), and the gpt-5.5 calls are the real spend. The open question is only
whether the engine **starts** -- its venv is verified (F46, re-checked
2026-09-10) but has never been run.

---

## F38 — What Scenario B actually receives, and why it is NOT warehouse-equivalent (2026-09-10)

Brian pushed on three things. All three check out, and together they change the
D/E port design.

### 1. The 39 rows are real (verified)

All 39 rows join to the feature matrix on (year, month) and `sales_units` is
**identical**. Not hallucinated, not synthesised. 39 of HARBOE's 46 months,
because the 7 held-out test months are correctly withheld.

### 2. My "June 30" date was wrong

`MANIFEST.json` says `2026-06-30`, but that is a **stale manifest timestamp**.
The converted parquets were written **2026-08-12**, and the data runs to
**2026-07** in both the converted `dim_period` and the engineered matrix — 46
distinct months, identical range in both. Brian was right; feature engineering
was done on the converted parquet, and the two agree.

**Lesson: a manifest is a claim with a timestamp, like a stated blocker.** Read
the data, not the file that describes it.

### 3. The CSV is heavily pre-processed, and that is the real problem

| | Raw warehouse (CSD) | What Scenario B gets |
|---|---|---|
| Shape | **10,311,342 rows x 32 cols**, 732 MB | **39 rows x 4 cols**, 1,701 bytes |
| Structure | star schema: `facts_v` + 3 dimension views, grain `market_id x period_id x product_id` | one flat table |
| Scope | every brand, market, product | **one brand, one category** |
| Aggregation | none | monthly, brand-level, pre-aggregated |
| Columns | 32 measures | `period_year, period_month, sales_units, promo_intensity` |

Delivered as **CSV text pasted into the prompt**, not a file — 1,701 bytes into
`code_interpreter` with `container: auto`.

**So Scenario B does not simulate warehouse access at all.** It simulates *"an
analyst has already found the right brand, joined the star schema, resolved the
product-hierarchy node, aggregated to monthly, and handed you the series."* Every
hard part of using this warehouse is done before B starts.

That is defensible as a design, but **it must be stated as an assumption rather
than left implicit** — Brian's framing is the right one: an agent asked about one
brand would plausibly filter to that brand first, because it is the cheapest path
to an answer. What cannot be claimed is that B measures warehouse-querying ability.

### The hierarchy trap makes this sharper, not softer

`warehouse_guide.md` documents five traps, and the first two are severe:

> `<p>_clean_facts_v` carries not only leaf UPC rows but also PRE-AGGREGATED rows
> (category / manufacturer / brand totals) under their own `product_id`s.
> `SUM(facts_v)` with no product filter -> includes the aggregate rows -> wildly
> overcounts.

and

> NEVER SUM ACROSS LEVELS ... within one level there are SEVERAL alternative
> breakdowns ... each re-partitions the total.

**An agent given the raw warehouse would very likely get the wrong number**, and
that failure would have nothing to do with forecasting. Handing B and D the raw
star schema would measure schema-navigation skill, not the intervention the
thesis is about.

**This is the strongest argument for the pre-aggregated CSV, and it is a better
one than convenience.** It should go in the methodology in those terms.

---

## F39 — How Prometheus feeds a 700 MB warehouse to an LLM (2026-09-10)

Brian asked how the engine avoids shipping the whole table to GPT-5.5. Read from
`prometheus_coder.py`; the mechanism is a **two-tier split**, and it matters for
the port.

```python
def _ru_show(df, max_rows=100):        # what the MODEL sees
_MAX_RESULT_CHARS = 8000               # hard cap on tool-result text
def _ru_stash(df):                     # the FULL frame stays in the kernel
    globals()["df"] = df               # available to execute_code as df, df_1, ...
```

| Tier | Holds | Size |
|---|---|---|
| Model context | a rendered text table | **100 rows max, 8,000 chars max**, then truncated with an instruction to re-query or aggregate |
| Sandbox kernel | the full DataFrame | whatever the query returned |

So the model never sees the data — it sees a **preview** and writes code against a
handle. Charts and derived numbers are computed sandbox-side. Nothing is persisted
per session; the sandbox is ephemeral.

**Consequence for the port:** the engine's data path is *preview + handle*, while
B's is *whole series inline in the prompt*. Given B's series is 39 rows and 1.7 KB,
it fits under both caps comfortably — so the same data can be delivered to D
without either arm being truncated. The delivery mechanism differs; the
information does not.

That difference is worth one sentence in the methodology, because it is a genuine
architectural difference between a general LLM and a production data agent, and
it favours neither on this task size.

---

## F40 — How Prometheus actually gives GPT-5.5 the warehouse, answered from the code (2026-09-10)

Brian asked three mechanism questions. Answered by reading, not paraphrase.

### Q1: the full frame stays in the kernel, and the model sees only 100 rows?

**Yes, and the kernel is the E2B SANDBOX, not Prometheus's own server.** `run_sql`
does not query the database in-process — it sends a *snippet* into the sandbox:

```python
snippet = (f"_df = _ru_query({query!r})\n"
           f"_n = _ru_stash(_df)\n"
           f"print('[stashed as df and df_%d]' % _n)\n"
           f"_ru_show(_df)\n")
return await _run_snippet(ctx, snippet)
```

So the chain is: **model writes SQL -> engine forwards it to the sandbox ->
sandbox connects to Fabric, holds the DataFrame, prints a preview -> only the
printed text returns to the model.**

| Where | What lives there | Limit |
|---|---|---|
| Model context | printed preview | `max_rows=100`, then `_MAX_RESULT_CHARS = 8000`, truncated with "re-query with fewer columns/rows or aggregate" |
| E2B sandbox kernel | the full DataFrame, as `df`, `df_1`, ... | whatever the query returned |
| Engine process | neither — it is a courier | -- |

The model therefore **never holds the data**. It holds a handle and writes code
against it. Charts are rendered sandbox-side. The sandbox is ephemeral, so nothing
persists per session -- answering Brian's storage question: no per-session storage
cost, because nothing is saved.

### Q2: who is `warehouse_guide.md` passed to?

**The coder sub-agent's system prompt, not the conversational agent's:**

```python
coder_guardrails=warehouse_guide,          # prometheus.py:61
conversational_guardrails=(persona + memory_guardrails + proactive_guidelines),
```

So it reaches GPT-5.5, but only in the coder role. It is ~5 KB of hard-won
warehouse semantics: the star schema, the five traps, the product-hierarchy rules.
**That is a substantial capability the general LLM in Scenario B does not have**,
and it is part of what "the production system" means -- it is not incidental
configuration.

### Q3: is this a fair comparison?

**Not on data access, no -- and it cannot be made fair by giving both the raw
warehouse.** Three asymmetries exist, and they need different treatment:

| Asymmetry | Fix |
|---|---|
| B gets a 39-row aggregate; the warehouse is 10.3M rows across a star schema | **Hold constant**: give D the same series |
| Prometheus's coder carries `warehouse_guide.md`; B's LLM carries nothing equivalent | **Becomes moot** once D is not querying SQL -- the guide describes tools D will not have |
| Prometheus has live Fabric access; B has prompt text | **Declare as a limitation** -- see DEC-D-SNAPSHOT (F36) |

The middle row is the useful consequence of removing the SQL tools: it removes the
prompt asymmetry at the same time, because the guide is only relevant to tools
that are no longer registered.

---

## F41 — Both free tests PASS: the engine starts, and the tools are composable (2026-09-10)

### The engine runs

```
ENGINE IMPORTS + GRAPH COMPILES OK
  main_agent_model: gpt-5.5
  coder_model     : gpt-5.5
```

Missing-integration warnings for Gemini, Logfire and Twilio only -- all optional.
**P0040 task 4 ("get the engine running locally") is effectively discharged.**

**Two env facts the port needs.** The engine has NO `.env` of its own, only
`.env.example`, and its `Settings` model has exactly **two required fields**:

| Variable | Source | Note |
|---|---|---|
| `OPENAI_API_KEY` | thesis `.env` under `thesis_manifold_openai_prompts` | name differs; must be mapped |
| `AZURE_STORAGE_CONNECTION_STRING` | **not held** | only used by `utils/blob_storage.py` for chart artefacts; `UseDevelopmentStorage=true` satisfies the validator and the engine starts |

Everything else defaults. `E2B_API_KEY` maps from `thesis_manifold_e2b_sandbox`,
the same indirection `measure_e2b_cost.py` already uses.

### The SQL tools are removable

`tool_names` on `ProjectDeps` is a plain list, and the coder registers its tools
explicitly:

```python
tools=[Tool(run_sql, ...), Tool(inspect_schema, ...), Tool(distinct_values, ...),
       Tool(sample_rows, ...), Tool(execute_code, ...)]
```

So a D-variant registering **only `execute_code`** is a small, local change rather
than a fork. That is exactly what DEC-D-SNAPSHOT requires, and it lands D on the
same footing as B: code-as-action over a supplied series, no database.

---

## OPEN QUESTIONS — Brian, 2026-09-10 (not yet resolved)

**Q-A: Does the brand sample still hold at three per category?** Brian recalls
planning B-E across **three brands per category** -- max-viable, median and
min-viable data quality -- so an assessor's generalisability question can be
answered on sparse brands too. `_stratified_brands()` already returns exactly 3
(highest / median / lowest volume), so the *mechanism* matches. **What is not
confirmed** is whether D/E run the same 3 or a subset, and what that does to
cost. Needs deciding before the funded set.

**Q-B: How is the reduced dataset declared?** Brian's position, recorded verbatim
in substance: the reduced dataset is *not* the scenario originally proposed
("data access & code vs. model access for predictive quality"). In production
Prometheus has live warehouse access; the experiment does not reproduce that.
Basic statistical code can still be written from 39 real rows, so **the experiment
holds** -- but it must be raised transparently in BOTH the experiment design and
the limitations, not just one.

**Q-C: Which raw shape, if not the aggregate?** The hierarchy traps (F38) argue
for keeping the 39-row series. Not yet written up as a decision.
