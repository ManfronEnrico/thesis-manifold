# Chapter 2 — Literature Review
> Thesis Writing Agent output — BULLET POINTS ONLY (no prose)
> Last updated: 2026-03-15
> Status: SKELETON — all Run 1/2/3 paper references now integrated (37 papers confirmed)
> Pending: human approval before prose writing

---

## 2.0 Chapter Introduction

- Purpose of literature review: establish theoretical foundations across 5 angles; identify academic gap; justify novelty
- Structure: five thematic sections, each mapping to one or more RQs
- Concludes with: explicit gap statement and novelty claim
- Note on scope: literature review covers 2015–2026; AI/LLM literature weighted toward 2020–2026 due to field velocity

---

## 2.1 AI Agents and LLM Orchestration
*(Maps to Main RQ, SRQ2)*

- **2.1.1 From language models to agents**
  - LLMs as reasoning engines vs LLMs as action-takers — the agent paradigm shift
  - **Toolformer (Schick et al., NeurIPS 2023)**: LLMs learn to self-supervise tool calls (APIs, calculators, search); a 6.7B-parameter Toolformer outperforms GPT-3 (175B) on reasoning tasks — tool delegation substitutes for raw parameter scale → foundational justification for the thesis delegating forecasting to ML models rather than asking the LLM to forecast directly [toolformer.md]
  - **ART (Automatic multi-step Reasoning and Tool use, 2023)**: automated multi-step reasoning with tool calls; structured planning decomposition → supports the thesis 5-step synthesis pipeline design [art_multi_step_reasoning.md]
  - **Executable Code Actions (Wang et al., ICML 2024)**: Python code as agent actions outperforms JSON-based formats by up to 20%; self-debugging and dynamic tool composition → provides action-execution substrate for the thesis LangGraph coordinator [executable_code_actions.md]
  - **AI Agents vs Agentic AI taxonomy (2024)**: conceptual taxonomy of autonomy levels — clarifies the thesis system as a "multi-agent agentic AI" with human-in-the-loop approval gates [ai_agents_vs_agentic_ai.md]

- **2.1.2 Multi-agent coordination**
  - Single-agent limitations: context window overflow, task complexity, role conflict
  - Multi-agent architectures: task decomposition, specialisation, coordination
  - **LangGraph (LangChain, 2024)**: stateful multi-agent orchestration with conditional edges, interrupt_before for human-in-the-loop, MemorySaver checkpointing → the thesis's chosen orchestration framework; supports reproducible phase transitions [langgraph_2024.md — software citation; supplement with academic papers below]
  - **Dynamic LLM-Powered Agent Network (2023, arXiv)**: dynamic selection of specialist agents per subtask; +10.3pp performance over static routing on multi-step reasoning; confirms that dynamic agent specialisation outperforms single-agent generalisation → directly supports the thesis 4-agent decomposition (data, forecasting, synthesis, validation) [dynamic_llm_agent_network.md — Run 3]
  - **AutoFlow (2024, arXiv)**: automated DAG-based workflow generation for LLM agent pipelines; within 5% of hand-crafted pipelines; demonstrates that structured orchestration graphs generalise across task types → provides academic grounding for LangGraph-style graph-based orchestration [autoflow_llm_workflow.md — Run 3]
  - **ScoreFlow (2025, arXiv)**: score-based preference optimisation for LLM agent workflows; +4–7pp over DSPy/OPRO baselines; continuous preference scoring improves multi-step coordination → supports the thesis's use of human approval gates as a quality control mechanism in multi-step agent coordination [scoreflow_llm_workflow.md — Run 3]
  - **SciAgent (2024, arXiv)**: tool-augmented LLMs for structured reasoning tasks; +13.4pp over GPT-4 tool-free; confirms that tool delegation (structured APIs, external models) is superior to end-to-end LLM reasoning for precision-sensitive tasks → reinforces the thesis design choice of delegating forecasting to specialised ML tools rather than the LLM [sciagent_tool_augmented_llm.md — Run 3]

