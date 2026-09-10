---
name: worked-pass-step1-load-and-aggregate
description: RULE - Full-file contextual pass over step_1_load_and_aggregate.py, showing every verdict with literal before/after text. Reference example for the submission-export comment pass.
category: reference
applies-to: [P0054, submission-export skill]
triggers: [running the comment pass, checking pass quality]
created: 2026_09_10-16_10
updated: 2026_09_10-16_10
---

# Worked pass — `step_1_load_and_aggregate.py` (458 lines)

Read in full before any verdict. Marker inventory used only afterwards, as a
completeness check.

**Verdicts: 4 KEEP, 5 DELABEL, 4 DELETE, 2 FIX.** The two FIX items are the
ones a grep-driven pass would have shipped.

---

## FIX 1 — A section heading that is a corrupted duplicate

**Line 78.** This is a defect, not a style issue.

```python
# AGGREGATION SPEC -- column-discovery column discovery
```

"column-discovery column discovery" is a broken edit — a phrase replaced over
itself. It carries no marker, no date and no plan ID, so nothing in the marker
inventory points at it. Only reading finds it.

**After:**

```python
# AGGREGATION SPEC -- measures are discovered, not enumerated
```

The same corruption appears in the `discover_measures` docstring at line 195:

```python
	Column-discovery: a column the pipeline has never seen is included automatically,
```

`Column-discovery:` is a decision-code label ("DEC-DISCOVER-COLUMNS") with the
prefix filed off, leaving a term that means nothing to a reader. **After:**

```python
	A column the pipeline has never seen is included automatically and classified
	by `classify_measure`. Nothing is dropped for not being on a list.
```

---

## FIX 2 — A docstring stating the wrong horizon

**Line 128**, inside the `REQUIRED_MEASURES` comment:

```python
# predicts (Y = log1p(sales_units_{t+1}), see pipeline_config).
```

`t+1` is H=1. The primary reported horizon is H=3, and `pipeline_config.py`
says explicitly that its own `FORECAST_HORIZON = 1` is a default only, with the
resolved value written into the per-category contract. So this comment asserts a
horizon the pipeline does not fix here.

An assessor reading the data chapter (H=3) and then this file (t+1) finds a
contradiction. **After:**

```python
# The forecast target. Not a category capability -- it is what the pipeline
# predicts (Y = log1p of sales_units at the forecast horizon, resolved per
# category in the step 3 contract). Without it there is nothing to forecast, so
# its absence is an error rather than something to degrade around. This is the
# only column named explicitly, and it is named for its role, not its category.
```

---

## DELETE 1 — The `Logic:` block's decision codes and the port history

**Before** (lines 2–21):

```python
"""
Nielsen Preprocessing -- Step 1: Load, Merge and Aggregate

Shared across all categories; select with --category.

Input:  The 4 Nielsen view parquet files (validated by step 0)
Output: step_1_aggregate_bymonth.parquet  -- brand x month panel
        step_1_console.log, step_1_log.json

Logic:
  1. Load facts + the 3 dimension views
  2. Merge to row level
  3. Filter to the DVH EXCL. HD parent market  (DEC-SCOPE)
  4. Assert exactly one market survives       (fan-out guard)
  5. Filter to positive sales
  6. Aggregate to brand x period_year x period_month  (DEC-GRAIN)

Ported from the CSD notebook cells "Step 1" and "Step 2" (P0038 task 2),
which in turn came from pre_csd_1_load_and_aggregate.py.
"""
```

**After:**

```python
"""
Nielsen preprocessing, step 1: load, merge and aggregate.

Shared across all four categories; select one with --category.

Input:  the four Nielsen view parquet files, validated by step 0
Output: step_1_aggregate_bymonth.parquet -- the brand x month panel
        plus a console log and a timing log

Steps:
  1. Load the fact table and the three dimension views
  2. Merge to row level
  3. Filter to the DVH EXCL. HD parent market
  4. Assert exactly one market survives (fan-out guard)
  5. Filter to positive sales
  6. Aggregate to brand x year x month
"""
```

The two `DEC-` codes go; the steps they labelled read identically without them.
The port history goes entirely — a notebook and a file named
`pre_csd_1_load_and_aggregate.py` that the assessor cannot see.

---

## DELETE 2 — The root-finder's assistant reference

