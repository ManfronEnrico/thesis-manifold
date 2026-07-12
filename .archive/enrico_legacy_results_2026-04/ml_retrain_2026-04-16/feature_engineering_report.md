# Step 04 — Feature Engineering Report
_Generated 2026-04-16T20:26:46_

- Rows: 3,234
- Columns before: 22
- Columns after: 39
- Output: `data/features/feature_matrix_v3.parquet`

## New features added

| Feature | Missing | Rationale |
|---|---:|---|
| `sales_units_lag_6` | 462 | Half-year lag suggested by PACF shape. |
| `sales_units_lag_12` | 924 | Annual seasonality suggested by ACF peak at 12. |
| `sales_units_rm_3` | 77 | Short-run momentum (causal 3-month mean). |
| `sales_units_rstd_3` | 154 | Short-run volatility. |
| `sales_units_rmedian_3` | 77 | Robust short-run central tendency. |
| `sales_units_rm_6` | 77 | Medium-run trend. |
| `sales_units_rstd_6` | 154 | Medium-run volatility. |
| `sales_units_rmedian_6` | 77 | Robust medium-run central tendency. |
| `sales_units_yoy_growth_lag1` | 1109 | Causal YoY growth: (lag_1 - lag_13)/lag_13. |
| `month_sin` | 0 | Cyclical seasonality encoding (sin component). |
| `month_cos` | 0 | Cyclical seasonality encoding (cos component). |
| `months_since_start` | 0 | Linear trend regressor. |
| `unit_price_lag_1` | 227 | Causal price proxy (sales_value / units, shifted). |
| `promo_momentum_3` | 77 | Rolling 3m promo intensity (causal). |
| `brand_mean_sales` | 0 | Brand-level baseline (TRAIN only, no leakage). |
| `brand_std_sales` | 0 | Brand-level dispersion (TRAIN only). |
| `brand_rank` | 0 | Brand volume rank (TRAIN only, dense rank). |

## Leakage safeguards

- All lags/rollings use causal shift (past-only).
- Brand aggregates computed on TRAIN rows only, then broadcast.
- Unit price proxy uses shift(1) — no contemporaneous info.