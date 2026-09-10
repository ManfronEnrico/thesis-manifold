---
name: ch4-prose-pass
description: NOTE - Chapter 4 converted to prose and reconciled with the repository as it stands on 2026-09-09. Nine paste-ready fixes, each verified against the pipeline EDA tables, the feature matrices and the benchmark scripts.
snapshot: 2026-09-09_16-05_prose-pass
category: workflow
applies-to: [chapter 4]
created: 2026_09_09-16_30
updated: 2026_09_09-16_30
status: ready
---

# Chapter 4 - prose pass, documented as the code stands

**Snapshot:** `2026-09-09_16-05_prose-pass`
**Notes swept:** `ch4-verification-pass.md` (applied - sections 4.3 and 4.4 in the
snapshot are its prose; archived) and `why-thirteen-features.md` (folded into
Fix 3 below; archived).

Sections 4.2 to 4.4 are already prose and largely correct. The work left is
concentrated in **4.1.2, 4.1.3, 4.1.4 and 4.5**, which still carry figures from
a pipeline version that no longer exists, and in **4.3**, where two sentences
survived underneath the pasted replacement and now contradict it.

Everything below was measured on 2026-09-09 against the pipeline's own EDA
tables, the engineered matrices and the benchmark scripts. Where the chapter and
the repository disagree, the repository is quoted.

---

# What the measurements say

One table, because six of the nine fixes rest on it. Counted from the four
`step_2_*.csv` EDA tables and the eight `*_feature_matrix_h*.parquet` files.

| | CSD | danskvand | energidrikke | RTD |
|---|---:|---:|---:|---:|
| Panel months | 46 | 41 | 43 | 41 |
| Brands in scope | 142 | 55 | 68 | 101 |
| Brand-month rows in scope | 4,209 | 1,225 | 1,702 | 2,509 |
| Brands retained, H=1 | 106 | 30 | 50 | 72 |
| Brands retained, H=3 | 95 | 29 | 44 | 62 |
| Matrix rows, H=3 | 4,370 | 1,189 | 1,892 | 2,542 |
| Matrix columns | 54 | 36 | 54 | 52 |
| **Columns the models consume** | **13** | **12** | **13** | **12** |

Danskvand and RTD consume twelve because they carry no promotional measure.

---

# The fixes

---

## Fix 1 - Section 4.1.2 states a retention rule the pipeline no longer has

The paragraph beginning "The temporal span is 37-42 months" is the single most
outdated passage in the chapter. Every figure in it is superseded, and it
describes a `MIN_PERIODS = 30` threshold that was **deleted from the code** on
2026-08-18.

