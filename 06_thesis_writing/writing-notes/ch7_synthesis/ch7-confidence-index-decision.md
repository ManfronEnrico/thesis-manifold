---
name: ch7-confidence-index-decision
description: NOTE - The confidence index the forecast tool returns is mathematically degenerate and must be removed or rebuilt before Chapter 7 describes the payload. Carries the diagnosis, the measured values, and the recommended wording.
category: workflow
applies-to: [chapter 7]
created: 2026_09_11-16_30
updated: 2026_09_11-16_30
status: open
---

# The confidence index, and the one sentence Chapter 7 gets wrong

**Raised by Enrico 2026-09-11. Diagnosed and measured the same day.** This is an
SRQ2 decision, which is why it sits in Chapter 7's folder rather than Chapter 5's
- Chapter 5 never uses the index and is unaffected.

Tracked as **S18** on the deferred structural list.

> ⚠ **Read this first: Chapter 7 already covers the defect, and covers it well.**
> Section 7.4 states that the index is constant within a category, that the
> quantile exceeds unity in all four categories, that this zeroes the second term
> by construction, that values run three to seven against a threshold of forty,
> and that "the index distinguishes nothing". **That is the finding, already
> written, and nothing below asks you to rewrite it.**
>
> **One sentence in it is wrong**, and it is the sentence immediately after. See
> *The one correction Chapter 7 needs* below. Everything else in this note is
> supporting evidence for text that already exists.

---

# The one correction Chapter 7 needs

Section 7.4, the paragraph beginning *"That is a property of the weights and the
cut-offs rather than of the forecasts"*:

> "That is a property of the weights and the cut-offs rather than of the
> forecasts, and **it could be repaired by recalibrating the bands against the
> widths actually observed.**"

⚠ **It could not.** Recalibrating the bands cannot repair it, and the reason is
in the chapter's own preceding sentence: the index is *constant within a
category*. Re-tiering a quantity that takes exactly four values - one per
category - assigns every brand in a category the same band. **The band would
simply be the category name**, which is not a confidence signal.

The chapter is also slightly too generous in calling it "a property of the
weights and the cut-offs". The weights are not the problem: **no choice of
weights repairs it either**, because both terms are functions of the same
per-category quantile. It is a property of the *construction*.

### Paste - replace that sentence

> That is a property of the construction rather than of the forecasts, and it is
> not repairable by choosing different weights or different band boundaries:
> both terms are functions of a quantile that is fixed within a category, so any
> reweighting or re-thresholding of them yields one value per category and
> assigns every brand in that category the same band. Reported as it stands,
> however, it settles a question this chapter has been carrying: the claim about
> how far a forecast may be relied upon is carried by the measured track record
> travelling in the same payload, and not by the index.

### Note - why this matters beyond accuracy

The current wording offers a repair that does not exist. **An examiner who takes
it at face value will ask why it was not done**, and the honest answer is that it
would not have worked. Saying so converts an apparent oversight into a
diagnosis, which is the stronger position and costs one sentence.

## What the field is

`forecast_tool.py:473` returns a `confidence` score from 0 to 100, tiered
High / Medium / Low at cut-offs of 70 and 40:

```python
rel  = (hi - lo) / yhat
conf = 100 * (0.5 * (1 / (1 + rel)) + 0.5 * (1 - min(q90, 1)))
```

## What it actually returns

Measured from the four served models' own metadata, 2026-09-11:

| Category | Served model | q90_log | rel. width | term 1 | term 2 | **conf** | tier |
|---|---|---|---|---|---|---|---|
| CSD | XGBoost | 2.027 | 7.46 | 5.91 | **0.00** | **5.9** | Low |
| danskvand | XGBoost | 2.040 | 7.56 | 5.84 | **0.00** | **5.8** | Low |
| energidrikke | LightGBM | 2.691 | 14.69 | 3.19 | **0.00** | **3.2** | Low |
| RTD | LightGBM | 1.890 | 6.47 | 6.69 | **0.00** | **6.7** | Low |

**Four possible values across the entire product range**, one per category, all
tiering Low. Enrico observed 3 to 7 out of 100 on every forecast; that is exactly
these four numbers.

---

# Why it is broken - the part worth understanding

**This is not a data problem and not a tuning problem. It is an algebra problem
in the formula, plus a units problem in the threshold.** Two independent defects,
either of which alone would flatten the score.

