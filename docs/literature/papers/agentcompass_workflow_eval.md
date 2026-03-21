---
title: "AgentCompass: Towards Reliable Evaluation of Agentic Workflows in Production"
authors: [Khattab, Omar, et al.]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2509.14647
tier: 2 — High Relevance
score: 7
srqs: [SRQ2]
---

## Core argument
AgentCompass addresses the challenge of reliably evaluating multi-agent LLM workflows in production settings, where standard benchmark-based evaluation fails to capture the brittleness, partial failures, and compounding errors that arise in real deployment. The paper proposes a structured evaluation protocol covering correctness, efficiency, robustness, and agent behaviour traceability, and argues that production-grade agentic systems require continuous monitoring metrics — not just pre-deployment benchmarks — to detect silent degradation.

## Method
The authors define a multi-dimensional evaluation framework and apply it to several production-deployed agentic workflows (customer service, code review, data analysis). Metrics include task completion rate, step-level correctness, tool-use efficiency, error propagation rate, and latency. Evaluation is conducted through both automated scoring and human expert assessment.

## Key finding
Production agentic workflows exhibit significantly higher failure rates on long-horizon tasks (up to 34% step-level error rate) than benchmark results suggest, with compounding errors across agent steps being the primary cause of full-task failure; structured traceability of agent decisions reduces debugging time by 60%.

## Key quote
> "AgentCompass reveals that production agentic workflows face systematic evaluation gaps: benchmark performance overestimates real-world reliability, and the absence of step-level traceability makes failure diagnosis intractable."

## Relevance to thesis
- [SRQ2]: AgentCompass's multi-dimensional evaluation protocol directly informs the thesis Validation Agent design — specifically Level 3 (agent behaviour monitoring), which must detect compounding errors, incomplete sub-agent outputs, and coordination failures in the thesis multi-agent pipeline.
- [SRQ2]: The paper's emphasis on step-level traceability aligns with the thesis's mandatory human approval gates between phases, which serve as natural checkpoints for catching agent errors before they propagate.

## Gap / limitation
AgentCompass evaluates general-purpose production agentic workflows (customer service, code review) with no application to forecasting, business analytics, or FMCG retail. There is no treatment of ML model integration, RAM constraints, or the synthesis of quantitative forecasting outputs. The evaluation framework is designed for LLM-only pipelines and does not address the hybrid LLM + classical ML architecture that is central to this thesis.
