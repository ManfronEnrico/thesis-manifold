<!-- PROSE STRIPPED 2026-09-01 (P0044); ARGUMENT BULLETS REBUILT 2026-09-05 (P0045).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-05_19-52_complete-review-pass/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 1 — Introduction

> **P0045 (2026-09-05) — Ch1 is now the LAST chapter still on 8 GB.**
> The 19-52 snapshot shows Ch2 §2.2 reading "on the order of four gigabytes" and Ch5
> reading "approximately four gigabytes", while Ch1 still says eight in §1.1, §1.2, §1.4
> and §1.5. The thesis contradicts itself across chapters. Item 1 of OPEN REWRITE NOTES
> below is therefore no longer just a Ch1 improvement — it is a consistency defect a
> reader can find unaided.
> Ch5 §5.8 also still computes "2.8%", which is 231 MB / 8 GB; against 4 GB it is 5.6%.
> Status: PROSE DRAFT — written 2026-04-05; realigned 2026-06-16 to the rescoped framing (forecast-informed agentic decision-support; RQs v3) with §1.1 reframed and reference list reconciled
> Author: Claude Code — requires human review before finalisation
> Word count target: ~8 standard CBS pages (2,275 chars/page)

---

## 1.1 Background and Motivation

**Claims**
- BI has been descriptive for decades — it tells managers *what happened*; markets now
  demand *what is likely next* and *what to do about it*
- FMCG beverage demand is erratic, intermittent and externally sensitive, so uniform
  forecasting approaches are inadequate
- Practical deployment faces a constraint the forecasting literature has largely left
  unexamined: **computational resource limits**
- That gap is not merely technical — it reflects a structural asymmetry in AI research,
  where benchmarks assume infrastructure available to large labs while most organisations
  that would benefit operate with far less
- **Demonstrating that reliable forecast-informed decision-support fits an SME envelope
  is itself a contribution, independent of the domain**
- The unaddressed combination: lightweight substrate + bounded tool-using agentic layer +
  structured interface preserving reliability/uncertainty + fixed RAM budget

**Warrant**
- **Ma et al. (2025)**, private-label beverage manufacturer: no single model dominates
  across demand patterns
- **M4 (Makridakis et al. 2020)**: combining beats single-best; hybrids win
- **M5 (Makridakis et al. 2022)**: all top-50 used LightGBM, >14% over the best
  statistical benchmark; exogenous promo/calendar features materially improved accuracy
- **González-Potes et al. (2026)**: architecturally closest exemplar — >98% state
  specification consistency, <3% median numerical error. *Keep the qualifier*: 98% is the
  labelling layer, not correct process operation
- **Rinaldi et al. (2025)** DSS4EX brings agentic decision support near this domain but
  explains point forecasts only, with no uncertainty representation
- Danish retail is a defensible empirical context: mature, highly concentrated, with
  systematic Nielsen scanner coverage giving granular longitudinal product/retailer data

**Open — this section carries the chapter's four unresolved premises**
- **RAM.** Still says "eight gigabytes" and still carries the GPU-cost passage and the
  `[CITATION TO ADD: cloud-instance pricing source]` placeholder. **Ch2 §2.2 and Ch5 now
  say four gigabytes.** The thesis currently contradicts itself across chapters — this is
  the highest-priority fix in Ch1. See OPEN REWRITE NOTES item 1
- **Exogenous enrichment.** The M4 "explanatory variables are the open frontier" quote is
  followed by "this thesis takes up that direction", which is unsupported. Narrow to
  promo + calendar, which are real. P0043 threads 15/18/20; OPEN REWRITE NOTES item 2
- **Ng's four terabytes** is unverified (P0043 thread 29). Cheapest fix: drop the figure,
  keep the citation for the memory-as-design-variable argument
- **Manifold hosts no LLM** (P0043 thread 27). The GPU/locally-hosted cost contrast
  describes a situation the company is not in; the 8 GB (now 4 GB) sandbox is for code
  execution and conversation, not model weights

---

## 1.2 Research Problem

**Claims**
- Commercial context: **Manifold AI**, building conversational "AI Colleagues" for retail
  analytics — production-oriented, agentic, and **currently descriptive only**. It reports
  volumes, market shares and weighted distribution; it does not forecast, anticipate or
  recommend
- That same production system is the thesis's **empirical reference case**, which is what
  makes SRQ3 answerable
- Extending a non-predictive agentic system with predictive capability raises **four
  problems**, and they map one-to-one onto the SRQs:
  1. the substrate must be accurate **yet deployable** within a tight compute budget (SRQ1)
  2. forecasts must reach the agentic layer through an interface preserving reliability,
     uncertainty and traceability (SRQ2)
  3. the production system must itself possess the capabilities to integrate one (SRQ3)
  4. the result must beat a **code-as-action baseline at justified cost** (SRQ4)
