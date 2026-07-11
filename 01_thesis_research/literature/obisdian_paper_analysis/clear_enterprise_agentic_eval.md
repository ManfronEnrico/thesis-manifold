---
title: "Beyond Accuracy: A Multi-Dimensional Framework for Evaluating Enterprise Agentic AI Systems"
authors: [Mehta, Sushant]
year: 2025
venue: "arXiv:2511.14136 [PREPRINT — single author; not peer-reviewed]"
url: https://arxiv.org/abs/2511.14136
tier: 2 — High relevance (preprint)
score: 6
srqs: [SRQ3, SRQ4]
tags: [gap-F, gap-H, evaluation, production-agents, preprint]
ch2_section: "2.5 Reliability/uncertainty & evaluation of agentic outputs; 2.6 Production-oriented agentic systems"
---

## Core argument
Benchmarks over-focus on task accuracy and ignore production realities. Proposes the CLEAR framework — Cost, Latency, Efficacy, Assurance, Reliability — for evaluating enterprise agentic AI systems.

## Method
Defines metrics (cost-normalised accuracy, SLA latency, efficacy, security/assurance, pass@k reliability); evaluates agents on 300 tasks across 6 domains; correlates results with expert deployment-readiness ratings; human evaluation with 15 experts.

## Key finding
Multidimensional evaluation correlates with deployment readiness (ρ=0.83) far better than accuracy-only evaluation (0.41); domain-specialised models beat general-purpose ones on cost-normalised performance; single-run success overstates reliability relative to multi-run consistency.

## Key quote
> "Multidimensional evaluation is not optional but essential" for enterprise agent deployment.

## Relevance to thesis
- [SRQ4]: Justifies evaluating decision-support outputs across **multiple dimensions** (reliability, cost, efficacy), not accuracy alone.
- [SRQ3]: Production constraints (cost/latency/reliability) inform integration readiness. Independently echoes the thesis's "specialised > general" finding and its small-N human evaluation.

## Gap / limitation
Single-author preprint; enterprise-agent generic (not forecasting-specific). Use for the *evaluation-design principle*, not for transferable numbers. **Do not present its metrics as our results.**
