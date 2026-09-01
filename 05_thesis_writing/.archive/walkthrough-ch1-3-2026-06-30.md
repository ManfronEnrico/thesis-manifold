---
title: "Paragraph-by-Paragraph Walkthrough — Chapters 1–3"
subtitle: "What each paragraph says · Introduction, Literature Review, Methodology"
author: "Enrico Manfron"
---

# Wrap-up: the arc of the three chapters

The first three chapters set up the thesis end to end, before any results:

- **Chapter 1 (Introduction)** states the problem and the questions. It argues for the shift from descriptive BI to forecast-informed decision-support, shows why FMCG beverages under an 8 GB budget are a hard and realistic case, introduces Manifold AI as the live case, and decomposes the Main RQ into four sub-questions (SRQ1–4).
- **Chapter 2 (Literature Review)** builds the gap. As a narrative, integrative review it walks through eight literatures (forecasting, lightweight ML, decision-support, LLM agents, reliability/evaluation, production agentic systems), then shows their intersection is unaddressed (gap G6) and frames the answer as Design Science Research.
- **Chapter 3 (Methodology)** operationalises everything: a pragmatist + DSR stance, a quasi-experiment plus single-case study, one data source (Nielsen), a distinct evaluation protocol per SRQ, and explicit validity and limitations.

The thread is continuous: Ch1 poses the problem → Ch2 proves it is an open gap → Ch3 specifies how it will be answered.

---

# Chapter 1 — Introduction

## §1.1 Background and Motivation

- **¶1 — From descriptive to forecast-informed.** For decades BI has been descriptive (dashboards, KPIs, trends on past data); it created value, but modern markets need to know what will happen and what to do, not only what happened.
- **¶2 — Why FMCG beverages.** The shift matters most in FMCG, where volatility, promotions, seasonality and SKU proliferation challenge classical statistics; beverage demand is erratic and intermittent, and Ma et al. (2025) show ML with exogenous features beats statistical baselines on high-volume stable SKUs, with no single model dominating.
- **¶3 — The forecasting literature confirms the direction.** M4 (combining models wins; hybrids most accurate) and M5 (LightGBM dominates Walmart retail; exogenous features help) point the same way; Makridakis names exogenous variables as the open frontier (with a footnote defining the exogenous predictors used here). The thesis takes up that direction and goes beyond accuracy alone.
- **¶4 — The ignored constraint.** The academic literature has neglected compute limits; transformers and local LLMs need costly GPUs while an 8 GB instance costs a fraction; Ng (2017) shows memory is a first-order variable in scanner-data work, so ~8 GB is a realistic SME ceiling that excludes most transformer architectures.
- **¶5 — The gap in the agentic literature.** Agentic work assumes cloud-scale infrastructure; this is a structural asymmetry (benchmarks validated on big-lab hardware). Demonstrating reliable decision-support within an SME budget is itself a contribution; existing systems (AutoFlow, ScoreFlow, SciAgent, and the closest, González-Potes 2026) do not address the targeted combination.
- **¶6 — The Danish empirical context.** Denmark is a mature, concentrated retail market; Nielsen scanner-panel data give granular, longitudinal sales visibility, and the Nielsen panel is the thesis's central forecasting input.

## §1.2 Research Problem

- **¶1 — The four problems of the predictive extension.** With Manifold AI ("AI Colleagues" / Prometheus) as the descriptive-only production case, extending it raises four problems: (1) accuracy within a tight compute budget; (2) a typed interface preserving reliability, uncertainty, traceability; (3) the production system's capability to integrate the substrate; (4) beating a code-as-action LLM baseline at justified cost.
- **¶2 — The thesis's response.** It extends a production agentic system with a lightweight forecasting substrate, exposed via a typed forecast-tool interface to a bounded agentic layer, specifying the integration-readiness capabilities required, all within ~8 GB RAM.

## §1.3 Research Questions

- **Intro + Main RQ.** States the guiding question (extend non-predictive agentic systems with lightweight forecasting for reliable, forecast-informed, cost-justified decisions under constraints), decomposed into four SRQs.
- **SRQ1.** Which lightweight models best trade accuracy / memory / category specialisation; motivates the Ch6 benchmark; accuracy alone is insufficient under a fixed RAM budget.
- **SRQ2.** How to expose forecasts via a structured interface preserving reliability, uncertainty, traceability; motivates the interface (Ch5) and its realisation (Ch7); JSON function-calling prototype, LangGraph as production target.
- **SRQ3.** What capabilities a production system needs to integrate forecast support; motivates an integration-readiness spec assessed on the real Prometheus, not a completed deployment.
- **SRQ4.** Whether dedicated-model integration improves correctness/consistency/replicability at justified cost/latency vs a code-as-action LLM; motivates the Ch8 pilot comparison with an LLM-as-judge and human-rated subset.
- **Figure 1.1.** The RQ tree: Main RQ and its four sub-questions.

