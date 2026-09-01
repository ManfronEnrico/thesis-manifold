Table of Contents

Table of Contents	2

Table of Figures	9

Table of Tables	9

Abstract	9

Purpose	9

Bullet skeleton (to be converted to prose after empirical results available)	9

Problem	9

Method	9

Key findings (TBD - fill after empirical results)	10

Contribution	10

Scope note	10

Character count target	10

Outstanding	10

Chapter 1 - Introduction	11

1.1 Background and Motivation	11

1.2 Research Problem	14

1.3 Research Questions	14

1.4 Delimitation	17

1.5 Thesis Structure	19

References cited in this chapter	20

Chapter 2 - Literature Review: Forecast-Informed Agentic Decision-Support under Constraints	21

2.0 Chapter Introduction	21

2.1 Forecasting as Predictive Substrate in FMCG	23

2.2 Lightweight ML under Computational and Deployment Constraints	25

2.3 From Descriptive BI to Forecast-Informed Decision-Support	26

2.4 LLM Agents and Tool-Mediated Reasoning	29

2.5 Reliability, Traceability, Uncertainty, and Evaluation of Agentic Outputs	31

2.6 Production-Oriented Agentic Systems and Integration Readiness	33

2.7 Research Gap: Forecast-Informed Extension of Non-Predictive Agentic Systems	35

2.8 Design Science Research	37

2.9 Chapter Summary and Transition to Methodology	38

References cited in this chapter	39

Chapter 3 - Methodology	41

3.1 Philosophy of Science	41

3.2 Research Design: Design Science Research	43

3.3 Research Strategy	44

3.4 Data Sources	46

3.5 Analytical Approach	46

3.6 Validity and Reliability	48

3.7 Limitations	49

References cited in this chapter	51

Chapter 4 - Data Assessment	51

4.1 Overview and Data Strategy	51

4.2 The Nielsen Scanner Panel (core forecasting input)	52

4.2.1 Source, Type, and Access	52

4.2.2 Schema and Structure	52

4.2.3 Overall Suitability	54

4.2.4 Precise Suitability	55

4.2.5 Forecasting Suitability	55

4.3 CSD - Worked Category (EDA and Parameters)	56

4.3.1 Scope and Filtering	56

4.3.2 Stationarity	56

4.3.3 Seasonality	57

4.3.4 Autocorrelation and Lag Structure	57

4.3.5 Parameter Summary	58

4.3.6 Per-category EDA - danskvand, energidrikke, RTD	58

4.4 Feature Engineering (forecasting substrate)	59

4.5 Train, Validation, and Test Split	61

4.6 Key Risks and Mitigations	62

References cited in this chapter	63

Chapter 5 - Predictive-Extension Architecture	63

5.1 Design Objectives and Constraints	63

5.2 Architectural Overview	64

5.3 The Forecasting Substrate (SRQ1)	65

5.4 The Structured Forecast-Tool Interface (SRQ2)	66

5.5 The Bounded Tool-Using Agentic Layer	67

5.6 Integration Readiness (SRQ3)	67

5.7 The Code-as-Action Baseline (SRQ4)	68

5.8 Memory, Cost, and Latency Budget	68

5.9 Technology Choices and Justification	69

5.10 Summary	70

References cited in this chapter	71

Chapter 6 - Model Benchmark & Selection	72

6.1 Rationale for model selection	72

6.2 Model descriptions	72

6.2.0 Simple benchmarks	72

6.2.1 ARIMA	73

6.2.2 Prophet (Meta)	73

6.2.3 LightGBM	73

6.2.4 XGBoost	73

6.2.5 Ridge regression	73

6.3 Experimental setup	74

6.3.1 Grain and data split	74

6.3.2 Feature engineering	74

6.3.3 Execution protocol	74

6.3.4 Validation scheme	74

6.3.5 Hyperparameter optimisation	75

6.4 Evaluation metrics	75

6.4.1 Why WMAPE is the primary metric	76

6.4.2 Scorability, and what is excluded from what	76

6.4.3 Targets	77

6.4.4 Demand-pattern categorisation	77

6.5 Results	78

6.5.1 Tabular-model benchmark	78

6.5.2 The simple benchmarks, and where they win	79

6.5.3 Scaled error (MASE)	80

6.5.4 Pooled versus per-category training	81

6.5.5 Results by demand pattern	82

6.5.6 Operational profile	82

6.5.7 Prediction-interval calibration	83

6.5.8 Remaining gaps	84

6.5.9 Forecast stability across seeds	84

6.6 Model selection decision	85

6.7 Connection to SRQs	86

Outstanding decisions	86

Chapter 7 - Context-Aware Decision Synthesis	87

7.1 The synthesis problem	87

7.2 Architecture of the Synthesis Agent	87

7.2.1 Inputs to the Synthesis Agent	87

7.2.2 Synthesis pipeline	88

7.2.3 Deterministic synthesis results	88

7.3 LLM prompt design	89

7.3.1 System prompt (Synthesis Agent)	89

7.3.2 User prompt structure	90

7.4 Design principles applied	90

7.5 Computational footprint	90

7.6 Evaluation (SRQ2 operationalisation)	91

7.6.1 Result	91

7.7 Connection to SRQs	91

Outstanding decisions	92

Chapter 8 - Experimental Evaluation	92

8.1 Evaluation overview	92

8.2 Level 1 - ML accuracy evaluation (SRQ1)	92

8.2.1 Benchmark design	92

8.2.2 Metrics	93

8.2.3 Baselines	93

8.2.5 Results (Level 1 - SRQ1)	93

8.3 Level 2 - Recommendation quality evaluation (SRQ2)	93

8.3.1 LLM-as-Judge protocol	93

8.3.2 Calibration check	94

8.3.3 SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst	94

8.3.4 Results (Level 2 - SRQ2)	94

8.4 Level 3 - Agent behaviour evaluation (SRQ1 + SRQ2)	95

8.4.1 RAM profiling	95

8.4.2 Latency profiling	95

8.4.3 Failure mode analysis	96

8.4.4 Results (Level 3 - operational)	96

8.5 Threats to validity	96

8.6 Connection to SRQs	97

Outstanding decisions	97

Chapter 9 - Discussion	98

9.1 Interpretation of findings	98

9.1.1 SRQ1: Forecasting accuracy under constraints	98

9.1.2 SRQ2: Synthesis quality	98

9.1.3 SRQ3: Integration readiness	99

9.1.4 SRQ4: dedicated ML vs the LLM/traditional baselines	99

9.2 Theoretical contributions	100

9.2.1 Design knowledge contribution (DSR framing)	100

9.2.2 Design principles (generalised from thesis findings)	100

9.2.2 Novelty claims	101

9.2.3 Contribution to IS literature	101

9.3 Practical implications	102

9.4 Limitations	102

9.5 Future research directions	102

Outstanding decisions	102

Chapter 10 - Conclusion	103

10.1 Summary of contributions	103

10.2 Theoretical contribution (design principles)	104

10.3 Practical recommendations for Manifold AI	104

10.4 Limitations recap	105

10.5 Future research	105

10.6 Final statement	105

Outstanding decisions	106

Reference List	106

AI Use Declaration	111

Draft text (bullet form - NOT prose yet)	111

Heading	111

What AI was used for (declaration bullets)	111

What AI was NOT used for	111

Transparency note	112

Placement options (confirm with supervisor)	112

Outstanding	112

Appendix	114

Table of Figures

Table of Tables

Abstract

Purpose

The abstract summarises the entire thesis in one page. CBS examiners read it first — it must communicate problem, method, findings, and contribution clearly.

Bullet skeleton (to be converted to prose after empirical results available)

Problem

Business Intelligence systems in SME retail contexts operate primarily at a descriptive analytics level, producing retrospective reports rather than forward-looking recommendations

Transitioning to predictive decision-support requires ML forecasting infrastructure that is typically resource-intensive and economically inaccessible at enterprise cloud scale for SME AI providers

Gap: no validated framework exists for resource-constrained (≤8GB RAM) multi-agent AI decision-support integrating heterogeneous data signals in a retail CPG context

Method

Design Science Research (Hevner et al., 2004; Peffers et al., 2007): design, implementation, and evaluation of a multi-agent AI framework

Artefact: a multi-agent system (LangGraph orchestration + 5 lightweight ML models + LLM synthesis via Claude API) deployed on Danish CSD retail data (Nielsen CSD panel + Indeks Danmark consumer survey)

3-level evaluation framework: ML accuracy (Level 1), recommendation quality / LLM-as-Judge (Level 2), RAM and latency profiling (Level 3)

Key findings (TBD - fill after empirical results)

SRQ1: [Best model family, MAPE achieved, RAM within/near 8GB constraint]

SRQ2: [Calibration coverage, LLM-as-Judge score, vs. baseline]

SRQ3: [MAPE improvement from consumer signal enrichment — X%]

SRQ4: [AI system vs. descriptive BI , on which dimensions and by how much]

Contribution

Validated proof-of-concept for AI-augmented demand forecasting within ≤8GB RAM

5 generalised design principles for resource-constrained multi-agent AI deployment

Memory profiling methodology for multi-component AI pipelines (replicable protocol)

Demonstrated feasibility of LLM synthesis layer for calibrated, contextualised demand recommendations

Scope note

Single empirical context: Danish CSD retail, Manifold AI / Nielsen CSD panel, Indeks Danmark consumer survey

Findings are indicative for the SME AI decision-support domain; generalisation requires further validation

Character count target

Maximum: 2,275 characters including spaces

Equivalent to approximately 350–380 words

When writing prose: use Word → Review → Word Count → Characters (with spaces) to verify

Outstanding

Fill SRQ1–SRQ4 findings once empirical results are available (Phase 4–6)

Confirm language of abstract with supervisor (English if English programme)

Final character count check before submission

Chapter 1 - Introduction

1.1 Background and Motivation

The accelerating adoption of artificial intelligence across business domains has fundamentally reshaped expectations for what analytical systems can and should deliver. For decades, business intelligence (BI) systems have served a primarily descriptive function: they aggregate historical data into dashboards, key performance indicator reports, and trend summaries that tell managers what has happened (Rinaldi et al., 2025). While such systems have generated substantial operational value, the growing complexity of modern markets demands something more: the ability to tell managers not just what happened, but what is likely to happen next and what they should do about it.

This transition from descriptive to forecast-informed decision-support is particularly consequential in the fast-moving consumer goods (FMCG) sector, where demand volatility, promotional dynamics, seasonal variation, and stock keeping unit (SKU) proliferation create forecasting challenges that traditional statistical approaches struggle to address (Ma et al., 2025). In the beverage segment, the domain investigated in this thesis, demand patterns are often erratic, intermittent, and sensitive to external signals such as consumer sentiment, seasonal consumption trends, and promotional calendars. These characteristics render uniform forecasting approaches inadequate: Ma et al. (2025) demonstrate in a large-scale empirical study of a private-label beverage manufacturer that no single model dominates across all demand patterns, and that machine learning models enriched with exogenous contextual features substantially outperform statistical baselines for high-volume stable SKUs.

The broader forecasting literature confirms this directional shift. The M4 Competition, the largest empirical benchmarking study in the history of the field covering 100,000 time series and 61 forecasting methods, established that combining multiple forecasting models consistently outperforms any single best model selection, and that hybrid methods blending statistical structure with machine learning achieve the highest accuracy (Makridakis et al., 2020). Its successor, the M5 Competition, focused specifically on hierarchical retail sales forecasting using real Walmart data and produced a finding of direct relevance to this thesis: all top 50 performing submissions used LightGBM, a gradient-boosted tree ensemble method, achieving more than 14% improvement over the best statistical benchmark (Makridakis et al., 2022). Critically, the M5 results also confirmed that exogenous and explanatory variables, including promotional calendars and environmental signals, materially improved forecasting accuracy. Makridakis et al. (2020) concluded their analysis by explicitly identifying the integration of explanatory variables as the open frontier for the field: “One thing that remains to be determined is the possible improvement in PF and PI performances that can be achieved by expanding time series forecasting to include explanatory/exogenous variables.1 This element could be explored in future M Competitions, thus expanding time series forecasting competitions in a new and ambitious direction.” This thesis takes up that direction by incorporating exogenous predictors into its forecasting substrate, while extending the problem beyond forecasting accuracy alone to how such forecasts can be reliably integrated into a resource-constrained agentic decision-support system.

Yet the practical deployment of predictive AI systems in business settings faces a constraint that the academic forecasting literature has largely left unexamined: computational resource limitations. Enterprise cloud deployments capable of running large deep learning models at scale are economically inaccessible to small and medium-sized AI providers. The cost asymmetry is stark: transformer-based forecasters and locally hosted large language models require GPU instances with tens to hundreds of gigabytes of accelerator memory, which on major cloud platforms cost on the order of one to seven US dollars per hour of continuous operation [CITATION TO ADD: cloud-instance pricing source], whereas a general-purpose instance with eight gigabytes of RAM costs a small fraction of that. For a provider serving inference continuously across many client queries, this differential compounds into an order-of-magnitude difference in operating cost, which is why resource-efficient deployment is treated as a first-order constraint in the edge and resource-constrained AI literature (Liu et al., 2025; Semerikov et al., 2025). Ng (2017), working with four terabytes of Nielsen weekly scanner data, demonstrated empirically that memory constraints are the primary binding design variable in retail scanner data analysis; even with unlimited financial resources, the full dataset cannot be loaded simultaneously, making memory-efficient algorithmic choices not merely convenient but necessary. For the realistic cloud deployment budget of an SME AI provider, a ceiling of approximately eight gigabytes of total RAM is not a worst-case assumption but a practical constraint that eliminates most transformer-based architectures and severely limits model selection options.

This constraint has received no systematic attention in the agentic AI literature, where frameworks for LLM-based decision support consistently assume cloud-scale compute infrastructure. The gap is not merely technical: it reflects a broader structural asymmetry in AI research, where benchmarks and system designs are validated on infrastructure available to large research labs and technology companies, while the majority of organisations that could benefit from forecast-informed decision-support operate with considerably more limited resources. Bridging this asymmetry by demonstrating that reliable forecast-informed decision-support is achievable within the resource envelope of an SME cloud deployment is itself a research contribution independent of the specific domain application. The emerging paradigm of Agentic AI, comprising systems of multiple specialised agents that coordinate, communicate, and dynamically allocate sub-tasks to achieve a common goal (Sapkota et al., 2026), has demonstrated substantial promise across industrial, clinical, and scientific applications, with systems such as AutoFlow, ScoreFlow, and SciAgent establishing the orchestration patterns reviewed in Chapter 2. The architecturally closest of these to the present work is the hybrid deterministic/LLM system of González-Potes et al. (2026), deployed for supervision of an industrial batch process, which achieved state specification consistency above 98%, meaning that the rule-based severity label assigned to a process state matched the actual process conditions in that proportion of cases, together with median LLM numerical errors below 3% in its summaries of buffered process variables, suggesting that LLM-based decision support can approach production-relevant reliability requirements when the architecture carefully separates deterministic and generative components. On the forecasting side, Rinaldi et al. (2025) bring agentic decision support closer to the present domain through DSS4EX, an explainability layer over time series forecasting pipelines. Neither line of work, however, addresses the specific combination this thesis targets: a lightweight forecasting substrate, exposed to a bounded tool-using agentic layer through a structured interface that preserves reliability and uncertainty, and deployed under a fixed RAM budget. This combination is the gap the thesis addresses.

The Danish retail market provides a particularly appropriate empirical context for this investigation. Denmark is a mature, highly concentrated retail market dominated by a small number of large grocery chains, in which scanner panel data, collected systematically by providers such as Nielsen, offers granular, longitudinal insight into sales dynamics at the product and retailer level. The Nielsen scanner panel is the core forecasting input for this thesis.

1.2 Research Problem

The commercial context motivating this research is Manifold AI, a Danish company building “AI Colleagues,” a conversational, production-oriented agentic decision-support system for retail analytics that currently operates at the descriptive level: it reports what has happened, including sales volumes, market shares, and weighted distribution, but does not forecast, anticipate, or recommend; this production system also serves as the empirical reference case for the thesis. Extending such a non-predictive agentic system with predictive capability raises four problems. First, the forecasting substrate must be accurate yet deployable within a tight computational budget, a trade-off the forecasting literature has only recently begun to measure systematically (Klee & Xia, 2025). Second, its forecasts must be exposed to the agentic layer through a structured tool interface that preserves reliability, uncertainty, and traceability. Third, the production agentic system itself must possess the architectural and operational capabilities required to integrate such a substrate. Fourth, the resulting decision-support outputs must demonstrably improve, at justified cost, on what a general-purpose LLM that writes and self-corrects its own code (a code-as-action baseline) would produce; the dedicated-model integration must earn its place against this strong LLM-only alternative.

This thesis addresses these problems by extending a production-oriented agentic decision-support system with a lightweight forecasting substrate, exposed through a structured forecast-tool interface to a bounded tool-using agentic decision-support layer, and by specifying the integration-readiness capabilities such an extension requires, all designed to operate within the 8GB RAM budget characteristic of realistic SME cloud deployment.

1.3 Research Questions

The overarching research question guiding this thesis is:

This question is decomposed into four subsidiary research questions, each targeting a component of the design and evaluation challenge:

SRQ1: Which lightweight forecasting models provide the best trade-off between accuracy, memory efficiency, and category specialization for FMCG demand forecasting under computational constraints?

SRQ1 motivates the empirical model benchmark in Chapter 6, which evaluates lightweight forecasting models across the four beverage categories on forecasting accuracy, memory efficiency, and forecast stability, and tests whether category-specialised models outperform a single pooled model. Accuracy alone is insufficient for production deployment: a model with marginally lower error but higher memory use or unstable output is a worse engineering choice under a fixed RAM budget (Klee & Xia, 2025). The models, metrics, and protocol are defined in Chapter 3.

SRQ2: How can forecasting outputs be exposed to an agentic decision-support system through a structured tool/action interface that preserves reliability, uncertainty, and traceability?

SRQ2 motivates the design of a structured forecast-tool interface (Chapter 5) and its realisation in a bounded tool-using agentic decision-support layer (Chapter 7). The interface is designed to preserve reliability (validating agent outputs against the source forecasts), uncertainty (forecasts accompanied by interval information), and traceability (a recorded mapping from tool call and forecast value to recommendation). The prototype uses a lightweight Python coordinator with JSON-based function calling; a LangGraph deployment, as in the production reference system, is the production target rather than the implementation evaluated in this thesis.

SRQ3: What architectural and operational capabilities are required for a production-oriented agentic system to integrate forecast-informed decision-support?

SRQ3 motivates an integration-readiness specification (Chapter 5, assessed in Chapters 7 and 9): the capabilities, namely a structured tool interface for invoking external predictive models, observability and traceability of tool calls, explicit handling of reliability and uncertainty, and operation within bounded cost, latency, and memory, that a production-oriented agentic system must possess to incorporate a forecasting substrate.

These capabilities are assessed against Manifold AI’s production agentic system as the empirical case. The assessment is grounded in a working integration rather than in architectural analysis alone: the forecasting tool developed for SRQ2 is registered with and executed inside the production system as part of the SRQ4 evaluation, and the readiness criteria are derived from the capabilities that integration actually depended upon. The thesis does not, however, claim a completed production deployment; the integration is conducted for evaluation purposes within a research collaboration, and questions of operational hardening, monitoring at scale, and organisational adoption remain outside its scope.

SRQ4: To what extent does giving an agentic decision-support system access to dedicated lightweight forecasting models improve the correctness, consistency, and replicability of forecast-informed decision-support outputs, at justified cost and latency, relative to the same system with only data access and code execution (a code-as-action baseline), and does that improvement hold in a production agentic system as well as in a general-purpose one?

SRQ4 motivates the comparative evaluation in Chapter 8, which tests whether dedicated forecasting models are warranted at all, or whether an agent that writes, executes, and self-corrects its own forecasting code in a sandboxed environment is already sufficient. The evaluation is structured as a ladder of scenarios in which capability is added one variable at a time: an LLM with no data access; the same LLM with data access and code execution; the same LLM additionally given a dedicated forecasting tool; and the same two conditions repeated inside Manifold AI’s production agentic system. The third and fifth rungs isolate the contribution of the dedicated model, once in a general-purpose orchestrator and once in the production one.

This structure is the central methodological feature of the evaluation. Because the same intervention, adding the forecasting tool, is applied in two independently built agentic systems, a consistent effect cannot be attributed to the design of a single evaluation harness. The two settings also differ in reproducibility, and deliberately so: the general-purpose rungs are reproducible from the thesis repository and an API key, while the production rungs are ecologically valid but cannot be re-executed by a reader, as the production system is proprietary. Neither property is sufficient alone, and the design is constructed so that the two corroborate one another.

The scenarios are compared on correctness, consistency, and replicability as primary dimensions and on cost and latency as secondary dimensions. All measures are computed programmatically against held-out actuals and recorded execution traces; no model is used to judge another model’s output. Consistency is measured by repeated execution of an identical prompt rather than by breadth of prompt coverage, since run-to-run variance is the property of interest. This evaluation is conducted at pilot scale in the first instance rather than as a full study; a full evaluation at greater scale, and an optional comparison against the non-predictive production reference system, are identified as further work.

Figure 1.1 - Hierarchical structure of the research questions: the main research question and its four subsidiary questions (SRQ1–SRQ4).

1.4 Delimitation

The scope of this thesis is bounded by a set of deliberate delimitations that reflect both the practical constraints of the research setting and the methodological choices required to ensure a tractable empirical evaluation.

Domain and geography. The thesis focuses on the Danish beverage retail market, evaluated across four Nielsen product categories: carbonated soft drinks (CSD), still and sparkling water (danskvand), energy drinks (energidrikke), and ready-to-drink beverages (RTD). A fifth category, beer (totalbeer), was included in the original scope and subsequently excluded on computational grounds: at 455 brands it is an order of magnitude larger than the others and would have dominated both preprocessing time and the memory budget the thesis sets out to respect. This multi-category scope is driven by data availability and by the design of the model benchmark: the Nielsen/Prometheus scanner panel provides up to 44 monthly periods per category at the market scope used here, giving sufficient longitudinal depth for time series forecasting while remaining manageable within the RAM constraint. The four categories were selected in collaboration with Manifold AI as representative of the FMCG challenges the system must address, including high promotional sensitivity, seasonal demand patterns, and strong competitive dynamics, while differing systematically in scale and in measurement coverage, which allows the benchmark to test whether the modelling findings generalise across heterogeneous category structures. The categories differ in capability as well as in size: promotional measures are reported for CSD and energidrikke but not for danskvand or RTD, a structural property of the Danish market as Nielsen measures it rather than a limitation of the data extract.

Computational constraint. The framework is constrained to a maximum of 8 gigabytes of total RAM across all simultaneously active components. This constraint explicitly excludes transformer-based deep learning architectures (including LSTM, Temporal Fusion Transformer, N-BEATS, and Chronos) that require substantially more memory at inference time. The constraint is not a convenience but a formal design criterion reflecting the realistic cloud budget of SME AI providers and is motivated by empirical precedent in the retail scanner data literature (Ng, 2017).

Processing mode. The framework operates on monthly batch processing of historical data, not real-time streaming. This reflects the operational planning horizon of retail demand forecasting, where tactical decisions are made on weekly or monthly cycles. Real-time data ingestion and streaming inference are explicitly out of scope.

Deployment scope. The thesis does not aim to produce a production-ready deployed system. The artefact, a lightweight forecasting substrate with a bounded tool-using agentic decision-support layer, is a research prototype evaluated on historical data using Design Science Research methodology (Hevner et al., 2004; Peffers et al., 2007). Its outputs are to be validated against defined research metrics, specifically forecast accuracy, computational efficiency, recommendation quality, and comparative performance against a general-purpose code-as-action LLM baseline at pilot scale, but not against live business outcomes.

Generalisability. The thesis is bounded to the Danish market and to the Nielsen scanner panel as the data source. While the five-category benchmark provides evidence on whether the modelling findings hold across heterogeneous beverage categories, generalisation to other national markets, to non-beverage FMCG categories, or to other data sources lies beyond its scope and is a direction for future research.

1.5 Thesis Structure

The remainder of this thesis is organised into nine chapters, each corresponding to a distinct phase of the Design Science Research process (Peffers et al., 2007).

