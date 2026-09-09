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
