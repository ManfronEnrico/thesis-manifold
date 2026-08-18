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

---

## F53 — the horizon analysis optimised for measurability and ignored usability (CORRECTS F52)

F50-F52 ranked horizons by how precisely they can be *evaluated* on this extract, and
concluded H=1. Brian rejected the conclusion on domain grounds, and he is right.

**The error**: a tight confidence interval on a question no user asks is still worthless.
The artefact is decision support for a marketing manager, and campaign planning runs on a
lead time of roughly a quarter — budget approval, creative production, retailer
coordination. A manager does not ask "what are sales next month", because by the time next
month arrives every decision it could inform has already been made.

This matters more here than in a generic forecasting paper: **SRQ2 evaluates an interface
for a decision-support task.** If the underlying task has no realistic user, the interface
comparison measures something with no external validity. That is a more serious objection
than a wide error bar.

**What survives from F52**: H=6 and H=12 remain excluded. Zero evaluable origins at H=12
is an impossibility, not an imprecision. That measurement stands.

**What was wrong**: the per-category framing. F52 reported origins per category (4-5 at
H=3) and treated that as marginal. The evaluation pools across four categories:

| H | Pooled origins | CSD | Danskvand | Energidrikke | RTD |
|--:|---------------:|----:|----------:|-------------:|----:|
| 1 | 25 | 7 | 6 | 6 | 6 |
| 3 | **17** | 5 | 4 | 4 | 4 |
| 6 | 5 | 2 | 1 | 1 | 1 |
| 12 | **0** | 0 | 0 | 0 | 0 |

17 pooled origins, each covering ~250 brands, is a reportable evaluation — the forecast
count is in the thousands. The cost of H=3 over H=1 is real but modest: 90.6% of training
rows and a wider confidence interval, not a broken analysis.

---

## F54 — report two horizons: H=3 operational, H=1 as the measurement anchor

**Decision**: H=3 becomes the primary reported horizon; H=1 is retained and reported
alongside it.

**Why not H=3 alone.** If the System A vs System B comparison comes out inconclusive at
H=3, that result is ambiguous between two very different explanations: the interfaces
genuinely perform alike, or the test lacked power to distinguish them. Running H=1 as well
separates those. H=1 has the tightest error bars of any evaluable horizon, so an interface
difference, if one exists, surfaces there most clearly.

The two horizons answer different questions and are not redundant:

| Horizon | Role | Question it answers |
|---------|------|---------------------|
| H=3 | Primary / operational | Does the artefact support a real planning decision? |
| H=1 | Measurement anchor | Does the interface difference hold where measurement is sharpest? |

**Cost**: the pipeline runs twice. Since horizon is a single contract parameter this is
cheap, and it forces a better design — step 3 must accept horizon as an argument rather
than reading a module constant, so `FORECAST_HORIZON` becomes a default rather than a
hardcoded assumption.

**CLOSED by Brian 2026-08-18** — both questions answered:

**(a) Basis for 3 months: the quarter as a planning period, not FMCG-specific practice.**
Brian declined to anchor this on his own marketing experience (Germany, not Denmark), which
was the right call — it would have been an anecdotal premise. The stronger basis is that
the quarter is the *financial reporting and budget-authorisation* period, near-universal
across commercial organisations, so the argument does not depend on the category or the
national market at all.

Stated as: a forecast is actionable if it reaches the next planning period; the planning
period is the quarter; therefore three months. No citation required — contesting the
premise means contesting how firms budget. If a supervisor later asks for one, the sales &
operations planning literature covers planning horizons directly.

**Important distinction for the write-up**: unsourced is fine, unjustified is not. "Three
months because that is a quarter" is an assertion. "Three months because budget approval,
creative production and retailer coordination each consume weeks, and the quarter is the
period in which those are authorised" is a reason. Same length, no citation, materially
harder to challenge. The note is written the second way.

**(b) Report both horizons.** H=3 headline, H=1 alongside. Confirmed.

**Thesis framing this enables**: "we forecast at the horizon the business plans on, and
additionally verify at the horizon where measurement is sharpest" is a stronger position
than "we forecast one month because that is what the data supported". The first is a design
choice, the second is a concession.

---

## F55 — CORRECTED: the stale holiday months were in the shared module and the
## three non-CSD scripts, NOT in the notebook

> **This finding was first written with the wrong attribution and is corrected here.**
> The original text claimed the notebook hardcoded `{1, 4, 6, 10, 12}`. It did not: the
> notebook derives holiday months from data at line 878 using a top-quartile rule, which
> yields `[3, 6, 12]` for CSD on current data. The `{1, 4, 6, 10, 12}` set lives in
> `engineer_features.DEFAULT_HOLIDAY_MONTHS` and was copied into the three non-CSD
> per-category scripts. The corrected account follows; the uplift measurements below are
> unaffected and stand.

Step 3 derives holiday months as those whose mean target exceeds the overall mean by more
than 10%, per category. For CSD it returns `[3, 6, 9, 12]`.

**Three different values were in play**, which is why the attribution took a second pass:

| Source | CSD value | Assessment |
|--------|-----------|------------|
| `engineer_features.DEFAULT_HOLIDAY_MONTHS` | `{1, 4, 6, 10, 12}` | **Wrong.** Stale, undated, includes the year's three weakest months |
| Notebook line 878 (top-quartile of monthly totals) | `[3, 6, 12]` | Defensible; sums totals |
| Step 3 (mean uplift > 10%) | `[3, 6, 9, 12]` | Preferred; see the methodological note below |

The notebook-versus-step-3 difference is a **methodological choice, not a defect**. The
notebook sums monthly totals, which is confounded by how many brands happened to be active
that month; step 3 averages, which is not. Averaging is the better rule here because the
panel is unbalanced by construction (brands enter and exit), but this should be presented
as a reasoned choice rather than as a correction.

The genuine defect is the first row of that table, and where it had spread.

Measured CSD uplift against the overall mean:

| Month | Uplift | Notebook | Derived |
|------:|-------:|:--------:|:-------:|
| 1 | **-26.6%** | yes | no |
| 3 | +14.7% | no | yes |
| 4 | **-9.2%** | yes | no |
| 6 | +22.3% | yes | yes |
| 9 | +16.9% | no | yes |
| 10 | **-16.0%** | yes | no |
| 12 | +34.2% | yes | yes |

Three of the notebook's five months (1, 4, 10) are **below-average** months — January is
the weakest month in the year at -26.6%. Only 6 and 12 were correct.

So `DEFAULT_HOLIDAY_MONTHS` was not merely stale: it was inverted for the majority of its
values. A binary `holiday_month` flag set on January, April and October tells the model
that the three weakest months of the year are high season.

The derived set is also interpretable in a way the hardcoded one was not: `[3, 6, 9, 12]`
are the **quarter-end months**, consistent with retail trade loading around quarterly
commercial cycles.

---

## F56 — seasonality is category-specific, and the notebook would have imposed CSD's on all four

Derived holiday months per category (H=3 run, 2026-08-18):

| Category | Holiday months | Commercial reading |
|----------|----------------|--------------------|
| CSD | 3, 6, 9, 12 | quarter-end trade loading |
| Danskvand | 6, 7, 8, 9 | summer — bottled water demand |
| Energidrikke | 3, 6, 9 | quarter-end, no December peak |
| RTD | 5, 6, 12 | early summer plus December |

