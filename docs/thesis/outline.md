# Thesis Outline — Approved Structure
> Last updated: 2026-03-14 (v2 — post ChatGPT structural revision)
> Status: DRAFT — awaiting human approval before Phase 7

---

## Identity

| Field | Value |
|---|---|
| Working title | How AI Systems Can Provide Predictive Decision-Support in Real-World Business Environments Under Computational Constraints |
| Programme | MSc Business Administration & Data Science, CBS |
| Partner | Manifold AI |
| Group | 2 students |
| Page limit | 120 standard pages (2,275 chars/page) |
| Deadline | 15 May 2026 |
| Language | English |

---

## Research Questions (v2 — 2026-03-14)

**Main RQ**: How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?

| | Sub-RQ | Phase |
|---|---|---|
| SRQ1 | Which predictive modelling approaches provide the best balance between forecasting accuracy and computational efficiency under realistic cloud resource constraints? | Phase 4 |
| SRQ2 | How can a multi-agent architecture coordinate predictive models and heterogeneous data signals to generate actionable managerial recommendations? | Phase 5 |
| SRQ3 | To what extent does additional contextual information improve the predictive and decision-support capabilities of AI systems? | Phase 5–6 |
| SRQ4 | How does the proposed predictive AI system compare to traditional descriptive analytics approaches used in business intelligence systems? | Phase 6 |

---

## Chapter Structure

| # | Chapter | Pages | Key Content | SRQ |
|---|---|---|---|---|
| 1 | Introduction | ~8 | Problem statement (limits of descriptive analytics), Manifold AI context, RQs, delimitation, structure | — |
| 2 | Literature Review | ~20 | AI agents & orchestration, predictive ML for decision-support, lightweight ML, resource-constrained AI, MCDM synthesis | — |
| 3 | Methodology | ~12 | Design Science Research, experimental evaluation framework, data sources, validation design | — |
| 4 | Data Assessment | ~10 | Nielsen/Prometheus quality & suitability, Indeks Danmark overview, feature engineering, limitations | — |
| 5 | Framework Design | ~10 | Multi-agent architecture (PydanticAI + LangGraph), agent roles, 8GB constraint justification | SRQ2 |
| 6 | Model Benchmark & Selection | ~15 | Candidate model evaluation, memory profiling, accuracy vs efficiency trade-off table | SRQ1 |
| 7 | Context-Aware Decision Synthesis | ~15 | Synthesis module design, integration of contextual signals (Indeks Danmark), confidence scoring | SRQ2, SRQ3 |
| 8 | Experimental Evaluation | ~12 | Forecasting accuracy metrics, recommendation quality, comparison vs descriptive baseline | SRQ3, SRQ4 |
| 9 | Discussion | ~8 | Implications for AI decision-support, business analytics practice, limitations, future work | — |
| 10 | Conclusion | ~5 | Answers to all RQs, contribution statement | — |
| — | Bibliography | not counted | APA 7 | — |
| — | Appendices | not counted | Data samples, extended results, agent diagrams | — |

**Total body**: ~115 pages (5-page buffer)

---

## What Changed from v1 (2026-03-14)

| Element | v1 | v2 |
|---|---|---|
| Main RQ | Focused on 8GB RAM specifically | Broader: "computational constraints" in real-world environments |
| SRQ count | 3 | 4 |
| SRQ3 (new) | — | Contextual information (Indeks Danmark) impact on decision-support |
| SRQ4 (was SRQ3) | Performance gains vs baseline | Explicit comparison with traditional BI/descriptive analytics |
| Ch.7 title | Synthesis Module | Context-Aware Decision Synthesis (explicitly integrates survey data) |
| Overall framing | Technical system building | Design + evaluation of predictive AI decision-support systems |

---

## Locked Decisions (confirmed 2026-03-14)

| # | Decision |
|---|---|
| OQ1 — Granularity | **Brand × retailer** level. Default market: DVH EXCL. HD. Category-level too coarse; SKU-level too granular for 8GB. |
| OQ2 — Models | **ARIMA, Prophet, LightGBM, XGBoost, Ridge Regression** (5 models: Ridge = simple baseline, XGBoost = LightGBM comparator) |
| OQ3 — Indeks Danmark | **Feature enrichment**: map consumer segments (demographic + attitudinal clusters) to retailer-level demand signals. No row-level join needed. |
| OQ4 — Metrics | **(1)** MAPE/RMSE for ML accuracy **(2)** Hit rate / directional accuracy for managerial usefulness **(3)** LLM-as-judge rubric for recommendation quality |
| OQ5 — Baseline | Manifold AI Colleagues current descriptive output. If unavailable: "static monthly report with last-period extrapolation" (standard BI benchmark). |
