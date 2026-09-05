<!-- PROSE STRIPPED 2026-09-01 (P0044); ARGUMENT BULLETS REBUILT 2026-09-05 (P0045).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-05_19-52_complete-review-pass/chapters.
     This file is a PLANNING surface: claims, warrants, evidence pointers, open items.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 5 — Predictive-Extension Architecture

> **P0044 OPEN (2026-09-01): RAM figure needs reconciling.** This file states an
> 8 GB budget. That number is a project assumption, not a sourced one -- Ng (2017)
> argues memory is the binding design variable, not that SMEs get 8 GB. Manifold's
> production Prometheus E2B template is provisioned at a **measured 4096 MB**
> (`fxe7gzkqjupdhbx4uvpr`, verified live 2026-09-01). Prefer the measured figure.
> All results hold under the tighter bound (serving 36.8 MB, refit ~37 MB).
> See `plans/P0044_2026-09-01_17-10_resource-measurement-and-retrain-arms/findings.md` F22-F23.

> **P0045 UPDATE (2026-09-05): the .docx is now HALF-migrated to 4 GB.**
> The 19-52 snapshot says "approximately four gigabytes" in §5.1, §5.3 and §5.8's
> opening, but §5.8's closing sentence still reads "2.8% of the eight-gigabyte
> budget" and §5.10 still says "an eight-gigabyte budget". Two figures now appear
> in one chapter. Finish the migration in the .docx; 231 MB of 4 GB is **5.6%**,
> not 2.8%.

> Status: COMPLETE (2026-06-27) — RQs v4 (predictive-extension architecture; lightweight Python coordinator evaluated, LangGraph/Graph Engine as production target; code-as-action baseline; no Indeks/enrichment). Component memory figures are measured by RSS from the local pipeline (Table 5.1) and the Figure 5.1 architecture diagram is drawn (`figures/ch5_architecture_v1.png`). No placeholders remain. Awaiting human review only.
> Author: Claude Code — requires human review before finalisation

---

## 5.1 Design Objectives and Constraints

**Claims**
- The chapter presents the artefact as a *designed object* whose components are
  justified against RQs and the deployment constraint — not as an implementation report
- Four design objectives, one per SRQ: forecast at brand×retailer grain within a
  memory budget (SRQ1); expose forecasts through a structured interface preserving
  reliability/uncertainty/traceability (SRQ2); specify capabilities a production
  agentic system needs to integrate them (SRQ3); permit controlled comparison against
  a code-as-action baseline (SRQ4)
- Two constraints shape every choice: a hard ceiling of **~4 GB** total RAM across
  simultaneously active components, and **monthly batch** processing, not streaming
- The RAM ceiling is a *formal design criterion*, not a convenience — it reflects the
  realistic cloud budget of a small/medium AI agent provider

**Warrant**
- DSR framing carried from Ch3 (Hevner et al. 2004; Peffers et al. 2007) — design
  knowledge is drawn out in Ch9/Ch10, so the artefact must be argued, not just built
- Pragmatist stance: judge the architecture by whether it works within the constraints,
  not by architectural elegance

**Evidence**
- Status honesty: substrate implemented and benchmarked (Ch6); interface and agentic
  layer realised in the coordinator (Ch7); cost/latency at pilot scale only (Ch8)
- Where a figure depends on a layer still being hardened, say so rather than presenting
  it as settled

**Open**
- The 4 GB figure is measured (P0044 F22-F23) but the *rationale* for treating it as
  the SME budget is still the unsourced assumption. State it as "the production
  template we measured", not "the SME budget"

---

## 5.2 Architectural Overview

1. a **forecasting substrate**, a set of lightweight machine learning models that produce point forecasts and interval information (SRQ1; benchmarked in Chapter 6);
2. a **structured forecast-tool interface**, a JSON-based function-calling contract through which the substrate is exposed to the agentic layer as a callable tool (SRQ2);
3. a **bounded tool-using agentic decision-support layer**, an LLM orchestrator that invokes the substrate through the interface and synthesises a confidence-qualified recommendation, with human-in-the-loop checkpoints.

**Claims**
- The artefact is a **bounded tool-using AI agent** with human oversight — *not* a
  multi-agent Agentic AI system, in Sapkota et al.'s (2025) taxonomy
- The boundary is deliberate: it keeps the system auditable and inside the resource budget
- Multi-agent decomposition is production-target and future work, not a property of the
  evaluated artefact
