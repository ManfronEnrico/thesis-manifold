---
name: ch5-prose-pass-followup-01
description: NOTE - Chapter 5 worked sequentially, section by section from 5.1 to the end. Each section is verified against the repository, converted to prose where it is still bullets, and its comments answered in place.
snapshot: 2026-09-10_19-08_ch5-sequential-followup
category: workflow
applies-to: [chapter 5]
supersedes: [ch5-prose-pass.md]
created: 2026_09_10-19_30
updated: 2026_09_10-19_30
status: ready
---

# Chapter 5, section by section

**Work top to bottom.** Every section of the chapter appears below in document
order, whether or not it needs changing. Each one carries what it is now, what
the repository says, the prose to paste, and the comments it answers.

Verified at `303f00f`, snapshot `2026-09-10_19-08_ch5-sequential-followup`,
Zotero re-pulled the same minute: **87 items**.

## What this replaces, and why

`ch5-prose-pass.md` is superseded. It was organised as sixteen fixes, which meant
jumping around the document and applying edits out of order, and its F1 proposed
repairing twenty-one cross-references **inside bullet lists that this pass
deletes**. Repairing a reference in a bullet that becomes prose two fixes later
is wasted work.

**Cross-references are handled differently here.** Where a section becomes prose,
its references are rewritten as part of that prose, named rather than numbered:
*"the validation scheme described earlier"* rather than a section number. Numbers
move; the pass that renumbered this chapter on 8 September is why every reference
in it currently points at Chapter 6.

Where a numbered reference genuinely earns its place - pointing at a specific
table or a section a reader must actually turn to - it is written in full as
**"Section 5.5.9"**, not with a section sign.

## How each section below is laid out

| Field | What it holds |
|---|---|
| **State** | prose already, bullets to convert, or a table to replace |
| **Verified** | what was checked against the repository, and the result |
| **Comments** | the threads on that section, with a verdict each |
| **Paste** | the finished text, ready for Word |

A section with nothing wrong still appears, marked **no change**, so you can move
through the chapter without wondering whether it was skipped.

---

# 5.0 Chapter title

### State

Carries the placeholder line **"COULD USE A SUBTITLE"**.

### Comments

**199 `FORMATTING`** - *"Could use a subtitle for the chapter"*. **ADDRESSED.**

### Paste

Replace the placeholder line with the subtitle:

> Selecting a Forecasting Substrate Under Memory and Data Constraints

Delete the duplicated **"Chapter 5 | Model Benchmark & Selection"** heading -
it appears twice in the export, which usually means a stray heading-styled
paragraph sits above the real one.

---

# 5.1 Rationale for model selection

### State

**Bullets.** Four bolded fragments, one of which has lost its "(b)" label so the
criteria read (a), then an unlabelled clause, then (c) and (d).

### Verified

| Claim | Result |
|---|---|
| five model families plus four benchmarks | **correct** - ARIMA, Prophet, LightGBM, XGBoost, Ridge, and the four simple methods |
| "≤4 GB sequential RAM budget" | ⚠ **contradicts Section 5.5.6**, which says 8 GB. One of the two is wrong and the same figure must appear in both |
| Hyndman & Athanasopoulos quotation | **correct**, verified wording |
| M4: six pure ML entries, none beat Comb, one beat Naive2 | **correct** (Makridakis et al., 2018, p. 803) |

⚠ **Settle the RAM figure before pasting.** The chapter states two different
budgets in two sections. The prose below leaves the number as `[4 or 8]` for you
to fix in one place; everything else about the sentence holds either way.

### Comments

**201 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.** Sources verified as above, prose
below.

### Paste

> Five model families were selected to span the range of inductive biases
> available for this problem: classical statistical methods in ARIMA and Prophet,
> gradient boosting in LightGBM and XGBoost, and regularised linear regression in
> Ridge. Alongside them sit four parameter-free benchmarks - mean, naive,
> seasonal naive and drift.
>
> Four criteria governed the selection. The first is established empirical
> performance on retail and fast-moving consumer goods panels. The second is a
> fit within the [4 or 8] GB sequential memory budget that constrains the
> deployment target. The third is interpretability sufficient to support the
> scenario comparison in Chapter 8, where a forecast must be explained as well as
> produced. The fourth is diversity of inductive bias, so that the comparison
> measures something more than two implementations of one idea.
>
> The benchmark rung is required rather than decorative. Hyndman and
> Athanasopoulos (2021) define the four simple methods as the standard against
> which "any forecasting methods we develop will be compared ... to ensure that
> the new method is better than these simple alternatives". A forecasting result
> reported without them is unbenchmarked, and the first question it invites is
> whether it beats assuming that next month resembles last month.
>
> The empirical weight behind that requirement comes from the M4 competition, in
> which none of the six pure machine-learning entries outperformed the
> statistical combination benchmark and only one beat a seasonally adjusted naive
> forecast (Makridakis et al., 2018).

