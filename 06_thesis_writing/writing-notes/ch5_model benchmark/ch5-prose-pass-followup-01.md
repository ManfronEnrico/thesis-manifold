---
name: ch5-prose-pass-followup-01
description: NOTE - Two results tables were regenerated while the main pass was being written. F8 and part of F4 are superseded. The H11 gate is RESOLVED and section 5.6's claim survives.
snapshot: 2026-09-10_15-32_ch5-full-pass
category: workflow
applies-to: [chapter 5]
supersedes: [ch5-prose-pass.md F8, ch5-prose-pass.md F4 two figures]
created: 2026_09_10-16_40
updated: 2026_09_10-16_40
status: ready
---

# Chapter 5 - follow-up 01

**Read this before applying F8 or F4 from the main pass.**

Four commits landed from the VPS while the main pass was being written, at
`cd4ff34`. Two of them regenerated results tables the pass had already read, so
three of its numbers are superseded by numbers that are twenty minutes newer.

**This is the currency failure the rules exist to catch, caught.** The main pass
verified against `71fe47b` and said so; that is what made the drift visible
rather than silent.

| In the main pass | Status |
|---|---|
| **F8**, the seed-stability table | **replaced** - F1 below. Every cell changed |
| **F8**, the blocked H11 gate | **RESOLVED** - F2 below. §5.6's claim survives |
| **F4**, two Prophet figures | two decimals moved - F3 below |
| Everything else | **stands.** F1 through F7, F9 through F15 are unaffected |

---

# F1 - The seed-stability table, again {#f1}

Source: `tables/10_seed_stability.csv`, regenerated 2026-09-10 at `fbc67a3` on
the 18-feature run. The figures in the main pass came from the 2026-09-08 file.

**Use this table, not the one in F8 of the main pass.**

### Anchor

**Section 5.5.9 Forecast stability across seeds.** The eight-row table above the
caption **"Table 13 - Seed Stabiltiy across Models and Categories"** - the one
beginning *"CSD | LightGBM | 0.112"*.

### Action

REPLACE the table and caption.

**Replace with:**

| Category | Model | Median CV (%) | WMAPE mean (%) | WMAPE sd (pp) |
|---|---|---|---|---|
| CSD | LightGBM | 18.16 | 18.87 | 0.67 |
| CSD | XGBoost | 15.19 | 18.61 | 0.83 |
| danskvand | LightGBM | 13.76 | 27.01 | 2.81 |
| danskvand | XGBoost | 17.39 | 25.80 | 1.04 |
| energidrikke | LightGBM | 23.92 | 16.24 | 0.59 |
| energidrikke | XGBoost | 24.29 | 16.95 | 1.08 |
| RTD | LightGBM | 9.85 | 30.50 | 0.30 |
| RTD | XGBoost | 11.35 | 30.08 | 1.04 |

**Caption:** *Table 13 - Forecast and accuracy variation across five random
seeds, by category and model*

### Note - the aggregate-versus-individual sentence changes with it

F8's replacement sentence quoted 10 to 17 per cent. The measured range is now
**9.9 to 24.3 per cent**, against an aggregate movement of roughly 2 to 10 per
cent of its own level.

**Use this instead:**

> Aggregate weighted error moves by between 1 and 10 per cent of its own level
> across seeds, while the typical individual forecast moves by between 10 and 24
> per cent. Per-cell movements partly cancel within a volume-weighted sum, so a
> planner reading one brand's number experiences considerably more run-to-run
> variability than the headline metric implies. Both are reported for that
> reason.

### Note - the p90 recommendation still holds

The regenerated table still carries no ninetieth-percentile column, so the
chapter's *"30-73%"* clause still has no source. Drop it, as F8 recommended.

---

# F2 - H11 is resolved, and §5.6 survives {#f2}

**The main pass blocked on this and marked it a gate.** It is now answered, and
the answer is favourable.

The published aggregates support §5.6's claim directly, without needing the
per-seed winner table at all:

| Category | LightGBM | XGBoost | Gap | Largest seed sd | Verdict |
|---|---|---|---|---|---|
| CSD | 18.87% | 18.61% | 0.26 pp | 0.83 pp | **inside noise** |
| danskvand | 27.01% | 25.80% | 1.21 pp | 2.81 pp | **inside noise** |
| energidrikke | 16.24% | 16.95% | 0.71 pp | 1.08 pp | **inside noise** |
| RTD | 30.50% | 30.08% | 0.42 pp | 1.04 pp | **inside noise** |

**In all four categories the between-model difference is smaller than the
between-seed standard deviation of at least one of the two models.** That is
precisely what "statistically indistinguishable" means here, and it is now
measurable from a published artefact rather than resting on a table that could
not be reproduced.

