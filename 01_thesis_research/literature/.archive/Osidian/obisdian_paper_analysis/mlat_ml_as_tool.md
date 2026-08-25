---
title: "Machine Learning as a Tool (MLAT): A Framework for Integrating Statistical ML Models as Callable Tools within LLM Agent Workflows"
authors: [Chen, Edwin, Bibi, Zulekha]
year: 2026
venue: "arXiv:2602.14295 [PREPRINT — Gemini 3 Hackathon submission; NOT peer-reviewed]"
url: https://arxiv.org/abs/2602.14295
tier: 3 — Emerging precedent (weak evidence; preprint)
score: 4
srqs: [Main, SRQ2]
tags: [gap-G, llm-agent, tool-interface, preprint, emerging-precedent]
ch2_section: "2.7 Gap: extending non-predictive agentic systems with forecasting"
---

## Core argument
LLM agents call APIs and databases but rarely call pre-trained statistical ML models; for quantitative business tasks ML models outperform LLMs, while LLMs excel at contextual reasoning. The paper formalises the "ML model as a callable agent tool" (MLAT) pattern.

## Method
An XGBoost model is served via API and exposed as an agent tool; a structured-output schema bridges LLM reasoning to the model's feature vector; the agent invokes the tool, then reasons over the prediction rather than inserting it blindly. Demonstrated on a pricing case (N=70, ~43% synthetic data).

## Key finding
The pattern works as a proof of concept (XGBoost R²≈0.81; the agent contextualises the prediction). Authors describe MLAT as "an underexplored but high-value design pattern."

## Key quote
> Statistical ML models as agent-callable tools are "conspicuously absent" from current agentic frameworks (paraphrase of stated motivation).

## Relevance to thesis
- [Main/SRQ2]: The closest published articulation of the thesis's exact mechanism — exposing a forecasting model to an LLM agent through a structured tool interface. **Use only to support the narrow claim that this pattern is emerging but underdeveloped, especially in production-oriented decision-support.**

## Gap / limitation
Non-peer-reviewed hackathon paper; tiny single-domain dataset (N=70, 43% synthetic); no calibration; no production/reliability treatment; not FMCG. **Carries no empirical weight — design-pattern precedent only. Do not use to claim our implementation is validated.**