- The **lightweight Python coordinator is the evaluated implementation**; the LangGraph /
  Prometheus Graph Engine deployment is the production target and the object of SRQ3

**Warrant**
- Claiming less than was built is the defensible move: an examiner can verify a bounded
  tool-using agent, and overclaiming "multi-agent" invites a challenge the artefact loses

**Evidence**
- Figure 5.1 `figures/ch5_architecture_v1.png`

![**Figure 5.1** — The predictive-extension architecture. A lightweight Python coordinator (≤ 4 GB RAM, one model resident at a time, the LLM kept out-of-process via remote API) wraps three layers: a forecasting substrate of five lightweight models (SRQ1), a structured JSON forecast-tool interface preserving reliability, uncertainty, and traceability (SRQ2), and a bounded tool-using agentic layer that produces a confidence-qualified, auditable recommendation (informing SRQ3). The dedicated-model path is compared against a code-as-action LLM baseline on correctness, consistency, replicability, cost, and latency (SRQ4).](../figures/ch5_architecture_v1.png){width=6.2in}

**Open**
- Figure caption says "five lightweight models"; the ladder narrowed to two tabular
  models for the headline comparison → [[srq1-model-ladder-and-baselines]]. Reconcile
- Caption still needs regenerating if the 4 GB migration changes the diagram label

---

## 5.3 The Forecasting Substrate (SRQ1)

**Claims**
- Substrate spans the accuracy–efficiency frontier: ARIMA, Prophet, LightGBM, XGBoost,
  Ridge — evaluated per-category and pooled (Ch6)
- Two design decisions follow from the RAM constraint:
  - models run **sequentially** (load → run → unload), one resident at a time
  - memory profiled by **RSS**, not tracemalloc alone
- The RAM budget binds the model-selection **space**, not the realised footprint —
  it excludes transformer and locally-hosted options *up front*
- Measured footprint sits two orders of magnitude below the ceiling

**Warrant**
- RSS over tracemalloc because tracemalloc misses the **native allocations** of XGBoost
  and LightGBM — this is a methodology point worth stating, not an implementation detail
- The model set is the standard benchmark set, not a convenience choice
  → [[srq1-model-ladder-and-baselines]]
- Inverse-MAPE aggregation follows Ahrens et al. (2024); run-to-run stability treated as
  production-relevant alongside accuracy (Klee & Xia 2025)

**Evidence**
- Per-model fit footprint, CSD, RSS over runtime baseline: XGBoost ~15 MB, LightGBM ~7 MB,
  Ridge < 1 MB
- tracemalloc cross-check (Python allocations only): Ridge 1.5 MB, LightGBM 18.7 MB,
  XGBoost 0.2 MB, ARIMA ~0.5 MB per series — confirms native buffers are the larger
  but still modest component
- Consolidated in Table 5.1 (§5.8)

**Open**
- Text claims gradient-boosted models use "promotional, distribution, and calendar"
  exogenous predictors. P0043 threads 15/16/17 dispute the enrichment framing: promo
  and calendar are real, **weather/macro/holiday-calendar are not**. Keep the narrow
  claim → [[sample-size-and-tool-interface-rationale]] §9
- Promo features are inactive for danskvand and RTD — state as structural asymmetry,
  not missing data → [[sample-size-and-tool-interface-rationale]] §8

---

## 5.4 The Structured Forecast-Tool Interface (SRQ2)

- **Reliability**, by validating the agent's stated numbers against the source forecast values before delivery, so that the agent reports the model's numbers rather than its own.
- **Uncertainty**, by attaching interval information to every forecast; interval calibration follows the post-hoc approach of Kuleshov et al. (2018) and is treated as a design target, not an empirically validated property of the current prototype.
- **Traceability**, by recording the mapping from tool call and forecast value to the resulting recommendation, so that each recommendation can be audited back to its source forecast.

**Claims**
- Realised as a **JSON function-calling contract with strict output schemas** — the
  agentic layer calls the substrate as a tool and receives point forecast + interval
- JSON function-calling is chosen over code-as-action *inside* the artefact for
  reliability and reproducibility: schema-constrained calls are deterministic and auditable
- Code-as-action (Wang et al. 2024) is not rejected — it is repositioned as the **SRQ4
  baseline** (§5.7)

**Warrant**
- The three properties are the answer to SRQ2, so each needs a mechanism, not an
  aspiration. Reliability = numeric validation before delivery; uncertainty = interval
  attached to every response; traceability = tool-call → value → recommendation mapping
