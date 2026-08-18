---
pid: P0038
created: 2026-08-12 18:32:00
updated: 2026-08-18 00:00:00
status: in_progress
focus_detail: "Steps 0/1/2 shipped and verified across all four categories. Step 2 runs 18/18 sections for CSD+Energidrikke, 16/18 for Danskvand+RTD (promo sections skipped by column discovery, not by category name). NEXT: task 4 (step_3_derive_params.py + contract JSON) -- it is the last blocker before feature engineering, and it must settle MIN_PERIODS (F38/P0036-8) and the TRAIN_END/VAL_END drift (F25/F28). Blocks P0036 task 6 (CSD parity check), which is the P0033 gate."
---

# P0038 — Decompose the CSD Notebook into Shared Step Scripts

> **Brian, 2026-08-12:** *"take the notebook and split it into its constituent
> steps ... one script for each of the identical steps before and after
> engineering, the engineering part will have one script per dataset."*

## Why this plan exists

The CSD notebook is 57,814 tokens — Read refuses it, NotebookEdit refuses it,
and every edit this session has gone through exact-match JSON patch scripts.
That is a hard tooling wall, not a preference.

But the decisive argument is not tokens. **CSD's orchestrator is broken**:
`CSD/preprocessing_csd.py` shells out to `pre_csd_1..6_*.py` in
`pipeline_step_scripts/`, and P0030 deleted those files when the notebook
absorbed them. `python preprocessing_csd.py` fails at step 1 today. CSD is not
"notebook instead of scripts" — it is a notebook *plus* a dead entry point.

The decomposition repairs that entry point rather than adding an eleventh one.

## The duplication correction (Brian, 2026-08-12)

An earlier draft of this argument claimed splitting CSD back into scripts would
recreate the P0027/P0029/P0030 drift. **That was wrong**, and Brian corrected it:

> *"that is only an issue if we duplicate the identical steps for each category,
> which we dont have to. We could have all the identical preprocessing steps
> bundled into one script, and then only have category specific feature
> engineering scripts, and the other scripts that are also reasonably identical
> (split, save outputs)."*

Drift comes from **copying**, not from splitting. One shared script per identical
step, parameterised by `--category`, removes the drift surface instead of
multiplying it. Measured evidence that the copies are real duplicates: the three
working orchestrators are **184 lines each and differ only in the category name**.

## Decisions locked

| ID | Decision | Basis |
|----|----------|-------|
| **DEC-SPLIT-FORMAT** | Script-based, not notebook | Broken orchestrator; 57.8k-token edit wall; scriptable/repeatable pipeline; per-category re-runs |
| **DEC-SHARED-SEAM** | Shared = steps 0,1,2,3,5,6; per-category = step 4 only | Capability tiers (32/32/31/15 cols, 7/7/6/0 promo) differ *only* at feature engineering |
| **DEC-CONTRACT** | `{category}_eda_findings.json` is the step 3 → step 4 interface | The JSON already exists and already carries all six params + rationale; it is simply never read back |
| **DEC-EDA-SPLIT** | Descriptive EDA and parameter-deriving EDA are separate steps | Re-deriving params must not require regenerating ~20 plots; keeps thesis-figure code out of the pipeline's dependency path |
| **DEC-NO-FALLBACK** | Step 4 fails loudly if the contract JSON is missing/incomplete | Silent in-code defaults are exactly what let the split and MIN_PERIODS rot unnoticed |
| **DEC-OPEN-WORLD** | Shared steps **discover** columns; they never enumerate them | Brian, 2026-08-12. A hardcoded list is category-*dependent* by construction — it silently drops whatever it does not name. The notebook's 5-column `agg_dict` discarded 24 of 29 available measures (F39) and could not express per-category spelling variants. Only the forecast target is named, and for its **role**, not its category |

## Evidence base

Full measurements in `findings.md`. Key structural facts:

**Notebook composition** (65 cells, 75,879 source chars):

| Cells | Section | Destination |
|-------|---------|-------------|
| 3–10 | Setup, paths, cache validation | shared `step_0` |
| 12–14 | Load views, merge, DEC-SCOPE filter | shared `step_1` |
| 17–39 | Descriptive EDA (8 plots) | shared `step_2` |
| 41–53 | Parameter derivation + findings JSON | shared `step_3` |
| 56–60 | Calendar, filter, engineer features | **per-category** `step_4` |
| 62 | Apply split | shared `step_5` |
| 64 | Save outputs | shared `step_6` |