These are four genuinely different seasonal profiles, and each is commercially plausible for
its category. Danskvand's summer peak in particular is the opposite shape from CSD's.

**And this had already happened.** Verified 2026-08-18: all three non-CSD per-category
scripts hardcode the stale set, under category-prefixed names that make an inherited
constant look like a per-category measurement:

    Danskvand/pre_danskvand_4_engineer_features.py:86
        Danskvand_HOLIDAY_MONTHS = {1, 4, 6, 10, 12}
    Energidrikke/pre_energidrikke_4_engineer_features.py:86
        Energidrikke_HOLIDAY_MONTHS = {1, 4, 6, 10, 12}
    RTD/pre_rtd_4_engineer_features.py:86
        RTD_HOLIDAY_MONTHS = {1, 4, 6, 10, 12}

Identical values, three different category prefixes. Danskvand peaks in **summer**
(June-September); its script asserts January. The naming is what makes this hard to spot in
review — `Danskvand_HOLIDAY_MONTHS` reads as a measured, category-specific constant.

This is the clearest single justification for the shared-script, derive-per-category design
(DEC-OPEN-WORLD): the duplication was not merely a maintenance cost, it had already
propagated a wrong feature into three categories nobody had checked.

---

## F57 — step 3 shipped; F25/F28 confirmed already fixed upstream, not re-implemented

`_shared_modules/step_3_derive_params.py` built and verified across all four categories at
both reported horizons.

**Correction to the earlier plan.** The plan listed "fix the TRAIN_END/VAL_END proportional
derivation" as step 3 work. On inspection `engineer_features.resolve_split_cutoffs()`
already implements it correctly — F25/F28 was fixed when task 15 landed. Step 3 therefore
*calls* it rather than reimplementing the logic, which would have recreated the drift it
removed. Verified: CSD now splits 32/7/7 of 46 months, a 15.2% test share against the
24-27% the hardcoded dates had drifted to.

**Verified behaviour**:

| Check | Result |
|-------|--------|
| All four categories, H=3 | 4/4 succeed |
| All four categories, H=1 | 4/4 succeed |
| `min_periods` tracks horizon | 15 at H=1, 17 at H=3, in every category |
| Training-row retention | **100.0%** in all four categories, both horizons |
| Contract collision | none — filenames carry the horizon |
| H=12 evaluability guard | fires; reports 0 test origins and warns step 5 will refuse |

**Design points worth keeping**:

- The contract carries `n_test_origins` and `horizon_evaluable`, so an unevaluable split is
  caught at derivation rather than discovered when results turn out unreportable.
- Every parameter carries a `provenance` string, so the contract answers "why this value"
  without anyone reading the script. This is what makes the JSON reviewable evidence rather
  than opaque configuration.
- Retention is recorded in **both** brands and training rows, so the brand-count framing
  (which makes the threshold look expensive) cannot be quoted without the row count (which
  shows it costs nothing). Guards against re-litigating F47.
- Period arithmetic goes through `period_index()` / `to_date_frame()` only, since the panel
  has no date column — the trap that produced the 4-months-per-category error in F52.

**Not yet done**: step 4 must validate `contract_version` and refuse an unknown one
(DEC-NO-FALLBACK). The field is written; the check belongs in the consumer.

---

## F58 — the two stale defaults are removed, not annotated

Both had previously been flagged in comments and left in place. A comment does not stop a
caller from silently receiving a wrong value, so this closes them properly.

**Removed from `engineer_features.py`:**

| Constant | Was | Why removed |
|----------|-----|-------------|
| `DEFAULT_HOLIDAY_MONTHS` | `{1, 4, 6, 10, 12}` | No correct default exists — seasonality is a property of the category |
| `DEFAULT_MIN_PERIODS` | `30` | No correct default exists — the value is horizon-dependent (15 at H=1, 17 at H=3) |

Both parameters are now **required**. `holiday_months` is keyword-only, so callers must
name it at the call site; `min_periods` was already positional and required.

The dataclass fields use `field(kw_only=True)` so they can stay required despite following
defaulted fields.

**Verified 2026-08-18:**

    engineer_features() without holiday_months -> TypeError
    filter_series() without min_periods        -> TypeError
    DEFAULT_HOLIDAY_MONTHS                     -> no longer exists
    DEFAULT_MIN_PERIODS                        -> no longer exists

    Real CSD panel, contract values passed:
      filter_series(min_periods=17)          -> 95 brands, 3,782 rows
      engineer_features(holiday={3,6,9,12})  -> 3,782 rows, 47 cols
      holiday_month flag set on              -> [3, 6, 9, 12]

**This is what DEC-NO-FALLBACK means in practice.** A missing contract value now fails at
the call site with a named argument in the error, rather than silently substituting a
constant that was measured on a different category three months earlier.

**Still open** (task 24 territory, not fixed here): the three per-category
`{Category}_HOLIDAY_MONTHS` constants still hold the stale set. They are now dead in the
sense that the shared pipeline does not read them, but the per-category scripts that do read
them are still on disk and still runnable. They are retired wholesale in task 24 rather than
patched individually — patching them would preserve the duplication this refactor exists
to remove. **Do not run the `pre_{category}_4_engineer_features.py` scripts in the
meantime.**

---

## F59 — two categories have NO promo data, and the shared code assumed they did

`make_calendar()` and `engineer_features()` both enumerated a fixed measure list
(`sales_units, sales_value, sales_liters, promo_units`). Step 4 raised `KeyError:
['promo_units'] not in index` on the first non-CSD category it touched.

Measured across all four categories (2026-08-18):

| Category | Panel columns | `promo_units` |
|----------|--------------:|:-------------:|
| CSD | 32 | yes |
| Energidrikke | 32 | yes |
| Danskvand | 15 | **no** |
| RTD | 31 | **no** |

Nielsen does not report promotion for Danskvand or RTD. So the shared modules
worked on exactly the two categories they had been exercised against — the same
shape of defect as the holiday months, a CSD assumption living in shared code
where it reads as general.

**Fix**: three sites in `engineer_features.py` now discover rather than assume —
the calendar zero-fill list, the `weighted_dist` ffill, and the `promo_intensity`
construction.

**The decision that matters**: where `promo_units` is absent, `promo_intensity` is
**omitted, not zero-filled**. A constant-zero column asserts "no promotion ran",
which is a factual claim the data does not support and which a model would learn
from. An absent feature is honest; a fabricated one is not. The consequence is
that the four categories do **not** share a feature space — CSD/Energidrikke get
45-47 columns, Danskvand 27, RTD 43 — and this must be stated wherever results are
compared across categories. The step 4 sidecar records `has_promo` per run so the
difference is never silent.

---

## F60 — step 4 shipped; the contract is now enforced on the OUTPUT, not just the input

`_shared_modules/step_4_engineer_features.py` built and verified: **8/8 runs**
succeed (4 categories x H=1 and H=3).