- Framing of problem 4 is deliberate: **the dedicated-model integration must earn its
  place against a strong LLM-only alternative**, not merely work

**Warrant**
- Problem 1 rests on a trade-off the literature has only recently begun to measure
  systematically (Klee & Xia 2025)
- Stating the baseline as *strong* rather than *straw* is what makes a null result
  publishable and a positive result credible

**Open**
- Closing sentence still says "the 8GB RAM budget characteristic of realistic SME cloud
  deployment". Two problems: the figure (→ 4 GB measured) and the *characteristic* claim,
  which is the unsourced assumption P0044 F22 identified. Restate as the measured
  production template

---

## 1.3 Research Questions

**Claims — the four SRQs and what each is for**
- **SRQ1** (Ch6): which lightweight models best trade accuracy, memory efficiency and
  category specialisation. *Accuracy alone is insufficient for production*: a model with
  marginally lower error but higher memory or unstable output is the worse engineering
  choice under a fixed budget (Klee & Xia 2025)
- **SRQ2** (Ch5 design, Ch7 realisation): expose forecasts through a structured interface
  preserving reliability (validate agent output against source forecasts), uncertainty
  (intervals attached), traceability (tool call → value → recommendation recorded)
- **SRQ3** (Ch5 spec, assessed Ch7/Ch9): the capabilities a production agentic system
  needs. **Grounded in a working integration, not architectural analysis alone** — the
  SRQ2 tool is registered with and executed inside the production system as part of SRQ4,
  and the readiness criteria derive from what that integration actually depended on
- **SRQ4** (Ch8): does dedicated-model access improve correctness, consistency and
  replicability at justified cost and latency, relative to the same system with only data
  access and code execution — **and does it hold in a production agentic system as well
  as a general-purpose one**

**Warrant — the ladder is the central methodological feature**
- Scenarios add capability **one variable at a time**: LLM alone → + data & code execution
  → + dedicated forecasting tool → and the last two repeated inside Manifold's production
  system
- Because **the same intervention is applied in two independently built agentic systems**,
  a consistent effect cannot be blamed on the design of one evaluation harness
- The two settings differ in reproducibility **deliberately**: general-purpose rungs are
  reproducible from the repo + an API key; production rungs are ecologically valid but not
  re-executable by a reader. Neither property suffices alone; they corroborate
- **No model judges another model's output.** All measures computed programmatically
  against held-out actuals and recorded traces → [[srq4-experiment-design-rationale]] §7
- Consistency is measured by **repeated execution of an identical prompt**, not breadth of
  prompt coverage — run-to-run variance is the property of interest

**Open**
- P0043 thread 42: SRQ4's wording is very long. Content is sound; consider splitting the
  production-system clause into a following sentence
- P0043 thread 43 (repository sharing): submission-time task. Needs a clean repo — no
  CLAUDE artefacts, no Nielsen data, no credentials
- OPEN REWRITE NOTES item 4: SRQ1's memory efficiency **is** tracked and SRQ3's
  observability **is** implemented. The gap is that observability is never *evaluated*.
  If Ch1 promises it as a measured property, that is the real exposure

> **Main RQ**: *How can production-oriented agentic decision-support systems without native predictive capabilities be extended with lightweight forecasting models to support reliable, forecast-informed, and cost-justified decision-making under computational and deployment constraints?*

![**Figure 1.1** — Hierarchical structure of the research questions: the main research question and its four subsidiary questions (SRQ1–SRQ4).](../figures/ch1_research_questions_tree.png){width=6in}

---

## 1.4 Delimitation

**Claims**
- **Domain and geography.** Danish beverage retail, four Nielsen categories: CSD,
  danskvand, energidrikke, RTD
- **totalbeer was excluded on computational grounds** — at 455 brands it is an order of
  magnitude larger and would have dominated preprocessing time and the memory budget the
  thesis sets out to respect. Stating this as a *budget-consistent* decision rather than
  an omission is the right framing
- Up to **44 monthly periods** per category at the market scope used — sufficient
  longitudinal depth while manageable under the RAM constraint
- Categories were chosen with Manifold as representative of the FMCG challenges (promo
  sensitivity, seasonality, competitive dynamics) **while differing systematically in
  scale and measurement coverage** — which is what lets the benchmark test generalisation
- **Promo measures exist for CSD and energidrikke but not danskvand or RTD** — a
  structural property of the Danish market as Nielsen measures it, **not** a defect of the
  extract