### Note - what changed and why

The lost "(b)" is restored by writing the criteria as sentences rather than as a
lettered list, which also removes the need for the labels.

"Interpretability sufficient for the SRQ4 scenario comparison" becomes "the
scenario comparison in Chapter 8". A reader meeting "SRQ4" in a results chapter
has to go and look it up; the chapter number is the thing they can act on.

---

# 5.2 Model descriptions

### State

Six subsections, all bullets, all carrying `VERIFY, SOURCE, PROSE`.

### Note - a structural option, not a requirement

These six read as six specification sheets with the same fields in a different
order each time. **A single comparison table plus one paragraph per model would
be shorter and easier to compare across.** That is on the deferred list as S15
and is not decided here - the prose below keeps the current structure, so it can
be pasted without waiting for that decision.

---

## 5.2.1 Simple benchmarks

### State

A formula table, then one bolded bullet.

### Verified

The four formulas match Hyndman and Athanasopoulos §5.2 exactly. The table stays
as it is.

### Comments

**204 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste

Keep the formula table and its caption. Replace the bullet beneath it:

> Seasonal naive is the decisive benchmark for this panel. Monthly beverage
> demand carries strong annual seasonality, which seasonal naive exploits with no
> parameters at all. It is therefore the direct test of whether a tuned model has
> learned that seasonality or merely fitted it, and it costs nothing to compute -
> which makes its absence harder to defend than its inclusion.

---

## 5.2.2 ARIMA

### State

Bullets. Contains a genuine limitation worth keeping.

### Verified

`statsmodels` SARIMAX at a fixed order, no automatic order search. **Correct** -
the environment has no `pmdarima`, confirmed against `requirements.txt`.

### Comments

**207 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste

> ARIMA enters as the classical univariate baseline, representing established
> time-series practice in the Box-Jenkins tradition. It is implemented through
> `statsmodels` as a seasonal ARIMA at a fixed order of (1,1,1), fitted per brand
> on log sales.
>
> The order is fixed rather than searched, because the automatic order-selection
> package was unavailable in the deployment environment. This is a stated
> limitation and bears directly on how the results should be read: the figures
> reported for ARIMA are a floor for the family rather than its best attainable
> performance. Peak memory is negligible at roughly half a megabyte. The model
> assumes stationarity and is univariate, so no promotional or calendar
> information reaches it.

---

## 5.2.3 Prophet

### State

Bullets. **Contains a claim that is now false.**

### Verified

⚠ **"No holiday calendar is supplied in this thesis" is wrong.** A Danish holiday
calendar was engineered on 2026-08-18 and three holiday columns now reach the
model: `days_in_month`, `n_holidays` and `non_holiday_days`. Verified in
`_features.py`.

**The claim is still true of Prophet specifically** - Prophet's own holiday
mechanism receives nothing - but as written it says the thesis has no holiday
data, which it does. The distinction has to be made explicit or Section 5.3.2
contradicts it two pages later.

### Comments

**209 `VERIFY, SOURCE, PROSE`** - **ADDRESSED**, and the holiday claim corrected.

### Paste

> Prophet is an additive decomposable model, y(t) = g(t) + s(t) + h(t) + e,
> combining trend, seasonality and holiday terms (Taylor & Letham, 2018). It was
> designed for forecasting at scale by analysts with domain rather than
> statistical expertise, and targets "piecewise trends, multiple seasonality,
> floating holidays".
>
> None of that machinery is available here. **Prophet's holiday component
> receives no input**: although this thesis does construct a Danish holiday
> calendar, its features are monthly counts rather than the dated events Prophet
> expects, and they are consumed by the tabular models instead. At month grain
> the multiple-seasonality machinery has nothing to fit either. Peak memory is
> the highest of any model considered, at roughly 50 to 100 megabytes, which
> remains acceptable against the budget.