| Category | H=3 rows / brands | H=1 rows / brands | Cols | Holiday months | promo |
|----------|------------------:|------------------:|-----:|----------------|:-----:|
| CSD | 4,370 / 95 | 4,876 / 106 | 47 | 3, 6, 9, 12 | yes |
| Danskvand | 1,189 / 29 | 1,230 / 30 | 29 | 6, 7, 8, 9 | no |
| Energidrikke | 1,892 / 44 | 2,150 / 50 | 47 | 3, 6, 9 | yes |
| RTD | 2,542 / 62 | 2,952 / 72 | 45 | 5, 6, 12 | no |

CSD H=3 retention (95 of 142 brands) matches the step 3 contract exactly, which is
the cheap end-to-end check that step 3 and step 4 agree.

**This file contains no parameter values.** Every number comes from the contract.
That is the whole point: the archived `pre_csd_4_engineer_features.py` carried
`CSD_HOLIDAY_MONTHS = {3, 6, 12}` privately, and the three non-CSD scripts each
carried `{1, 4, 6, 10, 12}` — four scripts with four private opinions about one
parameter.

**DEC-NO-FALLBACK, verified firing.** Six refusal paths tested, all raise
`ContractError` rather than defaulting:

| Condition | Refused |
|-----------|:-------:|
| Contract file absent | yes |
| `contract_version` unknown (`9.9`) | yes |
| `contract_version` field missing | yes |
| Body horizon disagrees with filename | yes |
| Required field dropped (`min_periods`) | yes |
| Matrix contradicts contract (holiday months) | yes |

The last one is the addition worth keeping. Steps 3 and 4 could previously agree on
paper while the matrix on disk disagreed with both, because `engineer_features()`
accepts any parameter and runs. Verifying the **output** — that `holiday_month` is
set on exactly the contracted months and no others — is what makes the contract
enforceable rather than merely documented. It is also the check that would have
caught the original defect years earlier.

**Provenance sidecar**: each run writes `step_4_log_h{N}.json` recording which
contract produced the matrix, the parameters applied, and `has_promo`. Without it a
parquet is unattributable — you can read its columns but not the thresholds behind
them, which is the position every previous notebook run left its outputs in.

---

## F61 — make_calendar silently dropped the panel's canonical period columns

`make_calendar()` drops `period_year`/`period_month` before merging (it keys on
`date`), and never restored them. Nothing was broken — `apply_split()` reads `date`
— but steps 1-3 and every contract express a period as the integer pair, so the
matrix stopped speaking the pipeline's own language and each consumer would have had
to re-derive it.

Both are now rebuilt from `date` after the fill. Rebuilt rather than merged back,
so calendar-filled rows (which have no source row) also carry correct values.
Verified consistent with `date` on every row.

---

## F62 — the feature was never a holiday indicator, and the thesis said it was

Brian, reviewing the step 4 output: *"why is it called holiday? technically it's just
the peak month rate."* Correct, and the consequence reached further than the codebase.

**What the feature actually is.** A month qualifies when its mean `sales_units` exceeds
the category's overall mean by more than 10%. That is a statement about the sales
distribution. **No holiday calendar is an input anywhere in the pipeline** — no Danish
public holidays, no Easter dates, no school terms.

**The evidence contradicts the holiday reading in three of four categories:**

| Category | Peak months | Most plausible driver |
|----------|-------------|----------------------|
| CSD | 3, 6, 9, 12 | quarter-ends — retail **trade loading** |
| Danskvand | 6, 7, 8, 9 | summer heat — **weather** |
| Energidrikke | 3, 6, 9 | quarter-ends, and **no December peak at all** |
| RTD | 5, 6, 12 | early summer + December |

Energidrikke is the clearest refutation: it peaks at quarter-ends while skipping
December, close to the opposite of what "holiday month" predicts. Danskvand's August
peak is bottled water in warm weather; calling it a holiday month is simply wrong.

**The name is also how the original defect survived review.** A hardcoded
`{1, 4, 6, 10, 12}` reads as a plausible list of holidays. Read as *"peak months for
soft drinks"* it is obviously wrong — January is the year's **weakest** month at
−26.6%. A name that describes what was measured invites the check; a name that
hypothesises why deflects it.

**Where it had already propagated — the serious part.** The claim had reached
approved thesis prose as a statement of fact about the data:

| Location | Claim | Status |
|----------|-------|--------|
| Ch1 §intro footnote | exogenous predictors include *"a binary indicator for Danish public holidays"* | **factually wrong**, corrected |
| Ch4 §4.3.3, §4.3.4 tables | `HOLIDAY_MONTHS = {3,6,12}`, "Holiday indicator" | corrected, now per-category |
| Ch6 §6.3.2 | *"Calendar: week of year, month, quarter, Danish public holidays"* | **factually wrong**, corrected |
| Ch6 §6.2.2 | Prophet *"handles Danish holiday calendar"* | **left intact** — legitimate; Prophet genuinely supports `add_country_holidays('DK')`. This is a model capability, not a description of the engineered feature |

An examiner reading Ch1 would reasonably conclude a holiday calendar was an input. It
was not. This is the kind of claim that is hard to defend in a viva precisely because
it is not a modelling judgement — it is a description of the data that does not match
the data.

**Renamed throughout** (13 code files, 3 thesis chapters): `holiday_month(s)` →
`peak_month(s)`, `HOLIDAY_MONTHS` → `PEAK_MONTHS`, plus console labels, EDA section
headings and table captions. Contract schema bumped **1.0 → 1.1**, so a stale contract
is refused rather than read with the renamed field silently absent — verified firing.

Re-ran steps 3 and 4 for all four categories at both horizons: **8/8 succeed, with row
counts identical to before.** The rename changed names, not values.

**Also found while correcting Ch6 §6.3.2**: it describes a *weekly* grain (t-52 weeks,
4/8/13-week windows) that no longer matches the locked brand×month grain (DEC-GRAIN).
Corrected list written in place with the original retained in an HTML comment and a
NEEDS REVIEW flag — not silently rewritten, since it may reflect an earlier deliberate
design decision.

---

## F63 — steps 5 and 6 shipped; the split now matches the F29 projection exactly

`_shared_modules/step_5_apply_split.py` and `step_6_save_outputs.py` built and
verified. **24 runs clean** (4 categories x 2 horizons x 3 steps).

Split geometry at H=3, against the F29 projection:

| Category | Projected | Actual | Ratio | Test origins |
|----------|-----------|--------|-------|-------------:|
| CSD | 32/7/7 | **32/7/7** | 69.6 / 15.2 / 15.2 | 5 |
| Danskvand | 29/6/6 | **29/6/6** | 70.7 / 14.6 / 14.6 | 4 |
| Energidrikke | 30/6/7 | **30/6/7** | 69.8 / 14.0 / 16.3 | 5 |
| RTD | 29/6/6 | **29/6/6** | 70.7 / 14.6 / 14.6 | 4 |

Four for four. Against the 24-27% test share the hardcoded dates had drifted to,
the proportional rule holds ~15% everywhere. **18 pooled test origins** at H=3.

**Step 5 refuses an unevaluable split — verified end to end.** This is the guard the
plan assigned to this step, and the three steps now differ deliberately in how they
treat H=12:

| Step | Behaviour at H=12 | Why |
|------|-------------------|-----|
| 3 | warns, writes contract | a contract is a measurement; recording that a horizon is unevaluable IS the finding |
| 4 | warns, builds matrix | a feature matrix is still a valid artifact independent of evaluation |
| 5 | **refuses** | a split is the object that DEFINES the evaluation, so an unevaluable split is a contradiction in terms |

