---
name: the-result-hinges-on-forecasting-practice
description: NOTE - The whole SRQ4 comparison is conditional on the quality of the EDA, feature engineering and forecasting practice on BOTH sides. Combination is established theory (Hyndman 13.4), the agents already do it unprompted, and the thesis pipeline does not - which reframes the F/G result and gives future work a concrete shape.
category: reference
applies-to: [ch9_discussion, ch10_limitations, ch8_experiment, ch5_model_benchmark]
triggers: [discussion, limitations, future research, why did code-as-action win, ensemble, forecast combination, what determines the result]
created: 2026_09_12-20_25
updated: 2026_09_12-20_25
status: bullets, not prose - PROVISIONAL on the funded run
---

# The result hinges on forecasting practice, on both sides

**Brian, 2026-09-12.** The comparison does not measure "language agent versus
trained model" in the abstract. It measures **one particular pipeline** against
**one particular agent's in-session practice**, and both are contingent. Say so
in the discussion, or the reader will over-generalise in whichever direction the
numbers point.

---

## What the agents already do unprompted

Evidence from the traces, not inference:

- **Scenario B fitted an 18-order SARIMA grid** in a single run — `(p,d,q)` over
  `p∈0..2, d∈{0,1}, q∈0..2` — selected on AIC, on log-transformed units.
- It then **combined across methods by hand**: "OLS gives 6.67, ETS provides a
  median of 6.4, and seasonal growth is at 7.14", settling near 6.7.
- **Scenario F imported six sklearn families** in one run (Huber, ElasticNetCV,
  LassoCV, RandomForest, GradientBoosting, plus OLS) and described its answer as
  "blended from various models".

So the agents are not naive. Within one session they reach for exactly the
practice the literature recommends — and one piece of that practice is
**absent from the thesis pipeline**.

### Confirmed on the v6 runs, and it is systematic

Not a one-off from an old smoke. Measured across the funded run's B and F
traces:

- **Every single run fitted exponential smoothing and a seasonal ARIMA.**
  Those are precisely the two things Chapter 5 records as missing: ETS is
  omitted entirely, and the pipeline's ARIMA carries no seasonal term.
- Most runs added STL decomposition, and several added Ridge, Huber, OLS or
  weighted least squares alongside.
- **12 of 14 runs used explicit combination language** — "ensemble", "blend",
  "median of", "simple average" — in their own reasoning.

The agent is therefore not merely combining. **It is routinely applying two
techniques the pipeline lacks**, on every run, unprompted. Whatever accuracy
advantage the data arms show, this is where a large part of it plausibly comes
from — and unlike agency, it is a gap the pipeline could close cheaply.

## Combination is established theory, and it favours the agents

Hyndman and Athanasopoulos (2021, §13.4) is unambiguous, and it is already a
cited source in this thesis:

> "The results have been virtually unanimous: combining multiple forecasts
> leads to increased forecast accuracy. In many cases one can make dramatic
> performance improvements by simply averaging the forecasts." (Clemen, 1989,
> quoted at §13.4)

And on the difficulty of beating the simplest version:

> "While there has been considerable research on using weighted averages, or
> some other more complicated combination approach, using a simple average has
> proven hard to beat" (Wang et al., 2023, cited at §13.4)

Their worked example has the combination beating **every** component model on
RMSE, MAE **and** the Winkler interval score. The text notes the general case
plainly: "For other data, ARIMA may be quite poor, while the combination
approach is usually not far off, or better than, the best component method."

**The implication is uncomfortable and should be stated.** The thesis pipeline
selects a single best model per category. The agents combine. On this evidence,
part of any accuracy advantage the data arms show may be **the combination
doing the work**, not code-as-action as such — which is a far more useful
finding than "the agent won".

**Citations to add:** Bates & Granger (1969), Clemen (1989), Wang et al.
(2023) — all in §13.4's bibliography. Check Zotero before citing; if absent,
cite Hyndman & Athanasopoulos (2021) §13.4 directly, which is already in the
library.

---

## The grain asymmetry — the largest confound, and it is not combination

**Brian, 2026-09-12.** The two sides were not fitted at the same grain, and
this may matter more than the combination point above.

| | Fitted on | Series seen |
|---|---|---|
| **The pipeline** | one model per **category**, or pooled across all categories | every brand in CSD, or every brand everywhere |
| **The agents (B, D, F, G)** | the **single brand** in the prompt | 39 months of one brand |

The agent fits a **bespoke model to the exact series it is asked about.** The
pipeline fits one model to many series and serves a slice of it. On a brand
whose behaviour is unlike the category average, the bespoke fit has a
structural advantage that has nothing to do with code-as-action, ensembling or
agency.

**This is the most likely single explanation for the data arms' accuracy, and
it must be stated before any other interpretation.**

### Why per-brand training was not done — four reasons, all defensible

1. **Series length.** ~37 training months per brand. Too sparse for the model
   families under test to benefit, and the sparsity argument is already made
   elsewhere in the thesis.
2. **Combinatorial cost.** Every tested brand would need its own training,
   benchmarking and tuning run. At the 50-plus brands originally planned for
   adequate sample size, the manual effort explodes.
3. **M5 precedent.** The literature review already carries this: M5 reports
   that **cross-learning — one model trained across many series — outperformed
   series-by-series training at lower computational cost**, and the review names
   that as "the direct precedent for the pooled-versus-per-category comparison
   of SRQ1" (Makridakis et al., 2022). Per-brand training is the approach M5
   found *worse*.
