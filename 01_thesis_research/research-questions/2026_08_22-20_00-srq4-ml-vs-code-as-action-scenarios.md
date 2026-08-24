---
name: SRQ4 — Dedicated ML Integration vs Code-as-Action LLM
description: SRQ4 (v4) scope, selection criteria, evaluation design, and chapter mapping
category: reference
applies-to: [literature-curation, ch3-methodology, ch8-evaluation]
triggers: [srq4, code-as-action, baseline, llm-as-judge, correctness, consistency, replicability]
created: 2026_08_11-00_00
updated: 2026_08_22-20_00
---

# SRQ4: Dedicated ML Integration vs. Code-as-Action LLM

> **v4 — canonical.** Replaces the v2 file `srq4-comparison-to-traditional-bi.md`, whose
> question (comparison against traditional descriptive BI) is retired as the SRQ4 baseline.
> v2 wording is preserved in `../literature/rq_evolution.md` and git history. Wording mirrors
> [research-questions.md](research-questions.md) and `ch1-introduction.md` §1.3.

## Research Question

**To what extent does giving an agentic decision-support system access to dedicated lightweight forecasting models improve the correctness, consistency, and replicability of forecast-informed decision-support outputs, at justified cost and latency, relative to the same system with only data access and code execution (a code-as-action baseline), and does that improvement hold in a production agentic system as well as in a general-purpose one?**

## What changed — and why it matters most

This is the SRQ that moved furthest. The baseline has been raised twice:

| Version | Baseline | Retired because |
|---|---|---|
| v2 | Traditional descriptive BI (OLAP, dashboards) | Too weak — beating a dashboard proves little |
| v3 | Non-agentic forecast template | Still a straw man |
| v4 | Code-as-action LLM (writes + executes + self-corrects its own forecasting code) | Superseded — a two-arm framing, adopted 2026-06-17 |
| **v5** | **The same system at a lower capability level**, run across two orchestrators (a five-rung ladder) | Current — adopted 2026-08-22 after Prometheus access landed |

The v4 baseline inverts the burden of proof. The question is no longer "is AI better than a
dashboard?" but **"is dedicated ML integration warranted at all, or is an LLM with a code
sandbox already sufficient?"** (Nika's open question, 17/06 meeting). A null result is a
legitimate and publishable finding here.

Consequence: code-as-action is **no longer "future work"** — it is the central comparator.

## Evaluation design (v4)

- **Primary dimensions**: correctness, consistency, replicability
- **Secondary dimensions**: cost, latency
- **Frame**: maps to the CLEAR multidimensional-evaluation frame (Mehta, 2025)
- **Prompt set**: ~~≈ 50~~ **1 prompt × N repeats per scenario × brand.** Repeats are
  what measure *consistency*, which a single pass over 50 varied prompts cannot do.
  Brand selection is stratified (highest / median / lowest volume among brands with a
  fully non-zero test window), so results span the volume range rather than only the
  largest series.
- **Judging**: ~~separate judge model with bias awareness + a human-rated subset~~
  **DROPPED (B-DEC-2).** All metrics are now **programmatic**: forecast error against
  held-out actuals, run-to-run variance, token cost, wall-clock latency. No model
  judges another model's output. This removes judge bias as a threat to validity and
  removes the human-rating protocol from scope.
- **Feasibility**: the code-as-action baseline runs locally (E2B sandbox), so SRQ4 did
  **not** depend on Prometheus access. **Access has since landed (2026-08-20)** and the
  design was extended rather than replaced — see the scenario ladder below.
- **Scale caveat (Ch1 §1.3)**: Ch. 8 reports a **pilot-scale** evaluation. The full run
  across the target prompt set — and an optional comparison against the non-predictive
  production reference system — are stated as further work. Do not describe Ch. 8 as a
  full-scale study.

## The scenario ladder as implemented (2026-08-22)

The two-arm framing in the research question understates the design. Five scenarios
are implemented, with a sixth proposed:

| Scenario | Engine | Forecast access |
|----------|--------|-----------------|
| `A_plain` | GPT-5.5 | none |
| `B_data` | GPT-5.5 | code execution (E2B sandbox) — the code-as-action baseline |
| `C_model` | GPT-5.5 | `forecast_demand` tool |
| `D_prometheus` | **Prometheus Graph Engine** | none (code-as-action, as shipped) |
| `E_prometheus_model` | **Prometheus Graph Engine** | `forecast_demand` tool |
| `F_ensemble` *(proposed)* | GPT-5.5 | pooled + specialised, with accuracy context |

**One variable per rung.** `A→B` measures what data access buys; `B→C` what the
trained model buys in a generic LLM; `D→E` what it buys in the production agent.

**`B→C` and `D→E` are the same intervention on two different orchestrators** — an
intentional replication, and the strongest structural feature of the design. If both
move the same direction, the finding is not an artefact of one harness.

**Reproducibility is deliberately two-tier.** A–C are reproducible from the repository
plus an API key; D–E are ecological validation in a proprietary production system that
nobody outside the collaboration could reproduce. Neither tier alone covers both
internal and external validity — present this as a design property, not an apology.

**A note on `B_data`'s role:** it was built as a proxy for Prometheus while access was
pending. Now that `D_prometheus` exists, B is no longer standing in for anything — it
is "a generic LLM with code execution." State this explicitly in the methodology; a
reviewer who notices the reframing unprompted will read it as drift.

**RQ wording updated to v5 (2026-08-22, Brian-approved).** The question now says
"the same system with only data access and code execution" rather than "a
general-purpose LLM", and adds a clause asking whether the improvement holds in a
production agentic system as well as a general-purpose one. That second clause is the
`B→C` / `D→E` replication, which the v4 wording did not convey at all. Ch1 §1.3 was
updated to match.

## Paper Selection Criteria

Include papers on:
- Code-as-action / executable-action LLM agents and self-correction loops
- Specialised/dedicated models vs. general-purpose LLMs (accuracy, cost, latency trade-offs)
- ~~LLM-as-judge methodology, judge bias, and human-rating protocols~~ **NO LONGER
  NEEDED** — judging is programmatic (B-DEC-2)
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
