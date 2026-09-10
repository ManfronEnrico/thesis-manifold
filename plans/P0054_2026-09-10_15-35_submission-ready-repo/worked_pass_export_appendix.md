---
name: worked-pass-export-appendix
description: RULE - Full-file contextual pass over export_appendix.py, covering both its source comments and the appendix text it emits. Reference example for auditing a generator whose output ships.
category: reference
applies-to: [P0054, submission-export skill, every appendix generator]
triggers: [running the comment pass on a generator, auditing emitted captions]
created: 2026_09_10-16_15
updated: 2026_09_10-16_15
---

# Worked pass — `export_appendix.py` (1,393 lines)

A generator needs **two passes**: one over its source, one over what it writes.
The second matters more, because its output goes into the thesis.

**Headline: the emitted text is the bigger problem.** The source comments are
ordinary DELABEL work. The `review=` arguments are 14 blocks of internal notes
that reach 26 files under `05_thesis_results/`, and the captions carry two
factual errors.

---

# Part 1 — What the generator emits

## E1 — The internal/submission split must go entirely

Verified on disk: **26 generated `.md` files currently carry an
`INTERNAL REVIEW -- NOT FOR SUBMISSION` block.** Here is the tail of a real one,
`05_thesis_results/04_data_assessment/tables/02_pipeline_execution.md`:

```markdown
---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Generated from run_manifest.json across 4 of 4 categories (8 runs), written
2026-09-07. Regenerate by re-running run_preprocessing.py; the manifest merges
horizons rather than overwriting, so H=1 and H=3 accumulate. A category absent
here has simply not been re-run since the manifest was added (P0046 F20) -- it
is not evidence of a failure. 12 skipped step(s) present.
```

In the working repo this design is right: the note sits at the table it
describes. In the submission repo there is no internal half, and a document
that visibly withholds a section is worse than one that never had it.

**Change in source:** delete `REVIEW_SEP`, drop the `review=` parameter from
`_emit()`, and remove all 14 `review=` arguments.

```python
# Before
REVIEW_SEP = "\n---\n\n<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->\n"

def _emit(slug, title, caption, df, note="", review="") -> None:
    ...
    if review:
        lines += [REVIEW_SEP, review]

# After
def _emit(slug, title, caption, df, note="") -> None:
    ...
```

**Some `review=` content is too valuable to lose.** Three blocks carry
methodological caveats that belong *in the thesis prose*, not in a code file:

| Block | The claim | Where it belongs |
|---|---|---|
| `retraining_cost` | "Do NOT claim re-tuning is less accurate. Optuna seed alone moves test WMAPE by more than the gap." | Already in the caption's `note=`. Verified — no loss. |
| `parameter_drift` | "INCONCLUSIVE — do not fit or cite a per-month drift slope." | Already in `note=` as "absence of evidence at this horizon". No loss. |
| `statistical_baselines` | "NLM Section J: PRO-04 Contradicted (T&L do NOT exclude monthly data)... Taylor & Letham (2018) is MISSING from the Ch2 reference list." | Verified: the source **is** in `bibtex.bib`, and the PRO-04/PRO-05 wording caveat is tracked in `writing-notes/ch5_model benchmark/srq1-model-ladder-and-baselines.md`. Only the reference-list gap needs checking at freeze. |

Checked all three against the writing notes rather than assuming. Two are
already carried in the emitted `note=` text, and the third is tracked in a live
chapter note — so **nothing is lost by deleting these blocks**, provided the
check is done rather than skipped.

The same check applies to the two items named in Part 1 below (the 2026-08-19
prompt exclusion and the horizon-labelling caveat). The horizon caveat is
already tracked at
`writing-notes/ch5_model benchmark/srq1-forecast-horizon-defect-and-split-correction.md`.
The prompt exclusion is **not** tracked anywhere outside this file, so it is the
one item that genuinely must be extracted.

## E2 — A caption states a wrong feature count

`table_feature_matrix` docstring, line ~1240:

```python
    count in particular has been wrong in the prose more than once (13, then 14,
    then 16, now 34 after the holiday enrichment), because it was written down
    instead of counted.
```

The current feature set is **18**, per CLAUDE.md and the 2026-09-08 commits.
"now 34" is a fourth wrong number in a sentence complaining about wrong numbers.

The emitted caption is safe — it interpolates `n_feat` from the manifest at run
time, which is the pattern working correctly. Only the docstring is wrong.

**After:**

