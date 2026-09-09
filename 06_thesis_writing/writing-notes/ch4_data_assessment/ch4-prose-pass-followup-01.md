---
name: ch4-prose-pass-followup-01
description: NOTE - Follow-up to ch4-prose-pass.md, regenerated against snapshot 19-35 after Brian applied most of the pass. Seven items left. Carries the feature-count correction from 13 to 18 after commit 3f8b0a9.
snapshot: 2026-09-09_19-35_ch4-followup
category: workflow
applies-to: [chapter 4]
supersedes: [ch4-prose-pass.md Fix 3, ch4-prose-pass.md Fix 4, ch4-prose-pass.md Citations]
created: 2026_09_09-19_20
updated: 2026_09_09-20_45
status: ready
---

# Chapter 4 prose pass - follow-up 01

Regenerated against snapshot `2026-09-09_19-35_ch4-followup`, taken after you
applied the pass. **Everything you have already inserted is dropped from this
file.** Only what is still outstanding appears below.

## What you applied

Diffed against the previous snapshot. Nine of the main pass's fixes are in:

| Main pass | Section | State |
|---|---|---|
| Fix 1, retention rule | 4.1.2 | applied |
| Fix 2, duplicated paragraph | 4.1.2 | applied |
| Fix 3 part A, matrix widths | 4.3 | applied - **but see F1, it now says 18 and 13 in the same section** |
| Fix 5, null rates | 4.1.3 | applied |
| Fix 6, retired filter + ARIMA reword | 4.1.4 | applied, both halves |
| Fix 7, scope and filtering | 4.2.1 | applied |
| Fix 8, seasonality changelog | 4.2.3 | applied |
| Fix 9, risks section | 4.5 | applied |
| F2b, the holiday/weighted-dist paragraph | 4.3 | applied |
| promo_intensity lag clause | 4.3, Table 4 | applied |

You also resolved seven comment threads. Chapter 4 is down from 27 to 20, and
two new ones appeared, both handled below.

## What is left

Seven items. **F1 is the only urgent one** - the chapter currently contradicts
itself about its own feature count.

