---
name: ch5-FINAL-prose-pass-followup-01
description: NOTE - Answers Brian's five review comments on the final Chapter 5 pass and the eight Word threads still open after he applied it. Corrects the pooled feature count, which was wrong in the pass and in the generator.
snapshot: 2026-09-11_15-41_ch5-applied-review
category: workflow
applies-to: [chapter 5]
created: 2026_09_11-16_00
updated: 2026_09_11-16_00
status: ready
---

# Follow-up 01 - your five comments, and the eight threads left

**The main pass is frozen.** Everything below is new. Where it contradicts the
pass, this file wins.

Re-snapped `2026-09-11_15-41_ch5-applied-review`. Repository at `01f162a`, remote
level. Zotero re-pulled: **87 items**, unchanged.

## What you applied

**Almost all of it.** Chapter 5 went from 4,855 to **7,164 words**, and its
comment threads from **46 to 8**. The whole document is now 40,197 words.

| Section | State |
|---|---|
| 5.0 to 5.4 | applied |
| 5.5.1 to 5.5.7 | applied, including the new tables |
| **5.5.8 holiday enrichment** | **applied** - the new subsection is in |
| 5.5.9, 5.5.10, 5.6, 5.7 | applied |
| Outstanding decisions | deleted |

You also shortened Tables 9 and 10 yourself, which is the answer to your own
point 4 - I have followed your lead below.

---

# Your five comments

## 1. LightGBM and XGBoost are one paragraph each - is there nothing more to say?

**There is more to say, and the sections should be longer.** Threads 211 and 213
say the same thing and add the real problem: **no citation.**

⚠ **Neither source paper is in the Zotero library.** I checked the unfiltered
API: no Ke et al. (2017) for LightGBM, no Chen and Guestrin (2016) for XGBoost.
Under the standing rule, **that means I cannot cite them**, and writing either
from memory is the exact failure the rule exists to prevent.

**Two routes, and they are not equivalent.**

**Route A, the one I recommend: add both papers to Zotero.** They are the
canonical references for the two models the thesis actually deploys, and a
methods chapter that describes a model without citing its source paper is a real
gap an examiner will notice. Both are one search away.

| Model | Reference to add |
|---|---|
| LightGBM | Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems*, 30, 3146-3154 |
| XGBoost | Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD*, 785-794 |

**Route B, if you would rather not add anything:** cite what is already there.
`E2V7QS37` is the Hastie chapter *Additive Models, Trees, and Related Methods*,
which covers the boosting foundation both implementations build on - but **not
either implementation specifically.** It supports the shared mechanism, not the
differences.

### Paste - 5.2.4 LightGBM, expanded

Assumes Route A. If you take Route B, delete the final sentence's citation and
keep the rest.

> LightGBM is the primary machine-learning candidate. It is a gradient-boosting
> implementation in which trees are grown leaf-wise rather than level-wise,
> splitting the leaf with the largest loss reduction rather than completing each
> depth in turn, and in which candidate split points are found on a histogram of
> binned feature values rather than on the raw values (Ke et al., 2017). The
> first choice reaches a given accuracy in fewer trees; the second is what makes
> training time and memory scale with the number of bins rather than with the
> number of rows.
>
> Both properties matter for this problem rather than in the abstract. The panel
> is wide and short - 230 brand series carrying between 41 and 46 monthly
> observations each - so the binding cost is the number of series, not the
> length of any one of them, and a histogram-based learner absorbs that shape
> cheaply. Leaf-wise growth is also the property that makes the model prone to
> overfitting short series, which is the risk the tuning protocol and the
> expanding-window objective are there to control.
>
> Hyperparameters are selected by the Optuna search described in the experimental
> setup below, over one hundred trials against a four-fold expanding-window
> cross-validation objective. Missing lag values are handled natively rather than
> imputed, which matters on a panel where short histories leave the thirteen-month
> lag undefined for a brand's first year.

### Paste - 5.2.5 XGBoost, expanded

