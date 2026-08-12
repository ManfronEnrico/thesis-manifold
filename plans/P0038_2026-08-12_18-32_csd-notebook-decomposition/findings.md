---
pid: P0038
created: 2026-08-12 18:32:00
updated: 2026-08-12 18:32:00
---

# P0038 Findings

Measurements taken 2026-08-12 during the decomposition design session.
Findings are numbered continuing from P0036 (F1–F25) to keep cross-references
unambiguous across the two plans.

---

## F26 — Only six parameters cross the EDA → pipeline boundary

**How measured**: AST parse of every code cell in the notebook, collecting
`Name` nodes by context (`Store` vs `Load`), then intersecting names defined in
EDA cells (17–53) against names read in pipeline cells (56–64).

| Name | Defined in cell | Read in cell(s) |
|------|-----------------|-----------------|
| `LAGS` | 41 | 60 |
| `ROLLING_WINDOWS` | 45 | 60 |
| `holiday_months` | 31 | 60 |
| `log_necessary` | 25 | 60 |
| `train_end_year` / `train_end_month` | 47 | 62 |
| `val_end_year` / `val_end_month` | 47 | 62 |
| ~~`c`~~ | 51 | 56, 60, 64 |
| ~~`grp`~~ | 29 | 60 |
| ~~`months`~~ | 33 | 56 |

The last three are **leaked loop variables**, not intentional state — they
happen to be in scope because notebook cells share one namespace. A script
decomposition drops them naturally (each script has its own namespace), which
is a correctness *gain*: any pipeline cell genuinely depending on a stray loop
variable would be a bug.

**Why this matters**: the earlier concern that a script split would require a
sprawling JSON contract (and would therefore re-hardcode values, the way
`pre_csd_5_apply_split.py` once did) was **overstated**. Six values is small
and tractable.

---

## F27 — The contract file already exists; it is simply never read back

`{category}_eda_findings.json` is written at notebook cell 53
(export line 1662). It already carries every parameter in F26, each paired
with a `_rationale` string:

```
parameters:
  MIN_PERIODS + MIN_PERIODS_rationale
  LAGS + LAGS_rationale
  ROLLING_WINDOWS + ROLLING_WINDOWS_rationale
  HOLIDAY_MONTHS + HOLIDAY_MONTHS_rationale
  LOG_TRANSFORM_NECESSARY
  TRAIN_END + TRAIN_END_rationale
  VAL_END + VAL_END_rationale
```

Step 4 never opens it — it takes the values in-memory from the shared notebook
namespace. So the JSON is a *report*, not an *interface*.

**Implication**: making the split honest is mostly making step 4 read a file
that is already produced, rather than designing a contract from scratch. The
`_rationale` fields additionally give Ch4's parameter table a direct source.

---

## F28 — Two contract fields look derived but are not

**`TRAIN_END` / `VAL_END`** — notebook cell 47 computes them from
`train_periods = 24` / `val_periods = 6`, i.e. **absolute month counts**, with
test as the remainder. Every newly arrived month therefore lands in test.

**`MIN_PERIODS`** — written as the literal `40` (export line 1612), while its
adjacent rationale string cites a computed `brands_40` and reads as though the
number were derived. `filter_series` at step 4.2 then describes it as coming
"from EDA Step 3.05".

Both are the same defect class: **a value that looks derived but is not**, with
a rationale string lending false confidence. This is precisely why P0036 F25's
split drift went unnoticed for months.

Brian, 2026-08-12: *"the min periods should be data based and read from a
previous EDA step."*

---

## F29 — P0036 F25 was measured on the wrong pathway for CSD

**Correction to P0036 F25.** That finding reported CSD splitting **63/13/24**
and attributed it to `DEFAULT_TRAIN_END`/`DEFAULT_VAL_END`. Both parts are wrong
for CSD.

Two distinct pathways exist, and F25 conflated them:

| Pathway | Used by | Mechanism |
|---------|---------|-----------|
| A | CSD notebook | absolute counts (train=24, val=6), test = remainder |
| B | Danskvand / Energidrikke / RTD step scripts | fixed dates (2025-02 / 2025-08) |

Measured on the fresh 2026-07 extract:

| Category | Pathway A (counts) | Pathway B (dates) |
|----------|--------------------|--------------------|
| CSD | **52/13/35** | 63/13/24 |
| Danskvand | 59/15/27 | 59/15/27 |
| Energidrikke | 56/14/30 | 60/14/26 |
| RTD | 59/15/27 | 59/15/27 |

