---
pid: P0033
created: 2026-08-01 00:00:00
updated: 2026-08-01 00:00:00
---

# P0033 — Findings

## Pre-existing (verified 2026-08-01)

### F1 — CSD is a notebook, the other three are still step scripts

Confirmed by glob over `02_thesis_data/_02_preprocessing/nielsen/`. CSD's step scripts
were archived 2026-07-13 into
`CSD/pipeline_step_scripts/.archive/2026_07_13-16_02 - Previous Modularized Step Scripts/`
and replaced by `pre_processing_notebook_csd.ipynb`. Danskvand/Energidrikke/RTD retain the
flat `pre_{cat}_0..6.py` layout.

This is the structural gap that "mirror CSD to the other three" actually means.

### F2 — PATHS.py already tolerates both layouts

`get_category_preprocessing_scripts_dir()` probes for a `pipeline_step_scripts/` subfolder
and falls back to the flat directory. No PATHS change is needed to support the mixed state
mid-migration, nor after it completes.

### F3 — promo-zero categories

danskvand and RTD are promo-zero (per Enrico's V3 note). They are unaffected by the
`promo_intensity` leakage fix in P0032, so their runs are not order-sensitive.
Energidrikke *is* affected.

### F4 — EDA enrichment candidates deliberately deferred

`_notes/eda-improvement-candidates.md` (Brian, 2026-06-30) lists 6 candidates. A Zotero
query recorded in that same doc found **0 of the 6 key references present** in the library.
Implementing them now would require a citation-gathering detour. Deferred by decision —
mirror first.

---

## Per-category deltas discovered during execution

<!-- record any parameter that legitimately differs from CSD, and why:
     MIN_PERIODS feasibility, period counts, promo-zero handling, brand counts -->

## Discovered during execution

<!-- append below -->
