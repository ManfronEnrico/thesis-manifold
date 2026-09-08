# 5.5.8 Remaining gaps

> Section of **Chapter 5 | Model Benchmark & Selection > 5.5 Results > 5.5.8 Remaining gaps**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE. Detail: `comments/sections/09-ch5-framework-design/05-5-5-results/08-5-5-8-remaining-gaps.md`

---

**The ≤15% accuracy target has been withdrawn, not scored.** Verification found the benchmark does not exist in the cited source (§6.4.3). Accuracy is therefore assessed against the simple benchmarks of §6.5.2 alone, on which two of four categories are beaten outright.
The tuning protocol is not nested, so every cross-validation figure above is optimistically biased by an unquantified amount (§6.3.5).
ARIMA and Prophet use a fixed specification per series rather than a per-series order search, on cost grounds. Their figures are a competent baseline, not the best attainable from those families.
fig4_ram_budget is stale and contradicts §6.5.6.
