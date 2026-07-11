# Nielsen / Prometheus Data Assessment
> Source: Thesis/prometheus_data_model-1.md + live query results 2026-04-12
> Last updated: 2026-04-12 — CONNECTION CONFIRMED; full assessment complete

---

## Database Overview

- **Database**: `Nielsen_clean`  **Schema**: `dbo`
- **Structure**: Star schema — 3 dimension tables + 1 fact table
- **Domain**: Carbonated Soft Drinks (CSD), Danish retail
- **Coverage**: 28 Danish retailers/market segments
- **History**: 42 monthly periods (Oct 2022 – Mar 2026 = 3.5 years)
- **Access modality**: ✅ CONFIRMED — Microsoft Fabric SQL connector (Service Principal auth)
- **Connector file**: `ai_research_framework/data/nielsen_connector.py`

---

## Tables

| Table | Rows | Description |
|---|---|---|
| `csd_clean_dim_market_v` | 28 | Market/retailer dimension |
| `csd_clean_dim_period_v` | 42 | Time period dimension (monthly) |
| `csd_clean_dim_product_v` | 2,057 | Product/SKU catalogue |
| `csd_clean_facts_v` | 2,535,464 | Sales metrics (grain: market × period × product) |

---

## Dimension: Market (28 rows)

| market_id | market_description |
|---|---|
| 1256338 | DVH EXCL. HD ← **primary analysis market** |
| 1262112 | DVH EXCL. DISCOUNT/HD |
| 1262102 | DVH/CONVENIENCE INCL. HD |
| 1262119 | DVH/CONVENIENCE EXCL. HD |
| 1262159 | DAGROFA |
| 1256452 | MENY |
| 1262129 | COOP |
| 1256459 | SPAR |
| 1256466 | MIN KØBMAND |
| 1256408 | SUPERBRUGSEN |
| 1262120 | SALLING GROUP |
| 1256401 | KVICKLY |
| 1262193 | TOTAL DISCOUNT |
| 1256441 | BRUGSEN |
| 1262395 | CONVENIENCE |
| 1256339 | FØTEX |
| 1262111 | GASOLINE/7-ELEVEN |
| 1256394 | BILKA |
| 1256365 | NETTO |
| 1260001 | OK PLUS |
| 1452407 | NEMLIG.COM |
| 1259985 | BFI SHELL |
| 1256426 | REMA 1000 |
| 1259982 | BFI EXTRA |
| 1259964 | 7-ELEVEN |
| 1259965 | CIRCLE K |
| 1259957 | Q8 |
| 1256423 | ALDI |

**NULL counts**: 0 in all columns

---

## Dimension: Period (42 rows)

| Year | Months | Count |
|---|---|---|
| 2022 | Oct, Nov, Dec | 3 |
| 2023 | Jan–Dec | 12 |
| 2024 | Jan–Dec | 12 |
| 2025 | Jan–Dec | 12 |
| 2026 | Jan, Feb, Mar | 3 |

**Date range**: "April 2023" (earliest) to "September 2025" (latest) per date_key field — the field stores a label string, not a date type  
**Note**: period_ids are NOT monotonically sequential with calendar time — sort by (period_year, period_month) for chronological ordering  
**NULL counts**: 0 in all columns

---

## Dimension: Product (2,057 rows)

**NULL counts**: 0 in all 18 columns — fully populated dimension