`--allow-unevaluable` exists for inspection and prints a loud banner. Verified: H=12
is refused by default, labelled with the flag.

**Step 5 also verifies the labels rather than trusting them.** Four guards, all
confirmed firing:

| Guard | Catches |
|-------|---------|
| empty partition | a split with no validation or test rows |
| month counts vs contract | matrix covering a different period than step 3 measured |
| strict temporal ordering | overlapping partitions — training on the future |
| cutoffs read from contract, never re-derived | the F25/F28 drift, structurally |

The ordering guard matters most because its failure is silent: a shuffled split
trains on the future and reports excellent, meaningless accuracy.

**Step 6 reads split dates back off the labelled frame** rather than recomputing them
from the contract. The two should agree, and step 5 asserts they do — but if they
ever diverge the file must report what the data says, because that is what a model was
actually trained on.

---

## F64 — three Nielsen measures were spelled three different ways across categories

Found immediately by step 6's `--check-consistency`, which is the argument for having
built it:

| Measure | CSD | Energidrikke | RTD |
|---------|-----|--------------|-----|
| display AND feature | `disp_feat` | `disp_feat` | `disp_and_feat` |
| display WITHOUT feature | `disp_w_o_feat` | `disp_wo_feat` | `disp_wo_feat` |
| feature WITHOUT display | `feat_w_o_disp` | `feat_wo_disp` | `feat_wo_disp` |

Verified as the same measure, not different ones: identical 0-1 distribution scale,
consistent relative ordering across all three categories.

This is exactly the case DEC-OPEN-WORLD anticipated when it noted a hardcoded column
list "could not express per-category spelling variants". Canonicalised through the
existing `RENAMES` map in step 1, spelling out `and`/`without` — `disp_feat` does not
say whether it means "display and feature" or the pair, and `w_o` must be decoded.

**Effect on the cross-category picture:**

| | Before | After |
|--|--------|-------|
| CSD vs Energidrikke | 3 apparent absences each | **feature-identical, 41 each** |
| RTD vs those two | 5 apparent absences | **differs by exactly the 2 promo columns** |
| Common to all four | 23 | 23 (unchanged) |

The common count does not move, because these measures are absent from Danskvand
regardless. What the fix buys is that RTD's **real** capability gap (no promo) is no
longer masked by three spelling artifacts. A correction to the note first written in
step 1: I predicted 26 common features; the true figure is unchanged at 23.

---

## F65 — twelve downstream scripts still read the notebook's output, not the pipeline's

`grep` across `03_thesis_modelling/` finds **12 scripts** reading
`{slug}_feature_matrix.parquet` — the un-suffixed file the notebook wrote. The new
pipeline writes `{slug}_feature_matrix_h{N}.parquet`, so nothing downstream currently
consumes it.

Affected: `srq1_baselines_stat`, `srq1_calibration`, `srq1_shap`, `srq1_benchmark`,
`srq1_benchmark_tuned`, `srq1_figures`, `srq1_profiling`, `srq2_synthesis`,
`srq4_experiment` (3 sites), `srq4_tier2`.

**Deliberately NOT changed here.** Task 23 is the parity check, and it compares the
new pipeline's output against the notebook's. Repointing the consumers first would
destroy the baseline the check needs, and would switch the modelling layer onto
unverified data. The correct order is: parity passes (task 23), then repoint, then
retire the notebook artifacts (task 24).

**Note for task 24**: repointing is not a pure find-and-replace. The consumers must
also choose a horizon, and H=1 and H=3 are different matrices with different
`min_periods` (15 vs 17) and different brand counts. A script that reads "the" feature
matrix no longer has an unambiguous referent — the horizon has to become an explicit
parameter downstream, exactly as it is in the pipeline.

---

## F66 — the shared orchestrator replaces four; the pipeline runs end to end

`_shared_modules/run_preprocessing.py` built (task 7). **8 runs clean**: 4
categories x 2 horizons, steps 0-6.

**`run_preprocessing.py --category CSD` completes end to end in 70.5s** — a
Definition-of-Done line for this plan, now met.

The four orchestrators it replaces were 184 lines each and differed only in the
category name, which is the failure mode DEC-OPEN-WORLD exists to prevent: a fix
applied to one was a fix missing from three. CSD's was already broken.

**The pipeline is declared, not hardcoded.** A `PIPELINE` tuple of `Step`
records carries one structural fact per step — `horizon_dependent` — and that
single flag drives both the skip logic and the artifact suffixing. Adding a step
is adding a row.

**Steps 0-2 are horizon-independent, and the orchestrator exploits it.** They
validate the cache, build the brand x month panel and describe it; none of that
changes with the horizon. So on a multi-horizon run they execute once and are
skipped thereafter — automatically, not only under an explicit `--skip-shared`:

| Run | Wall clock |
|-----|-----------:|
| Danskvand H=1 (steps 0-6) | 25.4s |
| Danskvand H=3 (steps 3-6, 0-2 skipped) | **2.0s** |

**Verified failure behaviour, which is the part that matters.** At H=12 on RTD:
step 5 refused, **step 6 did not run**, and the process exited **1**. Both halves
are load-bearing. Continuing past a failed step would let step 6 succeed against
a *stale artifact from a previous run* and write a manifest describing data that
the current run never produced. And without the non-zero exit, a shell loop or CI
job would record a failed pipeline as a pass.

**Step 2 needed explicit outcome checking.** It is the one step that reports
partial failure through its return value rather than by raising — individual EDA
sections are caught and collected so one bad section does not cost the other
forty. An orchestrator that only caught exceptions would record a step that
printed FAILED as `ok`.

**Output-side verification against F63.** Reading the written manifests back off
disk, rather than trusting the run summary:

| Category | Split (train/val/test) | F63 | Origins | Features | Promo |
|----------|------------------------|-----|--------:|---------:|-------|
| CSD | 32/7/7 | 32/7/7 | 5 | 41 | yes |
| Danskvand | 29/6/6 | 29/6/6 | 4 | 23 | no |
| Energidrikke | 30/6/7 | 30/6/7 | 5 | 41 | yes |
| RTD | 29/6/6 | 29/6/6 | 4 | 39 | no |

Four for four on geometry, origins, feature counts and promo capability.

**Deliberately not using `terminal_utils.print_orchestrator_start`.** Those
helpers render rich panels containing U+2713, which raises `UnicodeEncodeError`
under the cp1252 default the moment the console is teed to a file on Windows —
which is exactly what the orchestrator does. Matched the steps' own plain `=`
rule convention instead.

**Note on the manifest**: `split_dates` carries the boundary dates but not the
month counts, so the geometry above had to be derived from the boundaries. Not
changed here (task 8 compares against the notebook's manifests, and altering the
schema mid-comparison would muddy it), but worth adding afterwards — the counts
are the thing anyone actually checks.

---

## F67 — DEC-ALIAS was implemented before Brian ruled on it

Recording this as a process finding, not a technical one.

`task_plan.md` lists DEC-ALIAS under **Open decisions**, explicitly assigned to
Brian, and explicitly framed as "a modelling question" because unifying the names
asserts the measures are interchangeable across categories — something SRQ1's
cross-category ranking would then rely on.