> XGBoost is the alternative gradient-boosting implementation, and it is included
> to separate the effect of the algorithm from the effect of one vendor's choices.
> It grows trees level-wise, completing each depth before descending, and
> regularises with both an L1 and an L2 penalty on leaf weights in addition to
> the shrinkage both implementations apply (Chen & Guestrin, 2016). Its split
> finding is exact by default rather than histogram-based.
>
> These are genuine differences in inductive bias rather than packaging. Level-wise
> growth produces more balanced trees and is the more conservative choice on short
> series; the explicit leaf-weight penalties give a second lever on complexity
> beyond tree depth. Whether either difference matters at this data scale is an
> empirical question, and one this chapter answers directly in the stability
> analysis.
>
> It receives an identical feature set, an identical tuning protocol and identical
> test rows, so the comparison between the two isolates the implementation rather
> than confounding it with the data each model saw.

### Note - why the last sentence of the XGBoost block is worth keeping

It is the sentence that makes the LightGBM-versus-XGBoost comparison meaningful,
and it sets up 5.6's conclusion that the two are indistinguishable. **Without a
controlled comparison, "the winner flips with the seed" would be a weaker
finding**, because a reader could attribute the flip to a difference in setup.

---

## 2. You said 5.4.1 is prose - it is not, there are three bullets

**You are right and I was wrong.** The pass called 5.4.1 "already prose, and the
strongest passage in the chapter" and then only replaced its final sentence. It
has three bullets in the middle of the prose, and threads 232 and 233 sit on
exactly that.

### Paste - replace the lead-in and the three bullets with one paragraph

Replace from *"A scoring function determines which functional..."* through the
third bullet ending *"...consistent for the standard median."*

> The choice is theoretical rather than conventional. A scoring function
> determines which functional of the predictive distribution an optimal forecast
> reports (Gneiting, 2011), and the three metrics in play here target three
> different ones. Absolute-error loss is minimised by the median. Pointwise
> absolute percentage error is minimised instead by what Gneiting terms the
> (−1)-median, a density reweighted by the inverse of the outcome, which places
> systematically more weight on small actuals and so biases forecasts downward.
> Weighted MAPE avoids that reweighting by aggregating absolute errors before
> dividing by total volume: over a fixed evaluation sample the divisor is a
> constant, so minimising weighted MAPE is equivalent to minimising mean absolute
> error, and it is therefore consistent for the standard median.

### Note - the page numbers

The bullets carried "(p. 746)" and "(pp. 746, 752)". **Both are correct** and
both are now folded into the single citation at the head of the paragraph. If
you would rather keep the locators, attach them as
*(Gneiting, 2011, pp. 746, 752)*.

### Paste - the leftover sentence, thread 233

⚠ **Thread 233 is right: it no longer fits.** The sentence *"That objective
targets the (−1)-median and underforecasts, which WMAPE penalises directly"*
currently sits at the very end of the section, after the stability forward
reference, where "that objective" has no antecedent - the nearest noun is the
stability analysis.

**Delete it.** The paragraph above now states the same point, in its proper
place, where the (−1)-median is actually introduced.

If you would rather keep an explicit link, the surviving version belongs at the
end of the *preceding* sentence, not after the forward reference:

> ...so the cost is paid without the corresponding gain, even though the
> objective targets the (−1)-median and therefore underforecasts in a way
> weighted error penalises directly. The stability analysis later in this chapter
> explains why.

**Pick one.** Deleting is cleaner; the merged version keeps the mechanism
explicit.

---

## 3. You gave me comment numbers again - the number alone does not help

**Fair, and it was a regression.** The pass wrote "**238** `VERIFY`" with no
indication of what 238 says, which means you have to go and find it before you
can act.

**Fixed for the rest of this chapter and going forward.** Every thread below is
named by **what it says and where it sits**, with the number last as a
cross-check rather than as the identifier:

> **5.4.1, on the three bullets** - *"PROSE & VERIFY"* (thread 232)

Rather than:

> **232 `VERIFY, PROSE`**

I have also recorded this as a standing preference so it survives a compact, not
just this chapter.

---

## 4. Table names are too long and wrap in the table of tables

**Agreed, and you already fixed two of them.** Your Table 9 and Table 10 are the
model - short noun phrases, no trailing clause.

The rule I should have followed: **a caption is a label, not a sentence.** Say
what the table holds; the section already says why.

### Paste - the shortened captions

