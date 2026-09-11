---
pid: P0048
created: 2026-09-07 13:51:00
updated: 2026-09-07 16:45:00
---

# P0048 — Progress log

## Session 1 — 2026-09-07 (13:51 – 16:45)

**Account note:** this session ran under an account that is being switched away
from. Conversation history will not carry over. Everything below is reconstructable
from the files named.

### What was asked

Chapter-by-chapter prose pass from ch4 onward, verifying facts first, then generating
context-aware prose to paste into the `.docx` — and working the `05_thesis_results/`
tables and figures in as in-text citations.

### What happened

**1. Orientation.** Found the repo has been restructured to SRQ-aligned tiers
(`01_SRQ1_Model_Training/` … `06_thesis_writing/`); CLAUDE.md still documents the old
`00_thesis_context/` … `05_thesis_writing/` layout and is stale.

Snapshot `2026-09-05_19-52_complete-review-pass` read first; Brian later pointed at the
newer `2026-09-07_14-29_holiday-enrichment`, which is what the writing note is anchored
against.

**2. Chapter survey.** Ch4 is in better shape than expected — real prose throughout,
not bullets. The thin chapters are Ch7 (1,189 w), Ch8 (1,339 w), Ch9 (1,194 w). Ch8
splits diagnostically: **Results** subsections are real prose, **design** subsections
are unconverted bullets with unfilled placeholders (F8).

**3. Fact-checking Ch4 against current outputs.** Every locked parameter had moved.
Initially reported this as "prose is right, outputs disagree" — **Brian corrected the
authority direction**: the repo outputs are ground truth; the `.docx` prose predates the
EDA work and Enrico regenerated the pipeline. That inversion is what made the rest of
the session tractable.

**4. The horizon investigation (F1, F2).** Brian asked what H1/H3 meant, then asked to
document both and ensure both are benchmarked, including SRQ4 at 3 months with held-out
ground truth retained.

Investigating turned up the central finding: the horizon never reaches feature
construction, so both matrices are one-month tasks. Also corrected my own earlier
assumption — the published results are the **h3** file, not h1 (row-count proof).

**5. Writing note produced.**
`06_thesis_writing/writing-notes/srq1-forecast-horizon-defect-and-split-correction.md`,
following the structure of the existing holiday-enrichment note and the
`write-prose-from-bullets` skill: bullet skeleton, placement contract with verbatim
anchors, prose, provenance, blocked items declared.

**6. Plan created (this folder).**

### Corrections made mid-session

Worth recording, since the reasoning is not otherwise recoverable:

- **Authority direction** — I treated the `.docx` as correct and the outputs as drifted.
  It is the reverse. Corrected by Brian.
- **Which horizon is published** — I assumed h1 because the EDA showed both. `grep`
  showed zero `_h1` references in SRQ1 code, and row counts confirmed h3.
- **MIN_PERIODS framing** — I listed "30 → 15" as a loosened threshold. It is better
  than that: 15 is *derived* (`warmup + horizon + 1`), which retracts a limitation the
  thesis currently concedes (F6).

### Deliverables

| File | State |
|---|---|
| `writing-notes/srq1-forecast-horizon-defect-and-split-correction.md` | complete; 2 blocks paste-ready, 2 declared blocked |
| `plans/P0048_.../START_HERE.md` | complete |
| `plans/P0048_.../task_plan.md` | complete |
| `plans/P0048_.../findings.md` | F1–F8 complete |
| `plans/P0048_.../tasks/*.json` | 8 tasks |

### Nothing was changed in the repo

No code edited, no matrices regenerated, no `.docx` touched. The horizon fix is
**proposed, not applied** — deliberately, because it invalidates results Enrico
produced and he should be asked first (task 2).

### Next session starts here

1. Read `START_HERE.md`.
2. Brian pastes blocks P1 and P2 (closes 8 Word threads).
3. Raise the horizon question with Enrico — wording is in `START_HERE.md`.
4. On confirmation, apply the fix, regenerate, re-benchmark **with `XGB_N_JOBS=1`**.

## 2026-09-08 — Chapter-swap dependency verified (from the P0050 session)