- Interface mechanics and how the LLM actually reaches a forecast
  → [[sample-size-and-tool-interface-rationale]] §6

**Open**
- Uncertainty is explicitly a **design target, not a validated property**. Keep that
  hedge — P0043 thread 76 questions whether the uncertainty handling is real
- P0043 thread 214: "no human in loop atp" — the human-in-the-loop checkpoint is
  claimed in §5.2 and §5.5 but may not be implemented. Verify before it stays

---

## 5.5 The Bounded Tool-Using Agentic Layer

**Claims**
- The LLM is accessed by **remote API, never loaded locally** — this keeps it out of the
  RAM budget entirely; a local model would add several gigabytes (Semerikov et al. 2025)
- The layer embodies **delegation-over-generation**: the LLM does not predict demand or
  compute the forecast. It orchestrates, validates, and communicates
- Separating a generative orchestrator from deterministic predictive components is *the*
  architectural feature that makes agentic numerical decision-support both auditable and
  resource-feasible
- Decoding configured for reproducibility (temperature zero)

**Warrant**
- This is the chapter's strongest transferable design claim and feeds DP4 in Ch9 —
  it generalises past this dataset and past FMCG

**Evidence**
- Ch7 exercises the layer; Ch8 reports cost and latency at pilot scale

**Open**
- P0043 thread 216: the pinned model may not accept a temperature parameter at all.
  If so, "temperature zero" is a false reproducibility claim and must be restated as
  whatever determinism control actually applies
- P0043 thread 222: "locally" is misleading anywhere it appears — the API needs internet

---

## 5.6 Integration Readiness (SRQ3)

**Claims**
- Four capabilities a production agentic system must have to integrate forecast-informed
  decision-support:
  1. a **structured tool interface** for invoking external predictive models
  2. **observability and traceability** of tool calls and outputs
  3. explicit **handling of reliability and uncertainty**
  4. operation within **bounded cost, latency, and memory**
- Assessed against Prometheus (Graph Engine as the concrete integration point) as the
  empirical case
- This is a **capability-readiness analysis, not a live integration experiment** — it
  establishes which capabilities the production system already has and which the
  extension would add

**Warrant**
- Framing it as readiness rather than integration is what makes SRQ3 answerable without
  production deployment access. Say so explicitly; it converts a limitation into a
  scoping decision

**Open**
- P0043 thread 26 (Ch1) doubts observability/traceability was implemented well. P0044 F8
  resolves it: it **is** implemented (every SRQ4 run logs latency, tokens, cost, tool
  trace) but never **evaluated**. If SRQ3 promises it as a *measured* property, that is
  the real gap
- Prometheus scenario design and what D/E add → [[prometheus-scenarios-design-rationale]]

---

## 5.7 The Code-as-Action Baseline (SRQ4)

**Claims**
- Baseline = a general-purpose LLM that writes, executes and self-corrects its own
  forecasting code in a sandbox (E2B), given the **same data access and the same prompts**,
  with no dedicated pre-built model (Wang et al. 2024)
- It uses the **same base LLM** as the agentic layer, so the comparison isolates the
  effect of dedicated-model integration rather than model quality
- The baseline runs locally and needs no production access — this is what makes SRQ4
  feasible independently of integration access

**Warrant**
- Same-model control is the design decision that makes the comparison a *controlled*
  one; without it, SRQ4 measures nothing
- Three-arm information ladder A → B → C, so A→B measures what data access buys and
  B→C what the thesis artefact adds → [[srq4-experiment-design-rationale]] §1
- Sample design is brands × repeats, not one brand × many repeats
  → [[srq4-experiment-design-rationale]] §3
- Trial budget and validation protocol → [[srq1-tuning-and-validation-protocol]]

**Evidence**
- Protocol and metrics specified in Ch3, applied in Ch8. Primary: correctness,
  consistency, replicability. Secondary: cost, latency (Mehta 2025)
- Measured pilot costs → [[srq4-experiment-design-rationale]] §10;
  first results and the ~40× Scenario-B token cost → [[srq4-first-results-and-interpretation]]

**Open**
- P0043 thread 215: scenario naming — text refers to "Scenarios A, B, and D", but the
  locked vocabulary is A/B/C (see `.claude/rules/repo-tier-structure.md`). Reconcile