CSD actually runs pathway A, so its real split is **52/13/35** — worse than F25
reported. The notebook's own last-run output confirms it independently:
`{'train': 1450, 'test': 754, 'val': 348}` = **57/14/29** (differing from 52/13/35
because row counts weight brands with unequal panel depth, whereas the period
count is unweighted).

**Both mechanisms are broken, for the same underlying reason**: any cutoff fixed
in absolute terms (a date *or* a count) sends every newly arrived month to
whichever split is defined as "the remainder". The re-pull added 2–4 months and
pushed all of them into test.

Proportional cutoffs on each category's own sorted period list fix both:

| Category | Periods | Proportional 70/15/15 | train_end | val_end |
|----------|---------|----------------------|-----------|---------|
| CSD | 46 | 32/7/7 → 70/15/15 | 2025-05 | 2025-12 |
| Danskvand | 41 | 29/6/6 → 71/15/15 | 2025-07 | 2026-01 |
| Energidrikke | 43 | 30/6/7 → 70/14/16 | 2025-06 | 2025-12 |
| RTD | 41 | 29/6/6 → 71/15/15 | 2025-07 | 2026-01 |

---

## F30 — CSD's orchestrator is broken: it points at deleted step scripts

`CSD/preprocessing_csd.py` (210 lines) is a live orchestrator with a full CLI
(`--run-step N`, `--grain`, `--re-cache`, `--run-raw`). It `subprocess`-invokes
`pre_csd_1_load_and_aggregate.py` … `pre_csd_6_save_outputs.py` from
`pipeline_step_scripts/`.

**Those files do not exist.** P0030 deleted them when the notebook absorbed
their logic. The directory holds only the notebook and its 2026-08-12 export:

```
CSD/pipeline_step_scripts/
  pre_processing_notebook_csd.ipynb
  pre_processing_notebook_csd.py
```

So `python preprocessing_csd.py` fails at step 1 today.

**Implication**: CSD is not "notebook instead of scripts" — it is a notebook
*plus a dead entry point*. The decomposition **repairs** an existing broken
orchestrator rather than adding an eleventh one. This removes the main
structural objection to splitting.

The other three categories are intact (7 step scripts + orchestrator each).

---

## F31 — The three working orchestrators are name-only copies

| File | Lines |
|------|-------|
| `CSD/preprocessing_csd.py` | 210 (broken, has extra `--grain` docs) |
| `Danskvand/preprocessing_danskvand.py` | 184 |
| `Energidrikke/preprocessing_energidrikke.py` | 184 |
| `RTD/preprocessing_rtd.py` | 184 |

`diff Danskvand/… RTD/…` returns **only**: the category constant, the four
parquet filenames (`{cat}_clean_*_v.parquet`), and usage strings echoing the
script's own filename. Zero logic differences.

This is direct evidence for Brian's duplication argument: the copies exist
because each category got its own file, not because the categories differ. One
shared orchestrator with `--category` replaces all four with no loss.

---

## F32 — `base_preprocessing.py` is a utility library, not a third pipeline

Checked because a third live entry point would have disrupted the plan.
`_shared_modules/base_preprocessing.py` contains only helpers
(`validate_input`, `get_required_jsonl_files`) and no orchestration or
`__main__`. **No conflict** — it stays as-is.

---

## F33 — Notebook cell inventory (65 cells, 75,879 source chars)

| Cells | Section | Chars | Destination |
|-------|---------|-------|-------------|
| 3–10 | Setup, imports, root, paths, cache validation | ~6.2k | shared `step_0` |
| 12–14 | Load views, merge, aggregate | ~6.6k | shared `step_1` |
| 17–39 | Descriptive EDA (3.01–3.12) | ~24k | shared `step_2` |
| 41–53 | Param derivation (3.13–3.19) | ~22k | shared `step_3` |
| 56–60 | Calendar, filter, engineer | ~8.7k | **per-category** `step_4` |
| 62 | Apply split | 1.3k | shared `step_5` |
| 64 | Save outputs | 2.8k | shared `step_6` |

The largest single cell is 4,800 chars (cell 60, feature engineering) — all are
comfortably editable once separated. The 57,814-token wall is purely an artifact
of the `.ipynb` JSON envelope plus committed outputs.

**Plots already save to disk**: 8 `savefig` calls to `OUTPUT_PLOTS_DIR` at
DPI 150, each guarded by `if OUTPUT_PLOTS_DIR.exists()`. Console output and
printed DataFrames are *not* captured — that is the gap task 1 fills.

---

## F34 — Everything is already keyed on `CATEGORY`

The notebook derives every path from `CATEGORY = "CSD"` via
`get_category_pipeline_step_outputs_dir(CATEGORY)` and
`THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / CATEGORY / "views"`.

