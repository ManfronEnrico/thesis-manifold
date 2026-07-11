# SRQ1 — Final Model Comparison
_Generated 2026-04-16T21:21:29_

Comparison of the new global ML pipeline (results/ml_retrain_2026-04-16) against the Phase-1 per-brand benchmark (results/phase1/benchmark_summary_v2.md). All numbers are on the same VAL window (Mar-Aug 2025, 77 brands).

## Ranking (median MAPE across brands)

| Model | n_brands | Median MAPE | Δ vs Phase-1 LightGBM (31.03) |
|---|---:|---:|---:|
| aeon_Rocket_top10 | 10 | 14.54 | ▼ -16.49 |
| PyMC_hier_top10 | 10 | 17.27 | ▼ -13.76 |
| LightGBM_global | 77 | 29.83 | ▼ -1.20 |
| XGBoost_global | 77 | 30.09 | ▼ -0.94 |
| SeasonalNaive | 77 | 49.37 | ▲ +18.34 |
| NaiveMean | 77 | 57.51 | ▲ +26.48 |
| ARIMA_top10 | 10 | 71.86 | ▲ +40.83 |
| Ridge_global | 77 | 73.12 | ▲ +42.09 |
| OLS_global | 77 | 73.42 | ▲ +42.39 |

## Phase-1 reference (per-brand best-of, 77 brands each)

| Model | Median MAPE |
|---|---:|
| Phase1_LightGBM_perBrand | 31.03 |
| Phase1_Ensemble_perBrand | 31.59 |
| Phase1_XGBoost_perBrand | 32.84 |
| Phase1_Ridge_perBrand | 39.90 |
| Phase1_SeasonalNaive | 49.37 |
| Phase1_ARIMA_perBrand | 49.60 |
| Phase1_Prophet_perBrand | 58.61 |

## Gate G4 verdict

- **Criterion**: Global LightGBM median MAPE ≤ 31.03 (Phase-1 per-brand LightGBM).
- **Observed**: 29.83%
- **Verdict**: ✅ PASSED


## Methodology notes

- Feature set (31 cols) excludes contemporaneous functions of the target (`sales_value`, `sales_liters`, `promo_units`) to avoid leakage. Causal lags (1–13 months), rolling stats (3/4/6/13), cyclical seasonality (month_sin/cos), brand-level priors (mean/std/rank from TRAIN only), and promo/distribution features are retained.
- Hyperparameters selected via walk-forward CV (5 expanding folds inside TRAIN, horizon = 3 months). Final models refit on full TRAIN before VAL evaluation.
- TEST window (Sep 2025 – Mar 2026) is held out; not touched in this report. Final test-set numbers will be produced in the next iteration.
- Top-10 scoped models (aeon Rocket, PyMC hier.) are illustrative of brand-specific ceilings; not directly comparable to 77-brand global models.

## Artefact inventory

- `results/ml_retrain_2026-04-16/baselines_val.csv`
- `results/ml_retrain_2026-04-16/baselines_summary.md`
- `results/ml_retrain_2026-04-16/baselines_predictions.parquet`
- `results/ml_retrain_2026-04-16/advanced_val.csv`
- `results/ml_retrain_2026-04-16/advanced_summary.md`
- `results/ml_retrain_2026-04-16/advanced_predictions.parquet`
- `results/ml_retrain_2026-04-16/shap_feature_importance.csv`
- `results/ml_retrain_2026-04-16/shap_values_val.npy`
- `results/ml_retrain_2026-04-16/MANIFEST.json`
- `results/ml_retrain_2026-04-16/ingestion_report.md`
- `results/ml_retrain_2026-04-16/cleaning_report.md`
- `results/ml_retrain_2026-04-16/feature_engineering_report.md`
- `reports/eda/index.html` — EDA figures
- `reports/shap/index.html` — SHAP figures
- `reports/final/*.png` — publication figures