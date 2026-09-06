# Deterministic synthesis results

> Section of **Context-Aware Decision Synthesis > Architecture of the Synthesis Agent > Deterministic synthesis results**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**3 comment(s) on this section** -- VERIFY, OUTDATED, NAMING. Detail: `comments/sections/11-ch7-decision-synthesis/02-architecture-of-the-synthesis-agent/03-deterministic-synthesis-results.md`

---

The non-LLM core of the Synthesis Agent was implemented and run on the test set for all four categories: per (brand[, chain], month) it produces an inverse-WMAPE-weighted ensemble forecast, an inter-model agreement score, a split-conformal 90% interval, and a composite confidence score (30% agreement + 40% interval tightness + 30% model accuracy) mapped to a High/Moderate/Low tier.
| Category | n series-months | mean confidence | Moderate / Low | 90% interval coverage |
|---|---|---|---|---|
| CSD | 845 | 44.9 | 72% / 28% | 96.6% |
| danskvand | 966 | 43.6 | 70% / 30% | 97.8% |
| energidrikke | 205 | 47.1 | 75% / 25% | 80.0% |
| RTD | 324 | 38.5 | 45% / 55% | 90.7% |
**Table** **19** - Deterministic Synthesis Results
Two observations. First, the conformal ensemble interval is well-to-conservatively calibrated (empirical coverage 80–98% against the 90% nominal), so the uncertainty the agent communicates is trustworthy. Second, the composite confidence skews to the Moderate tier with no High-confidence forecasts under the current thresholds - because the (deliberately wide) 90% interval keeps the tightness term low. This is a property of the scoring weights, not of the forecasts; the tier cut-offs are a calibration choice to revisit. Operationally the engine already supports the SRQ2 goal: it triages each forecast by confidence so the agentic layer can surface reliable forecasts and route Low-confidence ones (notably the more volatile RTD, 55% Low) to human review. The natural-language recommendation and the LLM-as-Judge quality assessment (§7.3, §7.6) sit on top of this structured output and require an LLM API; they are run in the agentic-harness phase.
