---
name: Gap Analysis & Novelty (v4)
description: v4 gap analysis + novelty statement aligned to the code-as-action / cost-justified reframe. Supersedes gap_analysis.md (2026-03-15, pre-reframe, still Indeks-based). Bullet skeleton — approve before Ch2 prose.
status: DRAFT skeleton (bullets) — for approval
supersedes: gap_analysis.md (2026-03-15)
updated: 2026-06-23
---

# Gap Analysis & Novelty — v4

> Aligned to the v4 reframe (17/06, Manifold-endorsed): SRQ4 baseline = **code-as-action LLM**;
> Main RQ adds **cost-justified**; metrics = correctness/consistency/replicability (primary) +
> cost/latency (secondary). Replaces the March gap analysis, which was built on the dropped Indeks
> enrichment + MCDM synthesis + descriptive-BI baseline. Canonical RQs: [[research-questions]].

---

## 1. Corpus state (v4)

- 58 annotated paper notes in `obisdian_paper_analysis/` (superset of Brian's March corpus); 39+
  cited in `references.md`. No paper from Brian's corpus is missing.
- v4 SRQ4 anchors now present: [[infiagent_dabench]] (correctness), [[airepr_reproducibility]]
  (replicability), [[specialised_ml_outperform_llms_cost]] (cost/latency), alongside
  [[executable_code_actions]] (CodeAct method) and [[clear_enterprise_agentic_eval]] (CLEAR eval).
- Methodology anchored on Hevner (2004) + Peffers (2007) DSR, with Saunders, Lewis & Thornhill
  (2023) as the research-design scaffold (onion, secondary data). Philosophy = pragmatism.

## 2. Research angles → representative corpus

- **SRQ1 — lightweight forecasting under constraints**: [[ml_fmcg_demand_forecasting]],
  [[fmcg_demand_forecasting_methods]], [[retail_ml_tree_ensembles_lstm]],
  [[retail_hybrid_neural_forecasting]], [[model_averaging_double_ml]], Makridakis M4/M5.
- **SRQ2 — typed tool/action interface + calibration**: [[toolformer]], [[art_multi_step_reasoning]],
  [[executable_code_actions]], [[langgraph_2024]], [[calibrated_regression_uncertainty]] (Kuleshov),
  [[calibrating_uncertainty_regression]] (Levi).
- **SRQ3 — integration readiness (from a real deployed system)**: [[llms_supply_chain]],
  [[hybrid_ai_llm_industrial]] (González-Potes/Bürger — closest architectural blueprint),
  [[anah_hallucination_eval]], [[agent_noise_bench]], [[agentops_taxonomy]].
- **SRQ4 — dedicated ML vs code-as-action LLM**: [[infiagent_dabench]], [[airepr_reproducibility]],
  [[specialised_ml_outperform_llms_cost]], [[executable_code_actions]], [[clear_enterprise_agentic_eval]],
  [[humans_vs_llms_forecasting]], forecast-stability anchor (Klee & Xia, 2025) for *consistency*.
- **Cross-cutting (cost / resource constraint)**: [[edge_ai_inference_survey]],
  [[edge_ai_resource_constrained]], [[cost_aware_ml_3pl_forecasting]], [[neuro_symbolic_ai_survey_2024]].

## 3. Gaps (v4)

> G1–G5 carried over from Brian's analysis (still valid); **G6 is the new central v4 gap.**

- **G1** — No framework for **extending an existing production agentic system** with forecasting
  under ≤8GB RAM. *Evidence*: SRQ1 papers omit RAM as a design variable; none treat extension of a
  live deployed system. Partially adjacent: [[hybrid_ai_llm_industrial]] (no RAM budget, greenfield).
- **G2** — No head-to-head **ARIMA / Prophet / LightGBM / XGBoost / Ridge** benchmark under an
  explicit RAM budget **with category specialisation** in FMCG retail. *Evidence*: forecasting
  papers each test ≤2 model families; none enforce a memory ceiling or compare across categories.
- **G3** — No **typed tool/action interface** exposing ML forecasts — with uncertainty and
  traceability — to an LLM agent. *Evidence*: tool-use literature ([[toolformer]],
  [[art_multi_step_reasoning]]) covers general tool calling; calibration papers cover interval
  reliability but not the interface schema.
- **G4** — **Integration-readiness criteria** for agentic systems adopting predictive capability
  not empirically derived from a real deployed system. *Evidence*: AI-BI literature is survey/design
  based ([[ai_enhanced_bi_decision_making]], [[ai_augmented_decision_making_dsr]]); none derive
  criteria from a production system.
- **G5** — No **replicable RAM + cost/latency profiling methodology** for multi-component ML + LLM
  pipelines. *Evidence*: absent from all reviewed papers; [[edge_ai_inference_survey]] gives
  component-level benchmarks only.
- **G6 (NEW — central v4 gap)** — No study compares **integrating dedicated lightweight ML models
  into an agentic decision-support system vs a code-as-action LLM** (an LLM that writes, executes,
  and self-corrects its own forecasting code), evaluated on **correctness, consistency,
  replicability + cost/latency**, in a **cost-aware FMCG retail** context.
  - The *components* exist but never the *intersection*: [[infiagent_dabench]] defines and measures
    the code-as-action paradigm (but generic data analysis, no cost budget, no agentic-vs-ML
    comparison); [[airepr_reproducibility]] operationalises replicability of LLM analysis code (but
    generic); [[specialised_ml_outperform_llms_cost]] shows specialised ML beats an LLM on
    cost/latency/accuracy (but different domain, no agentic layer); [[executable_code_actions]] is
    the method, not an evaluation against dedicated ML.
  - **Verdict**: genuine, literature-supported gap — this is the thesis's primary novelty claim.

## 4. Novelty statement (v4)

- **Empirical/instantiation**: first evaluation of whether **integrating dedicated lightweight ML
  forecasting into a production-oriented agentic DSS is cost-justified** relative to a **code-as-action
  LLM baseline**, on a real FMCG retail scanner panel under a ≤8GB RAM deployment budget.
- **Artefact**: a working forecast-tool extension of a production agentic system — 3 layers
  (forecasting substrate → typed forecast-tool interface → bounded tool-using agent; see [[research-questions]] / Ch5).
- **Method-level**: a replicable evaluation protocol pairing **correctness / consistency /
  replicability** (primary) with **cost / latency** (secondary), CLEAR-aligned
  ([[clear_enterprise_agentic_eval]], Mehta 2025), plus an **RSS-based memory/cost profiling**
  protocol for ML + LLM pipelines (addresses G5).
- **Strongest differentiator**: the intersection of (dedicated-ML-vs-code-as-action) × (FMCG
  cost-aware) × (production agentic extension) appears in no corpus paper.

## 5. Explicit drops vs March novelty

- ❌ **Indeks Danmark / consumer-survey enrichment** — dropped entirely (one data source: Nielsen).
- ❌ **MCDM-style synthesis** as a novelty pillar — synthesis is ensemble + isotonic calibration,
  not MCDM aggregation.
- ❌ **"Descriptive analytics baseline"** as the SRQ4 comparator — replaced by the code-as-action
  LLM baseline.
- ❌ **"Multi-agent" framing** — recast as a **bounded tool-using agent** (Sapkota distinction;
  see [[ai_agents_vs_agentic_ai]]).

## 6. Open questions

- Is there a *direct* FMCG code-as-action precedent? (Expected: none — that absence is G6.)
- Is the **consistency** metric sufficiently anchored (forecast stability, Klee & Xia 2025), or add
  one more source?
- **DSR acceptance at CBS** for a Business Administration + Data Science thesis (supervisor
  confirmation — carried from March).
- Confirm preprint acceptability with supervisor: [[specialised_ml_outperform_llms_cost]] (2A) and
  the other flagged preprints.
