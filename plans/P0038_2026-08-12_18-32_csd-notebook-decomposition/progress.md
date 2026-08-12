---
pid: P0038
created: 2026-08-12 18:32:00
updated: 2026-08-12 18:32:00
---

# P0038 Progress Log

## Session 1 — 2026-08-12 (design only, no code written)

Forked out of P0036 mid-session after Brian raised reverting the CSD notebook
to step scripts.

### What happened

Brian asked whether to split the notebook back into scripts. My initial answer
argued **against**, on the grounds that four sets of near-identical step scripts
are what produced the P0027/P0029/P0030 drift.

**Brian corrected the premise** and was right:

> *"that is only an issue if we duplicate the identical steps for each category,
> which we dont have to."*

Drift comes from copying, not from splitting. Shared scripts parameterised by
`--category` remove the drift surface rather than multiplying it. The corrected
plan is 6 shared + 4 per-category = **11 files replacing 32**.

Brian also settled two questions I raised:
- **EDA split** — yes, separate descriptive from parameter-deriving
- **Order** — finish P0036 task 15 on the shared module, skip the notebook
  patch (the notebook is being dissolved anyway), then decompose

### Measurements taken

Six findings recorded (F26–F34 in `findings.md`). The two that changed the plan:

**F30 — CSD's orchestrator is broken.** `preprocessing_csd.py` invokes step
scripts P0030 deleted. `python preprocessing_csd.py` fails at step 1 today.
This inverted my main objection: the decomposition *repairs* a dead entry point
instead of adding one.

**F29 — P0036 F25 was wrong for CSD.** F25 reported 63/13/24 from fixed dates.
CSD actually runs a *different* pathway (absolute counts 24/6) giving
**52/13/35**. Both mechanisms are broken for the same underlying reason, but
the number and the cause in F25 were both wrong for CSD. Corrected in F29.

### Verification performed

| Check | Method | Result |
|-------|--------|--------|
| EDA→pipeline dataflow | AST parse, Store/Load intersection | 6 real params, 3 leaked loop vars |
| Contract file exists | Read export lines 1596–1669 | Already written, never read back |
| Params genuinely derived | grep assignments in cells 25/31/41/45 | 4 of 6 derived; TRAIN_END/VAL_END and MIN_PERIODS are not |
| Orchestrator liveness | `ls` all four category dirs | CSD's targets missing; other 3 intact |
| Orchestrator duplication | `diff` Danskvand vs RTD | Name-only differences, 184 lines each |
| `base_preprocessing.py` role | Read first 70 lines | Utility library, no `__main__`, no conflict |
| Split reality | Measured all 4 categories, both pathways, fresh parquet | Table in F29 |

### Errors encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| `FileNotFoundError` on `_01_converted/nielsen/{cat}/views/` | 1 | Wrong path shape — real layout is `_01_converted/nielsen/parquet_nielsen/{cat}/views/`. Fixed the scratch script. |

### Carried over from P0036 (uncommitted work)

P0036 task 15 is **partly landed** and its code is on disk:

- `_shared_modules/engineer_features.py` — `apply_split()` now proportional by
  default; new `resolve_split_cutoffs()`; `LEGACY_TRAIN_END`/`LEGACY_VAL_END`
  retained for reproducing published splits; `FeatureEngineer` fields updated
- 6 step scripts patched (Danskvand/Energidrikke/RTD × `_5_apply_split.py`,
  `_6_save_outputs.py`) — resolve cutoffs from data, and `_6` now reports the
  boundaries **actually applied** rather than re-deriving them from constants

The CSD notebook half of task 15 is **deliberately not done** — superseded by
P0038 task 4.

**None of this is committed yet.**

### State at session end

- Plan written, no code written for P0038 itself
- Tasks 1–9 defined, none started
- Next: task 1 (shared step 0 + capture utils)

### Open decisions

| Decision | Owner | Blocking? |
|----------|-------|-----------|
| MIN_PERIODS threshold value | Brian (P0036 task 8) | No — P0038 task 4 makes the value derived and surfaces the distribution; the choice can follow |
| DEC-HORIZON (one-step vs recursive) | Brian (P0037) | No |

### Note on git state

Unpushed commits on `main` from `31d2c65` through `af4cad9`. Commit `95723c3`
sits alone on `thesis/serving-interface-refinement` (= `main` + that one commit)
awaiting a fast-forward; `git checkout main` was blocked by the permission
classifier earlier in the session and was left for Brian.
