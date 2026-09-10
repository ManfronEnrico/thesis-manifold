---
name: fpp3-first-pass-findings
description: NOTE - A direct read of six FPP3 section PDFs against Chapter 5, with page-located quotations. Two findings are defects in the thesis rather than citation opportunities. Everything here is checkable against the PDFs before it reaches the chapter.
category: reference
applies-to: [chapter 5, citations]
created: 2026_09_10-21_10
updated: 2026_09_10-21_10
status: draft - verify each quotation against the PDF
---

# FPP3, first pass: what the sections actually say

**Read directly from the PDFs**, not from memory. Six of the forty sections, chosen
as the ones bearing on the four disputed claims in the source-review document.

⚠ **Check every quotation below against the PDF before it reaches the chapter.**
Each carries its section and its PDF page so this takes seconds. I have quoted
rather than paraphrased precisely so this is checkable.

**This does not replace the NotebookLM run.** It is a first pass to tell you where
the value is, so the full run can be aimed rather than exhaustive.

---

# The headline: two findings are defects, not citations

| # | What | Section | Severity |
|---|---|---|---|
| **1** | The thesis clips Ridge forecasts. The book gives a **transformation-based method for exactly this**, and calls an artificial constraint "unrealistic" | 13.3 | ⚠ **methodological** |
| **2** | The thesis back-transforms log forecasts without **bias adjustment**. The book says the result is a **median, not a mean** | 5.6 | ⚠ **methodological** |

Both are things the chapter currently does one way while the source recommends
another. Neither is fatal; both need a sentence acknowledging the choice.

---

# 1. Ridge clipping - the book offers the alternative the thesis did not use

### What the thesis does

Section 5.5.2: *"Ridge requires clipping to be reportable. Unclipped, its
energidrikke WMAPE is 2.8x10^13 ... because back-transformed linear extrapolation
diverges."*

### What section 13.3 says

**PDF page 1, opening sentence:**

> "It is common to want forecasts to be positive, or to require them to be within
> some specified range [a, b]. Both of these situations are relatively easy to
> handle using transformations."

**PDF page 1, "Positive forecasts":**

> "To impose a positivity constraint, we can simply work on the log scale. ...
> Because of the log transformation, the forecast distributions are constrained
> to stay positive, and so they will become progressively more skewed as the mean
> decreases."

**PDF page 2** gives the scaled logit for a bounded interval, mapping (a, b) to
the whole real line.

**PDF page 4, and this one cuts against post-hoc clipping:**

> "The prediction intervals lie above 50 due to the transformation. As a result
> of this artificial (and unrealistic) constraint, the forecast distributions
> have become extremely skewed."

### The finding

**The book treats bounding as a modelling decision made through the
transformation, not a post-hoc operation on the output.** The thesis does the
latter and does not say why.

There is a real defence available and the thesis should make it: the log
transformation *was* used, so positivity was already imposed the way the book
recommends. **The divergence is not a positivity failure but an
upper-tail extrapolation failure**, which the book's positivity method does not
address. That is a more precise account than "requires clipping".

**Recommended addition to Section 5.5.2**, and it needs no citation to stand:

> Sales are modelled on the log scale, which already constrains forecasts to be
> positive. The instability here is in the upper tail: a linear extrapolation on
> the log scale becomes an exponential one after back-transformation, so a modest
> slope error on a short series produces an arbitrarily large forecast. Clipping
> bounds that tail rather than imposing positivity, and the bound is reported
> alongside the unclipped values so the effect is visible.

⚠ **State the clipping bound in the chapter.** It currently is not given, and a
reader cannot assess a clipped figure without knowing the clip.

---

# 2. Back-transformed forecasts are medians, not means

**This one has consequences beyond wording**, and I do not think the chapter has
considered it.

### What section 5.6 says

**PDF page 2, "Bias adjustments":**

> "One issue with using mathematical transformations such as Box-Cox
> transformations is that the back-transformed point forecast will not be the
> mean of the forecast distribution. In fact, it will usually be the median of
> the forecast distribution (assuming that the distribution on the transformed
> space is symmetric). For many purposes, this is acceptable, although the mean
> is usually preferable. For example, you may wish to add up sales forecasts from
> various regions to form a forecast for the whole country. But medians do not
> add up, whereas means do."

**Same page**, the size of the effect:

> "The larger the forecast variance, the bigger the difference between the mean
> and the median."

### Why this matters here, and it connects to Section 5.4.1

The chapter fits on `log_sales_units` and back-transforms. **Its point forecasts
are therefore medians of the forecast distribution, not means.**