Chapter 2 reviews the literature across eight thematic sections: forecasting as a predictive substrate for FMCG demand; lightweight machine learning under computational and deployment constraints; the transition from descriptive business intelligence to forecast-informed decision-support; LLM agents and tool-mediated reasoning; the reliability, traceability, uncertainty, and evaluation of agentic outputs; production-oriented agentic systems and integration readiness; the research gap; and Design Science Research. This review establishes the theoretical foundations and the gap that the thesis addresses.

Chapter 3 details the research methodology, grounding the thesis in Design Science Research and specifying the data sources, preprocessing, the forecasting-model benchmark, the structured forecast-tool interface, the integration-readiness assessment, and the evaluation design that compares dedicated-model agentic decision-support against a code-as-action LLM baseline.

Chapter 4 presents the data assessment, characterising the quality, structure, and forecasting suitability of the Nielsen scanner data across the four beverage categories, and documenting the preprocessing decisions that inform the modelling.

Chapter 5 describes the predictive-extension architecture: the forecasting substrate, the structured forecast-tool interface, and the bounded tool-using agentic decision-support layer, together with the integration-readiness capabilities, justified against the 8GB RAM budget. The evaluated prototype uses a lightweight Python coordinator; a LangGraph deployment is identified as the production target.

Chapter 6 addresses SRQ1 through an empirical model benchmark, comparing lightweight forecasting models across the four categories on accuracy, memory efficiency, and stability, and testing category specialisation against pooling.

Chapter 7 addresses SRQ2, and informs SRQ3, through the agentic extension prototype: the tool-using agent that consumes forecasts and their uncertainty through the structured interface and produces decision-support recommendations.

Chapter 8 addresses SRQ4 through a pilot evaluation comparing dedicated-model agentic decision-support against a general-purpose code-as-action LLM baseline, on correctness, consistency, and replicability (primary) and cost and latency (secondary).

Chapter 9 discusses the contributions, the integration-readiness findings, and the limitations of the thesis, including pilot-scale evaluation and designed-but-unevaluated calibration, and identifies directions for future research.

Chapter 10 concludes by synthesising answers to the four subsidiary research questions and the main research question, and reflecting on the broader implications for extending production-oriented agentic decision-support systems with forecasting capabilities under resource constraints.

References cited in this chapter

González-Potes, A., et al. (2026). Hybrid AI and LLM-enabled agent-based real-time decision support architecture for industrial batch processes. AI, 7(2), 51.

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. MIS Quarterly, 28(1), 75–105.

Liu, S., Guo, B., Yu, Z., et al. (2025). On accelerating edge AI: Optimizing resource-constrained environments. arXiv preprint arXiv:2501.15014. [PREPRINT - not peer-reviewed]

Sapkota, R., Roumeliotis, K. I., & Karkee, M. (2026). AI agents vs. agentic AI: A conceptual taxonomy, applications and challenges. Information Fusion, 126, Article 103599. https://doi.org/10.1016/j.inffus.2025.103599

Semerikov, S. O., Vakaliuk, T. A., Kanevska, O. B., Ostroushko, O. A., & Kolhatin, A. O. (2025). Edge intelligence unleashed: A survey on deploying large language models in resource-constrained environments. Journal of Edge Computing, 4(2). https://doi.org/10.55056/jec.1000

Klee, S., & Xia, Y. (2025). Measuring time series forecast stability for demand planning. KDD ’25 Workshop on AI for Supply Chain.

Ma, B. J., Jackson, I., Huang, M., Villegas, S., & Macias-Aguayo, J. (2025). A data-driven and context-aware approach for demand forecasting in the beverage industry. International Journal of Logistics Research and Applications.

Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2020). The M4 competition: 100,000 time series and 61 forecasting methods. International Journal of Forecasting, 36(1), 54–74.

Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. International Journal of Forecasting, 38(4), 1346–1364.

Ng, S. (2017). Opportunities and challenges: Lessons from analyzing terabytes of scanner data. NBER Working Paper, 23673.

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. Journal of Management Information Systems, 24(3), 45–77.

Rinaldi, G., Giordano, F., De Stefano, C., & Fontanella, F. (2025). DSS4EX: A decision support system framework to explore artificial intelligence pipelines with an application in time series forecasting. Expert Systems With Applications, 269, 126421.

Chapter 2 - Literature Review: Forecast-Informed Agentic Decision-Support under Constraints

2.0 Chapter Introduction

This chapter reviews the literature that situates the thesis’s central problem: how a production-oriented agentic decision-support system that lacks native predictive capability can be extended with lightweight forecasting models to support reliable, forecast-informed decision-making under computational and deployment constraints. The review is organised so that each body of literature supplies one element of that problem, and the elements are then shown to be jointly under-addressed.

The research idea originated in a collaboration with Manifold AI, which introduced the topic in a university presentation; the authors took it up out of a shared academic interest in an ambitious and still under-exploited application of AI, namely the extension of agentic systems from describing the past toward supporting forward-looking, forecast-informed decisions. As the research questions were refined over the course of the project, from an initial multi-agent framing toward the present focus on forecast-informed, cost-justified decision support, the scope of the reviewed literature was refined in step, in the iterative manner characteristic of a literature review (Saunders et al., 2023).

This chapter is a narrative, integrative review rather than a systematic review (Saunders et al., 2023): the contribution lies at the intersection of several distinct literatures rather than in a single bounded effectiveness question, so a thematic synthesis is more appropriate than a protocol-driven search. The search was conducted using Google Scholar and NotebookLM, with references managed in Zotero. Starting from the research questions, key concepts and search terms were defined for each thematic area; an initial set of approximately one hundred records was screened by title, of which around forty were retained and assessed more closely by abstract, introduction, and conclusion. Retained sources were mapped onto the predefined thematic areas, and areas found to be under-covered prompted additional search terms and further rounds of searching and evaluation until the themes were adequately covered. Sources were selected for relevance to the research questions and read in full; peer-reviewed work was prioritised, and non-peer-reviewed preprints were included only where they constitute the closest available precedent and are flagged as such throughout. The review draws on the resulting corpus of forty-two cited sources, of which 14 are flagged as preprints or non-peer-reviewed. Following the source-level verification described below, several works are cited under corrected authorship or publication years relative to earlier drafts of this chapter.

The chapter proceeds in eight thematic sections. Section 2.1 reviews forecasting as the predictive substrate for FMCG demand, and Section 2.2 the lightweight-model and resource-constraint literature that governs how such a substrate can be deployed economically. Section 2.3 turns to the decision side, reviewing the move from descriptive business intelligence to forecast-informed decision-support and the peer-reviewed evidence that predictions create value through their connection to downstream decisions. Section 2.4 reviews LLM agents and tool-mediated reasoning, the mechanism by which a forecast can be exposed to a decision-support agent, and Section 2.5 the reliability, traceability, uncertainty, and evaluation requirements that such agentic outputs entail. Section 2.6 reviews production-oriented agentic systems and the capabilities required for integration. Section 2.7 consolidates these strands into the research gap the thesis addresses, and Section 2.8 establishes Design Science Research as the methodological paradigm. Section 2.9 summarises the review and transitions to the methodology.

Throughout, a distinction is maintained between what the reviewed literature establishes and what the thesis designs, plans to evaluate, or leaves to future work, so that the gap statement rests on evidence rather than aspiration.

2.1 Forecasting as Predictive Substrate in FMCG

Maps to SRQ1

The predictive substrate of a forecast-informed decision-support system is a demand-forecasting model. The retail FMCG forecasting literature has converged on a set of modelling approaches whose relative performance depends on the characteristics of the demand series: its temporal regularity, the availability of exogenous features, the size of the training set, and the computational resources available at inference. The models considered as the substrate in this thesis, namely ARIMA, Prophet, LightGBM, XGBoost, and Ridge Regression, span classical statistical approaches through gradient-boosted tree ensembles, chosen to cover the accuracy–efficiency trade-off frontier; the computational dimension is developed in Section 2.2.

The large-scale forecasting competitions provide the empirical backdrop. The M4 Competition (Makridakis et al., 2020), spanning 100,000 series and 61 methods, established that combining models tends to outperform any single best model and that hybrids of statistical structure and machine learning achieve the highest accuracy. Its scope must be stated precisely, because it bounds what may be inferred from it here: low-volume and intermittent series were explicitly excluded from the M4 dataset, and the authors caution that the findings refer to continuous business series and may not carry over to irregular demand. Evidence on irregular series in this thesis therefore rests on M5, which forecasts disaggregated product-store sales, and not on M4. The M5 Competition (Makridakis et al., 2022), focused on hierarchical retail sales forecasting on Walmart scanner data, is directly relevant: all of the top fifty submissions used LightGBM, and all of them improved on the best-performing statistical benchmark, exponential smoothing with bottom-up aggregation, by more than fourteen percent; submissions incorporating exogenous promotional and calendar features outperformed those using sales history alone. M5 further reports that cross-learning, in which one model is trained across many series rather than one model per series, outperformed series-by-series training at lower computational cost, which is the direct precedent for the pooled-versus-per-category comparison of SRQ1. These results motivate three substrate choices in this thesis: benchmarking multiple models rather than pre-selecting one, including LightGBM as a primary candidate, and incorporating exogenous features where available.

Domain studies reinforce these findings in FMCG specifically. Ceran et al. (2024), forecasting daily product-store sales across roughly fourteen million series for a national supermarket chain, select LightGBM with Optuna hyperparameter tuning and reach a weighted root mean squared scaled error of 0.83, improved to 0.81 by ensembling group-specific models. Their choice of metric is itself instructive here: they explicitly reject MAPE because their panel contains too many zero-demand observations for a percentage error to be well defined, adopting scaled and absolute errors instead. Chapter 6 encounters and documents the same problem on the Nielsen panel. Ma et al. (2025) extend this to the beverage sector, showing that machine learning models enriched with exogenous contextual features can outperform statistical baselines for high-volume, stable SKUs, with no single model dominating across demand patterns, a finding that motivates evaluating category-specialised models rather than assuming one model suits all categories. Al-Karkhi and Rządkowski (2025), reviewing over 120 machine learning papers in economic forecasting and SME applications, identify LightGBM and XGBoost as well suited to short-horizon forecasting with limited training observations, the regime of this thesis, in which each category provides roughly three years of monthly observations.

Two further results shape the substrate design. Ahrens et al. (2025) provide theoretical grounding for model combination, showing that stacking a diverse set of candidate learners under constrained least squares consistently lowers mean squared prediction error relative to any single learner, and introducing a lower-cost short-stacking variant. Their setting is double machine learning for causal inference rather than time-series forecasting, so the result transfers here as a general argument for pooling diverse estimators against model misspecification, not as direct forecasting evidence. Klee and Xia (2025) draw attention to forecast stability across repeated production runs, defining stability as the coefficient of variation of forecasts under nominally identical inputs and hyperparameters, varying only the random seed. The direction of their finding matters and is easily inverted: classical local statistical models such as ARIMA are deterministic and therefore trivially stable under this definition, with a coefficient of variation of zero, whereas stochastic deep-learning forecasters vary materially between seeds. Their contribution is that ensembling tree-based and zero-shot models with deep architectures recovers stability, to below five percent, without costing accuracy. The transferable point for this thesis is that any model with a stochastic fitting procedure, gradient-boosted trees included, must have its seed sensitivity measured rather than assumed, and that stability is a production-relevant criterion alongside accuracy. These results motivate evaluating the substrate, in the SRQ1 benchmark, on the joint criteria of accuracy, computational efficiency, and stability.

The computational dimension of this substrate, namely why lightweight models are necessary under a constrained deployment budget, is developed in the next section.

2.2 Lightweight ML under Computational and Deployment Constraints

Maps to SRQ1 and Main RQ

The deployment of AI systems in real business settings is subject to computational constraints that are often treated as secondary design considerations in forecasting research. For a small or medium-sized provider, the relevant budget is not the data-centre scale assumed in much of the agent literature but a modest cloud instance. The cost asymmetry is substantial: transformer-based forecasters and locally hosted large language models often require substantially more accelerator memory than lightweight tabular models, available only on GPU instances that are markedly more expensive to run continuously than a general-purpose instance with a few gigabytes of RAM; for a provider serving inference across many client queries, this difference can materially affect operating costs. Computational efficiency is therefore a binding consideration rather than an afterthought.

A precedent for treating memory as a first-order design variable in this domain comes from Ng (2017), who, analysing four terabytes of Nielsen scanner data, showed that memory can become the primary binding constraint in retail scanner-data analysis: at the full panel scale, in-memory analysis becomes infeasible and memory-efficient algorithmic choices become necessary rather than merely convenient. Two levels must be distinguished, however. Ng’s constraint is one of raw-data volume, which binds at the platform scale at which a production system ingests the complete scanner panel; the present thesis, by contrast, aggregates the panel to a brand-by-month modelling set of a few thousand rows per category (Chapter 4), at which data volume is no longer the binding factor. The constraint that does bind here is the deployment budget introduced above: the modest cloud instance an SME provider can afford to run continuously for inference, which excludes transformer and locally hosted large-language-model options before model fitting even begins. Ng therefore serves to establish that a memory budget is a legitimate, domain-grounded design variable rather than an artificial limitation, while making explicit that the budget operating in this thesis is one of deployment cost rather than of raw-data size.

The edge-AI and resource-constrained-LLM literatures characterise the same problem at the model level. Liu et al. (2025) evaluate quantisation and distillation for edge deployments, showing that substantial accuracy can be preserved at sharply reduced memory footprints. Semerikov et al. (2025) survey resource-constrained LLM deployment, documenting that quantisation and knowledge distillation are the dominant practical strategies but that even aggressively compressed LLMs typically require on the order of one to four gigabytes. The implication for a multi-component pipeline that must simultaneously load data, run forecasting models, and host a reasoning layer is that local LLM inference is difficult to accommodate within a small fixed memory budget; accessing the language model through an external API, rather than loading it locally, is the more viable pattern under such constraints.

Taken together with the FMCG forecasting evidence of the previous section, this literature supports the thesis’s substrate choice: lightweight gradient-boosted tree models, which the reviewed edge-AI and FMCG studies suggest may offer a favourable accuracy-to-memory ratio relative to deep-learning and transformer alternatives, evaluated explicitly against a fixed memory budget (on the order of eight gigabytes in this thesis’s deployment setting). The budget operates principally as a constraint on the model-selection space, ruling out transformer and locally hosted options at the design stage, rather than as a limit the selected lightweight models approach in practice; the realised footprint of the chosen substrate is shown in Chapter 5 to sit well within the budget. The memory-profiling method by which the thesis quantifies this budget, and the specific optimisation strategies it adopts, are matters of methodology and are presented in Chapters 3 and 5 rather than here.

2.3 From Descriptive BI to Forecast-Informed Decision-Support

Maps to Main RQ and SRQ4

Business intelligence systems have historically occupied the descriptive tier of the analytics spectrum, aggregating historical transactional data into dashboards, key performance indicator reports, and trend summaries. This descriptive function has generated substantial operational value for organisations, but the competitive dynamics of modern FMCG markets increasingly demand the ability to anticipate rather than retrospectively report. The transition from descriptive analytics to forecast-informed decision-support requires not only predictive models but a deliberate account of how forecasts are connected to the decisions they inform.

A substantial peer-reviewed literature establishes that predictive models create value chiefly through their connection to downstream decisions. Elmachtoub and Grigas (2022), in the smart “predict, then optimize” framework, show that minimising prediction error is not equivalent to maximising decision quality: a prediction with small statistical error can yield a poor decision, while a less accurate prediction aligned with the decision boundary can yield a near-optimal one. They formalise a decision-aware loss and a tractable convex surrogate, demonstrating that training predictors with respect to the downstream objective improves the resulting decisions. Mandi et al. (2024), in a Journal of Artificial Intelligence Research survey of decision-focused learning, generalise this insight across a taxonomy of methods, noting that zero prediction loss implies zero decision loss but not the converse, and that no single method dominates across decision problems. Together, these works ground the principle that a forecast is valuable to the extent that it is connected to a downstream decision.

This literature couples prediction and decision tightly: the predictor is trained, through differentiable optimization, against a known and formally specified decision objective. Such coupling presumes a single, well-defined optimization program. Managerial decision-support in FMCG retail rarely presents such a program; decisions there are open-ended, context-dependent, and mediated by a human planner. The present thesis therefore investigates a loose, agent-mediated form of forecast-to-decision coupling, in which forecasts are produced by conventionally trained models and surfaced to a decision-support layer that reasons over them to generate recommendations. The tight-coupling literature motivates the underlying principle but does not address this loosely coupled, agent-mediated setting, and it does not concern large language model agents.

Empirical work on the decision-support interface qualifies how that connection must be made. Rinaldi et al. (2025) propose DSS4EX, a decision-support framework that wraps time-series forecasting pipelines in an explainability layer generating natural-language explanations and Shapley-value feature attributions; their evaluation indicates that explanatory layers can improve perceived decision quality relative to raw model outputs. Two boundaries of that system matter for the gap developed in Section 2.7: DSS4EX explains point forecasts and does not represent forecast uncertainty, and it operates as a graphical dashboard querying a configured pipeline rather than as an agent that invokes tools autonomously. Olszak and Bartuś (2025) suggest that AI-enhanced business intelligence can increase decision confidence and forecast-adoption when predictions are accompanied by explanations. Pathirannehelage et al. (2025), through action design research across three organisations, derive a design principle of direct relevance: AI decision-support systems must communicate uncertainty to be trusted by non-technical business users. The decision value of communicated uncertainty is, however, conditional on how that uncertainty is presented, and the experimental evidence is a caution rather than an endorsement. Goodwin et al. (2010) gave participants a newsvendor-style production task under asymmetric shortage and surplus costs and found that supplying fifty or ninety-five percent prediction intervals alongside the point forecast did not improve decision quality relative to the point forecast alone. Worse, intervals actively degraded the participants’ responsiveness to the cost asymmetry: rather than shifting the order quantity toward the more expensive side of the loss function, participants anchored near the interval midpoint, and the proportion of decisions discriminating correctly between the two cost regimes fell from roughly eighty-four percent under point forecasts to forty-four percent under ninety-five percent intervals.

This result is important to state accurately, because it changes what the design must do. It does not license the conclusion that uncertainty should be withheld: Pathirannehelage et al. (2025) find that communicated uncertainty is a precondition of trust, and the calibration literature of Section 2.5 makes an uncommunicated interval useless. What it establishes is that an interval handed to a planner as a raw numeric range is not self-interpreting, and that the interpretive step between the interval and the decision, which Goodwin’s participants had to perform unaided and largely failed to perform, is the part that carries the decision value. That step is precisely what an agentic layer is positioned to supply.

Taken together, this body of work frames the requirements for the proposed forecast-informed decision-support layer: forecasts gain value when connected to decisions; that connection must expose uncertainty, but exposing it as a bare interval is demonstrably insufficient; and the interpretive interface therefore materially shapes decision quality. These findings motivate the design of a forecast-informed decision-support layer in which forecasts are accompanied by uncertainty information, explanatory context, and decision-oriented recommendations that make the implication of the interval explicit rather than leaving it to be inferred. How such a layer can be realised through a tool-using agent, and how it should be evaluated against a code-as-action LLM baseline, is the subject of Sections 2.4 to 2.7.

2.4 LLM Agents and Tool-Mediated Reasoning

Maps to SRQ2

The emergence of large language models as reasoning engines has shifted their role from generative text systems to action-taking agents that invoke external tools, decompose tasks, and revise plans in response to feedback. This distinction, between an LLM as a language model and an LLM as a tool-using agent, underpins the interface design at the centre of SRQ2.

A foundational result is Toolformer (Schick et al., 2023), which showed that language models can learn to invoke external APIs, calculators, and search engines, and that a 6.7-billion-parameter Toolformer can outperform a far larger model on downstream reasoning tasks. The implication, central to this thesis, is that tool delegation can partially compensate for model scale by allowing an LLM to rely on specialised external capabilities, including a dedicated forecasting model rather than attempting to forecast itself. Ma et al. (2024) reinforce this with SciAgent, showing that equipping an LLM with domain-specific tools for computation and retrieval substantially improves precision-sensitive reasoning over a tool-free baseline; for this thesis, an LLM acting as a reasoning orchestrator, delegating numerical prediction to a dedicated model while retaining synthesis and communication, is more appropriate than asking the LLM to perform numerical prediction end-to-end. Paranjape et al. (2023), through ART, show that automatically decomposing a task into structured reasoning-and-tool-use steps can improve task performance and controllability relative to single-shot prompting, motivating a structured rather than unstructured tool-invocation sequence in the thesis’s decision-support layer.

The format of the agent’s actions is itself a design dimension. Wang et al. (2024) report that executable code can offer advantages over JSON-formatted tool calls on some agentic benchmarks, enabling dynamic tool composition and self-debugging. The thesis’s own dedicated-model agent adopts the widely supported JSON-based function-calling interface for reliability and reproducibility; the code-as-action pattern characterised by Wang et al. (2024), in which a general-purpose LLM writes, executes, and self-corrects its own code, is adopted not as the thesis artefact but as the baseline against which dedicated-model integration is evaluated (SRQ4).

A conceptual taxonomy helps to situate, and to bound, the present system. Sapkota et al. (2026) distinguish AI Agents, defined as modular, task-specific systems driven by a single LLM with tool use, from Agentic AI, characterised by multi-agent collaboration, persistent memory, and coordinated autonomy. Under this taxonomy the thesis artefact at its current stage is most accurately described as a bounded tool-using AI agent with human-in-the-loop checkpoints, rather than a full multi-agent Agentic AI system; a multi-agent decomposition is a design and production-target consideration, not a property of the thesis artefact at its current stage. The multi-agent coordination literature is nonetheless instructive as design context: Liu et al. (2024, DyLAN) show that dynamically activating specialist agents can outperform fixed pipelines, while Li et al. (2024, AutoFlow) and Wang et al. (2025, ScoreFlow) show that structured, graph-based orchestration can be generated and optimised automatically, by reinforcement learning and by preference optimisation respectively, and report better consistency and error recovery than fixed pipelines. These are empirical architecture results rather than an established standard, and are read here as evidence about a promising design direction rather than as prescribed practice. These works inform how a single-agent prototype could later be decomposed into a coordinated multi-agent production system, but they are not part of the artefact at its current stage.

In sum, the agent literature supplies the core mechanism on which the thesis relies, an LLM delegating prediction to an external model through a structured tool interface, while the multi-agent strand describes an extension beyond the current artefact and the code-as-action strand supplies the baseline comparator for the thesis’s evaluation. How forecasts are exposed through that interface, and how the resulting outputs are made reliable and evaluable, is developed in Section 2.5.

2.5 Reliability, Traceability, Uncertainty, and Evaluation of Agentic Outputs

Maps to SRQ2 and SRQ4

When a forecast is surfaced through an agentic layer that reasons over it in natural language, the reliability of that layer becomes a first-order concern: in decision-support, an agent’s output influences managerial decisions with operational and financial consequences. The literature characterises three reliability risks directly relevant to a forecast-informed agent, namely hallucination, input-noise sensitivity, and coordination failure, together with the traceability and evaluation mechanisms needed to manage them.

Ji et al. (2024), through ANAH, establish a sentence-level annotation scheme for hallucination in knowledge-grounded generation, classifying each generated sentence against a retrieved reference fragment as containing no hallucination, a contradictory hallucination, an unverifiable hallucination, or no checkable fact at all. The scheme is developed for question answering rather than for numerical reporting, so it does not supply a category for misstated figures; what it does supply, and what this thesis takes from it, is the principle that a generated statement is assessable only against an explicitly retrieved source. Applied to a forecast-informed agent, whose reference fragment is the forecast value returned by the tool, that principle motivates a validation step in which the figures in an agent output are checked against the source forecast before delivery, so that a misstated number is a contradictory statement with respect to a known reference rather than an unverifiable one. Wang et al. (2026), through AgentNoiseBench, show that tool-using agents degrade systematically when tool inputs contain structured noise such as mislabelled features or formatting inconsistencies, establishing input-noise robustness as a measurable engineering challenge and motivating disciplined validation of the data passed to a forecasting tool.

