---
title: "Executable Code Actions Elicit Better LLM Agents"
authors: Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu Li, Heng Ji, Hanghang Tong
year: 2024
venue: ICML 2024
url: https://openreview.net/forum?id=jJ9BoXAfFa
tier: 1 — Core Essential
score: 10
angles: [LLM/Agent Requirements, Cloud Code Execution]
srqs: [SRQ2, SRQ4]
---

## Core argument
Representing LLM agent actions as executable Python code (vs JSON function calls or natural language) yields a more expressive, composable, generalizable action space — leading to substantially better task completion across diverse benchmarks.

## Method
CodeAct framework: agent actions are Python programs executed in an interactive interpreter. Multi-turn dialogues. Compared against text/JSON-based formats on 2,000+ tasks across 17 agent benchmarks.

## Key finding
CodeAct improves agent success rates by up to 20% relative to JSON-based formats, and enables emergent compositional behaviours such as self-debugging and dynamic tool creation.

## Key quote
> "CodeAct achieves 20% higher task success than the best text/JSON baselines and enables agents to self-debug and dynamically extend their own capabilities via code generation."

## Relevance to thesis
- SRQ2: provides action-execution substrate for an orchestrator coordinating ML models, data retrieval, decision synthesis
- SRQ4: code-executable actions allow agents to replicate and surpass what BI dashboards do, with programmable logic

## Gap / limitation
Evaluated in sandbox environments — does not address deployment under computational constraints (CPU-only, edge hardware), real-time latency requirements, or persistent business state. Multi-turn execution may be too expensive for low-latency business decision loops.
