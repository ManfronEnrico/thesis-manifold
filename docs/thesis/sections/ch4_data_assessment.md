# Chapter 4 — Data Assessment
> Status: BULLET POINT SKELETON — not prose yet
> Last updated: 2026-03-15
> Blocked items: Nielsen access, Indeks Danmark CSV download

---

## 4.1 Overview and data strategy

- Two datasets underpin the empirical work: Nielsen CSD (primary, quantitative sales panel) and Indeks Danmark (secondary, consumer survey)
- Both datasets complement each other: Nielsen captures the *what* (sales outcomes); Indeks Danmark captures the *who* (consumer demand profiles)
- Analytical goal: engineer a feature matrix combining both datasets that enables the 5 forecasting models to incorporate both historical sales patterns and consumer demand signals
- Cite: docs/data/nielsen_assessment.md; docs/data/indeksdanmark_notes.md

---

## 4.2 Nielsen CSD dataset

### 4.2.1 Data source and access

- Source: Manifold AI / Prometheus reporting platform
- Format: Star-schema SQL database (4 tables) OR CSV export — access modality TBD with Manifold
- ⚠️ **STATUS: NOT YET OBTAINED** — must contact Manifold AI to confirm access and sign confidentiality agreement (CBS requirement)
- Cite: docs/data/nielsen_assessment.md; Prometheus data model (Thesis/prometheus_data_model-1.md)

### 4.2.2 Schema

| Table | Key columns | Role |
|---|---|---|
| `csd_clean_dim_market_v` | market_id, retailer_name, channel | Retailer dimension |
| `csd_clean_dim_period_v` | period_id, year, week, month | Time dimension |
| `csd_clean_dim_product_v` | product_id, brand, category, SKU | Product dimension |
| `csd_clean_facts_v` | sales_value, sales_in_liters, sales_units, promo_flag, weighted_distribution | Fact table |

### 4.2.3 Coverage

- Scope: Carbonated Soft Drinks (CSD) category, Danish retail market
- Retailers: 28 Danish retailers across all channels (major chains, discounters, convenience)
- Time: ~36 monthly periods (~3 years) — minimum required for meaningful seasonal modelling
- Granularity: product × retailer × week (assumed — to be confirmed)

### 4.2.4 Data quality checks (plan)

- Missing value analysis: % missing per column per retailer × period
- Zero-sales weeks: distinguish true zero sales from missing data (critical for ARIMA)
- Distribution checks: outlier detection on sales_value, sales_units (promotional spikes)
- Temporal coverage: confirm all 36 periods present for all retailer × SKU combinations; flag gaps
- Forecasting suitability: minimum 2 full years required; verify data volume supports train/validation/test split

### 4.2.5 Target metrics for modelling

- Primary: `sales_units` (unit volume — most directly actionable for category managers)
- Secondary: `sales_value` (revenue), `sales_in_liters` (volume)
- Exclude from targets: `weighted_distribution` (use as a feature, not a target)

---

## 4.3 Indeks Danmark consumer survey

### 4.3.1 Data source and access

- Source: Indeks Danmark annual consumer survey (Danish market research)
- Format: 3 CSV files — main data, codebook, metadata
- ⚠️ **STATUS: CSVs NOT YET DOWNLOADED** — files are Google Drive shortcuts (.webloc) in Thesis/ folder
- Privacy: dataset contains survey weights and demographic variables — must not leave local environment
- Cite: docs/data/indeksdanmark_notes.md; Thesis/indeksdanmark_data_model-1.md

### 4.3.2 Structure

| File | Dimensions | Content |
|---|---|---|
| Main data CSV | 20,134 rows × 6,364 columns | Respondent-level survey responses (float64) |
| Codebook CSV | 6,364 rows × 11 columns | Variable definitions and labels |
| Metadata CSV | 29,185 rows × 3 columns | Variable metadata |

- Estimated RAM: ~970 MB for main data CSV alone
- Variables: product preferences, brand attitudes, lifestyle indicators, socio-demographics, media consumption, retail channel preferences

### 4.3.3 Data quality checks (plan)

- Variable completeness: % missing per variable across respondents
- Survey weight validation: confirm weights sum to Danish adult population
- Variable relevance filtering: from 6,364 variables, identify ~50–100 relevant to CSD consumption behaviour (using codebook labels)
- Correlation analysis: identify redundant variables before PCA

