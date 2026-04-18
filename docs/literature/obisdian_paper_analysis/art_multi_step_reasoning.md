---
title: "ART: Automatic Multi-Step Reasoning and Tool-Use for Large Language Models"
authors: Bhargavi Paranjape, Scott Lundberg, Sameer Singh, Hannaneh Hajishirzi, Luke Zettlemoyer, Marco Tulio Ribeiro
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2303.09014
tier: 1 — Core Essential
score: 9
angles: [LLM/Agent Requirements]
srqs: [SRQ1, SRQ2]
---

## Core argument
LLMs can automatically generate multi-step reasoning programs that interleave tool calls with chain-of-thought reasoning — without task-specific fine-tuning — by retrieving analogous demonstrations from a task library and generalizing to new problems.

## Method
Frozen LLM (Codex) + curated task library. For a new task: retrieve most relevant demonstrations via semantic similarity → generate reasoning+tool-use program → call external tools (search, code execution, arithmetic) at intermediate steps. Human feedback extends the library. Evaluated on BigBench and MMLU.

## Key finding
ART matches or exceeds few-shot CoT and task-specific fine-tuned baselines on 20/32 BigBench tasks in a zero-shot manner. Human feedback enables further improvement.

## Key quote
> "ART matches or surpasses few-shot prompting and fine-tuned models on 20 out of 32 BigBench tasks without any task-specific training, by automatically composing multi-step reasoning programs with tool calls."

## Relevance to thesis
- SRQ2: retrieval-augmented program generation applicable to an orchestrator selecting and sequencing analytical tools (forecasting models, MCDM modules, data retrievers) based on business query type
- Task library concept → reusable library of business analysis patterns enabling efficient orchestration without retraining

## Gap / limitation
Task library must be manually curated. Does not address continuous adaptation to shifting data distributions (common in business). Does not tackle real-time latency constraints or heterogeneous quantitative/qualitative business signals.
