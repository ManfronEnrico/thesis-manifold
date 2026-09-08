<!-- PROSE STRIPPED 2026-09-01 (P0044).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-01_18-50/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 10 — Conclusion

> **P0044 OPEN (2026-09-01): RAM figure needs reconciling.** This file states an
> 8 GB budget. That number is a project assumption, not a sourced one -- Ng (2017)
> argues memory is the binding design variable, not that SMEs get 8 GB. Manifold's
> production Prometheus E2B template is provisioned at a **measured 4096 MB**
> (`fxe7gzkqjupdhbx4uvpr`, verified live 2026-09-01). Prefer the measured figure.
> All results hold under the tighter bound (serving 36.8 MB, refit ~37 MB).
> See `plans/P0044_2026-09-01_17-10_resource-measurement-and-retrain-arms/findings.md` F22-F23.

> Status: DRAFT written from real results 2026-06-24 (§10.1 SRQ answers). RQs v4.
> SRQ4 partial (code-as-action sandbox pending). Pending human review.
> Last updated: 2026-06-24

---

## 10.1 Summary of contributions

- **SRQ1 (models & efficiency).** Tuned XGBoost is the best lightweight model in
- **SRQ2 (structured interface).** Forecasts are exposed with point estimate,
- **SRQ3 (integration readiness).** Assessed, not enacted: the substrate is
- **SRQ4 (dedicated ML vs baselines).** Dedicated ML beats the ARIMA traditional

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