Parameterising on `--category` is therefore mostly mechanical: replace one
constant with an `argparse` value. No hardcoded absolute paths survive in the
export (the last one was removed during P0036 task 3).

**Caveat**: two output names hardcode the lowercase category —
`"csd_eda_findings.json"` and `"csd_eda_plots"` (export lines 111–112). These
must become f-strings, or the shared script will overwrite CSD's artifacts when
run for another category.

**RESOLVED 2026-08-12 (task 1).** Both are now f-strings on the category slug,
produced by `pipeline_config.get_paths()`. A regression test asserts the four
categories' `findings_json` / `plots_dir` names are pairwise distinct, so a
future edit that reintroduces a literal fails the test rather than silently
overwriting CSD's artifacts.

---

## F35 — Cells 3–10 are not one step; they are config + one step

Discovered while porting. The notebook's "Step 0" cells contain four distinct
concerns, only one of which is actually step 0's job:

| Concern | Belongs to |
|---------|-----------|
| Cache validation | step 0 |
| ML target definition (`TARGET_COL`, `WARMUP_PERIODS`, …) | **every** step |
| Plot styling (`DPI`, `PALETTE`, `FIGSIZE_*`) | steps 2, 3 |
| Path derivation | **every** step |

In the notebook this distinction did not matter — one shared cell namespace made
all four visible everywhere for free. In a script decomposition it matters a
great deal: three of the four concerns have to reach steps 1–6 somehow.

Left inside `step_0`, the only ways to share them are re-declaration per step or
importing from a step script. **Re-declaration is the exact copy-paste mechanism
that produced the P0027/P0029/P0030 drift this plan exists to remove.**

Hence `pipeline_config.py`, holding everything category-keyed but step-agnostic.
This was not in the plan; the plan assumed cells 3–10 mapped 1:1 onto step 0.

**Generalises to the remaining ports**: before moving a cell block into a step,
check whether the notebook's shared namespace was doing invisible work. The same
question applies to the EDA cells feeding step 4.

---

## F36 — The notebook's cache validation cannot detect a truncated file

`validate_parquet_cache` in the notebook (export lines 174–199) tests
`.exists()` only. A parquet file written by an interrupted conversion run is
present but 0 bytes: it passes validation, then fails inside `pd.read_parquet`
at step 1 with an opaque Arrow error naming neither the cause nor the fix.

The ported version checks `st_size == 0` as a distinct outcome from missing, and
reports the two separately (`"[RTD] 2 missing and 1 empty of 4 …"`).

This is a genuine capability gain, not just a port — worth noting because the
decomposition's stated goal is "no degradation", and this is the first place the
split produced an actual improvement rather than parity.

---

## F37 — The fan-out guard does not catch the fan-out it was written for

**Measured 2026-08-12 while porting step 1.** The `_n_markets != 1` guard —
the fix for P0027's 6.16× double-count — tests
`merged["market_id"].nunique()`. That counts distinct **ids**, but a fan-out is
row **multiplication**. The two come apart:

| Defect shape | Rows multiplied? | `nunique()` | Guard fires? |
|---|---|---|---|
| Two *distinct* market ids survive the filter | yes | 2 | **yes** |
| `dim_market` holds the parent id on *two rows* | yes | **1** | **no** |

Reproduced directly: one fact row joined against a `dim_market` carrying
`market_id=1256338` twice (differing only in `market_description`, e.g.
`"DVH EXCL. HD"` vs `"DVH EXCL HD"`) yields **2 merged rows**, `nunique()==1`,
and the guard stays silent. Every downstream `SUM()` is then doubled — the exact
P0027 failure the guard exists to prevent.

**Not currently triggered.** All four categories' `dim_market` tables have 86
rows and **0 duplicate ids** today, with exactly 1 row for the parent. So this
is a latent gap, not a live defect — the current numbers are trustworthy.

**Closed** by adding `validate="m:1"` to all three dimension merges, which makes
pandas raise `MergeError` if any dimension table carries a duplicate join key.
Verified: duplicate `dim_market` rows and duplicate `dim_product` rows both now
raise; the clean path is unchanged.

Both halves are needed. `validate="m:1"` catches same-id row duplication;
`nunique() != 1` catches distinct ids surviving the filter. Neither alone is
sufficient.

**Re-run confirms zero behavioural change**: CSD 4,209 / Danskvand 1,225 /
Energidrikke 1,702 / RTD 2,509 rows before and after.

---

## F38 — `min_periods` has two disagreeing values, and step 1 held the unused one

