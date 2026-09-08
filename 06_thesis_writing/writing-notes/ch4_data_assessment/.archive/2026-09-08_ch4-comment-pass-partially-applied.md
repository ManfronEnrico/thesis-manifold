---
name: ch4-comment-pass
description: NOTE - Chapter 4 full comment pass. All 39 Word threads. Every number re-measured from the live artefacts on 2026-09-08. Anchors quoted verbatim with first/last words so they can be found by search.
snapshot: 2026-09-08_15-43_dynamic-naming-verified
category: workflow
applies-to: [chapter 4, data assessment]
created: 2026_09_08-16_30
updated: 2026_09_08-17_45
status: ready
---

# Chapter 4 - comment pass

**Snapshot:** `shared_snapshot/2026-09-08_15-43_dynamic-naming-verified`
**Threads:** 39, all with a verdict. **Decisions needed from you:** 3.

Every figure below was recomputed from the raw parquets, the engineered
matrices and the generation manifests on 2026-09-08. Nothing is quoted from
the chapter or from memory.

```
CSD            rows=4370 cols=54 brands=95 n_features=34 min_p=17 peaks=[3,6,9,12] promo=True
Danskvand      rows=1189 cols=36 brands=29 n_features=26 min_p=17 peaks=[6,7,8,9]  promo=False
Energidrikke   rows=1892 cols=54 brands=44 n_features=34 min_p=17 peaks=[3,6,9]    promo=True
RTD            rows=2542 cols=52 brands=62 n_features=33 min_p=17 peaks=[5,6,12]   promo=False
```

**How to find each edit:** every block gives the comment's anchor text with its
**opening words** and **closing words**, so you can search the document for
either end. Comment numbers are not shown in Word, so they are omitted here.

---

# 1. Section 4.4 - the split section is wrong in every particular

Five INCORRECT threads, one root cause. **Every cell of Table 5 is wrong,
including the period counts.**

| Chapter claims | Artefacts say |
|---|---|
| split fixed by calendar date, "locked, pre-registered" | proportional 70/15/15, derived per category |
| CSD 42 periods, 24/6/12 | CSD **46** periods, **32/7/7** |
| test windows end March 2026 | all four end **2026-07** |
| CSD takes a 12-month test window | CSD test is **7 months** |
| danskvand/RTD 23 training months | **29** |

`DEFAULT_TRAIN_FRAC = 0.70` and `DEFAULT_VAL_FRAC = 0.15`
(`engineer_features.py:71-72`) mean the boundaries move whenever the panel is
re-pulled. That is a defensible design, not a defect - it just has to be
described as what it is.

**Anchor** - opening paragraph of 4.4.
Starts: *"The split is defined by calendar date and locked..."*
Ends: *"...into training or validation."*

**Action:** REPLACE - from that sentence through the end of the paragraph that
starts *"CSD, the longest series, takes a 12-month..."* and ends
*"...one autumn/winter promotional cycle."*, **including Table 5 and its
caption**.

**Replace with:**

> The split is defined proportionally rather than by fixed calendar date. Each
> category panel is divided into contiguous chronological blocks by share of its
> available periods - seventy per cent for training, fifteen for validation and
> the remainder for testing - so the cut-off dates are derived from the data and
> move when the panel is extended. No random shuffling is applied: a strict
> temporal ordering preserves the autocorrelation structure and prevents future
> observations from leaking into training or validation.
>
> The proportional rule is preferred to a fixed date for a reason specific to
> this panel. The four categories differ in length by five months, and the
> database is re-pulled monthly, so any date written into the protocol would
> allocate a different share of each category to testing and would silently
> change that allocation at the next refresh. Expressing the split as a
> proportion makes the design invariant to both, at the cost that the boundary
> dates are an output of the pipeline rather than an input to it. They are
> recorded per category and per horizon in `<category>_split_dates_h<H>.json`
> alongside the feature matrix, so any reported result can be traced to the
> exact windows that produced it.
>
> The boundaries below are those in force at the three-month horizon.

