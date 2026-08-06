---
pid: P0032
created: 2026-08-01 00:00:00
updated: 2026-08-06 00:00:00
status: blocked
blocked_reason: "V3 + V4 fixes are applied and verified in worktree p0032-leakage-fix-v3-v4 (uncommitted). Phases 3-4 cannot proceed: (a) promo_intensity is identically zero across all 2552 CSD rows, so the before/after metric shift the plan was built to measure does not exist (F10); (b) the SRQ1 baseline in 04_thesis_results/srq1/metrics.csv is stale and raises KeyError under the current benchmark script (F11). Unblocking requires a grain decision — see F10.5."
focus_detail: "Phase 2 done (tasks 2,3,4,5,9). Tasks 1,6,7,8 blocked. Next action is the F10.5 decision on whether to switch the CSD grain to national rollup market 1256338."
---

# P0032 — Leakage Fix (V3) + Market-Scope Assert (V4)

> **Independent plan.** Touches one source file plus a CSD re-run. Does not depend on
> P0033 (EDA mirroring) or P0034 (chapter numbers). P0034 consumes this plan's output
> but can be prepared in parallel.

## Why

Enrico's stage-4 engineering review (`harness/reviews/feature-build.md`, 2026-07-12)
confirmed two defects. His review targeted the *archived* builders
(`.archive/enrico_legacy_preprocessing_2026-07/preprocessing/nielsen_dvh/`), which are
dead code post-P0028. Verification during this session found **the same leakage is live**
in the current shared module.

### V3 — `promo_intensity` target leakage (CONFIRMED live)

`02_thesis_data/_02_preprocessing/nielsen/_shared_modules/engineer_features.py:317-321`

```python
df["promo_intensity"] = np.where(
    df["sales_units"] > 0,
    df["promo_units"] / df["sales_units"].clip(lower=1), 0,
).clip(0, 1)
```

The target (`sales_units_t`) sits in the denominator, and the feature is consumed at
current `t` against the `log_sales_units` target. Every neighbouring lag/rolling feature
in the same function is correctly `.shift(1)`-ed — this one is not. That asymmetry is
what makes it a bug rather than a deliberate exogenous-planning choice.

`promo_intensity` appears in the FEATURES list of ~15 live scripts, e.g.
`03_thesis_modelling/model_training/srq1_benchmark_tuned.py:41`, `srq1_shap.py:35`,
`model_serving/system_a_forecast/forecast_service.py:36`.

**Impact:** CSD + energidrikke metrics are optimistic. danskvand/RTD are promo-zero → unaffected.

### V4 — market-scope filter unguarded

The single-market filter guards `len == 0` but not `len > 1`. If `DVH EXCL. HD` ever maps
to two `market_id`s, the previously-fixed 6.16× double-count silently returns.

### Also in scope (decide, don't assume)

`weighted_distribution` is likewise contemporaneous with the target. Enrico flagged it as
a "softer concern" inside V3 and did **not** log it separately. This plan decides it
explicitly rather than leaving it implicit.

## Scope boundary

- **In:** `_shared_modules/engineer_features.py`; the market-scope assert; CSD re-run; before/after metric capture.
- **Out:** the archived `build_feature_matrix*.py` (dead — do not edit); chapter prose (P0034); other categories' EDA (P0033).

## Phases

| Phase | Goal | Tasks |
|-------|------|-------|
| 1 | Establish baseline + confirm blast radius | 1, 2, 9 |
| 2 | Apply fixes | 3, 4, 5 |
| 3 | Re-run + quantify | 6, 7 |
| 4 | Hand off to P0034 | 8 |

### Task 9 — prior-bug context (verify only)

P0027 (2026-07-11) found a *different* leakage bug in this same module: it grouped by
`brand` only, so region-grain lag/rolling features conflated across regions. A 2026-08-01
check indicates this is **already fixed** — `group_keys` is threaded through all five
series-aware functions and defaults to `["brand"]`.

Task 9 re-confirms this before task 4 edits the file, so the V3 fix isn't built on a stale
assumption. If confirmed fixed, record and move on — do not re-fix.

## Decisions to make in-plan

1. **V3 fix shape** — `.shift(1)` (keep as lagged promo signal) vs drop entirely.
   Default: `.shift(1)`, preserving a promo signal without leaking `t`.
   Rationale must be recorded — it lands in Ch6/Ch3 prose later.
2. **`weighted_distribution`** — treat as known/planned exogenous (keep at `t`) or shift.
   Distribution coverage is arguably known in advance; promo ratio computed from realised
   sales is not. Decide and document.

## Definition of done

- No feature in `engineer_features.py` derives from `sales_units_t` at current `t`.
- Market-scope assert fails loudly on `> 1` id.
- CSD feature matrix regenerated; before/after WMAPE recorded in `findings.md`.
- Decision rationale for both V3 shape and `weighted_distribution` written down.

## Related

- `harness/reviews/feature-build.md` — original V3/V4 findings
- `harness/thesis_tasks.json` — V2/V3/V4/S01 entries (status `ready`)
- P0034 — consumes the before/after numbers
- V2 (mean-MAPE suppression) is **already reflected** in Ch6 §6.5.1 prose; it belongs to the S01 retrain, not this plan.