Reliability in production also depends on traceability. Kartik et al. (2025), in AgentCompass, highlight non-trivial step-level errors in unstructured agentic workflows and argue that structured traceability mechanisms reduce debugging effort when failures occur; that reduction is asserted on the basis of their deployment experience rather than measured against an untraced control, and is read here as a design rationale rather than an empirical result. Dong et al. (2024) generalise this into a taxonomy of AgentOps observability, specifying the artifacts, namely execution traces, tool-call spans, prompt and guardrail registries, that must be captured for a foundation-model agent to be auditable, positioning such traceability as relevant to emerging compliance and auditability expectations. These works establish traceability as a design requirement for any production-oriented agentic decision-support layer; in the present thesis it is treated as a design objective for the tool interface (a recorded mapping from tool call and forecast value to recommendation), not as a fully implemented capability of the artefact at its current stage. Guo et al. (2025) contribute a complementary reliability mechanism, self-verification sampling, in which an agent evaluates candidate outputs before committing to a tool call. Although not implemented in the thesis prototype, this mechanism illustrates a possible future reliability enhancement.

Communicating forecast uncertainty reliably requires that stated intervals be calibrated, and two distinct families of method address this. The first is post-hoc recalibration of a model’s own predictive distribution: Kuleshov et al. (2018) show that fitting an isotonic regression to the empirical cumulative distribution function can align observed interval coverage with stated coverage probabilities, and Levi et al. (2022) confirm the approach as consistently effective at reducing expected normalised calibration error. The scope of that confirmation should be stated: their evaluation covers neural architectures, a fully connected network and a DenseNet, and does not extend to gradient-boosted tree ensembles, so it cannot be read as validating isotonic calibration of the tree models used as this thesis’s substrate.

The second family is conformal prediction, which is the approach the artefact actually adopts and which the recalibration literature above does not cover. Rather than reshaping a model’s predictive distribution, split conformal prediction sets an interval half-width from the empirical quantile of residuals on a held-out calibration set, yielding distribution-free finite-sample coverage under an exchangeability assumption and requiring no assumption about the underlying model, which makes it applicable to gradient-boosted trees directly (Lei et al., 2018). Its guarantee is marginal, an average over the calibration population rather than a promise about any individual forecast, and exchangeability is violated by temporal data; Barber et al. (2023) quantify the resulting coverage loss under distribution drift and bound it rather than eliminating it. Both limitations bear directly on a monthly demand panel, and Chapter 6 accordingly measures coverage empirically on a held-out test period rather than treating the guarantee as given.

Finally, evaluating whether an agentic layer improves decision-support outputs requires an evaluation methodology that is itself reliable. A growing literature examines the use of LLMs as evaluators. Gu et al. (2025) survey this design space, concluding that pairwise comparison tends to be more consistent than absolute scoring and that judge reliability depends on consistency, robustness, and alignment with human judgment. Ye et al. (2024) quantify systematic biases in LLM judges, including position and self-enhancement bias, and recommend using a separate model for evaluation together with explicit bias checks. Mehta (2025), through the CLEAR framework, proposes that enterprise agentic systems should be evaluated across multiple dimensions, namely cost, latency, efficacy, assurance, and reliability, rather than accuracy alone, arguing, and reporting preliminary evidence, that multidimensional evaluation may correlate more strongly with deployment readiness than accuracy-only evaluation. The consistency dimension is grounded in direct empirical evidence: Ouyang et al. (2025) show that LLM-generated code for an identical prompt varies substantially across repeated runs, with roughly half to three quarters of code-generation tasks yielding no two identical outputs, and Atıl et al. (2025) show that this non-determinism persists even at nominally deterministic API settings such as temperature zero, proposing agreement-rate metrics for quantifying it. The treatment of cost and latency as evaluation dimensions in their own right follows an established line of work: Schwartz et al. (2020) argue that computational cost should be reported as a first-class evaluation criterion alongside accuracy, and Chen et al. (2024) demonstrate that inference costs for comparable output quality differ by orders of magnitude across language models, making cost an operationally decisive property of LLM systems. Together, these works inform the proposed evaluation design (SRQ4): a comparison of dedicated-model agentic decision-support against a code-as-action LLM baseline, judged on correctness, consistency, and replicability as primary dimensions and on cost and latency as secondary dimensions, using a separate judge model with bias awareness and a human-rated subset. These same reliability and bias findings also bound the strength of the thesis’s own evaluation, which at present rests on a small pilot rather than a full-scale study.

The reliability, traceability, and evaluation requirements identified here apply not in the abstract but in real deployment settings, where operational constraints further shape what is feasible, the subject of the next section.

2.6 Production-Oriented Agentic Systems and Integration Readiness

Maps to SRQ3

The reliability and traceability requirements of the previous section are sharpened in production-oriented settings, where an agentic decision-support system must operate within real operational and economic constraints. A small but growing literature examines agentic systems designed for, or deployed in, production rather than benchmark conditions, and it frames the integration-readiness question central to SRQ3: what architectural and operational capabilities a production-oriented agentic system must possess to incorporate forecast-informed decision-support.

González-Potes et al. (2026) provide the closest published exemplar, a hybrid deterministic/LLM architecture for real-time supervision of a clean-in-place batch process at an operating beverage plant, in which a deterministic rule-based supervisor is wrapped by a retrieval-augmented conversational layer running a locally hosted seven-billion-parameter model. They report a state specification consistency above ninety-eight percent, meaning that the rule-based severity label assigned to a process state matched the actual process conditions in that proportion of cases, together with a median numerical error below three percent in the language model’s summaries of buffered process variables. The consistency figure is a property of the labelling layer and should not be read as a rate of correct process operation, which was substantially lower on the degraded stages of their trial. Read with that qualification, the system suggests that LLM-based decision support can approach production-relevant reliability requirements when the architecture carefully separates deterministic and generative components.

Two boundaries of that system bear on the present work, and they are observations about its scope rather than limitations its authors state. The architecture is oriented to monitoring a live process: it summarises and explains buffered readings of current plant conditions, and contains no predictive component that projects a series forward over a historical tabular record. It also runs on dedicated industrial infrastructure with a locally hosted model, and does not treat hardware or operating cost as a design constraint. The authors’ own stated limitations lie elsewhere, in the single process site covered by their trial and the formal verification that regulated manufacturing would additionally demand. The exemplar therefore establishes that production-grade hybrid architectures combining deterministic components with a language model are feasible, while the forecast-extension and resource-constrained settings remain open.

Operational readiness has been characterised more generally. Dong et al. (2024) specify the artifacts a production agent must expose for observability and governance, namely registries, traces, guardrails, and monitoring, providing a vocabulary of operational capabilities that an integrating system must support. Mehta (2025), through the CLEAR framework, characterises the constraints under which such systems are judged, namely cost, latency, efficacy, assurance, and reliability, and reports preliminary evidence that single-run success can overstate reliability relative to multi-run consistency, underscoring that operational dependability, not peak accuracy, governs deployment readiness. Zheng et al. (2025) document the integration of large language models into enterprise supply-chain workflows, illustrating both the appetite for and the practical friction of embedding LLM capabilities into established operational systems.

Synthesised for SRQ3, this literature points to a set of capabilities that production-oriented agentic systems appear to require in order to integrate forecast-informed decision-support: a structured interface for invoking external predictive models; observability and traceability of tool calls and their outputs; explicit handling of reliability and uncertainty; and operation within bounded cost, latency, and memory budgets. The present thesis treats the integration of a forecasting substrate into such a system as a design-and-readiness question, assessed against these capabilities using a real production-oriented empirical case, rather than as a completed production deployment.

2.7 Research Gap: Forecast-Informed Extension of Non-Predictive Agentic Systems

The sections above establish the design space in which this thesis operates and reveal an under-addressed intersection rather than a single missing result.

First, a peer-reviewed literature establishes that predictive models create value chiefly through their connection to downstream decisions, but couples prediction and decision tightly, through differentiable optimization against a formally specified objective (Elmachtoub & Grigas, 2022; Mandi et al., 2024). It does not address open-ended managerial decision-support mediated by an agent, and it does not concern large language model agents. Second, the LLM-agent and tool-use literature shows that agents can invoke external tools and that tool delegation can substitute for raw model scale (Schick et al., 2023), and an emerging strand begins to expose pre-trained statistical models as callable agent tools (Chen & Bibi, 2026); the latter, however, exists only as small, non-peer-reviewed proofs of concept and does not address forecasting, reliability, or production constraints. Third, the reliability and evaluation literature establishes that agentic outputs carry measurable risks, namely hallucination, input-noise sensitivity, and coordination failure, and that their evaluation requires bias-aware, multidimensional methods (Ji et al., 2024; Kartik et al., 2025; Gu et al., 2025; Ye et al., 2024; Mehta, 2025). Fourth, production-oriented agentic systems demonstrate feasibility, but the closest published exemplars are built for real-time supervision of a live process on dedicated infrastructure; neither predictive extension over a historical tabular record nor operation under small-to-medium-enterprise resource constraints falls within their scope (González-Potes et al., 2026; Dong et al., 2024).

The intersection of these four bodies of work is under-addressed: how a production-oriented agentic decision-support system that lacks native predictive capability can be extended with lightweight forecasting models, through a loose, agent-mediated, reliable and traceable tool interface, and whether such dedicated-model integration improves decision-support outputs relative to a code-as-action LLM baseline that writes its own forecasting code. The forecast-to-decision literature supplies the principle but assumes tight coupling; the agent literature supplies tool use, while only emerging work begins to connect such tools to statistical prediction; the reliability and production literatures supply requirements but not the integration. The reviewed literature does not yet provide an integrated account of this combination in the specific setting of forecast-informed, production-oriented agentic decision-support.

This thesis addresses that intersection through four contributions, stated at the level of the system class rather than any single product, and distinguishing what is designed from what is planned for evaluation or left to future work:

Predictive substrate (SRQ1): designed; benchmark to be built. A memory-profiled benchmark of lightweight forecasting models across multiple FMCG beverage categories, characterising the accuracy–efficiency–specialization trade-off under a constrained compute budget.

Structured forecast-tool interface (SRQ2): designed. A tool/action interface exposing forecasts and uncertainty to a tool-using agent, with traceability treated as an explicit design objective.

Integration readiness (SRQ3): designed; assessment planned. A specification of the architectural and operational capabilities a production-oriented agentic system requires to integrate forecast-informed decision-support, to be assessed using a real production-oriented empirical case rather than a completed deployment.

Evaluation (SRQ4): designed; evaluation pending. A comparison of dedicated-model agentic decision-support against a code-as-action LLM baseline, on correctness, consistency, and replicability (primary) and cost and latency (secondary), planned at the scale of a pilot in the first instance rather than a full study.

The methodological contribution is framed, in the design science tradition (Hevner et al., 2004; Peffers et al., 2007), as transferable design knowledge about extending non-predictive agentic decision-support systems with a forecasting substrate, not as a claim of a fully deployed or fully evaluated production system. Empirical calibration of uncertainty and full-scale evaluation are identified as directions for further work rather than completed results.

2.8 Design Science Research

Maps to all research questions

The questions this thesis addresses are constructive: they concern how a system can be designed and what capabilities its design requires, rather than the testing of a pre-existing theory. Such questions are the province of Design Science Research (DSR), the information-systems paradigm concerned with building and evaluating novel artefacts and with generating transferable design knowledge from them. Hevner et al. (2004) establish the foundational DSR framework, distinguishing the construction of a working artefact from the behavioural study of existing systems, and articulating guidelines that require an artefact to be both demonstrably useful in a relevant problem context and a source of generalisable knowledge beyond its specific instantiation. Peffers et al. (2007) complement this with a process model, namely problem identification, objective definition, design and development, demonstration, evaluation, and communication, that structures a DSR project as an ordered, justifiable sequence.

DSR is well matched to the present work for two reasons. First, the central contribution is an artefact: a design artefact for extending non-predictive agentic decision-support systems with forecast-informed capabilities, together with the interface and integration-readiness design that the extension requires. Second, the intended contribution is not limited to that artefact but extends to design knowledge, a set of transferable principles about extending production-oriented agentic systems with a forecasting substrate, which is precisely the dual artefact-and-knowledge output that DSR is designed to produce. Framing the work as DSR also disciplines its evaluation: the artefact must be assessed against defined criteria in a relevant context, which here means evaluating the forecasting substrate, the tool interface, and the resulting decision-support outputs against the criteria developed in the preceding sections, informed by a real production-oriented empirical case.

The specific application of the DSR process to this thesis, namely the artefact definition, the evaluation design, and the validation against the empirical case, is detailed in the methodology (Chapter 3); this section establishes only the methodological paradigm and its fit to the research questions.

2.9 Chapter Summary and Transition to Methodology

The literature reviewed in this chapter establishes the components and the gap that motivate the thesis. The forecasting literature (Sections 2.1–2.2) supports a benchmark of lightweight, category-specialised models evaluated on accuracy, efficiency, and stability under a constrained memory budget. The decision-support literature (Section 2.3) establishes, on peer-reviewed evidence, that predictions create value when connected to downstream decisions, while showing that this connection has been studied chiefly as tight, optimization-level coupling. The agent, reliability, and production literatures (Sections 2.4–2.6) supply the mechanism of tool-mediated reasoning, the reliability, traceability, and evaluation requirements that govern agentic outputs, and the operational capabilities a production-oriented system must possess to integrate them. Section 2.7 identifies the under-addressed intersection, a loose, agent-mediated, reliable and traceable extension of a non-predictive production-oriented agentic system with a forecasting substrate, and Section 2.8 frames the response as Design Science Research.

The next chapter operationalises this paradigm. It defines the artefact, the multi-category forecasting benchmark, the structured tool interface, the integration-readiness assessment, and the evaluation design that compares dedicated-model agentic decision-support against a code-as-action LLM baseline, together with the limitations that bound the resulting claims.

References cited in this chapter

Ahrens, A., Hansen, C. B., Schaffer, M. E., & Wiemann, T. (2025). Model averaging and double machine learning. Journal of Applied Econometrics, 40(3). https://doi.org/10.1002/jae.3103

Al-Karkhi, M. I., & Rządkowski, G. (2025). Innovative machine learning approaches for complexity in economic forecasting and SME growth: A comprehensive review. International Journal of Innovation Studies, 9(1), 20–28.

Barber, R. F., Candès, E. J., Ramdas, A., & Tibshirani, R. J. (2023). Conformal prediction beyond exchangeability. The Annals of Statistics, 51(2), 816–845. https://doi.org/10.1214/23-AOS2276

Ceran, B., Özkan, E., Eskiocak, D. İ., Mert, B., & Yüceoğlu, B. (2024). Machine learning-based demand forecasting for an FMCG retailer. In Intelligent and Fuzzy Systems: Proceedings of INFUS 2024 (LNNS, Vol. 1090). Springer. https://doi.org/10.1007/978-3-031-67192-0_11

Chen, E., & Bibi, Z. (2026). Machine learning as a tool (MLAT): A framework for integrating statistical ML models as callable tools within LLM agent workflows. arXiv preprint arXiv:2602.14295. [PREPRINT, not peer-reviewed]

Dong, L., Lu, Q., & Zhu, L. (2024). A taxonomy of AgentOps for enabling observability of foundation model based agents. arXiv preprint arXiv:2411.05285. [PREPRINT]

Elmachtoub, A. N., & Grigas, P. (2022). Smart “predict, then optimize”. Management Science, 68(1), 9–26. https://doi.org/10.1287/mnsc.2020.3922

González-Potes, A., Mata-Rivera, M. F., Espinosa-Oviedo, J. A., Castellanos-Velasco, E., Alvarado-Nava, O., & Rodríguez-Reséndiz, J. (2026). Hybrid AI and LLM-enabled agent-based real-time decision support architecture for industrial batch processes. AI, 7(2), 51.

Goodwin, P., Önkal, D., & Thomson, M. (2010). Do forecasts expressed as prediction intervals improve production planning decisions? European Journal of Operational Research, 205(1), 195–201. https://doi.org/10.1016/j.ejor.2009.12.020

Gu, J., Jiang, X., Shi, Z., Tan, H., Zhai, X., Xu, C., Li, W., Shen, Y., Ma, S., Liu, H., Wang, S., Zhang, K., Wang, Y., Gao, W., Ni, L., & Guo, J. (2025). A survey on LLM-as-a-judge. arXiv preprint arXiv:2411.15594. [PREPRINT]

Guo, Z., et al. (2025). Sample, predict, then proceed: Self-verification sampling for tool use of LLMs. OpenReview. [PREPRINT]

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. MIS Quarterly, 28(1), 75–105. https://doi.org/10.2307/25148625

Ji, Z., Gu, Y., Zhang, W., Lyu, C., Lin, D., & Chen, K. (2024). ANAH: Analytical annotation of hallucinations in large language models. In Proceedings of ACL 2024 (pp. 8135–8158).

Kartik, N., Sapra, G., Hada, R., & Pareek, N. (2025). AgentCompass: Towards reliable evaluation of agentic workflows in production. arXiv preprint arXiv:2509.14647. [PREPRINT]

Klee, S., & Xia, Y. (2025). Measuring time series forecast stability for demand planning. KDD ’25 Workshop on AI for Supply Chain. [PREPRINT]

Kuleshov, V., Fenner, N., & Ermon, S. (2018). Accurate uncertainties for deep learning using calibrated regression. In Proceedings of ICML 2018 (PMLR, Vol. 80).

Lei, J., G’Sell, M., Rinaldo, A., Tibshirani, R. J., & Wasserman, L. (2018). Distribution-free predictive inference for regression. Journal of the American Statistical Association, 113(523), 1094–1111. https://doi.org/10.1080/01621459.2017.1307116

Levi, D., Gispan, L., Giladi, N., & Fetaya, E. (2022). Evaluating and calibrating uncertainty prediction in regression tasks. Sensors, 22(15), Article 5540. https://doi.org/10.3390/s22155540

Li, Z., et al. (2024). AutoFlow: Automated workflow generation for large language model agents. arXiv preprint arXiv:2407.12821. [PREPRINT]

Liu, S., Guo, B., Yu, Z., et al. (2025). On accelerating edge AI: Optimizing resource-constrained environments. arXiv preprint arXiv:2501.15014. [PREPRINT]

Liu, Z., et al. (2024). A dynamic LLM-powered agent network for task-oriented agent collaboration. In First Conference on Language Modeling (CoLM 2024).

Ma, B. J., Jackson, I., Huang, M., Villegas, S., & Macias-Aguayo, J. (2025). A data-driven and context-aware approach for demand forecasting in the beverage industry. International Journal of Logistics Research and Applications. https://doi.org/10.1080/13675567.2025.2451806

Ma, M., et al. (2024). SciAgent: Tool-augmented language models for scientific reasoning. arXiv preprint arXiv:2402.11451. [PREPRINT]

Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2020). The M4 competition: 100,000 time series and 61 forecasting methods. International Journal of Forecasting, 36(1), 54–74.

Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. International Journal of Forecasting, 38(4), 1346–1364.

Mandi, J., Kotary, J., Berden, S., Mulamba, M., Bucarey, V., Guns, T., & Fioretto, F. (2024). Decision-focused learning: Foundations, state of the art, benchmark and future opportunities. Journal of Artificial Intelligence Research, 81, 1623–1701. https://doi.org/10.1613/jair.1.15320

Mehta, S. (2025). Beyond accuracy: A multi-dimensional framework for evaluating enterprise agentic AI systems. arXiv preprint arXiv:2511.14136. [PREPRINT]

Ng, S. (2017). Opportunities and challenges: Lessons from analyzing terabytes of scanner data (Working Paper No. 23673). National Bureau of Economic Research. https://doi.org/10.3386/w23673

Olszak, C. M., & Bartuś, K. (2025). AI-enhanced business intelligence for decision-making. Procedia Computer Science, 270, 415–425. https://doi.org/10.1016/j.procs.2025.09.160

Paranjape, B., Lundberg, S., Singh, S., Hajishirzi, H., Zettlemoyer, L., & Ribeiro, M. T. (2023). ART: Automatic multi-step reasoning and tool-use for large language models. arXiv preprint arXiv:2303.09014. [PREPRINT]