| Category | Periods | Train | Valid. | Test | Train window | Validation window | Test window |
|---|---|---|---|---|---|---|---|
| CSD | 46 | 32 | 7 | 7 | 2022-10 - 2025-05 | 2025-06 - 2025-12 | 2026-01 - 2026-07 |
| danskvand | 41 | 29 | 6 | 6 | 2023-03 - 2025-07 | 2025-08 - 2026-01 | 2026-02 - 2026-07 |
| energidrikke | 43 | 30 | 6 | 7 | 2023-01 - 2025-06 | 2025-07 - 2025-12 | 2026-01 - 2026-07 |
| RTD | 41 | 29 | 6 | 6 | 2023-03 - 2025-07 | 2025-08 - 2026-01 | 2026-02 - 2026-07 |

> **Table 5** - Proportional train/validation/test boundaries per category, derived at the three-month horizon.

> All four test windows end in July 2026, the most recent month in the panel,
> and each spans six or seven months. Every training window comfortably exceeds
> the twenty-four periods conventionally cited as a minimum for stable ARIMA
> parameter identification: the shortest is twenty-nine. This removes the
> thin-training-window caveat that earlier drafts attached to danskvand and RTD,
> which arose from the older fixed-date split rather than from the data.

---

# 2. Section 4.1.2 - Table 4.1 regenerated

You asked me to regenerate rather than flag. Done - recomputed from the raw
facts, product and market dimensions with the `DVH EXCL. HD` filter applied.

**Anchor** - Table 4.1 itself, and the note beneath it.
The note starts: *"CSD figures supersede Brian's all-markets values..."*
and ends: *"...The bold column (>=30) is the retained set used downstream."*

**Action:** REPLACE the table and the entire note beneath it.

**Replace with:**

| Category | Periods | Brands in scope | Brands retained | Catalog SKUs | In-scope SKUs | Brand-month rows | In-scope fact rows |
|---|---|---|---|---|---|---|---|
| CSD | 46 | 142 | 95 | 2,130 | 7,991 | 4,209 | 223,240 |
| danskvand | 41 | 55 | 29 | 1,071 | 1,913 | 1,225 | 27,449 |
| energidrikke | 43 | 68 | 44 | 1,271 | 4,083 | 1,702 | 55,216 |
| RTD | 41 | 101 | 62 | 728 | 2,442 | 2,509 | 49,976 |

> **Table 1** - Per-category structure at the DVH EXCL. HD market scope, at the three-month forecast horizon.

> The retention threshold is not chosen; it is derived. A brand is usable only
> if it has enough history to fill the deepest lag and the widest rolling window
> the feature set requires, plus the forecast horizon, plus one row to predict.
> With a thirteen-month lag and a thirteen-month window the warm-up is thirteen
> periods, so the threshold is fifteen at a one-month horizon and seventeen at
> three. Deriving it this way rather than fixing a round number has a
> consequence worth stating: the threshold moves with the horizon, so the
> retained set is a property of the forecasting question being asked rather than
> a preprocessing decision taken before it.
>
> The columns distinguish two counts that are easily conflated. Catalog SKUs are
> the products Nielsen lists in the category dimension; in-scope SKUs are those
> with positive recorded sales at this market level. The gap between them - and
> the gap between brands in scope and brands retained - is where the category
> differences that matter for modelling appear. RTD lists the fewest products
> but the second-highest brand count, while danskvand carries a large catalog
> against a small active panel.

**Three corrections this makes, beyond the ones you flagged:**

1. **"8,608 catalog SKUs" is wrong; it is 2,130.** The dimension table has
   exactly 2,130 rows. The deleted note claimed 8,608 "supersedes the earlier
   2,080" - it was superseding the more nearly correct figure with a wrong one.
   8,608 is close to the in-scope SKU count (7,991), so the two were most
   likely transposed at some point.
2. **The "retained >=40 / >=30" columns are gone.** That rule no longer exists.
3. **All four period counts changed** (42/37/39/37 to 46/41/43/41).

**On the metadata note you flagged:** you are right that it does not belong in
the thesis. It is provenance - who computed what, superseding whose earlier
audit, and a pointer to `regeneration_report.md`. The column definitions inside
it are legitimate content, so I have folded the two that a reader actually needs
into the prose above and dropped the rest. The 6.16x inflation finding is worth
keeping, but it already appears properly in 4.1.3, where it is part of the
argument rather than a footnote.

---

# 3. "The worked category" framing is contradicted by the code

You said you did not know whether the justification was real, and asked me to
look for a contrary argument. **There is one, and it is decisive.**

`srq1_pooled.py` exists specifically to answer *"does a per-category model beat
a single pooled model?"*. Its design note reads:

> "train ONE pooled model, then score it SEPARATELY on each category's test rows,
> against the per-category model on those SAME rows."

