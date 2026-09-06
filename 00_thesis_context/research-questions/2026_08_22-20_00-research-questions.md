---
name: Research Questions
description: Main RQ + 4 SRQs (v4) — source of truth for all thesis components, mirroring ch1-introduction.md §1.3
updated: 2026_08_22-20_00
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
- **SRQ4 — ML Integration vs Code-as-Action, across two orchestrators**: To what extent does giving an agentic decision-support system access to dedicated lightweight forecasting models improve the correctness, consistency, and replicability of forecast-informed decision-support outputs, at justified cost and latency, relative to the same system with only data access and code execution (a code-as-action baseline), and does that improvement hold in a production agentic system as well as in a general-purpose one?

## Scope decisions

- **SRQ1** — comparison spans all four categories; relative model ranking on identical data,
  with Diebold-Mariano significance testing.
- **SRQ2** — the artefact is a typed tool call carrying point forecast, calibrated 90%
  interval, confidence score, source attribution and traceability metadata. Feature
  construction stays server-side; the LLM never handles feature vectors.
- **SRQ3** — an integration-readiness **assessment**, not a completed integration. Target is
  the Prometheus **Graph Engine**. **Access landed 2026-08-20**; the engine runs locally.
  Whether SRQ3 is promoted to a completed integration is now an **open scope decision**
  for Brian and Enrico, not a question access settles by itself.
- **SRQ4** — baseline is a **code-as-action LLM** (writes, executes and self-corrects its own
  forecasting code), runnable locally in an E2B sandbox. Metrics: **correctness, consistency,
  replicability** (primary) + **cost, latency** (secondary), per the CLEAR evaluation frame
  (Mehta, 2025). Ch8 reports a **pilot**; the full run is stated as further work.
  **Superseded details (2026-08-22):**
  - **LLM-as-judge is DROPPED** (B-DEC-2) — all metrics are programmatic.
  - **Prompt set is 1 prompt × N repeats**, not ≈50 varied prompts; repeats are what
    measure consistency. Brands are stratified across the volume range.
  - **Five scenarios, not two arms** — A_plain, B_data, C_model, D_prometheus,
    E_prometheus_model (F_ensemble proposed). See the SRQ4 scope file.

## Per-SRQ scope files

| SRQ | Scope file | Chapters |
|---|---|---|
| SRQ1 | [srq1-models-efficiency.md](srq1-models-efficiency.md) | Ch. 3, 4, 6 |
| SRQ2 | [srq2-tool-interface.md](srq2-tool-interface.md) | Ch. 3, 5, 7 |
| SRQ3 | [srq3-integration-readiness.md](srq3-integration-readiness.md) | Ch. 5, 7, 9 |
| SRQ4 | [srq4-ml-vs-code-as-action-scenarios.md](srq4-ml-vs-code-as-action-scenarios.md) | Ch. 3, 8, 9 |

## v5 wording change — SRQ4 (2026-08-22, Brian-approved)

SRQ4's wording was changed to reflect the implemented design. The previous text
described a **two-arm** comparison; the evaluation is a **five-scenario ladder** run
across two orchestrators.

| | Wording |
|---|---|
| v4 | "…compared with a general-purpose LLM that writes and self-corrects its own forecasting code (a code-as-action baseline)?" |
| **v5** | "…relative to the same system with only data access and code execution (a code-as-action baseline), **and does that improvement hold in a production agentic system as well as in a general-purpose one?**" |

Three things the new wording carries that the old did not:

1. **"the same system with…"** — the comparison is within one system at different
   capability levels, not between two different systems. That is what the ladder
   actually does.
2. **The second clause** names the replication (`B→C` and `D→E`), which is the
   design's strongest structural feature and was entirely absent before.
3. It drops "general-purpose LLM" as the sole comparator, since code-as-action now
   appears in both a general-purpose orchestrator (B) and the production one (D).

**Ch1 §1.3 has been updated to match** (2026-08-22). The two must stay in step.

## Ch1 corrections applied 2026-08-22

Also corrected in `05_thesis_writing/sections-drafts/ch1-introduction.md`:

- the dropped **LLM-as-judge** protocol → replaced with programmatic measurement
- "**five** Nielsen product categories … including beer (totalbeer)" → **four**, with
  the exclusion explained rather than silently dropped
- "between 37 and 42 monthly periods" → **up to 44**
- "across the five categories" (Ch6 outline) → four
- SRQ3 reframed to ground the readiness criteria in a working integration

## Source of truth for

- Thesis chapter structure and writing
- Literature curation and inclusion criteria
- Research scope