In the previous session, step 6's `--check-consistency` surfaced the variants
concretely (F64) and I canonicalised them through step 1's `RENAMES` immediately,
treating it as a data-cleaning fix. It is one, but it is also the reserved
decision, and it should have been raised before acting.

The evidence gathered does support option A and is stronger than what the block
had when written — identical 0-1 scale and consistent relative ordering, on top
of the byte-identical metadata descriptions. It is still not proof that Nielsen
computes them identically per category.

**Reversal is cheap**: delete the five spelling entries from `RENAMES` and
re-run. Nothing downstream hardcodes the canonical names. Flagged for Brian's
confirmation.

**Resolved 2026-08-18**: Brian reviewed and confirmed option A. The canonical
names stand and DEC-ALIAS is closed. The substance was right; the sequencing was
not, and that is the part worth remembering — a decision the plan assigns to a
person gets raised before it is implemented, even when the fix looks like
routine cleaning and even when reverting is cheap.

---

## F68 — parity check PASSES: every difference is explained by a decision we made

Task 8, the gate. The criterion the plan set was **not** that the numbers match —
the 2026-08-12 re-pull and three deliberate fixes guarantee they will not — but
that every difference is *explicable*. Each one below traces to a specific
decision, and nothing is left unaccounted for.

### The headline check: the split is fixed

| | train | val | test | ratio |
|--|------:|----:|-----:|-------|
| notebook (old) | 1,450 | 348 | 754 | 56.8 / 13.6 / **29.5** |
| pipeline (new) | 3,040 | 665 | 665 | 69.6 / 15.2 / **15.2** |

The old test set was **more than double its intended size** — the hardcoded
cutoffs had drifted as data accumulated, which is exactly the failure DEC-SPLIT
was raised to fix. The plan's target was ~70/15/15; the pipeline delivers
69.6/15.2/15.2. The old figures reproduce the plan's recorded 1450/348/754
exactly, confirming the baseline is the right one.

### The four differences, each traced

**1. +2 months of data** (ends 2026-07 vs 2026-05) — the 2026-08-12 re-pull.
Every one of the 58 shared brands gained exactly +2 rows. Nothing else moved.

**2. +37 brands** (58 → 95), from DEC-SCOPE. Decisive evidence that these are
*not* new arrivals: **all 37 have the full 46-month history back to 2022-10**,
and zero start in the two new months. They existed throughout and were being
excluded. They are 38.9% of rows but only **0.83% of units** — the long tail of
small brands that regional scope was dropping.

**Zero brands were lost.** All 58 old brands survive.

**3. +28 columns, −10 columns.** The additions are the Nielsen measures the
notebook discarded (baseline_*, numeric_distribution, the reach family) plus the
new rolling windows. The removals are either renames (`holiday_month` →
`peak_month`, DEC-PEAKNAME), window changes (`rolling_mean_12` → `rolling_mean_13`,
`lag_12` → `lag_13`), or capability columns now recorded in the manifest instead
(`has_promo`).

**4. Every measured value differs.** This is the one that needed real work, since
raw `sales_units` differing is alarming on its face.

| Direction | Share of cells | Cause |
|-----------|---------------:|-------|
| new **>** old | 84.2% | DEC-SCOPE: parent market vs 15 regional children |
| new **=** old | 10.8% | — |
| new **<** old | 5.0% | Nielsen restatement in the re-pull |

Total volume uplift **1.0765x**. The decreases were the part that could have
indicated a defect — a wider scope cannot reduce a brand's sales — so I measured
them: **8,484 units in total, 0.001% of volume**, median ratio 0.9992, scattered
across all 34 months rather than clustered at a boundary. That is Nielsen
revising history in the re-pull, not a pipeline error.

### `weighted_dist` moves the *opposite* way — and that is correct

It was the one feature with **0% exact matches** and, unlike everything else,
systematically **lower**: median ratio 0.735.

**I first hypothesised the bfill fix** (task 5) and tested it: if bfill were the
cause, the effect would concentrate in each brand's early months, where the
notebook invented distribution before the brand was stocked. It does not — the
reduction is uniform across brand history (median 0.73 in months 1-3 and 0.73 at
25+). **Hypothesis rejected.**

Measured directly on the raw facts instead:

| Scope | n | mean `weighted_distribution` |
|-------|--:|-----:|
| DVH EXCL. HD (parent) | 223,240 | 0.1489 |
| 15 regional children | 2,565,349 | 0.1973 |
| **ratio** | | **0.7548** |

The raw ratio 0.7548 matches the observed feature ratio 0.735. **Mechanism**:
distribution is a share-of-stores measure, so a brand stocked in a handful of
shops scores higher *within one region* than nationally. The old regional scope
systematically **overstated** distribution. Uniformity across brand history now
follows — it is a property of scope, not of time.

### Independent construction checks (not comparisons — assertions on the output)

| Check | Result |
|-------|--------|
| `log_sales_units` == `log1p(sales_units)` | **100.00%** |
| `lag_1` == previous month's sales | **100.00%** (4,275 rows) |
| `lag_3` == t-3 sales | **100.00%** (4,085 rows) |
| `rolling_mean_4` **excludes** current month | **100.00%** (3,990 rows) |
| — leaky variant (including t) would match | only 10.48% |
| `promo_intensity` uses t-1, not t | **99.97%**; leaky variant 22.40% |
| train < val < test, strictly | **True** on both boundaries |

The single `promo_intensity` residual (1 row of 3,699) is JARRITOS 2023-05, where
the raw ratio is 1.365 — promo units exceeding total sales, a Nielsen artifact —
correctly clipped to 1.0. A guard working, not a defect.

**No future leakage.** The rolling-window and promo checks are the ones that
matter here, because leakage does not announce itself: it produces a model that
looks excellent and fails in production.

### Verdict

**PASS.** Every difference is attributable to a decision on the record —
DEC-SCOPE, DEC-SPLIT, DEC-PEAKNAME, the bfill fix, and the re-pull — and the
feature construction verifies correct against independently recomputed values.
The notebook's split was genuinely broken; the pipeline's is not.

**P0033 is unblocked.**

### Caveat carried forward — CORRECTED

I first wrote that the `*_bymonth.parquet` intermediates are all stale
notebook-era artifacts. **That was too broad.**

`step_1_aggregate_bymonth.parquet` is **LIVE** in all four categories, written
today by the current step 1. Its `bymonth` suffix comes from `GRAIN` — the
brand × month modelling grain fixed by DEC-GRAIN — not from the notebook.
Every future run rewrites it.

Genuinely stale: the four **CSD steps 2-5** files
(`step_{2,3,4,5}_*_bymonth.parquet`, dated 2026-07-13, 140/58 brands,
pre-re-pull and pre-DEC-SCOPE). Those are notebook-era and must not be read as
current output.

The distinction matters because a date-based sweep would have deleted a live
pipeline output. Full disposition list in
`2026-08-18_DOC-stale-file-inventory.md`.

---

## F69 — the 12 downstream consumers repointed to H=3

All **13 call sites across 11 files** now read
`{slug}_feature_matrix_h3.parquet` instead of the notebook's un-suffixed file.