**EDA → pipeline dataflow** (AST-traced, F26). Only six real parameters cross
the boundary — the contract is small and tractable:

`LAGS`, `ROLLING_WINDOWS`, `holiday_months`, `log_necessary`,
`train_end_(year,month)`, `val_end_(year,month)`.

(`c`, `grp`, `months` also cross but are leaked loop variables, not state.)

**File-count reduction: 32 → 11.**

## Target structure

**Shared** — `_shared_modules/`, all take `--category`:

| File | From cells | Replaces |
|------|-----------|----------|
| `run_preprocessing.py` | orchestrators | 4 orchestrators (184 lines each, name-only diff) |
| `step_0_validate_cache.py` | 3–10 | 4 × `pre_*_0_cache.py` |
| `step_1_load_and_aggregate.py` | 12–14 | 4 × `pre_*_1_*` |
| `step_2_eda_descriptive.py` | 17–39 | — (new; notebook-only today) |
| `step_3_derive_params.py` | 41–53 | — (writes the contract JSON) |
| `step_5_apply_split.py` | 62 | 4 × `pre_*_5_*` (already fixed, P0036 task 15) |
| `step_6_save_outputs.py` | 64 | 4 × `pre_*_6_*` |

**Per-category** — `{Category}/`:

| File | From cells | Why not shared |
|------|-----------|----------------|
| `step_4_engineer_{category}.py` ×4 | 56–60 | Capability tiers genuinely differ |

The other three categories currently have **no EDA at all** — they gain steps 2
and 3 for free, which is most of what P0033 was scoped to do.

## Output capture (Brian's requirement)

Everything lands in `{Category}/pipeline_step_outputs/`:

```
pipeline_step_outputs/
  eda_plots/                  *.png   (already works)
  eda_tables/                 *.csv   (new — the printed DataFrames)
  logs/step_{N}_console.log           (new — full stdout per step)
  {category}_eda_findings.json        (the contract)
  step_{N}_*.parquet                  (already works)
```

Console capture via a `tee` context manager in `terminal_utils.py`: stdout goes
to terminal *and* log file, so the interactive view survives and the artifact
gets produced.

## Phases

| Phase | Goal | Tasks |
|-------|------|-------|
| 1 | Repair the seam — shared entry + load | 1, 2 |
| 2 | EDA split + the contract | 3, 4 |
| 3 | Per-category feature engineering | 5 |
| 4 | Tail steps + orchestrator | 6, 7 |
| 5 | Verify, then retire the old tree | 8, 9 |

## Tasks

| ID | Title | Phase | Blocked By | Status |
|----|-------|-------|------------|--------|
| 1 | Build shared `step_0_validate_cache.py` + console/table capture utils | 1 | — | **complete** |
| 2 | Build shared `step_1_load_and_aggregate.py` (carries DEC-SCOPE) | 1 | 1 | **complete** |
| 3 | Build shared `step_2_eda_descriptive.py` (plots + tables) | 2 | 2 | **complete** |
| 4 | Build shared `step_3_derive_params.py` + contract JSON schema | 2 | 2 | pending |
| 5 | Build `step_4_engineer_csd.py` reading the contract | 3 | 4 | pending |
| 6 | Generalise `step_5_apply_split.py` + `step_6_save_outputs.py` to `--category` | 4 | 5 | pending |
| 7 | Build shared `run_preprocessing.py` orchestrator | 4 | 6 | pending |
| 8 | Run CSD end-to-end + parity-check vs last notebook run | 5 | 7 | pending |
| 9 | Retire notebook, old step scripts, 4 orchestrators | 5 | 8 | pending |

**Task 8 is the gate.** It is the same verification as P0036 task 6, and it is
what unblocks P0033.

## Session 2026-08-18 — step 2 shipped, EDA now exists for all four categories

### Task 3 complete

`_shared_modules/step_2_eda_descriptive.py`, **18 sections**, run clean across
all four categories:

| Category | Sections | Tables | Plots |
|----------|----------|--------|-------|
| CSD | 18/18 | 22 | 8 |
| Energidrikke | 18/18 | 22 | 8 |
| Danskvand | 16/18 | 19 | 7 |
| RTD | 16/18 | 20 | 7 |

Zero failures. The two skipped sections in Danskvand/RTD are 3.13 and 3.17,
both requiring `promo_units`, skipped by **column discovery** with a printed
reason — no branch anywhere names a category (DEC-OPEN-WORLD holds).

**The defect this fixes, precisely.** Notebook cell 39 referenced
`df['promo_units']` guarded only by an `.empty` check, which tests for zero
**rows**, not a missing **column**. Danskvand has no promo columns, so the cell
raised `KeyError`. That single line is why three of four categories had no EDA.

### Blocker found and fixed mid-task: ArrowMemoryError in step 1

Step 2 could not run for CSD at all:
`pyarrow.lib.ArrowMemoryError: malloc of size 2097152 failed`.

`load_merged()` read the full facts table before applying the DEC-SCOPE filter.
CSD facts are **10,311,342 rows × 32 float64 columns** (767.5 MB compressed),
which materialises to ~2.6 GB dense plus pyarrow's conversion copy — against
2.0 GB free of 15.8 GB.

The filter keeps only the parent market, measured at **2.16%** of CSD rows
(Danskvand 1.99%, Energidrikke 1.59%, RTD 2.07%). Pushing it into the parquet
reader (`filters=[("market_id", "==", DVH_PARENT_MARKET_ID)]`) cuts the working
set ~46×: facts now load as **223,240 rows** and step 1 finishes in 6.5 s.

The pandas-level filter was **deliberately kept**. It is now a no-op on the
data, but it remains the readable statement of DEC-SCOPE and still guards the
case where a future engine ignores `filters=`.

**Verified non-regressive**: 142 brands / 4,209 rows / 32 cols / 46 periods,
identical to the pre-fix run.

### Brian's requirements, 2026-08-18

1. **Tables as Markdown, not TXT.** `save_table()` now writes `.md`. The TXT
   rendering mirrored notebook cell output, but these tables go into thesis
   appendices, and monospace alignment collapses the moment it is pasted into
   Word or Docs, which reflows it proportionally. `tabulate` is a hard
   dependency now, raising with the install command rather than degrading to
   `to_string()` — a silent fallback would put a fixed-width body in a `.md`
   file and look broken for an invisible reason. CSV is untouched.

2. **Interpretation bullets above every table.** `ctx.save(notes=[...])`, on
   all 22 tables. Each states what the table shows, how to read it, and the
   methodological basis where one exists — Kim (2013) skewness bands,
   Box & Jenkins (1970) for ACF, Chow (1960), Dickey & Fuller (1979). Several
   deliberately state a limitation rather than a finding (promo/no-promo is
   confounded by selection; contemporaneous correlation is not predictive
   value; ADF has low power at n≈46). Notes go to the `.md` only, not the CSV.

3. **Four orphaned plots recovered into step 2.** `02_ecdf`, `06_acf_pacf`,
   `07_promo_intensity`, `08_correlation` existed as PNGs under `CSD/` that no
   code regenerated. Now sections 3.15–3.18:
   - **3.16 / 3.17 / 3.18** recovered from notebook cells 43 / 49 / 51.
   - **3.15 (ECDF)** could not be recovered — the cell had already been deleted
     from the notebook, whose header still advertises "14 visualizations"
     against 8 PNGs on disk. Rebuilt from the documented intent.
   - **3.18 was closed-world in the notebook**: cell 51 hardcoded five column
     names and silently analysed only those it found. Now discovers every
     numeric measure, and adds a |r| > 0.9 near-duplicate scan feeding P0036 F7.

### Architecture question settled (Brian's recollection, checked)

Brian asked whether the per-category step scripts are stale duplicates.
**Confirmed, with one correction.**

- ✅ The three orchestrators are **byte-identical after name normalisation**
  (verified by `diff` on sed-normalised copies). DEC-SHARED-SEAM stands:
  shared = steps 0,1,2,3,5,6; per-category = step 4 only.
