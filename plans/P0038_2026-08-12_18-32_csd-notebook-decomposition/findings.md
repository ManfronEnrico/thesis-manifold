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

---

## F40 — The forecast target is present verbatim in all four categories

**Brian, 2026-08-12:**

> *"which dataset does not have sales units? Are you certain that is the case or
> did you simply try to match verbatim on the wording, but perhaps that dataset
> has a sales column, just not with the same name?"*

Fair challenge — the F39 work matched on names only. Checked properly against
the metadata this time.

**Answer: no category is missing it.** `sales_units`, `sales_value` and
`sales_in_liters` are present verbatim in all four. 35 sales-like candidate
columns were tested by name *and* by metadata description against
`sales|volume|units|qty|quantity|turnover|revenue|value|liter|litre|amount`;
none is an alias for the target in a category that lacks it.

So `REQUIRED_MEASURES` never fires today. It stays as a guard against a future
delivery, but it is not a live constraint — worth stating plainly, because the
earlier framing implied some category was at risk of tripping it.

---

## F41 — Three confirmed alias groups, verified by metadata not by name

The same measure is delivered under different spellings per category. Confirmed
by **byte-identical metadata descriptions**, not name similarity:

| Measure | CSD | Energidrikke | RTD | Danskvand |
|---------|-----|--------------|-----|-----------|
| display **and** feature | `…_disp_feat` | `…_disp_feat` | `…_disp_and_feat` | — |
| display **without** feature | `…_disp_w_o_feat` | `…_disp_wo_feat` | `…_disp_wo_feat` | — |
| feature **without** display | `…_feat_w_o_disp` | `…_feat_wo_disp` | `…_feat_wo_disp` | — |

Value distributions corroborate: medians 0.059/0.060, 0.039–0.081, 0.145–0.175
across the spellings.

### Deliberately NOT merged — DEC-ALIAS is open

Unifying these is a **modelling** decision, not a porting detail: it asserts the
measures are interchangeable across categories, which affects any cross-category
comparison SRQ1 makes. Reported, not silently renamed. **Brian's call.**

### A token-based matcher is not sufficient — one false positive

`weighted_distribution_disp_w_o_feat` and `weighted_distribution_feat_w_o_disp`
contain **the same tokens** but mean **opposite** things (display-without-feature
vs feature-without-display). My first automated pass paired them. Alias detection
must read the descriptions; names alone will produce wrong merges.

### Coverage

| Present in | Columns |
|---|---|
| all 4 | 35 |
| 3 | 17 |
| 2 | 14 |
| 1 | 35 |

Artifacts: `_shared_modules/build_feature_inventory.py` (re-runnable),
`nielsen_feature_inventory.csv`, `user-docs/reference/nielsen-feature-inventory.md`.

---

## F42 — Negative values exist in every category's sales measures

Surfaced while validating F41's distributions.

| Scope | Columns affected | Rate | Extreme |
|-------|------------------|------|---------|
| All 4 categories | `sales_value`, `sales_units`, `sales_in_liters` | 0.02–0.06% | −27,266 (RTD value) |
| CSD/Ene/RTD | promo + tpr variants | 0.01–0.05% | −217,242 (RTD tpr) |
| **RTD only** | 9 × `weighted_distribution*` | 0.01–0.04% | **−0.1745** |

The sales negatives are returns / Nielsen restatements, and step 1's
`sales_units > 0` filter removes those rows before aggregation — so the panel is
unaffected.

**The RTD distribution negatives are different** and worth flagging: those
columns are documented as "fraction 0–1", and a row can carry a negative
distribution while still having positive `sales_units`, so the positive-sales
filter does **not** remove it. Rare (≤0.04%), but it means a distribution
feature can be negative where the metadata says it cannot.

Not acted on — it needs a decision (clip at 0? drop? leave?) rather than a
silent fix. Flagged for step-2 EDA.

---

## F43 — Metadata JSONL and parquet metadata are identical; JSONL is now the source

Brian, 2026-08-12: *"i hope you read each and every metadata file such as
`metadata_csd_columns.jsonl`"*

The first inventory pass read the **parquet** metadata under `_01_converted/`,
not the delivered JSONL under `_00_raw/`. Verified before rebuilding:

