# SRQ4 — does model availability improve an LLM's forecasts?

2 brands x 3 repeats x 1 scenarios. Model `gpt-5.5-2026-04-23`, reasoning effort `medium`. Decoding: temperature/top_p unsupported by the model; defaults used. Forecasting the held-out test month from train+val.

The scenarios are an information ladder: **A -> B** measures what data access buys, **B -> C** measures what model integration adds on top.

| Metric | C — no firm data |
|---|---|
| Runs | 6 |
| Usable answers | 6 |
| **Correctness** — median APE (lower=better) | 56.4% |
| Correctness — mean APE | 93.7% |
| **Consistency** — mean CV across repeats | 16.2% |
| Replicability — % brands identical | 0% |
| Replicability — TAR@N, 1% tol (Atil et al., 2025) | 0.50 |
| Cost — mean tokens/answer | 83732 |
| Cost — mean reasoning tokens (billed as output) | 3816 |
| Cost — mean USD/answer (est.) | $0.5130 |
| Cost — total USD this run (est.) | $3.08 |
| Latency — mean seconds | 114.6 |

## Outcome taxonomy

Failures are reported as classes, not averaged away. An scenario that answers 60% of the time is not comparable to one that always answers, and a single implausible value destroys a mean (P0038 F72).

| Outcome | C — no firm data |
|---|---|
| ok | 6 |
| code_error | 0 |
| no_forecast | 0 |
| timeout | 0 |
| implausible | 0 |

## Cost reconciliation

Estimated from token counts: **$3.0782**.

Actually billed over the run window: **$13.7689**.

The estimate excludes the Code Interpreter container charge, which the API does not report per response — only the billing endpoint sees it. Report the billed figure.

| Line item | USD |
|---|---|
| gpt-5.5-2026-04-23, input | $7.586305 |
| gpt-5.5-2026-04-23, output | $5.081160 |
| web search tool calls | $1.060000 |
| gpt-5.5-2026-04-23, cached input | $0.032192 |
| gpt-5.6-sol, cache writes | $0.007769 |
| gpt-5.6-sol, output | $0.001200 |
| gpt-5.6-sol, input | $0.000245 |
| gpt-5.6-sol, cached input | $0.000000 |
