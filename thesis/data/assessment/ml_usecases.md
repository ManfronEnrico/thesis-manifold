# ML / Predictive Analytics Use Cases
> Brainstorm — based on Nielsen CSD + Indeks Danmark data models
> Status: ideas only — not yet approved for implementation

---

## What we're working with

### Nielsen / Prometheus CSD (SQL — now accessible)
Star schema, monthly granularity, **Carbonated Soft Drinks only**, 28 Danish retailers, ~36 months.

| Table | Key columns |
|---|---|
| `csd_clean_facts_v` | `sales_value`, `sales_units`, `sales_in_liters`, `sales_value_any_promo`, `sales_in_liters_any_promo`, `sales_units_any_promo`, `weighted_distribution` |
| `csd_clean_dim_product_v` | `brand`, `manufacturer`, `corporation_ru_1`, `type`, `regular_light`, `price_category`, `private_label`, `organic`, `packaging`, `size_variants` |
| `csd_clean_dim_market_v` | `market_description` (28 retailers: NETTO, REMA 1000, MENY, BILKA, etc.) |
| `csd_clean_dim_period_v` | `period_year`, `period_month`, `date_key` |

**Key flag**: `corporation_ru_1` identifies Royal Unibrew vs. Carlsberg vs. Coca-Cola A/S vs. others.
**Default market**: `DVH EXCL. HD` (total Danish grocery trade, excluding hard discount).

### Indeks Danmark (CSV — download still pending)
20,134 Danish consumers × 6,364 survey variables. Demographics, attitudes, behaviours, preferences.
Includes codebook with survey weights + value label mappings.

---

## Use Cases by Sub-Research Question

### SRQ1 — Forecasting benchmark (core deliverable)

**Monthly sales forecasting**
- **Target**: `sales_value`, `sales_units`, `sales_in_liters`
- **Granularity**: brand × retailer × month (aggregate from SKU level to ensure enough time series observations)
- **Models**: AutoARIMA · Prophet · LightGBM · XGBoost · Ridge (sequential, memory-profiled)
- **Evaluation**: MAPE, RMSE, MASE + prediction interval calibration coverage

**Feature engineering from Nielsen alone:**

| Feature | Derivation |
|---|---|
| Lag features | t-1, t-2, t-3, t-12 (captures seasonality) |
| Rolling statistics | 3m / 6m / 12m rolling mean + std |
| Calendar | month-of-year, Danish holiday flags (Christmas, Easter, summer) |
| Promotional rate | `sales_value_any_promo / sales_value` → % of sales on promotion |
| Distribution signal | `weighted_distribution` as leading shelf-availability indicator |
| Product attributes | `price_category`, `private_label`, `regular_light` as categorical features for tree models |

---

### SRQ2 — Multi-agent synthesis inputs

**Promotional uplift modelling**
- Derive per product-retailer: `(promo_sales − baseline_sales) / baseline_sales`
- Identifies which SKUs and retailers respond most to promotions
- SynthesisAgent uses this to qualify forecast-based recommendations

**Distribution risk flag**
- `weighted_distribution` declining → supply-side risk, not a demand problem
- Prevents SynthesisAgent from recommending "reduce production" when actually a distribution issue

**Competitive market share**
- Royal Unibrew share = RU `sales_value` / total category `sales_value` per retailer per month
- Derived from `corporation_ru_1` grouping
- SynthesisAgent combines absolute forecast + relative market share trajectory

---

### SRQ3 — Consumer signal enrichment (the differentiator)

**PCA + k-means on Indeks Danmark → consumer demand indices**

Steps:
1. Filter 6,364 variables to beverage/grocery/health-relevant subset using codebook labels
2. PCA → extract 5–10 interpretable indices (e.g. health-consciousness, price sensitivity, brand loyalty, sustainability orientation)
3. k-means → 4–6 consumer segments, population-weighted using codebook weights
4. Feed indices as additional features into LightGBM/XGBoost forecasting models
5. **Diebold-Mariano test** (already in `statsmodels`) → formally test whether consumer signals improve forecast accuracy

**Core thesis hypothesis for SRQ3:**
> Health-consciousness / anti-sugar attitudes in Indeks Danmark predict the REGULAR → LIGHT CSD shift *before it fully materialises in Nielsen sales numbers.* Consumer sentiment as a leading indicator of structural demand change.

---

### SRQ4 — Comparison vs. descriptive analytics baseline

What Manifold's current BI system does: YoY comparisons, 3-month rolling averages, market share tables.

| Baseline | Method |
|---|---|
| Naïve seasonal | Same month, previous year |
| BI baseline | 3-month rolling mean |
| AI system (ours) | Best model from SRQ1 benchmark |

Evaluation: MAPE + directional accuracy (did the forecast correctly predict up/down?).

---

## Secondary use cases (relevant but not core SRQ deliverables)

**Private label vs. branded competition**
- `private_label` flag: are branded CSD losing share to private label at discount retailers (NETTO, REMA 1000) vs. full-service (MENY, BILKA)?

**Retailer segmentation**
- Cluster 28 retailers by CSD sales patterns (volume, promo intensity, distribution levels)
- Feeds thesis narrative on channel strategy

**Organic CSD trend**
- `organic` flag: small but growing segment in Denmark
- May warrant a separate forecast given structurally different growth curve

---

## Implementation priority order

1. Run `scripts/explore_nielsen.py` → confirm actual table structure and row counts
2. **Sales forecasting pipeline** (SRQ1) — core, can start now with Nielsen access
3. **Promotional uplift + distribution risk flags** (SRQ2) — derived from Nielsen, low effort
4. **Competitive market share** (SRQ2) — aggregation from `corporation_ru_1`
5. **Indeks Danmark PCA/segmentation** (SRQ3) — needs CSV download first, RAM-intensive
6. **Descriptive baseline** (SRQ4) — simple, implement last as comparison

---

## Open questions (to decide before Phase 4 implementation)

1. **Scope**: Forecast Royal Unibrew portfolio only, or full CSD category?
2. **Horizon**: 1-month-ahead, 3-month, or 6-month forecasts?
3. **Indeks Danmark**: CSVs downloaded locally yet?