**Before** (lines 33–35):

```python
# Anchor on .env.example (committed; see .gitignore) rather than CLAUDE.md --
# the repo ships to assessors and should not advertise the assistant used.
# Walk from __file__, not cwd: cwd depends on where python was invoked.
```

The second clause is self-defeating: a comment explaining that the repo should
not advertise the assistant, by naming the assistant's file. **After:**

```python
# Anchor on a committed file at the repo root, and walk up from __file__ rather
# than from cwd, since cwd depends on where python was invoked.
```

This block appears in six shipped files with near-identical wording. All six get
the same treatment.

---

## DELETE 3 — The grain history

**Before** (lines 64–74):

```python
# ============================================================================
# GRAIN
# ============================================================================
# GRAIN HISTORY: SRQ1 scope is locked to brand x month only (DEC-GRAIN,
# 2026-07-12); the "bychain" and "byregion" grains were dropped to a documented
# limitation + future work, and their config entries removed (P0035, 2026-08-01).
# The parameter survives so a future grain can be registered -- do NOT resurrect
# the deleted PATHS helpers if one is.

GRAIN = "bymonth"
GROUP_KEYS: dict[str, list[str]] = {"bymonth": ["brand"]}
```

Every sentence is about deletions the assessor never saw, plus an instruction to
a future collaborator. But the code is genuinely odd without a word — a
one-entry dict looks like over-engineering. **After:**

```python
# ============================================================================
# GRAIN
# ============================================================================
# The modelling grain is brand x month. Kept as a parameter rather than inlined
# so a further grain can be registered here without touching the aggregation.

GRAIN = "bymonth"
GROUP_KEYS: dict[str, list[str]] = {"bymonth": ["brand"]}
```

Related, at line 332 — the same instruction inside a live error message:

```python
			f"Unknown grain {grain!r}. Valid grains: {list(GROUP_KEYS)}. "
			f"To add one, register it here -- do not reintroduce the PATHS "
			f"helpers removed by P0035."
```

**After:**

```python
			f"Unknown grain {grain!r}. Valid grains: {list(GROUP_KEYS)}. "
			f"To add one, register it in GROUP_KEYS."
```

Error strings are where meta most often survives a pass, because they do not
read like comments.

---

## DELETE 4 — The notebook's five columns, and the F-class aside

**Before** (lines 80–102), 23 lines. **After**, 10 lines:

```python
# Measure columns are discovered from the merged frame rather than enumerated.
#
# The four category views carry 35 distinct measure columns between them, and
# availability differs by category. The same measure is also spelled
# differently across categories:
#     weighted_distribution_disp_w_o_feat   (CSD)
#     weighted_distribution_disp_wo_feat    (Energidrikke, RTD)
#     weighted_distribution_disp_and_feat   (RTD)
# A fixed column list cannot express either kind of variation, so it would
# silently drop measures; discovery handles all three spellings without
# naming any of them.
```

Gone: the notebook's five hardcoded columns, "the same defect class as F28/F38:
an inherited literal wearing the appearance of a decision", the measurement
date, and `P0036 task 11`.

Kept: the design decision and its concrete evidence. **This is the strongest
comment in the file and it survives nearly intact.**

---

## DELABEL 1 — The scope measurement table

**Before** (lines 234–251):

```python
# DEC-SCOPE (P0036, 2026-08-11): market scope is the DVH EXCL. HD *parent*,
# not its 9 regional children. This reverses P0026's region choice.
#
# P0026 chose the 9 children to avoid double-counting, which is correct when
# SUMMING markets -- but selecting the parent alone avoids it equally well,
# since parent and children are alternative views of the same universe.
#
# Measured at brand x month (the modelling grain), parent vs children:
#   - promo columns : ~23,400 nonzero  vs  0  <- decisive; the whole promo
#                     feature family is empty at region scope
#   - distinct brands: 140 vs 140      <- no brand loss
#   - brand-month rows: 3,917 vs 3,975 <- costs 1.5%, not a gain
#   - fact rows      : 37,999 vs 243,691 <- children repeat each brand-period
#                     9x, inflating row count without adding information
#
# Net: costs 1.5% of brand-month rows, buys the entire promo feature set.
# The ID itself lives in pipeline_config (more than one step names it).
```

**After:**

