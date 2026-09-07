# The Bounded Tool-Using Agentic Layer

> Section of **Predictive-Extension Architecture > The Bounded Tool-Using Agentic Layer**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**4 comment(s) on this section** -- CONTEXT, VERIFY. Detail: `comments/sections/09-ch5-framework-design/05-the-bounded-tool-using-agentic-layer.md`

---

The agentic layer is an LLM orchestrator accessed through a remote API rather than loaded locally, a decision that keeps the language model out of the RAM budget entirely (a locally hosted model would add several gigabytes; Semerikov et al., 2025). Given a decision-support prompt, the layer invokes the forecasting substrate through the structured interface, optionally combines multiple model outputs, and produces a concise, confidence-qualified natural-language recommendation, subject to human-in-the-loop checkpoints.
The layer embodies a **delegation-over-generation** principle: the LLM does not itself predict demand or compute the forecast, but delegates numerical prediction to the dedicated models and confines itself to orchestration, validation, and communication. Decoding is configured for reproducibility (temperature zero). This separation of a generative orchestrator from deterministic predictive components is the architectural feature that makes the agentic numerical decision-support both auditable and resource-feasible.
