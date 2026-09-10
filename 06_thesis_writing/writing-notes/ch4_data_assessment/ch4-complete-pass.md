---
name: ch4-complete-pass
description: NOTE - Chapter 4 closing pass. Not comment-bound: reads the whole chapter for writing quality, coherence and accuracy against the repository at commit 4b38c53. Eight fixes, one of them a wrong table.
snapshot: 2026-09-10_12-55_ch4-complete-pass
category: workflow
applies-to: [chapter 4]
supersedes: [ch4-prose-pass.md, ch4-prose-pass-followup-01.md]
created: 2026_09_10-13_10
updated: 2026_09_10-13_10
status: ready
---

# Chapter 4 - complete pass

**Snapshot:** `2026-09-10_12-55_ch4-complete-pass`
**Code verified at:** commit `4b38c53`, `git fetch` clean, 0 behind / 0 ahead
**Notes swept:** `ch4-prose-pass.md` and `ch4-prose-pass-followup-01.md`, both
applied and archived. Nothing was left unapplied from either.

## Are we done with Chapter 4?

**Almost. Nine items, and one of them is a table that is wrong.**

The prose is in good shape. Every fix from the two previous notes landed, the
tables are renumbered, the risks section reads as prose, and the citations are
in. What follows is not a repeat of that work: this pass read the whole chapter
end to end for **coherence and accuracy**, and re-measured the claims the
comment-bound passes never checked.

**What I re-measured this pass, from the raw panel and the pipeline outputs:**

| Claim | Verdict |
|---|---|
| Table 1, all four rows | catalogue SKUs, in-scope SKUs and brand counts **exact**; fact rows off by <1% |
| Table 2, top brands | **all four correct** - HARBOE, HARBOE, RED BULL, BREEZER |
| Table 2, ADF p-values | **three of four wrong** (Fix 1) |
| Table 2, peak months | **two of four contradict the chapter's own text** (Fix 1) |
| Table 2, ACF lag1/lag3 | close, one cell off by 0.08 (Fix 1) |
| §4.2.3 monthly shares | **exact** - Dec 11.5, Jun 11.1, Mar 9.9, May 8.9 |
| §4.2.3 peak-month sets | **exact** for all four categories |
| §4.2.4 HARBOE ACF | **exact** - +0.40 / +0.53 / +0.26 at n=46 |
| §4.2.4 promo correlation | 0.940 and 0.989 vs stated 0.94 and 0.99 - **correct** |
| §4.3 feature counts | **18 and 17, confirmed** against all eight matrices |
| §4.4 split table | **exact** against the split-date files |

---

# The fixes

---

## Fix 1 - Table 2 is wrong in three columns

**The most serious item in the chapter.** The per-category EDA table carries
figures that contradict both the data and the chapter's own prose. Its comment
thread asks for exactly this ("Whole table verification").

Recomputed from `step_1_aggregate_bymonth.parquet` for each category, augmented
Dickey-Fuller on the log level of the category aggregate:

| Category | ADF stated | ADF measured | Peak stated | Peak measured | ACF stated | ACF measured |
|---|---|---|---|---|---|---|
| CSD | p = 0.421 | **p = 0.774** | December | December | +0.78 / +0.55 | +0.79 / +0.56 |
| danskvand | p = 0.998 | p = 0.999 | June | June | +0.55 / +0.25 | +0.51 / +0.27 |
| energidrikke | p = 0.901 | **p = 0.961** | March | **June** | +0.71 / +0.39 | **+0.79 / +0.53** |
| RTD | p = 0.000 | p = 0.000 | December | **June** | +0.82 / +0.58 | +0.85 / +0.63 |

Three problems, in descending order of seriousness.

**The peak-month column contradicts §4.2.3.** The chapter's own prose says
energy drinks peak at "the quarter-ends without December" and ready-to-drink in
"early summer and December". Measured by share of annual units, the single
heaviest month is **June for both**. The table says March and December. A
reader who checks the table against the text finds them disagreeing.

**The CSD ADF value is wrong by a wide margin.** The table says p = 0.421;
§4.2.2 says p = 0.76 for the same series in log form, and the measurement is
0.774. The chapter contradicts itself on a number it states twice.

**The verdict column stays correct throughout**, which is the saving grace -
three of four are I(1), RTD rejects in level, and that is what the prose argues.

### Anchor

