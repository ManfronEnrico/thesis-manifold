---
name: ch4-verification-pass
description: NOTE - Chapter 4 consolidated pass. Folds in the feature-eligibility, holiday-enrichment, exogenous-question and ch4/ch5-boundary notes. Every claim re-checked against the repository 2026-09-08.
snapshot: 2026-09-08_18-04_ch4-second-verification
category: workflow
applies-to: [chapter 4, chapter 5, data assessment]
created: 2026_09_08-19_10
updated: 2026_09_08-19_10
status: ready
---

# Chapter 4 - consolidated verification pass

**Snapshot:** `2026-09-08_18-04_ch4-second-verification`
**Threads open:** 27. Chapter is 5,195 words.

**Notes swept and folded in, now archived:**

| Note | What it contributed |
|---|---|
| `ch4-verification-pass.md` (prior) | Fixes 2-9 below, carried forward unchanged where still valid |
| `ch4-feature-eligibility.md` | The eligibility rule, the rejected reduction, the skewness measurement - **and the correction to my feature count** |
| `srq1-holiday-enrichment-result-and-limitations.md` | The ablation result, the SHAP redistribution test, five limitations |
| `exogenous-enrichment-and-the-holiday-question.md` | Two traps to avoid; the Prophet windows-vs-counts distinction |
| `ch4-ch5-boundary-decision.md` | Fixes 10-13 below |

---

## Correction: my feature count was wrong

The previous pass said the models train on **34 features including the holiday
calendar and seventeen Nielsen distribution measures**. That is wrong, and
`ch4-feature-eligibility.md` had it right.

`srq1_benchmark.py:171` and `srq1_benchmark_tuned.py:161` both define:

```python
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "peak_month",
            "promo_intensity"]
```

**Thirteen features.** No holiday columns. No Nielsen distribution measures.

I read the *manifest's* `features` list - what the matrix makes available - and
called it the input set. The benchmark selects a subset of that by name. The
manifest describes the matrix; `FEATURES` describes the model.

Two consequences:

- **The holiday columns are ablation-only.** `srq1_holiday_ablation_tuned.py:84`
  builds `list(FEATURES) + HOLIDAY_FEATURES` for the with-holiday arm. They are
  not in the standard input set, so the chapter must describe the enrichment as a
  measured experiment, not as part of the feature set.
- **The count is category-dependent for a different reason than I said.**
  `promo_intensity` is absent for danskvand and RTD, so those train on **twelve**.
  The 54-vs-36 column difference I quoted is a property of the matrix, not of the
  model.

**Anything in the previous note that says thirty-four is superseded by this
section.** Fix 1 below replaces it.

### Note - the brand-count discrepancy also resolves

`ch4-feature-eligibility.md` flagged 106/30/50/72 against my 95/29/44/62 and did
not trace it. It is the **horizon**: h1 gives 106/30/50/72 and h3 gives
95/29/44/62, because the minimum-history threshold is `warmup + horizon + 1`.
Both are correct for their horizon. **Chapter 4 reports the three-month horizon,
so 95/29/44/62 is right** - but the chapter should say which horizon it means.

---

# The fixes

---

## Fix 1 - Section 4.3, the feature count and what the models actually see

Supersedes the previous pass's Fix 1. Section 4.3 currently contradicts itself:
one paragraph says thirty-four inputs, another says seventeen. **Both are wrong.**

### 1a - Replace the stale count paragraph

#### Anchor

Starts: *"The 17 features comprise six lags, three rolling statistics..."*
Ends: *"...the linear model receives a zero-fill at fit time."*

#### Action

REPLACE.

#### Replace with

> The models train on thirteen of these columns, or twelve for the two
> categories without promotional measurement. Six are lagged realisations of the
> target reaching back one to thirteen months, three are rolling summaries of
> the trailing four- and thirteen-month windows, three locate the observation in
> the calendar, and one carries promotional intensity from the preceding period.
> The remaining columns of the matrix are retained for description and
> traceability rather than for fitting: they are contemporaneous Nielsen
> measures that the admissibility rule excludes, together with the identifier,
> the raw and log-transformed targets and the split label.
>
> Two clarifications prevent a misreading. The log-transformed target is what
> the models predict and is not itself an input, since using it as a predictor
> would be circular. The raw promotional unit count is likewise carried but not
> fitted; the models see the derived intensity ratio instead. Lagged and rolling
> features are necessarily missing for a brand's earliest months, and nothing is
> imputed during preprocessing: the tree models handle the gaps natively, while
> the linear baseline receives a zero-fill at fit time.

