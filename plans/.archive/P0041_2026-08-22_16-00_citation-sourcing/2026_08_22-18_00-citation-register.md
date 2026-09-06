---
pid: P0041
created: 2026_08_22-16_27
updated: 2026_08_23-20_00
purpose: Self-contained citation register for NotebookLM research. Pass this file directly.
---

# Citation register — for source research and validation

**This file is written to be handed to NotebookLM as-is.** It contains the thesis
context, every claim needing a source, the prospective source where one exists, and
a status per claim.

---

## Context for the researcher

**Thesis:** CBS Master's, 2026. Demand forecasting for Danish FMCG beverages
(Nielsen retail scanner data), combined with LLM agent integration.

**Data:** ~230 brand-category series across four categories (carbonated soft drinks,
bottled water, energy drinks, ready-to-drink). Monthly observations, brand × month
grain, forecast horizon H=3 months. Training sets range from ~460 to ~1,800
brand-month rows per category.

**Methods used:** LightGBM and XGBoost (tuned via Optuna TPE), Ridge regression,
ARIMA, Prophet, and naive/seasonal-naive/drift benchmarks. Evaluation by WMAPE
(volume-weighted) and median MAPE. Split-conformal prediction intervals. An LLM agent
consumes forecasts through a structured tool interface.

**Research questions this supports:**
- **SRQ1** — accuracy, memory efficiency, and category specialization trade-offs
- **SRQ2** — a structured tool interface exposing forecasts with uncertainty and traceability
- **SRQ4** — comparing LLM scenarios with and without access to trained models

**What is needed from research:** for each claim below, either (a) confirm the
prospective source contains it and give the precise location, (b) supply a better
source, or (c) confirm that no suitable academic source exists so the claim can be
argued empirically or dropped.

**Read alongside `2026_08_22-18_00-context-drift-addendum.md`** — the project-overview and research-question files are stale in nine respects, two of which would misdirect research (LLM-as-judge is dropped; Prometheus access has landed).

**Please flag any prospective source that does NOT support its claim.** These were
proposed by an AI assistant and are explicitly unverified. One claim in this register
(B4) was already found to be fabricated convention.

---

## Status legend

| Status | Meaning | Action needed |
|--------|---------|---------------|
| `PROSPECTIVE` | Source suggested, nobody has checked it | **Validate or refute** |
| `UNSOURCED` | No source identified | **Find one** |
| `UNSOURCEABLE` | Investigated; no academic source exists | None — argued empirically |
| `OURS` | The thesis's own contribution | None — must never be cited |

---

## GROUP 1 — Critical gaps (no source at all, load-bearing claims)

These support central thesis claims and currently have nothing behind them.
**Highest priority.**

