# Chapter 9 — Discussion
> Status: BULLET POINT SKELETON — not prose yet
> Last updated: 2026-03-14

---

## 9.1 Interpretation of findings

### 9.1.1 SRQ1: Forecasting accuracy under constraints
- Discuss which model family won and why (expected: gradient boosting due to feature richness)
- Interpret the RAM profile: was ≤8GB achievable? What was the binding constraint?
- Discuss trade-off between accuracy and RAM: does best-accuracy model fit within constraint, or is a sub-optimal model needed?
- Connect to: Edge AI paper, Efficient & Green LLMs paper, Cost-Aware 3PL paper

### 9.1.2 SRQ2: Synthesis quality
- Did calibrated confidence scores add value vs. raw model outputs?
- Was the LLM-as-Judge evaluation consistent? What were the weakest dimensions?
- Discuss the gap between calibration target (90%) and actual coverage — what drove under/over-coverage?
- Connect to: Kuleshov 2018, AI-augmented decision making DSR 2024

### 9.1.3 SRQ3: Consumer signal contribution
- Did Indeks Danmark signals improve MAPE? By how much?
- Which retailer types benefited most from consumer enrichment?
- Was the PCA + k-means segmentation meaningful? What do the clusters represent?
- Connect to: Customer Segmentation + Sales Prediction 2023, Model Averaging + DML 2024

### 9.1.4 SRQ4: AI vs. descriptive baseline
- Did the AI system outperform the Manifold descriptive analytics baseline on recommendation quality?
- What dimensions showed the largest gap?
- Was the improvement worth the computational and implementation complexity?
- Connect to: Humans vs. LLMs (IJF 2024), AI-Enhanced BI 2025, ML Business Decision Making

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
| DP1 | **Sequential execution** | Multi-model ML pipelines within ≤8 GB RAM | Load → fit → predict → del → gc.collect() keeps peak ≤ 512 MB/model; parallel would require ~1.5 GB simultaneously |
| DP2 | **Post-hoc calibration** | Confidence scoring in ML-based recommendation systems | Isotonic regression on held-out validation set; Kuleshov et al. (2018) method achieves ≥ 85% empirical coverage |
| DP3 | **Consumer signal integration** | Demand forecasting enrichment with survey data | PCA + k-means on Indeks Danmark → retailer demand index → MAPE improvement on SRQ3 ablation |
| DP4 | **LLM-as-synthesiser** | Translating ML outputs into managerial recommendations | Claude API synthesises 5-model ensemble + confidence + consumer context → actionable natural language recommendation |
| DP5 | **Computational transparency** | AI pipeline artefacts evaluated for practical deployment | RAM and latency profiling reported alongside MAPE/RMSE; tracemalloc per component |

- Cite: Pathways for Design Research on AI 2024 (ISR), AI-Based DSR Framework 2024, AI-augmented decision making DSR 2024

### 9.2.2 Novelty claims
- First system to combine: LLM orchestration + ≤8GB constrained ML ensemble + MCDM synthesis + consumer survey enrichment + real retail CPG evaluation
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
- Consumer signal timing: Indeks Danmark is an annual survey — may not capture in-year demand shifts
- Evaluation scope: LLM-as-Judge N=50 is statistically modest; significance claims are indicative
- DSR single-cycle: full ADR would require multiple build-evaluate-reflect cycles; thesis completes one cycle

---

## 9.5 Future research directions

- Multi-agent memory sharing: can agents share intermediate results to reduce redundant computation?
- Real-time streaming: adapting the pipeline for continuous data ingestion vs. batch weekly
- Alternative consumer signals: transaction loyalty card data, social media sentiment, web search trends
- Cross-retailer generalisation: test on a different FMCG category or market
- Full DSR second cycle: implement design principle refinements identified in this evaluation and re-evaluate

---

## Outstanding decisions

- Depth of theoretical contribution section: depends on how strong the empirical results are
- ✅ Design principles table added (section 9.2.2) — content mirrors Ch.10 section 10.2; values will be filled after empirical results
