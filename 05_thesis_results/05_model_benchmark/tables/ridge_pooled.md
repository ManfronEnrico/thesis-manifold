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
| within_category | CSD | 20.4% | 51.9% | 0.001 | 0 | 665 |
| within_category | Danskvand | 42.4% | 57.6% | 10.0 | 1 | 174 |
| within_category | Energidrikke | 22.7% | 90.5% | 0.001 | 8 | 308 |
| within_category | RTD | 67.4% | 69.3% | 10.0 | 3 | 372 |
| all_categories | CSD | 28.0% | 53.9% | 0.001 | 0 | 665 |
| all_categories | Danskvand | 27.5% | 52.0% | 0.001 | 0 | 174 |
| all_categories | Energidrikke | 19.1% | 98.2% | 0.001 | 0 | 308 |
| all_categories | RTD | 69.5% | 67.4% | 0.001 | 0 | 372 |

`clipped` counts predictions that hit the extrapolation bound (that
series' observed maximum x 3). A high count means the bound, not the
model, is setting the error — the unbounded extrapolation defect
that motivated it. It should be near zero in the pooled regimes.

