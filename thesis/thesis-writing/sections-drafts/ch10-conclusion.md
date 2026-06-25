# Chapter 10 — Conclusion
> Status: DRAFT written from real results 2026-06-24 (§10.1 SRQ answers). RQs v4.
> SRQ4 partial (code-as-action sandbox pending). Pending human review.
> Last updated: 2026-06-24

---

## 10.1 Summary of contributions

This thesis asked: *How can production-oriented agentic decision-support systems
without native predictive capabilities be extended with lightweight forecasting
models to support reliable, forecast-informed, and cost-justified decision-making
under computational and deployment constraints?* The answer it substantiates is
that a **lightweight gradient-boosted forecasting substrate, exposed through a
structured, calibrated interface and synthesised by an LLM, extends a
non-predictive agentic system reliably and within an SME-grade resource budget** —
with the dedicated-model layer justified over both classical and template baselines
on the decision-relevant dimensions. The sub-questions resolve as follows.

- **SRQ1 (models & efficiency).** Tuned XGBoost is the best lightweight model in
  every category (test WMAPE 11.4–31.0%; energidrikke near the ≤15% target),
  beating LightGBM, Ridge and SeasonalNaive. Category specialisation matters:
  the best *representation* differs by category (brand×month for CSD/energidrikke/
  RTD, brand×chain for danskvand), so "more data" via finer granularity is not
  uniformly better. All models run in tens of MB — the ≤8 GB constraint is
  non-binding.
- **SRQ2 (structured interface).** Forecasts are exposed with point estimate,
  split-conformal 90% interval (empirical coverage 80–98%), and a confidence tier;
  an LLM synthesises these into recommendations that an independent GPT-4o judge
  rates above a rule-based template on four of five dimensions (mean 3.81 vs 3.15),
  establishing reliability and traceability with a usefulness/accuracy trade-off
  to manage.
- **SRQ3 (integration readiness).** Assessed, not enacted: the substrate is
  reproducible and tool-call-ready; the gap to live integration with the Prometheus
  Graph Engine is operational (access/credentials), not architectural.
- **SRQ4 (dedicated ML vs baselines).** Dedicated ML beats the ARIMA traditional
  baseline in three of four categories; the code-as-action LLM comparator — the
  central v4 test — requires an execution sandbox (E2B) not configured here and is
  the main open empirical item. On the evidence gathered, dedicated integration is
  justified over classical and templated alternatives.

The thesis thus delivers a working DSR design artefact plus transferable design
knowledge for cost-justified, forecast-informed agentic decision-support under
resource constraints; the code-as-action comparison and a production integration
remain for a second cycle.

---

## 10.2 Theoretical contribution (design principles)

- Propose generalisable design principles (DSR design-theory output):
  1. **Sequential execution principle**: ML pipeline RAM budgets must be planned for sequential, not concurrent, model execution; a load, run, unload protocol enables sub-8GB multi-model forecasting
  2. **Delegation-over-generation principle**: the LLM should orchestrate and delegate numerical prediction to dedicated models rather than generate predictions, or its own forecasting code, itself, when correctness, consistency, and replicability matter
  3. **Cost-justification principle**: dedicated-model integration should be adopted only where it demonstrably beats a code-as-action LLM baseline on the decision-relevant dimensions at justified cost and latency; otherwise an LLM-plus-code approach may suffice
  4. **Structured-interface reliability principle**: exposing forecasts through a structured tool/action interface with output validation and a recorded tool-call-to-recommendation mapping is what makes agentic numerical decision-support auditable
  5. **Computational transparency principle**: deployment-oriented AI artefacts should report RAM, cost, and latency alongside accuracy; these are decision-relevant properties for SME adopters
- Note: uncertainty calibration is a design consideration deferred to future work (see §10.5)
- Cite: DSR design-theory sources (Hevner et al., 2004; Peffers et al., 2007; plus AI-DSR references)

---

## 10.3 Practical recommendations for Manifold AI

- Integrate the lightweight forecasting substrate as a callable tool in the production agentic system (Prometheus) via its Graph Engine, exposing forecasts and uncertainty through the structured interface
- Adopt dedicated-model integration where the SRQ4 evaluation shows it beats the code-as-action baseline on correctness, consistency, and replicability at acceptable cost; otherwise rely on the LLM-plus-code approach
- Infrastructure: deployable within an approximately 8GB RAM budget (for example a t3.large-class cloud instance), no GPU required [cloud-pricing citation: resolve in global references pass]

---

## 10.4 Limitations recap

- Empirical context bounded to the Danish beverage retail market (five Nielsen categories) and a single partner company
- One DSR design cycle; findings require validation across additional contexts before generalisation
- SRQ4 evaluation at pilot scale (on the order of fifty prompts), not a full study; results provisional pending the final improved models
- SRQ3 assessed as integration readiness (production access pending), not a live integration
- LLM API dependency for the agentic layer; uncertainty calibration is designed but not empirically validated

---

## 10.5 Future research

- Full-scale SRQ4 evaluation across the complete prompt set; a second DSR cycle refining the design principles
- Active integration into the production system (Prometheus Graph Engine) once access is granted: a before/after study on reliability and cost
- Empirical calibration of forecast uncertainty (post-hoc isotonic regression), currently designed only
- Adapt for streaming/real-time forecasting (currently monthly batch processing)
- Code-as-action as the artefact's *own* action format (replacing JSON function-calling), distinct from its use as the SRQ4 baseline, where the prototype's 0% numerical hallucination under JSON makes the marginal benefit an open question (Wang et al., 2024)

---

## 10.6 Final statement

- The thesis demonstrates how a resource-constrained agentic decision-support system can be extended with lightweight forecasting, the LLM structuring and contextualising dedicated-model predictions rather than replacing domain expertise or generating the predictions itself
- This positions AI as a calibrated decision partner, not a replacement for the category manager
- Close with the IS research framing: a validated DSR artefact plus design knowledge on cost-justified, forecast-informed agentic decision-support in SME retail contexts

---

## Outstanding decisions

- Exact "answer" language for each SRQ, dependent on the final empirical results
- Whether to include a one-page executive summary before Chapter 1 (not counted toward page limit)
- Whether to add a reflective paragraph on the collaborative human-AI research process (relevant to the philosophy-of-science section)
