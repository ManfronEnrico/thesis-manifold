# SRQ4 — does model availability improve an LLM's forecasts?

1 brands x 1 repeats x 7 scenarios. Model `gpt-5.5-2026-04-23`, reasoning effort `medium`. Decoding: temperature/top_p unsupported by the model; defaults used. Forecasting the held-out test month from train+val.

The scenarios are an information ladder, weakest first. On the hosted model: **A -> B** measures what data access buys, **B -> C** what the dedicated model adds, **C -> F** what returning code on top of the model does. **D -> E -> G** repeats those three rungs on the Prometheus orchestrator, so the two ladders compare rung for rung.

| Metric | A_llm_plain | B_llm_data | C_llm_model | D_prometheus_data | E_prometheus_model | F_llm_data_model | G_prometheus_data_model |
|---|---|---|---|---|---|---|---|
| Runs | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Usable answers | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| **Correctness** — median APE (lower=better) | 23.0% | 5.2% | 21.9% | 0.2% | 21.9% | 2.6% | 12.0% |
| Correctness — mean APE | 23.0% | 5.2% | 21.9% | 0.2% | 21.9% | 2.6% | 12.0% |
| **Consistency** — mean CV across repeats | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Replicability — % brands identical | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| Replicability — TAR@N, 1% tol (Atil et al., 2025) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Cost — mean tokens/answer | 82822 | 15616 | 1163 | 62593 | 30938 | 14810 | 43964 |
| Cost — mean reasoning tokens (billed as output) | 4975 | 4530 | 0 | 0 | 0 | 4608 | 0 |
| Cost — mean USD/answer (est.) | $0.5432 | $0.2243 | $0.0090 | $0.5190 | $0.2021 | $0.2230 | $0.3269 |
| Cost — total USD this run (est.) | $0.54 | $0.22 | $0.01 | $0.52 | $0.20 | $0.22 | $0.33 |
| Latency — mean seconds | 119.5 | 91.3 | 6.7 | 113.6 | 41.6 | 75.3 | 80.9 |

## Outcome taxonomy

Failures are reported as classes, not averaged away. An scenario that answers 60% of the time is not comparable to one that always answers, and a single implausible value destroys a mean.

| Outcome | A_llm_plain | B_llm_data | C_llm_model | D_prometheus_data | E_prometheus_model | F_llm_data_model | G_prometheus_data_model |
|---|---|---|---|---|---|---|---|
| ok | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| code_error | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| no_forecast | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| timeout | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| implausible | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| engine_unavailable | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| warehouse_access | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| no_evidence | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| no_code | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Cost reconciliation

Estimated from token counts: **$2.0475**.

Actually billed over the run window: **$4.0288**.

> NOTE: this file was REGENERATED on 2026-09-11 to relabel the arms after the rename. The billing figure above was re-queried at regeneration time and covers a WIDER window than the run itself. The seven-arm smoke billed **$3.62**; that is the figure to cite. Every per-run measurement in the tables above is unchanged.

The estimate excludes the Code Interpreter container charge, which the API does not report per response — only the billing endpoint sees it. Report the billed figure.

| Line item | USD |
|---|---|
| gpt-5.5-2026-04-23, output | $1.996170 |
| gpt-5.5-2026-04-23, input | $1.742110 |
| web search tool calls | $0.200000 |
| gpt-5.5-2026-04-23, cached input | $0.090560 |
