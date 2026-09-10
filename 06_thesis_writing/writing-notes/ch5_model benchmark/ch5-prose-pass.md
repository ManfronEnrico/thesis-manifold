---
name: ch5-prose-pass
description: NOTE - Chapter 5 full pass. Every results table is stale against the 2026-09-09/10 re-runs and must be replaced. Carries the replacement tables, the prose conversion for the bullet sections, all 49 comment verdicts, and the cross-reference repair.
snapshot: 2026-09-10_15-32_ch5-full-pass
category: workflow
applies-to: [chapter 5]
created: 2026_09_10-16_10
updated: 2026_09_10-16_10
status: ready
---

# Chapter 5 - full pass

Verified at commit `71fe47b`, snapshot `2026-09-10_15-32_ch5-full-pass`, Zotero
re-pulled the same minute: **87 items**.

**Notes swept:** `srq1-forecast-horizon-defect-and-split-correction.md`
(**superseded** - the defect it reports is fixed, archived),
`ch5-ch6-swap-reference-repair.md` (not applied - carried into Fix 1),
`srq1-holiday-ablation-and-the-tuning-inversion.md` (not applied - carried into
Fix 12), and the three August reference notes on the model ladder, pooling and
tuning (**absorbed** - the chapter already makes their arguments; kept as
reference, not queued work).

---

# Read this first

**Every results table in this chapter is stale.** Tables 8 through 13 were
written against runs that predate the 2026-09-09 and 2026-09-10 re-runs, and all
six now disagree with the files they came from.

This is not a decimal drift. Two of the chapter's stated findings change
identity:

| Chapter says | Measured now |
|---|---|
| On danskvand, **Ridge** reaches 10.9%, half the tuned error | Ridge is **74.9%**, the *worst* baseline. **Prophet** wins danskvand at 19.5% |
| CSD LightGBM 14.5%, XGBoost 15.2% | 19.3% and 18.4% |
| Plateau trials 3 to 87, median near 16 | 0 to 83, **median 55** |

The headline argument **survives** - two of four categories are still beaten by
a method that is not a tuned gradient booster - but the two categories are now
danskvand and RTD for different reasons, and the danskvand story reverses
completely.

**Do not paste any results paragraph in this note without its table.** The prose
and the numbers were re-measured together.

---

# The fixes

Fifteen fixes. Order matters only for 2 and 3, which touch the same table.

