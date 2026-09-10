---
name: srq1-holiday-ablation-and-the-tuning-inversion
description: NOTE - Ch5 needs a holiday-enrichment ablation subsection it does not currently have. The untuned and tuned arms disagree, and that disagreement is the methodological finding, not a discrepancy to hide. Carries the paste-ready prose and both appendix tables.
snapshot: 2026-09-10_14-08_ch4-fix9-check
category: workflow
applies-to: [chapter 5]
created: 2026_09_10-16_20
updated: 2026_09_10-16_20
status: ready
---

# Holiday enrichment, and the inversion under tuning

**Carried out of the Chapter 4 pass.** Chapter 4 §4.3 states the conclusion — the
calendar columns were adopted because a tuned ablation showed them helping in six
of nine cells — and that is all a data chapter needs. **The interesting half
belongs here**, because it is a finding about how a feature ablation must be run,
not about the data.

**Chapter 5 currently has no holiday-ablation subsection at all.** Two appendix
tables exist (94 and 95), both regenerated on the 18-feature set on 2026-09-10,
and neither is cited anywhere in the chapter.

---

# The finding

Two ablations were run on the same feature comparison. They disagree:

| Arm | Design | Verdict |
|---|---|---|
| Fixed configuration | one hyperparameter set, chosen for the smaller feature set, applied to both arms | holiday features **worse in 8 of 12** cells |
| Independently tuned | each arm tuned on the validation split, refit on train+validation, scored once on test | holiday features **better in 6 of 9** cells |

**The disagreement is not noise, and it is not a reason to suppress one arm.**
Table 95 shows why: tuning improved the *baseline itself* by up to 12.99
percentage points, and where a fixed configuration is badly mis-specified, a
feature comparison measured against it reflects the mis-specification rather than
the features.

Danskvand is the clearest case. Its tree models were mis-specified by roughly 8
to 13 percentage points under the fixed configuration. Adding three columns to a
model that cannot fit the data in the first place tells you nothing about the
columns.

**The generalisable point: the direction of a measured feature effect can invert
under tuning.** That is worth one sentence in a methods chapter, and it is
exactly what table 95's own internal review note asks for.

---

# The fixes

---

## Fix 1 - Add a holiday-enrichment subsection to §5.5

The chapter reports the tabular benchmark, the simple benchmarks, MASE, pooled
versus per-category, demand patterns, the operational profile, interval
calibration and seed stability. **The one experiment it does not report is the
only feature-level ablation in the study.**

### Anchor

**Section 5.5 Results.** Insert as a new subsection **between 5.5.7 Prediction-
interval calibration and 5.5.8 Remaining gaps**.

The preceding subsection ends with the interval-calibration discussion; the
following heading reads *"5.5.8 Remaining gaps"* and its first line begins
*"The ≤15% accuracy target has been withdrawn, not scored."*

Everything after it renumbers: 5.5.8 becomes 5.5.9, and 5.5.9 becomes 5.5.10.

### Action

INSERT — a new subsection, heading plus three paragraphs.

#### Replace with

> ### 5.5.8 Calendar enrichment, and what tuning does to an ablation
>
> The Danish public-holiday calendar is the only feature group in this study
> adopted on the strength of a dedicated ablation rather than on construction.
> Each model family was fitted twice per category, once on the standard feature
> set and once with the three calendar columns added, and the two arms were
> compared on the held-out test split. With hyperparameters tuned independently
> for each arm, the calendar columns improved accuracy in six of the nine
> category-and-model combinations tested, and they were adopted on that basis.
> The per-cell figures are reported in Appendix Table 94.
>
> The same comparison run against a single fixed hyperparameter configuration
> reaches the opposite conclusion, and the reason is instructive rather than
> troubling. Tuning improved the baseline itself by as much as thirteen
> percentage points in the water category, where the fixed configuration had left
> the tree models substantially mis-specified. A feature comparison measured
> against a model that cannot fit the data does not measure the features; it
> measures the mis-specification. Adding three columns to an underfitted model
> changes little, and what change there is has no clear interpretation.
>
> The methodological consequence is worth stating plainly, because it bears on
> how any feature ablation should be read: the direction of a measured feature
> effect can invert once the models on either side are properly specified. An
> ablation is only interpretable against a model that has been given a fair
> chance to fit, which is why both arms are tuned here rather than one. Appendix
> Table 95 reports the two comparisons side by side.

### Note - the numbers, and which are safe to quote

| Claim in the prose | Source |
|---|---|
| "six of the nine" | Table 94's own note; 6 improved, 3 worsened |
| "as much as thirteen percentage points" | Table 95, danskvand XGBoost baseline gain **+12.99pp** |
| "eight of twelve" — **not used above** | the untuned arm has 12 cells (3 model families), the tuned arm 9 |

⚠ **The two arms do not have the same number of cells.** The fixed-configuration
run covers three model families across four categories (12 cells); the tuned run
covers LightGBM and XGBoost for all four plus Ridge for CSD only (9 cells). The
prose above therefore says "the opposite conclusion" rather than pairing two
counts, which would imply a cell-for-cell comparison that does not exist.