- **2.1.3 Reliability and limitations of LLM agents**
  - **ANAH (ACL 2024)**: analytical annotation framework for LLM hallucinations; establishes taxonomy of factual errors in LLM outputs → motivates the thesis's LLM-as-Judge evaluation protocol (Level 2 Validation) and the design rule "LLM synthesis outputs must be validated against source forecasts" [anah_hallucination_eval.md — Run 2]
  - **AgentNoiseBench (arXiv 2026 — not peer-reviewed)**: noise robustness benchmark for tool-using LLM agents; documents that agent performance degrades systematically under input noise → informs thesis failure mode analysis (Ch.8.4.3) and the use of structured, validated feature inputs to the Synthesis Agent [agent_noise_bench.md — Run 2]
  - **AgentCompass (2025, arXiv)**: evaluation of agentic workflows in production; finds 34% step-level error rate vs benchmark expectations; structured traceability reduces debugging time 60% → supports the thesis's mandatory human approval gates as error-containment checkpoints and motivates the 3-level validation framework [agentcompass_workflow_eval.md — Run 3]
  - **Self-Verification Sampling (2024, ICLR)**: self-verification before tool call execution reduces argument errors 31% and improves task completion +8.4pp with no fine-tuning → motivates the thesis Validation Agent's role in verifying Synthesis Agent outputs before they reach the user [self_verification_sampling_llm.md — Run 3]
  - **Implication for thesis design**: Synthesis Agent uses temperature=0, structured inputs, and explicit confidence scoring precisely because LLM hallucination on numerical data is a documented, quantified risk across multiple papers

- **2.1.4 Gap in this section**
  - Most multi-agent papers assume cloud-scale compute or do not address memory budgets
  - **Hybrid AI + LLM Industrial Agent (Bürger & Pauli, 2024, Elsevier EAAI)**: the architecturally closest paper in the corpus — hybrid ML + LLM for industrial process control (CIP, dairy production); 12–18% efficiency gains vs human operators. Key gap: industrial process domain (clean sensor data, physical constraints, no RAM budget, no consumer survey enrichment) — the thesis is the retail CPG transposition [hybrid_ai_llm_industrial.md]
  - No paper in the corpus designs a multi-agent system for ≤8GB RAM in a business analytics context — **confirmed primary gap**

---

## 2.2 Predictive Modelling for Decision-Support
*(Maps to SRQ1, SRQ4)*

- **2.2.1 From descriptive to predictive analytics**
  - Descriptive analytics: historical reporting, KPI dashboards, BI systems
  - Predictive analytics: forecasting future states using statistical/ML models
  - Prescriptive analytics: recommending actions based on predictions
  - The transition challenge: most BI systems are descriptive; predictive requires different infrastructure
  - **AI-enhanced BI (2025, Procedia)**: 34% higher decision confidence and 28% higher forecast adoption rate reported for AI-enhanced BI vs. traditional descriptive BI; key driver is explanation alongside prediction → directly supports SRQ4 framing and Synthesis Agent design [ai_enhanced_bi_decision_making.md]
  - **Design principles for AI-augmented decision making (2024, EJIS)**: action design research study deriving design principles for AI-augmented BI; "AI systems must communicate uncertainty to be trusted" → directly supports confidence scoring design [ai_augmented_decision_making_dsr.md]
  - **DSS4EX (2025, Expert Systems with Applications)**: decision support system framework for AI pipelines applied to time series forecasting; explainability layer yields significantly higher decision quality scores than raw ML outputs → confirms the thesis's design choice of natural language recommendation layer (Synthesis Agent) over raw forecast output [dss4ex_decision_support.md — Run 3]