| # | Fix | Kind |
|---|---|---|
| [1](#f1) | Twenty-one cross-references still point at Chapter 6 | mechanical |
| [2](#f2) | Table 9 - every cell is stale | numbers |
| [3](#f3) | 5.5.1's prose, rebuilt on the new table | numbers + prose |
| [4](#f4) | Table 10 and the danskvand reversal | numbers + prose |
| [5](#f5) | Table 11 - MASE | numbers |
| [6](#f6) | Table 12 and the pooling story | numbers + prose |
| [7](#f7) | Table 8 - demand classes | numbers |
| [8](#f8) | Table 13 - seed stability | numbers |
| [9](#f9) | 5.5.6 - the operational profile is wrong in every figure | numbers |
| [10](#f10) | 5.5.7 - calibration, and the danskvand width claim | numbers + prose |
| [11](#f11) | 5.3.2 - the feature set is 18, not 13, and it now has holidays | numbers + prose |
| [12](#f12) | 5.5.8 needs the holiday ablation it does not have | new prose |
| [13](#f13) | 5.3.5 - the plateau claim | numbers |
| [14](#f14) | The bullet sections, converted to prose | prose |
| [15](#f15) | Metacomment, table names, and the Outstanding-decisions block | prose |

---

# F1 - Twenty-one cross-references still point at Chapter 6 {#f1}

The Ch5/Ch6 swap renumbered the headings but not the body text. Every internal
reference in this chapter names a section that is now in a different chapter.

**This is the highest-value fix in the note** because it is mechanical, it is
twenty-one errors, and an examiner following one lands in the wrong chapter.

### Action

Find and replace, whole document. Word's Replace All handles all of these.

| Find | Replace | Occurrences |
|---|---|---|
| `§6.2.0` | `§5.2.1` | 2 |
| `§6.3.1` | `§5.3.1` | 1 |
| `§6.3.4` | `§5.3.4` | 1 |
| `§6.3.5` | `§5.3.5` | 2 |
| `§6.4.1` | `§5.4.1` | 2 |
| `§6.4.3` | `§5.4.3` | 2 |
| `§6.4.4` | `§5.4.4` | 2 |
| `§6.5` | `§5.5` | 1 |
| `§6.5.2` | `§5.5.2` | 2 |
| `§6.5.6` | `§5.5.6` | 1 |
| `§6.5.7` | `§5.5.9` | 1 |
| `§6.5.9` | `§5.5.9` | 1 |
| `§6.6` | `§5.6` | 2 |
| `Ch.6` | `Ch.5` | 1 |

⚠ **Two of these are not a simple digit swap.** `§6.2.0` has no counterpart -
the section is `5.2.1 Simple benchmarks`. And `§6.5.7` was already wrong before
the swap: it points at the seed-stability section, which is **5.5.9**.

### Note - do these in descending order of specificity

Replace `§6.5.2`, `§6.5.6`, `§6.5.7` and `§6.5.9` **before** `§6.5`, or the shorter
pattern matches inside the longer ones and leaves you with `5.5.2` reached by
luck rather than by rule. Word replaces on literal text and will not warn you.

---

# F2 - Table 9, every cell is stale {#f2}

Source: `05_model_benchmark/tables/cv_metrics.csv`, written 2026-09-09 21:10.
The chapter's table predates it.

### Anchor

**Section 5.5.1 Tabular-model benchmark.** The table captioned **"Table 9 -
Performance Overview - Tuned WMAPE adn medMAPE"**. Its first data row begins
*"CSD | LightGBM | 17.0%"*.

### Action

REPLACE the whole table, and fix the caption's two typos.

**Replace with:**

| Category | Model | CV WMAPE | Test WMAPE | Test medMAPE | n test |
|---|---|---|---|---|---|
| CSD | LightGBM | 19.4% | 19.3% | 45.7% | 665 |
| CSD | XGBoost | 18.8% | 18.4% | 41.4% | 665 |
| danskvand | LightGBM | 28.7% | 27.3% | 37.5% | 174 |
| danskvand | XGBoost | 25.7% | 27.1% | 40.4% | 174 |
| energidrikke | LightGBM | 11.5% | 16.2% | 54.8% | 308 |
| energidrikke | XGBoost | 12.2% | 15.5% | 56.0% | 308 |
| RTD | LightGBM | 34.2% | 30.3% | 49.8% | 372 |
| RTD | XGBoost | 34.5% | 30.2% | 46.2% | 372 |

**Caption:** *Table 9 - Test performance of the tuned tabular models, by
category and objective*

### Note - answering comment 247

Thread 247 is a bare `VERIFY` on this table. **Verified, and it did not
survive**: all 24 numbers moved. The caption also carried two spelling errors
("adn", and no sentence structure), which the replacement fixes.

---

# F3 - 5.5.1's prose, rebuilt on the new table {#f3}

Two paragraphs quote figures that F2 replaces. The **argument is unchanged** -
the objectives still select different models and the validation-to-test gap is
still real - but every illustrative number moved.

### Anchor - part A

**Section 5.5.1.** The paragraph beginning **"The two objectives select
different models and produce different rankings."**

First five words: *"The two objectives select different..."*
Last five words: *"...why both are carried here."*

### Action

REPLACE the paragraph.

**Replace with:**

> The two objectives select different models and produce different rankings.
> Tuning for median absolute percentage error improves that metric and degrades
> weighted error, as the theory in §5.4.1 predicts: absolute-error loss is
> minimised by the median, while a pointwise percentage error is minimised by a
> lower functional. The effect is largest on energidrikke, where XGBoost tuned
> for median error reaches 24.7 per cent weighted error against 15.5 per cent
> when tuned for weighted error, a penalty of 9.3 percentage points for a gain
> of 8.3 on the metric it optimised. A single claim of a best model is therefore
> meaningless without naming the objective it was tuned against, which is why
> both are reported.

### Anchor - part B

**Section 5.5.1.** The next paragraph, beginning **"Validation-to-test movement
is substantial and is not hidden."**

First five words: *"Validation-to-test movement is substantial and..."*
Last five words: *"...degree (Cawley & Talbot, 2010)."*

### Action

REPLACE.

**Replace with:**

> Validation-to-test movement is substantial and is not concealed. Energidrikke
> tunes to between 11.5 and 12.2 per cent in cross-validation and lands at 15.5
> to 16.2 per cent on test, while RTD moves the other way, tuning to 34.2 per
> cent and testing at 30.3. The gap is consistent with the selection bias
> documented in §5.3.5: this protocol is not nested, so the cross-validation
> figure is an optimistically biased estimate of generalisation, to a degree
> that cannot be quantified from within the protocol itself (Cawley & Talbot,
> 2010).

### Note - the direction of the gap is now mixed, and that is worth keeping

Under the old numbers energidrikke over-fitted and RTD under-fitted. That still
holds, and it is the better illustration of the point: a non-nested protocol is
biased *in expectation*, not in every cell, so a chapter showing the gap running
one way in all four categories would be describing something other than
selection bias.

---

# F4 - Table 10, and the danskvand reversal {#f4}

**This is the largest single change in the chapter.** The chapter says a plain
Ridge regression reaches 10.9 per cent on danskvand, roughly half the tuned
gradient-boosted error, and builds a paragraph on it.

**Measured now, Ridge is 74.9 per cent on danskvand - the worst of the six
baselines.** The category is instead won by Prophet, at 19.5 per cent.

Source: `tables/09_statistical_baselines.csv`, written 2026-09-08 18:51.

### Anchor - part A, the table

**Section 5.5.2 The simple benchmarks, and where they win.** The table captioned
**"Table 10 - Four Categories x 5 Model Performance"**. Its first data row begins
*"CSD | 42.9%"*.

### Action

REPLACE the table and the caption.

**Replace with:**

| Category | Naive | Seasonal naive | Drift | Ridge | ARIMA | Prophet | Best tuned model |
|---|---|---|---|---|---|---|---|
| CSD | 42.9% | 19.2% | 47.7% | 23.8% | 21.8% | 105.7% | **18.4%** (XGBoost) |
| danskvand | 32.5% | 35.9% | 32.0% | 74.9% | 33.5% | **19.5%** | 27.1% (XGBoost) |
| energidrikke | 18.9% | 23.8% | 17.7% | 23.6% | 19.4% | 972.4% | **15.5%** (XGBoost) |
| RTD | 89.3% | **27.3%** | 95.9% | 52.4% | 53.3% | 66.8% | 30.2% (XGBoost) |

**Caption:** *Table 10 - Weighted MAPE of the simple and statistical benchmarks
against the best tuned model, by category. The lowest error in each row is
shown in bold.*

### Note - this answers comment 253 directly

You asked: *"wth is 'Best tuned ML'?! Which one does it refer to? It doesnt seem
like its jsut a focus column from the named approaches / models."*

**You were right to flag it.** The old column was the better of LightGBM and
XGBoost tuned for weighted error, but the table never said so, and the model
varied by row without being named. The replacement names the model in each cell,
so the reader can see it is XGBoost throughout - which is itself newly true, and
a change from the previous run where the winner varied.

### Anchor - part B, the paragraph that is now false

**Section 5.5.2.** The bolded paragraph beginning **"On danskvand, a plain Ridge
regression reaches 10.9%"**.

First five words: *"On danskvand, a plain Ridge..."*
Last five words: *"...least to learn from."*

### Action

REPLACE. The claim inverts.

**Replace with:**

> **On danskvand, Prophet reaches 19.5 per cent against the tuned models' 27.1**,
> and it is the only category where the method is competitive at all. Danskvand
> is also the smallest panel, at twenty-nine series and 174 test rows, where a
> high-capacity model has least to learn from. The same scarcity that limits the
> tuned models also flatters a method that imposes a strong parametric structure
> rather than estimating one from the data.

### Anchor - part C, the sentence naming which categories are lost

**Section 5.5.2.** The bolded sentence **"Two categories are not won by the
tuned models, and this is the most important result in the section."**

### Action

Keep the sentence. It is still true - danskvand and RTD - but the reason differs
per category, so the RTD paragraph that follows must change.

**Replace the RTD paragraph** (*"On RTD, seasonal naive beats every tuned
configuration - 27.3% against 31.8-36.1%..."*) with:

> **On RTD, seasonal naive beats every tuned configuration**, at 27.3 per cent
> against 30.2. The most irregular category is the one where a method with no
> parameters wins, and the margin is small enough that the tuned models cannot
> be said to have failed so much as to have bought nothing.

### Note - the Prophet paragraph needs one clause added

The paragraph beginning *"Prophet is applied outside its design regime"* now
sits directly above a table where **Prophet wins a category**. Its argument
still holds for the 105.7 and 972.4 figures, but it must acknowledge the
exception or it reads as contradicted by the table above it.

**Add as its final sentence:**

> That it nonetheless wins danskvand is consistent with this reading rather than
> against it: where the panel is shortest, a method that imposes a trend and an
> annual cycle rather than estimating flexible structure has least to get wrong.

### Note - the Ridge instability paragraph is still correct, with new figures

The paragraph beginning *"Ridge requires clipping to be reportable"* stands. The
unclipped figures now diverge to roughly 1e25 on danskvand, 1e13 on energidrikke
and 1e5 on RTD, and reach 84.8 per cent on CSD. Replace the two quoted values -
*"2.8x10^13"* and *"2459%"* - with those.

---

# F5 - Table 11, MASE {#f5}

Source: `tables/mase.csv`, 2026-09-09 21:10.

### Anchor

**Section 5.5.3 Scaled error (MASE).** The table captioned **"Table 11 -
Categories: MASE Comparison"**. Its first data row begins *"CSD | 0.95"*.

### Action

REPLACE the table and caption.

**Replace with:**

| Category | Naive MASE | Seasonal-naive MASE | Naive median ASE |
|---|---|---|---|
| CSD | 1.11 | 1.86 | 0.47 |
| danskvand | 1.18 | 1.76 | 0.53 |
| energidrikke | 0.84 | 2.14 | 0.13 |
| RTD | 11.80 | 13.48 | 0.28 |

**Caption:** *Table 11 - Mean and median scaled error by category, against the
in-sample naive benchmark*

### Note - one sentence in the prose below must change

The paragraph beginning *"RTD's mean MASE of 6.54 against a median ASE of 0.18"*
quotes two numbers that are now **11.80 and 0.28**. The argument is unaffected
and in fact strengthened: the gap between mean and median is wider, so the
distributional point is more visible.

⚠ **A second claim in that section needs checking.** The chapter says
*"Seasonal naive scores worse than naive on MASE in every category while winning
on WMAPE for RTD."* Seasonal naive is still worse on MASE everywhere. On
weighted error it now beats plain naive on CSD as well as RTD, so the contrast
as written is narrower than the data supports. Read it once Table 10 is in.

---

# F6 - Table 12, and the pooling story {#f6}

Source: `tables/pooled_summary.md`, 2026-09-09 21:10.

**The finding is unchanged in shape and larger in magnitude.** Pooling still
wins the two small categories and loses the two large ones. The deltas are now
5.7 and 5.6 percentage points rather than 2.2 and 1.6, which matters because the
chapter currently says the magnitudes sit within seed noise.

### Anchor

**Section 5.5.4 Pooled versus per-category training.** The table captioned
**"Table 12 - Pooled vs Per Category Performance Differences"**. Its first data
row begins *"CSD | 17.5% -> 16.3%"*.

### Action

REPLACE the table and caption.

**Replace with:**

| Category | LightGBM pooled to per-category | XGBoost pooled to per-category |
|---|---|---|
| CSD | 19.3% to 18.7% (per-category better by 0.6 pp) | 21.7% to 19.1% (per-category by 2.6) |
| danskvand | 21.0% to 26.7% (pooling wins by 5.7 pp) | 18.9% to 23.4% (pooling wins by 4.5) |
| energidrikke | 15.5% to 21.1% (pooling wins by 5.6) | 16.8% to 16.8% (level) |
| RTD | 31.3% to 31.9% (pooling wins by 0.6) | 40.5% to 30.8% (per-category by 9.8) |

**Caption:** *Table 12 - Weighted MAPE under pooled and per-category training,
by category and model*

### Note - the RTD row no longer agrees between the two models

Under the old numbers both families put RTD on the per-category side, which is
what the chapter calls *"what makes it a finding rather than noise"*. Now
LightGBM has RTD marginally pooled-better at 0.6 pp while XGBoost has it
strongly per-category-better at 9.8 pp.

**That claim needs narrowing.** Replace the sentence *"The pattern holds for
both model families, which is what makes it a finding rather than noise"* with:

> The pattern holds for both model families on the two small categories, where
> pooling wins by between 4.5 and 5.7 percentage points, and that agreement is
> what makes the small-panel result a finding rather than noise. The two large
> categories are less consistent: RTD favours per-category training under
> XGBoost by 9.8 points while the two arms are level under LightGBM, so the
> claim made here is confined to the direction of the small-panel effect.

### Note - one clause should now come out

The chapter says *"though §6.5.9 shows the magnitudes here sit within seed
noise, so the direction is the claim, not the pp values."* The seed standard
deviations are 0.38 to 1.94 pp (Table 13). **A 5.7 pp pooling gain is roughly
three times the largest seed standard deviation**, so it no longer sits within
noise.

**Reword to:**

> The two small-panel gains, at 4.5 and 5.7 percentage points, exceed the
> largest between-seed standard deviation reported in §5.5.9 by roughly a factor
> of three; the sub-point differences on CSD and on RTD under LightGBM do not,
> and are not read as ordering those categories.

### Note - the per-brand paragraph

The paragraph citing *"pooling helps between 44% and 64% of brands"* is now
**31 to 57 per cent**, from `pooled_perbrand_summary.md`. The coin-flip
characterisation holds for the smooth, erratic and intermittent classes. The
lumpy class is now clearly below a coin flip, at 31 and 38 per cent, which is
worth stating: it is the class where pooling was least likely to help, and it
visibly does not.

---

# F7 - Table 8, demand classes {#f7}

Source: `tables/demand_classes.md`, 2026-09-09 21:10.

### Anchor

**Section 5.4.4 Demand-pattern categorisation.** The table captioned **"Table 8
- Category Resulting Distribution (230 brands)"**. Its first data row begins
*"CSD | 44 | 32"*.

### Action

REPLACE the table. The caption's total of 230 is still correct.

**Replace with:**

| Category | smooth | erratic | intermittent | lumpy |
|---|---|---|---|---|
| CSD | 46 | 29 | 6 | 14 |
| RTD | 27 | 21 | 7 | 7 |
| energidrikke | 15 | 19 | 3 | 7 |
| danskvand | 16 | 9 | 3 | 1 |

### Note - the totals in 5.5.5 change with it

Section 5.5.5 opens *"the 230 brands divide into 108 smooth, 79 erratic, 12
intermittent and 31 lumpy."* The measured split is now **104 smooth, 78 erratic,
19 intermittent and 29 lumpy**, still 230.

⚠ **And the lumpy no-signal count changes.** The chapter says *"15 of the
31 lumpy brands have no test signal at all."* It is now **13 of 29**, leaving 16
scored - which is the same 16 the chapter already names, so only the two counts
need editing.

---

# F8 - Table 13, seed stability {#f8}

Source: `tables/10_seed_stability.md`, 2026-09-08 18:51.

### Anchor

**Section 5.5.9 Forecast stability across seeds.** The eight-row table above the
caption **"Table 13 - Seed Stabiltiy across Models and Categories"** - the one
beginning *"CSD | LightGBM | 0.112"*.

### Action

REPLACE the table.

**Replace with:**

| Category | Model | Median CV | WMAPE mean | WMAPE sd |
|---|---|---|---|---|
| CSD | LightGBM | 0.112 | 15.4% | 0.65 |
| CSD | XGBoost | 0.125 | 15.6% | 0.56 |
| danskvand | LightGBM | 0.119 | 20.8% | 0.69 |
| danskvand | XGBoost | 0.172 | 21.5% | 1.22 |
| energidrikke | LightGBM | 0.137 | 13.9% | 1.38 |
| energidrikke | XGBoost | 0.162 | 14.4% | 0.38 |
| RTD | LightGBM | 0.144 | 32.3% | 1.94 |
| RTD | XGBoost | 0.096 | 35.5% | 1.50 |

**Caption:** *Table 13 - Forecast and accuracy variation across five random
seeds, by category and model*

### Note - the p90 column is gone, and one sentence depends on it

The published table no longer reports a ninetieth-percentile coefficient of
variation. The chapter's clause *"and the ninetieth-percentile cell by 30-73%"*
therefore has no source in the current artefact.

**Two options.** Drop the clause, or re-derive p90 from the stability run's raw
output. **I recommend dropping it** - the median CV of 9.6 to 17.2 per cent
already carries the argument that individual cells move far more than the
aggregate, and that ratio is the point.

**Reworded sentence:**

> Aggregate weighted error moves by roughly 4 per cent of its own level across
> seeds, while the typical individual forecast moves by 10 to 17 per cent.

### Note - the winner-flip table needs re-deriving, and I could not

The second table in 5.5.9, listing the winning model per seed, is **not
reproducible from the published artefacts** - `10_seed_stability.csv` reports
per-model aggregates, not per-seed winners.

**It is also now in tension with the means.** LightGBM has the lower mean
weighted error in all four categories, by 0.1 to 3.2 points. The flip may well
be real, but the chapter cannot cite what is not on disk, and §5.6 rests on it
entirely.

**Tracked as H11 in `post-hpc-validation.md`, marked a gate.** See the Blocked
section below - this is the one item in the chapter I cannot close.

---

# F9 - 5.5.6, the operational profile {#f9}

Source: `tables/profiling.csv` and `tables/05_substrate_resource_profile.md`.

**Every figure in this section is wrong**, one of them by a factor of nearly
three hundred.

| Chapter | Measured |
|---|---|
| Ridge 5.5 MB | 5.4 MB resident |
| LightGBM 8.0 MB | **38.1 MB** |
| XGBoost 0.1 MB | **29.2 MB** |
| ARIMA 0.3 MB | 1.9 MB |
| XGBoost fits in 0.97 s | **3.6 s** |
| XGBoost predicts in 9.3 ms | 13.8 ms |
| LightGBM fits in 2.04 s | **8.0 s** |
| LightGBM predicts in 15.9 ms | 33.0 ms |
| "against the 8 GB sequential budget" | the budget is **4 GB** |

The chapter mixes two different memory measures. The old figures are Python-heap
allocations from `tracemalloc`; the published table now reports **resident set
size**, sampled every 5 ms in a separate process, which is the quantity a
deployment must actually provision.

### Anchor

**Section 5.5.6 Operational profile.** The paragraph beginning **"Peak RAM on
the largest matrix is in single-digit megabytes for every model"**.

First five words: *"Peak RAM on the largest..."*
Last five words: *"...does not bite here."*

### Action

REPLACE both paragraphs of the section.

**Replace with:**

> Peak resident memory on the largest category is 38.1 MB for LightGBM, 29.2 for
> XGBoost, 5.4 for Ridge and 1.9 for a per-series ARIMA fit, against the four-
> gigabyte sequential budget that motivates SRQ1. The heaviest model therefore
> occupies under one per cent of the memory available to it. Resident set size
> is reported here rather than Python-heap allocation because gradient-boosted
> ensembles are built by native libraries that the interpreter's own accounting
> does not observe; the serialised model sizes of 7.6 and 3.7 MB confirm which
> of the two measures reflects what a deployment must provision.
>
> The memory constraint is therefore non-binding by two orders of magnitude at
> this data scale. That is a substantive answer to the research question rather
> than a missing measurement: the constraint that motivated the question does
> not bite at brand-by-month granularity on a four-category panel, and would
> begin to matter only at a grain or a panel size this thesis does not use.
>
> Latency is likewise immaterial. XGBoost fits in 3.6 seconds and predicts in
> 13.8 milliseconds; LightGBM fits in 8.0 seconds and predicts in 33.0. Both sit
> far below any threshold at which an interactive agent would appear to
> hesitate.

### Note - "three orders of magnitude" was arithmetic, and it is now two

38.1 MB against 4096 MB is a factor of 107. The published table gives it as 0.93
per cent of budget. The old text said three orders against 8 GB, which was wrong
on both the numerator and the denominator.

### Note - the profiling run used 13 features

`profiling.csv` records `n_features: 13`, so these timings predate the
18-feature set. **The direction is safe** - more features cost more, not less,
and the headroom is two orders of magnitude - but the figures are a floor.

**Tracked as H12 in `post-hpc-validation.md`**, not a gate: no claim in the
chapter depends on the exact value, only on it being negligible.

---

# F10 - 5.5.7, calibration {#f10}

Source: `tables/calibration.csv`, 2026-09-09 21:10.

**The danskvand width claim is the one to look at.** The chapter says danskvand
meets 90 per cent coverage only with intervals seventeen times the forecast
quantity. Measured now, danskvand **does not meet the target at all** - it
covers 83.9 per cent - and the very wide intervals belong to energidrikke, where
they average thirty-four times the forecast.

### Anchor

**Section 5.5.7 Prediction-interval calibration.** The eight-row table beginning
*"CSD | 90% | 89.6%"*.

### Action

REPLACE the table. Note the column is now **mean** relative width, not median.

**Replace with:**

| Category | Nominal | Empirical coverage | Mean relative width | n test |
|---|---|---|---|---|
| CSD | 90% | 91.0% | 8.6x | 665 |
| RTD | 90% | 90.9% | 8.6x | 372 |
| energidrikke | 90% | 86.0% | 33.6x | 308 |
| danskvand | 90% | 83.9% | 11.9x | 174 |
| CSD | 80% | 82.3% | 3.8x | 665 |
| RTD | 80% | 80.6% | 3.8x | 372 |
| energidrikke | 80% | 78.9% | 12.4x | 308 |
| danskvand | 80% | 72.4% | 2.9x | 174 |

**Add a caption** - this table has none: *Table 14 - Empirical coverage and
relative interval width of the split-conformal intervals, by category and
nominal level*

⚠ **Adding a caption here renumbers Tables 14 onward through the rest of
the thesis.** Word's cross-reference fields update; plain-text table callouts do
not. See the deferred list, S13.

### Anchor - part B, the paragraph below

**Section 5.5.7.** The paragraph beginning **"Coverage alone is the wrong
success criterion, and this table shows why."**

### Action

REPLACE.

**Replace with:**

> Coverage alone is the wrong success criterion, and this table shows why. An
> arbitrarily wide interval attains perfect coverage while carrying no
> decision-relevant information. Energidrikke very nearly meets its 90 per cent
> target, at 86.0 per cent, but only with intervals averaging thirty-four times
> the quantity being forecast, which no planner can act on. CSD and RTD meet the
> target at widths of roughly eight and a half times, which is wide but
> interpretable. Danskvand meets neither level, undercovering at 83.9 per cent
> against a nominal 90 and at 72.4 against a nominal 80. Width rather than
> coverage is therefore the binding constraint on energidrikke, and coverage
> itself is the constraint on danskvand; both are reported as limitations rather
> than averaged into a claim that the intervals are well calibrated.

### Note - the calibration target in 5.4.3 is now failed by one category

Section 5.4.3 sets **85 per cent or better empirical coverage for a nominal 90
per cent interval**. Energidrikke passes at 86.0. **Danskvand fails at 83.9.**

That is worth stating rather than quietly dropping the target: a stated target
that one category misses is a stronger result than no target at all, and §5.5.8
is the place for it. See F12.

---

# F11 - 5.3.2, the feature set is 18, not 13 {#f11}

The chapter describes thirteen features. The canonical list at
`model_training/srq1/_features.py` defines **eighteen**, resolving to seventeen
for danskvand and RTD.

Two whole groups are missing from the chapter's description, and one sentence is
now flatly false.

### Anchor - part A

**Section 5.3.2 Feature engineering.** The bolded lead-in **"Calendar"**, and the
sentence it introduces.

First five words: *"Calendar: month, quarter, and a..."*
Last five words: *"...not from calendar dates."*

### Action

REPLACE. ⚠ **The clause "No holiday calendar is used" is false as of commit
`3f8b0a9`.**

**Replace with:**

> **Calendar.** Month and quarter give deterministic position within the year. A
> binary peak-month flag is derived from each category's own seasonal profile,
> marking months whose mean units exceed the category mean by more than ten per
> cent, and is measured from the sales distribution rather than assumed. Three
> further columns carry the Danish public-holiday calendar: the number of days in
> each month, the number of public holidays falling within it, and the difference
> between the two.

### Anchor - part B

**Section 5.3.2.** The final sentence of the section, beginning *"Missing lag
values for short histories are left as NaN"*.

### Action

INSERT AFTER - two new closing paragraphs.

**Insert:**

> Two columns describe the intermittency regime rather than the level: a flag for
> whether the brand is currently within a run of zero-sales months, and the
> length of that run. Both are shifted so that no value from the predicted month
> enters. A brand two months into a stock-out behaves unlike one selling
> steadily, and the level features alone do not distinguish them.
>
> The full set is therefore eighteen columns for CSD and energidrikke and
> seventeen for danskvand and RTD, the difference being the promotional measure
> Nielsen does not report for the latter two. The list is resolved against each
> category's feature matrix at run time rather than asserted, so a category
> lacking a column is served the columns it has rather than failing.

### Note - why this matters beyond the count

The feature set is the input to every result in §5.5. A chapter that describes
thirteen features while reporting numbers produced by eighteen is not merely
imprecise; it describes a different experiment. This fix and F2 through F10 are
the same correction seen from two ends.

### Note - §5.5.4 says twelve, and that is correct

Section 5.5.4 says both pooling arms use *"the same 12-feature intersection"*.
That is what `pooled_summary.md` reports and it is right **for that experiment**:
the pooled run drops the promotional and holiday columns so both arms see an
identical space. Leave the number, but say why, or it reads as contradicting
§5.3.2:

> Both arms use the same twelve-feature intersection, dropping the promotional
> measure and the holiday columns so that the pooled model sees an identical
> space in every category, the same tuning protocol, and identical test rows.

---

# F12 - 5.5.8 needs the holiday ablation {#f12}

**Chapter 5 has no holiday-ablation subsection, and two appendix tables exist
that nothing cites.** Tables 94 and 95 were regenerated on the 18-feature set on
2026-09-10.

This is the finding carried out of the Chapter 4 pass. Chapter 4 states the
conclusion, which is all a data chapter needs. The methodological half belongs
here.

### Anchor

**Section 5.5.8 Remaining gaps.** Insert **before** it, as a new subsection
5.5.8, pushing the current 5.5.8 to 5.5.9 and seed stability to 5.5.10.

The preceding text ends with the calibration paragraph replaced in F10, whose
last five words will be *"...intervals are well calibrated."*

### Action

INSERT - a new subsection.

**Insert:**

> ### 5.5.8 Holiday enrichment, and what an ablation measures
>
> The Danish public-holiday columns described in §5.3.2 were adopted on the
> evidence of an ablation, and the way that ablation had to be run is itself a
> result worth reporting.
>
> Run first with hyperparameters held fixed across both arms, the enrichment
> appeared to hurt: the holiday columns worsened test error in eight of twelve
> category-and-model combinations. Re-run with each arm tuned independently, the
> same columns improved accuracy in six of nine. The two experiments use the same
> data and the same features and reach opposite conclusions.
>
> The inversion is not a contradiction to be resolved by preferring one number.
> Adding three columns changes the shape of the search space, so a configuration
> tuned for the smaller space is mis-specified for the larger one. A
> fixed-configuration comparison therefore measures the cost of that
> mis-specification rather than the value of the features, and the tuned
> comparison is the one that answers the question actually asked. Tuning improved
> the enriched arm by up to 12.99 percentage points, an order of magnitude larger
> than the feature effect being measured.
>
> The tuned result is reported in Appendix Table 94 and the untuned comparison in
> Table 95. The effect is small in both directions, ranging from a 4.92-point
> improvement on RTD under XGBoost to a 2.21-point degradation on danskvand under
> XGBoost. No mean across cells is reported, because the model families respond
> differently: the linear model benefits in the single category where it was
> tested, while the tree models benefit in five of eight cells. That divergence
> is the substantive finding, and averaging it away would conceal it.
>
> The wider lesson generalises beyond this feature group. Any ablation that holds
> hyperparameters fixed across arms of differing dimensionality measures
> mis-specification rather than the feature, and reports it with a confidence the
> design does not support.

### Note - this is why Table 94 carries a warning

Table 94's internal review note reads: *"Do NOT quote the mean of this column. It
averages over model families that respond differently, and that difference is
itself the finding."* The prose above states the range and the split by family
without ever quoting the mean, which is what the note asks for.

### Note - what else 5.5.8 should now say

The existing Remaining-gaps section should gain the calibration failure from F10:

> The interval-calibration target of 85 per cent empirical coverage at a nominal
> 90 is met on three categories and missed on danskvand, at 83.9 per cent. It is
> reported as missed rather than dropped, since a target abandoned on the
> category that fails it is not a target.

And it must lose one line. **"fig4_ram_budget is stale and contradicts §6.5.6"**
is a note to the authors, not thesis prose. Delete it and fix the figure; it is
tracked as S14 on the deferred list.

---

# F13 - 5.3.5, the plateau claim {#f13}

The chapter says *"Measured plateaus range from 3 to 87 trials with a median near
16, so 100 trials comfortably contains the converged region."*

Measured across the sixteen tuned configurations in `cv_metrics.csv`: **0 to 83,
median 55**.

### Anchor

**Section 5.3.5 Hyperparameter optimisation.** The final sentence of the
paragraph beginning **"The trial budget is justified empirically, not by
convention."**

First five words: *"Measured plateaus range from 3..."*
Last five words: *"...for every configuration."*

### Action

REWORD.

**Before:**

> Measured plateaus range from 3 to 87 trials with a median near 16, so 100
> trials comfortably contains the converged region for every configuration.

**After:**

> Measured plateaus range from zero to 83 trials with a median of 55, so 100
> trials contains the converged region for every configuration, with the
> slowest-converging requiring 83.

### Note - the argument is weaker now and should not be overstated

A median of 55 against a budget of 100 is a much narrower margin than a median of
16. The budget is still justified, since every configuration converged inside it,
but "comfortably" is no longer the right word, and naming the slowest case at 83
of 100 lets a reader judge the headroom for themselves.

⚠ **One plateau is zero.** CSD XGBoost tuned for weighted error found its best
configuration on the first trial and never improved on it. That is not a
convergence failure, but it means the tuning bought that cell nothing, and it is
the cell that now leads Table 10.

---

# F14 - The bullet sections, converted to prose {#f14}

Sections 5.1 through 5.3.3 are still bullet skeletons. Nineteen of the
forty-nine comments carry a `PROSE` tag and they cover exactly these sections.

Rather than reproduce nine subsections, this fix gives the two that carry
argument and are hardest to convert. **The five model descriptions in 5.2.2
through 5.2.6 are specification lists**, and my recommendation is that they
become a comparison table rather than five near-identical paragraphs - see the
note at the end.

## 14a - Section 5.1, Rationale for model selection

### Anchor

**Section 5.1 Rationale for model selection.** The whole section, from the bolded
**"Five model families span the inductive-bias spectrum"** to the end of the
Makridakis paragraph.

First five words: *"Five model families span the..."*
Last five words: *"...(Makridakis et al., 2018, p. 803)"*

### Action

REPLACE the entire section.

**Replace with:**

> Five model families were selected to span the inductive-bias spectrum, from
> classical statistical methods through gradient boosting to regularised linear
> regression, alongside four parameter-free benchmarks. The intent is not to
> assemble the strongest possible ensemble but to establish which class of
> assumption suits monthly brand-level beverage demand, which is a different
> question and the one this sub-research question asks.
>
> Four criteria governed inclusion. A model had to have established empirical
> performance on retail or fast-moving-consumer-goods panels; to fit within the
> four-gigabyte sequential memory budget the deployment context imposes; to be
> interpretable enough to support the scenario comparison reported later in this
> thesis; and to differ in inductive bias from those already admitted. The last
> criterion is what excludes a second gradient-boosting variant chosen for
> accuracy alone, and what admits a regularised linear model despite an
> expectation that it would not win.
>
> The benchmark rung is required rather than decorative. Hyndman and
> Athanasopoulos (2021, §5.2) define the four simple methods as the standard
> against which "any forecasting methods we develop will be compared … to ensure
> that the new method is better than these simple alternatives". A forecasting
> result reported without them is unbenchmarked, and a reader has no way to judge
> whether the model earned its complexity.
>
> The empirical weight behind that requirement comes from the M4 competition, in
> which none of the six pure machine-learning entries beat the statistical
> combination benchmark and only one beat the seasonally adjusted naive baseline
> (Makridakis et al., 2018, p. 803). That result is not evidence that machine
> learning cannot forecast. It is evidence that the benchmark rung is where the
> claim gets tested, which is the use made of it here.

### Note - the criteria list had a broken enumeration

The original reads *"(a) established empirical performance …; fit within the ≤4
GB … (c) interpretability …"* - the (b) label is missing and its clause runs on
from (a). The prose above drops the labels entirely, which is the cleaner fix in
running text.

### Note - the RAM budget

The original says 4 GB here and 8 GB in §5.5.6. **4 GB is correct**, matching
`05_substrate_resource_profile.md`, which reports peak fit memory as a share of
4096 MB. F9 fixes the other end.

## 14b - Section 5.3.3, Execution protocol

### Anchor

**Section 5.3.3 Execution protocol.** The three bullet lines.

First five words: *"Sequential execution: load, fit, predict..."*
Last five words: *"...is measured separately (§6.5)"*

### Action

REPLACE.

**Replace with:**

> Models are fitted sequentially rather than in parallel, each loaded, fitted,
> used for prediction and then unloaded with an explicit garbage collection
> before the next begins. This mirrors the deployment constraint the research
> question names: a single model in memory at a time, on a machine that cannot
> hold several. Memory is profiled at each stage and the peak recorded per model,
> so the figures in §5.5.6 describe the same execution pattern a deployment would
> use rather than a best case measured in isolation.
>
> A fixed random seed of 42 is used throughout, and the sensitivity of the results
> to that choice is measured in §5.5.9 rather than assumed away.

### Note - the five model descriptions

Sections 5.2.2 through 5.2.6 each give role, implementation, memory and a stated
limitation for one model, in the same order. **A single comparison table would
read better than five paragraphs** and would make the ladder visible, which is
the argument §5.1 makes and then does not show.

That is a structural change rather than a sentence-level one, so it is on the
deferred list as **S15** rather than drafted here. Say the word and I will draft
the table.

---

# F15 - Metacomment, table names, and the outstanding-decisions block {#f15}

Six comments tag `METACOMMENT` and six tag `NAMING`. They are one problem in two
forms: the chapter talks about its own drafting history.

## 15a - The Outstanding decisions section must go

### Anchor

**The section headed "Outstanding decisions"**, at the end of the chapter.

First five words: *"Resolved since this list was..."*
Last five words: *"...a result or a deferred option"*

### Action

DELETE the entire section.

Every line in it fails the test of whether a reader who has never seen a previous
version would understand it. *"Resolved since this list was written"*, *"Closed
2026-08-25"*, *"HPO trial budget: 50 trials, may reduce under RAM pressure"* -
these are project-management artefacts.

**Two of its three genuinely-open items are real limitations** and belong in
§5.5.8 as prose rather than as a to-do list:

> Two limitations of the benchmark set remain. The ARIMA specification is fixed
> at SARIMAX(1,1,1) rather than searched per series, on cost grounds, so its
> figures are a competent floor for that family rather than its best attainable
> performance and the baseline comparison is correspondingly conservative. And
> the ensemble combination that the M4 evidence motivates is evaluated as a
> separate scenario rather than folded into this chapter's selection, so no claim
> about combination accuracy is made here.

The third, *"Which metric the ≤15% benchmark refers to"*, is already answered in
§5.4.3 and needs no second home.

## 15b - The meta line at the top of 5.5

### Anchor

**Section 5.5 Results.** The opening paragraph.

First five words: *"All results are on the..."*
Last five words: *"...appear in this chapter."*

### Action

REWORD. A plan identifier in thesis prose names an internal artefact.

**Before:**

> All results are on the locked brand × month grain (DEC-GRAIN). The alternative
> brand × chain representation, and the granularity comparison built on it, were
> removed from the project by P0035 and no longer appear in this chapter.

**After:**

> All results are reported on the brand-by-month grain. The chain and regional
> representations were evaluated during development and are reported as a
> limitation and as future work rather than as a live dimension of the
> comparison.

## 15c - Table captions

Five captions are placeholders or carry typos. F2, F4, F5, F6, F8 and F10 each
give a replacement caption in full. The two worst:

| Current | Replacement |
|---|---|
| **"Table 7 - NO IDEA"** | *Table 7 - The Syntetos-Boylan-Croston demand-pattern quadrants* |
| **"Table 13 - Seed Stabiltiy across Models and Categories"** | given in F8 |

**Table 7 is comment 240**, tagged `NAMING`, and it is the one an examiner would
notice first.

## 15d - The two stability paragraphs tagged WATERMARK

Comments 279 and 283 tag `WATERMARK, ACADEMIC` on *"Two findings, and both matter
more than the accuracy tables suggest"* and *"Every input is identical; only the
random seed differs."*

**Both read as written by someone arguing with a previous draft** rather than
reporting a result. The first asserts its own importance; the second is a
rhetorical flourish placed before a conclusion.

**Reword the first to:**

> Two findings follow, and both bear on how the accuracy tables in this chapter
> should be read.

**And the second:**

> Because every input other than the seed is held identical, a statement of which
> gradient-boosting model is best in a given category reports the outcome of one
> seed rather than a property of the models. §5.6 states the conclusion this
> supports instead.

⚠ **The second depends on F8's unresolved winner-flip table.** If that claim
cannot be supported, this paragraph and §5.6 both change. Do not paste it until
H11 is settled.

---

# Blocked

**One item, and it is load-bearing.**

## The winner-flip claim has no artefact

Section 5.5.9's per-seed winner table, and the whole of §5.6, rest on the claim
that the winning model changes with the seed in all four categories.

`10_seed_stability.csv` does not contain per-seed winners, only per-model
aggregates, and those aggregates say **LightGBM has the lower mean weighted error
in all four categories**, by between 0.1 and 3.2 points.

The flip may well be real. Five seeds with standard deviations of 0.4 to 1.9
points, against between-model gaps of 0.1 to 3.2, would produce flips in at least
the close categories. But the chapter cannot cite what is not on disk.

**What would answer it:** the per-seed WMAPE values the stability run produced
before aggregation, either retained by `srq1_stability.py` or re-derivable from
its raw output.

**If it does not hold**, §5.6's central claim has a weaker but still sound
replacement: a between-seed standard deviation of 0.4 to 1.9 points against a
between-model gap of 0.1 to 3.2 puts the difference inside noise for CSD,
danskvand and energidrikke, and outside it only for RTD. That supports "choose on
operational grounds for three of four categories" rather than "the two are
indistinguishable everywhere".

**Tracked as H11 in `post-hpc-validation.md`, marked as a gate.**

---

# Comment verdicts

All 49 threads, in document order. Forty-one are bare tags with no text, so the
verdict is against the tagged passage.

| # | Section | Verdict |
|---|---|---|
| 199 | chapter title | **NEEDS-BRIAN** - a subtitle is your call. *Benchmarking the Forecasting Substrate* would match Ch4's form |
| 201 | 5.1 | **ADDRESSED** - F14a. Both sources verified in Zotero |
| 204 | 5.2.1 | **VERIFIED-OK** - the four definitions match Hyndman & Athanasopoulos §5.2. Prose conversion is S15 |
| 207 | 5.2.2 | **VERIFIED-OK** - SARIMAX(1,1,1) confirmed in `srq1_baselines_stat.py` |
| 209 | 5.2.3 | **VERIFIED-OK** - Prophet is configured with yearly seasonality only and no holiday calendar, exactly as described |
| 211 | 5.2.4 | **ADDRESSED** - F1 fixes the §6.3.4 reference; F9 corrects the RAM figure |
| 213 | 5.2.5 | **ADDRESSED** - F9. The 0.2 MB figure is 29.2 MB resident |
| 215 | 5.2.6 | **ADDRESSED** - F9. Hastie et al. verified, pages 61-62 as cited |
| 218 | 5.3.1 | **VERIFIED-OK** - all four test-set sizes match `metrics.csv` exactly |
| 220 | 5.3.2 | **ADDRESSED** - F11. This was the largest factual error in the chapter |
| 222 | 5.3.3 | **ADDRESSED** - F14b |
| 225 | 5.3.4 | **VERIFIED-OK** - tagged `OUTDATED`, but the protocol described matches the code. See the note below |
| 227 | 5.3.5 | **ADDRESSED** - F13. Bergstra and Akiba both verified |
| 229 | 5.4 | **VERIFIED-OK** - metric definitions correct; Hyndman & Koehler verified at p. 683 |
| 231 | 5.4.1 | **ADDRESSED** - see the note below on the 8-13pp claim. Gneiting verified at pp. 746 and 752 |
| 233 | 5.4.2 | **ADDRESSED** - F15c for the caption. The 14-29% zero-actual range is confirmed: `mase.csv` gives 71.4% to 86.2% scorable, so 13.8% to 28.6% zero |
| 236 | 5.4.3 | **VERIFIED-OK** - the withdrawal of the 15% target is correct and well stated. F10 adds the calibration miss |
| 238 | 5.4.4 | **ADDRESSED** - F7. Syntetos, Boylan & Croston verified at p. 495 |
| 240 | 5.4.4 | **ADDRESSED** - F15c, "Table 7 - NO IDEA" |
| 243 | 5.5 | **ADDRESSED** - F15b |
| 245 | 5.5.1 | **ADDRESSED** - F2. Also delete the trailing `cv_metrics.csv.` - a filename is not a sentence |
| 247 | 5.5.1 | **ADDRESSED** - F2 |
| 248 | 5.5.1 | **ADDRESSED** - F3 part A |
| 249 | 5.5.1 | **ADDRESSED** - F3 part B. Cawley & Talbot verified |
| 251 | 5.5.2 | **ADDRESSED** - F1 for the §6.2.0 reference; delete the trailing `stat_baselines.csv.` |
| 253 | 5.5.2 | **ADDRESSED** - F4. Your question about "Best tuned ML" was right; the column now names its model |
| 254 | 5.5.2 | **ADDRESSED** - F4 part C. The claim inverts on danskvand |
| 255 | 5.5.2 | **ADDRESSED** - F4. Taylor & Letham verified |
| 257 | 5.5.3 | **ADDRESSED** - F5 |
| 259 | 5.5.3 | **ADDRESSED** - F5 caption |
| 260 | 5.5.3 | **ADDRESSED** - F5. The 6.54 and 0.18 become 11.80 and 0.28 |
| 262 | 5.5.4 | **ADDRESSED** - F6; delete the trailing `pooled_summary.md.` |
| 263 | 5.5.4 | **ADDRESSED** - F6 |
| 265 | 5.5.4 | **ADDRESSED** - F6 caption |
| 266 | 5.5.4 | **ADDRESSED** - F6. The both-families claim needed narrowing |
| 267 | 5.5.4 | **ADDRESSED** - F6. The 44-64% becomes 31-57% |
| 269 | 5.5.5 | **ADDRESSED** - F7, counts corrected |
| 271 | 5.5.6 | **ADDRESSED** - F9. Every figure was wrong |
| 273 | 5.5.7 | **ADDRESSED** - F10. Lei et al. verified; the finite-sample quantile is Algorithm 2 as cited |
| 274 | 5.5.7 | **ADDRESSED** - F10. The width claim was attached to the wrong category |
| 276 | 5.5.8 | **ADDRESSED** - F12 |
| 278 | 5.5.9 | **ADDRESSED** - F8 |
| 279 | 5.5.9 | **ADDRESSED** - F15d |
| 280 | 5.5.9 | **ADDRESSED** - F8. The p90 clause has no source in the current artefact |
| 282 | 5.5.9 | **FLAGGED** - F8, blocked on H11 |
| 283 | 5.5.9 | **ADDRESSED** - F15d, conditional on H11 |
| 285 | 5.6 | **FLAGGED** - blocked on H11 |
| 288 | 5.7 | **ADDRESSED** - see the note below |
| 289 | Outstanding decisions | **ADDRESSED** - F15a, delete the section |

### Note - comment 225, tagged OUTDATED, is not outdated

Section 5.3.4 describes expanding-window cross-validation splitting on distinct
periods rather than rows. **That is what the code does**, and the Tashman
citation supports it at the page given.

My reading is that the tag refers either to the `§6.3.4` reference inside it,
which F1 fixes, or to the horizon question - the validation scheme predates the
H=3 correction, which has since landed. **Both are now resolved.** If you meant
something else, tell me and I will look again.

### Note - comment 288, section 5.7

The SRQ table's first column reads *"How Ch.6 addresses it"*, which F1 fixes. But
two rows are also wrong on substance:

- **SRQ3** says *"integration readiness is addressed in Ch3 and Ch5"*. Chapter 5
  is this chapter, which does not address it. It should name Chapter 6 and
  Chapter 7.
- **SRQ1** says *"within ≤4GB RAM"*, which is right, and is worth keeping
  precisely because §5.5.6 currently contradicts it.

**Replacement caption:** *Table 15 - How the model benchmark contributes to each
sub-research question*

### Note - comment 231 and the 8-13pp claim

Section 5.4.1 says tuning against median APE *"costs 8-13 pp of WMAPE while
buying only 2-3 pp of median APE"*.

**Measured now: it costs between -2.9 and +9.3 points of weighted error, and buys
between -8.3 and +5.1 points of median error. In three of eight configurations it
makes both metrics worse.**

**Reword to:**

> Tuning against median absolute percentage error costs up to 9.3 percentage
> points of weighted error while buying at most 8.3 points of the metric it
> optimises, and in three of the eight configurations tested it worsens both.

That is a weaker claim and a more honest one. It is also consistent with the
functional argument rather than against it: a forecast targeting a lower
functional is not a better estimate of anything the evaluation measures, so there
is no reason to expect a clean trade.

---

# Citations

**Every source cited in Chapter 5 resolves against the 2026-09-10 pull, 87
items:** Hyndman & Athanasopoulos, Makridakis et al., Taylor & Letham, Gneiting,
Hyndman & Koehler, Tashman, Bergstra et al., Akiba et al., Syntetos Boylan &
Croston, Hastie et al., Cawley & Talbot, Lei et al., and Klee & Xia.

**No new citations are added by this pass**, so there is nothing to register.

⚠ **Two entries have metadata defects that will render wrong in the
bibliography:**

| Entry | Defect |
|---|---|
| Hyndman & Athanasopoulos | stored under the section title *"5.2 Some simple forecasting methods"* with **no year**, so it renders as "n.d." |
| Akiba et al. | the year field reads **"July"** rather than 2019 |

Both are fixed in Zotero rather than in Word, since the bibliography is generated
from the library. Tracked as **S16** on the deferred list.

⚠ **One more, from Table 10's internal note:** *"Taylor & Letham (2018) is
MISSING from the Ch2 reference list."* The entry is in Zotero and cited here, so
the reference list will resolve it. The note is about Chapter 2's coverage, which
is a Chapter 2 question.

---

# What this pass did not touch

On the deferred structural list rather than decided here:

- **S13** - adding a caption to the calibration table renumbers every later table
- **S14** - `fig4_ram_budget` is stale and contradicts §5.5.6
- **S15** - whether 5.2.2 to 5.2.6 become a comparison table or five paragraphs
- **S16** - the two Zotero metadata defects
- **S9** - the cross-chapter repetition pass, still open from Chapter 4

On the post-run validation list:

- **H11** - the per-seed winner data. **A gate** for §5.5.9 and §5.6
- **H12** - re-profile the operational figures on 18 features
