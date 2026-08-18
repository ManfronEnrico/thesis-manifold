---
pid: P0036
created: 2026-08-11 16:08:00
updated: 2026-08-18 23:30:00
status: in_progress
focus_detail: "P0038 COMPLETE, unblocking everything here. Task 9 CLOSED (its own measurement refutes the single-brand premise: 3,392 pooled rows vs 44). Task 4 half delivered (has_promo recorded, DEC-NO-PROMO-FILL); the all-zero assertion is still missing and two 2026-08-18 failures would have been caught by it. Tasks 7 and 11 unblocked; 11 still needs defining. See the 2026-08-18 status refresh at the foot of this file."
---

# P0036 — Fix CSD Before Mirroring

> **Gates P0033.** Per Brian 2026-08-11: *"Let us fix any issues that are necessary to
> the CSD EDA before we copy it over and waste time."* Every defect here is in shared
> code or in the notebook P0033 copies three times — fixed once now, or four times later.

## Why this plan exists

P0033 (mirror CSD EDA to three categories) is the top priority and the critical path to
Ch4. But mirroring a defective template multiplies the defects by four. This plan is the
prerequisite: land the fixes, re-run CSD, then let P0033 copy a clean template.

## Decisions locked (Brian, 2026-08-11)

| ID | Decision | Basis |
|----|----------|-------|
| **DEC-SCOPE** | Market scope = **parent `1256338` (DVH EXCL. HD)**, not the 9 region children | Supplier metadata names it the default (`nielsen-prometheus_data_model.md:69`); measured strictly better at brand×month |
| **DEC-GRAIN** | brand×month (unchanged, Enrico 2026-07-12) | Pre-existing; market scope is an independent axis |

DEC-SCOPE reverses P0026's region choice. P0026's reasoning (avoid rollup double-count)
is valid for *summing* markets but does not follow for *choosing* one — parent-only and
children-only both avoid double-counting.

## Evidence base

Full measurements in `findings.md`; originals in P0032 F12–F12.5 and P0033 F5–F11.

> **Corrected 2026-08-11 (task 3, F15).** The figures below are the *measured*
> values. The earlier table claimed parent scope gained rows (3,917 vs 3,641) and
> 119,010 nonzero promo — both wrong. Parent scope **costs** 1.5% of brand-month
> rows. The promo gain is real but per-column ~23,400, not 119,010.

**Parent vs children at brand×month — a trade, not a free win:**

| Metric | Parent `1256338` | Region children |
|--------|------------------|-----------------|
| Brand-month rows (>0) | 3,917 | **3,975** |
| Distinct brands | 140 | 140 |
| Brands @ MIN_PERIODS>=24 | **85** | 84 |
| Fact rows | **37,999** | 243,691 |
| Nonzero promo (per column) | **~23,400** | **0** |

Promo-zero was an artifact of the region filter, not a property of the data — this
is the entire case for DEC-SCOPE. Region scope repeats each brand-period across 9
children (6.41× redundancy) without adding information at the modelling grain.

**Net: costs 1.5% of brand-month rows, buys the entire promo feature family.**

## Phases

| Phase | Goal | Tasks |
|-------|------|-------|
| 1 | Preserve at-risk work | 1, 2 |
| 2 | Market scope fix + verification | 3, 4 |
| 3 | Shared-module correctness fixes | 5 |
| 4 | Re-run + parity check, hand off to P0033 | 6 |
| 5 | Open analyses feeding parameter choices | 7, 8, 9 |

## Tasks

> **Renumbered 2026-08-11 (session 2)** to match the in-session task list. Worktree
> cleanup was split out as its own task after it turned out to carry real risk.

| ID | Title | Phase | Blocked By | Status |
|----|-------|-------|------------|--------|
| 1 | Cherry-pick V3/V4 `engineer_features.py` from the locked worktree | 1 | — | ✅ complete |
| 2 | Preserve + remove four stale worktrees | 1 | 1 | ✅ complete |
| 3 | Switch CSD market filter to parent `1256338` | 2 | — | ✅ complete |
| 4 | Verify promo columns populate; assert non-degenerate | 2 | 3 | **complete** |
| 5 | Fix `make_calendar` bfill future-leakage | 3 | 1 | ✅ complete |
| 6 | Re-run CSD end-to-end + parity check | 5 | 3, 4, 5 | → **moved to P0038 task 8** |
| 7 | Resolve sales_value/sales_liters redundancy (P0031 task 4) | 4 | P0038 t8 | **complete** |
| 8 | Decide MIN_PERIODS threshold | 4 | — | **complete** |
| 9 | Measure single-brand vs pooled training cost | 4 | P0038 t8 | **complete** |
| 11 | Recover product-dimension features as brand-month signals | 4 | P0038 t8 | pending |
| 12 | Per-notebook feature engineering for capability tiers | — | — | → **moved to P0038 task 5** |
| 14 | Decide shared-vs-CSD-specific seam | — | — | → **answered by P0038 DEC-SHARED-SEAM** |
| 15 | Dynamic proportional split cutoffs | — | — | shared module **done**; notebook half → **P0038 task 4** |