```python
    """What the modelling matrix actually contains, column by column.

    Reads the matrix and its manifest rather than describing them, so the
    feature count is counted at render time rather than written down.

    The important content is the EXCLUDED block: contemporaneous sales and
    baseline columns are carried in the matrix for traceability and are not
    model inputs. A reader who assumed every column is a feature would conclude
    the model sees same-period sales, which would make the benchmark
    meaningless.
    """
```

## E3 — The appendix index tells the reader about our workflow

`APPENDIX_TABLES.md`, generated in `main()`. Four of its paragraphs are
instructions to us:

```python
"Do not edit these files by hand -- re-run the exporter. ..."
"Each table's own `.md` carries its internal review notes **below a horizontal
 rule**, under an `INTERNAL REVIEW` marker. ..."
"**Filenames are numbered, table content is not.** The `NN_` prefix gives the
 directory a stable generation order for our own review; ..."
"Tables are filed under the CHAPTER that discusses them, not under the script
 that produced them -- the writing workflow runs chapter by chapter, so the
 folder you open is the chapter you are writing."
```

The second is void once E1 lands. The rest describe our Word workflow. **After:**

```python
    idx = ["# Appendix tables", "",
           f"Generated by `{Path(__file__).resolve().relative_to(ROOT_DIR).as_posix()}`, {stamp}.",
           "",
           "Each table is written as `.md` for inclusion in the document and "
           "`.csv` so any figure can be traced to its source. Tables are filed "
           "under the chapter that discusses them.", "",
           "| # | Chapter | Table | File |", "|---|---|---|---|"]
```

The closing print also goes:

```python
# Before
    print("  each table .md carries its review notes below a horizontal rule.")
# After — deleted
```

## E4 — Two `_coverage()` disclosures that are correct but temporary

`_coverage()` emits, into the published caption:

```
Covers 6 of an intended 225 runs (15 brands x 5 repeats x 3 scenarios) and one
of the three scenarios; the remaining scenarios have not yet been run at the
corrected prompt.
```

This is **honest and must stay** if the experiment is still partial at freeze.
But "at the corrected prompt" refers to a prompt bug the assessor never saw.

**After:**

```python
        bits.append("and one of the three scenarios")
```

Its docstring separately explains the excluded 2026-08-19 run — a prompt asking
"what will X sell" without a unit, yielding ~4500% errors. That is a real
methodological exclusion and belongs in the thesis, so extract it to the
methodology notes rather than deleting it.

## E5 — Per-run review block dates itself

```python
          review=(f"Currently {len(df)} rows because only a scenario-A pilot has run "
                  "(CSD, 2 brands, 3 reps). Intended full size is 225 rows: 15 "
                  "brands x 5 repeats x 3 scenarios. Blocked on API credit (P0042 "
                  "blocks 1-3, ~$40). NOT the final length."))
```

"Blocked on API credit, ~$40" in a thesis appendix. Deleted with E1; the
`_coverage()` line already states the run count factually.

---

# Part 2 — The source comments

Lighter work than Part 1, but two path errors.

## S1 — FIX: the docstring's output path does not exist

```python
Output: 04_thesis_results/appendix/
```

Verified: neither `04_thesis_results/` nor `05_thesis_results/appendix/` exists.
Tables go to `05_thesis_results/<NN>_<chapter>/tables/`, which the code does
correctly via `get_chapter_tables_dir`. The docstring is two restructures stale.

**After:**

```python
Output: one tables/ folder per chapter under 05_thesis_results/
```

## S2 — DELETE: the file docstring's convention essay

**Before** (lines 2–45), 44 lines with two banner headers. **After**, 18 lines:

```python
#!/usr/bin/env python
"""Render every tracked metric as appendix tables.

`summary.md` answers "which scenario won" in one table and hides the rest. An
appendix has the opposite job: a reader must be able to check that a reported
number came from somewhere, which needs the per-run detail, the units and the
source of each figure. Both are generated from the same `runs.csv`, so they
cannot disagree.

Two presentation conventions are deliberate. Percentages are stored as numbers
and carry their unit in the column heading rather than in every cell, following
the M4 and M5 competition tables: repeating the unit adds width without
information and breaks numeric alignment. Comparative tables are pivoted wide so
that models sit side by side, since a reader comparing four models wants them
adjacent rather than 28 rows apart.

No API calls, and safe to re-run: it reads only results already on disk, and
skips missing inputs with a notice.

Usage:
    python 04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py

Output: one tables/ folder per chapter under 05_thesis_results/
"""
```

Gone: `WHY THIS EXISTS`, `CONVENTIONS THAT ARE DELIBERATE`, the whole "No table
numbers / Word's job" paragraph (a Word workflow note), the submission/notes
segregation paragraph (void after E1), and the stale output path.

