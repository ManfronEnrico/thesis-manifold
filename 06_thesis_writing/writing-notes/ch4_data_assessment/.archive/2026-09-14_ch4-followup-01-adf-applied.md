---
name: 2026-09-14_BRANCH_A_ch4-followup-01-adf-uniform-differencing
description: FOLLOW-UP - The uniform-differencing sentence proposed by the appendix session, corrected against the per-brand ADF tables. The proposed "a minority reject" is 34 to 37 per cent, and the strongest available fact was omitted.
category: workflow
applies-to: [ch4_data_assessment]
triggers: [ch4 prose pass, defending uniform differencing, appendix cross-reference]
created: 2026_09_14-12_40
updated: 2026_09_14-12_40
snapshot: 2026-09-14_11-55_ch9-followup-defence-and-anchoring
status: prose ready to paste, awaiting human review
---

# Chapter 4 — follow-up 01, the uniform-differencing sentence

Verified at `41ecb76`, fetch clean. Snapshot
`2026-09-14_11-55_ch9-followup-defence-and-anchoring`. Counts computed
2026-09-14 from the four per-brand ADF tables.

**Everything in the consolidated pass stands.** All four fixes are applied and
verified in this snapshot. This follow-up answers a proposal that arrived from
the appendix generation session.

---

# The proposal, and the verdict

**The instinct is right and the sentence should go in.** Chapter 4 currently
says the aggregate series is difference-stationary and that differencing is the
conventional treatment, and it never says that the treatment is applied to every
brand regardless of that brand's own test. A reader who opens the per-brand
appendix table finds brands being differenced that reject the unit root, with no
explanation. Closing that is worth three sentences.

**The wording needs three corrections before it can be pasted.**

## ⚠ 1. "A minority reject the unit root in level" is not supported

Measured across all four `step_2_05_adf_per_brand.csv` tables, 79 brands:

| | Rejecting at p < 0.05 | Share |
|---|---|---|
| raw level (`p_raw`) | 27 / 79 | **34.2%** |
| log level (`p_log`) | 29 / 79 | **36.7%** |
| either | 40 / 79 | **50.6%** |
| both | 16 / 79 | 20.3% |

Per category the log-level figures are CSD 8/20, Danskvand 7/20, Energidrikke
7/20, RTD 7/19 — **strikingly uniform at around 35 to 40 per cent.**

"A minority" reads as *a handful*. A reader who checks finds a third, and on the
"either" reading a half. **A soft quantifier that the appendix contradicts costs
more than it saves.**

## ⚠ 2. "In level" is ambiguous, and the two columns disagree per brand

`p_raw` and `p_log` are different tests and they disagree case by case — COCA
COLA is 0.061 raw against 0.000 log; FIRST PRICE is 0.000 raw against 0.744 log.

The baselines difference the **log** series, so `p_log` is the column the
sentence is about. Say so, or the claim cannot be checked.

## ⚠ 3. The low-power argument does not transfer cleanly from the transform

In the transform paragraph the objection is now that **per-brand estimation is
not supportable** — because the alternative there (Guerrero) is an *estimator*,
which is exactly why the consolidated pass reworded it away from "tests have
limited power".

Here the alternative genuinely **is** a per-brand hypothesis test, so low power
is the correct objection. But the rendered appendix table already states it in
its own preamble: *"a non-rejection should be read as inconclusive rather than
as evidence of a unit root."*

**Repeating it in the chapter makes one argument look like it is being reused to
cover two different decisions.** Lead with the design reason instead.

## ✅ And the strongest fact was left out

**Differencing fails to deliver stationarity for 13 of 79 brands** (`p_diff` ≥
0.05). That is a measured, countable cost of the uniform rule.

Stating it is much better evidence of rigour than any hedge about power: it
shows the chapter knows what its own convenience costs and reports it anyway.

---

# The fix

## F1 — 4.2.2, the uniform-differencing treatment

### Anchor

**Section 4.2.2.** The paragraph beginning *"On the aggregate monthly series, the
category level is non-stationary in both raw and logarithmic form"*.

