# Outstanding decisions

> Section of **Model Benchmark & Selection > Outstanding decisions**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, METACOMMENT. Detail: `comments/sections/10-ch6-model-benchmark/08-outstanding-decisions.md`

---

**Resolved since this list was written**  - retained so the reasoning is traceable:
Exact train/validation/test dates pending Nielsen access → data in hand; splits fixed, test sizes stated in §6.3.1
HPO trial budget: 50 trials, may reduce under RAM pressure → **100 trials**, and RAM was never the binding constraint (peak in the tens of MB against an 8 GB budget)
Whether to add a 6th model → four simple benchmarks added instead, which is the standard set and answers the “is it better than doing nothing” question directly
**Genuinely open:**
Which metric the ≤15% benchmark refers to.  **Closed 2026-08-25**: the benchmark is not in the cited source at all; the target is withdrawn (§6.4.3)
**Whether ARIMA should be order-searched.** The fixed SARIMAX(1,1,1) is a floor for the family, not its best performance, and the baseline comparison is weaker for it
**Whether the ensemble scenario runs**, which determines whether §6.6’s combination paragraph describes a result or a deferred option
