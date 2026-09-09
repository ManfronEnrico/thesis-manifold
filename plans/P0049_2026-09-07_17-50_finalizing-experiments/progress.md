---
name: p0049-progress
description: STATE - Session log for P0049. What was delivered, what was tried and rejected, and exactly where the two-horizon run stopped.
pid: P0049
created: 2026_09_07-20_45
updated: 2026_09_07-20_45
---

# P0049 — Progress

## Session 2026-09-07 (evening)

### Delivered

**The horizon fix, all three layers** (F23). Implemented, verified, committed.
`engineer_features()` now takes a required `horizon`; `srq4_experiment.py` scores
`test.iloc[HORIZON-1]`; the forecast tool is passed the scored month explicitly
and reports `months_ahead`. All 8 feature matrices rebuilt.

**Both horizons made runnable** (F24). `srq1/_horizon.py` resolves ONE value per
run (`SRQ1_HORIZON`, default 3) into both the input matrix and the output
directory. 21 SRQ1 scripts routed through it. H=3 keeps the unsuffixed paths;
H=1 writes to `h1/`, so **an H=1 run cannot overwrite an H=3 result**.

**`run_both_horizons.py`** — 8 ordered stages x 2 horizons, with `--dry-run`,
`--horizon`, `--only` and `--resume`.

### Where the two-horizon run actually stopped

| Stage | H=3 | H=1 |
|---|---|---|
| benchmark | done 18:51 | done 18:25 |
| benchmark_cv | **done 19:47** (56 min) | not started |
| benchmark_tuned | **done 19:51** (3 min) | not started |
| baselines_stat | not started | not started |
| calibration | not started | not started |
| train_persist | not started | not started |
| shap / perf figures | not started | not started |

**Resume tomorrow with one command:**

```bash
python 01_SRQ1_Model_Training/02_thesis_modelling/model_training/run_both_horizons.py --resume
```

`--resume` skips only stages whose artefact was written *after the current run
began*, so a stale table never counts as done.

### Two defects found, neither of which was the task

- **F25** — `train_and_persist.py` read its five model-selection inputs from the
  results tier ROOT; they live in `tables/` and `models/`. Every read is guarded
  by `is_file()`, so selection silently fell through to a hardcoded `"XGBoost"`
  default and never consulted the CV study — beneath a long comment explaining
  why selecting on `cv_score` matters. The default was wrong for all four
  categories.