It ends: *"...which is the conventional treatment for a series carrying a unit
root (Hyndman & Athanasopoulos, 2021), and by lagged and rolling features for the
tree models, which do not require a stationary level. Non-positive and missing
values are preserved as missing rather than imputed."*

### Action

INSERT AFTER — one new paragraph, after that paragraph and before the **4.2.3
Seasonality** heading.

#### Replace with

> That treatment is applied uniformly across brands rather than selected per
> series, and the per-brand tests show what the uniformity costs. Of the brands
> tested in each category, between a third and two-fifths reject the unit root
> in logarithmic level and are therefore differenced without needing to be,
> while differencing fails to deliver a stationary series for thirteen of the
> seventy-nine brands tested. Neither outcome is treated as grounds for a
> per-brand rule. A differencing rule applied unevenly would make the baselines
> incomparable across a panel whose comparability is the point of the exercise,
> and the per-brand test that would drive such a rule has low power at
> forty-odd observations, so acting on it selectively would fit sampling noise
> into the specification. The cost is accepted deliberately, and the per-brand
> results are reported in full in Appendix [N] rather than summarised away.

### Note — what changed from the proposal, and why

| Proposal | This version | Why |
|---|---|---|
| "a minority reject" | "between a third and two-fifths" | 34–37% measured. The appendix would contradict "a minority" |
| "the unit root in level" | "in logarithmic level" | `p_raw` and `p_log` disagree per brand; the baselines fit the log series |
| low power leads the argument | comparability leads, power second | the design reason is the real reason; power is a supporting point |
| — | **"fails for thirteen of seventy-nine"** | the strongest fact available, and it was missing |
| "at forty-six observations" | "at forty-odd observations" | 46 is CSD only. The four panels run 41–46, and the pooled claim spans all four |

⚠ **"Forty-six" would be wrong here.** The transform paragraph can say forty-six
because it discusses CSD. This sentence pools all four categories, whose panels
are 46, 43, 41 and 41 months. **Do not copy the number across from the paragraph
above.**

### Note — the appendix reference

`[N]` must be filled once the appendix numbering is settled. The table is
`step_2_05_adf_per_brand` and it exists for all four categories, so the
reference is to **the per-brand ADF section**, not to a single table.

⚠ **Check before pasting whether that appendix section actually ships.** The
sentence promises the per-brand results "in full", and it must not point at
something that was cut. If only CSD's table is included, the sentence needs to
say so or the promise is false.

---

# Provenance

✅ **Every figure here is regenerable**, which is the property the calibration
table in Chapter 5 lacks.

| | |
|---|---|
| Producer | `step_2_eda_descriptive.py:567`, `ctx.save(adf_df, "step_2_05_adf_per_brand", ...)` |
| Artefacts | `05_thesis_results/04_data_assessment/eda/{CSD,Danskvand,Energidrikke,RTD}/tables/step_2_05_adf_per_brand.md` |
| Written | 2026-09-10 18:13–18:14, all four |
| Rows | 20 + 20 + 20 + 19 = **79** |

⚠ **The tables cover the top brands by volume, not every brand.** The heading
says *"ADF Test per Brand (top brands by volume)"* and each category caps at
twenty. So the 79 is **79 tested brands**, not the whole panel — which carries
95, 44, 29 and 62 retained brands respectively.

**The prose above says "the brands tested in each category" and "the
seventy-nine brands tested" deliberately.** Do not let that become "of all
brands" in a later edit; it would be false.

⚠ **These tables predate the 2026-09-09 retraining by a day and were written
2026-09-10.** They are descriptive EDA over the panel rather than model output,
so retraining does not invalidate them — but if the panel itself is ever
rebuilt, this paragraph's counts move with it.

---

# Citations register

**No new citation.** The paragraph cites nothing the chapter does not already
cite: Hyndman & Athanasopoulos (2021) appears in the preceding sentence, and the
Dickey-Fuller reference lives in the appendix table's own preamble.
