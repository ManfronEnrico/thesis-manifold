---
name: SRQ4 — Dedicated ML Integration vs Code-as-Action LLM
description: SRQ4 (v4) scope, selection criteria, evaluation design, and chapter mapping
category: reference
applies-to: [literature-curation, ch3-methodology, ch8-evaluation]
triggers: [srq4, code-as-action, baseline, llm-as-judge, correctness, consistency, replicability]
created: 2026_08_11-00_00
updated: 2026_08_11-00_00
---

# SRQ4: Dedicated ML Integration vs. Code-as-Action LLM

> **v4 — canonical.** Replaces the v2 file `srq4-comparison-to-traditional-bi.md`, whose
> question (comparison against traditional descriptive BI) is retired as the SRQ4 baseline.
> v2 wording is preserved in `../literature/rq_evolution.md` and git history. Wording mirrors
> [research-questions.md](research-questions.md) and `ch1-introduction.md` §1.3.

## Research Question

**To what extent does integrating dedicated lightweight forecasting models into an agentic decision-support system improve the correctness, consistency, and replicability of forecast-informed decision-support outputs, at justified cost and latency, compared with a general-purpose LLM that writes and self-corrects its own forecasting code (a code-as-action baseline)?**

## What changed — and why it matters most

This is the SRQ that moved furthest. The baseline has been raised twice:

| Version | Baseline | Retired because |
|---|---|---|
| v2 | Traditional descriptive BI (OLAP, dashboards) | Too weak — beating a dashboard proves little |
| v3 | Non-agentic forecast template | Still a straw man |
| **v4** | **Code-as-action LLM** (writes + executes + self-corrects its own forecasting code) | Current — adopted 2026-06-17, Manifold-endorsed |

The v4 baseline inverts the burden of proof. The question is no longer "is AI better than a
dashboard?" but **"is dedicated ML integration warranted at all, or is an LLM with a code
sandbox already sufficient?"** (Nika's open question, 17/06 meeting). A null result is a
legitimate and publishable finding here.

Consequence: code-as-action is **no longer "future work"** — it is the central comparator.

## Evaluation design (v4)

- **Primary dimensions**: correctness, consistency, replicability
- **Secondary dimensions**: cost, latency
- **Frame**: maps to the CLEAR multidimensional-evaluation frame (Mehta, 2025)
- **Target prompt set**: ≈ 50
- **Judging**: separate judge model with bias awareness + a human-rated subset
- **Feasibility**: the code-as-action baseline runs locally (E2B sandbox), so SRQ4 does
  **not** depend on Prometheus access
- **Scale caveat (Ch1 §1.3)**: Ch. 8 reports a **pilot-scale** evaluation. The full run
  across the target prompt set — and an optional comparison against the non-predictive
  production reference system — are stated as further work. Do not describe Ch. 8 as a
  full-scale study.

## Paper Selection Criteria

Include papers on:
- Code-as-action / executable-action LLM agents and self-correction loops
- Specialised/dedicated models vs. general-purpose LLMs (accuracy, cost, latency trade-offs)
- LLM-as-judge methodology, judge bias, and human-rating protocols
- Multidimensional evaluation frameworks for agentic and LLM systems
- Reproducibility, determinism, and output consistency of LLM systems
- Cost- and latency-aware evaluation of AI systems
- LLMs as forecasters, and their limits

Exclude papers on:
- Traditional BI / OLAP / dashboard architecture as a comparison baseline (v2 scope, retired)
- Benchmarks reporting accuracy only, with no cost, latency, or consistency dimension
- Pure data visualisation

## Key Concepts to Track

- **Baseline strength**: is the LLM baseline given a fair shot (tools, retries, sandbox)?
- **Consistency measurement**: how is run-to-run variance actually quantified?
- **Judge validation**: is the judge checked against human ratings?
- **Cost accounting**: tokens, wall-clock, and infrastructure — or just one of them?

## Chapter Mapping

| Chapter | Role for SRQ4 |
|---|---|
| Ch. 3 — Methodology | Evaluation design, metric definitions, judge protocol |
| Ch. 8 — Evaluation | The pilot comparative evaluation |
| Ch. 9 — Discussion | Interpretation, including a possible null result |

## Related

- [research-questions.md](research-questions.md) — all four SRQs, v4 canonical
- `../literature/obisdian_paper_analysis/` — see the code-as-action and
  specialised-models-vs-LLM paper notes
