# SRQ2 synthesis engine — deterministic core (Ch7 §7.2)

Per-series ensemble forecast (inverse-WMAPE weighted), inter-model agreement, split-conformal 90% interval, composite confidence (30% agreement + 40% interval tightness + 30% model accuracy) and 3-tier label. LLM recommendation text + LLM-as-Judge (Ch7 §7.6 / Ch8 §8.3) need an LLM API and are not run here.

| Category | n_series | mean confidence | %High | %Moderate | %Low | interval coverage |
|---|---|---|---|---|---|---|
| CSD | 665 | 37.5 | 0% | 39% | 61% | 98.9% |
| danskvand | 174 | 33.3 | 0% | 18% | 82% | 91.4% |
| energidrikke | 308 | 35.1 | 0% | 29% | 71% | 97.1% |
| RTD | 372 | 31.7 | 0% | 22% | 78% | 100.0% |

Confidence-tier triage lets the agentic layer surface High-confidence forecasts directly and flag Low-confidence ones for human review (SRQ2 reliability/traceability).