---

## 5.2.4 LightGBM

### State

Bullets, four lines. Contains a cross-reference to §6.3.4.

### Verified

RAM figure of 18.7 MB. ⚠ **`profiling.csv` now reports 38.1 MB peak fit RSS and
23.0 MB tracemalloc.** Neither is 18.7. See Section 5.5.6 below - the same
figures are wrong there and are fixed once, in that section.

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
and stating it twice is how the two copies came to disagree. Same for XGBoost
below.

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
attribution above is what makes Ridge worth its place, and it is the same
one-variable-at-a-time logic the scenario ladder uses in Chapter 8 - worth the
three sentences.
---

# 5.3 Experimental setup

---

## 5.3.1 Grain and data split

### State

Bullets, five lines.

### Verified

| Claim | Result |
|---|---|
| grain is brand x month | **correct**, and locked as DEC-GRAIN |
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
| six lags, three rolling statistics, three calendar, one promotional | those thirteen, **plus three holiday and two intermittency columns** |
| (nothing about intermittency) | `zero_run_flag`, `zero_run_length` |
| **"No holiday calendar is used"** | ⚠ **false.** `days_in_month`, `n_holidays`, `non_holiday_days` |
| peak_month from the sales distribution | **correct**, and worth keeping - it is measured, not assumed |

**The model consumes 18 features where the chapter describes 13.** For danskvand
and RTD it resolves to 17, because those categories have no promotional measure.

⚠ **The "No holiday calendar is used" clause must come out.** It was true when
written and became false on 2026-08-18. It also contradicts Chapter 4, which
documents the holiday enrichment, and Section 5.5.8's ablation.

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

### Note - the count is worth stating explicitly

The feature matrix on disk has 54 columns and the model uses 18. That gap is not
an oversight: most columns are contemporaneous Nielsen measures that are unknown
at forecast time and would leak the target's own period. **If a reader compares
the matrix description in Chapter 4 against this section they will find the
discrepancy**, so one sentence naming it is cheaper than leaving it to be found.

Optional, after the first paragraph:

> The engineered matrix contains considerably more columns than this. The
> remainder are either identifiers or measures recorded contemporaneously with
> the target, which are unknown at the moment a forecast is made and would leak
> the period being predicted.

---

## 5.3.3 Execution protocol

### State

Bullets, three lines. Contains a cross-reference to §6.5.

### Verified

Sequential execution with explicit unloading and garbage collection, memory
profiled per stage. **Correct.** Seed 42 throughout. **Correct.**

### Comments

**222 `VERIFY, SOURCE, PROSE`** - **ADDRESSED.**

### Paste

> Models are fitted and evaluated strictly in sequence: each is loaded, fitted,
> used to predict, then unloaded and its memory reclaimed before the next begins.
> The sequential design is what makes the memory figures meaningful, since a
> parallel run would report the sum of several models rather than the peak of
> any one. Memory is profiled at each stage and peak usage recorded per model.
>
> A fixed random seed of 42 is used throughout. Sensitivity to that choice is not
> assumed away but measured directly, and Section 5.5.9 reports what it costs.

---

## 5.3.4 Validation scheme

### State

**Already prose.** Two well-written paragraphs.

### Verified

Four-fold expanding-window cross-validation splitting on periods. **Correct.**
The Tashman citation and both page numbers are **correct**.

### Comments

**225 `OUTDATED`** - this is the one comment tagged `OUTDATED` rather than
`VERIFY, SOURCE, PROSE`.

**FLAGGED, and I could not find what is outdated.** The scheme matches the code,
the citation checks out, and the section is already prose. Two candidates:

1. **The number of folds.** The text says four. If the tuner now runs a different
   number, that is the defect - but `srq1_benchmark_cv.py` still reads four.
2. **The missing justification.** The section explains what expanding-window
   cross-validation does but never says why standard K-fold was rejected. That
   is the obvious examiner question and the section does not answer it.

I have written the addition for the second reading below. **If you meant
something else by `OUTDATED`, say so and I will fix that instead.**

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
structural breaks. It is a defensible choice. Say "chosen because", not
"required by".

⚠ **Both sources are new to this chapter.** Registered as C5-01 and C5-02 in
`citations-added-register.md`, both `IN-ZOTERO` and `NLM-PENDING`.

---

## 5.3.5 Hyperparameter optimisation

### State

**Already prose.** Two paragraphs.

