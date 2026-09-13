---
name: anticipated-assessor-questions
description: REFERENCE - The questions an examiner is most likely to ask at defence, each with the measured answer and where the evidence sits. Cumulative across chapters; add to it whenever a pass turns up a question the thesis must survive.
category: reference
applies-to: [defence preparation, all chapters]
triggers: [preparing for defence, deciding whether a claim is defensible, writing a limitations section, answering "will they ask about this"]
created: 2026_09_11-20_35
updated: 2026_09_11-20_35
---

# Anticipated assessor questions

**One file, cumulative across chapters.** Every entry is a question a reader can
actually ask from the text, with an answer resting on something measured rather
than argued.

**Verified at `6ccdcc7`**, against snapshot `2026-09-11_20-08_ch6-prose-start`
and the results artefacts regenerated after the 9 September training.

## How to use it

| Field | Means |
|---|---|
| **Q** | the question, phrased as an examiner would ask it |
| **Answer** | what to say, in one or two sentences |
| **Evidence** | the artefact, file or measurement it rests on |
| ⚠ | where the honest answer concedes something |

**A question with no evidence row is not ready.** Those are collected at the end
under *Questions we cannot yet answer*, which is the more useful half of this
document.

---

# 1. The architecture and the memory budget

## Q1.1 — Your memory budget is four gigabytes and your system uses 231 megabytes. Was the constraint real?

**Answer.** The constraint bound the *selection space*, not the final footprint.
It excluded transformer and locally hosted options before any of them was fitted,
which is the decision it was there to make. That the selected models then sat far
below the ceiling is a result, not a failure of the constraint.

**Evidence.** `05_substrate_resource_profile`: peak fit memory is 0.04 to 0.78
per cent of the 4096 MB budget across all four models. Chapter 5 Section 5.5.6
states the conclusion.

⚠ **Concede this openly.** The honest framing is that the budget did its work at
design time. A thesis claiming the budget was binding at run time would be
contradicted by its own table.

## Q1.2 — Why sequential execution if the models fit concurrently anyway?

**Answer.** Sequential execution is what made the budget safe to design against
before anything was measured. Once measured, concurrent execution would also have
fitted. The design decision was correct under the information available when it
was made, and the measurement is what changed.

**Evidence.** Same table. Peak *prediction* memory is 0.03 to 0.47 MB, so all
four models resident at once would still cost under a megabyte at serving time.

## Q1.3 — Does the memory measurement still describe the model you ship?

**Answer.** Yes, as of 11 September. The profile was re-run against the
eighteen-feature matrix after the final training.

⚠ **This was not true until 11 September**, and the correction is instructive:
the earlier figures predated the training by eight days and the chapter had
inferred they were a *lower* bound. They were not. Memory tracks the size of the
tuned ensemble, not the width of the feature matrix.

**Evidence.** `profiling.csv`, re-run 2026-09-11;
`ch5_model_benchmark/ch5-profiling-rerun.md` records the correction.

---

# 2. The forecasting substrate

## Q2.1 — You say five models span an accuracy-efficiency frontier. Does Prophet?

**Answer. Not reliably, and the thesis should not claim a frontier.** Prophet's
weighted MAPE is 105.7 on CSD and 975.0 on energidrikke — worse than a naive
baseline, not a different trade-off. The five families were selected to cover
*inductive biases*, not to sit on a frontier.

**Evidence.** `09_statistical_baselines`. Chapter 5 already uses the correct
framing; Chapter 6 is being corrected to match.

⚠ **Do not say Prophet is dominated everywhere — it is the best model on
Danskvand**, at 19.4 against every alternative. That makes the honest answer more
interesting than a dismissal: Prophet's variance across categories is enormous,
which is itself the argument for selecting per category rather than globally.

⚠ **The failures have an explanation worth giving.** Prophet is built for daily
series with holiday effects, and the grain here is monthly, so its holiday
machinery receives no usable input. Where the seasonal structure happens to suit
it, it wins; where it does not, it diverges.

## Q2.2 — Why does model selection use cross-validation when test performance disagrees?

