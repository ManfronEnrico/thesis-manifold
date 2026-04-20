---
title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
authors: Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom
year: 2023
venue: NeurIPS 2023
url: https://arxiv.org/abs/2302.04761
tier: 1 — Core Essential
score: 10
angles: [LLM/Agent Requirements, Cloud/Resource-Constrained AI]
srqs: [SRQ1, SRQ2]
---

## Core argument
LLMs can self-supervise the learning of when and how to call external tools (calculators, search engines, APIs) by inserting API calls into their own training data — without large amounts of human annotation. Tool use is learned in a data-efficient, self-supervised manner.

## Method
(1) Prompt GPT-3 to generate candidate API call positions in existing text → (2) execute those calls → (3) keep only calls that reduce language modelling loss on subsequent tokens → (4) fine-tune a smaller model (GPT-J 6.7B) on the self-annotated corpus.

## Key finding
A 6.7B parameter model with tools outperforms GPT-3 (175B) on mathematical reasoning, factual QA, and temporal reasoning — tool use substitutes for raw parameter scale.

## Key quote
> "A 6.7B Toolformer model achieves substantially better performance than GPT-3 on a range of downstream tasks, while being 25x smaller in terms of parameters."

## Relevance to thesis
- SRQ1: tool delegation enables resource-efficient capability — a lightweight orchestrator achieves accuracy beyond its parameter budget
- SRQ2: foundational mechanism for an orchestrator agent delegating to specialised tools (forecasting models, databases)
- SRQ3: the model learns which contextual signals are worth querying per decision context

## Gap / limitation
Treats each tool call independently — no multi-step coordination across tools simultaneously. Assumes clean structured tool outputs — does not address heterogeneous noisy business data. No persistent state across decision cycles. → Feeds directly into thesis novelty argument.
