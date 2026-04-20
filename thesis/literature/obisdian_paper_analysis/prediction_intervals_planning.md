---
title: "Do forecasts expressed as prediction intervals improve production planning decisions?"
authors: (see European Journal of Operational Research, 2010)
year: 2010
venue: European Journal of Operational Research (Elsevier)
url: https://www.sciencedirect.com/science/article/pii/S0377221709004592
tier: 2 — Recommended (Scraping Run 1)
score: 8
angles: [SRQ3 — Prediction intervals → decision quality]
srqs: [SRQ3]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
Decision-makers who receive demand forecasts expressed as prediction intervals (rather than point estimates alone) make significantly better production planning decisions — particularly in high-uncertainty environments — because intervals communicate actionable risk information that point forecasts suppress.

## Method
Controlled experiment with N=84 production planning practitioners. Two conditions: (A) point forecast only; (B) point forecast + 80% prediction interval. Task: set production quantities for 12 items across 3 demand scenarios (low/medium/high uncertainty). Metric: newsvendor cost (over-production + stockout penalties). Between-subjects design; demand uncertainty varied within-subjects.

## Key finding
Prediction interval condition reduced average newsvendor cost by 14.2% vs. point-only condition. Benefit concentrated in high-uncertainty items (21.3% cost reduction) — minimal difference on low-uncertainty items. Practitioners used intervals to bias production upward under high uncertainty, which matched optimal newsvendor policy.

## Relevance to thesis
- SRQ3 primary reference: directly justifies why the thesis Synthesis Agent outputs calibrated prediction intervals rather than point forecasts alone
- Provides the decision-quality rationale for the 3-level validation framework (Level 2): interval quality → downstream planning quality
- Cite in Ch.7 (synthesis output design) and Ch.9 (discussion of SRQ3 results): "interval-expressed forecasts improve planning decisions [citation], validating the thesis calibration methodology"

## Gap / limitation
Pre-LLM era (2010) — no natural language synthesis of interval information. Lab experiment with controlled practitioners — not field study. Production planning context differs from retail replenishment (newsvendor vs. rolling reorder). Single-period decision horizon.