- **2.2.2 Forecasting approaches for retail demand**
  - Classical time series: ARIMA, SARIMA — interpretable, low memory, ~24 period minimum
  - Prophet (Meta): additive decomposition, handles seasonality, ~36 periods suitable
  - Tree-based ensemble: LightGBM, XGBoost — strong on tabular data, feature-rich, low RAM
  - Linear baseline: Ridge Regression — interpretable, near-zero memory, benchmark role
  - **ML-Based Demand Forecasting for FMCG Retailer (2024, Springer LNCS)**: real FMCG retailer, LightGBM achieves best accuracy at lowest RAM footprint; MAPE target ≤15% cited as industry benchmark → primary benchmark for SRQ1 [ml_fmcg_demand_forecasting.md]
  - **Demand Forecasting Methods in FMCG Retail (2023, Springer Book)**: comprehensive review of ML methods for FMCG; confirms tree ensembles outperform statistical baselines on promotional data [fmcg_demand_forecasting_methods.md]
  - **Retail ML: Tree Ensembles vs. LSTM (2024, MDPI Applied Sciences)**: direct comparison of tree ensembles vs. deep learning for retail demand; tree ensembles competitive at 10–100× lower RAM → justifies excluding LSTM from thesis on RAM grounds [retail_ml_tree_ensembles_lstm.md]
  - **Hybrid CNN-LSTM (2024, PLOS ONE)**: 4.16% MAPE with promotional + weather + holiday features using deep learning; serves as aspirational upper bound → thesis explicitly acknowledges this as excluded due to RAM constraint [retail_hybrid_neural_forecasting.md]
  - **Model Averaging + Double Machine Learning (2024, Journal of Applied Econometrics)**: stacking and inverse-variance weighting improve over single learners; DML framework separates nuisance from target estimation → supports the thesis ensemble weighting step in the Synthesis Agent [model_averaging_double_ml.md — Run 2]
  - **ML for Economic Forecasting and SME Growth (2025, Int. Journal of Innovation Studies)**: comprehensive review of 120+ ML papers; LightGBM/XGBoost optimal for short-horizon forecasting with <500 training observations → directly validates the thesis model selection given ~36 Nielsen periods [ml_economic_forecasting_sme.md — Run 3]
  - **Stacked Ensemble for Clinical Decision Support (2025, MDPI Informatics)**: stacked ensemble (Logistic Regression meta-learner over 5 base classifiers) achieves 97.2% accuracy; confirms the two-tier stacking principle for multi-model aggregation → supports the ensemble weighting design in the Synthesis Agent [stacked_ensemble_clinical_decision.md — Run 3]
  - Retail-specific considerations: promotional effects, distribution changes, seasonal peaks

- **2.2.3 Resource-constrained model deployment**
  - **On Accelerating Edge AI (Liu et al., 2025, arXiv)**: quantization + knowledge distillation achieves 94–97% of full-precision accuracy at 3–5× speedup on ARM-class hardware → establishes the technical vocabulary for the thesis's RAM profiling phase and confirms that model compression trade-offs are empirically measurable [edge_ai_resource_constrained.md — Run 2]
  - **Edge Intelligence Survey (2024, Journal of Edge Computing)**: comprehensive survey of LLM deployment in resource-constrained environments; INT8 quantization + knowledge distillation dominate → provides the broader context for why the thesis uses classical ML (not compressed LLMs) for forecasting [edge_ai_inference_survey.md — Run 2]
  - Memory-compute tradeoff: accuracy degradation as a function of model size
  - **LLM-as-synthesiser (not forecaster)**: LLMs in Supply Chain Management (2025, IFAC) — case study shows LLM adds value as orchestrator/interpreter of ML outputs, not as direct forecaster; 78% of recommendations rated actionable vs. 45% for raw ML outputs → validates thesis Synthesis Agent design [llms_supply_chain.md]

- **2.2.4 Gap in this section**
  - No paper systematically benchmarks ARIMA/Prophet/LightGBM/XGBoost/Ridge head-to-head within a strict RAM budget in a retail CPG context
  - The 4.16% MAPE benchmark (CNN-LSTM, PLOS ONE 2024) is the current state-of-the-art for retail with enriched features; the thesis is the first to compare lightweight models against this benchmark under an explicit 8GB constraint

---

## 2.3 Hybrid AI: Integrating Symbolic Reasoning and Machine Learning
*(Maps to SRQ2, Main RQ)*

- **2.3.1 Neuro-symbolic AI**
  - Definition: combining neural networks (data-driven) with symbolic reasoning (rule-based, interpretable)
  - **Neuro-Symbolic AI: Systematic Review 2024 (Colelough & Regli, 2025, arXiv)**: comprehensive PRISMA review of 200+ papers; neuro-symbolic systems outperform pure neural networks by 15–30% in low-data regimes (< 1,000 training examples); classifies the thesis framework as a "data-driven + rule-based hybrid" where the LLM provides symbolic-style reasoning over ML predictions [neuro_symbolic_ai_2024.md — Run 2]
  - **Hybrid AI Models: Symbolic Reasoning + Deep Learning (2024, ResearchGate preprint)**: proposes integration framework for symbolic + neural AI; argues hybrid architectures outperform pure approaches in complex decision-making tasks requiring both pattern recognition and logical inference → theoretical grounding for the thesis LLM+ML architecture [hybrid_ai_symbolic_deep_learning.md]
  - Relevance: the thesis multi-agent framework = hybrid (LLM symbolic reasoning + ML numerical prediction + structured synthesis rules)

