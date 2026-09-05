# Rationale for model selection

> Section of **Model Benchmark & Selection > Rationale for model selection**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, SOURCE, PROSE. Detail: `comments/sections/10-ch6-model-benchmark/01-rationale-for-model-selection.md`

---

**Five model families span the inductive-bias spectrum**: classical statistical (ARIMA, Prophet), gradient boosting (LightGBM, XGBoost), regularised linear (Ridge), plus four parameter-free benchmarks (mean, naive, seasonal-naive, drift)
**Selection criteria**: (a) established empirical performance on retail/FMCG panels;
fit within the ≤8 GB sequential RAM budget; (c) interpretability sufficient for the SRQ4 scenario comparison; (d) diversity of inductive bias
**The benchmark rung is required, not decorative.** Hyndman & Athanasopoulos (2021, §5.2) define the four simple methods as benchmarks against which “any forecasting methods we develop will be compared … to ensure that the new method is better than these simple alternatives”. A forecasting result reported without them is unbenchmarked
**Empirical weight for that requirement** comes from M4: of six pure machine-learning entries, none beat the statistical combination benchmark and only one beat Naïve2 (Makridakis et al., 2018, p. 803)
**NOT included, and why**: deep sequence models (LSTM/N-BEATS) - RAM footprint incompatible with the ≤8 GB constraint, and infeasible under the HPO time budget on ~30 monthly observations per series
