# Prophet (Meta)

> Section of **Model Benchmark & Selection > Model descriptions > Prophet (Meta)**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, SOURCE, PROSE. Detail: `comments/sections/10-ch6-model-benchmark/02-model-descriptions/03-prophet-meta.md`

---

Additive decomposable model, **y(t) = g(t) + s(t) + h(t) + ε**  - trend, seasonality, holidays (Taylor & Letham, 2018, p. 38, Eq. 1)
Designed for forecasting at scale by analysts with domain rather than statistical expertise, targeting “piecewise trends, multiple seasonality, floating holidays” (pp. 37–38)
**No holiday calendar is supplied in this thesis**, and none of the multi-seasonality machinery applies at month grain
RAM: ~50–100 MB; acceptable