## §1.4 Delimitation

- **¶ intro.** Scope is bounded by deliberate choices for tractability and methodological traceability.
- **Domain and geography.** Danish beverage retail, the Nielsen categories; multi-category scope driven by data and benchmark design; categories chosen with Manifold, differing in scale, to test generalisation across heterogeneous structures.
- **Computational constraint.** ≤ 8 GB RAM across active components; explicitly excludes transformer architectures; a formal design criterion motivated by Ng (2017).
- **Processing mode.** Monthly batch over historical data, not real-time streaming; reflects the tactical planning horizon.
- **Deployment scope.** Not a production-ready system; a research prototype evaluated under DSR on historical data, measured on research metrics rather than live business outcomes.
- **Generalisability.** Bounded to the Danish market and the Nielsen panel; other markets/categories/sources are future work.

## §1.5 Thesis Structure

- **¶ intro.** The thesis is organised into nine further chapters, each a phase of the DSR process.
- **Per-chapter map.** One line each: Ch2 literature/gap; Ch3 methodology; Ch4 data assessment; Ch5 architecture vs the 8 GB budget; Ch6 SRQ1 benchmark; Ch7 SRQ2 agentic prototype; Ch8 SRQ4 pilot; Ch9 discussion/limitations; Ch10 conclusion.

---

# Chapter 2 — Literature Review

## §2.0 Chapter Introduction

- **¶1 — Frames the central problem** and says the review is organised so each literature supplies one element, then shows the elements are jointly under-addressed.
- **¶2 — Origin and iteration.** The idea began with Manifold AI; as the RQs were refined (from a multi-agent framing toward forecast-informed, cost-justified support), the reviewed scope was refined in step.
- **¶3 — Method.** A narrative, integrative (not systematic) review; Google Scholar + NotebookLM + Zotero; ~100 records screened → ~40 read closely → 39 cited (15 flagged preprints).
- **¶4 — Roadmap** of the eight thematic sections.
- **¶5 — Discipline.** A distinction is kept throughout between what the literature establishes and what the thesis designs, plans, or leaves to future work.

## §2.1 Forecasting as Predictive Substrate in FMCG *(SRQ1)*

- **¶1 — The substrate is a demand model;** the five chosen models (ARIMA, Prophet, LightGBM, XGBoost, Ridge) span the accuracy–efficiency frontier.
- **¶2 — Competitions.** M4 (combining models, hybrids) and M5 (LightGBM, exogenous features) motivate three choices: benchmark many models, include LightGBM, use exogenous features.
- **¶3 — Domain studies.** Ceran (2024), Ma (2025), Nguyen (2025): LightGBM accurate and light, no single winner, gradient boosting suited to short series — the thesis's regime.
- **¶4 — Two further results.** Ahrens (2024) grounds model combination; Klee & Xia (2025) add forecast stability as a production criterion alongside accuracy.
- **¶5 — Transition** to why lightweight models are necessary under a budget.

## §2.2 Lightweight ML under Computational and Deployment Constraints *(SRQ1 + Main RQ)*

- **¶1 — Efficiency is binding, not secondary;** for an SME the budget is a modest cloud instance, and the GPU/RAM cost asymmetry materially affects operating cost.
- **¶2 — Ng (2017), reframed.** Ng is a precedent that memory is a first-order design variable, but his constraint is raw-data *volume* at platform scale; this thesis aggregates to a small per-category set, so the binding constraint here is *deployment cost*, not data size.
- **¶3 — Edge-AI / resource-constrained LLMs** (Liu 2025, Semerikov 2025): quantisation/distillation help, but a compressed LLM still needs ~1–4 GB → access the LLM via API rather than loading it locally.
- **¶4 — Conclusion.** Supports the substrate choice (lightweight gradient-boosted trees) evaluated against a fixed budget; the budget binds model selection, not the realised footprint (shown small in Ch5).

## §2.3 From Descriptive BI to Forecast-Informed Decision-Support *(Main RQ + SRQ4)*

- **¶1 — BI is historically descriptive;** modern FMCG needs to anticipate, which requires a deliberate account of how forecasts connect to decisions.
- **¶2 — Predict-then-optimize.** Elmachtoub & Grigas (2022) and Mandi et al. (2024): a forecast is valuable through its link to the decision; low prediction error ≠ good decision.
- **¶3 — Tight vs loose coupling.** That literature couples prediction and decision tightly (a formal objective); FMCG managerial support is open-ended, so the thesis studies a loose, agent-mediated coupling — which the tight-coupling work does not address.
- **¶4 — Interface evidence.** Rinaldi (2025), Olszak & Bartuś (2025), Herath (2024), Goodwin (2010): explanations and communicated uncertainty improve trust and decision quality.
- **¶5 — Synthesis.** Forecasts gain value when connected to decisions, the connection should expose uncertainty, and the explanatory interface shapes quality — motivating the design developed in §2.4–2.7.

