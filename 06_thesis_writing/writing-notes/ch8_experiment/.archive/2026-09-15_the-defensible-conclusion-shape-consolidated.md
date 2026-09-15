---
name: the-defensible-conclusion-shape
description: REFERENCE - The conclusion the SRQ4 evidence can carry ("dedicated models trade accuracy for auditability and cost at this data scale"), why it is stronger than a clean win, what would falsify it, and how it reconciles with the opposite result recorded in August.
category: reference
applies-to: [ch8-evaluation, ch9-discussion, ch10-conclusion]
triggers: [writing the SRQ4 conclusion, interpreting B vs C, deciding what the experiment proves, defending the artefact when an arm beats it]
created: 2026_09_11-22_40
updated: 2026_09_11-22_40
---

# The conclusion shape the evidence can actually carry

**Status: NOT YET SUPPORTED. Do not write this into prose.** One brand, one month,
one repeat per arm. This note records the SHAPE to build toward and what has to be
true before it can be claimed.

---

## The sentence

> **Dedicated models trade accuracy for auditability and cost at this data scale.**

## Why this is stronger than a clean win

A thesis claiming the artefact wins everywhere is falsified by one counterexample, and
the pilot already contains one. This sentence **names the operating regime** in which
the architecture is the right choice instead of asserting universal superiority. Three
properties make it the better claim:

- **It survives the result that threatens the obvious version.** An arm beating the
  dedicated model on accuracy is evidence FOR this sentence, not against it -- the
  trade is the finding.
- **It is falsifiable.** If the funded set shows the dedicated model also wins on
  accuracy, the sentence is wrong and a stronger one replaces it. If cost and latency
  converge, it is wrong in the other direction. Both are measurable.
- **It is decision-useful.** A practitioner can act on "at this data scale", which the
  thesis quantifies: 39 months, 95 brands, one category-tuned model per category.

"At this data scale" is the load-bearing clause. **It must be stated with the numbers
attached every time the claim is made**, or it degrades into the universal claim the
evidence cannot support.

---

## What the pilot shows, and what it does not

Seven-arm smoke, 2026-09-11, CSD/HARBOE, target 2026-03, actual 6,365,900.

| | dedicated model (C) | code-as-action (B) |
|---|---|---|
| APE | 21.9% | 5.2% |
| latency | 6.7 s | 91.3 s |
| cost per answer | $0.009 | $0.224 |
| auditability | one tool-call span, args verified | 15 opaque code blocks |
| reproducibility | same input -> same number | re-derives its models each run |

**Interpretable now** (mechanism, not magnitude -- these do not depend on sample size):

- The cost and latency gap is two orders of magnitude and will not reverse.
- C and E return identical numbers to the decimal across runs; B and D do not.
- F and G both OVERRODE the model, citing its own confidence tier and interval as the
  reason. The typed payload carried decision-relevant information rather than a bare
  number, which is a result for SRQ2 independent of accuracy.

**NOT interpretable yet:** the accuracy ordering. Scenario A moved 38.7% -> 23.0% and B
1.0% -> 5.2% between two runs on identical prompts. **The within-arm spread is
comparable to the between-arm gaps.** Any ranking read off the pilot is noise.

---

## The restatement that keeps it honest

> **A model fitted to ONE SERIES beat a model fitted to A CATEGORY.**

Not "code beats models". Scenario B fitted roughly eighty models to HARBOE's own 39
months -- exponential smoothing, a 72-model SARIMA grid, OLS and Ridge in linear and log
space, backtested at two earlier cutoffs -- and took the median. Scenario C serves all 95
CSD brands from one configuration tuned once for the category.

That is **per-series adaptation plus ensembling**, and both are genuine advantages of the
code-as-action approach rather than artefacts. Neither is evidence that the dedicated-model
architecture is unnecessary. See P0049 F53 for the four competing explanations and how
each is separated by measurement.

---

## Reconciling with the August note -- READ THIS BEFORE WRITING

`srq4-first-results-and-interpretation.md` (2026-08-19) records the **opposite ordering**:
C at 13.8% APE beating B at 17.3%, on the same brand. The September pilot has B ahead.

**Do not quietly drop either.** Two runs of the same comparison disagreeing about the
direction is itself the strongest available evidence that **n=1 settles nothing**, and it
is the honest justification for the funded set. The August note's headline is superseded
as a *result*; its reasoning about ladder increments and structural token cost stands.

If the funded set lands and the ordering is stable, say which way and by how much. If it
is not stable, that is a reportable finding about the variance of LLM forecasting, not a
failure of the experiment.

---

## Why this does not undermine the artefact

Ch6 section 6.4 justifies the structured tool interface on **reliability, reproducibility
and auditability** -- never on accuracy. The pilot is consistent with that justification
as written. The thesis does not need the dedicated model to be more accurate; it needs the
trade to be real, measured, and named.

## What must be true before this is written as prose

| Gate | Status |
|---|---|
| The funded set has run | NOT DONE |
| Within-arm spread reported alongside every between-arm gap | method agreed, not yet applied |
| The four F53 explanations addressed or declared unresolved | NOT DONE |
| "At this data scale" quantified wherever the claim appears | drafting rule, apply at write time |