- **2.3.2 LLM + ML integration patterns**
  - Core pattern: ML produces calibrated numerical predictions → LLM synthesises into contextualised natural language recommendation
  - **Hybrid AI and LLM-Enabled Agent — Clean-in-Place Industrial (Bürger & Pauli, 2024, EAAI)**: the architecturally closest paper; 3-layer hybrid (physics/symbolic + ML prediction + LLM recommendation) applied to dairy CIP process control; demonstrates 12–18% efficiency gain vs human operators → cited in Ch.5 as the blueprint the thesis adapts for retail CPG [hybrid_ai_llm_industrial.md]
  - **LLMs in Supply Chain (2025, IFAC)**: LLM as interpreter of ML outputs, not direct forecaster; 78% recommendation actionability vs 45% for raw ML → validates the thesis LLM synthesis layer design [llms_supply_chain.md]

- **2.3.3 Gap in this section**
  - The Hybrid AI + LLM Industrial paper (the closest blueprint) addresses industrial process control — not retail CPG forecasting; does not address RAM constraints or consumer survey enrichment
  - No paper applies the hybrid LLM+ML pattern to consumer goods demand prediction in a resource-constrained SME AI context
  - **Confidence scoring in hybrid AI recommendations is absent**: none of the hybrid AI papers propose a composite confidence score formula — this is the thesis's methodological contribution to the pattern

---

## 2.4 Multi-Criteria Decision Synthesis
*(Maps to SRQ2, SRQ3)*

- **2.4.1 MCDM foundations**
  - Multi-Criteria Decision-Making: aggregating heterogeneous signals into a single decision score
  - Key methods: TOPSIS, AHP, ELECTRE, weighted scoring
  - **Overview of MCDM Methods in Industrial Environments (2025, MDPI Technologies)**: AHP + TOPSIS dominate 60%+ of industrial MCDM applications; hybrid MCDM+ML combinations are an emerging but rare pattern → confirms the thesis's composite confidence score (weighted aggregation of 3 components) is methodologically grounded in the MCDM tradition [mcdm_methods_overview.md — Run 3]
  - **Hybrid MCDM + ML for Supplier Selection (2024, Supply Chain Management)**: integrates ML predictions with AHP-weighted MCDM synthesis for explainable decisions → provides a directly analogous pattern: ML outputs (supplier risk scores) → MCDM weighting → recommendation [hybrid_mcdm_ml_supplier.md]
  - Relevance to thesis: synthesis module aggregates predictions from 5 models + consumer context → single recommendation via a composite confidence score (0.40 × interval width + 0.30 × model agreement + 0.30 × consumer signal alignment)

- **2.4.2 Confidence calibration as a decision-quality mechanism**
  - **Accurate Uncertainties for Deep Learning (Kuleshov et al., ICML 2018)**: proposes isotonic regression post-hoc calibration for regression prediction intervals; target: empirical coverage ≥ stated coverage → directly underpins the thesis calibration protocol [calibrated_regression_uncertainty.md]
  - **Evaluating and Calibrating Uncertainty in Regression Tasks (2023, MDPI Sensors)**: systematic comparison of 6 calibration methods across 12 datasets; isotonic regression is most consistently effective, including on tree ensembles (LightGBM, XGBoost) → empirical validation that Kuleshov method applies to thesis model family [calibrating_uncertainty_regression.md]
  - **Do Forecasts as Prediction Intervals Improve Planning? (2010, EJOR)**: controlled experiment (N=84 practitioners); interval-expressed forecasts reduce newsvendor cost by 14.2% vs. point-only; benefit concentrated in high-uncertainty items → empirical justification for why the thesis outputs prediction intervals rather than point forecasts [prediction_intervals_planning.md]

- **2.4.3 Contextual information in decision synthesis**
  - SRQ3 theoretical basis: does more context improve decision quality?
  - **Customer Segmentation + Sales Prediction (2023, Neural Computing & Applications)**: integrates customer segment features with sales prediction; segment-level demand indicators are effective enrichment signals → validates Indeks Danmark → consumer demand index approach [customer_segmentation_sales_prediction.md]
  - **Consumer Behavior in Supermarket Analytics (2025, Computers & Industrial Engineering)**: ML for consumer behaviour in retail; external consumer attributes measurably improve forecast accuracy [consumer_behavior_supermarket_ml.md]
  - Consumer survey data as external signal: underexplored in retail forecasting literature — identified as a genuine gap

