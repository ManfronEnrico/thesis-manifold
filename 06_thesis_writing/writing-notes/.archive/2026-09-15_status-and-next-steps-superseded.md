---
name: 2026-09-14_BRANCH_A_status-and-next-steps
description: NOTE - Where BRANCH A stands on 2026-09-14 afternoon. What landed, the 38 remaining threads, subtitle decisions, and the ordered queue to submission on 2026-09-15 14:00.
category: workflow
applies-to: [all chapters, submission preparation]
triggers: [what is left, status, where are we, what next, submission checklist]
created: 2026_09_14-16_55
updated: 2026_09_14-16_55
snapshot: 2026-09-14_16-21_post-comment-pass-archive
status: current
---

# BRANCH A — status, 2026-09-14 afternoon

**Submission: 2026-09-15 14:00.** Branch B is closed (`41ecb76`); the thesis
ships Branch A.

Verified at `41ecb76`, fetch clean, origin and HEAD level. Snapshot
`2026-09-14_16-21_post-comment-pass-archive` — **46,726 words, 44 comments in 38
threads.** Zotero: 89 items.

---

# What landed today

| | |
|---|---|
| Comment threads | **100 → 38** |
| Applied prose passes | Ch1, Ch2, Ch3, Ch4, Ch5, Ch7, Ch9, Ch10 |
| Notes archived | 10 |

**Chapter 3's rewrite was the largest single repair in the thesis.** Verified
against this snapshot: no "LLM-as-judge" anywhere, no "approximately fifty
prompts", no "five Nielsen categories", the data cutoff corrected to July 2026,
Optuna cited to Akiba et al. (2019), and the sequential-execution limitation
inverted to the honest version — the memory budget bound the *selection space*,
not run time. +394 words.

**Ch1** lost the 8 GB budget entirely (−15 words net), and its §1.5 chapter map
now points at the right chapters and counts ten of them. **Ch2** dropped the
"designed; benchmark to be built" status labels and the judge-model method
(+85 words).

⚠ **One correction to my own note.** The Ch3 rewrite's Fix 9 asked for "four
limitations"; §3.7 correctly says **five** and lists five. I had proposed merging
two paragraphs and Brian kept them separate, which is the better structure. **No
defect — the count is right as it stands.**

## The reference list, explained

It dropped 1,318 words (177 → 75 lines) and I flagged it as unaccounted for.
✅ **Intentional:** the static reference list from the first draft was removed and
transferred to a `.txt` file, so the final dynamic list can be generated against
it.

⚠ **Sequencing this correctly matters.** The dynamic list can only be finalised
once every static in-text citation has been replaced with a Zotero field —
otherwise the bibliography will not match the text. **In-text first, then the
list.** That is Ch1 threads 22 and 25 (the workflow notes) and thread 309.

---

# The 38 remaining threads

**Five are unresolved work. The rest are queued, mechanical, or verifiable.**

| Surface | Threads | State |
|---|---|---|
| **Abstract** | 8 | **Blocked** — S29, write last. One task |
| **AI Use Declaration** | 4 | **Next up** — four drafts in `2026-09-14_BRANCH_A_ai-use-declaration-drafts.md` |
| **Chapter 4** | 9 | 6 VERIFY sweeps whose numbers reconcile to artefacts; ⚠ **thread 91's two figures (728, 2,442) remain untraced** |
| **Chapter 1** | 8 | 2 Zotero-workflow, 1 M5 verify, 3 RAM-framing (resolvable as VERIFIED-OK), plus 41 and 44 |
| **Chapter 3** | 3 | 2 watermarks → new note; 1 submission-repo reminder |
| **Chapter 2** | 1 | Thread 54, reword per decision below |
| **Ch7, Ch8, Ch10, refs, appendix** | 5 | One each, all known and recorded |

## Two Ch1 threads escalated rather than resolved — both my misreads

- **Thread 41** now says *"REWORD: We must shorten the length of the sub research
  question while retaining the meaning."* My note had recommended leaving SRQ4
  alone because it appears in Ch3, Ch8, Ch9 and Ch10. ⚠ **That caution still
  holds** — shortening it means four other chapters must match. **If it is
  shortened, it is a find-and-replace across five surfaces, and it must be done
  in one pass.**
- **Thread 44** says *"RE-GENEREATE"* for Figure 1. I had guessed it was already
  satisfied. It is not — the figure needs regenerating, and it belongs with the
  appendix/figure work already in flight.

## Decided this session

**Ch2 thread 54** (the descriptive-BI claim needs a source): ✅ **reword to stand
on what follows**, per Brian. The block is in the archived Ch2 note, Part 3. The
opening becomes framing rather than an assertion needing support:

> "Business intelligence systems have conventionally served the descriptive tier
> of the analytics spectrum..."

---

# Subtitles

