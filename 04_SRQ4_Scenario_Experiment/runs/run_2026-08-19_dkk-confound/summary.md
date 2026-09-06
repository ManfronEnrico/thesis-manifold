# SRQ4 — does model availability improve an LLM's forecasts?

2 brands x 3 repeats x 3 scenarios. Model `gpt-5.5-2026-04-23`, reasoning effort `medium`. Decoding: temperature/top_p unsupported by the model; defaults used. Forecasting the held-out test month from train+val.

The scenarios are an information ladder: **A -> B** measures what data access buys, **B -> C** measures what model integration adds on top.

| Metric | C — no firm data | B — code-as-action | A — dedicated model |
|---|---|---|---|
| Runs | 6 | 6 | 6 |
| Usable answers | 3 | 6 | 6 |
| **Correctness** — median APE (lower=better) | 569.6% | 13.5% | 7.7% |
| Correctness — mean APE | 506.8% | 14.5% | 7.7% |
| **Consistency** — mean CV across repeats | 24.1% | 2.9% | 0.0% |
| Replicability — % brands identical | 0% | 50% | 100% |
| Replicability — TAR@N, 1% tol (Atil et al., 2025) | 0.33 | 0.83 | 1.00 |
| Cost — mean tokens/answer | 46625 | 17691 | 707 |
| Cost — mean reasoning tokens (billed as output) | 2757 | 5634 | 20 |
| Cost — mean USD/answer (est.) | $0.3008 | $0.2664 | $0.0068 |
| Cost — total USD this run (est.) | $1.80 | $1.60 | $0.04 |
| Latency — mean seconds | 80.4 | 113.6 | 5.2 |

## Outcome taxonomy

Failures are reported as classes, not averaged away. An scenario that answers 60% of the time is not comparable to one that always answers, and a single implausible value destroys a mean (P0038 F72).

| Outcome | C — no firm data | B — code-as-action | A — dedicated model |
|---|---|---|---|
| ok | 3 | 6 | 6 |
| code_error | 0 | 0 | 0 |
| no_forecast | 0 | 0 | 0 |
| timeout | 0 | 0 | 0 |
| implausible | 3 | 0 | 0 |

## Cost reconciliation

Estimated from token counts: **$3.4437**.

Actually billed over the run window: **$9.4451**.

The estimate excludes the Code Interpreter container charge, which the API does not report per response — only the billing endpoint sees it. Report the billed figure.

| Line item | USD |
|---|---|
| gpt-5.5-2026-04-23, input | $5.033395 |
| gpt-5.5-2026-04-23, output | $3.498870 |
| web search tool calls | $0.880000 |
| gpt-5.5-2026-04-23, cached input | $0.023616 |
| gpt-5.6-sol, cache writes | $0.007769 |
| gpt-5.6-sol, output | $0.001200 |
| gpt-5.6-sol, input | $0.000245 |
| gpt-5.6-sol, cached input | $0.000000 |
