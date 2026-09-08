---
name: ch4-verification-pass
description: NOTE - Chapter 4 second pass. Every claim in the chapter checked against the repository as it stands 2026-09-08. All 31 open threads answered.
snapshot: 2026-09-08_17-13_ch4-verification-pass
category: workflow
applies-to: [chapter 4, data assessment]
created: 2026_09_08-17_20
updated: 2026_09_08-17_20
status: ready
---

# Chapter 4 - verification pass

**Snapshot:** `shared_snapshot/2026-09-08_17-13_ch4-verification-pass`
**Threads open:** 31 (down from 39 - eight resolved by your last paste).

Every figure here was recomputed from the raw parquets, the engineered matrices
and the generation manifests on 2026-09-08. Anchors are given as the comment's
own **first and last words**, matching the locator column in the snapshot index.

## Read this first: the paste left a contradiction in 4.4

You pasted the new proportional-split prose, but **the old closing paragraph
survived underneath it**, and the Test column of Table 5 kept its old values.
The section now contradicts itself inside twelve lines.

| | Table says | Windows prove | Old paragraph says |
|---|---|---|---|
| CSD test | 12 | **7** (2026-01 to 2026-07) | "12-month test window" |
| danskvand | 8 | **6** | "8-month test window" |
| energidrikke | 8 | **7** | "8-month" |
| RTD | 8 | **6** | "8-month" |

Also: energidrikke's **Valid.** cell reads 7, should be **6**; RTD's test window
is missing a space before the arrow; and the trailing paragraph still says
*"All test windows end in March 2026"* when the table above it says July.

**Fix 1 - Table 5 numbers.** Replace the four data rows with:

| Category | Periods | Train | Valid. | Test | Train window | Validation window | Test window |
|---|---|---|---|---|---|---|---|
| CSD | 46 | 32 | 7 | 7 | 2022-10 - 2025-05 | 2025-06 - 2025-12 | 2026-01 - 2026-07 |
| danskvand | 41 | 29 | 6 | 6 | 2023-03 - 2025-07 | 2025-08 - 2026-01 | 2026-02 - 2026-07 |
| energidrikke | 43 | 30 | 6 | 7 | 2023-01 - 2025-06 | 2025-07 - 2025-12 | 2026-01 - 2026-07 |
| RTD | 41 | 29 | 6 | 6 | 2023-03 - 2025-07 | 2025-08 - 2026-01 | 2026-02 - 2026-07 |

**Fix 2 - delete the stale paragraph.** This is the anchor of four separate
comments (the VERIFY on the 12-month window, the SOURCE on the ARIMA minimum,
the METACOMMENT on section 4.6, and the INCORRECT on March 2026).

Starts: *"CSD, the longest series, takes a 12-month..."*
Ends: *"...at least one autumn/winter promotional cycle."*

**Action:** REPLACE.

**Replace with:**

> Each test window spans the six or seven most recent months of its category and
> ends in July 2026, the latest month in the panel. Every training window runs
> to at least twenty-nine periods, so the concern that a short category might
> not support stable parameter estimation does not arise at the current panel
> length; danskvand and RTD, the two shortest, train on twenty-nine months
> apiece. Because the windows are proportional rather than fixed, all four also
> shift forward together at each monthly refresh, so the test period remains the
> most recent data rather than drifting into the past as the panel grows.

This deletes the ARIMA-minimum citation from this section - the claim survives
in 4.1.4, where it is registered for verification rather than repeated twice.

---

# 1. What I got wrong last time, and what it means for the rest

**The weighted-distribution null rates in 4.1.3 are badly wrong, and I nearly
let them through.** Last pass I flagged them as unverified and moved on. You
asked for everything checked, so I measured them:

| | chapter says | actually |
|---|---|---|
| CSD | 0.019% | **7.115%** |
| danskvand | 0.016% | 0.022% |
| energidrikke | 0.093% | 0.089% |
| RTD | 0.000% | 0.000% |

CSD is out by a factor of nearly four hundred. Three of the four are close
enough to be rounding, which is exactly what made the fourth easy to miss.

