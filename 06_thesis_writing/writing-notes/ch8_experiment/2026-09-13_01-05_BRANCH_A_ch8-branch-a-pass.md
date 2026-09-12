---
name: 2026-09-13_01-05_BRANCH_A_ch8-branch-a-pass
description: NOTE - Chapter 8 rebuilt from scratch against BRANCH A, the 63-run funded set. The three-level framework is replaced by the seven-arm ladder. Every number in the existing chapter is wrong; this note supplies a complete replacement, section by section.
category: workflow
applies-to: [chapter 8]
snapshot: 2026-09-12_22-28_ch7-post-merge
branch: A (fallback) — commit 58243f3, schema v6-shared-composition+af04a42a478b
created: 2026_09_13-01_05
updated: 2026_09_13-01_05
status: open
---

# Chapter 8 — BRANCH A pass

Written against **Branch A**, the funded 63-run set, as if it is final.

**Snapshot `2026-09-12_22-28_ch7-post-merge`.** Repository at `58243f3`, pushed.
Chapter 8 is **1,384 words** and is the original bullet-point draft: it has never
been revised. **All anchors verified verbatim against the snapshot.**

⚠ **This is a rewrite, not a pass.** Nine of the chapter's twelve sections are
replaced outright. Reading it as a list of fixes will not work; read it as the
new chapter, with the old one shown only at the anchors.

---

# The decision that shapes everything below

**The three-level evaluation framework is replaced by the seven-arm ladder.**
Approved by Brian, 2026-09-13.

The framework organises the chapter as ML accuracy, then recommendation quality,
then agent behaviour. Its middle level rests entirely on a **GPT-4o judge study
that was never run in the form described**, and its outer levels duplicate
material that Chapters 5 and 7 now own. The ladder is what Chapters 1 to 7 build
toward and what the 63 funded runs actually measured.

```
A_llm_plain → B_llm_data → C_llm_model → F_llm_data_model        (hosted)
D_prometheus_data → E_prometheus_model → G_prometheus_data_model (production)
```

**A→B measures what data access buys. B→C measures what the trained model adds,
and that is the thesis contribution. C→F measures what returning code on top
adds.** D, E and G repeat the three rungs on the production orchestrator so the
ladders compare rung for rung.

---

# Provenance of every figure in this note

| Artefact | Written | Used for |
|---|---|---|
| `08_experimental_evaluation/runs.csv`, **v6 rows only** | 2026-09-12 21:06 | every accuracy, cost, latency and stability figure |
| `raw_responses/*.json`, 63 funded traces | 2026-09-12 | the reliability check, the deviation flags, quoted answers |
| `tables/tuned_metrics.csv` | 2026-09-09 21:10 | the SRQ1 test WMAPE figures |
| `tables/stat_baselines.csv` | 2026-09-09 21:10 | the classical baselines |
| `models/index.json` | 2026-09-09 21:10 | which model each category serves |
| account balance, two movements | 2026-09-12 | the **$19.60** actual cost |

⚠ **Three figures must never be transcribed from `summary.md`:**

| Do not use | Use instead | Why |
|---|---|---|
| "63 rows in `runs.csv`" | **69 rows; filter `schema.str.startswith('v6')`** | six superseded `v2` rows remain |
| "Actually billed: $18.4647" | **$19.60** | that is one billing window; the spend came in two movements |
| `cost_usd_est` as cost | estimate **×0.78**, or ~$0.31/run | the estimator overshoots by 29% |

---

# The fixes

## Fix 1 — The chapter needs a subtitle, and the ladder names it

Comment 322 (Brian, FORMATTING): *"Could use a subtitle for the chapter"*.

### Anchor

Immediately under the chapter title:

> "COULD USE A SUBTITLE"

### Action

REPLACE.

#### Replace with

> Seven scenarios on a shared question, and what each rung of the ladder buys

---

## Fix 2 — 8.1 replaces the three-level framework with the ladder

### Anchor

**Section 8.1 Evaluation overview**, the whole section, from:

> "Three-level evaluation framework (3-level is the thesis's core methodological
> contribution to evaluation design for AI artefacts):"

through to:

> "Cite: AI-Based DSR Framework 2024 (evaluation dimensions for AI artefacts);
> Pathways for Design Research on AI 2024 (INFORMS ISR)"

### Action

REPLACE the entire section body.

#### Replace with

> The preceding chapters specify an artefact and argue for it on design grounds.
> This chapter asks whether the argument survives measurement. The question it
> puts is narrow and deliberately so: given the same forecasting task, does
> routing the forecast through a dedicated model reached by a structured
> interface produce a better answer than letting a language model write its own
> forecasting code, and at what cost.
>
> A two-way comparison cannot answer that, because it confounds two different
> things: the value of giving an agent access to the firm's data at all, and the
> value of giving it a trained model rather than a code sandbox. The evaluation
> is therefore built as a ladder of seven scenarios, each adding one capability
> to the one below it, so that the increments can be attributed separately.
> Every scenario is asked the identical question about the identical brands over
> the identical period, and differs only in what it is given to answer with.
>
> Four scenarios run on a hosted language model. The first is given no firm data
> at all. The second receives the brand's sales history and an execution
> environment in which it may write and run its own analysis. The third receives
> the same history behind the structured forecast tool and writes no code. The
> fourth receives both. Three further scenarios repeat the second, third and
> fourth rungs on the production agentic platform, so that each rung can be read
> across the two orchestrators as well as up the ladder.
>
> Read upward, the first step measures what access to the firm's own data buys.
> The second measures what replacing self-written analysis with a dedicated model
> adds, and that increment is the thesis contribution. The third measures what
> returning the code environment on top of the model adds. Read across, the
> paired rungs isolate the orchestrator from the capability.
>
> Outcomes are classified before they are averaged. A scenario that answers six
> of nine questions is not comparable to one that answers nine of nine on
> accuracy alone, and a failure rate says more about production readiness than a
> small difference in error does. Accuracy, stability across repeated runs, cost
> and latency are reported together throughout, because no scenario leads on all
> four and the shape of that disagreement is the finding.

---

## Fix 3 — 8.2 becomes the experimental design, replacing the benchmark-design bullets

Sections 8.2.1 to 8.2.3 describe a benchmark that Chapter 5 now owns, in a grain
the thesis does not use. ⚠ **`[N] SKUs × 28 retailers × [T] weeks` is wrong three
times over**: the panel is monthly, not weekly; the grain is brand-month, not
SKU-by-retailer; and the placeholders were never filled.

### Anchor

**Section 8.2 Level 1 - ML accuracy evaluation (SRQ1)**, from the heading
**"8.2.1 Benchmark design"** through the end of 8.2.3, ending:

> "Manifold descriptive baseline: descriptive analytics output from current
> Manifold AI tool (SRQ4 - requires access to baseline outputs)"

### Action

REPLACE all three subsections with one design section.

#### Replace with

> ### 8.2 Experimental design
>
> The evaluation is run on the carbonated soft drinks category, on three brands,
> with three repeated runs of every scenario for every brand: sixty-three runs in
> total. Each run asks for a single month's unit sales for one brand, forecast
> from the brand's history up to the end of the preceding period, and is scored
> against the realised figure for that month.
>
> The three brands are chosen by volume stratification from the qualifying
> population, taking the largest, the median and the smallest. They span three
> orders of magnitude of monthly sales, from roughly 2,850 units to roughly 6.4
> million. The stratification matters because a comparison run only on
> data-rich brands would flatter a trained model, and one run only on thin
> series would measure rounding rather than forecasting.
>
> Three inclusion criteria define the population the brands are drawn from, all
> applied before any run and identically to every scenario. A brand must have at
> least as many held-out months as the forecast horizon, or there is no month to
> score. It must have no zero months in the held-out window, because percentage
> error divides by the actual and a zero makes the score undefined rather than
> merely difficult. And the scored month must record at least a thousand units.
>
> The third criterion is a property of the measurement rather than of the
> method. Below roughly that volume, percentage error is dominated by integer
> rounding: on a nine-unit series a single unit of error registers as eleven per
> cent, which exceeds the differences the experiment is designed to detect.
> Fourteen of the category's qualifying brands sell fewer than a hundred units
> in the scored month, so the low end of the category is a cliff rather than a
> gradient. Excluding that region is not an exclusion of hard cases but of the
> region where the chosen metric stops discriminating, and it is applied to
> every scenario equally.
>
> Every scenario receives the identical user question. An earlier design gave
> each scenario differently worded instructions, so any difference in outcome
> would have partly measured the wording rather than the capability under test.
> The capability notes that distinguish the scenarios are composed from shared
> blocks rather than written individually, and an automated check renders all
> seven and asserts that paired scenarios are byte-identical wherever they
> should be. The full prompt set is given in the appendix and its identity is
> recorded as a hash, so that no prompt can be altered without the recorded run
> identity changing with it.

