# Chapter 1 — Introduction
> Status: PROSE DRAFT — written 2026-04-05, em dashes removed 2026-04-12, citation corrected 2026-04-12
> Author: Claude Code (Sonnet 4.6) — requires human review before finalisation
> Word count target: ~8 standard CBS pages (2,275 chars/page)

---

## 1.1 Background and Motivation

The accelerating adoption of artificial intelligence across business domains has fundamentally reshaped expectations for what analytical systems can and should deliver. For decades, business intelligence (BI) systems have served a primarily descriptive function: they aggregate historical data into dashboards, key performance indicator reports, and trend summaries that tell managers what has happened (Rinaldi et al., 2025). While such systems have generated substantial operational value, the growing complexity of modern markets demands something more: the ability to tell managers not just what happened, but what is likely to happen next and what they should do about it.

This transition from descriptive to predictive decision-support is particularly consequential in the fast-moving consumer goods (FMCG) sector, where demand volatility, promotional dynamics, seasonal variation, and stock keeping unit (SKU) proliferation create forecasting challenges that traditional statistical approaches struggle to address (Ma et al., 2025). In the beverage segment, the domain investigated in this thesis, demand patterns are often erratic, intermittent, and sensitive to external signals such as consumer sentiment, seasonal consumption trends, and promotional calendars. These characteristics render uniform forecasting approaches inadequate: Ma et al. (2025) demonstrate in a large-scale empirical study of a private-label beverage manufacturer that no single model dominates across all demand patterns, and that machine learning models enriched with exogenous contextual features substantially outperform statistical baselines for high-volume stable SKUs.

The broader forecasting literature confirms this directional shift. The M4 Competition, the largest empirical benchmarking study in the history of the field covering 100,000 time series and 61 forecasting methods, established that combining multiple forecasting models consistently outperforms any single best model selection, and that hybrid methods blending statistical structure with machine learning achieve the highest accuracy (Makridakis et al., 2020). Its successor, the M5 Competition, focused specifically on hierarchical retail sales forecasting using real Walmart data and produced a finding of direct relevance to this thesis: all top 50 performing submissions used LightGBM, a gradient-boosted tree ensemble method, achieving more than 14% improvement over the best statistical benchmark (Makridakis et al., 2022). Critically, the M5 results also confirmed that exogenous and explanatory variables, including promotional calendars and environmental signals, materially improved forecasting accuracy. Makridakis et al. (2020) concluded their analysis by explicitly identifying the integration of explanatory variables as the open frontier for the field: *"One thing that remains to be determined is the possible improvement in PF and PI performances that can be achieved by expanding time series forecasting to include explanatory/exogenous variables. This element could be explored in future M Competitions, thus expanding time series forecasting competitions in a new and ambitious direction."* This thesis directly responds to that call.

Yet the practical deployment of predictive AI systems in business settings faces a constraint that the academic forecasting literature has largely left unexamined: computational resource limitations. Enterprise cloud deployments capable of running large deep learning models at scale are economically inaccessible to small and medium-sized AI providers. Ng (2017), working with four terabytes of Nielsen weekly scanner data, demonstrated empirically that memory constraints are the primary binding design variable in retail scanner data analysis; even with unlimited financial resources, the full dataset cannot be loaded simultaneously, making memory-efficient algorithmic choices not merely convenient but necessary. For the realistic cloud deployment budget of an SME AI provider, a ceiling of approximately eight gigabytes of total RAM is not a worst-case assumption but a practical constraint that eliminates most transformer-based architectures and severely limits model selection options.

