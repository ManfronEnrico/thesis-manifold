---
name: SRQ3 — Integration Readiness
description: SRQ3 (v4) scope, selection criteria, and chapter mapping
category: reference
applies-to: [literature-curation, ch5-framework-design, ch7-synthesis, ch9-discussion]
triggers: [srq3, integration readiness, production agentic system, prometheus, graph engine]
created: 2026_08_11-00_00
updated: 2026_08_22-20_00
---

# SRQ3: Integration Readiness

> **v4 — canonical.** Replaces the v2 file `srq3-contextual-information.md`, whose question
> ("To what extent does additional contextual information improve…") is retired along with
> the Indeks Danmark consumer-survey enrichment scope. v2 wording is preserved in
> `../literature/rq_evolution.md` and git history. Wording mirrors
> [research-questions.md](research-questions.md) and `ch1-introduction.md` §1.3.

## Research Question

**What architectural and operational capabilities are required for a production-oriented agentic system to integrate forecast-informed decision-support?**

## What changed from v2

v2 SRQ3 was about **contextual information / feature enrichment** — whether consumer-survey
signals improved predictions. That scope is gone. v4 SRQ3 is an **integration-readiness
question about the host system**: what must a production agentic system already be able to do
before a forecasting substrate can be bolted on at all.

Per the v4 notes, this was framed as an **assessment**, not a completed integration,
partly because Prometheus access was pending (NDA + dev merge).

> **ACCESS HAS LANDED (2026-08-20).** The Prometheus Graph Engine was delivered,
> inspected, and now runs locally with its own environment and E2B sandbox template.
> The constraint that partly motivated the assessment framing no longer applies.
>
> **RESOLVED 2026-08-22 — a middle position, and Ch1 §1.3 now states it.**
>
> The framing that ships is: **readiness criteria derived from a working integration,
> without claiming a completed production deployment.**
>
> The reasoning that decided it: **the integration is happening regardless.** Scenario
> `E_prometheus_model` *is* `forecast_demand` running inside the Prometheus engine, and
> plan task 6 is literally "port `forecast_demand` to the verified API". SRQ4 cannot run
> without it. So the question was never whether to integrate — only whether SRQ3 claims
> that work as its evidence or leaves it as SRQ4's apparatus.
>
> Grounding the criteria in what the integration actually depended on is stronger
> evidence than architectural analysis alone, and costs no additional work.
>
> **What is explicitly NOT claimed**, and Ch1 says so: operational hardening, monitoring
> at scale, and organisational adoption. The integration is conducted for evaluation
> within a research collaboration, not deployed to production users.
>
> **One contingency to watch.** This framing assumes scenario E runs. If the integration
> hits a wall that cannot be cleared, revert to the pure-assessment framing — it remains
> fully available and nothing is lost. Decide finally after plan task 6 completes.

## The capabilities under assessment (Ch1 §1.3)

1. A structured tool interface for invoking external predictive models
2. Observability and traceability of tool calls
3. Explicit handling of reliability and uncertainty
4. Operation within bounded cost, latency, and memory

## Scope

1. **Architectural prerequisites**: what the host system's extension points must look like
2. **Operational prerequisites**: monitoring, logging, cost/latency budgets
3. **Readiness assessment method**: how capabilities are evidenced against a real production
   system used as the empirical case
4. **Gap identification**: which capabilities the reference system has, lacks, or partially has

## Paper Selection Criteria

Include papers on:
- Production-oriented / deployed agentic systems and their architecture
- Integration of ML components into existing enterprise or industrial systems
- Capability, maturity, or readiness models for AI/analytics adoption
- Observability, monitoring, and evaluation of agentic workflows in production
- Hybrid deterministic + LLM architectures (the closest architectural analogues)
- Technical debt and operational concerns in deployed ML systems

Exclude papers on:
- Contextual feature engineering as a topic in itself (v2 scope, retired)
- Greenfield agent designs with no deployment or integration dimension
- Organisational change management without an architectural component

## Key Concepts to Track

- **Extension points**: how does the paper's system admit a new capability?
- **Evidence base**: derived from a real deployment, or proposed a priori?
- **Readiness criteria**: are they stated as checkable criteria, or narrative?
- **Operational bounds**: are cost/latency/memory treated as design constraints?

## Chapter Mapping

| Chapter | Role for SRQ3 |
|---|---|
| Ch. 5 — Framework Design | The integration-readiness specification |
| Ch. 7 — Synthesis | Assessment against the production reference system |
| Ch. 9 — Discussion | Integration-readiness findings and their generalisability |

## Related

- [research-questions.md](research-questions.md) — all four SRQs, v4 canonical
- [srq2-tool-interface.md](srq2-tool-interface.md) — the interface whose adoption SRQ3 assesses
- `../../00_thesis_context/prometheus-integration/` — Prometheus/Graph Engine integration context
