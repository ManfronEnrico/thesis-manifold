# Theoretical contribution (design principles)

> Section of **Conclusion > Theoretical contribution (design principles)**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE. Detail: `comments/sections/14-ch10-conclusion/02-theoretical-contribution-design-principles.md`

---

Propose generalisable design principles (DSR design-theory output):
**Sequential execution principle**: ML pipeline RAM budgets must be planned for sequential, not concurrent, model execution; a load, run, unload protocol enables sub-8GB multi-model forecasting
**Delegation-over-generation principle**: the LLM should orchestrate and delegate numerical prediction to dedicated models rather than generate predictions, or its own forecasting code, itself, when correctness, consistency, and replicability matter
**Cost-justification principle**: dedicated-model integration should be adopted only where it demonstrably beats a code-as-action LLM baseline on the decision-relevant dimensions at justified cost and latency; otherwise an LLM-plus-code approach may suffice
**Structured-interface reliability principle**: exposing forecasts through a structured tool/action interface with output validation and a recorded tool-call-to-recommendation mapping is what makes agentic numerical decision-support auditable
**Computational transparency principle**: deployment-oriented AI artefacts should report RAM, cost, and latency alongside accuracy; these are decision-relevant properties for SME adopters
Note: uncertainty calibration is a design consideration deferred to future work (see §10.5)
Cite: DSR design-theory sources (Hevner et al., 2004; Peffers et al., 2007; plus AI-DSR references)
