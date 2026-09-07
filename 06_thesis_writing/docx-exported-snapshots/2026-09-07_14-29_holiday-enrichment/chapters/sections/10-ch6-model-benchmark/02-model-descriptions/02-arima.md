# ARIMA

> Section of **Model Benchmark & Selection > Model descriptions > ARIMA**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, SOURCE, PROSE. Detail: `comments/sections/10-ch6-model-benchmark/02-model-descriptions/02-arima.md`

---

Classical univariate time-series model in the Box–Jenkins framework
Role: statistical baseline representing established traditional forecasting
**Implementation:** **statsmodels**  **SARIMAX(order=(1,1,1))** **on log sales, fitted per brand.** A fixed order, not a search -  pmdarima/auto_arima was unavailable in the environment. **This is a stated limitation**: ARIMA is not order-optimised, so its numbers are a floor for the family rather than its best achievable performance
RAM: ~0.5 MB measured; negligible
Limitation: assumes stationarity; univariate, so no promotional or calendar inputs
