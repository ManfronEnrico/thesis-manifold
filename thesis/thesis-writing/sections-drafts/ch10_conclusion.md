# Chapter 10 — Conclusion
> Status: BULLET POINT SKELETON — not prose yet
> Last updated: 2026-03-14

---

## 10.1 Summary of contributions

- Restate the main RQ: *How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?*
- Answer each SRQ in 2–3 sentences based on findings:
  - SRQ1: [best model, MAPE achieved, RAM footprint — within/at/near constraint]
  - SRQ2: [confidence calibration coverage, LLM-as-Judge score, quality vs. baseline]
  - SRQ3: [consumer signal contribution to MAPE, which retailer segments benefited]
  - SRQ4: [AI system vs. descriptive BI comparison — dimensions of superiority and where human judgment still dominates]
- State the thesis's position: the system achieves [X] on all 4 SRQs, constituting a validated proof-of-concept for AI-augmented demand forecasting in SME retail contexts

---

## 10.2 Theoretical contribution (design principles)

- Propose 3–5 generalisable design principles from the thesis findings (DSR design theory output):
  1. **Sequential execution principle**: ML pipeline RAM budgets must be planned assuming sequential (not concurrent) model execution; load–run–unload protocol enables sub-8GB multi-model forecasting
  2. **Post-hoc calibration principle**: confidence scoring in recommendation systems must use held-out calibration data; raw model uncertainty estimates are systematically miscalibrated
  3. **Consumer signal integration principle**: demand forecasting accuracy improves when external consumer demand indices are included as features; survey-derived consumer segments are a viable proxy where transaction loyalty data is unavailable
  4. **LLM-as-synthesiser principle**: LLM orchestration adds measurable decision quality value when it translates calibrated multi-model outputs into contextualised natural language recommendations; LLMs should not replace ML models but synthesise their outputs
  5. **Computational transparency principle**: AI pipeline artefacts evaluated for practical deployment should report RAM and latency alongside accuracy metrics; these are decision-relevant properties for SME adopters
- Cite: Pathways for Design Research on AI (ISR 2024), AI-Based DSR Framework 2024, AI-augmented decision making DSR 2024

---

## 10.3 Practical recommendations for Manifold AI

- Phase 1: integrate the sequential ML ensemble as the predictive backbone of the AI Colleague tool (replace/augment current descriptive analytics)
- Phase 2: add Indeks Danmark consumer signal enrichment for retailers with available segment data
- Phase 3: deploy Synthesis Agent as a recommendation layer on top of the predictive outputs
- Infrastructure: deployable on M2 MacBook (≤8GB RAM) or equivalent cloud instance (t3.large, 8GB RAM, ~$0.10/hr) — no GPU required

---

## 10.4 Limitations recap

- Single empirical context (Danish CSD market, one partner company)
- One DSR design cycle — findings require validation across additional contexts before generalisation
- LLM API dependency: Synthesis Agent requires internet access and Anthropic API availability

---

## 10.5 Future research

- Second DSR cycle: refine design principles based on this evaluation and re-implement
- Extend to other FMCG categories: grocery, dairy, beer — same architecture, different feature profiles
- Adapt for streaming data: real-time pipeline for weekly automated forecasts
- Validate consumer signal methodology with alternative data sources (loyalty cards, scanner data)

---

## 10.6 Final statement

- The thesis demonstrates that a resource-constrained, multi-agent AI system can meaningfully augment FMCG demand forecasting — not by replacing domain expertise, but by structuring and contextualising it
- This positions AI not as a replacement for the category manager, but as a calibrated decision partner
- Close with the IS research framing: the framework is a validated DSR artefact that advances IS design knowledge on AI-augmented decision making in SME retail contexts

---

## Outstanding decisions

- Exact language for the "answer" to each SRQ — depends on empirical results
- Whether to include a one-page executive summary before Chapter 1 (not counted toward page limit)
- Whether to add a reflective paragraph on the collaborative human-AI research process (relevant to philosophy of science section)
