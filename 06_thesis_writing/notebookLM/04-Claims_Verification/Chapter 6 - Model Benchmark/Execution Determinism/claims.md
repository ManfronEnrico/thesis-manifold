---
name: ch6-execution-determinism-claims
description: Unverified mechanism claim in Ch6 §6.3.3 execution-protocol prose. The effect is measured in-project; only the explanation lacks a source.
chapter: 6
section: "6.3.3 Execution protocol"
topic: Execution Determinism
prose_source: writing-notes/srq1-holiday-enrichment-result-and-limitations.md §2.4
created: 2026_09_07-15_10
updated: 2026_09_07-15_10
---

# Ch6 §6.3.3 — Execution determinism: claim to verify

**Read the split before answering — it is unusual.**

| Part | Status |
|---|---|
| **The effect** | **MEASURED IN-PROJECT AND REPRODUCIBLE.** Needs no citation. |
| **The mechanism** | **UNSOURCED.** Claude's explanation from general knowledge. |

---

## CV-04 — Why XGBoost is not reproducible across thread counts

### The measured effect (safe, needs no source)

Holding seed, data and every hyperparameter constant, varying **only** thread count
(danskvand brand×month, seed 42):

| n_jobs | Test WMAPE |
|---|---|
| 1 | 34.648708 (repeatable across runs) |
| 2 | 34.946778 |
| 4 | 35.397904 |
| 8 | 37.297544 |

A 2.65 pp spread. Reproducible on demand in this repository.

### The unsourced explanation

> "XGBoost histogram building sums gradient statistics per thread and reduces them in
> completion order. Floating-point addition is not associative, so a different thread
> count produces a different sum, a different split, and a different tree."

**Appears in prose as (safe wording, currently used):**
> "...the seed governs which observations and features are sampled, not the order in
> which partial results computed on separate threads are combined."

This describes an *ordering* effect without asserting the internal mechanism, which is
why it is safe as written.

**To determine:**
1. Does XGBoost documentation address determinism and thread count?
2. Is parallel float-reduction order the documented cause, or is something else
   responsible (thread-dependent sketching, histogram binning)?
3. Is there a documented determinism guarantee other than single-threading?

**Why it matters:** the thesis reports this as a methods finding. Reporting a *measured*
effect is safe; asserting an unverified *cause* is not. The fix is one hedged clause, so
this is cheap to get right.

**If unverifiable:** keep the current wording. The finding stands on the measurement.

---

## Notebook routing

**Notebook B (factual).** Place XGBoost documentation on determinism / `n_jobs` /
`nthread` in `../../Candidate Sources/`.

A "No Source Found" verdict here does **not** weaken the finding — only the explanation.