| Check | Result |
|-------|--------|
| Column sets per category | identical (70 / 54 / 72 / 70) |
| Field contents (`data_type`, `unit`, `null_meaning`, `description`) | **266 field-sets compared, 0 differences** |

So nothing was wrong in the earlier output — but the generator now reads the
**JSONL** regardless. It is the delivered artifact; the parquet is a Stage-1
conversion of it, and reading the source directly means the inventory cannot
silently inherit a conversion defect.

---

## F44 — 52 columns are stored with a dtype contradicting their documented type

Surfaced by the rebuilt inventory. Two distinct classes:

**Foreign keys documented `string`, stored `int64`** (`market_id`, `period_id`,
`product_id`, `product_hierarchy_number`, `product_hierarchy_level`) — 8 per
category. Harmless for joining, since both sides converted consistently, but a
leading zero would already have been lost at Stage-1. Worth knowing before
anyone treats an ID as text.

**Columns that are 100% NULL** — `market_hierarchy_{level,number,name,column}`
in all four (Nielsen's own `null_meaning` documents these as a known upstream
issue), plus `controlled_label` (CSD/Danskvand/Energidrikke) and
`energy_drinks` (Energidrikke).

The all-null case also caused a **reporting bug**, now fixed: pandas types an
all-null column as `float64` regardless of content, so the report labelled
documented `string` columns as numeric. The generator now trusts the metadata
for `kind` when a column is entirely null.

---

## F45 — CSD has 508,714 NULL `sales_units` (4.9%); the other three have none

Surfaced by the per-category target table. Investigated:

- all 508,714 also have NULL `sales_value` (jointly missing, not partial)
- they span 7,691 of 8,881 distinct products
- **254,463 are UPC-level rows**; the other 254,251 have **no `dim_product`
  match at all** — the same orphan-row issue as P0036 F10

**Not a defect for the panel.** Step 1 filters to `sales_units > 0`, so NULL
rows never reach the brand×month grain, and the modelling grain is brand-level
where these UPC rows aggregate away. Recorded because a 4.9% null rate in the
forecast target looks alarming in isolation and will be asked about again.

---

## F43 — step 1 read 10.3M rows to keep 223k; predicate pushdown, not a tuning knob

`load_merged()` called `pd.read_parquet()` on the full facts table and applied
the DEC-SCOPE market filter afterwards. Measured on CSD: **10,311,342 rows ×
32 float64 columns**, 767.5 MB compressed, ~818 MB uncompressed columnar,
~2.6 GB as a dense pandas frame — plus pyarrow's conversion copy, roughly 5 GB
peak against **2.0 GB free of 15.8 GB**. Result: `ArrowMemoryError`.

Share of rows surviving the filter, measured per category:

| Category | Total rows | Parent-market rows | Share |
|----------|-----------:|-------------------:|------:|
| CSD | 10,311,342 | 223,240 | 2.16% |
| Danskvand | 1,382,673 | 27,449 | 1.99% |
| Energidrikke | 3,476,121 | 55,216 | 1.59% |
| RTD | 2,409,362 | 49,976 | 2.07% |

~98% of every read was being materialised only to be discarded. Fixed by
pushing the predicate into the reader. Step 1 for CSD: **6.5 s**, output
unchanged (142 brands / 4,209 rows / 46 periods).

**Why this was latent rather than new**: step 1 had run successfully earlier
the same day. The fragility was always there; it surfaced when free memory
dropped. A pipeline whose success depends on how much RAM happens to be free
is not reproducible, which matters more than the speed gain.

---

## F44 — the notebook's EDA was already lossy before decomposition

The notebook header advertises "**14 visualizations**". Eight PNGs exist on
disk, and only seven have surviving source cells — the cell that produced
`02_ecdf_distributions.png` had been deleted while the PNG remained.

So a stale-plot problem predates this decomposition: the notebook was already
emitting artifacts it could no longer regenerate. Recovered as section 3.15
rebuilt from the documented intent, not from source.

**Implication for task 9 (retirement)**: the notebook cannot be treated as the
authoritative record of what the EDA did. Where a plot exists without source,
step 2 is now the authority.

---

## F45 — the per-category scripts are duplicates, but they never did EDA

Checked against Brian's recollection that the per-category scripts were stale
EDA duplicates. Half right:

