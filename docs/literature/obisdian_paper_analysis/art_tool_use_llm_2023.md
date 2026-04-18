---
title: "ART: Automatic Multi-Step Reasoning and Tool-Use for Large Language Models"
authors: Bhargavi Paranjape, Scott Lundberg, Sameer Singh, Hannaneh Hajishirzi, Luke Zettlemoyer, Marco Tulio Ribeiro
year: 2023
venue: arXiv preprint (arXiv:2303.09014)
url: https://arxiv.org/abs/2303.09014
tier: 2 — Recommended (Scraping Run 2)
score: 8
angles: LLM Tool Use, Multi-Step Reasoning, SRQ2
srqs: [SRQ2]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
Frozen LLMs can automatically generate multi-step reasoning programs that interleave tool calls with chain-of-thought reasoning for new tasks — without any task-specific fine-tuning — by retrieving analogous demonstrations from a curated task library and generalising compositionally.

## Method
Frozen LLM (Codex) plus a curated task library of multi-step reasoning and tool-use demonstrations. For each new task: retrieve the most relevant demonstrations via semantic similarity, generate a reasoning+tool-use program, execute external tools (search, code execution, arithmetic) at intermediate steps, and integrate results before resuming generation. Evaluated on 32 BigBench tasks and MMLU.

## Key finding
ART matches or surpasses few-shot prompting and task-specific fine-tuned baselines on 20/32 BigBench tasks in a zero-shot manner; human feedback on task-specific programs enables further targeted improvement with minimal annotation cost.

## Relevance to thesis
- SRQ2: the task library concept directly maps to a reusable library of business analysis patterns — enabling the orchestrator to select and sequence forecasting models, MCDM modules, and data retrievers based on query type without retraining
- Ch.2.1 (Multi-Step Reasoning), Ch.5 (Orchestration Design): secondary citation alongside Toolformer for tool-augmented reasoning

## Gap / limitation
Task library requires manual curation and does not adapt automatically to shifting data distributions common in retail business contexts; does not address real-time latency or heterogeneous quantitative/qualitative business signals.

> Note: a more detailed annotation exists at `art_multi_step_reasoning.md` (Scraping Run 1, Tier 1). This file is the Scraping Run 2 record with updated tier/score metadata.
