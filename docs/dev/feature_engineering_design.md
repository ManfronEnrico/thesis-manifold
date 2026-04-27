# Feature Engineering Design — System A

**Created**: 2026-04-23 (Workstream B of `2026-04-23_system-a-feature-eng-integration.md`)
**Module**: `thesis/thesis_agents/ai_research_framework/features/engineer_features.py`
**Consumers**: `DataAssessmentAgent` (LangGraph), `thesis/data/preprocessing/combined_scripts/preprocessing.py` (CLI)

## Purpose

Single source of truth for converting Nielsen CSD brand-level monthly sales into a
model-ready feature matrix. Previously split across `preprocessing.py` and a stubbed
`DataAssessmentAgent._engineer_features()`; now unified in one leakage-safe module
reused by both call sites.

## Pipeline contract

```
CSV dir (facts + 3 dim) ──▶ aggregate_brand_month_from_csvs() ──▶ brand × month frame
                                                                       │
                                                                       ▼
                                            FeatureEngineer.fit_transform()
                                                                       │
                                                                       ▼
                                  make_calendar → filter_series → engineer_features → apply_split
                                                                       │
                                                                       ▼
                                              save_feature_matrix() → thesis/analysis/outputs/phase1/*.parquet
```

Output contract (unchanged from `preprocessing.py`): `thesis/analysis/outputs/phase1/feature_matrix.parquet`
with columns `brand, date, split, sales_units, log_sales_units, lag_{1,2,3,4,8,13},
rolling_mean_{4,13}, rolling_std_4, month, quarter, holiday_month, promo_intensity,
sales_value, sales_liters, promo_units, weighted_dist`.

## Feature list and rationale

| Feature | Source | Domain rationale | Leakage-safe? |
|---|---|---|---|
| `lag_{1,2,3,4,8,13}` | target shift per brand | seasonality at 3-month, quarterly, annual | ✅ — shift only uses past |
| `rolling_mean_{4,13}` | shift(1).rolling(w).mean() | short- and long-trend baseline | ✅ — shift(1) prevents t leaking into t |
| `rolling_std_4` | shift(1).rolling(4).std() | short-term volatility | ✅ — same |
| `month`, `quarter` | date | seasonality | ✅ — deterministic |
| `holiday_month` | date ∈ {1,4,6,10,12} | Danish public-holiday months (Jan, Apr, Jun, Oct, Dec) | ✅ — deterministic |
| `promo_intensity` | promo_units / sales_units | share of volume sold on promo | ✅ — deterministic ratio |
| `log_sales_units` | log1p(sales_units) | heteroskedasticity fix for tree models / ridge | ✅ — deterministic |

## Leakage analysis (per Brian's concern in plan §Workstream B risk)

**Finding**: the existing `engineer_features()` in `preprocessing.py` is **leakage-safe
by construction**. No fittable state (no scalers, no encoders, no target encoding).
Every transformation is either deterministic on the row (calendar, ratios, log) or
uses only the past within each brand group (lags via `shift(n)`, rolling via
`shift(1).rolling()`).

Therefore:
- Applying `engineer_features()` to the full frame **before** train/val/test split is
  safe.
- `FeatureEngineer.fit()` is currently a no-op.

**Design forward-looking choice**: the sklearn-style class shape exists so future
additions (OneHot/Ordinal encoding of brand, target encoding, StandardScaler for
non-tree models) can be added with the correct `fit(train) → transform(full)` pattern
without refactoring the agent wiring. See "Gaps not yet filled" below.

## Series filter

Brands with `< MIN_PERIODS = 30` non-zero observations in the full 42-month history
are dropped. This is a data-quality gate, not a learned transformation, so it runs
unconditionally on the full frame (not just training).

Result: 77 brands kept from 136 original (same as `preprocessing.py` baseline).

## Split boundaries (locked)

Fixed per `preprocessing.py` contract — do not drift without explicit methodological
review:

- Train: up to and including **Feb 2025** (~29 months)
- Val: Mar 2025 – **Aug 2025** (6 months)
- Test: Sep 2025 – Mar 2026 (7 months)

Locked via `DEFAULT_TRAIN_END = (2025, 2)` and `DEFAULT_VAL_END = (2025, 8)` constants
in the module.

## State-serialization constraint (LangGraph)

Discovered during Workstream B integration: LangGraph's `msgpack` checkpointer
cannot serialize `pd.DataFrame`. Accordingly:

- `DataAssessmentAgent.run()` returns **paths** (strings) in state, not DataFrames.
- `feature_matrix`, `nielsen_data`, `indeks_data` fields in `ResearchState` are kept
  as `None` at runtime; downstream agents load parquet from `feature_matrix_path`.
- Added new state fields `feature_matrix_path: Optional[str]` and
  `series_index_path: Optional[str]`.

## Gaps intentionally NOT filled (future work)

From Brian's plan gap-analysis table, these were left out with reason:

| Gap | Left out because | When to revisit |
|---|---|---|
| Categorical encoding (brand/market) | Tree models (LightGBM) consume `brand` as categorical natively; no need for OneHot | If ridge/MLP added to forecasting benchmark |
| StandardScaler | Same reason — tree models don't need it | Same |
| Polynomial / interaction features | No theoretical basis in demand-forecasting literature for this dataset — avoid adding noise | If domain review surfaces justified interactions |
| Missing-value imputation | Lags at series start are legitimately NaN (no history); tree models handle NaN natively | Only if non-tree model added |
| Time-series-specific transformers (seasonal decomposition, Fourier, wavelet, PAA via `aeon`) | Marginal benefit for 42-month series with explicit seasonal lags (8, 13) | If SRQ1 benchmark shows seasonal models underperform |
| Stationarity checks (ADF, KPSS) | Required only for ARIMA-family models; out of scope for tree-based models planned in SRQ1 | When (if) ARIMA is added to the benchmark |

## Extension path (Fase 2, multi-category)

For the 5-category redesign (CSD + danskvand + energidrikke + rtd + totalbeer), the
module extension will be:

1. Parameterize `aggregate_brand_month_from_csvs()` on category (or provide per-category
   overrides for differing schemas — e.g. 4 new categories have `baseline_sales_*`
   that CSD lacks).
2. Add `category` column to the output (required for pooled models).
3. Schema harmonization: union of columns, NaN for CSD where baseline/advanced metrics
   don't exist (LightGBM handles NaN natively).

This is deferred to Fase 2 of the thesis redesign plan (see
`.claude/plans/plan_files/seven_models_pipeline_redesign.md`) so Workstream B ships
with single-category (CSD) integration first.