| ID | Claim needing a source | Where used | Status | Prospective source | Notes for researcher |
|----|------------------------|-----------|--------|--------------------|----------------------|
| C3 | Split-conformal prediction produces valid distribution-free prediction intervals | Every served forecast carries a 90% conformal interval; core SRQ2 uncertainty claim | **`VERIFIED` 2026-08-23** | **Papadopoulos, Proedrou, Vovk & Gammerman (2002),** *Machine Learning: ECML 2002*, LNAI 2430, Springer, **pp. 345-356** (inductive/split conformal, origin). **Lei, G'Sell, Rinaldo, Tibshirani & Wasserman (2018),** ***Journal of the American Statistical Association*, 113(523), 1094-1111** (Algorithm 2 + Theorem 2). **Barber, Candes, Ramdas & Tibshirani (2023)** (beyond exchangeability). | **Two corrections applied.** Lei et al. is **JASA 113(523), 1094-1111**, NOT JRSS-B 80(5) 1097-1121 as previously recorded -- wrong journal entirely. Papadopoulos is **pp. 345-356**, not 327-338. **Three qualifications are mandatory when citing:** (1) coverage is **marginal, not conditional** (Lei, Remark 3) -- an average over cells, not a per-brand promise; (2) it assumes **exchangeability, which monthly demand violates** -- Barber et al. show unweighted split conformal loses coverage under drift and only *bounds* the loss; (3) the interval uses the **ceil((n+1)(1-alpha))/n** quantile, not the nominal one -- **our code did not, and was fixed 2026-08-23.** |
| C4 | Global (pooled) forecasting models can outperform local (per-series) models, especially for short series | The pooled-vs-per-category result: pooling wins below ~750-1000 training rows, loses above | **`VERIFIED for theory` / `DO NOT CITE for the threshold`** | **Montero-Manso & Hyndman (2021),** *International Journal of Forecasting*, **37(4), 1632-1653** | **Verified: the definitions (p. 1634), the non-homogeneity result (Prop. 1), the complexity argument (Prop. 2, p. 1638) and the short-series rationale (p. 1633) all hold.** **But the paper contains NO 750-1000 observation threshold.** Attributing our number to it would be, in the reviewer's words, *'a misattribution and a severe factual overstatement'*. **Cite it for WHY a crossover should exist; report the NUMBER as ours alone.** Two qualifications: Prop. 2's bound assumes **cross-series independence** (false for brands in one category), and Prop. 1's equivalence requires global models to use **relatively longer memory** than local ones -- a possible confound in our comparison, which uses an identical lag set for both. |
| A5 | WMAPE (weighted MAPE / WAPE) as an appropriate metric for demand forecasting | The headline metric throughout | `UNSOURCED` | — | Need (a) a definition source and (b) a justification for volume weighting in a retail/demand context. Also: what is the standard **name**? We have seen WMAPE, WAPE and weighted MAPE used interchangeably. |
| A6 | MAPE is undefined/unstable near zero actuals; a zero-stable metric is required | Justifies WMAPE as primary; explains the 9.3x10^10 artifact in our own results | **`VERIFIED` 2026-08-23, with a caveat that changed our practice** | **Hyndman & Koehler (2006),** *International Journal of Forecasting*, **22(4)**, pp. 679-688 (see esp. **p. 683**, and pp. 684-685 for MASE) | **Verified on the instability claim (p. 683).** **But it does NOT justify excluding zero-actual brands -- it explicitly criticises that.** They call it *'an artificial solution that is impossible to apply in practical situations'* (p. 683) and recommend zero-stable metrics instead of altering data to suit the metric. The earlier rationale recorded here ('justifies excluding 40% of brands') **inverted the source**. **Consequences:** (a) the exclusion is now applied to MAPE-family statistics only, never to WMAPE, which is defined at zero -- misapplying it had flipped the sign of a reported correlation; (b) they propose **MASE** (pp. 684-685) as the scale-free cross-series measure, and **we report no scaled metric** -- an open gap, not yet closed. |
| A7 | Choice of error metric determines which functional of the predictive distribution is optimal | Explains the WMAPE-vs-medMAPE disagreement (up to 20pp, seen in three separate analyses) and the dual-objective tuning result | **`VERIFIED` 2026-08-23 — NEW ENTRY, was entirely unsourced** | **Gneiting (2011),** 'Making and Evaluating Point Forecasts', *Journal of the American Statistical Association*, **106(494)**, see **pp. 746, 752, 758** | **This converts an empirical curiosity into a theoretical finding.** Absolute-error loss is optimised by the **median** (p. 746). Pointwise APE loss is optimised by the **(-1)-median** -- a density reweighted by y^-1 -- which **systematically underforecasts** (pp. 746, 752). WMAPE aggregates before dividing, so minimising it on a fixed sample equals minimising MAE, consistent for the **standard** median. **Therefore our WMAPE/medMAPE gap is predicted, not anomalous**, and tuning for medMAPE costing 8-13pp of WMAPE is the expected direction. Caveat: Gneiting never uses the terms 'WAPE'/'WMAPE'; the bridge from APE to WMAPE is an algebraic step we must state ourselves. |

---

## GROUP 2 — Prospective sources needing validation

A specific source is proposed but **nobody has opened it**. Please confirm or refute.

