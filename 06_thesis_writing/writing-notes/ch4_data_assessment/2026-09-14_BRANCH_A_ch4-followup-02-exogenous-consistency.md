---
name: 2026-09-14_BRANCH_A_ch4-followup-02-exogenous-consistency
description: FOLLOW-UP - Section 4.1.3 calls the weighted-distribution proxy an exogenous predictor while 4.3 records it as tested and not adopted. One clause reconciles them. Also retires the duplicate footnote in the AI Use Declaration.
category: workflow
applies-to: [ch4_data_assessment, ai-use-declaration]
triggers: [ch4 prose pass, exogenous variables, weighted distribution]
created: 2026_09_14-17_30
updated: 2026_09_14-17_30
snapshot: 2026-09-14_16-21_post-comment-pass-archive
status: prose ready to paste, awaiting human review
---

# Chapter 4 — follow-up 02, the exogenous-predictor inconsistency

Verified at `41ecb76`, fetch clean. Snapshot
`2026-09-14_16-21_post-comment-pass-archive`.

**You were right, and my earlier instruction was wrong.** I said the exogenous
footnote "belongs in Chapter 4" without giving an anchor, and you checked §4.3
and found the content already there. It is — and it is **correct** where it sits.

**The real defect is narrower: Chapter 4 contradicts itself about one feature.**

---

# The inconsistency

| Section | Says |
|---|---|
| **§4.1.3** *Measurement validity* | *"the weighted-distribution proxy and a promotional-intensity measure ... **serve as exogenous predictors**, alongside a Danish public-holiday calendar"* |
| **§4.3** feature table | `weighted_distribution` → **"Tested, not adopted"** |
| **§4.3** prose | *"fitting the benchmark with and without it **raised the error in three of the four categories**, and it is excluded on that measurement"* |

**Both statements are defensible in isolation.** Weighted distribution *is* an
exogenous variable by definition — it is external to the target series. It simply
**did not make the final feature set**.

⚠ **But a reader meeting §4.1.3 and then §4.3 sees a contradiction**, and §4.1.3
is the earlier of the two, so they meet the wrong version first. The fix is one
clause.

---

# The fix

## F1 — 4.1.3, name the exclusion where the predictor is introduced

### Anchor

**Section 4.1.3 Measurement validity / appropriateness**, the second sentence of
the paragraph beginning *"**Measurement validity / appropriateness.** The
recorded metrics must measure the forecasting target."*

Searchable, verbatim:

> "Sales units (and, where appropriate, litres) are the demand quantities to be
> forecast; the weighted-distribution proxy and a promotional-intensity measure
> derived from the promotional variants serve as exogenous predictors, alongside
> a Danish public-holiday calendar joined onto the monthly grid."

The sentence immediately after it begins *"The weighted-distribution metric is an
availability *proxy* rather than a direct census..."*

### Action

REWORD — that one sentence. Everything before and after it stands.

**Before:**
> "Sales units (and, where appropriate, litres) are the demand quantities to be
> forecast; the weighted-distribution proxy and a promotional-intensity measure
> derived from the promotional variants serve as exogenous predictors, alongside
> a Danish public-holiday calendar joined onto the monthly grid."

**After:**
> "Sales units (and, where appropriate, litres) are the demand quantities to be
> forecast; a promotional-intensity measure derived from the promotional variants
> and a Danish public-holiday calendar joined onto the monthly grid serve as
> exogenous predictors. The weighted-distribution proxy was assessed as a third
> candidate and was not adopted, for the reason given in Section 4.3."

### Note — why this ordering, and what it preserves

**The holiday calendar is promoted to the main clause**, which it deserves: it is
the thesis's clearest exogenous contribution, it was ablation-tested, and it
improved accuracy in six of nine category-and-model combinations.

⚠ **The following sentence still stands and should not be deleted.** It says the
weighted-distribution metric is an availability *proxy* rather than a census, and
that its proxy status is acknowledged in interpretation. **That remains true and
relevant** — the measure is still described in the data assessment even though it
is not a model input, which is the correct treatment for a column the panel
carries.

**The forward reference to §4.3 is what closes the loop.** A reader who wants the
reason gets sent to the measurement rather than being left with a bare
assertion.

---

# What this retires elsewhere

## The AI Use Declaration footnote — delete, do not relocate

The declaration's *"Outstanding Notes"* carries a footnote defining exogenous
variables and listing which the thesis uses. **It is a stale duplicate of the
Chapter 4 content and it is wrong in two ways:**

1. It lists **distribution coverage (the Nielsen weighted-distribution metric)**
   as a predictor in use. It was excluded.
2. It **omits the holiday calendar** entirely — the one exogenous feature that
   was added, tested and kept.

✅ **Chapter 4 §4.1.3 (as reworded above) and §4.3 together carry everything that
footnote was trying to say, accurately.**

→ **Delete the footnote with the rest of the AI Use Declaration section**, per
that note's Fix 1. **Do not move it into Chapter 4** — the content is already
there. This closes thread 315.

---

# Verification

| Claim | Checked against |
|---|---|
| weighted distribution excluded | Ch4 §4.3 table row and prose; error rose in 3 of 4 categories |
| holiday calendar adopted | Ch4 §4.3; 18 model inputs for CSD/energidrikke, 17 for the other two |
| holiday ablation result | Ch4 §4.3, six of nine combinations improved |
| the §4.1.3 sentence as quoted | snapshot `2026-09-14_16-21`, line 46 of `ch4-data-assessment.md` |

**No new citation.** The reword adds no claim requiring a source.
