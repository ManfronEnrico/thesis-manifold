---
pid: P0046
created: 2026-09-05 21:10:00
updated: 2026-09-05 21:10:00
---

# Progress — P0046

## Session 1 — 2026-09-05 21:10 (plan creation)

Split out of P0043 because the enrichment objection is not closable by editing prose.

### Done
- Collected the five Word threads that raise it (ch1 15/18/20, ch2 66/69, ch3 127,
  ch4 177, ch5 207) with their anchors.
- Read the live feature set in `engineer_features.py` and recorded what is genuinely
  exogenous today (F3).
- **Found the decisive prior art (F1)**: the pipeline had a `holiday_month(s)` feature and
  removed it on 2026-08-18, renaming it `peak_months`, because it consulted no calendar and
  the measured seasonality contradicted a holiday story — CSD peaks at quarter-ends,
  danskvand in summer, energidrikke has no December peak, and January is the weakest CSD
  month at -26.6%.
- Recorded the grain argument (F2), including that the thesis **already** uses "monthly data
  does not support holiday windows" to explain Prophet's weakness — so claiming a holiday
  calendar helps the monthly models would contradict an argument already in the text.

### Not done — deliberately
No code was written and no feature was added. Task 3 is a decision gate for Brian; building
first would prejudge it, and the funded-run deadline means the wrong choice is expensive.

### Next
Task 2 — size Option C honestly (hours to feature, retrain, re-benchmark, regenerate), so
the gate is a decision about schedule rather than about intuition.