### Note — the prompt-consistency correction should be owned, not hidden

⚠ An audit before the funded run found that the capability notes **had** drifted:
one scenario was instructed to produce a prediction interval while its paired
scenario was not, and both were scored on interval communication. The correction
landed **before any funded money was spent**, so no reported result rests on the
defective instrument.

**Say so, in the methods voice, in two sentences.** A thesis that reports a
control it found imperfect, says how it was detected and shows it was fixed
before measurement, is more credible than one that asserts the control held. Do
not bury it in limitations and do not write it as an apology. Suggested placement:
after the paragraph above beginning "Every scenario receives the identical user
question."

---

## Fix 4 — 8.2.4's SRQ1 figures are wrong in every cell

The paragraph reports test WMAPE from a superseded training run and names the
wrong model.

| The chapter says | Measured (`tuned_metrics.csv`, 2026-09-09) |
|---|---|
| CSD 16.5% | **18.4%** |
| Danskvand 22.0% | **23.4%** |
| Energidrikke 11.4% "≈ the ≤15% industry target" | **17.4%** — the target claim fails |
| RTD 31.0% | **30.8%** |
| "tuned XGBoost is the best model in every category" | **false**: Energidrikke and RTD serve LightGBM |
| ARIMA: CSD 24.2, Dansk 33.4, Energi 15.7, RTD 48.2 | **21.8 / 33.5 / 19.4 / 53.3** |

⚠ **The ≤15% industry target is no longer met anywhere.** That is a real change
of finding, not a rounding correction.

### Anchor

**Section 8.2.4 Results**, the whole paragraph, starting:

> "On the selected per-category configuration (Ch6 §6.5.6), tuned XGBoost is the
> best model in every category."

ending:

> "...SHAP attributes the forecasts chiefly to lag_1 (last-month sales) and
> weighted_distribution (shelf availability) across all categories."

### Action

DELETE the paragraph, and replace the section with a cross-reference.

#### Replace with

> ### 8.2.1 The forecasting substrate
>
> The accuracy of the substrate itself is established in Chapter 5 and is not
> re-reported here. What matters for this chapter is which model each category
> serves, because that is what the dedicated-model scenarios call: the two
> largest categories are served by a tuned gradient-boosted model of one family
> and the two smallest by the other, each selected on cross-validated rather
> than test accuracy so that selection is not made on the evaluation set.

### Note — why delete rather than update

Repeating Chapter 5's benchmark here creates a **second copy of the same
measurement, forty pages apart**. That is exactly the defect found between
Chapter 5 and Chapter 7 last week, where two copies of the calibration table had
silently drifted on three labels. One table, cited from wherever it is needed.

---

## Fix 5 — 8.3 replaces the judge study with the ladder results

⚠ **The entire Level 2 section describes a study that was not run in the form
described.** Comments 336, 343, 345 and 346 all flag it. There is no GPT-4o
judge, N was never 50, the temperature-0 control is not available on the current
model, and the rule-based template baseline does not exist in the design.

### Anchor

**Section 8.3 Level 2 - Recommendation quality evaluation (SRQ2)**, everything
from the heading **"8.3.1 LLM-as-Judge protocol"** through the end of 8.3.4,
ending:

> "...the SRQ4 code-as-action comparator requires an execution sandbox (E2B key
> not configured) and is deferred."

### Action

REPLACE the whole of 8.3 with the results of the funded evaluation.

#### Replace with

> ### 8.3 Results
>
> Sixty runs of sixty-three produced a usable forecast. The three that did not
> are all the same scenario on the same brand, and are discussed below rather
> than averaged away.

**Then insert this table:**

| Scenario | Runs | Usable | Median APE | Mean APE | Stability (CV) | Cost | Latency |
|---|---|---|---|---|---|---|---|
| A, no firm data | 9 | **6** | 502.2% | 662.1% | 23.3% | $3.42 | 69.5 s |
| B, data and code | 9 | 9 | 2.9% | 27.9% | 3.3% | $4.20 | 123.8 s |
| C, dedicated model | 9 | 9 | 14.6% | 13.1% | **0.0%** | **$0.08** | **6.0 s** |
| F, both | 9 | 9 | 7.3% | 18.3% | 1.4% | $3.83 | 103.9 s |
| D, data and code, production | 9 | 9 | **0.9%** | 25.0% | 6.6% | $6.90 | 111.3 s |
| E, dedicated model, production | 9 | 9 | 14.6% | 13.1% | **0.0%** | $1.79 | 31.7 s |
| G, both, production | 9 | 9 | 1.8% | 15.6% | 2.7% | $4.98 | 84.4 s |

> ***Table 20*** *- The seven scenarios on sixty-three runs. Cost is the token
> estimate, which exceeded the amount actually billed by roughly a third.*

> The first thing the table establishes is that the ladder's bottom rung behaves
> as designed. The scenario given no firm data is the only one that fails, and
> it fails on the smallest brand: asked about a small regional Danish producer
> selling roughly 2,850 units in the scored month, it answered 120,000, 62,000
> and 90,000 across three repeats. Those are not forecasts with large errors but
> answers of the wrong order of magnitude, and they are classified as failures
> rather than scored, because averaging them would let an arbitrary number
> determine the scenario's mean. Every other scenario answered every question.
>
> The second is that the two dedicated-model scenarios returned an identical
> figure on every repeat, to the decimal, and returned the same figure as each
> other whether the call was orchestrated by the hosted model or by the
> production platform. Their coefficient of variation is zero. This is not a
> duplicated column: both scenarios load the same persisted model and read its
> output, so the value cannot differ, and the identity is the reproducibility
> property Chapter 7 specifies, observed rather than asserted.
>
> The third is that no scenario leads on every axis, and the disagreement is
> systematic rather than noisy. The dedicated-model scenarios are the cheapest
> by a factor of roughly fifty and the fastest by a factor of roughly twenty
> against the code-writing scenarios, and they are the only ones whose answer
> does not change between runs. The code-writing scenarios are more accurate on
> the median and less accurate on the mean, which is to say they are better most
> of the time and occasionally much worse.

### Note — the mean and median disagree, and that is the finding

⚠ **Do not report one without the other.** Scenario B's median APE is 2.9 per
cent and its mean is 27.9. A single bad brand moves the mean by an order of
magnitude. The dedicated model's mean (13.1) is *better* than B's while its
median (14.6) is *worse* — the two metrics rank the scenarios oppositely, and
that is a real property of the comparison rather than a presentational choice.

---

## Fix 6 — The per-brand table, and the result that cuts against the headline

**Insert after the results table.** The handover flags this as the obvious
examiner question, and it must not be buried.

#### Insert

| Scenario | 7-UP | HARBOE | ØRBÆK |
|---|---|---|---|
| A, no firm data | 1305.8% | 18.5% | unscored |
| B, data and code | 78.9% | 4.1% | 0.8% |
| C / E, dedicated model | 14.6% | **21.9%** | 2.8% |
| F, both | 47.0% | 7.3% | 0.6% |
| D, data and code, production | 73.6% | **0.6%** | 0.6% |
| G, both, production | 41.9% | 3.7% | 1.3% |