- The three working orchestrators are **byte-identical after normalising the
  category name** — verified by diffing sed-normalised copies, zero output.
  Duplication confirmed; DEC-SHARED-SEAM is the right response.
- But **none of the 24 per-category scripts imports matplotlib**. They do no
  EDA whatsoever. The other three categories had no EDA to be stale.

**Numbering hazard for task 9**: the old and new step numbers do not mean the
same thing. Old `pre_{cat}_2_build_calendar.py` vs new `step_2_eda_descriptive`;
old `_3_filter_series` vs new `step_3_derive_params`. Retirement must match on
filename, never on step number.

---

## F46 — F7's redundancy question now has a standing measurement

Section 3.18 emits `step_2_18_redundant_pairs` for every |r| > 0.9 column pair.
CSD lands **13 pairs** above that threshold, including
`sales_in_liters_any_promo` ↔ `sales_units_any_tpr` at 0.9400 and
`weighted_distribution_any_promo` ↔ `weighted_distribution_any_tpr` at 0.9374.

This is a stricter bar than the 0.756 `weighted_dist` correlation P0036 F7 is
tracking, so it does not resolve F7 — but the pairs listed here are a stronger
claim, and the table regenerates on every run rather than being a one-off
measurement. Feeds P0036 task 7.

---

## F47 — brands retained is the wrong objective; training rows is the right one

The retention curve reports brands surviving each MIN_PERIODS threshold, and reads as a
straight trade-off: higher threshold, fewer brands. That framing is misleading, because a
pooled model consumes **rows**, and short brands contribute almost none.

    usable_rows(brand) = n_months(brand) - MAX_LAG - HORIZON

At `MAX_LAG = 13, HORIZON = 1`, a brand with 14 months yields `14 - 13 - 1 = 0` rows. It
appears in the brand count and contributes nothing to training.

Measured consequence (`minperiods_tradeoff.py`, 2026-08-18) — CSD at lag-12:

| MIN_PERIODS | Brands | % brands | Training rows | % of max |
|------------:|-------:|---------:|--------------:|---------:|
| 0 | 142 | 100.0% | 2,467 | 100.0% |
| 15 | 106 | 74.6% | **2,467** | **100.0%** |
| 20 | 89 | 62.7% | 2,429 | 98.5% |
| 30 | 79 | 55.6% | 2,315 | 93.8% |
| 40 | 62 | 43.7% | 1,961 | 79.5% |

Dropping 36 brands (25% of the panel) costs **zero** training rows. The same pattern holds
in all four categories.

**Implication beyond MIN_PERIODS**: any argument phrased in terms of brand counts —
coverage, representativeness, category comparability — should be re-checked in row terms
before it is trusted. Brand counts and row counts do not move together.

---

## F48 — forecast horizon and lag depth are separable levers, and were being conflated

The proposal was to shorten the forecast horizon to gain training periods. The arithmetic
does not support it: horizon enters `usable_rows` as a subtraction of 1 versus 6, whereas
**lag depth** is what moves row counts materially.

CSD training rows at the minimum viable threshold for each lag structure:

| Structure | Warm-up | MIN_PERIODS floor | Training rows | vs lag-12 |
|-----------|--------:|------------------:|--------------:|----------:|
| lag-12 | 13 | 15 | 2,467 | — |
| lag-6 | 7 | 9 | 3,157 | +28% |
| lag-3 | 4 | 6 | 3,533 | +43% |

So the gain the proposal sought is real but comes from **reducing lag depth**, not from
shortening the horizon. The two are independent parameters in the contract and should be
reasoned about separately.

Rejected here because EDA 3.16 measures lag 12 as significant across the majority of
leading brands. Retained as future work / sensitivity analysis.

---

## F49 — warm-up does not exist at serving time; the real constraint is cold start

Warm-up is the set of rows at the start of a brand's own series whose lag features point
before the data begins. It is a **training-time** property, not a runtime phase, and not a
fourth split alongside train/validation/test.

At serving, `forecast_service.py` builds the next-step feature row from the most recent
stored values — there is nothing to warm up, because nothing is being trained. This is
consistent with the SRQ2 design: the LLM emits a typed tool call and never assembles
feature vectors itself.