> **Handoff to P0038 (2026-08-12).** The parity check that gates P0033 is now
> P0038 task 8, because it must run against the decomposed scripts rather than
> the notebook being dissolved. Tasks 7, 9 and 11 still live here and depend on
> that run. Task 8 (MIN_PERIODS) depends on P0038 task 4, which makes the value
> genuinely derived and surfaces the brand-depth distribution — the *threshold
> choice* remains Brian's and remains this plan's task.

**Tasks 7–9 and 11 are modeling analyses that change no pipeline structure**, so
they deliberately run after mirroring starts rather than holding the critical path.

## Task detail

### Task 1 — Commit P0032's V3/V4 fixes
**At risk.** Fixes are applied but uncommitted in a **locked** worktree
(`worktrees/p0032-leakage-fix-v3-v4`). One power cycle from loss.

V3 = `promo_intensity` target leakage (`sales_units_t` in its own denominator),
`_shared_modules/engineer_features.py:317-321`. V4 = market_id assert.

Both remain correct. P0032 stalled only because promo was all-zero *at region scope* —
under DEC-SCOPE the fix becomes measurable and material (119,010 nonzero promo rows).

### Task 3 — Switch CSD market filter to parent
`pre_processing_notebook_csd.ipynb` — **2 sites remain** (was 3):
- `:423-426` — `DVH_REGION_IDS = { ... }` → single id `1256338`. Also rewrite the
  comment above it, which justifies the region choice on double-count grounds.
- `:457` — `merged[merged["market_id"].isin(DVH_REGION_IDS)]`
- ~~`:725` — `"region_ids": DVH_REGION_IDS` in the `byregion` grain config~~ —
  **already deleted** by the `chore/p0035-grain-artifact-removal` merge (`0f699a7`).
  See progress.md F14. Do not go looking for this line; it no longer exists.

The notebook is **57,814 tokens — too large for Read**. Use Grep to locate sites.

