# Remaining gaps

> Section of **Model Benchmark & Selection > Results > Remaining gaps**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE. Detail: `comments/sections/10-ch6-model-benchmark/05-results/08-remaining-gaps.md`

---

**The ≤15% accuracy target has been withdrawn, not scored.** Verification found the benchmark does not exist in the cited source (§6.4.3). Accuracy is therefore assessed against the simple benchmarks of §6.5.2 alone, on which two of four categories are beaten outright.
The tuning protocol is not nested, so every cross-validation figure above is optimistically biased by an unquantified amount (§6.3.5).
ARIMA and Prophet use a fixed specification per series rather than a per-series order search, on cost grounds. Their figures are a competent baseline, not the best attainable from those families.
fig4_ram_budget is stale and contradicts §6.5.6.
