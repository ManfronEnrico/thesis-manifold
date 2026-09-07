---
name: p0048-start-here
description: STATE - Entry point for P0048. Written for a session with NO prior conversation history. Explains the horizon defect, what is ready to paste, and what to do next.
pid: P0048
created: 2026_09_07-16_40
updated: 2026_09_07-16_40
status: handoff
---

# P0048 — START HERE

**You have no conversation history for this work.** It was produced in a session on
2026-09-07 under a different account. Everything is on disk. Read this page, then
`findings.md`.

---

## What this plan is

Finish the thesis prose from **chapter 4 onward**, and work the contents of
`05_thesis_results/` into the text as in-text citations.

The thesis currently cites **2 figures in total**, while `05_thesis_results/` holds
~317 files including per-category EDA plots that exist precisely to support chapter 4.

Working method, per section: **verify facts against the result files first, then write
prose with verbatim anchors.** Brian pastes into the OneDrive `.docx`. Never edit the
`.docx` or a snapshot yourself (`writing-surface-authority`).

---

## The one thing you must understand before touching SRQ1 numbers

### The forecast horizon is not implemented

The pipeline advertises two horizons — **H1** (one month ahead) and **H3** (three
months ahead, the primary reported one, because a quarter is when marketing budgets
are authorised). It threads `--horizon` through parameter derivation, contract
validation and filenames.

**It never reaches feature construction.** `engineer_features()` has no `horizon`
parameter. Lags are `shift(lag)`, so `lag_1` is always last month.

Reproduce it in one command:

```bash
python -c "
import pandas as pd
d='01_SRQ1_Model_Training/01_thesis_data/_03_engineered/bymonth/CSD/'
a=pd.read_parquet(d+'csd_feature_matrix_h1.parquet')
b=pd.read_parquet(d+'csd_feature_matrix_h3.parquet')
m=a.merge(b,on=['brand','period_year','period_month'],suffixes=('_1','_3'))
print('shared rows:',len(m))
for c in ['sales_units','lag_1','lag_3','lag_13']:
    print(c,'identical:',(m[c+'_1'].fillna(-9)==m[c+'_3'].fillna(-9)).all())
"
```

All identical. **Both matrices are one-month-ahead tasks.** The published results come
from the h3 file (row counts 1805/665/95 match `summary.md`), so the thesis reports
one-month accuracy while describing a three-month horizon.

**Brian's decision:** document both horizons and benchmark both, including SRQ4 at 3
months. Ground truth for that exists (7 held-out months, actuals present).

**Expect H3 accuracy to get worse after the fix.** That is correct and defensible.

---

## What is ready to paste RIGHT NOW

Both live in
`06_thesis_writing/writing-notes/srq1-forecast-horizon-defect-and-split-correction.md`
(PART 2 = placement contract, PART 2B = the prose).

| Block | What | Value |
|---|---|---|
| **P1** | Ch4 §4.4 split — full section REPLACE | **Closes 8 Word threads (183–191)** |
| **P2** | Ch4 §4.3 feature count 14 → 13 | Resolves the holiday note's open question |

Brian's own Word comments were right on every point: the split **is** proportional
(70/15/remainder), it is **not** locked, and no test window ends in March 2026.

**⚠ Apply P2 before the holiday note's P1.** That note says amend "14 → 17"; the base
is really 13, so the correct post-enrichment count is **16**.

Also ready, from P0047: `writing-notes/srq1-holiday-enrichment-result-and-limitations.md`
— six blocks, all unblocked.

---

## What is blocked, and on what

| Blocked | Needs |
|---|---|
| Ch4 horizon subsection (note P3) | the code fix + regeneration |
| Ch6/Ch8 dual-horizon results (note P4) | full SRQ1 re-run; **no H1 results exist** |
| Ch4 §4.2 EDA pass | the re-run — every figure there is stale |

Do **not** write prose describing a dual-horizon design before the fix lands. It would
put a false claim in the thesis.

---

## Scope boundary with P0049 — read this before starting anything

A parallel session created **P0049 (finalizing experiments)** on the same day. It
independently reproduced the horizon defect (its F22) and **owns the fix and every
re-run**. Its `START_HERE.md` says *"Don't do prose from P0049."*

| Plan | Owns |
|---|---|
| **P0048** (this) | Prose, drafts, Word threads, claims verification, citations |
| **P0049** | Horizon fix, SRQ1 re-runs, funded SRQ4 scenarios |

So tasks 2–6 below are **P0049's work**, kept here only because this plan's prose is
blocked on them. Do not run them from this plan — check P0049's status instead.

**P0045 and P0047 were archived into this plan.** Their open work is tasks 9–16;
their live state is in `INHERITED_CONTEXT.md`.

## Next action (decision, not code)

The fix invalidates results Enrico produced, so raise it before running anything:

> Was `engineer_features()` meant to shift the target by the horizon? Step 3 derives
> `min_periods = warmup + horizon + 1` and its docstring says H3 is the primary
> reported horizon, but lags are `shift(lag)` at both horizons — so h1 and h3 come out
> as the same one-month task on different brand sets. Merging the two matrices, every
> lag column is identical across all shared rows.

Then the fix: at horizon *h*, lags become `shift(lag + h − 1)`; rolling windows shift
identically. Everything else in the pipeline is already correct.

**⚠ Any re-run must set `XGB_N_JOBS=1`.** See
`plans/.archive/P0046_2026-09-05_21-10_exogenous-enrichment-decision/LOCKED_STATE.md`.
XGBoost with `n_jobs=-1` is not reproducible — 2.65 pp of WMAPE swing from thread
count alone, which is larger than most effects this thesis measures.

---

## Repo orientation (CLAUDE.md is out of date)

CLAUDE.md still describes `00_thesis_context/` … `05_thesis_writing/`. The repo has
since moved to SRQ-aligned tiers:

| Actual folder | Holds |
|---|---|
| `01_SRQ1_Model_Training/` | data pipeline (`01_thesis_data/`) + modelling |
| `02_SRQ2_Tool_Interface/` | structured tool interface |
| `03_SRQ3_Integration_Readiness/` | integration readiness |
| `04_SRQ4_Scenario_Experiment/` | scenario harness, runs, appendix exporter |
| `05_thesis_results/` | **all results**: appendix, eda, srq1–srq4, diagrams |
| `06_thesis_writing/` | drafts, snapshots, writing-notes, notebookLM |

Newest snapshot: `06_thesis_writing/docx-exported-snapshots/2026-09-07_14-29_holiday-enrichment/`.
Anchors in both writing notes are valid against it. Ask Brian before regenerating.

---

## Files in this plan

| File | Purpose |
|---|---|
| `START_HERE.md` | this page |
| `INHERITED_CONTEXT.md` | **live state absorbed from P0045 + P0047 when they were archived** — read before touching drafts, Word threads or claims verification |
| `task_plan.md` | phases, scope boundaries, sequencing constraints |
| `findings.md` | F1–F8, each independently reproducible |
| `progress.md` | session log |
| `tasks/*.json` | 8 tasks, restorable via the reload recipe in `config-prefer-task-list-breakdown` |