- ❌ They are **not stale EDA**. None of the 24 per-category scripts imports
  matplotlib — they do no EDA at all. CSD was not missing EDA scripts; CSD was
  the only category that *had* EDA, and it lived in the notebook.
- ⚠️ **Numbering trap**: old `step_2` = `build_calendar`, new `step_2` = EDA.
  Same number, different meaning. Task 9 (retirement) must not match on number.

### Deviation from plan: 18 sections, not 12

The plan scoped step 2 to notebook cells 17–39. Cells 43/49/51 sit inside the
41–53 range assigned to **step 3**, but they are descriptive figures, not
parameter derivation. Splitting on cell number would have sent plots into the
parameter step and violated DEC-EDA-SPLIT, whose whole point is that
re-deriving parameters must not regenerate ~20 plots. **The seam is the
function, not the cell index.** Cells 43/49/51 moved to step 2; the parameter
logic in 41–53 stays with step 3.

## Task detail

### Task 1 — Shared step 0 + capture utilities ✅ COMPLETE (2026-08-12)
Port cells 3–10. Both utilities are used by every later step, which is why this
task came first.

**Deviation from plan (2 items, both deliberate):**

1. **Capture utils landed in a NEW `capture_utils.py`, not `terminal_utils.py`.**
   `terminal_utils` is Rich-based *presentation*; these are disk *persistence*.
   Keeping them apart lets a step import capture without pulling in Rich's
   Console machinery, and keeps the Rich dependency off the test path.

2. **A third file was created: `pipeline_config.py`.** Not in the original plan.
   Cells 3–10 contain more than cache validation — they also hold the ML target
   definition (`TARGET_COL`, `FORECAST_HORIZON`, `WARMUP_PERIODS`), the plot
   styling constants, and the path derivations. In the notebook these lived in
   the shared cell namespace, so every later cell saw them for free. Scripts do
   not share a namespace, so leaving them inside `step_0` would have forced
   steps 1–6 to re-declare them — **precisely the copy-paste mechanism that
   caused the drift this plan exists to remove.**

**Files created:**

| File | Chars | Contents |
|------|-------|----------|
| `_shared_modules/capture_utils.py` | ~6.0k | `tee_console`, `save_table`, `print_and_save_table` |
| `_shared_modules/pipeline_config.py` | ~6.9k | `CATEGORIES`, `normalise_category`, ML target consts, plot style, `get_paths`, `view_filenames`, `suppress_warnings` |
| `_shared_modules/step_0_validate_cache.py` | ~6.4k | `validate_parquet_cache`, `report`, `run`, CLI |

**Improvement over the notebook**: validation now also rejects **zero-byte**
parquet files. The notebook tested `.exists()` only — a conversion interrupted
mid-write leaves a 0-byte file that passes an existence test and then fails
inside pandas at step 1 with an opaque error.

**F34 fixed**: `findings_json` and `plots_dir` are now f-strings keyed on the
category slug, verified non-colliding across all four categories.

**Verification**: 9 unit checks + 8 capture-util checks pass; all four
categories validate green against the real cache; unknown category raises;
parity check against notebook cells 3–10 shows no lost content.

### Task 2 — Shared step 1
Port cells 12–14. **Carries DEC-SCOPE** (market parent `1256338`) and the
`_n_markets != 1` fan-out guard from P0036 task 3. Both must survive the port
verbatim — they are the fix for P0027's 6.16× double-count defect.

Category differences here are data-shaped, not logic-shaped (different column
counts survive the same merge), so this stays genuinely shared.

**COMPLETE 2026-08-12.** `_shared_modules/step_1_load_and_aggregate.py`.

All ten critical invariants verified present verbatim (DEC-SCOPE id + full
measurement rationale, the `!= 1` guard and its message, positive-sales filter,
DEC-GRAIN/P0035 notes, promo NaN→0 semantics, brand×month keys).

**Live results — all four categories, first time the other three have ever run
this path:**

| Category | Brand-month rows | Brands | Periods | Cols |
|----------|------------------|--------|---------|------|
| CSD | 4,209 | 142 | 46 | 32 |
| Danskvand | 1,225 | 55 | 41 | 15 |
| Energidrikke | 1,702 | 68 | 43 | 32 |
| RTD | 2,509 | 101 | 41 | 31 |

