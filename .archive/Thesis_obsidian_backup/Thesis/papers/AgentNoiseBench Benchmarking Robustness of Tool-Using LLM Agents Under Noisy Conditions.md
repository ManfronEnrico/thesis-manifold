
title: "AgentNoiseBench: Benchmarking Robustness of Tool-Using LLM Agents Under Noisy Conditions"
authors: (multiple authors, affiliations: Meituan; National University of Singapore; USTC)
year: 2026
venue: arXiv preprint (arXiv:2602.11348v2)
doi:
apa7: >
  (Authors unknown). (2026). AgentNoiseBench: Benchmarking robustness of tool-using LLM agents
  under noisy conditions. *arXiv preprint arXiv:2602.11348*.
read_date: 2026-03-21
read_depth: full

## In one sentence

Current LLM agent benchmarks systematically overestimate real-world performance because they ignore the user-noise and tool-noise that agents routinely encounter in deployment, causing an average accuracy drop of 20.8% under realistic conditions.

## Method

Taxonomy of real-world noise into two types (user-noise: ambiguous/variable user inputs; tool-noise: failed, incomplete, or inconsistent tool outputs). Automated injection pipeline applied to τ²-Bench, VitaBench, and HotPotQA. Evaluated a broad set of open-source and proprietary models with trajectory-aware multi-dimensional protocol.

## Key findings — cite these

- All evaluated models degrade under noise; average accuracy drop of **20.8%**
- Models are **more sensitive to tool-noise than user-noise** across all model families
- General reasoning ability and noise robustness are **not strongly correlated** — strong benchmark performance does not predict real-world robustness
- Different noise sources affect agent trajectory entropy through distinct mechanisms

## Direct quotes — copy verbatim, include page/section

> "Most existing benchmarks evaluate agents under idealized assumptions, where instructions are carefully curated, and interactions with the environment are stable and well-controlled." (Section 1)

> "Real-world environments are inherently stochastic and imperfect. User interactions exhibit substantial diversity and unpredictability, while external tools frequently return noisy, incomplete, or failed outputs." (Section 1)

> "General reasoning ability and environmental robustness are not strongly correlated." (Section 7 / Figure 1 discussion)

## Where this goes in my thesis

- **Ch.2, Section 2.X (Multi-agent systems / LLM agents)**: Cite as empirical evidence that agent benchmarks systematically overestimate deployment performance — motivates why our validation framework must go beyond standard accuracy metrics
- **Ch.5 (Framework Design)**: Justifies designing the Validation Agent to test robustness under imperfect tool outputs and noisy data signals, not just clean benchmark conditions
- **Ch.8 (Evaluation / SRQ3–SRQ4)**: Supports the argument that comparing our system to a descriptive baseline requires robustness-aware evaluation, not just point-accuracy metrics
- **Ch.9 (Limitations / Related Work)**: Acknowledge that our evaluation may not fully capture real-world noise conditions; cite AgentNoiseBench as the standard for future robustness testing

## What this paper does NOT cover (gap it leaves)

AgentNoiseBench evaluates general-purpose tool-use agents on standard NLP benchmarks — it does not address robustness in domain-specific multi-agent pipelines operating on structured business data (e.g. retail scanner data + consumer surveys), where tool-noise manifests as missing sales periods, schema mismatches, or stale forecasts rather than generic API failures.

## My critical assessment

- Provides a **crucial reality check** by demonstrating that standard LLM agent benchmarks significantly overestimate real-world performance due to the absence of noise
- Empirically shows that **robustness is a first-class property**, with performance dropping by ~20.8% under realistic conditions
- Introduces a key insight that **reasoning ability does not imply robustness**, exposing a major flaw in current evaluation practices
- Strongly motivates the need for **robustness-aware validation**, directly supporting the thesis’s Validation Agent and evaluation design
- However, the benchmark is limited to **general NLP tasks** and does not capture domain-specific pipelines based on structured numerical data
- The definition of tool-noise (API failures, inconsistencies) does not fully translate to **data-centric noise** relevant to the thesis (e.g., missing time-series data, schema mismatches, forecast drift)
- Focuses on evaluation rather than providing **design or mitigation strategies** for building robust systems
- Therefore, highly valuable for **highlighting the gap between benchmark and real-world performance and justifying robustness evaluation**, but limited in guiding the implementation of robustness in domain-specific, multi-agent forecasting systems