This constraint has received no systematic attention in the multi-agent AI literature, where frameworks for LLM-based decision support consistently assume cloud-scale compute infrastructure. The gap is not merely technical: it reflects a broader structural asymmetry in AI research, where benchmarks and system designs are validated on infrastructure available to large research labs and technology companies, while the majority of organisations that could benefit from predictive AI operate with considerably more limited resources. Bridging this asymmetry by demonstrating that reliable predictive decision-support is achievable within the resource envelope of an SME cloud deployment is itself a research contribution independent of the specific domain application. The emerging paradigm of Agentic AI, which comprises systems composed of multiple specialised agents that coordinate, communicate, and dynamically allocate sub-tasks to achieve a common goal (Sapkota et al., 2025), has demonstrated substantial promise across industrial, clinical, and scientific applications. González-Potes et al. (2026) deployed a hybrid deterministic/LLM multi-agent architecture for industrial process supervision, achieving specification compliance rates above 98% and median LLM numerical errors below 3%, validating that LLM-based decision support can meet production reliability standards when architectural design carefully separates deterministic and generative components. However, González-Potes et al. (2026) explicitly acknowledge that their architecture was designed for continuous real-time industrial process supervision and does not address predictive forecasting over historical tabular retail data, multi-criteria synthesis of competing model outputs, or resource-constrained deployment with a fixed RAM budget. This is precisely the gap this thesis addresses. The Danish retail market provides a particularly appropriate empirical context for this investigation. Denmark is a mature, highly concentrated retail market dominated by a small number of large grocery chains, in which scanner panel data, collected systematically by providers such as Nielsen, offers granular, longitudinal insight into sales dynamics at the product and retailer level. At the same time, the Danish Consumer Survey (Indeks Danmark) provides one of the most comprehensive sources of consumer attitudinal and behavioural data in Scandinavia, covering over 20,000 respondents and 6,000 variables. The co-availability of these two data sources, namely transactional scanner data and consumer survey intelligence, in a single national market creates a unique opportunity to evaluate whether the integration of heterogeneous signals from different measurement traditions can materially improve predictive decision-support in FMCG retail.

---

## 1.2 Research Problem

The commercial context motivating this research is Manifold AI, a Danish artificial intelligence company building "AI Colleagues," a conversational AI system for retail analytics currently operating at the descriptive level. The system answers questions about what has happened: sales volumes, market shares, and weighted distribution metrics; it does not forecast, does not anticipate, and does not recommend. Transitioning to predictive decision-support requires three capabilities that are currently absent: the ability to generate reliable demand forecasts under tight computational constraints; the ability to integrate heterogeneous data signals, specifically structured scanner panel data and external consumer survey signals, into a coherent analytical output; and the ability to synthesise these outputs into natural language recommendations that are actionable for non-technical business managers.

Each of these three challenges constitutes a genuine unsolved problem at the intersection of forecasting, multi-agent systems, and decision support. First, the model selection problem under RAM constraints has no established solution: the forecasting literature benchmarks models primarily on accuracy metrics, with only recent work beginning to systematically measure computational cost alongside predictive performance (Klee & Xia, 2025). Klee and Xia explicitly call for further research on production-level deployment stability, noting that *"a deeper understanding of cycle-to-cycle stability across models is an important practical consideration for forecasting models that are deployed in production systems."* Second, the integration of consumer survey signals as exogenous inputs into ML-based demand forecasting pipelines remains underexplored, a gap formally identified by Makridakis et al. (2020) as an open research frontier. Third, the synthesis of heterogeneous model outputs into confidence-scored natural language recommendations within a multi-agent architecture has been demonstrated in industrial contexts (González-Potes et al., 2026) but not in retail demand forecasting, where data sparsity, promotional non-linearity, and managerial planning horizons create distinct design requirements.

This thesis addresses these three challenges through a unified multi-agent framework that coordinates lightweight machine learning forecasting, consumer signal enrichment, and LLM-based synthesis, designed to operate within the 8GB RAM constraint that defines realistic SME cloud deployment.

---

## 1.3 Research Questions

The overarching research question guiding this thesis is:

> **Main RQ**: *How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?*

This question is decomposed into four subsidiary research questions, each targeting a specific component of the design and evaluation challenge:

**SRQ1**: *Which predictive modelling approaches provide the best balance between forecasting accuracy and computational efficiency under realistic cloud resource constraints?*

SRQ1 motivates the empirical model benchmark presented in Chapter 6, where five lightweight forecasting models (ARIMA, Prophet, LightGBM, XGBoost, and Ridge Regression) are evaluated simultaneously on forecasting accuracy (MAPE, RMSE), computational efficiency (peak RAM usage, runtime), and forecast stability (coefficient of variation across repeated runs). This tri-dimensional evaluation framework is necessary because accuracy alone is insufficient for production deployment: a model with marginally lower MAPE but substantially higher RAM usage or output instability represents a worse engineering choice in a resource-constrained environment (Klee & Xia, 2025). The five models were selected to span the space from classical statistical approaches with well-understood memory footprints (ARIMA) to gradient-boosted ensemble methods that have demonstrated state-of-the-art retail forecasting performance (LightGBM, XGBoost), ensuring that the benchmark provides actionable guidance across the full accuracy-efficiency trade-off frontier.

