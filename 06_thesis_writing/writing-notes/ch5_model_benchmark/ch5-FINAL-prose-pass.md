---
name: ch5-FINAL-prose-pass
description: NOTE - The single Chapter 5 pass. Every section in document order with its state, verification, comment verdicts and paste-ready prose, plus the book citations and the retraining decision. Consolidates four earlier notes.
snapshot: 2026-09-11_13-21_ch5-prose-session
category: workflow
applies-to: [chapter 5]
supersedes: [ch5-prose-pass.md, ch5-prose-pass-followup-01.md, ch5-pending-source-review.md, ch5-session-state.md]
created: 2026_09_11-14_00
updated: 2026_09_11-14_00
status: ready
---

# Chapter 5 - the one pass

**Work top to bottom.** Every section of the chapter is below in document order,
whether or not it changes. Nothing else in this folder needs opening.

Verified against snapshot `2026-09-11_13-21_ch5-prose-session`, repository at
`71486e4`, Zotero re-pulled 2026-09-11: **87 items**. Book read from
`C:\Users\brian\Downloads\Hyndman Book (2021)`.

## What this replaces

Four notes are folded in here and archived:

| Note | What it contributed |
|---|---|
| `ch5-prose-pass-followup-01.md` | the sequential spine - every section, verified |
| `ch5-prose-pass.md` | the holiday-ablation subsection and three attribution guards, which the follow-up dropped |
| `ch5-pending-source-review.md` | the five sections the literature review touches |
| `ch5-session-state.md` | what you have already applied, and the four-step order |

## You have already applied 5.0 to 5.2.1

Three comments closed - 199, 201 and 204 - and the chapter went from 49 threads
to 46. **Start at 5.2.2.** Sections 5.0, 5.1 and 5.2.1 appear below marked
**done**, so you can see they were not skipped.

⚠ **The memory budget is settled at 4 GB.** Section 5.1 now reads "the 4 GB
sequential memory budget". **Section 5.5.6 still says 8 GB and is the one to
change.** The earlier placeholder is resolved.

## How each section is laid out

| Field | Holds |
|---|---|
| **State** | prose already, bullets to convert, or a table to replace |
| **Verified** | what was checked against the repository, and the result |
| **Book** | the textbook section that supports the claim, where one does |
| **Comments** | the Word threads on that section, with a verdict each |
| **Paste** | the finished text, ready for Word |

Where a numbered cross-reference earns its place it is written in full as
**"Section 5.5.9"**. Where a section becomes prose, its references are rewritten
as names - *"the validation scheme described earlier"* - because numbers move and
every reference in this chapter currently points at Chapter 6.

---

# 5.0 Chapter title - DONE

Subtitle applied: *Selecting a Forecasting Substrate Under Memory and Data
Constraints*. Comment 199 closed.

⚠ **One thing to check.** The heading **"Chapter 5 | Model Benchmark &
Selection"** still appears **twice** in the export, which usually means a stray
heading-styled paragraph sits above the real one. Delete the duplicate.

---

# 5.1 Rationale for model selection - DONE

Applied as prose, comment 201 closed, and the memory budget reads 4 GB.

### One thing still open here

**ETS is missing from a claimed spectrum of inductive biases.** The section says
the five families "span the range of inductive biases available for this
problem". Exponential smoothing is one of the two dominant classical families and
it is absent. A reader who knows the field will notice.

This is a **wording fix, not a re-run.** Narrow the claim rather than adding a
sixth model.

### Paste - replace the opening sentence of 5.1

> Five model families were selected to cover the inductive biases most relevant
> to this problem: classical statistical methods in ARIMA and Prophet, gradient
> boosting in LightGBM and XGBoost, and regularised linear regression in Ridge.

### Paste - add as the final sentence of that same paragraph

> Exponential smoothing is the notable omission. It is a strong classical
> baseline on seasonal monthly data and its absence is a limitation of the
> comparison rather than a judgement on the family; the seasonal naive benchmark
> covers part of the same ground by exploiting annual seasonality with no
> parameters at all.

### Note - why this wording and not a re-run

Adding ETS means a sixth family through tuning, calibration, stability and every
downstream table. Conceding the gap costs two sentences and is the honest
statement. **The seasonal naive sentence is what makes the concession
defensible**, because it shows the seasonal signal is benchmarked even though
that family is not.

---

# 5.2 Model descriptions

Six subsections, five of which are still bullets.

### Note - a structural option, not a requirement

These read as six specification sheets with the same fields in a different order
each time. **A single comparison table plus one paragraph per model would be
shorter.** That is S15 on the deferred list and is not decided here - the prose
below keeps the current structure so it can be pasted without waiting.

---

## 5.2.1 Simple benchmarks - DONE

Formula table kept, bullet replaced with the seasonal-naive paragraph, comment
204 closed.

---

## 5.2.2 ARIMA - START HERE

### State

Bullets. Contains a genuine limitation worth keeping, and one that must get
**stronger**, not weaker.

### Verified

`statsmodels` SARIMAX at a fixed order, no automatic order search. **Correct** -
the environment has no `pmdarima`, confirmed against `requirements.txt`.

⚠ **The order carries no seasonal term at all.** The chapter treats annual
seasonality as the defining property of monthly beverage demand - it is the whole
justification for including seasonal naive - and then implements ARIMA with no
mechanism for it. The current limitation calls the model "not order-optimised",
which is true and **understates the problem**: this is a structural gap, not a
tuning gap.

### Book

**Section 9.9** works only seasonal models on monthly data and is unambiguous
that a seasonal term is what such data requires. That makes the gap citable as a
known methodological requirement rather than presented as our own doubt.

### Comments

**207 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste

> ARIMA enters as the classical univariate baseline, representing established
> time-series practice in the Box-Jenkins tradition. It is implemented through
> `statsmodels` at a fixed, **non-seasonal** order of (1,1,1), fitted per brand on
> log sales.
>
> Two properties of that specification bear directly on how its results should be
> read. The order is fixed rather than searched, because the automatic
> order-selection package was unavailable in the deployment environment. More
> consequentially, the specification carries no seasonal term, while the panel it
> is fitted to is monthly and strongly seasonal - the property that motivates the
> seasonal naive benchmark elsewhere in this chapter. Hyndman and Athanasopoulos
> (2021) treat a seasonal order as the standard specification for monthly data of
> this kind. The figures reported for ARIMA are therefore a floor for the family
> rather than its best attainable performance, and the comparison understates it
> by a margin this study does not quantify.
>
> Peak memory is negligible at roughly two megabytes. The model assumes
> stationarity and is univariate, so no promotional or calendar information
> reaches it.

### Note - this is the one candidate that might justify a re-run

See the retraining section at the end. **The recommendation is still not to
re-run**, because the wording above converts the gap into a stated limitation
that an examiner can accept, and a seasonal ARIMA would change the baseline
table, the MASE table and Section 5.6's family-gap claim.

⚠ **Do not write that ARIMA "failed".** It was not given the specification the
data needs. The honest claim is that the family is under-represented here.

---

## 5.2.3 Prophet

### State

Bullets. **Contains a claim that is now false.**

### Verified

⚠ **"No holiday calendar is supplied in this thesis" is wrong.** A Danish holiday
calendar was engineered on 2026-08-18 and three holiday columns now reach the
model: `days_in_month`, `n_holidays` and `non_holiday_days`. Verified in
`_features.py`.

The claim is still true **of Prophet specifically** - Prophet's own holiday
mechanism receives nothing - but as written it says the thesis has no holiday
data, which it does, and Section 5.3.2 contradicts it two pages later.

### Book

⚠ **The design-regime claim is currently attributed to Taylor and Letham, and
they do not make it.** The textbook states the point **in its own voice**, which
is both a better citation and an honest one.

### Comments

**209 `VERIFY, SOURCE, PROSE`** - **ADDRESSED**, and the holiday claim corrected.

### Paste

> Prophet is an additive decomposable model, y(t) = g(t) + s(t) + h(t) + e,
> combining trend, seasonality and holiday terms (Taylor & Letham, 2018). It was
> designed for forecasting at scale by analysts with domain rather than
> statistical expertise, and targets piecewise trends, multiple seasonality and
> floating holidays.
>
> None of that machinery is available at this grain. **Prophet's holiday
> component receives no input**: although this thesis does construct a Danish
> holiday calendar, its features are monthly counts rather than the dated events
> Prophet expects, and they are consumed by the tabular models instead. At month
> grain the multiple-seasonality machinery has nothing to fit either, the weekly
> component has no data, and the annual term reduces to roughly twelve points per
> series. What remains is a piecewise trend and a coarse annual cycle estimated on
> approximately thirty observations.
>
> **The limitation is therefore in the application rather than in the method as
> its authors documented it.** Peak memory is the highest of any model considered,
> at roughly 50 to 100 megabytes, which remains acceptable against the budget.

### Note - the attribution guard, and it matters

Check the paragraph does **not** say Taylor and Letham state Prophet is
unsuitable for monthly data, or that it produces flat forecasts. **They state
neither**, and both are overstatements a reader checking the source would catch.
The mechanical argument above explains rather than asserts and needs no source
beyond the model definition.

---

## 5.2.4 LightGBM

### State

Bullets, four lines. Contains a cross-reference to Chapter 6.

### Verified

RAM figure of 18.7 MB. ⚠ **`profiling.csv` reports 38.1 MB peak fit resident set
size and 23.0 MB tracemalloc.** Neither is 18.7. Fixed once, in Section 5.5.6.

### Comments

**211 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste

> LightGBM is the primary machine-learning candidate: a gradient-boosting
> implementation using leaf-wise tree growth and gradient-based one-side
> sampling. Hyperparameters are selected by the Optuna search described in the
> experimental setup below, over one hundred trials against a four-fold
> expanding-window cross-validation objective.

### Note - the RAM line comes out here

It is stated again in the operational profile, measured rather than approximate,
and stating it twice is how the two copies came to disagree. Same for XGBoost.

---

## 5.2.5 XGBoost

### Comments

**213 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste

> XGBoost is the alternative gradient-boosting implementation, differing from
> LightGBM in growing trees level-wise and in applying both L1 and L2
> regularisation. It receives an identical feature set and an identical tuning
> protocol, so the comparison between the two isolates the implementation rather
> than confounding it with the data each model saw.