**The same measurement contradicts a second claim in the same paragraph.** The
chapter ends 4.1.3 with *"Core sales metrics are complete: sales_units has 0.00%
nulls in every category, confirmed locally."* For CSD, `sales_units` is
**7.10% null**. The two figures matching almost exactly is not a coincidence:
the rows missing a distribution reading are the rows missing a sales reading.

That is a real finding about the data, not just an erratum. CSD carries a body
of fact rows - roughly seven per cent - where the product existed in the
dimension but recorded no sales at this market level in that period.

**Anchor.** Starts: *"Weighted-distribution nulls: negligible across all categories..."* (italicised in the document)
Ends: *"...0.093% (energidrikke), 0.000% (RTD)."*

**Action:** REPLACE.

**Replace with:**

> Missing values are concentrated in one category and one pattern. For
> danskvand, energidrikke and RTD the weighted-distribution field is essentially
> complete, with null rates of 0.022, 0.089 and 0.000 per cent. For CSD it is
> null in 7.1 per cent of in-scope fact rows, and the sales fields are null in
> the same 7.1 per cent - these are the same rows. They represent products
> listed in the category dimension that recorded no measurable activity at this
> market level in a given period, rather than a failure to observe a product
> that was selling. Because the modelling grain aggregates to brand and month
> over positive sales only, these rows are excluded before a feature is
> computed; they bear on how the raw panel should be described, not on the
> modelling input.

⚠ **The "brand-and-market median" imputation described in the next sentence
needs checking against your EDA session.** The engineered pipeline drops
non-positive rows at aggregation rather than imputing them, so a median
imputation of weighted distribution may be a step that no longer runs. I have
not been able to find it in the current preprocessing code.

**The negative and zero counts are close but not exact:**

| | chapter | actual |
|---|---|---|
| CSD negatives | 58 (0.031%) | 62 (0.028%) |
| danskvand | 14 (0.057%) | 17 (0.062%) |
| energidrikke | 16 (0.032%) | 16 (0.029%) |
| RTD | 10 (0.022%) | 10 (0.020%) |
| zero rows | 12 / 1 / 28 / 17 | 12 / 1 / **31** / 17 |

Small, but the percentages all move because the row base changed. That thread
is already marked resolved, so this is a numbers-only correction to make while
you are in the paragraph.

---

# 2. Section 4.2.2 - the stationarity paragraph has two wrong counts

**Anchor.** Starts: *"The logarithmic transformation is applied uniformly..."* (immediately under the Stationarity heading)
Ends: *"...non-positive/missing values rather than imputed."*

Measured on the current CSD matrix:

- The chapter says **nine** volume features with raw skewness **5.0 to 8.0**.
  There are **twelve**, and the range is **4.1 to 5.1**.
- Log-transformed skewness falls below **0.25** in absolute value, not 0.2.
- The chapter says tests have "limited power at 46 observations" - 46 is right
  now, but the same paragraph elsewhere says n = 42.
- ADF for CSD: raw p = 0.765, log p = 0.763, differenced p < 0.001. The chapter
  says 0.360 and 0.421, which are the old-scope values.

**Action:** REPLACE the whole subsection.

**Replace with:**

> A logarithmic transformation is applied uniformly to the target and to the
> volume-valued inputs rather than selected per brand. The distributional
> evidence is unambiguous: the twelve volume-valued columns carry raw skewness
> between 4.1 and 5.1, and none exceeds 0.25 in absolute value once
> transformed. Uniform treatment is preferred to per-series selection because
> the tests that would drive such a selection have limited power at
> forty-six observations, and because a transformation applied unevenly across
> brands would make the feature semantics inconsistent within the panel.
>
> On the aggregate monthly series the category level is non-stationary in both
> raw and logarithmic form - an augmented Dickey-Fuller test returns p = 0.77
> and p = 0.76 respectively - and becomes stationary only after first
> differencing, where p falls below 0.001. CSD is therefore difference-
> stationary. Non-stationarity in the mean is handled by differencing for the
> statistical baselines and by lagged and rolling features for the tree models,
> which do not require a stationary level. Non-positive and missing values are
> preserved as missing rather than imputed.

