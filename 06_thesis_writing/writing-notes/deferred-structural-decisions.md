---
name: deferred-structural-decisions
description: NOTE - Running list of structural decisions deferred out of chapter prose passes. Appendix placement, table siting, internal cross-references and cross-chapter fluidity. One row per item, carried forward between passes rather than re-derived.
category: workflow
applies-to: [chapter 4, chapter 5, chapter 6, chapter 7, chapter 8, appendix]
created: 2026_09_09-17_10
updated: 2026_09_09-21_35
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
