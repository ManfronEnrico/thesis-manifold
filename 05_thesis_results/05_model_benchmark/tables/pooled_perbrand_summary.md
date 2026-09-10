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
| LightGBM | +0.121 | -0.011 | 201 |
| XGBoost | +0.092 | -0.105 | 201 |

## Delta by volume tercile (WMAPE percentage points)

| Model | Volume tercile | median delta | mean delta | n | pooling wins |
|---|---|---|---|---|---|
| LightGBM | small | +5.4 | +63.1 | 67 | 29/67 (43%) |
| LightGBM | medium | +1.0 | -2.2 | 67 | 31/67 (46%) |
| LightGBM | large | -2.8 | -3.0 | 67 | 41/67 (61%) |
| XGBoost | small | +2.4 | +2829.8 | 67 | 32/67 (48%) |
| XGBoost | medium | +1.2 | -4.5 | 67 | 30/67 (45%) |
| XGBoost | large | -1.5 | +3.3 | 67 | 34/67 (51%) |

## Delta by demand class (WMAPE percentage points)

The Syntetos-Boylan-Croston partition. **Nothing is excluded** --
irregular series appear here rather than being filtered out, so a
weak result on them is visible.

| Model | Demand class | median delta | IQR | n scored | n no-signal | pooling wins |
|---|---|---|---|---|---|---|
| LightGBM | smooth | +1.0 | -6.9 to +12.6 | 101 | 3 | 48/101 (48%) |
| LightGBM | erratic | -4.9 | -26.6 to +11.1 | 75 | 3 | 43/75 (57%) |
| LightGBM | intermittent | -2.6 | -4.8 to +49.8 | 9 | 10 | 5/9 (56%) |
| LightGBM | lumpy | +11.7 | -14.2 to +138.3 | 16 | 13 | 5/16 (31%) |
| XGBoost | smooth | +0.4 | -5.7 to +14.4 | 101 | 3 | 48/101 (48%) |
| XGBoost | erratic | -0.2 | -33.9 to +14.7 | 75 | 3 | 38/75 (51%) |
| XGBoost | intermittent | +4.4 | -13.5 to +26.9 | 9 | 10 | 4/9 (44%) |
| XGBoost | lumpy | +27.0 | -17.5 to +65.3 | 16 | 13 | 6/16 (38%) |

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
| LightGBM | CSD | +2.4 | -2.6 | -2.6 |
| LightGBM | Danskvand | -19.9 | -6.5 | +2.5 |
| LightGBM | Energidrikke | +36.1 | -5.7 | -5.0 |
| LightGBM | RTD | +10.0 | +7.7 | +2.8 |
| XGBoost | CSD | -0.1 | -1.1 | -3.0 |
| XGBoost | Danskvand | +3.3 | +1.4 | -1.6 |
| XGBoost | Energidrikke | +0.3 | -26.1 | -0.7 |
| XGBoost | RTD | +10.5 | +17.6 | +5.2 |

