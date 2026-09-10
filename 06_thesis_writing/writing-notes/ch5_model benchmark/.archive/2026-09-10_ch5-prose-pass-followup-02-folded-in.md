---
name: ch5-prose-pass-followup-02
description: NOTE - I read the wrong stability artefact. stability.md holds the per-seed winner table, the p90 column and a computed aggregate-vs-individual figure. F8 of the pass and F1/F2 of follow-up 01 are all corrected here.
snapshot: 2026-09-10_16-43_ch5-prose-work
category: workflow
applies-to: [chapter 5]
supersedes: [ch5-prose-pass.md F8, ch5-prose-pass-followup-01.md F1, ch5-prose-pass-followup-01.md F2]
created: 2026_09_10-17_15
updated: 2026_09_10-17_15
status: ready
---

# Chapter 5 - follow-up 02

**Read this before applying anything about section 5.5.9.**

Verified at `ebdb5f7`, snapshot `2026-09-10_16-43_ch5-prose-work`, Zotero 87
items. Chapter 5's prose is byte-identical to the pass snapshot, so every anchor
still holds.

---

# ⚠ I read the wrong file, and the pass is wrong because of it

The main pass said section 5.5.9's per-seed winner table was *"not reproducible
from the published artefacts"*, blocked it as gate H11, and warned that section
5.6 rested on a claim with no evidence.

**That was my error.** I searched `10_seed_stability.csv`, found only per-model
aggregates, and concluded the data did not exist. It does. It is in
`05_model_benchmark/tables/stability.md`, which I never opened.

That file carries **all three** things the pass said were missing:

| The pass said | `stability.md` has |
|---|---|
| no per-seed winner data | the winner-per-seed table, all four categories, verdict **FLIPS** in each |
| the p90 column is gone | `p90 CV`, a full column |
| no source for the aggregate-vs-individual gap | a computed sentence: ~4.6% against ~17%, about 3.6x |

**The chapter's claim was right all along.** Four of four categories change their
winning model on the seed alone. Section 5.6 needs no rewrite.

**Follow-up 01's F2 reached the right conclusion by the wrong route.** It argued
indistinguishability from mean-versus-standard-deviation arithmetic because it
thought the winner data was gone. The argument is sound, but it is second-best
evidence, and the direct table is better. **Use F1 below, not follow-up 01's F2.**

## What this supersedes

| Block | Status |
|---|---|
| Main pass, **F8** | **dead.** Its table, its p90 recommendation and its H11 gate are all superseded |
| Follow-up 01, **F1** | **dead.** Its table was right; its aggregate-vs-individual sentence was my own derivation, not the computed one |
| Follow-up 01, **F2** | **dead.** Right conclusion, weaker evidence. Replaced by F1 below |
| Follow-up 01, **F3** | **stands.** The two Prophet figures are unaffected |
| Everything else in the main pass | **stands** |

---

# F1 - Section 5.5.9, rebuilt on the right artefact {#f1}

Source: `05_model_benchmark/tables/stability.md` and `stability.csv`, regenerated
2026-09-10 at `471b5a3` on the 18-feature run.

## 1a - The stability table

### Anchor

**Section 5.5.9 Forecast stability across seeds.** The eight-row table above the
caption **"Table 13 - Seed Stabiltiy across Models and Categories"** - the one
beginning *"CSD | LightGBM | 0.112"*.

### Action

REPLACE the table and caption. **The p90 column comes back** - the pass was wrong
to drop it.

**Replace with:**

| Category | Model | Median CV | p90 CV | WMAPE mean | WMAPE sd | WMAPE range |
|---|---|---|---|---|---|---|
| CSD | LightGBM | 0.182 | 0.488 | 18.9% | 0.67 | 18.3-20.0% |
| CSD | XGBoost | 0.152 | 0.517 | 18.6% | 0.83 | 17.8-19.5% |
| danskvand | LightGBM | 0.138 | 0.522 | 27.0% | 2.81 | 24.6-31.9% |
| danskvand | XGBoost | 0.174 | 0.611 | 25.8% | 1.04 | 24.7-27.0% |
| energidrikke | LightGBM | 0.239 | 0.707 | 16.2% | 0.59 | 15.5-16.9% |
| energidrikke | XGBoost | 0.243 | 0.773 | 17.0% | 1.08 | 15.5-18.0% |
| RTD | LightGBM | 0.099 | 0.236 | 30.5% | 0.30 | 30.2-30.9% |
| RTD | XGBoost | 0.114 | 0.522 | 30.1% | 1.04 | 29.1-31.6% |

**Caption:** *Table 13 - Forecast and accuracy variation across five random
seeds, by category and model*

### Note - the WMAPE range column is worth keeping

It is not in the chapter now and it is the most legible column in the table. A
reader who does not think in standard deviations can see that danskvand's
LightGBM lands anywhere between 24.6 and 31.9 per cent depending on the seed,
which is the whole argument in one cell.

## 1b - The first finding, with the computed figure

