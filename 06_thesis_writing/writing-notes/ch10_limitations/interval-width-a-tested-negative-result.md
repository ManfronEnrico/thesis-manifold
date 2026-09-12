---
name: interval-width-a-tested-negative-result
description: REFERENCE - The intervals attain coverage and are very wide. Three alternative calibration schemes were implemented and measured; none improved coverage and width together in more than two of four categories. A sample-size limit, not a defect, and a contribution rather than an apology.
category: reference
applies-to: [ch10-limitations, ch7-tool-interface, ch5-model-benchmark]
triggers: [writing the interval limitation, answering why the intervals are so wide, defending the conformal choice, proposing to fix calibration]
created: 2026_09_11-21_10
updated: 2026_09_11-21_10
---

# The intervals are wide, and that was tested rather than accepted

**Routed here from the experiment session (P0049 F50, F52).** It had no chapter
note, and it is the strongest limitation the thesis can state, because it comes
with measurements of what was tried.

---

# The finding in one line

> The split conformal interval attains its marginal coverage guarantee and is
> nonetheless uninformative for an individual brand, and three alternative schemes
> were implemented and measured before that was accepted.

---

# What was tried, and what happened

**A scheme counts as a win only if coverage stays within five points of the 90 per
cent target *and* width falls.** Narrowing by undercovering is not an
improvement; it is the guarantee being given up quietly.

| Category | Scheme | Coverage | Median width |
|---|---|---|---|
| CSD | pooled, as shipped | 92.5% | 7.9x |
| CSD | two-bucket by size | 91.6% | **3.2x** — win |
| CSD | volatility-scaled | 86.5% | 3.0x — win |
| Danskvand | pooled, as shipped | 85.1% | 15.2x |
| Danskvand | two-bucket by size | 79.9% | 3.7x — **undercovers** |
| Danskvand | volatility-scaled | 88.5% | **5.9x** — win |
| Energidrikke | pooled, as shipped | 88.6% | 18.2x |
| Energidrikke | two-bucket by size | 79.9% | 6.4x — **undercovers** |
| Energidrikke | volatility-scaled | 82.1% | 12.4x — **undercovers** |

**No scheme wins in more than two of four categories.** The one that helps most
on one category undercovers on the next, which is the signature of a
sample-size limit rather than a modelling choice.

---

# Why the obvious fix does not work

The intuitive repair is to calibrate large brands separately from small ones,
since pooling one quantile over brands spanning six orders of magnitude is what
makes the band wide. **It fails on row counts.**

| Category | Brands over 1M units/month | Calibration rows in that bucket |
|---|---|---|
| CSD | 4 | 28 |
| Danskvand | 1 | 6 |
| Energidrikke | 3 | 18 |
| RTD | **0** | **0** |

A 90th percentile estimated from 28 rows is not a 90th percentile. With a
minimum-row guard in place, **every large bucket falls back to the pooled
quantile on exactly the brands the scheme was meant to fix**, so the fix reduces
to the thing it was replacing.

⚠ **One category has no brands above the threshold at all**, which means the
scheme is not merely weak there but undefined.

---

# The correction worth recording

An earlier version of this investigation reported that bucketing gave one brand a
band of ±1.35x instead of ±7.59x, and proposed adopting it. **That figure came
from 28 validation rows covering four brands and did not survive an honest test
on the held-out split.**

⚠ **The pattern is worth one sentence in the limitations chapter**: a promising
improvement measured on the data that motivated it, which disappeared when
measured properly. That is exactly the failure mode the train/validation/test
discipline exists to prevent, and catching it is evidence the discipline was
applied rather than described.

---

# What this is, precisely

**A sample-size limit of the reduced dataset, not a defect and not fixable by
retraining.** Two independent causes:

- One quantile is pooled across brands spanning **six orders of magnitude** of
  volume.
- Each brand contributes only a handful of validation months, so a per-brand
  quantile cannot be estimated at all.

⚠ **Retraining does not touch this.** The interval is computed from residual
quantiles, not from model weights. Changing how residuals are summarised leaves
both fitted models untouched, which is also why the alternatives could be
evaluated locally in minutes rather than on a cluster.

---

# How to write it

**As a contribution, not an apology.** The sequence is:

1. The guarantee holds — coverage is attained across all four categories.
2. The width is nonetheless large enough that the interval is uninformative for
   a single brand, and the thesis says so plainly.
3. **Three alternatives were implemented and measured**, and the table above is
   the evidence.
4. The cause is the panel's shape, which the thesis cannot change.

⚠ **Step 3 is what makes this a contribution.** Without it the limitation reads
as something noticed and endured. With it, the thesis has tested the obvious
remedies and reports why they fail, which is more useful to a practitioner than a
narrow band would have been.

⚠ **It is also the honest answer to the question a reader will ask on seeing the
interval in a results table**, which they will.

---

# What the interface does about it

Nothing, deliberately, and that is defensible. The interval is reported as
measured rather than narrowed to look useful. A consumer of the payload can act
on a wide interval — and in the pilot, two agents did exactly that, weighing the
model's forecast rather than adopting it and citing the width as their reason.

See `ch7_synthesis/ch7-verification-pass.md (Part 3)`. **A wide interval that is
honestly reported and correctly consumed is a better outcome than a narrow one
that undercovers.**

---

# Related

- `ch7_synthesis/ch7-verification-pass.md (Part 2)` — the sibling defect in the
  confidence tier, which is not recoverable the way this is explainable
- `ch7_synthesis/ch7-verification-pass.md (Part 3)` — the width being consumed
- `anticipated-assessor-questions.md` — Q2.3
- P0049 `findings.md` F50 and F52, and
  `2026-09-11_eval_calibration_schemes.py` in the same folder — the script that
  produced the table
