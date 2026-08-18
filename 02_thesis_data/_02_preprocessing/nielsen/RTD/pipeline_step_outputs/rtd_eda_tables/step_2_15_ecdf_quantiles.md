## Target Distribution Quantiles (sales_units)

- Cumulative share of brand-months at or below each sales_units value; shows the spread without the bin-width dependence a histogram introduces.
- p50 = 433 against p90 = 39,708: the gap between them is the concentration this panel has to forecast across.
- A long right tail here is the empirical case for LOG_TRANSFORM_TARGET. The second panel shows the same data after log1p, where an approximately straight curve indicates the transform has done its job.
- Companion to 3.02 (skewness): that figure states the asymmetry as a single number, this one shows where in the distribution it sits.

| quantile   |      value |
|:-----------|-----------:|
| p25        |    57.2900 |
| p50        |   432.6420 |
| p75        |  4375.3472 |
| p90        | 39707.6000 |
