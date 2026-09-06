# Comments — Discussion

Extracted 2026-09-05 from `MSc. Data Science - 175888 and 176171 - Master Thesis.docx`.
17 comment(s) in 17 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [405](#c405) | Discussion | FORMATTING |  | FORMATTING: Could use a subtitle for the chapter... |
| [408](#c408) | SRQ1: Forecasting accuracy under constraints | VERIFY |  | VERIFY, INTERNAL REFERENCE... |
| [409](#c409) | SRQ1: Forecasting accuracy under constraints | METACOMMENT |  | METACOMMENT... |
| [411](#c411) | SRQ2: Synthesis quality | VERIFY |  | VERIFY,... |
| [413](#c413) | SRQ3: Integration readiness | VERIFY, OUTDATED |  | OUTDATED, VERIFY... |
| [414](#c414) | SRQ3: Integration readiness | METACOMMENT |  | METACOMMENT... |
| [416](#c416) | SRQ4: dedicated ML vs the LLM/traditional bas | VERIFY, PROSE, OUTDATED |  | OUTDATED, VERIFY, PROSE... |
| [417](#c417) | SRQ4: dedicated ML vs the LLM/traditional bas | METACOMMENT |  | METACOMMENT... |
| [420](#c420) | Design knowledge contribution (DSR framing) | VERIFY, PROSE |  | VERIFY, PROSE... |
| [423](#c423) | Design principles (generalised from thesis fi | VERIFY, NAMING |  | NAMING, VERIFY, FORMAT... |
| [424](#c424) | Design principles (generalised from thesis fi | VERIFY, PROSE |  | VERIFY, PROSE... |
| [426](#c426) | Novelty claims | VERIFY, PROSE |  | VERIFY, PROSE... |
| [428](#c428) | Contribution to IS literature | VERIFY, SOURCE, PROSE |  | VERIFY, PROSE, SOURCE... |
| [430](#c430) | Practical implications | VERIFY, SOURCE, PROSE |  | VERIFY, PROSE, SOURCE... |
| [432](#c432) | Limitations | VERIFY, PROSE |  | VERIFY, PROSE... |
| [434](#c434) | Future research directions | VERIFY, PROSE |  | VERIFY, PROSE... |
| [435](#c435) | Outstanding decisions | METACOMMENT |  | METACOMMENT... |

---

<a id="c405"></a>

## [405] Brian Rohde -- Discussion  `FORMATTING`

- **Section:** Discussion
- **Date:** 2026-09-05T18:53:00
- **On:** “COULD USE A SUBTITLE”

FORMATTING: Could use a subtitle for the chapter

<a id="c408"></a>

## [408] Brian Rohde -- Discussion  `VERIFY`

- **Section:** Discussion > Interpretation of findings > SRQ1: Forecasting accuracy under constraints
- **Date:** 2026-09-05T17:54:00
- **On:** “Tuned XGBoost was the best model in every category, ahead of LightGBM, Ridge, and the SeasonalNaive baseline, confirming that gradient boosting over engineered lag/rolling/calendar features is the strongest lightweight family for this monthly FMCG panel. The selected per-category configurations reach test WMAPE of 16.5% (CSD), 22.0% (danskvand), 11.4% (energidrikke) and 31.0% (RTD). RTD remains hardest - short, volatile, promotion-blind series. A central and somewhat counter-intuitive result is that finer granularity does not uniformly help: disaggregating to a retail-chain dimension multiplied training rows roughly sixfold yet improved accuracy only for danskvand, while CSD, energidrikke and RTD forecast better at the aggregated brand level. This is a signal-to-noise effect - more rows of noisier per-chain demand do not beat fewer rows of a cleaner aggregate - and it motivates the per-category representation choice (Ch6 §6.5.6). On the operational axis the ≤8 GB constraint is non-binding at this data scale: peak RAM is in the tens of MB for every model and inference is sub-second, so the accuracy-optimal model also fits the budget with no compromise. SHAP attributes forecasts chiefly to last-month sales (lag_1) and shelf availability (weighted_distribution), which is consistent with retail demand dynamics and lends face validity to the models.”

VERIFY, INTERNAL REFERENCE

<a id="c409"></a>

## [409] Brian Rohde -- Discussion  `METACOMMENT`

- **Section:** Discussion > Interpretation of findings > SRQ1: Forecasting accuracy under constraints
- **Date:** 2026-09-05T17:55:00
- **On:** “Connect to: Edge AI / Efficient & Green LLMs (the constraint is easily met); gradient-boosting-for-retail literature.”

METACOMMENT

<a id="c411"></a>

## [411] Brian Rohde -- Discussion  `VERIFY`

- **Section:** Discussion > Interpretation of findings > SRQ2: Synthesis quality
- **Date:** 2026-09-05T17:58:00
- **On:** “The deterministic synthesis core produced well-to-conservatively calibrated ensemble intervals (empirical coverage 80–98% against a 90% nominal), so the uncertainty the system communicates is trustworthy. The composite confidence score skewed to the Moderate tier with no High-confidence forecasts under the current thresholds - an artefact of weighting interval tightness heavily while the conformal 90% interval is deliberately wide; the tier cut-offs, not the forecasts, are what need recalibration. On recommendation quality, the LLM synthesis added clear value over a rule-based template: GPT-4o (LLM-as-Judge, N=50) scored it higher on actionability (4.00 vs 2.14), relevance (4.00 vs 3.28), clarity (4.34 vs 3.46) and calibration (3.74 vs 3.46), with the template ahead only on accuracy (3.42 vs 2.96). The weakest LLM dimension is therefore accuracy: turning numbers into prose occasionally drifts from a strict reading of the inputs - a usefulness/precision trade-off, and the clearest target for prompt hardening. Connect to: Kuleshov 2018 (calibration); AI-augmented decision-making DSR 2024.”

VERIFY,

<a id="c413"></a>

## [413] Brian Rohde -- Discussion  `VERIFY * OUTDATED`

- **Section:** Discussion > Interpretation of findings > SRQ3: Integration readiness
- **Date:** 2026-09-05T18:13:00
- **On:** “SRQ3 is addressed as an integration-readiness assessment, not a live integration: production access to the Prometheus platform was not available and was not required for the thesis, which runs entirely on a local Nielsen snapshot. The forecasting substrate is nonetheless integration-ready in the senses Ch3/Ch5 specify - it is exposed through a structured, reproducible interface (committed scripts, deterministic seeds, versioned artefacts) and emits point forecasts plus calibrated intervals and a confidence tier suitable for an agent tool-call. The remaining gap to active integration is operational (credentials, a dev-merge into the Graph Engine), not architectural.”

OUTDATED, VERIFY

<a id="c414"></a>

## [414] Brian Rohde -- Discussion  `METACOMMENT`

- **Section:** Discussion > Interpretation of findings > SRQ3: Integration readiness
- **Date:** 2026-09-05T18:13:00
- **On:** “Connect to: Ch3/Ch5 integration-readiness specification.”

METACOMMENT

<a id="c416"></a>

## [416] Brian Rohde -- Discussion  `VERIFY * PROSE * OUTDATED`

- **Section:** Discussion > Interpretation of findings > SRQ4: dedicated ML vs the LLM/traditional baselines
- **Date:** 2026-09-05T18:14:00
- **On:** “Against the traditional statistical baseline, dedicated ML (XGBoost) beats ARIMA in three of four categories (by 7.7, 4.3 and 17.2 pp WMAPE for CSD, energidrikke, RTD), with only danskvand better served by an additive Prophet model - so dedicated lightweight ML is, on balance, justified over classical forecasting. The code-as-action LLM baseline central to the v4 SRQ4 - an LLM that writes and self-corrects its own forecasting code - was not executed: it requires a secure execution sandbox (E2B) that is not configured. This is the principal open piece of the empirical SRQ4 answer and is carried as future work; what the present results establish is the prior, weaker comparison (dedicated ML vs traditional, and LLM synthesis vs template), both favouring the dedicated/structured approach on the decision-relevant dimensions.”

OUTDATED, VERIFY, PROSE

<a id="c417"></a>

## [417] Brian Rohde -- Discussion  `METACOMMENT`

- **Section:** Discussion > Interpretation of findings > SRQ4: dedicated ML vs the LLM/traditional baselines
- **Date:** 2026-09-05T18:14:00
- **On:** “Connect to: Humans vs. LLMs (IJF 2024); code-as-action (Wang et al. 2024).”

METACOMMENT

<a id="c420"></a>

## [420] Brian Rohde -- Discussion  `VERIFY * PROSE`

- **Section:** Discussion > Theoretical contributions > Design knowledge contribution (DSR framing)
- **Date:** 2026-09-05T18:15:00
- **On:** “The multi-agent framework constitutes a DSR artefact at two levels (Hevner et al. 2004; Artifact Types in IS Design Science, LNCS 2012): Instantiation level: a working multi-agent system (System A) running on real retail CPG dataMethod/design-theory level: 5 generalised design principles reusable beyond this specific retail contextCite: Hevner 2004, Peffers 2007, AI-Based DSR Framework 2024, Pathways for Design Research on AI 2024, Artifact Types in IS Design Science 2012”

VERIFY, PROSE

<a id="c423"></a>

## [423] Brian Rohde -- Discussion  `VERIFY * NAMING`

- **Section:** Discussion > Theoretical contributions > Design principles (generalised from thesis findings)
- **Date:** 2026-09-05T18:18:00
- **On:** “Table 24 - Contributions - Design Principles”

NAMING, VERIFY, FORMAT

<a id="c424"></a>

## [424] Brian Rohde -- Discussion  `VERIFY * PROSE`

- **Section:** Discussion > Theoretical contributions > Design principles (generalised from thesis findings)
- **Date:** 2026-09-05T18:18:00
- **On:** “Cite: Pathways for Design Research on AI 2024 (ISR), AI-Based DSR Framework 2024, AI-augmented decision making DSR 2024”

VERIFY, PROSE

<a id="c426"></a>

## [426] Brian Rohde -- Discussion  `VERIFY * PROSE`

- **Section:** Discussion > Theoretical contributions > Novelty claims
- **Date:** 2026-09-05T18:18:00
- **On:** “First system to combine: LLM orchestration + ≤8GB constrained ML ensemble + MCDM synthesis + real retail CPG evaluationMemory profiling methodology for multi-component AI pipelines: replicable protocol contributionThe ≤8GB constraint as a design principle, not an afterthought: demonstrates that SME-grade hardware is sufficient for meaningful AI-augmented BI”

VERIFY, PROSE

<a id="c428"></a>

## [428] Brian Rohde -- Discussion  `VERIFY * SOURCE * PROSE`

- **Section:** Discussion > Theoretical contributions > Contribution to IS literature
- **Date:** 2026-09-05T18:19:00
- **On:** “Extends Pathways for Design Research on AI (ISR 2024): provides an instantiated AI artefact evaluated per the editorial’s recommended dimensionsExtends AI-augmented decision making design principles (2024): applies and validates principles in a retail CPG context”

VERIFY, PROSE, SOURCE

<a id="c430"></a>

## [430] Brian Rohde -- Discussion  `VERIFY * SOURCE * PROSE`

- **Section:** Discussion > Practical implications
- **Date:** 2026-09-05T18:19:00
- **On:** “For Manifold AI: validated architecture for integrating predictive analytics into the existing descriptive AI Colleague productFor SME retailers: demonstrates that AI-augmented demand forecasting does not require cloud-scale computeFor IS practitioners: memory profiling methodology is directly transferable to other ML pipeline deployments”

VERIFY, PROSE, SOURCE

<a id="c432"></a>

## [432] Brian Rohde -- Discussion  `VERIFY * PROSE`

- **Section:** Discussion > Limitations
- **Date:** 2026-09-05T18:19:00
- **On:** “Single company/context: Nielsen CSD data from one company’s clients - generalisability untestedData access dependency: if Nielsen access was delayed, fallback dataset may reduce ecological validityLLM non-determinism: claude-sonnet-4-6 at temperature=0 is near-deterministic but not fully; evaluation may not fully replicateEvaluation scope: LLM-as-Judge N=50 is statistically modest; significance claims are indicativeDSR single-cycle: full ADR would require multiple build-evaluate-reflect cycles; thesis completes one cycle”

VERIFY, PROSE

<a id="c434"></a>

## [434] Brian Rohde -- Discussion  `VERIFY * PROSE`

- **Section:** Discussion > Future research directions
- **Date:** 2026-09-05T18:19:00
- **On:** “Multi-agent memory sharing: can agents share intermediate results to reduce redundant computation?Real-time streaming: adapting the pipeline for continuous data ingestion vs. batch weeklyCross-retailer generalisation: test on a different FMCG category or marketFull DSR second cycle: implement design principle refinements identified in this evaluation and re-evaluate”

VERIFY, PROSE

<a id="c435"></a>

## [435] Brian Rohde -- Discussion  `METACOMMENT`

- **Section:** Discussion > Outstanding decisions
- **Date:** 2026-09-05T19:32:00
- **On:** “decisions”

METACOMMENT