Not a work session on this plan; findings transferred in from the figures/tables
session at Brian's request. He has decided to **execute the swap in this plan's
session**, not P0050's, because this session carries the prose context.

- Measured Ch5↔Ch6 dependency against snapshot `2026-09-07_19-41_internal-links`:
  **Ch5→Ch6 = 4 refs, all forward pointers; Ch6→Ch5 = 0.** The swap is safe and
  needs no argument rewritten — only renumbering.
- Wrote a full execution recipe into findings F(new): the one-line `CHAPTER_SLUGS`
  edit, two folder renames, six diagram stems, ~30 Word edits, and the
  `§5.2`-is-a-citation trap that would corrupt three Hyndman references.
- Added sequencing constraint 4: do phase 8 **before** phase 5, so cross-references
  are written once.

Nothing was executed. No code, folders or prose were changed by this transfer.

---

## 2026-09-09 — Chapter 4 prose pass, applied

**Delivered.** Chapter 4 is prose. Brian applied nine of the ten proposed fixes
plus the follow-up's table edits, and closed seven Word threads (27 → 20).

Sections rewritten and pasted: the retention rule and coverage figures (§4.1.2),
the duplicated minimum-history paragraph (§4.1.2), the null/negative/zero claims
(§4.1.3), the retired filter and the ARIMA sentence (§4.1.4), scope and filtering
(§4.2.1), the seasonality changelog (§4.2.3), the matrix widths (§4.3), and the
whole risks section (§4.5), which went from nine bold-lead fragments to five
prose paragraphs.

**Verification base.** Every figure measured against the pipeline's own
`step_2_*.csv` EDA tables, the eight feature matrices, the split-date JSON, and
the SRQ1 training scripts — not against previous notes. Three claims turned out to
describe a pipeline that no longer exists (F17), and the feature count changed
under us mid-session (F16).

**Tried and rejected.**
- *Deleting the holiday and weighted-distribution rows from Table 4.* Brian
  pushed back because retraining was in flight. He was right, and the columns
  became standard inputs the same day. Relabelling survives a rerun with a
  one-word edit; deletion has to be rebuilt.
- *Claiming the holiday columns' linear dependence rules out a linear model.*
  `srq1_ridge_cv.py:166` fits all three and drops none — the L2 penalty absorbs
  it, which is the better point and is what the prose now says.
- *Editing the reviewed pass file in place* (F19).

**Near-miss.** The follow-up was regenerated against a fresh snapshot only
because Brian asked. Had it not been, it would have re-proposed nine already-applied
blocks and missed two new comment threads.

**Left broken, deliberately.** `writing-notes/unverified-claims-to-check.md` is
referenced five times across the rule and skill and **does not exist** — the real
system is the `CV-NN` packs under `notebookLM/04-Claims_Verification/`. Three of
those references predate this session (present in commit `202f75a`). Fixed the two
I wrote; left the pre-existing three and recorded them as S12 in the deferred
list rather than repointing committed text at end of day.

**Four new tracking surfaces**, all cumulative across chapters:

| File | Holds |
|---|---|
| `writing-notes/deferred-structural-decisions.md` | 12 layout/cross-reference items, each with a recommendation |
| `writing-notes/post-hpc-validation.md` | 10 claims awaiting the training run, 2 marked as gates |
| `writing-notes/citations-added-register.md` | 8 citations with Zotero keys and the claim each must support |
| `ch4_data_assessment/ch4-prose-pass-followup-01.md` | 7 remaining Chapter 4 items |

**Six rules added** to `prose-insertion-discipline.md` and the skill: no
metacomment in prose, relabel-don't-delete when a rerun is in flight, the deferred
list, freeze a reviewed note, `git fetch` before verifying, snapshot before every
follow-up, Zotero re-pull before checking citations, register every added citation
with its claim, and record pending measurements when the claim is written.

**Next.** Chapter 5 — 39 bold-lead fragments, 55 lines with no terminal period,
49 open threads, and the chapter is the largest remaining prose job. Its §5.3.2
still states in bold that *"No holiday calendar is used"*, which is false and
contradicts Chapter 4 in the same document.