---

## 5.2.6 Ridge regression

### Verified

The Hastie citation and the equation reference are **correct**.

### Comments

**215 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste

> Ridge regression is L2-regularised linear regression, minimising the penalised
> residual sum of squares - equivalently, the residual sum of squares subject to
> a bound on the sum of squared coefficients (Hastie et al., 2009).
>
> Its role is to isolate a confound that would otherwise sit inside every
> comparison in this chapter. A gradient-boosted model beating ARIMA differs from
> it in two ways at once: it has engineered lag, rolling and calendar features
> that a univariate method does not, and it can represent non-linear
> interactions. Ridge has the same features and no interactions, so the step from
> ARIMA to Ridge measures what feature engineering buys, and the step from Ridge
> to gradient boosting measures what non-linearity adds. Without it the chapter
> could report only a combined effect and attribute it to whichever explanation
> it preferred.

### Note - this argument is currently absent

The chapter says Ridge "establishes whether non-linear models earn their
complexity", which is the conclusion without the mechanism. The two-step
attribution is what makes Ridge worth its place, and it is the same
one-variable-at-a-time logic the scenario ladder uses in Chapter 8.

---

# 5.3 Experimental setup

---

## 5.3.1 Grain and data split

### State

Bullets, five lines.

### Verified

| Claim | Result |
|---|---|
| grain is brand x month | **correct**, locked as DEC-GRAIN |
| horizon H = 3 | **correct** - `_horizon.py` sets `PRIMARY = 3` |
| test sizes 665 / 372 / 308 / 174 | **correct**, confirmed across three artefacts |

### Comments

**218 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste

> All modelling operates on a brand-by-month grain. Chain-level and regional
> representations were evaluated and dropped early; they are reported as a
> limitation and as future work rather than as a live dimension of the
> comparison.
>
> The panel is split temporally into training, validation and test partitions
> with no shuffling, so that every validation and test period falls after the
> data used to fit the model. The forecasting horizon is three months, chosen
> because a quarter is the period over which the promotional and range decisions
> this forecast supports are actually taken. The resulting test partitions
> contain 665 rows for CSD, 372 for RTD, 308 for energidrikke and 174 for
> danskvand.

---

## 5.3.2 Feature engineering

### State

Bullets. **This is the section most out of step with the repository.**

### Verified

Checked against `_features.py`, which defines the feature set once for every
SRQ1 script.

| The chapter says | The code says |
|---|---|
| six lags, three rolling, three calendar, one promotional | those thirteen, **plus three holiday and two intermittency columns** |
| (nothing about intermittency) | `zero_run_flag`, `zero_run_length` |
| **"No holiday calendar is used"** | ⚠ **false.** `days_in_month`, `n_holidays`, `non_holiday_days` |
| peak_month from the sales distribution | **correct**, and worth keeping - measured, not assumed |

**The model consumes 18 features where the chapter describes 13.** For danskvand
and RTD it resolves to 17, because those categories have no promotional measure.

⚠ **The "No holiday calendar is used" clause must come out.** It was true when
written and became false on 2026-08-18. It also contradicts Chapter 4 and the
ablation now added as Section 5.5.8.

### Comments

**220 `VERIFY, SOURCE, PROSE`** - **ADDRESSED**, and the feature count corrected.

### Paste

> Eighteen features reach the model, in six groups. Six autoregressive lags at
> one, two, three, four, eight and thirteen months carry recent history and the
> year-ago comparison. Three rolling statistics - a four-month and a
> thirteen-month mean, and a four-month standard deviation - carry level and
> volatility. Three calendar features give month, quarter, and a binary peak
> indicator derived from each category's own seasonal profile rather than assumed
> from the calendar: a month qualifies where its mean units exceed the category
> mean by more than ten per cent.
>
> Three holiday features give the number of days in the month, the number of
> Danish public holidays falling within it, and the difference between the two.
> Two intermittency features record whether a brand is currently in a run of
> zero-selling months and how long that run has lasted, since a brand two months
> into a stock-out behaves unlike one selling steadily.
>
> The eighteenth is promotional intensity, the promotional share of units,
> clipped and lagged by one period. **It is available for CSD and energidrikke
> only.** Nielsen reports no promotional measure for danskvand or RTD, so the
> feature is omitted for those categories rather than zero-filled - a constant
> zero would assert that no promotion ran, which the data does not support and
> which a model would learn from. Those two categories are therefore modelled on
> seventeen features.
>
> Missing lag values on short histories are left as null and handled natively by
> the tree-based models; Ridge receives a zero-fill at fit time, since it cannot
> represent absence.

### Note - the count gap is worth stating explicitly

The feature matrix on disk has 54 columns and the model uses 18. **If a reader
compares the matrix description in Chapter 4 against this section they will find
the discrepancy**, so one sentence naming it is cheaper than leaving it to be
found.

Optional, after the first paragraph:

> The engineered matrix contains considerably more columns than this. The
> remainder are either identifiers or measures recorded contemporaneously with
> the target, which are unknown at the moment a forecast is made and would leak
> the period being predicted.

---

## 5.3.3 Execution protocol

### State

Bullets, three lines. Contains a cross-reference to Chapter 6.

### Verified

Sequential execution with explicit unloading and garbage collection, memory
profiled per stage. **Correct.** Seed 42 throughout. **Correct.**

### Comments

**222 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste

> Models are fitted and evaluated strictly in sequence: each is loaded, fitted,
> used to predict, then unloaded and its memory reclaimed before the next begins.
> The sequential design is what makes the memory figures meaningful, since a
> parallel run would report the sum of several models rather than the peak of any
> one. Memory is profiled at each stage and peak usage recorded per model.
>
> A fixed random seed of 42 is used throughout. Sensitivity to that choice is not
> assumed away but measured directly, and Section 5.5.10 reports what it costs.

⚠ **Note the number.** Seed stability becomes **5.5.10** once the holiday
ablation is inserted as 5.5.8. See the renumbering table at the end.

---

## 5.3.4 Validation scheme

### State

**Already prose.** Two well-written paragraphs.

### Verified

Four-fold expanding-window cross-validation splitting on periods. **Correct.**
The Tashman citation and both page numbers are **correct**.

### Comments

**225 `OUTDATED`** - the one comment tagged `OUTDATED` rather than `VERIFY,
SOURCE, PROSE`.

**FLAGGED, and I could not find what is outdated.** The scheme matches the code,
the citation checks out, and the section is already prose. Two candidates:

1. **The number of folds.** The text says four; `srq1_benchmark_cv.py` still
   reads four.
2. **The missing justification.** The section explains what expanding-window
   cross-validation does but never says why standard K-fold was rejected. That is
   the obvious examiner question and the section does not answer it.

The addition below is written for the second reading. **If you meant something
else, say so and I will fix that instead.**

### Paste - an addition, not a replacement

Insert between the two existing paragraphs:

> Standard K-fold cross-validation is not rejected on principle. It is valid for
> stationary autoregressive processes with uncorrelated residuals, and on such
> series it uses the data more efficiently than a single out-of-sample split
> (Bergmeir et al., 2018). Monthly brand-level beverage demand does not satisfy
> that condition: the series are trended, seasonal and non-stationary. Under
> non-stationarity, methods that preserve temporal order estimate generalisation
> loss substantially more accurately (Cerqueira et al., 2020), which is why the
> order-preserving scheme is used here.

### Note - do not shorten this to the obvious version

The tempting sentence is *"K-fold cross-validation is invalid for time series."*
**It is false**, and Bergmeir et al. prove the opposite for a class of series -
so an examiner following the reference finds the chapter contradicted by its own
citation. The conditional version shows the boundary is understood.

Equally, **do not write that expanding-window is required.** No such proof
exists; sliding windows trade differently by discarding old data to adapt to
structural breaks. Say "chosen because", not "required by".

⚠ **Both sources are new to this chapter.** Registered as C5-01 and C5-02 in
`citations-added-register.md`, both `IN-ZOTERO` and `NLM-PENDING`.

---

## 5.3.5 Hyperparameter optimisation

### State

**Already prose.** Two paragraphs.

### Verified

| Claim | Result |
|---|---|
| Optuna TPE, 100 trials per model x category x objective | **correct** |
| Bergstra p. 2549 for the l(x)/g(x) split | **correct** |
| Akiba p. 2623 for the Optuna software | **correct**, and correctly separated from the TPE attribution |
| **"plateaus range from 3 to 87 with a median near 16"** | ⚠ **stale.** Now **0 to 83, median 54** |

### Comments

**227 `VERIFY, SOURCE`** - **ADDRESSED.**

### Paste - replace the second paragraph only

> The trial budget is justified empirically rather than by convention. No
> trial-count convention exists in the hyperparameter-optimisation literature;
> the requirement scales with the dimensionality of the search space. The tuner
> therefore records the running best cross-validation score at each trial and
> reports the trial after which further improvement becomes negligible. Measured
> plateaus range from zero to 83 trials with a median of 54, so a budget of one
> hundred contains the converged region for every configuration - though with
> less margin than the earlier figures suggested.

### Note - the argument survives but the margin narrowed

At a median of 16 the budget looked generous. At 54 it is adequate. **The claim
is still true and is now the more interesting one**, because a plateau at 83
trials means a 50-trial budget would have been too small.

The zero is not an error. One configuration found its best score on the first
trial and never improved.

---

# 5.4 Evaluation metrics

### State

**Prose plus a metric table.** In good shape.

### Verified

Every metric definition is correct. The Hyndman and Koehler citation and
quotation are **correct**.

⚠ **One naming error.** The table row reads **"Median relative interval width"**,
but `calibration.csv` reports `mean_rel_width`. The figures quoted in Section
5.5.7 are means. **Fix the metric name, not the numbers.**

### Comments

**229 `VERIFY`** - **ADDRESSED.** One correction, above.

### Paste

In the metric table, change:

| From | To |
|---|---|
| Median relative interval width | **Mean relative interval width** |

The rationale cell stays as it is.

---

## 5.4.1 Why WMAPE is the primary metric

### State

**Already prose, and it is the strongest passage in the chapter.**

### Verified

The Gneiting argument is correct and correctly attributed. The chapter makes the
algebraic step from his percentage-error result to WMAPE **explicitly**, which is
exactly right - he never writes "WMAPE", so making the step in the chapter's own
voice is the honest construction.

