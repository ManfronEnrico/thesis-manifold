# Step 3 — Workstream B: feature engineering integration

**Goal**: replace `DataAssessmentAgent._engineer_features()` stub
(`raise NotImplementedError`) with a proper sklearn-style pipeline.

## Audit of existing `engineer_features()` (in `preprocessing.py`)

| Feature | Source | Leakage-safe? |
|---|---|---|
| `lag_{1,2,3,4,8,13}` | target `shift(n)` per brand | ✅ — only past |
| `rolling_mean_{4,13}`, `rolling_std_4` | `shift(1).rolling(w).{mean,std}` | ✅ — `shift(1)` prevents look-ahead |
| `month`, `quarter`, `holiday_month` | from `date` column | ✅ — deterministic |
| `promo_intensity` | `promo_units / sales_units` | ✅ — row-level ratio |
| `log_sales_units` | `log1p(sales_units)` | ✅ — deterministic |

**Audit conclusion**: existing function is **leakage-safe by construction**.
No fittable state (no scalers, no encoders), so applying it to the full
frame before train/val/test split does not leak future info into past.

The sklearn-style class wrapper is built nonetheless to host future
extensions (categorical encoders, scalers) under a clean `fit(train) →
transform(full)` API.

## Module created

`thesis/thesis_agents/ai_research_framework/features/engineer_features.py`

Public API:
- Pure functions: `make_calendar`, `filter_series`, `engineer_features`,
  `apply_split`, `build_series_index`
- Data sourcing: `aggregate_brand_month_from_csvs(csv_dir)` (CSD only —
  see Step 4 for why) and `aggregate_brand_month_from_db(category, conn)`
  (all 5 categories, schema-tolerant)
- Class wrapper: `FeatureEngineer.fit/transform/fit_transform`
- Persistence: `save_feature_matrix(df, output_dir)`
- Pooling: `build_pooled_feature_matrix(matrices_by_category)`

## Bug found and fixed in v1 of the wrapper

First version of `FeatureEngineer.fit()` filtered brands using the train
portion only — which was 29 months, smaller than the `min_periods=30`
threshold — so **zero brands passed and the output was empty**.

**Fix**: the series filter is a *data quality gate*, not a learned
transformation. Apply on the full frame, not just train. `fit()` is now a
true no-op (consistent with sklearn convention for transformers with no
fittable parameters).

## Wiring into DataAssessmentAgent

Replaced both stubs in `data_assessment_agent.py`:
- `_engineer_features()` — calls `aggregate_brand_month_from_csvs` +
  `FeatureEngineer().fit_transform()` + `save_feature_matrix()`. Returns
  paths (not DataFrames — see next finding).
- `_format_report()` — produces a markdown summary of the Nielsen + Indeks
  reports (was also a stub).

## Discovery — LangGraph cannot serialize DataFrames

The first end-to-end test crashed with:
```
TypeError: Type is not msgpack serializable: DataFrame
```

LangGraph's checkpointer serializes state via msgpack, which doesn't know
how to handle `pd.DataFrame`. The agent was returning `feature_matrix=df`
directly into state.

**Fix (architectural)**:
- Added `feature_matrix_path: Optional[str]` and `series_index_path:
  Optional[str]` to `ResearchState`.
- Agent persists parquet to `results/phase1/` and propagates the path string
  through state.
- DataFrames in state are kept as `None` (or removed in future).
- Downstream agents (ForecastingAgent) read parquet from the path.

This is also better for memory: large feature matrices don't bloat the
checkpoint.

## Refactor — preprocessing.py imports from new module (deduplication)

The original `preprocessing.py` had inline definitions of `make_calendar`,
`filter_series`, `engineer_features`, `apply_split`, `build_series_index`.
Refactored to `from thesis.thesis_agents.ai_research_framework.features.engineer_features
import (...)` — single source of truth.

Verified: `python preprocessing.py` (CLI batch) still produces the same
77-brand output.

## Verification (success)

```
TEST 1 — preprocessing.py CLI:
   77 brands × 42 months → results/phase1/feature_matrix.parquet ✓

TEST 2 — test_langgraph_pipeline.py:
   [OK] LangGraph built
   [OK] Graph execution completed
        Final phase: feature_engineering   ← was stuck at data_assessment
        Errors: 0                          ← was NotImplementedError
   [OK] Data quality report generated
```

All Brian-stated acceptance criteria met:
- ✅ Pipeline advances past `data_assessment` without error
- ✅ Feature matrix at `results/phase1/feature_matrix.parquet`
- ✅ Sanity: no NaN in numeric cols (except expected lag/rolling at series
     start)
- ✅ No scaler fit on val/test (no scalers exist yet)

Design document delivered at `docs/dev/feature_engineering_design.md`.