**The genuine serving consequence is different**: a brand with fewer than 15 months of
stored history cannot be forecast at all, because `lag_13` is undefined. That is a
*coverage* limit, not a delay. The service must return a typed "insufficient history"
response rather than a point estimate computed from a partially-null feature row.

**This strengthens the SRQ2 argument.** A structured tool interface can express refusal as
a typed response; a code-as-action baseline constructing features ad hoc has no equivalent
guarantee and may return a plausible-looking number instead. Explicit failure is part of
the reliability claim and is demonstrable rather than merely assertable.

Coverage gap to report (Ch7/Ch10): 25% of CSD brands, 45% of Danskvand brands fall below
the threshold.

---

## F50 — forecast horizon costs training rows twice, not once

Horizon enters the row budget through two independent channels, and only the first is
obvious:

1. `usable_rows(brand) = n_months - MAX_LAG - H` — one row lost per brand per step of H.
2. The target is `y_{t+H}`, so the final H months of every brand have no target at all.

Measured across all four categories (`horizon_tradeoff.py`, 2026-08-18):

| H | Training rows | vs H=1 | Brands kept |
|--:|--------------:|-------:|------------:|
| 1 | 5,332 | 100.0% | 258/366 |
| 3 | 4,832 | 90.6% | 230/366 |
| 6 | 4,159 | 78.0% | 211/366 |
| 12 | 2,942 | **55.2%** | 196/366 |

An annual horizon discards 45% of training data before modelling starts.

---

## F51 — predictability decays with horizon, so row loss and task difficulty compound

Row loss would be tolerable if the longer-horizon task were equally learnable. Measured
within-brand corr(y_t, y_{t+H}) and the naive-persistence RMSE in log space
(`horizon_signal.py`):

| H | Mean corr | Naive RMSE | CSD | Danskvand | Energidrikke | RTD |
|--:|----------:|-----------:|----:|----------:|-------------:|----:|
| 1 | 0.962 | 0.96 | 0.972 | 0.958 | 0.949 | 0.968 |
| 3 | 0.924 | 1.34 | 0.943 | 0.940 | 0.892 | 0.923 |
| 6 | 0.891 | 1.61 | 0.913 | 0.933 | 0.846 | 0.872 |
| 12 | 0.838 | 1.98 | 0.867 | 0.920 | 0.750 | 0.814 |

The error floor roughly doubles from H=1 to H=12. Fewer examples AND a harder target —
the effects compound.

Energidrikke decays fastest and Danskvand slowest, consistent with the volatility asymmetry
already documented. A single horizon choice is therefore not equally costly across
categories, though H=1 is optimal for all four.

---

## F52 — the binding constraint on horizon is the test window, not accuracy

The decisive measurement (`horizon_testwindow.py`). At 70/15/15 the test window is 6-7
months. A forecast origin is evaluable only if its target month falls inside that window,
giving `n_origins = n_test - H + 1`:

| Category | Months | Test | H=1 | H=3 | H=6 | H=12 |
|----------|-------:|-----:|----:|----:|----:|-----:|
| CSD | 46 | 7 | 7 | 5 | 2 | **0** |
| Danskvand | 41 | 6 | 6 | 4 | 1 | **0** |
| Energidrikke | 43 | 6 | 6 | 4 | 1 | **0** |
| RTD | 41 | 6 | 6 | 4 | 1 | **0** |

**H=12 has no evaluable origin in any category** — the horizon exceeds the whole test
window. H=6 leaves exactly one outside CSD: a point estimate of error with no distribution,
hence no confidence interval and no significance test.

This reframes the horizon question entirely. It is not "which horizon trains the best
model" but "which horizon can be *measured* on this extract". H=1 is the answer, and H=3 is
the robustness check.

**Implication for step 3**: the contract should carry `n_test_origins` so step 5 asserts
horizon evaluability instead of silently emitting an unreportable test set. This is the
same class of defect as the TRAIN_END/VAL_END drift (F25/F28) — a split that looks fine
and is quietly unusable.

**Method note**: the first run of this measurement picked a spurious date column and
reported 4-5 months per category (epoch-1970 artifact). The step-1 panel keys on
`period_year`/`period_month` and carries no date column. Any future analysis over this
panel must construct the period index from those two integer columns.