---

# 3. Section 4.2.4 - the autocorrelation figures

**Anchor.** Starts: *"Lag set: LAGS = (1, 2, 3, 4, 8, 13)..."* (immediately under the Autocorrelation heading)
Ends: *"...carry no promotional data (promo-zero)."*

The single-brand HARBOE figures are wrong, and the pooled ones need a sign
correction.

| | chapter | measured |
|---|---|---|
| HARBOE lag 1 | +0.26 | **+0.40** |
| HARBOE lag 3 | +0.47 | **+0.53** |
| HARBOE lag 13 | approx. 0 | **+0.26** |
| HARBOE n | 42 | **46** |
| pooled CSD lag 1 | +0.78 | +0.81 |
| promo correlation CSD | r = 0.937 | r = 0.939 |
| promo correlation energidrikke | r = 0.988 | r = 0.989 |

HARBOE is confirmed as the top brand by units (237.2M, ahead of Coca-Cola at
218.0M), so the choice of exemplar still holds.

**Action:** REPLACE.

**Replace with:**

> The lag set is one, two, three, four, eight and thirteen months, with rolling
> summaries over four and thirteen months, covering short-run persistence and
> the annual cycle on the Nielsen calendar. Autocorrelation is reported two
> ways because the two answer different questions. For the largest brand by
> volume, the log series carries a first-order autocorrelation of +0.40, a
> third-order of +0.53 and a thirteenth-order of +0.26 across forty-six
> months - the quarterly signal is the strongest, and an annual component is
> present but weaker. Pooling across all retained brands after demeaning each
> series gives +0.81, +0.60 and -0.16 for the same three lags: short-horizon
> dependence is stronger once between-brand level differences are removed,
> while the annual carry turns mildly negative. Lag structure is therefore
> brand-dependent, and a single global lag set is a deliberate simplification;
> per-brand optimisation is outside the scope of this study.
>
> Promotional intensity is strongly associated with volume where it is
> measured, at r = 0.94 for CSD across 2,765 promotion-bearing brand-months and
> r = 0.99 for energidrikke. Neither danskvand nor RTD carries promotional
> data at all.

⚠ **The pooled and single-brand lag-13 figures now disagree in sign** (+0.26
against -0.16). That is a real property of the demeaning, not an error, and the
prose above says so explicitly rather than papering over it.

---

# 4. Threads I could not answer last time

You said some comments had no answer in the previous document. These are those.

**"Each category follows a star schema..." (APPENDIX, 4.1.2).** The schema
description is accurate - I verified the four view files per category:
`dim_market`, `dim_period`, `dim_product` and a facts table keyed on
`market_id`, `period_id`, `product_id`. The product dimension does carry brand,
manufacturer, packaging, variant and type. What the chapter claims exists,
exists. The request for *"a reference to the to-be generated data model"* is a
figure that does not yet exist - that belongs to the figure-generation plan, not
to this pass.

**"A technical note carried over..." (METACOMMENT, 4.1.2).** Your tag is right:
this is a note to yourselves, not thesis prose. It says the note is "to be
re-verified in reproduction attempts". Both claims in it are true - period
identifiers are not calendar-monotonic, and the facts table does carry more
products than the active dimension. **Recommendation: keep the two facts, drop
the meta-framing.**

**Action:** REWORD.

**After:**
> "Two structural properties of the source affect any reproduction. Period
> identifiers are not monotonic with calendar time, so all time-series
> operations sort on the composite year-and-month key rather than the
> identifier. The facts table also contains more distinct products than the
> active product dimension, because discontinued and out-of-scope items retain
> their history; the join to the product dimension is therefore what scopes the
> data, not the facts table alone."