- **Computational constraint.** Formal design criterion, not convenience; excludes LSTM,
  TFT, N-BEATS, Chronos at inference
- **Processing mode.** Monthly batch, not streaming — matches the tactical planning cycle
- **Deployment scope.** A research prototype validated against research metrics, **not**
  against live business outcomes. No claim of a production-ready system
- **Generalisability.** Bounded to the Danish market and the Nielsen panel

**Warrant**
- The asymmetry framing (structural property, not limitation) is the honest and the
  stronger reading — it converts a data gap into a test of robustness
  → [[sample-size-and-tool-interface-rationale]] §8

**Open**
- P0043 thread 49: the heterogeneous-generalisation claim is good but **must be shown in
  the code**. P0044: P0042 block 3 (9 brands, 3 categories) exists to test exactly this
- P0043 thread 51: the promo-coverage sentence **teases EDA results**. Keep the hint but
  add a forward pointer to Ch4, where it is treated properly
- Says "the **five**-category benchmark" under Generalisability while the scope is four.
  Stale from before the totalbeer exclusion — fix
- Computational constraint still reads 8 GB

---

## 1.5 Thesis Structure

**Claims**
- Nine chapters follow, each mapped to a phase of the DSR process (Peffers et al. 2007)
- **Ch2** — literature across eight thematic sections, establishing foundations and the gap
- **Ch3** — methodology: DSR grounding, data sources, preprocessing, benchmark, tool
  interface, readiness assessment, evaluation design
- **Ch4** — data assessment: quality, structure, forecasting suitability across four
  categories; preprocessing decisions
- **Ch5** — the predictive-extension architecture, justified against the RAM budget;
  lightweight Python coordinator evaluated, LangGraph as production target
- **Ch6** — SRQ1: model benchmark on accuracy, memory efficiency, stability; specialised
  vs pooled
- **Ch7** — SRQ2 (informing SRQ3): the agentic extension prototype
- **Ch8** — SRQ4: pilot evaluation vs the code-as-action baseline
- **Ch9** — contributions, integration-readiness findings, limitations
- **Ch10** — synthesis of the four SRQs and the main RQ

**Open**
- Ch5 entry still says "the 8GB RAM budget"
- P0043 thread 47 (`OUTDATED`): internal references must be made from in-text, and this
  structure list is a candidate for the reader-facing forward pointers requested in
  thread 51

---

## References cited in this chapter

- González-Potes, A., et al. (2026). Hybrid AI and LLM-enabled agent-based real-time decision support architecture for industrial batch processes. *AI*, *7*(2), 51.
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly*, *28*(1), 75–105.
- Liu, S., Guo, B., Yu, Z., et al. (2025). On accelerating edge AI: Optimizing resource-constrained environments. *arXiv preprint arXiv:2501.15014*. [PREPRINT — not peer-reviewed]
- Sapkota, R., Roumeliotis, K. I., & Karkee, M. (2026). AI agents vs. agentic AI: A conceptual taxonomy, applications and challenges. *Information Fusion*, *126*, Article 103599. https://doi.org/10.1016/j.inffus.2025.103599
- Semerikov, S. O., Vakaliuk, T. A., Kanevska, O. B., Ostroushko, O. A., & Kolhatin, A. O. (2025). Edge intelligence unleashed: A survey on deploying large language models in resource-constrained environments. *Journal of Edge Computing*, *4*(2). https://doi.org/10.55056/jec.1000
- Klee, S., & Xia, Y. (2025). Measuring time series forecast stability for demand planning. *KDD '25 Workshop on AI for Supply Chain*.
- Ma, B. J., Jackson, I., Huang, M., Villegas, S., & Macias-Aguayo, J. (2025). A data-driven and context-aware approach for demand forecasting in the beverage industry. *International Journal of Logistics Research and Applications*.
- Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2020). The M4 competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, *36*(1), 54–74.
- Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting*, *38*(4), 1346–1364.
- Ng, S. (2017). Opportunities and challenges: Lessons from analyzing terabytes of scanner data. *NBER Working Paper*, *23673*.
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems*, *24*(3), 45–77.
- Rinaldi, G., Giordano, F., De Stefano, C., & Fontanella, F. (2025). DSS4EX: A decision support system framework to explore artificial intelligence pipelines with an application in time series forecasting. *Expert Systems With Applications*, *269*, 126421.

---

## OPEN REWRITE NOTES (P0044, 2026-09-01) — act on these before prose

Source: Word comments [15]-[22], [25], [26], [30] on the 2026-09-01 snapshot,
plus measurements in `plans/P0044_.../findings.md`.

