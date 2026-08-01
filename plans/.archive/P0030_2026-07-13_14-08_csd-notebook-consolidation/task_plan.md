---
pid: P0030
created: 2026-07-13 14:08:00
updated: 2026-07-13 14:08:00
status: complete
completed: 2026-07-13 17:45:00
outcome_summary: "All 8 tasks complete. Notebook runs top-to-bottom (58 brands, 2,552 rows, 30 engineered columns) with EDA parameters threaded in-memory into feature engineering (never re-hardcoded). Post-migration hardening added: auto-detected structural break scan (replaced a dead COVID-only check -- CSD data starts 2022-10, after COVID onset), zero-run flag/length features (intermittent-demand literature), per-category log-transform gate (TARGET_FOR_MODEL, not a blanket rule across categories), log1p(weighted_dist) feature (from correlation-heatmap non-linearity finding), non-blocking plots (inline in Jupyter / Agg fallback in scripts), dead INPUT_AGGREGATE variable removed. Brian archived the original 7 .py scripts to pipeline_step_scripts/.archive/ -- notebook is now the sole CSD preprocessing path. One save collision occurred mid-session (Jupyter save clobbered 3 in-progress fixes); recovered by reapplying from source, re-verified end-to-end after recovery."
---

# P0030 — CSD Combined Preprocessing Notebook Migration

## Goal

Migrate CSD's 7-stage preprocessing pipeline (Step 0 cache validation → Step 1 load/aggregate → Step 2 build calendar → Step 3 filter series → Step 4 engineer features → Step 5 apply split → Step 6 save outputs) plus the already-fixed EDA stage, from 8 separate `.py` scripts into a **single combined Jupyter notebook**: `pre_processing_notebook_csd.py.ipynb` (already created 2026-07-13 as an exact copy of the fixed EDA notebook).

This is a direct continuation of P0029 (ChatGPT EDA gap analysis reconciliation), which fixed the EDA notebook's stale input path and surfaced several methodology gaps (model-selection leakage, missing-period audit, etc.) — several of those gaps are naturally addressed by this migration, since combining EDA + pipeline steps into one notebook makes previously-invisible full-dataset-vs-train-only decisions visible inline.

## Context

- **Why this migration, in Brian's words**: the EDA notebook should not be a separate, read-only diagnostic step that gets hand-copied into pipeline constants — it should be part of the same flow that imputes/transforms/engineers the data, so that decisions like log-transform, MIN_PERIODS, split boundaries are applied in the same place they're derived, not copy-pasted across files. Brian explicitly rejected the "EDA as report, pipeline reads report" architecture and the "keep .py scripts separate, notebook just calls their functions" middle-ground — he wants one notebook containing all steps' actual logic.
- **What "combining" means concretely**: each step's core computational logic (not its CLI/argparse/file-I/O wrapper) gets transferred into a new notebook section (markdown header + code cells), with data passed as in-memory variables between sections instead of parquet round-trips. Each section's stats/outputs/plots display inline.
- **What must NOT change**: `_shared_modules/engineer_features.py` (used by Step 4) stays a real, imported shared module — never inlined/duplicated into the notebook. Danskvand/Energidrikke/RTD's own pipelines import this same module; duplicating it here would recreate exactly the kind of drift risk (stale copies of the same logic) that P0027 and P0029 both had to spend real effort untangling.
- **Explicitly out of scope for this migration**: `preprocessing_csd.py` (the orchestrator) and its `--run-step`/`--grain` CLI mechanics. Whether/how the notebook eventually replaces or coexists with the orchestrator is a decision to make later (flagged explicitly in Task 7), not something to decide unilaterally mid-migration.
- **Verification discipline**: Brian verifies each step's transfer before the next one starts. Every task's "how to verify" step compares the notebook's in-memory result against the equivalent original `.py` script's file output (row counts, brand counts, key statistics) — this is not a rewrite-and-hope migration, it's transfer-and-diff at every stage.
- **Working notebook location**: `02_thesis_data/_02_preprocessing/nielsen/CSD/pipeline_step_scripts/pre_processing_notebook_csd.py.ipynb` (48 cells as of creation, copied from the fixed `pre_csd_1.5_eda.ipynb`).
- **Original step scripts** (all in the same folder): `pre_csd_0_cache.py`, `pre_csd_1_load_and_aggregate.py`, `pre_csd_2_build_calendar.py`, `pre_csd_3_filter_series.py`, `pre_csd_4_engineer_features.py`, `pre_csd_5_apply_split.py`, `pre_csd_6_save_outputs.py` — these remain on disk, untouched, throughout this migration (nothing is deleted until Brian confirms the notebook is a validated replacement).

## Tasks (persisted to `tasks/`)

