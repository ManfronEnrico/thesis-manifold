---
title: "AIRepr: An Analyst-Inspector Framework for Evaluating Reproducibility of LLMs in Data Science"
authors: Qiuhai Zeng, Chuan Jin, Xiao Wang, Yuhao Zheng, Qi Li
year: 2025
venue: Findings of the ACL — EMNLP 2025
url: https://doi.org/10.48550/arXiv.2502.16395
tier: 1 — Core Essential
score: 9
angles: [LLM Data-Science Reproducibility, Code-as-action Evaluation]
srqs: [SRQ4]
peer_reviewed: true
---

## Core argument
The reproducibility of LLM-generated data-analysis workflows can be automatically assessed and
improved. Reproducibility is a measurable, first-class quality dimension for LLM-written
analysis code — not just accuracy.

## Method
An analyst-inspector framework: one LLM ("analyst") produces a data-science workflow, a second
LLM ("inspector") evaluates whether the workflow reproduces. Evaluated across 15 analyst-inspector
LLM pairs on 1,032 tasks drawn from three public benchmarks. Introduces two prompting strategies
shown to raise reproducibility.

## Key finding
Workflows with higher reproducibility scores also yield more accurate analyses — i.e.
reproducibility and correctness are coupled. LLM-written analysis pipelines vary substantially in
how reliably they reproduce.

## Relevance to thesis
- SRQ4: directly operationalises **replicability/reproducibility of LLM-written analysis code**,
  one of our three primary SRQ4 metrics (correctness, consistency, replicability). Gives a
  citable definition and method for the dimension where a dedicated, fixed ML pipeline is expected
  to dominate a code-generating LLM baseline.
- Pairs with [[infiagent_dabench]] (correctness) and [[clear_enterprise_agentic_eval]] (CLEAR
  multidimensional eval) to cover the SRQ4 metric set.

## Gap / limitation
Cite the arXiv preprint URL until the ACL Anthology page is live (accepted to EMNLP 2025
Findings). Domain is general data science, not FMCG forecasting; reproducibility is measured via
LLM inspection rather than execution-level determinism, so transfer to our forecasting setting
needs framing.