## Defect 1: the forecast cancels out of the width

The interval is built multiplicatively, in log space:

```
lo = expm1(log(y) - q90)        hi = expm1(log(y) + q90)
```

So `hi - lo` is proportional to `y`, and dividing by `y` cancels it:

> **rel = (hi − lo) / y ≈ e^q90 − e^−q90 = 2·sinh(q90)**

The forecast value disappears. Since **q90 is a single number per category** -
one conformal quantile, calibrated once on that category's validation residuals -
`rel` is a **per-category constant**. It cannot distinguish a well-predicted
brand from a badly-predicted one, because nothing brand-specific enters it.

⚠ **This is a property of the design, not of our data.** Any multiplicative
interval with a shared quantile would behave identically. A relative width is
the right instinct; it just carries no information once the interval is
proportional to the forecast.

## Defect 2: the second term is off by a unit

`1 - min(q90, 1)` treats `q90` as though it lived on a 0-to-1 scale. **It does
not.** It is a residual quantile in **log space**, so it is a multiplicative
half-width, and it reaches 1.0 as soon as the 90 per cent band is wider than
roughly x0.37 to x2.7.

| q90_log | the 90% band it implies | term 2 |
|---|---|---|
| 0.25 | x0.78 to x1.28 | 0.75 |
| 0.50 | x0.61 to x1.65 | 0.50 |
| **1.00** | **x0.37 to x2.72** | **0.00** |
| 1.89 (RTD) | x0.15 to x6.6 | 0.00 |
| 2.69 (energidrikke) | x0.07 to x14.7 | 0.00 |

**Every real category sits at 1.9 to 2.7**, so the term is zero everywhere and
half the index is dead. It would only become non-zero if a category's 90 per cent
interval were tighter than about a factor of 2.7 either way.

## So what did we do wrong?

**Three things, in order of how much they matter.**

1. **The formula was never checked against the range its inputs actually take.**
   `min(q90, 1)` encodes an assumption that q90 is a probability-like quantity
   bounded near 1. It is a log-space residual quantile that can take any positive
   value. **A single print of the four q90 values would have caught it.**
2. **The two terms are not independent.** Both derive from q90, so the 0.5/0.5
   weighting combines one quantity with itself. The tool's own docstring already
   concedes this - *"because both its terms derive from the per-category q90, it
   varies little within a category"* - which is the defect stated and then
   shipped anyway.
3. **Nothing in the pipeline asserted that the output varied.** A score that
   returns four distinct values across 230 brands is the kind of thing a one-line
   sanity check catches immediately.

## What it is NOT

⚠ **It is not caused by sparse data, short series or the small panel.** Those are
real constraints and they explain why the *intervals* are wide - a q90 of 2.0
means the model genuinely is uncertain at this data scale, which is an honest
finding. But the intervals are **correctly calibrated**: empirical coverage is
91.0, 90.9, 86.0 and 83.9 per cent against a nominal 90. The uncertainty
measurement works. **It is the index built on top of it that does not.**

That distinction matters for how Chapter 7 reports this. The tool's uncertainty
machinery is sound; one derived convenience field is not.

---

# The decision

| Option | Verdict |
|---|---|
| **Drop the field, report as a finding** | ✅ **recommended** |
| Recalibrate the tier cut-offs | ❌ **does not work** - re-tiering a per-category constant yields four values, one per category. A category label wearing a number |
| Fix defect 2 only (rescale the second term) | ❌ insufficient - defect 1 still leaves it constant within a category |
| Rebuild on a per-forecast quantity | ⚠ real work, and the only route to an index that varies. Out of scope for the time available |

## Why dropping is the stronger result, not an omission

SRQ2 asks how a forecast reaches an agent with **reliability, uncertainty and
traceability** preserved. Check what the payload already carries:

| Property | Carried by | Status |
|---|---|---|
| uncertainty | the split-conformal interval | ✅ calibrated, coverage measured |
| reliability | `historical_*` - the model's measured held-out accuracy on both metrics, plus the best baseline under each | ✅ measured |
| traceability | `forecast_log.jsonl` - model file, training cutoff, calibration split, feature count, timestamp | ✅ complete |

**The confidence index carries none of the three.** It was a convenience layer
over the interval, and the interval does the job properly. Removing it loses no
capability.

## Draft wording - ONLY if Section 7.4 is ever restructured

