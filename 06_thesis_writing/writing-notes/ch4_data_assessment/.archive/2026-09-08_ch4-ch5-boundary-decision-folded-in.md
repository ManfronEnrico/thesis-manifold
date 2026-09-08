---
name: ch4-ch5-boundary-decision
description: NOTE - Where feature engineering and the data split belong. Revised: keep both in Ch4, cut Ch5 5.3.1/5.3.2 to a back-reference plus the experiment-specific facts. Includes the contradictions the duplication has already produced.
snapshot: 2026-09-08_18-04_ch4-second-verification
category: workflow
applies-to: [chapter 4, chapter 5, structure]
created: 2026_09_08-18_30
updated: 2026_09_08-18_55
status: ready
---

# Where feature engineering and the split belong

**Snapshot:** `2026-09-08_18-04_ch4-second-verification`
**Notes swept:** none live in `ch5_model benchmark/` bearing on this; the ch4
folder's applied notes are already archived.

**This note replaces its own earlier recommendation.** I first proposed moving
feature engineering to Chapter 5. Brian pushed back, and he is right. What
follows is the revised position and the reason the first one was wrong.

---

## Why the first recommendation was wrong

I argued that feature engineering is "a property of the model, not the data".
Two things defeat that.

**The pipeline computes features before it splits.** In `FeatureEngineer.transform`
the order is literally `calendar -> filter -> engineer_features -> apply_split`.
Feature construction is upstream of the split, so a chapter that describes the
split but not the features describes the pipeline out of order.

**The features are leakage-safe by construction, and the code says so.** From
`FeatureEngineer.fit`:

> "Currently a no-op: every transformation in this module is leakage-safe by
> construction (lags/rolling use shift, calendar/promo/log are deterministic).
> No statistics are learned from training data."

This is the crux. The usual reason to place feature engineering after the split
is that fitting a scaler or an encoder on the full panel leaks test information
into training. **Nothing here is fitted.** A lag is a shift; a calendar flag is a
lookup; the log transform is deterministic. So the argument that would have
forced these into the modelling chapter does not apply, and the `fit` method is
a deliberately empty placeholder kept for the day something *is* learned.

**And the features are computed in the EDA.** The lag set comes from the ACF in
4.2.4, the rolling windows from the same inspection, the peak months from the
seasonal profile in 4.2.3. Chapter 4 does not merely mention these values - it
is where they are derived. Moving the result to Chapter 5 would separate a
number from the evidence that produced it.

---

## The revised recommendation

**Everything stays in Chapter 4. Chapter 5's 5.3.1 and 5.3.2 shrink to a
back-reference plus the facts that belong to the experiment.**

Chapter 4 owns the substrate: what the data are, what was derived from them, how
they were divided. Chapter 5 owns the experiment: what horizon was forecast, how
many rows were scored, how hyperparameters were chosen. The boundary is not
"data versus model" - it is **construction versus use**.

### What Chapter 5 keeps

Only what is true of the *experiment* rather than the *matrix*:

- the horizon, H = 3
- test-set row counts (CSD 665, RTD 372, energidrikke 308, danskvand 174) -
  these are what a reader needs to weigh a WMAPE, and they are verified correct
- which features each model family consumes, since ARIMA and Prophet take the
  univariate series while the tabular models take the matrix
- the NaN-versus-zero-fill distinction, because it is a statement about **which
  model receives what**, not about how the column was built

Everything else in 5.3.1 and 5.3.2 is a restatement of Chapter 4 and goes.

### Note - this is the smaller edit, not just the better one

The revised version deletes about fifteen lines from Chapter 5 and adds one
sentence. The version I proposed first would have moved two sections between
chapters and rewritten both. Given that Chapter 5 has forty-nine open comments
of its own, the cheaper fix that produces the same result is clearly right.

---

# The fixes

---

## Fix 1 - Chapter 5 asserts no holiday calendar exists

The single most important item here: **Chapter 5 contradicts Chapter 4 on a
matter of fact, in the same document.**

### Anchor

In 5.3.2, the calendar bullet.
Starts: *"Calendar: month, quarter, and a binary peak_month flag..."*
Ends: *"...measured from the sales distribution, not from calendar dates"*

### Action

REPLACE.

#### Replace with

> **Calendar**: month, quarter, a binary peak-month flag derived from the
> category's own seasonal profile, and three columns from the Danish
> public-holiday calendar described in Section 4.3. The peak-month flag and the
> holiday columns measure different things and are both retained: the flag is
> derived from the sales distribution, while the holiday count comes from an
> external calendar.

### Note - the code settles it

`n_holidays`, `non_holiday_days` and `days_in_month` are all in the CSD
manifest's feature list, for all four categories. The sentence was true when
written and the enrichment landed afterwards - one chapter was updated, the
other was not. That is the failure mode duplication produces, and it is the
argument for the back-reference below.

---

## Fix 2 - Collapse 5.3.1 to the experiment-specific facts

### Anchor

Starts: *"Grain: brand x month (DEC-GRAIN). The chain and region grains..."*
Ends: *"...CSD 665 rows, RTD 372, energidrikke 308, danskvand 174"*

### Action

REPLACE the whole subsection body.

#### Replace with

> The modelling grain is brand x month, and the panel, its minimum-history
> requirement and its train/validation/test boundaries are as established in
> Sections 4.2 and 4.4; the chain and region grains were evaluated and dropped,
> and are reported as a limitation rather than a live dimension. Two properties
> belong to the experiment rather than to the data. The forecast horizon is
> three months, so each model predicts the value three periods ahead of the last
> observation it is given. And the resulting test sets contain 665 rows for CSD,
> 372 for RTD, 308 for energidrikke and 174 for danskvand - the denominators
> behind every error figure reported in Section 5.5.