Period counts match F29's projections exactly (46/41/43/41).

**Two changes beyond a literal port:**

1. **Open-world column discovery** (DEC-OPEN-WORLD, F39). Initially ported as a
   present-column check against a 5-entry list; Brian challenged the premise —
   a general script should not enumerate columns at all. He was right, and
   following it up found the notebook was **silently discarding 24 of 29
   measure columns** per category (the whole `baseline_*` family, the
   `numeric_distribution` family, `universe_number_of_stores`, …), plus it could
   not express per-category spelling variants like
   `disp_w_o_feat` / `disp_wo_feat` / `disp_and_feat`.

   Measures are now discovered and classified by semantics (additive → `sum`,
   intensive → `mean`). Panel width went **8 → 32** columns for CSD, with row,
   brand and period counts unchanged. Only `sales_units` is named, and for its
   role as forecast target rather than as a category feature.

2. **`validate="m:1"` on all three dimension merges** — closes F37, a real
   blind spot in the fan-out guard (see below).

**F37 — the fan-out guard did not catch the fan-out it was written for.**
`nunique() != 1` counts distinct *ids*, but a fan-out multiplies *rows*.
A `dim_market` carrying the parent id on two rows fans out every fact row while
leaving `nunique()` at 1 — silent, and exactly the P0027 6.16× shape. Not live
(all four dim tables have 0 duplicate ids today), now closed regardless. Re-run
confirms identical row counts before and after.

**F38 — `min_periods` disagrees with itself.** The notebook's `GRAIN_CONFIG`
says 40; the actual consumer `filter_series()` defaults to 30. Dropped from
step 1 deliberately (it is a filtering, not an aggregation, parameter) and
handed to task 4, which must derive it and pass it explicitly.

### Task 3 — Shared step 2 (descriptive EDA)
Port cells 17–39. 8 plots at DPI 150.

**Follows DEC-OPEN-WORLD** (Brian, 2026-08-12):

> *"where we can get statistics for all numeric features, and non numeric
> features, similarly have graphs and figures for each of them. That way it
> shouldn't matter?"*

Correct — and with step 1 now yielding 32/15/32/31 columns instead of 8/7/8/7,
per-column enumeration is not even viable. The EDA iterates over
`df.select_dtypes` and emits stats + figures per column found. A category with a
column no other has gets it analysed automatically; a category lacking one
produces one fewer figure, with **no branch anywhere naming a category**.

Consequence: "Danskvand has no promo columns, so skip the promo plots" stops
being a special case — there is no promo-plot code to skip, only a loop that
runs over whatever columns exist.

**Also confirm here**: whether `number_of_items_reach` is genuinely intensive
(F39 open question) — its distribution across brands should settle it.

### Task 4 — Shared step 3 (parameter derivation) + contract
Port cells 41–53. Writes `{category}_eda_findings.json`.

