---
name: p0055-start-here
description: STATE - Entry point for P0055. INACTIVE as of 2026-09-14 - Branch B was not pursued and the thesis ships Branch A. Kept for the book findings it records.
pid: P0055
created: 2026_09_12-21_00
updated: 2026_09_14-11_00
status: inactive
---

# ⛔ P0055 IS INACTIVE — the fallback was taken, as designed

**Decided 2026-09-14, 11:00.** Submission is due 14:00 on 2026-09-15, and
retraining plus re-running the experiment does not fit in the time remaining.
**The thesis ships Branch A** — the results already on `main`.

This is the plan working as intended, not a plan failing. It was written as
optional work with a named fallback, and the fallback was taken.

## Do not start any task in this folder.

Tasks 2 and 5–26 were never started. **Tasks 1, 3 and 4 are complete and their
output is on `main`** — the book scan and the Ljung-Box residual gate. Task 12
(re-run the gate on cross-validation residuals) will not run, so the gate's
in-sample limitation is permanent and is now **stated on the table itself**:
`05_thesis_results/05_model_benchmark/tables/residual_diagnostics.md`.

## What this folder is still good for

`findings.md` — 22 findings from a complete read of Hyndman & Athanasopoulos,
each one line-numbered against this repo. That is the evidence base behind the
limitations Chapters 5 and 9 admit, and behind the defence answers in
`06_thesis_writing/writing-notes/anticipated-assessor-questions.md`. It is worth
reading before the defence and is the most durable thing this plan produced.

---

<details>
<summary><strong>Superseded planning text, kept for the record — click to expand</strong></summary>

> Everything below describes Branch B as live work. It is retained because it
> records the reasoning behind the folder-split decision and the task list, but
> **none of it should be acted on.**

---

# P0055 — Forecasting feature re-engineering: START HERE

> ## THIS PLAN IS OPTIONAL WORK WITH A GUARANTEED FALLBACK.
> Everything it attempts can be abandoned. If it is not finished in time, the
> thesis ships the results already on `main`. **Read `FALLBACK.md` in this
> folder before touching anything** — it records the exact commit to return to.

---

# ⚠ READ FIRST — updated 2026-09-13

## 1. Branch B runs on `main`, in its own FOLDER TREE. Do NOT create a git branch.

`task_plan.md` step 0.5 says `git checkout -b data/forecasting-feature-reengineering`.
**That step is deliberately NOT taken.** A concurrent session is finalising
Branch A's Ch9/Ch10 and must push to `main` so Enrico has access; only one
branch can be open at a time.

