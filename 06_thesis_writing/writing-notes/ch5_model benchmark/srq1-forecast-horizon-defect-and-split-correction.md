---
name: srq1-forecast-horizon-defect-and-split-correction
description: NOTE - Investigation of the H1/H3 forecast-horizon implementation. Finds the horizon never reaches feature construction, so both matrices are one-month-ahead tasks. Bullet skeleton, the code fix, and prose for the split and feature-engineering sections once results are regenerated.
category: reference
applies-to: [ch4 §4.3, ch4 §4.4, ch6 §6.3, ch6 §6.5, ch8 §8.2, ch9 §9.4]
triggers: [writing up the forecast horizon, answering Word threads 183-191, reporting the train/val/test split, benchmarking H1 vs H3]
created: 2026_09_07-16_10
updated: 2026_09_07-16_10
---

# Forecast horizon (H1 / H3) — defect, correction, and the split rewrite

**Status: prose in PART 2B is written but MOSTLY BLOCKED on a code fix and a
re-run.** Read PART 0 first. Only block P1 (the split correction) is safe to paste
today; the horizon prose depends on numbers that do not exist yet.

**Every number below is read from a result file or measured programmatically.**
Sources: the step-3 contracts (`<slug>_eda_findings_h{1,3}.json`), the engineered
parquets, `summary.md`, `tuned_summary.md`, and the trained model metadata.

---

## PART 0 — THE FINDING, AND WHY MOST OF THIS IS BLOCKED

### 0.1 The horizon never reaches feature construction

The pipeline threads a `--horizon` argument carefully through parameter derivation,
contract validation and filename tagging, and then never uses it to build features.

- `engineer_features()` has **no `horizon` parameter**. Step 4 does not pass one.
- Lags are built as `g[target_col].shift(lag)`, so `lag_1` is month *t−1* at **both**
  horizons.
- At a genuine 3-month horizon, forecasting month *t* from origin *t−3*, `lag_1`
  must be *t−3*, not *t−1*.

**Verified by merging the two matrices on brand × year × month:** across all 4,370
shared CSD rows, `sales_units`, `lag_1`, `lag_3` and `lag_13` are **identical**.
The only difference between h1 and h3 is `min_periods` (15 vs 17), which drops 11
brands and 506 rows.

**So neither matrix is a 3-month forecast. Both are one-month-ahead tasks on
different brand subsets.**

### 0.2 This is a bug, not a documented simplification

Step 3's own docstring states the intent:

> "The primary reported horizon is 3 months — the quarter is the period in which
> marketing budgets are authorised... Both are real runs, so `--horizon` is a CLI
> argument."

The surrounding plumbing is deliberate and correct: `min_periods = warmup +
horizon + 1`, `n_origins = n_test − horizon + 1`, and a contract that hard-fails if
the filename horizon disagrees with the body. Nobody documents a design that
specifically and then intentionally omits the one line that implements it.

### 0.3 What the published results actually are

Every SRQ1 script hardcodes `_feature_matrix_h3.parquet` inline. There is **zero**
occurrence of `_h1` anywhere in the SRQ1 training code, and no horizon CLI flag.

Confirmed by row count: `summary.md` reports CSD `n_train 1805, n_test 665,
n_series 95`. The h3 matrix after `dropna` gives exactly 1805 / 665 / 95; h1 gives
2014 / 742 / 106.

**The published numbers come from the h3 file — but per §0.1 that file is a
one-month task. So the thesis currently reports one-month-ahead accuracy while
describing a three-month horizon.**

### 0.4 The fix, and its blast radius

The change is one function; the consequences are not.

At horizon *h*, lags become `shift(lag + h − 1)` — at H3, `lag_1` is *t−3*. Rolling
windows shift identically. Everything else in the pipeline is already correct.

| Affected | Action |
|---|---|
| `engineer_features()` | Add `horizon` param; step 4 passes it |
| 8 feature matrices (4 categories × 2 horizons) | Regenerate |
| SRQ1 benchmark, tuned, CV, calibration, SHAP, stat baselines, profiling | Re-run — **every published accuracy number changes** |
| 19 SRQ1 scripts | Parameterise the hardcoded `_h3` so both horizons can run |
| SRQ4 scenario runs | Re-run at both horizons |
| Ch4, Ch6, Ch8 | Rewrite against new output |

**Expect H3 accuracy to get worse.** Forecasting three months out is harder than one.
CSD's 15.0 % WMAPE will rise. That is the honest number for the task the thesis
claims to perform, and it is defensible; the current number is not, because it does
not measure what the surrounding prose says it measures.

### 0.5 SRQ4 at H3 is feasible — the harness is already built for it

`_brand_history()` in `srq4_experiment.py` is sound: it returns the target month
**explicitly** (so Scenario A cannot anchor on wall-clock time) and hard-fails via
`_assert_no_leakage` if the target appears in the history handed to an agent.

