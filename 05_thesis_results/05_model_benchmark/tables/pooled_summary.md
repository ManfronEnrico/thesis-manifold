# SRQ1 — pooled vs per-category (Optuna-tuned, TPE, seed=42)

Trials per model: 30. Both arms use the SAME 17-feature
intersection (`promo_intensity` dropped — absent in at least one
category), the same tuning protocol, and are scored on the SAME
per-category test rows. One pooled model is trained across all
categories and evaluated separately on each; the per-category arm is
re-trained here on those 17 features rather than read from
`tuned_metrics.csv`, so the two arms differ only in which rows they
were trained on.

Series key is `(category, brand)`: brand names are not unique across
categories and `OTHER BRAND` is a per-category residual bucket.

## LightGBM

| Category | pooled WMAPE | per-category WMAPE | delta (pp) | pooled medMAPE | per-cat medMAPE | n test |
|---|---|---|---|---|---|---|
| CSD | 19.3% | 18.7% | +0.6 | 48.2% | 51.5% | 665 |
| Danskvand | 21.0% | 26.7% | -5.7 | 45.6% | 57.6% | 174 |
| Energidrikke | 15.5% | 21.1% | -5.6 | 87.0% | 80.4% | 308 |
| RTD | 31.3% | 31.9% | -0.6 | 65.1% | 46.9% | 372 |

## XGBoost

| Category | pooled WMAPE | per-category WMAPE | delta (pp) | pooled medMAPE | per-cat medMAPE | n test |
|---|---|---|---|---|---|---|
| CSD | 21.7% | 19.1% | +2.6 | 51.3% | 48.9% | 665 |
| Danskvand | 18.9% | 23.4% | -4.5 | 45.8% | 56.9% | 174 |
| Energidrikke | 16.8% | 16.8% | +0.1 | 79.9% | 81.3% | 308 |
| RTD | 40.5% | 30.8% | +9.8 | 62.5% | 51.9% | 372 |

Positive delta = the per-category model is more accurate on that
category (pooled WMAPE is higher). Negative = pooling wins.