Pathirannehelage, S. H., Shrestha, Y. R., & von Krogh, G. (2025). Design principles for artificial intelligence-augmented decision making: An action design research study. European Journal of Information Systems, 34(2), 207–229. https://doi.org/10.1080/0960085X.2024.2330402

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. Journal of Management Information Systems, 24(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302

Rinaldi, G., Giordano, F., De Stefano, C., & Fontanella, F. (2025). DSS4EX: A decision support system framework to explore artificial intelligence pipelines with an application in time series forecasting. Expert Systems With Applications, 269, 126421.

Sapkota, R., Roumeliotis, K. I., & Karkee, M. (2026). AI agents vs. agentic AI: A conceptual taxonomy, applications and challenges. Information Fusion, 126, Article 103599. https://doi.org/10.1016/j.inffus.2025.103599

Saunders, M. N. K., Lewis, P., & Thornhill, A. (2023). Research Methods for Business Students (9th ed.). Harlow: Pearson.

Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. In Advances in Neural Information Processing Systems 36 (NeurIPS 2023).

Semerikov, S. O., Vakaliuk, T. A., Kanevska, O. B., Ostroushko, O. A., & Kolhatin, A. O. (2025). Edge intelligence unleashed: A survey on deploying large language models in resource-constrained environments. Journal of Edge Computing, 4(2). https://doi.org/10.55056/jec.1000

Wang, R., Chen, Y., Wang, Y., Wu, C., Fang, J., Cai, X., Gu, Q., Su, H., Zhang, A., Wang, X., Cai, X., & Chua, T.-S. (2026). AgentNoiseBench: Benchmarking robustness of tool-using LLM agents under noisy conditions. arXiv preprint arXiv:2602.11348. [PREPRINT]

Wang, X., Chen, Y., Yuan, L., Zhang, Y., Li, Y., Ji, H., & Tong, H. (2024). Executable code actions elicit better LLM agents. In Proceedings of ICML 2024.

Wang, Y., et al. (2025). ScoreFlow: Mastering LLM agent workflows via score-based preference optimization. arXiv preprint arXiv:2502.04306. [PREPRINT]

Ye, J., Wang, Y., Huang, Y., Chen, D., Zhang, Q., Moniz, N., Gao, T., Geyer, W., Huang, C., Chen, P.-Y., Chawla, N. V., & Zhang, X. (2024). Justice or prejudice? Quantifying biases in LLM-as-a-judge. arXiv preprint arXiv:2410.02736. [PREPRINT, peer-review status uncertain, verify]

Zheng, G., Almahri, S., Xu, L., Minaricova, M., & Brintrup, A. (2025). LLMs in supply chain management: Opportunities and a case study. IFAC-PapersOnLine, 59(10), 2951–2956. https://doi.org/10.1016/j.ifacol.2025.09.496

Chapter 3 - Methodology

3.1 Philosophy of Science

This thesis adopts a pragmatist philosophy of science, a position that evaluates knowledge claims by their practical consequences and their capacity to generate useful solutions to real-world problems. Pragmatism holds that there is no single, context-independent criterion of truth, and that the adequacy of a theory or framework is properly judged by how well it enables action in the domain it is intended to address. This stance is particularly well-suited to design-oriented research, in which the primary output is an artefact, specifically a lightweight forecasting substrate exposed to a bounded tool-using agentic decision-support layer through a structured forecast-tool interface, rather than a universal explanatory theory. For this thesis, the pragmatist criterion for success is not whether the artefact reveals deep structural features of retail demand, but whether it enables Manifold AI and similar organisations to extend a production-oriented agentic system that lacks native predictive capability with reliable, computationally feasible, and actionable forecast-informed decision-support that improves on the non-predictive descriptive systems currently in use.

Consistent with this pragmatist orientation, the thesis adopts a modest realism about the business realities it studies: demand patterns, consumer preferences, and retailer-level sales dynamics are taken to exist independently of the researcher, yet are known only through measurement instruments that carry their own assumptions and limitations, and they matter here for their practical consequences rather than as objects of deep structural explanation. The Nielsen scanner panel captures sales volumes and market shares through a structured data collection process that reflects retailer reporting conventions and panel design choices. The scanner panel provides meaningful, reproducible, and workable representations rather than direct, theory-free access to reality. This stance has practical methodological implications: it motivates careful data quality assessment, explicit documentation of measurement assumptions, and conservative interpretation of findings as context-bounded rather than universal.

The epistemological stance is empirical: knowledge claims in this thesis are grounded in data and in the outcomes of controlled evaluations rather than in pure theoretical deduction. The primary epistemic mechanism is prediction and comparison: the thesis generates quantitative forecasts, measures their accuracy against observed outcomes, and compares system performance against a defined baseline. This empirical orientation contrasts with a purely positivist epistemology in two respects. First, the thesis does not claim to discover universal forecasting laws applicable across all contexts; findings are explicitly bounded to the Danish beverage retail market, the eight-gigabyte RAM constraint, and the batch processing mode described in Chapter 4. Second, the thesis does not aspire to purely objective, theory-free observation; the choice of evaluation metrics, the definition of the baseline, and the design of the evaluation protocol all embed theoretical commitments that are made explicit rather than concealed. The empirical stance equally contrasts with interpretivism: quantitative accuracy metrics and reproducible experimental protocols are the primary evidence, and the thesis does not seek to interpret the subjective meaning that decision-makers attach to forecasts.

The alignment between this pragmatist philosophy and Design Science Research reflects its internal logic as an established methodology for information systems and technology research. DSR produces knowledge through the construction and evaluation of artefacts, and judges that knowledge by whether the artefact achieves its design objectives in the target environment. This is precisely the pragmatist criterion: knowledge is what works. The consistency between the philosophical position and the research methodology is not incidental; it reflects the deliberate choice to adopt a methodology whose epistemological foundations are compatible with the pragmatist orientation of the research.

3.2 Research Design: Design Science Research

This thesis adopts Design Science Research (DSR) as its primary research methodology. DSR is the established framework for information systems research that involves the construction of novel artefacts, whether systems, methods, models, or frameworks, and the systematic evaluation of those artefacts against defined performance criteria in a relevant application domain (Hevner et al., 2004). DSR is distinguished from purely behavioural IS research by its dual emphasis on both the construction of a working artefact and the generation of transferable design knowledge that extends beyond the specific instantiation. In the context of this thesis, the artefact is the predictive extension, namely a lightweight forecasting substrate exposed to a bounded tool-using agentic decision-support layer through a structured forecast-tool interface, and the design knowledge takes the form of generalised design principles derived from the evaluation of that extension.

Hevner et al. (2004) establish three foundational cycles of DSR activity: the relevance cycle, which connects the research to a real-world problem in a specific application domain; the design cycle, which iterates between construction and evaluation of the artefact; and the rigor cycle, which grounds the design in existing knowledge bases, specifically the academic literature reviewed in Chapter 2. This thesis explicitly engages all three cycles. The relevance cycle is established through the collaboration with Manifold AI, whose operational need to extend a non-predictive, production-oriented agentic system with forecast-informed decision-support defines the problem that the artefact addresses. The design cycle is enacted through the iterative development, testing, and refinement of the predictive-extension architecture across Chapters 5 through 8. The rigor cycle is enacted through the systematic literature review in Chapter 2, which identifies the theoretical and empirical foundations on which the framework design is built.

Peffers et al. (2007) provide a process model for DSR comprising six sequential activities that structure the research design of this thesis. Problem identification and motivation, the first activity, is addressed in Chapters 1 and 2, where the limits of descriptive analytics in resource-constrained SME environments are documented and the gap in the existing literature is established. The definition of objectives for a solution, the second activity, is formalised through the four subsidiary research questions that specify the design requirements for the framework. Design and development, the third activity, constitutes the core contribution of Chapters 5 and 6, where the predictive-extension architecture is specified and the forecasting models are implemented and profiled. Demonstration, the fourth activity, is achieved in Chapter 7, where the bounded tool-using agentic decision-support layer is applied to real Nielsen scanner data to generate forecast-informed recommendations. Evaluation, the fifth activity, is conducted in Chapter 8, where the artefact’s performance is assessed against accuracy, computational efficiency, recommendation quality, and comparison with a code-as-action LLM baseline at pilot scale. Communication, the sixth activity, is realised through this thesis and its associated artefact documentation.

The research design type within the CBS taxonomy is explanatory: the thesis is not merely describing what the framework does, but explaining how and why specific architectural choices, specifically sequential model execution, the structured forecast-tool interface, and the bounded tool-using agentic layer, produce better forecast-informed decision-support outcomes than a general-purpose code-as-action LLM baseline that writes and self-corrects its own forecasting code. This explanatory orientation is manifest in the evaluation design, which is structured to isolate the contribution of individual components through controlled comparisons rather than reporting aggregate performance alone. The prototype status of the artefact is explicitly acknowledged: the artefact is a research prototype to be evaluated on historical data under controlled conditions, and is not claimed to be a production-ready deployed system.

3.3 Research Strategy

The primary research strategy is a quantitative experiment combined with a single-case embedded study. The experimental component provides the controlled evaluations that address SRQ1 and SRQ4: in SRQ1, the set of forecasting models (and the choice between category-specialised and pooled estimation) is systematically varied while all other conditions are held constant; in SRQ4, the decision-support pipeline is varied between dedicated-model integration (the thesis artefact) and a code-as-action baseline in which a general-purpose LLM writes, executes, and self-corrects its own forecasting code in a sandboxed environment, with the task and prompt set held constant across the two. This controlled variation enables attribution of performance differences to the manipulated variable rather than to confounding factors, providing the internal validity required to answer the research questions with appropriate confidence.

The single-case embedded study component provides the organisational context that grounds the experimental findings in a real application environment. Manifold AI serves as the case organisation, its production-oriented agentic system (Prometheus) serves as the empirical case for the integration-readiness assessment in SRQ3, and the Danish beverage retail market across the five Nielsen categories constitutes the empirical context. The case study orientation means that all experimental data, evaluation protocols, and baseline comparisons are anchored in the actual data and operational context of the case rather than in synthetic benchmarks. This design choice reflects the DSR relevance criterion: the artefact must be evaluated in a context that is relevant to the problem it addresses. The CBS case study guidelines apply to this research, and the Nielsen data are used under a confidentiality agreement with Manifold AI, as documented in Chapter 4.

The unit of analysis is the predictive-extension artefact, evaluated on the Nielsen dataset across the five Danish beverage categories at brand-times-retailer granularity. The granularity choice, specifically brand-level data aggregated across retailer-week combinations and collapsed to monthly periods, reflects the operational planning horizon relevant to Manifold AI’s client organisations and is consistent with the temporal resolution of the Nielsen panel. The default market definition, DVH EXCL. HD, is adopted in alignment with the market segmentation conventions used by Manifold AI. These choices are documented here as locked design decisions to ensure reproducibility and to prevent retroactive revision based on observed model performance.

3.4 Data Sources

This thesis uses one data source: the Nielsen/Prometheus beverage scanner panel, the core forecasting input across all five categories.

The Nielsen/Prometheus dataset provides longitudinal retail transaction data for five Danish beverage categories: carbonated soft drinks (CSD), still and sparkling water (danskvand), energy drinks (energidrikke), ready-to-drink beverages (RTD), and beer (totalbeer). Its structure follows a star schema, with a facts table recording sales value, sales in litres, sales units, and weighted distribution at the brand-times-retailer-times-period level, linked to dimension tables for market, period, and product. The panel provides between 37 and 42 monthly periods per category (CSD being the longest, October 2022 to March 2026), giving a transaction history of roughly three to three-and-a-half years. The sales metrics include both base and promotional variants, enabling the identification of promotional uplifts as a feature engineering input. The weighted distribution metric provides a proxy for product availability, which is a meaningful predictor of sales volume for categories with intermittent distribution. The Nielsen dataset is used under a confidentiality agreement with Manifold AI.

3.5 Analytical Approach

The analytical approach addresses each of the four subsidiary research questions through a distinct evaluation protocol, because the thesis evaluates not only forecasting accuracy but also interface design, integration readiness, and decision-support output quality, and these dimensions require different evidence types and evaluation instruments.

SRQ1 - forecasting accuracy and computational efficiency. Five forecasting models are evaluated across the five Nielsen beverage categories: ARIMA, Prophet, LightGBM, XGBoost, and Ridge Regression. These models were selected to span the accuracy-efficiency frontier: ARIMA and Ridge Regression provide interpretable statistical and linear baselines with well-understood memory footprints; Prophet provides an additive decomposition approach with explicit seasonality handling; and LightGBM and XGBoost represent the gradient-boosted ensemble methods that have demonstrated state-of-the-art performance in the M5 retail forecasting benchmark (Makridakis et al., 2022). Hyperparameters for the gradient-boosted models are tuned with Optuna. All models are evaluated on a common held-out test set using mean absolute percentage error (MAPE) and root mean squared error (RMSE) as accuracy metrics, peak RAM consumption and runtime as efficiency metrics, and coefficient of variation across repeated runs as a stability metric, following the methodology proposed by Klee and Xia (2025). The benchmark additionally tests whether category-specialised models outperform a single pooled model trained across categories. Memory profiling is conducted by measuring process resident set size (RSS) via the Python psutil/resource interfaces rather than tracemalloc alone, because tracemalloc does not capture the native (non-Python) allocations of XGBoost and LightGBM; the RSS measurements are reported in Chapter 6.

SRQ2 - structured forecast-tool interface. SRQ2 concerns how forecasting outputs are exposed to the agentic decision-support layer in a way that preserves reliability, uncertainty, and traceability. The interface is realised as a JSON-based function-calling contract with strict output schemas: the agentic layer invokes the forecasting substrate as a tool, receives point forecasts accompanied by interval information (prediction intervals following Kuleshov et al. (2018); interval calibration is a design target, not an empirically validated property of the current prototype), and where multiple models are combined the substrate aggregates them using inverse-MAPE weighting in the spirit of Ahrens et al. (2024). Reliability is preserved by validating the agent’s stated numbers against the source forecasts; traceability is preserved by recording the mapping from tool call and forecast value to the resulting recommendation. The prototype is orchestrated by a lightweight Python coordinator that passes typed state between components; LangGraph is the intended production substrate (the Prometheus production system, whose Graph Engine is the concrete integration target examined under SRQ3), not the evaluated implementation. The lightweight orchestration is chosen deliberately against the 8GB RAM constraint, and the JSON function-calling action format is chosen for the thesis artefact’s reliability and reproducibility; the code-as-action action format is instead employed in the SRQ4 baseline described below.

SRQ3 - integration readiness. SRQ3 concerns the architectural and operational capabilities a production-oriented agentic system must possess to integrate forecast-informed decision-support: a structured tool interface for invoking external predictive models, observability and traceability of tool calls, explicit handling of reliability and uncertainty, and operation within bounded cost, latency, and memory. These capabilities are assessed against a real production-oriented agentic system (Prometheus, whose Graph Engine is the concrete integration interface) as the empirical case, rather than through a completed production deployment; the assessment is a capability-readiness analysis, not a live integration experiment.

SRQ4 - dedicated-model integration versus a code-as-action LLM. SRQ4 concerns whether integrating dedicated lightweight forecasting models into the agentic system is warranted at all, or whether a general-purpose LLM that writes, executes, and self-corrects its own forecasting code (a code-as-action baseline) is already sufficient. The two pipelines are run on a common set of approximately fifty decision-support prompts, holding the task and inputs constant; the code-as-action baseline executes LLM-generated code in a sandboxed environment (for example E2B), which is runnable locally and does not require access to the production system. Outputs are scored on correctness, consistency, and replicability as primary dimensions and on cost and latency as secondary dimensions. Consistency is measured over repeated runs because LLM-generated code varies substantially across identical requests, even at nominally deterministic settings (Ouyang et al., 2025; Atıl et al., 2025); cost and latency are treated as evaluation dimensions in their own right, following the argument that computational cost belongs among a system’s first-class evaluation criteria (Schwartz et al., 2020) and the evidence that inference cost differs by orders of magnitude across models of comparable quality (Chen et al., 2024); the overall multidimensional frame follows Mehta (2025). Scoring uses an LLM-as-judge protocol with a separate judge model, explicit bias awareness, and a human-rated subset for validation. This evaluation is conducted at pilot scale in the first instance rather than as a full study; a full evaluation across the complete prompt set, and an optional comparison against the non-predictive production reference system, are identified as further work.

3.6 Validity and Reliability

Internal validity is maintained through three design choices. First, a common train-test split is applied identically across all five forecasting models, ensuring that performance differences reflect model characteristics rather than differences in the data each model observes. Second, all models are initialised with fixed random seeds and all preprocessing steps are fully documented, enabling exact reproduction of any result. Third, the controlled comparison used for SRQ4, in which the decision-support pipeline (dedicated-model integration versus the code-as-action baseline) is the sole manipulation while the prompt set and inputs remain constant, isolates the contribution of dedicated-model integration from potential confounders.

External validity is explicitly bounded. The findings of this thesis are applicable to the Danish beverage retail market (the five Nielsen categories) under an eight-gigabyte RAM cloud deployment constraint and a monthly batch processing mode. Generalisation to other FMCG categories, other national markets, other RAM budgets, or real-time streaming contexts is a direction for future research rather than a claim of this thesis. The single-case embedded study design strengthens relevance to the Manifold AI operational context but limits statistical generalisation to other case organisations.

Construct validity is addressed by operationalising each research question in the measurement protocols specified in Section 3.5: accuracy, memory, runtime, and stability metrics together with the specialised-versus-pooled comparison for SRQ1; the reliability, uncertainty, and traceability properties of the structured forecast-tool interface for SRQ2; the capability-readiness assessment for SRQ3; and the correctness, consistency, replicability, cost, and latency dimensions, scored via an LLM-as-judge protocol with a human-rated subset, for SRQ4. Each operationalisation is pre-specified before data analysis begins to prevent post-hoc metric selection bias.

Reliability is ensured through code versioning, documentation of all hyperparameters and preprocessing decisions, and fixed random seeds throughout. Any deviation from the documented protocol is recorded as a limitation. The LLM-as-judge evaluation introduces a source of non-determinism: LLM outputs at temperature zero are highly reproducible but not guaranteed to be identical across API versions. To mitigate this, all LLM evaluation calls are logged with their exact prompt and output, enabling retrospective auditing.

3.7 Limitations

The methodology described in this chapter is subject to five limitations that bound the scope and generalisability of the findings.

Data confidentiality. The Nielsen/Prometheus dataset is used under a confidentiality agreement with Manifold AI. The raw scanner data cannot be redistributed, which constrains full external reproducibility to the processed features, code, and documented protocol rather than the underlying transaction records.

Training sample size. Between 37 and 42 monthly periods per category is at the lower boundary for reliable time series model estimation. ARIMA models generally require a minimum of 24 periods for stable parameter identification; this window satisfies that requirement but provides limited statistical power for detecting seasonal patterns spanning multiple years. LightGBM and XGBoost are less sensitive to sample size constraints than classical time series models, but the restricted training window limits their ability to learn longer-cycle promotional patterns. This limitation is partially mitigated by the feature engineering approach, which incorporates lagged variables and rolling statistics that increase the effective information content per observation.

Pilot-scale evaluation of decision-support outputs. The SRQ4 comparison of dedicated-model integration against the code-as-action LLM baseline is conducted at pilot scale (on the order of fifty prompts) in the first instance rather than as a full study. Findings on correctness, consistency, replicability, cost, and latency are therefore indicative rather than conclusive; a full evaluation across the complete prompt set, and an optional comparison against the non-predictive production reference system, are identified as further work in Chapter 10.

Sequential model execution constraint. The eight-gigabyte RAM budget requires models to be executed sequentially rather than in parallel, increasing total pipeline runtime relative to a compute-unconstrained deployment. In a production setting, this latency may be acceptable for monthly batch processing but would be prohibitive for higher-frequency planning cycles. The sequential execution design is a binding architectural constraint of the thesis artefact that would need to be re-evaluated for any real-time or sub-monthly deployment.

Case study generalisability. The single-case embedded study design provides strong internal relevance to the Manifold AI operational context but limits statistical generalisation to other retail AI providers, other product categories, and other national markets. The design principles derived from the evaluation are intended to be theoretically transferable through the DSR generalisation mechanism, but their applicability to contexts with different data characteristics, regulatory environments, or competitive dynamics requires empirical validation in those contexts.

References cited in this chapter

Ahrens, A., Hansen, C. B., Schaffer, M. E., & Wiemann, T. (2024). Model averaging and double machine learning. Journal of Applied Econometrics. https://doi.org/10.48550/arXiv.2401.01645

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. MIS Quarterly, 28(1), 75–105.

Klee, S., & Xia, Y. (2025). Measuring time series forecast stability for demand planning. KDD ’25 Workshop on AI for Supply Chain.

Kuleshov, V., Fenner, N., & Ermon, S. (2018). Accurate uncertainties for deep learning using calibrated regression. In Proceedings of ICML 2018 (PMLR, Vol. 80).

Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. International Journal of Forecasting, 38(4), 1346–1364.

Mehta, S. (2025). Beyond accuracy: A multi-dimensional framework for evaluating enterprise agentic AI systems. arXiv preprint arXiv:2511.14136. [PREPRINT, not peer-reviewed]

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. Journal of Management Information Systems, 24(3), 45–77.

Chapter 4 - Data Assessment

4.1 Overview and Data Strategy

This thesis draws on one secondary data source in the sense of Saunders et al. (2023): data originally collected by others for another purpose and reanalysed here. The Nielsen/Prometheus beverage scanner panel is the forecasting input, covering four Danish beverage categories: carbonated soft drinks (CSD), still and sparkling water (danskvand), energy drinks (energidrikke), and ready-to-drink beverages (RTD). A fifth category, beer (totalbeer), was scoped out because its facts table is absent from the source data (the data do not exist at source, not a size or memory constraint); this is recorded as a data limitation rather than an analytical choice. CSD is the worked category, assessed in full (Section 4.3); the other three are processed through the identical pipeline as parallel proofs of concept.

It is survey-type, structured, commercial secondary data. Consistent with the pragmatist stance of Chapter 3, it is treated as a partial but workable representation of demand realities, shaped by the collecting instrument, rather than as a theory-free objective record.

This chapter assesses the data following the three-stage secondary-data evaluation of Saunders et al. (2023): (i) overall suitability (measurement validity and coverage), (ii) precise suitability (reliability/dependability, validity/credibility, and measurement bias/trustworthiness), and (iii) costs, benefits, and ethics. The assessment is conducted per category, since the four categories differ systematically in scale and promotional structure. The train, validation, and test split is then specified as a locked, pre-registered design decision applied identically across the forecasting models (Chapter 6), and the key data risks are documented to bound the empirical claims of the later chapters.

4.2 The Nielsen Scanner Panel (core forecasting input)

4.2.1 Source, Type, and Access

The Nielsen/Prometheus dataset is provided by Manifold AI through its Prometheus reporting platform. In Saunders et al.’s (2023) taxonomy it is survey secondary data (a continuously maintained commercial scanner panel), structured (organised in a star schema), and quantitative. It is used under a confidentiality agreement with Manifold AI: the raw data are not redistributed and do not leave the local research environment. Because access is commercial and restricted, the data could not have been collected independently within the scope of a thesis, which is itself a Saunders-listed advantage of using secondary data.

The four categories are each scoped by Manifold AI from the broader Prometheus platform. The exact extraction interface used by the pipeline is documented in Chapter 5; this chapter concerns the data themselves.

4.2.2 Schema and Structure

Each category follows a star schema: dimension tables for market, period, and product, linked to a facts table at the grain of market × product × period. The facts table records the core sales metrics (sales value, sales in litres, sales units), their promotional variants (the same metrics under promotion), and a weighted-distribution metric that proxies product availability. The product dimension captures brand, manufacturer, packaging format, flavour or type, price tier, and corporate attribution.

A technical note carried over from the prior pipeline and to be re-verified in the rebuild: period identifiers are not necessarily monotonic with calendar time, so all time-series operations sort by the composite key (period_year, period_month). The facts table may also contain more distinct products than the active product dimension (discontinued or out-of-scope SKUs), so the join to the product dimension is the correct scoping mechanism.

Per-category structural counts (periods, brands, products/SKUs, brand-month rows, in-scope fact rows) are reported in Table 4.1, all computed locally under the DVH EXCL. HD scope.

Category

Periods (max)

Brands (in scope)

retained ≥40

retained ≥30

Catalog SKUs

In-scope SKUs

Brand-month rows

In-scope fact rows

CSD

42

136

57

77

8,608

7,668

3,789

187,907

danskvand

37

49

0 ⚠️

24

565

453

1,090

24,796

energidrikke

39

64

0 ⚠️

27

747

577

1,520

49,345

RTD

37

93

0 ⚠️

42

589

511

2,193

44,449

Table 4.1. Per-category structure, all four categories computed locally under the DVH EXCL. HD scope (2026-06-27). CSD figures supersede Brian’s all-markets values, inflated 6.16× by summing hierarchical markets; the CSD catalog-SKU count (8,608 distinct product_id in the product dimension) likewise supersedes the earlier 2,080. Column definitions: Catalog SKUs = distinct product_id in dim_product; In-scope SKUs = distinct product_id with positive sales at the DVH EXCL. HD scope; Brand-month rows = positive-sales brand × month observations across all in-scope brands (the retained ≥30 subset yields 3,077 / 885 / 1,007 / 1,543 observed rows respectively, per regeneration_report.md). MIN_PERIODS feasibility: danskvand, energidrikke, and RTD have only 37–39 monthly periods, so a ≥40-observation filter retains zero brands for them; a single global threshold of ≥30 is therefore adopted across all categories (CSD 77, danskvand 24, energidrikke 27, RTD 42 brands), which is both feasible and consistent - preferable to the inherited mixed rule (40 for CSD, 30 for the rest). The bold column (≥30) is the retained set used downstream.

4.2.3 Overall Suitability

Measurement validity / appropriateness. The recorded metrics must measure the forecasting target. Sales units (and, where appropriate, litres) are the demand quantities to be forecast; the promotional variants and the weighted-distribution proxy serve as exogenous predictors. The weighted-distribution metric is an availability proxy rather than a direct census of shelf presence, and this proxy status is acknowledged in interpretation. Market scope (resolved). The primary market is DVH EXCL. HD (Danish grocery retail excluding hard discount), Nielsen’s recommended default and the scope on which Manifold AI reports. This choice is not cosmetic: the 28 CSD market values form a hierarchy (individual chains nested within group aggregates such as COOP and SALLING GROUP, nested within grand-total roll-ups such as DVH/CONVENIENCE INCL. HD). A local check confirmed that aggregating sales across all 28 - as the inherited pipeline did - counts the same sales at multiple levels and inflates CSD volume by 6.16× (168.6B units summed across all 28 levels vs 27.4B units at the single DVH EXCL. HD level, a legitimate grand-total comparable to DVH/CONVENIENCE INCL. HD at 32.2B; all figures de-duplicated on the slowly-changing market dimension before aggregation). Scoping to the single DVH EXCL. HD market level eliminates this by construction (one market identifier, no cross-market summation) and yields a clean branded-demand signal excluding the structurally different hard-discount channel.

Coverage. The panel must cover the right population and period and leave sufficient data after exclusions. All four categories are scoped to the single DVH EXCL. HD market level (one market identifier per category, by design), so coverage is assessed on the temporal span, the brand and SKU counts, and the retained series. The temporal span is 37–42 months (CSD 42, energidrikke 39, danskvand and RTD 37), with complete intermediate calendar years constituting the primary training window. In-scope brand counts are 136 (CSD), 49 (danskvand), 64 (energidrikke), and 93 (RTD); in-scope SKU counts are 7,668, 453, 577, and 511 respectively (Table 4.1). After the ≥30-month retention filter, 77 / 24 / 27 / 42 brands remain for benchmarking, with 3,077 / 885 / 1,007 / 1,543 observed brand-month rows. A category-specific coverage caveat applies to promotional coverage: for danskvand and RTD the promotional variables are effectively absent (promo-zero), so the promotional features are unmeasured for those categories, an unmeasured-variable limitation in Saunders’ terms, carried forward to the modelling and discussion.

4.2.4 Precise Suitability

Reliability / dependability. Nielsen is an established commercial panel provider whose continued operation depends on data credibility; its scanner data are therefore treated as reliable, while recognising that, as with any provider, definitions and collection conventions are fixed by Nielsen rather than by the researcher.

Validity / credibility. Credibility rests on how the data were collected and compiled (scanner capture aggregated to the market × product × period grain). Definitions (market aggregates such as DVH EXCL. HD, metric definitions, corporate attribution) are provider-set and are documented rather than altered.

Measurement bias / trustworthiness. Three data patterns require explicit treatment; per-category figures, computed locally on the in-scope facts, are reported below: - Promotional values: where the promotional metric exists (CSD and energidrikke) it is fully populated (0.00% null), with the absence of promotional activity encoded as a zero rather than a null; for danskvand and RTD the promotional column is absent entirely, collapsing to the promo-zero case above. - Weighted-distribution nulls: negligible across all categories - 0.019% (CSD), 0.016% (danskvand), 0.093% (energidrikke), 0.000% (RTD). These reflect products Nielsen does not track for distribution in a given period; they are imputed using a brand-and-market median, which preserves central tendency but ignores within-period time variation (a moderate limitation for niche brands, immaterial at these null rates). - Negative and zero values: negatives are return/correction adjustments standard in scanner data and are clipped to zero - they are rare (CSD 58 rows, 0.031%; danskvand 14, 0.057%; energidrikke 16, 0.032%; RTD 10, 0.022%). True zero-sales rows are likewise rare (CSD 12, danskvand 1, energidrikke 28, RTD 17) and are retained and flagged as genuine zeros, distinct from corrections. Core sales metrics are complete: sales_units has 0.00% nulls in every category, confirmed locally.

4.2.5 Forecasting Suitability

The panel must support the forecasting models. The 37–42-month span exceeds the ARIMA minimum of roughly 24 periods for stable parameter identification and contains enough annual cycles for seasonality to be learned by both decomposition and gradient-boosted models. Benchmarking (Chapter 6) is conducted on the brand series retained by the ≥30-month filter (77 / 24 / 27 / 42 brands for CSD / danskvand / energidrikke / RTD), so that model comparisons are not confounded by very short series; missing months within a retained series are exposed on the regular monthly grid and handled natively by the models rather than imputed. A stricter, fully observed subset (brands present in every period) comprises 57 / 22 / 18 / 37 brands respectively. Applicability to shorter or intermittent series is a bound on external validity, not a claim of this thesis.

4.3 CSD - Worked Category (EDA and Parameters)

CSD is the worked category. The structural counts and the stationarity, seasonality, and autocorrelation statistics below are recomputed locally under the DVH EXCL. HD scope (2026-06-23); the few items still taken from Brian’s all-markets audit are flagged. The other three categories are processed through the identical pipeline; per-category EDA replication under the corrected scope is pending (Section 4.6).

4.3.1 Scope and Filtering

Market scope: DVH EXCL. HD (single Nielsen market level; see header). 187,907 facts rows fall in scope.

Span: 42 monthly periods (Oct 2022–Mar 2026) on Nielsen’s 4-4-5 week calendar. (Period identifiers are not calendar-monotonic, so the span is taken from the documented window, not raw min/max.)

Brands: 136 total; the adopted filter MIN_PERIODS ≥ 30 (≥30 non-zero monthly observations) retains 77 brands and 3,077 brand-month rows (of 3,789 total). A ≥40 filter would retain only 57 and is infeasible for the other three categories (37–39 periods → zero brands), so ≥30 is applied globally (Table 4.1). These figures are recomputed locally under DVH EXCL. HD and supersede Brian’s all-markets values (143 → 62 brands; 4,040 rows), inflated by the market double-count.

Aggregation grain: brand × month, positive sales only; weighted distribution averaged rather than summed (correct for an ACV metric).

4.3.2 Stationarity

ADF test (aggregate monthly total, n = 42, DVH EXCL. HD): the level series is non-stationary in both raw (p = 0.360) and log form (p = 0.421); it becomes stationary only after first differencing (p < 0.001) - i.e. the series is difference-stationary, I(1). This revises Brian’s all-markets finding that the log level was stationary (p = 0.028): that does not hold at the corrected scope. (ADF power is limited at n = 42.)

Treatment: a natural-log transform is applied to sales_units to stabilise variance; non-stationarity in the mean is handled by differencing for ARIMA and by lagged/rolling features for the tree models (which do not require a stationary level). NaN is preserved for non-positive/missing values rather than imputed.

4.3.3 Seasonality

Peak months (share of annual units, DVH EXCL. HD): December (12.8%), March (10.9%), June (8.9%); September is next at 8.5%.

Peak-month indicator: PEAK_MONTHS - months whose mean sales_units exceeds the category’s overall mean by more than 10%, measured per category. For CSD this gives {3, 6, 9, 12}.

Renamed from HOLIDAY_MONTHS (2026-08-18). No holiday calendar is an input to the pipeline, so the former name asserted a cause the computation never established. The evidence often contradicts it: CSD’s peaks are the quarter-end months, consistent with retail trade loading rather than holidays.

Now verified per category, resolving the open question: CSD {3, 6, 9, 12}; Danskvand {6, 7, 8, 9} (summer - bottled water); Energidrikke {3, 6, 9} (quarter-ends, no December peak); RTD {5, 6, 12}. Four distinct seasonal profiles, each commercially plausible for its category.

The earlier {3, 6, 12} came from a top-quartile rule on monthly totals, which is confounded by how many brands were active in a month. The current rule uses means, which is not - the panel is unbalanced by construction. September enters CSD’s set under the corrected rule.

4.3.4 Autocorrelation and Lag Structure

Lag set: LAGS = (1, 2, 3, 4, 8, 13) and ROLLING_WINDOWS = (4, 13) (4-month and ~annual cycles on the Nielsen calendar).

Autocorrelation (recomputed, DVH EXCL. HD): for the top brand by units (HARBOE, n = 42) the log-series ACF is +0.26 (lag 1), +0.47 (lag 3), and ≈0 (lag 13) - a strong quarterly (lag-3) signal but a weak annual (lag-13) one for this brand. Lag structure is clearly brand-dependent, so a single global lag set is a simplification; per-brand optimisation is out of scope. This revises Brian’s Coca-Cola example (lag-1 = −0.399), which was computed on the inflated all-markets series. Method note: the per-category figures in §4.3.6 (CSD lag-1 +0.78) use a pooled, brand-demeaned log series across all retained brands, whereas the HARBOE figures here are a single-brand series; the pooled estimate is larger because demeaning removes between-brand level differences and leaves the common short-horizon dynamics. Both are reported; the qualitative conclusion (positive short-horizon, near-zero annual carry) is robust to the method.

Promotional intensity: strongly correlated with sales units, confirmed under DVH EXCL. HD at r = 0.937 (n = 2,442 promo-bearing brand-month rows), closely matching Brian’s all-markets value (r = 0.941); the relationship is robust to market scope. For energidrikke the promotional signal is even stronger (r = 0.988); danskvand and RTD carry no promotional data (promo-zero).

4.3.5 Parameter Summary

Parameter

Value (CSD)

Basis

Status

MIN_PERIODS

30 (global)

feasibility (other cats have 37–39 periods) + quality

adopted

LAGS

1, 2, 3, 4, 8, 13

ACF/PACF inspection

empirical; needs prose justification

ROLLING_WINDOWS

4, 13

4-month + annual cycle

empirical

PEAK_MONTHS

per category: CSD 3,6,9,12; Danskvand 6,7,8,9; Energidrikke 3,6,9; RTD 5,6,12

mean monthly units >10% above the category mean

derived per category (renamed from HOLIDAY_MONTHS)

log transform

applied to sales_units

variance stabilisation; series is I(1), diff-stationary (ADF p<0.001)

confirmed

Train / Val / Test

24 / 6 / 12 months

forward-chaining (Section 4.5)

confirmed

These parameters are EDA-driven rather than theory-first; their academic justification is developed in the modelling chapter, and their empirical (not theoretical) origin is stated honestly as a limitation.

4.3.6 Per-category EDA - danskvand, energidrikke, RTD

The three proof-of-concept categories were taken through the identical pipeline and their EDA recomputed under the corrected DVH EXCL. HD scope, closing the gap previously flagged in §4.6.

Category

Promo correlation

Peak month

Top brand

ADF (log level)

Verdict

ACF lag1 / lag3

CSD

r = 0.937

December

HARBOE

p = 0.421

non-stationary, I(1)

+0.78 / +0.55

danskvand

none (promo-zero)

June

HARBOE

p = 0.998

non-stationary, I(1)

+0.55 / +0.25

energidrikke

r = 0.988

March

RED BULL

p = 0.901

non-stationary, I(1)

+0.71 / +0.39

RTD

none (promo-zero)

December

BREEZER

p = 0.000

stationary in level

+0.82 / +0.58

Three of the four category-level series are difference-stationary (I(1)); RTD is already stationary in log level. All show strong positive short-horizon autocorrelation (lag-1 +0.55…+0.82), supporting the shared lag/rolling feature set, with near-zero lag-13 carry. Seasonality is category-appropriate (water peaks in summer, the others in autumn/spring). danskvand and RTD carry no promotional signal - the unmeasured-variable limitation already noted. MIN_PERIODS and LAGS transfer reasonably across categories. PEAK_MONTHS does not and is no longer treated as a transferable default: it is derived per category, and the four profiles differ materially (water peaks in summer, Energidrikke has no December peak). Per-series lag structure is brand-dependent and not separately optimised (a stated scope bound).

4.4 Feature Engineering (forecasting substrate)

The forecasting substrate uses features derived from the Nielsen facts table at the brand × month granularity. The feature matrix contains 22 columns: 14 modelling features per observation, plus index/key columns, the target, the carried promo_units, and the split label (verified against the parquet, scripts/srq1_benchmark_tuned.py). These are the exogenous and autoregressive predictors referenced in Chapter 1.

Feature

Description

Models

lag_1, lag_2, lag_3, lag_4, lag_8, lag_13

Lagged sales_units (short, medium, seasonal)

LightGBM, XGBoost, Ridge

rolling_mean_4, rolling_std_4

4-month rolling mean and standard deviation

LightGBM, XGBoost, Ridge

rolling_mean_13

Trailing annual average

LightGBM, XGBoost, Ridge

month, quarter, peak_month

Calendar features (peak_month = month in the category’s derived PEAK_MONTHS)

LightGBM, XGBoost, Ridge

promo_intensity

Promotional share of units (clipped 0–1)

LightGBM, XGBoost, Ridge

weighted_distribution

Nielsen weighted-distribution availability proxy

LightGBM, XGBoost, Ridge

The 14 features comprise six lags, three rolling statistics, three calendar features, promo_intensity, and weighted_distribution. Two clarifications resolve earlier ambiguity: log_sales_units is the modelling target (the models predict log sales and exponentiate back), not an input feature - using it as a predictor would be trivial leakage; and weighted_distribution is the fourteenth input feature, while the raw promo_units column is carried through the matrix but is not itself a model input (only its derived promo_intensity is). Index/target/label columns carried alongside the features: brand, period_index, period_year, period_month, sales_units (raw target), log_sales_units (log target), promo_units, split. Lag and rolling features carry NaN for short history (expected); no imputation is done in preprocessing, so the tree models handle NaN natively and the linear model receives a zero-fill at fit time.

ARIMA and Prophet are fitted as univariate statistical baselines on the (log) sales series, not on the tabular feature matrix. The promotional feature is not informative for danskvand and RTD (promo-zero) and is handled accordingly for those categories.

4.5 Train, Validation, and Test Split

The split is defined by calendar date and locked as a pre-specified design decision, applied identically across the forecasting models and across categories. No random shuffling is applied: a strict temporal split preserves the autocorrelation structure and prevents leakage of future observations into training or validation.

Because the categories differ in length, the split is expressed as contiguous chronological blocks per category (training → validation → test), with the test window placed in the most recent months relevant to Manifold AI’s planning horizon and covering at least one autumn/winter promotional cycle. The training window is required to satisfy the ARIMA minimum (~24 periods) and to contain at least two seasonal cycles for Prophet.

The per-category boundaries, taken from the locked split files (<cat>_split_dates.json), are:

Category

Periods

Train

Validation

Test

Train window

Validation window

Test window

CSD

42

24

6

12

2022-10 → 2024-09

2024-10 → 2025-03

2025-04 → 2026-03

danskvand

37

23

6

8

2023-03 → 2025-01

2025-02 → 2025-07

2025-08 → 2026-03

energidrikke

39

25

6

8

2023-01 → 2025-01

2025-02 → 2025-07

2025-08 → 2026-03

RTD

37

23

6

8

2023-03 → 2025-01

2025-02 → 2025-07

2025-08 → 2026-03

Table 4.2. Forward-chaining train/validation/test boundaries per category (locked, pre-registered). CSD, the longest series, takes a 12-month test window covering a full annual cycle; the three shorter categories take an 8-month test window (a ≥40-month series would be needed for a 12-month test under the same rule). Every training window satisfies the ARIMA minimum (~24 periods; danskvand and RTD at 23 are marginally below and are flagged as a thin-data caveat in §4.6) and contains at least two seasonal cycles for Prophet. All test windows end in March 2026 and cover at least one autumn/winter promotional cycle.

4.6 Key Risks and Mitigations

Figures verified (resolved). All structural, data-quality, and EDA figures in this chapter are recomputed locally from the data/raw parquets under the DVH EXCL. HD scope (2026-06-27), superseding the earlier P0023 audit values; no placeholders remain. Residual dependence is only on Brian’s final harmonised pipeline, against which the local figures are expected to reconcile.

Market scope (resolved). Confirmed locally that the inherited “All Markets” aggregation double-counts (6.16× inflation for CSD; 14–17× for the other three categories, which expose 86 market levels). Resolved by scoping all four categories to the single DVH EXCL. HD market level; feature matrices regenerated accordingly (2026-06-23) under DVH EXCL. HD + MIN_PERIODS=30.

Per-category EDA (resolved). All four categories now have a dedicated EDA recomputed under DVH EXCL. HD (§4.3.6): stationarity (three of four series I(1), RTD stationary in level), short-horizon autocorrelation (lag-1 +0.55…+0.82), seasonality, and promo correlation. MIN_PERIODS and LAGS transfer reasonably across categories; PEAK_MONTHS is derived per category rather than inherited, since the four seasonal profiles differ materially. Per-brand lag optimisation remains a stated scope bound.

Thin training windows (danskvand, RTD). Both have only 23 training months, marginally below the ~24-period ARIMA rule of thumb, and danskvand has just 24 retained brands. Mitigation: these three categories are framed as parallel proofs of concept rather than primary evidence; CSD (42 periods, 77 brands) is the worked category carrying the main claims, and the short-window caveat is restated in the discussion.

Empirical parameters. MIN_PERIODS, LAGS, ROLLING_WINDOWS, and PEAK_MONTHS are EDA-driven, not theory-first. Mitigation: justified post hoc in the modelling chapter and stated as a limitation.

Promotional coverage (danskvand, RTD). Promo-zero categories lack the promotional signal (an unmeasured-variable limitation). Mitigation: promotional features are disabled for these categories and the limitation is stated in the discussion.

Weighted-distribution imputation. Median imputation ignores within-period time variation (moderate risk for niche brands, low for high-coverage brands). Mitigation: documented; sensitivity noted.

Commercial access / confidentiality. Raw data cannot be redistributed and must stay local; full external reproducibility is limited to processed features, code, and protocol.

Generalisability bound. Findings are bounded to the DVH EXCL. HD scope, the available period window, and the fully observed series filter; applicability to other markets, intermittent series, or non-beverage categories is future research.

References cited in this chapter

Saunders, M. N. K., Lewis, P., & Thornhill, A. (2023). Research Methods for Business Students (9th ed.). Pearson.

Chapter 5 - Predictive-Extension Architecture

5.1 Design Objectives and Constraints

This chapter specifies the architecture of the thesis artefact: a predictive extension that equips a production-oriented, non-predictive agentic decision-support system with forecast-informed capability. Following the Design Science Research framing of Chapter 3 (Hevner et al., 2004; Peffers et al., 2007), the architecture is presented as a designed artefact whose components are justified against the research questions and the deployment constraint, and from which transferable design knowledge is drawn in Chapters 9 and 10.

The architecture pursues four design objectives, each tied to a research question. First, it must produce reliable demand forecasts at brand-by-retailer granularity within a fixed memory budget (SRQ1). Second, it must expose those forecasts to an agentic layer through a structured tool and action interface that preserves reliability, uncertainty, and traceability (SRQ2). Third, it must specify the architectural and operational capabilities that a production-oriented agentic system requires in order to integrate forecast-informed decision-support (SRQ3). Fourth, it must permit a controlled comparison between the dedicated-model agentic approach and a general-purpose code-as-action baseline (SRQ4).

Two constraints shape every choice. The first is a hard ceiling of approximately eight gigabytes of total RAM across all simultaneously active components, treated as a formal design criterion rather than a convenience, reflecting the realistic cloud budget of a small or medium-sized AI provider. The second is the processing mode: monthly batch forecasting over historical data, not real-time streaming. Consistent with the pragmatist stance of Chapter 3, the architecture is judged by whether it works within these constraints, not by architectural elegance for its own sake.

A note on status: this is a design specification, but its lower layers are implemented and measured. The forecasting substrate is implemented and benchmarked across the five categories (Chapter 6), and its component memory figures are measured by RSS and reported in Table 5.1. The structured interface and the bounded agentic layer are realised in the lightweight Python coordinator (exercised in Chapter 7), while the cost and latency of the agentic and code-as-action paths are the secondary SRQ4 dimensions reported at pilot scale in Chapter 8. Where a figure depends on a layer still being hardened, this is stated explicitly rather than presented as a settled result.

5.2 Architectural Overview

The predictive extension is organised in three layers:

a forecasting substrate, a set of lightweight machine learning models that produce point forecasts and interval information (SRQ1; benchmarked in Chapter 6);

a structured forecast-tool interface, a JSON-based function-calling contract through which the substrate is exposed to the agentic layer as a callable tool (SRQ2);

a bounded tool-using agentic decision-support layer, an LLM orchestrator that invokes the substrate through the interface and synthesises a confidence-qualified recommendation, with human-in-the-loop checkpoints.

In the conceptual taxonomy of Sapkota et al. (2025), the artefact at its current stage is most accurately described as a bounded tool-using AI agent with human oversight, rather than a full multi-agent Agentic AI system. A multi-agent decomposition, in which specialist agents coordinate, is a production-target and future-work consideration, not a property of the evaluated artefact. This deliberate boundary keeps the system auditable and within the resource budget.

The layers are coordinated by a lightweight Python coordinator that passes typed state between components. This lightweight coordinator is the evaluated implementation. The production target, exemplified by Manifold AI’s Prometheus platform, is a LangGraph-based deployment whose concrete integration point is the Prometheus Graph Engine; that production substrate is the object of the integration-readiness assessment (SRQ3, Section 5.6), not the evaluated implementation. The architecture is summarised in Figure 5.1.

Figure 5.1 - The predictive-extension architecture. A lightweight Python coordinator (≤ 8 GB RAM, one model resident at a time, the LLM kept out-of-process via remote API) wraps three layers: a forecasting substrate of five lightweight models (SRQ1), a structured JSON forecast-tool interface preserving reliability, uncertainty, and traceability (SRQ2), and a bounded tool-using agentic layer that produces a confidence-qualified, auditable recommendation (informing SRQ3). The dedicated-model path is compared against a code-as-action LLM baseline on correctness, consistency, replicability, cost, and latency (SRQ4).

5.3 The Forecasting Substrate (SRQ1)

The substrate comprises lightweight models spanning the accuracy-efficiency frontier: ARIMA, Prophet, LightGBM, XGBoost, and Ridge Regression, evaluated across the five beverage categories and compared in their category-specialised and pooled variants (Chapter 6). The gradient-boosted models use the exogenous predictors described in Chapter 4, namely promotional, distribution, and calendar features, alongside autoregressive features; the two promotional features are inactive for the promo-zero categories.

Two design decisions follow from the RAM constraint. First, models are executed sequentially (load, run, unload) so that only one model occupies memory at a time, rather than concurrently. Second, memory is profiled by process resident set size (RSS, via the Python psutil and resource interfaces) rather than by tracemalloc alone, because tracemalloc does not capture the native allocations of XGBoost and LightGBM. The substrate exposes, for each forecast, a point estimate accompanied by interval information; where multiple models are combined, it aggregates them using inverse-MAPE weighting in the spirit of Ahrens et al. (2024). Stability across repeated runs is treated as a production-relevant property alongside accuracy (Klee and Xia, 2025).

Measured locally on the largest category (CSD), the per-model fit footprint is small in RSS terms: XGBoost adds about 15 MB, LightGBM about 7 MB, and Ridge under 1 MB over the runtime baseline (sequential, one model resident at a time). For reference, a tracemalloc run capturing Python-level allocations alone reports even smaller per-fit peaks (Ridge 1.5 MB, LightGBM 18.7 MB, XGBoost 0.2 MB; ARIMA fitted per series at ~0.5 MB), confirming that native library buffers are the larger but still modest component. Either way the substrate operates two orders of magnitude below the eight-gigabyte ceiling; the binding effect of the RAM budget is on the model-selection space (it excludes transformer and locally hosted options up front), not on the footprint of the selected models. Component figures are consolidated in Table 5.1.

5.4 The Structured Forecast-Tool Interface (SRQ2)

The interface is the mechanism by which a forecast is exposed to the agentic layer, and is the locus of SRQ2. It is realised as a JSON-based function-calling contract with strict output schemas: the agentic layer invokes the substrate as a tool and receives a structured response containing the point forecast and its interval. The interface is designed to preserve three properties:

Reliability, by validating the agent’s stated numbers against the source forecast values before delivery, so that the agent reports the model’s numbers rather than its own.

Uncertainty, by attaching interval information to every forecast; interval calibration follows the post-hoc approach of Kuleshov et al. (2018) and is treated as a design target, not an empirically validated property of the current prototype.

Traceability, by recording the mapping from tool call and forecast value to the resulting recommendation, so that each recommendation can be audited back to its source forecast.

The artefact deliberately adopts JSON function-calling, rather than code-as-action, for reliability and reproducibility: the schema-constrained interface yields deterministic, auditable tool calls. The code-as-action pattern (Wang et al., 2024) is not used inside the artefact; it is instead the baseline against which the artefact is compared (Section 5.7).

5.5 The Bounded Tool-Using Agentic Layer

The agentic layer is an LLM orchestrator accessed through a remote API rather than loaded locally, a decision that keeps the language model out of the RAM budget entirely (a locally hosted model would add several gigabytes; Semerikov et al., 2025). Given a decision-support prompt, the layer invokes the forecasting substrate through the structured interface, optionally combines multiple model outputs, and produces a concise, confidence-qualified natural-language recommendation, subject to human-in-the-loop checkpoints.

The layer embodies a delegation-over-generation principle: the LLM does not itself predict demand or compute the forecast, but delegates numerical prediction to the dedicated models and confines itself to orchestration, validation, and communication. Decoding is configured for reproducibility (temperature zero). This separation of a generative orchestrator from deterministic predictive components is the architectural feature that makes the agentic numerical decision-support both auditable and resource-feasible.

5.6 Integration Readiness (SRQ3)

SRQ3 concerns the capabilities a production-oriented agentic system must possess to integrate forecast-informed decision-support. The architecture identifies four such capabilities: a structured tool interface for invoking external predictive models; observability and traceability of tool calls and their outputs; explicit handling of reliability and uncertainty; and operation within bounded cost, latency, and memory.

These capabilities are assessed against a real production-oriented agentic system, Prometheus, whose Graph Engine is the concrete integration interface, as the empirical case. The assessment is a capability-readiness analysis rather than a live integration experiment: it establishes which of the required capabilities the production system already possesses and which the predictive extension would add, without depending on a completed production deployment.

5.7 The Code-as-Action Baseline (SRQ4)

To evaluate whether dedicated-model integration is warranted at all, the architecture includes a code-as-action baseline: a general-purpose LLM that, given the same data access and the same prompts, writes, executes, and self-corrects its own forecasting and analysis code in a sandboxed environment (for example, E2B), without a dedicated pre-built model (Wang et al., 2024). The baseline uses the same base LLM as the agentic layer, so that the comparison isolates the effect of dedicated-model integration rather than differences in model quality.

The baseline is runnable locally and does not require access to the production system, which makes the SRQ4 comparison feasible independently of integration access. The comparison protocol and metrics (correctness, consistency, and replicability as primary dimensions; cost and latency as secondary; following the multidimensional frame of Mehta, 2025) are specified in Chapter 3 and applied in Chapter 8.

5.8 Memory, Cost, and Latency Budget

The eight-gigabyte ceiling is respected by construction: data and one model are held in memory at a time, the language model is accessed by API rather than loaded, and intermediate artefacts are released after use. Memory is reported by RSS; cost (API tokens) and latency (wall-clock, including tool round-trips) are tracked as the secondary SRQ4 dimensions. The per-component budget, measured by RSS on the local pipeline over the largest category (CSD), is summarised in Table 5.1.

Component

Peak RAM (RSS)

When

Python runtime and libraries (numpy, pandas, LightGBM, XGBoost, scikit-learn)

~194 MB

Always

Coordinator state (typed state passed between components)

< 1 MB

Always

Nielsen data (per category, largest = CSD)

~15 MB

Data loading

Active model (one at a time; XGBoost ≈15, LightGBM ≈7, Ridge < 1 MB)

~15 MB

Forecasting

Agentic layer (remote API; no weights loaded, network buffer only)

negligible

Synthesis

End-to-end peak

~231 MB

Forecasting

Table 5.1. Per-component budget, measured by RSS (psutil) on the local pipeline, 2026-06-27. The end-to-end peak of approximately 231 MB is about 2.8% of the eight-gigabyte budget. The budget therefore binds the model-selection space (excluding transformer and locally hosted LLM options up front) rather than the final footprint; the realised footprint sits two orders of magnitude below the ceiling because the language model is kept out of process by the remote-API design and only one lightweight model is resident at a time.

5.9 Technology Choices and Justification

Choice

Alternative not adopted

Reason

Lightweight Python coordinator (evaluated)

LangGraph deployment

LangGraph is the production target (Prometheus); the lightweight coordinator is leaner for the evaluated prototype under the RAM budget

JSON function-calling interface (artefact)

Code-as-action inside the artefact

Reliability and reproducibility; code-as-action is instead the SRQ4 baseline

LightGBM and XGBoost

LSTM, Temporal Fusion Transformer, Chronos

An order of magnitude lower RAM at competitive accuracy on tabular retail data under the period budget

LLM via remote API

Locally hosted LLM

Avoids several gigabytes of model weights, keeping the language model out of the RAM budget (Semerikov et al., 2025)

Sandbox (e.g. E2B) for the baseline

Bespoke execution harness

Open and local; runs the code-as-action baseline without production access

Each choice is argued against the eight-gigabyte constraint, in keeping with the design criterion of Chapter 1.

5.10 Summary

The architecture instantiates the predictive extension as three layers, a forecasting substrate, a structured forecast-tool interface, and a bounded tool-using agentic layer, coordinated by a lightweight Python coordinator and designed to operate within an eight-gigabyte budget. It is deliberately a bounded tool-using agent rather than a multi-agent system, delegates prediction to dedicated models rather than generating it, and is positioned for integration into a production-oriented agentic system through a structured interface. The forecasting substrate is benchmarked in Chapter 6 (SRQ1), the interface and agentic layer are realised and exercised in Chapter 7 (SRQ2, informing SRQ3), and the dedicated-model approach is compared against the code-as-action baseline in Chapter 8 (SRQ4).

References cited in this chapter

Ahrens, A., Hansen, C. B., Schaffer, M. E., & Wiemann, T. (2024). Model averaging and double machine learning. Journal of Applied Econometrics. https://doi.org/10.48550/arXiv.2401.01645

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. MIS Quarterly, 28(1), 75–105.

Klee, S., & Xia, Y. (2025). Measuring time series forecast stability for demand planning. KDD ’25 Workshop on AI for Supply Chain.

Kuleshov, V., Fenner, N., & Ermon, S. (2018). Accurate uncertainties for deep learning using calibrated regression. In Proceedings of ICML 2018 (PMLR, Vol. 80).

Mehta, S. (2025). Beyond accuracy: A multi-dimensional framework for evaluating enterprise agentic AI systems. arXiv preprint arXiv:2511.14136. [PREPRINT, not peer-reviewed]

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. Journal of Management Information Systems, 24(3), 45–77.

Sapkota, R., Roumeliotis, K. I., & Karkee, M. (2025). AI agents vs. agentic AI: A conceptual taxonomy, applications and challenges. Information Fusion, 126, Article 103599. https://doi.org/10.1016/j.inffus.2025.103599

Semerikov, S. O., Vakaliuk, T. A., Kanevska, O. B., Ostroushko, O. A., & Kolhatin, A. O. (2025). Edge intelligence unleashed: A survey on deploying large language models in resource-constrained environments. Journal of Edge Computing, 4(2). https://doi.org/10.55056/jec.1000

Wang, X., Chen, Y., Yuan, L., Zhang, Y., Li, Y., Ji, H., & Tong, H. (2024). Executable code actions elicit better LLM agents. In Proceedings of the 41st International Conference on Machine Learning (PMLR).

Chapter 6 - Model Benchmark & Selection

6.1 Rationale for model selection

Five model families span the inductive-bias spectrum: classical statistical (ARIMA, Prophet), gradient boosting (LightGBM, XGBoost), regularised linear (Ridge), plus four parameter-free benchmarks (mean, naive, seasonal-naive, drift)

Selection criteria: (a) established empirical performance on retail/FMCG panels;

fit within the ≤8 GB sequential RAM budget; (c) interpretability sufficient for the SRQ4 scenario comparison; (d) diversity of inductive bias

The benchmark rung is required, not decorative. Hyndman & Athanasopoulos (2021, §5.2) define the four simple methods as benchmarks against which “any forecasting methods we develop will be compared … to ensure that the new method is better than these simple alternatives”. A forecasting result reported without them is unbenchmarked

Empirical weight for that requirement comes from M4: of six pure machine-learning entries, none beat the statistical combination benchmark and only one beat Naïve2 (Makridakis et al., 2018, p. 803)

NOT included, and why: deep sequence models (LSTM/N-BEATS) - RAM footprint incompatible with the ≤8 GB constraint, and infeasible under the HPO time budget on ~30 monthly observations per series

6.2 Model descriptions

6.2.0 Simple benchmarks

Four parameter-free methods, defined as in Hyndman & Athanasopoulos (2021, §5.2):

Method

Forecast for horizon h

Mean

ŷ(T+h) = ȳ

Naive

ŷ(T+h) = y(T)

Seasonal naive

ŷ(T+h) = y(T+h−m(k+1)), with m the seasonal period and k = ⌊(h−1)/m⌋

Drift

ŷ(T+h) = y(T) + h · (y(T) − y(1)) / (T−1)

Seasonal naive is the decisive one for this panel. Monthly beverage demand has strong annual seasonality, which seasonal naive exploits with zero parameters. It is the direct test of whether a tuned model has learned seasonality or merely fitted it

6.2.1 ARIMA

Classical univariate time-series model in the Box–Jenkins framework

Role: statistical baseline representing established traditional forecasting

Implementation: statsmodels SARIMAX(order=(1,1,1)) on log sales, fitted per brand. A fixed order, not a search - pmdarima/auto_arima was unavailable in the environment. This is a stated limitation: ARIMA is not order-optimised, so its numbers are a floor for the family rather than its best achievable performance

RAM: ~0.5 MB measured; negligible

Limitation: assumes stationarity; univariate, so no promotional or calendar inputs

6.2.2 Prophet (Meta)

Additive decomposable model, y(t) = g(t) + s(t) + h(t) + ε - trend, seasonality, holidays (Taylor & Letham, 2018, p. 38, Eq. 1)

Designed for forecasting at scale by analysts with domain rather than statistical expertise, targeting “piecewise trends, multiple seasonality, floating holidays” (pp. 37–38)

No holiday calendar is supplied in this thesis, and none of the multi-seasonality machinery applies at month grain

RAM: ~50–100 MB; acceptable

6.2.3 LightGBM

Gradient boosting with leaf-wise tree growth and GOSS sampling

Role: primary ML candidate

RAM: ~18.7 MB measured

HPO: Optuna TPE, 100 trials, 4-fold expanding-window CV (§6.3.4)

6.2.4 XGBoost

Gradient boosting with level-wise growth and L1/L2 regularisation

Role: ML alternative with a different regularisation strategy

Identical feature set to LightGBM for a controlled comparison

RAM: ~0.2 MB measured

HPO: identical protocol

6.2.5 Ridge regression

L2-regularised linear regression: minimises the penalised residual sum of squares, equivalently RSS subject to Σβ² ≤ t (Hastie et al., 2009, pp. 61–62, Eq. 3.41–3.42)

Role: linear baseline - establishes whether non-linear models earn their complexity

RAM: ~1.5 MB measured

6.3 Experimental setup

6.3.1 Grain and data split

Grain: brand × month (DEC-GRAIN). The chain and region grains were evaluated and dropped; they are reported as a limitation and future work, not as a live dimension

Temporal train/validation/test split, no shuffling

Horizon H = 3 months

Test-set sizes: CSD 665 rows, RTD 372, energidrikke 308, danskvand 174

6.3.2 Feature engineering

Lags: t−1, t−2, t−3, t−4, t−8, t−13 months

Rolling statistics: 4-month and 13-month mean; 4-month standard deviation

Calendar: month, quarter, and a binary peak_month flag derived from the category’s own seasonal profile (months whose mean units exceed the category mean by more than 10%). No holiday calendar is used - the flag is measured from the sales distribution, not from calendar dates

Promotional: promo_intensity (promotional share of units, clipped to [0,1], lagged one period). Available for CSD and energidrikke only - Nielsen reports no promotional measure for danskvand or RTD, so the feature is omitted rather than zero-filled, since a constant zero would assert that no promotion ran

Missing lag values for short histories are left as NaN (handled natively by the tree models); Ridge receives a zero-fill at fit time

6.3.3 Execution protocol

Sequential execution: load → fit → predict → unload → gc.collect()

Memory profiling via tracemalloc at each stage; peak RAM recorded per model

Fixed seed (42) throughout; seed sensitivity is measured separately (§6.5)

6.3.4 Validation scheme

Hyperparameters are selected by 4-fold expanding-window (rolling-origin) cross-validation, splitting on distinct periods rather than rows - the rows are brand-months, so a row-wise split would place the same month in training and validation for different brands. The training window grows forward and validation is the block immediately following it, so no model ever sees a period later than the one it predicts. The test split is untouched throughout.

Rolling-origin evaluation successively advances the forecast origin instead of relying on a single split, which is vulnerable to “corruption by occurrences unique to that origin” (Tashman, 2000, p. 439). Because each fold refits from scratch, this is recalibration rather than mere updating - Tashman’s preferred procedure (p. 440).

6.3.5 Hyperparameter optimisation

Optuna’s TPE sampler, 100 trials per model × category × objective. TPE models the configuration density conditional on performance, splitting observed trials into densities l(x) below and g(x) above a quantile threshold (Bergstra et al., 2011, p. 2549). Optuna supplies the define-by-run interface, sampling and pruning infrastructure (Akiba et al., 2019, p. 2623).

The trial budget is justified empirically, not by convention. No trial-count convention exists in the HPO literature; the requirement scales with search-space dimensionality. The tuner therefore records the running best CV score per trial and reports the trial after which improvement becomes negligible. Measured plateaus range from 3 to 87 trials with a median near 16, so 100 trials comfortably contains the converged region for every configuration.

6.4 Evaluation metrics

Metric

Definition

Rationale

WMAPE

Σ|y−ŷ| / Σ|y| × 100

Primary. Volume-weighted, defined at zero actuals, and consistent for the median (see below)

Median APE

median(|y−ŷ|/y) over y > 0

Robust per-series view; undefined where y = 0

MASE

mean(|y−ŷ|) / in-sample MAE of the naive forecast, per series

Scale-free, defined at zero, and absolutely interpretable: < 1 beats a naive forecast

Coverage (80 / 90% PI)

share of actuals inside the interval

Calibration signal for SRQ2

Median relative interval width

interval width ÷ actual

Reported beside coverage - see below

Peak RAM (MB)

tracemalloc peak

The operational constraint

Inference latency (ms)

wall-clock prediction time

Agent responsiveness

Plain mean MAPE is not reported. It is undefined against a zero actual and diverges to meaningless magnitudes near zero - on this panel it reaches 10¹³ - because percentage errors are “infinite or undefined if Yₜ = 0 … and have an extremely skewed distribution when any value of Yₜ is close to zero” (Hyndman & Koehler, 2006, p. 683).

6.4.1 Why WMAPE is the primary metric

The choice is not conventional but theoretical. A scoring function determines which functional of the predictive distribution an optimal forecast reports (Gneiting, 2011):

absolute-error loss is minimised by the median (p. 746);

pointwise absolute percentage error is minimised by the (−1)-median - a density reweighted by y⁻¹ - which biases forecasts systematically downward (pp. 746, 752);

WMAPE aggregates absolute errors before dividing by total volume, so minimising it over a fixed evaluation sample is equivalent to minimising MAE, and is therefore consistent for the standard median.

This predicts, rather than merely describes, the WMAPE/median-APE divergence reported throughout this chapter. The two metrics estimate different functionals, so agreement was never to be expected. It also explains why tuning against median APE costs 8–13 pp of WMAPE while buying only 2–3 pp of median APE: that objective targets the (−1)-median and underforecasts, which WMAPE penalises directly.

6.4.2 Scorability, and what is excluded from what

Between 14% and 29% of test rows per category have a zero actual, where APE is undefined. Two distinct decisions follow, and they are not the same rule:

Rule

Applies to

Basis

Exclude zero-actual rows

Median APE and MAPE only

Mathematical - APE is undefined there

(nothing else)

-

-

WMAPE and MASE are computed on every row. Both are defined at zero actuals, so neither requires an exclusion, and none is applied.

Irregular series are handled by categorisation rather than removal - see §6.4.4.

6.4.3 Targets

Accuracy target: none imported from the literature. Earlier drafts carried a ≤15% WMAPE target attributed to Ceran et al. (2024). Source-level verification (2026-08-25) found no such benchmark in that paper: the authors explicitly reject MAPE because their panel contains too many zero-demand observations for a percentage error to be well defined, and report WRMSSE, RMSE and MAE instead. The target is therefore withdrawn, and no claim that an external accuracy target is met or approached should be written anywhere in the thesis

What replaces it: the simple benchmarks of §6.2.0, scored on this thesis’s own test rows (§6.5.2). This is the stricter test and needs no cross-study metric alignment - a target borrowed from a daily product-store study with a 15-day horizon was never comparable to brand × month at H=3 in any case

Calibration target: ≥85% empirical coverage for a nominal 90% interval - and interval width must be reported alongside, since an arbitrarily wide interval attains perfect coverage while carrying no decision-relevant information

6.4.4 Demand-pattern categorisation

Brand-level demand on this panel ranges from steady weekly sellers to series with long gaps and highly variable order sizes. Reporting a single pooled accuracy figure across that range obscures more than it conveys, and thresholding the difficult series away would reproduce exactly the practice the metric literature objects to.

Each brand is therefore classified using the scheme of Syntetos, Boylan and Croston (2005, p. 495), on two measured quantities with derived cut-offs:

p - average inter-demand interval (periods per non-zero demand)

CV² - squared coefficient of variation of non-zero demand sizes

CV² ≤ 0.49

CV² > 0.49

p ≤ 1.32

smooth

erratic

p > 1.32

intermittent

lumpy

The thresholds are not tuned to this data: they mark where the relative accuracy ordering of Croston’s method, the Syntetos–Boylan Approximation and simple exponential smoothing changes. Classification uses train and validation periods only - deriving classes from test rows and then reporting test accuracy per class would leak.

Resulting distribution (230 brands):

Category

smooth

erratic

intermittent

lumpy

CSD

44

32

5

14

RTD

32

20

2

8

energidrikke

16

18

2

8

danskvand

16

9

3

1

This categorises; it does not exclude. Accuracy is reported per class, so weak performance on lumpy series appears as a stated limitation rather than as an absence. That is the response Syntetos and Boylan’s own work recommends - their contribution is estimators for such series, not advice to discard them.

6.5 Results

All results are on the locked brand × month grain (DEC-GRAIN). The alternative brand × chain representation, and the granularity comparison built on it, were removed from the project by P0035 and no longer appear in this chapter.

6.5.1 Tabular-model benchmark

Both gradient-boosted models were tuned with Optuna (TPE, 100 trials) against an expanding-window cross-validation objective, then scored once on the untouched test split. Because WMAPE and median APE are minimised by different functionals (§6.4.1), each model was tuned twice - once per objective - and both results are reported. cv_metrics.csv.

Tuned for WMAPE:

Category

Model

CV WMAPE

Test WMAPE

Test medMAPE

n test

CSD

LightGBM

17.0%

14.5%

33.2%

665

CSD

XGBoost

16.1%

15.2%

31.8%

665

danskvand

LightGBM

17.9%

20.5%

38.6%

174

danskvand

XGBoost

17.1%

20.9%

35.8%

174

energidrikke

LightGBM

10.6%

16.5%

34.7%

308

energidrikke

XGBoost

10.6%

13.0%

32.3%

308

RTD

LightGBM

27.9%

31.8%

38.1%

372

RTD

XGBoost

28.0%

36.1%

32.8%

372

The two objectives select different models and produce different rankings. Tuning for median APE improves that metric and degrades WMAPE, as the theory in §6.4.1 predicts: absolute-error loss is minimised by the median, while a pointwise percentage error is minimised by a lower functional. On energidrikke the effect is large - LightGBM tuned for medMAPE reaches 29.8% test WMAPE against 16.5% when tuned for WMAPE. A single “best model” number is therefore meaningless without naming the objective it was tuned against, which is why both are carried here.

Validation-to-test movement is substantial and is not hidden. energidrikke tunes to 10.6% in cross-validation and lands at 13.0–16.5% on test; RTD moves the other way on LightGBM. The gap is consistent with the selection bias documented in §6.3.5 - this protocol is not nested, so the cross-validation figure is an optimistically biased estimate of generalisation, to an unquantifiable degree (Cawley & Talbot, 2010).

6.5.2 The simple benchmarks, and where they win

The four benchmarks of §6.2.0 were run on the same test rows. stat_baselines.csv.

Category

Naive

Seasonal naive

Drift

Ridge

ARIMA

Prophet

Best tuned ML

CSD

42.9%

19.2%

47.7%

19.4%

21.8%

105.7%

14.5%

danskvand

32.5%

35.9%

32.0%

10.9%

33.5%

19.5%

20.5%

energidrikke

18.9%

23.8%

17.7%

18.3%

19.4%

972.4%

13.0%

RTD

89.3%

27.3%

95.9%

40.5%

53.3%

66.8%

31.8%

Two categories are not won by the tuned models, and this is the most important result in the section.

On RTD, seasonal naive beats every tuned configuration - 27.3% against 31.8–36.1%. The most irregular category is the one where a method with no parameters wins.

On danskvand, a plain Ridge regression reaches 10.9%, roughly half the tuned gradient-boosted error. danskvand is also the smallest panel (29 series, 174 test rows), where a high-capacity model has least to learn from.

This is precisely the outcome the benchmark rung exists to detect. Hyndman and Athanasopoulos (2021, §5.2) recommend the simple methods as a standard against which any new method must justify itself; here they are not a formality but a live constraint, and reporting a headline ML number without them would have concealed that the thesis’s approach is beaten outright on half the categories.

Prophet is applied outside its design regime and its numbers should not be read as a defect of the method. Taylor and Letham (2018) target daily business series with multiple seasonalities and holiday effects; at month grain, weekly seasonality does not exist, no holiday calendar is supplied, and yearly seasonality reduces to about twelve observations. Fitting a linear trend on log-transformed short series lets the trend extrapolate to extreme values on back-transformation, producing the 105.7% and 972.4% figures. This is a limitation of the application, not of Prophet, and is reported as such.

Ridge requires clipping to be reportable. Unclipped, its energidrikke WMAPE is 2.8×10¹³ and its RTD WMAPE 2459%, because back-transformed linear extrapolation diverges. The clipped variant is what appears above; the raw values are retained in stat_baselines.csv because the instability is itself informative about linear models on this panel.

6.5.3 Scaled error (MASE)

WMAPE compares models within a category but says nothing about whether a category is forecastable at all. MASE answers that directly: below 1 beats the in-sample naive forecast. mase.csv.

Category

Naive MASE

Seasonal-naive MASE

Naive median ASE

CSD

0.95

1.63

0.39

danskvand

0.99

1.60

0.52

energidrikke

0.67

2.02

0.05

RTD

6.54

14.02

0.18

RTD’s mean MASE of 6.54 against a median ASE of 0.18 is a distributional finding, not an accuracy one. The typical RTD series is forecast better than naive; the mean is carried by a small number of cells with very large scaled errors. Reporting only the mean would describe RTD as catastrophically unforecastable, and only the median would conceal that a few series are. Both are reported for this reason.

Seasonal naive scores worse than naive on MASE in every category while winning on WMAPE for RTD - the two metrics weight differently (volume versus per-series scale), and the disagreement is surfaced rather than resolved by picking one.

6.5.4 Pooled versus per-category training

Whether one model trained across all four categories beats four category-specific models is SRQ1’s central design question. Both arms use the same 12-feature intersection, the same tuning protocol, and are scored on identical test rows, so they differ only in which rows they were trained on. pooled_summary.md.

Category

LightGBM pooled → per-cat

XGBoost pooled → per-cat

CSD

17.5% → 16.3% (per-cat better by 1.2 pp)

16.6% → 15.3% (per-cat by 1.3)

danskvand

21.4% → 23.7% (pooling wins 2.2 pp)

18.9% → 21.5% (pooling wins 2.5)

energidrikke

12.1% → 13.7% (pooling wins 1.6)

12.5% → 13.9% (pooling wins 1.4)

RTD

35.8% → 35.1% (per-cat by 0.7)

37.0% → 35.5% (per-cat by 1.5)

The answer is conditional, and the condition is data volume. Pooling wins on the two smallest panels (danskvand 174 test rows, energidrikke 308) and loses on the two largest (CSD 665, RTD 372). This is the expected transfer-learning trade-off: a small category borrows strength from the others, while a large one is diluted by them. The pattern holds for both model families, which is what makes it a finding rather than noise - though §6.5.9 shows the magnitudes here sit within seed noise, so the direction is the claim, not the pp values.

Per-brand, the aggregate conceals wide disagreement. Broken out by demand class (pooled_perbrand_summary.md), pooling helps between 44% and 64% of brands depending on class and model - close to a coin flip everywhere. The aggregate deltas above are small differences between two distributions that overlap heavily.

6.5.5 Results by demand pattern

Using the Syntetos–Boylan–Croston partition of §6.4.4, the 230 brands divide into 108 smooth, 79 erratic, 12 intermittent and 31 lumpy. Nothing is excluded; irregular series are reported rather than filtered.

The most informative fact here is an absence: 15 of the 31 lumpy brands have no test signal at all - their entire test window is zero. Pooling deltas for the lumpy class are computed on the 16 that remain, and any per-brand percentage statistic for the other 15 would be undefined. This is a property of the data that a volume threshold would have hidden by removing the brands quietly; the categorisation makes it visible and countable.

For the classes with signal, pooling win-rates run 46–55% (smooth), 51–64% (erratic) and 44–56% (intermittent). No demand class shows a decisive pooling effect.

6.5.6 Operational profile

Peak RAM on the largest matrix is in single-digit megabytes for every model - Ridge 5.5, LightGBM 8.0, XGBoost 0.1, ARIMA 0.3 MB - against the 8 GB sequential budget of SRQ1. The memory constraint is non-binding by three orders of magnitude at this data scale, which is a real answer to the research question and not a missing measurement: the constraint that motivated the question does not bite here.

Latency is likewise immaterial: XGBoost fits in 0.97 s and predicts in 9.3 ms; LightGBM fits in 2.04 s and predicts in 15.9 ms. profiling.csv.

6.5.7 Prediction-interval calibration

A split-conformal wrapper on the tuned model, calibrated on validation residuals in log space, gives the following on the untouched test split. calibration.csv.

Category

Nominal

Empirical coverage

Median relative width

n calib

CSD

90%

89.6%

3.3×

665

RTD

90%

89.0%

3.1×

372

danskvand

90%

87.4%

16.8×

174

energidrikke

90%

93.5%

8.9×

264

CSD

80%

78.6%

1.9×

665

RTD

80%

76.1%

1.7×

372

danskvand

80%

70.7%

3.5×

174

energidrikke

80%

82.5%

3.3×

264

The half-width is the ⌈(n+1)(1−α)⌉/n empirical quantile of the calibration residuals - Algorithm 2 of Lei et al. (2018) - not the nominal (1−α) quantile. The finite-sample correction is what supports the distribution-free guarantee at finite n.

Coverage alone is the wrong success criterion, and this table shows why. An arbitrarily wide interval attains perfect coverage while carrying no decision-relevant information. danskvand meets its 90% coverage target only with intervals spanning roughly seventeen times the quantity being forecast, which no planner can act on. For danskvand and energidrikke, width - not coverage - is the binding constraint, and both are reported as limitations rather than averaged into a “well-calibrated” claim. At the 80% level danskvand additionally undercovers, at 70.7%.

6.5.8 Remaining gaps

The ≤15% accuracy target has been withdrawn, not scored. Verification found the benchmark does not exist in the cited source (§6.4.3). Accuracy is therefore assessed against the simple benchmarks of §6.5.2 alone, on which two of four categories are beaten outright.

The tuning protocol is not nested, so every cross-validation figure above is optimistically biased by an unquantified amount (§6.3.5).

ARIMA and Prophet use a fixed specification per series rather than a per-series order search, on cost grounds. Their figures are a competent baseline, not the best attainable from those families.

fig4_ram_budget is stale and contradicts §6.5.6.

6.5.9 Forecast stability across seeds

Chapter 2 motivates evaluating the modelling substrate on accuracy, computational efficiency and stability, and SRQ1’s scope names stability as its fourth axis. This section supplies that measurement, which had not previously been made.

Stability is measured as the coefficient of variation of the forecast for each (brand, month) cell across five random seeds, with data, splits, features and protocol held identical. Only the seed varies, driving Optuna’s sampler and the models’ own stochastic elements.

Category

Model

median CV

p90 CV

WMAPE mean

WMAPE sd

CSD

LightGBM

0.112

0.295

15.4%

0.65

CSD

XGBoost

0.123

0.422

15.1%

0.59

danskvand

LightGBM

0.119

0.687

20.8%

0.69

danskvand

XGBoost

0.124

0.539

21.8%

1.04

energidrikke

LightGBM

0.174

0.634

14.1%

1.18

energidrikke

XGBoost

0.174

0.730

13.9%

0.79

RTD

LightGBM

0.125

0.397

33.5%

1.64

RTD

XGBoost

0.104

0.400

35.1%

0.92

Two findings, and both matter more than the accuracy tables suggest.

First, aggregate stability flatters the system by roughly three times. Aggregate WMAPE moves by about 4.7% of its own level across seeds, while the typical individual forecast moves by about 13%, and the ninetieth-percentile cell by 30–73%. Per-cell movements partly cancel within a volume-weighted sum, so a planner reading one brand’s number experiences considerably more run-to-run variability than a headline metric implies. Both figures are therefore reported; quoting only the aggregate would understate instability threefold.

Second, and more consequentially for this chapter: the winning model changes with the seed in every category.

Category

Winner per seed

CSD

XGBoost, XGBoost, LightGBM, XGBoost, LightGBM

flips

danskvand

LightGBM ×3, XGBoost, LightGBM

flips

energidrikke

LightGBM, LightGBM, XGBoost, LightGBM, LightGBM

flips

RTD

XGBoost, XGBoost, LightGBM, LightGBM, LightGBM

flips

Every input is identical; only the random seed differs. A per-category statement of which gradient-boosting model is best is therefore not a finding - it reports the outcome of one seed. §6.6 states the conclusion this supports instead.

6.6 Model selection decision

The choice between LightGBM and XGBoost is not supported by this data. A five-seed sweep with every input held identical shows the winning model changes with the seed in all four categories (§6.5.7). Naming a winner per category would be reporting one seed’s outcome as a finding

The defensible claim is that the two are statistically indistinguishable here, the between-seed spread exceeding the between-model difference. This is a weaker headline but a true one, and it is useful: a practitioner deciding what to deploy can choose on operational grounds - training time, memory, tooling - rather than accuracy

What the benchmark does support is the gap between families: both gradient boosters clearly beat Ridge and ARIMA on most categories, and clearly lose to seasonal naive on RTD. Those differences exceed the seed noise; the LightGBM-vs-XGBoost one does not

The served model carries its own track record. The forecast tool returns the selected model’s measured accuracy (WMAPE and median APE), both simple baselines for that category, and a conformal interval - so the consuming agent receives the forecast’s reliability alongside the forecast

Metric disagreement is surfaced, not hidden. Where WMAPE and median APE rank models differently, the payload flags it rather than silently reporting one

Ensemble combination is evaluated as a separate scenario, not folded into this chapter’s selection. M4’s evidence that combinations outperform single models (Makridakis et al., 2018) motivates it, and treating it as its own rung is what makes the contribution measurable rather than assumed

6.7 Connection to SRQs

SRQ

How Ch.6 addresses it

SRQ1

Direct answer: which models work best for retail CSD forecasting within ≤8GB RAM

SRQ2

Prediction intervals + calibration coverage provide the raw confidence signal for SRQ2

SRQ3

Not addressed here; integration readiness is addressed in Ch3 and Ch5

SRQ4

Supplies the trained models and their measured accuracy to the scenario ladder; the models benchmarked here are what distinguishes the model-equipped scenarios from the data-only ones

Outstanding decisions

Resolved since this list was written - retained so the reasoning is traceable:

Exact train/validation/test dates pending Nielsen access → data in hand; splits fixed, test sizes stated in §6.3.1

HPO trial budget: 50 trials, may reduce under RAM pressure → 100 trials, and RAM was never the binding constraint (peak in the tens of MB against an 8 GB budget)

Whether to add a 6th model → four simple benchmarks added instead, which is the standard set and answers the “is it better than doing nothing” question directly

Genuinely open:

Which metric the ≤15% benchmark refers to. Closed 2026-08-25: the benchmark is not in the cited source at all; the target is withdrawn (§6.4.3)

Whether ARIMA should be order-searched. The fixed SARIMAX(1,1,1) is a floor for the family, not its best performance, and the baseline comparison is weaker for it

Whether the ensemble scenario runs, which determines whether §6.6’s combination paragraph describes a result or a deferred option

Chapter 7 - Context-Aware Decision Synthesis

7.1 The synthesis problem

After 5 models each produce a point forecast + prediction interval, a decision-maker needs a single actionable recommendation - not 5 competing numbers

The synthesis problem: how to aggregate heterogeneous ML outputs into a confidence-scored, natural language recommendation

This is the core SRQ2 question: How can an LLM synthesise multi-model forecasts into a confidence-scored recommendation?

Analogy: MCDM (Multi-Criteria Decision Making) - weight and aggregate multiple indicators into a ranked decision

Cite: Hybrid MCDM + ML Supplier Selection paper; Hybrid AI + LLM Industrial paper

7.2 Architecture of the Synthesis Agent

7.2.1 Inputs to the Synthesis Agent

Input

Source

Format

Model forecasts (5×)

Forecasting Agent

{model_name: {point_forecast, lower_90, upper_90, MAPE_validation}}

Historical context

Nielsen data

last_N_periods actuals, seasonality flags

Market context

Coordinator prompt

product category, retailer, planning horizon

7.2.2 Synthesis pipeline

Step 1 - Model consensus scoring - Compute inter-model agreement: std(point_forecasts) / mean(point_forecasts) = relative disagreement metric - High agreement (low spread) → higher base confidence - Assign inverse-MAPE weights to each model’s forecast: w_i = (1/MAPE_i) / Σ(1/MAPE_j) - Weighted ensemble point forecast = Σ(w_i × forecast_i)

Step 2 - Interval calibration - Apply Kuleshov et al. (2018) post-hoc calibration to ensemble prediction intervals - Calibration set: validation period actuals vs. stated intervals - Output: calibrated 90% prediction interval with empirically validated coverage

Step 4 - Confidence score computation - Composite confidence score (0–100): - 40% weight: calibrated interval width (narrower = higher confidence) - 30% weight: inter-model agreement (lower spread = higher confidence) - Map to 3-tier natural language: High (≥70), Moderate (40–69), Low (<40) - Cite: Kuleshov et al. 2018, Do Forecasts as Prediction Intervals Improve Planning (2010)

Step 5 - LLM recommendation generation - LLM (claude-sonnet-4-6 via API) receives structured synthesis context: - Ensemble forecast + calibrated interval - Confidence score + tier - Historical actuals for comparison - LLM generates: 2–3 sentence natural language recommendation + stock action suggestion - Temperature: 0 (deterministic for reproducibility) - Prompt template: stored in agent code, versioned

7.2.3 Deterministic synthesis results

The non-LLM core of the Synthesis Agent was implemented and run on the test set for all four categories: per (brand[, chain], month) it produces an inverse-WMAPE-weighted ensemble forecast, an inter-model agreement score, a split-conformal 90% interval, and a composite confidence score (30% agreement + 40% interval tightness + 30% model accuracy) mapped to a High/Moderate/Low tier.

Category

n series-months

mean confidence

Moderate / Low

90% interval coverage

CSD

845

44.9

72% / 28%

96.6%

danskvand

966

43.6

70% / 30%

97.8%

energidrikke

205

47.1

75% / 25%

80.0%

RTD

324

38.5

45% / 55%

90.7%

Two observations. First, the conformal ensemble interval is well-to-conservatively calibrated (empirical coverage 80–98% against the 90% nominal), so the uncertainty the agent communicates is trustworthy. Second, the composite confidence skews to the Moderate tier with no High-confidence forecasts under the current thresholds - because the (deliberately wide) 90% interval keeps the tightness term low. This is a property of the scoring weights, not of the forecasts; the tier cut-offs are a calibration choice to revisit. Operationally the engine already supports the SRQ2 goal: it triages each forecast by confidence so the agentic layer can surface reliable forecasts and route Low-confidence ones (notably the more volatile RTD, 55% Low) to human review. The natural-language recommendation and the LLM-as-Judge quality assessment (§7.3, §7.6) sit on top of this structured output and require an LLM API; they are run in the agentic-harness phase.

7.3 LLM prompt design

7.3.1 System prompt (Synthesis Agent)

You are a demand forecasting analyst for FMCG retail. Given a set of ML model forecasts, a calibrated confidence score, and consumer demand signals, you produce a concise, actionable recommendation for a category manager.

Rules:
- Always state the forecast range (lower to upper bound), not just the point estimate
- Always state the confidence level (High/Moderate/Low) and why
- If models disagree, flag the uncertainty explicitly
- Keep recommendations to 2-3 sentences maximum
- Do not hallucinate data - only use provided inputs

7.3.2 User prompt structure

PRODUCT: {product_name} | RETAILER: {retailer_name} | WEEK: {target_week}

ENSEMBLE FORECAST: {point_forecast} units (90% interval: {lower} – {upper})
CONFIDENCE: {score}/100 ({tier}) - based on {inter_model_spread} model agreement, {calibration_quality} calibration
HISTORICAL: Last 4 weeks actuals: {actuals_list}

Generate a recommendation.

7.4 Design principles applied

Progressive uncertainty disclosure (show interval, not just point) - cite AI-augmented decision making DSR 2024

Human override preserved - synthesis output is a recommendation, not an automated order

Contextualised explanation included in rationale

Confidence calibration (post-hoc isotonic regression) - cite Kuleshov 2018

7.5 Computational footprint

LLM API call: ~1–3 seconds per synthesis request; ~500–1000 input tokens; ~100–200 output tokens

No local LLM loaded - API call only; ~0MB additional RAM (vs. ~3–6GB for local Llama/Mistral)

Total synthesis step RAM: <50MB (structured data manipulation + API call)

This is the key architectural decision: using claude-sonnet-4-6 API keeps total RAM under 8GB ceiling

7.6 Evaluation (SRQ2 operationalisation)

LLM-as-Judge protocol: GPT-4o evaluates synthesis outputs on 5 dimensions (relevance, accuracy, calibration quality, actionability, clarity) - Likert 1–5

Evaluate on N=50 randomly sampled product×retailer×week combinations from test set

Baseline comparison: simple rule-based text generation (“Forecast is X units, model confidence: Y%”) - does LLM add value?

Calibration check: empirical coverage of stated 90% intervals vs. actuals in test set

Cite: ANAH (evaluation framework for LLM outputs), Hybrid AI + LLM Industrial paper

7.6.1 Result

The protocol was executed (N=50, claude-sonnet-4-6 synthesis, GPT-4o judge, temp 0). The LLM synthesis outscored the rule-based baseline on four of five dimensions - actionability 4.00 vs 2.14, relevance 4.00 vs 3.28, clarity 4.34 vs 3.46, calibration 3.74 vs 3.46 - with the baseline ahead only on accuracy (3.42 vs 2.96). Mean score 3.81 (LLM) vs 3.15 (baseline). The LLM thus adds clear value in turning a number-plus-interval into an actionable, well-framed recommendation, at the cost of a small accuracy penalty from its added interpretation. Full results and the discussion of this trade-off are in Ch8 §8.3.4.

7.7 Connection to SRQs

SRQ

How Ch.7 addresses it

SRQ2

Direct answer: multi-model synthesis → calibrated confidence score → LLM recommendation

SRQ3

Not addressed here; integration readiness is addressed in Ch3 and Ch5

SRQ4

Synthesis output (natural language + confidence) is the proposed alternative to descriptive BI dashboards

Outstanding decisions

Whether to add a 4th confidence component (forecast accuracy trend: is the model improving or degrading over time?)

Whether to include a “flag for human review” output for Low confidence recommendations

API cost ceiling: estimate per-recommendation cost and total evaluation cost (N=50 × ~$0.005/call ≈ $0.25 - negligible)

Whether synthesis outputs should be stored in a local SQLite log for reproducibility

Chapter 8 - Experimental Evaluation

8.1 Evaluation overview

Three-level evaluation framework (3-level is the thesis’s core methodological contribution to evaluation design for AI artefacts):

Level 1 - ML accuracy: are the forecasting models accurate? (SRQ1)

Level 2 - Recommendation quality: does the synthesis produce actionable, calibrated outputs? (SRQ2)

Level 3 - Agent behaviour: does the system operate within computational constraints? (SRQ1 + SRQ2)

Cite: AI-Based DSR Framework 2024 (evaluation dimensions for AI artefacts); Pathways for Design Research on AI 2024 (INFORMS ISR)

8.2 Level 1 - ML accuracy evaluation (SRQ1)

8.2.1 Benchmark design

Dataset: Nielsen CSD panel data, [N] SKUs × 28 retailers × [T] weeks

Stratification: evaluate separately by product category (regular CSD, diet, energy) and retailer tier (major chain, discount, convenience)

Test period: hold-out test set, [T_test] weeks (minimum 13 weeks - one quarter)

8.2.2 Metrics

MAPE, RMSE, MAE (see Ch.6 definitions)

Directional accuracy: % of weeks where model correctly predicts direction of change (increase/decrease/flat)

Statistical significance: Diebold-Mariano test for pairwise model comparison

8.2.3 Baselines

ARIMA: best-in-class statistical baseline

Naïve seasonal: last year’s same week (simple but competitive in seasonal FMCG data)

Manifold descriptive baseline: descriptive analytics output from current Manifold AI tool (SRQ4 - requires access to baseline outputs)

8.2.5 Results (Level 1 - SRQ1)

On the selected per-category configuration (Ch6 §6.5.6), tuned XGBoost is the best model in every category. Test WMAPE: CSD 16.5%, danskvand 22.0%, energidrikke 11.4% (≈ the ≤15% industry target), RTD 31.0%. Against the traditional baselines, the ML model beats ARIMA (CSD 24.2%, danskvand 33.4%, energidrikke 15.7%, RTD 48.2%) in three of four categories; for danskvand an additive Prophet model (16.9%) is competitive. Every model beats the SeasonalNaive baseline (e.g. CSD 39.9%, RTD 58.8%), confirming genuine learned skill rather than trend persistence. SHAP attributes the forecasts chiefly to lag_1 (last-month sales) and weighted_distribution (shelf availability) across all categories.

8.3 Level 2 - Recommendation quality evaluation (SRQ2)

8.3.1 LLM-as-Judge protocol

Evaluator: GPT-4o (independent LLM - not the same model as the Synthesis Agent to avoid self-evaluation bias)

Sample: N=50 randomly selected product×retailer×week recommendations from test period

Dimensions (Likert 1–5):

Accuracy: is the forecast number consistent with the stated confidence?

Calibration quality: does the recommendation correctly communicate uncertainty?

Actionability: does the recommendation give the category manager a clear action?

Relevance: is the provided context used appropriately?

Clarity: is the recommendation written clearly and concisely?

Cite: ANAH evaluation framework; Humans vs. LLMs (IJF 2024)

8.3.2 Calibration check

Compare stated 90% prediction intervals to actual outcomes in test set

Compute empirical coverage rate: should be 85–95% for well-calibrated outputs

Plot calibration curve (stated vs. empirical coverage across quantiles)

Cite: Kuleshov et al. 2018; Evaluating and Calibrating Uncertainty 2023 (MDPI Sensors)

8.3.3 SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst

The SRQ4 baseline is not a human analyst (that comparison is out of scope - infeasible within the project timeline). It is the production code-as-action agent, Prometheus (the Manifold/Royal Unibrew Graph Engine): a LangGraph + PydanticAI agent whose coder writes and executes SQL/Python in an E2B sandbox in an investigate-and-verify loop to answer a data/forecasting brief. SRQ4 therefore compares the dedicated-model integration (this thesis: an LLM that delegates forecasting to pre-trained XGBoost models exposed as a structured tool) against the code-as-action baseline (Prometheus: an LLM that writes its own forecasting code), on correctness, consistency, replicability, cost and latency over a common prompt set. Both run on the same Nielsen categories (CSD, danskvand, energidrikke, RTD); execution is local + sandbox, with no human-in-the-loop baseline.

8.3.4 Results (Level 2 - SRQ2)

On N=50 stratified test cases, GPT-4o (LLM-as-Judge, independent model family) scored the Synthesis-Agent recommendation against a rule-based template baseline on five Likert(1–5) dimensions:

System

accuracy

calibration

actionability

relevance

clarity

mean

LLM synthesis

2.96

3.74

4.00

4.00

4.34

3.81

Rule-based baseline

3.42

3.46

2.14

3.28

3.46

3.15

The LLM synthesis clearly adds value on actionability (4.00 vs 2.14), relevance (4.00 vs 3.28), clarity (4.34 vs 3.46) and calibration (3.74 vs 3.46) - answering the SRQ2 “does the LLM add value over a template?” question affirmatively on four of five dimensions. The baseline edges out the LLM only on accuracy (3.42 vs 2.96): the template merely restates the forecast number, so it cannot contradict its inputs, whereas the LLM’s added interpretation occasionally drifts from a strict reading of the numbers - a precision/usefulness trade-off worth stating. Interval calibration is empirically validated separately (§8.3.2 / Ch6 §6.5.4: ensemble conformal coverage 80–98% against the 90% nominal). The human-analyst comparison (§8.3.3) requires a Manifold team member and is not run here; the SRQ4 code-as-action comparator requires an execution sandbox (E2B key not configured) and is deferred.

8.4 Level 3 - Agent behaviour evaluation (SRQ1 + SRQ2)

8.4.1 RAM profiling

Tool: tracemalloc (Python standard library)

Protocol: profile each agent component separately, then full pipeline end-to-end

Measurement: peak RAM per component, peak total pipeline RAM

Target: total peak ≤8GB (hard constraint)

Report: memory profile table per component (Forecasting Agent × 5 models, Synthesis Agent, Coordinator)

8.4.2 Latency profiling

Wall-clock time for full pipeline: data load → feature engineering → model training → prediction → synthesis → recommendation

Target: end-to-end ≤5 minutes for single SKU×retailer×week forecast (reasonable for a category manager’s tool)

Separate training latency from inference latency (training once, inference per request)

8.4.3 Failure mode analysis

Deliberately trigger: API timeout (synthesis), memory pressure (all models loaded simultaneously), missing data (incomplete Nielsen week)

Document agent recovery behaviour: does the Coordinator handle gracefully? Does the system fall back to the next-best model?

8.4.4 Results (Level 3 - operational)

Peak RAM (tracemalloc) is in the tens of MB for every model - Ridge 1.5, LightGBM 18.7, XGBoost 0.2, ARIMA 0.5 MB - i.e. three orders of magnitude below the 8 GB ceiling; the constraint is non-binding at this data scale (a different result from the hypothesised 4–6 GB, because the corrected matrices are far smaller than the all-markets ones). Training latency is seconds, not minutes (XGBoost ~1.7 s, LightGBM ~7.7 s with its tuned n_estimators); inference is ~16 ms for XGBoost. The Synthesis Agent adds only structured arithmetic plus, optionally, one LLM API call (~1–3 s, no local RAM). The end-to-end pipeline therefore runs comfortably within the operational budget. Note: tracemalloc captures Python-level allocations; native LightGBM/XGBoost C++ buffers are additional but small at this scale.

(Failure-mode analysis §8.4.3 - API timeout / fallback - is part of the agentic harness evaluation and is run with the LLM-dependent layer.)

8.5 Threats to validity

Threat

Type

Mitigation

Single company dataset

External validity

Discuss generalisability scope; document data characteristics

LLM-as-Judge self-consistency

Internal validity

Use GPT-4o (different model family) as judge; evaluate inter-rater agreement with human judge on 10% sample

Temporal leakage

Internal validity

Strict temporal train/test split; no future features in training set

Demand volatility in CSD

Construct validity

Report MAPE distribution not just mean; flag high-volatility SKUs separately

Access to Manifold descriptive baseline

External validity

If not available, substitute with published descriptive analytics benchmark or Naïve seasonal

8.6 Connection to SRQs

SRQ

Evaluation evidence

SRQ1

Level 1: MAPE/RMSE/MAE vs. baselines; Level 3: RAM + latency within constraints

SRQ2

Level 2: LLM-as-Judge scores; calibration coverage; Level 3: synthesis latency

SRQ3

Not addressed here; integration readiness is addressed in Ch3 and Ch5

SRQ4

Level 2 comparison: AI system vs. human descriptive baseline on recommendation quality

Outstanding decisions

Whether N=50 is sufficient for LLM-as-Judge evaluation (statistical power consideration)

Whether to include inter-rater reliability (Cohen’s κ) between LLM judge and human judge

Data access dependency: evaluation design complete, execution blocked until Nielsen access obtained

Manifold descriptive baseline: need to discuss with Manifold AI team what form the current tool’s outputs take

Chapter 9 - Discussion

9.1 Interpretation of findings

9.1.1 SRQ1: Forecasting accuracy under constraints

Tuned XGBoost was the best model in every category, ahead of LightGBM, Ridge, and the SeasonalNaive baseline, confirming that gradient boosting over engineered lag/rolling/calendar features is the strongest lightweight family for this monthly FMCG panel. The selected per-category configurations reach test WMAPE of 16.5% (CSD), 22.0% (danskvand), 11.4% (energidrikke) and 31.0% (RTD). RTD remains hardest - short, volatile, promotion-blind series. A central and somewhat counter-intuitive result is that finer granularity does not uniformly help: disaggregating to a retail-chain dimension multiplied training rows roughly sixfold yet improved accuracy only for danskvand, while CSD, energidrikke and RTD forecast better at the aggregated brand level. This is a signal-to-noise effect - more rows of noisier per-chain demand do not beat fewer rows of a cleaner aggregate - and it motivates the per-category representation choice (Ch6 §6.5.6). On the operational axis the ≤8 GB constraint is non-binding at this data scale: peak RAM is in the tens of MB for every model and inference is sub-second, so the accuracy-optimal model also fits the budget with no compromise. SHAP attributes forecasts chiefly to last-month sales (lag_1) and shelf availability (weighted_distribution), which is consistent with retail demand dynamics and lends face validity to the models. Connect to: Edge AI / Efficient & Green LLMs (the constraint is easily met); gradient-boosting-for-retail literature.

9.1.2 SRQ2: Synthesis quality

The deterministic synthesis core produced well-to-conservatively calibrated ensemble intervals (empirical coverage 80–98% against a 90% nominal), so the uncertainty the system communicates is trustworthy. The composite confidence score skewed to the Moderate tier with no High-confidence forecasts under the current thresholds - an artefact of weighting interval tightness heavily while the conformal 90% interval is deliberately wide; the tier cut-offs, not the forecasts, are what need recalibration. On recommendation quality, the LLM synthesis added clear value over a rule-based template: GPT-4o (LLM-as-Judge, N=50) scored it higher on actionability (4.00 vs 2.14), relevance (4.00 vs 3.28), clarity (4.34 vs 3.46) and calibration (3.74 vs 3.46), with the template ahead only on accuracy (3.42 vs 2.96). The weakest LLM dimension is therefore accuracy: turning numbers into prose occasionally drifts from a strict reading of the inputs - a usefulness/precision trade-off, and the clearest target for prompt hardening. Connect to: Kuleshov 2018 (calibration); AI-augmented decision-making DSR 2024.

9.1.3 SRQ3: Integration readiness

SRQ3 is addressed as an integration-readiness assessment, not a live integration: production access to the Prometheus platform was not available and was not required for the thesis, which runs entirely on a local Nielsen snapshot. The forecasting substrate is nonetheless integration-ready in the senses Ch3/Ch5 specify - it is exposed through a structured, reproducible interface (committed scripts, deterministic seeds, versioned artefacts) and emits point forecasts plus calibrated intervals and a confidence tier suitable for an agent tool-call. The remaining gap to active integration is operational (credentials, a dev-merge into the Graph Engine), not architectural. Connect to: Ch3/Ch5 integration-readiness specification.

9.1.4 SRQ4: dedicated ML vs the LLM/traditional baselines

Against the traditional statistical baseline, dedicated ML (XGBoost) beats ARIMA in three of four categories (by 7.7, 4.3 and 17.2 pp WMAPE for CSD, energidrikke, RTD), with only danskvand better served by an additive Prophet model - so dedicated lightweight ML is, on balance, justified over classical forecasting. The code-as-action LLM baseline central to the v4 SRQ4 - an LLM that writes and self-corrects its own forecasting code - was not executed: it requires a secure execution sandbox (E2B) that is not configured. This is the principal open piece of the empirical SRQ4 answer and is carried as future work; what the present results establish is the prior, weaker comparison (dedicated ML vs traditional, and LLM synthesis vs template), both favouring the dedicated/structured approach on the decision-relevant dimensions. Connect to: Humans vs. LLMs (IJF 2024); code-as-action (Wang et al. 2024).

9.2 Theoretical contributions

9.2.1 Design knowledge contribution (DSR framing)

The multi-agent framework constitutes a DSR artefact at two levels (Hevner et al. 2004; Artifact Types in IS Design Science, LNCS 2012):

Instantiation level: a working multi-agent system (System A) running on real retail CPG data

Method/design-theory level: 5 generalised design principles reusable beyond this specific retail context

Cite: Hevner 2004, Peffers 2007, AI-Based DSR Framework 2024, Pathways for Design Research on AI 2024, Artifact Types in IS Design Science 2012

9.2.2 Design principles (generalised from thesis findings)

#

Principle

Problem class

Evidence from this thesis

DP1

Sequential execution

Multi-model ML pipelines within ≤8 GB RAM

Load → fit → predict → del → gc.collect(); measured peak RAM is tens of MB per model (Ridge 1.5, LightGBM 18.7, XGBoost 0.2 MB) - the 8 GB budget is non-binding at this data scale

DP2

Post-hoc calibration

Confidence scoring in ML-based recommendation systems

Split-conformal interval calibrated on validation residuals; ensemble achieves 80–98% empirical coverage against a 90% nominal (CSD 96.6%)

DP4

LLM-as-synthesiser

Translating ML outputs into managerial recommendations

Claude API synthesises a multi-model ensemble + confidence into an actionable natural language recommendation

DP5

Computational transparency

AI pipeline artefacts evaluated for practical deployment

RAM and latency profiling reported alongside MAPE/RMSE; tracemalloc per component

Cite: Pathways for Design Research on AI 2024 (ISR), AI-Based DSR Framework 2024, AI-augmented decision making DSR 2024

9.2.2 Novelty claims

First system to combine: LLM orchestration + ≤8GB constrained ML ensemble + MCDM synthesis + real retail CPG evaluation

Memory profiling methodology for multi-component AI pipelines: replicable protocol contribution

The ≤8GB constraint as a design principle, not an afterthought: demonstrates that SME-grade hardware is sufficient for meaningful AI-augmented BI

9.2.3 Contribution to IS literature

Extends Pathways for Design Research on AI (ISR 2024): provides an instantiated AI artefact evaluated per the editorial’s recommended dimensions

Extends AI-augmented decision making design principles (2024): applies and validates principles in a retail CPG context

9.3 Practical implications

For Manifold AI: validated architecture for integrating predictive analytics into the existing descriptive AI Colleague product

For SME retailers: demonstrates that AI-augmented demand forecasting does not require cloud-scale compute

For IS practitioners: memory profiling methodology is directly transferable to other ML pipeline deployments

9.4 Limitations

Single company/context: Nielsen CSD data from one company’s clients - generalisability untested

Data access dependency: if Nielsen access was delayed, fallback dataset may reduce ecological validity

LLM non-determinism: claude-sonnet-4-6 at temperature=0 is near-deterministic but not fully; evaluation may not fully replicate

Evaluation scope: LLM-as-Judge N=50 is statistically modest; significance claims are indicative

DSR single-cycle: full ADR would require multiple build-evaluate-reflect cycles; thesis completes one cycle

9.5 Future research directions

Multi-agent memory sharing: can agents share intermediate results to reduce redundant computation?

Real-time streaming: adapting the pipeline for continuous data ingestion vs. batch weekly

Cross-retailer generalisation: test on a different FMCG category or market

Full DSR second cycle: implement design principle refinements identified in this evaluation and re-evaluate

Outstanding decisions

Depth of theoretical contribution section: depends on how strong the empirical results are

✅ Design principles table added (section 9.2.2) - content mirrors Ch.10 section 10.2; values will be filled after empirical results

Chapter 10 - Conclusion

10.1 Summary of contributions

This thesis asked: How can production-oriented agentic decision-support systems without native predictive capabilities be extended with lightweight forecasting models to support reliable, forecast-informed, and cost-justified decision-making under computational and deployment constraints? The answer it substantiates is that a lightweight gradient-boosted forecasting substrate, exposed through a structured, calibrated interface and synthesised by an LLM, extends a non-predictive agentic system reliably and within an SME-grade resource budget - with the dedicated-model layer justified over both classical and template baselines on the decision-relevant dimensions. The sub-questions resolve as follows.

SRQ1 (models & efficiency). Tuned XGBoost is the best lightweight model in every category (test WMAPE 11.4–31.0%), beating LightGBM, Ridge and SeasonalNaive. Category specialisation matters: the best representation differs by category (brand×month for CSD/energidrikke/ RTD, brand×chain for danskvand), so “more data” via finer granularity is not uniformly better. All models run in tens of MB - the ≤8 GB constraint is non-binding.

SRQ2 (structured interface). Forecasts are exposed with point estimate, split-conformal 90% interval (empirical coverage 80–98%), and a confidence tier; an LLM synthesises these into recommendations that an independent GPT-4o judge rates above a rule-based template on four of five dimensions (mean 3.81 vs 3.15), establishing reliability and traceability with a usefulness/accuracy trade-off to manage.

SRQ3 (integration readiness). Assessed, not enacted: the substrate is reproducible and tool-call-ready; the gap to live integration with the Prometheus Graph Engine is operational (access/credentials), not architectural.

SRQ4 (dedicated ML vs baselines). Dedicated ML beats the ARIMA traditional baseline in three of four categories; the code-as-action LLM comparator - the central v4 test - requires an execution sandbox (E2B) not configured here and is the main open empirical item. On the evidence gathered, dedicated integration is justified over classical and templated alternatives.

The thesis thus delivers a working DSR design artefact plus transferable design knowledge for cost-justified, forecast-informed agentic decision-support under resource constraints; the code-as-action comparison and a production integration remain for a second cycle.

10.2 Theoretical contribution (design principles)

Propose generalisable design principles (DSR design-theory output):

Sequential execution principle: ML pipeline RAM budgets must be planned for sequential, not concurrent, model execution; a load, run, unload protocol enables sub-8GB multi-model forecasting

Delegation-over-generation principle: the LLM should orchestrate and delegate numerical prediction to dedicated models rather than generate predictions, or its own forecasting code, itself, when correctness, consistency, and replicability matter

Cost-justification principle: dedicated-model integration should be adopted only where it demonstrably beats a code-as-action LLM baseline on the decision-relevant dimensions at justified cost and latency; otherwise an LLM-plus-code approach may suffice

Structured-interface reliability principle: exposing forecasts through a structured tool/action interface with output validation and a recorded tool-call-to-recommendation mapping is what makes agentic numerical decision-support auditable

Computational transparency principle: deployment-oriented AI artefacts should report RAM, cost, and latency alongside accuracy; these are decision-relevant properties for SME adopters

Note: uncertainty calibration is a design consideration deferred to future work (see §10.5)

Cite: DSR design-theory sources (Hevner et al., 2004; Peffers et al., 2007; plus AI-DSR references)

10.3 Practical recommendations for Manifold AI

Integrate the lightweight forecasting substrate as a callable tool in the production agentic system (Prometheus) via its Graph Engine, exposing forecasts and uncertainty through the structured interface

Adopt dedicated-model integration where the SRQ4 evaluation shows it beats the code-as-action baseline on correctness, consistency, and replicability at acceptable cost; otherwise rely on the LLM-plus-code approach

Infrastructure: deployable within an approximately 8GB RAM budget (for example a t3.large-class cloud instance), no GPU required [cloud-pricing citation: resolve in global references pass]

10.4 Limitations recap

Empirical context bounded to the Danish beverage retail market (five Nielsen categories) and a single partner company

One DSR design cycle; findings require validation across additional contexts before generalisation

SRQ4 evaluation at pilot scale (on the order of fifty prompts), not a full study; results provisional pending the final improved models

SRQ3 assessed as integration readiness (production access pending), not a live integration

LLM API dependency for the agentic layer; uncertainty calibration is designed but not empirically validated

10.5 Future research

Full-scale SRQ4 evaluation across the complete prompt set; a second DSR cycle refining the design principles

Active integration into the production system (Prometheus Graph Engine) once access is granted: a before/after study on reliability and cost

Empirical calibration of forecast uncertainty (post-hoc isotonic regression), currently designed only

Adapt for streaming/real-time forecasting (currently monthly batch processing)

Code-as-action as the artefact’s own action format (replacing JSON function-calling), distinct from its use as the SRQ4 baseline, where the prototype’s 0% numerical hallucination under JSON makes the marginal benefit an open question (Wang et al., 2024)

10.6 Final statement

The thesis demonstrates how a resource-constrained agentic decision-support system can be extended with lightweight forecasting, the LLM structuring and contextualising dedicated-model predictions rather than replacing domain expertise or generating the predictions itself

This positions AI as a calibrated decision partner, not a replacement for the category manager

Close with the IS research framing: a validated DSR artefact plus design knowledge on cost-justified, forecast-informed agentic decision-support in SME retail contexts

Outstanding decisions

Exact “answer” language for each SRQ, dependent on the final empirical results

Whether to include a one-page executive summary before Chapter 1 (not counted toward page limit)

Whether to add a reflective paragraph on the collaborative human-AI research process (relevant to the philosophy-of-science section)

Reference List

Ahrens, A., Hansen, C. B., Schaffer, M. E., & Wiemann, T. (2025). Model averaging and double machine learning. Journal of Applied Econometrics, 40(3). https://doi.org/10.1002/jae.3103

Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. In Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (pp. 2623–2631). Association for Computing Machinery. https://doi.org/10.1145/3292500.3330701

Al-Karkhi, M. I., & Rządkowski, G. (2025). Innovative machine learning approaches for complexity in economic forecasting and SME growth: A comprehensive review. International Journal of Innovation Studies, 9(1), 20–28.

Barber, R. F., Candès, E. J., Ramdas, A., & Tibshirani, R. J. (2023). Conformal prediction beyond exchangeability. The Annals of Statistics, 51(2), 816–845. https://doi.org/10.1214/23-AOS2276

Bergstra, J., Bardenet, R., Bengio, Y., & Kégl, B. (2011). Algorithms for hyper-parameter optimization. In Advances in Neural Information Processing Systems (Vol. 24). Curran Associates.

Cawley, G. C., & Talbot, N. L. C. (2010). On over-fitting in model selection and subsequent selection bias in performance evaluation. Journal of Machine Learning Research, 11(70), 2079–2107.

Ceran, B., Özkan, E., Eskiocak, D. İ., Mert, B., & Yüceoğlu, B. (2024). Machine learning-based demand forecasting for an FMCG retailer. In Intelligent and Fuzzy Systems: Proceedings of INFUS 2024 (LNNS, Vol. 1090). Springer. https://doi.org/10.1007/978-3-031-67192-0_11

Chen, E., & Bibi, Z. (2026). Machine learning as a tool (MLAT): A framework for integrating statistical ML models as callable tools within LLM agent workflows. arXiv preprint arXiv:2602.14295. [PREPRINT, not peer-reviewed]

Dong, L., Lu, Q., & Zhu, L. (2024). A taxonomy of AgentOps for enabling observability of foundation model based agents. arXiv preprint arXiv:2411.05285. [PREPRINT]

Elmachtoub, A. N., & Grigas, P. (2022). Smart "predict, then optimize". Management Science, 68(1), 9–26. https://doi.org/10.1287/mnsc.2020.3922

Gneiting, T. (2011). Making and evaluating point forecasts. Journal of the American Statistical Association, 106(494), 746–762. https://doi.org/10.1198/jasa.2011.r10138

González-Potes, A., et al. (2026). Hybrid AI and LLM-enabled agent-based real-time decision support architecture for industrial batch processes. AI, 7(2), 51.

González-Potes, A., Mata-Rivera, M. F., Espinosa-Oviedo, J. A., Castellanos-Velasco, E., Alvarado-Nava, O., & Rodríguez-Reséndiz, J. (2026). Hybrid AI and LLM-enabled agent-based real-time decision support architecture for industrial batch processes. AI, 7(2), 51.

Goodwin, P., Önkal, D., & Thomson, M. (2010). Do forecasts expressed as prediction intervals improve production planning decisions? European Journal of Operational Research, 205(1), 195–201. https://doi.org/10.1016/j.ejor.2009.12.020

Gu, J., Jiang, X., Shi, Z., Tan, H., Zhai, X., Xu, C., Li, W., Shen, Y., Ma, S., Liu, H., Wang, S., Zhang, K., Wang, Y., Gao, W., Ni, L., & Guo, J. (2025). A survey on LLM-as-a-judge. arXiv preprint arXiv:2411.15594. [PREPRINT]

Guo, Z., et al. (2025). Sample, predict, then proceed: Self-verification sampling for tool use of LLMs. OpenReview. [PREPRINT]

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. MIS Quarterly, 28(1), 75–105.

Ji, Z., Gu, Y., Zhang, W., Lyu, C., Lin, D., & Chen, K. (2024). ANAH: Analytical annotation of hallucinations in large language models. In Proceedings of ACL 2024 (pp. 8135–8158).

Kartik, N., Sapra, G., Hada, R., & Pareek, N. (2025). AgentCompass: Towards reliable evaluation of agentic workflows in production. arXiv preprint arXiv:2509.14647. [PREPRINT]

Klee, S., & Xia, Y. (2025). Measuring time series forecast stability for demand planning. KDD '25 Workshop on AI for Supply Chain.

Kuleshov, V., Fenner, N., & Ermon, S. (2018). Accurate uncertainties for deep learning using calibrated regression. In Proceedings of ICML 2018 (PMLR, Vol. 80).

Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J., & Wasserman, L. (2018). Distribution-free predictive inference for regression. Journal of the American Statistical Association, 113(523), 1094–1111. https://doi.org/10.1080/01621459.2017.1307116

Levi, D., Gispan, L., Giladi, N., & Fetaya, E. (2022). Evaluating and calibrating uncertainty prediction in regression tasks. Sensors, 22(15), Article 5540. https://doi.org/10.3390/s22155540

Li, Z., et al. (2024). AutoFlow: Automated workflow generation for large language model agents. arXiv preprint arXiv:2407.12821. [PREPRINT]

Liu, S., Guo, B., Yu, Z., et al. (2025). On accelerating edge AI: Optimizing resource-constrained environments. arXiv preprint arXiv:2501.15014. [PREPRINT - not peer-reviewed]

Liu, Z., et al. (2024). A dynamic LLM-powered agent network for task-oriented agent collaboration. In First Conference on Language Modeling (CoLM 2024).

Ma, B. J., Jackson, I., Huang, M., Villegas, S., & Macias-Aguayo, J. (2025). A data-driven and context-aware approach for demand forecasting in the beverage industry. International Journal of Logistics Research and Applications.

Ma, M., et al. (2024). SciAgent: Tool-augmented language models for scientific reasoning. arXiv preprint arXiv:2402.11451. [PREPRINT]

Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2018). The M4 competition: Results, findings, conclusion and way forward. International Journal of Forecasting, 34(4), 802–808. https://doi.org/10.1016/j.ijforecast.2018.06.001

Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2020). The M4 competition: 100,000 time series and 61 forecasting methods. International Journal of Forecasting, 36(1), 54–74.

Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. International Journal of Forecasting, 38(4), 1346–1364.

