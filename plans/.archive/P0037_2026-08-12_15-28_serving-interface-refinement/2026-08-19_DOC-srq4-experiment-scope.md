---
name: 2026-08-19_DOC-srq4-experiment-scope
description: DOC - What must exist to run the SRQ4 System A vs System B experiment, the thesis' central premise
category: reference
applies-to: [03_thesis_modelling, 04_thesis_results]
triggers: [srq4, system a vs b, thesis premise, llm experiment]
created: 2026_08_19-10_30
updated: 2026_08_19-10_30
---

# SRQ4 scope — what must exist to test the thesis premise

**The premise**: does having a dedicated forecasting model available improve an LLM's
answers, versus letting the LLM write its own forecasting code?

The harness for this already exists at
`03_thesis_modelling/model_training/srq4_experiment.py`. It is further along than the
plan files suggest. This document says what still has to be true for it to produce a
result you can defend in a chapter.

## The design, as already implemented

One variable under test: **how the agent produces a forecast.**

| | System A (Oracle) | System B (Prometheus-style) |
|---|---|---|
| Mechanism | Claude calls a `forecast_demand` tool | Claude writes and runs its own code in an E2B sandbox |
| Backing | pre-trained XGBoost via `forecast_service.py` | the brand's monthly history, pandas/numpy/sklearn/statsmodels |
| Code written by the model | none | all of it |

Held constant: the model (`claude-sonnet-4-6`, temperature 0), the prompts, the brand,
the horizon. Recorded per run: numeric forecast, token cost, latency. Scored against
the held-out actual; consistency measured as spread over repeated runs.

That is a clean single-variable design. **The experiment is well posed** — what it
lacks is execution, not conception.

## Blocker: credentials

`srq4_experiment.py` reads `03_thesis_modelling/.env` for:

```
ANTHROPIC_API_KEY=...
E2B_API_KEY=...
```

The file is gitignored and absent from this machine, so the harness raises
`FileNotFoundError` on import. **Nothing else about SRQ4 can be verified until it
exists.** This is the single highest-value unblock in the repo.

`forecast_service.py` itself imports cleanly, so System A's backing is in place.

## What is ready

| Component | State |
|-----------|-------|
| Feature matrices, 4 categories x 2 horizons | **done**, verified 8/8 |
| H=3 as primary horizon | **decided** (DEC-HORIZON), all 13 call sites repointed |
| `forecast_service.py` | **imports cleanly**; open-world feature selection |
| Trained models + SRQ1 benchmark | **runs**, XGBoost wins all four categories |
| SRQ4 harness code | **written**, cannot execute |

## What must be settled before results are quotable

### 1. Conformal calibration uses the wrong split (P0037 task 7)

`build_service` calibrates prediction intervals on **test** residuals. The intervals
are therefore fitted on the data they are evaluated against.

This matters more than a normal bug because the thesis' contribution rests partly on
leakage discipline — the pipeline now demonstrates that discipline everywhere else
(rolling windows exclude the current month, `promo_intensity` uses t-1, splits are
strictly ordered, contemporaneous measures are excluded from features). Shipping a
results chapter whose intervals are calibrated on test data undercuts that claim in
the one place a reviewer will look hardest.

**Fix**: calibrate on validation residuals. Small change, high defensibility value.

### 2. What counts as a "better answer"

The harness records a numeric forecast and scores it against the actual. That answers
*accuracy*. The premise as stated — "improves LLM responses" — is broader.

Decide and state which of these the thesis claims, because each needs different
evidence:

| Claim | Evidence needed |
|-------|-----------------|
| A is more **accurate** | forecast error vs held-out actual (harness does this) |
| A is more **consistent** | spread across repeated runs at temperature 0 (harness does this) |
| A is **cheaper / faster** | tokens and latency (harness does this) |
| A is more **trustworthy** | traceability: which model, which cutoff, which data (P0037 task 4 — *not implemented*) |

The first three are already instrumented. The fourth is named as an SRQ2 property with
zero implementation. Either implement it or drop the claim.

### 3. Sample size and generalisation

One brand through one prompt is a demo, not a result. Before writing the chapter,
decide:

- how many brands, and chosen how (top-N by volume risks selecting the easiest series)
- how many prompts per brand, and how many repeats per prompt for the consistency
  measure
- which categories — all four, or CSD only with the others as robustness

**Recommendation given the deadline**: CSD as the primary experiment with a stated
number of brands and repeats, and one smaller category as a robustness check. That is
defensible and finishable. Four categories at full depth is not, and a reviewer will
accept a scoped claim more readily than a thin one spread wide.

### 4. System B's failure modes are part of the result

System B writes its own code, so it can fail in ways System A cannot: syntax errors,
timeouts, hallucinated columns, a forecast that is not a number. **Those are findings,
not noise.** Decide now how they are recorded, because retrofitting a failure taxonomy
after the runs means re-running them.

A precedent from this session: Prophet's unbounded trend produced a forecast of 101M
against 301k actual (F72). If System B writes something similar, it must be reported
as a divergence rather than averaged into a mean — the same reasoning that removed
`mean MAPE` from the SRQ1 table (F75).

## Suggested order

1. **Add `.env`** with both keys — unblocks everything, costs minutes
2. **Run `--demo`** — one prompt through A and B, confirm the harness works end to end
3. **Fix conformal calibration** to use val residuals (task 7)
4. **Decide scope** — brands, prompts, repeats, categories — and write it down before running
5. **Run the experiment**, recording System B failures as a category
6. **Then** resume P0034 chapter reconciliation, once these numbers are final

Steps 1-2 are the ones that tell you whether the remaining schedule is realistic. Do
them first, even before the calibration fix.

## Deliberately out of scope

Everything the EDA plans still list. The pipeline is verified and its remaining gaps
are reporting-level, not correctness-level (P0031 task 3's heterogeneity forwarding is
the only one, recorded as a limitation). With under a month to submission, further EDA
refinement trades directly against the 120 pages and against the experiment that is
the thesis' actual contribution.