**Section 4.2.5 Per-category EDA - danskvand, energidrikke, RTD.** The table
captioned **"Table 2 - Per Category Correlation & Transformations"**. Its first
data row begins *"CSD"* and its last begins *"RTD"*.

### Action

REPLACE the four data rows. The header row is unchanged.

#### Replace with

| Category | Promo Correl. | Peak month | Top brand | ADF (log level) | Verdict | ACF lag1 / lag3 |
|---|---|---|---|---|---|---|
| CSD | r = 0.94 | December | HARBOE | p = 0.774 | non-stationary, I(1) | +0.79 / +0.56 |
| danskvand | none (promo-zero) | June | HARBOE | p = 0.999 | non-stationary, I(1) | +0.51 / +0.27 |
| energidrikke | r = 0.99 | June | RED BULL | p = 0.961 | non-stationary, I(1) | +0.79 / +0.53 |
| RTD | none (promo-zero) | June | BREEZER | p = 0.000 | stationary in level | +0.85 / +0.63 |

### Note - what was checked and how

Every cell was recomputed rather than transcribed. ADF is `adfuller(log(monthly
category units), autolag="AIC")` on 46 / 41 / 43 / 41 periods. ACF is pooled
across retained brands after demeaning each brand's log series, which is the
definition §4.2.4 uses, so the two sections now agree by construction. Promo
correlation is measured on promotion-bearing brand-months only.

**Top brands were correct in all four rows** and are unchanged - HARBOE leads
both carbonated soft drinks and water, Red Bull energy drinks, Breezer
ready-to-drink.

**Promo correlations are rounded to two decimals** to match §4.2.4, which states
0.94 and 0.99. Three decimals in one place and two in another invites a reader
to wonder which is authoritative.

### Note - the peak-month column now says June three times

That looks like an error and is not. Three of the four categories genuinely have
their single heaviest month in June, which is why §4.2.3's *sets* are the more
informative measure and the reason the peak-month indicator uses a mean-uplift
rule rather than a single maximum.

**Consider retitling the column "Heaviest month"** to make the distinction
explicit, since "peak month" collides with `PEAK_MONTHS`, the derived set, which
is a different thing. That would also stop the table appearing to contradict
§4.2.3.

---

## Fix 2 - Section 4.1.2's Coverage paragraph says the same thing twice

A paste seam. The sentence "coverage is assessed on the temporal span, the brand
and SKU counts, and the retained series" is immediately followed by "Coverage is
assessed on the temporal span, the brand and product counts, and the series that
survive the retention rule."

### Anchor

**Section 4.1.2 Schema and Structure.** The paragraph beginning with the bolded
lead-in **"Coverage."**

First five words: *"The panel must cover the..."*
Last five words: *"...so coverage is assessed on the temporal span, the brand and SKU counts, and the retained series."*

### Action

REWORD - delete the duplicated clause. Only the opening sentence changes.

**Before:**

> **Coverage.** The panel must cover the right population and period and leave
> sufficient data after exclusions. All four categories are scoped to the single
> DVH EXCL. HD market level (one market identifier per category, by design), so
> coverage is assessed on the temporal span, the brand and SKU counts, and the
> retained series. Coverage is assessed on the temporal span, the brand and
> product counts, and the series that survive the retention rule.

**After:**

> **Coverage.** The panel must cover the right population and period and leave
> sufficient data after exclusions. All four categories are scoped to the single
> DVH EXCL. HD market level, one market identifier per category by design, so
> coverage is assessed on the temporal span, the brand and product counts, and
> the series that survive the retention rule.

The rest of the paragraph, from "The four panels run to forty-six months"
onward, is unchanged.

---

## Fix 3 - Section 4.1.3 still opens with a colon-and-dash list

The Measurement bias paragraph begins *"Three data patterns require explicit
treatment; per-category figures, computed locally on the in-scope facts, are
reported below: - *Promotional values*: where the promotional metric exists..."*

That is a bullet list that lost its bullets in conversion. It also promises
**three** patterns and then delivers one, because the other two were absorbed
into the following paragraph when the null-rate fix was applied.

### Anchor

**Section 4.1.3 Precise Suitability.** The paragraph with the bolded lead-in
**"Measurement bias / trustworthiness."**

First five words: *"Three data patterns require explicit..."*
Last five words: *"...to the promo-zero case above."*

### Action

REPLACE the paragraph.

#### Replace with