**SRQ2**: *How can a multi-agent architecture coordinate predictive models and heterogeneous data signals to generate actionable managerial recommendations?*

SRQ2 motivates the design and implementation of the Synthesis Module in Chapter 7, where the outputs of the forecasting models are aggregated by an LLM-orchestrated Synthesis Agent into a confidence-scored natural language recommendation. The coordination logic, shared state management, and human-approval gates are implemented via a LangGraph-based multi-agent pipeline and constitute the primary architectural contribution of the thesis. The design draws on the principle, established empirically by Makridakis et al. (2020) and theoretically by the model averaging literature (Ahrens et al., 2024), that data-driven combination of multiple model outputs is systematically superior to pre-selecting a single best model, and extends this principle to the generation of business-level recommendations rather than numerical forecasts alone.

**SRQ3**: *To what extent does additional contextual information improve the predictive and decision-support capabilities of AI systems?*

SRQ3 motivates the controlled evaluation in Chapter 7 of whether including Indeks Danmark consumer survey signals as exogenous features improves forecast accuracy and recommendation quality relative to a baseline using only Nielsen scanner data. This directly responds to the explicit call by Makridakis et al. (2020) for research on the value of explanatory variables in forecasting pipelines, and extends the M5 finding (Makridakis et al., 2022), which demonstrated that exogenous promotional and calendar variables improve retail forecasting, to a qualitatively different class of external signal: consumer attitudinal data collected through a dedicated national survey. Whether such signals, operating at a different temporal resolution and semantic level than transactional records, translate into measurable forecasting and recommendation improvements is an empirical question this thesis is positioned to answer.

**SRQ4**: *How does the proposed predictive AI system compare to traditional descriptive analytics approaches used in business intelligence systems?*

SRQ4 motivates the comparative evaluation in Chapter 8, where the multi-agent predictive framework is benchmarked against a descriptive analytics baseline representing the current state of the Manifold AI system. The comparison is conducted on defined decision quality metrics, establishing the incremental value of the predictive transition over the status quo. This sub-question is necessary to ground the technical contributions of SRQ1–SRQ3 in organisational reality: a system that is technically sophisticated but delivers no measurable improvement over simpler alternatives would not constitute a meaningful contribution to either research or practice.

---

## 1.4 Delimitation

The scope of this thesis is bounded by a set of deliberate delimitations that reflect both the practical constraints of the research setting and the methodological choices required to ensure a tractable empirical evaluation.

**Domain and geography.** The thesis focuses exclusively on the Danish carbonated soft drinks (CSD) retail market. This delimitation is driven by data availability: the Nielsen/Prometheus scanner panel covers 28 Danish retailers across approximately 36 monthly periods, providing sufficient longitudinal depth for time series forecasting while remaining manageable within the RAM constraint. The CSD category was selected in collaboration with Manifold AI as representative of the FMCG challenges the system must address, including high promotional sensitivity, seasonal demand patterns, and strong competitive dynamics, while being sufficiently bounded to permit rigorous empirical evaluation within the thesis timeline.

**Computational constraint.** The framework is constrained to a maximum of 8 gigabytes of total RAM across all simultaneously active components. This constraint explicitly excludes transformer-based deep learning architectures (including LSTM, Temporal Fusion Transformer, N-BEATS, and Chronos) that require substantially more memory at inference time. The constraint is not a convenience but a formal design criterion reflecting the realistic cloud budget of SME AI providers and is motivated by empirical precedent in the retail scanner data literature (Ng, 2017).

**Processing mode.** The framework operates on monthly batch processing of historical data, not real-time streaming. This reflects the operational planning horizon of retail demand forecasting, where tactical decisions are made on weekly or monthly cycles. Real-time data ingestion and streaming inference are explicitly out of scope.

