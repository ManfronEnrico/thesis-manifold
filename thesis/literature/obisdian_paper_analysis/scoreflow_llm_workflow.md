---
title: "ScoreFlow: Mastering LLM Agent Workflows via Score-based Preference Optimization"
authors: [Wu, Yinjie, et al.]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2502.04306
tier: 2 — High Relevance
score: 7
srqs: [SRQ2]
---

## Core argument
ScoreFlow introduces a method to optimise multi-agent LLM workflows by framing workflow quality as a differentiable score-based preference signal. Rather than treating workflow design as a discrete search or manual process, ScoreFlow uses continuous preference optimisation — scored by an LLM judge or task metric — to iteratively improve the structure and parameterisation of agentic workflows. The paper argues this yields more robust and higher-performing workflows than prior combinatorial or prompt-based approaches.

## Method
A scoring function (either rule-based metric or LLM-as-judge) evaluates workflow execution traces; preference pairs (higher-scored vs lower-scored trajectories) are used to fine-tune workflow generation via a preference optimisation objective. Experiments are run on code generation, mathematical reasoning, and question-answering benchmarks.

## Key finding
ScoreFlow outperforms prior workflow optimisation baselines (including OPRO and DSPy) by 4–7% on average across benchmarks, with particularly large gains on multi-step reasoning tasks requiring complex agent coordination.

## Key quote
> "ScoreFlow treats workflow optimisation as a score-based preference learning problem, enabling continuous improvement of LLM agent pipelines without requiring discrete search or manual redesign."

## Relevance to thesis
- [SRQ2]: The LLM-as-judge scoring mechanism in ScoreFlow is directly relevant to the thesis Validation Agent, which must assess recommendation quality using an LLM-based evaluation protocol (Level 2 validation).
- [SRQ2]: The preference optimisation framing offers a methodological basis for iteratively improving the Synthesis Agent's output quality based on measurable recommendation scores.

## Gap / limitation
ScoreFlow is evaluated purely on reasoning and coding benchmarks with no application to business analytics or time-series forecasting. It does not address RAM constraints, integration with lightweight ML models (LightGBM, ARIMA, Prophet), or the specific challenge of synthesising heterogeneous probabilistic forecasts into actionable managerial guidance. The preference optimisation loop requires repeated LLM inference across many traces, which is computationally expensive under the thesis's 8GB RAM constraint.