> ***Table 21*** *- Mean absolute percentage error by brand. Actual sales in the
> scored month: 7-UP 13,042 units, HARBOE 6,365,900, ØRBÆK 2,850.*

> Two features of this table qualify the aggregate figures. The first is that one
> brand is hard for every scenario: the mid-volume brand draws the worst error in
> six of the seven, and the scenario with no firm data is wrong by a factor of
> thirteen on it. Per-brand heterogeneity of this size means an aggregate over
> three brands is a summary of three quite different problems rather than an
> estimate of a single underlying quantity.
>
> The second is that on the largest brand the dedicated model is beaten, and
> beaten decisively, by the scenarios that write their own analysis. The trained
> model scores 21.9 per cent where the production code-writing scenario scores
> 0.6. This is the clearest single result in the evaluation that runs against the
> artefact, and it is reported rather than qualified away. The explanation is not
> that code beats models; it is that a model fitted to one series beat a model
> fitted to a category. The code-writing scenarios fit their models to the single
> brand in the prompt, using its own thirty-nine months, while the dedicated
> model serves every brand in the category from one configuration tuned once.
> Per-series adaptation is a genuine advantage of writing code, and on a brand
> with a long clean history it is a large one.

### Note — the restatement is load-bearing

⚠ **"A model fitted to one series beat a model fitted to a category" is the
sentence that keeps this honest.** Without it the reader concludes the artefact is
unnecessary. With it, the result is a scope condition on when per-category
training is the wrong choice — which is decision-useful and survives the funded
set.

---

## Fix 7 — Stability, and why the repeats exist

**Insert after the per-brand table.** This is the methodological point that makes
every other number readable.

#### Insert

> Every scenario answered each question three times, and the variation within a
> scenario is reported alongside the differences between them. The reason is
> visible in the data: on the mid-volume brand, the scenario with no firm data
> returned errors of 1740, 1204 and 974 per cent across three runs of an
> identical prompt, a spread of 767 percentage points. The scenario that writes
> its own code varied by 23 points on the same brand. Differences between
> scenarios smaller than the variation within them cannot be read as ordering,
> and a single run of each scenario would have produced a ranking that looked
> clean and meant nothing.
>
> The dedicated-model scenarios are the limiting case in the other direction.
> Their spread is zero on every brand, because the model is fitted once and
> loaded rather than re-derived, so repeated runs are repeated reads of the same
> parameters. Between those two extremes the combined scenarios vary by one to
> three per cent. Stability is therefore not a secondary property that happens to
> accompany the structured interface; across these runs it is the axis on which
> the two approaches differ most cleanly.

---

## Fix 8 — Cost, reconciled against the account rather than estimated

#### Insert as a short subsection after stability

> ### 8.3.1 Cost
>
> The evaluation cost **$19.60** in total, measured as the change in the account
> balance across the two invocations that ran it, which is the only figure not
> subject to estimation error. Token-based estimates computed from the logged
> usage total $25.20, an overshoot of twenty-nine per cent, and the provider's
> billing endpoint reports $18.46 for a single billing window that does not cover
> the whole run. Where per-scenario costs are quoted in this chapter they are
> token estimates and are therefore upper bounds.
>
> The practical figure is roughly thirty-one cents per run. A larger evaluation
> can be sized from it directly: four brands across five repeats and seven
> scenarios would be a hundred and forty runs, or about forty-three dollars.

### Note — three cost figures exist and only one is correct

⚠ **Never cite `summary.md:42`.** It states "Actually billed over the run window:
$18.4647" as though it were the total. It covers one window of a two-movement
spend. The file is internally consistent and externally wrong, which is the
hardest kind of error to catch.

---

## Fix 9 — 8.4 keeps the resource question but drops the unrun protocol

Sections 8.4.1 to 8.4.3 describe profiling protocols and a failure-mode analysis
that were not executed as described. Comments 349, 351, 353 and 355 flag all of
them. 8.4.4's figures are also superseded: it reports tracemalloc values from a
thirteen-feature matrix against an **8 GB** ceiling, where the thesis constraint
is four.

