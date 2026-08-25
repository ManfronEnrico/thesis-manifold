---
title: "AutoFlow: Automated Workflow Generation for Large Language Model Agents"
authors: [Chen, Zelong, et al.]
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2407.12821
tier: 2 — High Relevance
score: 8
srqs: [SRQ2]
---

## Core argument
AutoFlow proposes a system that automatically generates multi-step agentic workflows from high-level task descriptions, removing the need for manual workflow engineering. The paper argues that LLM agents benefit from structured, graph-based workflow representations — where nodes are subtasks and edges are data dependencies — and that these workflows can be synthesised and optimised autonomously by an LLM planner. This makes complex multi-agent orchestration more accessible and adaptable without requiring domain-expert workflow design.

## Method
An LLM planner decomposes a task description into a directed acyclic graph (DAG) of subtasks, assigns tool-augmented sub-agents to each node, and iteratively refines the workflow using execution feedback. Evaluation is conducted on general agentic benchmarks including ALFWorld and HotpotQA, measuring task completion rate and workflow efficiency.

## Key finding
AutoFlow reduces manual workflow design effort and achieves competitive task completion rates (within 5% of hand-crafted workflows on ALFWorld), while being substantially more generalisable to novel task types with minimal re-engineering.

## Key quote
> "AutoFlow automatically generates workflows for LLM agents by decomposing complex tasks into structured DAGs of subtasks, enabling scalable multi-agent coordination without manual pipeline construction."

## Relevance to thesis
- [SRQ2]: AutoFlow's DAG-based workflow decomposition maps directly onto the thesis's LangGraph architecture, where nodes are agents (Data Assessment, Forecasting, Synthesis, Validation) and edges represent data flow between phases.
- [SRQ2]: The automated orchestration pattern informs how the Coordinator agent can dynamically route tasks and manage dependencies between sub-agents rather than relying on a hard-coded sequential pipeline.

## Gap / limitation
AutoFlow operates on general agentic benchmarks without any domain adaptation to business analytics, time-series forecasting, or FMCG retail. It does not address resource constraints (RAM/compute), ML model integration, or the synthesis of quantitative forecasting outputs into natural-language business recommendations. There is no treatment of human-in-the-loop approval gates, which are a mandatory design requirement in the thesis framework.
