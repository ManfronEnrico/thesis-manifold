---
name: SRQ1 — Lightweight Forecasting Models & Efficiency
description: SRQ1 (v4) scope, selection criteria, and chapter mapping
category: reference
applies-to: [literature-curation, ch3-methodology, ch6-model-benchmark]
triggers: [srq1, model benchmark, forecasting accuracy, memory efficiency, category specialisation]
created: 2026_04_20-00_00
updated: 2026_08_11-00_00
---

# SRQ1: Lightweight Forecasting Models & Efficiency

> **v4 — canonical.** Wording mirrors
> [research-questions.md](research-questions.md) and
> `05_thesis_writing/sections-drafts/ch1-introduction.md` §1.3. Ch1 is the editing
> surface; this file is scope/curation context, not a second source of truth for wording.

## Research Question

**Which lightweight forecasting models provide the best trade-off between accuracy, memory efficiency, and category specialization for FMCG demand forecasting under computational constraints?**

## What changed from v2

The v2 wording ("Which predictive modelling approaches provide the best balance between
forecasting accuracy and computational efficiency under realistic cloud resource
constraints?") was generic. v4 narrows it on three axes:

- **lightweight** models specifically — deep/transformer architectures are excluded by
  delimitation (8 GB RAM), not left as an open comparison
- **FMCG demand forecasting** as the concrete domain, not "predictive modelling" broadly
- **category specialization** added as a third trade-off dimension alongside accuracy and
  memory — i.e. does a per-category model beat a single pooled model?

## Scope

1. **Lightweight model families**: statistical baselines, linear models, tree ensembles
2. **Accuracy**: error metrics appropriate to intermittent/volatile FMCG demand
3. **Memory efficiency**: peak RAM under a fixed budget; profiling methodology
4. **Forecast stability**: run-to-run and revision stability, not accuracy alone
5. **Category specialization**: per-category vs pooled modelling across the five categories

## Paper Selection Criteria

Include papers on:
- Classical forecasting methods (ARIMA, exponential smoothing, state space)
- Tree ensembles and gradient boosting for demand forecasting
- Benchmarking studies comparing multiple model families on retail/FMCG data
- Memory, latency, and cost profiling of ML models; resource-constrained deployment
- Exogenous/explanatory variables in demand forecasting (promotions, distribution, calendar)
- Forecast stability as an evaluation dimension
- Pooled vs. per-segment/per-category modelling strategies

Exclude papers on:
- Deep/transformer forecasters presented without a resource-cost analysis — these are
  outside the delimitation and only cited as excluded-on-RAM-grounds context
- Pure classification problems
- Purely theoretical complexity analysis without empirical evaluation

## Key Concepts to Track

- **Accuracy**: which metric, and is it robust to zero/low-volume periods?
- **Memory**: peak RSS or tracemalloc? Train vs. inference separated?
- **Stability**: is forecast revision volatility measured at all?
- **Specialisation**: evidence for or against pooling across heterogeneous categories
- **Exogenous features**: which ones actually moved accuracy, and by how much?

## Chapter Mapping

| Chapter | Role for SRQ1 |
|---|---|
| Ch. 3 — Methodology | Models, metrics, benchmark protocol, RAM profiling method |
| Ch. 4 — Data Assessment | Category structure and forecasting suitability of the Nielsen panel |
| Ch. 6 — Model Benchmark | The empirical answer: accuracy × memory × stability × specialisation |

## Related

- [research-questions.md](research-questions.md) — all four SRQs, v4 canonical
- [srq2-tool-interface.md](srq2-tool-interface.md) — consumes SRQ1's selected model
- `../literature/rq_evolution.md` — v1/v2 history