**Answer.** Selecting on the test split is selection on the evaluation set, which
biases every number downstream of it. Cross-validation selection is the
defensible choice even though it picks a different model in two categories.

**Evidence.** `best_model_for()` carries the reasoning in code. On test, XGBoost
wins everywhere; on cross-validation, energidrikke and RTD select LightGBM.

⚠ **This looks like an error until explained**, so it should be explained in the
text rather than left for the viva.

## Q2.3 — Your prediction intervals attain coverage but are enormous. Is that useful?

**Answer.** The marginal guarantee holds: 83.9 to 91.7 per cent against a 90 per
cent target. The width is the honest cost of one pooled quantile over brands
spanning six orders of magnitude with few validation months each. Three
alternative schemes were implemented and measured, and none improved coverage and
width together in more than two of four categories.

**Evidence.** `calibration.csv`; P0049 findings F50 and F52.

⚠ **A tested negative result is a contribution.** The answer is stronger for
naming what was tried and failed than it would be for defending the width.

---

# 3. The tool interface (SRQ2)

## Q3.1 — The user asks a natural-language question. How does the model get the lag values?

**Answer. It does not, and must not.** The language model performs exactly two
translations: intent into typed parameters, and a structured payload into prose.
Feature construction happens server-side, where it is versioned and identical on
every call. The model never sees a feature vector.

**Evidence.** `forecast_tool.py`. Recorded tool-call spans carry the arguments
and an `args_match_request` flag.

**This is the SRQ2 contribution**, so the question is a gift rather than a
threat.

## Q3.2 — Why function-calling rather than letting the model write code?

**Answer.** A schema-constrained call has one well-formed shape and its arguments
can be checked against the request that produced it. Generated code is re-derived
on every invocation and is not guaranteed to be the same twice, which is
measurable and substantial.

**Evidence.** Ouyang, Zhang & Harman (2025) measure non-determinism in
language-model code generation. In the pilot, the tool-backed arms returned
identical numbers to the decimal across runs; the code-writing arms did not.

⚠ **Do not claim it is more accurate.** The justification is reliability,
reproducibility and auditability. On the pilot brand-month the code-writing arms
were *more* accurate, and the argument survives that because it never rested on
accuracy.

## Q3.3 — Your confidence index returns the same value for every brand in a category. Why ship it?

**Answer. It is degenerate and the thesis says so.** Two independent defects: the
forecast cancels out of the relative width, leaving a function of the per-category
quantile alone, and the second term is identically zero because it assumes a
quantile bounded near one when the measured values are 1.89 to 2.69. Four
attainable values exist across all brands, all tiering "Low".

**Evidence.** `ch7_synthesis/ch7-verification-pass.md (Part 2)`;
`forecast_tool.py` now carries an assertion that fires if the degeneracy ever
lifts.

⚠ **It cannot be repaired by recalibrating the bands**, because re-tiering four
constants yields a category label wearing a number. The field is retained only
because published experiment runs are scored against it.

⚠ **There is an unexpected defence here.** In the combined scenarios both agents
departed from the model's forecast and cited its confidence tier and interval
width as the reason. A constant "low" was, on that brand, the honest signal — and
it changed behaviour. That is the uncertainty channel working even through a
broken index.

---

# 4. The experiment (SRQ4)

## Q4.1 — Three brands from one category. What can that possibly establish?

**Answer.** It is sized to detect differences between scenarios that are large
relative to the variation within them, not to establish cross-category
generalisation, and the thesis does not claim the latter. The three brands span
three orders of magnitude of volume, and every scenario answers for the same
three brands, so differences are attributable to the scenario rather than to the
draw.

**Evidence.** DEC-MVP-DESIGN in P0049; `ch8_experiment/brand-sampling-and-inclusion-criteria.md`.

⚠ **Declare this in the design chapter, not only in limitations.** A scope
limitation that appears first in Chapter 10 reads as something discovered late.

⚠ **Never justify the brand selection on "hard to forecast" grounds.** That is
outcome-based selection. The criteria are volume coverage and a meaningful error
metric, both fixed in advance.