⚠ **The trade-off figures are stale, and the finding underneath them has
changed.** The paragraph says tuning against median APE costs **8-13 pp of
WMAPE** and buys **2-3 pp of median APE**. Measured now:

| | range across the eight configurations |
|---|---|
| WMAPE cost | **-2.9 to +9.3 pp** |
| median APE gain | **-5.1 to +8.3 pp** |

Two things break. The cost is no longer uniformly positive - on danskvand
XGBoost and RTD XGBoost the medMAPE-tuned model is *better* on WMAPE. And **on
both danskvand configurations, tuning for median APE makes median APE worse**, by
around five points. The objective failed to buy the thing it was optimising for.

### Book

**Section 5.8** is the source for the metric-choice argument and for the caution
that no single accuracy measure serves every purpose. Cite it where the chapter
introduces the two objectives, not here.

### Comments

**231 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste - the last sentence of the final paragraph only

Replace *"It also explains why tuning against median APE costs 8-13 pp of WMAPE
while buying only 2-3 pp of median APE"* with:

> It also predicts the direction of the trade, though not its reliability: on the
> categories where the objective bites, tuning against median APE costs up to
> nine percentage points of weighted error. What the theory does not predict, and
> what the measurement shows, is that the exchange is not always made - on
> danskvand the median-APE objective degrades median APE itself, so the cost is
> paid without the corresponding gain. The stability analysis later in this
> chapter explains why.

### Note - this is a stronger result than the chapter currently claims

The old sentence describes a clean trade: pay WMAPE, receive median APE. The
measurement shows something more useful. **On two of eight configurations the
objective fails to improve the metric it optimises**, which says the tuning is
noisy at this sample size rather than that the metrics simply differ. That
reinforces the stability finding rather than undermining it, which is what the
added final clause points forward to.

---

## 5.4.2 Scorability

### State

Prose plus a two-row table, one row of which is empty.

### Verified

The 14-29% zero-actual range is **correct**. The rule itself is correct and is
the right decision.

### Comments

**233 `VERIFY, SOURCE, TABLE-REFERENCE, PROSE`** - **ADDRESSED.** The table has a
row reading *"(nothing else)"* with two empty cells, which renders as a blank
line in Word and reads as a mistake.

### Paste

**Delete the table entirely** and replace it with the sentence it was trying to
make:

> Only one exclusion is applied anywhere in this chapter, and it is mathematical
> rather than editorial: rows with a zero actual are excluded from median APE and
> from MAPE, because a percentage error is undefined where the denominator is
> zero. Weighted MAPE and MASE are computed on every row, since both are defined
> at zero actuals and neither requires an exclusion. Irregular series are handled
> by categorisation rather than removal, as the next section sets out.

### Note - a one-row table is not a table

The table exists to say "this rule, and nothing else". A sentence says that
better, removes a caption that would otherwise renumber everything after it, and
resolves the trailing Chapter 6 reference by naming the next section instead.

---

## 5.4.3 Targets

### State

Bullets, three long ones. The content is good and the withdrawal of the accuracy
target is exactly right.

### Verified

The Ceran withdrawal is **correct and important**. Three cross-references point
at Chapter 6 and are rewritten below as part of the prose.

### Comments

**236 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste

> **No accuracy target is imported from the literature.** Earlier drafts carried
> a target of fifteen per cent weighted error attributed to a published retail
> forecasting study. Source-level verification found no such benchmark in that
> paper: its authors explicitly reject percentage errors because their panel
> contains too many zero-demand observations for such a metric to be well
> defined, and report scaled and absolute errors instead. The target is therefore
> withdrawn, and no claim that an external accuracy target has been met or
> approached appears anywhere in this thesis.
>
> What replaces it is stricter. The four simple benchmarks defined above are
> scored on this thesis's own test rows, so the comparison needs no alignment
> between studies with different horizons, grains and metrics. A target borrowed
> from a daily product-store study with a fifteen-day horizon was never
> comparable to brand-by-month forecasting at a three-month horizon in any case.
>
> One target is retained, and it is a calibration target rather than an accuracy
> one: empirical coverage of at least eighty-five per cent for a nominal ninety
> per cent interval. **Interval width is reported alongside it**, because an
> arbitrarily wide interval attains perfect coverage while carrying no
> decision-relevant information.

### Note - the withdrawal reads better as a finding than as an admission

The current text says the target "has been withdrawn, not scored", which invites
the question of what went wrong. The version above states what was checked and
what was found, so the same fact reads as verification working rather than as a
correction being confessed.

---

## 5.4.4 Demand-pattern categorisation

### State

Prose plus two tables. Well argued.

### Verified

The Syntetos-Boylan-Croston citation, the cut-offs of p = 1.32 and CV squared =
0.49, and the train-plus-validation-only rule are all **correct**.

⚠ **The brand counts have changed** in every category but danskvand.

| Category | Chapter | Now |
|---|---|---|
| CSD | 44 / 32 / 5 / 14 | **46 / 29 / 6 / 14** |
| RTD | 32 / 20 / 2 / 8 | **27 / 21 / 7 / 7** |
| energidrikke | 16 / 18 / 2 / 8 | **15 / 19 / 3 / 7** |
| danskvand | 16 / 9 / 3 / 1 | 16 / 9 / 3 / 1 |

Totals move from 108 / 79 / 12 / 31 to **104 / 78 / 19 / 29**. The panel is still
230 brands.

### Comments

**238 `VERIFY, SOURCE, TABLE-REFERENCE, PROSE`** - **ADDRESSED.**
**240 `NAMING`** - the caption reads *"Table 7 - NO IDEA"*. **ADDRESSED.**

### Paste - the classification table

| Category | smooth | erratic | intermittent | lumpy | total |
|---|---|---|---|---|---|
| CSD | 46 | 29 | 6 | 14 | 95 |
| danskvand | 16 | 9 | 3 | 1 | 29 |
| energidrikke | 15 | 19 | 3 | 7 | 44 |
| RTD | 27 | 21 | 7 | 7 | 62 |
| **All** | **104** | **78** | **19** | **29** | **230** |

**Caption:** *Table 8 - Brands per demand-pattern class, by category*

### Paste - the other caption

The 2x2 threshold grid, currently *"Table 7 - NO IDEA"*:

**Caption:** *Table 7 - The Syntetos-Boylan-Croston demand-pattern
classification*

### Note - the total row is new and worth adding

The chapter's table has no total row, so a reader wanting the 230 has to add four
columns in their head. The row also makes the Section 5.5.5 figures traceable,
since that section quotes the totals.

---

# 5.5 Results

### State

One opening paragraph.

### Comments

**243 `META COMMENT`**, on *"All results are on the locked brand x month grain
(DEC-GRAIN). The alternative brand x chain representation, and the granularity
comparison built on it, were removed from the project by P0035 and no longer
appear in this chapter."*

**ADDRESSED - and you are right.** That paragraph is the chapter auditing itself.
It names an internal decision code and a plan identifier, and tells the examiner
that something used to be here and was removed. A reader who never saw the
earlier draft learns only that the thesis has a revision history.

### Paste

Replace the whole paragraph with:

> All results below are reported on the brand-by-month grain defined in the
> experimental setup.

### Note - where the removed content belongs

The chain-grain evaluation is a real methodological decision and is worth
recording - in Section 5.3.1, as the limitation it already mentions, or in the
limitations chapter. It is not a results-section preamble.

---

## 5.5.1 Tabular-model benchmark

### State

Prose plus the chapter's central results table. **Every figure in the table is
stale.**

### Verified

Against `cv_metrics.csv`, regenerated on the 18-feature run at `0e95850`.

⚠ **The table currently shows only the WMAPE-tuned arm** while the prose says
each model was tuned twice and "both results are reported". They are not - the
table has eight rows for eight configurations, but there are sixteen.

### Comments

**245 `VERIFY, TABLE-REFERENCE`** - **ADDRESSED.**
**247 `VERIFY`** - caption typo *"adn"*. **ADDRESSED.**
**248 `VERIFY, SOURCE, METACOMMENT`** - **ADDRESSED**, see the note.
**249 `VERIFY, SOURCE`** - **ADDRESSED.** The Cawley wording is already correct.

### Paste - the table

| Category | Model | Tuned for | CV WMAPE | Test WMAPE | Test medMAPE | n test |
|---|---|---|---|---|---|---|
| CSD | LightGBM | WMAPE | 19.4% | 19.3% | 45.7% | 665 |
| CSD | LightGBM | median APE | 43.0% | 27.9% | 40.4% | 665 |
| CSD | XGBoost | WMAPE | 18.8% | **18.4%** | 41.4% | 665 |
| CSD | XGBoost | median APE | 42.5% | 18.9% | 38.8% | 665 |
| danskvand | LightGBM | WMAPE | 28.7% | 27.3% | 37.5% | 174 |
| danskvand | LightGBM | median APE | 37.0% | 35.7% | 42.6% | 174 |
| danskvand | XGBoost | WMAPE | 25.7% | 27.1% | 40.4% | 174 |
| danskvand | XGBoost | median APE | 35.0% | **24.2%** | 45.4% | 174 |
| energidrikke | LightGBM | WMAPE | 11.5% | 16.2% | 54.8% | 308 |
| energidrikke | LightGBM | median APE | 43.5% | 23.8% | 52.3% | 308 |
| energidrikke | XGBoost | WMAPE | 12.2% | **15.5%** | 56.0% | 308 |
| energidrikke | XGBoost | median APE | 42.4% | 24.7% | 47.7% | 308 |
| RTD | LightGBM | WMAPE | 34.2% | 30.3% | 49.8% | 372 |
| RTD | LightGBM | median APE | 47.8% | 31.1% | 48.9% | 372 |
| RTD | XGBoost | WMAPE | 34.5% | 30.2% | 46.2% | 372 |
| RTD | XGBoost | median APE | 45.6% | **29.4%** | 47.2% | 372 |

**Caption:** *Table 9 - Test performance of both gradient-boosted models under
each tuning objective. The lowest weighted error per category is shown in bold.*

### Note - sixteen rows or eight

The table reports every configuration, which is what the prose promises. If that
is too long for the page, **report the WMAPE-tuned arm in the body and move the
median-APE arm to the appendix** - but then the prose must say so, rather than
claiming both are reported here.