`05_thesis_results/05_model_benchmark/models/` holds a trained model directory
for **each of the four categories**, plus `pooled_params.json`. And
`srq4_experiment.py:880` selects the experiment sample as
`_select_brands(per_cat=(4, 4, 4, 3))` - four brands from each of three
categories and three from the fourth.

So all four categories are trained, tuned, benchmarked and carried into the
scenario experiment. **CSD is not the worked category and the other three are
not proofs of concept.** The framing is a leftover from when CSD was the only
category processed, and it now understates the design: the whole point of
running four is that pooling can be tested against specialisation, which needs
four real categories.

**Anchor** - opening of 4.2.
Starts: *"CSD is the worked category. The structural counts..."*
Ends: *"...replication under the corrected scope is pending (Section 4.6)."*

**Action:** REPLACE.

**Replace with:**

> CSD is presented first and in the greatest detail. It is the largest panel on
> every axis - forty-six periods against forty-one to forty-three, ninety-five
> retained brands against twenty-nine to sixty-two, and 4,370 brand-month
> observations against 1,189 to 2,542 - so it is where the exploratory evidence
> is thickest and the parameter choices are easiest to see. It is not, however,
> a pilot from which the others are extrapolated. All four categories are
> processed through the same pipeline, trained and tuned independently, and
> carried into both the pooled-versus-specialised comparison of Chapter 5 and
> the scenario experiment of Chapter 8. The three categories reported in Section
> 4.2.6 are full members of the design, and the differences between them -
> in seasonal profile, promotional coverage and panel size - are what makes the
> generalisation question answerable at all.

**This also fixes:** the *"Brian's all-markets audit"* metadata reference (also
flagged by the METADATA tags in 4.2.1 through 4.2.4), and the dangling forward
reference to Section 4.6, which does not exist.

⚠ The same framing recurs in **4.5**, in the risk item that starts *"Thin
training windows (danskvand, RTD)."* - handled in section 6 below.

---

# 4. Section 4.2 EDA - every statistic re-measured

You asked for these checked against the repository as it stands now. All
recomputed from the current feature matrices.

| | CSD | danskvand | energidrikke | RTD |
|---|---|---|---|---|
| periods | 46 | 41 | 43 | 41 |
| ADF raw | p = 0.765 | p = 0.999 | p = 0.876 | **p = 0.000** |
| ADF log | p = 0.763 | p = 0.998 | p = 0.766 | **p = 0.000** |
| ADF differenced | p < 0.001 | p < 0.001 | p < 0.001 | p < 0.001 |
| peak months | 3, 6, 9, 12 | 6, 7, 8, 9 | 3, 6, 9 | 5, 6, 12 |
| pooled ACF lag 1 | +0.81 | +0.63 | +0.83 | +0.86 |
| pooled ACF lag 3 | +0.60 | +0.36 | +0.59 | +0.66 |
| pooled ACF lag 13 | **-0.16** | **-0.06** | **-0.15** | **-0.04** |
| promo correlation | r = 0.939 | none | r = 0.989 | none |

**Two chapter claims fail this check.**

**(a) "near-zero lag-13 carry" is wrong in sign.** Lag-13 autocorrelation is
negative in all four categories, from -0.04 to -0.16. Describing it as
near-zero is defensible for RTD but not for CSD at -0.16.

**(b) CSD's December share is 11.5 per cent, not 12.8**, and the ordering has
changed: December 11.5, June 11.1, March 9.9, May 8.9. September - which the
chapter names as "next at 8.5%" - is no longer in the top four.

**Anchor** - the stationarity summary in 4.2.6.
Starts: *"Three of the four category-level series are difference-stationary..."*
Ends: *"...not separately optimised (a stated scope bound)."*

**Action:** REPLACE.

**Replace with:**

> Three of the four category aggregates are difference-stationary: the level
> series does not reject a unit root in either raw or logarithmic form, but the
> first difference rejects it decisively. RTD is the exception, rejecting in
> level. All four show strong positive short-horizon dependence, with a pooled
> brand-demeaned first-order autocorrelation between +0.63 and +0.86 and a
> third-order value between +0.36 and +0.66, which is what the lag and rolling
> feature set is built to exploit. The thirteenth lag is consistently negative
> rather than absent, ranging from -0.04 to -0.16; it is retained because a
> mild negative annual carry is still information, but it should not be
> described as a seasonal signal. Seasonality is category-appropriate and
> genuinely distinct across the four: water peaks across the summer, carbonated
> soft drinks at the quarter ends, energy drinks likewise but with no December
> peak, and ready-to-drink beverages in early summer and December. Promotional
> data exist for two categories only.