## Q4.2 — A scenario without your model beat your model. Doesn't that refute the thesis?

**Answer. No, and it is evidence for the claim rather than against it.** The
defensible conclusion is that dedicated models trade accuracy for reproducibility
and cost at this data scale. A scenario beating the model on accuracy is the
trade becoming visible. The cost and latency gap is structural and will not
reverse: one model inference against roughly eighty model fits plus a sandbox.

**Evidence, funded set (63 runs, 2026-09-12).** The tool-backed scenario answered
in 6.0 seconds at $0.0091 per answer through a single verifiable tool call; the
code-writing scenario took 123.8 seconds at $0.4667, which is **51.5 times the
cost and 20.8 times the latency**. On accuracy the code-writing scenario leads on
the median, 2.9 against 14.6 per cent, and trails on the mean, 27.9 against 13.1.

⚠ **"At this data scale" is load-bearing and must carry its numbers every time.**
Without them the claim degrades into a universal one the evidence cannot support.
The numbers are 39 months, 95 brands in the category, one category-tuned model.

⚠ **The accuracy ordering is interpretable only as median-versus-mean.** The
code-writing scenario is better most of the time and occasionally much worse;
that is the honest ordering, and it is not a ranking on accuracy as such.
Differences smaller than the within-scenario spread are still not orderable.

## Q4.3 — Why does an arm that already has the forecast still write code?

**Answer.** Because the model's forecast is supplied as one input among several
rather than as a starting figure to revise. An agent handed a number and
permitted to keep it will usually keep it, and the design would then measure
deference rather than integration.

**Evidence.** Verified across the funded set: **all 18 combined-scenario runs
carry `deviates_from_model = True`**, so not one adopted the figure it was
handed. Several cite the model's own stated uncertainty as the reason.

## Q4.4 — Did code execution win, or did fitting per brand win?

**Answer. The design cannot separate them, and the thesis says so rather than
choosing.** Four explanations compete for any accuracy gap, and the first two are
additive rather than rival:

| | Explanation | What would separate it |
|---|---|---|
| 1 | **Per-series beats per-category.** A category-tuned model is pulled toward brands unlike the one being forecast | Fit the pipeline per brand on the same three brands and re-compare. One training run |
| 2 | **Combination beats a single model.** The code-writing scenarios fit many models and average; the substrate serves one | Add a combination baseline to the pipeline and re-run |
| 3 | **Established practice the substrate lacks.** Exponential smoothing and a seasonal ARIMA term | Close both gaps, then re-compare |
| 4 | **Horizon interaction.** A per-series method may degrade more slowly | Only separable if the secondary horizon is run |

**Evidence.** Measured over the 37 data-scenario responses in the funded set:
**36 fitted exponential smoothing, 32 a seasonal ARIMA, 28 used explicit
combination language.** Chapter 5 records that the substrate has neither ETS nor
a seasonal term.

⚠ **Explanation 1 is the largest and the cheapest to test.** The agent fits a
bespoke model to the exact series it is asked about; the pipeline serves a slice
of a model fitted across ninety-five brands. State this before any other
interpretation.

⚠ **The grain choice was deliberate and defensible, not an oversight.** M5 found
cross-learning superior to series-by-series training at scale, the panel gives
roughly 37 training months per brand, and one model per brand is not a
small-business memory budget. It also could not serve a brand with no history.

⚠ **Never let "the code scenario won" stand as the headline without the
restatement.** As a bare fact it invites the reader to conclude the artefact is
unnecessary. The measured claim is narrower and more useful: at 39 months and 95
brands, a per-series ensemble outperforms a category-tuned booster on the median
while costing 51.5 times more, taking 20.8 times longer, and producing no
auditable tool call.

## Q4.5 — Is your cost figure measured or estimated?

**Answer.** Token counts come from the provider's own usage object and are
measured; rates were verified against billing. Web search is now priced from the
response's own output items. The one genuine unknown is sandbox duration, which
the API does not expose to anyone. Total spend is reconciled against the billing
record.

