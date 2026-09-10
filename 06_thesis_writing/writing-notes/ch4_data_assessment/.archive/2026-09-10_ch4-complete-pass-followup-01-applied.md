---
name: ch4-complete-pass-followup-01
description: NOTE - Follow-up to ch4-complete-pass.md, regenerated against snapshot 14-08 after Brian applied Fixes 1-8. Three items left, one of them new from the HPC results round.
snapshot: 2026-09-10_14-08_ch4-fix9-check
category: workflow
applies-to: [chapter 4]
supersedes: [ch4-complete-pass.md]
created: 2026_09_10-16_00
updated: 2026_09_10-16_00
status: ready
---

# Chapter 4 complete pass - follow-up 01

Regenerated against `2026-09-10_14-08_ch4-fix9-check`, taken after you applied
the complete pass.

**I owe you a correction on process.** I added Fix 9 and rewrote two sections of
`ch4-complete-pass.md` in place, after you had already read it, and without
re-snapshotting first. Both are things the project rules now forbid and I wrote
them. This file is the correct form: the pass is archived, and what remains is
here.

## What you applied

Diffed against the 12-55 snapshot. **Eight of nine fixes are in:**

| Fix | Section | State |
|---|---|---|
| 1, Table 2's wrong columns | 4.2.5 | applied - and you renamed the column to "Heaviest month", which was the optional half |
| 2, duplicated Coverage clause | 4.1.2 | applied |
| 3, "three patterns" listing one | 4.1.3 | applied |
| 4, stranded intermittency sentence | 4.1.4 | applied |
| 5, split-dates filename | 4.4 | applied |
| 6, "These parameters" pointing at a deleted table | 4.2.4 | applied |
| 7, the worked-category framing | 4.1, 4.2 heading | applied, both halves |
| 8, the bolded fragment above Table 3 | 4.3 | applied |

## What is left

Three items, and only one is a fix.

