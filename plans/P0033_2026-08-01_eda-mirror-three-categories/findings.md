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

## 2026-08-11 session

### F5 — BLOCKING: CSD's market filter must be fixed before mirroring

The CSD notebook filters to **9 region children** of DVH EXCL. HD rather than the
single parent market `1256338`. Measured consequence: **zero** promo observations at
region scope vs **119,010 nonzero** at parent scope. Full evidence in P0032 `findings.md`
F12–F12.5.

Brian decided 2026-08-11: **use the parent (`DVH EXCL. HD`, id `1256338`)**, per the
supplier metadata that names it the default market
(`02_thesis_data/_00_raw/nielsen/description/nielsen-prometheus_data_model.md:69`).

**Why this blocks P0033:** the plan mirrors CSD's notebook structure to three categories.
Mirroring the current notebook propagates the region filter and its all-zero promo columns
to all four. Fix CSD first, mirror second — per Brian: *"Let us fix any issues that are
necessary to the CSD EDA before we copy it over and waste time."*

Fix location: `pre_processing_notebook_csd.ipynb:426` (`DVH_REGION_IDS`), `:457` (the
`isin` filter), `:725` (findings artifact).

### F6 — F3 above is unreliable, and is superseded

F3 recorded danskvand and RTD as "promo-zero" from Enrico's V3 note. Since CSD's
promo-zero turned out to be a filter artifact rather than a data property, the same
likely applies to any category whose pipeline filters to region children. Do **not**
rely on F3 when building the three notebooks — re-derive promo presence per category
at parent scope.

### F7 — pre-existing filter state of the other three is moot

Whether Danskvand/Energidrikke/RTD currently filter on the single market or on regions
does not need checking (Brian, 2026-08-11): they are being rebuilt from the corrected
CSD template and will inherit its filter regardless. Recorded only so a future session
does not re-open the question.

### F8 — open question gating the scope switch

Parent scope has 196,657 CSD fact rows over 44 periods; the current region-scope pipeline
yields ~2,300 rows in the final feature matrix. How many brands survive `MIN_PERIODS` at
parent scope is **not yet measured** — that determines whether the scope switch is free or
trades forecastable series for the promo feature. Series *length* (~44 periods) is
identical at both scopes.

Also flagged for the same investigation (Brian, 2026-08-11): whether the 196k → ~2k
reduction through grouping + MIN_PERIODS is itself justified, and whether the resulting
matrix is adequate to train the chosen ML and statistical models.

### F9 — F8 resolved: parent scope dominates children at brand×month (measured 2026-08-11)

| Metric | Parent `1256338` | Region children |
|--------|------------------|-----------------|
| Fact rows | 196,657 | 453,685 |
| Distinct brands | **144** | 136 |
| Distinct periods | 44 | 44 |
| Brand-month rows (>0) | **3,917** | 3,641 |
| Brands @ MIN_PERIODS>=24 | **85** | 74 |
| Rows @ MIN_PERIODS>=24 | **3,392** | 3,038 |
| Nonzero promo | **119,010** | 0 |

**No trade-off exists.** The parent yields more rows, more brands and the promo feature.
The earlier concern that parent scope costs row count was wrong — it conflated fact-row
count with post-aggregation feature-matrix rows.

Region children have more *fact* rows but fewer *brand-month* rows: geographic splitting
fragments each brand-month into thin slices that then individually fail MIN_PERIODS.
P0026's "10.6x more data" (2.3k -> 25.1k) counted the same brand-months nine times.

### F10 — the 196k -> 2,552 funnel is arithmetic, not attrition

Measured from `pipeline_step_outputs/`:

| Stage | Rows | Brands |
|-------|------|--------|
| Facts @ DVH EXCL. HD | 196,657 | — |
| step_1_aggregate_bymonth | 3,975 | 140 |
| step_2_calendar_filled | 6,160 | 140 |
| step_3_filtered_series | 2,552 | 58 |
| step_4/5 + final matrix | 2,552 | 58 |

The large drop is the **product→brand rollup** (SKU-level facts collapsed to brand×month).
144 brands × 44 periods caps at ~6,336 cells — the reduction is definitional, and is
exactly what DEC-GRAIN specifies. Not a data-loss defect.

**One genuine concern:** MIN_PERIODS culls 140 -> 58 brands (59%). At parent scope with
MIN_PERIODS>=24, 85 brands survive. Worth revisiting the threshold — separate question
from market scope.

### F11 — sample-size adequacy assessment (Brian asked 2026-08-11)

Binding constraint is **44 months per series**, invariant to market scope. Split is
1450/348/754 (~12 test months per brand).

| Model class | Verdict |
|-------------|---------|
| Statistical per-brand (ARIMA/ETS/Prophet) | Thin but defensible. ~3.5 seasonal cycles; 12 seasonal lags on 44 points is tight. Declare as limitation. |
| Classical ML pooled (XGBoost/LightGBM) | Adequate — 2,552 rows × ~30 features. **Must pool across brands**; per-brand collapses. |
| Deep learning from scratch | **Not viable.** Do not attempt. |
| Pre-trained / foundation models (Chronos, TimesFM, Moirai) | Well-suited — zero-shot on short series is their target regime. |

**Assessment:** adequate for the thesis's actual contribution. The RQ is whether
pre-trained models improve predictive results over training from scratch; a low-data
regime is the *condition that makes that question meaningful*, not a defect. A dataset
large enough to train deep models from scratch would weaken the framing. Recommend
stating this explicitly in Ch4 as a deliberate design property.
