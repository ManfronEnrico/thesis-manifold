---
name: Research Questions Evolution
description: Main RQ + 4 SRQs (v4), source of truth for all thesis components — synced to ch1-introduction.md
updated: 2026-06-17
---

# Research Questions (v4)

> **Canonical version.** Synced 2026-06-17 to the approved wording in
> `thesis/thesis-writing/sections-drafts/ch1-introduction.md` §1.3. This file and Ch1 must always match;
> Ch1 is the editing surface, this file mirrors it. v4 adopts the Manifold-aligned reframe (17/06 meeting,
> Enrico–Nika): SRQ4 baseline raised to a code-as-action LLM, Main RQ gains "cost-justified", evaluation
> metrics set to correctness/consistency/replicability (primary) and cost/latency (secondary). Supersedes
> v3 (non-agentic-template baseline) and v2 (multi-agent / contextual-info / vs-BI), retained only in
> [rq_evolution.md](../../docs/literature/rq_evolution.md).

## Main Research Question

**How can production-oriented agentic decision-support systems without native predictive capabilities be extended with lightweight forecasting models to support reliable, forecast-informed, and cost-justified decision-making under computational and deployment constraints?**

## Sub-Research Questions

- **SRQ1 — Models & Efficiency**: Which lightweight forecasting models provide the best trade-off between accuracy, memory efficiency, and category specialization for FMCG demand forecasting under computational constraints?
- **SRQ2 — Structured Tool Interface**: How can forecasting outputs be exposed to an agentic decision-support system through a structured tool/action interface that preserves reliability, uncertainty, and traceability?
- **SRQ3 — Integration Readiness**: What architectural and operational capabilities are required for a production-oriented agentic system to integrate forecast-informed decision-support?
- **SRQ4 — ML Integration vs LLM-Coder**: To what extent does integrating dedicated lightweight forecasting models into an agentic decision-support system improve the correctness, consistency, and replicability of forecast-informed decision-support outputs, at justified cost and latency, compared with a general-purpose LLM that writes and self-corrects its own forecasting code (a code-as-action baseline)?

## Notes

These RQs are the source of truth for:
- Thesis chapter structure and writing
- Literature curation and inclusion criteria
- Research scope

**v4 reframe (adopted 2026-06-17, Manifold-endorsed):**
- SRQ4 baseline is a **code-as-action LLM** (writes + executes + self-corrects its own forecasting code), not a static non-agentic template. The core test is whether dedicated ML integration is warranted at all, or whether LLM + code execution is already sufficient (Nika's open question).
- Evaluation metrics: **correctness, consistency, replicability** (primary) + **cost, latency** (secondary), mapping to the CLEAR multidimensional-evaluation frame (Mehta, 2025); target prompt set ≈ 50.
- The code-as-action LLM baseline is runnable locally (E2B sandbox), so SRQ4 is feasible without Prometheus access.
- **SRQ3** remains an integration-readiness *assessment* for now (Prometheus access pending: NDA + dev merge); the concrete integration target is the Prometheus **Graph Engine**. If access lands, SRQ3 may move to *active* integration.
- code-as-action is therefore **no longer "future work"** but the central SRQ4 comparator (propagation to Ch2/Ch3/Ch10 in progress).

v4 — Synced to Ch1 on 2026-06-17. Full history in [rq_evolution.md](../../docs/literature/rq_evolution.md).
