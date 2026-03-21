# Chapter 3 — Methodology
> Thesis Writing Agent output — BULLET POINTS ONLY (no prose)
> Last updated: 2026-03-14
> Status: DRAFT — requires human approval before prose writing

---

## 3.1 Philosophy of Science

- Thesis adopts a **pragmatist** philosophy of science stance
  - Knowledge is judged by its practical consequences and usefulness
  - Aligns with Design Science Research: truth = what works in context
  - Justification: the thesis builds an artefact (framework) to solve a real problem (predictive decision-support for Manifold AI)
- Ontology: **moderate realism** — external business realities (sales patterns, consumer behaviour) exist independently, but are accessed through measurement instruments (Nielsen data, Indeks Danmark survey)
- Epistemology: **empirical** — knowledge claims derived from data and experimental evaluation, not pure theory
- Contrast with positivism: we do not claim universal laws; findings are context-bounded (Danish CSD retail, 8GB cloud environment)
- Contrast with interpretivism: quantitative data and reproducible metrics are primary evidence; no qualitative interpretation of meaning

---

## 3.2 Research Design — Design Science Research (DSR)

- Adopted framework: **Design Science Research** (Hevner et al., 2004; Peffers et al., 2007)
  - DSR is the dominant methodology for IS/AI artefact construction research
  - Produces both an artefact (the framework) and knowledge (design principles, evaluation findings)
  - Accepted at CBS for business/technology theses — aligns with RQ framing ("How can AI systems be designed...")
- DSR cycle:
  1. **Problem identification**: limits of descriptive analytics in resource-constrained environments
  2. **Objective definition**: reliable predictive decision-support within ≤8GB RAM
  3. **Design & development**: multi-agent framework (Phases 3–5)
  4. **Demonstration**: framework runs on real retail data (Phase 6)
  5. **Evaluation**: comparison with descriptive baseline, 3-level validation (Phase 6)
  6. **Communication**: thesis chapters
- Research design type (CBS taxonomy): **Explanatory** — explaining HOW the system achieves decision-support AND why certain design choices produce better outcomes than alternatives

---

## 3.3 Research Strategy

- **Primary strategy**: quantitative experiment + system evaluation
  - Model benchmark: controlled experiment (same data, different models)
  - SRQ3: controlled comparison (with vs without Indeks Danmark contextual signals)
  - SRQ4: quasi-experimental comparison (framework vs descriptive baseline)
- **Secondary strategy**: case study (Manifold AI as case organisation)
  - Provides real-world validation context
  - CBS case study guidelines apply (confidentiality agreement may be required)
- Unit of analysis: the multi-agent framework evaluated on Danish CSD retail data

---

## 3.4 Data Sources

| Source | Type | Role |
|---|---|---|
| Nielsen/Prometheus | Proprietary retail panel data | Primary forecasting data (SRQ1, SRQ4) |
| Indeks Danmark | Consumer survey data | Contextual enrichment signal (SRQ3) |

- Nielsen: star schema SQL, CSD category, 28 Danish retailers, ~36 monthly periods
- Indeks Danmark: 20,134 respondents, 6,364 variables, survey-weighted

**Data access**:
- Nielsen: access pending confirmation from Manifold AI (potential confidentiality agreement)
- Indeks Danmark: dataset received; CSVs to be downloaded locally

---

## 3.5 Analytical Approach

- **Forecasting models**: ARIMA, Prophet, LightGBM, XGBoost, Ridge Regression
  - Granularity: brand × retailer (DVH EXCL. HD default) × monthly period
  - Justification: tree-based models (LightGBM, XGBoost) suited for tabular retail data with ~36 periods; ARIMA/Prophet provide interpretable baselines
- **Consumer segmentation**: PCA + k-means on Indeks Danmark variables → 4–6 consumer segments
- **Synthesis**: ensemble weighting (inverse-MAPE) + LLM natural language generation (Claude API)
- **Evaluation metrics**:
  - Level 1 (ML accuracy): MAPE, RMSE, directional accuracy
  - Level 2 (recommendation quality): hit rate, LLM-as-judge rubric
  - Level 3 (agent behaviour): memory footprint, latency, error rate

---

## 3.6 Validity & Reliability

- **Internal validity**: same training/test split across all models; reproducible random seeds
- **External validity**: limited to Danish CSD retail context; generalisation to other categories/geographies is a stated limitation
- **Construct validity**: SRQ3 (contextual information impact) measured by ablation — compare framework with vs without Indeks Danmark signals
- **Reliability**: all code versioned; data preprocessing steps documented; model hyperparameters logged

---

## 3.7 Limitations

- Nielsen data access timeline uncertain — may require fallback to synthetic/public data for SRQ3/SRQ4
- ~36 monthly periods is borderline for ARIMA (minimum 24 recommended)
- Consumer-to-retailer segment mapping is a proxy — no direct row-level linkage between Indeks Danmark and Nielsen
- 8GB RAM constraint limits parallelism; sequential model execution is a design tradeoff
- Case study generalisability is bounded to Manifold AI's specific operational context

---

## CBS Compliance Notes for This Chapter

- ✅ Philosophy of science section included (CBS mandatory)
- ✅ Research design justified against RQ
- ✅ DSR is an accepted methodology at CBS for technology/IS theses — confirm with supervisor
- ⚠️ Cite foundational DSR papers: Hevner et al. (2004), Peffers et al. (2007)
- ⚠️ Confirm with supervisor whether DSR is accepted for this specific programme
