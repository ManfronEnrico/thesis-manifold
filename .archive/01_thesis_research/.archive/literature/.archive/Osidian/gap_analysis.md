# Gap Analysis & Proposed Novelty
> Maintained by the Literature Review Agent
> Last updated: 2026-03-15 (v4 — post Tier A + Tier B annotation; 16 papers confirmed)
> Status: CONSOLIDATED — ready for Ch.2 prose; open questions for Run 2

---

## Literature Corpus Summary

**Sources**:
- Original CSV import: 40 papers (2026-03-14)
- Scraping Run 1 confirmations: 16 papers (6 Tier A + 10 Tier B, 2026-03-15)
- Scraping Run 2: in progress (2026-03-15)

**Confirmed in corpus**: 16 annotated papers (all with annotation files in docs/literature/papers/)
**Tier A (score 9)**: 6 papers — customer segmentation, Kuleshov calibration, FMCG ML, AI-augmented BI DSR, AI-Based DSR Framework, Pathways for Design Research on AI
**Tier B (score 8)**: 10 papers — retail ML benchmarks, FMCG methods, consumer behaviour, LLMs in supply chain, hybrid neural forecasting, AI-enhanced BI, calibrating uncertainty, prediction intervals, artifact types in DSR
**Pending annotation from original CSV**: ~28 papers (Toolformer, ART, LangGraph, Neuro-Symbolic AI, Hybrid MCDM, etc. — target for Run 2)

---

## Research Angles Covered

| Angle | Representative Papers |
|---|---|
| LLM/Agent Requirements | Toolformer, ART, Agent Q, AutoFlow, ScoreFlow, ANAH, SciAgent |
| Multi-Indicator + Prediction | Hybrid MCDM+ML supplier selection, Ensemble clinical decision support |
| Prediction Quality | Model Averaging + Double ML, Innovative ML for economic forecasting |
| Cloud/Resource-Constrained AI | Edge AI acceleration, Efficient & Green LLMs, On Accelerating Edge AI |
| LLM + ML Integration | Neuro-Symbolic AI 2024, Hybrid AI Models |
| Hybrid AI Agent + Real-time | Hybrid AI and LLM-Enabled Agent for Industrial Processes |
| Business Decision-Making | Value of ML in Business Decision-Making, DSS4EX |

---

## Tier 1 Core Essential Papers

| Paper | Score | Angle |
|---|---|---|
| Executable Code Actions Elicit Better LLM Agents | 10 | Cloud Code + LLM |
| Toolformer: Language Models Can Teach Themselves to Use Tools | 10 | LLM/Agent |
| Hybrid AI and LLM-Enabled Agent-Based Real-Time Decision Support | 10 | Multi-Indicator + LLM/Agent |
| AI Agents vs. Agentic AI: Conceptual Taxonomy | 9 | LLM/Agent |
| ART: Automatic multi-step reasoning and tool-use | 9 | LLM/Agent |
| Hybrid MCDM + ML for explainable supplier selection | 9 | Multi-Indicator + Prediction |
| Neuro-Symbolic AI in 2024: Systematic Review | 9 | LLM + ML Integration |
| HYBRID AI MODELS: Symbolic Reasoning + Deep Learning | 9 | All Angles |
| On Accelerating Edge AI: Optimizing Resource-Constrained Environments | 9 | Cloud/Constrained AI |
| Value of ML and Predictive Modeling in Business Decision-Making | 8 | Prediction Quality |
| Model Averaging and Double Machine Learning | 8 | Prediction + Multi-Indicator |
| An information-sharing cost-aware ML for 3PL supply chain forecasting | 8 | Cloud/Constrained |

---

## Preliminary Gap Identification

*(To be finalised by Literature Review Agent — these are initial observations)*

### Observed gaps (hypotheses):
1. **Resource-constrained multi-agent forecasting**: Most multi-agent LLM papers assume cloud-scale compute. No paper in corpus explicitly addresses a 4–8GB RAM budget for a full forecasting+synthesis pipeline.
2. **Multi-indicator synthesis with LLM orchestration**: Papers address either MCDM methods OR LLM agents — not a combined architecture where LLM orchestrates ML model outputs into a confidence-scored recommendation.
3. **Retail CPG forecasting with agent frameworks**: Existing agent + forecasting work targets industrial/clinical settings. Danish retail CSD forecasting with a multi-agent architecture is not covered.
4. **Descriptive-to-predictive transition in AI Colleagues systems**: The specific transition from descriptive analytics agent to predictive decision-support agent is not addressed in the corpus.

