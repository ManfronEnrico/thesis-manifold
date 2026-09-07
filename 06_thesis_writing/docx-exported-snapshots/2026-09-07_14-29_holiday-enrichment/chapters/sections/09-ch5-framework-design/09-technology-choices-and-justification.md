# Technology Choices and Justification

> Section of **Predictive-Extension Architecture > Technology Choices and Justification**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- METACOMMENT, TABLE-REFERENCE, PROSE. Detail: `comments/sections/09-ch5-framework-design/09-technology-choices-and-justification.md`

---

| Choice | Alternative not adopted | Reason |
|---|---|---|
| Lightweight Python coordinator (evaluated) | LangGraph deployment | LangGraph is the production target (Prometheus); the lightweight coordinator is leaner for the evaluated prototype under the RAM budget |
| JSON function-calling interface (artefact) | Code-as-action inside the artefact | Reliability and reproducibility; code-as-action is instead the SRQ4 baseline |
| LightGBM and XGBoost | LSTM, Temporal Fusion Transformer, Chronos | An order of magnitude lower RAM at competitive accuracy on tabular retail data under the period budget |
| LLM via remote API | Locally hosted LLM | Avoids several gigabytes of model weights, keeping the language model out of the RAM budget (Semerikov et al., 2025) |
| Sandbox (e.g. E2B) for the baseline | Bespoke execution harness | Open and local; runs the code-as-action baseline without production access |
**Table** **7** - Technology Choices and Justification
Each choice is argued against the four-gigabyte constraint, in keeping with the design criterion of Chapter 1.