Measured today: last fit month **2025-12** → target **2026-01** = a **1-month** gap,
at both h1 and h3 (it takes `test.iloc[0]`).

There are **7 held-out test months** (2026-01 … 2026-07) with actuals present. To
evaluate at 3 months, select `test.iloc[2]` and end the supplied history 3 months
before target. **The ground-truth requirement you asked about is preserved** — the
actuals exist for every horizon up to 7 months, and the leakage assertion already
covers the wider gap.

### 0.6 What is blocked

| Block | Status |
|---|---|
| **P1** — Ch4 §4.4 split correction | **READY.** Independent of the horizon bug; closes 8 Word threads |
| **P2** — Ch4 §4.3 feature count | **READY.** Resolves the note's open `weighted_distribution` question |
| **P3** — Ch4 §4.4 horizon design | **BLOCKED** on the fix + regeneration |
| **P4** — Ch6/Ch8 dual-horizon results | **BLOCKED** on the re-run; no H1 numbers exist |

---

## PART 1 — BULLET SKELETON

### 1.1 The split is proportional, not locked (P1)

- Cutoffs come from `resolve_split_cutoffs()`: **70 % train / 15 % validation /
  remainder test**, over distinct periods.
- Derived from the panel, **not** fixed calendar dates. Recomputed on every data
  refresh.
- Rationale in the code: fixed dates had drifted to a 24–27 % test share against an
  intended 15 %. Proportions hold the ratio steady as the panel grows and keep
  categories with different start dates comparable — which the cross-category
  ranking depends on.
- **The panel has grown.** CSD is now **46 periods**, not 42. All four categories
  gained months.
- Current boundaries (from the step-3 contracts, identical at both horizons):

| Category | Periods | Train | Val | Test | Train end | Val end |
|---|---|---|---|---|---|---|
| CSD | 46 | 32 | 7 | 7 | 2025-05 | 2025-12 |
| Danskvand | 41 | 29 | 6 | 6 | 2025-07 | 2026-01 |
| Energidrikke | 43 | 30 | 6 | 7 | 2025-06 | 2025-12 |
| RTD | 41 | 29 | 6 | 6 | 2025-07 | 2026-01 |

- **No test window ends in March 2026** — they end 2026-07. Thread 191 is correct.
- Every training window now comfortably exceeds the ~24-period ARIMA rule of thumb
  (29–32 months), so the "danskvand and RTD at 23 are marginally below" caveat is
  **obsolete** and should be deleted, not restated.

### 1.2 MIN_PERIODS is derived, not chosen (P1/P3)

- Old prose: MIN_PERIODS = 30, "EDA-driven, not theory-first", conceded as a
  limitation.
- Now: `min_periods = warmup + horizon + 1` → **15 at H1, 17 at H3**.
- It is not a free parameter. A brand-month is usable only once its lag features are
  defined; a shorter series yields no usable observation under the specification.
- **This retracts a stated limitation.** Worth writing deliberately rather than
  swapping the number silently.

### 1.3 The feature count is 13, not 14 (P2)

- `srq1_benchmark.py::FEATURES` contains **13** entries and does **not** include
  `weighted_distribution`.
- Confirmed against the trained artefacts (`models/<cat>/metadata.json`):
  CSD 13, energidrikke 13, danskvand **12**, RTD **12**.
- Promo-zero categories drop `promo_intensity` rather than zero-filling it, because
  a constant-zero column would assert "no promotion ran" — which the data does not
  support (DEC-DISCOVER-COLUMNS).
- **So the thesis is wrong, not the code.** `weighted_distribution` is carried in
  the matrix but is not a model input.
- This resolves discrepancy 2 in `srq1-holiday-enrichment-result-and-limitations.md`:
  the corrected count after holiday enrichment is **16**, not 17.

### 1.4 Horizon as a reported design (P3 — blocked)

- Two horizons: **H1** (one month ahead) and **H3** (three months ahead).
- H3 is the primary reported horizon — the quarter is the period in which marketing
  budgets are authorised, so it is the first horizon at which a forecast can change
  a decision.
- The horizon propagates to `min_periods` (15 / 17) and to evaluable test origins:
  `n_origins = n_test − horizon + 1`.

| Category | Test months | Origins @H1 | Origins @H3 | Brands @H1 | Brands @H3 |
|---|---|---|---|---|---|
| CSD | 7 | 7 | 5 | 106 | 95 |
| Danskvand | 6 | 6 | 4 | 30 | 29 |
| Energidrikke | 7 | 7 | 5 | 50 | 44 |
| RTD | 6 | 6 | 4 | 72 | 62 |

- A longer horizon costs both evaluable origins and eligible brands. Both are
  mechanical consequences of the specification, not judgement calls.

---