## S3 — DELETE: four "this used to be N tables" blocks

Each explains a refactor. `table_resource_profile`, before:

```python
    """ONE table for the whole resource question.

    This previously stood as three: a per-model profile, a budget share table,
    and a retraining-cost table. They were separated because they answer
    different questions, but they share a single unit system (seconds and
    megabytes against one budget) and a single subject (what the substrate
    costs to run), so a reader comparing "fit" against "refit" against "re-tune"
    had to hold three tables in view at once. Merged, the comparison the
    appendix exists to support is visible in one screenshot.

    What stays separate is the drift table: its unit is percentage points of
    forecast error across forecast origins, not time or memory, and merging
    unlike quantities into one grid would invite comparison down a column where
    none exists."""
```

**After:**

```python
    """Time, memory and retraining cost for the forecasting substrate, in one table.

    These share a unit system (seconds and megabytes against one budget) and a
    subject, so they belong in one grid. The drift table stays separate: its
    unit is percentage points of forecast error, and merging unlike quantities
    would invite comparison down a column where none exists."""
```

The same treatment for `table_baselines_wide` ("The long form ran 28 rows"),
`table_pipeline_execution` ("Before that manifest existed the run record lived
only as prose... P0046 F20"), and `table_pipeline_data_reduction`.

## S4 — DELETE: `_clear_previous()`'s 20-line archaeology

**Before**: five paragraphs on the old numeric-block scheme, the 2026-09-07
incident where three tables were all called `02_`, the bound "once set to 89"
that deleted the literature table, and `DEC-CHAPTER-FOLDERS`.

**After:**

```python
def _clear_previous() -> int:
    """Delete this exporter's own tables before regenerating.

    Matched by slug, not by filename prefix: the `NN_` prefix is a generation
    order, so a missing input shifts every later table and writing without
    clearing would leave the previous run's files behind under stale numbers.
    Matching on slug means this cannot reach another producer's output.
    """
```

## S5 — DELABEL: three short ones

| Line | Before | After |
|---|---|---|
| 59 | `Replaces a hard-coded parents[N] hop, which silently points at the wrong directory whenever a script moves between folder depths -- as happened in the 2026-09-06 restructure.` | `A hard-coded parents[N] hop points at the wrong directory whenever a script moves between folder depths.` |
| 81 | `Measured allocation of Manifold's production E2B template (alias \`prometheus\`), not a literature estimate. See P0044 findings.` | `Measured allocation of the production sandbox template, not a literature estimate.` |
| 99 | `This script is a CROSS-CUTTING exporter... It lives with the SRQ4 harness for historical reasons, but only 5 of its 15 tables concern the scenario experiment... Filing them all under SRQ4 put pipeline-execution figures in "scenario experiments", so each table now names the chapter that discusses it.` | `A cross-cutting exporter: only five of its tables concern the scenario experiment, so each table names the chapter that discusses it.` |

## S6 — KEEP: the presentation-logic comments

Six blocks explain non-obvious display decisions and every one earns its place:

| What | Why keep |
|---|---|
| Python-heap row deliberately not bolded (line ~383) | bolding it would award "best" to the model whose native allocation the instrument cannot see — inverts the row's purpose |
| `Ridge(unclipped)` excluded from bolding | a diagnostic variant, not a candidate; letting it win misrepresents selection |
| `_num()` marking divergence by order of magnitude | `2.8e+13` reads as a typo in print |
| Bold+italic because Markdown has no underline that survives Word | practical and non-obvious |
| `n` in the column header so every percentage carries its denominator | good table design |
| Environment facts in the caption, not as repeated rows | good table design |

---

## Result

| | Before | After |
|---|---|---|
| Source lines | 1,393 | ~1,290 |
| `review=` blocks emitted | 14 | 0 |
| Generated `.md` files with an internal block | 26 | 0 |
| Factual errors in comments | 2 | 0 |
| Items needing extraction before deletion | — | 1 (the 2026-08-19 prompt exclusion) |

**Check before deleting, every time.** Of the five candidate items in the
`review=` blocks, four turned out to be tracked elsewhere already — two in the
emitted captions, two in live chapter notes. One is not: the excluded
2026-08-19 run, whose unit-less prompt produced ~4500% errors. That is a real
methodological exclusion an examiner could ask about, and this Python file is
currently its only home.

The lesson generalises: a `review=` block is not automatically disposable and
not automatically precious. Verify each against the writing notes.
