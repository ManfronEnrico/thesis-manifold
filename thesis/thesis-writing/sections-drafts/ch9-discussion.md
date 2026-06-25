# Chapter 9 — Discussion
> Status: DRAFT written from real results 2026-06-24 (§9.1 interpretation; §9.2/§9.4
> aligned to actual findings). Grounded in thesis/data/_05_results_srq1/ and
> _06_results_srq2/. SRQ3 remains an assessment; SRQ4 is partial (ML-vs-ARIMA done;
> code-as-action baseline needs an execution sandbox). Pending human review.
> Last updated: 2026-06-24

---

## 9.1 Interpretation of findings

### 9.1.1 SRQ1: Forecasting accuracy under constraints

Tuned **XGBoost was the best model in every category**, ahead of LightGBM, Ridge,
and the SeasonalNaive baseline, confirming that gradient boosting over engineered
lag/rolling/calendar features is the strongest lightweight family for this monthly
FMCG panel. The selected per-category configurations reach test WMAPE of 16.5%
(CSD), 22.0% (danskvand), **11.4% (energidrikke, near the ≤15% industry target)**
and 31.0% (RTD). RTD remains hardest — short, volatile, promotion-blind series. A
central and somewhat counter-intuitive result is that **finer granularity does not
uniformly help**: disaggregating to a retail-chain dimension multiplied training
rows roughly sixfold yet improved accuracy only for danskvand, while CSD,
energidrikke and RTD forecast better at the aggregated brand level. This is a
signal-to-noise effect — more rows of noisier per-chain demand do not beat fewer
rows of a cleaner aggregate — and it motivates the per-category representation
choice (Ch6 §6.5.6). On the operational axis the **≤8 GB constraint is non-binding**
at this data scale: peak RAM is in the tens of MB for every model and inference is
sub-second, so the accuracy-optimal model also fits the budget with no compromise.
SHAP attributes forecasts chiefly to last-month sales (`lag_1`) and shelf
availability (`weighted_distribution`), which is consistent with retail demand
dynamics and lends face validity to the models. *Connect to: Edge AI / Efficient &
Green LLMs (the constraint is easily met); gradient-boosting-for-retail literature.*

### 9.1.2 SRQ2: Synthesis quality

The deterministic synthesis core produced **well-to-conservatively calibrated**
ensemble intervals (empirical coverage 80–98% against a 90% nominal), so the
uncertainty the system communicates is trustworthy. The composite confidence score
skewed to the Moderate tier with no High-confidence forecasts under the current
thresholds — an artefact of weighting interval *tightness* heavily while the
conformal 90% interval is deliberately wide; the tier cut-offs, not the forecasts,
are what need recalibration. On recommendation quality, the **LLM synthesis added
clear value over a rule-based template**: GPT-4o (LLM-as-Judge, N=50) scored it
higher on actionability (4.00 vs 2.14), relevance (4.00 vs 3.28), clarity (4.34 vs
3.46) and calibration (3.74 vs 3.46), with the template ahead only on accuracy
(3.42 vs 2.96). The weakest LLM dimension is therefore accuracy: turning numbers
into prose occasionally drifts from a strict reading of the inputs — a
usefulness/precision trade-off, and the clearest target for prompt hardening.
*Connect to: Kuleshov 2018 (calibration); AI-augmented decision-making DSR 2024.*

### 9.1.3 SRQ3: Integration readiness

SRQ3 is addressed as an **integration-readiness assessment**, not a live
integration: production access to the Prometheus platform was not available and was
not required for the thesis, which runs entirely on a local Nielsen snapshot. The
forecasting substrate is nonetheless integration-ready in the senses Ch3/Ch5
specify — it is exposed through a structured, reproducible interface (committed
scripts, deterministic seeds, versioned artefacts) and emits point forecasts plus
calibrated intervals and a confidence tier suitable for an agent tool-call. The
remaining gap to active integration is operational (credentials, a dev-merge into
the Graph Engine), not architectural. *Connect to: Ch3/Ch5 integration-readiness
specification.*

### 9.1.4 SRQ4: dedicated ML vs the LLM/traditional baselines

