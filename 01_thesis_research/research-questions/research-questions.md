---
name: Research Questions
description: Main RQ + 4 SRQs (v4) — source of truth for all thesis components, mirroring ch1-introduction.md §1.3
updated: 2026-08-11
---

# Research Questions (v4)

> **Canonical.** Ch1 §1.3 is the editing surface; this file mirrors it and the two must always
> match. Version history: [rq_evolution.md](../literature/rq_evolution.md).

## Main Research Question

**How can production-oriented agentic decision-support systems without native predictive capabilities be extended with lightweight forecasting models to support reliable, forecast-informed, and cost-justified decision-making under computational and deployment constraints?**

## Sub-Research Questions

- **SRQ1 — Models & Efficiency**: Which lightweight forecasting models provide the best trade-off between accuracy, memory efficiency, and category specialization for FMCG demand forecasting under computational constraints?
- **SRQ2 — Structured Tool Interface**: How can forecasting outputs be exposed to an agentic decision-support system through a structured tool/action interface that preserves reliability, uncertainty, and traceability?
- **SRQ3 — Integration Readiness**: What architectural and operational capabilities are required for a production-oriented agentic system to integrate forecast-informed decision-support?
- **SRQ4 — ML Integration vs LLM-Coder Scenarios**: To what extent does integrating dedicated lightweight forecasting models into an agentic decision-support system improve the correctness, consistency, and replicability of forecast-informed decision-support outputs, at justified cost and latency, compared with a general-purpose LLM that writes and self-corrects its own forecasting code (a code-as-action baseline)?

## Scope decisions

- **SRQ1** — comparison spans all four categories; relative model ranking on identical data,
  with Diebold-Mariano significance testing.
- **SRQ2** — the artefact is a typed tool call carrying point forecast, calibrated 90%
  interval, confidence score, source attribution and traceability metadata. Feature
  construction stays server-side; the LLM never handles feature vectors.
- **SRQ3** — an integration-readiness **assessment**, not a completed integration. Target is
  the Prometheus **Graph Engine**; access pending NDA + dev merge. Moves to active integration
  only if access lands.
- **SRQ4** — baseline is a **code-as-action LLM** (writes, executes and self-corrects its own
  forecasting code), runnable locally in an E2B sandbox, so SRQ4 does not depend on Prometheus
  access. Metrics: **correctness, consistency, replicability** (primary) + **cost, latency**
  (secondary), per the CLEAR evaluation frame (Mehta, 2025). Prompt set ≈ 50. Ch8 reports a
  **pilot**; the full run is stated as further work.

## Per-SRQ scope files

| SRQ | Scope file | Chapters |
|---|---|---|
| SRQ1 | [srq1-models-efficiency.md](srq1-models-efficiency.md) | Ch. 3, 4, 6 |
| SRQ2 | [srq2-tool-interface.md](srq2-tool-interface.md) | Ch. 3, 5, 7 |
| SRQ3 | [srq3-integration-readiness.md](srq3-integration-readiness.md) | Ch. 5, 7, 9 |
| SRQ4 | [srq4-ml-vs-code-as-action.md](srq4-ml-vs-code-as-action.md) | Ch. 3, 8, 9 |

## Source of truth for

- Thesis chapter structure and writing
- Literature curation and inclusion criteria
- Research scope