**Anchor** - seasonality, in 4.2.3.
Starts: *"Peak months (share of annual units, DVH EXCL. HD): December (12.8%)..."*
Ends: *"...September is next at 8.5%."*

**Action:** REPLACE.

**Replace with:**

> Measured as share of annual units at this market scope, CSD's heaviest months
> are December at 11.5 per cent, June at 11.1, March at 9.9 and May at 8.9. The
> peak-month indicator is not taken from these shares directly: a month enters
> the set when its mean units exceed the category mean by more than ten per
> cent, which for CSD selects March, June, September and December.

⚠ **The seasonality section also carries a naming justification worth keeping.**
The paragraph explaining that `PEAK_MONTHS` was renamed from `HOLIDAY_MONTHS`
because no holiday calendar was an input is **no longer true** - the pipeline
now carries `n_holidays` and `non_holiday_days` from the Nager.Date calendar.
The rename was still correct, but the reason must change: peak months are
derived from sales, and the holiday calendar is a separate feature. Left for
you to decide how much of that history to keep in the text.

**On 4.2.1's structural counts:** *"Span: 42 monthly periods"* and *"Brands: 136
total... retains 77 brands and 3,077 brand-month rows"* are superseded by 46
periods, 142 brands in scope and 95 retained across 4,209 brand-month rows,
per the regenerated Table 4.1 above.

---

# 5. Section 4.3 - feature counts

**"22 columns: 17 modelling features" is wrong, and the count is not constant
across categories** - which the chapter never says.

**Anchor.** Starts: *"The feature matrix contains 22 columns: 17 modelling..."*
Ends: *"...scripts/srq1_benchmark_tuned.py)."*

**Action:** REPLACE.

**Replace with:**

> The matrix width is category-dependent, because two of the four categories
> carry no promotional measures. CSD and energidrikke have fifty-four columns of
> which thirty-four are model inputs; RTD has fifty-two and thirty-three, and
> danskvand thirty-six and twenty-six. The remaining columns are the identifier,
> the raw and log-transformed targets, the split label, and the Nielsen measures
> retained for description but excluded from the input set by the admissibility
> rule above. The per-category counts are recorded in the generation manifest
> written beside each matrix.

**Anchor** - the stale ordinal.
Starts: *"and weighted_distribution is the fourteenth input feature..."*
Ends: *"...(only its derived promo_intensity is)"*

**Action:** REWORD.

**After:**
> "and `weighted_distribution` is admitted as an input in its own right, while
> the raw `promo_units` column is carried through the matrix for description
> only - the model sees the derived `promo_intensity` instead."

**Holiday enrichment is already shipped.** `n_holidays` and `non_holiday_days`
are present in all four matrices, and the chapter's own feature table already
lists them. That thread can be closed. Whether the enrichment *helped* is a
benchmark-chapter question and is blocked on the re-run.

---

# 6. Section 4.1.4 and 4.5 - two places where you were right and the chapter was backwards

**Zero versus null.** You wrote *"I believe our current code does the exact
opposite."* Confirmed. `engineer_features.py:341` reads
`.transform(lambda s: s.replace(0, np.nan).ffill().fillna(0))` - zeros are
converted **to** nulls before forward-filling.

**Anchor.** Starts: *"it is fully populated (0.00% null), with the absence..."*
Ends: *"...encoded as a zero rather than a null"*

**Action:** REWORD.

**After:**
> "it is fully populated (0.00 per cent null). A recorded zero is treated as
> genuinely unmeasured rather than as evidence of no promotion: the pipeline
> converts zeros to nulls and carries the last observed value forward, on the
> reasoning that an absent promotional record for a brand-month is more
> plausibly a gap in reporting than a confirmed absence of trade activity. Where
> no earlier value exists the feature falls back to zero."

**Negatives.** You remembered this correctly too - the justification is
uncertainty, not a settled reading. `engineer_features.py:345` is a bare
`clip(lower=0)`.

**Anchor.** Starts: *"negatives are return/correction adjustments standard..."*
Ends: *"...and are clipped to zero"*

**Action:** REWORD.

