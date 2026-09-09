---
name: post-hpc-validation
description: NOTE - Running list of thesis claims that must be re-verified or updated once the HPC training run finishes. Cumulative across chapters. Each item names the sentence, the file that will answer it, and what the answer changes.
category: workflow
applies-to: [chapter 4, chapter 5, chapter 8, results]
created: 2026_09_09-21_00
updated: 2026_09_09-21_00
status: open
---

# Post-HPC validation list

Claims that are **written but not yet confirmed by a completed training run**.
Each one is either currently true and unverified, or written against the code as
it stands while the numbers behind it are being regenerated.

**This file is cumulative across chapters**, like the deferred-structural list.
Append rather than replace, so the whole set can be worked through in one sitting
when the run lands.

**Why this exists separately from the deferred list:** those items need a
*decision*, these need a *measurement*. Different work, different moment.

---

# Quick reference

| # | Claim | Chapter | What answers it | If wrong |
|---|---|---|---|---|
| [H1](#h1) | 18 model inputs, 17 without promotion | 4 §4.3 | run banner `[features] n/18 resolved` | count reverts to 15 / 14 |
| [H2](#h2) | Holiday columns are standard inputs | 4 §4.3, Table 4 | same banner | row reverts to "Ablation arm" |
| [H3](#h3) | Intermittency columns are inputs | 4 §4.3, §4.1.3 | same banner | delete the new sentence |
| [H4](#h4) | promo_intensity lag description | 4 Table 4 | matrix + feature resolution | reword the cell |
| [H5](#h5) | Reduction from 16 to 9 features | 4 §4.3 | re-run redundancy analysis | number changes |
| [H6](#h6) | WMAPE 26.44 → 28.82 | 4 §4.3 | re-run redundancy analysis | both numbers change |
| [H7](#h7) | All Chapter 5 accuracy figures | 5 §5.5 | the run itself | every reported result |
| [H8](#h8) | Casing bug may have dropped 2 categories | 5, 8 | check run covers 4 categories | results cover half the panel |
| [H9](#h9) | Test-set row counts 665 / 372 / 308 / 174 | 5 §5.3.1 | run output | denominators change |
| [H10](#h10) | XGB_N_JOBS = 1 was set | 5 | run config | 2.65pp WMAPE spread |

---

# Chapter 4

## H1 - The feature count {#h1}

**Claim as written:** *"Of these, eighteen are model inputs for carbonated soft
drinks and energy drinks and seventeen for water and ready-to-drink beverages"*
(§4.3), and *"The eighteen inputs fall into six groups"*.

**Status:** true against the code at commit `3f8b0a9`, verified against all eight
feature matrices on 2026-09-09. **Not yet confirmed by a completed run.**

**What answers it:** every SRQ1 script prints a features banner at start-up:

```
[features] 18/18 resolved
[features] 17/18 resolved; absent: promo_intensity
```

That line is `_features.describe()` and it reports what the model actually
received, which is the claim the chapter is making.

**If it reads anything else**, the chapter's count is wrong and F1a of
`ch4-prose-pass-followup-01.md` must be redone with the real number.

---

## H2 - The holiday columns as standard inputs {#h2}

**Claim as written:** Table 4 lists `days_in_month, n_holidays,
non_holiday_days` against "LightGBM, XGBoost, Ridge", and §4.3 says their
contribution *"was measured by an ablation against an otherwise identical model
before they were adopted"*.

**Status:** in `FEATURES` as of `3f8b0a9`. **Your own comment on this row says
"Waiting for HPC Training Run to finish", which is the right call.**

**What answers it:** the same banner. If the holiday columns resolve, they
trained.

**Why this needs a run and not just the code:** the commit message records that
the previous state had these columns *measured by the ablation but absent from
every feature list*, so the ablation reported a benefit the served model could
not receive. That is exactly the class of error a code read misses and a run
banner catches.

**If they did not resolve:** the row reverts to "Ablation arm", H1's count drops
to fifteen, and the §4.3 sentence returns to describing them as a separate
benchmark arm.

---

## H3 - The intermittency columns {#h3}

**Claim as written:** *"the remaining two describe intermittency, flagging
whether a month falls inside a run of zero-sales months and how long that run has
lasted"* (§4.3), plus the optional §4.1.3 sentence if you took it.

**Status:** same as H2. In `FEATURES`, never previously consumed by any training
script.

**Note:** these are the more likely of the two groups to behave unexpectedly.
`step_2_07_zero_types.csv` reports **"no zeros"** for all four categories, so
`zero_run_flag` may be constant zero across the entire panel. A constant column
is harmless but carries no information, and claiming it as a model input would be
technically true and substantively empty.

**Check specifically:** whether `zero_run_flag` has any non-zero values in the
matrices. If it does not, say so in the chapter or drop the claim.

---

## H4 - The promotional lag description {#h4}

**Claim as written:** Table 4's promotional row now reads *"Promotional share of
units (clipped 0–1), carried forward one period for forecast availability."*

**Status:** matches `engineer_features.py:585`, which groups and shifts the
ratio. **Your comment says "Added after Prose Pass. Must be verified after HPC
Training Run".**

**What answers it:** the shift is applied in feature engineering, not training,
so a run does not strictly test it. What a run confirms is that the column the
model consumed is the shifted one and not a re-derived contemporaneous ratio.

**Cheaper check, available now:** correlate `promo_intensity` against
`promo_units / sales_units` in the same row of a matrix. If they match exactly,
the shift did not apply.

---

## H5 and H6 - The redundancy reduction {#h5} {#h6}

**Claim as written:** §4.3 says the reduction *"yields a smaller set"* and *"raised
mean test error from 26.4 to 28.8 per cent"*.

**Status:** the *direction* is safe; the *numbers* are not. Both were measured
against a 16-feature input set. The set is now 18, so grouping at the same
threshold produces a different reduced set and a different error.

**Deliberate mitigation already applied:** F3d of the follow-up removed the
phrase "a set of nine" for exactly this reason. The remaining exposure is the
26.4 and 28.8 figures, which are still stated.

**What answers it:** re-run whatever produced
`98_feature_redundancy_reduction.md` against the current feature set.

**If you cannot re-run it in time:** the honest fallback is to describe the
result qualitatively — *"a reduced feature set was evaluated and performed
worse"* — and drop both numbers. A directional claim from a superseded feature
set is defensible; a decimal from one is not.

---

# Chapter 5

## H7 - Every accuracy figure in §5.5 {#h7}

The whole results section rests on the run. Nothing to check item by item until
it lands; recorded so the Chapter 5 pass does not treat those numbers as settled.

**The Chapter 5 prose pass should be written knowing this** — convert the
fragments to prose, but do not spend effort verifying individual WMAPE values
that are about to be regenerated.

---

## H8 - The casing bug, and whether results cover four categories {#h8}

⚠ **The item on this list most likely to invalidate something.**

Commit `9745bf3`: *"fix: category-name casing silently dropped
Danskvand/Energidrikke on Linux"*.

**What this means:** results produced on the HPC *before* that fix may cover two
of four categories rather than all four, with no error raised — the categories
were dropped silently.

**What answers it:** confirm the completed run's outputs contain all four
category names. Any results file predating `9745bf3` should be treated as
suspect until re-checked.

**Why it matters beyond correctness:** the pooled-versus-specialised comparison
and the cross-category generalisation claim both depend on four categories being
present. A two-category run would not fail, it would quietly answer a different
question.

---

## H9 - Test-set row counts {#h9}

**Claim as written:** Chapter 5 §5.3.1 gives 665 rows for CSD, 372 for RTD, 308
for energidrikke and 174 for danskvand.

**Status:** verified correct against the matrices in an earlier session. They are
a property of the split and the retention rule, so they only change if the panel
is re-pulled or the horizon changes.

**Check anyway**, because they are the denominators behind every error figure
reported, and the panel is re-pulled monthly.

---

## H10 - Thread count on the accuracy runs {#h10}

**The project rule:** any SRQ1 accuracy run must set `XGB_N_JOBS = 1`. Thread
count alone produced a 2.65 percentage-point WMAPE spread, so a run without it
is not comparable to one with it.

**What answers it:** the run's configuration. Confirm before any number from it
reaches the thesis.

**Not applicable to profiling runs**, where multi-threading is deliberate and
documented.

---

# How to work through this list

When the run finishes, the fastest order is:

1. **H8 first** — if the run covers two categories, nothing else on the list
   matters until it is re-run.
2. **H10** — if threads were not pinned, the accuracy numbers are not usable.
3. **H1, H2, H3** — one banner line answers all three.
4. **H4** — a two-line correlation check.
5. **H5, H6** — needs a separate re-run of the redundancy analysis.
6. **H7, H9** — the Chapter 5 numbers themselves.

Steps 1 and 2 are gates. Everything below them assumes they passed.

---

# Appending to this file

Any pass that writes a claim resting on a pending run adds a row here **at the
time it writes the claim**, not afterwards. A claim that depends on a future
measurement and is not recorded is a claim nobody will re-check.