**As of 2026-09-13, isolation is by FOLDER SPLIT** (task 26, Brian's decision),
superseding the file-surface contract. `BRANCH_B_FILES.md` still governs until
the split lands, and its RED zone stays correct afterwards.

**Why a folder split and not shared files** — three reasons, all Brian's:

1. **Branch A will not be retrained or re-experimented.** The money is spent and
   the 63 runs are locked. Fixing Branch A's code would make it *look* like it
   produced numbers it did not produce. Leaving Branch A wrong-as-shipped is
   **provenance, not debt.**
2. **`PATHS.py` forking is solved by naming it** — `PATHS_branch_A.py` /
   `PATHS_branch_B.py`, one repo-wide import rename. Measured: 1123 lines,
   **48 importers** (31 in `01_SRQ1_Model_Training`, 7 in `04_SRQ4`, 5 in
   `05_thesis_results`, 3 in `utility_scripts`, 1 in `02_SRQ2`).
3. **1.5 working days left.** Deleting a folder is verifiable by looking;
   git-reverting interleaved commits is not.

My original objection assumed long-run duplicate maintenance. There is none —
one branch gets deleted at the end.

**Three things the split must get right:** `05_thesis_results/05_model_benchmark/`
splits too (or Branch B's retrain overwrites tables Ch5/Ch9 cite *now*);
`02_SRQ2_Tool_Interface/forecast_tool.py` is in the split (`lag_13` at line 488);
`04_SRQ4_Scenario_Experiment/` **stays single and untouched**.

## 2. Phase 0 is COMPLETE. G0 passed.

`58243f3` is committed **and pushed** — `origin/main...HEAD` returns `0 0`.
Earlier text in this plan folder says it was not pushed; that was true when
written. The fallback is safe.

## 3. The scan is CLOSED, 41 of 41.

5.5, 6.7 and 9.7 were all obtained and read on 2026-09-13. §9.7 was never
missing — it had been on disk since 09-10 and was merely unread.

## 4. Where to start: task 26, then task 12.

Tasks 1, 3 and 4 are complete (`tasks/*.json`). **There are now 26 tasks, not
11** — tasks 12–26 were added 2026-09-13 after a diff of the book scan against
the task list found **25 findings recorded but never converted** (findings F15).

**Start at task 26 — the BRANCH A / BRANCH B FOLDER SPLIT.** Brian decided this
on 2026-09-13, against my initial recommendation, and his reasoning is recorded
in task 26 and below. Everything else lands inside Branch B's tree, so the split
comes first.

**Then task 12** — re-run the Ljung-Box gate on CV residuals.

### ⚠ G1 is PROVISIONAL, not passed. The gate I ran has a defect.

`srq1_residual_diagnostics.py` ran on **in-sample** residuals. §5.3 requires
**cross-validation** residuals — *"fitted values are often not true forecasts
because any parameters involved are estimated using all available observations,
including future observations."* The `dof = p+q` half (§9.7) and the log-scale
half were both done correctly; only this is wrong.

In-sample residuals are optimistically clean, so the true rejection rate is
likely **higher** than the 22.2% recorded — the verdict direction is probably
safe, but **the number must not be cited until task 12 re-runs it.** See F13.

## 5. Two things that are true and easy to get wrong

- **Task 2 (seasonal-naive lag) is NOT a standalone quick win.** There is no
  `lag_12` column in the matrices — verified in `csd_manifest_h3.json`. It is
  blocked behind task 5's rebuild. Do not compute a lag-12 inline.
- **§5.5 gives BRANCH A a free citation.** *"Point forecasts can be of almost no
  value without the accompanying prediction intervals."* Ch7 can cite it for why
  the interval-communication criterion exists. Hand to the Ch9/Ch10 session.

**You have no conversation history. This file is the whole picture.**

---

## The one-paragraph version

The SRQ4 experiment is **finished and locked**: 63 runs, prompt schema
`v6-shared-composition+af04a42a478b`, results on `main`. The experiment's
*architecture* — interface, integration, leakage boundary, prompt composition —
is final and **will not be touched by this plan**.

What this plan attempts is narrower, and **it is mostly repair rather than
addition**. Three sites in the forecasting pipeline are provably wrong — a
non-seasonal ARIMA on a seasonal monthly panel, a stationarity rule that
computes `p_diff` and never uses it, and a transform decision that computes a
verdict then returns a constant. **Chapter 5 already admits two of the three.**
Fixing them converts stated limitations into results. Only then, and only if
measurement justifies it, do new features follow.

Any of it means retraining, which means re-running the experiment (~$20,
~1 hour). The risk is running out of time, which the fallback removes.

---

## What is locked and what is in scope

| | Status |
|---|---|
| SRQ4 experiment architecture (interface, integration, leakage, prompts) | **LOCKED** — SRQ2/SRQ3 answered, do not change |
| Prompt schema v6 | **LOCKED** — any edit re-runs everything |
| Pooled / per-category training grain | **LOCKED** — a design choice, defended from M5 |
| Chapters 6 and 7 | **Declared locked** — but see the ⚠ below |
| Feature engineering (`engineer_features.py`, `_features.py`) | **IN SCOPE** |
| Chapters 4 and 5 prose | **IN SCOPE** — they describe the features |
| Chapter 8 results and figures | **IN SCOPE** — they change if models change |

### ⚠ Chapter 7 is not as locked as assumed

`ch7-verification-pass.md` pins its latency, token and cost figures to
`smoke/runs.csv` dated **2026-09-11**. That file has been **superseded** by the
63-run v6 set. Chapter 7's *argument* is unaffected; three of its *numbers* are
stale regardless of whether this plan proceeds. See `findings.md` F4.

---

## Read in this order

1. **`FALLBACK.md`** — the commit to return to, and how
2. **`findings.md`** — what is actually missing, with the evidence
3. **`task_plan.md`** — the phases, and the decision gate
4. `progress.md` — session log

## Related plans, and who owns what

| Plan | Owns | Relationship |
|---|---|---|
| **P0048** | remaining prose + results citations | Consumes this plan's output; Ch4/Ch5 prose changes land there |
| **P0049** | the SRQ4 experiment | **Complete for v6.** This plan re-runs it only if retraining lands |
| **P0050** | figures and tables | Regenerates everything after a retrain |
| **P0051** | EDA diagnostics computed-but-unconsumed | **READ IT FIRST.** It is this plan's evidence base, not a subset — see findings F5. Stays open |
| **P0053** | HPC training runs | The retraining executes there; runbook is in its `START_HERE.md` |

</details>