### 1b - Recaption Table 4

#### Anchor

*"Table 4 - Feature Engineering Overview"*

#### Action

REWORD the caption.

#### Replace with

> **Table 4** - The thirteen model inputs. Promotional intensity is available
> for CSD and energidrikke only; the remaining categories train on twelve.

### Note - the table is now accurate, but the holiday row is not

Table 4 lists `days_in_month, n_holidays, non_holiday_days` as inputs to
LightGBM, XGBoost and Ridge. **They are not** - they enter only the ablation.
Either move that row out of Table 4 and into the enrichment subsection, or mark
it explicitly as tested-not-adopted. Fix 2 assumes the former.

⚠ **Do not cite Appendix A for the feature list.** Appendix A is the star schema.
Its title promises "and Resulting Category Features", so extending it is the
natural home, but it does not contain the list today.

---

## Fix 2 - The holiday enrichment, described as what it is

The chapter presents the enrichment as part of the feature set. It is a measured
experiment, and reporting it as such is both accurate and a stronger result.

### 2a - The provenance and construction

#### Anchor

*"Exogenous Variable Enrichment"* (the bold run-in heading)

#### Action

INSERT AFTER the heading, before *"These are the exogenous and autoregressive predictors"*.

#### Replace with

> The panel carries no calendar information of its own, so a Danish
> public-holiday calendar was joined onto it from the Nager.Date public API. Ten
> years of holidays, 2018 to 2027, were retrieved once and cached with a
> per-year checksum and a fetch timestamp, so the enrichment is reproducible
> without re-contacting the service and a later revision upstream would surface
> as a checksum mismatch rather than as a silent difference in results. Where
> the calendar cannot be supplied, the pipeline records that fact in its
> generation contract and fails rather than substituting an unenriched run for
> an enriched one.
>
> The join produces three monthly columns: the number of days in the month, the
> number of public holidays within it, and the difference between them. The
> third is deliberately not called trading days. Danish retail trades at
> weekends and many stores open on public holidays with reduced hours, so the
> column is a proxy for trading exposure rather than a measurement of it, and
> naming it otherwise would assert a commercial fact the computation never
> established.
>
> One boundary condition is handled explicitly. A month inside the fetched range
> with no public holidays is recorded as zero, which is a measurement; a month
> outside that range is recorded as missing, because a year that was never
> retrieved and a year with no holidays are different facts, and filling the
> second with a zero would convert an absence of data into an observation.

### 2b - What the enrichment is for

#### Action

INSERT AFTER 2a.

#### Replace with

> These three columns are not part of the standard input set. They were added to
> test whether an external calendar carries information beyond the calendar
> features the models already have, and that test is reported in Chapter 5
> rather than assumed here. The question is not idle: month, quarter and the
> peak-month flag already encode position in the year, so a holiday count could
> in principle be a re-encoding of information the models hold. What makes it
> testable is that holiday counts vary between years in a way a month indicator
> cannot represent - Easter moves between March and April, so those months carry
> between zero and five holiday-days across the panel, while December is flat at
> four in every year. A national holiday was also abolished partway through the
> observation window, permanently reducing the annual count, which is a
> structural break no month-of-year feature can express.

### Note - two arguments that are wrong, and were nearly made

Both are recorded in `exogenous-enrichment-and-the-holiday-question.md` and are
worth restating because both are tempting.

**The `peak_months` rename is not evidence about holiday calendars.** In August a
feature named `holiday_month` was renamed `peak_months` because it consulted no
calendar and was computing peak months from sales. That fixed a mislabelled
feature; it tested nothing. Do not write that the rename showed holiday features
do not help - a real calendar now exists and the question is answered
empirically.