| ID | Claim | Where used | Status | Prospective source | What to verify |
|----|-------|-----------|--------|--------------------|----------------|
| A1 | Mean, naive, seasonal-naive and drift are the standard benchmark set | Justifies the benchmark rung; justifies calling a result "unbenchmarked" without them | **`VERIFIED` 2026-08-23** | **Hyndman & Athanasopoulos (2021),** *Forecasting: Principles and Practice*, 3rd ed., **Section 5.2** (open access, otexts.com/fpp3) | Verified wording: *"Some forecasting methods are extremely simple and surprisingly effective. We will use four simple forecasting methods as benchmarks throughout this book"* and *"any forecasting methods we develop will be compared to these simple methods to ensure that the new method is better than these simple alternatives."* **An earlier draft quoted them as saying these "are the best we can do" -- that phrase is NOT in the source and was removed.** Write the four formulas out (all in Section 5.2). **Companion (BM-03/BM-04), Makridakis et al. (2018), p. 803:** of six pure ML entries in M4, none beat the Comb benchmark and only one beat Naive2 -- but the competition was **won by a hybrid** (Smyl ES-RNN, +9.4% over Comb), with a seven-method combination second. Cite BOTH halves: M4 is not "simple beats complex", it is "pure ML underperformed, combinations won". |
| A2 | Sophisticated methods frequently fail to beat simple benchmarks | Contextualises our finding that seasonal-naive (27.3% WMAPE) beats every tuned model on one category | `PROSPECTIVE` | Makridakis, Spiliotis & Assimakopoulos, M4 competition, *IJF* 2018 and/or 2020 | **Check which paper carries which claim** — M4 results vs the M5 competition. We need the one making the simple-beats-complex point. This citation turns an awkward result into a contextualised one, so precision matters. |
| A3 | Rolling-origin / expanding-window evaluation for non-stationary series | Justifies our 4-fold expanding-window CV | **`VERIFIED` 2026-08-23, with a boundary condition that must be stated** | **Tashman (2000),** *IJF* **16(4), 437-450**, pp. 439-440. **Cerqueira, Torgo & Mozetic (2020),** *Machine Learning* **109(11), 1997-2028**. **Bergmeir, Hyndman & Koo (2018),** *CSDA* **120, 70-83**, Theorem 1 | **DO NOT WRITE "K-fold is invalid for time series" -- that is false (CV-04).** Bergmeir et al. **prove** standard K-fold is valid for purely autoregressive models with uncorrelated errors, and Cerqueira et al. agree it helps on stationary or small samples. **The argument must be conditional**: our series are trended/seasonal/non-stationary, and under non-stationarity temporal-order-preserving methods estimate generalisation loss more accurately (Cerqueira). **Also do not write that expanding-window is "mathematically mandatory" (CV-06)** -- no such proof exists; it is a defensible choice, and sliding windows trade differently (Tashman, p. 441). Bonus: Tashman distinguishes **updating** from **recalibration** and prefers the latter -- our folds refit from scratch, so we recalibrate. Worth one sentence. |
| B1 | Tree-structured Parzen Estimator as a Bayesian HPO method | We use Optuna TPE sampler | **`VERIFIED` 2026-08-23** | **Bergstra, Bardenet, Bengio & Kegl (2011),** *NeurIPS* 24, **p. 2549** | Verified: TPE models p(x|y) via two non-parametric densities, l(x) below a quantile threshold y* and g(x) above, with EI proportional to (gamma + g(x)/l(x)(1-gamma))^-1. **Cite this for the MATHEMATICS of TPE, never Akiba et al. (see B3).** Limitation worth one sentence: Bergstra et al. note SMBO **can underperform random search** when the surrogate is misspecified -- and we never ran random search as a control. |
| B2 | Random search outperforms grid search for HPO | Only needed if the thesis explains why not grid search | `PROSPECTIVE` | Bergstra & Bengio (2012) *JMLR* 13, "Random Search for Hyper-Parameter Optimization" | Confirm. Low priority — may not be needed. |
| B3 | Optuna define-by-run design, pruning, distributed architecture | Tool citation | **`VERIFIED` 2026-08-23** | **Akiba, Sano, Yanase, Ohta & Koyama (2019),** KDD 19, **p. 2623** | Verified for the three design criteria (define-by-run API, efficient searching/pruning, versatile architecture). **Cite for the SOFTWARE ONLY.** The paper does not formulate TPE -- it explicitly attributes the algorithm to Bergstra et al. Citing Akiba for the TPE mathematics is a misattribution (HPO-04). |
| C1 | Ridge regression as a regularised linear baseline | Justifies the Ridge rung in the model ladder | **`VERIFIED` 2026-08-23, but the strong version is refuted** | **Hastie, Tibshirani & Friedman (2009),** *ESL* 2nd ed., **pp. 61-62** (Eq. 3.41, 3.42) | Verified for the definition: ridge minimises penalised RSS subject to an L2 coefficient-norm budget. **TREE-02 Contradicted: ESL contains NO normative rule that ridge is a baseline every tabular model "must beat".** Its merit is conditional on the data-generating process (dense vs sparse signals). Write "a foundational benchmark for regularised linear models", not "the standard every model must beat". **Also verified here (TREE-03, p. 307):** trees are invariant to strictly monotone transforms of the **predictors** -- the F54 citation. **TREE-05 Contradicted:** that invariance does NOT extend to the **target**; logging Y changes leaf means and boosting gradients, so it affects LightGBM too. |