**Evidence.** P0049 F57, including its correction.

⚠ **An earlier version of this answer was wrong and the correction matters.** The
project briefly believed the estimate under-reported by up to 1.77 times. The
billing endpoint buckets by whole day, organisation-wide, so every comparison had
been against a day of unrelated traffic. Like for like, the estimate is
conservative by about 17 per cent.

---

# 5. Data and method

## Q5.1 — If the model needs thirteen months of lag depth, how does it answer today?

**Answer.** Warm-up is a training-time concept, not a runtime phase. It is the
set of rows at the start of each brand's series whose lag features point before
the data begins, so they cannot be training examples. At serving time the
history is already stored and the feature row is built directly from it.

⚠ **The real serving constraint is cold start**: a brand with too little stored
history cannot be forecast at all. That is a coverage limitation, and the correct
response is a typed refusal naming the brand rather than a degraded forecast.

## Q5.2 — You compare models "on identical data", but the categories differ. Do they?

**Answer. Not entirely, and the asymmetry is real.** The panel reports promotion
for two of four categories, because the source lacks the measures rather than
through a configuration gap. Where absent the column is omitted, never
zero-filled, since a constant-zero column would assert that no promotion ran.
Panel depth also differs by category.

⚠ **This limits cross-category generalisation of any promotion-driven finding**,
and the interval coverage differences track calibration-set size for the same
underlying reason.

## Q5.3 — Why one month ahead?

**Answer.** The binding constraint is evaluation, not modelling: at longer
horizons there is no evaluable test origin left in the panel. Predictability also
decays with horizon, and training rows are lost to deeper lags, but those are
secondary to having nothing left to score against.

---

# Questions we cannot yet answer

**The useful half of this document.** Each of these is askable from the current
text and does not have an answer resting on a measurement.

| | Question | What would answer it | Blocked on |
|---|---|---|---|
| **U1** | Does the accuracy ordering between scenarios hold up? | the funded run, three brands x repeats x seven arms | funding; nothing is paid for yet |
| **U2** | Does an effect on the lightweight coordinator survive on the production orchestrator? | the paired arms D, E and G against B, C and F | same run |
| **U3** | Is the interface's reliability property *guaranteed* or merely *exercised*? | repeated runs showing the reported figure always equals the model's | same run. One pilot run is not a guarantee |
| **U4** | Would the architecture hold in another category? | out of scope by design | not answerable; declare it |
| **U5** | Does the thesis's own conclusion sentence hold? | the funded run, against pre-stated falsification conditions | same run; the conditions are written down, which is what makes it a real test |

⚠ **U1 to U3 all resolve with one funded run.** That is worth knowing when
deciding what to spend: the experiment is not three separate open questions but
one, and the evidence gates are already specified.

⚠ **U4 is not a gap to close but a boundary to state.** An examiner asking it is
testing whether the thesis knows its own limits.

---

# Where the evidence lives

| Kind | Location |
|---|---|
| Any measured number | `05_thesis_results/`, by chapter |
| The reasoning behind a design decision | `plans/P00NN_*/findings.md` |
| What is still open or blocked | `writing-notes/deferred-structural-decisions.md` |
| Claims awaiting a run | `writing-notes/post-hpc-validation.md` |
| Citations added, and the claim each supports | `writing-notes/citations-added-register.md` |

⚠ **Every number quoted at defence must come from an artefact regenerated after
the last training run**, which was 2026-09-09 at 21:10. Four artefacts in the
benchmark folder still predate it and none is currently cited: `param_drift.csv`,
`refit_vs_retune.csv`, `retune_single_cutoff.csv` and `sandbox_profiling.csv`.
**Prefer the numbered appendix table to the raw CSV** wherever both exist.


---

# The forecasting methodology, and why it was not right first time

*Added 2026-09-13 from the P0055 book scan (Hyndman & Athanasopoulos, 41/41
sections read). Full catalogue at `plans/P0055_*/findings.md` F15.*

## Q - Your own Chapter 4 analysis found a significant lag at 12 months. Your feature matrix uses lag 13. Why?

