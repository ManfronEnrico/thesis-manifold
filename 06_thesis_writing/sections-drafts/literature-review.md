<!-- PROSE STRIPPED 2026-09-01 (P0044); ARGUMENT BULLETS REBUILT 2026-09-05 (P0045).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-05_19-52_complete-review-pass/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 2 — Literature Review: Forecast-Informed Agentic Decision-Support under Constraints

> **P0044 OPEN (2026-09-01): RAM figure needs reconciling.** This file states an
> 8 GB budget. That number is a project assumption, not a sourced one -- Ng (2017)
> argues memory is the binding design variable, not that SMEs get 8 GB. Manifold's
> production Prometheus E2B template is provisioned at a **measured 4096 MB**
> (`fxe7gzkqjupdhbx4uvpr`, verified live 2026-09-01). Prefer the measured figure.
> All results hold under the tighter bound (serving 36.8 MB, refit ~37 MB).
> See `plans/P0044_2026-09-01_17-10_resource-measurement-and-retrain-arms/findings.md` F22-F23.

> **P0045 (2026-09-05):** §2.2 in the 19-52 snapshot now reads "on the order of four
> gigabytes", so the .docx half of N11 is done. This file's own 8 GB references are the
> remaining half. Bullets below were rebuilt from that snapshot; 12 hollow sections filled.