| Column | Distinct values |
|---|---|
| brand | 144 |
| manufacturer | 114 |
| packaging | 4 (PLAST, DÅSE, GLAS, ANDET EMBALLAGE) |
| type | 8 (COLA, APPELSIN, TONIC, CITRUS/GRAPE, LEMON/LIME, GINGER BEER, EKSOTISK, ØVRIG SMAG) |
| regular_light | 2 (REGULAR, LIGHT) |
| price_category | 2 (MÆRKEVARE, BILLIGVAND) |
| organic | 2 (IKKE ØKOLOGISK, ØKOLOGISK) |
| private_label | 2 (NON PRIVATE LABEL, PRIVATE LABEL) |
| corporation_ru_1 | 7 (CARLSBERG, ROYAL UNIBREW, HARBOE, PRIVATE LABEL EKSKL. CL, VESTFYN, ANDRE LEVERANDØRER, AQUA D'OR) |

**Top brands by SKU count**: COCA COLA (236), PEPSI (147), FAXE KONDI (143), FANTA (140), HARBOE (137)

**⚠️ Product dimension mismatch**: 8,522 distinct product_ids in facts vs 2,057 in dim_product.  
Interpretation: dim_product is filtered to the Manifold analysis scope; facts table contains full historical transaction product_ids including discontinued/out-of-scope SKUs. Join to dim_product effectively scopes to the active catalogue.

---

## Fact Table (2,535,464 rows)

**Grain**: market_id × period_id × product_id

**Columns**: market_id, period_id, product_id, sales_value, sales_in_liters, sales_units, sales_value_any_promo, sales_in_liters_any_promo, sales_units_any_promo, weighted_distribution

### NULL counts

| Column | Nulls | % |
|---|---|---|
| market_id | 0 | 0.00% |
| period_id | 0 | 0.00% |
| product_id | 0 | 0.00% |
| sales_value | 0 | 0.00% |
| sales_in_liters | 0 | 0.00% |
| sales_units | 0 | 0.00% |
| sales_value_any_promo | 1,001,078 | 39.48% |
| sales_in_liters_any_promo | 1,001,078 | 39.48% |
| sales_units_any_promo | 1,001,078 | 39.48% |
| weighted_distribution | 391,035 | 15.42% |

**Interpretation**: Promo NULLs = no promotion in that period/market/product (not missing data). weighted_distribution NULLs = product not tracked for distribution in that combination.

### Descriptive statistics

| Metric | Min | Max | Mean | Std |
|---|---|---|---|---|
| sales_value (DKK) | -20,431 | 522,043,917 | 1,037,479 | 12,391,642 |
| sales_in_liters | -4,293 | 53,103,073 | 97,532 | 1,203,720 |
| sales_units | -900 | 34,531,818 | 66,495 | 822,234 |
| sales_value_any_promo | -31,927 | 308,302,434 | 541,495 | 6,146,178 |
| sales_in_liters_any_promo | -21,722 | 39,164,036 | 57,012 | 664,081 |
| sales_units_any_promo | -14,481 | 21,825,529 | 29,353 | 351,840 |
| weighted_distribution | 0.00 | 1.00 | 0.26 | 0.35 |

**Negative values**: Returns and corrections. Require pre-processing (clip to 0 or exclude).  
**High std relative to mean**: Heavy right-skew from aggregate markets (DVH composite rows are very large; individual retailer rows are small). Log transformation likely needed.

### Zero-sales and promotional rows

- Zero-sales rows (sales_units = 0): 52,919 (2.09%) — low; distinguishable from genuine gaps
- Promotional rows (any_promo > 0): 890,269 (35.11%) — substantial promotion activity

### Coverage by market (top 10 by row count)

| Market | Rows |
|---|---|
| DVH/CONVENIENCE INCL. HD | 213,327 |
| DVH/CONVENIENCE EXCL. HD | 204,286 |
| DVH EXCL. HD | 187,907 |
| DVH EXCL. DISCOUNT/HD | 179,229 |
| DAGROFA | 154,378 |
| MENY | 142,239 |
| COOP | 124,128 |
| SPAR | 122,616 |
| MIN KØBMAND | 111,800 |
| SUPERBRUGSEN | 111,215 |

### Time-series completeness (brand × market series)

- 779 brand × market series have all 42 periods (fully observed)
- Remaining series have shorter coverage (intermittent/niche products)

### All top brands in DVH EXCL. HD: full 42-period coverage

| Brand | Periods | Total units |
|---|---|---|
| HARBOE | 42 | 208M |
| COCA COLA | 42 | 199M |
| PEPSI | 42 | 171M |
| FAXE KONDI | 42 | 128M |
| FANTA | 42 | 34M |
| JOLLY | 42 | 19M |
| TUBORG SQUASH | 42 | 17M |

---

## Proposed Train / Validation / Test Split

Based on chronological ordering (sort by period_year, period_month):

| Split | Periods | Calendar range | % |
|---|---|---|---|
| Training | 29 | Oct 2022 – Feb 2025 | 69% |
| Validation | 6 | Mar 2025 – Aug 2025 | 14% |
| Test | 7 | Sep 2025 – Mar 2026 | 17% |

**Rationale**: Strict temporal split (no shuffling). 29 training periods satisfies ARIMA minimum of 24 periods; provides 2+ full seasonal cycles. 6-month validation enables hyperparameter optimisation. 7-month test set covers the most recent data, including potential trend shifts from 2025 consumer behaviour changes.

---

## Data Quality Summary

| Issue | Severity | Action |
|---|---|---|
| Promo NULLs (39.48%) | 🟡 Expected | Treat as 0 (no promo) — not missing data |
| weighted_distribution NULLs (15.42%) | 🟡 Moderate | Impute with median by market×brand or exclude from features |
| Negative sales values | 🟡 Low count | Clip to 0 before modelling |
| Product dimension mismatch (8,522 vs 2,057) | 🟢 Understood | Join to dim_product to scope analysis correctly |
| Zero-sales rows (2.09%) | 🟢 Low | Retain; mark as known zero (not imputed) |
| period_id ordering | 🟢 Known | Always sort by (period_year, period_month) |
| High variance (std >> mean) | 🟡 Expected | Log-transform sales targets for tree-based models |

---

## Forecasting Suitability Verdict

✅ **Data is suitable for all 5 planned models** (ARIMA, Prophet, LightGBM, XGBoost, Ridge Regression)  
✅ 42 periods exceeds ARIMA minimum of 24; covers 3+ seasonal cycles  
✅ Core metrics are complete (0 nulls in sales_value, sales_in_liters, sales_units)  
✅ Top brands in DVH EXCL. HD have full 42-period coverage — no imputation required  
✅ Promotional uplift data available for 35.11% of rows — sufficient for promo feature engineering  
⚠️ Scope modelling to dim_product join to avoid 8,522 vs 2,057 mismatch  
⚠️ Remove or clip negative values before model training  
⚠️ Log-transform sales targets to address right-skew