| # | Item | Why |
|---|---|---|
| [F1](#f1) | The holiday adoption sentence names no ablation | new - two ablations exist and they disagree |
| [F2](#f2) | The redundancy decimals | **re-measured** - 29.3/32.1, paste the update |
| [F3](#f3) | One figure in Table 2 | 0.937 vs measured 0.940 - your call |

---

# F1 - The holiday sentence needs to say which ablation {#f1}

**New, from the 2026-09-10 results round.** This is the only genuine fix left in
the chapter.

Section 4.3 says the holiday columns' contribution *"was measured by an ablation
against an otherwise identical model before they were adopted"*. True, but the
results folder now holds **two** ablations, and they reach opposite conclusions:

| Artefact | Design | Verdict |
|---|---|---|
| `holiday_ablation_delta.csv` | untuned, fixed hyperparameters | **worse in 8 of 12** cells |
| `94_holiday_ablation_tuned.md` | each arm tuned independently, refit on train+validation | **improved in 6 of 9** cells |

The tuned comparison is the appendix-grade one and is the right basis for the
decision: an untuned comparison penalises the arm with more features, because
the fixed hyperparameters were chosen for the smaller set. That is a real
methodological point, not a convenience.

**But "an ablation" without a qualifier invites a reader to find the other one.**

### Anchor

**Section 4.3 Feature Engineering.** The paragraph directly below the caption
**"Table 3 - Feature Engineering Overview"**, which begins *"Two of the column
groups in the table warrant further comment."*

The sentence to change is the third.
First five words: *"Their contribution was measured by..."*
Last five words: *"...adopted, rather than assumed."*

### Action

REWORD - one sentence. The rest of the paragraph stands.

**Before:**

> Their contribution was measured by an ablation against an otherwise identical
> model before they were adopted, rather than assumed.

**After:**

> Their contribution was measured rather than assumed: an ablation fitted each
> model family with and without them, tuning both arms independently so that the
> comparison did not penalise the larger feature set, and the calendar columns
> improved accuracy in six of the nine category-and-model combinations tested.

### Note - do not quote the mean delta

Table 94's own internal review note is explicit: *"Do NOT quote the mean of this
column. It averages over model families that respond differently, and that
difference is itself the finding."* The six-of-nine count is the safe summary,
and it is what the wording above uses.

### Note - the untuned table is not wrong

It is the same experiment before tuning was added, and it answers a different
question: *would these columns help a model tuned for the smaller set?* No, and
that is unsurprising. **Chapter 5 may want both**, since the gap between them is
a genuine point about how ablations should be run. Chapter 4 needs only the
conclusion.

---

# F2 - The redundancy decimals: now measured, keep them {#f2}

**Resolved by measurement while this note was being written.** Commits `1b0de33`
through `0206402` replaced the hardcoded WMAPE pair with a computed one:
`feature_diagnostics.py` now has an `evaluate_reduction()` step that fits the
full and reduced sets per category and model, writes
`feature_reduction_eval.csv`, and the table 98 caption reads its means.

**The figures on the current 18-feature set are 29.31 and 32.13**, over twelve
category-by-model cells. The chapter's 26.4 and 28.8 came from a 2026-09-06 run
on 16 features.

So the fallback is no longer needed. **Keep the decimals and update them.**

### Anchor

**Section 4.3 Feature Engineering.** The second paragraph, beginning *"Within
that admissible set, two further questions were put to the data."*

The sentence to change.
First five words: *"It performed worse, raising mean..."*
Last five words: *"...to 28.8 per cent."*

### Action

REWORD.

**Before:**

> It performed worse, raising mean test error from 26.4 to 28.8 per cent.

**After:**

> It performed worse, raising mean test error from 29.3 to 32.1 per cent across
> the twelve category-and-model combinations tested.

### Note - the direction held, and the gap widened

The reduction cost 2.4 percentage points on 16 features and costs 2.8 on 18. The
argument in the surrounding prose is unchanged and is now better supported: more
correlated features means more genuine information lost when the groups are
collapsed.

The per-cell figures are worth knowing, because two are extreme. Water's
LightGBM and Ridge both lose roughly eleven percentage points under reduction,
while its XGBoost *gains* three. **Do not quote a per-cell number in Chapter 4** —
the mean over twelve cells is the claim, and the spread belongs in Chapter 5 if
anywhere.

### Note - the 0.95 threshold is no longer uncited either

The same round made the grouping threshold a computed value read from
`feature_proposed_set.csv`'s new `rho` column rather than a literal in the
caption. The chapter still does not name it, which remains the right call: it is
a project parameter with no external source, and the argument does not need it.

⚠ **One number in the chapter is now stale in the opposite direction.** If you
paste the update above, check that no other sentence in §4.3 still says 26.4 or
28.8.

---

# F3 - One figure in Table 2, your call {#f3}

You applied Fix 1 and took the corrected ADF, ACF and heaviest-month values, but
kept the CSD promotional correlation at **r = 0.937** where I proposed 0.94.

Re-measured today on promotion-bearing brand-months:

| Category | In Table 2 | Measured |
|---|---|---|
| CSD | 0.937 | **0.940** (n = 2,972) |
| energidrikke | 0.99 | **0.989** (n = 1,369) |

**Neither is wrong to three decimals**, and 0.937 may be from an earlier panel
pull - the difference is well within a monthly refresh. Two small things:

- The table now mixes precisions, **0.937 against 0.99**. One or the other.
- §4.2.4 states *"r = 0.94 for CSD ... and r = 0.99 for energidrikke"*, so at
  three decimals the table and the prose read as different measurements.

### Anchor

**Section 4.2.5 Per-category EDA.** The table captioned **"Table 2 - Per Category
Correlation & Transformations"**, the **Promo Correl.** column, rows *CSD* and
*energidrikke*.

### Action

EDIT - two cells, to match §4.2.4.

#### Replace with

| Row | Value |
|---|---|
| CSD | r = 0.94 |
| energidrikke | r = 0.99 |

### Note - or go the other way

Three decimals everywhere would also be consistent: 0.940 and 0.989 in the
table, and §4.2.4 changed to match. **Two decimals is the better choice** - the
third digit is not stable across a monthly re-pull, and reporting it implies a
precision the panel does not support.

---

# Verified, no action

Re-measured against the current repository at commit `9cc084e`.

**Table 2 is now correct** in every column I flagged. The ADF values (0.774,
0.999, 0.961, 0.000), the ACF pairs and the heaviest-month values all reproduce.
Renaming the column to "Heaviest month" removes the collision with `PEAK_MONTHS`
and stops it appearing to contradict §4.2.3.

**Table 3's holiday and intermittency rows are confirmed** by the fixed
`training_report.md`, which now reads `yes` for all four categories. Your two
UPDATE comments on those rows can be closed.

**The feature counts, the split table, Table 1, the monthly shares, the
HARBOE autocorrelations and the peak-month sets** were all verified in the
complete pass and none has changed since.

---

# After F1 and F2

Chapter 4 is done. F3 is cosmetic and F2 is a decision rather than a
measurement, so **F1 and F2 are each one reworded sentence**, and both have their
final wording above.

Two things remain tracked elsewhere and neither blocks the chapter:

- **S1 and S4** in `deferred-structural-decisions.md`: whether Table 1's two SKU
  columns move to an appendix, and extending Appendix A with the per-category
  feature list. Both are layout decisions for the end.
- **S9**, the cross-chapter repetition pass, which is where §4.1 and §4.2.1
  both establishing scope gets resolved.

Ready for Chapter 5.