### Verified

| Claim | Result |
|---|---|
| Optuna TPE, 100 trials per model x category x objective | **correct** - the default in `srq1_benchmark_cv.py` |
| Bergstra p. 2549 for the l(x)/g(x) split | **correct** |
| Akiba p. 2623 for the Optuna software | **correct**, and correctly separated from the TPE attribution |
| **"plateaus range from 3 to 87 with a median near 16"** | ⚠ **stale.** Now **0 to 83, median 54** |

The plateau figures come from `cv_metrics.csv`, regenerated on the 18-feature
run. The median more than tripled.

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
trials means a 50-trial budget would have been too small - which is worth one
clause, since it retrospectively justifies a choice that would otherwise look
arbitrary.

The zero is not an error. One configuration found its best score on the first
trial and never improved.

---

# 5.4 Evaluation metrics

### State

**Prose plus a metric table.** In good shape.

### Verified

Every metric definition is correct. The Hyndman & Koehler citation and quotation
are **correct**.

⚠ **One naming error.** The table row reads **"Median relative interval width"**,
but `calibration.csv` reports `mean_rel_width`. The figures quoted in Section
5.5.7 are means, not medians. **Fix the metric name, not the numbers.**

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
XGBoost and RTD XGBoost the medMAPE-tuned model is *better* on WMAPE. And more
importantly, **on both danskvand configurations tuning for median APE makes
median APE worse**, by around five points. The objective failed to buy the thing
it was optimising for.

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
> paid without the corresponding gain.

### Note - this is a stronger result than the chapter currently claims

The old sentence describes a clean trade: pay WMAPE, receive median APE. The
measurement shows something more useful. **On two of eight configurations the
objective fails to improve the metric it optimises**, which says the tuning is
noisy at this sample size rather than that the metrics simply differ.

That reinforces rather than undermines Section 5.5.9's stability finding, and
the two should be read together. Consider adding one clause pointing forward to
it, since a reader meeting this anomaly here will want to know it is explained
later.

---

## 5.4.2 Scorability

### State

Prose plus a two-row table, one row of which is empty.

### Verified

The 14-29% zero-actual range is **correct**. The rule itself is correct and is
the right decision.

### Comments

**233 `VERIFY, SOURCE, TABLE-REFERENCE, PROSE`** - **ADDRESSED.** The table
reference is the problem: the table has a row reading *"(nothing else)"* with two
empty cells, which renders as a blank line in Word and reads as a mistake.

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
better, and removes a caption that would otherwise renumber everything after it.
This also resolves the trailing reference to §6.4.4 by naming the next section
instead.
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

> **No accuracy target is imported from the literature.** Earlier drafts carried a
> target of fifteen per cent weighted error attributed to a published retail
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

⚠ **The brand counts have changed.** The chapter's table and the current
`demand_classes.md` disagree in every category.

| Category | Chapter | Now |
|---|---|---|
| CSD | 44 / 32 / 5 / 14 | **46 / 29 / 6 / 14** |
| RTD | 32 / 20 / 2 / 8 | **27 / 21 / 7 / 7** |
| energidrikke | 16 / 18 / 2 / 8 | **15 / 19 / 3 / 7** |
| danskvand | 16 / 9 / 3 / 1 | **16 / 9 / 3 / 1** |

Totals move from 108 / 79 / 12 / 31 to **104 / 78 / 19 / 29**. The panel is still
230 brands.

### Comments

**238 `VERIFY, SOURCE, TABLE-REFERENCE, PROSE`** - **ADDRESSED.**

**240 `NAMING`** - the caption reads *"Table 7 - NO IDEA"*. **ADDRESSED**, caption
below.

### Paste - the classification table

| Category | smooth | erratic | intermittent | lumpy | total |
|---|---|---|---|---|---|
| CSD | 46 | 29 | 6 | 14 | 95 |
| danskvand | 16 | 9 | 3 | 1 | 29 |
| energidrikke | 15 | 19 | 3 | 7 | 44 |
| RTD | 27 | 21 | 7 | 7 | 62 |
| **All** | **104** | **78** | **19** | **29** | **230** |

**Caption:** *Table 8 - Brands per demand-pattern class, by category*

### Paste - the two captions

The 2x2 threshold grid, currently *"Table 7 - NO IDEA"*:

**Caption:** *Table 7 - The Syntetos-Boylan-Croston demand-pattern classification*

