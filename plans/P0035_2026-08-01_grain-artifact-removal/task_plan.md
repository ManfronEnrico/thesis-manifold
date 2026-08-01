---
pid: P0035
created: 2026-08-01 00:00:00
updated: 2026-08-01 00:00:00
status: in_progress
focus_detail: "Remove every chain/region-grain artifact from live code, paths and results so the pipeline targets brand×month only, per DEC-GRAIN. Data is already gone from disk; the code references are not."
---

# P0035 — Remove Grain Artifacts (brand×month only)

> **Independent plan.** Pure cleanup — no new analysis. Can run in parallel with
> P0032/P0033/P0034, with one sequencing note (see Coupling).

## Decision

**DEC-GRAIN** (Enrico, 2026-07-12) fixed the grain to **brand×month**, adopting Brian's
proposal. Chain and region grains are dropped from active results and become a documented
limitation + future work.

**Brian, 2026-08-01:** remove all grain-related artifacts so everything targets brand×month only.

## Current state — data is gone, code is not

Verified 2026-08-01:

- `02_thesis_data/_03_engineered/` now contains **only** `bymonth/`. The `bychain/` folder
  is already deleted from disk.
- But **~20 live files still reference the chain/region grain** — path constants, FEATURES
  lists, a whole standalone test script, and results artifacts.

This is the dangerous half-state: code that resolves paths to a directory that no longer
exists, and results files that report numbers from a grain the thesis no longer claims.

### Live references to clean (excludes `.archive/`, plans, harness docs)

| Area | Files |
|------|-------|
| **Path constants** | `PATHS.py` — `THESIS_DATA_ENGINEERED_BYCHAIN_DIR`, `get_category_engineered_bychain_dir()`, and the deprecated `get_category_engineered_dir()` alias |
| **Standalone region test** | `03_thesis_modelling/model_training/phase3_region_grain_test.py` — entire script exists only to test the region grain against the 16.5% brand×month baseline. Obsolete by DEC-GRAIN. |
| **Model training** | `srq1_benchmark.py`, `srq1_benchmark_tuned.py`, `srq1_figures.py`, `srq1_profiling.py`, `srq2_synthesis.py`, `srq4_experiment.py`, `srq4_tier2.py` |
| **Model serving** | `model_serving/system_a_forecast/forecast_service.py` |
| **utility_scripts duplicates** | `utility_scripts/scripts/` carries near-identical copies of most of the above — verify whether these are live or stale leftovers before editing both |
| **Results** | `04_thesis_results/srq1/tuned_params.json`, `tuned_summary.md` — contain chain-grain entries |
| **Preprocessing** | `_02_preprocessing/nielsen/CSD/preprocessing_csd.py`, `pre_processing_notebook_csd.ipynb` |
| **Docs** | `.claude/rules/repo-tier-structure.md`, `user-docs/contributing/repository_map.md` |

## Scope boundary

**In:** live code, path constants, results artifacts, and repo docs that reference chain/region grain.

**Out:**
- `.archive/**` — leave alone, it is archived by definition.
- `plans/.archive/**` and harness docs — historical record of *why* the grain was dropped; deleting them destroys the audit trail.
- **Ch6/Ch8 prose tables** — these are P0034's job (task 5). This plan does code and data only.
- The `group_keys` parameterization in `_shared_modules/engineer_features.py` — see F1 in `findings.md`. It is grain-*capable*, not grain-*committed*, and removing it would be a gratuitous rewrite. Default it to `["brand"]` and leave the mechanism.

## Coupling

- **P0033** builds three notebooks that will call the shared modules. Doing P0035 first
  means those notebooks are written against a clean brand×month-only surface. If P0033
  starts first, that is fine — just do not add chain-grain calls to the new notebooks.
- **P0034 task 5** rewrites the Ch6 tables that present the month-vs-chain comparison.
  P0035 supplies the code-side truth those tables must match.

## Phases

| Phase | Goal | Tasks |
|-------|------|-------|
| 1 | Inventory + classify each reference | 1, 2 |
| 2 | Remove path constants + obsolete script | 3, 4 |
| 3 | Clean consumers + results | 5, 6 |
| 4 | Update docs + verify nothing breaks | 7, 8 |

## Definition of done

- No live code resolves a `bychain` path.
- `phase3_region_grain_test.py` removed or archived with a reason.
- `04_thesis_results/srq1/` contains no chain-grain entries.
- Repo docs describe a brand×month-only pipeline.
- CSD pipeline still runs end-to-end after the removals.

## Related

- `harness/thesis_tasks.json` — DEC-GRAIN; B02 dropped as a consequence
- P0026 — the earlier brand×region×period grain work this supersedes
- P0034 — the prose-side counterpart
