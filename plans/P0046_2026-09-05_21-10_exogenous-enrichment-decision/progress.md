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

## Session 1 (cont.) — 2026-09-05, Brian's corrections

Brian corrected two findings and settled the decision gate. **Both corrections weaken the
case against enrichment; neither was a point he had to concede.**

### F1 was wrong and is rewritten

I wrote that the project "already ran this experiment informally and got a negative
answer". It did not. The 2026-08-18 change was a **rename of a mislabelled feature** —
`holiday_month(s)` was computing peak months and consulting no calendar. That is evidence
the old feature was fake, not evidence a real calendar adds nothing.

> Brian: *"this was only because the old holiday_months was underlying actually just peak
> months -> thus the rename. But I am talking about including an ACTUAL holiday month api
> enrichment, something which was not done back then."*

Correct. A derived peak-month rule and an external calendar are different inputs. **No
prior art exists**, so the delta is unknown rather than predictable — which strengthens
rather than weakens the case for measuring it.

### F2 was overreaching and is narrowed

The Prophet consistency argument holds for holiday *windows* (a span of days around a date,
genuinely inexpressible at monthly grain). It does not extend to a monthly holiday count or
a trading-day count, which are constructible and were never tested. Trading-day count in
particular is **not** a re-encoding of month-of-year: it varies year to year for the same
month, which a month dummy cannot carry.

Going into `writing-notes/` as task 9, so the thesis does not argue the overreaching
version in prose.

### Decision: Option C, and it runs BEFORE the experiments finish

> Brian: *"exactly thats why I want to do it before we finish the experiments"*

The funded-run deadline is the reason to do it now, not a constraint to schedule around.
Enrichment is therefore **upstream of P0042 blocks 1-3**, not parallel to them. Task 3 is
closed as decided; task 2 now only confirms the retrain fits before the runs, with Option A
as the fallback if it does not.

### Next session starts here

1. **Task 2** — size the build honestly (calendar source, feature, retrain, re-benchmark,
   table/figure regeneration) and check it against the P0042 schedule.
2. **Task 5** — add the feature behind a flag defaulting off. At monthly grain build
   *both* candidate forms: public-holiday-day count, and trading-day count. They are
   different constructs and only the second is orthogonal to month-of-year.
3. **Task 6** — benchmark with and without across all four categories; report the
   per-category delta whatever it is. Compare SHAP between runs to check the feature is not
   merely re-encoding `month`/`peak_month`.
4. **Task 9** — the writing-notes entry, which can be done any time and is independent.

Open question worth deciding early in task 2: **school holidays** move with public holidays
and plausibly matter more for beverage demand than public holidays alone. In or out of
scope? Cheap to add while the feature is being built, expensive to add afterwards.
