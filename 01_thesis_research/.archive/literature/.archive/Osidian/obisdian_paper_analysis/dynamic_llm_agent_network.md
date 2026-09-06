---
title: "A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration"
authors: [Liu, Zijun, et al.]
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2310.02170
tier: 2 — High Relevance
score: 7
srqs: [SRQ2]
---

## Core argument
This paper proposes DyLAN (Dynamic LLM-Powered Agent Network), a framework in which multiple LLM agents collaborate on complex tasks through a dynamically constructed communication network. Rather than using a fixed pipeline or a single orchestrator, DyLAN allows agents to be selectively activated, ranked by their contribution, and connected in a topology that adapts to task requirements. The paper argues that dynamic, heterogeneous agent networks outperform static pipelines or simple ensembles on multi-step reasoning and code generation tasks.

## Method
Multiple LLM agents with distinct system prompts (roles) are instantiated; a dynamic routing mechanism selects which agents communicate with which others based on task context and agent performance scores. Experiments are conducted on arithmetic reasoning (MATH), code generation (HumanEval), and multi-agent decision tasks, measuring final task accuracy and agent utilisation efficiency.

## Key finding
DyLAN outperforms static multi-agent baselines by up to 10.3% on the MATH benchmark and 3.1% on HumanEval, with dynamic agent selection consistently reducing unnecessary computation while preserving output quality.

## Key quote
> "DyLAN introduces a dynamic agent network where LLM agents are selectively activated and ranked, enabling efficient task-oriented collaboration without the rigidity of fixed multi-agent pipelines."

## Relevance to thesis
- [SRQ2]: DyLAN's dynamic agent activation and ranking mechanism informs the Coordinator's task-routing logic — the thesis framework similarly needs to selectively invoke sub-agents (Forecasting, Synthesis, Validation) based on task phase and prior output quality.
- [SRQ2]: The concept of heterogeneous agent roles with distinct competencies (reasoning, coding, retrieval) maps directly onto the thesis's agent specialisation architecture (Data Assessment, Forecasting, Synthesis, CBS Compliance agents).

## Gap / limitation
DyLAN is evaluated exclusively on reasoning and coding benchmarks, with no application to forecasting, business decision support, or FMCG retail analytics. There is no treatment of memory constraints, ML model integration, or natural-language synthesis of quantitative outputs. The dynamic routing mechanism assumes homogeneous LLM-based agents, whereas the thesis framework mixes LLM agents with classical ML models (ARIMA, Prophet, LightGBM) that require different invocation patterns.
