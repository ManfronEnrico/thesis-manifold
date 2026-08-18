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

---

## Session 2 — 2026-08-12 (task 1: shared step 0 + capture utils)

Brian, opening the session:

> *"make sure that the content of the CSD version does not degrade in the
> splitting process"*

Treated as the acceptance criterion for every port in this plan, not just task 1.
Implemented as an explicit parity check per step (see below), rather than
eyeballing the diff.

### What was built

Three files in `_shared_modules/`:

| File | Purpose |
|------|---------|
| `capture_utils.py` | `tee_console`, `save_table`, `print_and_save_table` |
| `pipeline_config.py` | Category-keyed config shared by all steps (F35) |
| `step_0_validate_cache.py` | The runnable step, `--category` |

Two deviations from the plan, both recorded in `task_plan.md` task 1 detail:
capture utils went to a new `capture_utils.py` rather than `terminal_utils.py`
(persistence vs presentation), and `pipeline_config.py` was added because cells
3–10 turned out to hold config for *every* step, not just step 0 (F35).

### Verification performed

| Check | Method | Result |
|-------|--------|--------|
| Capture utils behave | 8 assertions incl. exception-safety, overwrite-not-append, non-ASCII | all pass |
| Step 0 unit behaviour | 9 assertions | all pass |
| Real cache, all 4 categories | ran the CLI against live parquet | 4/4 OK, exit 0 |
| Missing-file path | synthetic empty dir | detected, raises with remediation |
| Zero-byte path | synthetic truncated parquet | detected (new capability, F36) |
| Mixed missing+empty | synthetic | reported separately and precisely |
| Unknown category | `--category Totalbeer` | `ValueError`, lists valid values |
| **Notebook parity** | AST-extract every name from cells 3–10, check each is kept or deliberately dropped | **no content lost** |

The parity check flagged one name, `required_view_files`, as "LOST". It is a
rename, not a loss — it became the `view_filenames()` function. The checker
matches literal identifiers and cannot see renames; verified manually.

### Content-preservation ledger (task 1)

Everything from cells 3–10 is accounted for:

- **Kept**: all ML target constants, all plot styling constants, the validation
  function and its message format, the cache-verification summary block, the
  target-definition echo, the root-discovery walk
- **Transformed**: `CATEGORY` → CLI arg; the 4 path constants → `get_paths()`;
  `required_view_files` → `view_filenames()`; `warnings.filterwarnings` →
  opt-in `suppress_warnings()` (import-time suppression would hide warnings from
  every importer, including tests)
- **Dropped deliberately**: the four `%pip install` cells — dependencies belong
  in `requirements.txt`, not in a pipeline step
- **Gained**: zero-byte detection (F36), per-category artifact isolation (F34),
  console log persisted to `step_0_console.log`

### Errors encountered

None. The port ran clean on first execution for all four categories.

### State at session end

- Task 1 complete and verified
- Task 2 (`step_1_load_and_aggregate.py`) unblocked and next
- The pattern is now established: port → unit-test → run live → AST parity check

### Note on git state

Unpushed commits on `main` from `31d2c65` through `af4cad9`. Commit `95723c3`
sits alone on `thesis/serving-interface-refinement` (= `main` + that one commit)
awaiting a fast-forward; `git checkout main` was blocked by the permission
classifier earlier in the session and was left for Brian.

---

## Session 2026-08-18 — task 3 (step 2) complete

### Shipped

| File | Change |
|------|--------|
| `_shared_modules/step_2_eda_descriptive.py` | **new**, 18 sections |
| `_shared_modules/step_1_load_and_aggregate.py` | predicate pushdown on `market_id` |
| `_shared_modules/capture_utils.py` | `.md` output + `notes=` bullets |

### Run results

All four categories, zero failures:

| Category | Sections | Tables | Plots |
|----------|----------|--------|-------|
| CSD | 18/18 | 22 | 8 |
| Energidrikke | 18/18 | 22 | 8 |
| Danskvand | 16/18 | 19 | 7 |
| RTD | 16/18 | 20 | 7 |

**Three of four categories now have EDA for the first time.**

### Errors encountered

| Error | Cause | Resolution |
|-------|-------|------------|
| `ArrowMemoryError: malloc of size 2097152 failed` | step 1 materialised 10.3M × 32 before filtering to 2.16% | predicate pushdown at the reader (F43) |
| `ModuleNotFoundError: statsmodels` | ADF + seasonal decomposition dependency absent | `python -m pip install statsmodels` (0.14.6) |
| Heredoc mangled `\n` and apostrophes in patch scripts | bash consumed the escapes before Python saw them | wrote patch content via the Write tool instead |

### Verification

- Step 1 output identical pre/post pushdown: 142 brands, 4,209 rows, 32 cols,
  46 periods
- Facts load drops 10,311,342 → 223,240 rows, matching the independently
  measured parent-market count exactly
- Danskvand/RTD skip 3.13 and 3.17 with a printed reason, not a raise
- Markdown tables verified to carry alignment markers and render as real tables

### State at session end

- Tasks 1, 2, 3 complete → **task 4 (`step_3_derive_params.py`) is next**
- Task 4 must settle MIN_PERIODS (F38 / P0036-8) and TRAIN_END/VAL_END (F25/F28)
- **Unpushed**: 2 commits (`ffe6f45`, `4455951`). The earlier 11 landed on
  `origin/main` mid-session. `git push` is blocked by the permission
  classifier for this session; Brian runs `! git push origin main`.
- Correction to the previous session's note: `thesis/serving-interface-refinement`
  does **not** exist, and `95723c3` is already on both `main` and `origin/main`.
- `origin/enrico/local-backup` last moved 2026-07-13 and touches no
  preprocessing code — not a merge risk for this work.

