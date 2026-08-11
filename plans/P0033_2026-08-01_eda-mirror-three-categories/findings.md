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

### F5 — RTD HAS NO DATA. This is a hard blocker, not a delta.

Probed 2026-08-01 directly from the parquet cache:

| Category | facts rows | periods | DVH regions | promo column |
|----------|-----------:|--------:|-------------|--------------|
| CSD          | 9,080,538 | 44 | 9/9 | present, 1,297,265 non-zero |
| Danskvand    | 1,248,913 | 37 | 9/9 | **column absent** |
| Energidrikke | 3,112,010 | 41 | 9/9 | present, 568,515 non-zero |
| **RTD**      | **0**     | 37 | 9/9 | **column absent** |

`rtd_clean_facts_v.parquet` is 636 bytes — schema, zero rows. The dimension
tables are fine (product 46 KB, market, period all populated), so this is not a
corrupt conversion: **the source `rtd_clean_facts_v.jsonl` is itself 0 bytes /
0 lines**, while CSD's is 11 GB, Energidrikke's 3.4 GB, Danskvand's 600 MB.

The RTD fact extract was never pulled from the warehouse. No notebook can be run
for RTD until it is. Re-extraction is a warehouse job (Enrico's side per the
handover), not something this plan can resolve.

**Consequence for P0033's scope: it is 2 categories, not 3.** Danskvand and
Energidrikke can be completed now; RTD is blocked upstream. This should be raised
with Brian/Enrico immediately — it also affects P0034, which currently plans to
report an RTD WMAPE figure (31.0%) that no current data can reproduce.

### F6 — `sales_units_any_promo` is absent from danskvand and RTD, not merely zero

P0033's F3 and Enrico's V3 note both describe danskvand/RTD as "promo-zero". The
stronger fact: the column **does not exist** in their facts tables.

CSD's Step 2 `agg_dict` references `"sales_units_any_promo"` unconditionally, so a
naive copy raises `KeyError` on danskvand rather than producing zeros. The mirrored
notebook must guard the aggregation and skip the promo-dependent EDA cell (Step
3.17, promo intensity distribution) when the column is missing.

Silver lining: with no promo column, danskvand cannot carry the V3
`promo_intensity` leakage at all — confirming F3's conclusion that danskvand is
not order-sensitive w.r.t. P0032, and strengthening it (structurally immune, not
just numerically unaffected).

### F7 — period counts differ, so MIN_PERIODS=40 does NOT transfer

CSD's `min_periods: 40` was derived as the "High data-quality tier" entry point
against **44 available months**. Available months per category:

- CSD 44 · Energidrikke 41 · Danskvand 37 · RTD 37

Copying 40 to danskvand would demand 40 non-zero months out of 37 possible —
**mathematically unsatisfiable, filtering every series to zero**. Energidrikke at
41 months would leave a 1-month margin, almost certainly over-filtering too.

MIN_PERIODS must be **re-derived per category** from that category's own EDA Step
3.06 brand-stability analysis, using CSD's *method* (the >~80% non-zero-month
tier boundary) rather than its *number*. This is exactly the "EDA-derived, not
hard-coded" discipline the CSD notebook already implements — the mirror must
preserve the derivation, not the constant.

### F8 — the notebook is already category-parameterized; the mirror is mostly mechanical

Only ~8 genuine code changes exist; every other `CSD` hit is a comment or a plot
title. Verified against the live notebook:

| Cell | Line | Change |
|------|------|--------|
| 8 | `CATEGORY = "CSD"` | → category name (drives all PATHS lookups) |
| 8 | `OUTPUT_FINDINGS`, `OUTPUT_PLOTS_DIR` | `"csd_eda_*"` → f-string on `CATEGORY.lower()` |
| 12 | 4× `pd.read_parquet(... "csd_clean_*_v.parquet")` | → f-string; **filenames follow `{category.lower()}_clean_*_v.parquet` exactly for all four categories — verified on disk**, no special-casing needed |
| 14 | `agg_dict` | guard `sales_units_any_promo` (F6) |
| 14 | `GRAIN_CONFIG["bymonth"]["min_periods"]` | re-derive per category (F7) |
| 25 | `csd_monthly_values` | local variable, rename only |
| 51 | `plt.suptitle('CSD Sales Metrics…')` | → f-string |

