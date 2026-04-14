---
title: "AgentCompass: Towards Reliable Evaluation of Agentic Workflows in Production"
authors: Sapra, K.N., Sapra, G., Hada, R., & Pareek, N.
year: 2025
venue: arXiv preprint (arXiv:2509.14647v1)
doi:
apa7: |
  Sapra, K. N., Sapra, G., Hada, R., & Pareek, N. (2025). AgentCompass: Towards reliable evaluation of agentic workflows in production. *arXiv preprint arXiv:2509.14647*.
read_date: 2026-03-21
read_depth: full
---

## In one sentence

Post-deployment monitoring of multi-agent LLM systems requires a dedicated evaluation framework — AgentCompass addresses this by combining structured error taxonomy, multi-stage diagnostic reasoning, trace-level clustering, and a dual episodic/semantic memory system to surface recurring failure patterns that static benchmarks miss.

## Method

Multi-stage analytical pipeline modelling expert debugger cognition: error identification/categorisation → thematic clustering → quantitative scoring → strategic summarisation. Dual memory system (episodic + semantic) for continual learning across executions. Trace-level density-based clustering to surface systemic failures. Validated on real-world design-partner deployments and the TRAIL benchmark.

## Key findings — cite these

- Achieves **state-of-the-art results on TRAIL** in error localisation and joint metrics
- Uncovers **critical errors missed by human annotations**, including safety and reflection gaps
- Automation via agentic workflows has yielded **20–30% cost savings** in enterprise deployments (cited industry data)
- Most current evaluation frameworks prioritise technical metrics (accuracy, speed) and neglect edge cases, contextual failures, and compounding errors across agent chains
- Errors propagate and compound through multi-agent pipelines, making correction and accountability complex

## Direct quotes — copy verbatim, include page/section

> "Poor evaluation and systems breaking in production are major causes of financial and reputational damage to organizations adopting agentic AI." (Section 1)

> "Most organizations are unprepared for the complexities of agentic and multi-agentic AI risks, with governance blind spots multiplying post-deployment." (Section 1)

> "Errors and biases often compound and propagate through multi-agent workflows, making correction and accountability complex." (Section 1)

## Where this goes in my thesis

- **Ch.2, Section 2.X (Multi-agent systems / evaluation)**: Cite as the state-of-the-art framework for production monitoring of agentic workflows — establishes that standard accuracy benchmarks are insufficient for real-world multi-agent deployments
- **Ch.5 (Framework Design)**: The hierarchical error taxonomy and trace-level clustering are design precedents for our Validation Agent's 3-level validation framework; the dual memory system parallels our agent state persistence requirements
- **Ch.8 (Evaluation / SRQ3–SRQ4)**: AgentCompass's multi-stage scoring pipeline is a methodological reference for how we evaluate recommendation quality beyond point-accuracy metrics
- **Ch.9 (Limitations / Related Work)**: Acknowledge that our validation framework does not implement production monitoring or continual learning — AgentCompass represents the next maturity level beyond our thesis scope

## What this paper does NOT cover (gap it leaves)

AgentCompass evaluates general-purpose agentic workflows in enterprise IT contexts; it does not address domain-specific evaluation criteria for **predictive decision-support in retail analytics**, where correctness is not binary but measured against business outcomes (forecast accuracy, decision quality scores) — the evaluation design problem central to SRQ3 and SRQ4.

## My critical assessment


- Establishes a **state-of-the-art framework for evaluating multi-agent systems in production**, moving beyond static benchmarks to continuous, real-world monitoring
    
- Key insight: **errors propagate and compound across agent chains**, making single-step evaluation insufficient — directly supporting the thesis’s multi-level validation design
    
- Introduces a **structured, trace-level evaluation paradigm** (error taxonomy, clustering, diagnostics) that aligns closely with the need for systematic validation in complex agentic workflows
    
- Highlights that **standard metrics (accuracy, speed) are insufficient**, reinforcing the thesis’s approach to evaluating recommendation quality beyond point performance
    
- However, the framework is tailored to **enterprise IT workflows** and does not address domain-specific evaluation for forecasting-based decision support
    
- Lacks integration with **quantitative performance metrics** (e.g., forecast accuracy, confidence calibration) central to the thesis
    
- Does not consider **resource-constrained implementations** or simplified evaluation pipelines required in an academic setting
    
- Therefore, highly valuable as a **conceptual and methodological benchmark for evaluating agentic systems**, but requires adaptation to fit the domain-specific and quantitative evaluation needs of the thesis