### Anchor

**Section 8.4 Level 3 - Agent behaviour evaluation**, from the heading
**"8.4.1 RAM profiling"** through the parenthetical closing 8.4.4:

> "*(Failure-mode analysis §8.4.3* *-* *API timeout / fallback* *-* *is part of
> the agentic harness evaluation and is run with the LLM-dependent layer.)*"

### Action

REPLACE with one short section.

#### Replace with

> ### 8.4 Operating cost of the substrate
>
> The memory behaviour of the substrate is measured in Chapter 5 and summarised
> in Chapter 6's budget; it is not re-measured here. The figure relevant to this
> chapter is what serving a forecast costs at the moment an agent asks for one.
> Loading a persisted model and returning a prediction peaks below half a
> megabyte of resident memory for every model family in the substrate, against a
> four-gigabyte ceiling, and completes in milliseconds. The fitting path, which
> the serving interface never executes, peaks at thirty-two megabytes.
>
> The consequence for the comparison is that the resource constraint which
> motivated the whole substrate does not bind the delivered system. What binds it
> is the cost of the language model, which is billed per token and runs
> elsewhere. A dedicated-model answer consumes about a thousand input tokens
> because the payload it receives is a structured response; a code-writing answer
> consumes between twenty-eight thousand and a hundred thousand, because the
> brand's full history is placed in the prompt and the analysis is generated
> rather than retrieved.

### Note — the latency and cost asymmetry is structural, not incidental

It will not reverse with a better prompt or a faster model, because the two
approaches move different amounts of data. **State it as a property of the
architecture**, which is what makes it a design finding rather than a benchmark
result.

---

## Fix 10 — 8.5 needs prose and a threats table that matches the study that ran

Comments 357, 358 and 360: the section is a bare table with no context, and two
of its five rows describe the judge study.

### Anchor

**Section 8.5 Threats to validity**, the heading and the whole table beneath it,
through the caption:

> "**Table** **21** - Threats to Validity"

### Action

REPLACE the section, adding an opening paragraph and revising the table.

#### Replace with

> ### 8.5 Threats to validity
>
> Four threats bear on what these results can support, and each is stated with
> what was done about it rather than only named.

| Threat | Type | What was done |
|---|---|---|
| Three brands in one category | External validity | The scope is stated wherever a result is claimed; the brands are stratified by volume rather than chosen, so the range is covered even though the sample is small |
| Within-scenario variation comparable to between-scenario gaps | Internal validity | Three repeats per cell; the spread is reported beside every mean, and no ordering is claimed where the gap is smaller than the spread |
| Prompt wording confounded with capability | Construct validity | The question is identical across scenarios and the capability notes are composed from shared blocks, with an automated check asserting paired scenarios are byte-identical |
| Volume floor on brand inclusion | Construct validity | The floor is a property of the error metric's resolution, applied identically to every scenario and before any run; brands below it are outside the study's scope rather than excluded by outcome |

> ***Table 22*** *- Threats to validity and the measures taken*

> A fifth limitation is not a threat to the design but a boundary on the claim.
> What the evaluation measures is what each scenario communicated and how
> accurate it was, not whether a planner receiving that communication decided
> better. Establishing the latter would require an experiment with human
> participants and ethical approval, and is outside the scope of this thesis.

---

## Fix 11 — 8.6 needs prose, and its SRQ table is wrong on two rows

Comments 362 and 364: bare header and table. The table also credits SRQ4 with a
"human descriptive baseline" comparison that does not exist.

### Anchor

**Section 8.6 Connection to SRQs**, the heading through the caption:

> "**Table** **22** - Chapter 8: Results Connection to SRQs"

### Action

REPLACE.

#### Replace with

> ### 8.6 Connection to the sub-research questions
>
> The evaluation reported here answers the fourth sub-research question directly
> and supplies evidence to two of the others.