### Note - verified

All four row counts are correct against the current matrices. They are the one
part of 5.3.1 that says something Chapter 4 does not.

---

## Fix 3 - Collapse 5.3.2 to a back-reference

### Anchor

Starts: *"Lags: t-1, t-2, t-3, t-4, t-8, t-13 months"*
Ends: *"...Ridge receives a zero-fill at fit time"*

(Apply Fix 1 first if pasting separately, or apply this replacement in its place
— it subsumes the calendar bullet.)

### Action

REPLACE the whole subsection body.

#### Replace with

> The feature matrix is the one constructed in Section 4.3: lagged and rolling
> summaries of the target, calendar position including the public-holiday
> columns, promotional intensity where Nielsen reports it, and the Nielsen
> distribution and reach measures. Its construction is not repeated here.
>
> What matters for the benchmark is which models consume it. The tabular
> learners - LightGBM, XGBoost and Ridge - take the full matrix; ARIMA and
> Prophet are fitted on the univariate log sales series and never see it. The
> two groups also differ in how they handle the missing values that lagged
> features necessarily carry for a brand's earliest months: the tree models
> handle missingness natively, while Ridge cannot and receives a zero-fill at
> fit time. Promotional features exist for CSD and energidrikke only; for
> danskvand and RTD the column is omitted rather than zero-filled, since a
> constant zero would assert that no promotion ran when the truth is that none
> was recorded.

### Note - what this preserves

The three things in the old 5.3.2 that Chapter 4 does not say - the model-family
split, the NaN/zero-fill contrast, and the omit-versus-zero-fill reasoning - all
survive. Only the parameter values are dropped, and those are in Chapter 4 with
the evidence that produced them.

---

## Fix 4 - Chapter 4's own duplicate

Section 4.2.5's Table 2 restates parameters that 4.3 and 4.4 now state
correctly, and it carries two superseded figures.

### Anchor

The Table 2 rows.
Starts: *"MIN_PERIODS | 30 (global)"*
Ends: *"Train / Val / Test | 24 / 6 / 12 months"*

### Action

DELETE the table. Keep the sentence that follows it.

#### Replace with

> These parameter values are reported where they are derived: the lag set and
> rolling windows in Section 4.2.4, the peak months in Section 4.2.3, the
> minimum-history requirement in Section 4.1.2 and the split in Section 4.4.
> Their origin is empirical rather than theoretical - they follow from this
> panel's own structure rather than from a prior specification - and that is
> stated as a limitation rather than presented as a design principle.

### Note - two stale figures die with the table

"MIN_PERIODS 30 (global)" and "Train / Val / Test 24 / 6 / 12 months" are both
superseded, and both sit two sections above the tables that correct them. This
is the same duplication problem inside a single chapter.

⚠ The sentence after Table 2 currently says the parameters' *"academic
justification is developed in the modelling chapter"*. After these fixes,
Chapter 5 no longer restates the parameters, so that promise has nowhere to
land. The replacement above removes it.

---

# Where this leaves the two chapters

| Topic | Chapter 4 | Chapter 5 |
|---|---|---|
| Grain | derived, 4.2.1 | named, cited |
| Minimum history | derived, 4.1.2 | cited |
| Lags, rolling, peak months | derived from EDA, 4.2.3-4.2.5 | cited |
| Holiday enrichment | provenance, 4.3 | cited |
| Feature admissibility rule | stated, 4.3 | cited |
| Split boundaries | Table 5, 4.4 | cited |
| **Horizon** | — | **5.3.1** |
| **Test-set row counts** | — | **5.3.1** |
| **Which model takes which input** | — | **5.3.2** |
| **NaN handling per model family** | — | **5.3.2** |

Each fact appears once, in the chapter that establishes it, and Chapter 5 points
at Chapter 4 rather than paraphrasing it.

---

## Note - the bullet-fragment style is chapter-wide, not just 5.3

You noted 5.3 looks like Enrico's old draft. It does, but so does the rest of
Chapter 5 - 5.1's selection criteria, 5.4.1's scoring-function argument and
5.2's model descriptions are all in the same run-in bold-lead fragment style,
including passages carrying real citations (Gneiting 2011, Hyndman &
Athanasopoulos 2021, Makridakis et al. 2018).

**So the prose conversion is a chapter-level job, not something to fold into
these fixes.** The replacements above are written as finished prose, which will
make them sit oddly against their neighbours until the rest is converted. That
is the right trade: they are correct now and correctly styled later, rather than
matching a style that is itself being replaced.

---

## Note - Appendix A

Correcting my earlier error: Appendix A is *"Star Schema Diagram (CSD Example)
and Resulting Category Features"* - the raw table schema. It does **not** contain
the engineered feature list, so the reference to it in Fix 1 of
`ch4-verification-pass.md` must not be pasted as written.

Its title already promises "Resulting Category Features", so extending it to
carry the per-category feature list beneath the schema would honour the existing
title and put raw and derived columns in one place. That is my recommendation
over adding an Appendix B.

---

## Note - this settles the repetition comment

The ACADEMIC comment on 4.1 asks whether the thesis's cross-chapter repetition
is rigour or slop, and your reply records the answer you were given: *"ideally
no repetition, or keep it to the lowest necessary degree, pointing towards the
sections where it is actually covered."*

That is exactly the pattern above - one chapter establishes, the other cites.
And the holiday contradiction is the evidence for why it matters: the repetition
did not merely bore a reader, it let one chapter go stale while the other was
corrected.