---

# 2026-09-10 — Chapter 5 verified, reorganised, and given a literature spine

## What the chapter turned out to be

Every results table stale, and **two findings changed identity**. Danskvand was
reported as won by Ridge at 10.9% weighted error, roughly half the tuned models;
Ridge is now **74.9%, the worst of six baselines**, and the category is won by
Prophet. The plateau claim moved from a median near 16 trials to 54.

Six sections carry factual errors beyond stale decimals: the feature count (13
described, 18 used), a bold claim that no holiday calendar is used which became
false on 2026-08-18, every operational figure, the calibration table's headline
example, the pooling comparison's cross-family agreement, and the median-APE
trade-off in 5.4.1.

## Reorganised from fixes to sections, on Brian's instruction

The first pass was sixteen fixes, which meant jumping around the document. **Its
F1 proposed repairing twenty-one cross-references inside bullet lists that the
pass itself deletes** — work that would have been thrown away two fixes later.

`ch5-prose-pass-followup-01.md` replaces it: every section in document order, each
carrying its state, what was verified, its comment verdicts, and paste-ready
prose. References are rewritten as part of the prose, named rather than numbered.
All 49 threads carry a verdict.

## An error worth recording

A pass claimed section 5.5.9's per-seed winner table could not be reproduced from
any artefact, blocked it as a gate, and warned that section 5.6 rested on nothing.
**The data was in `stability.md` all along** — the pass had searched
`10_seed_stability.csv`, the appendix export, and concluded the question was
unanswerable rather than looking for the source.

A follow-up then instructed Brian to **delete a correct, sourced table**. Caught
and reversed. Recorded in `post-hpc-validation.md` as withdrawn rather than
resolved, because the failure mode will recur: **an appendix table is a projection
of a result, not the result.**

## The August reference notes were checked, not assumed

Three notes sat in the Chapter 5 folder from 22 August. Measured against current
artefacts, all three are stale on numbers and one has **inverted**: the
pooled-vs-per-category note says the sign flips exactly once and both model
families agree on all four categories, and tells you to lead with that. They now
disagree on two, with a 9.8-point delta against its stated 2.5-point ceiling.

Their citation work survived and is now F16 of the pass, because it concerns what
a source says rather than what a run measured.

## Citations audited per source

Fifteen sources, checked one at a time against the **unfiltered** Zotero API
rather than `citations.json`, which filters by item type. All fifteen present.
Brian rebuilt the malformed Hyndman entry; **DEC-FPP-WHOLE-BOOK** now records that
the book is cited whole, with a section locator only where a passage is quoted and
never a page number.

Two duplicate-author pairs remain a live risk — two M4 papers and two Bergstra
papers, indistinguishable in rendered text, where a wrong citation field shows up
only in the bibliography.

## Six FPP3 sections read directly

Brian printed all 40 section PDFs. Six read, quoting with page numbers.
**Two findings are defects rather than citation gaps:**

- **13.3** handles bounded forecasts through the transformation and calls an
  artificial constraint "unrealistic". The thesis clips post-hoc without stating
  the bound.
- **5.6** states a back-transformed point forecast is a **median, not a mean**,
  and that medians do not aggregate additively. The tool serves per-brand
  forecasts with no warning against summing them — an SRQ2 item.

Also closed Chapter 4's open ARIMA minimum-length claim: it has no source because
13.7 calls such rules "misleading and unsubstantiated" and names 30 as having no
justification. **Remove the claim rather than source it.**

⚠ **A caution on how those six were read.** All six were read in full, but the
quotations came almost entirely from pages 1 and 2 — that is where each section
states its thesis, and the reading stopped once a usable quote appeared. Brian
caught the pattern. The quotations are real and checkable; the coverage was not
what it looked like. **Section 12.2's strongest sentence for this thesis is on its
last page.** Tomorrow's pass quotes from where the answer is.

## Next

**Chapter 5 to finished prose, plus a retraining decision**, defined as a session
in `task_plan.md`. Chapter 5 is the last chapter that produces rather than
consumes SRQ1 output, so the retraining question is settled here or it costs the
chapter twice.

