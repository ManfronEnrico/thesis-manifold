# SRQ1 — per-brand pooled-vs-per-category breakdown

Tests the F50 explanation directly: *does pooling help large series
and hurt small ones within a category?*

`delta` = pooled error - per-category error. **Negative = pooling is
better for that brand.** If the explanation holds, delta should rise
with brand size (pooling helps small brands, hurts large ones), i.e.
a **positive** correlation between delta and size.

Brands scored: 460 rows (213 distinct brands x 2 models).

**WMAPE statistics below use all 460 rows.** WMAPE is defined against zero actuals (the sum is in the denominator), so no exclusion is needed or applied.

**A volume floor of 1 unit/month applies to the WMAPE tables**, leaving 384 of 460 rows. Brands below it average under one unit across the whole test window; WMAPE is arithmetically defined there but produces deltas in the thousands of percentage points (89 rows exceed 100pp, with a median volume of 0.0 units/month). That is division by an almost-empty denominator, not evidence about pooling. **This is a declared inclusion criterion, not the scorability filter** -- a different decision, made for a different reason.

**MAPE-family statistics use the 336 scorable rows** (124, 27%, have a zero actual somewhere in the test window, where APE is undefined rather than merely large). Hyndman & Koehler (2006, p. 683) criticise dropping such windows as impractical, which is a further reason to read the WMAPE columns as primary here.

## Correlation of delta with brand size

| Model | vs log(train rows) | vs log(mean test units) | n |
|---|---|---|---|
| LightGBM | +0.028 | +0.152 | 192 |
| XGBoost | +0.114 | +0.176 | 192 |

## Delta by volume tercile (WMAPE percentage points)

| Model | Volume tercile | median delta | mean delta | n | pooling wins |
|---|---|---|---|---|---|
| LightGBM | small | -9.0 | -15.8 | 64 | 36/64 (56%) |
| LightGBM | medium | +6.7 | +2.3 | 64 | 26/64 (41%) |
| LightGBM | large | +0.6 | +1.1 | 64 | 31/64 (48%) |
| XGBoost | small | -8.4 | -27.6 | 64 | 42/64 (66%) |
| XGBoost | medium | -0.5 | -4.2 | 64 | 35/64 (55%) |
| XGBoost | large | -0.3 | -0.1 | 64 | 35/64 (55%) |

## Per-category, per-tercile (WMAPE pp, median)

| Model | Category | small | medium | large |
|---|---|---|---|---|
| LightGBM | CSD | -1.3 | +9.0 | -0.3 |
| LightGBM | danskvand | -1.0 | -0.5 | +8.0 |
| LightGBM | energidrikke | -49.4 | -3.9 | -1.2 |
| LightGBM | RTD | -3.3 | +9.8 | +1.8 |
| XGBoost | CSD | -8.4 | +3.7 | -0.4 |
| XGBoost | danskvand | -1.8 | -12.5 | +1.1 |
| XGBoost | energidrikke | -23.7 | -7.1 | -0.3 |
| XGBoost | RTD | -7.7 | -3.8 | -0.0 |