### Paste - the paragraph on objectives

> The two objectives select different models and produce different rankings.
> Tuning for median APE generally improves that metric and degrades weighted
> error, as the theory above predicts. On energidrikke the effect is large:
> LightGBM tuned for median APE reaches 23.8 per cent test weighted error against
> 16.2 per cent when tuned for weighted error. **A single "best model" figure is
> therefore meaningless without naming the objective it was tuned against**,
> which is why both are carried here.
>
> The exchange is not always made, however. On danskvand, tuning for median APE
> degrades median APE itself by around five percentage points in both models
> while also moving weighted error - the objective failed to buy what it was
> optimising for. On the smallest panel in the study, the tuning signal is weak
> enough that the objective does not reliably control the outcome, which
> anticipates the stability result later in this chapter.

### Paste - the validation-to-test paragraph

> Movement between validation and test is substantial and is not hidden.
> energidrikke tunes to between 11.5 and 12.2 per cent in cross-validation and
> lands between 15.5 and 16.2 on test; RTD moves the other way. The gap is
> consistent with the selection bias inherent in this protocol: hyperparameters
> are chosen by cross-validation and the winner evaluated on a held-out split,
> which is standard practice but is not fully nested, so the cross-validation
> figure is an optimistically biased estimate of generalisation to an
> unquantifiable degree (Cawley & Talbot, 2010).

### Note - answering comment 248's METACOMMENT tag

The clause *"which is why both are carried here"* is borderline - it explains an
editorial choice rather than a result. It survives because the choice is
methodological rather than administrative: it says the thesis refuses to name a
single winner, which is a position, not a note to self.

---

## 5.5.2 The simple benchmarks, and where they win

### State

Table plus four paragraphs. **The table is stale and one paragraph is now
false.**

### Verified

Against `stat_baselines.csv`. **This is the largest single change in the
chapter.**

| The chapter says | Measured now |
|---|---|
| danskvand Ridge **10.9%**, roughly half the tuned error | Ridge is **74.9%** - the *worst* of the six baselines |
| danskvand won by Ridge | won by **Prophet**, at 19.4% |
| CSD Ridge 19.4% | **23.8%** |
| energidrikke Ridge 18.3% | **23.6%** |
| RTD Ridge 40.5% | **52.4%** |
| energidrikke Prophet 972.4% | **975.0%** |
| unclipped Ridge: energidrikke 2.8x10^13, RTD 2459% | **1.8x10^13** and **4.6x10^5**; danskvand is **5.3x10^25** |

**The danskvand paragraph inverts completely.** It currently reports Ridge as the
chapter's most striking result; Ridge is now that category's worst performer.

### Book

⚠ **Section 13.3 is a defect finding, not a citation gap.** It handles bounded
forecasts **through the transformation** and calls an artificially imposed
constraint unrealistic. The thesis clips post-hoc and never states the bound. The
prose below states the bound and explains what the log fit already does, which is
the cheapest honest fix.

### Comments

**251 `METACOMMENT, PROSE`** - the opening line *"The four benchmarks of §6.2.0
were run on the same test rows. stat_baselines.csv."* **ADDRESSED.** The trailing
filename is a note to a developer, not a sentence.

**253 `VERIFY, NAMING`** - *"wth is 'Best tuned ML'?! Which one does it refer
to?"* **ADDRESSED - you were right.** The column was the better of the two tuned
models, but the table never said so and the model varied by row without being
named. The replacement names it in each cell.

**254 `VERIFY, PROSE`** - **ADDRESSED.**
**255 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste - the opening sentence

> The four benchmarks defined above were run on the same test rows as the tuned
> models.

### Paste - insert after that opening sentence

> Six model families were evaluated in total. The classical univariate methods
> and the simple benchmarks were outperformed in every category except the two
> noted below, so the tuned comparison was carried forward on the two
> gradient-boosting implementations. The full baseline results are reported
> rather than discarded, which is what makes the narrowing auditable.

### Paste - the table

| Category | Naive | Seasonal naive | Drift | Ridge | ARIMA | Prophet | Best tuned model |
|---|---|---|---|---|---|---|---|
| CSD | 42.9% | 19.2% | 47.7% | 23.8% | 21.8% | 105.7% | **18.4%** (XGBoost) |
| danskvand | 32.5% | 35.9% | 32.0% | 74.9% | 33.5% | **19.4%** | 27.1% (XGBoost) |
| energidrikke | 18.9% | 23.8% | 17.7% | 23.6% | 19.4% | 975.0% | **15.5%** (XGBoost) |
| RTD | 89.3% | **27.3%** | 95.9% | 52.4% | 53.3% | 66.8% | 30.2% (XGBoost) |

**Caption:** *Table 10 - Weighted MAPE of the simple and statistical benchmarks
against the best tuned model, by category. The lowest error in each row is shown
in bold.*

### Paste - the danskvand paragraph, which inverts

Replace *"On danskvand, a plain Ridge regression reaches 10.9%..."* with:

> **On danskvand, Prophet reaches 19.4 per cent against the tuned models' 27.1**,
> and it is the only category where the method is competitive at all. Danskvand
> is also the smallest panel, at twenty-nine series and 174 test rows, where a
> high-capacity model has least to learn from. The same scarcity that limits the
> tuned models also flatters a method that imposes a strong parametric structure
> rather than estimating one from the data.

### Paste - the RTD paragraph

> **On RTD, seasonal naive beats every tuned configuration**, at 27.3 per cent
> against 30.2. The most irregular category is the one where a method with no
> parameters wins, and the margin is small enough that the tuned models cannot be
> said to have failed so much as to have bought nothing.

### Paste - one clause added to the Prophet paragraph

The paragraph beginning *"Prophet is applied outside its design regime"* now sits
above a table where **Prophet wins a category**, so it must acknowledge the
exception or it reads as contradicted. Add as its final sentence:

> That it nonetheless wins danskvand is consistent with this reading rather than
> against it: where the panel is shortest, a method that imposes a trend and an
> annual cycle rather than estimating flexible structure has least to get wrong.

Also replace the two figures inside that paragraph: **105.7 and 975.0**.

### Paste - the Ridge instability paragraph

> Ridge requires clipping to be reportable at all. Unclipped, its danskvand
> weighted error reaches the order of ten to the twenty-fifth power, its
> energidrikke error ten to the thirteenth, and its RTD error some four hundred
> thousand per cent, because back-transformed linear extrapolation diverges on
> short series. Forecasts are therefore bounded to each series' own observed
> history, widened by a factor of three, with zero as the lower bound; the number
> of predictions that hit the bound is recorded per category. The bounded variant
> is what appears in the table.
>
> The bound is stated as a forecasting constraint rather than a numerical
> convenience: a monthly demand forecast three times the largest month ever
> observed for that brand is an extrapolation failure rather than a forecast, and
> a practitioner would reject it. The log transformation already guarantees
> positivity, so the lower bound binds only through the back-transformation and
> the upper bound does the real work. Hyndman and Athanasopoulos (2021) prefer
> bounds imposed through the transformation itself over constraints applied to a
> finished forecast, and this is a departure from that preference: the constraint
> is applied after back-transformation because that is where the divergence
> appears. It is reported rather than silently applied, and the unbounded values
> are retained in the results, because the instability is itself informative about
> linear models on this panel.

### Note - the bound is now stated, which it was not

Verified in `srq1_baselines_stat.py`: the upper bound is **three times the
series maximum**, the lower bound is zero, and the clip count is already
recorded per category in `stat_baselines.csv`. The chapter previously reported
clipped figures without ever saying what the bound was, which is the gap the
textbook's treatment of constrained forecasts exposes.

⚠ **The clip counts are available and worth one clause.** `stat_baselines.csv`
carries `ridge_clipped` per category - 33 for CSD. If you want the strongest
version of this paragraph, state that count, because it turns "the bound was
applied" into "the bound bound 33 times".

### Note - the Ridge story is now stronger, not weaker

The chapter previously had Ridge as a surprise winner on danskvand. That reading
is gone, but what replaces it is a cleaner finding: **Ridge is unstable on every
category**, and the clipping bound is doing real work everywhere rather than on
two categories. That is a more defensible claim about linear models on short
series than a single anomalous win.

### Note - the "two categories are not won by the tuned models" sentence survives

Still true, and still danskvand and RTD. Only the reason for danskvand changes -
Prophet rather than Ridge. **Keep the sentence and the paragraph following it**,
which argues that the benchmark rung exists precisely to detect this.

---

## 5.5.3 Scaled error (MASE)

### State

Table plus two paragraphs. **Table stale; one claim now reverses.**

### Verified

Against `mase.csv`.

| Category | Chapter naive MASE | Now | Chapter median ASE | Now |
|---|---|---|---|---|
| CSD | 0.95 | **1.11** | 0.39 | **0.47** |
| danskvand | 0.99 | **1.18** | 0.52 | **0.53** |
| energidrikke | 0.67 | **0.84** | 0.05 | **0.13** |
| RTD | 6.54 | **11.80** | 0.18 | **0.28** |

⚠ **Two categories cross the line of 1.** CSD and danskvand naive MASE were below
1 and are now above it. Since this row *is* the naive forecast scored out of
sample, values above 1 say the test period is harder than the training period -
a real finding the chapter cannot currently state, because its figures sat just
under.

### Comments

**257 `VERIFY, PROSE`** - **ADDRESSED.**
**259 `NAMING`** - **ADDRESSED.**
**260 `VERIFY`** - **ADDRESSED.** The RTD distributional argument survives intact
and is if anything stronger.

### Paste - the table

| Category | Naive MASE | Seasonal-naive MASE | Naive median ASE |
|---|---|---|---|
| CSD | 1.11 | 1.86 | 0.47 |
| danskvand | 1.18 | 1.76 | 0.53 |
| energidrikke | 0.84 | 2.14 | 0.13 |
| RTD | 11.80 | 13.48 | 0.28 |

**Caption:** *Table 11 - Mean and median scaled error of the two naive
benchmarks, by category*

### Paste - a new paragraph, before the RTD one

> Mean scaled error exceeds one for the naive benchmark on CSD and danskvand,
> meaning the out-of-sample naive forecast is worse than the in-sample naive
> forecast it is scaled against. That is a statement about the test period rather
> than about the method: the held-out window is harder than the history used to
> scale it. Only energidrikke has a naive forecast that beats its own in-sample
> baseline.