That interacts with the chapter's own metric argument in a way worth stating.
Section 5.4.1 argues WMAPE is the right metric *because it is consistent for the
median*. So the metric and the transformation agree: both target the median.
**That is a genuine coherence in the design that the chapter does not currently
claim**, and it is worth one sentence.

But the book's warning applies directly to this thesis's use case:

> "you may wish to add up sales forecasts from various regions to form a forecast
> for the whole country. But medians do not add up, whereas means do."

**A demand planner aggregating brand forecasts to a category total is doing
exactly that.** The forecast tool serves per-brand forecasts to an agent that may
well sum them.

**Recommended addition to Section 5.4.1 or 5.5.7:**

> Because the models are fitted on log sales and back-transformed, the point
> forecasts are medians of the forecast distribution rather than means (Hyndman &
> Athanasopoulos, 2021). This is consistent with the choice of weighted error as
> the primary metric, which is itself minimised by the median. It carries one
> consequence for downstream use: medians do not aggregate additively, so a sum
> of brand-level forecasts is not the median forecast of the category total.

⚠ **This may also be worth a line in the SRQ2 chapter**, since the tool returns
per-brand forecasts and nothing currently warns a consumer against summing them.

### Prediction intervals are unaffected

**PDF page 2:**

> "If a transformation has been used, then the prediction interval is first
> computed on the transformed scale, and the end points are back-transformed ...
> This approach preserves the probability coverage of the prediction interval,
> although it will no longer be symmetric around the point forecast."

**Good news for Section 5.5.7** - the conformal intervals are calibrated in log
space and back-transformed, and coverage is preserved under that operation. The
chapter can say so.

---

# 3. Prophet - the book supports the thesis's claim, and more strongly than
# Taylor & Letham do

The source review flagged *"Prophet is applied outside its design regime"* as
possibly overstating Taylor and Letham. **It does.** But section 12.2 makes a
compatible claim in the book's own voice, which is a better citation.

**PDF page 1:**

> "This model was introduced by Facebook (S. J. Taylor & Letham, 2018),
> originally for forecasting daily data with weekly and yearly seasonality, plus
> holiday effects. It was later extended to cover more types of seasonal data.
> **It works best with time series that have strong seasonality and several
> seasons of historical data.**"

**PDF page 2**, on the quarterly example:

> "Note that the seasonal term must have the period fully specified for quarterly
> and monthly data, as the default values assume the data are observed at least
> daily."

> "In this example, the Prophet forecasts are worse than either the ETS or ARIMA
> forecasts."

**PDF page 6, the closing verdict:**

> "Prophet has the advantage of being much faster to estimate than the DHR models
> we have considered previously, and it is completely automated. **However, it
> rarely gives better forecast accuracy than the alternative approaches**, as
> these two examples have illustrated."

### The finding

**Three things the thesis can now say with a citation rather than as its own
inference:**

1. Prophet's defaults **assume at least daily data** and must be overridden at
   month grain. That is the book stating the design-regime point directly.
2. It **works best with several seasons of historical data**. The thesis panel has
   roughly three to four years per brand.
3. The book's own comparison finds Prophet **worse than ARIMA and ETS**, and
   states it rarely wins generally.

**Recommended rewrite of the Prophet paragraph in Section 5.5.2:**

> Prophet is applied outside the regime its defaults target. Its seasonal
> machinery assumes data observed at least daily, so the period must be specified
> explicitly at month grain, and it works best on series with strong seasonality
> and several seasons of history (Hyndman & Athanasopoulos, 2021). Neither
> condition is comfortably met here. The same source reports that Prophet rarely
> achieves better accuracy than the classical alternatives, which is consistent
> with what is observed on this panel. Fitting a linear trend on log-transformed
> short series lets the trend extrapolate to extreme values on back-
> transformation, producing the figures reported above. This is a limitation of
> the application rather than a defect of the method, and it is reported as such.

**This is strictly better than the current paragraph**, because it attributes the
design-regime claim to a source that makes it, rather than to Taylor and Letham
who do not.

---

# 4. Short series - direct support for the small-panel argument

Section 13.7's opening is almost written for this thesis.

**PDF page 1:**

> "We often get asked how *few* data points can be used to fit a time series
> model. As with almost all sample size questions, there is no easy answer. It
> depends on the *number of model parameters to be estimated and the amount of
> randomness in the data*. The sample size required increases with the number of
> parameters to be estimated, and the amount of noise in the data."

**Same page**, and this one is useful defensively:

> "Some textbooks provide rules-of-thumb giving minimum sample sizes for various
> time series models. These are misleading and unsubstantiated in theory or
> practice. ... There is, for example, no justification for the magic number of
> 30 often given as a minimum for ARIMA modelling."

**Same page**, the mechanism the thesis needs:

> "What tends to happen with short series is that the AICc suggests simple models
> because anything with more than one or two parameters will produce poor
> forecasts due to the estimation error."

### Two findings

**A. The danskvand explanation now has a source.** Section 5.5.2 argues that
Prophet wins the smallest panel because a high-capacity model has least to learn
from. The book states the mechanism: more parameters need more observations, and
on short series the extra parameters produce poor forecasts through estimation
error.

**B. This retires an open Chapter 4 claim.** The registers carry an unresolved
item on whether a source states a minimum series length for ARIMA, around 24
periods. **The answer is that the book explicitly rejects such rules**, and names
the number 30 as having no justification.

⚠ **That claim should be removed from Chapter 4 rather than sourced.** Citing a
minimum-length rule would be citing something this book calls "misleading and
unsubstantiated". Chapter 4 can instead say that no defensible minimum exists and
that the constraint is parameter count against noise.

---

# 5. ARIMA - the seasonality gap is real, and the book is explicit

The source review's first problem is confirmed.

**Section 9.9, PDF page 1:**

> "So far, we have restricted our attention to non-seasonal data and non-seasonal
> ARIMA models. However, ARIMA models are also capable of modelling a wide range
> of seasonal data."

The whole section then works two **monthly** examples, and in both the chosen
model carries a seasonal order.

**PDF page 3**, on monthly employment data:

> "The data are clearly non-stationary, with strong seasonality and a nonlinear
> trend, so we will first take a seasonal difference."

**PDF page 8**, on monthly drug sales:

> "The data are strongly seasonal and obviously non-stationary, so seasonal
> differencing will be used."

### The finding

**The book's treatment of monthly seasonal data always includes a seasonal
term.** The thesis fits `SARIMAX(order=(1,1,1))` with no seasonal order on
monthly data it describes as strongly seasonal.

**This is not a citation opportunity. It is a limitation the chapter understates.**
Its current wording says ARIMA is "not order-optimised", which suggests a tuning
gap. The real gap is structural: the model has no mechanism for the seasonality
the chapter says dominates the panel.

**Recommended replacement for the ARIMA limitation in Section 5.5.8:**

> ARIMA is fitted at a fixed, **non-seasonal** order of (1,1,1) per series, and
> Prophet at a fixed specification, on cost grounds. The ARIMA limitation is
> structural rather than one of tuning: the panel is monthly with strong annual
> seasonality, and standard practice for such data includes a seasonal order
> (Hyndman & Athanasopoulos, 2021). Without one, the model has no mechanism for
> the pattern seasonal naive exploits directly, so the comparison between them
> understates what the ARIMA family could achieve here. Their figures are a floor
> for these families rather than their best attainable performance.

⚠ **Consider whether to rerun.** A seasonal order on four categories is cheap
compared to the tuned models. The alternative is a clearly stated limitation, and
the wording above is that. **This is Brian's call, not mine** - but the current
text does not give a reader enough to make it themselves.

---

# What I have not read yet

Thirty-four of the forty sections. The ones most likely to carry further findings,
in the order I would open them:

| Section | Why |
|---|---|
| **5.8 Evaluating point forecast accuracy** | the MASE denominator, and whether the thesis implements it the same way. Section 5.5.3's figures depend on this |
| **5.9 Evaluating distributional forecast accuracy** | whether the coverage-plus-width approach matches what the book recommends, or whether an interval score is preferred |
| **5.10 Time series cross-validation** | whether the book's rolling origin matches the thesis's period-level panel split |
| **13.8 Forecasting on training and test sets** | the nested-selection question |
| **9.10 ARIMA vs ETS** | whether the missing-ETS problem is as serious as the review suggests |
| **13.4 Forecast combinations** | for the ensemble paragraph in Section 5.6 |

**Say the word and I will read them the same way** - quoting with page numbers so
you can check.

---

# How to use this

1. **Spot-check three or four quotations** against the PDFs. If they hold, the
   rest were read the same way.
2. **Findings 1, 2 and 5 change the chapter** and are independent of the
   NotebookLM run.
3. **Findings 3 and 4 improve citations** the chapter already makes.
4. Feed the full set to NotebookLM as planned. This pass tells you which verdicts
   to read first, not what they will say.
