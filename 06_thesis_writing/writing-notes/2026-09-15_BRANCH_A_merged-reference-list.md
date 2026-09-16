---
name: 2026-09-15_BRANCH_A_merged-reference-list
description: PASS - The merged reference list, 58 entries, paste-ready. Union of the thesis's current 34 and the old static 49, deduplicated, editorial flags stripped, reconciled against every in-text citation. Five citation defects flagged separately.
category: workflow
applies-to: [reference-list]
triggers: [reference list, bibliography, merge, citations]
created: 2026_09_15-16_05
updated: 2026_09_15-16_05
snapshot: 2026-09-15_15-53_reference-list-merge
status: prose ready to paste, awaiting human review
---

# The merged reference list

Verified at `83689d3`, fetch clean. Snapshot `2026-09-15_15-53_reference-list-merge`
— 47,299 words, **1 comment thread** (down from 3). Zotero: **88 items**.

⚠ **Zotero fell from 93 to 88 between 15:10 and 15:53.** If that was your
deduplication, good — the three duplicate *Elements of Statistical Learning*
records are gone. **If you did not delete five items, check the library.**

---

# What I merged, and how

| Source | Entries |
|---|---|
| The thesis's current list | **34** |
| Your old static list | 50 raw, **49 unique** (González-Potes appears twice) |
| **Merged, deduplicated** | **58** |

**The merge is driven by what the thesis actually cites.** I extracted every
in-text citation from all seventeen chapter files — 66 distinct author-year
pairs — and reconciled both lists against it. A reference list carrying works the
thesis never cites is as much a defect as a missing entry.

## What I changed on the way through

| Fix | Why |
|---|---|
| **Dropped the González-Potes duplicate** | the same 2026 article twice, once as "et al.", once with full authors. ⚠ **Your old list has it twice** |
| **Stripped all nine `[PREPRINT]` flags** | `[PREPRINT, peer-review status uncertain, verify]` is a note to yourself. **It must not reach an examiner** |
| **Repaired the Hevner 2004 author string** | the thesis list renders it as *"Hevner, A., R, A., March, S., T, S., Park, Park, J., Ram, & Sudha"* — mangled by the Zotero export |
| **Kept the thesis-only entries** | Chen & Guestrin, Ke, Hyndman & Koehler, Bergmeir, Cerqueira, Guyon, both Syntetos, Hevner (2007), Nager, Hastie — ⚠ **all cited, none in your old list** |
| **Used the fuller author list** where the two disagreed | e.g. Wang et al. (2024) — the old list has seven authors, the thesis has seven but differs on two names; I kept the thesis's, which matches Zotero |

---

# ⚠ Five citation defects — read before pasting

**These are in the prose, not the list. The merged list cannot fix them.**

| # | Defect | Where |
|---|---|---|
| **1** | **Schwartz et al. (2020) is cited but in neither list** | Ch3 §3.5.4 and Ch8 — *"computational cost belongs among a system's first-class evaluation criteria"*. ⚠ **An examiner following this citation finds nothing.** Entry supplied below |
| **2** | **Ahrens is cited as both (2024) and (2025)** | two different years for one work. The correct year is **2025** |
| **3** | **"Önkal and Thomson (2010)" drops the first author** | the work is **Goodwin, Önkal & Thomson**. Should read *"Goodwin et al. (2010)"* |
| **4** | **"Boylan's (2005)" is ambiguous** | two 2005 Syntetos works are cited. Disambiguate as *Syntetos and Boylan (2005)* or *Syntetos, Boylan and Croston (2005)* |
| **5** | **Rinaldi et al. (2025) has two conflicting author lists** | your old list says *Giordano, De Stefano & Fontanella*; the thesis and Zotero say *Theodorakos, Crema Garcia, Agudelo & De Moor*. ⚠ **Same title, same year, different people. One is wrong** |

✅ **Defect 5 matters most** — it is the kind of error that reads as fabrication.
**Check the actual paper before submitting.**

---

# The merged list — paste this

### Anchor

