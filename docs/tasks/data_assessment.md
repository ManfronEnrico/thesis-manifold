# Data Assessment Plan
> Phase 1 — Data Assessment Agent
> Last updated: 2026-03-14
> Status: PARTIALLY BLOCKED (Nielsen access pending; Indeks Danmark CSVs not yet local)

---

## What this phase produces

**Output**: `docs/data/nielsen_assessment.md` (extended) + `docs/data/indeksdanmark_notes.md` (extended)
**Definition of Done**: Written report covering data quality, missing values, forecasting suitability, feature engineering plan, and recommendation on additional data needs

---

## Part 1 — Nielsen / Prometheus

### Status: BLOCKED — data access not yet obtained

### When access is confirmed, run these checks:

**Quality checks**
- [ ] Row count per table (facts, markets, products, periods)
- [ ] Date range: earliest and latest `period_id` — confirm ~36 months
- [ ] Missing periods: any gaps in monthly sequence?
- [ ] Null/zero value analysis: % of facts rows where `sales_value = 0`
- [ ] Product count: total distinct `product_id` values
- [ ] Distribution check: revenue concentration (top 10 brands = what % of total sales?)

**Forecasting suitability**
- [ ] Minimum series length check: are there products with <24 months of data? (ARIMA minimum)
- [ ] Seasonality test: visual inspection of CSD sales pattern (expected: summer peak)
- [ ] Promotional signal: % of sales under `sales_value_any_promo` vs total
- [ ] Intermittent demand: % of series with >20% zero-value periods (affects model choice)

**Feature engineering plan**
- [ ] Lag features: sales_value t-1, t-2, t-3, t-12
- [ ] Rolling features: 3-month and 6-month moving average
- [ ] Promotional ratio: `sales_value_any_promo / sales_value`
- [ ] Distribution trend: `weighted_distribution` delta month-over-month
- [ ] Market share: brand sales / total category sales per retailer per period
- [ ] Indeks Danmark enrichment: consumer segment affinity per retailer (see Part 2)

**Default query scope**
- Market: `DVH EXCL. HD` as primary; all 28 markets for full benchmark
- Product: `corporation_ru_1` filter for Royal Unibrew brands (primary client)
- Period: all available (max 36 months)

---

## Part 2 — Indeks Danmark

### Status: BLOCKED — CSVs must be downloaded from Google Drive locally

### Files needed (currently .webloc shortcuts)
- `indeksdanmark_data.csv` (20,134 × 6,364)
- `official_codebook.csv` (6,364 × 11, includes survey weights)
- `indeksdanmark.metadata.csv` (29,185 × 3, value labels)

### When CSVs are local, run these checks:

**Quality checks**
- [ ] Confirm row count (expected: 20,134 respondents)
- [ ] Column count and all-float64 data type verification
- [ ] Missing value analysis: % null per variable
- [ ] Survey weight distribution: inspect `weight` column from codebook

**Feature selection plan (for SRQ3)**
- [ ] Identify beverage/CSD-relevant variables (search codebook for: drink, beverage, cola, soft drink, grocery, supermarket)
- [ ] Identify retailer preference variables (search for: Netto, Bilka, Rema, Meny, etc.)
- [ ] Identify demographic variables (age, gender, income, region)
- [ ] Identify behavioral variables (shopping frequency, brand loyalty proxies)
- [ ] Reduce to ~50–100 most relevant variables (dimensionality reduction for 8GB budget)

**Consumer segmentation plan (SRQ3 feature enrichment)**
- [ ] Apply PCA on selected variables to reduce dimensions
- [ ] K-means clustering to build 4–6 consumer segments
- [ ] Profile each segment (demographic + behavioral centroid)
- [ ] Map segments to retailer affinity (which segment shops where?)
- [ ] Output: segment-level demand signal per retailer → feed to Synthesis Agent

---

## Part 3 — Additional Data Considerations

| Source | Type | Purpose | Priority |
|---|---|---|---|
| Macroeconomic data (Statistics Denmark) | Public | External demand signal (CPI, consumer confidence) | Low — nice to have |
| Weather data | Public | Seasonality signal for CSD (temperature → consumption) | Low |
| Competitor price data | Proprietary | Promotional response modelling | Out of scope (no access) |

---

## Data Security Checklist

- [ ] Nielsen data stays local — no external uploads
- [ ] Indeks Danmark stays local — survey personal data
- [ ] Confirm with Manifold AI: confidentiality agreement needed before Nielsen access?
- [ ] All data paths in code use local file paths only
