---
name: p0055-start-here
description: STATE - Entry point for P0055. The forecasting-feature re-engineering attempt, run on a branch with a named fallback. Written for a session with no conversation history.
pid: P0055
created: 2026_09_12-21_00
updated: 2026_09_12-21_00
status: in_progress
---

# P0055 — Forecasting feature re-engineering: START HERE

> ## THIS PLAN IS OPTIONAL WORK WITH A GUARANTEED FALLBACK.
> Everything it attempts can be abandoned. If it is not finished in time, the
> thesis ships the results already on `main`. **Read `FALLBACK.md` in this
> folder before touching anything** — it records the exact commit to return to.

---

# ⚠ READ FIRST — updated 2026-09-13

## 1. Branch B runs on `main`. Do NOT create a branch.

`task_plan.md` step 0.5 says `git checkout -b data/forecasting-feature-reengineering`.
**That step is deliberately NOT taken.** A concurrent session is finalising
Branch A's Ch9/Ch10 and must push to `main` so Enrico has access; only one
branch can be open at a time.

**Isolation is by FILE SURFACE instead. Read `BRANCH_B_FILES.md` before any
edit** — green / red / amber zones, plus the announcement rule for regenerated
results tables. Creating a branch here would break the other session.

## 2. Phase 0 is COMPLETE. G0 passed.

`58243f3` is committed **and pushed** — `origin/main...HEAD` returns `0 0`.
Earlier text in this plan folder says it was not pushed; that was true when
written. The fallback is safe.

## 3. The scan is CLOSED, 41 of 41.

5.5, 6.7 and 9.7 were all obtained and read on 2026-09-13. §9.7 was never
missing — it had been on disk since 09-10 and was merely unread.

## 4. Where to start: task 4.

Tasks 1 and 3 are complete (`tasks/*.json`). **Task 4 is the gate**: write and
run a Ljung-Box residual test. It is free — no retrain, no API spend — and its
verdict decides whether the 2.B feature additions happen at all.

⚠ **It must pass `dof = p + q`** (§9.7). Omitting it overstates significance,
biasing the gate toward "do more work".

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
