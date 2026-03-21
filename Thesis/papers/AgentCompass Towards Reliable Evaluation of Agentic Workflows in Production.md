---
title: "AgentCompass: Towards Reliable Evaluation of Agentic Workflows in Production"
authors: Sapra, K.N., Sapra, G., Hada, R., & Pareek, N.
year: 2025
venue: arXiv preprint (arXiv:2509.14647v1)
doi:
apa7: >
  Sapra, K. N., Sapra, G., Hada, R., & Pareek, N. (2025). AgentCompass: Towards reliable evaluation
  of agentic workflows in production. *arXiv preprint arXiv:2509.14647*.
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

- Provides a **state-of-the-art perspective on post-deployment evaluation**, highlighting that traditional benchmarks fail to capture real-world failure modes in multi-agent systems
- Introduces a **structured and systematic evaluation paradigm** (error taxonomy, trace-level analysis, multi-stage diagnostics) that aligns closely with the thesis’s Validation Agent design
- Key contribution: demonstrates that **errors propagate and compound across agent chains**, reinforcing the need for multi-level validation rather than single-point checks
- Emphasises the importance of **continuous monitoring and learning (episodic + semantic memory)**, positioning evaluation as an ongoing process rather than a one-time benchmark
- However, the framework is designed for **enterprise IT workflows** and does not directly address domain-specific evaluation in predictive analytics or forecasting systems
- Focuses on error detection and monitoring rather than **quantitative decision quality metrics** (e.g., forecast accuracy, confidence calibration) central to the thesis
- Does not consider **resource-constrained environments** or simplified evaluation pipelines required for lightweight academic implementations
- Therefore, highly valuable as a **conceptual and methodological reference for evaluating multi-agent systems in production**, but requires adaptation to fit the domain-specific, quantitative evaluation setting of the thesis