---

## GROUP 3 — Gaps worth filling (supporting claims, no source yet)

| ID | Claim | Where used | Status | Notes for researcher |
|----|-------|-----------|--------|----------------------|
| A4 | K-fold cross-validation is invalid for time series because it permits training on future observations | Methodology justification for expanding-window CV | `UNSOURCED` | May be implicit in A3 rather than separately citable. **Question:** does a source state the invalidity explicitly, or should we present it as a logical consequence? |
| B5 | Selecting hyperparameters and evaluating on the same data yields optimistically biased estimates | Stated as a limitation: our protocol is not nested | **`VERIFIED` 2026-08-23 -- and it forbids the word we used** | **Cawley & Talbot (2010),** *JMLR* **11(70), 2079-2107**, pp. 2079, 2083, 2097, 2101-2102 | Verified on all three substantive points: model selection can overfit a noisy criterion exactly as training overfits data; re-using estimates for selection and evaluation biases the result; unbiased assessment needs nested CV. **MS-04: the phrase "mildly optimistic" must be struck.** Cawley & Talbot call the bias "of surprising magnitude", large enough to "conceal even the true difference between state-of-the-art and uncompetitive learning algorithms" (p. 2102), and show it persists **even with strictly disjoint train/val/test sets** (p. 2097). Write **"optimistically biased to an unquantifiable degree"**. |
| C2 | Feature attribution measures what a fitted model used, not which features to select | Justifies dropping `promo_intensity`; explains why a high-SHAP feature can be droppable | **`VERIFIED` 2026-08-23 -- and it invalidated our stated evidence** | **Lundberg & Lee (2017),** *NeurIPS* 30, **4765-4774** (pp. 1, 2, 4 Thm 1). **Guyon & Elisseeff (2003),** *JMLR* **3, 1157-1182**, pp. 1158, 1163-1164 | SHAP-01/02 verified (unified additive attribution; Shapley values uniquely satisfy local accuracy, missingness, consistency). SHAP-04 verified (relevant variables can be redundant; individually useless ones can be jointly useful). **SHAP-05 Contradicted -- Lundberg & Lee never evaluate feature pruning at all.** Never cite them for a selection result. **Consequence for our code:** `srq1_pooled.py` called a SHAP rank the "measured cost" of dropping `promo_intensity`. That is the exact relevance-vs-usefulness conflation Guyon & Elisseeff warn against. **Now actually measured** by refitting: dropping it costs +0.30/+0.27pp WMAPE on CSD, +1.44pp for XGBoost on energidrikke, and **HELPS by 1.36pp for LightGBM on energidrikke** -- better on 5 of 8 combinations. Conclusion unchanged, evidence corrected. |
| C5 | Intermittent / zero-inflated demand needs specialised estimators and categorisation, not exclusion | Justifies how we treat sparse brands; would replace the ad-hoc 1 unit/month volume floor | **`VERIFIED` 2026-08-23 -- NEW ENTRY, currently cited nowhere in the thesis** | **Syntetos & Boylan (2005),** *IJF* **21(2), 303-314**, p. 304. **Syntetos, Boylan & Croston (2005),** *JORS* **56(5), 495-503**, pp. 495, 499 | SBA bias correction (1 - alpha/2) on Croston estimator, verified. Demand categorisation into smooth/intermittent/erratic/lumpy at **p = 1.32** and **CV^2 = 0.49**, verified. **ID-04 Contradicted: they do NOT recommend excluding intermittent series** -- their whole contribution is estimators that forecast them. Same objection as Hyndman & Koehler on zero-exclusion (A6). **ADOPTED 2026-08-23 (Brian).** The p/CV^2 quadrants now replace the ad-hoc 1 unit/month volume floor: `srq1_demand_classes.py` classifies all 230 brands from train+val, and `srq1_pooled_perbrand.py` reports per demand class with **no exclusion at all**. The measurement that justified the swap: the floor removed **8 smooth brands** (well-behaved, merely small) while leaving **21 lumpy/intermittent** ones above it -- volume is a poor proxy for regularity. Distribution: 108 smooth, 79 erratic, 12 intermittent, 31 lumpy. **Caveat to state when citing:** the cut-offs were derived for Croston-type estimators (alpha = 0.15, lead time 1), not for gradient boosting on a brand-month panel -- use them as a principled partition of demand patterns, not as a claim the same accuracy ordering transfers. |
| C6 | Prophet design regime and why it underperforms here | Explains the Prophet baseline result | **`VERIFIED` 2026-08-23** | **Taylor & Letham (2018),** *The American Statistician* **72(1), 37-45**, pp. 37-38, 41 | Verified: additive decomposition y(t) = g(t) + s(t) + h(t) + eps (Eq. 1, p. 38); designed for non-specialist analysts at scale; targets piecewise trends, multiple seasonality, floating holidays. **PRO-04 Contradicted / PRO-05 Not Found: they never state Prophet is unsuitable for monthly data, and never show it flatlines.** Do not write either. **Use the mechanical argument instead:** at month grain weekly seasonality does not exist, holiday windows collapse (and we supply no holiday calendar), and yearly seasonality reduces to ~12 points the tabular models already capture via `month`/`quarter`/`lag_13`. We applied Prophet outside its design regime -- our limitation, not their documented defect. |
| C5 | Log transformation is appropriate for multiplicative relationships; tree models are invariant to monotone feature transforms | We found raw-unit features against a logged target break linear models while leaving trees unaffected | `UNSOURCED` | Two separate claims. The tree-invariance one is textbook (possibly ESL). The multiplicative-relationship one may be in a forecasting or econometrics text. |
| C6 | Prophet is designed for daily/sub-daily data with multiple seasonalities and performs poorly on short monthly series | We report Prophet failing badly (up to 972% WMAPE) and want to attribute it to fit-for-purpose rather than claim "Prophet is bad" | `UNSOURCED` | Taylor & Letham (2018) "Forecasting at Scale" is the Prophet paper — does it state the intended data regime? Any independent evaluation of Prophet on monthly data would also help. |
| C7 | Intermittent/zero-inflated demand is a distinct forecasting problem requiring different methods | We exclude brands with zero-sales test windows and want to justify treating them as out of scope rather than as a convenient omission | `UNSOURCED` | Croston (1972) is the classic intermittent-demand reference; Syntetos & Boylan have later work. Verify relevance. |