⚠ **Do not quote the mean of either delta column.** Table 94's internal review
note: *"It averages over model families that respond differently, and that
difference is itself the finding."*

### Note - RTD XGBoost is the least stable cell in the study

Table 95 flags it: it swings 2.95pp between the untuned and tuned runs, and it
carries the largest single improvement in the tuned arm (-4.92pp). **Do not build
an argument on that cell alone.** The six-of-nine count absorbs it; a sentence
singling it out would not survive a re-run.

---

## Fix 2 - §5.3.2 still says no holiday calendar is used

**This is a factual error, and it contradicts Chapter 4 in the same document.**
It was flagged in an earlier session and is still present.

### Anchor

**Section 5.3.2 Feature engineering.** The calendar bullet.

First five words: *"Calendar: month, quarter, and a..."*
Last five words: *"...not from calendar dates."*

The line contains the bolded assertion **"No holiday calendar is used"**.

### Action

REPLACE.

#### Replace with

> **Calendar**: month, quarter, a binary peak-month flag derived from the
> category's own seasonal profile, and three columns from the Danish
> public-holiday calendar described in Section 4.3. The peak-month flag and the
> holiday columns measure different things and are both retained: the flag is
> derived from the sales distribution, while the holiday count comes from an
> external calendar. Their contribution is measured in Section 5.5.8 rather than
> assumed.

### Note - why this survived

The sentence was true when written. The holiday enrichment landed on 2026-08-18,
Chapter 4 was updated and Chapter 5 was not. It is the clearest instance in the
thesis of the cross-chapter repetition problem producing a factual contradiction
rather than merely redundant prose — worth remembering for the S9 pass.

---

## Fix 3 - The feature count in §5.3.2

Whatever §5.3.2 says about how many features the models consume, it predates the
2026-09-09 change. The count is **18 for CSD and energidrikke, 17 for danskvand
and RTD**, verified against all eight matrices and confirmed by the HPC run's
`training_report.md`.

### Anchor

**Section 5.3.2 Feature engineering.** Any sentence naming a feature count.

### Action

VERIFY-THEN-EDIT. Read the section against the snapshot before writing — if it
gives no count, nothing to do; if it gives one, it is wrong.

### Note - the ch4-ch5 boundary decision still stands

§5.3.2 should shrink to a back-reference plus the experiment-specific facts: the
horizon, which model family consumes which inputs, and the NaN-versus-zero-fill
distinction. Feature *construction* is Chapter 4's, established before the split
and leakage-safe by construction. That decision is recorded in
`.archive/2026-09-08_ch4-ch5-boundary-decision-folded-in.md` in the ch4 folder.

---

# Assets

**Table 94** (`94_holiday_ablation_tuned.md`) — **appendix, cite don't inline.**
Nine rows of per-cell WMAPE. The body needs the six-of-nine count, not the grid.

**Table 95** (`95_holiday_ablation_tuning_sensitivity.md`) — **appendix, cite
don't inline.** Six columns wide, and its value is as evidence for a claim the
prose makes in one sentence.

Both were regenerated on 2026-09-10 against the 18-feature set (`cf5fdbe`) and
carry `INTERNAL REVIEW` separators, so they are submission-ready below the rule.
**Neither is cited anywhere in the chapter today.**

---

# Note - what Chapter 4 says, so the two do not collide

Chapter 4 §4.3 carries only the conclusion:

> "Their contribution was measured rather than assumed: an ablation fitted each
> model family with and without them, tuning both arms independently so that the
> comparison did not penalise the larger feature set, and the calendar columns
> improved accuracy in six of the nine category-and-model combinations tested."

That sentence and §5.5.8 above share one number, the six of nine, and nothing
else. Chapter 4 says *what was decided*; Chapter 5 says *how the measurement was
made and what it revealed about measuring*. One establishes, the other develops —
which is the pattern the repetition pass is meant to enforce.

---

# Note - a second ablation now exists, and it is also Chapter 5 material

The 2026-09-10 provenance round (P0053 F8, F10) turned the redundancy reduction
into a real experiment rather than a cited constant.
`feature_diagnostics.py::evaluate_reduction()` now fits the full and reduced
feature sets per category and model and writes `feature_reduction_eval.csv`,
twelve cells.

**Chapter 4 takes the mean** (29.3 to 32.1 per cent, a 2.8pp cost) because the
data chapter needs only the decision. **The per-cell spread is Chapter 5's**, and
it is more interesting than the mean:

| Cell | Delta under reduction |
|---|---|
| danskvand LightGBM | **+10.95pp** |
| danskvand Ridge | **+10.68pp** |
| danskvand XGBoost | **-3.15pp** |
| CSD XGBoost | -0.87pp |
| everything else | +0.5 to +4.7pp |

**Water's three model families disagree in both direction and magnitude on the
same feature set** — two lose eleven points, one gains three. That is the same
lesson as the holiday inversion, in a different experiment: an aggregate over
model families that respond differently hides the finding.

If §5.5.8 is written as proposed above, a sibling paragraph on the redundancy
reduction would sit naturally beside it, and the two together make the
methodological point once rather than twice. **Not drafted here** — it needs the
Chapter 5 pass to see what §5.3.5 already says about tuning.
