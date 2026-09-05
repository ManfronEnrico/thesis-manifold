# Summary of contributions

> Section of **Conclusion > Summary of contributions**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE. Detail: `comments/sections/14-ch10-conclusion/01-summary-of-contributions.md`

---

This thesis asked: *How can production-oriented agentic decision-support systems without native predictive capabilities be extended with lightweight forecasting models to support reliable, forecast-informed, and cost-justified decision-making under computational and deployment constraints?* The answer it substantiates is that a lightweight gradient-boosted forecasting substrate, exposed through a structured, calibrated interface and synthesised by an LLM, extends a non-predictive agentic system reliably and within an SME-grade resource budget - with the dedicated-model layer justified over both classical and template baselines on the decision-relevant dimensions. The sub-questions resolve as follows.
**SRQ1 (models & efficiency).** Tuned XGBoost is the best lightweight model in every category (test WMAPE 11.4–31.0%), beating LightGBM, Ridge and SeasonalNaive. Category specialisation matters: the best *representation* differs by category (brand×month for CSD/energidrikke/ RTD, brand×chain for danskvand), so “more data” via finer granularity is not uniformly better. All models run in tens of MB - the ≤8 GB constraint is non-binding.
**SRQ2 (structured interface).** Forecasts are exposed with point estimate, split-conformal 90% interval (empirical coverage 80–98%), and a confidence tier; an LLM synthesises these into recommendations that an independent GPT-4o judge rates above a rule-based template on four of five dimensions (mean 3.81 vs 3.15), establishing reliability and traceability with a usefulness/accuracy trade-off to manage.
**SRQ3 (integration readiness).** Assessed, not enacted: the substrate is reproducible and tool-call-ready; the gap to live integration with the Prometheus Graph Engine is operational (access/credentials), not architectural.
**SRQ4 (dedicated ML vs baselines).** Dedicated ML beats the ARIMA traditional baseline in three of four categories; the code-as-action LLM comparator - the central v4 test - requires an execution sandbox (E2B) not configured here and is the main open empirical item. On the evidence gathered, dedicated integration is justified over classical and templated alternatives.
The thesis thus delivers a working DSR design artefact plus transferable design knowledge for cost-justified, forecast-informed agentic decision-support under resource constraints; the code-as-action comparison and a production integration remain for a second cycle.