```python
# Market scope is the DVH EXCL. HD parent market, not its nine regional
# children. Selecting the parent alone avoids double-counting just as
# effectively as summing the children, since the two are alternative views of
# the same universe.
#
# Measured at brand x month, parent against children:
#   - promo columns   : ~23,400 nonzero  vs  0   <- decisive; the whole promo
#                       feature family is empty at region scope
#   - distinct brands : 140 vs 140               <- no brand loss
#   - brand-month rows: 3,917 vs 3,975           <- costs 1.5%
#   - fact rows       : 37,999 vs 243,691        <- children repeat each
#                       brand-period nine times, adding no information
#
# Net: 1.5% of brand-month rows for the entire promotional feature set. The
# market ID lives in pipeline_config, since more than one step names it.
```

Only the label and the "reverses P0026" sentence go. **This is exactly the kind
of comment an assessor rewards** — a design choice with the measurement behind
it — and it must not be shortened for tidiness.

---

## DELABEL 2 — The spelling-variant table

**Before** (lines 141–160): opens `# --- per-category spelling variants (P0038,
2026-08-18) ---`, then explains that step 6's `--check-consistency` found the
problem, gives before/after feature counts (23 common, 41 each for CSD and
Energidrikke), and cites `DEC-DISCOVER-COLUMNS`.

**After:**

```python
	# --- per-category spelling variants ---------------------------------
	# Nielsen spells the same three display/feature measures differently per
	# category. Left uncanonicalised they present as six distinct features, so
	# any cross-category comparison misreports what the categories share:
	#
	#   measure                  CSD            Energidrikke   RTD
	#   display AND feature      disp_feat      disp_feat      disp_and_feat
	#   display WITHOUT feature  disp_w_o_feat  disp_wo_feat   disp_wo_feat
	#   feature WITHOUT display  feat_w_o_disp  feat_wo_disp   feat_wo_disp
	#
	# This is a naming difference, not a capability difference. The canonical
	# form spells out "and"/"without": "disp_feat" does not say whether it means
	# the conjunction or the pair, and "w_o" must be decoded by the reader.
```

The feature counts go — they are a before/after of our own fix, and they would
need re-verifying against the current 18-feature set to stay true.

---

## DELABEL 3, 4, 5 — Three short ones

| Line | Before | After |
|---|---|---|
| 184 | `Generalised from the notebook's promo-only \`lambda x: sum(pd.Series(x).fillna(0))\`: the null-means-zero convention is a property of...` | `The null-means-zero convention is a property of how Nielsen encodes additive measures, not of the promo columns specifically.` |
| 284 | `Measured 2026-08-12: all four categories have 0 duplicate market_ids today, so this is a regression guard, not a fix for a live defect.` | `All four categories currently have no duplicate market IDs, so this is a regression guard rather than a fix for a live defect.` |
| 304 | `...silently multiply every downstream SUM() -- the 6.16x defect P0027 found. Assert == 1, not > 0.` | `...silently multiply every downstream sum. Assert exactly 1, not greater than 0.` |

The 6.16x figure is a measured defect from our history. It goes because it
describes a bug the assessor never saw — but the *guard* and the reason it
asserts equality stay, which is the useful half.

---

## KEEP — four blocks, unchanged

These are why the file reads as considered work. **Touching them would be the
pass doing damage.**

| Lines | What |
|---|---|
| 110–125 | Additive vs intensive aggregation, with the "70% + 70% is not 140%" example. Explains the whole `INTENSIVE_PATTERNS` design. |
| 259–266 | Predicate pushdown: 10.3M rows, ~2% survive, 2.6 GB dense, ArrowMemoryError on a 15.8 GB machine, ~46x smaller working set. Genuine engineering, and it explains why the later pandas filter is deliberately kept. |
| 218–223 | Why additive measures use NaN-as-zero and intensive ones keep pandas' NaN-skipping mean. |
| 302–309 | The two-guard argument: `nunique()` catches distinct IDs, `validate="m:1"` catches same-ID duplicates, neither alone is sufficient. |

The 259–266 block does carry a date ("measured 2026-08-12"). Strip the date,
keep every number.

---

## Result

458 lines to roughly 430. The file gets **more** trustworthy, not thinner: two
factual defects fixed, four history blocks removed, and every piece of
engineering reasoning intact.