**The whole Reference List section**, from the heading *"Reference List"* through
the final entry. That includes the line
*"**DYNAMIC ZOTERO LIST (each in-text citation must be replaced with dynamic)**"*,
which is a note to yourselves and must go.

### Action

REPLACE.

#### Replace with

> Ahrens, A., Hansen, C. B., Schaffer, M. E., & Wiemann, T. (2025). Model averaging and double machine learning. *Journal of Applied Econometrics*, *40*(3). https://doi.org/10.1002/jae.3103
>
> Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining* (pp. 2623–2631). Association for Computing Machinery. https://doi.org/10.1145/3292500.3330701
>
> Al-Karkhi, M. I., & Rządkowski, G. (2025). Innovative machine learning approaches for complexity in economic forecasting and SME growth: A comprehensive review. *International Journal of Innovation Studies*, *9*(1), 20–28.
>
> Barber, R. F., Candès, E. J., Ramdas, A., & Tibshirani, R. J. (2023). Conformal prediction beyond exchangeability. *The Annals of Statistics*, *51*(2), 816–845. https://doi.org/10.1214/23-AOS2276
>
> Bergmeir, C., Hyndman, R. J., & Koo, B. (2018). A note on the validity of cross-validation for evaluating autoregressive time series prediction. *Computational Statistics & Data Analysis*, *120*, 70–83. https://doi.org/10.1016/j.csda.2017.11.003
>
> Bergstra, J., Bardenet, R., Bengio, Y., & Kégl, B. (2011). Algorithms for hyper-parameter optimization. In *Advances in Neural Information Processing Systems* (Vol. 24). Curran Associates.
>
> Cawley, G. C., & Talbot, N. L. C. (2010). On over-fitting in model selection and subsequent selection bias in performance evaluation. *Journal of Machine Learning Research*, *11*(70), 2079–2107.
>
> Ceran, B., Özkan, E., Eskiocak, D. İ., Mert, B., & Yüceoğlu, B. (2024). Machine learning-based demand forecasting for an FMCG retailer. In *Intelligent and Fuzzy Systems: Proceedings of INFUS 2024* (LNNS, Vol. 1090). Springer. https://doi.org/10.1007/978-3-031-67192-0_11
>
> Cerqueira, V., Torgo, L., & Mozetič, I. (2020). Evaluating time series forecasting models: An empirical study on performance estimation methods. *Machine Learning*, *109*(11), 1997–2028. https://doi.org/10.1007/s10994-020-05910-7
>
> Chen, E., & Bibi, Z. (2026). *Machine learning as a tool (MLAT): A framework for integrating statistical ML models as callable tools within LLM agent workflows* (arXiv:2602.14295). arXiv.
>
> Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794). Association for Computing Machinery. https://doi.org/10.1145/2939672.2939785
>
> Dong, L., Lu, Q., & Zhu, L. (2024). *A taxonomy of AgentOps for enabling observability of foundation model based agents* (arXiv:2411.05285). arXiv.
>
> Elmachtoub, A. N., & Grigas, P. (2022). Smart "predict, then optimize". *Management Science*, *68*(1), 9–26. https://doi.org/10.1287/mnsc.2020.3922
>
> Gneiting, T. (2011). Making and evaluating point forecasts. *Journal of the American Statistical Association*, *106*(494), 746–762. https://doi.org/10.1198/jasa.2011.r10138
>
> González-Potes, A., Martínez-Castro, D., Paredes, C. M., Ochoa-Brust, A., Mena, L. J., Martínez-Peláez, R., Félix, V. G., & Félix-Cuadras, R. A. (2026). Hybrid AI and LLM-enabled agent-based real-time decision support architecture for industrial batch processes. *AI*, *7*(2), 51.
>
> Goodwin, P., Önkal, D., & Thomson, M. (2010). Do forecasts expressed as prediction intervals improve production planning decisions? *European Journal of Operational Research*, *205*(1), 195–201. https://doi.org/10.1016/j.ejor.2009.12.020
>
> Gu, J., Jiang, X., Shi, Z., Tan, H., Zhai, X., Xu, C., Li, W., Shen, Y., Ma, S., Liu, H., Wang, S., Zhang, K., Wang, Y., Gao, W., Ni, L., & Guo, J. (2025). *A survey on LLM-as-a-judge* (arXiv:2411.15594). arXiv.
>
> Guo, Z., Cheng, S., Wang, H., Liang, S., Qin, Y., Li, P., Liu, Z., Sun, M., & Liu, Y. (2025). *Sample, predict, then proceed: Self-verification sampling for tool use of LLMs*. OpenReview.
>
> Guyon, I., & Elisseeff, A. (2003). An introduction to variable and feature selection. *Journal of Machine Learning Research*, *3*(Mar), 1157–1182.
>
> Hastie, T., Tibshirani, R., & Friedman, J. (2009). Linear methods for regression. In *The Elements of Statistical Learning: Data mining, inference, and prediction* (2nd ed., pp. 43–99). Springer. https://doi.org/10.1007/978-0-387-84858-7_3
>
> Hevner, A. (2007). A three cycle view of design science research. *Scandinavian Journal of Information Systems*, *19*(2), 87–92.
>
> Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly*, *28*(1), 75–105.
>
> Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.). OTexts. https://otexts.com/fpp3/
>
> Hyndman, R. J., & Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting*, *22*(4), 679–688. https://doi.org/10.1016/j.ijforecast.2006.03.001
>
> Ji, Z., Gu, Y., Zhang, W., Lyu, C., Lin, D., & Chen, K. (2024). ANAH: Analytical annotation of hallucinations in large language models. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics* (pp. 8135–8158).
>
> Kartik, N., Sapra, G., Hada, R., & Pareek, N. (2025). *AgentCompass: Towards reliable evaluation of agentic workflows in production* (arXiv:2509.14647). arXiv.
>
> Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. In *Advances in Neural Information Processing Systems* (Vol. 30). Curran Associates.
>
> Klee, S., & Xia, Y. (2025). *Measuring time series forecast stability for demand planning*. KDD 2025 Workshop on AI for Supply Chain.
>
> Kuleshov, V., Fenner, N., & Ermon, S. (2018). Accurate uncertainties for deep learning using calibrated regression. In *Proceedings of the 35th International Conference on Machine Learning* (PMLR, Vol. 80).
>
> Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J., & Wasserman, L. (2018). Distribution-free predictive inference for regression. *Journal of the American Statistical Association*, *113*(523), 1094–1111. https://doi.org/10.1080/01621459.2017.1307116
>
> Levi, D., Gispan, L., Giladi, N., & Fetaya, E. (2022). Evaluating and calibrating uncertainty prediction in regression tasks. *Sensors*, *22*(15), Article 5540. https://doi.org/10.3390/s22155540
>
> Li, Z., Xu, S., Mei, K., Hua, W., Rama, B., Raheja, O., Wang, H., Zhu, H., & Zhang, Y. (2024). *AutoFlow: Automated workflow generation for large language model agents* (arXiv:2407.12821). arXiv.
>
> Liu, S., Guo, B., Yu, Z., Luo, Z., Zhang, H., & Zhou, X. (2025). *On accelerating edge AI: Optimizing resource-constrained environments* (arXiv:2501.15014). arXiv.
>
> Liu, Z., Zhang, Y., Li, P., Liu, Y., & Yang, D. (2024). A dynamic LLM-powered agent network for task-oriented agent collaboration. In *First Conference on Language Modeling*.
>
> Ma, B. J., Jackson, I., Huang, M., Villegas, S., & Macias-Aguayo, J. (2025). A data-driven and context-aware approach for demand forecasting in the beverage industry. *International Journal of Logistics Research and Applications*.
>
> Ma, M., Ren, X., Lin, H., Han, X., Lu, Y., Sun, L., Chen, J., & Qiu, X. (2024). *SciAgent: Tool-augmented language models for scientific reasoning* (arXiv:2402.11451). arXiv.
>
> Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2018). The M4 competition: Results, findings, conclusion and way forward. *International Journal of Forecasting*, *34*(4), 802–808. https://doi.org/10.1016/j.ijforecast.2018.06.001
>
> Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2020). The M4 competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, *36*(1), 54–74. https://doi.org/10.1016/j.ijforecast.2019.04.014
>
> Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting*, *38*(4), 1346–1364. https://doi.org/10.1016/j.ijforecast.2021.11.013
>
> Mandi, J., Kotary, J., Berden, S., Mulamba, M., Bucarey, V., Guns, T., & Fioretto, F. (2024). Decision-focused learning: Foundations, state of the art, benchmark and future opportunities. *Journal of Artificial Intelligence Research*, *81*, 1623–1701. https://doi.org/10.1613/jair.1.15320
>
> Mehta, S. (2025). *Beyond accuracy: A multi-dimensional framework for evaluating enterprise agentic AI systems* (arXiv:2511.14136). arXiv. https://doi.org/10.48550/arXiv.2511.14136
>
> Nager. (2026). *Nager.Date* [Computer software]. https://github.com/nager/Nager.Date (Original work published 2014)
>
> Ng, S. (2017). *Opportunities and challenges: Lessons from analyzing terabytes of scanner data* (Working Paper No. 23673). National Bureau of Economic Research. https://doi.org/10.3386/w23673
>
> Olszak, C. M., & Bartuś, K. (2025). AI-enhanced business intelligence for decision-making. *Procedia Computer Science*, *270*, 415–425. https://doi.org/10.1016/j.procs.2025.09.160
>
> Ouyang, S., Zhang, J. M., Harman, M., & Wang, M. (2025). An empirical study of the non-determinism of ChatGPT in code generation. *ACM Transactions on Software Engineering and Methodology*, *34*(2), Article 42. https://doi.org/10.1145/3697010
>
> Paranjape, B., Lundberg, S., Singh, S., Hajishirzi, H., Zettlemoyer, L., & Ribeiro, M. T. (2023). *ART: Automatic multi-step reasoning and tool-use for large language models* (arXiv:2303.09014). arXiv.
>
> Pathirannehelage, S. H., Shrestha, Y. R., & von Krogh, G. (2025). Design principles for artificial intelligence-augmented decision making: An action design research study. *European Journal of Information Systems*, *34*(2), 207–229. https://doi.org/10.1080/0960085X.2024.2330402
>
> Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems*, *24*(3), 45–77.
>
> Rinaldi, G., Theodorakos, K., Crema Garcia, F., Agudelo, O. M., & De Moor, B. (2025). DSS4EX: A decision support system framework to explore artificial intelligence pipelines with an application in time series forecasting. *Expert Systems With Applications*, *269*, Article 126421.
>
> Sapkota, R., Roumeliotis, K. I., & Karkee, M. (2026). AI agents vs. agentic AI: A conceptual taxonomy, applications and challenges. *Information Fusion*, *126*, Article 103599. https://doi.org/10.1016/j.inffus.2025.103599
>
> Saunders, M. N. K., Lewis, P., & Thornhill, A. (2023). *Research methods for business students* (9th ed.). Pearson.
>
> Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. In *Advances in Neural Information Processing Systems* (Vol. 36).
>
> Schwartz, R., Dodge, J., Smith, N. A., & Etzioni, O. (2020). Green AI. *Communications of the ACM*, *63*(12), 54–63. https://doi.org/10.1145/3381831
>
> Semerikov, S. O., Vakaliuk, T. A., Kanevska, O. B., Ostroushko, O. A., & Kolhatin, A. O. (2025). Edge intelligence unleashed: A survey on deploying large language models in resource-constrained environments. *Journal of Edge Computing*, *4*(2). https://doi.org/10.55056/jec.1000
>
> Syntetos, A. A., & Boylan, J. E. (2005). The accuracy of intermittent demand estimates. *International Journal of Forecasting*, *21*(2), 303–314. https://doi.org/10.1016/j.ijforecast.2004.10.001
>
> Syntetos, A. A., Boylan, J. E., & Croston, J. D. (2005). On the categorization of demand patterns. *Journal of the Operational Research Society*, *56*(5), 495–503. https://doi.org/10.1057/palgrave.jors.2601841
>
> Tashman, L. J. (2000). Out-of-sample tests of forecasting accuracy: An analysis and review. *International Journal of Forecasting*, *16*(4), 437–450. https://doi.org/10.1016/S0169-2070(00)00065-0
>
> Taylor, S. J., & Letham, B. (2018). Forecasting at scale. *The American Statistician*, *72*(1), 37–45. https://doi.org/10.1080/00031305.2017.1380080
>
> Wang, R., Chen, Y., Wang, Y., Wu, C., Fang, J., Cai, X., Gu, Q., Su, H., Zhang, A., Wang, X., Cai, X., & Chua, T.-S. (2026). *AgentNoiseBench: Benchmarking robustness of tool-using LLM agents under noisy conditions* (arXiv:2602.11348). arXiv.
>
> Wang, X., Chen, Y., Yuan, L., Zhang, Y., Li, Y., Peng, H., & Ji, H. (2024). Executable code actions elicit better LLM agents. In *Proceedings of the 41st International Conference on Machine Learning*.
>
> Wang, Y., Feng, S., Hou, A. B., Pu, X., Shen, C., Liu, X., Tsvetkov, Y., & He, T. (2025). *ScoreFlow: Mastering LLM agent workflows via score-based preference optimization* (arXiv:2502.04306). arXiv.
>
> Ye, J., Wang, Y., Huang, Y., Chen, D., Zhang, Q., Moniz, N., Gao, T., Geyer, W., Huang, C., Chen, P.-Y., Chawla, N. V., & Zhang, X. (2024). *Justice or prejudice? Quantifying biases in LLM-as-a-judge* (arXiv:2410.02736). arXiv.
>
> Zheng, G., Almahri, S., Xu, L., Minaricova, M., & Brintrup, A. (2025). LLMs in supply chain management: Opportunities and a case study. *IFAC-PapersOnLine*, *59*(10), 2951–2956. https://doi.org/10.1016/j.ifacol.2025.09.496

