---
name: SRQ4 Evaluation Protocol — Specification (blueprint for the from-scratch build)
description: Design spec for the SRQ4 experiment (dedicated-model integration vs code-as-action LLM baseline). NOT code. Guides the rebuild; numbers pending.
status: DRAFT SPEC — design only; to be finalised (open decisions at end) then implemented from scratch
updated: 2026-06-19
---

# SRQ4 Evaluation Protocol (specification)

> This is a **specification document**, not code. All code is being rebuilt from scratch; this spec is the
> blueprint the rebuild should follow. No results exist yet. Aligned to RQs v4.

## 1. Question

**SRQ4**: *To what extent does integrating dedicated lightweight forecasting models into an agentic
decision-support system improve the correctness, consistency, and replicability of forecast-informed
decision-support outputs, at justified cost and latency, compared with a general-purpose LLM that writes
and self-corrects its own forecasting code (a code-as-action baseline)?*

Core test (Nika's open question): *do we even need to integrate dedicated ML models, or is LLM + code
execution already good enough?* Either answer is a valid finding.

## 2. Conditions compared (same task, same data, same base LLM)

- **Condition A — Dedicated-model integration (thesis artefact).** An LLM orchestrator answers each prompt
  by calling, through a structured JSON tool/action interface, the **dedicated lightweight forecasting
  model(s)** built for SRQ1; it receives point forecasts plus interval information, validates the numbers
  against the tool output, and synthesises the decision-support answer. The LLM does **not** compute the
  forecast itself.
- **Condition B — Code-as-action LLM baseline.** The **same base LLM**, given the **same data access**,
  **writes, executes, and self-corrects its own forecasting / analysis code** in a sandboxed environment
  (E2B or equivalent) to produce the answer. No dedicated pre-built model is provided.
- **Held constant across A and B:** the prompt set, the underlying data, the base LLM and its decoding
  settings, the sandbox/data interface, the judge, and the logging. The **only** manipulated variable is
  *dedicated-model integration vs self-written code* (isolates that factor, not LLM quality).
- *(Optional floor condition C — plain LLM, no tools, no code execution: include only if we want a lower
  bound. OPEN DECISION.)*

## 3. Prompt set (~50)

Decision-support prompts over the Nielsen beverage data, grouped by archetype. Proposed taxonomy and
target counts (to finalise):

| Archetype | What it asks | ~count | Ground-truth type |
|---|---|---|---|
| descriptive / arithmetic (single entity) | totals, shares, averages over history | ~8 | deterministic from data |
| multi-entity comparison | brand_vs_brand, channel_ranking, top_performers | ~12 | deterministic from data |
| temporal | yoy_comparison, trend, volatility | ~8 | deterministic from data |
| anomaly / risk | detect outliers, flag risk | ~6 | deterministic / rule-defined |
| **forecasting** | next-period demand for a brand×retailer | ~10 | actual held-out value (backtest) |
| forecast-to-decision | "should stock go up/down for X?" given forecast | ~6 | derived from held-out actual |

Two ground-truth regimes: **(a) deterministic** (descriptive/arithmetic over known history — there is one
correct answer) and **(b) backtested** (forecasting — ground truth is the actual observed value on a
held-out period).

## 4. Metrics (operationalised)

**Primary**
- **Correctness** — fraction of prompts whose answer is correct. For (a) deterministic prompts: numeric
  match to the true value within a defined tolerance, and no hallucinated entities/numbers. For (b)
  forecasting prompts: forecast error (e.g., MAPE) against the held-out actual, plus directional
  correctness for forecast-to-decision prompts. *Much of this is measurable programmatically against
  ground truth, reducing reliance on the LLM judge.*
- **Consistency** — run each prompt **K times** under identical settings and measure run-to-run agreement
  (exact-match rate for categorical answers; coefficient of variation for numeric answers). Hypothesis: the
  dedicated model (A) is deterministic and so more consistent; self-written code (B) varies run-to-run.
- **Replicability** — can the result be reproduced from the recorded spec/seed in a fresh
  session/environment? Measured by re-running end-to-end on a different machine/day and comparing outputs.

**Secondary**
- **Cost** — $ per prompt: API tokens (and any compute) summed per condition.
- **Latency** — wall-clock per prompt, including tool round-trips (A) or code-write/execute/retry loops (B).

Mapping to the CLEAR multidimensional frame (Mehta, 2025): cost, latency, efficacy ≈ correctness,
assurance/reliability ≈ consistency + replicability.

## 5. Judging protocol

- Numeric/deterministic correctness: checked **programmatically** against ground truth (primary).
- Qualitative dimensions (clarity, actionability of the recommendation), if retained: **LLM-as-judge** with
  a **separate judge model**, pairwise comparison where possible (more consistent per Gu et al., 2024),
  explicit **bias mitigation** (position/self-enhancement; Ye et al., 2024), plus a **human-rated subset**
  for validation. Log every judge prompt and output.

## 6. Validity / controls

- Same base LLM and decoding settings for A and B (isolate the integration factor, not model quality).
- Fixed prompt set and inputs; K repetitions for consistency; fixed seeds where applicable.
- Full logging of inputs, outputs, tool calls (A) / generated code + execution traces (B), tokens, timings.
- Pilot scale ≈ 50 prompts in the first instance; full study = larger prompt set and/or more repetitions
  (future work).

## 7. Feasibility / dependencies

- **Runs locally** (E2B sandbox); **no Prometheus access required** for SRQ4.
- Condition A depends on the **final dedicated forecasting models** (SRQ1 rebuild, Brian). Conditions B and
  the harness can be built and dry-run **before** the models are final.
- No live business outcomes; offline/backtest only.

## 8. OPEN DECISIONS (finalise before building)

1. Exact prompt set and per-archetype counts (start from §3; confirm/freeze the ~50).
2. **K** (repetitions per prompt for consistency) — e.g., 3 or 5.
3. Correctness tolerance for numeric answers (e.g., exact vs ±x%).
4. Base LLM(s) and decoding settings (temperature) used identically for A and B.
5. Judge model choice; which qualitative dimensions (if any) beyond the programmatic metrics.
6. Ground-truth source per archetype (confirm deterministic vs backtest split and the held-out period).
7. Include the optional floor condition C (plain LLM) or not.
8. Whether to keep any role for the old static-template baseline (recommend: drop).
