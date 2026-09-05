<!-- PROSE STRIPPED 2026-09-01 (P0044); ARGUMENT BULLETS REBUILT 2026-09-05 (P0045).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-05_19-52_complete-review-pass/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 9 — Discussion

> **P0045 (2026-09-05) — this chapter's prose is the most stale in the thesis.**
> The 19-52 snapshot's §9.1 still reports: LLM-as-Judge GPT-4o N=50 scores (**the judge
> was dropped**), the retail-chain grain (**deleted by DEC-GRAIN / P0035**), the SRQ4
> code-as-action baseline as "not executed" (**it has run and produced paid results**),
> a ≤8 GB budget (**measured 4096 MB**), and 2026-06 WMAPE figures that every current
> results file contradicts.
> §9.2–§9.5 below were never prose and remain the reference form for the whole corpus.
> Fix §9.1 in the .docx; the bullets below record what is *currently* true.

> **P0044 OPEN (2026-09-01): RAM figure needs reconciling.** This file states an
> 8 GB budget. That number is a project assumption, not a sourced one -- Ng (2017)
> argues memory is the binding design variable, not that SMEs get 8 GB. Manifold's
> production Prometheus E2B template is provisioned at a **measured 4096 MB**
> (`fxe7gzkqjupdhbx4uvpr`, verified live 2026-09-01). Prefer the measured figure.
> All results hold under the tighter bound (serving 36.8 MB, refit ~37 MB).
> See `plans/P0044_2026-09-01_17-10_resource-measurement-and-retrain-arms/findings.md` F22-F23.

> Status: DRAFT written from real results 2026-06-24 (§9.1 interpretation; §9.2/§9.4
> aligned to actual findings). Grounded in thesis/data/_05_results_srq1/ and
> _06_results_srq2/. SRQ3 remains an assessment; SRQ4 is partial (ML-vs-ARIMA done;
> code-as-action baseline needs an execution sandbox). Pending human review.
> Last updated: 2026-06-24

---

## 9.1 Interpretation of findings

### 9.1.1 SRQ1: Forecasting accuracy under constraints

**Claims**
- Tuned **XGBoost** is the best model in every category, ahead of LightGBM, Ridge and
  SeasonalNaive — gradient boosting over engineered lag/rolling/calendar features is the
  strongest lightweight family for this monthly FMCG panel
- **RTD remains hardest**: short, volatile, promotion-blind series
- The RAM constraint is **non-binding at this data scale** — peak RAM in tens of MB,
  sub-second inference. The accuracy-optimal model also fits the budget with no compromise
- **SHAP attributes forecasts chiefly to `lag_1` and `weighted_distribution`** — consistent
  with retail demand dynamics, lending face validity

**Warrant**
- The budget binds the model-selection **space** (transformers excluded up front), not the
  realised footprint. Say this — it is the honest reading and it is still a result
- Model ladder rationale → [[srq1-model-ladder-and-baselines]]
- Pooled vs per-category, and the metric disagreement it exposed
  → [[srq1-pooled-vs-per-category]]

**Evidence**
- `04_thesis_results/srq1/cv_metrics.csv` — **the only current source for WMAPE figures**

**Open — the snapshot prose for this section is stale in three ways**
- **Numbers.** It cites CSD 16.5 / danskvand 22.0 / energidrikke 11.4 / RTD 31.0. Current
  values are **15.2 / 20.9 / 13.0 / 36.1** (staleness audit, 2026-08-22). RTD is off by
  5.1pp and moves the wrong way
