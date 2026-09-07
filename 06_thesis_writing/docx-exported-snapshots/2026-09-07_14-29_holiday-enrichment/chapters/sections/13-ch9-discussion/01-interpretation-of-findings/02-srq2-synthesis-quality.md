# SRQ2: Synthesis quality

> Section of **Discussion > Interpretation of findings > SRQ2: Synthesis quality**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY. Detail: `comments/sections/13-ch9-discussion/01-interpretation-of-findings/02-srq2-synthesis-quality.md`

---

The deterministic synthesis core produced well-to-conservatively calibrated ensemble intervals (empirical coverage 80–98% against a 90% nominal), so the uncertainty the system communicates is trustworthy. The composite confidence score skewed to the Moderate tier with no High-confidence forecasts under the current thresholds - an artefact of weighting interval *tightness* heavily while the conformal 90% interval is deliberately wide; the tier cut-offs, not the forecasts, are what need recalibration. On recommendation quality, the LLM synthesis added clear value over a rule-based template: GPT-4o (LLM-as-Judge, N=50) scored it higher on actionability (4.00 vs 2.14), relevance (4.00 vs 3.28), clarity (4.34 vs 3.46) and calibration (3.74 vs 3.46), with the template ahead only on accuracy (3.42 vs 2.96). The weakest LLM dimension is therefore accuracy: turning numbers into prose occasionally drifts from a strict reading of the inputs - a usefulness/precision trade-off, and the clearest target for prompt hardening. *Connect to: Kuleshov 2018 (calibration); AI-augmented decision-making DSR 2024.*
