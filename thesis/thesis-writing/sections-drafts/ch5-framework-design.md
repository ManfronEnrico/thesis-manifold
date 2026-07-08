# Chapter 5 — Predictive-Extension Architecture
> Status: COMPLETE (2026-06-27) — RQs v4 (predictive-extension architecture; lightweight Python coordinator evaluated, LangGraph/Graph Engine as production target; code-as-action baseline; no Indeks/enrichment). Component memory figures are measured by RSS from the local pipeline (Table 5.1) and the Figure 5.1 architecture diagram is drawn (`figures/ch5_architecture_v1.png`). No placeholders remain. Awaiting human review only.
> Author: Claude Code — requires human review before finalisation

---

## 5.1 Design Objectives and Constraints

This chapter specifies the architecture of the thesis artefact: a predictive extension that equips a production-oriented, non-predictive agentic decision-support system with forecast-informed capability. Following the Design Science Research framing of Chapter 3 (Hevner et al., 2004; Peffers et al., 2007), the architecture is presented as a designed artefact whose components are justified against the research questions and the deployment constraint, and from which transferable design knowledge is drawn in Chapters 9 and 10.

The architecture pursues four design objectives, each tied to a research question. First, it must produce reliable demand forecasts at brand-by-retailer granularity within a fixed memory budget (SRQ1). Second, it must expose those forecasts to an agentic layer through a structured tool and action interface that preserves reliability, uncertainty, and traceability (SRQ2). Third, it must specify the architectural and operational capabilities that a production-oriented agentic system requires in order to integrate forecast-informed decision-support (SRQ3). Fourth, it must permit a controlled comparison between the dedicated-model agentic approach and a general-purpose code-as-action baseline (SRQ4).

Two constraints shape every choice. The first is a hard ceiling of approximately eight gigabytes of total RAM across all simultaneously active components, treated as a formal design criterion rather than a convenience, reflecting the realistic cloud budget of a small or medium-sized AI provider. The second is the processing mode: monthly batch forecasting over historical data, not real-time streaming. Consistent with the pragmatist stance of Chapter 3, the architecture is judged by whether it works within these constraints, not by architectural elegance for its own sake.

A note on status: this is a design specification, but its lower layers are implemented and measured. The forecasting substrate is implemented and benchmarked across the five categories (Chapter 6), and its component memory figures are measured by RSS and reported in Table 5.1. The structured interface and the bounded agentic layer are realised in the lightweight Python coordinator (exercised in Chapter 7), while the cost and latency of the agentic and code-as-action paths are the secondary SRQ4 dimensions reported at pilot scale in Chapter 8. Where a figure depends on a layer still being hardened, this is stated explicitly rather than presented as a settled result.

---

## 5.2 Architectural Overview

The predictive extension is organised in three layers:

1. a **forecasting substrate**, a set of lightweight machine learning models that produce point forecasts and interval information (SRQ1; benchmarked in Chapter 6);
2. a **structured forecast-tool interface**, a JSON-based function-calling contract through which the substrate is exposed to the agentic layer as a callable tool (SRQ2);
3. a **bounded tool-using agentic decision-support layer**, an LLM orchestrator that invokes the substrate through the interface and synthesises a confidence-qualified recommendation, with human-in-the-loop checkpoints.

In the conceptual taxonomy of Sapkota et al. (2025), the artefact at its current stage is most accurately described as a **bounded tool-using AI agent** with human oversight, rather than a full multi-agent Agentic AI system. A multi-agent decomposition, in which specialist agents coordinate, is a production-target and future-work consideration, not a property of the evaluated artefact. This deliberate boundary keeps the system auditable and within the resource budget.

The layers are coordinated by a **lightweight Python coordinator** that passes typed state between components. This lightweight coordinator is the evaluated implementation. The production target, exemplified by Manifold AI's Prometheus platform, is a LangGraph-based deployment whose concrete integration point is the Prometheus Graph Engine; that production substrate is the object of the integration-readiness assessment (SRQ3, Section 5.6), not the evaluated implementation. The architecture is summarised in Figure 5.1.

![**Figure 5.1** — The predictive-extension architecture. A lightweight Python coordinator (≤ 8 GB RAM, one model resident at a time, the LLM kept out-of-process via remote API) wraps three layers: a forecasting substrate of five lightweight models (SRQ1), a structured JSON forecast-tool interface preserving reliability, uncertainty, and traceability (SRQ2), and a bounded tool-using agentic layer that produces a confidence-qualified, auditable recommendation (informing SRQ3). The dedicated-model path is compared against a code-as-action LLM baseline on correctness, consistency, replicability, cost, and latency (SRQ4).](../figures/ch5_architecture_v1.png){width=6.2in}

---

## 5.3 The Forecasting Substrate (SRQ1)

The substrate comprises lightweight models spanning the accuracy-efficiency frontier: ARIMA, Prophet, LightGBM, XGBoost, and Ridge Regression, evaluated across the five beverage categories and compared in their category-specialised and pooled variants (Chapter 6). The gradient-boosted models use the exogenous predictors described in Chapter 4, namely promotional, distribution, and calendar features, alongside autoregressive features; the two promotional features are inactive for the promo-zero categories.