**H=3 chosen by Brian (2026-08-18)**, matching DEC-HORIZON: a quarter is the
budget-authorisation period, so H=3 is the primary reported horizon.

Repointing was mechanically a one-line change per site — h1 and h3 carry
**identical columns** — but it is not cosmetic. The row populations differ,
because h3's higher `MIN_PERIODS` (17 vs 15) retains fewer brands:

| Matrix | rows | brands | train/val/test |
|--------|-----:|-------:|----------------|
| notebook (old) | 2,552 | 58 | 1450/348/754 |
| h1 | 4,876 | 106 | 3392/742/742 |
| **h3 (chosen)** | 4,370 | **95** | 3040/665/665 |

Every downstream result therefore moves — onto the split the pipeline actually
validates, and onto 95 brands rather than 58.

Includes `model_serving/system_a_forecast/forecast_service.py`, which is the
serving path rather than a training script. Worth naming: the repoint changes
what System A serves, not only what the thesis reports.

---

## F70 — `period_index` was missing from every matrix, and 5 consumers needed it

Running a repointed consumer (rather than assuming the rename sufficed)
immediately raised `KeyError: 'period_index'`.

**This is pre-existing breakage, not damage from the repoint.** Verified two
ways: the committed version of the script references `period_index` against the
notebook matrix, and **no feature matrix has ever contained that column** —
neither the notebook's nor the pipeline's. Five consumers were already dead:

```
srq1_baselines_stat  srq1_figures  srq1_profiling  srq4_experiment
system_a_forecast/forecast_service
```

Every use is a temporal sort key or a plot axis.

**Fixed in step 6 rather than in the five call sites.** It is a genuine property
of the panel (which period is this, on a scale shared across brands), so it
belongs where the panel is written — one definition that cannot drift between
consumers.

Computed **from the calendar, not from row order**: two brands observed in the
same month must receive the same index, or a pooled model places them at
different points on the same axis. Verified: 0 months carry more than one
distinct index; values run 0..45 across 46 months; strictly monotonic with date.

**Registered in `NON_FEATURE_COLS`.** A monotonic counter correlates with any
trending target, so a model handed it as a feature learns "later means bigger" —
scoring well in-sample while learning nothing that transfers past the observed
window. Confirmed: feature count stays **41**, `period_index` absent from the
manifest's feature list.

`--from-step 6 --to-step 6` regenerated all 8 artifacts in ~1s total, which is
the step-range flag earning its place.

**Verified working**: `srq1_baselines_stat` now runs to completion and reports
series counts matching the H=3 matrices exactly — CSD 95, Danskvand 29,
Energidrikke 44, RTD 62.

---

## F71 — Prophet: absent here, and diverged when it did run

Surfaced while verifying the repoint. `srq1_baselines_stat` reports
**n_series=0 / WMAPE=nan for Prophet in all four categories**, while ARIMA
reports normally.

**Immediate cause**: `prophet` is not installed in this environment. The import
sits inside `run_prophet()` and the per-series loop catches the exception, so
every series fails identically and the failure aggregates into `nan` rather than
raising.

**Correcting my first reading of this.** I initially wrote that Prophet's rows
are empty and always have been. The committed `04_thesis_results/srq1/stat_baselines.md`
shows otherwise — it ran in some earlier environment and produced numbers. But
those numbers are not usable:

| Category | Prophet WMAPE (committed) |
|----------|--------------------------:|
| CSD | **1,715,701,549,531,750,912 %** |
| energidrikke | **14,858,220,394.7 %** |
| danskvand | 16.9 % |
| RTD | 45.4 % |

Two of four are diverged fits — 1.7 x 10^18 % is not a poor forecast, it is a
model that blew up, most likely exponentiating a runaway trend back from log
space. So the ladder Ch6 describes has never had four working Prophet baselines;
it had two plausible ones and two failures being carried in a results table.

**Not fixed here**, and deliberately so: installing a package changes the
environment, and which baselines the thesis claims is Brian's call. The options
are to install `prophet` and re-run (then handle the divergence, which will
recur), or to drop Prophet and say so. What should not happen is either number
reaching a thesis table — `nan` or 10^18 % both misrepresent the comparison the
ML models are being judged against.

**`04_thesis_results/srq1/stat_baselines.md` was deliberately NOT committed** by
this session's re-run. Two reasons: the ARIMA figures legitimately changed (95
brands at H=3 vs 77 before, which is the repoint working as intended), but the
script also rewrote the file with mangled encoding — `—` became `�` — so the
regenerated file is worse than the committed one regardless of its numbers. The
script writes without specifying an encoding and inherits cp1252 on Windows.
That is a real bug in `srq1_baselines_stat.py`, filed here rather than fixed
mid-cleanup.

---

## F72 — why Prophet diverged: unbounded trend, exponentiated

Brian asked. Diagnosed per-brand rather than reasoned about in the abstract.

**One brand causes it.** CSD, H=3:

| Brand | actual (test) | Prophet predicted | share of category error |
|-------|--------------:|------------------:|------------------------:|
| FRESH | 300,859 | **101,201,667** | **59.9%** |
| JOLLY | 3,166,314 | 16,741,237 | 8.1% |
| FRESH MOJITO | 78,986 | 10,908,130 | 6.4% |

FRESH is over by **336x**. WMAPE is volume-weighted and unbounded above, so a
single exploded series sets the category number.

### Mechanism

1. The script fits on `log(units)`, so the model operates on exponents.
2. Prophet's default trend is **linear and unbounded**; it extrapolates the
   slope it saw in training with nothing to stop it.
3. `expm1()` inverts. The largest log-space prediction observed is **17.2**,
   which becomes **2.85e7**.

In log space the error is a few units — unremarkable. After exponentiating, a
few units *is* a factor of several hundred. Prophet does not know it is
predicting a physical quantity with a ceiling.

Three properties make CSD especially exposed:

| Property | Value | Why it matters |
|----------|------:|----------------|
| brands hitting 0 in train | **38 of 95** | the `max(units, 1)` floor creates artificial cliffs in log space |
| max within-brand dynamic range | **6,308x** | a slope fitted on the low end explodes at the high end |
| short, noisy small-brand histories | — | a spurious upward slope is easy to fit and impossible to falsify in-sample |

### A separate, genuine bug

`run_arima` and `run_prophet` both fit with `np.log(max(y, 1))` and invert with
`np.expm1()`. **Those do not pair**: `expm1` is the inverse of `log1p`, not of
`log`. It is a constant off-by-one — negligible at 1e6 units, real at small
counts, and exactly the kind of asymmetry that survives review because the two
function names look symmetrical.

### Why the number moved from 1.7e18% to 105.7%

Not a fix. The committed run scored **77 series** on the notebook's matrix;
today's scores **95** on the H=3 matrix. Different brands, different fitted
slopes, different worst case. **The failure mode is still live** — it is simply
less extreme for this particular brand set.

That is the part worth carrying forward: a metric that swings by 16 orders of
magnitude on a change of series membership is not measuring forecast quality.

### Recommendation (Brian's call, not changed here)

Cap the trend before reporting either figure — `growth="logistic"` with a
per-series cap, or a much lower `changepoint_prior_scale`. An unbounded-trend
baseline fitted in log space is not a fair comparator: it makes the ML models
look strong for a reason that has nothing to do with the ML models.