This also answers threads *"The temporal span is 37-42 ... / 1,543 observed
brand-month rows."* and *"by the >=30-month filter (77 ... confounded by very
short series;"*.

### Anchor

Starts: *"The temporal span is 37-42 months (CSD 42, energidrikke 39..."*
Ends: *"...carried forward to the modelling and discussion."*

### Action

REPLACE the whole paragraph.

#### Replace with

> Coverage is assessed on the temporal span, the brand and product counts, and
> the series that survive the retention rule. The four panels run to forty-six
> months for carbonated soft drinks, forty-three for energy drinks and
> forty-one for water and ready-to-drink beverages, each ending in July 2026.
> Before retention they carry 142, 68, 55 and 101 brands respectively, over
> 4,209, 1,702, 1,225 and 2,509 brand-month observations. Applying the derived
> minimum-history rule at the three-month horizon leaves 95, 44, 29 and 62
> brands. A category-specific coverage caveat applies to promotional
> measurement: for water and ready-to-drink beverages the promotional variables
> are absent from the source entirely, so the promotional feature is unmeasured
> for those two categories. In Saunders et al.'s terms this is an
> unmeasured-variable limitation, and it is carried forward to the modelling
> and the discussion.

### Note - why the old numbers cannot be repaired in place

They are not merely stale, they describe a different rule. The chapter's
"37-42 months" predates the July 2026 refresh; its "77 / 24 / 27 / 42 brands"
is the output of a `>= 30` filter. `engineer_features.py:51` records the
deletion of that constant explicitly:

> "REMOVED 2026-08-18: there was a DEFAULT_MIN_PERIODS = 30 here. It was a
> THIRD source of truth ... MIN_PERIODS is not a free parameter: it follows
> from the feature specification as warmup + horizon + 1."

**The derived rule reproduces the matrices exactly.** The pipeline's retention
table shows 15 periods retaining 106 / 30 / 50 / 72 brands, which is precisely
the H=1 matrix brand count in all four categories. The chapter's own §4.1.2
already states this rule correctly two paragraphs earlier - the fix removes the
contradiction rather than introducing a new claim.

---

## Fix 2 - Section 4.1.2 says the same thing twice, in the same paragraph

The paragraph beginning "The columns distinguish two counts" ends by restating
the minimum-series-length rule that its own preceding paragraph has already
given, running two versions of the same explanation together with no break.

### Anchor

Starts: *"The columns distinguish two counts that are easily conflated."*
Ends: *"...44 for energidrikke and 62 for RTD."*

### Action

REPLACE.

#### Replace with

> The columns distinguish two counts that are easily conflated. Catalog
> products are those Nielsen lists in the category dimension; in-scope products
> are those with positive recorded sales at this market level. The gap between
> them, and the gap between brands in scope and brands retained, is where the
> category differences that matter for modelling appear. Ready-to-drink
> beverages list the fewest products but the second-highest brand count, while
> water carries a large catalogue against a small active panel.

### Note - what is being deleted

The deleted half is the sentence beginning "Minimum series length. The
retention threshold is not chosen; it is derived" through to the brand counts.
It duplicates the paragraph two above it almost word for word. The surviving
copy is the earlier one, which reads better and is already correctly placed.

---

## Fix 3 - Section 4.3 contradicts itself on the feature count

Two sentences survived underneath the replacement prose and now disagree with
it, with each other, and with the code. The section currently says CSD has
**"thirty-four are model inputs"** and then **"The 17 features comprise six
lags..."**. The models consume **thirteen**.

### Anchor - part A

Starts: *"Thus, the forecasting substrate uses features derived from the Nielsen facts table"*
Ends: *"...recorded in the generation manifest written beside each matrix."*

### Action

REPLACE.

#### Replace with

> The forecasting substrate is therefore built from the Nielsen facts table at
> the brand-and-month grain. Each matrix is wider than the model input set,
> because the Nielsen measures are retained for description alongside the
> engineered columns: carbonated soft drinks and energy drinks carry fifty-four
> columns, ready-to-drink beverages fifty-two and water thirty-six. Of these,
> thirteen are model inputs for carbonated soft drinks and energy drinks and
> twelve for water and ready-to-drink beverages, which carry no promotional
> measure. The remaining columns are the brand and period identifiers, the raw
> and log-transformed targets, the split label, and the Nielsen measures
> excluded from the input set by the admissibility rule above. The per-category
> composition is recorded in the manifest written beside each matrix.

### Anchor - part B

Starts: *"The 17 features comprise six lags, three rolling statistics"*
Ends: *"...the linear model receives a zero-fill at fit time."*

### Action

REPLACE.

#### Replace with

> The thirteen inputs are six lagged realisations of the target at one, two,
> three, four, eight and thirteen months; three rolling summaries, being the
> four-month mean and standard deviation and the trailing annual mean; three
> calendar terms, being the month, the quarter and the peak-month indicator;
> and promotional intensity. Two clarifications resolve an ambiguity carried by
> earlier drafts. The log-transformed target is what the models predict and
> exponentiate back, not an input, since using it as a predictor would be
> trivial leakage. The weighted-distribution measure is likewise not an input:
> it was tested and excluded, for reasons given below. Lagged and rolling
> features are undefined for a brand's earliest months and are left as missing
> rather than imputed, so the tree models handle the gaps natively while the
> linear model receives a zero-fill when it is fitted.

### Note - the count is verified eight times over

`FEATURES` is defined identically in eight scripts under
`02_thesis_modelling/model_training/srq1/`, including the benchmark, the tuned
benchmark, the pooled trainer and the calibration run. All thirteen are present
in the CSD and energidrikke matrices; `promo_intensity` is the one absent from
danskvand and RTD, which is what makes those two twelve.

The "thirty-four" in the current text is real but is a different quantity: the
manifest's `features` list has 34 entries, which is what the matrix *offers*.
The gap between 34 and 13 is the subject of Fix 4.

---

## Fix 4 - Table 4 lists two columns the models do not receive

The feature table currently includes rows for the holiday calendar and for
weighted distribution, both marked as consumed by LightGBM, XGBoost and Ridge.
Neither is in `FEATURES`. This is the table thread tagged VERIFICATION, and the
thread on the holiday enrichment.

### Anchor

The two table rows.
Starts: *"days_in_month, n_holidays, non_holiday_days"*
Ends: *"Nielsen weighted-distribution availability proxy | LightGBM, XGBoost, Ridge"*

### Action

DELETE both rows from Table 4, then INSERT the prose below after the table
caption.

#### Replace with

> Two groups of columns are constructed by the pipeline but withheld from the
> standard input set, and the reasons differ. The Danish public-holiday
> calendar is joined onto the monthly grid from the Nager.Date service, giving
> the number of days in each month, the number of public holidays falling
> within it, and the difference between them. These three enter the benchmark
> only as an ablation arm, so that the value of calendar enrichment can be
> measured rather than assumed; they are also exactly linearly dependent by
> construction, since the third is the first minus the second, which rules out
> admitting all three to a linear model. The weighted-distribution measure was
> tested as an input and rejected on measured evidence. It is not
> contemporaneous with the target in the way the excluded Nielsen measures are,
> and it moves slowly enough to be known in advance, so it was a genuine
> candidate. Fitting the benchmark with and without it, however, raised the
> error in three of the four categories, and it is excluded on that result
> rather than on principle.

### Note - the holiday reason is worth keeping short in the chapter

The full derivation is in `engineer_features.py:379-440`, which also records why
the column is named `non_holiday_days` rather than `selling_days`: Danish
grocery is not uniformly closed on public holidays, so the arithmetic supports
only "days that are not public holidays", not "days the shop was open". If you
want one more sentence in the chapter, that is the one to add.

**Watch the promotional row too.** Table 4 describes `promo_intensity` as the
promotional share of units clipped to zero and one. That is right as far as it
goes, but the pipeline also **lags it one period** before the models see it
(`engineer_features.py:585`), which is what makes it admissible at all. Worth a
clause: *"the promotional share of units, clipped to the unit interval and
carried forward one period so that it is known when the forecast is issued."*

---

## Fix 5 - Section 4.1.3 asserts null rates the data does not have

Three separate claims here are contradicted by the pipeline's own measurement
table. This covers the thread on median imputation and the thread on negative
values.

### Anchor

Starts: *"Missing values are concentrated in one category and one pattern."*
Ends: *"...confirmed locally."*

### Action

REPLACE the whole span, which runs across three paragraphs and includes the
median-imputation sentence and the negative-values sentence.

#### Replace with

> The core measures are complete. Sales units, sales value and the
> weighted-distribution proxy carry no nulls, no zeros and no negative values in
> any of the four categories, measured on the in-scope facts after the market
> scoping described above. Missingness is confined to the promotional
> decomposition, where between twenty-nine and eighty-two per cent of rows are
> null for the finer display-and-feature breakdowns; none of those columns is a
> model input. Negative values appear in four rows in total across the whole
> panel, always in a promotional variant rather than in the sales measures
> themselves. They are conventionally read as returns or corrections, but the
> panel carries no field distinguishing a genuine return from a recording
> error, so they are floored at zero as a decision taken under that ambiguity
> rather than an interpretation the data support. At four rows the treatment is
> immaterial to any result.

### Note - what was measured, and what it displaces

`step_2_14_measure_quality.csv`, written by the pipeline for each category:

| | nulls | zeros | negatives |
|---|---:|---:|---:|
| `sales_units`, all four categories | 0 | 0 | 0 |
| `sales_value`, all four categories | 0 | 0 | 0 |
| `weighted_dist`, all four categories | 0 | 0 | 0 |

Negative rows across the entire panel: **4** (CSD), **0** (danskvand), **1**
(energidrikke), **3** (RTD).

Three claims in the current text do not survive this:

- **"For CSD it is null in 7.1 per cent of in-scope fact rows"** - the measured
  rate is zero. My earlier pass reported 7.115 per cent; that measurement was
  taken before the market scoping and does not describe the in-scope facts.
- **"they are imputed using a brand-and-market median"** - there is no median
  imputation anywhere in the pipeline. What exists is a zero-to-null conversion
  followed by a forward fill, at `engineer_features.py:341`, which is the
  opposite operation. **This is the sentence to be most careful about**: it
  describes a method the thesis does not use.
- **"True zero-sales rows are likewise rare (CSD 12, danskvand 1, ...)"** - the
  pipeline's zero-type table reports "no zeros" for all 142, 55, 68 and 101
  brands respectively.

---

## Fix 6 - Section 4.1.4 repeats the retired filter

Same stale figures as Fix 1, in a section that is otherwise fine. Also carries a
SOURCE thread on the ARIMA minimum.

### Anchor

Starts: *"Benchmarking (Chapter 6) is conducted on the brand series retained"*
Ends: *"...comprises 57 / 22 / 18 / 37 brands respectively."*

### Action

REPLACE.

#### Replace with

> Benchmarking is conducted on the brand series that satisfy the derived
> minimum-history rule, which at the three-month horizon retains 95 brands for
> carbonated soft drinks, 44 for energy drinks, 29 for water and 62 for
> ready-to-drink beverages, so that model comparisons are not confounded by very
> short series. Missing months within a retained series are exposed on the
> regular monthly grid and handled natively by the models rather than imputed.

### Note - the ARIMA claim above it

The preceding sentence says the span "exceeds the ARIMA minimum of roughly 24
periods for stable parameter identification". **That number has no source in
the library**, and the thread tagged SOURCE is asking for one.

Two options. Either find a source and cite it, or drop the number and let the
sentence rest on what the project measured. The second is safer and costs
nothing:

> **REWORD** - *"The panel spans forty-one to forty-six months, which provides
> at least three full annual cycles in every category and supports both the
> seasonal decomposition the statistical baselines require and the annual lag
> terms the tree models use."*

That claim is true by inspection of the panel and needs no citation.

---

## Fix 7 - Section 4.2.1 is the last bullet block in the chapter

Four bold-lead fragments, and two of them carry retired figures: the 42-period
span and the `MIN_PERIODS >= 30` filter with its 77 brands.

### Anchor

Starts: *"Market scope: DVH EXCL. HD (single Nielsen market level; see header)."*
Ends: *"...weighted distribution averaged rather than summed (correct for an ACV metric)."*

### Action

REPLACE the whole block.

#### Replace with

> Carbonated soft drinks are assessed at the single DVH EXCL. HD market level,
> the scope adopted for all four categories, which admits 4,209 brand-month
> observations across 142 brands. The panel spans forty-six monthly periods from
> October 2022 to July 2026 on Nielsen's four-four-five week calendar; because
> period identifiers are not monotonic with calendar time, the span is taken
> from the year-and-month key rather than from the identifier range. Applying
> the derived minimum-history rule retains 95 brands and 4,370 observations at
> the three-month horizon, and 106 brands at one month, the difference being the
> two additional periods the longer horizon requires. Aggregation is to brand
> and month over positive sales only, with the weighted-distribution proxy
> averaged rather than summed, which is the correct treatment for a measure
> expressed as a share of category volume.

### Note - one sentence is deleted rather than rewritten

The current block ends with a note that these figures "supersede Brian's
all-markets values (143 -> 62 brands; 4,040 rows), inflated by the market
double-count". That is a changelog entry, not a thesis sentence - it names a
person and an internal correction. The double-count itself is already explained
properly in §4.1.2, which is where it belongs.

---

## Fix 8 - Section 4.2.3 carries three paragraphs of changelog

The seasonality section states its result twice and then explains, at length,
what a previous version of the code did wrong. The thread on this section is
tagged PROSE and METADATA, which is exactly right.

### Anchor

Starts: *"Peak-month indicator: PEAK_MONTHS - months whose mean"*
Ends: *"...September enters CSD's set under the corrected rule."*

### Action

REPLACE all three paragraphs with one.

#### Replace with

> The indicator is derived per category rather than inherited, and the four
> profiles that result are distinct and commercially plausible: quarter-end
> months for carbonated soft drinks, the summer for water, the quarter-ends
> without December for energy drinks, and early summer with December for
> ready-to-drink beverages. The measure is deliberately named for what it
> detects. An earlier version called these holiday months, which asserted a
> cause the computation never establishes, and the evidence frequently
> contradicts it: the carbonated-soft-drink peaks fall at the quarter ends,
> consistent with retail trade loading rather than with any holiday.

### Note - the threshold is in the code, uncited

`step_3_derive_params.py:149` sets `PEAK_UPLIFT_THRESHOLD = 0.10`, with the
comment that ten per cent "is the notebook's implied threshold, now stated
explicitly". **It has no external source**, in the same way the 0.95 grouping
threshold in the redundancy analysis has none. The replacement prose above
therefore does not name it; the preceding paragraph in the chapter already
states the rule in words, which is enough.

---

## Fix 9 - Section 4.5 is a bullet list wearing bold labels

Nine bold-lead fragments, three of them beginning "(resolved)" - which is a task
tracker speaking, not a thesis. The thread here is tagged VERIFY and PROSE.

### Anchor

Starts: *"Figures verified (resolved). All structural, data-quality, and EDA figures"*
Ends: *"...or non-beverage categories is future research."*

### Action

REPLACE the entire section body.

#### Replace with

> Five risks bound the empirical claims that follow, and each is stated with the
> mitigation actually applied rather than the one available in principle.
>
> The first is the market hierarchy. The twenty-eight market values Nielsen
> exposes for carbonated soft drinks are nested rather than parallel, so
> aggregating across them counts the same sales at several levels and inflates
> category volume by a factor of 6.16. Every category is therefore scoped to the
> single DVH EXCL. HD market level, which eliminates the double-count by
> construction because no cross-market summation occurs, at the cost of
> excluding the structurally different hard-discount channel from the scope of
> the findings.
>
> The second is the imbalance between categories. Carbonated soft drinks
> contribute 4,370 brand-month observations across 95 brands where water
> contributes 1,189 across 29, so the four categories carry unequal evidential
> weight. The proportional split gives every category a training window of at
> least twenty-nine periods, so none is thin in the time dimension, but the
> cross-sectional imbalance remains and is not correctable within the available
> data. Carbonated soft drinks accordingly carry the primary claims, and the
> other three are reported as parallel replications whose agreement is evidence
> of transfer rather than independent confirmation.
>
> The third is that the pipeline parameters are empirical rather than
> theory-first. The lag set, the rolling windows and the peak-month sets are
> derived from this panel's own structure, and a different panel would yield
> different values. The minimum-history requirement is the exception: it follows
> from the feature specification and the forecast horizon by construction, and
> is not free to choose.
>
> The fourth is promotional coverage. Water and ready-to-drink beverages carry
> no promotional measure at all, so the promotional feature is omitted for those
> categories rather than zero-filled. A constant zero would assert that no
> promotion ran, which the data does not support; omission asserts only that
> nothing was recorded, which is what is true.
>
> The fifth bounds the generalisation. The findings hold for the DVH EXCL. HD
> scope, the observed period window and the series long enough to satisfy the
> retention rule. Applicability to other markets, to intermittent series, or to
> non-beverage categories is a question for future research rather than a claim
> of this thesis.

### Note - three risks were dropped, and why

**"Figures verified (resolved)"** and **"Per-category EDA (resolved)"** are
project-status entries. They record that work was completed, which no longer
needs saying once the chapter reports the results of that work.

**"Weighted-distribution imputation"** is dropped because the median imputation
it describes does not exist - see Fix 5. Leaving it would carry a
methodological limitation for a method the thesis does not use.

**"Commercial access / confidentiality"** is folded out pending the
confidentiality decision below. Add it back once that is settled.

---

# Decisions

---

## The confidentiality claim - still the most important open item

Section 4.1.1 states the data "is used under a confidentiality agreement with
Manifold AI". Your comment says no NDA was signed.

**This is the one item in the chapter that cannot be resolved by measurement**,
and it is the only one with consequences outside the document. An examiner may
reasonably ask to see an agreement the thesis asserts exists.

The sentence can be made true without one, because the substantive claim does
not depend on a signed instrument:

> **REWORD** - *"The data are commercial and are not redistributed: they remain
> in the local research environment and are not published with this thesis.
> Because access is commercial and restricted, the data could not have been
> collected independently within the scope of a thesis, which is itself a
> Saunders-listed advantage of using secondary data."*

This states the handling restriction you actually observe, drops the assertion
about a document, and keeps the Saunders point intact. **Confirm before
pasting** - if an agreement does exist, the original sentence is better.

---

## Citations - the chapter still rests on one source

The thread on the closing word of §4.5 notes that Chapter 4 cites Saunders
et al. and essentially nothing else.

That is defensible for a data chapter, whose content is measurement rather than
argument, but two places would carry a citation naturally if you want them:

- **The scanner-panel-as-secondary-data framing** in §4.1, currently Saunders
  alone. A retail-scanner methodology reference would sit here well.
- **The log transform for variance stabilisation** in §4.2.2, which is
  standard enough to cite from any forecasting text already in the library.

**Do not add the ARIMA minimum-periods citation from memory.** That is the one
in Fix 6, and it is what the register exists for. Either verify it in Zotero or
take the reworded sentence, which needs no source.

---

## What this pass did not touch

**Table 1, Table 2, Table 3 and the appendix question.** Four threads ask
whether these tables belong in an appendix. That is a layout decision that
depends on where the appendix lands, and it does not block the prose. My view:
Table 2 should go entirely, since Fix 7 and Fix 8 now state its contents in
prose where they are derived, and it carries two superseded figures. Tables 1
and 3 are earning their place in the body.

**The internal cross-reference "flagged in §4.6".** One thread notes this
points at a section that does not exist. It is a leftover from an earlier
numbering. Delete the clause; the sentence reads correctly without it.

**The repetition question.** Your reply on that thread already settles the
approach - one chapter establishes, the others cite - and records that it is a
final-pass job once the chapters are prose. Nothing here conflicts with that.
