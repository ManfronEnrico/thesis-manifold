# SRQ1 — Ridge fitted per-brand vs pooled

Ridge is run in the same fitting regimes as the tabular models so the
**method** and the **fitting regime** can be separated. The per-brand
figures come from `stat_baselines.csv`.

**Only feature-based learners appear here.** Naive, seasonal-naive and
drift are per-series definitions with no cross-sectional form, and
ARIMA/Prophet are univariate by construction — pooling them is
undefined, not merely unimplemented.

| Regime | Category | WMAPE | medMAPE | alpha | clipped | n test |
|---|---|---|---|---|---|---|
| within_category | CSD | 22.8% | 28.8% | 10.0 | 27 | 665 |
| within_category | danskvand | 21.5% | 35.1% | 1.0 | 5 | 174 |
| within_category | energidrikke | 22.1% | 41.5% | 0.001 | 20 | 308 |
| within_category | RTD | 56.3% | 34.3% | 0.001 | 28 | 372 |
| all_categories | CSD | 25.1% | 31.9% | 0.001 | 26 | 665 |
| all_categories | danskvand | 24.0% | 36.4% | 0.001 | 7 | 174 |
| all_categories | energidrikke | 19.9% | 33.0% | 0.001 | 25 | 308 |
| all_categories | RTD | 52.0% | 36.5% | 0.001 | 23 | 372 |

`clipped` counts predictions that hit the extrapolation bound (that
series' observed maximum x 3). A high count means the bound, not the
model, is setting the error — the defect that motivated this script
(P0040 F53). It should be near zero in the pooled regimes.