- P0043 thread 221: each scenario should be *named*, not just lettered
- **LLM-as-judge was dropped** → [[srq4-experiment-design-rationale]] §7. Any judge
  language surviving in this chapter is stale

---

## 5.8 Memory, Cost, and Latency Budget

**Claims**
- The ceiling is respected **by construction**, not by tuning: one model + data resident
  at a time, LLM by API, intermediates released after use
- Memory by RSS; cost (API tokens) and latency (wall-clock incl. tool round-trips) are
  the secondary SRQ4 dimensions
- End-to-end peak ~231 MB — **5.6% of 4 GB**

| Component | Peak RAM (RSS) | When |
|---|---|---|
| Python runtime and libraries (numpy, pandas, LightGBM, XGBoost, scikit-learn) | ~194 MB | Always |
| Coordinator state (typed state passed between components) | < 1 MB | Always |
| Nielsen data (per category, largest = CSD) | ~15 MB | Data loading |
| Active model (one at a time; XGBoost ≈15, LightGBM ≈7, Ridge < 1 MB) | ~15 MB | Forecasting |
| Agentic layer (remote API; no weights loaded, network buffer only) | negligible | Synthesis |
| **End-to-end peak** | **~231 MB** | Forecasting |

**Open**
- **The .docx says 2.8% here.** That is 231 MB / 8 GB. Against the measured 4 GB it is
  **5.6%**. Fix in the .docx — this is the arithmetic half of the half-finished migration
- Serving-only footprint is 36.8 MB and refit ~37 MB (P0044); those are tighter and more
  favourable figures than the 231 MB pipeline peak. Consider reporting both, and be
  explicit about which scenario each describes

---

## 5.9 Technology Choices and Justification

| Choice | Alternative not adopted | Reason |
|---|---|---|
| Lightweight Python coordinator (evaluated) | LangGraph deployment | LangGraph is the production target (Prometheus); the lightweight coordinator is leaner for the evaluated prototype under the RAM budget |
| JSON function-calling interface (artefact) | Code-as-action inside the artefact | Reliability and reproducibility; code-as-action is instead the SRQ4 baseline |
| LightGBM and XGBoost | LSTM, Temporal Fusion Transformer, Chronos | An order of magnitude lower RAM at competitive accuracy on tabular retail data under the period budget |
| LLM via remote API | Locally hosted LLM | Avoids several gigabytes of model weights, keeping the language model out of the RAM budget (Semerikov et al., 2025) |
| Sandbox (e.g. E2B) for the baseline | Bespoke execution harness | Open and local; runs the code-as-action baseline without production access |

**Warrant**
- Every row is argued against the RAM constraint, tying back to the Ch1 design criterion

**Open**
- Row 5 says the sandbox is "open and local". P0043 thread 115/116: E2B is **not local**
  — it is a hosted sandbox, and it is what Manifold actually uses. Rewrite the reason
- P0043 thread 213: the sandbox is instantiated per session — relevant to the RAM
  argument and currently unstated

---

## 5.10 Summary

**Claims**
- Three layers — substrate, structured interface, bounded agentic layer — coordinated by
  a lightweight Python coordinator, operating within a **4 GB** budget
- Deliberately a bounded tool-using agent, not a multi-agent system
- Delegates prediction to dedicated models rather than generating it
- Positioned for production integration through the structured interface

**Evidence**
- Forward pointers: substrate benchmarked Ch6 (SRQ1); interface and agentic layer
  exercised Ch7 (SRQ2, informing SRQ3); dedicated-model vs code-as-action Ch8 (SRQ4)

**Open**
- **The .docx summary still says "eight-gigabyte budget".** Second half of the
  half-finished migration (see the P0045 block at the top of this file)

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

---

## Writing-notes wired into this chapter (P0045)

- [[srq1-model-ladder-and-baselines]] — §5.3 model set justification, and why the
  comparison narrows to two tabular models
- [[srq1-tuning-and-validation-protocol]] — §5.7 trial budget, expanding-window CV
- [[sample-size-and-tool-interface-rationale]] — §5.3 feature reality, §5.4 SRQ2
  mechanics, §5.3 cross-category asymmetry
- [[srq4-experiment-design-rationale]] — §5.7 three-arm ladder, sample design, judge dropped
- [[prometheus-scenarios-design-rationale]] — §5.6 integration readiness
- [[srq4-first-results-and-interpretation]] — §5.7 measured cost asymmetry
