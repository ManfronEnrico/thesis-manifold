<!-- PROSE STRIPPED 2026-09-01 (P0044).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-01_18-50/chapters.
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