**Ch4 already has one** (*From Scanner Panel to Modelling Matrix*). **Ch10's is
written** in its applied rewrite (*What the extension is worth, and on which
axis*) — confirm it landed.

| Chapter | Recommended | Alternative |
|---|---|---|
| **1 · Introduction** | *A capability gap in a deployed system* | *Extending a system that explains but cannot anticipate* |
| **2 · Literature Review** | *What is known, and what is missing* | *From descriptive analytics to forecast-informed decisions* |
| **3 · Methodology** | *How the artefact was built, and how it was judged* | *Design, construction and evaluation* |
| **8 · Experimental Evaluation** | *What each rung of the ladder buys* | *Seven scenarios, one question* |

⚠ **"Why a working assistant cannot forecast" is withdrawn.** Brian's challenge
was correct: the thesis does not answer why the deployed system cannot forecast.
It takes that as its premise and asks what extending it costs and buys. A
subtitle that promises an answer the thesis never gives is worse than none.

⚠ **Chapter 8's current subtitle is too long** — *"Seven scenarios on a shared
question, and what each rung of the ladder buys"* is thirteen words and wraps.
Both replacements above are five or fewer and keep the ladder metaphor, which is
the chapter's organising idea.

---

# The queue to submission

**Ordered by dependency, not by importance.**

| # | Item | Blocks | Owner |
|---|---|---|---|
| 1 | **AI Use Declaration** | nothing | drafts ready, pick one |
| 2 | **Appendix regeneration** — tables, figures, EDA | items 3 and 4 | Brian, in flight |
| 3 | **Select artefacts for in-text vs appendix** | the abstract's final numbers | after 2 |
| 4 | **Figure 1 regeneration** (Ch1 thread 44) | — | with 2 |
| 5 | **Abstract** | — | **write last** |
| 6 | **In-text citations → Zotero fields**, then the dynamic reference list | the bibliography | Brian |
| 7 | **Watermark sweep** | — | new note, run on a locked document |
| 8 | **Submission repository** (`/submission-export`) | — | Ch3 thread 70 |

## What must not slip

⚠ **The abstract is the first page an examiner reads and it is still a bullet
skeleton** carrying `[TBD - fill after empirical results]`, an "Indeks Danmark
consumer survey" that does not exist, "≤8GB RAM", a "3-level evaluation
framework" with an LLM judge, and four bracketed SRQ placeholders. **S29.**

⚠ **The appendix still ships the superseded prompt schema** — `v4-five
scenarios+e37111d3daaa` against the funded `v6-shared-composition+af04a42a478b`.
Regenerate, never hand-edit; it is generated by `export_appendix.py`.

⚠ **`ch7_scenarios_v2.svg` draws five scenarios where seven ran.** Same redesign,
same regeneration pass.

⚠ **`scenario_inputs/` is a stale export naming pre-F58 brands** (S33). Re-export
is not possible — `agent_inputs/` holds only CSD — so the recommendation is
**delete**, or strip the README's false "cannot drift" claim.

---

# Live notes, and what each is for

| Note | Purpose |
|---|---|
| `00_appendices/…appendix-inventory-and-provenance-audit.md` | the master artefact audit — 242 files, 36 producers |
| `00_appendices/…table-format-options-and-two-findings.md` | table rendering options |
| `ch{1..9}/2026-09-14_appendix-citations-ch*.md` | per-chapter artefact citation recommendations, **none applied** |
| `2026-09-14_BRANCH_A_ai-use-declaration-drafts.md` | four drafts, awaiting selection |
| `2026-09-14_BRANCH_A_watermark-patterns-to-remove.md` | seven machine-writing patterns, sweep not yet run |
| `2026-09-14_BRANCH_A_remaining-comment-threads.md` | ⚠ **partly spent** — its Ch2/Ch3/Ch4 sections describe threads now closed. Its Abstract, AI-declaration and appendix items are still live |
| `2026-09-13_18-40_…cross-chapter-flow-and-connectedness.md` | nine cross-chapter items; C2 struck, most applied |
| `deferred-structural-decisions.md` | S1–S33, cumulative |
| `anticipated-assessor-questions.md` | defence preparation, current |
| `citations-added-register.md`, `post-hpc-validation.md`, `dec-vendor-model-choice.md` | registers |
| `ch3_methodology/srq4-data-input-is-a-constructed-choice.md`, `verification-of-the-experimental-harness.md` | design rationale, reference |
| `ch5_model_benchmark/ch5-profiling-rerun.md` | measurement task |
| `ch8_experiment/*.md` (7 files) | design rationale, reference |
| `ch9_discussion/the-result-hinges-on-forecasting-practice.md` | spans four chapters, reference |

**Nothing in the chapter folders is an unapplied prose pass.** Every pass written
this session has been applied and archived.
