---
pid: P0032
created: 2026-08-01 00:00:00
updated: 2026-08-01 00:00:00
---

# P0032 — Progress Log

## 2026-08-01 — Plan created

- Verified V3 leakage live at `_shared_modules/engineer_features.py:317-321`
- Verified both legacy builders are dead code (`.archive/`, referenced nowhere live)
- Confirmed blast radius: ~15 consumer scripts read `promo_intensity` from the matrix
- Tasks 1–8 decomposed; no code changed yet

## Session log

<!-- append: date, what ran, results, errors -->

### 2026-08-06 — Execution session (worktree + sub-agent)

**Status at session end: partially complete. Nothing committed, nothing pushed.**

#### Setup

- Created worktree `worktrees/p0032-leakage-fix-v3-v4` on branch
  `cc/20260801-1630/p0032-leakage-fix-v3-v4`, branched from `e9fd769`.
- All code changes live **only in that worktree**. The main repo is untouched
  except for the pre-existing uncommitted modification to
  `02_thesis_data/_02_preprocessing/nielsen/CSD/pipeline_step_scripts/pre_processing_notebook_csd.ipynb`,
  which predates this session and was not edited here.

Three git errors hit and resolved during setup (logged for future worktree work
on the Z: drive):

| Error | Cause | Fix |
|-------|-------|-----|
| `git worktree add` timed out at 2m | Large repo on slow Z: drive | Re-ran checkout with `run_in_background: true` |
| `fatal: detected dubious ownership` | Z: filesystem records no ownership | `git config --global --add safe.directory Z:/_dev-ssd/thesis-manifold/worktrees/p0032-leakage-fix-v3-v4` |
| `Another git process seems to be running` | Stale zero-byte `index.lock` left by the killed `worktree add` | Removed `.git/worktrees/p0032-leakage-fix-v3-v4/index.lock`, re-ran checkout |

Also noted: `git worktree list` reported stale branch labels. `git rev-parse
--abbrev-ref HEAD` was correct — trust `rev-parse`, not the list output.

#### Tasks

| Task | Status | Notes |
|------|--------|-------|
| 1 — capture baseline metrics | **blocked** | Baseline is stale and unreproducible — see F11 |
| 2 — confirm no script recomputes `promo_intensity` | completed | Confirmed: consumers read the column, none recompute |
| 3 — decide V3 fix shape | completed | `.shift(1)`, not drop — see Decisions below |
| 4 — apply V3 fix | completed | `engineer_features.py:353-380` |
| 5 — apply V4 assert | completed | `:183-193` (CSV path) + `:77-101` (DB path) |
| 6 — re-run CSD | **blocked** | Blocked by F10 (promo all-zero) + F11 (stale baseline) |
| 7 — quantify before/after | **blocked** | Same |
| 8 — hand off to P0034 | **blocked** | P0034 paused; handled in a separate session |
| 9 — verify P0027 groupby fix | completed | Confirmed still fixed; one correction to F4 below |

#### What changed in `_shared_modules/engineer_features.py`

**V3 (`:353-380`)** — `promo_intensity` now group-shifted:

```python
_promo_intensity_t = pd.Series(
    np.where(
        df["sales_units"] > 0,
        df["promo_units"] / df["sales_units"].clip(lower=1),
        0,
    ).clip(0, 1),
    index=df.index,
)
df["promo_intensity"] = _promo_intensity_t.groupby(
    [df[k] for k in group_keys]
).shift(1)
```

Execution-verified: correct one-period shift, first observation per series is
NaN, no cross-series bleed, `[0, 1]` range preserved, multi-key grain honoured.

**V4a (`:183-193`)** — CSV path now raises on `len(target_market_ids) > 1`.

**V4b (`:77-101`)** — DB path gained a pre-flight id count. Added by the agent
beyond the plan's literal scope; justified because that SQL filters a *joined*
`dim_market`, so a duplicate description fans out the JOIN and every `SUM()`
double-counts. Kept.

#### Correction to F4

F4 claimed `group_keys` is threaded through `apply_split (:348)`. It is not —
`apply_split` takes no `group_keys` and needs none. The other four call sites
are correct: `make_calendar (:190)`, `filter_series (:244)`,
`engineer_features (:263)`, `build_series_index (:346)`, plus the
`FeatureEngineer` dataclass (:401).

#### Decisions taken

1. **V3 fix shape** — `.shift(1)`, not drop. Preserves a lagged promo signal
   without leaking `sales_units_t`. Matches the treatment of every neighbouring
   lag/rolling feature in the same function.
2. **`weighted_distribution`** — kept contemporaneous at `t`, on the reasoning
   that distribution coverage is plausibly known in advance whereas a promo
   ratio computed from realised sales is not. **Flagged as the weakest link**:
   its correlation with the target (0.756) exceeds `lag_1`'s (0.585), which is
   suspicious for a genuinely exogenous variable. Recommend a Ch6 sensitivity
   check (fit with and without it) before defending this choice.

#### Related issue found, not fixed

`make_calendar:232-235` uses `bfill`, which pulls future values backwards
across gap months. Out of scope for P0032; worth a separate ticket.

#### Scope landmine noted

Duplicate, divergent SRQ scripts under `utility_scripts/scripts/` use the column
name `weighted_distribution`, while the live copies under `03_thesis_modelling/`
use `weighted_dist`. Any future rename touches both trees.

#### Why the plan could not finish

The plan's central premise did not survive contact with the data. `promo_intensity`
is **identically zero across all 2552 CSD rows** — independently verified
(`promo_units` nonzero count = 0, max = 0.0). The leakage was real in code but
carried no signal, so the expected "WMAPE gets worse after the fix" outcome
cannot occur. The honest before/after result is *no change*.

Three blockers stand between here and the definition of done:

1. **F10** — promo is structurally absent at the selected market grain.
2. **F11** — the SRQ1 baseline in `04_thesis_results/srq1/metrics.csv` is stale
   and cannot be reproduced by the current benchmark script.
3. Only CSD has a feature matrix; the other three categories have none.

See `findings.md` F10 and F11 for the full investigation.

#### Next session should start by

Deciding F10.5 — whether to adopt the national rollup market (`1256338`) as the
CSD grain. That decision gates tasks 1, 6 and 7. It is a thesis-level grain
change, deliberately **not** implemented here.
