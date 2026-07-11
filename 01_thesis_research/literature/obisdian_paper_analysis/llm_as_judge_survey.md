---
title: "A Survey on LLM-as-a-Judge"
authors: [Gu, Jiawei, Jiang, Xuhui, Shi, Zhichao, Tan, Hexiang, Zhai, Xuehao, Xu, Chengjin, Li, Wei, Shen, Yinghan, Ma, Shengjie, Liu, Honghao, Wang, Saizhuo, Zhang, Kun, Wang, Yuanzhuo, Gao, Wen, Ni, Lionel, Guo, Jian]
year: 2024
venue: "arXiv:2411.15594 [PREPRINT — survey; not peer-reviewed]"
url: https://doi.org/10.48550/arXiv.2411.15594
tier: 2 — Methodological reference (preprint)
score: 6
srqs: [SRQ4]
tags: [gap-H, llm-as-judge, evaluation, survey, preprint]
ch2_section: "2.5 Reliability/uncertainty & evaluation of agentic outputs"
---

## Core argument
Asks "how can reliable LLM-as-a-Judge systems be built?" and organises the design space and reliability-enhancement strategies for using LLMs as evaluators.

## Method
Taxonomy across five dimensions: in-context learning format (scoring, yes/no, pairwise), model selection (general vs fine-tuned), post-processing, evaluation pipelines, and improvement strategies. Proposes a meta-evaluation benchmark for judge reliability.

## Key finding
Pairwise comparison is more consistent than score-based judging; bias mitigation via content shuffling, structured outputs, and criteria decomposition; post-processing methods are brittle; fine-tuned judges overfit. Reliability defined as consistency + robustness + alignment with human judgment.

## Key quote
> Reliability requires "consistency, robustness, and alignment with human judgment" (near-verbatim).

## Relevance to thesis
- [SRQ4]: Methodological backbone for designing and justifying the thesis's judge protocol (favour pairwise comparison, structured outputs, and a separate judge model).

## Gap / limitation
Preprint survey; provides no transferable empirical reliability figure for the thesis's specific judge. Pair with Ye et al. (2024) for bias specifics. Full text read via arXiv HTML (v6); conclusion truncated in render.