> Status: PROSE DRAFT — written 2026-04-12; §2.2 reframed 2026-06-27 to separate Ng's raw-data-volume constraint (platform scale) from the thesis's binding deployment-cost constraint (the aggregated modelling set is small; the 8GB budget binds model selection, not the realised footprint)
> Author: Claude Code (Sonnet 4.6) — requires human review before finalisation
> Word count target: ~22 standard CBS pages (~50,050 chars excl. spaces)
> All citations resolved: 0 CITATION NEEDED flags remain
> Source-level verification 2026-08-25: every claim in this chapter was checked against the cited PDF via NotebookLM; reports in `05_thesis_writing/notebookLM/01-Literature Review/`. Five claims were returned Contradicted (Ceran's MAPE benchmark, M4 on intermittent series, Goodwin on prediction intervals, the ANAH taxonomy, Levi et al. on tree models) and are corrected here; eleven in-text citations were corrected for authorship or year. Reference-list entries regenerate from Zotero and are provisional pending that refresh.

---

## 2.0 Chapter Introduction

**Claims**
- The chapter establishes a design space and identifies an **under-addressed
  intersection**, not a single missing result -- this framing matters, because the
  gap claim is otherwise easy to attack
- Six strands are reviewed, each mapped to an SRQ, then intersected in 2.7

**Warrant**
- Framing the contribution as an intersection is defensible where a "nobody has done
  X" claim would not be: each strand individually is well populated

---

## 2.1 Forecasting as Predictive Substrate in FMCG

*Maps to SRQ1*

**Claims**
- Relative model performance depends on series characteristics: temporal regularity,
  exogenous feature availability, training-set size, inference-time compute
- The five-model substrate (ARIMA, Prophet, LightGBM, XGBoost, Ridge) spans classical
  statistical to gradient-boosted, chosen to cover the accuracy-efficiency frontier
- Three substrate choices follow from the competition evidence: **benchmark multiple
  models** rather than pre-select one, **include LightGBM** as a primary candidate,
  **incorporate exogenous features where available**
- Stability is a production-relevant criterion **alongside** accuracy, not after it

**Warrant**
- **M4 (Makridakis et al. 2020)**: combining beats any single best model; hybrids of
  statistical structure + ML win. *Scope bound stated precisely*: low-volume and
  intermittent series were **excluded** from M4, and the authors caution the findings
  are for continuous business series
- Therefore evidence on irregular series here rests on **M5, not M4** -- this is a
  deliberate correction (NotebookLM returned the earlier M4-on-intermittent claim as
  Contradicted)
- **M5 (Makridakis et al. 2022)**: all top-50 used LightGBM; all beat the best
  statistical benchmark by >14%; exogenous promo/calendar features outperformed
  sales-history-only; **cross-learning beat series-by-series at lower cost** -- the
  direct precedent for SRQ1's pooled-vs-per-category comparison
- **Ceran et al. (2024)**: LightGBM + Optuna on ~14M daily series, wRMSSE 0.83 -> 0.81
  ensembled. They **reject MAPE** because too many zero-demand observations make a
  percentage error undefined. Ch6 hits the same problem on the Nielsen panel
- **Ma et al. (2025)**: beverage sector; no single model dominates across demand
  patterns -> motivates category-specialised evaluation
- **Al-Karkhi & Rzadkowski (2025)**: 120+ papers; LightGBM/XGBoost suit short-horizon
  forecasting with limited observations -- this thesis's regime (~3 years monthly)
- **Ahrens et al. (2025)**: stacking diverse learners lowers MSPE. *Transfer stated
  honestly*: their setting is double ML for causal inference, so it transfers as a
  general argument for pooling estimators against misspecification, **not** as direct
  forecasting evidence
- **Klee & Xia (2025)**: stability = CV of forecasts under identical inputs, seed varied.
  *Direction is easily inverted and must not be*: ARIMA is deterministic and therefore
  trivially stable (CV=0); deep forecasters vary by seed. Their contribution is that
  ensembling recovers stability to <5% without costing accuracy

**Evidence**
- Substrate justification and why the ladder narrows -> [[srq1-model-ladder-and-baselines]]
- Pooled vs per-category result and the metric disagreement it exposes
  -> [[srq1-pooled-vs-per-category]]

**Open**
- P0043 thread 66/69: this section is read as an argument **for** exogenous enrichment
  that the thesis does not deliver. Either narrow the claim to promo+calendar (which
  are real) or add the enrichment. See Ch1 OPEN REWRITE NOTES item 2
- Any model with a stochastic fitting procedure -- gradient-boosted trees included --
  must have seed sensitivity **measured, not assumed**. P0044 F21 measured 3.97pp of
  seed-driven wMAPE movement, which is larger than several effects the thesis reports

---

## 2.2 Lightweight ML under Computational and Deployment Constraints

*Maps to SRQ1 and Main RQ*

**Claims**
- Computational efficiency is a **binding consideration, not an afterthought**
- The relevant budget for an SME provider is a modest cloud instance, not data-centre
  scale as much of the agent literature assumes
- The budget constrains the **model-selection space** -- ruling out transformer and
  locally-hosted options at design time -- rather than being a limit the selected
  models approach in practice
- Accessing the LLM through an external API rather than loading it locally is the
  viable pattern under a small fixed budget

**Warrant**
- **Ng (2017)** establishes memory as a legitimate, domain-grounded design variable in
  retail scanner analysis. *Two levels must be distinguished, and the chapter does so*:
  Ng's constraint is **raw-data volume** at full-panel platform scale; this thesis
  aggregates to a few thousand rows per category, where volume no longer binds. What
  binds here is **deployment cost**
- This distinction is what keeps the Ng citation honest -- it supports "a memory budget
  is legitimate", not "SMEs get N gigabytes"
- **Liu et al. (2025)**: quantisation/distillation preserve accuracy at sharply reduced
  footprints
- **Semerikov et al. (2025)**: even aggressively compressed LLMs need ~1-4 GB --
  therefore local LLM inference cannot share a small budget with data + models

**Open**
- **N11 (below) is still live**: the section states the budget as "on the order of four
  gigabytes", which now matches the measured production template (P0044 F22-F23). Confirm
  every remaining 8 GB mention in this chapter is gone
- P0043 threads 71/72/73: the hosting-cost argument describes a situation Manifold is
  **not** in -- it calls the OpenAI API and hosts no LLM. Thread 73 notes this makes the
  preceding hosting claims "a bit less" relevant. The cost-asymmetry passage needs to
  argue the *selection-space* point, not a hosting bill the project never pays

---

## 2.3 From Descriptive BI to Forecast-Informed Decision-Support

*Maps to Main RQ and SRQ4*

**Claims**
- Predictive models create value **primarily through their connection to downstream
  decisions**
- But that literature couples prediction and decision **tightly** -- differentiable
  optimization against a formally specified objective, presuming a single well-defined
  program
- Managerial FMCG decision-support rarely presents such a program: decisions are
  open-ended, context-dependent, human-mediated
- This thesis therefore investigates a **loose, agent-mediated** coupling: conventionally
  trained models, surfaced to a layer that reasons over them
- An interval handed to a planner as a bare numeric range is **not self-interpreting**;
  the interpretive step between interval and decision is where the decision value sits

**Warrant**
- **Elmachtoub & Grigas (2022)**, smart predict-then-optimize: minimising prediction
  error is *not* equivalent to maximising decision quality
- **Mandi et al. (2024)** (JAIR survey): zero prediction loss implies zero decision loss,
  **but not the converse**; no method dominates
- **Rinaldi et al. (2025)** DSS4EX: explanatory layers improve perceived decision quality.
  *Two boundaries matter for the 2.7 gap*: it explains point forecasts and does **not**
  represent uncertainty, and it is a dashboard, not an autonomous tool-invoking agent
- **Pathirannehelage et al. (2025)** (ADR, 3 orgs): communicating uncertainty is a
  **precondition of trust** for non-technical users
- **Goodwin et al. (2010)** -- the crucial counterweight, and the one most easily
  misreported: 50%/95% intervals alongside a point forecast **did not** improve
  newsvendor decision quality, and *actively degraded* responsiveness to cost asymmetry.
  Correct discrimination fell from ~84% (point only) to **44%** (95% intervals);
  participants anchored on the interval midpoint

**Evidence**
- Goodwin is a **caution, not an endorsement**, and does not license withholding
  uncertainty -- Pathirannehelage makes uncertainty a trust precondition and the
  calibration literature (2.5) makes an uncommunicated interval useless

**Open**
- The Goodwin asymmetry was the chapter's largest open problem across four P0044
  sessions. **Resolved** -- see the GOODWIN blocks below (N22, N42): the experiment now
  measures the decision step. Do not reopen without reading N34/N35/N42 first

---

## 2.4 LLM Agents and Tool-Mediated Reasoning

*Maps to SRQ2*

**Claims**
- The distinction between LLM-as-language-model and LLM-as-tool-using-agent underpins
  the SRQ2 interface design
- **Tool delegation can partially compensate for model scale** -- the central mechanism
  this thesis relies on
- The artefact is a **bounded tool-using AI agent with human-in-the-loop**, not a
  multi-agent Agentic AI system (Sapkota et al. 2026 taxonomy)
- The action *format* is itself a design dimension: JSON function-calling is chosen for
  the artefact; code-as-action becomes the SRQ4 **baseline**, not a rejected option

**Warrant**
- **Schick et al. (2023)** Toolformer: a 6.7B model with tool access outperforms a far
  larger one -- delegation substitutes for scale
- **Ma et al. (2024)** SciAgent: domain tools substantially improve precision-sensitive
  reasoning -> the LLM should orchestrate, not forecast
- **Paranjape et al. (2023)** ART: structured decomposition beats single-shot prompting
  -> motivates a *structured* tool-invocation sequence
- **Wang et al. (2024)**: executable code can beat JSON tool calls on some benchmarks,
  enabling dynamic composition and self-debugging. The thesis chooses JSON anyway, for
  reliability and reproducibility -- and states the trade-off rather than hiding it
- Multi-agent strand (**Liu et al. 2024 DyLAN; Li et al. 2024 AutoFlow; Wang et al. 2025
  ScoreFlow**) is read as **design context and a promising direction, not prescribed
  practice** -- empirical architecture results, not an established standard

**Open**
- P0043 thread 58: "THIS IS NOT ACCEPTABLE" -- flags a passage as something the thesis
  cannot and should not claim. Resolve before prose is finalised

---

## 2.5 Reliability, Traceability, Uncertainty, and Evaluation of Agentic Outputs

*Maps to SRQ2 and SRQ4*

**Claims**
- Three reliability risks bear on a forecast-informed agent: **hallucination**,
  **input-noise sensitivity**, **coordination failure**
- A generated statement is assessable **only against an explicitly retrieved source** --
  for this artefact, the reference fragment is the forecast value returned by the tool
- This motivates the validation step in the SRQ2 interface: a misstated figure becomes a
  *contradictory* statement against a known reference, not an unverifiable one
- Traceability is treated as a **design objective**, not a fully implemented capability
- **Conformal prediction, not isotonic recalibration**, is the approach adopted -- and
  the reason is a scope limit in the recalibration evidence

**Warrant**
- **Ji et al. (2024)** ANAH: sentence-level hallucination taxonomy. *Scope stated*:
  built for QA, not numerical reporting, so it supplies no category for a misstated
  figure -- what transfers is the source-grounded assessability principle
- **Wang et al. (2026)** AgentNoiseBench: tool-using agents degrade under structured
  input noise -> disciplined validation of data passed to the tool
- **Kartik et al. (2025)** AgentCompass: traceability reduces debugging effort --
  *asserted from deployment experience, not measured against an untraced control*, and
  read here as design rationale
- **Dong et al. (2024)** AgentOps: the artefacts an auditable agent must capture
- **Kuleshov et al. (2018)** / **Levi et al. (2022)**: isotonic post-hoc recalibration
  works -- but Levi's evaluation covers **neural architectures only**, so it cannot be
  read as validating calibration of the tree models used here
- **Lei et al. (2018)** split conformal: distribution-free finite-sample coverage under
  exchangeability, model-agnostic, therefore applicable to GBTs directly
- Its guarantee is **marginal** (an average over the calibration population, not a
  promise about any individual forecast), and **exchangeability is violated by temporal
  data**; **Barber et al. (2023)** bound the resulting coverage loss rather than
  eliminating it -> Ch6 measures coverage empirically instead of assuming it
- **Ouyang et al. (2025)**: LLM code output for an identical prompt varies across runs
  (half to three quarters of tasks yield no two identical outputs)
- **Atil et al. (2025)**: non-determinism persists **even at temperature zero** --
  directly relevant to Ch5's reproducibility claim
- **Schwartz et al. (2020)** / **Chen et al. (2024)**: cost is a first-class evaluation
  criterion; inference costs differ by orders of magnitude

**Open**
- The passage still specifies "a separate judge model with bias awareness and a human-
  rated subset" (Gu et al. 2025; Ye et al. 2024; Mehta 2025). **LLM-as-judge was
  dropped** -> [[srq4-experiment-design-rationale]] §7. The evaluation-design sentence
  must be rewritten; the judge-bias citations may survive only as context for *why* it
  was dropped

---

## 2.6 Production-Oriented Agentic Systems and Integration Readiness

*Maps to SRQ3*

**Claims**
- Production-oriented settings sharpen the reliability/traceability requirements into an
  **integration-readiness** question -- what capabilities a production agentic system
  must possess to incorporate forecast-informed decision-support
- Four capabilities synthesised: structured interface for invoking external predictive
  models; observability and traceability; explicit reliability/uncertainty handling;
  operation within bounded cost, latency, memory
- The thesis treats integration as a **design-and-readiness question**, assessed against
  a real production case -- not a completed deployment

**Warrant**
- **Gonzalez-Potes et al. (2026)** is the closest published exemplar: deterministic
  rule-based supervisor wrapped by a RAG conversational layer, local 7B model, live
  beverage plant. >98% state specification consistency, <3% median numerical error
- *The qualification is essential and must not be dropped*: 98% is a property of the
  **labelling layer**, not a rate of correct process operation, which was substantially
  lower on degraded stages
- **Two boundaries bear on this thesis** -- and they are observations about scope, not
  limitations the authors state: (1) it monitors a **live process** and has no predictive
  component projecting a series forward over a historical record; (2) it runs on
  dedicated industrial infrastructure and does **not** treat cost as a design constraint
- **Dong et al. (2024)**: the operational vocabulary -- registries, traces, guardrails,
  monitoring
- **Mehta (2025)** CLEAR: single-run success **overstates** reliability relative to
  multi-run consistency; operational dependability governs deployment readiness
- **Zheng et al. (2025)**: enterprise LLM/supply-chain integration -- appetite and friction

**Open**
- P0043 threads 79/82/83: whether these capabilities are actually implemented needs
  verifying. P0044 F8: observability **is** implemented but never **evaluated**

---

## 2.7 Research Gap: Forecast-Informed Extension of Non-Predictive Agentic Systems

**Claims**
- The gap is an **under-addressed intersection of four literatures**, not a single
  missing result -- each strand individually is well populated
  1. forecast-to-decision value is established but assumes **tight** coupling, does not
     address open-ended managerial support, and does not concern LLM agents
  2. agent/tool-use shows delegation substitutes for scale; an emerging strand exposes
     pre-trained statistical models as agent tools (Chen & Bibi 2026) but only as small,
     **non-peer-reviewed** proofs of concept, not addressing forecasting, reliability or
     production constraints
  3. reliability/evaluation establishes the risks and the need for bias-aware,
     multidimensional methods -- but not the integration
  4. production exemplars prove feasibility, but are built for **real-time supervision
     on dedicated infrastructure**; neither predictive extension over a historical
     tabular record nor SME resource constraints fall in scope
- The methodological contribution is **transferable design knowledge**, explicitly not a
  claim of a fully deployed or fully evaluated production system

**Contributions** (stated at system-class level; designed vs planned distinguished)

- **Predictive substrate (SRQ1): designed; benchmark to be built.** A memory-profiled benchmark of lightweight forecasting models across multiple FMCG beverage categories, characterising the accuracy–efficiency–specialization trade-off under a constrained compute budget.
- **Structured forecast-tool interface (SRQ2): designed.** A tool/action interface exposing forecasts and uncertainty to a tool-using agent, with traceability treated as an explicit design objective.
- **Integration readiness (SRQ3): designed; assessment planned.** A specification of the architectural and operational capabilities a production-oriented agentic system requires to integrate forecast-informed decision-support, to be assessed using a real production-oriented empirical case rather than a completed deployment.
- **Evaluation (SRQ4): designed; evaluation pending.** A comparison of dedicated-model agentic decision-support against a code-as-action LLM baseline, on correctness, consistency, and replicability (primary) and cost and latency (secondary), planned at the scale of a pilot in the first instance rather than a full study.

---

## 2.8 Design Science Research

*Maps to all research questions*

**Claims**
- The thesis's questions are **constructive** -- how a system can be designed, what
  capabilities its design requires -- not tests of pre-existing theory
- DSR fits for two reasons: the central contribution **is an artefact**, and the intended
  contribution extends beyond it to **transferable design knowledge**
- DSR framing also **disciplines the evaluation**: the artefact must be assessed against
  defined criteria in a relevant context

**Warrant**
- **Hevner et al. (2004)**: distinguishes building an artefact from behavioural study of
  existing systems; requires the artefact be both demonstrably useful and a source of
  generalisable knowledge
- **Peffers et al. (2007)**: the six-step process model structuring the project as an
  ordered, justifiable sequence

**Evidence**
- This section establishes only the paradigm and its fit; the applied DSR process --
  artefact definition, evaluation design, validation against the empirical case -- is Ch3

**Open**
- P0043 thread 88: why is the Saunders methodology book not cited here? It is used
  elsewhere. Reconcile -- see also the Ch3 threads on the same question

---

## 2.9 Chapter Summary and Transition to Methodology

**Claims**
- 2.1-2.2 support a benchmark of lightweight, category-specialised models on accuracy,
  efficiency and **stability** under a memory budget
- 2.3 establishes prediction-to-decision value on peer-reviewed evidence, while showing
  the connection has been studied as **tight, optimization-level coupling**
- 2.4-2.6 supply the mechanism (tool-mediated reasoning), the governing requirements
  (reliability, traceability, evaluation) and the operational capabilities
- 2.7 names the under-addressed intersection; 2.8 frames the response as DSR

**Evidence**
- Transition: Ch3 operationalises the paradigm -- artefact, benchmark, tool interface,
  readiness assessment, and the evaluation comparing dedicated-model agentic
  decision-support against the code-as-action baseline, with its bounding limitations

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


---

## OPEN AUDIT NOTES (P0044, 2026-09-03)

> Companion to the Ch3 notes of the same date. Bullets only.

### N9. The Goodwin asymmetry -- Sec 2.3 argues for something SRQ4 does not measure

- Sec 2.3 makes Goodwin et al. (2010) a centrepiece, and correctly: bare prediction
  intervals **degraded** newsvendor decisions, with correct cost-asymmetry
  discrimination falling from ~84% (point forecast) to 44% (95% interval).
- The chapter then draws the right conclusion -- "the interpretive step between the
  interval and the decision ... is the part that carries the decision value. That step
  is precisely what an agentic layer is positioned to supply."
- **But SRQ4 scores APE.** It measures whether the forecast was right, never whether the
  agent made the interval actionable. The literature review argues for a capability the
  evaluation is silent on.
- This is the single largest coherence gap between Ch2 and the experiment design.
- Options and cost are set out in N10. **Decision pending.**

### N10. Closing the Goodwin gap -- three options

**Option 1 -- scope Goodwin down to motivation (zero cost)**
- Keep Goodwin as justification for *why the artefact emits a decision-oriented
  recommendation rather than a bare interval*, and say plainly that whether this improves
  human decisions was not tested.
- Add to Sec 3.7 limitations and Ch10 further work.
- Honest, cheap, and leaves the strongest claim in Ch2 unevidenced.

**Option 2 -- add an interval-actionability dimension to SRQ4 (low cost, no new API spend)**
- Every scenario-C run already returns `forecast_units` **plus interval and confidence
  tier** from `forecast_tool.py`; the answer text is already stored per run.
- So the data needed to score "did the agent USE the interval" is **already being logged**.
  This can be scored retrospectively on runs already paid for.
- Deterministic, rule-based checks -- no judge needed (consistent with N5):
  - does the answer state the interval at all;
  - is the stated interval numerically faithful to the tool payload (same
    check `args_match_request` performs for the point forecast);
  - does the answer name the confidence tier;
  - does it give a directional recommendation rather than only a number.
- Yields a 4-part **interval-communication score**, reportable per scenario. A is expected
  to score near zero (no tool, no interval), which makes it a real ladder result.
- **This directly evidences the Sec 2.3 claim and the Sec 2.5 ANAH-derived validation
  principle, and it costs nothing beyond writing the scorer.**

**Option 3 -- human decision experiment (out of scope)**
- Goodwin's actual design: give planners forecasts under asymmetric costs, measure order
  quantities. Needs participants, ethics approval (cf. MR-10), and a pilot.
- Not feasible in the remaining timeline. Name it as further work.

**Recommendation: Option 2, with Option 1's limitation paragraph as backstop.**
- Option 2 converts a rhetorical claim into a measured one for the price of a scorer,
  and it strengthens rather than weakens the deterministic-scoring position from N5b.
- It does NOT claim improved human decisions -- only that the artefact communicates the
  interval that Goodwin shows a bare number fails to convey. State that boundary explicitly.

### N11. Sec 2.2 -- the 8 GB figure

- "on the order of eight gigabytes in this thesis's deployment setting" -> 4 GB measured.
- See Ch3 note N3 for the full occurrence list and the reasoning that must be rewritten
  rather than find-replaced.

### N12. Missing reference

- **Taylor, S. J., & Letham, B. (2018). Forecasting at scale. *The American Statistician*,
  72(1), 37-45.** Prophet is benchmarked in Ch6 and reported in Appendix A.4, but the
  source is absent from the Ch2 reference list. Required by NLM audit Section J.


---

## GOODWIN GAP -- CLOSED (P0044, 2026-09-03, session 2)

### N22. The Sec 2.3 / SRQ4 asymmetry is now measured

- Built `03_thesis_modelling/scenario_setup/score_interval_communication.py`.
- **Zero new API spend.** Every scenario-C run already logs the tool payload
  (`forecast_units`, `interval_90`, `confidence`, `confidence_tier`) and the answer text,
  so communication is scored **retrospectively** on runs already paid for.
- **No judge** -- every check is deterministic, consistent with the N5b position.

Four criteria:

| # | Criterion | What it catches |
|---|-----------|-----------------|
| 1 | States a range | silence about uncertainty |
| 2 | **Range matches the tool output** (5% tol) | an invented but plausible interval |
| 3 | States confidence | a range with no reliability attached |
| 4 | Gives a recommendation | a number with no decision attached |

- Criterion 2 is the **ANAH principle from Sec 2.5** applied to the interval: a generated
  statement is assessable only against an explicitly retrieved source. It is the same
  check `args_match_request` performs for the point forecast.
- Scenario A cannot satisfy criterion 2 by construction -- no tool, no source. **That is a
  ladder result, not a bug.**

**First pilot output (scenario A, n=3):** states a range **100%**, matches tool output
**0%**, states confidence **100%**, gives a recommendation **33%**.

- This is *precisely* Goodwin's failure mode: a confident-sounding range, ungrounded in
  any model, with no decision attached. Strong material for the discussion.

### N23. What this does and does NOT claim -- state the boundary explicitly

- **Does:** measure whether the artefact *communicated* the interval, and whether what it
  said was faithful to what the model produced.
- **Does NOT:** show human decisions improved. That needs Goodwin's own design --
  participants, asymmetric costs, measured order quantities, ethics approval (cf. MR-10).
- Both the caption and the generated `.md` state this boundary. **Keep it in the prose.**
- Ch10 further work: the human decision experiment.

### N24. Consequence for the Sec 2.7 contribution list

- SRQ2's contribution currently reads "traceability treated as an explicit design
  objective." With N4 (args-match logging) and N22 (interval faithfulness) both
  implemented and measured, that can be upgraded from *objective* to *evidenced*.
- This is the strongest available answer to the "designed; evaluation pending" framing
  that currently marks three of the four contributions.


---

## GOODWIN -- SCOPE DECISION PENDING (P0044, 2026-09-03, session 3)

### N34. Confirmed: we do NOT test human decision improvement

- Agreed explicitly with Brian, 2026-09-03. Recording it so it is not re-litigated.
- **What we measure:** whether the artefact *communicated* the interval, and whether what
  it stated was faithful to what the model produced.
- **What we do not measure:** whether that communication improves a human planner's
  decisions. That requires Goodwin's own design -- participants, asymmetric costs,
  measured order quantities, ethics approval (cf. NLM finding MR-10).
- Already stated in: the scorer docstring, the generated `.md`, and the appendix caption.
- **Must also appear in:** Ch2 sec 2.3 (where Goodwin is introduced), Ch3 sec 3.7 (limitations),
  and Ch10 (further work). Verify all three when revising.

### N35. The "recommendation" criterion was dropped -- and why that matters for Sec 2.3

- The scorer originally had a fourth criterion, "gives a recommendation". **Removed.**
- Reason: the shared prompt asks only for a number, a range, and a confidence. It never
  asks for a recommendation, so scoring one measured our own prompt, not the scenario.
- **This exposes a live tension in Sec 2.3.** The chapter argues that the interpretive step
  between the interval and the decision "is precisely what an agentic layer is positioned
  to supply" -- but the experiment never asks the agent to supply it.
- **Two coherent resolutions (decide before the paid runs):**
  1. **Add a recommendation request to the shared question.** All three scenarios get the
     identical addition, so the single-variable design survives. Goodwin becomes a
     measured dimension rather than a motivating citation.
  2. **Scope Goodwin down.** Keep it as justification for *why the artefact carries
     uncertainty at all*, and state that the decision step was not evaluated.
- Option 1 is the stronger thesis. Option 2 is honest and free. **Either is defensible;
  silently keeping the Sec 2.3 rhetoric while measuring neither is not.**


---

## GOODWIN -- RESOLVED (P0044, 2026-09-03, session 4)

### N42. Option 1 taken: the experiment now measures the decision step

- **Decided (Brian, 2026-09-03).** The shared question now asks for a recommendation,
  identically in all three scenarios. See Ch3 note N36.
- **Sec 2.3 no longer over-claims.** The chapter argues the interpretive step from interval
  to decision "is precisely what an agentic layer is positioned to supply" -- and the
  experiment now asks for that step and scores whether it was supplied.
- Scored deterministically (label match, then recommendation verbs), no judge.
- **The N34 boundary still holds and must stay in the prose:** we measure what the system
  *communicated*, never whether human decisions improved.

### N43. New citation required -- Brown et al. (2020)

- The one-shot prompting design needs grounding. **Brown, T. B., et al. (2020). Language
  models are few-shot learners. *Advances in Neural Information Processing Systems 33*.**
- Used for: most of the in-context-learning gain arrives with the first example, with
  diminishing returns after -- which justifies *one* exemplar rather than several.
- **Not currently in the Ch2 reference list.** Add it, alongside Taylor & Letham (2018)
  from N12.
- Where it belongs: Sec 2.4 (LLM agents and tool-mediated reasoning) sits closest, since
  the prompting method is part of how the agent is instructed.

### N44. Reference-list gaps now standing at two

| Reference | Needed for | Raised in |
|---|---|---|
| Taylor & Letham (2018), *The American Statistician*, 72(1), 37-45 | Prophet is benchmarked and reported | N12 |
| Brown et al. (2020), NeurIPS 33 | one-shot prompting design | N43 |

---

## Writing-notes wired into this chapter (P0045)

- [[srq1-model-ladder-and-baselines]] — §2.1 why the substrate contains these five models
- [[srq1-pooled-vs-per-category]] — §2.1 the M5 cross-learning precedent, and the metric
  disagreement the comparison exposed
- [[srq4-experiment-design-rationale]] — §2.5 LLM-as-judge dropped (§7 of that note),
  which invalidates this chapter's stated evaluation design
- [[sample-size-and-tool-interface-rationale]] — §2.5 what the intervals can and cannot
  claim at this sample size