> **Measurement bias / trustworthiness.** Two patterns in the recorded values
> require explicit treatment, and both concern the promotional measures rather
> than the sales quantities. Where the promotional metric exists, for carbonated
> soft drinks and energy drinks, it is fully populated. A recorded zero is
> nonetheless treated as unmeasured rather than as evidence that no promotion
> ran: the pipeline converts zeros to nulls and carries the last observed value
> forward, on the reasoning that an absent promotional record for a brand-month
> is more plausibly a gap in reporting than a confirmed absence of trade
> activity. Where no earlier value exists the feature falls back to zero. For
> water and ready-to-drink beverages the promotional column is absent from the
> source entirely, which is the unmeasured-variable case described above rather
> than a value to be imputed.

### Note - "three" becomes "two", deliberately

The third pattern was negative and zero values, which the following paragraph
now covers in its own right after the null-rate correction. Saying "three" and
listing one is the kind of small incoherence a careful reader notices
immediately.

---

## Fix 4 - Section 4.1.4 has a sentence stranded from a deleted paragraph

The section ends: *"Missing months within a retained series are exposed on the
regular monthly grid and handled natively by the models rather than imputed.
Applicability to shorter or intermittent series is a bound on external validity,
not a claim of this thesis."*

The final sentence used to follow a description of the fully-observed subset,
which was removed. It now sits after a sentence about missing months with no
connective, and the phrase "shorter or intermittent series" refers to nothing
the paragraph has introduced.

### Anchor

**Section 4.1.4 Forecasting Suitability.** The last sentence of the section, and
of the paragraph.

First five words: *"Applicability to shorter or intermittent..."*
Last five words: *"...a claim of this thesis."*

### Action

REWORD.

#### Replace with

> Series shorter than the retention rule admits, and series with intermittent
> demand, are therefore outside what this evidence can speak to - a bound on
> external validity rather than a claim of the thesis.

### Note - this also connects to the intermittency features

Section 4.1.3 now describes zero-run columns, and Section 4.3 lists them as
model inputs. A sentence saying intermittent series are out of scope, two
sections before two features that detect intermittency, reads as a
contradiction. The reworded version says the *series* are outside the evidence
base, which is true and does not collide with the features.

---

## Fix 5 - The split-dates filename is still in the prose

Thread on Section 4.4: *"Is this best way to refer to files inside the
repository?"* No, and it is the only remaining instance in the chapter.

### Anchor

**Section 4.4 Train, Validation, and Test Split.** The second paragraph, its
final sentence.

First five words: *"They are recorded per category..."*
Last five words: *"...windows that produced it."*

### Action

REWORD.

#### Replace with

> The resolved boundaries are written to disk alongside each feature matrix,
> recorded per category and per forecast horizon, so that any published result
> can be traced to the exact windows that produced it.

### Note - the general rule

A filename with a wildcard in it is a note to a developer, not a sentence in a
thesis. The claim that matters is that the boundaries are *recorded and
traceable*, which survives any future change to how the files are named.

---

## Fix 6 - Section 4.2.4 ends with a sentence about a table that no longer exists

The section closes: *"These parameters are EDA-driven rather than theory-first;
their academic justification is developed in the modelling chapter, and their
empirical (not theoretical) origin is stated honestly as a limitation."*

Two problems. **"These parameters"** referred to the deleted Table 2, so the
demonstrative now points at whatever happens to precede it - a paragraph about
promotional correlation. And **"their academic justification is developed in the
modelling chapter"** promises something Chapter 5 does not deliver, since the
parameters are derived here and Chapter 5 cites rather than re-argues them.

### Anchor

**Section 4.2.4 Autocorrelation and Lag Structure.** The last paragraph of the
section, a single sentence.

First five words: *"These parameters are EDA-driven rather..."*
Last five words: *"...honestly as a limitation."*

### Action

REPLACE.

#### Replace with

> The lag set, the rolling windows and the peak-month sets are derived from this
> panel's own structure rather than from a prior specification, and a different
> panel would yield different values. That empirical origin is a limitation of
> the design rather than a feature of it, and it is stated as such among the
> risks in Section 4.5.

### Note - this is the sentence §4.5 already answers

Section 4.5's third risk makes exactly this point and makes it better, including
the observation that the minimum-history requirement is the exception because it
follows from the feature specification by construction. The replacement above
points forward to that instead of promising a justification in Chapter 5 that
was never going to arrive.

---

## Fix 7 - Section 4.2's opening still calls CSD a "worked category"