Mandi, J., Kotary, J., Berden, S., Mulamba, M., Bucarey, V., Guns, T., & Fioretto, F. (2024). Decision-focused learning: Foundations, state of the art, benchmark and future opportunities. Journal of Artificial Intelligence Research, 81, 1623–1701. https://doi.org/10.1613/jair.1.15320

Mehta, S. (2025). Beyond accuracy: A multi-dimensional framework for evaluating enterprise agentic AI systems. arXiv preprint arXiv:2511.14136. [PREPRINT]

Ng, S. (2017). Opportunities and challenges: Lessons from analyzing terabytes of scanner data. NBER Working Paper, 23673.

Olszak, C. M., & Bartuś, K. (2025). AI-enhanced business intelligence for decision-making. Procedia Computer Science, 270, 415–425. https://doi.org/10.1016/j.procs.2025.09.160

Ouyang, S., Zhang, J. M., Harman, M., & Wang, M. (2025). An empirical study of the non-determinism of ChatGPT in code generation. ACM Transactions on Software Engineering and Methodology, 34(2), 42:1–42:28. https://doi.org/10.1145/3697010

Paranjape, B., Lundberg, S., Singh, S., Hajishirzi, H., Zettlemoyer, L., & Ribeiro, M. T. (2023). ART: Automatic multi-step reasoning and tool-use for large language models. arXiv preprint arXiv:2303.09014. [PREPRINT]

