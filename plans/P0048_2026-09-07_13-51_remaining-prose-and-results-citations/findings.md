---
pid: P0048
created: 2026-09-07 16:40:00
updated: 2026-09-07 16:40:00
---

# P0048 — Findings

Every finding below was measured in-session, not inferred. Each carries the command
or file that reproduces it, because the session that found them is not recoverable.

---

## F1 — The forecast horizon never reaches feature construction (**critical**)

`engineer_features()` in
`01_SRQ1_Model_Training/01_thesis_data/_02_preprocessing/nielsen/_shared_modules/engineer_features.py`
has **no `horizon` parameter**, and `step_4_engineer_features.py` passes none. Lags
are built as `g[target_col].shift(lag)`, so `lag_1` is month *t−1* at every horizon.

At a genuine 3-month horizon, forecasting *t* from origin *t−3*, `lag_1` must be
*t−3*.

**Reproduce:** merge the two CSD matrices on `brand × period_year × period_month`.
Across all 4,370 shared rows, `sales_units`, `lag_1`, `lag_3`, `lag_13` are identical.
The sole difference between h1 and h3 is `min_periods` (15 vs 17), dropping 11 brands
and 506 rows.

`grep -n "horizon" engineer_features.py` returns **only comment lines** — the word
never appears in executable code.