**Answer.** The diagnostics were performed and documented; they did not
propagate into feature construction. No contract existed between the analysis
layer and the engineering layer - the EDA wrote reports for human readers, and
the feature builder read a hardcoded configuration. Nothing connected them, so a
correct diagnostic and an inconsistent feature could coexist without either
being revised.

**Evidence.** `step_2_eda_descriptive.py:543` computes `p_diff`; the decision
rule at `:549` ignores it. `derive_log_transform()` records
`adf_stationary_at_5pct` and then returns the constant `LOG_TRANSFORM_TARGET`.
The repo's own provenance field states *"the lag-12 term is retained"* while the
shipped manifests carry `13`. The ACF measured lag 12 significant for **20 of 20**
brands tested.

⚠ **Concede the narrower point.** No contract was needed to notice that 13 is
not a multiple of 12 on monthly data. If the lag set was inherited from an
earlier weekly-grain prototype and never re-derived when the grain became
monthly, say so plainly - it is an ordinary and truthful explanation.
**This must be confirmed before it is asserted.**

**Why this answer holds.** It is a recognised class of defect - provenance
failure between pipeline stages - rather than unfamiliarity with forecasting
methodology. And it demonstrates the thesis's own SRQ2 argument from the
negative case: a forecast is auditable only if its features carry their
justification.

## Q - You admit a non-seasonal ARIMA on a seasonal panel. Why not simply fit a seasonal one?

**Answer.** The statistical baselines were implemented without `pmdarima`
available, so the order was fixed rather than selected. Section 9.7 specifies
the Hyndman-Khandakar algorithm that would select it. Chapter 5 states the
limitation.

**Evidence.** `srq1_baselines_stat.py:283` - `SARIMAX(order=(1,1,1))`, no
seasonal order; the docstring at line 26 records *"no pmdarima"*.

⚠ Section 9.9 supplies the mitigating sentence, and it is the book's own:
*"it is not possible to find a model that passes all of the residual tests... we
would normally use the best model we could find, even if it did not pass all of
the tests."*

**Measured 2026-09-13:** a Ljung-Box test on the ARIMA residuals rejects white
noise for a substantial share of series, with the remaining autocorrelation
concentrated at the **seasonal lag** - median ACF(12) of +0.361 among rejecting
brands versus +0.064 among non-rejecting. That is the seasonal-order limitation
demonstrated rather than asserted.

⚠ **The exact figures are PROVISIONAL.** The gate ran on in-sample residuals
where 5.3 requires cross-validation residuals; it is being re-run. Direction is
expected to hold - in-sample residuals are optimistically clean, so the true
rejection rate should be higher, not lower. **Do not quote the percentage until
the re-run lands** (P0055 F13, task 12).

## Q - Why MASE rather than MAPE, and is your MASE correct?

**Answer on the choice.** Section 5.9 prefers MASE or RMSSE because percentage
errors need a test set large enough "especially in the denominator". The choice
is the source's own.

⚠ **Concede on the implementation.** The MASE denominator currently uses the
non-seasonal (m=1) difference on a seasonal monthly panel, where 5.8 defines it
with m. The visible symptom is two shipped tables disagreeing about whether
seasonal naive beats naive. **Under repair** (P0055 2.A5, task 7).

---

# Questions this register now answers that it did not before

| Question | Where the answer sits |
|---|---|
| Why does the feature set contradict the chapter's own analysis? | above - provenance failure, line-numbered |
| Is the single-month H=3 scoring a shortcut? | No - 13.8 says averaging across horizons combines unequal variances. See `ch5_model_benchmark/2026-09-13_21-15_BRANCH_A_book-citations-that-strengthen.md` |
| Why tune on WMAPE when the book says RMSE? | Principled - 5.8 shows MAE and RMSE are minimised by different functionals, so the repo tunes once per objective. Same note |
| Is comparing ARIMA against gradient boosting on a test set legitimate? | Yes - 9.10 states AICc **cannot** compare across model classes and prescribes exactly this. Same note |