**The Prophet grain argument is about windows, not counts.** The thesis correctly
says monthly observations cannot support Prophet's holiday-window component,
which models a span of days around a date. It does not follow that no monthly
holiday feature is constructible: a count of holiday-days per month plainly is.
The thesis must not argue both "monthly data cannot support holiday effects" and
"our holiday enrichment helped". State the distinction once, wherever Prophet's
weakness is explained.

---

## Fix 3 - Section 4.2, the log transform

Carried from `ch4-feature-eligibility.md`, whose measurement is across all four
categories rather than CSD alone.

#### Anchor

Starts: *"A logarithmic transformation is applied uniformly..."*
Ends: *"...inconsistent within the panel."*

⚠ This is prose from the previous pass that you have already pasted. It carries
**CSD-only** figures ("twelve volume-valued columns... 4.1 and 5.1"); the
replacement below spans all four categories and is the better measurement.

#### Action

REPLACE.

#### Replace with

> The logarithmic transformation is applied uniformly to the target and to the
> volume-valued inputs of the linear model, rather than selected per brand. The
> distributional evidence supports it without qualification: across all four
> categories the volume-valued features carry raw skewness between 3.7 and 10.4,
> and fall below 0.5 in absolute value under the transformation, while the
> calendar and intensity features remain close to symmetric and are left
> untransformed. Uniform treatment is preferred to per-series selection because
> the tests that would drive such a selection have limited power at the
> available series length, and because a transformation applied unevenly across
> brands would make the feature semantics inconsistent within the panel.

### Note - this supersedes my own earlier version

The previous pass gave "twelve volume columns, 4.1 to 5.1" from CSD alone. The
range above spans all four categories and matches the partition
`LOG_SCALE_FEATURES` actually applies - the nine lag and rolling columns are
log-scaled for Ridge, the four calendar and intensity columns are not. The
hand-written tuple and the measured partition are the same set, which is worth
knowing and is not currently stated anywhere.

---

## Fix 4 - Thread 186, referring to repository files

#### Anchor

*"They are recorded per category and per horizon in `<category>_split_dates_h<H>.json`"*

#### Action

REWORD.

#### Replace with

> "The resolved boundaries are written to disk alongside each feature matrix as
> part of the generation record, so every reported result can be traced to the
> exact windows that produced it."

### Note - the general rule

A filename with a wildcard in it is a note to a developer, not a sentence in a
thesis. State what is recorded and why it matters; if the artefact needs naming,
name it in the appendix where reproduction instructions live. The same applies to
the `regeneration_report.md` pointer under Table 1 and to
`scripts/srq1_benchmark_tuned.py` wherever it survives.

---

## Fix 5 - Thread 154, the imputation claim is not implemented

#### Anchor

Starts: *"These reflect products Nielsen does..."*
Ends: *"...immaterial at these null rates)."*

#### Action

REPLACE.

#### Replace with

> These are products Nielsen does not track for distribution in a given period.
> They are not imputed: aggregation to the brand-month grain runs over
> positive-sales rows only, so a row with no distribution reading and no sales is
> excluded before any feature is computed rather than filled with an estimate.
> The null rates therefore describe the raw panel and do not propagate into the
> modelling matrix.

### Note - confirmed absent

The pipeline aggregates with `facts[facts["sales_units"].fillna(0) > 0]` and
averages weighted distribution across survivors. There is no median fill. The
sentence describing one describes a step that is not in this version, and it is
also the basis of a risk item in 4.5 that consequently describes a risk the
project does not run - see Fix 9.

---

## Fix 6 - Section 4.1.2, Table 1 and its metadata note

### 6a - Regenerate Table 1

#### Anchor

The row starting *"RTD | 41 | 101"* and ending *"728 | 2,442 | 2,509"*.

#### Action

REPLACE the table body.

#### Replace with

| Category | Periods | Brands in scope | Brands retained | Catalog SKUs | In-scope SKUs | Brand-month rows | In-scope fact rows |
|---|---|---|---|---|---|---|---|
| CSD | 46 | 142 | 95 | 2,130 | 7,991 | 4,209 | 223,240 |
| danskvand | 41 | 55 | 29 | 1,071 | 1,913 | 1,225 | 27,449 |
| energidrikke | 43 | 68 | 44 | 1,271 | 4,083 | 1,702 | 55,216 |
| RTD | 41 | 101 | 62 | 728 | 2,442 | 2,509 | 49,976 |

