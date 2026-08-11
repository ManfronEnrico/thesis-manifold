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

### F6 — V3 and V4 applied and execution-verified

`_shared_modules/engineer_features.py` in worktree
`worktrees/p0032-leakage-fix-v3-v4` (branch `cc/20260801-1630/p0032-leakage-fix-v3-v4`):

- **V3** at `:353-380` — `promo_intensity` computed then `.groupby(group_keys).shift(1)`.
  Verified by execution: correct one-period shift, first observation per series
  NaN, no cross-series bleed, `[0, 1]` preserved, multi-key grain honoured.
- **V4a** at `:183-193` — CSV path raises on `len(target_market_ids) > 1`.
- **V4b** at `:77-101` — DB path pre-flight id count. Beyond the plan's literal
  scope but justified: that SQL filters a *joined* `dim_market`, so a duplicate
  description fans out the JOIN and every `SUM()` double-counts.

Uncommitted. Nothing pushed.

### F7 — correction to F4

F4 states `group_keys` is threaded through `apply_split (:348)`. **It is not** —
`apply_split` takes no `group_keys` and does not need any. The remaining call
sites are correct: `make_calendar (:190)`, `filter_series (:244)`,
`engineer_features (:263)`, `build_series_index (:346)`, `FeatureEngineer` (:401).

The P0027 groupby fix is otherwise confirmed still in place (task 9 done).

### F8 — decisions recorded

1. **V3 shape** — `.shift(1)`, not drop. Keeps a lagged promo signal without
   leaking `sales_units_t`; consistent with every neighbouring lag/rolling feature.
2. **`weighted_distribution`** — kept contemporaneous. Rationale: distribution
   coverage is plausibly known in advance; a promo ratio from realised sales is
   not. **Weakest link in the plan**: its target correlation (0.756) exceeds
   `lag_1`'s (0.585), which is odd for a truly exogenous variable. Recommend a
   Ch6 sensitivity check (with/without) before this is defended in prose.

### F9 — unrelated issue found in the same module

`make_calendar:232-235` uses `bfill`, pulling future values backwards across gap
months. Out of P0032 scope; worth its own ticket.

### F10 — the plan's central premise fails: promo is all-zero

**`promo_intensity` is identically zero across all 2552 CSD rows.** Independently
verified: `promo_units` nonzero count = 0, max = 0.0.

The leakage was real in code but carried **no signal**. The expected "WMAPE gets
worse once the leak is closed" outcome therefore cannot occur, and the honest
before/after answer is *no change*. This is the reason tasks 1, 6 and 7 are blocked.

#### F10.1 — the defect is upstream, in market selection

The fact table has 9,080,538 rows, of which 2,212,600 carry non-null
`sales_units_any_promo`. The 9 hard-coded `DVH_REGION_IDS` cover 1,334,969 rows
and **0** of them have non-null promo.

Exactly 22 markets in the data carry promo — **all of them rollups or chains**,
none of them geographic regions. The second-largest is `DVH EXCL. HD`, id
**1256338** — precisely the id the region list was constructed to avoid, because
including it alongside the regions caused the 6.16× double-count that P0027 fixed.

#### F10.2 — why it happened

Structural Nielsen panel design: promo is reported at rollup/chain level, not at
geographic-region level. The region-based grain chosen to eliminate double-counting
also eliminates every promo observation.

The pipeline consequently ships **three structurally dead columns**, and the EDA
report does not flag them as empty. That silent failure is itself worth fixing.

Root of the choice: cell 12 (STEP 1) of
`02_thesis_data/_02_preprocessing/nielsen/CSD/pipeline_step_scripts/pre_processing_notebook_csd.ipynb`,
which hard-codes the 9 region ids.

#### F10.3 — the national rollup is a viable substitute

Measured directly:

| Quantity | Value |
|----------|-------|
| National total (`1256338`) | 2.6974e10 |
| Regions summed | 2.6656e10 |
| **Ratio** | **1.0119** (1.2% gap — not 6.16×) |
| Brand-months at that grain | 3,917 |
| Panel shape | 140 brands × 44 months |
| `promo_intensity` nonzero | **70.8%** |
| mean / median | 0.3012 / 0.2584 |

So the national rollup restores a real promo signal at a 1.2% cost in total
volume, versus the 6.16× error that motivated the region list in the first place.

#### F10.4 — what this does *not* settle

- Switching grain is a **thesis-level decision**, not a bug fix. It changes the
  unit of analysis for SRQ1 and must be defended in Ch3/Ch6.
- The 1.2% gap needs an explanation before it appears in prose.
- The other three categories (Danskvand, Energidrikke, RTD) were **not** checked
  for the same defect.
- **Deliberately not implemented in this session.** Awaiting user decision.

#### F10.5 — recommendation

Adopt the national rollup as a **separate, explicitly-scoped plan**, in this order:

1. Confirm the same promo-absence defect in the other three categories.
2. Explain the 1.2% national-vs-summed-regions gap.
3. Switch the CSD grain to market `1256338` and regenerate the feature matrix.
4. Re-run SRQ1 and record before/after — which then also unblocks P0032 tasks 6-7.