`DVH_REGION_IDS` (cell 12) **transfers unchanged** — all 9 region IDs are present
in all four categories' market dimensions. No per-category region mapping needed.

Cells 56/58/60/62/64 (Step 4) need **no changes at all**: they already consume
`CATEGORY`, `GRAIN_CONFIG`, and the live EDA variables (`LAGS`,
`ROLLING_WINDOWS`, `holiday_months`, `train_end_*`, `log_necessary`) in-memory.

### F9 — cell 64 imports a grain function P0035 is removing

`get_category_engineered_bychain_dir` is imported and placed in
`ENGINEERED_DIR_FOR_GRAIN`. Since `GRAIN = "bymonth"` it is never called, but
P0035 deletes that PATHS function — which would break this import at load time in
all four notebooks.

Coordination point: the mirrored notebooks should drop the `bychain` entry and
import only `get_category_engineered_bymonth_dir`. Cheap to do now, avoids a
cross-plan break later.

## Discovered during execution

### F10 — the parquet data is gitignored and exists ONLY in the main repo

The worktree at `worktrees/p0033-eda-mirror/` has no
`02_thesis_data/_01_converted/nielsen/parquet_nielsen/` directory at all —
the whole data tree is gitignored, so `git worktree add` never materialised it.
`PATHS.THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR` resolves relative to whichever
`CLAUDE.md`-bearing root the notebook's Step 0.2 walk-up finds, which inside the
worktree is the worktree — a path that does not exist.

**Consequence:** notebooks authored in the worktree cannot be *executed* there.
Derivation for this session was done by reading the main repo's parquet cache
read-only from a temp script. Full end-to-end notebook runs must happen from the
main repo after this branch merges. This is a property of the worktree workflow
vs. gitignored data, not a defect in the notebooks.

### F11 — CORRECTION to F5/F7: Energidrikke has 39 usable months, not 41

F7 listed available months as "CSD 44 · Energidrikke 41 · Danskvand 37".
Re-derived 2026-08-01 by replicating the notebook's own Step 1 + Step 2
(DVH-region filter + `sales_units > 0` filter + brand×month aggregation):

| Category | facts rows | rows after filter | brands | date range | total_months | promo col |
|----------|-----------:|------------------:|-------:|------------|-------------:|-----------|
| CSD          | 9,080,538 | 243,691 | 140 | 2022-10 .. 2026-05 | **44** | present |
| Energidrikke | 3,112,010 |  75,872 |  64 | 2023-01 .. 2026-03 | **39** | present |
| Danskvand    | 1,248,913 |  64,533 |  49 | 2023-03 .. 2026-03 | **37** | **absent** |

The CSD row reproduces the notebook's documented numbers exactly (140 brands,
44 months, 58 brands at min_periods=40 = 41.4%), which validates that this
replication is faithful and therefore that the Energidrikke correction is real.
F7's "41" was measured before the region/positive-sales filters.

### F12 — MIN_PERIODS re-derived per category (Danskvand 34, Energidrikke 35)

CSD's `min_periods = 40` is **0.909 of its 44 available months** — the entry
into its "High data-quality tier". F7 mandated preserving CSD's *method*, not
its constant. Two readings of "the method" were computed:

- **Ratio-equivalent** (same fraction of available months as CSD's 40/44)
- **High-tier entry point** (the `>35/44 = 0.795` tier boundary generalised)

| Category | months | ratio-equiv (0.909) | brands kept | % kept | High-tier entry | **chosen** |
|----------|-------:|--------------------:|------------:|-------:|----------------:|-----------:|
| CSD          | 44 | **40** | 58 | 41.4% | 36 | 40 (unchanged) |
| Energidrikke | 39 | **35** | 23 | 35.9% | 32 | **35** |
| Danskvand    | 37 | **34** | 24 | 49.0% | 30 | **34** |

**Chosen: the ratio-equivalent**, because that is the reading under which CSD's
own published constant (40) is reproduced exactly — the High-tier-entry reading
would have re-derived CSD as 36, contradicting the locked CSD value. Choosing
the reading that is self-consistent on CSD is the only way the three categories
are actually comparable for Ch4.

Both chosen values sit on a **stable plateau** rather than a cliff, which is
what makes them defensible:

- Danskvand: 30→35 all retain 24 brands; 34 is inside that flat region.
- Energidrikke: 33→35 all retain 23 brands; 35 is the top of that flat region.

Retention rates (49.0% / 35.9%) bracket CSD's 41.4%, so no category is being
filtered anomalously hard or soft relative to the template.

### F13 — F6 confirmed and scoped precisely

`sales_units_any_promo` is confirmed **absent from Danskvand's facts schema**
(15 columns, no promo family at all) and **present in Energidrikke's** (32
columns, full promo family incl. `baseline_sales_*`). So:

- **Danskvand**: cell 14 `agg_dict` must omit the promo aggregation; the
  aggregated frame has 7 columns and no `promo_units`. EDA Step 3.17 (promo
  intensity) is skipped. Step 3.12's promo-spread block and Step 3.18's
  correlation list already guard on column presence and need no change.
- **Energidrikke**: promo present, behaves exactly like CSD. It remains the one
  category order-sensitive w.r.t. P0032.

### F14 — RTD re-confirmed as hard-blocked, and dropped from this plan's scope

Re-verified: `rtd_clean_facts_v.parquet` is 636 bytes / 0 rows because the
source JSONL is 0 bytes. No notebook was created for RTD — creating one would
produce a file that cannot run and would misrepresent the category as ready.
**P0033 delivers 2 notebooks, not 3.** Task 5 is marked `blocked`, not
`completed`. Unblocking requires Enrico re-pulling the RTD fact extract from
the warehouse.

### F15 — both notebooks verified structurally; residual `csd` strings are benign

Verification was run separately after the authoring session hit its limit
(it had been announced but not executed). Results:

| Check | Danskvand | Energidrikke | CSD (control) |
|-------|-----------|--------------|---------------|
| Valid JSON / nbformat | 4.5 | 4.5 | 4.5 |
| Cells (total / code / md) | 65 / 31 / 34 | 65 / 31 / 34 | 65 / 31 / 34 |
| Code cells compile (`ast.parse`, magics stubbed) | 0 errors | 0 errors | 0 errors |

Exact cell-count parity across all three is the property Ch4 comparability
depends on — the mirror is cell-for-cell aligned with the template.

Every per-category delta was confirmed present on disk, not merely intended:

| Delta | Danskvand | Energidrikke |
|-------|-----------|--------------|
| `CATEGORY` (cell 8) | `"Danskvand"` | `"Energidrikke"` |
| `OUTPUT_FINDINGS` / `OUTPUT_PLOTS_DIR` | f-string on `CATEGORY.lower()` | same |
| 4× `read_parquet` (cell 12) | f-string on `CATEGORY.lower()` | same |
| `min_periods` (cell 14) | **34** | **35** |
| promo aggregation (cell 14) | **omitted** (F13) | present, as CSD |
| `bychain` import (cell 64, F9) | dropped; `bymonth` only | dropped; `bymonth` only |

**Residual `csd` occurrences are not leakage.** 15 unique lines in Danskvand,
13 in Energidrikke — all are deliberate provenance comments (e.g. "CSD's 40 is
0.909 of its 44…", which documents the F12 derivation and is worth keeping),
plus one local variable `csd_monthly_values` in cell 25 that is assigned and
consumed inside that same cell. No functional path depends on the string.
Optional cosmetic rename; not a correctness issue.