**Every field must be genuinely derived** (Brian: *"we also must make sure that
it gets written by the pipeline steps dynamically, and is not a hard coded not
code / data science derived values"*).

Current derivation status, from the notebook export:

| Field | Derived? | Basis |
|-------|----------|-------|
| `LAGS` | yes | lag corr \|r\|>0.1 in ≥50% of stable brands + ACF/PACF |
| `ROLLING_WINDOWS` | yes | predictive corr, collinearity-pruned |
| `HOLIDAY_MONTHS` | yes | q75 threshold on monthly sales |
| `LOG_TRANSFORM_NECESSARY` | yes | per-brand ADF majority vote |
| `TRAIN_END` / `VAL_END` | **no** | absolute counts (24/6) — F27 |
| `MIN_PERIODS` | **no** | literal `40` with a derived-*sounding* rationale — F28 |

The last two must become real. `TRAIN_END`/`VAL_END` call
`resolve_split_cutoffs()`; `MIN_PERIODS` is computed from the brand-depth
distribution (see task 4 note in P0036 — the threshold *choice* is still
Brian's, this task only makes the value honest and surfaces the distribution).

### Task 5 — Per-category step 4
Port cells 56–60 for CSD. Reads the contract JSON; **raises on missing file or
missing field** (DEC-NO-FALLBACK). The other three categories' step 4 scripts
are P0033's work, not this plan's — this task establishes the pattern only.

### Task 8 — Parity check
Run CSD end-to-end. Compare against the last notebook run:

| Metric | Last notebook run | Expect |
|--------|-------------------|--------|
| Split distribution | train 1450 / val 348 / test 754 (57/14/29) | ~70/15/15 |
| Fact rows post-filter | 37,999 | re-measure (data refreshed) |
| Brand-month rows | 3,917 | re-measure |
| Distinct brands | 140 | re-measure |

Every count from P0036 F15–F21 is **SUPERSEDED** by the 2026-08-12 re-pull.
Differences are expected; the check is that they are *explicable*, not that
they match.

### Task 9 — Retire the old tree
Only after task 8 passes. Build the new tree **alongside** the old; delete
nothing until parity is confirmed.

Removals: the notebook + its export, `pre_{cat}_{0..6}_*.py` ×4, the four
orchestrators. Archive rather than delete anything carrying decision evidence.

## Relationship to P0036

P0038 absorbs three P0036 tasks:

| P0036 task | Fate |
|------------|------|
| 12 (per-notebook feature engineering for capability tiers) | → P0038 task 5 |
| 14 (shared-vs-CSD-specific seam) | → **answered** by DEC-SHARED-SEAM |
| 15 (dynamic split cutoffs) | shared-module half **done**; notebook half → P0038 task 4 |

P0036 keeps: 4 (promo asserts), 6 (parity — now P0038 task 8), 7, 8, 9, 11.

## Definition of done

- CSD runs end-to-end via `run_preprocessing.py --category CSD`
- Contract JSON written with every field genuinely derived
- Step 4 raises on a missing/incomplete contract
- Plots, tables and console logs land in `pipeline_step_outputs/`
- Parity check passes with explicable differences
- Old tree retired; 32 files → 11
- P0033 unblocked

## Open decisions

### DEC-ALIAS — unify the three cross-category spelling variants? (Brian)

Three measures arrive under different names per category, confirmed identical by
metadata description (F41):

| Measure | CSD | Energidrikke | RTD |
|---------|-----|--------------|-----|
| display **and** feature | `…_disp_feat` | `…_disp_feat` | `…_disp_and_feat` |
| display **without** feature | `…_disp_w_o_feat` | `…_disp_wo_feat` | `…_disp_wo_feat` |
| feature **without** display | `…_feat_w_o_disp` | `…_feat_wo_disp` | `…_feat_wo_disp` |

**Not decided here, because it is a modelling question**: renaming asserts the
measures are interchangeable across categories, which SRQ1's cross-category
ranking would then rely on.

| Option | Consequence |
|--------|-------------|
| **A — unify** to one canonical name | These become comparable features across 3 categories; assumes Nielsen computes them identically per category |
| **B — leave as-is** | Each spelling stays category-unique, so they can only be used within a category, never compared across |

Recommendation: **A**, if Nielsen's per-category definitions are genuinely the
same computation — the descriptions are byte-identical, which is evidence but not
proof. Cheap to reverse; the mapping would live in `pipeline_config`.

**Not blocking**: step 2's EDA is open-world and analyses whatever columns exist
under whatever names, so this can be settled any time before step 4.

**Warning for whoever implements it**: do NOT match on tokens.
`disp_w_o_feat` and `feat_w_o_disp` share every token and mean opposite things.

### Also open

- **F42** — RTD carries negative `weighted_distribution*` values (min −0.17) in
  columns documented as fractions 0–1. The positive-sales filter does not remove
  them. Clip / drop / leave? Needs a decision, deferred to step-2 EDA.
- **F39** — is `number_of_items_reach` intensive (current) or additive?

## Explicitly out of scope

- Building step 4 for the other three categories (that *is* P0033)
- The MIN_PERIODS threshold **decision** (P0036 task 8 — this plan only makes
  the value honestly derived and surfaces the distribution)
- DEC-HORIZON (P0037)
- Chapter numbers (P0034)

## Related

- P0036 — the plan this forked from; tasks 4, 6, 7, 8, 9, 11 remain there
- P0030 — consolidated the step scripts into the notebook; this reverses it with
  the duplication lesson applied
- P0027/P0029 — the drift these shared scripts are designed to prevent
- P0033 — unblocked by task 8
