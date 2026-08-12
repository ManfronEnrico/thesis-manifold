---
pid: P0036
created: 2026-08-11 16:08:00
updated: 2026-08-11 22:00:00
status: in_progress
focus_detail: "Tasks 1-3 and 5 complete. CSD filters to parent 1256338 (37,999 rows, 1 market, 140 brands, promo populated); make_calendar bfill future-leakage removed (contaminated 1,176 rows / 19.1% / 51 brands, all leading gaps) and its docstring now names both leakage kinds. F15 corrects the plan's wrong scope numbers; F16 documents the bfill fix. Ch4 writing notes updated with the corrected funnel + a leakage-control section. NEXT: task 4 (derived promo asserts + reusable all-zero guard), then task 6 (re-run, the gate that unblocks P0033). Notebook is 57.8k tokens -- Grep + JSON-patch script; Read and NotebookEdit both refuse it."
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
| 4 | Verify promo columns populate; assert non-degenerate | 2 | 3 | pending |
| 5 | Fix `make_calendar` bfill future-leakage | 3 | 1 | ✅ complete |
| 6 | Re-run CSD end-to-end + parity check | 5 | 3, 4, 5 | pending |
| 7 | Resolve sales_value/sales_liters redundancy (P0031 task 4) | 4 | 6 | pending |
| 8 | Decide MIN_PERIODS threshold | 4 | 6 | pending |
| 9 | Measure single-brand vs pooled training cost | 4 | 6 | pending |

**Task 6 is the gate that unblocks P0033.** Tasks 7–9 are modeling analyses that
change no notebook structure, so they deliberately run *after* mirroring starts
rather than holding the critical path.

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

### Task 8 — Decide MIN_PERIODS
Current threshold culls 140 → 58 brands (59%). At parent scope:

| MIN_PERIODS | Brands | Rows |
|-------------|--------|------|
| >=12 | 109 | 3,744 |
| >=24 | **85** | **3,392** |
| >=30 | 76 | 3,152 |
| >=36 | 67 | 2,865 |

51 brands already have all 44 months. Trade-off is series quality vs pooled sample size.
Brian 2026-08-11: *"the min_period decision is shaky at best either way."* Needs a
defensible basis for Ch4, not just a number.

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