**After:**
> "negatives are floored at zero. They are conventionally read as return and
> correction adjustments, but the panel carries no field distinguishing a
> genuine return from a measurement error, so the treatment is a decision taken
> under that ambiguity rather than an interpretation the data support."

**The thin-training-window risk is now false and must be deleted, not softened.**

**Anchor.** Starts: *"Thin training windows (danskvand, RTD). Both have only..."*
Ends: *"...restated in the discussion."*

**Action:** REPLACE.

**Replace with:**

> **Category imbalance.** The four categories differ substantially in evidential
> weight: CSD contributes 4,370 brand-month observations across ninety-five
> brands, where danskvand contributes 1,189 across twenty-nine. The proportional
> split gives every category a training window of at least twenty-nine periods,
> so no category is thin in the time dimension, but the cross-sectional
> imbalance remains and bears on the pooled-versus-specialised comparison, where
> a pooled model is necessarily fitted more to CSD than to the rest.
> Mitigation: that comparison is scored per category on identical test rows
> rather than in aggregate, so the imbalance affects what is learned but not
> how it is measured.

⚠ Also in 4.5: **"under DVH EXCL. HD + MIN_PERIODS=30"** in the market-scope
risk item. Replace with **"under DVH EXCL. HD"** - the threshold is 17 and
derived.

---

# 7. Section 4.1.5 - one immediate correction, one citation

**Anchor.** Starts: *"The 37-42-month span exceeds the ARIMA minimum..."*
Ends: *"...by both decomposition and gradient-boosted models."*

**Action:** REWORD the opening clause only.

**After:** *"The panel spans forty-one to forty-six months by category."*

The rest of the sentence depends on a citation I will not write from memory.
Registered below.

The *"at least 30-month filter (77 / 24 / 27 / 42 brands)"* later in the same
section is the superseded rule; the counts become 95 / 29 / 44 / 62.

---

# 8. Claims to verify

For `writing-notes/unverified-claims-to-check.md`. Each is phrased to be
answerable yes or no against a document.

| # | Claim as the thesis states it | Where | To verify |
|---|---|---|---|
| CV-A | ARIMA requires roughly 24 periods for stable parameter identification | 4.1.5, 4.4 | Does an authoritative forecasting text state a minimum series length for ARIMA estimation, and is it ~24? If not, reword to rest on the observed 29-46 periods. |
| CV-B | Prophet requires at least two seasonal cycles | 4.4 | Does the Prophet documentation or paper state a minimum number of cycles? |
| CV-C | Nielsen scanner data are reliable because a commercial provider depends on credibility | 4.1.4 | Is there a methodological source on commercial panel reliability, or is this the author's own reasoning? If the latter, mark it as such. |
| CV-D | LightGBM and XGBoost handle NaN natively | 4.3 | Both document this; cite the docs rather than asserting it. |

**On the "only one source in the whole chapter" thread:** that is the real
structural problem here and it cannot be fixed by inserting citations into
existing sentences. The four claims above are the entire unsourced
methodological load. A data-assessment chapter legitimately cites little, but
four unsourced rules of thumb is a different thing from a chapter that has
little to cite.

---

# 9. Decisions I still need

| Where | Question |
|---|---|
| Chapter title, on *"From Scanner Panel to Modelling Matrix"* | Keep the subtitle or drop it? |
| 4.1.1, on *"confidentiality agreement with Manifold AI"* | **You never signed an NDA.** The chapter asserts one exists. This is a factual claim about a legal document in a submitted thesis - only you can settle it. |
| 4.1.2, 4.2.5, 4.2.6 tables | Appendix split - do you want the full tables moved to an appendix with a reduced summary in text? I recommend yes for the parameter and per-category tables; Table 4.1 as regenerated above is small enough to stay. |

The cross-chapter repetition thread is deferred by your own reply on it - final
pass once all chapters are prose.

---

# What I did not touch

**The null percentages in 4.1.4** (0.019 / 0.016 / 0.093 / 0.000 per cent for
weighted-distribution nulls, and the negative-value row counts). These come from
a scan of the raw facts I have not re-run, and the market-scope filter I used
for Table 4.1 is not obviously the same one those figures were computed under.
Given that the catalog-SKU figure in the same region of the chapter turned out
to be wrong by a factor of four, I would rather regenerate them explicitly than
carry them forward on the assumption that they are fine. Say the word and I will
compute them.