### Note - the total row is new and worth adding

The chapter's table has no total row, so a reader wanting the 230 has to add four
columns in their head. The row also makes the Section 5.5.5 figures traceable,
since that section quotes the totals.

---

# 5.5 Results

### State

One opening paragraph.

### Comments

**243** tagged `META COMMENT`, on *"All results are on the locked brand x month
grain (DEC-GRAIN). The alternative brand x chain representation, and the
granularity comparison built on it, were removed from the project by P0035 and no
longer appear in this chapter."*

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
**247 `VERIFY`** - caption typo *"adn"*. **ADDRESSED** below.
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

The table above reports every configuration, which is what the prose promises. If
that is too long for the page, **report the WMAPE-tuned arm in the body and move
the median-APE arm to the appendix** - but then the prose must say so, rather
than claiming both are reported here.

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
> anticipates the stability result in Section 5.5.9.

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
editorial choice rather than a result. It survives above because the choice is
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
> short series. The clipped variant appears in the table above; the raw values
> are retained in the results because the instability is itself informative about
> linear models on this panel.

### Note - the Ridge story is now stronger, not weaker

The chapter previously had Ridge as a surprise winner on danskvand. That reading
is gone, but what replaces it is a cleaner finding: **Ridge is unstable on every
category**, and the clipping bound is doing real work everywhere rather than only
on two categories. That is a more defensible claim about linear models on short
series than a single anomalous win.

### Note - the "two categories are not won by the tuned models" sentence survives

It is still true, and still danskvand and RTD. Only the reason for danskvand
changes - Prophet rather than Ridge. **Keep the sentence and the paragraph
following it**, which argues that the benchmark rung exists precisely to detect
this. That argument is unaffected.
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
1 and are now above it. Since MASE below 1 means beating the in-sample naive
forecast, and this row *is* the naive forecast scored out of sample, values above
1 say the test period is harder than the training period - which is a real
finding the chapter cannot currently state, because its figures sat just under.

### Comments

**257 `VERIFY, PROSE`** - **ADDRESSED.**
**259 `NAMING`** - **ADDRESSED**, caption below.
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

⚠ **"the same 12-feature intersection"** - `pooled_summary.md` still says twelve,
so this is correct *for the pooled run*, but the per-category models elsewhere in
the chapter now use 18. **The pooled comparison has not been re-run on the
enriched feature set.** Say so, or a reader comparing sections will find two
feature counts and no explanation.

### Comments

**262 `VERIFY, TABLE-REFERENCE`** - **ADDRESSED.**
**263 `VERIFY, FORMATTING`** - on the RTD row specifically. **ADDRESSED** - that
row is now the one that disagrees between models, so it needed the attention.
**265 `NAMING`** - **ADDRESSED**, caption below.
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
> Those gains exceed the between-seed standard deviations reported in Section
> 5.5.9, which reach 2.81 percentage points, by roughly a factor of two. The
> sub-point differences on CSD and on RTD under LightGBM do not, and are not read
> as ordering those categories.

### Paste - the per-brand paragraph

> Beneath the aggregate the picture is close to a coin flip. Broken out by demand
> class, pooling helps between 48 and 57 per cent of brands in the smooth,
> erratic and intermittent classes - no decisive effect in either direction. The
> lumpy class is the exception and falls clearly below a coin flip, at 31 per
> cent under LightGBM and 38 under XGBoost: the class where pooling was least
> likely to help is the one where it visibly does not.

### Note - the feature-count sentence

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

Two paragraphs. **Every figure is wrong.**

### Verified

Against `profiling.csv`.

| The chapter says | Measured |
|---|---|
| Ridge 5.5 MB | 5.4 MB ✓ |
| LightGBM **8.0 MB** | **38.1 MB** peak fit |
| XGBoost **0.1 MB** | **29.2 MB** peak fit |
| ARIMA 0.3 MB | 1.9 MB |
| XGBoost fits in **0.97 s**, predicts in **9.3 ms** | **3.6 s** and **13.8 ms** |
| LightGBM fits in **2.04 s**, predicts in **15.9 ms** | **8.0 s** and **33.0 ms** |
| "against the **8 GB** sequential budget" | Section 5.1 says **4 GB** |

