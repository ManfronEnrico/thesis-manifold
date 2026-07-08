---
title: "InfiAgent-DABench: Evaluating Agents on Data Analysis Tasks"
authors: Xiao Hu, Zhihan Zhao, Shaopan Wei, Zihao Chai, Qixin Ma, Guang Wang, Xiaowen Wang, Jianfeng Su, Junjie Xu, Ming Zhu, Yu Cheng, Jiabao Yuan, Jiacheng Li, Kun Kuang, Yiquan Yang, Hongtao Yang, Fei Wu
year: 2024
venue: ICML 2024 (PMLR Vol. 235)
url: https://proceedings.mlr.press/v235/hu24s.html
tier: 1 — Core Essential
score: 9
angles: [LLM/Agent Requirements, Code-as-action Evaluation]
srqs: [SRQ4]
peer_reviewed: true
---

## Core argument
LLM agents that solve data-analysis tasks by writing and executing code against a live
execution environment can be evaluated rigorously and at scale. The paper introduces the first
benchmark purpose-built for this paradigm, converting open-ended analysis into automatically
gradable form.

## Method
InfiAgent-DABench: 603 questions over 124 real CSV datasets, posed to LLM agents that operate in
a sandboxed code-execution loop (write → run → observe → refine). Uses a "format-prompting"
technique to turn open-ended analytical questions into closed, machine-checkable answers.
Benchmarks 34 LLMs and introduces DAAgent, an agent specialised for data analysis.

## Key finding
The code-writing-and-executing agent paradigm can be measured for correctness at scale; current
LLMs show a wide and uneven performance spread on end-to-end data-analysis tasks, exposing
reliability gaps in the "LLM writes its own analysis code" approach.

## Relevance to thesis
- SRQ4: the canonical peer-reviewed grounding for the **code-as-action LLM baseline** — an LLM
  that writes, runs, and self-corrects its own analysis/forecasting code in a sandbox (our E2B
  baseline). Legitimises both the baseline design and the **correctness** metric used to compare
  it against dedicated lightweight ML models.
- Complements [[executable_code_actions]] (CodeAct = the *method*; InfiAgent-DABench = the
  *evaluation* of the same paradigm on data-analysis tasks).

## Gap / limitation
Benchmark is task-completion oriented and domain-general (generic CSV analysis), not FMCG demand
forecasting under a RAM/cost budget. Does not measure deployment cost, latency, or memory — the
secondary (cost-justified) dimension of our SRQ4 must come from elsewhere (see
[[specialised_ml_outperform_llms_cost]]).