## PART 2 — PLACEMENT CONTRACT

**Snapshot these anchors are written against:** `2026-09-07_14-29_holiday-enrichment`.
Re-verify if the `.docx` has been edited since.

---

### P1 — Ch4 §4.4 Train, Validation, and Test Split — **READY**

> **File:** `chapters/sections/08-ch4-data-assessment/04-train-validation-and-test-split.md`
> **Closes 8 Word threads: 183, 184, 185, 187, 188, 189, 190, 191.**
> Threads 183 ("Dynamic Train/Test/Val sets based on percentage cutoff"), 185 ("Not
> locked"), 187 and 191 ("All test windows end in March 2026") are all correct — the
> code confirms every one of them.

**⚠ This section needs a full REPLACE, not an edit.** Both the framing (locked vs.
proportional) and every number in the table are wrong.

**Anchor (opening sentence):**
> "The split is defined by calendar date and locked as a pre-specified design decision, applied identically across the forecasting models and across categories."

**Action:** REPLACE — from this sentence through the closing sentence of the section,
> "All test windows end in March 2026 and cover at least one autumn/winter promotional cycle."

Paste §2.1 prose below, and replace Table 5 with the grid in §1.1.

**Also amend the Table 5 caption.** Current: "(locked, pre-registered)" — thread 187.
Replace with: *Proportional train/validation/test boundaries per category, derived
from each panel*.

**Assets:**
- **In-text:** Table 5 (replaced — the 6-column grid from §1.1, dropping the
  now-meaningless "Train window / Validation window / Test window" spans in favour of
  cutoffs).
- **Appendix, cite don't inline:** none required.
- **Figure:** not needed.

**⚠ Threads 184 and 189 ask for a SOURCE on the ARIMA ~24-period rule of thumb.**
The replacement prose **drops that claim entirely** rather than sourcing it — every
training window is now 29–32 months, so the constraint is not binding and does not
need to be argued. This closes both threads by removing what they objected to. If you
would rather keep the claim, it needs a real citation and I have not verified one.

---

### P2 — Ch4 §4.3 Feature Engineering — **READY**

> **File:** `chapters/sections/08-ch4-data-assessment/03-feature-engineering-forecasting-substrate.md`
> **Interacts with P1 of the holiday note** — see the sequencing constraint below.

**Anchor:**
> "The 14 features comprise six lags, three rolling statistics, three calendar features, “promo_intensity”, and weighted_distribution."

**Action:** REPLACE this sentence and the clause that follows it asserting
`weighted_distribution` **is** the fourteenth input feature.

Paste §2.2 prose below.

**Also — remove the `weighted_distribution` row from Table 4.** It is not a model
input.

**Assets:**
- **In-text:** Table 4 (one row removed).
- **Appendix:** none.

**⚠ SEQUENCING — this changes the holiday note's arithmetic.** That note's P1 says
amend "14 → 17". With `weighted_distribution` removed, the base is 13, so the
post-enrichment count is **16**. Apply P2 first, then the holiday note's P1 with 16.

**⚠ The "22 columns" discrepancy is still unresolved** and is *not* fixed here — the
CSD matrix has 52–54 columns depending on horizon. Flagged in the holiday note as
discrepancy 1; establish what it was counting before amending.

---

### P3 — Ch4 §4.4, new subsection: the forecast horizon — **BLOCKED**

> **Blocked on:** the `engineer_features()` fix and matrix regeneration (§0.4).
> **Why it cannot be written now:** the prose would describe a dual-horizon design
> that the data does not implement. Writing it against current output would put a
> false claim into the thesis.

**Intended action, once unblocked:** INSERT a new subsection after the split section,
using the §1.4 bullets. The origins/brands table is already correct — those numbers
come from the contracts and survive the fix.

---

### P4 — Ch6 §6.5 / Ch8 §8.2, dual-horizon results — **BLOCKED**

> **Blocked on:** the full SRQ1 re-run at both horizons.
> **No H1 results exist at all.** Every SRQ1 script hardcodes `_h3`.

**⚠ Existing prose is currently false and must not be left standing after the fix.**
Ch8 §8.2 reports "Test WMAPE: CSD 16.5%, danskvand 22.0%, energidrikke 11.4%, RTD
31.0%". These are stale against even the current output (`tuned_summary.md` gives CSD
15.0, danskvand 20.9, energidrikke 13.1, RTD 36.0) **and** they describe a horizon the
pipeline does not implement. Both problems need the re-run.

---

## PART 2B — THE PROSE

### §2.1 → goes to P1 (Ch4 §4.4, replacing the section body)

The split is defined proportionally rather than by fixed calendar dates. Each
category's panel is divided into seventy per cent training, fifteen per cent
validation and the remainder as test, measured over distinct monthly periods and
derived from the panel itself. No random shuffling is applied: a strict temporal
split preserves the autocorrelation structure and prevents observations from the
future entering training or validation.