| # | Item | Why it is still open |
|---|---|---|
| [F1](#f1) | 4.3 says both 18 and 13 | Fix 3 part B was not applied; part A was |
| [F2](#f2) | Table 4 header and rows | waiting on the HPC run, per your comment |
| [F3](#f3) | Citations, five paste-ready blocks | you asked for prose, not a table |
| [F4](#f4) | The stale "§4.6" reference | traced to its real target |
| [F5](#f5) | The confidentiality claim | needs your decision, not measurement |
| [F6](#f6) | Two forward references to Chapter 6 | at least one means Chapter 5 |
| [F7](#f7) | Table 2 still carries superseded figures | structural, in the deferred list |

---

# F1 - Section 4.3 now contradicts itself {#f1}

**This is the one to fix first.** Fix 3 part A landed and part B did not, so the
section states two different feature counts three paragraphs apart:

> "Of these, **eighteen** are model inputs for carbonated soft drinks..."
>
> "The **thirteen** inputs are six lagged realisations..."

Eighteen is correct. The count changed on remote main today in commit
**`3f8b0a9`**, *"define FEATURES once; holiday + intermittency columns now reach
the model"*, which promoted the three holiday columns and two intermittency
columns into the standard set. Verified against all eight matrices: **18 for
carbonated soft drinks and energy drinks, 17 for water and ready-to-drink**.

The paragraph you applied from F2b also needs one clause changed, for the same
reason - it says the holiday columns "sit outside the standard input set", which
was true this morning and is not true now.

## F1a - The thirteen-inputs paragraph

### Anchor

**Section 4.3 Feature Engineering.** The last full paragraph of the section,
directly above the one beginning "ARIMA and Prophet are fitted".

First five words: *"The thirteen inputs are six..."*
Last five words: *"...when it is fitted."*

### Action

REPLACE the paragraph.

#### Replace with

> The eighteen inputs fall into six groups. Six are lagged realisations of the
> target at one, two, three, four, eight and thirteen months, and three are
> rolling summaries of it, being the four-month mean and standard deviation and
> the trailing annual mean. Three are calendar position: the month, the quarter
> and the peak-month indicator. One is promotional intensity, where Nielsen
> reports it. Three come from the Danish public-holiday calendar, and the
> remaining two describe intermittency, flagging whether a month falls inside a
> run of zero-sales months and how long that run has lasted. The log-transformed
> target is what the models predict and exponentiate back, and is not itself an
> input, since using it as a predictor would be trivial leakage. The
> weighted-distribution measure is likewise not an input: it was tested and
> excluded, for the reason given above. Lagged and rolling features are
> undefined for a brand's earliest months and are left as missing rather than
> imputed, so the tree models handle the gaps natively while the linear model
> receives a zero-fill when it is fitted.

### Note - one word changed beyond the count

The old text ended *"for the reason given below"*. The weighted-distribution
reason now sits **above** this paragraph, in the block you applied from F2b, so
it reads "above".

## F1b - The paragraph you already applied needs one clause

### Anchor

**Section 4.3 Feature Engineering.** The paragraph directly below the caption
**"Table 4 - Feature Engineering Overview"**.

First five words: *"Two groups of columns are..."*
Last five words: *"...rather than on principle."*

### Action

REWORD - the opening and the third sentence. Everything else stands.

**Before:**

> Two groups of columns are constructed by the pipeline but sit outside the
> standard input set, for different reasons. The Danish public-holiday calendar
> is joined onto the monthly grid from the Nager.Date service, giving the number
> of days in each month, the number of public holidays falling within it, and
> the difference between the two. These enter as a separate arm of the
> benchmark, so that the contribution of calendar enrichment is measured against
> an otherwise identical model rather than assumed.

**After:**

> Two of the column groups in the table warrant further comment. The Danish
> public-holiday calendar is joined onto the monthly grid from the Nager.Date
> service, giving the number of days in each month, the number of public
> holidays falling within it, and the difference between the two. Their
> contribution was measured by an ablation against an otherwise identical model
> before they were adopted, rather than assumed.

The rest of the paragraph - the linear dependence, the regularisation, and the
whole weighted-distribution passage - is unchanged and correct.

### Note - the intermittency columns are still unexplained

They are new to the input set and the chapter has never mentioned them. A reader
meeting `zero_run_flag` in an appendix table with no prior explanation will
stop. They come from P0038 and are shifted, so they carry no leakage.

Optional. In **Section 4.1.3**, after the sentence about negative values:

> A brand's sales series may contain runs of consecutive months with no recorded
> sales, which is a different condition from a single missing observation. Two
> derived columns record this regime, flagging whether a month falls inside such
> a run and how many months the run has lasted, so that a model can distinguish
> a brand two months into a stock-out from one selling steadily.

---

# F2 - Table 4, held for the HPC run {#f2}

Your comment on the holiday row says *"UPDATE: Waiting for HPC Training Run to
finish"*, and the one on the promotional row says *"Added after Prose Pass. Must
be verified after HPC Training Run"*.

**Both are the right call, and the code already answers the first one.** The
holiday columns are in `FEATURES` as of commit `3f8b0a9`, so the row's model
list is correct today. What the HPC run confirms is that a model was actually
*trained* with them, which is a different claim and worth waiting for.

**Two edits are safe to make now**, because neither depends on the run.

## F2a - The weighted-distribution row is wrong today

### Anchor

**Section 4.3 Feature Engineering.** The table captioned **"Table 4 - Feature
Engineering Overview"**, its **last row**, the one beginning
*"weighted_distribution"*.

### Action

EDIT - the third cell of that row only.

#### Replace with

That cell currently reads "LightGBM, XGBoost, Ridge". It becomes:

> Tested, not adopted

`weighted_dist` is not in `FEATURES` and never has been. The row is otherwise
fine - the column exists in the matrix and is described correctly - but listing
three models against it says they consume it, and they do not. The paragraph
below the table already explains why, so no prose change is needed.

## F2b - The header, once the run lands

### Anchor

**Section 4.3 Feature Engineering.** The header row of Table 4, whose third
cell reads **"Models"**.

### Action

EDIT - **after the HPC run confirms the holiday columns trained.**

#### Replace with

Rename the third column header from **"Models"** to **"Used by"**, and add one
row at the bottom of the table:

| zero_run_flag, zero_run_length | Intermittency regime: whether the month falls inside a run of zero-sales months, and how long that run has lasted | LightGBM, XGBoost, Ridge |

"Used by" is the honest header once one row says "Tested, not adopted" rather
than naming models.

### Note - what the run can still change

If the HPC run shows the holiday columns did not reach the trained model despite
being in `FEATURES`, then F1a's count returns to fifteen (13 plus the two
intermittency columns) and the holiday row goes back to being an ablation arm.
**That is the only outcome that would move the number again**, and it is the
thing worth checking in the run's `[features]` banner, which prints
`n/18 resolved` at start-up.

---

# F3 - Citations, as paste-ready prose {#f3}

> *"why did you not propose prose sections here? I am glad you agree with me but
> I also need something to insert"*

Fair - a table of gaps is not something you can paste. Five blocks below.

You were also right about the substance. Saunders licenses *assessing* secondary
data and supplies the chapter's vocabulary for doing it. It says nothing about
log transforms, lag selection, differencing, or how to read a skewness
statistic. **Every source used below is already in `citations.json`** - none
needs finding, and none is written from memory.

## F3a - The scanner panel needs a scanner-data source

### Anchor

**Section 4.1 Overview and Data Strategy.** The chapter's opening paragraph.
Insert after the sentence naming the four categories, before the sentence about
the beer exclusion.

First five words: *"The Nielsen/Prometheus beverage scanner panel..."*
Last five words: *"...ready-to-drink beverages (RTD)."*

### Action

INSERT AFTER.

#### Replace with

> Retail scanner panels of this kind have become a standard empirical basis for
> demand research, and their characteristic strengths and limitations are well
> documented: they capture transactions at the point of sale rather than
> responses to a survey instrument, which removes recall error but bounds
> coverage by which retailers report and by how the provider defines its market
> aggregates (Ng, 2017).

### Note - why this one first

It is the missing counterpart to Saunders. Saunders licenses the assessment; Ng
describes the instrument being assessed, which is what Section 4.1 is actually
claiming. One citation closes the gap you named, and it pre-empts the "is a
scanner panel representative?" question rather than leaving it to the viva.

## F3b - The log transform and the skewness reading

Section 4.2.2 reports raw skewness of 4.1 to 5.1 and treats that as decisive
without saying why those values are severe. It is the place where the chapter
most visibly asserts a statistical judgement on its own authority.

### Anchor

**Section 4.2.2 Stationarity.** The first paragraph of the section.

First five words: *"A logarithmic transformation is applied..."*
Last five words: *"...inconsistent within the panel."*

### Action

REPLACE the paragraph.

#### Replace with

> A logarithmic transformation is applied uniformly to the target and to the
> volume-valued inputs rather than selected per brand. Logarithmic
> transformation is the standard response to multiplicative variance in
> forecasting practice, stabilising the variance so that a proportional change
> has the same effect at every level of the series (Hyndman & Athanasopoulos,
> 2021). The distributional evidence is unambiguous: the twelve volume-valued
> columns carry raw skewness between 4.1 and 5.1, and none exceeds 0.25 in
> absolute value once transformed. Values of this magnitude are well beyond the
> range at which a distribution is conventionally treated as approximately
> normal, and are severe enough that the choice of transformation is not a
> matter of judgement (Doane & Seward, 2011; Cain, Zhang & Yuan, 2017). Uniform
> treatment is preferred to per-series selection because the tests that would
> drive such a selection have limited power at forty-six observations, and
> because a transformation applied unevenly across brands would make the feature
> semantics inconsistent within the panel.

### Note - three sources exist, use two

Doane & Seward and Cain, Zhang & Yuan are enough. Kim (2013) is also in the
library and says the same thing for a clinical audience; adding it is padding.

⚠ **Check the Hyndman year in Zotero before pasting.** The entry I inspected
carries no year, and the chapter cites the third edition elsewhere. Match
whatever form the rest of the thesis uses, so the reference list ends with one
entry rather than two.

## F3c - Differencing as the response to a unit root

### Anchor

**Section 4.2.2 Stationarity.** The second and final paragraph of the section.

First five words: *"On the aggregate monthly series..."*
Last five words: *"...rather than imputed."*

### Action

REWORD - one sentence inside the paragraph.

**Before:**

> Non-stationarity in the mean is handled by differencing for the statistical
> baselines and by lagged and rolling features for the tree models, which do not
> require a stationary level.

**After:**

> Non-stationarity in the mean is handled by differencing for the statistical
> baselines, which is the conventional treatment for a series carrying a unit
> root (Hyndman & Athanasopoulos, 2021), and by lagged and rolling features for
> the tree models, which do not require a stationary level.

## F3d - The admissibility rule and the retained collinearity

Section 4.3 makes two methodological arguments on its own authority: that
contemporaneous predictors are inadmissible, and that correlated features should
be kept for tree models. Both are defensible and both are citable.

### Anchor

**Section 4.3 Feature Engineering.** The second paragraph of the section.

First five words: *"Within that admissible set, two..."*
Last five words: *"...evidence for the decision"* - note it ends without a full
stop in the current document.

### Action

REPLACE the paragraph.

#### Replace with

> Within that admissible set, two further questions were put to the data. The
> first is collinearity: the lag and rolling features are correlated by
> construction, since each is computed from the same series, and variance
> inflation factors confirm this directly. The second is whether the redundancy
> warrants reduction. Grouping features by correlation and retaining the most
> important member of each group yields a smaller set, and that reduced set was
> evaluated against the benchmark rather than adopted on principle, following
> the standard caution that a selection rule is justified only by the
> performance of the model it produces (Guyon & Elisseeff, 2003). It performed
> worse, raising mean test error from 26.4 to 28.8 per cent. The correlated
> features are therefore retained: collinearity is a pathology of linear
> estimation, where it inflates coefficient variance and makes individual
> coefficients uninterpretable (Hastie, Tibshirani & Friedman, 2009), whereas a
> gradient-boosted tree splits on whichever correlated feature is locally most
> informative and loses genuine information when the others are removed. The
> reduction is reported here because the negative result is the evidence for the
> decision.

### Note - two changes beyond the citations

**The count is deliberately vague now.** The current text says the reduction
"yields a set of nine". That was measured against a 16-feature set; the input
set is 18, so the reduction would produce a different number. "A smaller set" is
true at any feature count and needs no re-measuring before you can paste. **If
you want the number back, the reduction must be re-run after the HPC run.**

**The paragraph now ends with a full stop.** The current one does not.

## F3e - The leakage argument, optional

Section 4.3's opening paragraph argues the admissibility rule from first
principles, which is sound on its own - hence optional. But it is also a
well-established result about evaluating autoregressive models.

### Anchor

**Section 4.3 Feature Engineering.** The first paragraph of the section.

First five words: *"Feature selection is governed by..."*
Last five words: *"...determines the input set."*

### Action

REWORD - the final sentence only.

**Before:**

> This rule, rather than a judgement about which measures are interesting,
> determines the input set.

**After:**

> This rule, rather than a judgement about which measures are interesting,
> determines the input set, and observing it is what allows the evaluation in
> Chapter 5 to be read as an estimate of forecasting performance rather than of
> in-sample fit (Bergmeir, Hyndman & Koo, 2018).

### Note - the reference list gains five or six entries

Ng (2017); Doane & Seward (2011); Cain, Zhang & Yuan (2017); Guyon & Elisseeff
(2003); Hastie, Tibshirani & Friedman (2009); and Bergmeir, Hyndman & Koo (2018)
if you take F3e. Hyndman & Athanasopoulos is presumably already present from
Chapter 5.

All are in Zotero, so re-exporting the bibliography picks them up. **None was
written from memory** - each was checked against `citations.json` first.

### Note - two thresholds that should stay uncited

The **ten per cent peak-month uplift** (`step_3_derive_params.py:149`) and the
**0.95 redundancy grouping threshold** are project choices, not borrowed
conventions. Describe them as choices this study made, which the chapter already
does for the parameters generally. **Do not attach a citation to either.**

---

# F4 - The stale cross-reference, traced {#f4}

> *"where I would like you to try to find the passage that is perhaps the proper
> internal reference"*

**Found it.** Section 4.2.6 says *"closing the gap previously flagged in §4.6"*.
There is no §4.6. The reference is to an earlier draft's **risks section**,
which is **Section 4.5 today**.

**But do not repoint it.** You have already applied Fix 9, which replaced the
§4.5 body - so the entry it pointed at no longer exists. Repointing would send a
reader to a section that no longer discusses it.

### Anchor

**Section 4.2.6 Per-category EDA - danskvand, energidrikke, RTD.** The opening
sentence, the only sentence before the table.

First five words: *"The three proof-of-concept categories were..."*
Last five words: *"...previously flagged in §4.6."*

### Action

REWORD.

#### Replace with

> The three remaining categories were taken through the identical pipeline, with
> their exploratory analysis recomputed under the DVH EXCL. HD market scope.

### Note - the other two stale references are already gone

Fix 9 removed the "(§4.3.6)" reference along with the §4.5 body. The
"forward-chaining (Section 4.5)" reference is inside Table 2, which is covered
by F7 below.

---

# F5 - The confidentiality claim {#f5}

**Still open, and still the only item in the chapter with consequences outside
the document.** Section 4.1.1 states the data "is used under a confidentiality
agreement with Manifold AI"; your comment says no NDA was signed. An examiner
may reasonably ask to see an agreement the thesis asserts exists.

The sentence can be made true without one, because the substantive claim does
not depend on a signed instrument.

### Anchor

**Section 4.1.1 Source, Type, and Access.** The first paragraph, the sentence
containing the phrase "confidentiality agreement".

First five words: *"It is used under a..."*
Last five words: *"...of using secondary data."*

### Action

REWORD.

#### Replace with

> The data are commercial and are not redistributed: they remain in the local
> research environment and are not published with this thesis. Because access is
> commercial and restricted, the data could not have been collected
> independently within the scope of a thesis, which is itself a Saunders-listed
> advantage of using secondary data.

### Note - confirm before pasting

This states the handling restriction you actually observe and drops the
assertion about a document. **If an agreement does exist, the original sentence
is better** - it is a stronger claim and costs nothing when true.

---

# F6 - Two forward references to Chapter 6 {#f6}

The chapter contradicts itself about where its own result lives.

**Section 4.1** says the categories *"are what allows **Chapter 6** to test
whether one pooled model generalises"*. **Section 4.2**, further down, calls the
same thing *"the pooled-versus-specialised comparison of **Chapter 5**"*.

Chapter 5 is right - the comparison is Section 5.5.4.

The other Chapter 6 reference, in **Section 4.1.1** (*"The exact extraction
interface used by the pipeline is documented in Chapter 6"*), is **probably
correct**, since Chapter 6 is the Predictive-Extension Architecture. Verify
rather than change it.

### Note - deliberately not written as a fix

Recorded as S8 in the deferred list. Forward references should be swept in one
pass once the chapter order is final, because fixing them piecemeal per chapter
is how this inconsistency arose in the first place. Two minutes at the end
beats two minutes per chapter with a risk of drift.

---

# F7 - Table 2 still carries two superseded figures {#f7}

Section 4.2.5's parameter table still says **"MIN_PERIODS 30 (global)"** and
**"Train / Val / Test 24 / 6 / 12 months"**. Both are superseded, and both now
sit above sections that state the correct values in prose - which you have
already applied.

**Recommendation: delete the table.** Fixes 7 and 8, which you applied, state
its contents in prose at the point each value is derived. An appendix copy would
preserve the errors rather than fix them, and its "forward-chaining (Section
4.5)" cross-reference is wrong about both the section and the method.

**One sentence survives** - the closing note that the parameters are empirical
rather than theory-first. Main pass Fix 7 keeps it.

Recorded as S2 in the deferred list, with the reasoning. Flagged here because
the thread on Section 4.2.5 is still open and this is what I would tell you to
do with it.

---

# Still tracked, not acted on

`06_thesis_writing/writing-notes/deferred-structural-decisions.md` carries eleven
structural items, cumulative across chapters. From Chapter 4 the live ones are:

| ID | Item | My view |
|---|---|---|
| S1 | Table 1, per-category structure | keep in body, move the two SKU columns to the appendix |
| S2 | Table 2, EDA parameters | **delete** - see F7 |
| S3 | Table 3, per-category EDA | keep in body, but verify it - the ADF and top-brand columns are unchecked |
| S4 | Appendix A | extend it rather than adding B. Unblocked now that the counts are settled |
| S8 | Forward references | see F6 |

---

# When you mark this chapter complete

Both files archive together:

```
writing-notes/ch4_data_assessment/.archive/
  2026-09-XX_ch4-prose-pass-applied.md
  2026-09-XX_ch4-prose-pass-followup-01-applied.md
```

`deferred-structural-decisions.md` **does not archive** - it stays live until the
structural pass at the end, and Chapter 5 will append to it.
