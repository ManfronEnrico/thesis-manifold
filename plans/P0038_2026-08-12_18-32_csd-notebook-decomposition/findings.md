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
