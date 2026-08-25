---
title: "A Taxonomy of AgentOps for Enabling Observability of Foundation Model based Agents"
authors: [Dong, Liming, Lu, Qinghua, Zhu, Liming]
year: 2025
venue: "arXiv:2411.05285 [PREPRINT — CSIRO Data61 / UNSW; not a peer-reviewed venue]"
url: https://arxiv.org/abs/2411.05285
tier: 2 — High relevance (reputable institution; preprint)
score: 6
srqs: [SRQ2, SRQ3]
tags: [gap-F, observability, traceability, production-agents, preprint]
ch2_section: "2.6 Production-oriented agentic systems and integration readiness"
---

## Core argument
Reliable outputs from foundation-model agents require observability. The paper asks "what data/artifacts should be traced in AgentOps?" and proposes a taxonomy of traceable artifacts across the agent lifecycle.

## Method
Multivocal review of AgentOps/observability tooling (platforms, observability tools, agent frameworks); derives a taxonomy: creation registry, prompt registry, guardrails, execution (planning/reasoning/memory/workflows), evaluation/feedback, tracing (sessions/traces/spans), monitoring.

## Key finding
Observability must be built into agent platforms from the start; traceability connects to compliance (EU AI Act); the prototype-to-production gap is large; planning/reasoning/memory artifacts are under-covered by current tools.

## Key quote
> Observability is "crucial for LLM-based agents" and should be integrated "from the beginning" rather than added later (paraphrase).

## Relevance to thesis
- [SRQ3]: Supplies the **architectural/operational capabilities** vocabulary (observability, tracing, registries, guardrails) that integration-readiness requires.
- [SRQ2]: Grounds the *traceability* requirement of the structured forecast-tool interface.

## Gap / limitation
Preprint; taxonomy derived from grey-literature review, not empirical deployment. Supports *requirements*, NOT a claim that the thesis prototype implements observability/tracing (the trace log is **planned, not built**).