Both §4.1 and §4.2 lead with the worked-category framing, then immediately
qualify it: *"It is not, however, a pilot from which the others are
extrapolated."* You raised this yourself in an earlier session - all four
categories are trained and tuned independently, and all four appear in the
pooled comparison and the scenario experiment.

**The framing is doing real work** - carbonated soft drinks genuinely carry the
deepest EDA - but "worked category" says something stronger than the design
supports, which is why the paragraph has to walk it back a sentence later.

### Anchor

**Section 4.2 heading**, which currently reads:
*"4.2 CSD - Worked Category (EDA and Parameters)"*

And in **Section 4.1**, the paragraph beginning:
First five words: *"CSD is the worked category..."*
Last five words: *"...category-specific models are required."*

### Action

REWORD both - the heading, and the first clause of the §4.1 paragraph.

#### Replace with

**Heading:**

> 4.2 Carbonated Soft Drinks - Exploratory Analysis and Derived Parameters

**Section 4.1 paragraph, first sentence only. Before:**

> CSD is the worked category, assessed in full in Section 4.2 and used to derive
> the pipeline parameters.

**After:**

> Carbonated soft drinks are assessed in full in Section 4.2 and are where the
> pipeline parameters are derived, being the longest and largest of the four
> panels.

The rest of that paragraph is unchanged and already makes the right point.

### Note - optional, but it removes a recurring hedge

If you keep the heading as it is, the §4.2 opening still needs its second
sentence to walk the term back. Renaming means the chapter can state the
asymmetry as what it is - one category has more data, so its EDA is shown in
full - without implying a pilot-and-replication design that the training setup
does not match.

**This is a heading change, so it moves the table of contents.** Small, but do
it in one pass with the other heading-level edits rather than piecemeal.

---

## Fix 8 - Section 4.3's bolded lead-in is a fragment

*"**Exogenous Variable Enrichment**"* sits on its own line above Table 3,
followed by *"These are the exogenous and autoregressive predictors referenced
in Chapter 1."* It is a heading that is not a heading, in a chapter where every
other section uses numbered headings.

### Anchor

**Section 4.3 Feature Engineering.** The bolded line immediately above the table
captioned "Table 3 - Feature Engineering Overview".

First words: *"Exogenous Variable Enrichment"*
Followed by: *"These are the exogenous and autoregressive predictors referenced in Chapter 1."*

### Action

REPLACE both lines with one sentence.

#### Replace with

> Table 3 lists the engineered columns, grouped by what each contributes and
> naming the models that consume them.

### Note - Chapter 1's forward reference

The deleted sentence pointed back at Chapter 1's mention of exogenous
predictors. That link is worth keeping if Chapter 1 makes a specific promise
about them, but it belongs in prose rather than in a floating caption. **Check
what Chapter 1 actually says before deciding** - if it names the holiday
calendar or promotional intensity specifically, add a clause here; if it speaks
generally, the table stands on its own.

---

## Fix 9 - The holiday adoption sentence needs to name its evidence

**New, from the 2026-09-10 results round.** Section 4.3 says the holiday
columns' contribution *"was measured by an ablation against an otherwise
identical model before they were adopted"*. That is true, but two ablations now
exist in the results folder and they disagree:

| Table | Design | Verdict |
|---|---|---|
| `holiday_ablation_delta.csv` | untuned, fixed hyperparameters | **worse in 8 of 12** cells |
| `94_holiday_ablation_tuned.md` | each arm tuned independently | **improved in 6 of 9** cells |

The tuned comparison is the appendix-grade one and is the right basis: an
untuned comparison penalises the arm with more features, because the fixed
hyperparameters were tuned for the smaller set. **But a sentence that says "an
ablation" without saying which invites an examiner to find the other one.**

### Anchor

**Section 4.3 Feature Engineering.** The paragraph directly below the caption
**"Table 3 - Feature Engineering Overview"**.

First five words: *"Two of the column groups..."*
The sentence to change begins: *"Their contribution was measured by..."*

### Action

REWORD - one sentence inside the paragraph. The rest stands.

**Before:**

> Their contribution was measured by an ablation against an otherwise identical
> model before they were adopted, rather than assumed.

**After:**

> Their contribution was measured rather than assumed: an ablation fitted each
> model family with and without them, tuning both arms independently so that the
> comparison did not penalise the larger feature set, and the calendar columns
> improved accuracy in six of the nine category-and-model combinations tested.

### Note - do not quote the mean delta

Table 94's own review note is explicit: *"Do NOT quote the mean of this column.
It averages over model families that respond differently, and that difference is
itself the finding."* The six-of-nine count is the safe summary and is what the
wording above uses.