⚠ Retained counts are for the **three-month horizon**. At one month the threshold
is lower and retains 106 / 30 / 50 / 72. State the horizon in the caption.

### 6b - Delete the provenance note

#### Anchor

Starts: *"These figures are recomputed locally under DVH EXCL. HD and supersede"*
Ends: *"...per regeneration_report.md)."*

#### Action

REPLACE.

#### Replace with

> The columns distinguish two counts that are easily conflated. Catalog SKUs are
> the products Nielsen lists in the category dimension; in-scope SKUs are those
> with positive recorded sales at this market level. The gap between them - and
> between brands in scope and brands retained - is where the category
> differences that bear on modelling appear. RTD lists the fewest products but
> the second-highest brand count, while danskvand carries a large catalog against
> a small active panel.

### Note - a number that was wrong in the deleted text

The note claimed 8,608 catalog SKUs "superseding the earlier 2,080". The product
dimension has exactly **2,130 rows**. It superseded the more nearly correct figure
with a wrong one; 8,608 is close to the in-scope SKU count, so the two look
transposed.

---

## Fix 7 - Section 4.1.2, the coverage paragraph

#### Anchor

Starts: *"The temporal span is 37-42 months..."*
Ends: *"...1,543 observed brand-month rows."*

#### Action

REPLACE.

#### Replace with

> The panel spans forty-one to forty-six months by category - forty-six for CSD,
> forty-three for energidrikke and forty-one for danskvand and RTD - and is
> re-pulled monthly, so the span grows over time rather than being fixed. Within
> the DVH EXCL. HD scope the categories carry 142, 55, 68 and 101 brands
> respectively, of which 95, 29, 44 and 62 satisfy the minimum-history
> requirement at the three-month horizon and are carried into modelling. Because
> that requirement is derived from the feature set and the horizon rather than
> fixed, the retained counts are a property of the forecasting question being
> asked: at a one-month horizon the same rule retains 106, 30, 50 and 72.

---

## Fix 8 - Section 4.1.4, the ARIMA span claims

### 8a - The span figure

#### Anchor

Starts: *"37-42-month span exceeds the ARIMA..."*
Ends: *"...decomposition and gradient-boosted models."*

#### Action

REWORD the opening clause only.

#### Replace with

> "The panel spans forty-one to forty-six months by category."

### 8b - The superseded filter

#### Anchor

Starts: *"retained by the >=30-month filter (77 / 24 / 27 / 42"*
Ends: *"...confounded by very short series;"*

#### Action

REWORD.

#### Replace with

> "retained by the minimum-history requirement (95 / 29 / 44 / 62 brands for
> CSD / danskvand / energidrikke / RTD at the three-month horizon), so that model
> comparisons are not confounded by very short series;"

### Note

The ARIMA-minimum claim is registered as CV-A. Do not write a citation from
memory.

---

## Fix 9 - Section 4.5, the risk list

#### Anchor

Starts: *"Figures verified (resolved). All structural,"*
Ends: *"...non-beverage categories is future research."*

#### Action

Within that block: **delete** the "Figures verified", "Market scope" and
"Per-category EDA" items - all three are provenance, not risk. **Replace** "Thin
training windows" and "Weighted-distribution imputation" as below. **Keep**
"Empirical parameters", "Promotional coverage", "Commercial access" and
"Generalisability bound".

#### Replace with