Pathirannehelage, S. H., Shrestha, Y. R., & von Krogh, G. (2025). Design principles for artificial intelligence-augmented decision making: An action design research study. European Journal of Information Systems, 34(2), 207–229. https://doi.org/10.1080/0960085X.2024.2330402

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. Journal of Management Information Systems, 24(3), 45–77.

Rinaldi, G., Giordano, F., De Stefano, C., & Fontanella, F. (2025). DSS4EX: A decision support system framework to explore artificial intelligence pipelines with an application in time series forecasting. Expert Systems With Applications, 269, 126421.

Sapkota, R., Roumeliotis, K. I., & Karkee, M. (2026). AI agents vs. agentic AI: A conceptual taxonomy, applications and challenges. Information Fusion, 126, Article 103599. https://doi.org/10.1016/j.inffus.2025.103599

Saunders, M. N. K., Lewis, P., & Thornhill, A. (2023). Research Methods for Business Students (9th ed.). Harlow: Pearson.

Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. In Advances in Neural Information Processing Systems 36 (NeurIPS 2023).

Semerikov, S. O., Vakaliuk, T. A., Kanevska, O. B., Ostroushko, O. A., & Kolhatin, A. O. (2025). Edge intelligence unleashed: A survey on deploying large language models in resource-constrained environments. Journal of Edge Computing, 4(2). https://doi.org/10.55056/jec.1000

