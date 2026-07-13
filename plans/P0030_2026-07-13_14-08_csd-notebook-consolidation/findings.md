# P0030 Findings

## Pre-Decomposition Investigation (2026-07-13)

### Step script sizes and structure

| Script | Lines | Core function(s) |
|--------|-------|-------------------|
| `pre_csd_0_cache.py` | 265 | `validate_parquet_cache()` (lines 111-181) |
| `pre_csd_1_load_and_aggregate.py` | 363 | `_load_merged()` (197-220), `load_and_aggregate()` (223-271), `GRAIN_CONFIG`/`DVH_REGION_IDS` config (123-176) |
| `pre_csd_2_build_calendar.py` | 254 | `build_calendar_index()` (100-159) |
| `pre_csd_3_filter_series.py` | 196 | filtering logic inside `run_step()` (99-172) |
| `pre_csd_4_engineer_features.py` | 252 | `engineer_csd_features()` (116-159), wraps shared `engineer_features()` from `_shared_modules` |
| `pre_csd_5_apply_split.py` | 202 | split logic inside `run_step()` (110-178) |
| `pre_csd_6_save_outputs.py` | 404 | output-writing logic inside `run_step()` (118-380) |

Total: 1,936 lines across 7 scripts. A large fraction of each file is CLI/argparse wrapper, path-resolution boilerplate (root-finding, `sys.path.insert`), and per-step timing/logging via `_shared_modules/terminal_utils.py` and `timing_utils.py` — none of that is "logic" in the sense that matters for the notebook; Brian's point that raw line-count comparisons are misleading is correct and was accounted for in each task's scope (only the named core functions transfer, not the full file).

### Shared module dependency (critical constraint)

Only **Step 4** (`pre_csd_4_engineer_features.py`, line 46) imports actual computational logic from `_shared_modules`: `from engineer_features import engineer_features as shared_engineer_features`. All other steps' `_shared_modules` imports are for `terminal_utils`/`timing_utils` (print formatting / step timing), not core logic.

This means Task 5 (Step 4 transfer) is the only task where "don't duplicate the shared module" is a hard constraint — the notebook must `sys.path.insert` and `import` the real `_shared_modules/engineer_features.py`, exactly as `pre_csd_4_engineer_features.py` does, rather than copying its function body inline. This module also carries the `group_keys` leakage fix (P0027 Phase 4a) and is shared by Danskvand/Energidrikke/RTD's pipelines — duplicating it here would fork a fix that already required real effort to land correctly once.

### Orchestrator scope boundary

`preprocessing_csd.py` (the CSD orchestrator) was explicitly named out of scope by Brian's task-decomposition instructions. It currently runs Steps 1-6 as subprocesses (`STEPS = [1, 2, 3, 4, 5, 6]`) with `--grain`/`--run-step` CLI flags (see P0029 findings for full detail). Task 7 flags — but does not decide — the eventual question of whether the notebook replaces this subprocess chain or coexists with it.

### Starting point: notebook already exists

`pre_processing_notebook_csd.py.ipynb` was created in the prior session (before this plan) as an exact copy of the fixed `pre_csd_1.5_eda.ipynb` (48 cells, `INPUT_AGGREGATE` path bug already fixed to `step_1_aggregate_{grain}.parquet`, dynamic `GRAIN` variable). This plan's Task 1 begins by inserting Step 0 *before* the existing Cell 1 (which currently reads Step 1's output parquet) — Task 2 then replaces that read with real Step 1 logic.

## Task Execution Log

_Populated as each task is executed — see progress.md for narrative session log._