Reporting 105.7% as "Prophet's performance" would overstate how weak the
statistical baseline genuinely is.

---

## F73 — capability-transfer audit: one real feature was dropped, and it was leaky

Brian asked for proof that the archived scripts' capabilities were transferred,
improved, or removed *on purpose* — not silently lost — before anything is
deleted. Audited by diffing every function defined in the archived notebook
export against the shared pipeline.

**6 functions in the notebook, 65 in the pipeline. Four appeared "missing":**

| Archived function | Disposition |
|---|---|
| `_load_merged` | renamed → `step_1.load_merged` |
| `build_calendar_index` | renamed → `engineer_features.make_calendar` |
| `_get_date_str` | local report-string helper; pipeline formats dates directly — no capability |
| `_zero_run_features` | **genuinely dropped — now restored, fixed** |

### The one that mattered

The notebook computed two intermittent-demand features:

```
zero_run_flag   = (sales_units == 0)             at time t
zero_run_length = length of the zero run ending at t
```

**Both read `sales_units[t]` — the value being forecast.** Verified against the
preserved baseline: `zero_run_flag` equals `(sales_units == 0)` on **100.00%** of
rows. Not correlated with the target; a *function of* the target, at the same
timestamp.

**Why nobody noticed**: the notebook's matrix had **0 rows** with
`sales_units == 0` — regional scope filtered them out — so a leaky feature was
constant and harmless. The current parent-scope matrix has **588 (13.5%)**.
Restoring the code as written would have leaked on one row in seven.

### Restored, shifted

The signal is real: intermittent demand is a distinct forecasting regime, and a
brand two months into a stock-out behaves unlike one selling steadily. So both
features are kept, shifted one period within `group_keys` — the same discipline
`promo_intensity` already uses. At time t they describe t-1, which a forecaster
genuinely knows.

**Verified on the regenerated matrix:**

| Test | Result |
|------|--------|
| matches `sales_units[t] == 0` (old leaky behaviour) | 96.05% |
| matches `sales_units[t-1] == 0` (correct behaviour) | **100.00%** |
| run length range | 0..29, 576 non-zero rows |
| first row of each series | `NaN` (no prior month) |
| feature count | 41 → **43** |

Worked example: April 2023 has sales of 44 but `zero_run_flag = 1`, correctly
describing March.

**The 96.05% figure is the lesson.** The leaky version still matches the current
month on 96% of rows — close enough to look correct in any spot check. Only an
explicit t vs t-1 comparison separates them.

### Audit verdict

Every archived capability is accounted for: two renamed, one genuinely
unnecessary, one restored in corrected form. **Safe to delete the superseded
tree**, with the notebook itself archived rather than deleted since it is the
parity baseline's source.

---

## F74 — deletions executed; audit widened first and found three more issues

Brian asked whether the deletions were safe because functionality was verified
carried over. My audit had been narrower than that: F73 diffed **function
definitions**, which would miss logic written inline in notebook cells. Widened
before deleting, by extracting every column the notebook assigns.

**12 columns assigned; 6 absent from the current matrix:**

| Column | Verdict |
|--------|---------|
| `chow_f`, `chow_p`, `mean_ratio`, `std_ratio` | structural-break **diagnostics**, printed to an EDA table — never features |
| `period` | intermediate merge key, replaced by `date` + `period_index` |
| `log_weighted_dist` | **genuinely produced**, and genuinely redundant — see below |

`log_weighted_dist` is `log1p(weighted_dist)`. Measured on the preserved
baseline: Pearson 0.999, **Spearman exactly 1.000**. Rank correlation of 1 means
any tree model splits identically on either column, and the models here are
XGBoost/LightGBM. No downstream consumer references it. **Removed with purpose,
not lost.**

### Three fixes that had to land before deleting

**1. Dead code writing a horizon-ambiguous filename.**
`engineer_features.save_feature_matrix()` wrote un-suffixed
`feature_matrix.parquet` and had **no callers** in live code (verified
repo-wide; the only caller is an archived pre-integration agent). Removed rather
than left: a dead helper in a *shared module* that writes exactly the artifact
this cleanup deletes is an invitation to recreate it with apparent authority.

**2. `pipeline_config.findings_json` named a file no step writes.** Step 3 writes
`{slug}_eda_findings_h{N}.json`. Replaced with `findings_json_for(horizon)`.

**3. Hardcoded FEATURES lists in nine modelling scripts.** This one is
substantive. Every script indexed the frame by a fixed list including
`promo_intensity` — which Danskvand and RTD legitimately do not have (F59:
Nielsen does not report promotion for them, so the pipeline omits the column
rather than zero-filling). `srq1_benchmark` died with
`KeyError: ['promo_intensity'] not in index` on Danskvand.

The preprocessing layer follows DEC-OPEN-WORLD; the modelling layer did not.
Added `available_features(fm)` to all nine, selecting by intersection with the
frame's actual columns. 24 indexing sites switched.

### Deletions

40 files across groups 1-5, per the inventory. **`step_1_aggregate_bymonth.parquet`
survived in all four categories** — the live-vs-stale distinction from the
corrected F68 holding up in practice; a date-based sweep would have taken it.

### Verification after deleting

| Check | Result |
|-------|--------|
| full pipeline, 4 categories x 2 horizons | **8/8 clean**, exit 0 |
| `srq1_benchmark` end to end | **runs on all 4 categories**, incl. the two that crashed |
| tree models vs naive | beat it everywhere (CSD 17.5% vs 34.9%) |

Also installed the missing ML stack (scikit-learn, xgboost, lightgbm) — without
it every ML row reported `ERR`, swallowed into the results table rather than
raised.

---

## F75 — `mean MAPE` is meaningless in the benchmark output and should not be reported

Visible in every row of `04_thesis_results/srq1/summary.md`: mean MAPE runs to
**10^12 – 10^15 %**, including for **SeasonalNaive**. A naive baseline cannot be
wrong by a quadrillion percent in any meaningful sense.

Same defect as F72's Prophet blow-up, in a different place: MAPE divides by the
actual, and the guard is `np.maximum(y, 1e-9)`. For a brand-month with near-zero
sales the ratio explodes, and the **mean** carries it into the headline. There
are 588 zero rows (13.5%) in the CSD matrix at parent scope.

`WMAPE` (volume-weighted) and `medMAPE` (median) are both robust to this and
agree with each other. **Recommendation: drop mean MAPE from the reported table**
rather than explain it — a column no reader can interpret is worse than absent.
Not removed here: which metrics the thesis reports is Brian's call.

---

## F76 — P0036 task 4 delivered: the degenerate-feature guard

The missing half of task 4. The existing verification checked that contracted
columns are **present**; a column can be present and carry no information, which
is the failure that actually happened.

Added to `step_4_engineer_features._verify()`, scoped to **every** engineered
feature rather than promo alone — what the original task asked for, and the next
silent-zero column will not be one anybody predicted.

**Distinguishing degenerate from legitimately absent was the design question.**
DEC-NO-PROMO-FILL means a category without promotion has no `promo_intensity`
column at all, and that is correct. So the guard fires only on columns that
**exist and say nothing** (single distinct value, or all-null); absence stays
with the presence check above it. Calendar/identity columns are exempt, plus
`peak_month`, which is legitimately all-zero when a contract lists no peak months
and is verified against the contract separately.