Two design decisions follow from the RAM constraint. First, models are executed **sequentially** (load, run, unload) so that only one model occupies memory at a time, rather than concurrently. Second, memory is profiled by **process resident set size** (RSS, via the Python `psutil` and `resource` interfaces) rather than by `tracemalloc` alone, because `tracemalloc` does not capture the native allocations of XGBoost and LightGBM. The substrate exposes, for each forecast, a point estimate accompanied by interval information; where multiple models are combined, it aggregates them using inverse-MAPE weighting in the spirit of Ahrens et al. (2024). Stability across repeated runs is treated as a production-relevant property alongside accuracy (Klee and Xia, 2025).

Measured locally on the largest category (CSD), the per-model fit footprint is small in RSS terms: XGBoost adds about 15 MB, LightGBM about 7 MB, and Ridge under 1 MB over the runtime baseline (sequential, one model resident at a time). For reference, a `tracemalloc` run capturing Python-level allocations alone reports even smaller per-fit peaks (Ridge 1.5 MB, LightGBM 18.7 MB, XGBoost 0.2 MB; ARIMA fitted per series at ~0.5 MB), confirming that native library buffers are the larger but still modest component. Either way the substrate operates two orders of magnitude below the eight-gigabyte ceiling; the binding effect of the RAM budget is on the model-selection *space* (it excludes transformer and locally hosted options up front), not on the footprint of the selected models. Component figures are consolidated in Table 5.1.

---

## 5.4 The Structured Forecast-Tool Interface (SRQ2)

The interface is the mechanism by which a forecast is exposed to the agentic layer, and is the locus of SRQ2. It is realised as a **JSON-based function-calling contract with strict output schemas**: the agentic layer invokes the substrate as a tool and receives a structured response containing the point forecast and its interval. The interface is designed to preserve three properties:

- **Reliability**, by validating the agent's stated numbers against the source forecast values before delivery, so that the agent reports the model's numbers rather than its own.
- **Uncertainty**, by attaching interval information to every forecast; interval calibration follows the post-hoc approach of Kuleshov et al. (2018) and is treated as a design target, not an empirically validated property of the current prototype.
- **Traceability**, by recording the mapping from tool call and forecast value to the resulting recommendation, so that each recommendation can be audited back to its source forecast.

The artefact deliberately adopts JSON function-calling, rather than code-as-action, for **reliability and reproducibility**: the schema-constrained interface yields deterministic, auditable tool calls. The code-as-action pattern (Wang et al., 2024) is not used inside the artefact; it is instead the baseline against which the artefact is compared (Section 5.7).

---

## 5.5 The Bounded Tool-Using Agentic Layer

The agentic layer is an LLM orchestrator accessed through a remote API rather than loaded locally, a decision that keeps the language model out of the RAM budget entirely (a locally hosted model would add several gigabytes; Semerikov et al., 2025). Given a decision-support prompt, the layer invokes the forecasting substrate through the structured interface, optionally combines multiple model outputs, and produces a concise, confidence-qualified natural-language recommendation, subject to human-in-the-loop checkpoints.

The layer embodies a **delegation-over-generation** principle: the LLM does not itself predict demand or compute the forecast, but delegates numerical prediction to the dedicated models and confines itself to orchestration, validation, and communication. Decoding is configured for reproducibility (temperature zero). This separation of a generative orchestrator from deterministic predictive components is the architectural feature that makes the agentic numerical decision-support both auditable and resource-feasible.

---

## 5.6 Integration Readiness (SRQ3)

SRQ3 concerns the capabilities a production-oriented agentic system must possess to integrate forecast-informed decision-support. The architecture identifies four such capabilities: a **structured tool interface** for invoking external predictive models; **observability and traceability** of tool calls and their outputs; explicit **handling of reliability and uncertainty**; and operation within **bounded cost, latency, and memory**.

These capabilities are assessed against a real production-oriented agentic system, Prometheus, whose Graph Engine is the concrete integration interface, as the empirical case. The assessment is a capability-readiness analysis rather than a live integration experiment: it establishes which of the required capabilities the production system already possesses and which the predictive extension would add, without depending on a completed production deployment.

---

## 5.7 The Code-as-Action Baseline (SRQ4)

To evaluate whether dedicated-model integration is warranted at all, the architecture includes a **code-as-action baseline**: a general-purpose LLM that, given the same data access and the same prompts, writes, executes, and self-corrects its own forecasting and analysis code in a sandboxed environment (for example, E2B), without a dedicated pre-built model (Wang et al., 2024). The baseline uses the **same base LLM** as the agentic layer, so that the comparison isolates the effect of dedicated-model integration rather than differences in model quality.

The baseline is runnable locally and does not require access to the production system, which makes the SRQ4 comparison feasible independently of integration access. The comparison protocol and metrics (correctness, consistency, and replicability as primary dimensions; cost and latency as secondary; following the multidimensional frame of Mehta, 2025) are specified in Chapter 3 and applied in Chapter 8.