**Verdict: a bug, not a simplification.** Step 3's docstring states the intent
explicitly ("The primary reported horizon is 3 months... Both are real runs, so
`--horizon` is a CLI argument"), and the surrounding plumbing is deliberate:
`min_periods = warmup + horizon + 1`, `n_origins = n_test − horizon + 1`, plus a
contract that hard-fails if the filename horizon disagrees with the body. Nobody
documents a design that precisely and then intentionally omits its implementation.

**Fix:** lags become `shift(lag + h − 1)`; rolling windows shift identically. One
function. Everything downstream of it is already correct.

---

## F2 — The published SRQ1 results are the h3 file, and there are no H1 results

Every SRQ1 script hardcodes `_feature_matrix_h3.parquet` inline. `grep -rn "_h1"` over
`01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/*.py` returns
**nothing**. No horizon CLI flag exists (only `--trials`, `--grain`, `--grains`).

Confirmed by row count. `summary.md` reports CSD `n_train 1805, n_test 665,
n_series 95`. After `dropna(subset=["log_sales_units","lag_1","lag_13"])`:

| matrix | train | test | series |
|---|---|---|---|
| h1 | 2014 | 742 | 106 |
| **h3** | **1805** | **665** | **95** |

Combined with F1: **the thesis reports one-month-ahead accuracy while describing a
three-month horizon.** Benchmarking "both horizons" today would produce two nearly
identical result sets differing only by brand coverage — which would not support the
1-month vs 3-month storyline, and a reader comparing them would notice.

**19 scripts need the hardcoded `_h3` parameterised** before both horizons can run.

---

## F3 — The feature count is 13, not 14; `weighted_distribution` is not a model input

`srq1_benchmark.py::FEATURES` has 13 entries and does **not** contain
`weighted_distribution`. Confirmed against the trained artefacts at
`05_thesis_results/srq1_model_performance/models/<cat>/metadata.json`:

| category | n features |
|---|---|
| CSD | 13 |
| energidrikke | 13 |
| danskvand | **12** |
| RTD | **12** |

Promo-zero categories omit `promo_intensity` rather than zero-filling — a constant-zero
column would assert "no promotion ran", which the data does not support
(DEC-DISCOVER-COLUMNS). So the feature set genuinely differs across categories, and
cross-category comparison must account for a difference in available *information*,
not just values.

**The thesis is wrong, not the code.** Ch4 §4.3 asserts `weighted_distribution` "**is**
the fourteenth input feature".

**Resolves discrepancy 2 in the holiday note**: post-enrichment the count is **16**,
not 17.

---

## F4 — The split is proportional and recomputed, not locked or pre-registered

`resolve_split_cutoffs()` derives **70 % / 15 % / remainder** over distinct periods
(`DEFAULT_TRAIN_FRAC = 0.70`, `DEFAULT_VAL_FRAC = 0.15`).

The code comment records why fixed dates were abandoned: they had drifted to a
24–27 % test share against an intended 15 %, because every refreshed month lands in
whichever split is the remainder.

Current boundaries, from the 8 step-3 contracts (identical at both horizons):

| Category | Periods | Train | Val | Test | Train end | Val end |
|---|---|---|---|---|---|---|
| CSD | 46 | 32 | 7 | 7 | 2025-05 | 2025-12 |
| Danskvand | 41 | 29 | 6 | 6 | 2025-07 | 2026-01 |
| Energidrikke | 43 | 30 | 6 | 7 | 2025-06 | 2025-12 |
| RTD | 41 | 29 | 6 | 6 | 2025-07 | 2026-01 |

**The panel has grown** — CSD is 46 periods, not the 42 the thesis states.

Ch4 §4.4 is wrong on all counts, and **Brian's own Word threads already say so**: 183
("Dynamic Train/Test/Val sets based on percentage cutoff"), 185 ("Not locked"), 187,
191 ("All test windows end in March 2026" — they end 2026-07). All eight threads
(183–191) are closable by one section replace.

**Side effect:** training windows are now 29–32 months, so the "~24-period ARIMA
minimum; danskvand and RTD at 23 are marginally below" caveat is obsolete. The
staged prose **drops** that claim rather than sourcing it, which closes threads 184
and 189 by removing what they objected to.

---

## F5 — SRQ4 can evaluate at H3 with ground truth retained

`_brand_history()` in `04_SRQ4_Scenario_Experiment/scenario_setup/srq4_experiment.py`
is well built: it returns the target month **explicitly** (so Scenario A cannot anchor
on wall-clock time and score a different month than B and C), and `_assert_no_leakage`
hard-fails if the target appears in the history handed to an agent.

Measured today: last fit month **2025-12** → target **2026-01** = a **1-month** gap at
both h1 and h3, because it takes `test.iloc[0]`.

There are **7 held-out test months** (2026-01 … 2026-07) with actuals present.
Evaluating at 3 months requires selecting `test.iloc[2]` and ending the supplied
history 3 months before target. The leakage assertion already covers the wider gap.

**Brian's requirement — verify against held-out real values for every scenario — is
satisfiable at H3.**

---

## F6 — MIN_PERIODS is derived, which retracts a stated limitation

`min_periods = warmup + horizon + 1` → **15 at H1, 17 at H3**
(`derive_lag_structure()`). A brand-month is usable only once its lag features are
defined, so a shorter series yields no usable observation under the specification.

The thesis states MIN_PERIODS = 30 and concedes it as "EDA-driven, not theory-first"
— a limitation. It is now *derived*, so that concession can be **retracted**, not
merely renumbered. Worth writing deliberately.

A third live value (40, in the old notebook) was removed 2026-08-18 for the same
reason.

---

## F7 — Ch8 accuracy numbers are stale twice over

Ch8 §8.2 states "Test WMAPE: CSD 16.5%, danskvand 22.0%, energidrikke 11.4%
(≈ the ≤15% industry target), RTD 31.0%".

Current `tuned_summary.md` (tuned XGBoost): CSD **15.0**, danskvand **20.9**,
energidrikke **13.1**, RTD **36.0**. RTD moved materially worse.

So the numbers are wrong against current output *and* they describe a horizon the
pipeline does not implement (F1). Both need the re-run.

Note also the "≤15% industry target" phrasing — P0041 recorded that target as
**unsourced and withdrawn** from Ch6/Ch9/Ch10. It appears to survive here.

---

## F8 — Chapter 8's design subsections are still bullets with stale placeholders

Ch8 splits cleanly: every **Results** subsection is real prose with real numbers,
while every **design** subsection is unconverted bullets — Benchmark design, Metrics,
Baselines, LLM-as-Judge protocol, Calibration check, RAM profiling, Latency profiling,
Failure mode analysis.

Some carry placeholders that were never filled: `[N] SKUs × 28 retailers × [T] weeks`.
The weekly framing also contradicts the brand × month grain locked since DEC-GRAIN.

Ch7 (1,189 w), Ch8 (1,339 w) and Ch9 (1,194 w) are the thin chapters. Ch4 is in better
shape than expected — genuine prose throughout — but its numbers are stale (F3, F4).

---

## Cross-cutting: the results folder is almost entirely uncited

`05_thesis_results/` holds ~317 files:

- **26 appendix tables**, export-ready, regenerated 2026-09-07 by `export_appendix.py`
- **44 SRQ1 tables** (`srq1_model_performance/tables/`)
- **per category: 31 EDA tables + 8 plots** — seasonal decomposition, ACF/PACF, ECDF,
  correlation heatmaps, promo intensity

The thesis cites **2 figures total** (`table-of-figures.md`). Chapter 4 cites none of
the EDA plots.

Also visible in `table-of-tables.md`: **Table 10 is captioned "NO IDEA"**, and Tables
9 and 12 carry typos ("Exclud", "adn"). Cosmetic, but they are in the document.

---

## F(new) — Chapter order: Ch5 sits before the chapter it depends on

Raised by Brian 2026-09-07 while reviewing the research-question figure, which
shows SRQ1→Ch6, SRQ2→Ch5+7, SRQ3→Ch5+7+9, SRQ4→Ch8. His question was whether the
scatter is a red flag and whether the chapters should be regrouped by SRQ.

**The scatter is not the problem.** SRQ3 being answered across 5, 7 and 9 is what
a synthesis question looks like, and a discussion chapter drawing on earlier
chapters is what discussion chapters do. Reordering to tidy a diagram would be
optimising for the diagram.

**The forward dependency is the problem**, and it is real. Ch5 §5.3 is titled
"The Forecasting Substrate (SRQ1)", describes the model set, and defers with
"benchmarked in Chapter 6". The architecture chapter explains the artefact whose
evidence arrives only in the *next* chapter — the reader meets the substrate as
an assumption and learns later whether it works.

### Why "regroup Ch5 and Ch7 under SRQ2" does not work

Ch5 is not an SRQ2 chapter. Its §5.2 presents the artefact as three layers and it
carries a section per SRQ: 5.3 SRQ1, 5.4 SRQ2, 5.6 SRQ3, 5.7 SRQ4. Regrouping it
would mean **splitting the chapter**, not moving it — and an architecture chapter
that presents the whole artefact before the evaluation chapters take it apart is
a legitimate structure worth keeping.

### Recommended: a single swap, Ch5 ↔ Ch6

| | Now | Proposed |
|---|-----|----------|
| 4 | Data | Data |
| 5 | Framework design | **Model benchmark** |
| 6 | Model benchmark | **Framework design** |
| 7 | Decision synthesis | Decision synthesis |
| 8 | Experimental evaluation | Experimental evaluation |

Gives data → models → architecture → synthesis → evaluation: the DSR build order
and the repo's own tier order agree with it. Ch5's per-SRQ sections stay intact
and Ch7–Ch10 do not move.

**Check before executing: DONE 2026-09-08, and it passes.** Measured against
snapshot `2026-09-07_19-41_internal-links`:

| Direction | Count | Nature |
|---|---|---|
| Ch5 → Ch6 | 4 | all **forward** pointers ("benchmarked in Chapter 6") |
| Ch6 → Ch5 | **0** | Ch6 never cites Ch5 |

Ch6 is self-contained: it defines its own model set, split, metrics and protocol,
and uses the word "substrate" exactly once, inside a sentence about Ch2. §6.3.2
"Feature engineering" describes the matrix directly and does not lean on Ch5.
The dependency is strictly one-way, so the swap converts four forward promises
into backward references — the reader meets the evidence before the architecture
that assumes it.

**Two wins independent of the swap:**
- An SRQ→chapter map table in Ch1 does more for the reader than any reordering.
- Ch8 §8.2 is "Level 1 — ML accuracy evaluation (SRQ1)" while Ch6 already reports
  SRQ1 results. That overlap deserves a look on its own terms.

**Cost**: touches every cross-reference, figure and table number, and the Word
document. Cheaper now than after the remaining prose lands — an argument for
deciding soon, not for doing it hastily.

### Execution recipe (measured 2026-09-08, P0050 session)

**Cost is lower than the paragraph above assumed.** No path contains a chapter
number that is typed by hand, so the code half is one line.

**1. Code — one edit.** Swap the two entries in `CHAPTER_SLUGS` (`PATHS.py:175`):
`"architecture"` and `"model_benchmark"`. `CHAPTER_ORDER` derives from position,
`_chapter_folder()` derives the `NN_` prefix from that, and every constant and
helper derives from those. `export_appendix.py`'s `_TABLE_CHAPTER` keys on
**slugs**, so it needs nothing.

**2. Results folders — two renames.**
`05_thesis_results/05_architecture/` → `06_architecture/`, and
`06_model_benchmark/` → `05_model_benchmark/`. Do these together; the numbers
collide if done one at a time without a temp name.

**3. Diagram stems — 6 files + the generator.**
`ch5_layered_architecture_v2`, `ch5_tool_interface_v1`, `ch5_architecture_v1`
(superseded, retained) → `ch6_*`; `ch6_model_selection_v2`,
`ch6_modelling_pipeline_v1`, `ch6_resource_profile_v2` → `ch5_*`. Stems are
string literals in `generate_architecture_diagrams.py` (lines ~360, 448, 533,
886, 968); `_out_for()` parses the `ch<N>_` prefix to route, so a renamed stem
lands in the renumbered folder automatically. `_check_stem()` raises on a stem
without the prefix, so a typo fails loudly rather than silently.

**4. Word prose — ~30 edits.** 2 chapter titles, ~10 cross-chapter references
(Ch1×5, Ch3×1, Ch7×1, Ch8×3, Ch9×2, plus the ToC), and ~18 internal `§6.x` refs
inside the benchmark chapter that become `§5.x`.

**⚠ The trap: three `§5.2` references in Ch6 are CITATIONS, not sections** —
*Hyndman & Athanasopoulos (2021, §5.2)*, at ch6 lines 17, 27 and 259 of the
snapshot. A find-and-replace of `§5.` or `§6.` across that chapter corrupts them.
Exclude them explicitly.

**5. Draft image links.** `06_thesis_writing/sections-drafts/ch5-framework-design.md`
carries `05_thesis_results/05_architecture/figures/ch5_layered_architecture_v2.svg`.
Re-resolve every image path after the rename — P0050's end-of-day pass found three
links broken this exact way (repointed before a later rename).

**6. One judgement call.** Ch6 §6.7's SRQ table row reads "integration readiness
is addressed in Ch3 and Ch5" — after the swap that becomes a forward reference.
Still correct, no longer "as established". The same sentence in Ch7 and Ch8 is
unaffected.

---

## F9 — The horizon defect is FIXED in code and matrices, but NOT in results (2026-09-07)

**Supersedes F1's "proposed, not applied" status.** P0049 landed the fix while this
plan's session was compacted.

**Code:** `engineer_features()` now takes `horizon: int` as a REQUIRED parameter
(`_shared_modules/engineer_features.py:452`), documenting that `lag_k` becomes
`shift(k + horizon - 1)` and shift(1) features become `shift(horizon)`.

**Matrices:** regenerated 2026-09-07 15:59. Verified on CSD:

| check | result |
|---|---|
| lag columns identical across h1/h3 | **False** (was True — this was the bug) |
| `lag_1` == `shift(1+3-1)` at h3 | **True** |
| naive `shift(1)` at h3 | False |

`n_test_origins = 5` now appears in the manifest, so the horizon reaches evaluation too.

**⚠ Results are NOT regenerated.** `tables/metrics.csv` and `pooled_summary.md` are dated
2026-09-06 22:55/23:12 — *before* the 15:59 matrix regeneration. Every SRQ1 accuracy
number currently in `05_thesis_results/` is therefore still one-month-ahead in substance.
`srq1_model_performance/h1/` exists but is **empty**.

**Consequence for prose:** structural claims about the pipeline (how the split is derived,
that lags are horizon-offset, feature composition) can be written now. **Accuracy numbers
cannot** — they will move when the benchmark re-runs.

## F10 — The feature matrix now carries holiday features and 34 features, not 13

CSD h3 manifest (regenerated 15:59): **54 columns, 34 features, 95 brands, 4,370 rows**;
h1 has 4,876 rows.

The matrix includes `days_in_month`, `n_holidays`, `non_holiday_days` — the P0047 holiday
enrichment. **F3's "13 features" was the modelling FEATURES list in `srq1_benchmark.py`,
not the matrix width**, and the two must not be conflated in prose:

| count | what it is |
|---|---|
| 54 | columns in the parquet (includes raw Nielsen measures, target, split, keys) |
| 34 | `n_features` per the manifest |
| 13 | features the benchmark actually trains on (pre-holiday) |
| 12 | the pooled-vs-per-category intersection (`promo_intensity` dropped) |

Ch4 §4.1.2's "22 columns" matches none of these. Flagged, not amended — establish what it
was counting first.

## F11 — Comment 136 (survey-type) is decisively wrong, and the metadata says so

The word "survey" appears **nowhere** in the Nielsen metadata (0 hits across all five
categories' `metadata_*_columns.jsonl` plus both index files). The only provenance term
present is **"scanner"** (7 hits), and `NIELSEN_METADATA_INDEX.json` describes
`sales_value` as *"Consumer retail price including VAT (point-of-sale scanner data)."*

Scanner data is a census of transactions at participating retailers, not a sample-based
survey instrument. The thesis's "survey-type" claim is unsupported by the only metadata
available and should be replaced with the sourced term.

## F12 — Comment 134 (totalbeer) is confirmed; the thesis states the opposite of the truth

`save_all_datasets.py` registers `totalbeer_clean_facts_v` and `totalbeer_clean_facts` in
its download config, and `_00_raw/nielsen/data_jsonl/Totalbeer/metadata/` exists on disk.
The fact table **does** exist. The script's own docstring: *"Totalbeer is out of scope for
the thesis (dropped from the prose on compute-constraint grounds, P0034)."*

The thesis says the data "do not exist at source, not a size or memory constraint" and
calls it a data limitation. Both halves are inverted: it exists, the constraint WAS
compute, and it is an analytical choice.

## F13 — Comment 135 understates its own case

The three non-CSD categories are not "parallel proofs of concept" — they carry the
pooled-vs-per-category finding (`tables/pooled_summary.md`), which is only possible
because all four ran. Pooling helps the small categories and hurts CSD:

| | LightGBM | XGBoost |
|---|---|---|
| CSD | +1.2 pp (per-cat wins) | +3.8 pp (per-cat wins) |
| danskvand | −2.2 pp (pooled wins) | −1.2 pp (pooled wins) |
| energidrikke | −1.6 pp (pooled wins) | −2.8 pp (pooled wins) |
| RTD | +0.7 pp | +1.3 pp |

⚠ These numbers are pre-fix (see F9) — the *pattern* is the citable claim, not the digits.


## F14 — The Ch5/Ch6 swap is DONE in Word; prose refs repaired in a note (2026-09-08)

Snapshot `2026-09-08_14-05_chapter-reorder` confirms the swap landed:
**Ch5 = Model Benchmark & Selection** (4,738 w), **Ch6 = Predictive-Extension
Architecture** (2,153 w). Ch7-Ch10 unmoved, as phase 8 predicted.

**Word auto-renumbered every heading.** `## 5.1 Rationale for model selection` etc. are
already correct. **Body-text references did not** — they are plain text. That split is the
whole content of the repair.

**37 stale references found and written as verified find/replace pairs** in
`06_thesis_writing/writing-notes/ch5-ch6-swap-reference-repair.md`:

| block | count | what |
|---|---:|---|
| A | 20 | `§6.x` → `§5.x` inside the benchmark chapter |
| B | 2 | `Section 5.x` → `Section 6.x` inside the architecture chapter |
| C | 12 | cross-chapter refs in ch1-ch4, ch8, ch9 |
| D | 3 | the SRQ3 table row, which appears in ch5, ch7 AND ch8 |

**Every find-string was verified to occur exactly once** against the snapshot
(scripted check). Three of my first drafts did not match and were corrected:

1. **A20** used a straight apostrophe; the document has a curly one.
2. **C3a** — I recorded the wrong sentence ending. The real ch3 reference is
   *"the RSS measurements are reported in Chapter 6"*, a **fourth** ch3 ref sitting at the
   tail of a `psutil`/`tracemalloc` sentence, nowhere near another chapter pointer.
3. **D** — the SRQ3 row is in **three chapters**, not one, and lives in the *benchmark*
   chapter rather than the architecture chapter. It also points at integration readiness,
   which is §6.6 — so all three rows now say Ch5 where they mean Ch6.

**Two traps recorded in the note:**

- **Three `§5.2` refs in the benchmark chapter are citations to Hyndman & Athanasopoulos
  (2021, §5.2)**, not thesis sections (lines 17, 27, 259). A blanket find/replace on
  `§5.` or `§6.` corrupts them into self-references. Every pair is word-anchored.
- **Snapshot filenames are now inverted**: `chapters/ch5-framework-design.md` holds
  *Model Benchmark*, `chapters/ch6-model-benchmark.md` holds *Architecture*. The exporter
  keeps the slug it first assigned. Key scripts off `MANIFEST.md`, never the filename.

**Also fixed, pre-existing:** A4/A9 cite **§6.2.0**, a section number that exists in
neither numbering. Correct target is **§5.2.1** ("Simple benchmarks").

**Also correct-by-accident, do not "fix":** ch2's *"shown in Chapter 5 to sit well within
the budget"* — the realised RAM footprint is §5.5.6, in the benchmark chapter. Right
before the swap for the wrong reason, right after it for the right one.

**Repo-side half (PATHS.py, folder renames, 6 diagram stems) is NOT done** — still P0050's.

## F15 — Archived snapshots untracked from git (2026-09-08)

Four archived snapshots were tracked as **1,306 files** of derived markdown. Now
gitignored via `06_thesis_writing/docx-exported-snapshots/.archive/`; files remain on disk.
Only the current snapshot is tracked. Rationale in that folder's README: a snapshot mirrors
the `.docx` at one moment, and the `.docx`'s own history is the OneDrive version history.
