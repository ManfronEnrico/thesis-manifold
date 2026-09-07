# SRQ1 -- mean absolute scaled error (MASE)

Scaling denominator: in-sample MAE of the one-step naive forecast, per
brand, computed on train+val in raw units (Hyndman & Koehler, 2006,
pp. 684-685).

**MASE < 1 beats a naive one-step forecast on that series' own history;
MASE > 1 does not.** Unlike WMAPE and median MAPE, this threshold is
absolute rather than relative to another model.

**Mean and median are both reported.** Mean MASE is a mean of ratios and
is not robust: on RTD it reads 6.54 while the median reads 0.18, because
one brand (STRONGBOW) has a scaled error near 317. Quote the median as
the typical case and the mean only with that caveat attached.

| Category | Model | MASE (mean) | MASE (median) | WMAPE | medMAPE | n_test | % series scaled | % rows MAPE-scorable |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| CSD | Naive | 0.947 | **0.386** | 29.2% | 36.0% | 665 | 100.0% | 86.2% |
| CSD | SeasonalNaive | 1.633 | **0.885** | 34.9% | 70.6% | 665 | 100.0% | 86.2% |
| danskvand | Naive | 0.990 | **0.516** | 24.3% | 35.7% | 174 | 100.0% | 81.6% |
| danskvand | SeasonalNaive | 1.603 | **1.131** | 44.0% | 50.6% | 174 | 100.0% | 81.6% |
| energidrikke | Naive | 0.672 | **0.050** | 22.6% | 30.9% | 308 | 100.0% | 71.4% |
| energidrikke | SeasonalNaive | 2.016 | **1.030** | 30.6% | 95.4% | 308 | 100.0% | 71.4% |
| RTD | Naive | 6.544 | **0.178** | 67.0% | 34.1% | 372 | 100.0% | 79.3% |
| RTD | SeasonalNaive | 14.023 | **0.992** | 54.8% | 73.8% | 372 | 100.0% | 79.3% |

## Why the last two columns matter

`% rows MAPE-scorable` is the share of test rows on which a percentage
error is defined at all. Where it is well below 100%, every MAPE-family
number in this project is computed on a **subset** of the data, and that
subset is not random -- it excludes the intermittent, low-volume brands.

`% series scaled` is the share with a usable MASE denominator; it is
lower than 100% only for brands with a perfectly flat training history,
where MASE is undefined for a different and much rarer reason.

Hyndman & Koehler (2006, p. 683) call dropping zero-actual windows "an
artificial solution that is impossible to apply in practical
situations". Reporting MASE alongside is what lets those rows be scored
rather than discarded.
