# Archived: Enrico's standalone Nielsen preprocessing scripts

**Archived**: 2026-07-12, on branch `chore/archive-colleague-preprocessing`.

Originally at `02_thesis_data/preprocessing/` (colleague's independent implementation of
the brand×month / brand×chain feature pipeline). Superseded by the CSD orchestrator at
`02_thesis_data/_02_preprocessing/nielsen/CSD/` (`preprocessing_csd.py` + numbered
`pre_csd_N_*.py` steps), which is more rigorous (empirical EDA-driven parameter
selection, region-grain scoping, shared feature-engineering module across categories)
and is the pattern being copied to Danskvand/Energidrikke/RTD.

See `plans/P0027_2026-07-10_15-30_csd-eda-reconciliation/findings.md`
("2026-07-12 Session — Colleague Pipeline Comparison + Archive") for the full
side-by-side comparison and what was/wasn't carried forward.

## What was kept / carried forward (not literally, but as design input)

- **Chain-grain scoping approach** (`build_feature_matrix_bychain.py`'s `LEAF_CHAINS`
  list) — informs Phase 4b (add a chain-grain branch to the CSD orchestrator).
- **Global MIN_PERIODS=30-across-all-categories rationale** — reference data point
  for reconciling CSD's own internal MIN_PERIODS discrepancy (Step 3: 24, Step 6: 40).
- **The "hierarchical market double-counting" bug pattern** — already independently
  found and fixed differently in the CSD pipeline (9-region scoping instead of a
  single collapsed market row); useful as a sanity-check reference, not a fix to port.

## What was NOT carried forward

- The scripts themselves reference pre-P0028 paths (`thesis/data/...`) and will not
  run as-is against the current repo tree.
- No EDA/parameter-justification work exists in this tree — the CSD orchestrator's
  `pre_csd_1.5_eda.py` supersedes it entirely.