### Anchor

**Section 5.5.9.** The paragraph beginning **"First, aggregate stability flatters
the system by roughly three times."**

First five words: *"First, aggregate stability flatters the..."*
Last five words: *"...would understate instability threefold."*

### Action

REPLACE.

⚠ **Use this wording, not follow-up 01's.** These figures are computed by the
generator from `stability.csv` at render time. The ones I gave in follow-up 01
were my own arithmetic off the aggregates, which is exactly the transcription the
provenance rule exists to stop.

**Replace with:**

> First, aggregate stability flatters the system by roughly a factor of four.
> Aggregate weighted error moves by about 4.6 per cent of its own level across
> seeds, while the typical individual forecast moves by about 17 per cent, and
> the ninetieth-percentile cell by between 24 and 77 per cent. Per-cell movements
> partly cancel within a volume-weighted sum, so a planner reading one brand's
> number experiences considerably more run-to-run variability than a headline
> metric implies. Both are therefore reported; quoting only the aggregate would
> understate instability roughly fourfold.

### Note - the chapter's "three times" was measured on an older run

The chapter says 4.7 per cent against 13 per cent, roughly threefold. The
regenerated figures are 4.6 against 17, about 3.6x, which the source file rounds
to fourfold. The direction and the argument are unchanged; only the multiplier
moved, and it moved **against** the system, so the finding is slightly stronger
than the chapter currently claims.

## 1c - The winner-flip table stays, and gains a verdict column

### Anchor

**Section 5.5.9.** The second table, listing the winner per seed, beginning
*"CSD | XGBoost, XGBoost, LightGBM..."*.

### Action

REPLACE. ⚠ **Do not delete this table** - follow-up 01 told you to, and that was
wrong.

**Replace with:**

| Category | Winner per seed | Verdict |
|---|---|---|
| CSD | XGBoost, XGBoost, XGBoost, LightGBM, LightGBM | flips |
| danskvand | LightGBM, LightGBM, XGBoost, XGBoost, XGBoost | flips |
| energidrikke | XGBoost, LightGBM, LightGBM, LightGBM, XGBoost | flips |
| RTD | XGBoost, LightGBM, XGBoost, XGBoost, XGBoost | flips |

**Caption:** *Table 14 - The selected model per category under each of five
random seeds*

### Note - the per-seed orderings changed, so do not keep the old rows

Every row differs from what the chapter currently prints. The verdict is
identical in all four categories, which is why the surrounding prose survives -
but the sequences themselves are from the superseded run and must be replaced,
not left.

## 1d - The paragraph after it

### Anchor

**Section 5.5.9.** The paragraph beginning **"Every input is identical; only the
random seed differs."**

### Action

REPLACE. This also answers comments 279 and 283, tagged `WATERMARK, ACADEMIC`.

**Replace with:**

> Because every input other than the seed is held identical, the selected model
> is not a property of the categories but an outcome of one draw. A statement
> that a particular gradient-boosting model is best for a given category is
> therefore unsupported here, in all four categories. §5.6 states the conclusion
> this supports instead.

---

# F2 - Section 5.6 needs no rewrite {#f2}

**The main pass flagged this section as blocked and follow-up 01 proposed
replacing its central claim. Neither is necessary.**

Section 5.6 currently says the winning model changes with the seed in all four
categories, and that the two models are statistically indistinguishable with the
between-seed spread exceeding the between-model difference.

**Both statements are correct and both are now sourced.** `stability.md` states
the same conclusion in its own words, independently of this chapter.

### The only edit section 5.6 needs

Its cross-reference. **F1 of the main pass covers it:** *"(§6.5.7)"* becomes
*"(§5.5.9)"*.

### Note - one sentence could be strengthened

§5.6 says the two models are indistinguishable. The seed table now lets it say
how far apart they would have to be before the claim changed:

> The between-model difference in mean weighted error ranges from 0.3 to 1.2
> percentage points across the four categories, against a between-seed standard
> deviation reaching 2.8. The difference between the two models is smaller than
> the variation either produces on its own.

**Optional.** The existing sentence is already true and already sourced.

---

# The registers

- **H11 is closed as an error on my part**, not as a finding. The data was never
  missing; I looked in one file and did not look in the other. Recorded that way
  in `post-hpc-validation.md` rather than deleted, because the failure mode is
  worth keeping: an artefact that does not answer a question is not evidence that
  nothing does.
- **H12 stands.** `profiling.csv` still reports 13 features, so the operational
  figures in §5.5.6 are still a floor.

---

# What I should have done

The pass read `10_seed_stability.csv`, which is the **appendix export** of the
stability run. `stability.md` and `stability.csv` are the **source artefacts**,
and they carry more: the per-seed winners, the p90 column, the WMAPE range, and
prose figures computed at render time.

**An appendix table is a projection of a result, not the result.** When a
projection does not answer a question, the answer is to find the source, not to
declare the question unanswerable. I did the latter and wrote a gate around it.
