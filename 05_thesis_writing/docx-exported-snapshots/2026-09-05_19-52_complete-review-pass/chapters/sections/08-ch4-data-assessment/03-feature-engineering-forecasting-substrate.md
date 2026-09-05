# Feature Engineering (forecasting substrate)

> Section of **Data Assessment > Feature Engineering (forecasting substrate)**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**4 comment(s) on this section** -- VERIFY, UPDATE, SOURCE. Detail: `comments/sections/08-ch4-data-assessment/03-feature-engineering-forecasting-substrate.md`

---

The forecasting substrate uses features derived from the Nielsen facts table at the brand × month granularity. The feature matrix contains 22 columns: **14 modelling features** per observation, plus index/key columns, the target, the carried promo_units, and the split label (verified against the parquet, scripts/srq1_benchmark_tuned.py). These are the exogenous and autoregressive predictors referenced in Chapter 1.
| Feature | Description | Models |
|---|---|---|
| lag_1, lag_2, lag_3, lag_4, lag_8, lag_13 | Lagged “sales_units” (short, medium, seasonal) | LightGBM, XGBoost, Ridge |
| rolling_mean_4, rolling_std_4 | 4-month rolling mean and standard deviation | LightGBM, XGBoost, Ridge |
| rolling_mean_13 | Trailing annual average | LightGBM, XGBoost, Ridge |
| month, quarter, peak_month | Calendar features (peak_month = month in the category’s derived PEAK_MONTHS) | LightGBM, XGBoost, Ridge |
| “promo_intensity” | Promotional share of units (clipped 0–1) | LightGBM, XGBoost, Ridge |
| weighted_distribution | Nielsen weighted-distribution availability proxy | LightGBM, XGBoost, Ridge |
**Table** **4** - Feature Engineering Overview
The 14 features comprise six lags, three rolling statistics, three calendar features, “promo_intensity”, and weighted_distribution. Two clarifications resolve earlier ambiguity: log_”sales_units” is the **modelling target** (the models predict log sales and exponentiate back), **not** an input feature - using it as a predictor would be trivial leakage; and weighted_distribution  **is** the fourteenth input feature, while the raw promo_units column is carried through the matrix but is not itself a model input (only its derived “promo_intensity” is). Index/target/label columns carried alongside the features: brand, “period_index”, “period_year”, “period_month”, “sales_units” (raw target), “log_sales_units” (log target), “promo_units”, split. Lag and rolling features carry “NaN” for short history (expected); no imputation is done in preprocessing, so the tree models handle NaN natively and the linear model receives a zero-fill at fit time.
ARIMA and Prophet are fitted as univariate statistical baselines on the (log) sales series, not on the tabular feature matrix. The promotional feature is not informative for danskvand and RTD (promo-zero) and is handled accordingly for those categories.