**"the promotional variants and the weighted-distribution proxy serve as
exogenous predictors" (VERIFY, 4.1.2).** Half true, and the half that is false
matters. `weighted_dist` **is** a model input (confirmed in the manifest feature
list). The raw promotional variants are **not** - only the derived
`promo_intensity` is, and `promo_units` is carried through the matrix for
description only. Your note asks *"perhaps we add the holiday calendar
enrichment"* - it is already there: `n_holidays` and `non_holiday_days` are in
all four matrices.

**Action:** REWORD.

**After:**
> "the weighted-distribution proxy and a promotional-intensity measure derived
> from the promotional variants serve as exogenous predictors, alongside a
> Danish public-holiday calendar joined onto the monthly grid."

**"Nielsen is an established commercial panel provider..." (SOURCE, 4.1.3).**
This cannot be sourced as written, because it is not a claim about Nielsen - it
is an inference from commercial incentive to data quality. Either it gets a
methodological citation on commercial panel reliability, or it is reframed as
the assumption it is. Registered as CV-C below. **I would reframe rather than
hunt for a source**, because the honest version is stronger:

**Action:** REWORD.

**After:**
> "Nielsen is an established commercial panel provider, and its data are treated
> here as reliable at the level of the recorded measures. This is an assumption
> rather than a verified property: the collection instrument, the market
> definitions and the metric conventions are fixed by the provider and cannot be
> independently audited from the delivered extract. What can be checked -
> internal consistency, completeness, and the hierarchy behaviour described
> above - was checked, and is reported in this section."

**"log_sales_units is the modelling target..." (VERIFY & SOURCE, 4.3).**
Verified true in the manifest: `target_col` is `sales_units` with
`log_transform_target: true`, and neither `log_sales_units` nor `promo_units`
appears in the feature list. No change needed. The SOURCE tag here is asking for
a citation on leakage, which is a textbook point - registered as CV-E.

**"so the tree models handle NaN natively..." (SOURCE, 4.3).** True of both
libraries and documented by both. Registered as CV-D. No prose change.

**"Table 4 - Feature Engineering Overview" (VERIFICATION, 4.3).** The table
lists fourteen feature names across seven rows. The manifest says **34 features
for CSD**. The table is not wrong so much as incomplete - it lists the
*engineered* features and omits the twenty-odd Nielsen distribution measures
that are also inputs. Given the appendix decision below, **my recommendation is
that this table moves to the appendix in full and the text keeps a sentence
naming the families**, which is also what the 4.3 prose you already pasted
implies.

---

# 5. Still outstanding from the last pass

These blocks were in the previous note and have not been applied. Anchors
re-verified against the new snapshot.

| What | Anchor starts | Anchor ends |
|---|---|---|
| Table 4.1 regeneration | "RTD \| 41 \| 101" (the table row) | "2,442 \| 2,509" |
| Metadata note under Table 1 | "These figures are recomputed locally under DVH EXCL. HD and supersede" | "per regeneration_report.md)." |
| "Worked category" reframing | "The three proof-of-concept categories were" | "gap previously flagged in section 4.6." |
| Span correction | "37-42-month span exceeds the ARIMA" | "decomposition and gradient-boosted models." |
| Superseded filter counts | "retained by the ≥30-month filter (77 / 24 / 27 / 42" | "confounded by very short series;" |
| Thin-window risk deletion | "Figures verified (resolved). All structural," | "non-beverage categories is future research." |
| 4.2.1 structural counts | "Market scope: DVH EXCL. HD (single Nielsen market level" | "(correct for an ACV metric)." |
| 4.2.6 per-category table | "RTD \| none (promo-zero) \|" | "level \| +0.82 / +0.58" |

The regenerated Table 4.1, measured from raw facts with the DVH EXCL. HD filter:

| Category | Periods | Brands in scope | Brands retained | Catalog SKUs | In-scope SKUs | Brand-month rows | In-scope fact rows |
|---|---|---|---|---|---|---|---|
| CSD | 46 | 142 | 95 | 2,130 | 7,991 | 4,209 | 223,240 |
| danskvand | 41 | 55 | 29 | 1,071 | 1,913 | 1,225 | 27,449 |
| energidrikke | 43 | 68 | 44 | 1,271 | 4,083 | 1,702 | 55,216 |
| RTD | 41 | 101 | 62 | 728 | 2,442 | 2,509 | 49,976 |

