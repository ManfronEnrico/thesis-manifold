# Results

> Section of **Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > Results**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**3 comment(s) on this section** -- VERIFY, OUTDATED, INCORRECT. Detail: `comments/sections/12-ch8-experimental-evaluation/03-level-2-recommendation-quality-evaluation-srq2/04-results.md`

---

On N=50 stratified test cases, GPT-4o (LLM-as-Judge, independent model family) scored the Synthesis-Agent recommendation against a rule-based template baseline on five Likert(1–5) dimensions:
| System | accuracy | calibration | actionability | relevance | clarity | mean |
|---|---|---|---|---|---|---|
| LLM synthesis | 2.96 | 3.74 | 4.00 | 4.00 | 4.34 | 3.81 |
| Rule-based baseline | 3.42 | 3.46 | 2.14 | 3.28 | 3.46 | 3.15 |
**Table** **21** - LLM Judge Scoring Likert Scale Results
The LLM synthesis clearly adds value on **actionability** (4.00 vs 2.14), **relevance** (4.00 vs 3.28), **clarity** (4.34 vs 3.46) and **calibration** (3.74 vs 3.46) - answering the SRQ2 “does the LLM add value over a template?” question affirmatively on four of five dimensions. The baseline edges out the LLM only on **accuracy** (3.42 vs 2.96): the template merely restates the forecast number, so it cannot contradict its inputs, whereas the LLM’s added interpretation occasionally drifts from a strict reading of the numbers - a precision/usefulness trade-off worth stating. Interval calibration is empirically validated separately (§8.3.2 / Ch6 §6.5.4: ensemble conformal coverage 80–98% against the 90% nominal). The human-analyst comparison (§8.3.3) requires a Manifold team member and is not run here; the SRQ4 code-as-action comparator requires an execution sandbox (E2B key not configured) and is deferred.
