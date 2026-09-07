# The Structured Forecast-Tool Interface (SRQ2)

> Section of **Predictive-Extension Architecture > The Structured Forecast-Tool Interface (SRQ2)**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY. Detail: `comments/sections/09-ch5-framework-design/04-the-structured-forecast-tool-interface-srq2.md`

---

The interface is the mechanism by which a forecast is exposed to the agentic layer, and is the locus of SRQ2. It is realised as a **JSON-based function-calling contract with strict output schemas**: the agentic layer invokes the substrate as a tool and receives a structured response containing the point forecast and its interval. The interface is designed to preserve three properties:
**Reliability**, by validating the agent’s stated numbers against the source forecast values before delivery, so that the agent reports the model’s  numbers rather than its own.
**Uncertainty**, by attaching interval information to every forecast; interval calibration follows the post-hoc approach of Kuleshov et al. (2018) and is treated as a design target, not an empirically validated property of the current prototype.
**Traceability**, by recording the mapping from tool call and forecast value to the resulting recommendation, so that each recommendation can be audited back to its source forecast.
The artefact deliberately adopts JSON function-calling, rather than code-as-action, for **reliability and reproducibility**: the schema-constrained interface yields deterministic, auditable tool calls. The code-as-action pattern (Wang et al., 2024) is not used inside the artefact; it is instead the baseline against which the artefact is compared (Section 5.7).
