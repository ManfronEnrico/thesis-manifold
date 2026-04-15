---
title: "Hybrid AI and LLM-Enabled Agent-Based Real-Time Decision Support Architecture for Industrial Batch Processes: A Clean-in-Place Case Study"
authors: González-Potes, A., Martínez-Castro, D., Paredes, C. M., Ochoa-Brust, A., Mena, L. J., Martínez-Peláez, R., Félix, V. G., & Félix-Cuadras, R. A.
year: 2026
venue: AI, 7(2), 51
doi: 10.3390/ai7020051
apa7: >
  González-Potes, A., Martínez-Castro, D., Paredes, C. M., Ochoa-Brust, A., Mena, L. J.,
  Martínez-Peláez, R., Félix, V. G., & Félix-Cuadras, R. A. (2026). Hybrid AI and LLM-enabled
  agent-based real-time decision support architecture for industrial batch processes: A
  Clean-in-Place case study. *AI*, *7*(2), 51. https://doi.org/10.3390/ai7020051
read_date: 2026-03-21
read_depth: full
---

## In one sentence

A real-world deployment of a hybrid deterministic/LLM multi-agent architecture for industrial process supervision shows that separating hard real-time deterministic agents from soft real-time LLM analytics — while enriching raw sensor signals into linguistic variables — enables reliable AI-assisted decision support without modifying legacy PLC/SCADA control infrastructure.

## Method

Case study design (not statistical generalisation). Six-month deployment at an industrial beverage plant (VivaWild Beverages). Three purposively selected CIP executions spanning nominal baseline, preventive warning, and diagnostic alert conditions. Metrics: stage-specification compliance, state-to-specification consistency (Γs), temporal stability of supervisory states (Λs), and numerical fidelity of LLM summaries vs. enriched logs (spot-check audits). Architecture: layered cyber/physical separation, fuzzy logic + statistical signal enrichment, rule-based deterministic agents, LLM analytics agent via RAG.

## Key findings — cite these

- **Γs ≥ 0.98** (state-specification consistency) in alkaline stages across all three evaluated runs
- **100% specification compliance** in sanitising stages across nominal, preventive, and diagnostic runs
- **Median LLM numerical error below 3%** in audited samples — LLM summaries are data-grounded, not hallucinated
- **Median reaction time ~35–36 seconds** between critical episode onset and alert in diagnostic regime (CIP 3)
- Temporal domain separation (deterministic hard real-time <100 ms vs. LLM soft real-time 1–2 s) is the key architectural mechanism for safe LLM integration in safety-critical environments
- RAG prevents hallucination by grounding LLM responses in enriched process logs rather than parametric knowledge

## Direct quotes — copy verbatim, include page/section

> "LLM outputs are non-deterministic, may hallucinate and must coexist with hard safety constraints, deterministic interlocks and real-time requirements." (Section 1)

> "The Deterministic Supervisor enforces safety barriers preventing non-deterministic LLM outputs from directly commanding actuators." (Figure 2 caption)

> "The contribution lies in demonstrating how to bridge the gap between AI theory and industrial practice through careful system architecture, data transformation pipelines, and integration patterns that enable reliable AI-enhanced decision support in production environments." (Abstract)

> "Signal enrichment pipelines to bridge the semantic gap between numerical sensor data and natural language LLM inputs." (Section 1.3)

## Where this goes in my thesis

- **Ch.2, Section 2.X (Multi-agent systems / hybrid AI)**: Cite as a real-world deployment precedent for hybrid deterministic/LLM multi-agent architectures — directly analogous to our System A design where deterministic ML models feed LLM-based synthesis
- **Ch.5 (Framework Design / SRQ2)**: The temporal domain separation pattern (deterministic agents → enriched signals → LLM analytics) is a direct design precedent for our pipeline: ML forecasts → signal enrichment → Synthesis Agent LLM call
- **Ch.5**: RAG-based hallucination prevention supports our design choice to ground the Synthesis Agent's recommendations in structured forecast outputs rather than free LLM generation
- **Ch.8 (Evaluation / SRQ3–SRQ4)**: The evaluation metrics (specification compliance, state consistency, LLM fidelity audits) are methodological references for our 3-level validation framework — particularly Level 2 (recommendation quality) and Level 3 (system reliability)
- **Ch.9 (Limitations)**: Single case study limitation mirrors ours; cite to contextualise the generalisability constraint of our evaluation

## What this paper does NOT cover (gap it leaves)

This architecture is designed for continuous real-time industrial process supervision (sensor streams at 100–1000 ms intervals) with deterministic safety-critical constraints — it does not address **predictive forecasting over historical tabular retail data**, **multi-criteria synthesis of competing model outputs**, or **resource-constrained cloud deployment with a fixed RAM budget**, which are the specific design problems of this thesis.

## My critical assessment

- **Strengths:** Demonstrates a real-world hybrid deterministic/LLM multi-agent system with rigorous evaluation of safety, temporal separation, and LLM grounding via RAG; highlights value of signal enrichment pipelines for reliable AI-assisted decision support.
- **Weaknesses:** Domain-specific (CIP processes) and based on a small purposive sample; lacks statistical generalisation; metrics focus on process compliance rather than predictive accuracy or multi-model synthesis.
- **Relevance to thesis:** Temporal domain separation and LLM integration principles inform your multi-agent orchestration design; signal enrichment idea supports your approach to combining ML forecasts with survey data.
- **Gap addressed by your work:** Does not cover predictive forecasting of tabular retail sales data, multi-model synthesis under strict RAM constraints, or enrichment with consumer survey signals — all central to your CBS + Manifold AI project.