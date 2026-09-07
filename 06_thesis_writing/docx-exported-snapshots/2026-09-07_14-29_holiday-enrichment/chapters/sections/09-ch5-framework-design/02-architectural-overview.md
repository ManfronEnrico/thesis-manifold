# Architectural Overview

> Section of **Predictive-Extension Architecture > Architectural Overview**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- VERIFY, INCORRECT. Detail: `comments/sections/09-ch5-framework-design/02-architectural-overview.md`

---

The predictive extension is organised in three layers:
a **forecasting substrate**, a set of lightweight machine learning models that produce point forecasts and interval information (SRQ1; benchmarked in Chapter 6);
a **structured forecast-tool interface**, a JSON-based function-calling contract through which the substrate is exposed to the agentic layer as a callable tool (SRQ2);
a **bounded tool-using agentic decision-support layer**, an LLM orchestrator that invokes the substrate through the interface and synthesises a confidence-qualified recommendation, with human-in-the-loop checkpoints.
In the conceptual taxonomy of Sapkota et al. (2025), the artefact at its current stage is most accurately described as a **bounded tool-using AI agent** with human oversight, rather than a full multi-agent Agentic AI system. A multi-agent decomposition, in which specialist agents coordinate, is a production-target and future-work consideration, not a property of the evaluated artefact. This deliberate boundary keeps the system auditable and within the resource budget.
The layers are coordinated by a lightweight Python coordinator that passes typed state between components. This lightweight coordinator is the evaluated implementation. The production target, exemplified by Manifold AI’s Prometheus platform, is a LangGraph-based deployment whose concrete integration point is the Prometheus Graph Engine; that production substrate is the object of the integration-readiness assessment (SRQ3, Section 5.6), not the evaluated implementation. The architecture is summarised in  ***Figure*** ***1***.
**Figure** **2** - Architectural Overview
The predictive-extension architecture. A lightweight Python coordinator (≤ 4 GB RAM, one model resident at a time, the LLM kept out-of-process via remote API) wraps three layers: a forecasting substrate of five lightweight models (SRQ1), a structured JSON forecast-tool interface preserving reliability, uncertainty, and traceability (SRQ2), and a bounded tool-using agentic layer that produces a confidence-qualified, auditable recommendation (informing SRQ3). The dedicated-model path is compared against a code-as-action LLM baseline on correctness, consistency, replicability, cost, and latency (SRQ4).