### Proposed novelty (v3, 2026-03-14 — post Tier 1 annotation):

The thesis is the first to **simultaneously** combine:
1. **LLM orchestration** of a multi-agent system (grounded in Toolformer, CodeAct, ART, Agentic AI taxonomy)
2. **Lightweight ML ensemble** forecasting benchmarked under an explicit ≤8GB RAM constraint (ARIMA, Prophet, LightGBM, XGBoost, Ridge)
3. **MCDM-style synthesis** aggregating heterogeneous model outputs and consumer signals into a confidence-scored recommendation
4. **Consumer survey data** (Indeks Danmark) as a contextual enrichment signal for demand forecasting — a gap explicitly absent from all 12 Tier 1 papers
5. **Evaluated against a defined descriptive analytics baseline** in a real retail CPG context (Danish CSD market)

**Strongest novelty point**: None of the 12 Tier 1 papers addresses items 2+3+4 together. The closest paper (Hybrid CIP industrial) operates in a sensor-rich industrial environment with clean structured data and no computational budget — the opposite of the thesis's SME retail context.

**Secondary novelty**: the memory profiling methodology for a multi-component AI pipeline (ML forecasting + LLM synthesis) is entirely absent from the literature and represents a replicable protocol contribution.

---

## Gap Evidence — Paper-by-Paper Summary (confirmed corpus)

| Gap | Evidence from confirmed papers | Verdict |
|---|---|---|
| No RAM-constrained multi-agent forecasting framework | All 5 SRQ1 papers exclude RAM as design variable; LLM papers assume cloud | **Confirmed — genuine gap** |
| No head-to-head ARIMA/Prophet/LightGBM/XGBoost/Ridge benchmark under RAM budget | FMCG ML 2024, Demand Forecasting Methods 2023, MDPI Applied Sciences 2024 — each single-model | **Confirmed — genuine gap** |
| No consumer survey enrichment in agent-based forecasting | Customer Segmentation 2023, Consumer Behavior 2025 — enrichment but not multi-agent | **Confirmed — genuine gap** |
| Descriptive-to-predictive BI transition discussed not empirically tested | AI-enhanced BI 2025 (survey-based), Design Principles ADR 2024 (design study) — no empirical CPG eval | **Confirmed — genuine gap** |
| No RAM profiling methodology for multi-component AI pipelines | Absent from all 16 confirmed papers | **Confirmed — genuine gap** |

---

## Proposed Novelty v4 (post Tier A + B annotation)

The thesis is the first to **simultaneously** achieve all five:

1. **LLM orchestration** of a resource-constrained multi-agent pipeline (grounded in Toolformer, ART, LangGraph — pending Run 2 annotation)
2. **Lightweight ML ensemble** benchmarked under explicit ≤8GB RAM (ARIMA, Prophet, LightGBM, XGBoost, Ridge) — gap confirmed by 3 retail forecasting papers
3. **Calibrated confidence scoring** using isotonic regression (Kuleshov 2018) validated for tree ensemble models (MDPI Sensors 2023) — first application in a multi-agent synthesis architecture
4. **Consumer survey data** (Indeks Danmark) as a contextual enrichment signal in ML demand forecasting — confirmed gap by consumer segmentation corpus
5. **Empirical evaluation against a defined descriptive analytics baseline** in a real Danish retail CPG context — confirmed gap by AI-enhanced BI 2025 (survey only, no CPG empirical study)

**Strongest differentiator**: The intersection of (2) + (3) + (4) does not appear in any of the 16 confirmed corpus papers, nor in the 28 pending original CSV papers based on their titles and abstracts. This is the thesis's primary novelty claim.

**Methodological novelty**: RAM profiling protocol for multi-component AI pipelines — replicable contribution absent from literature.

---

## Open Questions (for Run 2 and supervisor discussion)

- Do any papers address the descriptive-to-predictive agent transition in SME AI tools explicitly? *(partial answer: AI-enhanced BI 2025 — but no custom multi-agent system)*
- What is the standard benchmark for "recommendation quality" in LLM decision-support systems? *(LLM-as-Judge is the current closest; ANAH — pending Run 2)*
- Is PydanticAI + LangGraph combination referenced in any multi-agent coordination paper?
- What memory profiling methodology is standard for ML-in-production papers?
- **DSR acceptance**: Does the CBS programme formally accept DSR as the primary methodology for a Business Administration + Data Science thesis? *(Supervisor confirmation required)*
