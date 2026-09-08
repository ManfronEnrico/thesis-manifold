---
pid: P0051
created: 2026-09-08 00:00:00
updated: 2026-09-08 00:00:00
---

# P0051 — Findings

All findings below were measured on 2026-09-08 by two independent repo-wide
searches plus a third exhaustive `grep -ril "adfuller\|adf_"` covering
`worktrees/`. Paths are as they resolved on that date.

---

## F1 — Per-brand ADF recommendations are computed and reported, never consumed

**Producer**: `01_SRQ1_Model_Training/01_thesis_data/_02_preprocessing/nielsen/_shared_modules/step_2_eda_descriptive.py`,
`s05_stationarity()` at line 504. Top-20 brands by volume (`N_BRANDS_ADF = 20`).

Decision rule (lines 526-546):

```python
if   p_raw < 0.05: rec = "raw"
elif p_log < 0.05: rec = "log1p"
else:              rec = "log1p+diff"
```

Output columns: `brand, n, p_raw, p_log, p_diff, recommendation` — there is
literally a `recommendation` column. Written to
`{Category}/pipeline_step_outputs/{cat}_eda_tables/step_2_05_adf_per_brand.csv`
and promoted (md only) to
`05_thesis_results/04_data_assessment/eda/{Category}/tables/`.

**Consumers: none.** An exhaustive repo-wide grep (including `worktrees/`,
excluding `.venv/`) returns exactly five files touching ADF: the producer, an
unrelated aggregate-level test (`step_3_derive_params.py`), a **diagram label**
(`generate_architecture_diagrams.py:715` → `"adf_per_brand": "unit-root tests"`),
and two superseded archive copies. The two archives are *also producers* — so the
per-brand ADF has been recomputed across three generations of the pipeline
without a consumer ever being written. It is a long-standing reporting artefact,
not half-finished wiring.

## F2 — The recommendations are heterogeneous in every category

Parsed from the four `step_2_05_adf_per_brand.md` artefacts:

| Category | raw | log1p | log1p+diff | n |
|----------|-----|-------|------------|---|
| CSD | 4 | 4 | 12 | 20 |
| Danskvand | 7 | 3 | 10 | 20 |
| Energidrikke | 8 | 3 | 9 | 20 |
| RTD | 8 | 3 | 8 | 19 |
| **All** | **27** | **13** | **39** | **79** |

No category has a clean majority. The blanket `d=1` matches the plurality
(39/79) but **over-differences the 27 `raw` brands** — the ones the test says are
already stationary.

## F3 — What is actually applied

| Layer | Behaviour | Driven by |
|-------|-----------|-----------|
| Target | `log1p` on every brand | `pipeline_config.py:82` `LOG_TRANSFORM_TARGET = True`, hardcoded |
| Feature matrix | **no differenced columns at all** (54 cols, one `log_sales_units`) | `engineer_features.py:619-620`, unconditional |
| ARIMA | `SARIMAX(order=(1,1,1))` — fixed `d=1` for every brand | `srq1_baselines_stat.py:283`, hardcoded; `auto_arima` never called |
| Ridge features | `log1p` on a **hardcoded** volume-column tuple | `srq1_benchmark.py:230`; gated by model family, not distribution |

Trend is absorbed by the lag/rolling block (`lag_1..lag_13`, `rolling_mean_4/13`,
`rolling_std_4`) rather than by differencing — which is exactly the fallback the
EDA's own note anticipates (`step_2_eda_descriptive.py:565-567`).

## F4 — Skewness: the diagnostic computes the answer, then discards it

`step_3_derive_params.py:263-294`, `derive_log_transform()`:

```python
supported = abs(skew_log) < abs(skew_raw)
verdict   = "supports" if supported else "does NOT support"
...
return LOG_TRANSFORM_TARGET, provenance   # <- the config constant, not `supported`
```

`supported` is interpolated into a **provenance string** and nothing else. Had a
category's data said "does NOT support", the contract would still be written with
the transform on.

Three related dead ends:

- `step_2_eda_descriptive.py:302-311` — the `if skewness > 2:` chain assigns an
  **interpretation string** ("log transform necessary"), not a transform.
- `ctx.derived["log_transform_supported"]` is written once (`:594`) and **never
  read**. A dead key.
- `step_4_engineer_features.py:350-354` checks the contract flag, but since the
  value is always `True` and the column is always created, the branch can never
  meaningfully fire.

The measured numbers do vindicate the choice: CSD skew **5.00 → 0.03** under
`log1p`. The evidence is real; it just is not what selected the transform.

## F5 — The Ch4 prose implies an evidentiary link that does not exist

Measured against snapshot `2026-09-07_19-41_internal-links`.

**Ch4 is already partly candid** — it says these parameters are *"EDA-driven
rather than theory-first"* and that their *"empirical (not theoretical) origin is
stated honestly as a limitation."* That framing is correct and should be kept.

Two specific claims overstate:

1. **Table 2, log-transform row** (ch4 line 110) gives the basis as
   *"variance stabilisation; series is I(1), diff-stationary (ADF p<0.001)"*,
   status **confirmed**. But three of four categories are non-stationary at
   aggregate level and **RTD is stationary (p = 0.000)**. The transform was
   applied by config; the test corroborated it afterwards.

2. **§4.2.2 treatment sentence** (ch4 line 80): *"non-stationarity in the mean is
   handled by **differencing** for ARIMA"* — mechanically true (`d=1`), but reads
   as though the data selected it, and it is **wrong for RTD**, the one category
   whose ADF says no differencing is needed. Table 3 (line ~120) shows RTD
   `p = 0.000, stationary in level`, contradicting the blanket claim two sections
   earlier.

**Recommended framing** (costs nothing, and is a stronger claim):
the per-brand ADF and per-feature skewness **motivate two global design choices**
— universal `log1p`, and lag features in place of explicit differencing — and
ARIMA's `d=1` is a **fixed specification**, not an ADF-selected one. Uniform
treatment is defensible on the low-power argument; retrospective selection is not.

## F6 — A code comment states the opposite of the truth

`_shared_modules/pipeline_config.py:218`:

> *"the .csv step outputs STAY here -- later EDA steps consume them (structural
> breaks, ADF-per-brand feed data-handling decisions)."*

**Nothing reads `step_2_05_adf_per_brand.csv`.** The structural-break half may be
true and was not checked. One-line fix; independent of everything else.

## F7 — The recommendation column has an internal defect

`p_diff` is computed but **never used in the decision rule** — `log1p+diff` is the
else-branch fallback, assigned regardless of whether differencing actually
achieved stationarity. Example from the CSD artefact: `TUBORG SQUASH` has
`p_diff = 0.471` (differencing plainly failed) and is still labelled
`log1p+diff`. The rule can also never emit `"none"` or `"diff"`.

If the table is cited in the thesis, this matters: the column is less informative
than its name suggests.