## §2.4 LLM Agents and Tool-Mediated Reasoning *(SRQ2)*

- **¶1 — LLM as a tool-using agent** (not just a language model) underpins the SRQ2 interface.
- **¶2 — Foundational tool-use work.** Toolformer (a small model that calls tools can beat a larger one), SciAgent, ART: delegation can substitute for scale and improve precise reasoning → delegate forecasting to a dedicated model.
- **¶3 — Action format.** Wang et al. (2024) on code-as-action; the thesis adopts JSON function-calling for reliability/reproducibility and uses code-as-action only as the SRQ4 baseline.
- **¶4 — Taxonomy and bound.** Sapkota (2025): the artefact is a bounded tool-using agent with human-in-the-loop, not a multi-agent system; multi-agent work (DyLAN, AutoFlow, ScoreFlow) is design context / future work.
- **¶5 — Summary.** The agent literature supplies the core mechanism; multi-agent and code-as-action strands frame the extension and the baseline respectively.

## §2.5 Reliability, Traceability, Uncertainty, and Evaluation of Agentic Outputs *(SRQ2 + SRQ4)*

- **¶1 — Reliability is first-order** when an agent reasons over forecasts that drive decisions; three risks framed: hallucination, input-noise sensitivity, coordination failure.
- **¶2 — Hallucination and noise.** ANAH (Ji 2024) frames numerical hallucination as quantifiable → validate agent outputs against source forecasts; AgentNoiseBench shows degradation under noisy tool inputs.
- **¶3 — Traceability.** AgentCompass and the AgentOps taxonomy (Dong 2025) specify the artifacts needed for auditability; in the thesis traceability is a design objective, with self-verification (Huang 2024) noted as a future enhancement.
- **¶4 — Calibration.** Kuleshov (2018) and Levi (2022): isotonic regression is an effective post-hoc calibration; treated as a design target/requirement (note: conformal calibration is in fact implemented — to be reflected when finalising).
- **¶5 — Evaluation.** Gu (2024), Ye (2024), Mehta/CLEAR (2025): pairwise judging, bias awareness, multidimensional evaluation → the SRQ4 design (separate judge, human-rated subset, pilot scale).
- **¶6 — Transition** to production settings where operational constraints further shape feasibility.

## §2.6 Production-Oriented Agentic Systems and Integration Readiness *(SRQ3)*

- **¶1 — Production sharpens the requirements;** frames the integration-readiness question central to SRQ3.
- **¶2 — Closest exemplar.** González-Potes (2026): a hybrid deterministic/LLM system with high compliance and low numerical error, but real-time industrial supervision, not forecast extension under SME constraints.
- **¶3 — Operational readiness.** Dong (2025) on observability artifacts, Mehta on CLEAR constraints, Zheng (2025) on LLMs in supply-chain workflows.
- **¶4 — Synthesis.** The required capabilities for SRQ3: structured tool interface, observability/traceability, reliability/uncertainty handling, bounded cost/latency/memory — assessed on a real case, not a completed deployment.

## §2.7 Research Gap

- **¶1 — The design space** reveals an under-addressed intersection, not a single missing result.
- **¶2 — The four bodies recapped** with what each does not cover (tight coupling without an agent; tool use without forecasting/production; reliability without integration; production without SME forecast extension).
- **¶3 — The intersection.** How to extend a non-predictive production agentic system with lightweight forecasting through a loose, reliable, traceable interface, and whether this beats a code-as-action baseline.
- **¶4 — Four contributions** stated as designed vs to-be-evaluated (SRQ1 benchmark; SRQ2 interface; SRQ3 readiness; SRQ4 pilot evaluation).
- **¶5 — Methodological framing** as transferable DSR design knowledge, not a fully deployed/evaluated system.

## §2.8 Design Science Research

- **¶1 — Constructive questions** (how to design a system, what its design requires) are the province of DSR.
- **¶2 — Why DSR fits:** the contribution is an artefact plus transferable design knowledge, and DSR disciplines the evaluation against defined criteria in a relevant context.
- **¶3 — Pointer** to Ch3 for the concrete application of the DSR process.

## §2.9 Chapter Summary and Transition

- **¶1 — Recap** of how each literature group supplies a piece (forecasting 2.1–2.2, decision-support 2.3, agent/reliability/production 2.4–2.6) and the identified intersection.
- **¶2 — Transition** to Ch3, which operationalises the artefact, benchmark, interface, readiness assessment, and evaluation design.

