# Model selection decision

> Section of **Model Benchmark & Selection > Model selection decision**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE. Detail: `comments/sections/10-ch6-model-benchmark/06-model-selection-decision.md`

---

**The choice between LightGBM and XGBoost is not supported by this data.** A five-seed sweep with every input held identical shows **the winning model changes with the seed in all four categories** (§6.5.7). Naming a winner per category would be reporting one seed’s outcome as a finding
**The defensible claim is that the two are statistically indistinguishable here**, the between-seed spread exceeding the between-model difference. This is a weaker headline but a true one, and it is useful: a practitioner deciding what to deploy can choose on operational grounds - training time, memory, tooling - rather than accuracy
**What the benchmark does support** is the gap between *families*: both gradient boosters clearly beat Ridge and ARIMA on most categories, and clearly lose to seasonal naive on RTD. Those differences exceed the seed noise; the LightGBM-vs-XGBoost one does not
**The served model carries its own track record.** The forecast tool returns the selected model’s measured accuracy (WMAPE and median APE), both simple baselines for that category, and a conformal interval - so the consuming agent receives the forecast’s reliability alongside the forecast
**Metric disagreement is surfaced, not hidden.** Where WMAPE and median APE rank models differently, the payload flags it rather than silently reporting one
**Ensemble combination is evaluated as a separate scenario**, not folded into this chapter’s selection. M4’s evidence that combinations outperform single models (Makridakis et al., 2018) motivates it, and treating it as its own rung is what makes the contribution measurable rather than assumed
