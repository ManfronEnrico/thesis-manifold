# Design principles (generalised from thesis findings)

> Section of **Discussion > Theoretical contributions > Design principles (generalised from thesis findings)**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- VERIFY, NAMING, PROSE. Detail: `comments/sections/13-ch9-discussion/02-theoretical-contributions/02-design-principles-generalised-from-thesis-findings.md`

---

| # | Principle | Problem class | Evidence from this thesis |
|---|---|---|---|
| DP1 | Sequential execution | Multi-model ML pipelines within ≤4 GB RAM | Load → fit → predict → del → gc.collect(); measured peak RAM is tens of MB per model (Ridge 1.5, LightGBM 18.7, XGBoost 0.2 MB) - the 8 GB budget is non-binding at this data scale |
| DP2 | Post-hoc calibration | Confidence scoring in ML-based recommendation systems | Split-conformal interval calibrated on validation residuals; ensemble achieves 80–98% empirical coverage against a 90% nominal (CSD 96.6%) |
| DP4 | LLM-as-synthesiser | Translating ML outputs into managerial recommendations | Claude API synthesises a multi-model ensemble + confidence into an actionable natural language recommendation |
| DP5 | Computational transparency | AI pipeline artefacts evaluated for practical deployment | RAM and latency profiling reported alongside MAPE/RMSE; tracemalloc per component |
**Table** **24** - Contributions - Design Principles
Cite: Pathways for Design Research on AI 2024 (ISR), AI-Based DSR Framework 2024, AI-augmented decision making DSR 2024