| SRQ | What this chapter contributes |
|---|---|
| SRQ1 | Consumed, not answered. The substrate's accuracy is established in Chapter 5; this chapter serves the selected model and does not revisit the selection. |
| SRQ2 | Evidence. The reproducibility the interface is designed for is observed across every run, and the departure of the combined scenarios from the model's forecast identifies a field the payload does not carry, discussed in Chapter 7. |
| SRQ3 | Not addressed. Integration readiness is argued in Chapters 3 and 6. |
| SRQ4 | Answered. Seven scenarios on a shared question, with the increments attributed separately and the trade between accuracy, cost, stability and auditability measured rather than asserted. |

> ***Table 23*** *- Chapter 8 contributions to the sub-research questions*

---

## Fix 12 — Delete "Outstanding decisions"

Comment 365 (METACOMMENT, VERIFY). Four bullets addressed to the authors, inside
submission prose. All four are now answered or void: the judge study is gone, so
the sample-size and inter-rater questions are void; Nielsen access was obtained;
and the baseline question is settled by the ladder.

### Anchor

The heading **"Outstanding decisions"** and the four bullets beneath it, ending:

> "Manifold descriptive baseline: need to discuss with Manifold AI team what form
> the current tool's outputs take"

### Action

DELETE.

---

# Comment ledger

All 23 threads.

| Threads | Section | Verdict |
|---|---|---|
| 322 | title | **ADDRESSED** — Fix 1 |
| 324 | 8.1 | **ADDRESSED** — Fix 2 replaces the framework |
| 327, 329, 331 | 8.2.1–8.2.3 | **ADDRESSED** — Fix 3. The weekly SKU-by-retailer grain was wrong and is gone |
| 333 | 8.2.4 | **ADDRESSED** — Fix 4. Every figure was wrong; the section becomes a cross-reference |
| 336, 343, 345, 346 | 8.3.1–8.3.4 | **ADDRESSED** — Fix 5. The judge study was never run in that form |
| 338 | 8.3.2 | **ADDRESSED** — calibration is Chapter 5's, cited not repeated |
| 340, 341 | 8.3.3 | **ADDRESSED** — Fix 3 and Fix 5. The metacomment heading goes; the comparator is now described in the design section |
| 349, 351, 353, 355 | 8.4.1–8.4.4 | **ADDRESSED** — Fix 9. The 8 GB ceiling and tracemalloc figures are superseded |
| 357, 358, 360 | 8.5 | **ADDRESSED** — Fix 10 |
| 362, 364 | 8.6 | **ADDRESSED** — Fix 11 |
| 365 | Outstanding decisions | **ADDRESSED** — Fix 12 |

---

# Two things this chapter must not claim

⚠ **The four interval-communication criteria have not been scored on this run.**
The artefact holding them contains three rows, all from a different scenario on a
brand not in this sample, dated before the current prompt schema. Chapter 7
specifies the check; **Chapter 8 must not report figures from it** until
`score_interval_communication.py` is re-run over the sixty-three funded runs.

⚠ **Do not write the conclusion sentence yet.** The shape the evidence supports
is *"dedicated models trade accuracy for auditability and cost at this data
scale"*, and "at this data scale" must carry its numbers every time: three
brands, one category, thirty-nine months, one model per category. Chapter 9 owns
the interpretation; this chapter reports what was measured.

---

# One fix outside this chapter

**Chapter 9, section 9.1.4 states the code-as-action baseline "was *not*
executed: it requires a secure execution sandbox (E2B) that is not configured."**

⚠ **It ran sixty-three times**, and the sandbox provider named is no longer part
of the design. The sentence is false on either branch and must go. Flagged here
because Chapter 8 is where its replacement evidence lives.

---

# Related

- `plans/P0049_.../BRANCH_A_STATE.md` — the measured experiment
- `plans/P0049_.../HANDOVER_CH6_CH7_CH8_BRANCH_A.md` — the brief
- `the-agent-input-contract.md`, `prompt-consistency-as-an-experimental-control.md`,
  `brand-sampling-and-inclusion-criteria.md` — folded into Fix 3; archive on applying
- `the-defensible-conclusion-shape.md` — still live, still correctly unwritten;
  its gates are now met except the Chapter 9 interpretation
