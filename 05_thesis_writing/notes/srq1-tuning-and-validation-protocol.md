---
name: srq1-tuning-and-validation-protocol
description: RULE - How the SRQ1 models were tuned and validated, which claims are citable, and which must be justified empirically because no source exists.
category: reference
applies-to: [srq1, methodology, ch5]
triggers: [writing the tuning methodology, defending hyperparameter search, answering "did you cross-validate"]
created: 2026_08_22-15_00
updated: 2026_08_22-15_00
---

# SRQ1 — tuning and validation protocol

For the methodology chapter. **Read the citation section first** — some claims made
during development cannot be sourced and must be argued differently.

## The protocol

| Element | Choice |
|---------|--------|
| Search | Optuna TPE (Bayesian, sequential model-based) |
| Budget | 100 trials per model × category × objective |
| Validation | Expanding-window time-series CV, 4 folds |
| Selection | Mean score across folds |
| Refit | Best configuration on all of train+val |
| Evaluation | **Once**, on an untouched test split |
| Seed | 42 throughout |
| Objectives | WMAPE and median MAPE, tuned separately |

## What can be cited — and what cannot

**This distinction matters more than the protocol itself.** A confident-sounding
claim with no real source is worse than an honest empirical argument.

### Citable (verify each before submission)

| Claim | Source |
|-------|--------|
| naive / seasonal-naive / drift are the standard benchmark set | Hyndman & Athanasopoulos, *FPP3*, §5.2 |
| simple methods frequently beat sophisticated ones | Makridakis et al., M4 (2018, 2020) |
| TPE as a hyperparameter sampler | Bergstra, Bardenet, Bengio & Kégl (2011), NeurIPS |
| random search outperforms grid search | Bergstra & Bengio (2012), *JMLR* 13 |
| Optuna's define-by-run design | Akiba et al. (2019), KDD |
| rolling-origin evaluation for time series | Hyndman & Athanasopoulos §5.10; Tashman (2000), *IJF* 16(4) |
| regularised linear models as a tabular baseline | Hastie, Tibshirani & Friedman, *ESL* ch. 3 |

**Every entry above is a lead to verify, not a verified reference.** Check page
numbers, exact titles, and that the claim actually appears where stated. Do not
submit an unverified citation.

### NOT citable — argue these differently

- **"50–200 trials is conventional."** This is practitioner folklore. No paper
  prescribes a trial count, because the requirement depends on the search space.
  **Use the convergence evidence instead** (below).
- **The 3× extrapolation bound** on Ridge predictions. Invented for this project.
- **The `confidence` index** in the serving tool — 0.5/0.5 weights, 70/40 tier
  cutoffs, both arbitrary. Describe as a heuristic ordinal hint; never imply a
  calibrated probability.

## Justifying the trial budget without a citation

Rather than appealing to a convention that does not exist, the tuner records the
running best CV score per trial (`cv_convergence.csv`) and reports the trial after
which improvement fell below 0.1% relative (`plateau_trial`).

**The claim to write:**

> The search budget was set to 100 trials per configuration. The best
> cross-validated objective plateaued after approximately N trials (Figure X),
> indicating the budget was sufficient for this search space.

This is stronger than a citation: it is evidence from the actual experiment, and it
can be shown as a figure. An examiner cannot object that the source was misread.

## Why K-fold cross-validation would be invalid

State this explicitly — it demonstrates the choice was reasoned, not defaulted.

Standard K-fold shuffles rows into folds. On a time series that permits a model to
train on 2026-06 and predict 2026-03, which is not forecasting. Expanding-window
(rolling-origin) evaluation instead grows the training window forward and validates
on the block immediately after it, so the model never sees a period later than the
one it predicts.

**A second subtlety worth one sentence:** rows here are *brand-months*, so splitting
row-wise would place the same month in both training and validation for different
brands. Splits are therefore on distinct **periods**, not rows.

Verified on danskvand: training grows 203 → 319 → 435 → 551 rows across four folds
while validation remains a fixed forward block.

The test split is untouched throughout — CV operates strictly within train+val.

## The objective choice, resolved by measurement