> **Category imbalance.** The four categories differ substantially in evidential
> weight: CSD contributes 4,370 brand-month observations across ninety-five
> brands, where danskvand contributes 1,189 across twenty-nine. The proportional
> split gives every category a training window of at least twenty-nine periods,
> so no category is thin in the time dimension, but the cross-sectional imbalance
> remains and bears on the pooled-versus-specialised comparison, where a pooled
> model is necessarily fitted more to CSD than to the rest. Mitigation: that
> comparison is scored per category on identical test rows rather than in
> aggregate, so the imbalance affects what is learned but not how it is measured.
>
> **Unmeasured availability.** Where Nielsen does not track distribution for a
> product in a period, the row carries no reading and is excluded at aggregation
> rather than estimated. For CSD this affects 7.1 per cent of in-scope fact rows.
> Mitigation: the exclusion is applied before feature construction and is
> therefore visible in the retained row counts rather than hidden in an imputed
> value; no distributional assumption is introduced.
>
> **External calendar dependency.** The holiday enrichment rests on a third-party
> source that can be revised upstream, as the abolition of a Danish public
> holiday during the observation window illustrates. Mitigation: the calendar is
> cached with a fetch timestamp and per-year checksum, which makes a revision
> detectable rather than impossible, and an unenriched run is declared in the
> generation contract rather than silently substituted.

### Note - why three items were deleted

"Figures verified", "Market scope (resolved)" and "Per-category EDA (resolved)"
describe work that was done, not risks that remain; they read as a project log.
The market-scope finding is important but already appears in 4.1.3 as part of the
argument. Their deletion also removes the last "MIN_PERIODS=30" reference and the
last mention of a `regeneration_report.md`.

---

## Fix 10 - Section 4.2, the remaining EDA blocks

### 10a - Scope and filtering counts

#### Anchor

Starts: *"Market scope: DVH EXCL. HD (single Nielsen market level"*
Ends: *"...(correct for an ACV metric)."*

#### Action

REPLACE.

#### Replace with

> Market scope is the single DVH EXCL. HD level. Within it the category spans
> forty-six monthly periods on Nielsen's 4-4-5 week calendar; period identifiers
> are not calendar-monotonic, so the span is taken from the documented window
> rather than from raw minimum and maximum values. Of 142 brands present, 95
> satisfy the minimum-history requirement at the three-month horizon and
> contribute 4,209 brand-month observations. Aggregation is to brand and month
> over positive sales only, with weighted distribution averaged rather than
> summed, which is the correct treatment for an all-commodity-volume metric.

### 10b - Per-category EDA table

#### Anchor

Starts: *"RTD | none (promo-zero) |"*
Ends: *"level | +0.82 / +0.58"*

#### Action

REPLACE the table body.

#### Replace with

| Category | Promo correlation | Peak months | ADF (level) | ADF (differenced) | Pooled ACF lag 1 / 3 / 13 |
|---|---|---|---|---|---|
| CSD | r = 0.94 | 3, 6, 9, 12 | p = 0.76 | p < 0.001 | +0.81 / +0.60 / -0.16 |
| danskvand | none | 6, 7, 8, 9 | p = 1.00 | p < 0.001 | +0.63 / +0.36 / -0.06 |
| energidrikke | r = 0.99 | 3, 6, 9 | p = 0.77 | p < 0.001 | +0.83 / +0.59 / -0.15 |
| RTD | none | 5, 6, 12 | **p < 0.001** | p < 0.001 | +0.86 / +0.66 / -0.04 |

⚠ Lag-13 is **negative in all four categories**. The chapter calls it "near-zero
carry", defensible for RTD at -0.04 but not for CSD at -0.16.

### 10c - The proof-of-concept framing

#### Anchor

Starts: *"The three proof-of-concept categories were"*
Ends: *"...gap previously flagged in section 4.6."*

#### Action

REPLACE.

#### Replace with

> All four categories are processed through the identical pipeline and their
> exploratory results are reported below. They are not replications of a pilot:
> each is trained and tuned independently, and all four are carried into both the
> pooled-versus-specialised comparison and the scenario experiment. The
> differences between them - in seasonal profile, promotional coverage and panel
> size - are what makes the generalisation question answerable at all.

### Note - the code contradicts the framing

`srq1_pooled.py` exists to answer whether a per-category model beats a pooled
one; the results tree holds a trained model directory for each category; and the
scenario experiment samples brands from all four. CSD is presented first because
it is the largest panel, not because the others are proofs of concept.

---

## Fix 11 - Chapter 5 asserts no holiday calendar exists

**Chapter 5 contradicts Chapter 4 on a matter of fact, in the same document.**

#### Anchor