Taylor, S. J., & Letham, B. (2018). Forecasting at scale. The American Statistician, 72(1), 37–45. https://doi.org/10.1080/00031305.2017.1380080

Wang, R., Chen, Y., Wang, Y., Wu, C., Fang, J., Cai, X., Gu, Q., Su, H., Zhang, A., Wang, X., Cai, X., & Chua, T.-S. (2026). AgentNoiseBench: Benchmarking robustness of tool-using LLM agents under noisy conditions. arXiv preprint arXiv:2602.11348. [PREPRINT]

Wang, X., Chen, Y., Yuan, L., Zhang, Y., Li, Y., Ji, H., & Tong, H. (2024). Executable code actions elicit better LLM agents. In Proceedings of ICML 2024.

Wang, Y., et al. (2025). ScoreFlow: Mastering LLM agent workflows via score-based preference optimization. arXiv preprint arXiv:2502.04306. [PREPRINT]

Ye, J., Wang, Y., Huang, Y., Chen, D., Zhang, Q., Moniz, N., Gao, T., Geyer, W., Huang, C., Chen, P.-Y., Chawla, N. V., & Zhang, X. (2024). Justice or prejudice? Quantifying biases in LLM-as-a-judge. arXiv preprint arXiv:2410.02736. [PREPRINT, peer-review status uncertain, verify]