### F11 — the SRQ1 baseline is stale and unreproducible

`04_thesis_results/srq1/metrics.csv` (dated Jul 13, CSD-only, 4 models) cannot be
reproduced by the current benchmark script:

| Mismatch | `metrics.csv` / benchmark expects | Current feature matrix has |
|----------|-----------------------------------|----------------------------|
| Split sizes | 692 / 752 | 1450 / 348 / 754 |
| Rolling features | `rolling_mean_4`, `rolling_std_4`, `rolling_mean_13` | `rolling_mean_2/3/8/12`, no `rolling_std_*` |

`03_thesis_modelling/model_training/srq1_benchmark.py:52-55` requests the missing
columns; running it raises `KeyError` — confirmed by execution.

**Consequence:** any before/after delta computed against this file would measure
pipeline drift, not the leakage fix. Task 1 is blocked until the baseline is
regenerated.

This also blocks P0034 (which consumes these numbers). Per user instruction
2026-08-06, **P0034 is paused and is being handled in a separate session** — no
P0034 files were touched here.

---

## 2026-08-11 session — F10 corrected

### F12 — F10's premise was wrong: promo is present at DVH EXCL. HD, absent only at the region children

F10 concluded "promo is structurally absent" and F10.5 framed adopting the national
rollup as a **thesis-level grain decision**. Both were overstated. Measured directly
against `_01_converted/nielsen/parquet_nielsen/CSD/views/csd_clean_facts_v.parquet`
(9,080,538 fact rows; promo column `sales_value_any_promo`):

| Scope | Rows | Non-null promo | Nonzero promo |
|-------|------|----------------|---------------|
| **Parent `1256338`** (DVH EXCL. HD) | 196,657 | 182,467 | **119,010** |
| **9 region children** (live notebook filter) | 453,685 | **0** | **0** |

Parent covers 44 periods; max promo value 308,302,433.53.

**Promo-zero is an artifact of the market filter, not a property of the data.**
Switching to the parent recovers a well-populated feature.

### F12.1 — consequence for P0032's own conclusion

P0032 stalled because the V3 leakage fix could produce no measurable before/after
delta on an all-zero column. That reasoning holds *only at region scope*. At parent
scope `promo_intensity` carries real signal, so the V3 fix becomes measurable and
material. **The V3/V4 fixes remain correct and should be committed** (currently
uncommitted in worktree `p0032-leakage-fix-v3-v4`).

Corollary: the earlier suggestion to drop `promo_units` / `promo_intensity` as
"structurally dead columns" (F10.2) must **not** be actioned — it would discard a
real feature to accommodate a filter bug.

### F12.2 — this is a scope choice, not a grain choice

DEC-GRAIN (brand×month) is untouched by this. Market scope and aggregation grain are
independent axes; both parent-only and children-only yield brand×month. The parent is
one pre-aggregated market row per brand×month; the children are nine geographic slices
of the same universe. Summing them double-counts — hence one or the other, never both.

### F12.3 — P0026 chose the children deliberately; this reverses that on supplier grounds

Not pure drift. `P0026/task_plan.md:42` and `findings.md:20` explicitly exclude the
"national DVH EXCL. HD total" as a double-count risk, selecting the 9 regions to
maximize rows (2.3k → 25.1k). That reasoning is valid for *summing* markets but does
not follow for *choosing* one.

Reversed 2026-08-11 (Brian) on the supplier's own metadata:
`02_thesis_data/_00_raw/nielsen/description/nielsen-prometheus_data_model.md:69` —
*"Unless the user specifies a particular market, always use **DVH EXCL. HD**
(Dagligvarehandel excluding hard discount) as the default."*
Enrico's archived builder already used it (`build_feature_matrix.py:92`,
`MARKET_SCOPE = "DVH EXCL. HD"`), as does P0024 (complete, "fix DVH EXCL. HD market
filter across all 5 pipelines").

Note on series length: regions do **not** lengthen any series — same ~44 periods either
way. They multiply rows by decomposing a brand-month into nine geographic parts, a
decomposition DEC-GRAIN already declines to model.

### F12.4 — "HD" means hard discount (a retail channel), not discounting/promotions

Settled — it had been a plausible explanation for the zeros. Confirmed by
`nielsen-prometheus_data_model.md:69`, `build_feature_matrix.py:24`
("excluding **hard discount**"), and the market list itself, which contains sibling
channel definitions `DVH EXCL. LIDL`, `DVH EXCL. DISCOUNT/HD`, and a `DISCOUNT` market
that carries promo. Excluding hard-discount *stores* never implied excluding
promotional *selling* in the stores that remain.

### F12.5 — live location of the defect

`02_thesis_data/_02_preprocessing/nielsen/CSD/pipeline_step_scripts/pre_processing_notebook_csd.ipynb`
- `:426` — `DVH_REGION_IDS = { ... }` (9 region ids)
- `:457` — `merged = merged[merged["market_id"].isin(DVH_REGION_IDS)].copy()`
- `:725` — `"region_ids": DVH_REGION_IDS` (carried into the findings artifact)

Must be fixed **before** P0033 mirrors the notebook, or all four categories inherit
the all-zero promo columns.
