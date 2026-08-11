# Archived grain artifacts — P0035, 2026-08-01

Everything here was removed from the live tree by plan
`plans/P0035_2026-08-01_grain-artifact-removal/`. Nothing here is deleted,
because all of it is **evidence for why the chain/region grain was dropped**.

## Why

**DEC-GRAIN** (Enrico, 2026-07-12) locked the modelling grain to **brand x month**.
Chain and region grain became a documented limitation + future work rather than
an active result. The `02_thesis_data/_03_engineered/bychain/` data directory was
deleted from disk before this plan ran, leaving live code resolving to a
non-existent path — that half-state is what P0035 removed.

## Contents

### `phase3_region_grain_test.py`
Was: `03_thesis_modelling/model_training/phase3_region_grain_test.py`
(added in commit `d892af8`).

Standalone harness whose entire purpose was to load the region-grain CSD feature
matrix (brand x region x period, 25.1k rows) and compare its test WMAPE against
the 16.5% brand x month baseline. That comparison is exactly the question
DEC-GRAIN closed, and the same test harness that harness task **B02** was dropped
for. Archived rather than deleted: it is the evidence behind the grain decision.

### `srq1_benchmark.py`, `srq1_benchmark_tuned.py`, `srq1_figures.py`, `srq1_profiling.py`, `srq2_synthesis.py`, `srq4_experiment.py`, `srq4_tier2.py`, `forecast_service.py`
Were: `utility_scripts/scripts/*`.

**Stale P0028 shadow copies** of the canonical scripts in
`03_thesis_modelling/model_training/` and
`03_thesis_modelling/model_serving/system_a_forecast/`. See P0035 finding **F6**
for the full canonical-tree determination. Summary of the evidence:

- Both trees landed together in `8329881`; only `03_thesis_modelling/` received
  later commits (`5b64c40`, `d892af8`). `utility_scripts/scripts/` received none.
- The `03_thesis_modelling/` copies are grain-aware (argparse `--grain/--grains`,
  `DEFAULT_GRAINS = ["bymonth"]`, graceful skip on missing matrix) and fix the
  feature name `weighted_distribution` -> `weighted_dist`. The archived copies
  still carry the pre-DEC-GRAIN shape ("Runs on BOTH granularities ... _04
  brand x chain (primary)").
- Nothing in the repo imports or invokes the `utility_scripts/` copies.
- `.claude/rules/repo-tier-structure.md` states `utility_scripts/` is
  tooling-only and must never hold thesis pipeline logic.

## Known follow-up (NOT done by P0035)

`utility_scripts/scripts/` still holds four more shadow copies —
`srq1_baselines_stat.py`, `srq1_calibration.py`, `srq1_shap.py`,
`srq2_agent.py` — which duplicate `03_thesis_modelling/model_training/`.
They were left in place because they contain **no grain references**, so they
fall outside P0035's scope. They are still a tier-structure violation and should
be archived by a separate cleanup pass.
