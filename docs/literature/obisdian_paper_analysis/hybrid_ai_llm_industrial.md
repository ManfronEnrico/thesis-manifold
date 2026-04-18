---
title: "Hybrid AI and LLM-Enabled Agent-Based Real-Time Decision Support Architecture for Industrial Batch Processes"
authors: Fabian Bürger, Josef Pauli (et al.)
year: 2024
venue: Engineering Applications of Artificial Intelligence (Elsevier)
url: https://www.sciencedirect.com/science/article/pii/S0952197624013988
tier: 1 — Core Essential
score: 10
angles: [Multi-Indicator + LLM/Agent, Prediction Quality]
srqs: [SRQ1, SRQ2, SRQ3, SRQ4]
note: CLOSEST PAPER TO THIS THESIS
---

## Core argument
A hybrid architecture combining physics-based process models, lightweight ML predictors, and an LLM orchestration agent can deliver real-time decision support in industrial batch processes (CIP case study), outperforming both pure data-driven and pure rule-based approaches.

## Method
3-layer system: (1) symbolic/physics layer encoding domain constraints and regulatory rules; (2) lightweight ML models (gradient boosting, LSTM variants) trained on sensor streams for process state prediction; (3) LLM agent that interprets predictions, retrieves contextual history, and generates actionable operator recommendations in natural language. Real industrial sensor data from a dairy production facility.

## Key finding
The hybrid LLM-agent architecture reduces CIP process time by 12–18% and water/chemical consumption by up to 20% vs manual operator decisions, while maintaining regulatory compliance.

## Key quote
> "The system reduces CIP process duration by 12–18% and chemical consumption by up to 20% relative to experienced human operators, while achieving 100% regulatory compliance."

## Relevance to thesis
- **The closest architectural blueprint in the literature** — directly analogous system transposed from industrial process control to business analytics
- SRQ1: lightweight ML under real-time constraints
- SRQ2: multi-agent coordination of predictive models
- SRQ3: contextual process history improving recommendations
- SRQ4: outperforms traditional manual/rule-based decision-making

## Gap / limitation
Domain-specific to industrial process control — well-defined physical constraints and sensor ontologies. Does not address heterogeneous, unstructured business data; multi-criteria trade-off decisions; or scalability across diverse business units. No computational budget constraint (RAM/CPU). → All gaps addressed by this thesis.
