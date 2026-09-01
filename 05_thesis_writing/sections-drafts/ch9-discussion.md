<!-- PROSE STRIPPED 2026-09-01 (P0044).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-01_18-50/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 9 — Discussion

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

### 9.1.2 SRQ2: Synthesis quality

### 9.1.3 SRQ3: Integration readiness

### 9.1.4 SRQ4: dedicated ML vs the LLM/traditional baselines

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
