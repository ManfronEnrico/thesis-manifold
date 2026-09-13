---
name: ch5-book-citations-that-strengthen-existing-choices
description: NOTE - Six sections of Hyndman & Athanasopoulos that ENDORSE choices Ch5 already made but does not claim. Free citations, no prose rewrite needed.
category: reference
applies-to: [ch5 model benchmark]
triggers: [ch5 prose pass, defending the benchmark design, answering why this metric]
created: 2026_09_13-21_15
updated: 2026_09_13-21_15
source: P0055 book scan, 41/41 sections. Full catalogue in plans/P0055_*/findings.md F15
---

# Ch5 - six free citations the chapter is currently leaving on the table

**These are not corrections.** Each one is a design choice the thesis ALREADY
made correctly, which the source independently endorses, and which the prose
currently justifies from first principles or not at all. Adding the citation
costs a sentence and converts an unexplained convention into a sourced decision.

**Source:** Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*,
3rd ed. All 41 sections read 2026-09-13 (P0055 book scan). **Every one of these
is already in the Zotero library** as the book is cited elsewhere in Ch5 -
verify the section-level citation format before pasting.

---

## 1. Section 13.8 - scoring a SINGLE month at exactly H=3 is a strength

### What the book says

> "the comparisons on the test data use **different forecast horizons**... The
> forecast variance usually increases with the forecast horizon, so if we are
> simply averaging the absolute or squared errors from the test set, we are
> **combining results with different variances**."

### What the repo does

`test.iloc[HORIZON-1]` - scores exactly one month, at exactly H=3. This
sidesteps the problem entirely.

### What the prose currently says

It is justified only as "the horizon contract" - i.e. as a convention, not as a
methodological choice.

### To claim

That the single-month-at-fixed-horizon design **avoids averaging errors of
unequal variance**, citing 13.8. This is a deliberate strength presented as an
implementation detail.

⚠ Also carries a guard worth stating: **an H=3 result must never be compared
against an H=1 figure.** If any table does this, it is a defect.

---

## 2. Section 9.10 - comparing model families on a test set is the CORRECT method

### What the book says

> "The AICc is useful for selecting between models **in the same class**...
> However, it **cannot be used to compare between ETS and ARIMA models**."

The two-level procedure: AICc *within* a family, test set or cross-validation
*across* families.

### What the repo does

SRQ1 compares statistical, ML and neural families on a held-out test set -
exactly the book's prescribed method for heterogeneous families.

### To claim

That the held-out-test comparison is not a convenience but **the correct
instrument** for cross-family comparison, and that an information criterion
would have been the wrong one. Direct endorsement of SRQ1's core design.

### Pairs with 9.9

> "when comparing models using a **test set**... the comparisons are always
> valid"

- which legitimises comparing models fitted under different differencing
regimes. Worth stating explicitly if any reviewer questions it.

---

## 3. Section 5.10 - the WMAPE tuning deviation is PRINCIPLED, not an oversight

### What the book says

> "A good way to choose the best forecasting model is to find the model with the
> **smallest RMSE** computed using time series cross-validation."

### What the repo does

Tunes on **WMAPE**, not RMSE - a visible deviation from the book's single named
recommendation. But it tunes **twice**, once per objective, because WMAPE and
median APE are minimised by different functionals.

### The theory that justifies it

Section 5.8: MAE is minimised by the **median**, RMSE by the **mean**. So tuning
once per objective is the methodologically correct response to having two
objectives - arguably better than the book's single recommendation.

### To claim

Say the deviation is deliberate and say why. An unexplained deviation from a
named textbook recommendation is the kind of thing an examiner circles;
a one-sentence justification removes it entirely.

---

## 4. Section 7.5 - the weighted-distribution rejection was made on the RIGHT criterion

### What the book says

Two approaches are named **invalid**: dropping a predictor from a scatterplot
("This is invalid") and dropping by p > 0.05 ("also invalid... statistical
significance does not always indicate predictive value"). Recommended instead:
"AICc, AIC, or CV... each of which has **forecasting as their objective**".

### What the repo did

Rejected the weighted-distribution feature because **measured error rose in
three of four categories** - a predictive criterion, which is exactly what 7.5
sanctions.

### To claim

The rejection currently stands **unsourced** in the prose. 7.5 confirms the
decision rule was the right one. Free defensive citation.

⚠ The other half of 7.5 is a genuine gap (the repo computes no information
criterion at all) - that is Branch B work, task 22. Do not claim it here.

---

## 5. Section 5.9 - MASE/RMSSE over MAPE is the source's own preference

### What the book says

The test set must be large enough "**especially in the denominator**", so
"**MASE or RMSSE are often preferable**" to percentage errors. And: "When the
data are seasonal, the benchmark used is the **seasonal naive method**."

### To claim

CONFIRMS the choice to report MASE. Free.

⚠ **BUT** - the seasonal-naive-benchmark half is currently VIOLATED: the MASE
denominator uses m=1 on a seasonal panel. That is a Branch B repair (2.A5,
task 7). **Do not cite 5.9's seasonal sentence in Ch5 until that is fixed**, or
the chapter cites a rule it breaks.

---

## 6. Section 5.6 - CONFIRMS the log-space conformal interval

### What the book says

Prediction intervals formed on the transformed scale and back-transformed retain
their coverage, "because **quantiles are preserved under monotonically
increasing transformations**".

### What the repo does

Forms the split-conformal interval in log space, then exponentiates.

### To claim

The interval construction is sourced, not improvised. Free.

⚠ **The other half of 5.6 is a real issue and belongs to Ch5 or SRQ2**, see the
ch9/ch10 note: back-transformed point forecasts are **medians, not means**, and
"**medians do not add up**". So brand forecasts must not be summed to a category
total without bias adjustment. P0048 already has this open as an SRQ2 item.

---

## Not for Ch5 - routed elsewhere

| Finding | Goes to |
|---|---|
| 5.5, point forecasts need intervals | **Ch7** - see the ch7 note |
| 13.3, positivity via log not clipping | **Ch9/Ch10 limitations** |
| 13.7, minimum-sample rules of thumb | **Ch4** - it may undercut MIN_PERIODS |
| 6.1/6.2/6.7, judgmental forecasting | **Ch3/Ch9** |
