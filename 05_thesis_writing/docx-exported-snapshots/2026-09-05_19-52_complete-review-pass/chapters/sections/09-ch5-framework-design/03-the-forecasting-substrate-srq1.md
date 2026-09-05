# The Forecasting Substrate (SRQ1)

> Section of **Predictive-Extension Architecture > The Forecasting Substrate (SRQ1)**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**3 comment(s) on this section** -- MISSING, UPDATE, VERIFY. Detail: `comments/sections/09-ch5-framework-design/03-the-forecasting-substrate-srq1.md`

---

The substrate comprises lightweight models spanning the accuracy-efficiency frontier: ARIMA, Prophet, LightGBM, XGBoost, and Ridge Regression, evaluated across the five beverage categories and compared in their category-specialised and pooled variants (Chapter 6). The gradient-boosted models use the exogenous predictors described in Chapter 4, namely promotional, distribution, and calendar features, alongside autoregressive features; the two promotional features are inactive for the promo-zero categories.
Two design decisions follow from the RAM constraint. First, models are executed **sequentially** (load, run, unload) so that only one model occupies memory at a time, rather than concurrently. Second, memory is profiled by **process resident set size** (RSS, via the Python psutil and resource interfaces) rather than by tracemalloc alone, because tracemalloc does not capture the native allocations of XGBoost and LightGBM. The substrate exposes, for each forecast, a point estimate accompanied by interval information; where multiple models are combined, it aggregates them using inverse-MAPE weighting in the spirit of Ahrens et al. (2024). Stability across repeated runs is treated as a production-relevant property alongside accuracy (Klee and Xia, 2025).
Measured locally on the largest category (CSD), the per-model fit footprint is small in RSS terms: XGBoost adds about 15 MB, LightGBM about 7 MB, and Ridge under 1 MB over the runtime baseline (sequential, one model resident at a time). For reference, a tracemalloc run capturing Python-level allocations alone reports even smaller per-fit peaks (Ridge 1.5 MB, LightGBM 18.7 MB, XGBoost 0.2 MB; ARIMA fitted per series at ~0.5 MB), confirming that native library buffers are the larger but still modest component. Either way the substrate operates two orders of magnitude below the four-gigabyte ceiling; the binding effect of the RAM budget is on the model-selection *space* (it excludes transformer and locally hosted options up front), not on the footprint of the selected models. Component figures are consolidated in  **Table** **6**.
