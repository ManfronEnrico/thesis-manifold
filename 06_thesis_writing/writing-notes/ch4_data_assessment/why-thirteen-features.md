---
name: why-thirteen-features
description: NOTE - Why the models train on 13 columns of a 54-column matrix. The justification exists, is measured, and is already in appendix-ready tables. Answers the "55 to 13 with no justification" concern.
snapshot: 2026-09-08_18-04_ch4-second-verification
category: reference
applies-to: [chapter 4, chapter 5, feature engineering]
created: 2026_09_08-19_40
updated: 2026_09_08-20_10
status: ready
---

# Why thirteen features

**There was never a 55-to-13 reduction.** The two numbers count different
things, and reading them as a before-and-after is what makes the pipeline look
unjustified. Every exclusion is documented and most are measured.

---

## The 54 columns, decomposed

Counted from `csd_feature_matrix_h3.parquet` on 2026-09-08:

| Role | n | Why it is not an input |
|---|---:|---|
| Identifiers, dates, split label | 6 | not measurements |
| Targets (`sales_units`, `log_sales_units`) | 2 | the thing being predicted |
| **Trained on** | **13** | — |
| Holiday columns | 3 | **to be added to the trained set** - see Cause 3 |
| Excluded Nielsen measures | 30 | contemporaneous, see below |

So the matrix is **6 bookkeeping + 2 targets + 46 candidate measures**, of which
13 are used. The interesting number is 46 to 13, not 55 to 13, and the gap has
three separate causes rather than one unexplained decision.

---

## Cause 1 - thirty columns are contemporaneous with the target

This is the whole of the eligibility rule, and it disqualifies the largest group
by far.

A column is admissible only if its value is known when the forecast is issued. A
Nielsen measure recorded *for the month being predicted* cannot inform a
prediction of it. Measured against same-month sales units:

| Excluded column | correlation with same-month sales |
|---|---:|
| `baseline_sales_in_liters` | 0.97 |
| `baseline_sales_units` | 0.96 |
| `sales_liters` | 0.95 |
| `promo_units` | 0.94 |
| `sales_units_any_tpr` | 0.93 |
| `sales_value` | 0.90 |

Twelve of the thirty exceed 0.50. Admitting `sales_value` would produce a model
reporting near-perfect accuracy while forecasting nothing - it is the same
month's sales in different units.

**This is not a judgement call and needs no empirical defence.** It is the
definition of a forecast. The columns stay in the matrix because they describe
the data and belong in a data assessment; they are simply not inputs.

---

## Cause 2 - `weighted_dist` was tested and rejected on measured evidence

This is the one exclusion that *is* a judgement call, and it is the best
documented decision in the codebase. From the comment block above `FEATURES` in
`srq1_benchmark.py`:

> "weighted_dist is deliberately ABSENT from this list (P0036 task 7,
> 2026-08-19). Not because it leaks -- it was tested and cleared."

It is never lagged, so it was a candidate. It is also structural and barely
moves: `corr(wd[t], wd[t-1]) = 0.976`, `corr(wd[t], wd[t+3]) = 0.946`, median
month-on-month change 0.00114 on a 0-1 scale. Month *t*'s value is a sound proxy
for *t+3* because it essentially **is** *t+3*'s value.

It was excluded because it does not help. Fitted with and without, LightGBM, 300
trees, three seeds, deterministic:

| Category | without | with | lagged |
|---|---:|---:|---:|
| CSD | 17.20% | 18.24% | 18.32% |
| Danskvand | 33.39% | 34.36% | 32.89% |
| Energidrikke | 17.40% | 16.94% | 16.86% |
| RTD | 31.83% | 32.54% | 31.26% |

Worse in three of four categories. The comment states the reasoning plainly:
carrying an unlagged contemporaneous measure that does not help means defending
*"why does your feature read the month it predicts?"* for no measured benefit.

---

## Cause 3 - the holiday columns: SUPERSEDED 2026-09-08

> ⚠ **This section's reasoning was overturned by a scope decision on 2026-09-08.**
> It is kept because the VIF fact in it is still true and still constrains the design.

**What this note originally said:** the holiday columns sit outside `FEATURES` so the
ablation has something to measure against.

**Why that is now wrong.** The thesis proposition is *whether trained models help an LLM
forecast* - not whether exogenous variables improve models. Feature contribution is not an
SRQ. Reporting a holiday ablation invites assessment against a claim the thesis does not
make, and spends space SRQ4 needs.

M4 and M5 identify explanatory (exogenous) variables as the open frontier in forecasting
practice. That motivates the **direction**; it is **not** a prescription for holiday
calendars, which neither competition specifies for this setting. The holiday calendar is
*one instance* of that direction, chosen because it was constructible at monthly grain from
a free source.