And the per-category EDA table for 4.2.6:

| Category | Promo | Peak months | ADF (level) | ADF (differenced) | Pooled ACF lag 1 / 3 / 13 |
|---|---|---|---|---|---|
| CSD | r = 0.94 | 3, 6, 9, 12 | p = 0.76 | p < 0.001 | +0.81 / +0.60 / -0.16 |
| danskvand | none | 6, 7, 8, 9 | p = 1.00 | p < 0.001 | +0.63 / +0.36 / -0.06 |
| energidrikke | r = 0.99 | 3, 6, 9 | p = 0.77 | p < 0.001 | +0.83 / +0.59 / -0.15 |
| RTD | none | 5, 6, 12 | **p < 0.001** | p < 0.001 | +0.86 / +0.66 / -0.04 |

RTD is stationary in level; the other three are difference-stationary.

---

# 6. Claims register

| # | Claim | Where | To verify |
|---|---|---|---|
| CV-A | ARIMA requires roughly 24 periods for stable parameter identification | 4.1.4 | Does an authoritative forecasting text state a minimum series length for ARIMA, and is it ~24? If not, reword to rest on the observed 29-46 periods. |
| CV-B | Prophet requires at least two seasonal cycles | 4.4 | Does the Prophet documentation or paper state a minimum? |
| CV-C | Commercial panel providers are reliable because their business depends on credibility | 4.1.3 | Is there a methodological source, or is this an assumption? The reword above assumes the latter. |
| CV-D | LightGBM and XGBoost handle NaN natively | 4.3 | Both document this; cite the docs. |
| CV-E | Using the contemporaneous target as a predictor constitutes leakage | 4.3 | Standard; cite a forecasting or ML methodology text. |

**On the "only one source in the whole chapter" thread:** five claims carry the
entire unsourced methodological load, and they are all above. A data-assessment
chapter legitimately cites little, but five unsourced rules of thumb is a
different thing from a chapter that has little to cite.

---

# 7. Decisions

| Where | Question |
|---|---|
| 4.1.1, on *"confidentiality agreement with Manifold AI"* | **You never signed an NDA.** The chapter asserts one exists. Still open, still the most important item here - it is a factual claim about a legal document in a submitted thesis. |
| Chapter title, on *"From Scanner Panel to Modelling Matrix"* | Keep the subtitle or drop it? |
| 4.1.2, 4.2.5, 4.2.6, 4.3 tables | Appendix split. My recommendation: Table 4.1 as regenerated stays in text; the parameter summary, the per-category EDA grid and the full feature table move to the appendix with a short summary retained. |
| 4.1.3 | Does the weighted-distribution median imputation still run? I cannot find it in the current preprocessing code, and the prose describes it as active. |

---

# 8. Does the chapter hold together?

You asked. My honest read, now that every number in it has been checked:

**The structure is sound and the argument is the right one.** Saunders' three
stages, a worked category, per-category replication, then the split and the
risks - that sequence does what a data-assessment chapter should do.

**Two things undermine it as written.**

First, **the chapter describes a pipeline that has been superseded in at least
four places** - the fixed split, the >=30 filter, the 22-column matrix, the
proof-of-concept framing. Each was true once. Together they read as a chapter
written against a pipeline that no longer exists, and a reader who checks any
one of them loses confidence in the rest.

Second, **the provenance scaffolding is still visible.** References to a
personal audit, to superseding earlier values, to a `regeneration_report.md`,
to a section 4.6 that does not exist. These are working notes that survived into
the document, and they signal an unfinished draft more strongly than any of the
individual numbers do.

**Neither is a structural problem.** Both are fixed by the replacements in this
note and the previous one. The chapter does not need rethinking - it needs its
numbers brought to the present and its scaffolding removed.

The one place I would push back on the chapter's own logic is the
worked-category framing, which the code contradicts, and which is covered in
the outstanding block above.
