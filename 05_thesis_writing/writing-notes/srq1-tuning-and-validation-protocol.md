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

**Independently confirmed 2026-08-23 (HPO-07).** A source-level check of Bergstra
et al. (2011), Bergstra & Bengio (2012), Snoek et al. (2012) and Akiba et al. (2019)
found **no support anywhere** for a 50–200 trial convention: "a classic practitioner
rule of thumb with no rigorous support in academic literature". The required budget
grows with search-space dimensionality. Our empirical plateau approach is the right
response, and the register entry stays UNSOURCEABLE by design rather than by omission.

**A related trap (HPO-08):** do not attribute the plateau *criterion* to Snoek et al.
They evaluate over **fixed budgets** (50 or 100 trials, or wall-time) and define no
stopping rule based on flattening curves. The convergence criterion is **our design
decision** — which is fine, and must be presented as such.

**Two attributions to keep straight (HPO-04):**

| Cite | For |
|---|---|
| **Bergstra et al. (2011), p. 2549** | the **mathematics** of TPE — the l(x)/g(x) density split at quantile γ |
| **Akiba et al. (2019), p. 2623** | the **Optuna software** — define-by-run API, pruning, distribution |

Citing Akiba for the TPE formulation is a misattribution: that paper explicitly
attributes the algorithm to Bergstra. Also worth one sentence as a limitation —
Bergstra et al. note SMBO **can underperform random search** when the surrogate is
misspecified, which is a real caveat given we never tested random search as a control.

## Why expanding-window CV, and the boundary the literature actually draws

**Do NOT write "K-fold cross-validation is invalid for time series."** Source
verification (2026-08-23, CV-04) established that this common claim is **false as
stated**, and it is the kind of overreach an examiner who knows the field will catch.

**Bergmeir, Hyndman & Koo (2018, *CSDA* 120, 70–83, Theorem 1) prove** that standard
K-fold CV *is* valid for purely autoregressive models whose errors are uncorrelated,
and is *more* data-efficient than out-of-sample splitting on stationary series.
Cerqueira et al. (2020) concur, noting CV is beneficial "when the time series is
stationary, or the sample size is small".

**So the argument must be conditional, and made on OUR data's properties, not on a
universal rule:**

> Standard K-fold cross-validation is valid for stationary autoregressive processes
> with uncorrelated residuals (Bergmeir et al., 2018). Monthly brand-level beverage
> demand does not satisfy that condition — the series are trended, seasonal, and
> non-stationary — and under non-stationarity, methods preserving temporal order give
> substantially more accurate estimates of generalisation loss (Cerqueira et al.,
> 2020). Expanding-window rolling-origin evaluation is therefore used.

**This is a stronger position than the absolute claim**, because it shows we know
where the boundary is and why our data falls on one side of it.

**Equally, do not write that expanding-window is "mathematically mandatory"** (CV-06,
also contradicted). No such proof exists. It is a **defensible design choice**;
sliding windows trade differently, discarding old data to adapt to structural breaks
(Tashman, 2000, p. 441). Say "chosen because", not "required by".

Standard K-fold shuffles rows into folds. On a time series that permits a model to
train on 2026-06 and predict 2026-03, which is not forecasting. Expanding-window
(rolling-origin) evaluation instead grows the training window forward and validates
on the block immediately after it, so the model never sees a period later than the
one it predicts.

**Sourcing for the scheme itself** (Tashman, 2000, *IJF* 16(4), 437–450, pp. 439–440),
verified: rolling-origin successively advances the forecast origin rather than relying
on a single split, which is vulnerable to "corruption by occurrences unique to that
origin". Tashman also distinguishes **updating** (adding data to the fit window) from
**recalibration** (re-estimating parameters), and prefers recalibration — *our folds
refit the model from scratch each time, so we recalibrate*, which is worth one sentence
because it is the preferred procedure and we happen to do it.

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
2. **No nested CV — and "mildly" is the wrong word (MS-04, verified 2026-08-23).**
   Hyperparameters are selected by CV and the winner evaluated on a held-out test
   split — standard practice, but not fully nested.

   **Cawley & Talbot (2010, *JMLR* 11(70), 2079–2107) is the citation, and it does
   not license the reassuring adjective.** They show model selection can overfit a
   noisy selection criterion exactly as training overfits data (pp. 2079, 2083), that
   the resulting bias is "of surprising magnitude", and that it can be "large enough
   to conceal even the true difference between state-of-the-art and uncompetitive
   learning algorithms" (p. 2102). They further show the bias persists **even when
   training, validation and test sets are strictly disjoint** (p. 2097).

   **Write:** *the reported test metrics are optimistically biased to an unquantifiable
   degree*, not "mildly optimistic". Naming the bias honestly costs nothing here —
   every model was selected under the same protocol, so the comparison between models
   is unaffected; it is the absolute level that is uncertain.
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