⚠ **The chapter quotes tracemalloc for some models and nothing consistent for
others.** `profiling.csv` carries both `peak_fit_RSS_MB` and
`peak_fit_tracemalloc_MB`, and they differ by a factor of 290 for XGBoost. The
figures above are resident set size, which is what an operator provisioning a
container actually sees.

⚠ **`profiling.csv` reports `n_features: 13`.** These measurements predate the
18-feature set, so the memory figures are a **floor** rather than a measurement
of the shipped model. Tracked as H12.

### Comments

**271 `VERIFY`** - **ADDRESSED**, with the caveat above.

### Paste

> Peak resident memory during fitting is in the tens of megabytes for every
> model: 38.1 MB for LightGBM, 29.2 for XGBoost, 5.4 for Ridge and 1.9 for a
> per-series ARIMA. Against a sequential budget measured in gigabytes, the memory
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

### Note - the two-orders-of-magnitude claim

The chapter says three orders. At 38 MB against 4 GB the ratio is about 105, and
against 8 GB about 210 - so "two orders" is right for the first and borderline
for the second. **Two is safe under either reading**, which is why it is written
that way while the budget figure is unsettled.

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

The metric is also a **mean**, not a median - see Section 5.4 above.

### Comments

**273 `VERIFY, PROSE, MATH`** - **ADDRESSED.** The Lei et al. formula and the
finite-sample argument are **correct** and unchanged.
**274 `VERIFY`** - **ADDRESSED**, the paragraph is rewritten below.

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

### Note - this is a better result than the chapter currently reports

The old text had one category with wide intervals and three broadly fine. The new
figures give a **monotone relationship between calibration set size and
calibration quality**, which explains the failures instead of listing them. That
is worth the extra paragraph.

---

## 5.5.8 Remaining gaps

### State

Four short bullets, and **one of them is a note to a developer**.

### Verified

The nested-CV gap and the fixed-order ARIMA limitation are both **real and
correctly stated**. The withdrawn accuracy target is correct.

⚠ *"fig4_ram_budget is stale and contradicts §6.5.6"* is a repository TODO that
has been pasted into a thesis. It names a file the examiner cannot see. **Delete
it from the chapter** - it belongs on the deferred list, where it is already
tracked as S14.

⚠ **A gap is missing:** the pooling comparison has not been re-run on the
enriched feature set. It is now the only result in the chapter measured on a
different feature space, and that belongs here.

### Comments

**276 `VERIFY, PROSE`** - **ADDRESSED.**

### Paste

> Four limitations qualify the results above.
>
> The accuracy target has been withdrawn rather than met. Verification found that
> the benchmark cited in earlier drafts does not appear in its stated source, so
> accuracy here is assessed against the simple benchmarks alone - on which two of
> four categories are beaten outright.
>
> The tuning protocol is not nested, so every cross-validation figure reported
> above is optimistically biased by an unquantified amount. This affects the
> absolute level rather than the comparison between models, since every model was
> selected under the same protocol.
>
> ARIMA and Prophet use a fixed specification per series rather than a per-series
> order search, on cost grounds. Their figures are a competent baseline rather
> than the best attainable from those families, and the benchmark comparison is
> weaker for it.
>
> The pooled-versus-per-category comparison was measured before the holiday and
> intermittency features were added, on the twelve-feature intersection available
> at the time. It is internally consistent, since both of its arms use that same
> set, but it is not directly comparable with the per-category figures reported
> elsewhere in this chapter.

---

## 5.5.9 Forecast stability across seeds

### State

Two tables and four paragraphs. **Both tables stale; the argument survives
intact.**

### Verified

Against `stability.md` and `stability.csv`, regenerated at `471b5a3`.

⚠ **A correction to an earlier note.** The pass that preceded this one claimed
the per-seed winner table could not be reproduced from any artefact, blocked it,
and warned that Section 5.6 rested on nothing. **That was wrong.** The data is in
`stability.md`, which that pass did not open - it searched the appendix export
instead. The winner table, the p90 column and a computed
aggregate-versus-individual figure are all there.

**The chapter's claim was right all along.** Four of four categories flip.

### Comments

**278 `VERIFY, METACOMMENT, PROSE`** - **ADDRESSED.** The opening paragraph
explains why the section exists by referring to Chapter 2 and to SRQ1's scope,
which reads as the chapter justifying its own structure. Rewritten below.
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

