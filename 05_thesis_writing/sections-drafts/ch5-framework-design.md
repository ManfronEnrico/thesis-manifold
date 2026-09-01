<!-- PROSE STRIPPED 2026-09-01 (P0044).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-01_18-50/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 5 — Predictive-Extension Architecture
> Status: COMPLETE (2026-06-27) — RQs v4 (predictive-extension architecture; lightweight Python coordinator evaluated, LangGraph/Graph Engine as production target; code-as-action baseline; no Indeks/enrichment). Component memory figures are measured by RSS from the local pipeline (Table 5.1) and the Figure 5.1 architecture diagram is drawn (`figures/ch5_architecture_v1.png`). No placeholders remain. Awaiting human review only.
> Author: Claude Code — requires human review before finalisation

---

## 5.1 Design Objectives and Constraints

---

## 5.2 Architectural Overview

1. a **forecasting substrate**, a set of lightweight machine learning models that produce point forecasts and interval information (SRQ1; benchmarked in Chapter 6);
2. a **structured forecast-tool interface**, a JSON-based function-calling contract through which the substrate is exposed to the agentic layer as a callable tool (SRQ2);
3. a **bounded tool-using agentic decision-support layer**, an LLM orchestrator that invokes the substrate through the interface and synthesises a confidence-qualified recommendation, with human-in-the-loop checkpoints.

![**Figure 5.1** — The predictive-extension architecture. A lightweight Python coordinator (≤ 8 GB RAM, one model resident at a time, the LLM kept out-of-process via remote API) wraps three layers: a forecasting substrate of five lightweight models (SRQ1), a structured JSON forecast-tool interface preserving reliability, uncertainty, and traceability (SRQ2), and a bounded tool-using agentic layer that produces a confidence-qualified, auditable recommendation (informing SRQ3). The dedicated-model path is compared against a code-as-action LLM baseline on correctness, consistency, replicability, cost, and latency (SRQ4).](../figures/ch5_architecture_v1.png){width=6.2in}

---

## 5.3 The Forecasting Substrate (SRQ1)

---

## 5.4 The Structured Forecast-Tool Interface (SRQ2)

- **Reliability**, by validating the agent's stated numbers against the source forecast values before delivery, so that the agent reports the model's numbers rather than its own.
- **Uncertainty**, by attaching interval information to every forecast; interval calibration follows the post-hoc approach of Kuleshov et al. (2018) and is treated as a design target, not an empirically validated property of the current prototype.
- **Traceability**, by recording the mapping from tool call and forecast value to the resulting recommendation, so that each recommendation can be audited back to its source forecast.

---

## 5.5 The Bounded Tool-Using Agentic Layer

---

## 5.6 Integration Readiness (SRQ3)

---

## 5.7 The Code-as-Action Baseline (SRQ4)

---

## 5.8 Memory, Cost, and Latency Budget

| Component | Peak RAM (RSS) | When |
|---|---|---|
| Python runtime and libraries (numpy, pandas, LightGBM, XGBoost, scikit-learn) | ~194 MB | Always |
| Coordinator state (typed state passed between components) | < 1 MB | Always |
| Nielsen data (per category, largest = CSD) | ~15 MB | Data loading |
| Active model (one at a time; XGBoost ≈15, LightGBM ≈7, Ridge < 1 MB) | ~15 MB | Forecasting |
| Agentic layer (remote API; no weights loaded, network buffer only) | negligible | Synthesis |
| **End-to-end peak** | **~231 MB** | Forecasting |

---

## 5.9 Technology Choices and Justification

| Choice | Alternative not adopted | Reason |
|---|---|---|
| Lightweight Python coordinator (evaluated) | LangGraph deployment | LangGraph is the production target (Prometheus); the lightweight coordinator is leaner for the evaluated prototype under the RAM budget |
| JSON function-calling interface (artefact) | Code-as-action inside the artefact | Reliability and reproducibility; code-as-action is instead the SRQ4 baseline |
| LightGBM and XGBoost | LSTM, Temporal Fusion Transformer, Chronos | An order of magnitude lower RAM at competitive accuracy on tabular retail data under the period budget |
| LLM via remote API | Locally hosted LLM | Avoids several gigabytes of model weights, keeping the language model out of the RAM budget (Semerikov et al., 2025) |
| Sandbox (e.g. E2B) for the baseline | Bespoke execution harness | Open and local; runs the code-as-action baseline without production access |

---

## 5.10 Summary

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