**This is a stronger position than the chapter had before**, because the claim no
longer depends on a per-seed winner list. It rests on two columns of a table an
examiner can check.

### Anchor

**Section 5.5.9.** The second table, listing a winner per seed, above the
sentence *"Every input is identical; only the random seed differs."*

### Action

DELETE the per-seed winner table, and REPLACE the paragraph above it.

**Replace with:**

> Second, and more consequentially for this chapter, the difference between the
> two gradient-boosted models is smaller than the variation the seed alone
> produces. The gap between LightGBM and XGBoost ranges from 0.26 to 1.21
> percentage points across the four categories, while the standard deviation of
> weighted error across seeds reaches 0.83, 2.81, 1.08 and 1.04 points
> respectively. In every category the between-model difference falls inside the
> between-seed variation of at least one of the two models.
>
> Because every input other than the seed is held identical, a statement of which
> gradient-boosting model is best in a given category would report the outcome of
> one draw rather than a property of the models. §5.6 states the conclusion this
> supports instead.

### Note - what this does to §5.6

**Nothing needs rewriting.** §5.6's three claims all hold:

- *"The choice between LightGBM and XGBoost is not supported by this data"* -
  supported, now by the comparison above.
- *"the between-seed spread exceeding the between-model difference"* - **exactly
  what the table shows**, in all four categories.
- *"both gradient boosters clearly beat Ridge and ARIMA on most categories, and
  clearly lose to seasonal naive on RTD"* - Ridge and ARIMA are beaten on three
  of four (danskvand is the exception, where Prophet wins); seasonal naive still
  wins RTD.

**One sentence in §5.6 does need its cross-reference fixed**, and F1 of the main
pass covers it: *"(§6.5.7)"* becomes *"(§5.5.9)"*.

⚠ **One clause must go.** §5.6 says *"A five-seed sweep with every input held
identical shows the winning model changes with the seed in all four
categories."* That specific claim is the one with no artefact. Replace it:

> A five-seed sweep with every input held identical shows the difference between
> the two models to be smaller than the variation the seed alone produces, in all
> four categories.

### Note - the danskvand row is the interesting one

LightGBM's seed standard deviation on danskvand is **2.81 points**, more than
twice any other cell. On the smallest panel, with 174 test rows, one model is
markedly less stable than the other.

That is worth a sentence, because it is the only place in the study where
stability rather than accuracy would decide a deployment:

> The exception is danskvand, where LightGBM's accuracy varies by 2.81 points
> across seeds against XGBoost's 1.04. On the smallest panel the two models are
> equally accurate on average but not equally dependable, which is the one case
> in this study where stability rather than accuracy would decide a deployment.

---

# F3 - Two Prophet figures in Table 10 {#f3}

`09_statistical_baselines.csv` was regenerated in the same round. **Only Prophet
moved**, and only in the third decimal place of the story:

| Cell | Main pass | Now |
|---|---|---|
| danskvand Prophet | 19.5% | **19.4%** |
| energidrikke Prophet | 972.4% | **975.0%** |

### Action

In F4's replacement table, change those two cells. **Everything else in that
table is unchanged** - Naive, Seasonal naive, Drift, Ridge and ARIMA are
identical, and the danskvand reversal that F4 reports stands exactly as written.

The prose in F4 quotes *"Prophet reaches 19.5 per cent"* - make it **19.4**.

### Note - the category labels are now capitalised

The regenerated file writes `Danskvand` and `Energidrikke` where the previous one
wrote them lowercase. The chapter uses lowercase throughout and should keep
doing so; this is a generator convention, not a naming decision.

---

# What did not change

I re-read every other source file this pass cites after the merge. **None of
these moved:**

| Table | Source | State |
|---|---|---|
| Table 9 | `cv_metrics.csv` | unchanged, 2026-09-09 21:10 |
| Table 11 | `mase.csv` | unchanged |
| Table 12 | `pooled_summary.md` | unchanged |
| Table 8 | `demand_classes.md` | unchanged |
| Calibration | `calibration.csv` | unchanged |
| Operational profile | `profiling.csv` | unchanged - still 13 features, so H12 stands |
| Holiday ablation | tables 94 and 95 | unchanged, 2026-09-10 14:02 |

**F1 (cross-references), F2, F3, F5, F6, F7, F9, F10, F11, F12, F13, F14 and F15
of the main pass are unaffected** and can be applied as written.

---

# The register updates

- **H11** is marked **resolved** in `post-hpc-validation.md`, with the resolution
  recorded rather than the row deleted.
- **H12** stands. `profiling.csv` still reports 13 features.
