---
pid: P0041
created: 2026_08_22-16_27
updated: 2026_08_22-18_00
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
| C3 | Split-conformal prediction produces valid distribution-free prediction intervals | Every served forecast carries a 90% conformal interval; core SRQ2 uncertainty claim | `UNSOURCED` | Possibly Lei, G'Sell, Rinaldo, Tibshirani & Wasserman (2018) *JASA*, "Distribution-Free Predictive Inference for Regression"; or Shafer & Vovk (2008) *JMLR* tutorial; or Vovk, Gammerman & Shafer (2005) book | Need the canonical citation for **split** (inductive) conformal specifically, not conformal prediction generally. Also useful: any source on conformal methods for **time series**, where exchangeability is violated — this is a known weakness of our application and we would rather cite the limitation than ignore it. |
| C4 | Global (pooled) forecasting models can outperform local (per-series) models, especially for short series | The pooled-vs-per-category result: pooling wins below ~750–1000 training rows, loses above | `UNSOURCED` | Possibly Montero-Manso & Hyndman (2021) *IJF*, "Principles and algorithms for forecasting groups of time series"; M5 competition papers | **Highest value in this register.** We have a clean measured result (sign flips once, replicated across two algorithms) that is currently presented as if novel. Need the global-vs-local literature to position it. Also of interest: does any source give a **sample-size threshold** at which global beats local? |
| A5 | WMAPE (weighted MAPE / WAPE) as an appropriate metric for demand forecasting | The headline metric throughout | `UNSOURCED` | — | Need (a) a definition source and (b) a justification for volume weighting in a retail/demand context. Also: what is the standard **name**? We have seen WMAPE, WAPE and weighted MAPE used interchangeably. |
| A6 | MAPE is undefined/unstable near zero actuals; median APE is more robust | Justifies excluding 40% of brands as unscorable; justifies medMAPE for per-series baselines; explains a 9.3×10¹⁰ artifact in our own results | `UNSOURCED` | Possibly Hyndman & Koehler (2006) *IJF* 22(4), "Another look at measures of forecast accuracy" | Likely the standard reference but **unverified**. Does it recommend MASE over MAPE? If so we may need to justify not using MASE. |

---

## GROUP 2 — Prospective sources needing validation

A specific source is proposed but **nobody has opened it**. Please confirm or refute.

| ID | Claim | Where used | Status | Prospective source | What to verify |
|----|-------|-----------|--------|--------------------|----------------|
| A1 | Naive, seasonal-naive and drift are the standard forecasting benchmark set | Justifies adding four benchmarks; justifies calling a result "unbenchmarked" without them | `PROSPECTIVE` | Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed., §5.2 | Open-access at otexts.com/fpp3, so cheap to check. Confirm the section number in the **3rd** edition and the exact framing. |
| A2 | Sophisticated methods frequently fail to beat simple benchmarks | Contextualises our finding that seasonal-naive (27.3% WMAPE) beats every tuned model on one category | `PROSPECTIVE` | Makridakis, Spiliotis & Assimakopoulos, M4 competition, *IJF* 2018 and/or 2020 | **Check which paper carries which claim** — M4 results vs the M5 competition. We need the one making the simple-beats-complex point. This citation turns an awkward result into a contextualised one, so precision matters. |
| A3 | Rolling-origin / expanding-window evaluation is the correct CV scheme for time series | Justifies our 4-fold expanding-window CV | `PROSPECTIVE` | (a) Hyndman & Athanasopoulos §5.10 "Time series cross-validation"; (b) Tashman (2000) *IJF* 16(4) | (a) is probably safe. **Verify (b) fully** — volume, issue, year, and whether it actually concerns rolling-origin evaluation. |
| B1 | Tree-structured Parzen Estimator as a Bayesian HPO method | We use Optuna's TPE sampler | `PROSPECTIVE` | Bergstra, Bardenet, Bengio & Kégl (2011), NeurIPS, "Algorithms for Hyper-Parameter Optimization" | Confirm authors and venue. |
| B2 | Random search outperforms grid search for HPO | Only needed if the thesis explains why not grid search | `PROSPECTIVE` | Bergstra & Bengio (2012) *JMLR* 13, "Random Search for Hyper-Parameter Optimization" | Confirm. Low priority — may not be needed. |
| B3 | Optuna's define-by-run design | Tool citation | `PROSPECTIVE` | Akiba, Sano, Yanase, Ohta & Koyama (2019), KDD | Confirm. |
| C1 | Regularised linear models are a standard tabular baseline | Justifies the Ridge rung in the model ladder | `PROSPECTIVE` | Hastie, Tibshirani & Friedman, *Elements of Statistical Learning*, ch. 3 | ESL ch. 3 certainly covers ridge regression. **Less certain** that it frames it as a standard comparison baseline, which is the actual claim. A better source may exist. |

---

## GROUP 3 — Gaps worth filling (supporting claims, no source yet)

| ID | Claim | Where used | Status | Notes for researcher |
|----|-------|-----------|--------|----------------------|
| A4 | K-fold cross-validation is invalid for time series because it permits training on future observations | Methodology justification for expanding-window CV | `UNSOURCED` | May be implicit in A3 rather than separately citable. **Question:** does a source state the invalidity explicitly, or should we present it as a logical consequence? |
| B5 | Selecting hyperparameters and evaluating on the same data yields optimistically biased performance estimates | Stated as a limitation: our protocol is CV-select + held-out test, not fully nested | `UNSOURCED` | Possibly Cawley & Talbot (2010) *JMLR*, "On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation". Verify. |
| C2 | Feature importance (e.g. SHAP) measures what a fitted model used, not which features should be selected | A feature ranked #2 by SHAP was dropped because removing it improved held-out accuracy in 3 of 4 categories | `UNSOURCED` | Lundberg & Lee (2017) covers SHAP itself. The **attribution ≠ selection** point needs its own source. We have our own measured instance, so a source for the general principle would suffice. |
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