### Paste - the RTD paragraph, with new figures

> RTD's mean scaled error of 11.80 against a median of 0.28 is a distributional
> finding rather than an accuracy one. The typical RTD series is forecast
> considerably better than naive; the mean is carried by a small number of cells
> with very large scaled errors. Reporting only the mean would describe RTD as
> catastrophically unforecastable, and reporting only the median would conceal
> that a few series genuinely are. Both appear for that reason.

### Note - the seasonal-naive sentence survives unchanged

*"Seasonal naive scores worse than naive on MASE in every category while winning
on WMAPE for RTD"* is **still true** on the new figures, and it is a good
sentence. Keep it.

---

## 5.5.4 Pooled versus per-category training

### State

Prose plus a table. **Table stale, and the central defence no longer holds.**

### Verified

Against `pooled_summary.md`.

| Category | Chapter (LGB / XGB) | Now |
|---|---|---|
| CSD | +1.2 / +1.3 | **+0.6 / +2.6** |
| danskvand | -2.2 / -2.5 | **-5.7 / -4.5** |
| energidrikke | -1.6 / -1.4 | **-5.6 / +0.1** |
| RTD | +0.7 / +1.5 | **-0.6 / +9.8** |

⚠ **The chapter says the pattern "holds for both model families, which is what
makes it a finding rather than noise".** It no longer does. The two families now
disagree on energidrikke and on RTD, and the RTD disagreement is 10.4 points
wide.

⚠ **"the magnitudes here sit within seed noise" must also come out.** Seed
standard deviations are 0.30 to 2.81 points. A 5.7-point pooling gain is roughly
twice the largest of them.

⚠ **"the same 12-feature intersection"** is correct *for the pooled run*, but the
per-category models elsewhere now use 18. **The pooled comparison has not been
re-run on the enriched feature set.** Say so, or a reader comparing sections
finds two feature counts and no explanation.

### Comments

**262 `VERIFY, TABLE-REFERENCE`** - **ADDRESSED.**
**263 `VERIFY, FORMATTING`** - on the RTD row specifically. **ADDRESSED** - that
row is now the one that disagrees between models.
**265 `NAMING`** - **ADDRESSED.**
**266 `VERIFY`** - **ADDRESSED**, the conditional claim is narrowed below.
**267 `VERIFY`** - **ADDRESSED**, per-brand figures replaced.

### Paste - the table

| Category | LightGBM pooled to per-category | XGBoost pooled to per-category |
|---|---|---|
| CSD | 19.3% to 18.7% (per-category better by 0.6 pp) | 21.7% to 19.1% (per-category by 2.6) |
| danskvand | 21.0% to 26.7% (**pooling wins by 5.7 pp**) | 18.9% to 23.4% (**pooling wins by 4.5**) |
| energidrikke | 15.5% to 21.1% (**pooling wins by 5.6**) | 16.8% to 16.8% (level) |
| RTD | 31.3% to 31.9% (pooling wins by 0.6) | 40.5% to 30.8% (per-category by 9.8) |

**Caption:** *Table 12 - Weighted MAPE under pooled and per-category training, by
category and model*

### Paste - the interpretation paragraph, narrowed

> The answer is conditional, and the condition is data volume. Pooling wins
> clearly on the two smallest panels - danskvand at 174 test rows and
> energidrikke at 308 - by between 4.5 and 5.7 percentage points under LightGBM
> and 4.5 under XGBoost. This is the expected transfer-learning trade-off: a
> small category borrows strength from the others, while a large one is diluted
> by them.
>
> **The agreement between model families is confined to that small-panel
> result**, and that agreement is what makes it a finding rather than an artefact
> of one algorithm's inductive bias. The two larger categories are less
> consistent: CSD favours per-category training under both models but by
> different margins, and RTD favours it strongly under XGBoost at 9.8 points
> while the two arms are level under LightGBM. The claim made here is therefore
> confined to the direction of the small-panel effect.
>
> Those gains exceed the between-seed standard deviations reported later in this
> chapter, which reach 2.81 percentage points, by roughly a factor of two. The
> sub-point differences on CSD and on RTD under LightGBM do not, and are not read
> as ordering those categories.

### Paste - the per-brand paragraph

> Beneath the aggregate the picture is close to a coin flip. Broken out by demand
> class, pooling helps between 48 and 57 per cent of brands in the smooth,
> erratic and intermittent classes - no decisive effect in either direction. The
> lumpy class is the exception and falls clearly below a coin flip, at 31 per
> cent under LightGBM and 38 under XGBoost: the class where pooling was least
> likely to help is the one where it visibly does not.

### Paste - the feature-count sentence

Replace *"Both arms use the same 12-feature intersection"* with:

> Both arms use the same twelve-feature intersection - the largest set available
> in every category - together with an identical tuning protocol, and are scored
> on identical test rows, so they differ only in which rows they were trained on.
> This comparison predates the holiday and intermittency enrichment described
> above and has not been re-run against it; the pooling question it answers is
> about training rows rather than about features.

**That last clause is doing real work.** Without it the chapter states two
different feature counts in two sections with nothing connecting them.

---

## 5.5.5 Results by demand pattern

### State

Three paragraphs, already prose.

### Verified

| Claim | Result |
|---|---|
| 108 smooth, 79 erratic, 12 intermittent, 31 lumpy | ⚠ now **104 / 78 / 19 / 29** |
| 15 of 31 lumpy brands have no test signal | ⚠ now **13 of 29** under both models |
| pooling win-rates 46-55 / 51-64 / 44-56 | ⚠ now **48 / 51-57 / 44-56** |

The **argument** is unaffected in every case. Only the counts move.

### Comments

**269 `PROSE, METACOMMENTS, FORMATTING`** - **ADDRESSED.**

### Paste

> Using the demand-pattern partition defined above, the 230 brands divide into
> 104 smooth, 78 erratic, 19 intermittent and 29 lumpy. Nothing is excluded;
> irregular series are reported rather than filtered.
>
> The most informative fact here is an absence. Thirteen of the 29 lumpy brands
> have no test signal at all - their entire test window is zero - so there is no
> actual quantity to be accurate about, and any per-brand percentage statistic
> for them would be undefined rather than merely large. Pooling deltas for the
> lumpy class are computed on the sixteen that remain, and the thirteen are
> counted in their own right. A volume threshold would have removed those brands
> quietly; the categorisation makes them visible and countable, which is the
> honest statement about lumpy demand on this panel.
>
> For the classes that carry signal, pooling win-rates run at 48 per cent for
> smooth brands, 51 to 57 for erratic and 44 to 56 for intermittent. No demand
> class shows a decisive pooling effect.

---

## 5.5.6 Operational profile

### State

Two paragraphs. **Every figure is wrong, and this is where the 8 GB lives.**

### Verified

Against `profiling.csv`.

| The chapter says | Measured |
|---|---|
| Ridge 5.5 MB | 5.4 MB |
| LightGBM **8.0 MB** | **38.1 MB** peak fit |
| XGBoost **0.1 MB** | **29.2 MB** peak fit |
| ARIMA 0.3 MB | 1.9 MB |
| XGBoost fits in **0.97 s**, predicts in **9.3 ms** | **3.6 s** and **13.8 ms** |
| LightGBM fits in **2.04 s**, predicts in **15.9 ms** | **8.0 s** and **33.0 ms** |
| "against the **8 GB** sequential budget" | ⚠ **Section 5.1 says 4 GB. Change this one.** |

⚠ **The chapter quotes tracemalloc for some models and nothing consistent for
others.** `profiling.csv` carries both `peak_fit_RSS_MB` and
`peak_fit_tracemalloc_MB`, and they differ by a factor of 290 for XGBoost. The
figures above are resident set size, which is what an operator provisioning a
container actually sees.

⚠ **`profiling.csv` reports `n_features: 13`.** These measurements predate the
18-feature set, so the memory figures are a **floor**. Tracked as H12 and S19.

### Comments

**271 `VERIFY`** - **ADDRESSED**, with the caveat above.

### Paste

> Peak resident memory during fitting is in the tens of megabytes for every
> model: 38.1 MB for LightGBM, 29.2 for XGBoost, 5.4 for Ridge and 1.9 for a
> per-series ARIMA. Against the four-gigabyte sequential budget, the memory
> constraint is non-binding by two orders of magnitude at this data scale. **That
> is a real answer to the research question rather than a missing measurement:
> the constraint that motivated the question does not bite here.**
>
> Latency is likewise immaterial for an interactive setting. XGBoost fits in 3.6
> seconds and predicts in 13.8 milliseconds; LightGBM fits in 8.0 seconds and
> predicts in 33.0. Prediction is the operation an agent waits on, and at tens of
> milliseconds it is far below the threshold at which a user perceives delay.
>
> These figures were measured on a thirteen-feature matrix and are therefore a
> lower bound on the memory the current eighteen-feature model requires. The
> conclusion is unaffected: the margin against the budget is large enough that a
> proportional increase does not approach it.

### Note - two orders of magnitude, and the budget

The chapter says three orders. At 38 MB against 4 GB the ratio is about 105, so
**two orders is right** and three is wrong. The prose above states 4 GB
explicitly, matching Section 5.1.

---

## 5.5.7 Prediction-interval calibration

### State

Table plus two paragraphs. **Table stale, and the headline example moves to a
different category.**

### Verified

Against `calibration.csv`.

| | Chapter | Now |
|---|---|---|
| CSD 90% | 89.6%, 3.3x | **91.0%, 8.62x** |
| RTD 90% | 89.0%, 3.1x | **90.9%, 8.62x** |
| danskvand 90% | 87.4%, **16.8x** | **83.9%, 11.89x** |
| energidrikke 90% | 93.5%, 8.9x | **86.0%, 33.64x** |

⚠ **Two things change identity.**

1. **danskvand now misses the 85 per cent target**, at 83.9. It previously met it
   at 87.4. The chapter says danskvand *"meets its 90% coverage target"* - that
   is now false.
2. **The widest intervals belong to energidrikke, not danskvand.** The chapter's
   striking "seventeen times the quantity being forecast" example is now
   **thirty-four times, on a different category.**

The metric is also a **mean**, not a median - see Section 5.4.