The multiplier comes from the generator, which computes it from the per-cell
data at render time. The chapter's "three times" was measured on an older run;
the move to 3.6x is **against** the system, so the finding is slightly stronger
than the chapter currently claims.

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
RTD"*. Checked cell by cell, they beat Ridge and ARIMA on **all four**, so
"most" understates it. But the sentence names only one loss, and there are now
two: **Prophet wins danskvand outright** at 19.4 against 27.1. That has to be
named here, or Section 5.6 contradicts the table in Section 5.5.2.

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
> receives the forecast's reliability alongside the forecast itself. Where the
> two metrics rank models differently, the payload flags the disagreement rather
> than silently reporting one of them.
>
> Ensemble combination is evaluated as a separate scenario rather than folded
> into this chapter's selection. The M4 evidence that combinations outperform
> single models motivates it, and treating it as its own step is what makes the
> contribution measurable rather than assumed.

### Note - one open dependency

The final paragraph describes the ensemble as evaluated. **Confirm that scenario
has actually run before pasting it** - the chapter's own outstanding-decisions
list flags this as unresolved. If it has not, the paragraph must say the
combination is proposed rather than evaluated.

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
| SRQ2 | The calibrated prediction intervals of Section 5.5.7 are the confidence signal the tool interface carries |
| SRQ3 | Not addressed here; integration readiness is argued in Chapter 7 |
| SRQ4 | Supplies the trained models and their measured accuracy to the scenario comparison, which is what distinguishes the model-equipped scenario from the data-only one |

**Caption:** *Table 16 - How the model benchmark contributes to each
sub-research question*

### Note - verify the SRQ3 chapter number before pasting

I have written Chapter 7 from `PATHS.CHAPTER_ORDER`. **Check it against the
document**, since this is exactly the reference that broke last time.

---

# Outstanding decisions

### State

A section of resolved and open decisions, in the thesis.

### Comments

**289 `VERIFY, METACOMMENT`** - **ADDRESSED.**

### Action

**Delete the entire section.**

It is a project management artefact. It tells an examiner that trial budgets were
once fifty, that dates were once pending, and that the authors were unsure
whether to add a sixth model. None of that is a finding, and the resolved items
are already stated in their own sections as settled fact.

### Note - the two genuinely open items go elsewhere

They are real and should not be lost:

| Item | Where it belongs |
|---|---|
| Whether ARIMA should be order-searched | **already in Section 5.5.8** as a limitation. Nothing to move |
| Whether the ensemble scenario runs | a dependency for Section 5.6's final paragraph, noted above. Not a thesis sentence |

---

# What this pass did not touch

On the deferred structural list:

- **S13** - adding a caption to the calibration table renumbers every later table
- **S14** - `fig4_ram_budget` is stale, and Section 5.5.8's reference to it is
  deleted above
- **S15** - whether 5.2.2 to 5.2.6 become a comparison table
- **S16** - Zotero metadata defects that will render wrong in the bibliography.
  **Now four, not two** - the Hyndman & Athanasopoulos entry is worse than
  previously recorded, and two duplicate-author pairs need their Word citation
  fields verified. See the Citations section below
- **S9** - the cross-chapter repetition pass, open since Chapter 4

On the post-run validation list:

- **H12** - `profiling.csv` still reports 13 features, so Section 5.5.6's figures
  are a floor. Stated as such in the prose above, so this is disclosed rather
  than blocking

**Nothing in this chapter is blocked.**

---

# Table renumbering

Two changes above shift every table number after them. **Apply the deletions
first, then renumber once**, rather than tracking numbers through each edit.

| Change | Effect |
|---|---|
| Section 5.4.2's one-row table is deleted | everything after moves **down** one |
| Section 5.5.9's stability tables both need captions | Table 13 becomes 14, and a new 15 appears |

The numbering used throughout this note assumes both are applied. Word does not
update plain-text table callouts automatically, so search for **"Table "** once
at the end and check each against its caption.

---

# Citations

**Every source cited in Chapter 5 is in the library.** Checked one at a time
against the unfiltered Zotero API rather than against `citations.json`, which
filters by item type and would hide a `computerProgram` or `dataset` entry.

Library re-pulled 2026-09-10: **87 items**.