| # | Current | Replace with |
|---|---|---|
| 7 | The Syntetots-Boylan-Croston demand-pattern classification | **Demand-Pattern Classification Thresholds** |
| 8 | Brands per demand-pattern class, by category | **Brands per Demand Class** |
| 11 | Mean and median scaled error of the two naive benchmarks, by category | **Scaled Error of the Naive Benchmarks** |
| 12 | Weighted MAPE under pooled and per-category training, by category and model | **Pooled versus Per-Category Training** |
| 13 | Empirical coverage and mean relative interval width of the split-conformal intervals, against nominal levels of 80 and 90 per cent | **Prediction-Interval Coverage and Width** |
| 14 | Forecast and accuracy variation across five random seeds, by category and model | **Seed Sensitivity of Forecasts and Accuracy** |
| 15 | The selected model per category under each of five random seeds | **Selected Model per Seed** |
| 16 | How the model benchmark contributes to each sub-research question | **Contribution to the Sub-Research Questions** |

⚠ **Table 7 also has a typo**: *"Syntetots"* should be **"Syntetos"**. The
shortened caption above drops the author names entirely, which removes the
problem and reads better - the names are already in the citation two lines above.

⚠ **Table 13 is the one thread 260 tags `SHORTEN`**, and it is the worst
offender at 132 characters. The replacement is 38.

### Note - what the captions lost, and where it went

The detail dropped from Table 13 - "against nominal levels of 80 and 90 per
cent" - is already visible in the table's own Nominal column, so nothing is lost
to the reader. That is the test for a caption: **if the table's own headers say
it, the caption should not.**

---

## 5. Was the pooled comparison really run before the enrichment?

**No. You were right and the pass was wrong.** This is the most important item in
this note, and it is a correction to the chapter you have already pasted.

### What I found

**The pooled comparison ran on 17 features, including holiday and
intermittency.** Not 12. The sentence I gave you says the opposite.

The evidence, in order:

| Check | Result |
|---|---|
| the feature-centralisation commit `3f8b0a9` | 2026-09-09 at **17:12** |
| the 18-feature HPC retrain `0e95850`, *"run on UCloud HPC (18-feature codebase)"* | 2026-09-09 at **21:02** |
| `pooled_metrics.csv`, `pooled_summary.md`, `pooled_params.json` all written | 2026-09-09 at **21:10** |
| that commit's diff to `pooled_summary.md` | **every WMAPE number changed** |
| resolving the intersection against today's matrices | **17 features** |

**So the run is four hours after the feature change, its numbers moved in that
commit, and the intersection is 17.** Your memory was accurate.

### Why the artefact said 12 - and this is the interesting part

`srq1_pooled.py` computes its feature set at run time, correctly. But the summary
header was a **hardcoded string**:

```python
f"Trials per model: {trials}. Both arms use the SAME 12-feature",
"intersection (`promo_intensity` dropped - absent in danskvand and",
```

The retrain regenerated every number in the file and left the header saying 12,
because nothing computed it. **The file paired fresh results with a stale
description**, which is precisely the failure the generated-artefact provenance
rule names - and I read the description rather than the data.

**Both are now fixed:**

- `srq1_pooled.py` computes the count and the dropped-column list from the
  resolved intersection, with a comment recording why.
- `pooled_summary.md`'s header now reads **17-feature**. Only the header changed;
  the tables were already correct.

### Paste - replace the sentence you pasted into 5.5.4

Find *"This comparison predates the holiday and intermittency enrichment
described above and has not been re-run against it; the pooling question it
answers is about training rows rather than about features."*

**Replace with:**

> Both arms use the seventeen-feature intersection available in every category,
> which is the full feature set less promotional intensity - the one measure
> Nielsen does not report for danskvand or RTD. The comparison therefore runs on
> the same enriched features as the rest of this chapter, and the two arms differ
> only in which rows they were trained on.

### Note - what this changes in the chapter

**It removes a limitation rather than adding one.** Section 5.5.9 currently lists
the pooled comparison as the one result measured on a different feature space.
**That bullet is now false and must come out.**

### Paste - 5.5.9, delete the fifth limitation

Delete the paragraph beginning *"The pooled-versus-per-category comparison was
measured before the holiday and intermittency features were added..."* and change
the opening from **"Five limitations"** to **"Four limitations"**.

### Note - the honest framing of the 17 versus 18