Surfaced by the step-1 parity check. The notebook's `GRAIN_CONFIG` (cell 14)
declares `min_periods: 40` with a detailed rationale string. But the actual
consumer, `filter_series()` in `engineer_features.py`, takes
`min_periods: int = DEFAULT_MIN_PERIODS` — and `DEFAULT_MIN_PERIODS = 30`.

So there are two numbers:

| Location | Value | Used? |
|---|---|---|
| notebook `GRAIN_CONFIG["bymonth"]["min_periods"]` | 40 | declared in step 1, never passed to step 4 |
| `engineer_features.DEFAULT_MIN_PERIODS` | 30 | **the value that actually filters** |

This compounds F28. F28 established that `MIN_PERIODS: 40` in the contract JSON
is a hardcoded literal wearing a derived-sounding rationale. F38 adds that the
literal is not even the number in force — the pipeline filters at 30 while the
documentation, the contract, and the rationale all say 40.

**Deliberately not fixed in step 1.** `min_periods` is a *filtering* parameter,
so it belongs to the step-3 contract and step-4 filter, not to aggregation. It
was dropped from step 1's config rather than carried, and task 4 must derive it
honestly and pass it explicitly to `filter_series`.

**Task 4 acceptance criterion**: after the port, exactly one value governs, it is
derived from the brand-depth distribution, and it is passed explicitly rather
than inherited from a default.

---

## F39 — The notebook silently discarded 24 of 29 available measure columns

**Brian, 2026-08-12**, on the promo-column handling:

> *"why is that even an issue exactly? I thought we wanted to have a general
> script that is category independent... Couldn't we have this also dynamic?"*

Correct, and following it up exposed something larger than the promo question.

The notebook's `agg_dict` names **five** measure columns. The fact views actually
carry **29 measures for CSD** (35 distinct across all four categories). So 24
columns per category never reached the panel — including the entire `baseline_*`
family (6 columns), the `numeric_distribution` family, `universe_number_of_stores`
and `sales_units_any_tpr`.

They were not evaluated and rejected. The notebook listed five, and the list was
inherited unexamined through every subsequent port. **Same defect class as F28
and F38**: an inherited literal wearing the appearance of a decision.

### Column availability is not just presence/absence

A fixed list cannot express what the data actually does, because the *same
measure is spelled differently per category*:

| CSD | Energidrikke | RTD |
|-----|--------------|-----|
| `weighted_distribution_disp_w_o_feat` | `weighted_distribution_disp_wo_feat` | `weighted_distribution_disp_wo_feat` |
| `weighted_distribution_feat_w_o_disp` | `weighted_distribution_feat_wo_disp` | `weighted_distribution_feat_wo_disp` |
| — | — | `weighted_distribution_disp_and_feat` |

Any hardcoded list keeps whichever spelling it happens to name and drops the
rest, per category, invisibly.

### Fix: open-world discovery

Measures are now **discovered** — every numeric column that is not a join key —
and classified by what the measure *is*:

- **additive** (`sum`): counts and volumes; a brand's total is the sum of its products
- **intensive** (`mean`): rates, ratios, distributions, per-store averages. Summing
  a 70% weighted distribution with another 70% does not give 140%.

Matched on substrings (`distribution`, `avg_`, `universe_`, `_reach`) so a
newly-arrived Nielsen column is classified by semantics rather than needing to be
added to a list. All 29 CSD classifications reviewed individually and correct.

### Result

| Category | Panel cols before | after |
|----------|-------------------|-------|
| CSD | 8 | **32** |
| Danskvand | 7 | **15** |
| Energidrikke | 8 | **32** |
| RTD | 7 | **31** |

Row counts, brand counts and period counts **unchanged** — this adds columns
without disturbing the grain.

### The one column that stays named

`sales_units` is the only explicitly required column, and it is required for its
**role, not its category**: it is the forecast target
(`Y = log1p(sales_units_{t+1})`). Absent, there is nothing to predict and every
later step is meaningless, so it raises rather than degrades. This is not a
category-capability check — a category lacking it is not a category with fewer
features, it is not a forecasting dataset.

### Bearing on P0036 task 11

Task 11 ("recover discarded product-dimension features") is **partly resolved**
at the step-1 level: measures are no longer dropped on the way into the panel.
What remains for task 11 is genuinely product-*dimension* attributes (pack size,
flavour etc. from `dim_product`), which is a different question from the fact
measures addressed here.

### Open question, deliberately not settled

`number_of_items_reach` is classified intensive (mean). It is a count, which
argues additive, but `_reach` metrics are typically already de-duplicated across
products, so summing would double-count. Mean is the safer default. Flagged for
step-2 EDA to confirm empirically rather than asserted here.