Against the **traditional statistical baseline**, dedicated ML (XGBoost) beats
ARIMA in three of four categories (by 7.7, 4.3 and 17.2 pp WMAPE for CSD,
energidrikke, RTD), with only danskvand better served by an additive Prophet model
— so dedicated lightweight ML is, on balance, justified over classical forecasting.
The **code-as-action LLM baseline** central to the v4 SRQ4 — an LLM that writes and
self-corrects its own forecasting code — was *not* executed: it requires a secure
execution sandbox (E2B) that is not configured. This is the principal open piece of
the empirical SRQ4 answer and is carried as future work; what the present results
establish is the prior, weaker comparison (dedicated ML vs traditional, and LLM
synthesis vs template), both favouring the dedicated/structured approach on the
decision-relevant dimensions. *Connect to: Humans vs. LLMs (IJF 2024); code-as-action
(Wang et al. 2024).*

---

## 9.2 Theoretical contributions

### 9.2.1 Design knowledge contribution (DSR framing)
- The multi-agent framework constitutes a DSR artefact at two levels (Hevner et al. 2004; Artifact Types in IS Design Science, LNCS 2012):
  - **Instantiation level**: a working multi-agent system (System A) running on real retail CPG data
  - **Method/design-theory level**: 5 generalised design principles reusable beyond this specific retail context
- Cite: Hevner 2004, Peffers 2007, AI-Based DSR Framework 2024, Pathways for Design Research on AI 2024, Artifact Types in IS Design Science 2012

### 9.2.2 Design principles (generalised from thesis findings)

| # | Principle | Problem class | Evidence from this thesis |
|---|---|---|---|
| DP1 | **Sequential execution** | Multi-model ML pipelines within ≤8 GB RAM | Load → fit → predict → del → gc.collect(); measured peak RAM is tens of MB per model (Ridge 1.5, LightGBM 18.7, XGBoost 0.2 MB) — the 8 GB budget is non-binding at this data scale |
| DP2 | **Post-hoc calibration** | Confidence scoring in ML-based recommendation systems | Split-conformal interval calibrated on validation residuals; ensemble achieves 80–98% empirical coverage against a 90% nominal (CSD 96.6%) |
| DP4 | **LLM-as-synthesiser** | Translating ML outputs into managerial recommendations | Claude API synthesises a multi-model ensemble + confidence into an actionable natural language recommendation |
| DP5 | **Computational transparency** | AI pipeline artefacts evaluated for practical deployment | RAM and latency profiling reported alongside MAPE/RMSE; tracemalloc per component |

- Cite: Pathways for Design Research on AI 2024 (ISR), AI-Based DSR Framework 2024, AI-augmented decision making DSR 2024

### 9.2.2 Novelty claims
- First system to combine: LLM orchestration + ≤8GB constrained ML ensemble + MCDM synthesis + real retail CPG evaluation
- Memory profiling methodology for multi-component AI pipelines: replicable protocol contribution
- The ≤8GB constraint as a design principle, not an afterthought: demonstrates that SME-grade hardware is sufficient for meaningful AI-augmented BI

### 9.2.3 Contribution to IS literature
- Extends Pathways for Design Research on AI (ISR 2024): provides an instantiated AI artefact evaluated per the editorial's recommended dimensions
- Extends AI-augmented decision making design principles (2024): applies and validates principles in a retail CPG context

---

## 9.3 Practical implications

- For Manifold AI: validated architecture for integrating predictive analytics into the existing descriptive AI Colleague product
- For SME retailers: demonstrates that AI-augmented demand forecasting does not require cloud-scale compute
- For IS practitioners: memory profiling methodology is directly transferable to other ML pipeline deployments

---

## 9.4 Limitations

- Single company/context: Nielsen CSD data from one company's clients — generalisability untested
- Data access dependency: if Nielsen access was delayed, fallback dataset may reduce ecological validity
- LLM non-determinism: claude-sonnet-4-6 at temperature=0 is near-deterministic but not fully; evaluation may not fully replicate
- Evaluation scope: LLM-as-Judge N=50 is statistically modest; significance claims are indicative
- DSR single-cycle: full ADR would require multiple build-evaluate-reflect cycles; thesis completes one cycle

---

## 9.5 Future research directions

- Multi-agent memory sharing: can agents share intermediate results to reduce redundant computation?
- Real-time streaming: adapting the pipeline for continuous data ingestion vs. batch weekly
- Cross-retailer generalisation: test on a different FMCG category or market
- Full DSR second cycle: implement design principle refinements identified in this evaluation and re-evaluate

---

## Outstanding decisions

- Depth of theoretical contribution section: depends on how strong the empirical results are
- ✅ Design principles table added (section 9.2.2) — content mirrors Ch.10 section 10.2; values will be filled after empirical results