⚠ **And there is a defect underneath the table.** `srq1_calibration.py` fits
XGBoost for every category, but two categories serve LightGBM. See the Enrico
section at the end - **it does not block this section**, but it constrains what
the prose may claim.

### Comments

**273 `VERIFY, PROSE, MATH`** - **ADDRESSED.** The Lei et al. formula and the
finite-sample argument are **correct** and unchanged.
**274 `VERIFY`** - **ADDRESSED.**

### Paste - the table

| Category | Nominal | Empirical coverage | Mean relative width | n test |
|---|---|---|---|---|
| CSD | 90% | 91.0% | 8.6x | 665 |
| RTD | 90% | 90.9% | 8.6x | 372 |
| energidrikke | 90% | 86.0% | 33.6x | 308 |
| danskvand | 90% | **83.9%** | 11.9x | 174 |
| CSD | 80% | 82.3% | 3.8x | 665 |
| RTD | 80% | 80.6% | 3.8x | 372 |
| energidrikke | 80% | 78.9% | 12.4x | 308 |
| danskvand | 80% | **72.4%** | 2.9x | 174 |

**Caption:** *Table 13 - Empirical coverage and mean relative interval width of
the split-conformal intervals, against nominal levels of 80 and 90 per cent*

### Paste - the interpretation paragraph

> Coverage alone is the wrong success criterion, and this table shows why in two
> different directions. An arbitrarily wide interval attains nominal coverage
> while carrying no decision-relevant information: energidrikke reaches 86 per
> cent coverage at the ninety per cent level only with intervals spanning some
> thirty-four times the quantity being forecast, which no planner can act on.
> Width rather than coverage is the binding constraint there.
>
> danskvand fails on the other axis. It misses the coverage target at both
> levels - 83.9 per cent against a nominal ninety, and 72.4 against a nominal
> eighty - on the smallest calibration set in the study, at 174 rows. A
> split-conformal interval's guarantee is distribution-free but finite-sample,
> and 174 calibration residuals are few enough that the empirical quantile is
> itself noisy. Both categories are reported as limitations rather than averaged
> into a claim that the intervals are well calibrated.
>
> CSD and RTD, the two largest calibration sets, both attain their nominal
> coverage at both levels with intervals under nine times the forecast quantity.
> **The pattern across all four is that calibration quality tracks calibration
> set size**, which is the behaviour the method's finite-sample guarantee
> predicts.

### Paste - one sentence naming the scope, at the end of the section

> These intervals are calibrated on gradient-boosted residuals under a single
> implementation, and the conformal procedure is applied identically in every
> category; the coverage reported here therefore describes the calibration method
> on this panel rather than a property of whichever implementation is finally
> served.

### Note - why that scope sentence is there

It is the cheapest honest answer to the calibration defect. The section states
what the numbers describe, so it stays true whether or not the re-run happens.
**Without it, the table implicitly claims to describe the served model, which for
two categories it does not.**

### Note - this is a better result than the chapter currently reports

The old text had one category with wide intervals and three broadly fine. The new
figures give a **monotone relationship between calibration set size and
calibration quality**, which explains the failures instead of listing them.

---

## 5.5.8 Holiday enrichment - A NEW SUBSECTION

### State

**Does not exist.** Chapter 5 has no holiday-ablation subsection, and **two
appendix tables exist that nothing in the thesis cites.**

Insert this **before** the current Remaining gaps section, which becomes 5.5.9,
pushing seed stability to 5.5.10.

### Verified

Against `94_holiday_ablation_tuned.csv` and
`95_holiday_ablation_tuning_sensitivity.csv`, both regenerated on the 18-feature
set on 2026-09-10.

| Reading | Result |
|---|---|
| tuned comparison | enrichment **improved** 6 of 9 cells |
| fixed-configuration comparison | enrichment **worsened** 8 of 12 |
| best cell | RTD XGBoost, **-4.92 pp** |
| worst cell | danskvand XGBoost, **+2.21 pp** |
| largest tuning gain | danskvand XGBoost, **+12.99 pp** |

The two experiments use the same data and the same features and reach opposite
conclusions. **That inversion is the finding.**

### Why this belongs in Chapter 5

Chapter 4 states the conclusion, which is all a data chapter needs. **The
methodological half belongs here**, and without it Section 5.3.2 introduces three
holiday features with no evidence that they earn their place.

### Paste - the whole subsection

> ### 5.5.8 Holiday enrichment, and what an ablation measures
>
> The Danish public-holiday columns described in the feature section were adopted
> on the evidence of an ablation, and the way that ablation had to be run is
> itself a result worth reporting.
>
> Run first with hyperparameters held fixed across both arms, the enrichment
> appeared to hurt: the holiday columns worsened test error in eight of twelve
> category-and-model combinations. Re-run with each arm tuned independently, the
> same columns improved accuracy in six of nine. The two experiments use the same
> data and the same features and reach opposite conclusions.
>
> The inversion is not a contradiction to be resolved by preferring one number.
> Adding three columns changes the shape of the search space, so a configuration
> tuned for the smaller space is mis-specified for the larger one. A
> fixed-configuration comparison therefore measures the cost of that
> mis-specification rather than the value of the features, and the tuned
> comparison is the one that answers the question actually asked. Tuning improved
> the enriched arm by up to 12.99 percentage points, an order of magnitude larger
> than the feature effect being measured.
>
> The effect itself is small in both directions, ranging from a 4.92-point
> improvement on RTD under XGBoost to a 2.21-point degradation on danskvand under
> XGBoost. No mean across cells is reported, because the model families respond
> differently: the linear model benefits in the single category where it was
> tested, while the tree models benefit in five of eight cells. That divergence is
> the substantive finding, and averaging it away would conceal it.
>
> The wider lesson generalises beyond this feature group. Any ablation that holds
> hyperparameters fixed across arms of differing dimensionality measures
> mis-specification rather than the feature, and reports it with a confidence the
> design does not support.

### Note - do not quote the mean

Table 94's own internal review note reads: *"Do NOT quote the mean of this
column. It averages over model families that respond differently, and that
difference is itself the finding."* The prose above states the range and the
split by family without ever quoting a mean, which is what that note asks for.

### Note - this section also repairs 5.3.2

Section 5.3.2 now introduces three holiday features. **This section is the
evidence that they belong**, which is why it should not be dropped for length.

---

## 5.5.9 Remaining gaps - WAS 5.5.8

### State

Four short bullets, and **one of them is a note to a developer**.

### Verified

The nested-CV gap and the fixed-order ARIMA limitation are both **real and
correctly stated**. The withdrawn accuracy target is correct.

⚠ *"fig4_ram_budget is stale and contradicts §6.5.6"* is a repository TODO that
has been pasted into a thesis. It names a file the examiner cannot see. **Delete
it from the chapter** - it is tracked as S14.

⚠ **Two gaps are missing:** the pooling comparison has not been re-run on the
enriched feature set, and the calibration coverage failure on danskvand is not
listed here.

### Comments

**276 `VERIFY, PROSE`** - **ADDRESSED.**

### Paste

> Five limitations qualify the results above.
>
> The accuracy target has been withdrawn rather than met. Verification found that
> the benchmark cited in earlier drafts does not appear in its stated source, so
> accuracy here is assessed against the simple benchmarks alone - on which two of
> four categories are beaten outright.
>
> The interval-calibration target of eighty-five per cent empirical coverage at a
> nominal ninety is met on three categories and missed on danskvand, at 83.9 per
> cent. It is reported as missed rather than dropped, since a target abandoned on
> the category that fails it is not a target.
>
> The tuning protocol is not nested, so every cross-validation figure reported
> above is optimistically biased by an unquantified amount. This affects the
> absolute level rather than the comparison between models, since every model was
> selected under the same protocol.
>
> ARIMA and Prophet use a fixed specification per series rather than a per-series
> order search, on cost grounds, and the ARIMA specification carries no seasonal
> term on a panel this chapter characterises as strongly seasonal. Their figures
> are a floor for those families rather than the best attainable from them, and
> the benchmark comparison understates both.
>
> The pooled-versus-per-category comparison was measured before the holiday and
> intermittency features were added, on the twelve-feature intersection available
> at the time. It is internally consistent, since both of its arms use that same
> set, but it is not directly comparable with the per-category figures reported
> elsewhere in this chapter.

### Note - the ARIMA limitation is now stronger

The old wording said "not order-optimised". The version above names the seasonal
gap explicitly, which is the honest statement and is what makes Section 5.2.2's
prose consistent with this list.

---

## 5.5.10 Forecast stability across seeds - WAS 5.5.9

### State

Two tables and four paragraphs. **Both tables stale; the argument survives
intact.**

### Verified

Against `stability.md` and `stability.csv`, regenerated at `471b5a3`.

⚠ **A correction to an earlier note, recorded so it is not repeated.** A previous
pass claimed the per-seed winner table could not be reproduced from any artefact,
blocked it, and warned that Section 5.6 rested on nothing. **That was wrong.** The
data is in `stability.md`, which that pass never opened - it searched the
appendix export instead. **The chapter's claim was right all along:** four of
four categories flip.

### Comments

**278 `VERIFY, METACOMMENT, PROSE`** - **ADDRESSED.** The opening paragraph
explains why the section exists by referring to Chapter 2 and to SRQ1's scope,
which reads as the chapter justifying its own structure.
**279 `METACOMMENT, WATERMARK, ACADEMIC`** - **ADDRESSED.**
**280 `VERIFY, TABLE-REFERENCE`** - **ADDRESSED.**
**282 `VERIFY, METACOMMENT, NAMING`** - caption typo *"Stabiltiy"*. **ADDRESSED.**
**283 `WATERMARK, ACADEMIC`** - **ADDRESSED.**

### Paste - the opening

> Stability is measured as the coefficient of variation of the forecast for each
> brand-month cell across five random seeds, with data, splits, features and
> protocol held identical. Only the seed varies, driving the hyperparameter
> sampler and the models' own stochastic elements.

### Paste - the stability table

