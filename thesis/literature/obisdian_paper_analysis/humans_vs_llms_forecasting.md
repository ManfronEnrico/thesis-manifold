---
title: "Humans vs. LLMs: Judgmental forecasting in an era of advanced AI"
authors: (see International Journal of Forecasting, ScienceDirect, 2024)
year: 2024
venue: International Journal of Forecasting (ScienceDirect)
url: https://www.sciencedirect.com/science/article/pii/S0169207024000700
tier: 2 — Recommended (Scraping Run 1)
score: 8
angles: [SRQ4 — Baseline comparison]
srqs: [SRQ4]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
LLMs applied to forecasting tasks match or exceed human judgment forecasting in structured scenarios, but humans retain advantages in contextual, domain-specific, and causal reasoning tasks. The gap closes as LLMs are provided with more domain context.

## Method
Controlled experiment: human forecasters (N=150, professional analysts) vs. GPT-4 and other LLMs on the M4 forecasting competition dataset + a proprietary B2B sales forecasting dataset. Metrics: MAPE, directional accuracy, overconfidence rate. Conditions: zero-shot, few-shot, chain-of-thought.

## Key finding
GPT-4 (zero-shot) achieves MAPE within 15% of professional human forecasters on standard series. With chain-of-thought prompting, gap narrows to < 5%. Humans outperform on series requiring domain knowledge not in training data.

## Relevance to thesis
- SRQ4 framing: establishes that LLM-augmented AI systems are a credible alternative to human-in-the-loop descriptive BI — not just automation of existing dashboards
- Provides the benchmark claim: thesis compares AI synthesis to descriptive BI baseline (not just to human forecasters)
- Supports the thesis position that LLM contribution is in contextualisation and synthesis, not raw forecasting

## Gap / limitation
LLMs tested as direct forecasters (not as synthesis orchestrators over ML models). Does not address confidence calibration, RAM constraints, or multi-agent architecture. Forecasting competition datasets differ from retail CPG panel data.