The holiday features therefore belong in the feature set *by design*, as a stated choice
consistent with the cited direction - not because the literature prescribed them, and not
on the strength of an internal ablation.

⚠ **Do not write that M4/M5 prescribe holiday enrichment.** The archived note
`.archive/2026-09-08_exogenous-enrichment-and-the-holiday-question-folded-in.md` sets the
exact boundary: the M4/M5 quotation may stay, but only at the scale the thesis actually
reached - **one calendar source, monthly grain**.

**The VIF constraint survives and still binds.** `non_holiday_days = days_in_month -
n_holidays` by construction, so the three are exactly linearly dependent and Table 97
reports their VIF as `inf` in all four categories. Including all three in a *linear* model
gives a singular design matrix. So the enriched set is **`FEATURES` + two of the three**
(`days_in_month` and `n_holidays`, dropping the derived `non_holiday_days`), not all three.
Trees tolerate the dependency; Ridge does not, and the benchmark fits both.

**Consequence for the write-up:** the holiday calendar is described as part of the feature
set on literature grounds, and the ablation is not a reported result.

---

## And the reduction that was tried anyway

The obvious follow-up question - *"you kept thirteen correlated features, why not
fewer?"* - was tested and answered. Table 98:

| Category | features available | after reduction | clusters |
|---|---:|---:|---:|
| CSD | 16 | 9 | 2 |
| danskvand | 15 | 8 | 2 |
| energidrikke | 16 | 9 | 2 |
| RTD | 15 | 9 | 2 |

Grouping at pairwise absolute Spearman >= 0.95 and keeping the highest
permutation-importance member of each group. **Rejected: mean test WMAPE rose
from 26.44 to 28.82.**

The reasoning is worth keeping because it is a real methodological point:
collinearity is a pathology of *linear* estimation. Ridge cannot apportion credit
between correlated predictors, but a gradient-boosted tree splits on whichever
correlated feature is locally most informative and loses genuine information when
the others are removed. The lag features are correlated by construction - each is
computed from the same series - and Table 97 confirms it, with
`rolling_mean_4` at VIF 212-256 across categories.

**A reduction rule adopted without validation would have degraded every reported
number while appearing rigorous.** That is the contribution of the negative
result.

---

## So the write-up is straightforward

Four sentences carry it, and each has a table behind it:

1. A column is an input only if its value is known when the forecast is issued;
   thirty Nielsen measures are contemporaneous with the target and are retained
   for description rather than fitting.
2. `weighted_dist` is time-safe but was excluded because fitting with and
   without it made accuracy worse in three of four categories.
3. The holiday calendar is adopted as part of the feature set as a design choice,
   consistent with the exogenous-variable direction M4 and M5 identify, rather than
   evaluated as an ablation; of its three columns only two are independent, since the
   third is their difference.
4. A redundancy-based reduction from sixteen features to nine was tested and
   rejected: it raised mean test error from 26.4 to 28.8 per cent.

**The evidence is already appendix-ready.** Tables 94-98 in
`05_thesis_results/05_model_benchmark/tables/` are numbered, captioned and carry
their own INTERNAL REVIEW separators. Nothing needs generating.

---

## Note - what is genuinely missing

Two things, and neither is the justification itself.

**The chapter never states the rule.** All of the above lives in code comments
and result tables. Section 4.3's admissibility paragraph states the principle but
does not connect it to a count, so a reader sees thirteen inputs from a
fifty-four-column matrix and has nowhere to go. **This is a writing gap, not a
methodology gap** - which is the good version of the problem.

**The 0.95 grouping threshold has no source.** Table 98's own review note flags
it: *"a reporting parameter with no cited source -- register item 2. Either
justify it by sensitivity analysis or describe it as an arbitrary choice."* The
prose in the consolidated pass avoids naming the number for exactly this reason.
The same applies to the VIF bands of 5 and 10 if they are ever quoted.

---

## Note - on reporting the pipeline as it currently stands

Your instinct to paste the corrected sections even while the EDA is under review
is the right one, and it is worth saying why rather than treating it as a
compromise.

Everything in the consolidated note is measured against the artefacts that
produced the results the thesis reports. If the EDA overhaul changes which
features are eligible, the *numbers* in these sections change - but the
*structure* does not: there will still be a rule, still an excluded set, still a
tested-and-rejected reduction. Replacing stale text that describes a pipeline
which no longer exists strictly improves the document, and it does so in a way
that survives the overhaul.

The alternative - leaving sections that describe a >=30-month filter and a
fixed-date split that were removed months ago - is worse on every axis.

⚠ **The one thing to hold back** is any sentence claiming the feature set is
*justified by the EDA diagnostics*. That claim is what your other session is
investigating, and it is the one place where the evidence may not survive.
Everything above rests on benchmark measurements, not on EDA recommendations.
