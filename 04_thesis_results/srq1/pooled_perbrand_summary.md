# SRQ1 — per-brand pooled-vs-per-category breakdown

Tests the F50 explanation directly: *does pooling help large series
and hurt small ones within a category?*

`delta` = pooled error - per-category error. **Negative = pooling is
better for that brand.** If the explanation holds, delta should rise
with brand size (pooling helps small brands, hurts large ones), i.e.
a **positive** correlation between delta and size.

Brands scored: 460 rows (213 distinct brands x 2 models). Excluded as unscorable (zero actual in test window): 124 rows.

## Correlation of delta with brand size

| Model | vs log(train rows) | vs log(mean test units) | n |
|---|---|---|---|
| LightGBM | -0.014 | +0.137 | 168 |
| XGBoost | +0.155 | +0.252 | 168 |

## Delta by volume tercile (WMAPE percentage points)

| Model | Volume tercile | median delta | mean delta | n | pooling wins |
|---|---|---|---|---|---|
| LightGBM | small | +2.0 | -3.9 | 56 | 26/56 (46%) |
| LightGBM | medium | +2.9 | +2.5 | 56 | 25/56 (45%) |
| LightGBM | large | +2.2 | +1.3 | 56 | 26/56 (46%) |
| XGBoost | small | -6.9 | -13.9 | 56 | 38/56 (68%) |
| XGBoost | medium | -1.0 | -6.7 | 56 | 33/56 (59%) |
| XGBoost | large | -0.3 | -0.0 | 56 | 30/56 (54%) |

## Per-category, per-tercile (WMAPE pp, median)

| Model | Category | small | medium | large |
|---|---|---|---|---|
| LightGBM | CSD | +0.2 | +10.1 | -0.2 |
| LightGBM | danskvand | -0.1 | +9.1 | +6.8 |
| LightGBM | energidrikke | -12.7 | -3.9 | -1.2 |
| LightGBM | RTD | +0.4 | +7.5 | +1.8 |
| XGBoost | CSD | -7.6 | +3.6 | -0.3 |
| XGBoost | danskvand | -27.9 | -2.4 | -0.5 |
| XGBoost | energidrikke | -7.1 | -8.0 | +0.4 |
| XGBoost | RTD | -7.7 | -4.4 | +0.7 |