---

## 5.8 Memory, Cost, and Latency Budget

The eight-gigabyte ceiling is respected by construction: data and one model are held in memory at a time, the language model is accessed by API rather than loaded, and intermediate artefacts are released after use. Memory is reported by RSS; cost (API tokens) and latency (wall-clock, including tool round-trips) are tracked as the secondary SRQ4 dimensions. The per-component budget, measured by RSS on the local pipeline over the largest category (CSD), is summarised in Table 5.1.

| Component | Peak RAM (RSS) | When |
|---|---|---|
| Python runtime and libraries (numpy, pandas, LightGBM, XGBoost, scikit-learn) | ~194 MB | Always |
| Coordinator state (typed state passed between components) | < 1 MB | Always |
| Nielsen data (per category, largest = CSD) | ~15 MB | Data loading |
| Active model (one at a time; XGBoost ≈15, LightGBM ≈7, Ridge < 1 MB) | ~15 MB | Forecasting |
| Agentic layer (remote API; no weights loaded, network buffer only) | negligible | Synthesis |
| **End-to-end peak** | **~231 MB** | Forecasting |

*Table 5.1. Per-component budget, measured by RSS (psutil) on the local pipeline, 2026-06-27.* The end-to-end peak of approximately 231 MB is about 2.8% of the eight-gigabyte budget. The budget therefore binds the model-selection space (excluding transformer and locally hosted LLM options up front) rather than the final footprint; the realised footprint sits two orders of magnitude below the ceiling because the language model is kept out of process by the remote-API design and only one lightweight model is resident at a time.

---

## 5.9 Technology Choices and Justification

| Choice | Alternative not adopted | Reason |
|---|---|---|
| Lightweight Python coordinator (evaluated) | LangGraph deployment | LangGraph is the production target (Prometheus); the lightweight coordinator is leaner for the evaluated prototype under the RAM budget |
| JSON function-calling interface (artefact) | Code-as-action inside the artefact | Reliability and reproducibility; code-as-action is instead the SRQ4 baseline |
| LightGBM and XGBoost | LSTM, Temporal Fusion Transformer, Chronos | An order of magnitude lower RAM at competitive accuracy on tabular retail data under the period budget |
| LLM via remote API | Locally hosted LLM | Avoids several gigabytes of model weights, keeping the language model out of the RAM budget (Semerikov et al., 2025) |
| Sandbox (e.g. E2B) for the baseline | Bespoke execution harness | Open and local; runs the code-as-action baseline without production access |

Each choice is argued against the eight-gigabyte constraint, in keeping with the design criterion of Chapter 1.

---

## 5.10 Summary

The architecture instantiates the predictive extension as three layers, a forecasting substrate, a structured forecast-tool interface, and a bounded tool-using agentic layer, coordinated by a lightweight Python coordinator and designed to operate within an eight-gigabyte budget. It is deliberately a bounded tool-using agent rather than a multi-agent system, delegates prediction to dedicated models rather than generating it, and is positioned for integration into a production-oriented agentic system through a structured interface. The forecasting substrate is benchmarked in Chapter 6 (SRQ1), the interface and agentic layer are realised and exercised in Chapter 7 (SRQ2, informing SRQ3), and the dedicated-model approach is compared against the code-as-action baseline in Chapter 8 (SRQ4).

---

## References cited in this chapter

- Ahrens, A., Hansen, C. B., Schaffer, M. E., & Wiemann, T. (2024). Model averaging and double machine learning. *Journal of Applied Econometrics*. https://doi.org/10.48550/arXiv.2401.01645
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly*, *28*(1), 75–105.
- Klee, S., & Xia, Y. (2025). Measuring time series forecast stability for demand planning. *KDD '25 Workshop on AI for Supply Chain*.
- Kuleshov, V., Fenner, N., & Ermon, S. (2018). Accurate uncertainties for deep learning using calibrated regression. In *Proceedings of ICML 2018* (PMLR, Vol. 80).
- Mehta, S. (2025). Beyond accuracy: A multi-dimensional framework for evaluating enterprise agentic AI systems. *arXiv preprint arXiv:2511.14136*. [PREPRINT, not peer-reviewed]
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems*, *24*(3), 45–77.
- Sapkota, R., Roumeliotis, K. I., & Karkee, M. (2025). AI agents vs. agentic AI: A conceptual taxonomy, applications and challenges. *Information Fusion*, *126*, Article 103599. https://doi.org/10.1016/j.inffus.2025.103599
- Semerikov, S. O., Vakaliuk, T. A., Kanevska, O. B., Ostroushko, O. A., & Kolhatin, A. O. (2025). Edge intelligence unleashed: A survey on deploying large language models in resource-constrained environments. *Journal of Edge Computing*, *4*(2). https://doi.org/10.55056/jec.1000
- Wang, X., Chen, Y., Yuan, L., Zhang, Y., Li, Y., Ji, H., & Tong, H. (2024). Executable code actions elicit better LLM agents. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR).