### 1. RAM: re-anchor on the MEASURED 4 GB, not the assumed 8 GB  (F22, F23)

- Manifold's production Prometheus E2B template `fxe7gzkqjupdhbx4uvpr` is
  provisioned at **4096 MB**, verified live against the E2B API.
- The **8 GB** figure is this project's own assumption. Ng (2017) is cited in
  support, but Ng argues that *memory is the binding design variable* at
  terabyte scale -- Ng does not state an 8 GB SME budget. The number is
  unsourced.
- So the contrast is an **unsourced assumption vs. a measured production
  value**. Prefer the measured one.
- Every result holds a fortiori under the tighter bound: serving 36.8 MB,
  refit ~37 MB, ~1% of 4 GB.
- **Delete** the GPU-instance / locally-hosted-LLM cost passage (comment [20]):
  Manifold hosts no LLM. The 4 GB is sandbox budget for code execution and
  conversation. The `[CITATION TO ADD: cloud-instance pricing source]` placeholder
  goes with it.
- Reframe RAM from promise to **result**: not "we operate under a hard
  constraint" but "serving a trained model fits in a measured 4 GB production
  sandbox, which is what makes the design deployable".

### 2. Drop the exogenous-enrichment premise  (comments [15] [16] [17]; F7)

- VERIFIED unsupported. Live features are lags, rolling mean/std, month,
  quarter, peak_month, promo_intensity, zero_run_*, log_sales_units -- all
  endogenous or calendar-derived. Every holiday-calendar hit is in `.archive/`.
- **Narrow, do not delete**: `promo_intensity` IS exogenous (promotion is a
  decision external to the demand series), as is distribution coverage. Claim
  promotional + calendar signals; drop any implication of weather, macro or
  holiday-calendar enrichment.
- The M4/M5 "explanatory variables are the open frontier" quote can stay only if
  the thesis stops claiming to take up that direction wholesale.

### 3. Promote the serving-approach contribution  (comment [22])

Currently under-elaborated, and it is what SRQ4 actually measures: what a
multi-indicator ML serving approach buys in prediction quality, cost and latency.
The harness logs all three per run. This should share billing with the RAM
framing, not sit beneath it.

### 4. Do NOT "fix" these -- they are already implemented  (F8)

- [25] memory efficiency IS tracked (`srq1_profiling.py`,
  `train_and_persist.py:214-244`). The instrument was wrong, not absent; fixed.
- [26] observability/traceability IS implemented -- every SRQ4 run logs
  latency, tokens, cost and a tool trace. What is missing is an *evaluation*
  of it. If Ch1 promises observability as a **measured** property, that is the
  real gap; as an **implemented** property it is satisfied.

### 5. On-demand retraining: state as measured, with the cost caveat  (F19-F21, F24)

- Refit on stored hyperparameters: ~3 s, ~37 MB. Re-tuning costs **12x**
  (measured: 84.4 s vs 7.0 s across 5 cutoffs, 30 trials each).
- The ~100x figure for a 200-trial budget is an **extrapolation**, not a
  measurement. Label it as such.
- **Do NOT claim re-tuning is less accurate** -- retracted (F21). Varying only
  the Optuna seed on identical data moves test wMAPE by 3.97pp, which swamps the
  0.28pp between arms.
- Defensible claim: refit is chosen on **cost**, being indistinguishable in
  accuracy at this data scale.
- Report the one-month (95-row) validation window as a limitation.

### 6. Smaller items

- [21] Ng (2017) "four terabytes" is unverified. Cheapest fix: cut the figure,
  keep the citation for the memory-as-design-variable argument.
- [27] SRQ4's wording is very long. Content is sound; consider splitting the
  production-system clause into a following sentence.
- [30] heterogeneous-category generalisation IS verifiable -- P0042 block 3
  (9 brands, 3 categories, C_model) exists to test exactly this.
- [31] the promo-coverage asymmetry teases EDA results; keep the hint but add a
  forward pointer to the chapter that treats it properly.
- [28] repository sharing: submission-time task. Needs a clean repo with no
  CLAUDE artefacts, no Nielsen data, no credentials.

---

## Writing-notes wired into this chapter (P0045)

- [[sample-size-and-tool-interface-rationale]] — §1.4 cross-category asymmetry as a
  structural property, and the sample-size boundary on what Ch8 can claim
- [[srq4-experiment-design-rationale]] — §1.3 the information ladder, the same-base-model
  control, and LLM-as-judge dropped (§7)
- [[srq1-model-ladder-and-baselines]] — §1.3 SRQ1 scope: what "lightweight models" denotes
- [[srq4-first-results-and-interpretation]] — §1.3 what the pilot can and cannot support