In 5.3.2.
Starts: *"Calendar: month, quarter, and a binary peak_month flag..."*
Ends: *"...measured from the sales distribution, not from calendar dates"*

#### Action

REPLACE.

#### Replace with

> **Calendar**: month, quarter, and a binary peak-month flag derived from the
> category's own seasonal profile - months whose mean units exceed the category
> mean by more than ten per cent. The peak-month flag is measured from the sales
> distribution rather than from a calendar; the separate public-holiday
> enrichment described in Section 4.3 is evaluated as an ablation in Section 5.5
> and is not part of the standard input set.

### Note - the sentence was true when written

The bold claim *"No holiday calendar is used"* predates the enrichment. One
chapter was updated and the other was not, which is precisely the failure mode
the duplication produces - and the argument for Fixes 12 and 13.

---

## Fix 12 - Collapse 5.3.1 to the experiment-specific facts

#### Anchor

Starts: *"Grain: brand x month (DEC-GRAIN). The chain and region grains..."*
Ends: *"...CSD 665 rows, RTD 372, energidrikke 308, danskvand 174"*

#### Action

REPLACE the subsection body.

#### Replace with

> The modelling grain is brand x month, and the panel, its minimum-history
> requirement and its train/validation/test boundaries are as established in
> Sections 4.2 and 4.4; the chain and region grains were evaluated and dropped,
> and are reported as a limitation rather than a live dimension. Two properties
> belong to the experiment rather than to the data. The forecast horizon is three
> months, so each model predicts the value three periods ahead of the last
> observation it is given. And the resulting test sets contain 665 rows for CSD,
> 372 for RTD, 308 for energidrikke and 174 for danskvand - the denominators
> behind every error figure reported in Section 5.5.

### Note - verified

All four row counts are correct against the current matrices. They are the one
part of 5.3.1 that says something Chapter 4 does not.

---

## Fix 13 - Collapse 5.3.2 to a back-reference

Apply after Fix 11, or in its place - this replacement subsumes the calendar
bullet.

#### Anchor

Starts: *"Lags: t-1, t-2, t-3, t-4, t-8, t-13 months"*
Ends: *"...Ridge receives a zero-fill at fit time"*

#### Action

REPLACE the subsection body.

#### Replace with

> The feature matrix is the one constructed in Section 4.3, and the models train
> on the thirteen admissible columns identified there: six lags, three rolling
> summaries, three calendar features and promotional intensity. Its construction
> is not repeated here.
>
> What matters for the benchmark is which models consume it. The tabular learners
> - LightGBM, XGBoost and Ridge - take the full input set; ARIMA and Prophet are
> fitted on the univariate log sales series and never see it. The two groups also
> differ in how they handle the missing values that lagged features necessarily
> carry for a brand's earliest months: the tree models handle missingness
> natively, while Ridge cannot and receives a zero-fill at fit time. Promotional
> intensity exists for CSD and energidrikke only, leaving twelve inputs for the
> other two categories; the column is omitted rather than zero-filled, since a
> constant zero would assert that no promotion ran when the truth is that none
> was recorded.

---

## Fix 14 - Chapter 4's own duplicate

Section 4.2.5's Table 2 restates parameters that 4.3 and 4.4 now state correctly,
and carries two superseded figures.

#### Anchor

Starts: *"MIN_PERIODS | 30 (global)"*
Ends: *"Train / Val / Test | 24 / 6 / 12 months"*

#### Action

DELETE the table; keep the sentence that follows it, replaced as below.

#### Replace with

> These parameter values are reported where they are derived: the lag set and
> rolling windows in Section 4.2.4, the peak months in Section 4.2.3, the
> minimum-history requirement in Section 4.1.2 and the split in Section 4.4.
> Their origin is empirical rather than theoretical - they follow from this
> panel's own structure rather than from a prior specification - and that is
> stated as a limitation rather than presented as a design principle.

### Note - two stale figures die with the table

"MIN_PERIODS 30 (global)" and "Train / Val / Test 24 / 6 / 12 months" are both
superseded, and both sit two sections above the tables that correct them. The
sentence after Table 2 also promises that the parameters' *"academic
justification is developed in the modelling chapter"* - after Fixes 12 and 13
that promise has nowhere to land, so the replacement removes it.

