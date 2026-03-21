# Nielsen / Prometheus Data Assessment
> Source: Thesis/prometheus_data_model-1.md
> Last updated: 2026-03-14

---

## Database Overview

- **Database**: `Nielsen_clean`  **Schema**: `dbo`
- **Structure**: Star schema — 3 dimension tables + 1 fact table
- **Domain**: Carbonated Soft Drinks (CSD), Danish retail
- **Coverage**: 28 Danish retailers/market segments
- **History**: ~3 years monthly (~36 periods)
- **Access modality**: 🔴 NOT YET OBTAINED — data access must be requested from Manifold AI

---

## Tables

| Table | Type | Description |
|---|---|---|
| `csd_clean_dim_market_v` | Dimension | Market/retailer (28 entries) |
| `csd_clean_dim_period_v` | Dimension | Time period (monthly) |
| `csd_clean_dim_product_v` | Dimension | Product catalogue |
| `csd_clean_facts_v` | Fact | Sales metrics |

---

## Key Columns

**Market**: `market_id`, `market_description`
Default analysis market: `DVH EXCL. HD` (Dagligvarehandel excl. hard discount)

**Period**: `period_id`, `period_year`, `period_month`, `date_key`

**Product**: `product_id`, `category` (always CSD), `manufacturer`, `brand`, `ru_subbrand`, `ru_variant`, `packaging`, `size_variants`, `type`, `regular_light`, `price_category`, `organic`, `private_label`, `corporation_ru_1` (key: identifies Royal Unibrew vs competitors)

**Facts**: `sales_value` (DKK), `sales_in_liters`, `sales_units`, `sales_value_any_promo`, `sales_in_liters_any_promo`, `sales_units_any_promo`, `weighted_distribution`

---

## Forecasting Suitability (preliminary)

- Monthly time series: product × market × period → suits ARIMA/Prophet/LightGBM
- ~36 periods: borderline for ARIMA (needs ≥24); adequate for tree-based models
- Promo variants provide feature engineering opportunities
- `weighted_distribution` useful as a coverage/availability feature
- 28 markets × N products × 36 periods → dimensionality relevant to 8GB constraint

---

## Open Items

- [ ] Access modality confirmed (SQL vs CSV)?
- [ ] Actual row count of facts table
- [ ] Latest period available (data freshness)
- [ ] Product count (total grain size estimate)
- [ ] Any known missing periods or data gaps?