**Deployment scope.** The thesis does not aim to produce a production-ready deployed system. The multi-agent framework is a research prototype evaluated on historical data using Design Science Research methodology (Hevner et al., 2004; Peffers et al., 2007). Its outputs are validated against defined research metrics, specifically forecast accuracy, computational efficiency, recommendation quality, and comparative performance against a descriptive baseline, but not against live business outcomes.

**Generalisability.** The thesis does not address other FMCG categories, other national markets, or data sources beyond the Nielsen scanner panel and Indeks Danmark consumer survey. Generalisation of the framework's findings to other retail contexts is a direction for future research.

---

## 1.5 Thesis Structure

The remainder of this thesis is organised into nine chapters, each corresponding to a distinct phase of the Design Science Research process (Peffers et al., 2007).

**Chapter 2** presents a structured literature review across five research angles: multi-agent and LLM-based decision support, predictive modelling for retail FMCG, ensemble methods and model averaging, multi-criteria decision synthesis, and design science methodology. This review establishes the theoretical foundations and academic gap that the thesis addresses.

**Chapter 3** details the research methodology, grounding the thesis within Design Science Research and specifying the data sources, preprocessing pipeline, evaluation metrics, and three-level validation framework that govern all subsequent empirical work.

**Chapter 4** presents the data assessment, characterising the quality, structure, and forecasting suitability of the Nielsen scanner data and Indeks Danmark consumer survey, and documenting all preprocessing decisions that inform the modelling phases.

**Chapter 5** describes the multi-agent framework design, specifying the architecture of the four research agents and their coordination logic, and justifying all architectural choices against the 8GB RAM constraint and the requirements established in Chapters 2 and 3.

**Chapter 6** addresses SRQ1 through an empirical model benchmark, comparing five lightweight forecasting models across accuracy, computational efficiency, and stability metrics, and identifying the optimal model configuration for the Danish CSD context.

**Chapter 7** addresses SRQ2 and SRQ3 through the Context-Aware Decision Synthesis module, evaluating the Synthesis Agent's ability to coordinate model outputs and consumer signals into confidence-scored managerial recommendations, and quantifying the marginal value of Indeks Danmark enrichment.

**Chapter 8** addresses SRQ4 through a comparative evaluation of the predictive framework against a descriptive analytics baseline, assessing the incremental decision quality improvement achieved by the predictive transition.

**Chapter 9** discusses the theoretical contributions, practical implications, and limitations of the thesis, situating the findings within the broader literature and identifying concrete directions for future research.

**Chapter 10** concludes the thesis by synthesising answers to all four subsidiary research questions and the main research question, and reflecting on the broader implications for AI-augmented business intelligence in resource-constrained environments.

---

## References cited in this chapter

- González-Potes, A., et al. (2026). Hybrid AI and LLM-enabled agent-based real-time decision support architecture for industrial batch processes. *AI*, *7*(2), 51.
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly*, *28*(1), 75–105.
- Ahrens, A., Hansen, C. B., Schaffer, M. E., & Wiemann, T. (2024). Model averaging and double machine learning. *Journal of Applied Econometrics*. https://doi.org/10.48550/arXiv.2401.01645
- Sapkota, R., Roumeliotis, K. I., & Karkee, M. (2025). AI agents vs. agentic AI: A conceptual taxonomy, applications and challenges. *Information Fusion*, *126*, Article 103599. https://doi.org/10.1016/j.inffus.2025.103599
- Klee, S., & Xia, Y. (2025). Measuring time series forecast stability for demand planning. *KDD '25 Workshop on AI for Supply Chain*.
- Ma, B. J., Jackson, I., Huang, M., Villegas, S., & Macias-Aguayo, J. (2025). A data-driven and context-aware approach for demand forecasting in the beverage industry. *International Journal of Logistics Research and Applications*.
- Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2020). The M4 competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, *36*(1), 54–74.
- Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting*, *38*(4), 1346–1364.
- Ng, S. (2017). Opportunities and challenges: Lessons from analyzing terabytes of scanner data. *NBER Working Paper*, *23673*.
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems*, *24*(3), 45–77.
- Rinaldi, G., Giordano, F., De Stefano, C., & Fontanella, F. (2025). DSS4EX: A decision support system framework to explore artificial intelligence pipelines with an application in time series forecasting. *Expert Systems With Applications*, *269*, 126421.