---

# Chapter 3 — Methodology

## §3.1 Philosophy of Science

- **¶1 — Pragmatism.** Knowledge is judged by practical consequences ("what works"), well-suited to artefact-oriented research aimed at helping Manifold and similar organisations.
- **¶2 — Modest realism.** Demand and sales exist independently but are known only through the Nielsen instrument with its assumptions → careful data-quality assessment and context-bounded interpretation.
- **¶3 — Empirical stance.** Knowledge claims rest on data and controlled evaluations (prediction and comparison), contrasting with both pure positivism and interpretivism.
- **¶4 — Pragmatism–DSR alignment.** DSR judges knowledge by whether the artefact achieves its objectives — the pragmatist criterion — so the philosophy and method are deliberately consistent.

## §3.2 Research Design: Design Science Research

- **¶1 — DSR adopted** as the primary methodology; the artefact is the predictive extension, plus generalised design principles.
- **¶2 — Three cycles** (Hevner): relevance (Manifold's need), design (Ch5–8), rigor (Ch2 literature) — all explicitly engaged.
- **¶3 — Six activities** (Peffers) mapped onto chapters: problem, objectives, design/development, demonstration, evaluation, communication.
- **¶4 — Design type.** Explanatory (why architectural choices beat the baseline), with the artefact's research-prototype status explicitly acknowledged.

## §3.3 Research Strategy

- **¶1 — Quasi-experiment + case.** A quantitative experiment provides the controlled evaluations for SRQ1 and SRQ4 (single manipulation, all else constant) → internal validity.
- **¶2 — Single-case embedded study.** Manifold = case organisation, Prometheus = empirical case for SRQ3, the Danish beverage market = context; everything anchored in real data, not synthetic benchmarks.
- **¶3 — Unit of analysis.** The artefact, evaluated across categories at brand × retailer → month granularity; DVH EXCL. HD scope locked, decisions pre-registered for reproducibility.

## §3.4 Data Sources

- **¶1 — One source:** the Nielsen/Prometheus scanner panel, the core forecasting input.
- **¶2 — Structure.** Star schema (facts + market/period/product dimensions); 37–42 monthly periods per category (~3–3.5 years); base and promotional sales variants plus weighted distribution as an availability proxy; used under a confidentiality agreement.

## §3.5 Analytical Approach

- **Intro.** Each SRQ has a distinct evaluation protocol because the thesis evaluates accuracy, interface design, integration readiness, and output quality — different evidence types.
- **SRQ1.** Five models across categories; Optuna-tuned; MAPE/RMSE + peak RAM/runtime + stability (Klee & Xia); specialised vs pooled; RAM by RSS (not tracemalloc), reported in Ch6.
- **SRQ2.** JSON function-calling with strict schemas; point forecast + interval (Kuleshov; calibration a design target); inverse-MAPE combination (Ahrens); reliability via validation, traceability via mapping; lightweight coordinator, LangGraph as production target.
- **SRQ3.** Capability-readiness of the four capabilities against the real Prometheus (Graph Engine), not a live integration experiment.
- **SRQ4.** ~50 shared prompts; dedicated-model vs code-as-action (E2B sandbox); correctness/consistency/replicability (primary) + cost/latency (secondary); LLM-as-judge with separate judge, bias awareness, human subset; pilot scale.

## §3.6 Validity and Reliability

- **Internal validity.** Common split across models; fixed seeds + documented preprocessing; single manipulation in SRQ4 isolates the dedicated-model contribution.
- **External validity.** Explicitly bounded (Danish market, 8 GB, monthly batch); single-case design strengthens relevance but limits statistical generalisation.
- **Construct validity.** Each SRQ operationalised through pre-specified metrics to prevent post-hoc metric-selection bias.
- **Reliability.** Code versioning, documented hyperparameters, fixed seeds; LLM-judge non-determinism mitigated by temperature 0 and full logging of prompts/outputs for audit.

## §3.7 Limitations

- **Intro.** Five limitations bound scope and generalisability.
- **Data confidentiality.** Raw data cannot be redistributed → reproducibility limited to features, code, protocol.
- **Training sample size.** 37–42 periods is near the lower bound; meets the ARIMA minimum but limits multi-year seasonal power; partially mitigated by lag/rolling features.
- **Pilot-scale SRQ4.** ~50 prompts → indicative, not conclusive; full evaluation is future work.
- **Sequential execution.** The 8 GB budget forces sequential model runs, increasing latency; acceptable for monthly batch, not for higher-frequency cycles.
- **Case generalisability.** Strong relevance to Manifold but limited statistical generalisation; design principles transferable via the DSR mechanism, to be validated elsewhere.
