# SRQ1: Forecasting accuracy under constraints

> Section of **Discussion > Interpretation of findings > SRQ1: Forecasting accuracy under constraints**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- VERIFY, METACOMMENT. Detail: `comments/sections/13-ch9-discussion/01-interpretation-of-findings/01-srq1-forecasting-accuracy-under-constraints.md`

---

Tuned *XGBoost* was the best model in every category, ahead of *LightGBM*, *Ridge*, and the *SeasonalNaive* baseline, confirming that gradient boosting over engineered lag/rolling/calendar features is the strongest lightweight family for this monthly FMCG panel. The selected per-category configurations reach test WMAPE of 16.5% (CSD), 22.0% (danskvand), 11.4% (energidrikke) and 31.0% (RTD). RTD remains hardest - short, volatile, promotion-blind series. A central and somewhat counter-intuitive result is that finer granularity does not uniformly help: disaggregating to a retail-chain dimension multiplied training rows roughly sixfold yet improved accuracy only for danskvand, while CSD, energidrikke and RTD forecast better at the aggregated brand level. This is a signal-to-noise effect - more rows of noisier per-chain demand do not beat fewer rows of a cleaner aggregate - and it motivates the per-category representation choice (Ch6 §6.5.6). On the operational axis the ≤8 GB constraint is non-binding at this data scale: peak RAM is in the tens of MB for every model and inference is sub-second, so the accuracy-optimal model also fits the budget with no compromise. SHAP attributes forecasts chiefly to last-month sales (lag_1) and shelf availability (weighted_distribution), which is consistent with retail demand dynamics and lends face validity to the models.  *Connect to: Edge AI / Efficient & Green LLMs (the constraint is easily met); gradient-boosting-for-retail literature.*