---

# Where feature engineering belongs

Recorded here because the question was settled and the reasoning should not be
lost with the archived note.

**Everything stays in Chapter 4.** I first proposed moving feature engineering to
Chapter 5; that was wrong, for two reasons found in the code.

`FeatureEngineer.transform` runs `calendar -> filter -> engineer_features ->
apply_split`. Feature construction is **upstream of the split**, so a chapter
describing the split but not the features describes the pipeline out of order.

And the usual reason to defer feature engineering does not apply here.
`FeatureEngineer.fit` is a documented no-op:

> "every transformation in this module is leakage-safe by construction
> (lags/rolling use shift, calendar/promo/log are deterministic). No statistics
> are learned from training data."

Nothing is fitted, so nothing can leak. The boundary is not "data versus model" -
it is **construction versus use**. Chapter 4 builds the matrix; Chapter 5 reports
what was done with it.

| Topic | Chapter 4 | Chapter 5 |
|---|---|---|
| Grain, minimum history, split | derived | cited |
| Lags, rolling, peak months | derived from EDA | cited |
| Holiday enrichment | provenance and construction | **ablation result** |
| Feature admissibility rule | stated | cited |
| Horizon, test-set row counts | — | stated |
| Which model takes which input | — | stated |

---

# Claims register

| # | Claim | Where | To verify |
|---|---|---|---|
| CV-A | ARIMA requires roughly 24 periods for stable parameter identification | 4.1.4 | Does an authoritative forecasting text state a minimum series length, and is it ~24? If not, reword to rest on the observed 29-46 periods. |
| CV-B | Prophet requires at least two seasonal cycles | 4.4 | Does the Prophet documentation or paper state a minimum? |
| CV-C | Commercial panel providers are reliable because their business depends on credibility | 4.1.3 | Is there a methodological source, or is this an assumption? |
| CV-D | LightGBM and XGBoost handle NaN natively | 4.3 | Both document this; cite the docs. |
| CV-E | Using the contemporaneous target as a predictor constitutes leakage | 4.3 | Standard; cite a forecasting or ML methodology text. |
| CV-F | Danish retail trades at weekends under a liberalised opening-hours statute | 4.3 (Fix 2a) | The claim is used to justify the `non_holiday_days` naming. Statute name and year unverified - carried from the enrichment note as CV-03. |
| CV-G | A Danish public holiday was abolished with effect from 2024 | 4.3 (Fix 2b) | The effect is visible in the fetched calendar; the legislative reference is unverified - carried as CV-05. |

Fix 2b deliberately says "a national holiday was abolished" without naming it or
citing a statute, so the prose can be pasted before CV-G is resolved. **Do not add
the name or the year until it is.**

---

# Decisions

| Where | Question |
|---|---|
| 4.1.1, on *"confidentiality agreement with Manifold AI"* | **You never signed an NDA.** The chapter asserts one exists. Still open, still the most important item in this chapter. |
| Chapter title, on *"From Scanner Panel to Modelling Matrix"* | Keep the subtitle or drop it? |
| Appendix A | Extend it to carry the per-category feature list beneath the star schema - its title already promises "Resulting Category Features" - or add Appendix B? I recommend extending. |
| 4.2.5 / 4.2.6 / 4.3 tables | Which tables move to the appendix. Table 1 as regenerated is small enough to stay in text. |

---

# Does the chapter hold together?

The structure is sound - Saunders' three stages, then the substrate, then the
split, then the risks. Two things still undermine it, and both are narrower than
at the last pass.

**The chapter describes a pipeline the code has moved past**, in the feature
count, the median imputation and the proof-of-concept framing. Each is small
alone; together they mean a reader who checks one claim has reason to doubt the
others. That this pass had to correct my *own* feature count against a note
written by another session is the same problem one level up.

**Provenance scaffolding remains visible** - filename references, "(resolved)"
risk items, a pointer to a regeneration report. These read as working notes and
signal an unfinished draft more strongly than any individual number.

Neither requires rethinking the chapter. Both are addressed above.
