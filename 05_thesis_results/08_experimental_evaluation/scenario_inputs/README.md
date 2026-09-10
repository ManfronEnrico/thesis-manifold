# Scenario inputs

One CSV per brand: the monthly sales history a scenario is given, and
nothing else. This is exactly what Scenario B receives in its prompt and
what Scenario D is handed, so the two arms differ only in the
orchestrator around them.

Forecast horizon: **H=3** (months ahead).

## Columns

| Column | Meaning |
|---|---|
| `period_year`, `period_month` | the observation month |
| `sales_units` | units sold, that brand, that month |
| `promo_intensity` | share of units sold on promotion, lagged; absent where Nielsen reports no promotion for the category |

## What is deliberately NOT here

The **held-out months are withheld** from every CSV. Each series stops at
the training cutoff; the month being forecast is not in the file a model
sees. `index.csv` records `scored_month` and `held_out_actual` so a run
can be verified, but a scenario is never shown them.

## Selection

Three brands per category: highest, median and lowest volume among those
with a complete non-zero held-out window. The spread is deliberate, so
results can be read for sparse brands as well as strong ones.

## Provenance

Written by `04_SRQ4_Scenario_Experiment/scenario_setup/export_scenario_inputs.py`, which calls the experiment harness's own
`_brand_history()` rather than rebuilding the series -- so these files
cannot drift from what the scenarios actually run on.