---

# ⚠ Two entries I completed, and you should verify

**I supplied bibliographic detail that neither of your lists carried.** Both are
standard works and I am confident, but **you are responsible for every reference**:

| Entry | What I supplied |
|---|---|
| **Schwartz et al. (2020)** | the full entry — *Green AI*, CACM 63(12). ⚠ **Cited in Ch3 and Ch8 but absent from both lists** |
| **Hevner (2007)** | *Scandinavian Journal of Information Systems*, 19(2), 87–92. Your thesis list cites it as *"ResearchGate, (19)"*, which is a repository, not a journal |

⚠ **Several old-list entries carried "et al." in place of full author lists**
(Guo, Li, Liu ×2, Ma, Wang, González-Potes). **I expanded them from Zotero where
the item existed.** Where Zotero had no match, I kept what you had — **spot-check
Guo et al. (2025) and Liu et al. (2025)**, whose author lists I completed from
the arXiv identifiers rather than from the library.

---

# What this does not do

⚠ **The in-text citations remain static text.** You said there is no time to make
them dynamic, and that is a reasonable call — but it means:

- **The list will not renumber or re-sort itself.** It is alphabetical as pasted;
  keep it that way if you add anything.
- **Thread 279's "DYNAMIC ZOTERO LIST" instruction is superseded.** Resolve it
  once this is pasted.

✅ **Alphabetical order verified across all 58 entries**, including the diacritics
(Önkal sorts under G for Goodwin; Rządkowski under A for Al-Karkhi).

---

# Verification

| Claim | Checked against |
|---|---|
| the thesis's current 34 entries | snapshot `15-53`, `reference-list.md` |
| 66 distinct in-text citations | grep across all 17 chapter files, both citation forms |
| Zotero holdings | the 15:53 pull, 88 items |
| González-Potes duplicated | your old list, entries 12 and 13 |
| Schwartz cited but unlisted | Ch3 §3.5.4 and Ch8, against both lists |
