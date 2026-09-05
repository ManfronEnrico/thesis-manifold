# Comments -- Deterministic synthesis results

> Objections on **Context-Aware Decision Synthesis > Architecture of the Synthesis Agent > Deterministic synthesis results**
>
> Prose: `chapters/sections/11-ch7-decision-synthesis/02-architecture-of-the-synthesis-agent/03-deterministic-synthesis-results.md`
>
> 3 comment(s) in 3 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
3 comment(s) in 3 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [338](#c338) | Deterministic synthesis results | VERIFY, OUTDATED |  | OUTDATED, VERIFY: Wrong grain.... |
| [340](#c340) | Deterministic synthesis results | VERIFY, NAMING |  | NAMING, VERIFY... |
| [341](#c341) | Deterministic synthesis results | VERIFY |  | VERIFY... |

---

<a id="c338"></a>

## [338] Brian Rohde -- Context-Aware Decision Synthesis  `VERIFY * OUTDATED`

- **Section:** Context-Aware Decision Synthesis > Architecture of the Synthesis Agent > Deterministic synthesis results
- **Date:** 2026-09-05T16:34:00
- **On:** “The non-LLM core of the Synthesis Agent was implemented and run on the test set for all four categories: per (brand[, chain], month) it produces an inverse-WMAPE-weighted ensemble forecast, an inter-model agreement score, a split-conformal 90% interval, and a composite confidence score (30% agreement + 40% interval tightness + 30% model accuracy) mapped to a High/Moderate/Low tier.”

OUTDATED, VERIFY:


Wrong grain.

<a id="c340"></a>

## [340] Brian Rohde -- Context-Aware Decision Synthesis  `VERIFY * NAMING`

- **Section:** Context-Aware Decision Synthesis > Architecture of the Synthesis Agent > Deterministic synthesis results
- **Date:** 2026-09-05T16:37:00
- **On:** “Table 19 - Deterministic Synthesis Results”

NAMING, VERIFY

<a id="c341"></a>

## [341] Brian Rohde -- Context-Aware Decision Synthesis  `VERIFY`

- **Section:** Context-Aware Decision Synthesis > Architecture of the Synthesis Agent > Deterministic synthesis results
- **Date:** 2026-09-05T16:37:00
- **On:** “Two observations. First, the conformal ensemble interval is well-to-conservatively calibrated (empirical coverage 80–98% against the 90% nominal), so the uncertainty the agent communicates is trustworthy. Second, the composite confidence skews to the Moderate tier with no High-confidence forecasts under the current thresholds - because the (deliberately wide) 90% interval keeps the tightness term low. This is a property of the scoring weights, not of the forecasts; the tier cut-offs are a calibration choice to revisit. Operationally the engine already supports the SRQ2 goal: it triages each forecast by confidence so the agentic layer can surface reliable forecasts and route Low-confidence ones (notably the more volatile RTD, 55% Low) to human review. The natural-language recommendation and the LLM-as-Judge quality assessment (§7.3, §7.6) sit on top of this structured output and require an LLM API; they are run in the agentic-harness phase.”

VERIFY