The pooled arms use 17 features where CSD and energidrikke elsewhere use 18. That
is not a staleness problem, it is the definition of a cross-category
intersection: a pooled model trained across all four categories cannot use a
column that two of them do not have. **The sentence above states that as the
design it is**, which is stronger than the limitation it replaces.

⚠ **Do not describe this as "12 features" anywhere.** If you have already pasted
the old sentence, this is the one correction in this note that changes a factual
claim rather than wording.

---

# The eight threads still open

Five are answered by the blocks above. Three are new.

| Where | What it says | Answered by |
|---|---|---|
| 5.2.4 LightGBM | *"PROSE, CITATION: Very short and no citation"* (211) | your point 1 above |
| 5.2.5 XGBoost | *"PROSE, CITATION: Very short and no citation"* (213) | your point 1 above |
| 5.4.1, on the three bullets | *"PROSE & VERIFY"* (232) | your point 2 above |
| 5.4.1, on the trailing sentence | *"Leftover Sentence from first prose pass, unsure if still fits"* (233) | your point 2 above |
| 5.4.4, on the p and CV-squared definitions | *"PROSE"* (239) | **below** |
| 5.5.4, on the feature-count sentence | *"Is this truly the case?"* (255) | your point 5 above |
| 5.5.7, on the Table 13 caption | *"SHORTEN"* (260) | your point 4 above |
| 5.5.7, on the quantile formula | *"MATH"* (261) | **below** |

## 5.4.4, the two definitions set as bullets - thread 239

Same issue as 5.4.1: two bolded fragments interrupting prose.

### Paste - replace both bullets with one sentence

Replace the two lines defining **p** and **CV²** with:

> The scheme classifies each brand on two measured quantities: the average
> inter-demand interval, written p, which counts periods per non-zero demand and
> so measures how often a brand sells at all; and the squared coefficient of
> variation of its non-zero demand sizes, which measures how variable those sales
> are when they occur. The first separates regular from intermittent demand, the
> second steady from erratic, and the two cut-offs below divide the plane into
> four classes.

### Note - this also fixes the table that follows

The 2x2 grid reads as a matrix with no explanation of its axes unless the two
quantities have been introduced as a *pair*. The sentence above does that, which
the two separate bullets did not.

## 5.5.7, the quantile formula - thread 261

⚠ **The sentence is garbled, and the mathematics is right.** It currently reads:

> "The half-width is the ⌈(n+1)(1−α)⌉/n empirical quantile of the calibration
> residuals algorithm of Lei et al. (2018) - not the nominal (1−α) quantile."

*"the calibration residuals algorithm of Lei et al."* has the words in the wrong
order - the algorithm is not an algorithm of the residuals. **Verified against
`srq1_calibration.py`**, which carries the same formula and cites Lei et al.
Algorithm 2 in its own comments, so the formula itself is correct and should
stay.

### Paste

> Following Algorithm 2 of Lei et al. (2018), the half-width is not the nominal
> (1−α) quantile of the calibration residuals but the ⌈(n+1)(1−α)⌉/n empirical
> quantile of them. The correction is small, and it is what buys the
> distribution-free coverage guarantee at finite sample sizes rather than only
> asymptotically.

### Note - why the correction is worth a sentence

It is the difference between a guarantee that holds at 174 calibration rows and
one that holds in the limit. **Since danskvand's failure is explained by having
only 174 rows**, the finite-sample property is load-bearing for the paragraph two
below it, not a technicality.

---

# What I changed in the repository

Two edits, both Correctness-tier, both committed:

| File | Change |
|---|---|
| `srq1_pooled.py` | the summary header now computes its feature count and dropped-column list instead of hardcoding "12" |
| `pooled_summary.md` | header corrected 12 to **17**. Tables untouched - they were already right |

**No model was re-trained and no result number moved.** The tables were correct;
only their description was wrong.

---

# Still open

| Item | State |
|---|---|
| **Add Ke et al. and Chen & Guestrin to Zotero** | needs you - see point 1. The expanded 5.2.4 and 5.2.5 assume they are there |
| **Comment 225, the validation scheme tagged OUTDATED** | ⚠ **it is gone from the chapter.** You either resolved it or applied the addition. Nothing further needed unless you still think something is outdated |

**Nothing else in Chapter 5 is blocked.**
