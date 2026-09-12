# SRQ4 — does model availability improve an LLM's forecasts?

3 brands x 3 repeats x 7 scenarios. Model `gpt-5.5-2026-04-23`, reasoning effort `medium`. Decoding: temperature/top_p unsupported by the model; defaults used. Forecasting the held-out test month from train+val.

The scenarios are an information ladder, weakest first. On the hosted model: **A -> B** measures what data access buys, **B -> C** what the dedicated model adds, **C -> F** what returning code on top of the model does. **D -> E -> G** repeats those three rungs on the Prometheus orchestrator, so the two ladders compare rung for rung.

| Metric | A_llm_plain | B_llm_data | C_llm_model | D_prometheus_data | E_prometheus_model | F_llm_data_model | G_prometheus_data_model |
|---|---|---|---|---|---|---|---|
| Runs | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Usable answers | 6 | 9 | 9 | 9 | 9 | 9 | 9 |
| **Correctness** — median APE (lower=better) | 502.2% | 2.9% | 14.6% | 0.9% | 14.6% | 7.3% | 1.8% |
| Correctness — mean APE | 662.1% | 27.9% | 13.1% | 25.0% | 13.1% | 18.3% | 15.6% |
| **Consistency** — mean CV across repeats | 26.7% | 4.1% | 0.0% | 8.1% | 0.0% | 1.7% | 3.3% |
| Replicability — % brands identical | 0% | 0% | 100% | 0% | 100% | 33% | 33% |
| Replicability — TAR@N, 1% tol (Atil et al., 2025) | 0.33 | 0.44 | 1.00 | 0.56 | 1.00 | 0.67 | 0.78 |
| Cost — mean tokens/answer | 60566 | 39420 | 1165 | 109228 | 30168 | 38437 | 81827 |
| Cost — mean reasoning tokens (billed as output) | 3391 | 10740 | 10 | 0 | 0 | 10165 | 0 |
| Cost — mean USD/answer (est.) | $0.3798 | $0.4667 | $0.0091 | $0.7664 | $0.1994 | $0.4253 | $0.5536 |
| Cost — total USD this run (est.) | $3.42 | $4.20 | $0.08 | $6.90 | $1.79 | $3.83 | $4.98 |
| Latency — mean seconds | 69.5 | 123.8 | 6.0 | 111.3 | 31.7 | 103.9 | 84.4 |

## Outcome taxonomy

Failures are reported as classes, not averaged away. An scenario that answers 60% of the time is not comparable to one that always answers, and a single implausible value destroys a mean.

| Outcome | A_llm_plain | B_llm_data | C_llm_model | D_prometheus_data | E_prometheus_model | F_llm_data_model | G_prometheus_data_model |
|---|---|---|---|---|---|---|---|
| ok | 6 | 9 | 9 | 9 | 9 | 9 | 9 |
| code_error | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| no_forecast | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| timeout | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| implausible | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| engine_unavailable | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| warehouse_access | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| no_evidence | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| no_code | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Cost reconciliation

Estimated from token counts: **$25.2024**.

Actually billed over the run window: **$18.4647**.

The estimate excludes the Code Interpreter container charge, which the API does not report per response — only the billing endpoint sees it. Report the billed figure.

| Line item | USD |
|---|---|
| gpt-5.5-2026-04-23, output | $10.982130 |
| gpt-5.5-2026-04-23, input | $6.077065 |
| gpt-5.5-2026-04-23, cached input | $0.755328 |
| web search tool calls | $0.650000 |
| gpt-4.1-nano-2025-04-14, output | $0.000100 |
| gpt-4.1-nano-2025-04-14, input | $0.000087 |
| gpt-4.1-nano-2025-04-14, cached input | $0.000000 |