- **Grain.** The chain-granularity paragraph ("disaggregating to a retail-chain dimension
  multiplied training rows roughly sixfold…") describes a grain **deleted from the project**
  by DEC-GRAIN (Enrico, 2026-07-12) and removed from code and results by P0035. Brand ×
  month is the locked grain. This passage must be cut or explicitly reframed as a
  documented limitation / future work — it cannot stand as a finding
- **RAM.** "≤8 GB" → measured 4096 MB (P0044 F22-F23)

### 9.1.2 SRQ2: Synthesis quality

**Claims**
- The deterministic synthesis core produces **well-to-conservatively calibrated** ensemble
  intervals — empirical coverage 80–98% against a 90% nominal
- The composite confidence score **skews to Moderate with no High-confidence forecasts**.
  This is an artefact of weighting interval *tightness* heavily while the conformal 90%
  interval is deliberately wide
- **The tier cut-offs need recalibration, not the forecasts** — a precise and defensible
  distinction worth keeping

**Warrant**
- Coverage is measured on a held-out test period rather than assumed from the conformal
  guarantee, because exchangeability is violated by temporal data (Ch2 §2.5; Barber et
  al. 2023)
- Tool-interface mechanics → [[sample-size-and-tool-interface-rationale]] §6

**Open**
- **The entire LLM-as-Judge comparison in the snapshot prose is void.** It reports GPT-4o
  judging N=50 on actionability 4.00 vs 2.14, relevance 4.00 vs 3.28, clarity 4.34 vs
  3.46, calibration 3.74 vs 3.46, accuracy 2.96 vs 3.42. **The judge was dropped**
  → [[srq4-experiment-design-rationale]] §7. No model now judges another model's output
  (Ch1 §1.3 states this explicitly). Every one of those figures must come out
- What survives the deletion is the *observation* that turning numbers into prose can
  drift from a strict reading of the inputs — a usefulness/precision trade-off. Keep the
  point; it now needs a programmatic measure, not a judge score

### 9.1.3 SRQ3: Integration readiness

**Claims**
- SRQ3 is answered as an **integration-readiness assessment, not a live integration**
- The substrate is integration-ready in the Ch3/Ch5 senses: exposed through a structured,
  reproducible interface (committed scripts, deterministic seeds, versioned artefacts),
  emitting point forecasts + calibrated intervals + a confidence tier suitable for an
  agent tool call
- **The remaining gap is operational (credentials, a dev-merge into the Graph Engine),
  not architectural** — this is the sharpest sentence in the section and should survive

**Open**
- The snapshot says "production access to the Prometheus platform was not available and
  was not required". **Ch1 §1.3 in the same snapshot now says the SRQ2 tool is registered
  with and executed inside the production system as part of SRQ4.** These two statements
  cannot both be current. Ch1 describes the newer design → [[prometheus-scenarios-design-rationale]].
  Reconcile in the .docx before anything else in this section is edited
- P0044 F8: observability/traceability **is** implemented but never **evaluated**. If SRQ3
  claims it as a measured capability, that is the real gap

### 9.1.4 SRQ4: dedicated ML vs the LLM/traditional baselines

**Claims**
- Against the **traditional statistical baseline**, dedicated ML (XGBoost) beats ARIMA in
  three of four categories; only danskvand is better served by an additive Prophet model
- So dedicated lightweight ML is, on balance, justified over classical forecasting
- The **information ladder** is the current SRQ4 frame: A (plain LLM) → B (LLM + data &
  code execution) → C (LLM + trained models). A→B measures what data access buys;
  **B→C measures what the thesis artefact adds**

**Warrant**
- Three-arm design and the same-base-model control → [[srq4-experiment-design-rationale]] §1
- Sample design is brands × repeats, not one brand × many repeats → same note, §3
- Scenario B's ~40× token cost is **structural, not incidental** — mechanism measured
  → [[srq4-first-results-and-interpretation]] §3

**Evidence**
- First paid results 2026-08-19 (HARBOE, actual 4,778,907 units)
  → [[srq4-first-results-and-interpretation]] §1–2

**Open**
- The snapshot says the code-as-action baseline "was *not* executed: it requires a secure
  execution sandbox (E2B) that is not configured". **Superseded** — the ladder has run at
  pilot scale and produced paid results. This section is describing a state the project
  left behind
- The ARIMA margins quoted (7.7 / 4.3 / 17.2 pp) are computed from **two stale numbers
  each** (staleness audit): current ARIMA is CSD 21.8, danskvand 33.5, energidrikke 19.4,
  RTD 53.3. Every margin must be recomputed, not adjusted
- **What can and cannot be claimed at n=6** → [[srq4-first-results-and-interpretation]] §6.
  State the boundary explicitly rather than letting the reader infer it
- The "arm" vocabulary and any A/B/C lettering running the other way must not reappear
  (`.claude/rules/repo-tier-structure.md`)

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
- **P0045 flags on the tables above (not edited here — they are the reference form):**
  - DP1 cites "≤8 GB" and per-model RAM (Ridge 1.5, LightGBM 18.7, XGBoost 0.2 MB).
    Those are the **tracemalloc** figures; Ch5 now reports **RSS** (XGBoost ~15,
    LightGBM ~7, Ridge <1 MB) because tracemalloc misses native allocations. Pick one
    instrument and say which
  - DP2's coverage range (80–98% vs 90% nominal) is consistent with §9.1.2 — keep
  - §9.2.2 has **two headings numbered 9.2.2** (design principles, then novelty claims)
  - Novelty claims and §9.4 limitations both cite the ≤8 GB constraint and the
    LLM-as-Judge N=50 evaluation. Both are void → see the banner
  - §9.4 "if Nielsen access was delayed, fallback dataset may reduce ecological validity"
    is a hypothetical that never happened — cut it
  - §9.4 should gain the real limitations: n=6 pilot scale
    ([[srq4-first-results-and-interpretation]] §6), the one-month/95-row validation
    window (P0044), and seed sensitivity of 3.97pp wMAPE (P0044 F21), which is larger
    than several effects this chapter reports
- ✅ Design principles table added (section 9.2.2) — content mirrors Ch.10 section 10.2; values will be filled after empirical results

---

## Writing-notes wired into this chapter (P0045)

- [[srq4-first-results-and-interpretation]] — §9.1.4 the information ladder, B-vs-C, the
  structural token-cost asymmetry, and what n=6 cannot claim
- [[srq1-model-ladder-and-baselines]] — §9.1.1 why the substrate contains what it does
- [[srq1-pooled-vs-per-category]] — §9.1.1 specialisation, and the metric disagreement
- [[srq4-experiment-design-rationale]] — §9.1.2 LLM-as-judge dropped (§7); §9.1.4 arm design
- [[prometheus-scenarios-design-rationale]] — §9.1.3 what the production rungs add
- [[sample-size-and-tool-interface-rationale]] — §9.4 limitations, sample-size boundary
