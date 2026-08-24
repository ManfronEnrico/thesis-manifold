---
name: SRQ2 — Structured Forecast-Tool Interface
description: SRQ2 (v4) scope, selection criteria, and chapter mapping
category: reference
applies-to: [literature-curation, ch5-framework-design, ch7-synthesis]
triggers: [srq2, tool interface, tool calling, uncertainty, traceability, reliability]
created: 2026_08_11-00_00
updated: 2026_08_22-19_00
---

# SRQ2: Structured Forecast-Tool Interface

> **v4 — canonical.** Replaces the v2 file `srq2-multi-agent-architecture.md`, whose
> question ("How can a multi-agent architecture coordinate predictive models and
> heterogeneous data signals…") is retired. v2 wording is preserved in
> `../literature/rq_evolution.md` and git history. Wording mirrors
> [research-questions.md](research-questions.md) and `ch1-introduction.md` §1.3.

## Research Question

**How can forecasting outputs be exposed to an agentic decision-support system through a structured tool/action interface that preserves reliability, uncertainty, and traceability?**

## What changed from v2

v2 asked about **multi-agent coordination** — how many agents, how they talk, how conflicts
resolve. v4 drops that framing entirely. The unit of analysis is now the **interface
contract** between a forecasting substrate and a bounded tool-using agent, not the agent
topology. Three properties are named as design requirements:

- **reliability** — agent outputs validate against the source forecasts
- **uncertainty** — forecasts travel with interval information, not as bare point estimates
- **traceability** — a recorded mapping from tool call → forecast value → recommendation

## Scope

1. **Tool/action interface design**: typed schemas, function calling, contract validation
2. **Uncertainty propagation**: prediction intervals, calibration, how uncertainty survives
   the hand-off to an LLM layer
3. **Traceability**: provenance metadata, tool-call logging, auditability of a recommendation
4. **Reliability guards**: validating generated text against the numeric source of truth
5. **Bounded agent design**: constraining what the agent may do with a forecast

## Paper Selection Criteria

Include papers on:
- LLM tool use and function calling (typed tool schemas, tool-call reliability)
- Code-as-action / executable-action agents (also the SRQ4 comparator — see
  [srq4-ml-vs-code-as-action.md](srq4-ml-vs-code-as-action.md))
- Uncertainty quantification and calibration for regression forecasts
- Communicating uncertainty to decision-makers
- Hallucination detection, groundedness, and output-vs-source validation
- Observability, provenance, and traceability in ML/LLM pipelines
- Agent robustness under noisy or degraded tool output

Exclude papers on:
- Multi-agent coordination/negotiation as a topic in itself (v2 scope, retired)
- General prompt engineering without a tool-interface or reliability angle
- Game-theoretic agent coordination without practical system application

## Key Concepts to Track

- **Schema design**: what does the tool return, and is uncertainty a first-class field?
- **Validation**: how is the agent's claim checked against the forecast it was given?
- **Failure modes**: what happens when the tool returns something unexpected?
- **Traceability granularity**: per-call, per-recommendation, or per-session?

## Interface contract as implemented (2026-08-22)

The artefact has grown since this scope was written. `forecast_demand` returns:

| Field group | Contents |
|---|---|
| Forecast | point estimate, split-conformal 90% interval |
| Confidence | heuristic index + tier (High/Moderate/Low) |
| **Track record** | this model's held-out WMAPE **and** median MAPE |
| **Baselines** | best-by-WMAPE **and** best-by-medMAPE, which can be different models |
| **Disagreement flag** | `metrics_disagree` when the two comparisons contradict |
| Provenance | model file, training cutoff, calibration split, feature count, UTC timestamp |

**Two design principles emerged that belong in the SRQ2 contribution:**

1. *An interface should not serve a number it cannot vouch for, however much caveat
   text accompanies it.* Implausible error rates (a failed model reported 2.8×10¹³%)
   are replaced with an explicit `"n/a"` plus a reason, rather than passed through
   with a warning. A consumer given a caveat still lacks the information to act on it.
2. *Where two metrics disagree, serving one is a choice that must be surfaced.* On one
   category the served model beats the best medMAPE baseline by 7.4pp while losing to
   the best WMAPE baseline by 6.3pp. Reporting either alone would be a framing
   decision disguised as a measurement.

**Caution for the write-up:** the `confidence` score is a **heuristic index** with
hand-chosen weights and tier cutoffs, both derived from the same per-category
quantile. It is not a calibrated probability and has no literature definition.
Describe it as an ordinal hint; let the track-record fields carry the reliability
claim.

## Chapter Mapping

| Chapter | Role for SRQ2 |
|---|---|
| Ch. 3 — Methodology | Interface evaluation approach |
| Ch. 5 — Framework Design | The structured forecast-tool interface design itself |
| Ch. 7 — Synthesis | The realised prototype: agent consuming forecasts through the interface |

**Implementation note (from Ch1 §1.3):** the evaluated prototype uses a lightweight Python
coordinator with JSON-based function calling. LangGraph is the *production* target, not the
implementation evaluated in this thesis — do not describe LangGraph as the evaluated artefact.

## Related

- [research-questions.md](research-questions.md) — all four SRQs, v4 canonical
- [srq3-integration-readiness.md](srq3-integration-readiness.md) — the capabilities a host
  system needs to accept this interface