---

## GROUP 4 — Confirmed unsourceable

| ID | Claim | Status | Resolution |
|----|-------|--------|-----------|
| B4 | "Convention for hyperparameter search is 50–200 trials" | `UNSOURCEABLE` | **Asserted by an AI assistant as established fact. It is not.** No paper prescribes a trial count; the requirement depends on the search space. Replaced with an empirical argument: the tuner records the convergence curve and reports the trial at which the objective plateaued. **Still worth researching:** does any source describe a principled method for *determining* an adequate HPO budget (convergence-based stopping)? That would let the empirical argument cite a method. |

---

## GROUP 5 — Our own contributions (must NEVER carry a citation)

Recorded so no one attaches a source later by mistake.

| Claim | Note |
|-------|------|
| The 3× extrapolation bound on Ridge predictions | Arbitrary constant invented for this project. Both bounded and unbounded results are published. |
| The `confidence` index (0.5/0.5 weighting, 70/40 tier cutoffs) | Entirely arbitrary. Describe as a heuristic ordinal hint; never imply a calibrated probability. |
| The five/six-scenario ladder design | The thesis's own contribution. |
| The ~750–1000 training-row crossover for pooled vs per-category | Our measurement, interpolated from four data points. State as measured, not as a known threshold. |
| The 300% implausibility threshold for served metrics | A display choice, not an analysis parameter. |

