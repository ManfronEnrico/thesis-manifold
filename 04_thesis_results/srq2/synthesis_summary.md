# SRQ2 synthesis engine — deterministic core (Ch7 §7.2)

Per-series ensemble forecast (inverse-WMAPE weighted), inter-model agreement, split-conformal 90% interval, composite confidence (30% agreement + 40% interval tightness + 30% model accuracy) and 3-tier label. LLM recommendation text + LLM-as-Judge (Ch7 §7.6 / Ch8 §8.3) need an LLM API and are not run here.

| Category | n_series | mean confidence | %High | %Moderate | %Low | interval coverage |
|---|---|---|---|---|---|---|
| CSD | 845 | 44.9 | 0% | 72% | 28% | 96.6% |
| danskvand | 966 | 43.6 | 0% | 70% | 30% | 97.8% |
| energidrikke | 205 | 47.1 | 0% | 75% | 25% | 80.0% |
| RTD | 324 | 38.5 | 0% | 45% | 55% | 90.7% |

Confidence-tier triage lets the agentic layer surface High-confidence forecasts directly and flag Low-confidence ones for human review (SRQ2 reliability/traceability).