| ID | Title | Phase | Blocked By | Status |
|----|-------|-------|-----------|--------|
| 1 | Transfer Step 0 (cache validation) into combined notebook | core | — | complete |
| 2 | Replace EDA's Step-1-output read with real Step 1 (load/aggregate) logic | core | 1 | complete |
| 3 | Transfer Step 2 (build calendar) into combined notebook | core | 2 | complete |
| 4 | Transfer Step 3 (filter series) into combined notebook | core | 3 | complete |
| 5 | Transfer Step 4 (engineer features) into combined notebook, preserving shared module import | core | 4 | complete |
| 6 | Transfer Step 5 (apply split) into combined notebook | core | 5 | complete |
| 7 | Transfer Step 6 (save outputs) into combined notebook | integration | 6 | complete |
| 8 | End-to-end validation of combined notebook against original 7-script pipeline | testing | 7 | complete |

Full task descriptions (what to do, exact file/line references, verification steps) are in `tasks/1.json` through `tasks/8.json`.

**Sequential, not parallel**: each task's blockedBy chain is linear (1→2→3→4→5→6→7→8) because each step's in-memory dataframe depends on the previous step's output — this mirrors the pipeline's own inherent sequential dependency (Step 2 can't run without Step 1's df, etc.), not an artificial constraint. Brian reviews/verifies after each task before starting the next.

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| One combined notebook, not per-step notebooks or notebook-calls-py-functions hybrid | Brian's explicit choice after weighing tradeoffs (git-diffability, reuse-across-categories, checkpointing) — he judged those concerns non-blocking for his and his colleague's review/audit workflow priority |
| `_shared_modules/engineer_features.py` stays imported, not inlined | Danskvand/Energidrikke/RTD depend on the same shared module; inlining would fork the logic and reintroduce the exact staleness/drift problem this migration and P0027/P0029 both fought |
| Orchestrator (`preprocessing_csd.py`) migration/replacement is explicitly deferred | Bigger decision requiring its own scoping; not to be decided as a side-effect of this migration |
| Transfer-and-verify per step, not bulk-transfer-then-test-once | Brian explicitly wants to verify correctness after each step |
| Original `.py` scripts stay on disk untouched during migration | Nothing is deleted/deprecated until the notebook is validated end-to-end (Task 8) |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| Broken multi-line f-string (`print(f"\n{...}")`) landing as a literal newline mid-source during cell authoring, causing `SyntaxError: unterminated f-string literal` | Recurred 3x across Tasks 1-2 (heredoc/bash escaping artifact, not a real notebook logic bug) | Replaced pattern with `print(); print(f"...")` everywhere; verify every new/edited cell via `compile(src, ..., "exec")` before considering it done |
| Stray `df = pd.read_parquet(INPUT_AGGREGATE)` in EDA Cell 3.01, clobbering the in-memory `df` Steps 1-2 had just produced | Brian hit `FileNotFoundError` running the notebook live | Removed the read; confirmed no other EDA cell (3.02-3.19) has a similar re-read |
| `_shared_modules` never added to the notebook's `sys.path`, so `from engineer_features import ...` failed in Step 4.2 | Standalone verification run hit `ModuleNotFoundError: No module named 'engineer_features'` | Added `sys.path.insert(0, ... / "_shared_modules")` to the PROJECT INITIALIZATION cell (cell 6), alongside the existing `ROOT_DIR` insert |
| Step 4.3's own `np.log()` override silently clobbered the shared module's leakage-safe `log_sales_units` (log1p) column, producing NaN on zero-sales rows | Found during EDA-actioning review (log-transform gate, zero-sales characterisation) | Deleted the override; added `TARGET_FOR_MODEL = "log_sales_units" if log_necessary else "sales_units"` gated per-category on that category's own ADF/skewness result |
| `plt.show()` opened a blocking OS window requiring manual close per plot (7 plotting cells), since no matplotlib backend was set | Brian reported needing to close each plot window for the script to continue | Cell 4 now calls `get_ipython().run_line_magic("matplotlib","inline")` in a Jupyter kernel, falling back to `matplotlib.use("Agg")` (`NameError` catch) in a plain-script context |
| Mid-session save collision: notebook was open in Jupyter/IDE while I was editing the same file via script; an IDE/Jupyter save overwrote 3 in-progress fixes (zero-run flag, TARGET_FOR_MODEL, matplotlib-inline) between edits, though the structural-break-scan fix survived | Detected via file mtime (17:26 write when I hadn't just written) plus content check (`zero_run_flag` missing from the on-disk JSON) | Asked Brian to close the notebook tab before continuing; reapplied all 3 fixes cleanly from source once confirmed closed, re-verified end-to-end (exit 0, 30 output columns) |
