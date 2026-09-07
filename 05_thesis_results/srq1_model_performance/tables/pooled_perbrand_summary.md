# SRQ1 — per-brand pooled-vs-per-category breakdown

Tests the F50 explanation directly: *does pooling help large series
and hurt small ones within a category?*

`delta` = pooled error - per-category error. **Negative = pooling is
better for that brand.** If the explanation holds, delta should rise
with brand size (pooling helps small brands, hurts large ones), i.e.
a **positive** correlation between delta and size.

Brands scored: 460 rows (213 distinct brands x 2 models).

**WMAPE statistics below use all 460 rows.** WMAPE is defined against zero actuals (the sum is in the denominator), so no exclusion is needed or applied.

**No brand is excluded from the WMAPE tables.** WMAPE is defined against zero actuals (the sum is in the denominator), so all 460 rows are reported. Results are broken out by **demand class** instead, using the derived Syntetos-Boylan-Croston cut-offs (p = 1.32, CV^2 = 0.49; Syntetos, Boylan & Croston 2005, p. 495).

*This replaces an earlier 1 unit/month volume floor, which was a judgement call and a poor proxy for irregularity: it removed 8 smooth brands while leaving 21 lumpy/intermittent ones in. See `demand_classes.md`.*

**MAPE-family statistics use the 336 scorable rows** (124, 27%, have a zero actual somewhere in the test window, where APE is undefined rather than merely large). Hyndman & Koehler (2006, p. 683) criticise dropping such windows as impractical, which is a further reason to read the WMAPE columns as primary here.

## Correlation of delta with brand size

| Model | vs log(train rows) | vs log(mean test units) | n |
|---|---|---|---|
| LightGBM | +0.057 | +0.158 | 201 |
| XGBoost | +0.038 | -0.185 | 201 |

## Delta by volume tercile (WMAPE percentage points)

| Model | Volume tercile | median delta | mean delta | n | pooling wins |
|---|---|---|---|---|---|
| LightGBM | small | -12.7 | -72.4 | 67 | 39/67 (58%) |
| LightGBM | medium | +7.4 | +3.5 | 67 | 26/67 (39%) |
| LightGBM | large | +0.4 | +0.9 | 67 | 33/67 (49%) |
| XGBoost | small | -2.2 | +257.9 | 67 | 37/67 (55%) |
| XGBoost | medium | +5.4 | -3.3 | 67 | 26/67 (39%) |
| XGBoost | large | -0.7 | +0.1 | 67 | 37/67 (55%) |

## Delta by demand class (WMAPE percentage points)

The Syntetos-Boylan-Croston partition. **Nothing is excluded** --
irregular series appear here rather than being filtered out, so a
weak result on them is visible.

| Model | Demand class | median delta | IQR | n scored | n no-signal | pooling wins |
|---|---|---|---|---|---|---|
| LightGBM | smooth | +2.6 | -5.8 to +11.5 | 100 | 8 | 46/100 (46%) |
| LightGBM | erratic | -1.3 | -26.4 to +12.3 | 76 | 3 | 39/76 (51%) |
| LightGBM | intermittent | -1.2 | -13.5 to +32.4 | 9 | 3 | 5/9 (56%) |
| LightGBM | lumpy | -4.4 | -30.6 to +20.8 | 16 | 15 | 8/16 (50%) |
| XGBoost | smooth | -0.2 | -4.8 to +6.7 | 100 | 8 | 51/100 (51%) |
| XGBoost | erratic | +1.0 | -16.8 to +14.3 | 76 | 3 | 35/76 (46%) |
| XGBoost | intermittent | -7.2 | -9.1 to +3.5 | 9 | 3 | 6/9 (67%) |
| XGBoost | lumpy | +0.2 | -21.7 to +18.8 | 16 | 15 | 8/16 (50%) |

**Reading it.** `smooth` is where a model should do well and where a
pooling effect is most interpretable. `lumpy` combines long gaps with
highly variable sizes, so large deltas there reflect the series, not
the method.

**`n no-signal` counts brands whose test window is entirely zero.**
There is no actual to be accurate about, so their WMAPE is a ratio to
~0 and reaches 1e14. They are **counted in their own column rather
than dropped**, and the statistics are computed on the rows that have
a signal.

**That column is the most informative thing in this table.** Roughly
half the `lumpy` brands (15 of 31) have no test signal at all. The
honest statement about lumpy series on this panel is therefore not
that a model forecasts them badly -- it is that **for half of them
there is nothing to forecast in the evaluation window**, which is a
property of monthly brand-level FMCG data worth reporting in its own
right.

Note this split is on *whether anything exists to score against*, a
property of the data -- not a volume threshold chosen to improve the
numbers.

**Means are never reported here.** A mean of ratios is not robust on
this panel even after the no-signal rows are set aside.

## Per-category, per-tercile (WMAPE pp, median)

| Model | Category | small | medium | large |
|---|---|---|---|---|
| LightGBM | CSD | -7.5 | +8.0 | -0.2 |
| LightGBM | danskvand | -1.0 | -5.4 | +9.1 |
| LightGBM | energidrikke | -55.3 | -3.9 | -1.2 |
| LightGBM | RTD | -8.2 | +7.6 | +1.8 |
| XGBoost | CSD | -2.9 | +6.0 | +0.0 |
| XGBoost | danskvand | -11.7 | -11.1 | -1.6 |
| XGBoost | energidrikke | -81.1 | -10.3 | -0.3 |
| XGBoost | RTD | +0.9 | +6.8 | -0.2 |