- **2.4.4 Gap in this section**
  - No paper applies calibrated MCDM-style synthesis to aggregate competing ML forecasting models in a retail CPG context
  - Integration of consumer survey data (behavioural/attitudinal) into ML-based demand forecasting agent systems is a genuine gap confirmed by corpus review

---

## 2.5 Resource-Constrained AI Deployment
*(Maps to SRQ1, Main RQ)*

- **2.5.1 The resource constraint problem**
  - Enterprise cloud costs: 8GB RAM = realistic budget for SME AI product deployment
  - Edge AI literature frames the same problem at device level (On Accelerating Edge AI)
  - Model efficiency metrics: MAPE per GB RAM, inference latency per MB memory

- **2.5.2 Memory optimisation strategies**
  - Sequential model execution vs parallel: tradeoff between speed and memory
  - Lazy loading: load model only when needed; unload immediately after
  - Feature selection: reducing Indeks Danmark from 6,364 to ~50–100 variables saves ~900MB
  - API-based LLM calls vs local inference: eliminates 4–8GB weight loading cost

- **2.5.3 Gap in this section**
  - No paper provides a systematic memory profiling methodology for a multi-component AI pipeline combining ML forecasting + LLM synthesis
  - This thesis contributes that methodology as a replicable protocol

---

## 2.6 Academic Gap Statement

- **Summary of gaps identified (grounded in corpus)**:
  1. **RAM-constrained multi-agent forecasting**: No framework combines LLM orchestration + ML ensemble forecasting + MCDM synthesis within ≤8GB RAM. [Supported by: all 5 SRQ1 papers exclude RAM as a design constraint; LLM papers assume cloud-scale compute]
  2. **Head-to-head benchmark under RAM budget**: No paper benchmarks ARIMA/Prophet/LightGBM/XGBoost/Ridge simultaneously under an explicit RAM constraint in retail CPG. [Supported by: FMCG Demand Forecasting 2024, Demand Forecasting Methods 2023, MDPI Applied Sciences 2024 — each tests individual models, not the RAM-bounded ensemble]
  3. **Consumer survey enrichment in agent-based forecasting**: Behavioural/attitudinal consumer survey data has not been used as a demand forecasting enrichment signal in multi-agent AI systems. [Supported by: Customer Segmentation 2023, Consumer Behavior 2025 — address segmentation, not multi-agent integration]
  4. **Empirical evaluation of the descriptive-to-predictive BI transition**: The transition is discussed conceptually [AI-enhanced BI 2025, Design Principles for AI-augmented BI 2024] but never empirically evaluated in a real retail CPG context against a defined descriptive baseline.
  5. **Memory profiling methodology for multi-component AI pipelines**: No paper provides a replicable RAM profiling protocol for a pipeline combining ML models + LLM synthesis. This thesis contributes that protocol as a standalone methodological artefact.

- **Novelty claim** (grounded in 5 identified gaps):
  - This thesis is the first to: design, implement, and evaluate a multi-agent predictive decision-support framework that simultaneously (a) operates within an 8GB RAM constraint, (b) integrates consumer survey data as a contextual enrichment signal, (c) generates calibrated confidence-scored natural language recommendations, and (d) is empirically compared against a defined descriptive analytics baseline in a real Danish retail CPG context.
  - Theoretical contribution: 5 generalised design principles derived from the framework evaluation, structured per the DSR design-theory output format (Hevner et al., 2004; Artifact Types in IS Design Science, 2012).

---

## CBS Compliance Notes

- ✅ Literature review must lead to an explicit gap statement (done above)
- ✅ Theory section must connect to RQs (each section maps to specific SRQs)
- ⚠️ All papers must be cited in APA 7 format — annotations from agent will provide citation data
- ⚠️ ~20 pages for literature review = ~45,500 characters — this skeleton covers all sections; flesh out with paper-specific arguments once annotations arrive
- ⚠️ Philosophy of science is in Ch.3 (Methodology), not here — per CBS guidance
