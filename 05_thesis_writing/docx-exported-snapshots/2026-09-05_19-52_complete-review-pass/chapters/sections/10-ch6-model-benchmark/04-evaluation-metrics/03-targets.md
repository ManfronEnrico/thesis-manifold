# Targets

> Section of **Model Benchmark & Selection > Evaluation metrics > Targets**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, SOURCE, PROSE. Detail: `comments/sections/10-ch6-model-benchmark/04-evaluation-metrics/03-targets.md`

---

**Accuracy target: none imported from the literature.** Earlier drafts carried a ≤15% WMAPE target attributed to Ceran et al. (2024). Source-level verification (2026-08-25) found **no such benchmark in that paper**: the authors explicitly reject MAPE because their panel contains too many zero-demand observations for a percentage error to be well defined, and report WRMSSE, RMSE and MAE instead. The target is therefore withdrawn, and **no claim that an external accuracy target is met or approached should be written anywhere in the thesis**
**What replaces it: the simple benchmarks of §6.2.0**, scored on this thesis’s own test rows (§6.5.2). This is the stricter test and needs no cross-study metric alignment - a target borrowed from a daily product-store study with a 15-day horizon was never comparable to brand × month at H=3 in any case
**Calibration target: ≥85% empirical coverage** for a nominal 90% interval -  **and interval width must be reported alongside**, since an arbitrarily wide interval attains perfect coverage while carrying no decision-relevant information