- Third instance of one pattern (F21, F22's scoring default, F25): **a
  soft-failing read of a misplaced path degrades into a weaker result rather than
  an error.** Worth a lint rule.

### Tried and rejected — do not revisit without new information

**Moving training to a VPS, and committing the feature matrices** (F27). Both were
proposed to escape memory kills. Both were wrong:

- The suite uses **282 MB** (CV) / **247 MB** (tuned). Measured while running, not
  estimated. It was never memory-hungry — `XGB_N_JOBS=1` keeps per-fit memory low.
- The kills came from **two suites running concurrently**: a `nohup` launch whose
  wrapper had returned (so it looked finished) was still alive when a second run
  started. Six orphaned processes terminated.
- Freeing them recovered ~0.1 GB. The pressure was **other applications** — Word
  424 MB, VS Code 527 MB, `MemCompression` 1.27 GB.
- The matrices are **4.5 MB total**, so GitHub limits were never the obstacle. They
  stay gitignored because of the **Nielsen confidentiality agreement with Manifold
  AI** — brand-level monthly sales for named Danish brands is the confidential
  data itself, merely transformed.

### Near-misses

- **My "RTD improves because of survivorship" hypothesis was wrong**, and I only
  found out by testing it. The 10 brands H=3 drops carry **0.3 % of test volume**,
  and WMAPE is volume-weighted. Restricting H=1 to the surviving brands moved the
  baseline 0.1 pp. Corrected in F26 rather than left standing.
- **Two files had their horizon import inserted AFTER first use** by a regex whose
  continuation pattern over-matched. Compiled fine; would have raised `NameError`
  at runtime. Caught by an explicit import-before-use scan across all files, not
  by `py_compile`.
- **`training_report.py` had its import spliced into the middle of an existing
  comment**, and referenced a `_here` variable that file does not define. Also
  compiled fine.

### State at close

- Training stopped cleanly; no half-written artefacts.
- `verify_setup.py`: **10/10, no warnings** — re-checked after the restructure.
- Horizon fix re-verified post-restructure: `h3.lag_1 == h1.lag_3` in all 4
  categories.
- The parallel session restructured `05_thesis_results/` into chapter-keyed
  folders mid-run (`srq1_model_performance` -> `06_model_benchmark`). All outputs
  survived; `PATHS.py` was updated, so the horizon helper follows automatically.

### Note on the commit history

The parallel session's commit `362fe1f` (20:34) **swept in this session's code
changes** — `engineer_features.py`, `srq4_experiment.py`, `forecast_tool.py`,
`_horizon.py`, `run_both_horizons.py` and the 21 routed scripts are all already
committed under a message about the results restructure. Nothing was lost, but
the horizon fix is not findable by its commit message. This is what selective
staging is meant to prevent.

---

## Session 2026-09-09 — experiment-side work, training moved off this machine

Training now runs on the HPC (P0053). This session deliberately covered only what
is **decoupled from training**, so results plug in when they land.

### Delivered

**F31 — the feature set.** Brian asked why training used 13 features from a
54-column matrix. Most of that gap is correct (~28 columns are contemporaneous
Nielsen measures that would leak). Two parts were not:

- holiday enrichment reached NO model, so the ablation measured a benefit the
  served model could not receive
- `FEATURES` existed as a literal in 11 live files and had already drifted

Now `srq1/_features.py`, one definition, **13 -> 18 features**. `srq1_pooled.py`
computes the cross-category intersection (17) rather than carrying a literal.

**F32 — casing sweep.** The HPC's `CATS` fix covered SRQ1; three experiment-side
files still had lowercase keys. `srq4_experiment.CAT_FILE` raised `KeyError` on
two of four categories: **scorable brands 120 -> 168**, so the funded-run sample
was missing 40 % of its population. Added `_cat_key()` (case-folded join) and
`canonical_category()` (normalises caller input, which matters because Scenario
C's caller is an LLM).

Also: the harness logged `tool_output` but never checked it. Scenario C could
have run every repeat with no `historical_*` fields, each logged `outcome: ok`.
Added `_payload_complete()`, per call and in the run trace.

**F33/F34 — traceability and the smoke test.** Read ch2 §2.5 from snapshot
`2026-09-09_16-05_prose-pass` to derive requirements rather than choosing them.
Dong et al. (2024) name four auditable artefacts; three were present, the
**prompt registry was not** — `prompts.schema_id()` existed and was never
called. Now in every trace.

`scenario_setup/smoke_test.py`: one run per scenario, ~$0.81, nine checks each
tied to a stated requirement.

### Corrected mid-session

**Brian's diagnosis of the holiday features was half right.** He proposed that
retraining on the HPC would pick them up. It would not: `available_features()`
intersects a hardcoded list with the matrix and never *adds* a column the list
omits. The HPC run would have produced a holiday-free model and needed doing
twice. Verified before accepting.

**My blanket edit of `srq1_pooled.py` was wrong.** Replacing its literal with the
full 18-item list would have made it hard-fail on Danskvand/RTD, which lack
`promo_intensity`. Pooling needs the intersection, not the union. Caught by
reading how the file used `FEATURES` rather than assuming.

### Near-misses

- Three figures (`ch6_model_selection_v2` and two siblings) existed ONLY in the
  stale `06_model_benchmark/` tree I deleted earlier. Restored from git and moved
  into the live tree. The mistake was inspecting a sample of four files, not the
  full set, before an irreversible delete.
- `requirements.txt` pins the laptop's SYSTEM python versions (xgboost 3.4.1) not
  the venv's (3.2.0). A VPS built from it would produce incomparable numbers,
  silently. Hence `P0053/requirements-training.txt`.

### State at close

- 4 commits, all pushed: `3f8b0a9`, `67a5474`, `a7002ea`, `ae4c290`
- `verify_setup.py` 10/10; all four categories resolve; 168 scorable brands;
  18 features; every payload complete at `months_ahead=3`
- Working tree holds only the parallel prose session's files

### Open, in order

1. **DEC-VENDOR** — pure writing, blocks the funded runs
2. **Scenarios D/E** — `SCENARIOS` holds A/B/C only. **Not implemented at all**,
   and the E2B template is unbuilt. B->C and D->E are the same intervention on
   two orchestrators; only one half exists
3. **Run the smoke test** once HPC results land, then the funded set
