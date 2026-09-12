---
name: srq4-data-input-is-a-constructed-choice
description: NOTE - SHORT pointer. The data handed to the SRQ4 scenarios is a constructed experimental choice, not a property of the dataset, so the methodology chapter states the boundary in three sentences and refers to chapter 8 for the full construction.
category: reference
applies-to: [ch3_methodology, ch8_experiment]
triggers: [methodology, what data did the scenarios get, experimental design, data boundary]
created: 2026_09_12-20_15
updated: 2026_09_12-20_15
status: bullets, not prose - SHORT BY DESIGN
---

# The SRQ4 data input is a constructed choice

> **This note is deliberately short.** The full construction, the three
> declared human choices and the figures live in
> [[the-agent-input-contract]] (chapter 8). Chapter 3 states the boundary and
> points there.

**Why it is not a data-assessment topic.** At the point the thesis assesses the
data, the work is training models. The payload handed to the scenarios is
constructed **later**, during the experiment phase, and it is an instrument of
that experiment rather than a property of the dataset. Describing it in the
data chapter would imply the dataset arrived in that shape. It did not — the
frame did not exist on disk until it was built for this purpose.

---

## What the methodology chapter needs to say

Three sentences, no more:

1. The scenarios receive the brand-month series **as it comes out of the
   warehouse after joining and aggregating** — and nothing further.
2. Cleaning, imputation and feature engineering are **withheld deliberately**,
   because they are the pipeline under evaluation; supplying them would mean
   measuring nothing.
3. The held-out window is **cut from the file at generation time**, so the
   input a scenario receives cannot contain the month it is asked to forecast.

Then cite the experiment chapter for the construction, the three declared
choices (market, SKU-to-brand aggregation, sum-versus-mean) and the figures.

---

## The one thing chapter 3 should NOT delegate

**The leakage boundary.** A methodology chapter that does not state how the
held-out period was protected invites the question immediately. Say it plainly:
the visible window is train plus validation, ending at the same origin the
model is fitted to, and the cut is applied when the file is written rather than
when it is read — so no downstream consumer can reintroduce the leak. It is
independently re-asserted on every run.

---

## Related

- [[the-agent-input-contract]] — the full version; keep the two in step
- [[prompt-consistency-as-an-experimental-control]] — the other constructed
  instrument, and for the same reason it belongs in 6/7/8 rather than here
- [[verification-of-the-experimental-harness]] — the existing chapter 3 note on
  how the harness is checked