4. **SRQ1 is a substrate question, not a per-brand one.** SRQ1 asks which
   lightweight models trade accuracy against memory and category
   specialisation. A per-brand regime answers a different question and would
   have made the memory-budget framing incoherent — one model per brand is not
   a small-business cloud memory budget.

**Add a fifth, worth stating:** a per-brand model cannot serve a brand with no
history. The pooled and per-category models generalise to new and short-history
brands; a per-brand regime has nothing to serve them with. That is a
deployability argument, not an accuracy one, and it belongs with the
reproducibility case.

### How to write it

**Do not present this as a flaw.** Present it as a **scope boundary with a
consequence**: the comparison is between an agent fitting bespoke models per
brand and a pipeline fitting shared models across brands, and the grain
difference is a live alternative explanation for any accuracy gap. Then note
that M5's own evidence runs the other way at scale, which makes the result
here specific to **short single-brand series**, not general.

**Future work gets a sharp, testable form:** fit the pipeline per brand on the
same three brands and re-compare. If the gap closes, the finding is about
**grain**, not about agents. That is one training run, not fifty.

---

## This reframes F and G

The intuition was "more context should help, and it did not". The better
reading, given §13.4, is about **what kind of disagreement is being combined**:

- Combination works when components are **comparably good and errors are
  imperfectly correlated**. Averaging then cancels error.
- F and G average an in-session ensemble against **one** model whose
  `confidence_tier` is *Low* and whose interval is wide. That is not a
  combination of peers — it is a good estimate dragged toward a weaker one.
- Both arms recorded `deviates_from_model = True`, so they did not simply
  defer. They weighed and still landed worse.

**So the F/G result is not evidence against combination.** It is evidence that
combination needs a **weighting policy**, and that presenting sources without
one — which is what a decision-support layer naively does — can destroy value.
That is a genuine SRQ2 finding, and it is actionable: inverse-error weighting
is already implemented in `srq2_synthesis.py` for the ensemble there.

**Do not over-claim at n=3.** State it as a hypothesis the design can test.

---

## Where the thesis already admits the gaps (keep these consistent)

Chapter 5 is candid, and the discussion should point back rather than
re-litigate:

- **Exponential smoothing is omitted** — "a strong classical baseline on
  seasonal monthly data", absence acknowledged as a limitation.
- **ARIMA carries no seasonal term** on a strongly seasonal monthly panel,
  because automatic order selection was unavailable in the deployment
  environment. Chapter 5 already calls its figures "a floor for the family
  rather than its best attainable performance".
- **Seasonal naive beats every tuned model on RTD.**
- **Bounds are applied after back-transformation**, a stated departure from
  §13.3's preference for imposing limits through the transformation itself.

**The honest framing:** the agent is not being compared against the best
attainable statistical practice. It is compared against **this pipeline**, whose
own limitations are documented. That cuts against over-claiming a win for either
side.

---

## What goes where

**Discussion.** The conditionality, and the reframing of F/G as a weighting
problem rather than a context problem.

**Limitations.** Three sentences: the pipeline omits ETS, fits a non-seasonal
ARIMA to seasonal data, and selects a single model where combination is the
better-established practice. The agents, by contrast, combine unprompted. The
comparison is therefore between a *specific* pipeline and a *specific* agent
practice.

**Future research.** Concrete and testable, not vague:

0. **Fit the pipeline per brand on the same three brands** and re-compare.
   This is the **cheapest and most informative** item on the list: one training
   run, not fifty, and it separates *grain* from *agency*. If the gap closes,
   the headline finding changes shape entirely.
1. **Add a combination baseline to the pipeline.** A simple average across
   families is the single highest-value change suggested by §13.4, and it is
   cheap. Add ETS and a seasonal ARIMA at the same time — the agents fit both
   on every run, and the pipeline has neither.
2. **Give F and G an explicit weighting policy** (inverse historical WMAPE, or
   confidence-tier gating) instead of presenting sources unweighted.
3. **Close the ETS and seasonal-ARIMA gaps** so the comparison is against
   competent classical practice.
4. **Test whether the agent's advantage survives** once the pipeline itself
   combines. If it does not, the finding is about combination, not agency.

---

## The sentence the discussion needs

> The experiment measures a specific pipeline against a specific in-session
> practice. Both are contingent, and two identifiable asymmetries favour the
> agent before agency is invoked at all: it fits a bespoke model to the single
> series it is asked about, where the pipeline serves a slice of a model fitted
> across many; and it routinely applies exponential smoothing, seasonal ARIMA
> and forecast combination, none of which the pipeline employs.

Both asymmetries were **chosen for defensible reasons** — cross-learning is
what M5 found superior at scale, and the memory budget rules out one model per
brand. Neither is a mistake. But they bound the claim: what the experiment
shows is specific to **short, single-brand series**, and it does not generalise
to the regime M5 measured.

---

## Related

- [[when-to-use-which-scenario-group]] — the deployment guidance this qualifies
- [[ad-hoc-data-science-vs-a-trained-pipeline]] — the reproducibility axis,
  which combination does not change
- [[srq4-interpreting-the-accuracy-gap]] — the four competing explanations;
  combination belongs in that list
- Hyndman & Athanasopoulos (2021) §13.4, §13.3, §5.2 — split PDFs held locally