The original tuner optimised WMAPE only. Given that WMAPE and median MAPE disagree
repeatedly in this project (see `srq1-pooled-vs-per-category.md` and
`srq1-model-ladder-and-baselines.md`), optimising one silently favours it.

**Every configuration is now tuned twice**, once per objective. Two possible
outcomes, both reportable:

- **Same model selected** → the objective choice was immaterial, and saying so
  closes the question with evidence.
- **Different model selected** → the magnitude is measured, and the thesis reports
  which objective was chosen for the headline results and what it cost on the other.

Either way an implicit choice becomes a stated and evidenced one. `cv_summary.md`
carries the comparison table.

### The disagreement is PREDICTED by theory, not an anomaly (verified 2026-08-23)

This is the most useful thing source verification has returned for SRQ1, because it
turns a recurring empirical oddity into a result with a name and a citation.

**Gneiting (2011, *JASA* 106(494), pp. 746, 752, 758)** proves that a scoring
function determines *which functional of the predictive distribution* is optimal:

| Loss | Optimal point forecast |
|---|---|
| Absolute error | the **median** |
| Pointwise **absolute percentage error** | the **(−1)-median** — the median of a density reweighted by `y⁻¹` |
| **WMAPE** (aggregate before dividing) | equivalent to minimising MAE ⇒ the **standard median** |

The `(−1)`-median is pulled toward zero, because dividing by a small actual
amplifies the penalty. **A model tuned on a MAPE-family objective therefore
systematically underforecasts** — by construction, not by accident.

**Three things this explains at once:**

1. **Why WMAPE and median MAPE disagree by up to 20pp** across three independent
   analyses in this project. They are estimates of *different functionals*. There
   was never a reason to expect them to agree.
2. **Why tuning for medMAPE costs 8–13pp of WMAPE and buys only 2–3pp of medMAPE.**
   The medMAPE-tuned model is targeting the `(−1)`-median and underforecasting;
   WMAPE penalises exactly that. The asymmetry of the trade is the theory's
   signature, not a quirk of the search.
3. **Why WMAPE is the defensible headline metric.** Not merely because it is
   volume-weighted and robust at zero, but because **it is consistent for the
   standard median**, which is the quantity a demand planner actually wants.

**Write it this way.** "We report WMAPE because it is standard in retail" is weak.
"We report WMAPE because it is *consistent for the median of the predictive
distribution, whereas pointwise MAPE optimisation is consistent for the
(−1)-median and systematically underforecasts* (Gneiting, 2011)" is a
methodological argument.

**One honest caveat when citing:** Gneiting never writes "WAPE" or "WMAPE". The
step from his APE result to WMAPE is a short algebraic one — the denominator
`Σ|yₜ|` is constant across candidate models on a fixed evaluation sample, so
minimising WMAPE is minimising Σ|error| — and **we must state that step ourselves
rather than implying he made it.**

## Honest limitations to state

1. **Single seed.** All results use seed 42. A seed sweep would establish whether
   selected configurations are stable; not yet run (P0040 task 11).
2. **No nested CV.** Hyperparameters are selected by CV and the winner evaluated on
   a held-out test split — standard practice, but not fully nested, so the reported
   test score is a mildly optimistic estimate of generalisation.
3. **The dual-objective result is a within-sample comparison of objectives**, not
   a claim about which metric a business should optimise. Gneiting's argument says
   what each objective *targets*; which target is right depends on the decision the
   forecast feeds, which this thesis does not model.
4. **Search space bounds were chosen, not searched.** `n_estimators` 200–1200,
   `learning_rate` 0.01–0.15, etc. are reasonable ranges but not themselves
   justified by experiment. If a selected value sits at a boundary, that indicates
   the range was too narrow and should be reported.

Stating limitation 3 is worth doing: it is the kind of thing an examiner notices in
the parameters table, and pre-empting it costs a sentence.

## Related

- `srq1-model-ladder-and-baselines.md` — which models and why
- `srq1-pooled-vs-per-category.md` — the pooled result
- `04_thesis_results/srq1/cv_summary.md` — CV-tuned results
- `04_thesis_results/srq1/cv_convergence.csv` — the plateau evidence
- `plans/P0040_2026-08-20_prometheus-scenarios-d-e/findings.md` — F58–F62
