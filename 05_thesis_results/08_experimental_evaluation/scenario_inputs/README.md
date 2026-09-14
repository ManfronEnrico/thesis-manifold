# Scenario inputs

One CSV per brand: the monthly sales history a scenario is given, and
nothing else. This is exactly what Scenario B receives in its prompt and
what Scenario D is handed, so the two arms differ only in the
orchestrator around them.

Forecast horizon: **H=3** (months ahead).

## What this export covers

- **Exported:** 2026-09-14
- **Categories:** CSD
- **Brands:** HARBOE, 7-UP, ØRBÆK
- **Shape:** 32 columns per file

These are the brands the funded experiment scored. Categories whose
warehouse extract was never built are not represented here, because the
experiment never ran on them -- see *Provenance* below.

## Columns

Each file carries the brand-month row **as the sales data warehouse
produces it**, after joining the fact and dimension tables and
aggregating to brand-month. That is volume, value and litres, their
promotion and baseline splits, and the distribution measures -- the
columns a production agent would see by querying the star schema.

Two points a reader should not have to infer:

- **These are warehouse columns, not engineered features.** No lag,
  rolling statistic or ratio built by the modelling pipeline appears
  here. Handing those over would give away the work SRQ4 exists to
  measure.
- **The scenario also receives the warehouse's own column
  documentation**, so the columns are not unexplained. Withholding it
  would make a poor result unfalsifiable.

## What is deliberately NOT here

The **held-out months are withheld** from every CSV. Each series stops at
the training cutoff; the month being forecast is not in the file a model
sees. `index.csv` records `scored_month` and `held_out_actual` so a run
can be verified, but a scenario is never shown them.

## Selection

Up to three brands per category: highest, median and lowest volume among
those with a complete non-zero held-out window whose scored actual clears
the 1,000-unit floor. The spread is deliberate, so results can
be read for sparse brands as well as strong ones; the floor exists
because a defined percentage error is not automatically a meaningful
one, and on a nine-unit series it measures integer rounding.

## Provenance

Written by `04_SRQ4_Scenario_Experiment/scenario_setup/export_scenario_inputs.py`, which calls the experiment harness's own
`_brand_history()` rather than rebuilding the series.

**This is an export, and an export has a date.** It reflects the brand
selection and column shape in force on the date above. It is not
self-updating: if the selection rule or the extract changes, this folder
is stale until the script is run again. Re-run it rather than editing
anything here by hand.
