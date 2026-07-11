# Step 08 — Advanced Models Summary (VAL set)
_Generated 2026-04-16T21:19:05_

## Ranking (median MAPE, lower is better)

| model | n_brands | median_mape | mean_mape | median_wape | mean_rmse | mean_mae |
|---|---|---|---|---|---|---|
| aeon_Rocket_top10 | 10 | 14.54 | 24.31 | 14.30 | 509345.75 | 446430.97 |
| PyMC_hier_top10 | 10 | 17.27 | 24.89 | 17.26 | 499518.99 | 436105.47 |
| LightGBM_global | 77 | 29.83 | 54.40 | 27.38 | 54880.95 | 46636.23 |
| XGBoost_global | 77 | 30.09 | 44.07 | 30.15 | 50137.26 | 41670.17 |

## Training metadata

```json
{
  "LightGBM_global": {
    "best_cfg": {
      "num_leaves": 31,
      "learning_rate": 0.03,
      "n_estimators": 1200,
      "feature_fraction": 0.85,
      "min_data_in_leaf": 20
    },
    "cv_median_mape": 42.29317746848472,
    "elapsed_s": 48.8
  },
  "XGBoost_global": {
    "best_cfg": {
      "max_depth": 4,
      "learning_rate": 0.08,
      "n_estimators": 500,
      "subsample": 0.9,
      "colsample_bytree": 0.9
    },
    "cv_median_mape": 43.81531512146911,
    "elapsed_s": 22.1
  },
  "PyMC_hier_top10": {
    "elapsed_s": 5.4
  },
  "aeon_Rocket_top10": {
    "elapsed_s": 4.9
  }
}
```