Five candidates are open and **four are wording problems rather than measurement
problems**. Only the missing seasonal ARIMA order is arguably worth a re-run.

---

# Session 2026-09-11 (evening) — Chapter 5 closed, Chapter 6 all but closed

## Delivered

| | |
|---|---|
| **Chapter 5** | every thread closed. Two re-runs landed and both moved numbers |
| **Chapter 6** | 17 threads → 4; 2,176 → 2,553 words; everything applied but Section 6.7 |
| **Section 6.7** | written, waiting to be applied |
| **Assessor questions** | new cumulative note, 15 answered + 5 not yet answerable |
| **Experiment insights** | routed to four chapters that had no note for them |

## The two re-runs, and why they were needed

**The calibration re-run** fitted XGBoost for all four categories while two serve
LightGBM. Fixed to read the served model from metadata. Nine seconds, locally —
the HPC was never needed, because it fits four models with no tuning loop.
Coverage became strictly monotone with calibration set size, strengthening the
chapter's central claim.

**The profiling re-run** came from applying Brian's own rule: a cited number must
come from an artefact regenerated *after* the last training. Last training was
09-09 21:10; `profiling.csv` was 09-01 21:32. Eight days early, and the only
Chapter 5 source that failed the check.

⚠ **It moved a long way and not in the predicted direction.** Chapter 5 had
inferred the 13-feature figures were a *lower bound* on the 18-feature model.
They were not:

| | before | after |
|---|---|---|
| LightGBM | 38.1 | **14.9** |
| XGBoost | 29.2 | **31.9** |
| Ridge | 5.4 | **1.6** |

**Memory tracks the size of the tuned ensemble, not the width of the feature
matrix.** That is a better claim than the hedge it replaces.

⚠ **This will recur.** `srq1_profiling.py` is deliberately excluded from
`run_both_horizons.py` because it runs at `n_jobs=-1` on purpose. **Re-run it by
hand after every retraining.**

## Chapter 6

Consolidated three notes into one pass, then wrote Section 6.7 after the arm
rename unblocked it. Both earlier notes and the 978-line sample-size rationale
are archived; two sections of the latter were carried forward and re-verified,
and its RTD "empty fact table" warning was confirmed superseded.

**Two comments found defects in the artefact rather than the prose**, both
verified in code rather than taken as read: there is no human approval gate
anywhere, and temperature is not settable on the pinned model.

## Two things I got wrong

1. **I reported Fix 3b as applied. It was not.** "With human oversight" still
   sits in Section 6.2, and it is now the only surviving claim of a control the
   artefact lacks.
2. **I repeated the cost under-reporting claim** (1.20x–1.77x) from P0049 F57.
   The experiment session retracted it the same evening: the costs endpoint
   buckets by whole day, org-wide, so every comparison was against a day of
   unrelated traffic. **Like for like the estimate is conservative by ~17%.**

⚠ **The lesson from the second is worth keeping.** The tell was in the data and
was walked past by both of us: the harness recorded zero cached-input tokens
while the day's billing carried a cached-input charge. A number that cannot have
come from your own process is the strongest possible signal that a comparison is
not like-for-like.

## Found, not fixed

- **Section 6.8 carries a duplicated clause** — "Memory is reported by RSS;
  Memory is reported by resident set size". The only application error in the
  pass.
- **Semerikov et al. (2025) is cited twice and is not in Zotero.**
- **Three more duplicate Zotero items** and two malformed dates (S16).
- **Two finding IDs are used twice** across parallel sessions (S23).
- **"Spanning the accuracy-efficiency frontier"** overstates the substrate.
  Prophet records 105.7 and 975.0 on two categories — while *winning* Danskvand
  at 19.4, which makes per-category selection the interesting reading.

## Open, and whose it is

| | |
|---|---|
| Apply `ch6-followup-02-section-6-7.md` | Brian |
| Semerikov: add to Zotero or drop | Brian |
| "baseline" vs "comparator", two sites | Brian |
| Chapter 6 subtitle, three options offered | Brian |
| The funded experiment run, 1–2 hours | Brian, tomorrow |