**Verified by mutation, not by observing it stay quiet.** A guard that never
fires is untested:

| Case | Result |
|------|--------|
| unmodified matrix (control) | **PASS** |
| `promo_intensity` all-zero — *the exact P0032 failure* | **CAUGHT** `constant (0)` |
| `lag_1` all-null | **CAUGHT** `all-null` |
| `weighted_dist` constant | **CAUGHT** `constant (0.5)` |

Full pipeline re-run afterwards: **8/8 clean**. No degenerate features in current
data, which is the correct outcome — the guard is a tripwire, not a finding.

The error message names the likely causes (empty source measure at this scope,
or missing inputs) and states the DEC-NO-PROMO-FILL rule, so whoever hits it is
not left to rediscover this session's reasoning.

---

## F77 — metric reporting fixed: mean MAPE dropped, medMAPE promoted, log1p paired

Three changes acting on F72 and F75, all in the reported tables rather than in
the models — deliberately, since tuning a baseline until it flatters the models
it is compared against is not a defensible move.

**1. `mean MAPE` dropped from the benchmark table.** It read 1e12 – 1e15 % for
every model *including SeasonalNaive*. Cause measured: MAPE divides by the
actual, guarded as `max(y, 1e-9)`, and **92 of CSD's 665 test rows (13.8%) are
exactly zero** at parent scope, so a one-unit error there scores 1e11 %. Still
written to `metrics.csv` — the raw numbers are evidence — but no longer reported
as a headline a reader might quote.

**2. medMAPE promoted to headline for the statistical baselines**, WMAPE kept
alongside with a caption explaining why. The table is now readable: Prophet beats
ARIMA on Danskvand (37.1% vs 48.4%) and loses elsewhere, which is a sentence the
thesis can carry. Energidrikke's WMAPE of 975.6% is still visible but no longer
leads.

**3. `log` → `log1p` in both baseline fit paths.** Both fitted on
`np.log(max(y, 1.0))` and inverted with `np.expm1()`. Those do not pair — `expm1`
inverts `log1p`, not `log` — leaving a constant −1-unit bias on every prediction,
negligible at 1e6 units and material for the small brands that dominate the
per-series median. `log1p` also removes the need for the `max(y, 1.0)` floor,
which silently rewrote genuine zeros as ones.

**The divergence itself is untouched.** F72's recommendation stands: Prophet's
unbounded linear trend fitted in log space is still capable of predicting 101M
against 301k actual. What changed is that the reported metric no longer lets one
series set a category's number. Capping the trend remains available and remains
Brian's call.

---

## F78 — P0036 task 7: `weighted_dist` is exonerated, but it does not earn its place

**The suspicion was leakage. It is not leakage.**

P0032 flagged `weighted_dist` correlating with the target at 0.756, above
`lag_1`'s 0.585 — backwards for a supposedly exogenous variable. Re-measured on
the current matrix: **0.674**, still above every lag (~0.445). So the pattern is
real and survived the scope fix.

**Tested rather than assumed.** `weighted_dist` is never lagged in
`engineer_features.py` — it enters as month t's own value, unlike
`promo_intensity`. That makes it a leakage candidate. But:

| Test | Result | Reading |
|------|--------|---------|
| corr(wd[t], target[t]) vs corr(wd[t], target[t-1]) | 0.6732 vs 0.6634 | no same-month spike |
| corr(wd[t], wd[t-1]) | **0.9764** | highly persistent |
| corr(wd[t], wd[t+3]) | **0.9459** | still knowable 3 months out |
| median month-on-month change | **0.00114** (0-1 scale) | structural, not volatile |

It is a "how widely is this brand stocked" variable that barely moves. Using
t's value as a proxy for t+3 is defensible because it *is* essentially t+3's
value. **Not leakage.**

### But the sensitivity check says drop it anyway

The task asked for a fit-with/without comparison. LightGBM, 300 trees, three
seeds (identical results — deterministic here, so no seed variance to hide in):

| Category | base | +wd[t] | +wd[t-1] | verdict |
|----------|-----:|-------:|---------:|---------|
| CSD | **17.20%** | 18.24% | 18.32% | hurts |
| Danskvand | 33.39% | 34.36% | **32.89%** | hurts unlagged, helps lagged |
| Energidrikke | 17.40% | 16.94% | **16.86%** | helps |
| RTD | **31.83%** | 32.54% | 31.26% | hurts unlagged |

**Hurts in 3 of 4 categories.** Where it helps, the lagged form helps more — so
if it is kept it should be lagged, which also removes the timing objection
entirely.

**Recommendation (Brian's call)**: drop `weighted_dist` from the models' FEATURES
list, or replace it with a lagged variant. Keeping it unlagged is the one option
the evidence does not support. Not changed here — it alters reported model
results, which is a thesis decision rather than a pipeline fix.

---

## F79 — the redundancy half found something worse: same-month measures in the feature list

The task's premise was multicollinearity: `sales_value` / `sales_liters` /
`sales_units` are the same quantity in different units. Confirmed — pairwise
correlations **0.90 to 0.997** across all four categories.

**But the real problem is timing, not duplication.**

`sales_value` and `sales_liters` sit in the **manifest's `features` list**, and
they are **contemporaneous**: they describe the same month as the target, with no
shift applied (each equals its own t-1 value on only ~12% of rows). They are the
same trading activity measured in kroner and litres.

**Ruled out the stronger charge first.** No feature is a copy of the current
month's sales — tested by matching every manifest feature against
`sales_units` shifted 0..4 periods: `lag_1..lag_4` match their own stated shift
at **100.0%**, and **nothing** matches shift 0. The lags are exactly what they
claim. Raw correlation alone could not have shown this, since sales are
autocorrelated and a correct lag also correlates ~0.94.

**Measured the cost of the exposure** (CSD H=3, LightGBM):

| Feature set | WMAPE |
|-------------|------:|
| base (what models train on today) | 17.20% |
| base + `sales_value` + `sales_liters` | **15.02%** |

A **2.2pp "improvement" bought by reading the month being forecast.**

**Why this mattered now**: nothing trained on them only because the modelling
scripts carried a hardcoded FEATURES list — and F74 made that list open-world
earlier in this same session. A maintainer selecting "all manifest features"
would have picked them up and got a flattering, wrong result.

### Fixed at the definition, not the call site

Added `CONTEMPORANEOUS_COLS` to `step_6_save_outputs.py`, excluded from the
manifest's `features`. Feature counts drop 43 → 31 (CSD/Energidrikke), 25 → 23
(Danskvand), 41 → 30 (RTD).

**The columns remain in the matrix.** `sales_units` is the target's source and
the rest are legitimate EDA material; they are simply no longer *advertised* as
model inputs. A lagged version of any of them would be a fair feature and should
be built in `engineer_features.py` like `promo_intensity` — not smuggled in
unshifted.

**Verified**: benchmark re-run gives identical results (CSD 17.5%, Danskvand
34.4%, Energidrikke 14.8%, RTD 33.1%), confirming current models never used
them. This closes a future hazard rather than changing a present finding.

