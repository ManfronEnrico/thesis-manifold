---
name: deferred-structural-decisions
description: NOTE - Running list of structural decisions deferred out of chapter prose passes. Appendix placement, table siting, internal cross-references and cross-chapter fluidity. One row per item, carried forward between passes rather than re-derived.
category: workflow
applies-to: [chapter 4, chapter 5, chapter 6, chapter 7, chapter 8, appendix]
created: 2026_09_09-17_10
updated: 2026_09_10-16_10
status: open
---

# Deferred structural decisions

Items a chapter prose pass surfaced but deliberately did not act on, because
they are layout or cross-chapter decisions rather than sentence-level fixes.

**This file is cumulative.** Each chapter pass appends to it rather than
starting a new list, so the appendix and cross-reference questions can be
settled once, at the end, with the whole picture visible.

**Status values:** `open` (needs a decision), `recommended` (I have a view,
stated), `blocked` (waiting on something), `done` (settled - keep the row and
record what was decided).

---

# Quick reference

| # | Item | Chapter | Status |
|---|---|---|---|
| [S1](#s1) | Table 1, per-category structure - body or appendix | 4 | recommended |
| [S2](#s2) | Table 2, EDA parameter overview - delete entirely | 4 | recommended |
| [S3](#s3) | Table 3, per-category EDA - body or appendix | 4 | recommended |
| [S4](#s4) | Table 4, feature list - and the Appendix A question | 4 | open |
| [S5](#s5) | Stale internal reference, "flagged in §4.6" | 4 | recommended |
| [S6](#s6) | Stale internal reference, "(§4.3.6)" in §4.5 | 4 | recommended |
| [S7](#s7) | Stale internal reference, "(Section 4.5)" in Table 2 | 4 | recommended |
| [S8](#s8) | Forward references to Chapter 6 that mean Chapter 5 | 4 | open |
| [S9](#s9) | Cross-chapter repetition, final pass | all | blocked |
| [S10](#s10) | Chapter 4 subtitle | 4 | open |
| [S11](#s11) | Where feature engineering is discussed | 4, 5 | recommended |
| [S12](#s12) | Rule/skill cite a claims register that does not exist | tooling | recommended |

---

# The appendix question

## S1 {#s1}

**Table 1 - per-category structure at DVH EXCL. HD.**

Seven columns wide: periods, brands in scope, brands retained, catalog SKUs,
in-scope SKUs, brand-month rows, in-scope fact rows.

**Recommendation: keep in the body, drop two columns.** This table is the
chapter's evidential foundation - it is what "the panel can support this
question" means concretely, and the argument in §4.1.2 fails without it.

But `Catalog SKUs` and `In-scope SKUs` are the two columns the surrounding
prose uses only to make a general point about the gap between them. Moving
those two to the appendix leaves a five-column table that reads at a glance and
still carries the argument.

**Comment thread:** the one on the RTD row, tagged OUTDATED and APPENDIX.

---

## S2 {#s2}

**Table 2 - EDA parameter overview.**

**Recommendation: delete entirely, do not move to the appendix.**

This is the strongest recommendation in the list. The table restates parameters
that §4.2.3, §4.2.4 and §4.4 each derive properly in prose, and it restates two
of them *wrongly* - it still carries `MIN_PERIODS 30 (global)` and
`Train / Val / Test 24 / 6 / 12 months`, both superseded, sitting two sections
above the corrected text.

An appendix copy would preserve the error rather than fix it. Fixes 7 and 8 of
the Chapter 4 pass put its content into prose at the point each value is
derived, which is where a reader wants it.

**One sentence survives** - the closing note that the parameters are empirical
rather than theory-first. Fix 7 keeps it.

**Comment thread:** the one on the §4.2.5 heading, tagged VERIFY, PROSE and
APPENDIX.

---

## S3 {#s3}

**Table 3 - per-category EDA summary.**

Six columns: promo correlation, peak month, top brand, ADF p-value, stationarity
verdict, ACF at lags 1 and 3.

**Recommendation: keep in the body as is.** Four rows and six columns is small,
and this table is the entire evidential basis for the claim that the four
categories are genuinely different rather than replications of one another.
That claim is load-bearing for the pooled-versus-specialised comparison in
Chapter 5, so the evidence should be visible where it is made.

**But verify it first.** The thread asks for whole-table verification and the
Chapter 4 pass did not do it - only the columns that overlapped other fixes
were checked. The ADF p-values and the top-brand column are unverified.

**Comment thread:** the one on the RTD row, tagged VERIFY and APPENDIX.

---

## S4 {#s4}

**Table 4 - the feature list, and what Appendix A should become.**

**Status: open, because it depends on a decision not yet made.**

Two separable questions:

**(a) Does Table 4 stay in the body?** Yes - it is seven rows, and it is the
only place a reader can see what the models actually receive. Fix 4 of the
Chapter 4 pass relabels its third column rather than moving it.

**(b) Where does the full per-category feature list go?** This is the open one.
Appendix A is titled *"Star Schema Diagram (CSD Example) and Resulting Category
Features"* but currently contains only the star schema. Its title already
promises the second half.

**My view: extend Appendix A rather than adding Appendix B.** Raw columns above,
derived columns below, in one place, showing how the panel becomes a matrix.
That is one question, and the existing title already commits to answering it.

**⚠ Blocked on retraining.** If the holiday columns move into the standard
input set, the per-category counts change (13 to 16 for CSD and energidrikke).
Do not typeset this appendix until that run lands.

---

# Internal cross-references

Three are stale. All three point at the chapter's own earlier scaffolding
rather than at content, which is why none of them can be repaired by
renumbering.

## S5 {#s5}

**"closing the gap previously flagged in §4.6"** - §4.2.6, opening sentence.

**Traced.** There is no §4.6 in the current chapter. The reference is to an
earlier draft's risks section, which recorded "per-category EDA not yet
recomputed" as an open risk. That section is **§4.5 today**, and the risk entry
still exists in it, beginning *"Per-category EDA (resolved)"*.

**Recommendation: delete the clause rather than repoint it.** Repointing gives
you §4.2.6 saying "this closes a gap flagged in §4.5" while §4.5 says "this was
resolved in §4.2.6" - two sections pointing at each other, both describing
project history rather than the data.

Fix 9 already removes the §4.5 half. Deleting this clause removes the other.
The sentence reads correctly without it:

> *"The three remaining categories were taken through the identical pipeline,
> with their exploratory analysis recomputed under the DVH EXCL. HD scope."*

---

## S6 {#s6}

**"recomputed under DVH EXCL. HD (§4.3.6)"** - §4.5, the per-category risk entry.

Same class of error, pointing at §4.2.6 under an older numbering.

**Recommendation: resolved by Fix 9**, which replaces the whole §4.5 body and
drops this entry as project status rather than risk. No separate action needed
- listed here so it is not re-flagged later as an unaddressed reference.

---

## S7 {#s7}

**"forward-chaining (Section 4.5)"** - Table 2, the split row.

Points at the risks section for a description of the splitting scheme. The
split is in **§4.4**, and it is not forward-chaining - it is a single
proportional three-way split.

**Recommendation: resolved by S2**, since the whole table goes. Recorded because
it is evidence for deleting rather than relocating Table 2: an appendix copy
would carry a cross-reference that is wrong about both the section and the
method.

---

## S8 {#s8}

**Forward references to Chapter 6 that appear to mean Chapter 5.**

**Status: open - needs checking against the current chapter order, not assumed.**

Chapter 4 refers forward twice in ways that may not survive the Ch5/Ch6 swap:

- §4.1.4: *"Benchmarking (Chapter 6) is conducted on..."* - benchmarking is
  **Chapter 5** in the current order. Fix 6 rewrites this sentence and drops the
  reference.
- §4.1.1: *"The exact extraction interface used by the pipeline is documented in
  Chapter 6"* - this one is probably **correct**, since Chapter 6 is
  Predictive-Extension Architecture, which is where an extraction interface
  would live. **Verify before touching.**
- §4.1: *"they are what allows Chapter 6 to test whether one pooled model
  generalises"* - the pooled-versus-specialised comparison is §5.5.4, so this
  should be **Chapter 5**. Note that §4.2, twelve lines later, refers to the
  same comparison as *"the pooled-versus-specialised comparison of Chapter 5"* -
  so the chapter contradicts itself on where its own result lives.

**Recommendation: sweep all forward references in one pass, at the end**, once
chapter order is final. Doing it piecemeal per chapter is how the current
inconsistency arose.

---

# Cross-chapter fluidity

## S9 {#s9}

**The repetition question.**

**Status: blocked, by your own decision - and correctly so.**

The thread on §4.1 asks whether cross-chapter repetition is rigour or slop. Your
reply records the answer: *"ideally no repetition, or keep it to the lowest
necessary degree, pointing towards the sections where it is actually covered"*,
and that it is a final-pass job once the chapters are prose.

**One piece of evidence to carry into that pass.** The repetition has already
produced a factual contradiction rather than merely redundant prose: Chapter 5
§5.3.2 states in bold that *"No holiday calendar is used"*, while Chapter 4 §4.3
devotes a table row and a subsection to the holiday enrichment. One chapter was
updated and the other was not.

That is the argument for the establish-once-and-cite pattern, and it is worth
stating in the final pass rather than re-deriving.

**The Chapter 5 pass should fix the false sentence immediately**, without waiting
for the structural pass. A one-line deletion that removes a contradiction is not
a restructuring decision.

---

## S10 {#s10}

**Chapter 4 subtitle.**

Currently *"From Scanner Panel to Modelling Matrix"*, with a resolved thread
asking whether the chapter could use one.

**Status: open, but the existing subtitle is good** - it names the chapter's
actual arc, which is exactly what the chapter does. My only note is that
Chapter 5 carries a literal *"COULD USE A SUBTITLE"* placeholder in the
document, which must not reach submission.

---

## S11 {#s11}

**Where feature engineering is discussed.**

**Status: recommended, settled in the previous session - recorded here so it is
not reopened.**

Feature engineering stays in **Chapter 4**. Chapter 5's §5.3.1 and §5.3.2 shrink
to a back-reference plus the facts that belong to the experiment: the horizon,
the test-set row counts, which model family consumes which inputs, and the
NaN-versus-zero-fill distinction.

**The reasoning**, which is worth keeping because the opposite conclusion looks
plausible: the pipeline computes features *before* it splits
(`calendar → filter → engineer_features → apply_split`), and `FeatureEngineer.fit`
is a documented no-op because every transformation is leakage-safe by
construction. The usual argument for placing feature engineering after the split
- that fitting a scaler on the full panel leaks - does not apply, because
nothing is fitted. The features are also *derived* in Chapter 4's exploratory
analysis, so moving them would separate a number from its evidence.

---

## S12 {#s12}

**`writing-notes/unverified-claims-to-check.md` is referenced but does not
exist.**

Three references sit in `.claude/rules/prose-insertion-discipline.md` and two in
the prose skill, including one in the rule's *Where the surfaces live* table
which presents it as a live editable surface. **The file has never existed** —
the three in the rule are present in commit `202f75a`, so they predate this
session.

**The real system is better than the missing one.** Claims awaiting verification
live in `notebookLM/04-Claims_Verification/Chapter <N> - <Name>/<Topic>/claims.md`,
numbered `CV-NN`, with a master brief and a HOW-TO-RUN beside them. It is more
developed than a flat register would be: per-chapter, per-topic, and it already
distinguishes the safe wording in use from the stronger wording pending
verification.

**Recommendation: repoint the five references at the `CV-NN` packs.** Do not
create the missing file — that would add a second queue competing with a working
one, which is the failure the single-queue rule exists to prevent.

**Why this was not fixed at end of day:** two of the five were written this
session and are fixed; the other three are committed text, and repointing
committed rule references is an edit worth making deliberately rather than as a
tidy-up inside a commit about Chapter 4. Fifteen minutes, mechanical.

⚠ **The consequence while it stands.** The rule instructs that every `SOURCE`
comment becomes a row in a register that cannot be found, and states "a claim
named in a writing note but absent from it will not be verified". A session
following that instruction has nowhere to write, and may either invent the file
or skip the step.

---

# Appending to this file

A chapter pass adds rows under a new `# Chapter N` heading and extends the quick
reference table. Do not re-derive items already listed - if a later pass changes
a recommendation, edit the row and say what changed, so the reasoning survives.

## S13 - Captioning the calibration table renumbers everything after it

**Status:** `recommended`

Chapter 5's split-conformal coverage table (§5.5.7) has no caption and no number,
while every other table in the chapter has both. Adding one makes it Table 14 and
pushes the SRQ-contribution table to 15, along with every numbered table in the
chapters that follow.

**Recommendation: add the caption.** An uncaptioned table cannot be referred to
and does not appear in the table of figures, which is a formal-requirements
problem rather than a stylistic one. Word's cross-reference fields renumber on
F9; **plain-text callouts of the form "Table 14" typed as literal text do not**,
so grep the document for those before pasting.

**Raised by:** the Chapter 5 pass, 2026-09-10.

---

## S14 - fig4_ram_budget is stale and contradicts §5.5.6

**Status:** `open`

Chapter 5's Remaining-gaps section carries the line *"fig4_ram_budget is stale
and contradicts §6.5.6"*. That sentence is a note to the authors and must come
out of the prose either way (F12).

The underlying problem is real: the figure was drawn against an 8 GB budget and
tracemalloc heap figures, where the chapter now reports a 4 GB budget and
resident set size. **Regenerate it from
`tables/05_substrate_resource_profile.md`**, which already carries the
share-of-budget row.

**Raised by:** the Chapter 5 pass, 2026-09-10.

---

## S15 - Should the five model descriptions become one comparison table?

**Status:** `recommended`

Sections 5.2.2 through 5.2.6 each give role, implementation, memory and a stated
limitation for one model, in the same order, as a bullet list. Nineteen `PROSE`
comments cover them.

**Recommendation: one table, not five paragraphs.** A reader comparing six models
wants columns, and §5.1 argues the ladder is the point without ever showing it.
Columns for model, family, role, implementation, peak memory and stated
limitation would carry the same content in a third of the space and make the
inductive-bias spread visible.

The simple-benchmark definitions in 5.2.1 already work as a table and should
stay one.

**Not drafted** - say the word and it takes ten minutes.

**Raised by:** the Chapter 5 pass, 2026-09-10.

---

## S17 - The calibration table describes a model two categories do not serve

**Status:** `open`. **Raised by Enrico 2026-09-11, validated the same day.**

`srq1_calibration.py` line 184 fits `XGBRegressor` unconditionally for every
category. But `train_and_persist.best_model_for()` selects on the
**cross-validation** score, not test error, and on that basis:

| Category | CV picks | CV score | Calibration fits |
|---|---|---|---|
| CSD | XGBoost | 18.8 | XGBoost ✓ |
| Danskvand | XGBoost | 25.7 | XGBoost ✓ |
| **Energidrikke** | **LightGBM** | 11.5 | ⚠ XGBoost |
| **RTD** | **LightGBM** | 34.2 | ⚠ XGBoost |

**Half the calibration table describes a model that is not served.** Enrico named
exactly these two categories.

⚠ **Selecting on test WMAPE gives XGBoost everywhere**, which is why this looks
wrong at first glance. It is not: `best_model_for()` deliberately selects on CV,
because selecting on test is selection on the evaluation set and biases every
downstream number. The code carries that reasoning in its own comments. **Do not
"fix" this by switching the selection to test.**

**Fix:** `srq1_calibration.py` reads the selected model per category rather than
hardcoding XGBoost, then re-runs. Section 5.5.7's table and every coverage figure
in it move.

**Chapter impact:** Section 5.5.7 and the SRQ2 confidence payload.

---

## S18 - The confidence index is mathematically dead

**Status:** `open`, and this is the most consequential of the four.
**Raised by Enrico 2026-09-11, verified by evaluating the formula.**

`forecast_tool.py:473`:

```python
conf = 100 * (0.5 * (1 / (1 + rel)) + 0.5 * (1 - min(q90, 1)))
```

**Two independent defects, and Enrico found both.**

**The relative width carries no per-forecast information.** With
`lo = expm1(log(y) - q90)` and `hi = expm1(log(y) + q90)`, the width ratio is
`(hi - lo)/y ≈ 2·sinh(q90)` — the forecast value cancels. Since `q90` is one
number per category, **`rel` is constant within a category** and the first term
cannot distinguish one brand's forecast from another's.

**The second term is identically zero.** `1 - min(q90, 1)` is 0 whenever
`q90 ≥ 1`. Implied q90 from the current calibration:

| Category | mean rel. width | implied q90 | second term |
|---|---|---|---|
| CSD | 8.62 | 2.17 | **0** |
| Danskvand | 11.89 | 2.48 | **0** |
| Energidrikke | 33.64 | 3.52 | **0** |
| RTD | 8.62 | 2.17 | **0** |

So half the index is dead everywhere, and the surviving half is a per-category
constant. **Every forecast scores between 2 and 6 out of 100 and tiers as
"Low"** — matching Enrico's observed 3 to 7.

### The decision, and it is not only cosmetic

| Option | Cost | What it means |
|---|---|---|
| **Drop the field** | small; SRQ2 prose changes | honest. The index measures nothing |
| **Recalibrate the cut-offs** | ⚠ **does not fix it** | re-tiering a per-category constant still yields four values, one per category — a category label wearing a number |
| **Rebuild on something per-forecast** | real work | the only route to an index that varies per forecast |

⚠ **Recalibrating cut-offs is the tempting option and the wrong one.** The
problem is not where the thresholds sit; it is that the quantity being
thresholded does not vary within a category.

**This reaches SRQ2 directly.** The research question asks how a forecast reaches
an agent with *reliability, uncertainty and traceability* preserved. The interval
carries uncertainty and the track record carries reliability. **The confidence
index carries neither**, and its docstring already calls it "a heuristic index"
and warns against reading it as a probability.

**Recommendation: drop the field.** The payload already carries a calibrated
interval and a measured track record, both of which do what this index was
supposed to do. Removing a broken signal is a stronger SRQ2 result than shipping
one, and it can be reported as a finding rather than hidden as an omission.

**Chapter impact:** Chapter 7 (the tool interface) and the SRQ2 payload
description wherever it appears.

---

## S19 - Operational figures predate the 18-feature retraining

**Status:** `open`. Raised by Enrico 2026-09-11; already tracked as **H12** in
`post-hpc-validation.md`. Recorded here too because it is a prose decision as
well as a re-run.

`profiling.csv` is dated **2026-09-01** and reports `n_features: 13`. The model
uses 18 (17 for danskvand and RTD). `06_retraining_cost.csv` has the same
problem.

**Chapter 5's prose already handles this** without a re-run: the
sequential follow-up reports the figures as a **floor** and says why. The margin
against the memory budget is roughly a hundredfold, so a proportional increase in
feature count does not approach it.

**Re-running is cheap and would remove the caveat.** Not a blocker either way.

---

## S20 - Chapter 7 rewritten against SRQ2's three properties

**Status:** `done`, recorded for traceability. **Enrico, 2026-09-11.**

Retitled *The Structured Tool Interface* from SRQ2's own wording, and restructured
around reliability, uncertainty and traceability. The judge section and the
five-model synthesis framing are **dropped** — neither matched the repository.

Confirmed present in the 2026-09-11 snapshot as
`chapters/chapter-7-the-structured-tool-interface.md`.

⚠ **The snapshot exporter does not recognise the new title**, warning that the
chapter is "not in CHAPTER_SUBJECTS" and naming the file from its heading instead.
Harmless for now, but it means Chapter 7 will not pair with its draft in the drift
table. **That is P0052's concern** — the exporter keys chapter identity off
number and title.

**Still open on Enrico's side:** Section 7.6, waiting on the S17 re-run, and the
SRQ4 runs.

---

## S16 - Zotero metadata defects that will render wrong in the bibliography

**Status:** `open`, one of four resolved. Raised by the Chapter 5 pass, widened
2026-09-10 by a per-source audit against the unfiltered Zotero API, and
partially closed the same day.

### RESOLVED - Hyndman & Athanasopoulos

Fixed in Zotero 2026-09-10 and confirmed against a fresh pull. `5NFQRRXS` now
reads as a book: *Forecasting: principles and practice*, both authors, 3rd
edition, OTexts, Melbourne, 2021, URL pointing at the book, tracking parameter
removed.

**DEC-FPP-WHOLE-BOOK (2026-09-10): cite the whole book, never individual
chapters.** The authors present it as one work with one canonical reference, and
the bibliography carries one entry accordingly.

In-text, add a section locator only where a passage is quoted directly:

| Use | Form |
|---|---|
| default | (Hyndman & Athanasopoulos, 2021) |
| quoting a passage | (Hyndman & Athanasopoulos, 2021, Section 5.2) |

⚠ **Never a page number.** The online edition is revised continuously and its
pagination does not match the print version, so any page number is wrong for one
of the two. Section numbers are stable across both.

Feeding individual chapters to NotebookLM is a verification-input decision and
has no bearing on how the source is cited.

### Still open - a cited source is ABSENT, and three items are duplicated

**Found 2026-09-11** during the Chapter 6 pass, against the 17:24 pull (89
items), searched by author across every item type rather than the filtered
export.

⚠ **Semerikov et al. (2025) is not in the library at all**, and Chapter 6 cites
it **twice** - in Section 6.5 and in the Table 18 row for the remote-API choice.
Under the standing rule, it is not a source. `ch6-prose-pass.md` Fix 9b removes
both citations and rests the claim on arithmetic instead; **if the source is
real and gets added, revert that fix and keep the citations.**

**Three items are duplicated**, each pair being one work entered twice:

| Work | Keys | Note |
|---|---|---|
| Wang et al., Executable Code Actions | `U24G3Z36`, `wang_executable_2024` | one copy's date reads `July` instead of a year |
| Paranjape et al., ART | `VA9UT3F9`, `paranjape_art:_2023` | |
| Ahrens et al., Model Averaging | `I86QMNYE`, `ahrens_model_2025` | cited in Chapter 6 Section 6.3 |

⚠ **A duplicate with two different dates can render as two different in-text
citations for one source**, and a reader checking the reference list finds the
same paper twice. The Wang pair is the live risk, because it is cited in
Chapter 6 twice and one copy has no usable year.

**Two further malformed dates:** Sapkota, *AI Agents vs. Agentic AI*, stored as
`02/2`; Chen, *ACGraph*, stored as `Dece`. Both will render wrong. Sapkota is
cited in Chapter 6 Section 6.2.

### Still open - the BibTeX exporter mangles every author list

**Found 2026-09-10 while checking the corrected Hyndman entry.** Not caused by
that fix - it affects **all 87 entries**.

`zotero_client.py` line 224 joins authors with a comma and writes each name as
`Last First`:

```
author = {Hyndman Rob J., Athanasopoulos George}
```

BibTeX requires ` and ` as the separator and reads `Last, First` per name:

```
author = {Hyndman, Rob J. and Athanasopoulos, George}
```

**As exported, a BibTeX-driven bibliography will treat each entry as having one
author with a very long name**, so "Hyndman & Athanasopoulos (2021)" cannot
render and neither can any other multi-author citation.

⚠ **Whether this matters depends on how the bibliography is actually built.** If
Word's own citation manager is the source, the `.bib` file is a convenience
export and nothing is broken. If the `.bib` drives the reference list, **every
multi-author reference in the thesis is wrong** and this is a Trust-tier defect
rather than a deferred one.

**Establish which before submission.** The fix is two lines in
`zotero_client.py`; the risk is not knowing the file is load-bearing.

### Still open - Akiba et al.

| Entry | Defect | Renders as |
|---|---|---|
| Akiba et al. | date field reads **"July 25, 2019"** | a full date where a year belongs |

### Two author pairs are ambiguous, and the risk is silent

The library holds two papers in each of these pairs. Both render nearly
identically in text, so a citation field pointing at the wrong one is invisible
in the document and wrong only in the bibliography.

| Pair | Key | Year | What it supports |
|---|---|---|---|
| M4 | `EXNY7D4X` | **2018** | pure-ML entries versus the combination benchmark, p. 803 - **the one Chapter 5 needs** |
| | `V58EFK8B` | 2020 | the 100,000-series description |
| Bergstra | `S4WQS877` | **2011** | the TPE density split, p. 2549 - **the one Chapter 5 needs** |
| | `34DWJUWN` | 2012 | random search versus grid search |

**Both in-text citations in Chapter 5 name the right year**, so the prose is
correct. What needs checking is which entry each Word citation *field* resolves
to.

Note that "Bergstra et al." is only correct for the 2011 paper, which has four
authors; the 2012 paper has two and would take "Bergstra & Bengio".

### Everything else is clean

The audit checked all fifteen Chapter 5 sources individually. **Every one is in
the library** and the remaining eleven have complete metadata. Nothing needs
adding to Zotero.

**Why the unfiltered API and not `citations.json`:** that export keeps only
scholarly item types, so a `computerProgram`, `dataset` or `blogPost` entry is
silently dropped and reads as missing.

**Raised by:** the Chapter 5 pass, 2026-09-10. **Widened** by the sequential
Chapter 5 follow-up, and **partially closed** by Brian's Zotero fix, the same
day.

---

---

## S21 - "Code-as-action baseline" names a two-way comparison the design no longer is

**Status:** open. **Raised by:** the first paid five-scenario run, 2026-09-11.
**Blocks:** the Chapter 6 §6.7 rewrite, which is marked BLOCKED in
`ch6_architecture/2026-09-11_experiment-state-for-ch6-prose.md` for this reason.

Chapter 6 §6.7 is titled **"The Code-as-Action Baseline (SRQ4)"** and describes
one comparator: the artefact versus an LLM writing its own code. Chapter 3 and
Chapter 8 describe a **five-rung information ladder** in which every rung is the
comparator for the rung below:

| | scenario | what it adds |
|---|---|---|
| A | plain LLM, web search | -- |
| B | + history and a code sandbox | what data access buys |
| C | + the trained model behind the tool | what the artefact adds |
| D | B's task on the production orchestrator | orchestrator effect on B |
| E | C's task on the production orchestrator | orchestrator effect on C |

"Baseline" implies a single fixed reference point. The ladder has no single
baseline: A is the baseline for B, B is the baseline for C, and D->E repeats
B->C on a second orchestrator so the two increments can be compared to each
other.

**Why it is deferred rather than fixed now:** a sixth and seventh rung -- an arm
holding data, code AND the trained model at once, on both orchestrators -- is
under active consideration (costed at roughly $9 on top of the funded set, since
it reuses the existing prompt and dispatch machinery). If those land, §6.7
enumerates seven things, not five, and rewriting it twice is waste.

**Recommendation when it is taken up:** retitle §6.7 to name the ladder rather
than the baseline, and let §6.4's existing reliability/reproducibility argument
carry the design justification. The section's *content* is largely correct --
it is the framing and the enumeration that have been outrun.

**One factual correction to apply whenever it is rewritten:** §6.7 cites **E2B**
as the sandbox ("for example, E2B as it is used in our testing scenarios").
The harness uses **OpenAI's Code Interpreter**; E2B appears nowhere in it.

---

## S21 - The SRQ4 scenario display labels are inverted and cover three of seven

**Status:** open - **fix before the funded run, not after**
**Found:** 2026-09-11, verifying scenario names for the Chapter 6 prose pass

`srq4_experiment.py` writes its summary table through a display-label map that
covers **three** of the seven registered scenarios, and **inverts the lettering**
for all three:

| internal name | prints as |
|---|---|
| `C_model` | **"A - dedicated model"** |
| `B_data` | "B - code-as-action" |
| `A_plain` | **"C - no firm data"** |

`D_prometheus`, `E_prometheus_model`, `F_data_model` and
`G_prometheus_data_model` are not in the map, so they fall through to their raw
internal names. **One header row can therefore mix inverted display letters with
raw internal names.**

**Why it must be fixed before the funded run:** published tables carry the
labels. A table whose first column reads "A" for the dedicated-model arm, while
the chapter's own ladder calls that arm C, is the kind of defect that makes a
reader distrust every number beside it.

**Why the inversion exists:** the display order runs best-to-worst for a reader,
while the internal order runs as an information ladder from least to most
capability. Both orderings are defensible; **carrying both at once is not.**

**Recommendation:** delete the display map and print the ladder letters, which
are the ones the thesis uses. If a best-first presentation is wanted, sort the
columns and leave the names alone.

⚠ Blocks the Section 6.7 rewrite (Fix 14 of `ch6-prose-pass.md`) alongside the
F/G run, because that section is where the scenarios get named.

---

## S20 addendum - "baseline" has two sites, not one

**Added 2026-09-11** to the existing S20 entry above.

Section 6.4 also uses "baseline", in *"it is instead the baseline against which
the artefact is compared"*. The Chapter 6 pass changes it to **"comparator"** on
the assumption the ladder framing wins.

**If "baseline" is kept, revert that one word** - Fix 8 of
`ch6-prose-pass.md`. The decision should be taken once for both sites.
