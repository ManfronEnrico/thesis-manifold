# Comments — Conclusion

Extracted 2026-09-05 from `MSc. Data Science - 175888 and 176171 - Master Thesis.docx`.
8 comment(s) in 8 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [437](#c437) | Conclusion | FORMATTING |  | FORMATTING: Could use a subtitle for the chapter... |
| [439](#c439) | Summary of contributions | VERIFY, PROSE |  | VERIFY, PROSE... |
| [441](#c441) | Theoretical contribution (design principles) | VERIFY, PROSE |  | VERIFY, PROSE... |
| [443](#c443) | Practical recommendations for Manifold AI | VERIFY, PROSE |  | VERIFY & PROSE... |
| [445](#c445) | Limitations recap | VERIFY, PROSE |  | VERIFY, PROSE... |
| [447](#c447) | Future research | VERIFY, PROSE |  | VERIFY, PROSE... |
| [449](#c449) | Final statement | VERIFY, PROSE |  | VERIFY, PROSE... |
| [450](#c450) | Outstanding decisions | METACOMMENT |  | METACOMMENT... |

---

<a id="c437"></a>

## [437] Brian Rohde -- Conclusion  `FORMATTING`

- **Section:** Conclusion
- **Date:** 2026-09-05T18:53:00
- **On:** “COULD USE A SUBTITLE”

FORMATTING: Could use a subtitle for the chapter

<a id="c439"></a>

## [439] Brian Rohde -- Conclusion  `VERIFY * PROSE`

- **Section:** Conclusion > Summary of contributions
- **Date:** 2026-09-05T18:22:00
- **On:** “This thesis asked: How can production-oriented agentic decision-support systems without native predictive capabilities be extended with lightweight forecasting models to support reliable, forecast-informed, and cost-justified decision-making under computational and deployment constraints? The answer it substantiates is that a lightweight gradient-boosted forecasting substrate, exposed through a structured, calibrated interface and synthesised by an LLM, extends a non-predictive agentic system reliably and within an SME-grade resource budget - with the dedicated-model layer justified over both classical and template baselines on the decision-relevant dimensions. The sub-questions resolve as follows.SRQ1 (models & efficiency). Tuned XGBoost is the best lightweight model in every category (test WMAPE 11.4–31.0%), beating LightGBM, Ridge and SeasonalNaive. Category specialisation matters: the best representation differs by category (brand×month for CSD/energidrikke/ RTD, brand×chain for danskvand), so “more data” via finer granularity is not uniformly better. All models run in tens of MB - the ≤8 GB constraint is non-binding.SRQ2 (structured interface). Forecasts are exposed with point estimate, split-conformal 90% interval (empirical coverage 80–98%), and a confidence tier; an LLM synthesises these into recommendations that an independent GPT-4o judge rates above a rule-based template on four of five dimensions (mean 3.81 vs 3.15), establishing reliability and traceability with a usefulness/accuracy trade-off to manage.SRQ3 (integration readiness). Assessed, not enacted: the s […495 more characters — see the chapter file…] ssical and templated alternatives.The thesis thus delivers a working DSR design artefact plus transferable design knowledge for cost-justified, forecast-informed agentic decision-support under resource constraints; the code-as-action comparison and a production integration remain for a second cycle.”

VERIFY, PROSE

<a id="c441"></a>

## [441] Brian Rohde -- Conclusion  `VERIFY * PROSE`

- **Section:** Conclusion > Theoretical contribution (design principles)
- **Date:** 2026-09-05T18:23:00
- **On:** “Propose generalisable design principles (DSR design-theory output): Sequential execution principle: ML pipeline RAM budgets must be planned for sequential, not concurrent, model execution; a load, run, unload protocol enables sub-8GB multi-model forecastingDelegation-over-generation principle: the LLM should orchestrate and delegate numerical prediction to dedicated models rather than generate predictions, or its own forecasting code, itself, when correctness, consistency, and replicability matterCost-justification principle: dedicated-model integration should be adopted only where it demonstrably beats a code-as-action LLM baseline on the decision-relevant dimensions at justified cost and latency; otherwise an LLM-plus-code approach may sufficeStructured-interface reliability principle: exposing forecasts through a structured tool/action interface with output validation and a recorded tool-call-to-recommendation mapping is what makes agentic numerical decision-support auditableComputational transparency principle: deployment-oriented AI artefacts should report RAM, cost, and latency alongside accuracy; these are decision-relevant properties for SME adoptersNote: uncertainty calibration is a design consideration deferred to future work (see §10.5)Cite: DSR design-theory sources (Hevner et al., 2004; Peffers et al., 2007; plus AI-DSR references)”

VERIFY, PROSE

<a id="c443"></a>

## [443] Brian Rohde -- Conclusion  `VERIFY * PROSE`

- **Section:** Conclusion > Practical recommendations for Manifold AI
- **Date:** 2026-09-05T18:23:00
- **On:** “Integrate the lightweight forecasting substrate as a callable tool in the production agentic system (Prometheus) via its Graph Engine, exposing forecasts and uncertainty through the structured interfaceAdopt dedicated-model integration where the SRQ4 evaluation shows it beats the code-as-action baseline on correctness, consistency, and replicability at acceptable cost; otherwise rely on the LLM-plus-code approachInfrastructure: deployable within an approximately 8GB RAM budget (for example a t3.large-class cloud instance), no GPU required [cloud-pricing citation: resolve in global references pass]”

VERIFY & PROSE

<a id="c445"></a>

## [445] Brian Rohde -- Conclusion  `VERIFY * PROSE`

- **Section:** Conclusion > Limitations recap
- **Date:** 2026-09-05T18:23:00
- **On:** “Empirical context bounded to the Danish beverage retail market (five Nielsen categories) and a single partner companyOne DSR design cycle; findings require validation across additional contexts before generalisationSRQ4 evaluation at pilot scale (on the order of fifty prompts), not a full study; results provisional pending the final improved modelsSRQ3 assessed as integration readiness (production access pending), not a live integrationLLM API dependency for the agentic layer; uncertainty calibration is designed but not empirically validated”

VERIFY, PROSE

<a id="c447"></a>

## [447] Brian Rohde -- Conclusion  `VERIFY * PROSE`

- **Section:** Conclusion > Future research
- **Date:** 2026-09-05T18:24:00
- **On:** “Full-scale SRQ4 evaluation across the complete prompt set; a second DSR cycle refining the design principlesActive integration into the production system (Prometheus Graph Engine) once access is granted: a before/after study on reliability and costEmpirical calibration of forecast uncertainty (post-hoc isotonic regression), currently designed onlyAdapt for streaming/real-time forecasting (currently monthly batch processing)Code-as-action as the artefact’s own action format (replacing JSON function-calling), distinct from its use as the SRQ4 baseline, where the prototype’s 0% numerical hallucination under JSON makes the marginal benefit an open question (Wang et al., 2024)”

VERIFY, PROSE

<a id="c449"></a>

## [449] Brian Rohde -- Conclusion  `VERIFY * PROSE`

- **Section:** Conclusion > Final statement
- **Date:** 2026-09-05T18:24:00
- **On:** “The thesis demonstrates how a resource-constrained agentic decision-support system can be extended with lightweight forecasting, the LLM structuring and contextualising dedicated-model predictions rather than replacing domain expertise or generating the predictions itselfThis positions AI as a calibrated decision partner, not a replacement for the category managerClose with the IS research framing: a validated DSR artefact plus design knowledge on cost-justified, forecast-informed agentic decision-support in SME retail contexts”

VERIFY, PROSE

<a id="c450"></a>

## [450] Brian Rohde -- Conclusion  `METACOMMENT`

- **Section:** Conclusion > Outstanding decisions
- **Date:** 2026-09-05T19:33:00
- **On:** “decisions”

METACOMMENT
