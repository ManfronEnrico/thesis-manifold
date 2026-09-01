<!-- PROSE STRIPPED 2026-09-01 (P0044).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-01_18-50/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 2 — Literature Review: Forecast-Informed Agentic Decision-Support under Constraints
> Status: PROSE DRAFT — written 2026-04-12; §2.2 reframed 2026-06-27 to separate Ng's raw-data-volume constraint (platform scale) from the thesis's binding deployment-cost constraint (the aggregated modelling set is small; the 8GB budget binds model selection, not the realised footprint)
> Author: Claude Code (Sonnet 4.6) — requires human review before finalisation
> Word count target: ~22 standard CBS pages (~50,050 chars excl. spaces)
> All citations resolved: 0 CITATION NEEDED flags remain
> Source-level verification 2026-08-25: every claim in this chapter was checked against the cited PDF via NotebookLM; reports in `05_thesis_writing/notebookLM/01-Literature Review/`. Five claims were returned Contradicted (Ceran's MAPE benchmark, M4 on intermittent series, Goodwin on prediction intervals, the ANAH taxonomy, Levi et al. on tree models) and are corrected here; eleven in-text citations were corrected for authorship or year. Reference-list entries regenerate from Zotero and are provisional pending that refresh.

---

## 2.0 Chapter Introduction

---

## 2.1 Forecasting as Predictive Substrate in FMCG

---

## 2.2 Lightweight ML under Computational and Deployment Constraints

---

## 2.3 From Descriptive BI to Forecast-Informed Decision-Support

---

## 2.4 LLM Agents and Tool-Mediated Reasoning

---

## 2.5 Reliability, Traceability, Uncertainty, and Evaluation of Agentic Outputs

---

## 2.6 Production-Oriented Agentic Systems and Integration Readiness

---

## 2.7 Research Gap: Forecast-Informed Extension of Non-Predictive Agentic Systems

- **Predictive substrate (SRQ1): designed; benchmark to be built.** A memory-profiled benchmark of lightweight forecasting models across multiple FMCG beverage categories, characterising the accuracy–efficiency–specialization trade-off under a constrained compute budget.
- **Structured forecast-tool interface (SRQ2): designed.** A tool/action interface exposing forecasts and uncertainty to a tool-using agent, with traceability treated as an explicit design objective.
- **Integration readiness (SRQ3): designed; assessment planned.** A specification of the architectural and operational capabilities a production-oriented agentic system requires to integrate forecast-informed decision-support, to be assessed using a real production-oriented empirical case rather than a completed deployment.
- **Evaluation (SRQ4): designed; evaluation pending.** A comparison of dedicated-model agentic decision-support against a code-as-action LLM baseline, on correctness, consistency, and replicability (primary) and cost and latency (secondary), planned at the scale of a pilot in the first instance rather than a full study.

---

## 2.8 Design Science Research

---

## 2.9 Chapter Summary and Transition to Methodology

---

## References cited in this chapter

- Ahrens, A., Hansen, C. B., Schaffer, M. E., & Wiemann, T. (2025). Model averaging and double machine learning. *Journal of Applied Econometrics*, *40*(3). https://doi.org/10.1002/jae.3103
- Al-Karkhi, M. I., & Rządkowski, G. (2025). Innovative machine learning approaches for complexity in economic forecasting and SME growth: A comprehensive review. *International Journal of Innovation Studies*, *9*(1), 20–28.
- Barber, R. F., Candès, E. J., Ramdas, A., & Tibshirani, R. J. (2023). Conformal prediction beyond exchangeability. *The Annals of Statistics*, *51*(2), 816–845. https://doi.org/10.1214/23-AOS2276
- Ceran, B., Özkan, E., Eskiocak, D. İ., Mert, B., & Yüceoğlu, B. (2024). Machine learning-based demand forecasting for an FMCG retailer. In *Intelligent and Fuzzy Systems: Proceedings of INFUS 2024* (LNNS, Vol. 1090). Springer. https://doi.org/10.1007/978-3-031-67192-0_11
- Chen, E., & Bibi, Z. (2026). Machine learning as a tool (MLAT): A framework for integrating statistical ML models as callable tools within LLM agent workflows. *arXiv preprint arXiv:2602.14295*. [PREPRINT, not peer-reviewed]
- Dong, L., Lu, Q., & Zhu, L. (2024). A taxonomy of AgentOps for enabling observability of foundation model based agents. *arXiv preprint arXiv:2411.05285*. [PREPRINT]
- Elmachtoub, A. N., & Grigas, P. (2022). Smart "predict, then optimize". *Management Science*, *68*(1), 9–26. https://doi.org/10.1287/mnsc.2020.3922
- González-Potes, A., Mata-Rivera, M. F., Espinosa-Oviedo, J. A., Castellanos-Velasco, E., Alvarado-Nava, O., & Rodríguez-Reséndiz, J. (2026). Hybrid AI and LLM-enabled agent-based real-time decision support architecture for industrial batch processes. *AI*, *7*(2), 51.
- Goodwin, P., Önkal, D., & Thomson, M. (2010). Do forecasts expressed as prediction intervals improve production planning decisions? *European Journal of Operational Research*, *205*(1), 195–201. https://doi.org/10.1016/j.ejor.2009.12.020
- Gu, J., Jiang, X., Shi, Z., Tan, H., Zhai, X., Xu, C., Li, W., Shen, Y., Ma, S., Liu, H., Wang, S., Zhang, K., Wang, Y., Gao, W., Ni, L., & Guo, J. (2025). A survey on LLM-as-a-judge. *arXiv preprint arXiv:2411.15594*. [PREPRINT]
- Guo, Z., et al. (2025). Sample, predict, then proceed: Self-verification sampling for tool use of LLMs. *OpenReview*. [PREPRINT]
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly*, *28*(1), 75–105. https://doi.org/10.2307/25148625
- Ji, Z., Gu, Y., Zhang, W., Lyu, C., Lin, D., & Chen, K. (2024). ANAH: Analytical annotation of hallucinations in large language models. In *Proceedings of ACL 2024* (pp. 8135–8158).
- Kartik, N., Sapra, G., Hada, R., & Pareek, N. (2025). AgentCompass: Towards reliable evaluation of agentic workflows in production. *arXiv preprint arXiv:2509.14647*. [PREPRINT]
- Klee, S., & Xia, Y. (2025). Measuring time series forecast stability for demand planning. *KDD '25 Workshop on AI for Supply Chain*. [PREPRINT]
- Kuleshov, V., Fenner, N., & Ermon, S. (2018). Accurate uncertainties for deep learning using calibrated regression. In *Proceedings of ICML 2018* (PMLR, Vol. 80).
- Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J., & Wasserman, L. (2018). Distribution-free predictive inference for regression. *Journal of the American Statistical Association*, *113*(523), 1094–1111. https://doi.org/10.1080/01621459.2017.1307116
- Levi, D., Gispan, L., Giladi, N., & Fetaya, E. (2022). Evaluating and calibrating uncertainty prediction in regression tasks. *Sensors*, *22*(15), Article 5540. https://doi.org/10.3390/s22155540
- Li, Z., et al. (2024). AutoFlow: Automated workflow generation for large language model agents. *arXiv preprint arXiv:2407.12821*. [PREPRINT]
- Liu, S., Guo, B., Yu, Z., et al. (2025). On accelerating edge AI: Optimizing resource-constrained environments. *arXiv preprint arXiv:2501.15014*. [PREPRINT]
- Liu, Z., et al. (2024). A dynamic LLM-powered agent network for task-oriented agent collaboration. In *First Conference on Language Modeling (CoLM 2024)*.
- Ma, B. J., Jackson, I., Huang, M., Villegas, S., & Macias-Aguayo, J. (2025). A data-driven and context-aware approach for demand forecasting in the beverage industry. *International Journal of Logistics Research and Applications*. https://doi.org/10.1080/13675567.2025.2451806
- Ma, M., et al. (2024). SciAgent: Tool-augmented language models for scientific reasoning. *arXiv preprint arXiv:2402.11451*. [PREPRINT]
- Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2020). The M4 competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, *36*(1), 54–74.
- Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting*, *38*(4), 1346–1364.
- Mandi, J., Kotary, J., Berden, S., Mulamba, M., Bucarey, V., Guns, T., & Fioretto, F. (2024). Decision-focused learning: Foundations, state of the art, benchmark and future opportunities. *Journal of Artificial Intelligence Research*, *81*, 1623–1701. https://doi.org/10.1613/jair.1.15320
- Mehta, S. (2025). Beyond accuracy: A multi-dimensional framework for evaluating enterprise agentic AI systems. *arXiv preprint arXiv:2511.14136*. [PREPRINT]
- Ng, S. (2017). *Opportunities and challenges: Lessons from analyzing terabytes of scanner data* (Working Paper No. 23673). National Bureau of Economic Research. https://doi.org/10.3386/w23673
- Olszak, C. M., & Bartuś, K. (2025). AI-enhanced business intelligence for decision-making. *Procedia Computer Science*, *270*, 415–425. https://doi.org/10.1016/j.procs.2025.09.160
- Paranjape, B., Lundberg, S., Singh, S., Hajishirzi, H., Zettlemoyer, L., & Ribeiro, M. T. (2023). ART: Automatic multi-step reasoning and tool-use for large language models. *arXiv preprint arXiv:2303.09014*. [PREPRINT]
- Pathirannehelage, S. H., Shrestha, Y. R., & von Krogh, G. (2025). Design principles for artificial intelligence-augmented decision making: An action design research study. *European Journal of Information Systems*, *34*(2), 207–229. https://doi.org/10.1080/0960085X.2024.2330402
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems*, *24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302
- Rinaldi, G., Giordano, F., De Stefano, C., & Fontanella, F. (2025). DSS4EX: A decision support system framework to explore artificial intelligence pipelines with an application in time series forecasting. *Expert Systems With Applications*, *269*, 126421.
- Sapkota, R., Roumeliotis, K. I., & Karkee, M. (2026). AI agents vs. agentic AI: A conceptual taxonomy, applications and challenges. *Information Fusion*, *126*, Article 103599. https://doi.org/10.1016/j.inffus.2025.103599
- Saunders, M. N. K., Lewis, P., & Thornhill, A. (2023). *Research Methods for Business Students* (9th ed.). Harlow: Pearson.
- Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. In *Advances in Neural Information Processing Systems 36* (NeurIPS 2023).
- Semerikov, S. O., Vakaliuk, T. A., Kanevska, O. B., Ostroushko, O. A., & Kolhatin, A. O. (2025). Edge intelligence unleashed: A survey on deploying large language models in resource-constrained environments. *Journal of Edge Computing*, *4*(2). https://doi.org/10.55056/jec.1000
- Wang, R., Chen, Y., Wang, Y., Wu, C., Fang, J., Cai, X., Gu, Q., Su, H., Zhang, A., Wang, X., Cai, X., & Chua, T.-S. (2026). AgentNoiseBench: Benchmarking robustness of tool-using LLM agents under noisy conditions. *arXiv preprint arXiv:2602.11348*. [PREPRINT]
- Wang, X., Chen, Y., Yuan, L., Zhang, Y., Li, Y., Ji, H., & Tong, H. (2024). Executable code actions elicit better LLM agents. In *Proceedings of ICML 2024*.
- Wang, Y., et al. (2025). ScoreFlow: Mastering LLM agent workflows via score-based preference optimization. *arXiv preprint arXiv:2502.04306*. [PREPRINT]
- Ye, J., Wang, Y., Huang, Y., Chen, D., Zhang, Q., Moniz, N., Gao, T., Geyer, W., Huang, C., Chen, P.-Y., Chawla, N. V., & Zhang, X. (2024). Justice or prejudice? Quantifying biases in LLM-as-a-judge. *arXiv preprint arXiv:2410.02736*. [PREPRINT, peer-review status uncertain, verify]
- Zheng, G., Almahri, S., Xu, L., Minaricova, M., & Brintrup, A. (2025). LLMs in supply chain management: Opportunities and a case study. *IFAC-PapersOnLine*, *59*(10), 2951–2956. https://doi.org/10.1016/j.ifacol.2025.09.496