⚠ **Do not paste this now.** Section 7.4 already says all of it, in its own
voice, better integrated than a block dropped in from a note. This is kept only
so the argument is not lost if that section is rewritten.

> No scalar confidence score is presented as part of the forecast's reliability
> evidence. An earlier design combined relative interval width with the conformal
> quantile into a single index, and evaluating it showed the construction to be
> degenerate: because a multiplicative interval is proportional to the forecast it
> surrounds, the relative width reduces to a function of the calibration quantile
> alone, which is constant within a category. The index therefore could not
> distinguish one brand's forecast from another's, and no choice of threshold
> could recover that information.
>
> The decision reflects a more general point about designing for an agent
> consumer. A single number invites the consuming model to treat it as a
> probability and to reason with it, so a score that looks informative and is not
> is worse than no score at all. What the payload provides instead is the
> calibrated interval, which answers how uncertain this forecast is, and the
> model's measured track record against the relevant baselines, which answers how
> accurate this model has been. Those two answer different questions, and keeping
> them separate is what lets the agent state which one it is relying on.

### Note - this is a real SRQ2 contribution

**Do not bury it as an omission.** A design-science thesis that reports a
component it built, evaluated and then removed - with the reason - is
demonstrating the evaluation working. The paragraph above is written so it reads
as a finding rather than an apology.

⚠ **No metacomment.** The wording says "an earlier design" rather than naming
plans, sessions or authors, so it stands for a reader who never saw a draft.

---

# What has to happen in code, if the field is dropped

Not yet done - this note records the decision, not its execution.

⚠ **Deleting the key is NOT a local change.** Checked 2026-09-11: **SRQ4 depends
on `confidence_tier` in three places, and one of them is an already-scored
result.**

| Consumer | What it does | Impact of deletion |
|---|---|---|
| `verify_setup.py:215` | asserts `confidence_tier` is in the tool payload | **pre-flight check fails**, blocking every SRQ4 run |
| `score_interval_communication.py` | scores `states_confidence` as one of four criteria | **a scored criterion disappears**; the 0-4 score becomes 0-3 |
| `inspect_runs.py:133` | prints the tier when reading back runs | cosmetic |
| `interval_communication.csv` | **already contains scored runs** with a `states_confidence` column | **existing results would no longer be reproducible** |

**This changes the recommendation's execution, not its substance.** Three routes:

| Route | What it costs |
|---|---|
| **A - keep the key, stop reporting it** ✅ recommended | nothing. The tool still returns a tier so SRQ4's contract and scoring hold; Chapter 7 simply does not present it as a confidence signal, and states why |
| B - delete the key outright | re-run SRQ4's scored communication arm, and re-generate `interval_communication.*`. Real money and time |
| C - delete and drop the criterion | as B, plus the four-criterion score becomes three and the comparison across scenarios changes shape |

⚠ **Route A is the honest option, not a fudge.** The SRQ4 criterion asks whether
an agent *communicates* the uncertainty it was given, which is a question about
the agent's behaviour and is unaffected by whether the underlying index is
informative. Chapter 7's claim is about what the payload should be *trusted* for.
Both statements are true at once, and Route A lets the thesis make each in its
own place without a re-run.

**If Route A is taken, the code change is only this:**

| Where | Change |
|---|---|
| the module docstring | strengthen the NOTE on `confidence`: it does not merely "vary little within a category", it is constant within one. Say so |
| Chapter 7 | the wording below, which explains why no confidence score is presented |
| Chapter 8 / SRQ4 | where `states_confidence` is described, note that it scores communication of the tier, not the tier's informativeness |

---

# The other item carried from Chapter 5

**The calibration table describes a model two categories do not serve** (S17).
`srq1_calibration.py` line 184 fits `XGBRegressor` for every category, but the
served metadata shows energidrikke and RTD are LightGBM - `model.joblib` rather
than `model.json`.

**This is the one re-run worth doing if time appears.** Full specification is in
`plans/P0053_2026-09-08_15-40_vps-hpc-model-training/findings.md` under
*The calibration re-run*, written so it can be executed on the HPC without
rediscovering any of it.

It touches Chapter 5's Section 5.5.7 and this chapter's description of the
interval. **Chapter 5 is already written so it stays true either way** - its
scope sentence says the coverage figures describe the calibration method on this
panel rather than a property of whichever implementation is served.
