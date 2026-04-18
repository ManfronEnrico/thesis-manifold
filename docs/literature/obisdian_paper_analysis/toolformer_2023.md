---
title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
authors: Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom
year: 2023
venue: NeurIPS 2023
url: https://arxiv.org/abs/2302.04761
tier: 2 — Recommended (Scraping Run 2)
score: 9
angles: LLM Tool Use, SRQ2, Agent Capabilities
srqs: [SRQ2]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
LLMs can learn when and how to call external tools (APIs, calculators, search engines, calendars) in a self-supervised manner, without requiring large amounts of human annotation — by using their own generation to identify useful API call positions and filtering on language modelling loss improvement.

## Method
(1) Prompt GPT-3 to generate candidate API call positions in existing text; (2) execute those API calls; (3) retain only calls that reduce language modelling loss on subsequent tokens; (4) fine-tune a smaller model (GPT-J 6.7B) on the resulting self-annotated corpus. Evaluated across five tool types on six benchmarks.

## Key finding
A 6.7B parameter Toolformer model outperforms GPT-3 (175B) on mathematical reasoning, factual QA, and temporal reasoning — demonstrating that tool use can substitute for raw parameter scale, achieving superior capability at a fraction of the memory footprint.

## Relevance to thesis
- SRQ2: foundational mechanism for the thesis's orchestrator agent delegating analytical sub-tasks (forecasting, data retrieval, MCDM scoring) to specialised tools — directly models the agent's tool-selection logic
- SRQ1: shows that lightweight models with tools can outperform large monolithic models — justifies the resource-efficient multi-tool architecture under the 8GB constraint
- Ch.2.1 (LLM Tool Use), Ch.5 (Framework Design): primary citation for tool-augmented LLM orchestration

## Gap / limitation
Each tool call is independent — no multi-step coordination across tools or persistent state across decision cycles, which are both required in the thesis's multi-agent architecture.

> Note: a more detailed annotation exists at `toolformer.md` (Scraping Run 1, Tier 1). This file is the Scraping Run 2 record with updated tier/score metadata.