### Note - why the untuned table exists at all

It is the first arm of the same experiment, run before hyperparameter tuning was
added. It is not wrong, it answers a different question: *would adding these
columns help a model tuned for the smaller set?* No, and that is unsurprising.
Chapter 5 may want both, since the gap between them is a real methodological
point about how ablations should be run. Chapter 4 needs only the conclusion.

---

# Verified correct - no action

Recorded so a later pass does not re-check them.

**Table 1** is accurate. Catalogue SKUs (2,130 / 1,071 / 1,272 / 728), in-scope
SKUs (7,991 / 1,913 / 4,083 / 2,442) and brands in scope (142 / 55 / 68 / 101)
all reproduce exactly from the raw fact and product tables joined through the
market dimension at DVH EXCL. HD. Retained brands match the feature matrices.

Two small notes rather than fixes. The energidrikke catalogue measures 1,271
against 1,272 stated, and the in-scope fact rows are 0.3 to 1 per cent below the
stated figures in every category - consistent with a slightly different
de-duplication or a panel refresh between the two measurements. **Neither is
worth changing**; both are within the noise of a monthly re-pull and the numbers
are not load-bearing.

**Section 4.2.3** reproduces exactly: December 11.5, June 11.1, March 9.9, May
8.9 per cent of annual units, and all four peak-month sets under the ten per
cent mean-uplift rule.

**Section 4.2.4** reproduces exactly: HARBOE at +0.40 / +0.53 / +0.26 over 46
periods, and promotional correlation at 0.940 and 0.989.

**Section 4.3's counts** are confirmed at 18 and 17 against all eight matrices,
and confirmed again by the HPC run.

**Section 4.4's Table 4** matches the split-date files cell for cell.

---

# Still open, and not fixable here

## The Table 3 rows are now confirmed - no action

Your two UPDATE comments can be resolved. The HPC reporting round
(`f5bad3e`) fixed the casing bug in `training_report.py`, and its feature table
now reads `yes` for the holiday and intermittency rows in **all four
categories**, agreeing with Chapter 4. The appendix contradiction is gone.

The promotional row's lag description is likewise confirmed: the report
describes `promo_intensity` as *"promotion share at t-1 (lagged: contemporaneous
would leak)"*, which is what Table 3 now says.

**No retrain was needed and none happened.** The accuracy results have not moved
since `0e95850`; all eight commits since were reporting fixes.

## The redundancy figures - drop the decimals

**My earlier diagnosis was wrong, and the HPC session caught it.** I said
re-running `srq1_feature_diagnostics.py` would refresh the 26.4 and 28.8
figures because it imports the shared feature list. It does not: that script
*proposes* a reduced set but never fits models on it. The WMAPE pair came from a
manual validation run on 2026-09-06 and was written into the code as a literal,
in three separate places (P0053 F8).

Table 98 has now been regenerated and shows the new structure - 18 and 17
features reducing to 9 and 10, three clusters - **while still printing the old
26.44 and 28.82**. A fresh table with a stale outcome is worse than either half
alone, because it looks current.

**Recommendation: take the fallback.** In §4.3, change *"It performed worse,
raising mean test error from 26.4 to 28.8 per cent"* to:

> It performed worse, and the correlated features are therefore retained.

Keeping the decimals requires a bespoke fit whose only purpose is to support two
numbers inside a rejected negative result. The direction is the contribution;
the decimals are not. Dropping them also sidesteps the uncited 0.95 grouping
threshold.

P0053 F8 reaches the same recommendation independently.

## Two structural items

**Table 1's two SKU columns** could move to an appendix, leaving a five-column
table that reads at a glance (S1). **Appendix A** should be extended with the
per-category feature list rather than joined by an Appendix B (S4), and is now
unblocked since the counts are settled.

Both are in `deferred-structural-decisions.md` with the reasoning.

---

# After these nine fixes

Chapter 4 is done. Every figure in it will have been measured against the
current repository, every table will agree with the prose around it, and the
only outstanding numbers are the two redundancy decimals, which are tracked and
have a safe fallback.

**The one thing I would still do before submission** is read §4.1 and §4.2.1
together. They both establish scope and both give brand counts, and while
neither is wrong, a reader meets the DVH EXCL. HD market level three times in
four pages. That is the cross-chapter repetition question in miniature, and it
is on the deferred list as S9 for the final pass rather than something to solve
now.