---

## GROUP 6 — Areas where additional citation would strengthen the thesis

Not gaps in existing claims — **opportunities** where literature would add depth.
Offered as an open research brief.

| Area | Why it would help | Suggested search direction |
|------|-------------------|---------------------------|
| LLM agents with tool access for quantitative tasks | SRQ4 compares LLM scenarios with and without model access. Any prior work measuring whether tool access improves quantitative accuracy would position the contribution. | Tool-augmented LLMs; function calling; LLMs for time-series forecasting |
| Whether LLMs can forecast time series directly | Scenario A (LLM with no data) is a baseline we assume is weak. Literature would justify the assumption. | "LLMs as zero-shot time series forecasters"; recent work on LLM numerical reasoning |
| Communicating forecast uncertainty to decision-makers | SRQ2 concerns how a tool interface should expose uncertainty. Human-factors literature on uncertainty communication may transfer. | Forecast uncertainty communication; decision support systems |
| Does providing more context improve or degrade LLM output? | We plan to test whether richer payloads improve agent forecasts. Prior work on context dilution / long-context degradation is directly relevant. | Context length and performance; "lost in the middle"; prompt bloat |
| Retail demand forecasting practice in FMCG | Domain grounding for the problem framing. | Retail/FMCG demand forecasting; Nielsen scanner data studies |
| Model deployment footprint / efficiency trade-offs | SRQ1's memory-efficiency leg — we measure 3–4 MB models against hundreds of MB of agent runtime. | Efficient ML deployment; model size vs accuracy trade-offs |

---

## GROUP 7 — Literature-review disconnections (a DIFFERENT kind of problem)

Full detail in `2026_08_22-22_00-literature-review-audit.md`. These are **not** missing
citations. The sources exist and are correctly described. The problem is that the
thesis's own evidence now cuts against what Chapter 2 said they motivated.

| ID | Ch2 claim | Our evidence | Action |
|----|-----------|-------------|--------|
| D1 | M4 + Ahrens: combining models beats a single model | No ensemble built; one model served | Build `F_ensemble`, or state that combination was evaluated and deferred |
| D2 | Ceran et al.: ≤15% MAPE is the acceptable benchmark | Met on 2/4 categories **on WMAPE**; RTD ~2x over | **Verify which metric Ceran uses** — decides whether the target is met |
| D3 | Klee & Xia: stability is a production criterion | **Never measured** — no CV-across-runs exists | Measure it (cheap), or drop the claim |
| D4 | Ma et al.: no single model dominates | **Corroborated, strongly** | Strengthen — we can add a sample-size threshold Ma et al. do not offer |

## GROUP 8 — Gap claims to actively REFUTE

G1–G5 are assertions that no literature addresses X. One counterexample defeats each.
**Instruct NotebookLM to search FOR the thing we claim does not exist.**

| Gap | Claim | Refutation risk |
|-----|-------|-----------------|
| G2 | No head-to-head benchmark of these models under an explicit RAM budget in retail FMCG | **HIGH** — benchmark papers are common |
| G3 | No structured tool interface exposing ML forecasts with uncertainty to LLM agents | **HIGH** — fast-moving area, 2025–26 work likely |
| G1, G4, G5 | see the project overview | Medium |

Also verify **Bürger & Pauli (2024, EAAI)** — the "closest paper", on which the whole
novelty claim rests — and search for anything closer published since.

## Summary counts

| Status | Count |
|--------|------:|
| `UNSOURCED` — critical (Group 1) | 4 |
| `PROSPECTIVE` — needs validation (Group 2) | 7 |
| `UNSOURCED` — supporting (Group 3) | 6 |
| `UNSOURCEABLE` (Group 4) | 1 |
| `OURS` — never cite (Group 5) | 5 |
| Open research areas (Group 6) | 6 |

**Priority order for research:** Group 1 (C3, C4, A5, A6) → Group 2 validation →
Group 3 → Group 6.