### 4.3.4 Consumer segmentation plan (SRQ3)

- **Step 1 — Variable selection**: filter to CSD-relevant variables using codebook (beverages, supermarket shopping, brand loyalty, health consciousness)
- **Step 2 — Dimensionality reduction**: PCA to reduce ~100 variables to 10–15 principal components explaining ≥ 80% variance
- **Step 3 — Segmentation**: k-means clustering (k=4–6 determined by elbow method) on principal components → consumer segments
- **Step 4 — Retailer mapping**: assign each retailer's primary shopper profile to a segment using retailer × channel preferences in survey
- **Step 5 — Demand index**: compute segment-level demand index for CSD per retailer → time-varying enrichment feature
- Cite: Customer Segmentation + Sales Prediction (2023); Model Averaging + Double ML (Ahrens et al. 2024)

---

## 4.4 Feature engineering

### 4.4.1 Time-series features (for all models)

| Feature | Description | Models |
|---|---|---|
| `lag_1` to `lag_4` | Sales t-1, t-2, t-3, t-4 weeks | LightGBM, XGBoost, Ridge |
| `lag_8`, `lag_13`, `lag_52` | Medium/long-term lags | LightGBM, XGBoost, Ridge |
| `rolling_mean_4w` | 4-week rolling average | LightGBM, XGBoost, Ridge |
| `rolling_std_4w` | 4-week rolling standard deviation | LightGBM, XGBoost, Ridge |
| `rolling_mean_13w` | Quarterly rolling average | LightGBM, XGBoost, Ridge |
| `week_of_year` | Seasonal indicator (1–52) | All |
| `month` | Monthly seasonality | All |
| `quarter` | Quarterly indicator | All |
| `is_danish_holiday` | Danish public holiday flag | All |
| `promo_flag` | Promotion active this week | LightGBM, XGBoost, Ridge |
| `weighted_distribution` | Distribution level (0–1) | LightGBM, XGBoost, Ridge |

### 4.4.2 Consumer signal features (SRQ3)

| Feature | Description | Source |
|---|---|---|
| `consumer_demand_index` | Retailer-level demand index from PCA + k-means | Indeks Danmark |
| `segment_id` | Primary consumer segment for this retailer | Indeks Danmark |
| `trend_direction` | Quarterly change in demand index (up/flat/down) | Indeks Danmark |

### 4.4.3 ARIMA treatment

- ARIMA: univariate time-series — no exogenous features by default
- Optional extension: ARIMAX with `promo_flag` and `consumer_demand_index` as exogenous regressors
- Decision: include ARIMAX as a separate model run to assess feature value for statistical models

---

## 4.5 Train / validation / test split

- **Protocol**: strict temporal split — no random shuffling (preserves time series integrity)
- **Training set**: earliest available → [split_date_1] — used for model fitting and HPO
- **Validation set**: [split_date_1] → [split_date_2] — used for MAPE-based model selection and calibration
- **Test set**: [split_date_2] → latest — held out, used only for final evaluation (Ch.8)
- Minimum test set: 13 weeks (one quarter) — to capture seasonal variation
- Exact dates: pending Nielsen data access

---

## 4.6 Key risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Nielsen access delayed | 🟡 Medium | Fallback: synthetic CSD data or publicly available FMCG panel |
| Indeks Danmark not mappable to retailers | 🟡 Medium | Use channel-level (supermarket vs. discount) if retailer-level not feasible |
| Insufficient history (< 2 years) | 🔴 Low | Document scope limitation; use shorter seasonal cycles if needed |
| Indeks Danmark variable relevance | 🟡 Medium | Systematic codebook review + domain expert (Manifold AI) input |
| Missing data gaps in Nielsen | 🟡 Medium | Interpolation for short gaps; exclude SKUs with > 20% missing |

---

## Outstanding

- [ ] Confirm Nielsen access modality with Manifold AI (SQL vs CSV)
- [ ] Sign confidentiality agreement (CBS requirement before data access)
- [ ] Download Indeks Danmark 3 CSVs from Google Drive to Thesis/ folder
- [ ] Confirm granularity of Nielsen data (weekly vs. monthly)
- [ ] Identify Manifold contact person for Nielsen data request
