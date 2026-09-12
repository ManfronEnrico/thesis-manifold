---
name: ad-hoc-data-science-vs-a-trained-pipeline
description: NOTE - The framing that turns SRQ4 from an accuracy contest into a question about what a data scientist is paid for. Every agent session re-derives an approach from scratch; a trained pipeline is derived once and deployed. Bullets for the discussion and conclusion chapters.
category: reference
applies-to: [ch9_discussion, ch10_limitations, ch8_experiment]
triggers: [discussion chapter, conclusion, what the experiment means, non-determinism, cost of forecasting]
created: 2026_09_12-19_30
updated: 2026_09_12-19_30
status: bullets, not prose
---

# Ad-hoc data science versus a trained pipeline

**Source.** Brian, 2026-09-12, while deciding what data the scenarios should
receive. Recorded because it reframes the whole experiment and is currently
nowhere in the thesis text.

**Status.** Bullets. Not prose, and not yet placed against a snapshot anchor.

---

## The framing, in one paragraph

The thesis reads as though it asks which forecasting approach is more accurate.
That is the measurement, but it is not the question. The question is **what a
data scientist is actually paid for**, and whether a language agent can supply
it on demand.

A trained pipeline is the product of work done **once**: exploratory analysis,
cleaning decisions, feature construction, model selection, hyperparameter
tuning, calibration. That work is expensive and slow. Its output is an artefact
that can then be deployed indefinitely and which returns **the same answer for
the same input, every time**.

An agent handed the same data does that work **again, from scratch, in every
session** -- and a different version of it each time. So the comparison is not
model versus model. It is *an artefact produced once and reused* against *a
process re-enacted per request*.

---

## The four questions this framing generates

Each maps onto something the harness already measures, which is why the framing
is worth adopting rather than merely interesting.

| Question | What answers it |
|---|---|
| How **well** can an agent do the data science job on demand? | APE / WMAPE per arm, and the failure classification |
| How **long** does it take? | per-run latency, already logged |
| How **non-deterministic** is it? | within-arm spread across repeats at a fixed prompt |
| What does it **cost**? | per-run USD, already logged and reconciled |

The third is the one the thesis is currently weakest on and the one this
framing makes load-bearing. Measured on the 2026-09-11 smoke: **Scenario A
moved 15 percentage points between two runs on a byte-identical prompt.**
Under an accuracy framing that is noise to be apologised for. Under this
framing it is a **finding about deployability**.

---

## Why non-determinism is a result, not a limitation

- A category planner who asks the same question twice and receives two
  materially different forecasts cannot build a process on it.
- The trained model returns the same number for the same input, and its
  interval is calibrated by construction (split conformal). Reproducibility is
  not a nice property here; it is what makes the output *auditable*, which is
  the SRQ2 contribution.
- So run-to-run variance is not measurement error obscuring the comparison. It
  **is** one of the dimensions being compared, and it runs in the trained
  model's favour independently of which is more accurate on the day.
- This reframes a weak accuracy result as a partial answer rather than a null
  one: even where an agent matches the model on average, matching *on average*
  while varying per run is a different product.

**Careful with this claim.** At n=3 repeats we can report the spread we
observed; we cannot claim a precise variance. Say "in this sample", and put
the sample size in the same sentence.

---

## What the experiment can and cannot say about the EDA

- The agents are handed the data **post-join and post-aggregation, pre
  cleaning and pre feature engineering** (see the ch8 note on the input
  contract). So they must do the EDA, the cleaning and the feature
  construction themselves, in-session.
- That is deliberate: the EDA and feature engineering are the proprietary
  pipeline, and giving them away would mean measuring nothing.
- The three brands differ sharply in data quality, which is what makes this
  measurable rather than rhetorical:

| Brand | Columns with nulls | Worst column |
|---|---|---|
| HARBOE | 3 | 2.6% null |
| 7-UP | 3 | 41.0% null |
| ØRBÆK | 7 | 100% null (three columns entirely empty) |

- Sparsity is **preserved, never zero-filled**. A zero asserts "measured, and
  it was zero", which the warehouse does not say. Handling that is precisely
  the judgement a data scientist is paid for, so filling it in would be doing
  the agent's job for it.
- Whether an agent notices that three of ØRBÆK's columns are entirely empty, and
  what it does about it, is observable in the traces.

---

## Where this lands in the thesis

- **Discussion.** As the interpretive frame for the results, placed before the
  arm-by-arm reading rather than after it.
- **Conclusion.** As the answer to "so what": the contribution is not a more
  accurate forecast, it is a *reproducible* one at a *known* cost with an
  *auditable* provenance.
- **Limitations.** The honest counterweight -- three brands, one category,
  three repeats. We observe direction, not effect size.

---

## Draft sentences to work from

Not prose for insertion. Raw material, to be rewritten in the chapter's voice.

- "The comparison is not between two forecasts. It is between an artefact
  produced once and a process re-enacted on every request."
- "A forecast that is correct on average but different every time is a
  different product from one that is correct on average and the same every
  time."
- "Each session reconstructs an approach from scratch; nothing carries over,
  and nothing accumulates."
- "The pipeline's cost is paid once, in advance, and is visible. The agent's
  cost is paid per question, and is visible only in aggregate."

---

## Related

- [[the-defensible-conclusion-shape]] -- the accuracy-versus-auditability
  claim this sits behind
- [[brand-sampling-and-inclusion-criteria]] -- why these three brands
- `plans/P0049_.../findings.md` -- the measured within-arm spread
