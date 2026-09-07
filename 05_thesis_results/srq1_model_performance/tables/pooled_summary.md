# SRQ1 — pooled vs per-category (Optuna-tuned, TPE, seed=42)

Trials per model: 30. Both arms use the SAME 12-feature
intersection (`promo_intensity` dropped — absent in danskvand and
RTD), the same tuning protocol, and are scored on the SAME
per-category test rows. One pooled model is trained across all
categories and evaluated separately on each; the per-category arm is
re-trained here on 12 features rather than read from
`tuned_metrics.csv`, so the two arms differ only in which rows they
were trained on.

Series key is `(category, brand)`: brand names are not unique across
categories and `OTHER BRAND` is a per-category residual bucket.

## LightGBM

| Category | pooled WMAPE | per-category WMAPE | delta (pp) | pooled medMAPE | per-cat medMAPE | n test |
|---|---|---|---|---|---|---|
| CSD | 17.5% | 16.3% | +1.2 | 40.3% | 37.0% | 665 |
| danskvand | 21.4% | 23.7% | -2.2 | 37.3% | 47.4% | 174 |
| energidrikke | 12.1% | 13.7% | -1.6 | 50.3% | 57.8% | 308 |
| RTD | 35.8% | 35.1% | +0.7 | 55.0% | 43.4% | 372 |

## XGBoost

| Category | pooled WMAPE | per-category WMAPE | delta (pp) | pooled medMAPE | per-cat medMAPE | n test |
|---|---|---|---|---|---|---|
| CSD | 19.1% | 15.3% | +3.8 | 37.6% | 35.5% | 665 |
| danskvand | 19.7% | 20.9% | -1.2 | 30.0% | 50.8% | 174 |
| energidrikke | 12.7% | 15.5% | -2.8 | 50.1% | 41.0% | 308 |
| RTD | 37.3% | 36.0% | +1.3 | 40.5% | 35.0% | 372 |

Positive delta = the per-category model is more accurate on that
category (pooled WMAPE is higher). Negative = pooling wins.