The proportional rule replaces an earlier scheme of fixed cutoff dates, and the
reason is that a fixed date does not survive a growing panel. The Nielsen extract is
refreshed periodically, and every newly arrived month falls into whichever split is
defined as the remainder. Measured on the current extract, the two previous fixed
schemes had drifted to a test share of between twenty-four and twenty-seven per cent
against an intended fifteen. Proportions hold the ratio steady as the panel grows,
and they keep categories that begin at different dates comparable with one another,
which the cross-category comparison in Chapter 6 depends upon.

A consequence worth stating plainly is that the boundaries are recomputed whenever
the data are refreshed, so they are a reproducible rule rather than a fixed
pre-registration. The rule is fixed; the dates it produces are not. The boundaries
below were derived from the extract used throughout this thesis.

*(Table 5 here — the grid from §1.1.)*

The categories differ in length because their panels begin at different dates, so the
same proportions yield training windows of twenty-nine to thirty-two months and test
windows of six or seven. Every category therefore carries a training window
containing at least two full annual cycles, and a test window spanning at least two
calendar quarters.

### §2.2 → goes to P2 (Ch4 §4.3)

The thirteen features comprise six lags, three rolling statistics, three calendar
features and promotional intensity. Two clarifications resolve earlier ambiguity.
The log of sales units is the modelling target rather than an input: the models
predict log sales and exponentiate back, and using the target as a predictor would
be trivial leakage. The weighted-distribution metric is carried through the feature
matrix but is **not** a model input; neither is the raw promotional unit count, whose
derived intensity ratio is used instead.

The feature set is also not identical across categories, and this is deliberate.
Nielsen does not report promotional measures for danskvand or for ready-to-drink
beverages, so promotional intensity is omitted for those two categories rather than
filled with zeros, leaving them with twelve features apiece. A constant-zero column
would assert that no promotion ran, which is a claim the data does not support: the
measure is absent, not observed to be nil. Cross-category comparisons in the
benchmark chapter must therefore account for a genuine difference in available
information, not merely in values.

---

## PART 3 — Assets summary

| Prose | In-text asset | Appendix |
|---|---|---|
| §2.1 (Ch4 §4.4) | Table 5, fully replaced + caption amended | none |
| §2.2 (Ch4 §4.3) | Table 4, one row removed | none |
| P3 (blocked) | horizon origins/brands table | none |
| P4 (blocked) | TBD after re-run | none |

**Renumbering:** none. P1 and P2 replace existing tables in place.

---

## PART 4 — Provenance and open items

| Element | Source |
|---|---|
| Split fractions 70/15/remainder | `engineer_features.py` `DEFAULT_TRAIN_FRAC` / `DEFAULT_VAL_FRAC` |
| Drift to 24–27 % test share | `engineer_features.py` split-sizing comment (F25/F28) |
| Periods / train / val / test / origins | `<slug>_eda_findings_h{1,3}.json`, all 8 contracts |
| min_periods 15 / 17 | contracts; `derive_lag_structure()` = warmup + horizon + 1 |
| 13 features, 12 for promo-zero | `srq1_benchmark.py::FEATURES`; `models/<cat>/metadata.json` |
| h1/h3 lag identity | merge of the two parquets on brand × year × month, 4,370 rows |
| Published results are the h3 file | row-count match 1805/665/95 vs `summary.md` |
| SRQ4 1-month gap | measured on `csd_feature_matrix_h{1,3}.parquet`, COCA COLA |

### Unverified claims

**None.** Every statement in the prose rests on measured project data or on the
pipeline's own recorded parameters. No external citation is introduced, so nothing
here needs routing to `04-Claims_Verification/`.

The one claim deliberately **removed** rather than sourced is the ARIMA ~24-period
rule of thumb (threads 184, 189) — see P1.

### Discrepancies flagged, not fixed

1. **"22 columns"** — carried over from the holiday note. The CSD matrix has 52
   columns at h1. Unresolved; do not amend blind.
2. **Ch4 §4.2 EDA figures** are stale throughout (136 brands, 3,789 rows, 42
   periods, MIN_PERIODS 30, ADF and ACF values). Not addressed in this note — that is
   the §4.2 pass, and it should follow the regeneration so it is done once.

### Next action

**Decide on the horizon fix before writing P3 or P4.** Recommended: raise it with
Enrico first, since he regenerated the pipeline and the fix invalidates results he
produced. Suggested wording:

> Was `engineer_features()` meant to shift the target by the horizon? Step 3 derives
> `min_periods = warmup + horizon + 1` and its docstring says H3 is the primary
> reported horizon, but lags are `shift(lag)` at both horizons — so h1 and h3 come out
> as the same one-month task on different brand sets. Merging the two matrices, every
> lag column is identical across all shared rows.