| Cited as | In library | Note |
|---|---|---|
| Hyndman & Athanasopoulos (2021) | yes, `5NFQRRXS` | ⚠ **metadata broken** - see below |
| Makridakis et al. (2018) | yes, `EXNY7D4X` | ⚠ **two M4 papers in the library** - see below |
| Taylor & Letham (2018) | yes | complete |
| Hastie et al. (2009) | yes | complete, stored as a book section |
| Tashman (2000) | yes | complete |
| Bergstra et al. (2011) | yes, `S4WQS877` | ⚠ **a second Bergstra paper exists** - see below |
| Akiba et al. (2019) | yes | ⚠ **date field reads "July 25, 2019"** |
| Gneiting (2011) | yes | complete |
| Hyndman & Koehler (2006) | yes | complete |
| Syntetos, Boylan & Croston (2005) | yes | complete |
| Cawley & Talbot (2010) | yes | complete |
| Lei et al. (2018) | yes | complete |
| Ceran et al. (2024) | yes | complete. Cited only to record that its benchmark does **not** exist |
| Bergmeir et al. (2018) | yes | **added by this pass**, Section 5.3.4 |
| Cerqueira et al. (2020) | yes | **added by this pass**, Section 5.3.4 |

**Nothing needs adding to Zotero.** Two sources are new to this chapter and both
were already in the library.

## Four defects to fix in Zotero, not in Word

The bibliography is generated from the library, so it will carry whatever is
there regardless of how the in-text citation is written.

### 1. Hyndman & Athanasopoulos is stored as a chapter, with no year and no
second author

| Field | Current value |
|---|---|
| Title | `5.2 Some simple forecasting methods \| Forecasting: Principles and Practice (3rd ed)` |
| Authors | **Hyndman only** - Athanasopoulos is missing |
| Date | **empty** |
| URL | carries a `utm_source=chatgpt.com` parameter |

**It will render as "Hyndman, R. J. (n.d.). 5.2 Some simple forecasting
methods..."** - a section heading, no year, one author, and a URL that says where
the reference was found. This is the single most-cited source in the chapter,
appearing in Sections 5.1, 5.2.1 and 5.5.2.

**Fix in Zotero:** title becomes *Forecasting: Principles and Practice*, add
Athanasopoulos as second author, set the year to 2021, edition to 3rd, publisher
OTexts, and strip the tracking parameter from the URL.

### 2. There are two M4 papers, and the chapter needs the 2018 one

| Key | Year | Title | Pages |
|---|---|---|---|
| `EXNY7D4X` | **2018** | The M4 Competition: Results, findings, conclusion and way forward | 802-808 |
| `V58EFK8B` | 2020 | The M4 Competition: 100,000 time series and 61 forecasting methods | 54-74 |

**The chapter cites "Makridakis et al., 2018, p. 803", which is correct** - that
page falls inside the 2018 paper. No prose change needed.

⚠ **But check which entry Word's citation field is actually pointing at.** Two
entries with near-identical author lists and titles are exactly the pair a
reference manager picks wrongly, and the error is invisible in the text: both
render as "Makridakis et al." and only the year differs.

### 3. There are two Bergstra papers, and they support different claims

| Key | Year | Title | Supports |
|---|---|---|---|
| `S4WQS877` | **2011** | Algorithms for Hyper-Parameter Optimization | the **TPE mathematics** - the l(x)/g(x) density split |
| `34DWJUWN` | 2012 | Random Search for Hyper-Parameter Optimization | that random search beats grid search |

**Section 5.3.5 cites "Bergstra et al., 2011, p. 2549" for the TPE density
split, which is the correct paper.** The 2012 paper has two authors, so "et al."
would be wrong for it in any case.

⚠ **Same warning as the M4 pair.** Verify the field points at `S4WQS877`.

### 4. Akiba's date field reads "July 25, 2019"

It renders as a date string rather than a year. Set it to 2019.

## What this does not cover

**None of these sources has been checked against the claim it supports.** The
audit above establishes only that each entry exists and will render correctly.
Whether Gneiting says what Section 5.4.1 uses him for, or whether Bergmeir
supports the sentence in Section 5.3.4, is a separate question.

**That is the NotebookLM pass, and it runs after the chapter is prosed.** The two
sources this pass adds are registered as `IN-ZOTERO` / `NLM-PENDING` in
`citations-added-register.md` with the sentence each must support, quoted, so
they enter that queue rather than being assumed.

The thirteen pre-existing sources are not in the register, because this pass did
not add them. If the verification pass is meant to cover the whole chapter rather
than only new citations, they need rows too - **worth deciding before the
NotebookLM run**, since a source cited since August is no more verified than one
cited today.