Zheng, G., Almahri, S., Xu, L., Minaricova, M., & Brintrup, A. (2025). LLMs in supply chain management: Opportunities and a case study. IFAC-PapersOnLine, 59(10), 2951–2956. https://doi.org/10.1016/j.ifacol.2025.09.496

AI Use Declaration

CBS requirement: Autumn 2025 rules - must declare use of AI when required by course/programme Placement: confirm with supervisor - likely in front matter (before abstract) or as a mandatory appendix Status: DRAFT - requires supervisor confirmation on required format Last updated: 2026-03-15

Draft text (bullet form - NOT prose yet)

Heading

“Use of Artificial Intelligence in This Thesis”

What AI was used for (declaration bullets)

Claude claude-sonnet-4-6 (Anthropic) was used as a research component:

As the Synthesis Agent’s natural language generation engine - integrated into the multi-agent framework as an API call (see Chapter 7). This is NOT an assistive use; it is the research object/artefact itself.

Temperature: 0 (deterministic outputs); all prompts and outputs logged for reproducibility

Claude Code (Anthropic CLI) was used as a software development assistant during implementation:

Assisted with Python code scaffolding for System A (LangGraph, forecasting agents, synthesis pipeline)

Assisted with System B thesis production scaffolding (diagram generation scripts, compliance checks)

All code reviewed and verified by the authors; final implementation decisions are the authors’ own

No AI tools were used to generate thesis prose: all written text (arguments, analysis, discussion) was written by the authors

What AI was NOT used for

Literature search and evaluation - done manually by the authors using CBS library resources

Data analysis interpretation - conducted by the authors based on empirical results

Thesis argumentation, conclusions, or theoretical contributions - authored independently

Transparency note

The use of Claude API as a system component (Synthesis Agent) is the thesis’s primary research contribution - its behaviour, limitations, and evaluation are central to the thesis

Source code for all AI integrations is included in Appendix [X] and the project repository

Placement options (confirm with supervisor)

Option

Placement

Pros

Cons

A

Front matter (before abstract)

Maximum visibility; signals transparency

May be unusual format for CBS programme

B

End of Chapter 3 (Methodology)

Contextually appropriate; fits research design

Buried; examiners may miss it

C

Mandatory appendix

Doesn’t use page budget

CBS may require it in main text

Recommended: Option A - place in front matter, before abstract, clearly labelled.

Outstanding

Confirm with supervisor: required format and placement per programme rules

Confirm whether Anthropic/Claude must be cited as a tool (APA 7 software citation format)

Confirm scope: does declaration need to cover ALL AI use or only AI in the research object?

In the forecasting literature, explanatory or exogenous variables are predictors external to the target series itself: factors that carry information about the underlying drivers of demand, rather than being derived solely from the past values of the series being forecast (Makridakis et al., 2022; Ma et al., 2025). Typical examples in the retail demand context include promotional activity, pricing, weather, calendar effects, and macroeconomic or consumer indicators. In this thesis, the exogenous predictors used in the forecasting models comprise promotional signals (units sold under promotion and promotional intensity), distribution coverage (the Nielsen weighted-distribution metric), and calendar and seasonality signals (month, quarter, and a binary peak-month indicator derived from each category’s own observed seasonal profile); these complement the models’ autoregressive features (lagged sales and rolling statistics) derived from the historical sales series itself.↩︎

Appendix