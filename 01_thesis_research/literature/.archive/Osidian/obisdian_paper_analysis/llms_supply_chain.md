---
title: "LLMs in Supply Chain Management: Opportunities and a Case Study"
authors: (see IFAC-PapersOnLine, ScienceDirect, 2025)
year: 2025
venue: IFAC-PapersOnLine (ScienceDirect)
url: https://www.sciencedirect.com/science/article/pii/S2405896325012595
tier: 2 — Recommended (Scraping Run 1)
score: 8
angles: [SRQ2 — LLM + forecasting]
srqs: [SRQ2]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
LLMs add value in supply chain management not as direct forecasters, but as orchestrators that interpret, contextualise, and translate structured ML outputs into actionable recommendations for human decision-makers.

## Method
Case study: LLM (GPT-4) integrated with an existing demand planning system at a mid-sized CPG manufacturer. LLM role: interpret forecast outputs, generate restocking recommendations, flag anomalies, explain forecast drivers in natural language. Human evaluation of recommendation quality.

## Key finding
LLM-generated recommendations rated as "actionable" by 78% of category managers, vs. 45% for raw ML forecast outputs. LLM adds value primarily through contextualisation (explaining *why* the forecast changed) and uncertainty flagging.

## Relevance to thesis
- SRQ2: directly supports the thesis Synthesis Agent design — LLM orchestrates ML outputs into actionable recommendations, not replaces them
- Validates the 5-step synthesis pipeline approach (ensemble → LLM recommendation)
- CPG manufacturer context is directly analogous to the thesis's Manifold AI / Nielsen CSD setting

## Gap / limitation
Single-company case study. LLM used as post-hoc interpreter, not as part of a multi-agent framework. No confidence scoring or calibration methodology. No RAM/compute constraints reported.