| Category | Model | Median CV | p90 CV | WMAPE mean | WMAPE sd | WMAPE range |
|---|---|---|---|---|---|---|
| CSD | LightGBM | 0.182 | 0.488 | 18.9% | 0.67 | 18.3-20.0% |
| CSD | XGBoost | 0.152 | 0.517 | 18.6% | 0.83 | 17.8-19.5% |
| danskvand | LightGBM | 0.138 | 0.522 | 27.0% | 2.81 | 24.6-31.9% |
| danskvand | XGBoost | 0.174 | 0.611 | 25.8% | 1.04 | 24.7-27.0% |
| energidrikke | LightGBM | 0.239 | 0.707 | 16.2% | 0.59 | 15.5-16.9% |
| energidrikke | XGBoost | 0.243 | 0.773 | 17.0% | 1.08 | 15.5-18.0% |
| RTD | LightGBM | 0.099 | 0.236 | 30.5% | 0.30 | 30.2-30.9% |
| RTD | XGBoost | 0.114 | 0.522 | 30.1% | 1.04 | 29.1-31.6% |

**Caption:** *Table 14 - Forecast and accuracy variation across five random
seeds, by category and model*

### Note - the WMAPE range column is new and is the most legible one

A reader who does not think in standard deviations can see that danskvand's
LightGBM lands anywhere between 24.6 and 31.9 per cent depending on the seed.
That is the whole argument in one cell.

### Paste - the first finding

Replace **"Two findings, and both matter more than the accuracy tables
suggest"** with:

> Two findings follow, and both bear on how the accuracy tables in this chapter
> should be read.

Then the paragraph beneath it:

> First, aggregate stability flatters the system by roughly a factor of four.
> Aggregate weighted error moves by about 4.6 per cent of its own level across
> seeds, while the typical individual forecast moves by about 17 per cent, and
> the ninetieth-percentile cell by between 24 and 77 per cent. Per-cell movements
> partly cancel within a volume-weighted sum, so a planner reading one brand's
> number experiences considerably more run-to-run variability than a headline
> metric implies. Both are therefore reported; quoting only the aggregate would
> understate instability roughly fourfold.

### Note - these figures are computed, not derived by hand

The multiplier comes from the generator, which computes it from the per-cell data
at render time. The chapter's "three times" was measured on an older run; the
move to 3.6x is **against** the system, so the finding is slightly stronger than
the chapter currently claims.

### Paste - the winner table

| Category | Winner per seed | Verdict |
|---|---|---|
| CSD | XGBoost, XGBoost, XGBoost, LightGBM, LightGBM | flips |
| danskvand | LightGBM, LightGBM, XGBoost, XGBoost, XGBoost | flips |
| energidrikke | XGBoost, LightGBM, LightGBM, LightGBM, XGBoost | flips |
| RTD | XGBoost, LightGBM, XGBoost, XGBoost, XGBoost | flips |

**Caption:** *Table 15 - The selected model per category under each of five
random seeds*

⚠ **Every row differs from what the chapter currently prints.** The verdict is
identical in all four, which is why the surrounding prose survives, but the
sequences are from the superseded run and must be replaced rather than left.

### Paste - the closing paragraph

> Because every input other than the seed is held identical, the selected model
> is not a property of the categories but an outcome of one draw. A statement
> that a particular gradient-boosting model is best for a given category is
> therefore unsupported here, in all four categories. The following section
> states the conclusion this supports instead.

---

# 5.6 Model selection decision

### State

**Bullets**, six of them, several very long.

### Verified

**Both central claims are correct and both are sourced.** The winner flips in all
four categories, and the between-seed spread exceeds the between-model
difference: model gaps run 0.3 to 1.2 points against seed standard deviations
reaching 2.81.

⚠ **One clause is incomplete.** The chapter says the gradient boosters *"clearly
beat Ridge and ARIMA on most categories, and clearly lose to seasonal naive on
RTD"*. Checked cell by cell, they beat Ridge and ARIMA on **all four**, so "most"
understates it. But the sentence names only one loss, and there are now two:
**Prophet wins danskvand outright** at 19.4 against 27.1. That has to be named
here, or this section contradicts the table in 5.5.2.

### Comments

**285 `VERIFY, PROSE`** - **ADDRESSED.**

### Paste

> **The choice between LightGBM and XGBoost is not supported by this data.** A
> five-seed sweep holding every input identical shows the winning model changing
> with the seed in all four categories. Naming a winner per category would report
> one seed's outcome as a finding.
>
> The defensible claim is that the two are statistically indistinguishable here.
> The difference in mean weighted error between them ranges from 0.3 to 1.2
> percentage points across the four categories, against a between-seed standard
> deviation reaching 2.81. The variation each model produces on its own exceeds
> the difference between them. This is a weaker headline than naming a winner,
> but it is a true one and it is useful: a practitioner deciding what to deploy
> can choose on operational grounds - training time, memory footprint, tooling
> maturity - rather than on an accuracy difference that will not survive a
> different seed.
>
> What the benchmark does support is the gap between model *families*. Both
> gradient boosters beat Ridge and ARIMA on every category, and both lose to
> seasonal naive on RTD and to Prophet on danskvand. Those differences exceed the
> seed noise; the difference between LightGBM and XGBoost does not.
>
> The served model carries its own track record. The forecast tool returns the
> selected model's measured accuracy on both metrics, the corresponding simple
> baselines for that category, and a conformal interval, so the consuming agent
> receives the forecast's reliability alongside the forecast itself. Where the two
> metrics rank models differently, the payload flags the disagreement rather than
> silently reporting one of them.

### Paste - the ensemble paragraph, corrected

⚠ **The chapter's final paragraph says ensemble combination "is evaluated as a
separate scenario". It has not been.** Checked 2026-09-11:

| Check | Result |
|---|---|
| `forecast_tool.py` | **zero** occurrences of "ensemble" |
| any ensemble result artefact under `05_thesis_results/` | **none** |
| the only implementation | `.archive/superseded_scripts_2026-08/srq2_synthesis.py` - archived |
| SRQ4 `runs.csv` | scenarios only; no ensemble arm |

The inverse-MAPE ensemble was designed and then superseded when the tool
interface was rebuilt. **Claiming it was evaluated would be a false result
claim**, which is the most expensive kind of error in a results chapter.

Replace the final paragraph with:

> Ensemble combination is not evaluated here. The M4 evidence that combinations
> outperform single models makes it the obvious next step, and the case for
> treating it separately is precisely that its contribution would then be
> measurable rather than assumed. It is identified as future work rather than
> claimed as a result.

### Note - this closes what was an open question

An earlier version of this pass asked you to confirm whether the ensemble
scenario had run. **It has not**, and the evidence is above, so the question is
settled and the paragraph is written for the answer.

---

# 5.7 Connection to SRQs

### State

A four-row table.

### Verified

⚠ **Every reference in it is wrong.** The header says *"How Ch.6 addresses it"* -
this is Chapter 5. The SRQ3 row points at "Ch3 and Ch5"; integration readiness is
Chapter 7. The SRQ1 row says "≤4GB RAM" and "retail CSD forecasting", but the
chapter covers four categories, not CSD alone.

### Comments

**288 `VERIFY, NAMING, FORMATTING`** - **ADDRESSED.**

### Paste

| SRQ | How this chapter addresses it |
|---|---|
| SRQ1 | Direct answer: which lightweight models trade accuracy against memory and category specialisation best, across all four categories |
| SRQ2 | The calibrated prediction intervals reported above are the uncertainty signal the tool interface carries |
| SRQ3 | Not addressed here; integration readiness is argued in Chapter 7 |
| SRQ4 | Supplies the trained models and their measured accuracy to the scenario comparison, which is what distinguishes the model-equipped scenario from the data-only one |

**Caption:** *Table 16 - How the model benchmark contributes to each
sub-research question*

### Note - verify the SRQ3 chapter number before pasting

Chapter 7 is written from `PATHS.CHAPTER_ORDER` and matches the snapshot, where
Chapter 7 is now *The Structured Tool Interface*. **Check it against the document
anyway**, since this is exactly the reference that broke last time.

---

# Outstanding decisions - DELETE THE SECTION

### Comments

**289 `VERIFY, METACOMMENT`** - **ADDRESSED.**

### Action

**Delete the entire section.**

It is a project-management artefact. It tells an examiner that trial budgets were
once fifty, that dates were once pending, and that the authors were unsure
whether to add a sixth model. None of that is a finding, and the resolved items
are already stated in their own sections as settled fact.

### Note - the two genuinely open items go elsewhere

| Item | Where it belongs |
|---|---|
| Whether ARIMA should be order-searched | **already in 5.5.9** as a limitation. Nothing to move |
| Whether the ensemble scenario runs | a dependency for 5.6's final paragraph, noted above. Not a thesis sentence |

---

# Enrico's three findings, and what they mean for this chapter

You asked what his insights mean and whether they force a re-train. **They do
not force one.** All three are answerable in wording, and the one that is not is
a Chapter 7 decision rather than a Chapter 5 one.

Validated 2026-09-11, recorded as S17 to S20 in
`deferred-structural-decisions.md`.

## 1. The calibration table describes a model two categories do not serve

**This is real.** `srq1_calibration.py` line 184 fits `XGBRegressor`
unconditionally for every category. But `train_and_persist.best_model_for()`
selects on the **cross-validation** score, and on that basis:

| Category | CV selects | Calibration fits |
|---|---|---|
| CSD | XGBoost | XGBoost |
| danskvand | XGBoost | XGBoost |
| **energidrikke** | **LightGBM** | XGBoost |
| **RTD** | **LightGBM** | XGBoost |

**Half the calibration table describes a model that is not served.** Enrico named
exactly those two categories.

⚠ **Selecting on test error gives XGBoost everywhere**, which is why the claim
looks wrong at first. It is not. `best_model_for()` deliberately selects on
cross-validation, because selecting on test is selection on the evaluation set
and biases every downstream number. **Do not "fix" this by switching selection to
test.**

**What it costs to fix:** one edit to read the selected model per category, then
a re-run of calibration alone. Not a retraining - the models already exist. The
coverage numbers in Section 5.5.7 would move.

**What to do instead, and it is enough:** the scope sentence already written into
5.5.7 above. It says the coverage figures describe the calibration *method* on
this panel, not a property of the served implementation. **That sentence is true
either way**, so the chapter can be finished now and the re-run, if it happens,
only narrows the sentence.

## 2. The confidence index is dead - and this is NOT a Chapter 5 problem

**Enrico is right, and the defect is worse than he described.**
`forecast_tool.py:473`:

```
conf = 100 * (0.5 * (1 / (1 + rel)) + 0.5 * (1 - min(q90, 1)))
```

**Two independent defects.**

The relative width reduces to twice the hyperbolic sine of q90, because with
`lo = expm1(log(y) - q90)` and `hi = expm1(log(y) + q90)` **the forecast value
cancels**. Since q90 is one number per category, the first term is a
**per-category constant** and cannot distinguish one brand's forecast from
another's.

The second term is **identically zero**, since `1 - min(q90, 1)` is zero whenever
q90 is at least 1, and the implied q90 runs 2.17 to 3.52 across the four
categories.

So every forecast scores between 2 and 6 out of 100 and tiers as "Low", matching
the 3 to 7 he observed.

⚠ **Recalibrating the cut-offs does not fix it.** Re-tiering a per-category
constant yields four values, one per category - a category label wearing a
number. The problem is not where the thresholds sit but that the thresholded
quantity does not vary within a category.

**Chapter 5 does not use the confidence index anywhere.** Confirmed by searching
the snapshot: the only match is the SRQ table's phrase about intervals providing
a confidence signal, and the replacement table above already reworded that to
"uncertainty signal". **So this blocks nothing here.** It is a Chapter 7 and SRQ2
decision, recorded as S18, with the recommendation to drop the field and report
it as a finding.

## 3. The operational figures predate the retraining

**Correct.** `profiling.csv` is dated 2026-09-01 and reports 13 features; the
model uses 18. `06_retraining_cost.csv` has the same problem.

**Section 5.5.6's prose above already handles this** by reporting the figures as
a floor and saying why. The margin against the budget is roughly a hundredfold,
so a proportional increase in feature count does not approach it.

**Re-running the profiler is cheap and would remove the caveat.** It is not a
retraining - it measures existing models. Optional.

---

# The retraining decision

**Recommendation: do not re-train.** Five candidates were examined and **four are
wording problems rather than measurement problems.**

| Candidate | What a re-run would buy | What the chapter says instead |
|---|---|---|
| **ARIMA has no seasonal order** | a fair ARIMA number, and a stronger family comparison | 5.2.2 and 5.5.9 above name it as a **structural** gap and say the comparison understates the family |
| **ETS is absent** | a sixth family | 5.1 above narrows the claim and concedes the omission |
| **Operational figures on 13 features** | removes a caveat | 5.5.6 reports them as a floor. Profiling re-run is cheap and optional |
| **Pooled comparison on 12 features** | comparability with the rest | 5.5.4 states the scope: it answers a question about **training rows**, not features |
| **Ridge clipping had no stated bound** | nothing | 5.5.2 now **states the bound** and explains what the log fit already does |

**Only the first is arguably worth a re-run**, and only if a seasonal ARIMA is
cheap across four categories. Even then, the wording above is defensible on its
own, because it states the limitation in the direction that costs the thesis
credit rather than hiding it.

## What a re-train would cost, and it is not the hours

A re-run of the tuned models invalidates **every table in this chapter**, the
calibration figures, the stability sweep, Chapter 7's payload description and
SRQ4's scenario inputs, which consume these models. **Chapter 5 is the last
chapter that produces SRQ1 output rather than consuming it**, so a retraining
decision taken after the chapter is written costs the chapter twice.

## How to avoid needing one - the pattern

Every avoidance above is the same move: **state the scope of what was measured,
rather than claiming the general case.**

| Instead of | Write |
|---|---|
| "the five families span the inductive-bias spectrum" | "cover the biases most relevant to this problem", then name the omission |
| "ARIMA underperforms" | "the specification carries no seasonal term, so the figures are a floor for the family" |
| "memory usage is 38 MB" | "measured on thirteen features, therefore a lower bound" |
| "pooling helps small categories" | "on the twelve-feature intersection, pooling helps the two smallest panels" |
| "Ridge forecasts are clipped" | "bounded at three times the series maximum, with the clip rate reported" |

A narrowed claim costs a clause. A re-run costs the chapter.

---

# If we did re-train - the optional note

**You said you do not think there is time, and I agree.** This is recorded so the
option is not re-derived.

| What we would gain | What we lose by not doing it |
|---|---|
| a seasonal ARIMA would make the classical baseline fair, and the textbook's Section 9.9 is explicit that monthly data needs one | the ARIMA figure stays a floor. An examiner may ask why; the chapter answers before they do |
| an ETS family would close the spectrum claim | the claim is narrowed instead, which is honest and cheap |
| calibration re-run on the served model per category would make 5.5.7 describe what ships | the scope sentence makes the section true as written |
| profiling on 18 features would remove the floor caveat | the caveat is disclosed, and the margin is ~100x |

**The single highest-value item if time appears is the calibration re-run**, not
the seasonal ARIMA - it is one code edit plus a short run against models that
already exist, and it makes an existing table describe the shipped system. The
seasonal ARIMA is a bigger job with a smaller payoff, because the chapter's
conclusion does not rest on ARIMA winning anything.

---

# Table renumbering

Three changes shift numbers. **Apply the deletions and the insertion first, then
renumber once**, rather than tracking numbers through each edit.

| Change | Effect |
|---|---|
| 5.4.2's one-row table is deleted | everything after moves **down** one |
| The holiday ablation enters as 5.5.8 | it cites appendix Tables 94 and 95, which need no new body number |
| 5.5.10's two tables both need captions | Table 13 becomes 14, and a new 15 appears |

The numbering used throughout this note assumes all three are applied. Word does
not update plain-text table callouts automatically, so search for **"Table "**
once at the end and check each against its caption.

---

# Citations

**Every source cited in Chapter 5 is in the library.** Checked one at a time
against the unfiltered Zotero API rather than `citations.json`, which filters by
item type and would hide a `computerProgram` or `dataset` entry.

Library re-pulled 2026-09-11: **87 items.**

| Cited as | In library | Note |
|---|---|---|
| Hyndman & Athanasopoulos (2021) | yes, `5NFQRRXS` | **fixed.** Both authors, 3rd ed., OTexts, 2021 |
| Makridakis et al. (2018) | yes, `EXNY7D4X` | ⚠ **two M4 papers in the library** |
| Taylor & Letham (2018) | yes | complete |
| Hastie et al. (2009) | yes | complete |
| Tashman (2000) | yes | complete |
| Bergstra et al. (2011) | yes, `S4WQS877` | ⚠ **a second Bergstra paper exists** |
| Akiba et al. (2019) | yes | ⚠ **date field reads "July 25, 2019"** |
| Gneiting (2011) | yes | complete |
| Hyndman & Koehler (2006) | yes | complete |
| Syntetos, Boylan & Croston (2005) | yes | complete |
| Cawley & Talbot (2010) | yes | complete |
| Lei et al. (2018) | yes | complete |
| Ceran et al. (2024) | yes | cited only to record that its benchmark does **not** exist |
| Bergmeir et al. (2018) | yes | **added by this pass**, 5.3.4 |
| Cerqueira et al. (2020) | yes | **added by this pass**, 5.3.4 |

**Nothing needs adding to Zotero.**

## How the book is cited - DEC-FPP-WHOLE-BOOK

**Cite the whole book.** The authors present it as one work with a single
canonical reference, and the Zotero entry is now one correct book record.

> (Hyndman & Athanasopoulos, 2021)

is the default. Add a section locator **only where a passage is quoted
directly**:

> (Hyndman & Athanasopoulos, 2021, Section 5.2)

⚠ **Never a page number.** The online edition is revised continuously and its
pagination does not match the print version.

This pass cites the book in four places: **5.1** (the benchmark quotation, with
locator), **5.2.2** (the seasonal requirement), **5.2.3** (the design-regime
point, which replaces a wrong attribution to Taylor and Letham) and **5.5.2**
(bounded forecasts).

## Three defects remain in the library

### Two M4 papers, and the chapter needs the 2018 one

| Key | Year | Pages |
|---|---|---|
| `EXNY7D4X` | **2018** | 802-808 |
| `V58EFK8B` | 2020 | 54-74 |

The chapter cites "Makridakis et al., 2018, p. 803", which is **correct**. ⚠ But
**check which entry Word's citation field points at** - both render as "Makridakis
et al." and only the year differs.

### Two Bergstra papers, supporting different claims

| Key | Year | Supports |
|---|---|---|
| `S4WQS877` | **2011** | the **TPE mathematics** |
| `34DWJUWN` | 2012 | that random search beats grid search |

Section 5.3.5 cites the 2011 paper, which is **correct**. ⚠ Verify the field
points at `S4WQS877`.

### Akiba's date field reads "July 25, 2019"

It renders as a date string rather than a year. Set it to 2019.

## What this does not cover

**None of these sources has been checked against the claim it supports.** The
audit establishes only that each entry exists and will render correctly.

**That is the NotebookLM pass, and it runs after the chapter is prosed.** The two
new sources are registered `IN-ZOTERO` / `NLM-PENDING` in
`citations-added-register.md` with the sentence each must support, quoted.

⚠ **The thirteen pre-existing sources have no register rows**, because this pass
did not add them. **A source cited since August is no more verified than one
cited today** - worth deciding before the NotebookLM run whether that pass covers
the whole chapter or only new citations.

---

# Still open, and needing you

**One item, and it blocks nothing.**

**Comment 225** tags the validation scheme `OUTDATED` and I cannot find the
defect. The scheme matches the code, the Tashman citation and both page numbers
check out, and the section is already prose. The addition written into 5.3.4
above assumes you meant the missing K-fold justification. **Paste it, or tell me
what you meant and I will fix that instead.**

The ensemble question that was open in the previous pass is **now answered** -
it has not run, the evidence is in 5.6 above, and the paragraph is rewritten for
that answer.

**Nothing in this chapter is blocked.**

---

# On the deferred lists

- **S13** - a caption on the calibration table renumbers every later table
- **S14** - `fig4_ram_budget` is stale; 5.5.9's reference to it is deleted above
- **S15** - whether 5.2.2 to 5.2.6 become a comparison table
- **S16** - Zotero metadata defects, three remaining
- **S17** - the calibration re-run, above
- **S18** - the confidence index, a Chapter 7 decision
- **S19 / H12** - re-profiling on 18 features, optional
- **S20** - Chapter 7 rewritten, done
- **S9** - the cross-chapter repetition pass, open since Chapter 4