Keep the SCD market-dim dedup on `market_id` before merging (P0027's double-count guard).
Guard `len == 1` after filtering, not just `len > 0` (P0032 task_plan:48 flagged this).

### Task 4 — Verify promo populates
✅ **Partly pre-verified by task 3**: all 7 raw promo columns confirmed non-degenerate
at parent scope (`sales_value_any_promo` 23,406 … `weighted_distribution_any_promo`
23,407; all were 0 at region scope). What remains is the *derived* features and the
reusable assertion.

After task 3, confirm `promo_units` / `promo_intensity` / `has_promo` are non-degenerate.
Add an EDA assertion that **fails loudly on all-zero columns** — the silent pass-through
is the reason this went unnoticed for weeks (P0032 F10.2). Applies to any all-zero
feature, not just promo.

### Task 5 — Fix `make_calendar` bfill
`_shared_modules/engineer_features.py:232-235` uses `bfill`, pulling future values
backward across gap months. Found during P0032, deferred as out of scope. **Shared
module — affects all four categories.** Real leakage, unlike V3's zero-signal case.

### Task 7 — sales_value/sales_liters redundancy
P0031 task 4, imported here because CSD is about to become the template. Both correlate
near-perfectly with `sales_units` (same quantity in different units) — multicollinearity
entering the model silently.

Also re-examine `weighted_dist`: P0032 measured its target correlation at **0.756**,
*above* `lag_1`'s 0.585 — suspicious for a supposedly exogenous variable. Recommend a
fit-with/without sensitivity check.

### Task 8 — Decide MIN_PERIODS ✅ **RESOLVED 2026-08-18 (DEC-MINPERIODS)**

**Decision: `MIN_PERIODS = MAX_LAG + HORIZON + 1 = 15`** — derived from the feature
specification, not chosen.

Brian 2026-08-11 called this *"shaky at best either way"*, and it was, because the question
was being asked in the wrong units.

**The framing error.** The table below (kept for the record, superseded) counted **panel
rows**, not **usable training rows**. A brand-month is only trainable once its lag features
are defined:

    usable_rows(brand) = n_months(brand) - MAX_LAG - HORIZON

At `MAX_LAG = 13, HORIZON = 1` a brand with 14 months yields `14 - 13 - 1 = 0`. It counts
in the panel and contributes nothing to training. Once measured in row terms, the trade-off
the old table implied largely disappears.

**Superseded table** (panel rows, 44-month extract, pre-refresh):

| MIN_PERIODS | Brands | Panel rows |
|-------------|--------|------------|
| >=12 | 109 | 3,744 |
| >=24 | 85 | 3,392 |
| >=30 | 76 | 3,152 |
| >=36 | 67 | 2,865 |

**Correct measurement** (usable training rows, 46-month refreshed extract, CSD, lag-12):

| MIN_PERIODS | Brands | % brands | Training rows | % of max |
|------------:|-------:|---------:|--------------:|---------:|
| 0 | 142 | 100.0% | 2,467 | 100.0% |
| **15** | **106** | **74.6%** | **2,467** | **100.0%** |
| 20 | 89 | 62.7% | 2,429 | 98.5% |
| 30 | 79 | 55.6% | 2,315 | 93.8% |
| 40 | 62 | 43.7% | 1,961 | 79.5% |

Dropping 36 brands at MIN_PERIODS=15 costs **zero** training rows. Holds in all four
categories (100.0% retention each). The old hardcoded 40 cost 20.5% / 16.8% / 40.8% /
30.2% for CSD / Danskvand / Energidrikke / RTD.

**The defensible basis for Ch4** that this task asked for: the threshold is the
minimum-information requirement of the feature specification. Brands below it are excluded
because they *cannot be represented*, not because they were judged uninteresting. The rule
generalises — 9 at lag-6, 6 at lag-3 — so a change to the lag structure carries the
threshold with it and needs no fresh justification.

**Ch10 limitation**: results generalise to brands with >=15 months of continuous presence;
the cold-start case is out of scope by construction.

Full derivation, four-category tables and the rejected lag-3 alternative:
`plans/P0038_.../task_plan.md` (DEC-MINPERIODS), findings F47/F48, and
`05_thesis_writing/notes/sample-size-and-tool-interface-rationale.md` §11.

### Task 9 — Single-brand vs pooled training cost
**Brian's proposal (2026-08-11):** train exclusively on the brand with the most data,
since the System B demo only needs one brand (e.g. Faxe Kondi) for simulated user
questions. Framed as: *"If we can get more data and a better training result with that
approach, then we should probably do that."*

**Measured counter-evidence — the premise does not hold:**

| | Pooled (MIN_PERIODS>=24) | Single best brand |
|---|---|---|
| Training rows | **3,392** | **44** |
| Brands | 85 | 1 |

Selecting the best brand yields **no additional data**. The panel is 44 months deep and
**51 brands already sit at 44/44**, including FAXE KONDI (4th by volume, 118M units, zero
gaps). MIN_PERIODS is a *series-length* filter — discarding brands cannot lengthen the
survivor. Single-brand training is a **77× reduction**, and ~30 features on 44 rows is
more features than observations (unfittable for XGBoost/LightGBM, which need pooling).

Second problem: ~12 test points would give error bars wide enough to swallow any
realistic difference between base LLM / LLM+data / LLM+model — the thesis's core claim.

**Recommended resolution — separate training scope from evaluation scope:**
- **Train** pooled across all surviving brands (global forecasting model, standard practice)
- **Demo and evaluate** on Faxe Kondi

Delivers the intended demo, keeps statistical power, and forecasts the chosen brand
*better* than a single-brand model would. Costs nothing narratively.

**This task is the measurement, not the decision.** Fit both on Faxe Kondi (pooled-then-
predict vs single-brand-only), compare WMAPE. Brian decides on the numbers.

### Task 6 — Re-run + parity check
Full CSD notebook run under DEC-SCOPE. Record before/after: row count, brand count,
promo populated, WMAPE delta from the V3 fix. Confirm `_03_engineered/bymonth/CSD/`
regenerates. **This output becomes P0033's template.**

**Expected at parent scope (measured, F15)** — not the plan's original figures:

| | Value |
|---|---|
| Fact rows (post-filter, sales>0) | **37,999** |
| Brand-month rows (>0) | **3,917** |
| Distinct brands | **140** |
| Brands @ MIN_PERIODS>=24 | **85** |
| Panel depth | **44 months** |

Also rebuild Ch4's funnel narrative, which currently starts from the wrong 196,657
figure (see `05_thesis_writing/notes/sample-size-and-tool-interface-rationale.md`).

## Definition of done

- V3/V4 committed, off the locked worktree
- CSD filters to `1256338`; promo columns populated and asserted non-empty
- bfill leakage fixed in the shared module
- Redundancy + `weighted_dist` resolved or documented
- MIN_PERIODS decided with a stated basis
- Single-brand vs pooled measured, decision recorded
- CSD re-runs clean; P0033 unblocked

## Explicitly out of scope

- The 6 EDA enrichment candidates (P0033 F4 — 4 need absent Zotero refs)
- P0031 tasks 1, 2, 3, 5 (documentation/cosmetic; only task 4 has modeling risk)
- Chapter numbers (P0034 — deliberately last; prose will be rewritten once EDA and
  model training settle)
- Mirroring itself (P0033)

## Related

- P0032 `findings.md` F12–F12.5 — market scope evidence, V3/V4 status
- P0033 `findings.md` F5–F11 — blocking constraint, funnel analysis, adequacy assessment
- P0031 task 4 — redundancy (imported as task 5)
- P0026 — the region-scope decision this reverses


---

## 2026-08-18 — status refresh after P0038 completed

P0038 finished (pipeline decomposed, gate passed, notebook retired). That
unblocks everything here that was waiting on the parity check, and settles some
of it outright.

### Task 9 — CLOSED, the measurement already answers it

No further work needed. The plan's own table refutes the premise: pooled
training gives **3,392 rows**, single-brand gives **44**. Selecting the
best brand yields no extra data because 51 brands already sit at full panel
depth — `MIN_PERIODS` filters *series length*, and discarding brands cannot
lengthen the survivor. ~30 features on 44 rows is more features than
observations, which XGBoost/LightGBM cannot fit. Marked complete.

### Task 4 — half delivered by P0038, and the remaining half is now better motivated

**Delivered**: the pipeline records promo capability per category as
`has_promo` in the manifest, and omits `promo_intensity` where `promo_units` is
absent rather than zero-filling (DEC-NO-PROMO-FILL). A constant-zero column
would assert "no promotion ran", which the data does not support.

**Still missing**: the reusable assertion that **fails loudly on an all-zero
column**. Two independent failures in the 2026-08-18 session would have been
caught by exactly that guard:

| Failure | How it presented |
|---------|------------------|
| promo columns empty at region scope | silent for weeks (P0032 F10.2) |
| Prophet uninstalled | `n_series=0`, aggregated to `nan`, script exited 0 |

Both are the same shape: a component produced nothing, and nothing complained.
Scope the assertion to any all-zero *or* all-null feature, not promo alone.

### Task 7 — unblocked, and P0038 sharpened the `weighted_dist` question

The redundancy half stands: `sales_value` / `sales_liters` / `sales_units` are
the same quantity in different units.

The `weighted_dist` half is more interesting than when written. P0032 measured
its target correlation at **0.756**, above `lag_1`'s 0.585 — backwards for a
supposedly exogenous variable. **P0038 F68 adds context**: `weighted_dist` is a
share-of-stores measure whose scale depends on market scope (parent mean 0.1489
vs regional children 0.1973, ratio 0.7548). It was also the one feature the
notebook back-filled, which P0038 fixed.

Given that P0038 found a leaky feature hiding behind a **96% spot-check match**
(F73 `zero_run_flag`), a correlation this high on an "exogenous" variable
deserves an explicit t vs t-1 check before the sensitivity fit, not after.

### Task 11 — unblocked, still undefined

No detail section was ever written for this task. Before starting it, someone
has to say which product-dimension fields are meant and what brand-month signal
they would become. As written it is a title, not a task.

### Also open, not tracked here

- **F72** (P0038): Prophet's unbounded log-space trend — one CSD brand predicted
  101M vs 301k actual, 59.9% of category error. Recommendation is to report
  medMAPE rather than tune the baseline.
- **F75** (P0038): `mean MAPE` reaches 10^15% for *SeasonalNaive* in the
  benchmark table; the column is uninterpretable and should be dropped.
- **P0037 DEC-HORIZON** remains open per this plan's frontmatter.
