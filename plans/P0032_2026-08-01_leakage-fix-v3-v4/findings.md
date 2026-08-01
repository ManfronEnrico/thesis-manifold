---
pid: P0032
created: 2026-08-01 00:00:00
updated: 2026-08-01 00:00:00
---

# P0032 — Findings

## Pre-existing (verified 2026-08-01, before any edit)

### F1 — V3 leakage is live, not just archived

Enrico's review cited `build_feature_matrix.py:237` and `build_feature_matrix_bychain.py:179`.
Both files live only under `.archive/enrico_legacy_preprocessing_2026-07/` (archived in commit
`4808670`) and are referenced by nothing outside `.archive/`, harness docs, and old plan files.

The live occurrence is `_shared_modules/engineer_features.py:317-321`. **This file is the only
one that needs the fix** — correcting an earlier assumption that the fix had to land in two
builders plus the shared module.

### F2 — the two feature builders are both dead

- `build_feature_matrix.py` — 330 lines, brand×month
- `build_feature_matrix_bychain.py` — 264 lines, brand×chain

They existed to serve two grains. DEC-GRAIN (2026-07-12) fixed the grain to brand×month, so
the `bychain` variant is doubly obsolete. Neither needs V3/V4 applied.

### F3 — consumer blast radius

`promo_intensity` appears in FEATURES lists across ~15 live scripts under
`03_thesis_modelling/` and `utility_scripts/`. These consume the column from the feature
matrix; they do not recompute it. Fixing the producer should be sufficient — but task 2
verifies no script recomputes it independently.

### F4 — the P0027 groupby leakage bug appears already fixed

P0027 found `engineer_features.py` grouped by `brand` only, conflating lag/rolling features
across regions on a multi-region grain. Verified 2026-08-01: `group_keys` is now threaded
through `make_calendar` (:192), `filter_series` (:248), `engineer_features` (:269),
`apply_split` (:348) and the pipeline class (:401), defaulting to `["brand"]`. Docstrings
explicitly warn about grouping by `"brand"` alone on a multi-region grain.

Task 9 re-confirms before task 4 touches the file. Recorded so nobody re-investigates.

Note: this fix is what made the chain grain *correct* — and DEC-GRAIN then dropped the
chain grain anyway (see P0035).

### F5 — hard-coded numbers downstream

Chapters 6, 8, 9, 10 carry hard-coded WMAPE figures that this fix will move. Full inventory
lives in P0034; not repeated here.

---

## Discovered during execution

<!-- append below -->
