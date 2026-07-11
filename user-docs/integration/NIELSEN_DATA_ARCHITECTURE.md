# Nielsen Data Architecture & Preprocessing Strategy

**Date:** 2026-05-05  
**Status:** Analysis (In Discussion)  
**Context:** Defining which Nielsen table types (views vs. raw) to use in preprocessing pipelines and how to organize the data hierarchy.

---

## Table Types Overview

### Type 1: VIEWS (suffix `_v`) — Cleaned Data
- Pre-filtered, deduplicated, standardized views from Nielsen warehouse
- Column-reduced (subset of important columns)
- Organized in star schema: Facts + 3 Dimensions (market, period, product)
- Designed for quick analysis and reporting

**CSD Example:**
- `csd_clean_facts_v`: 2.5M rows, 10 columns
- `csd_clean_dim_product_v`: 2,057 rows, 18 columns
- `csd_clean_dim_market_v`: 28 rows, 2 columns
- `csd_clean_dim_period_v`: 42 rows, 4 columns

### Type 2: BASE TABLES (no suffix) — Raw Data
- Full granularity with ALL columns Nielsen provides
- Include metadata: `last_server_update`, `pipeline_run_at`, `valid_from/to`, `change_detection_hash`
- Used for audit trails, versioning, compliance
- Significantly larger and more detailed

**CSD Example:**
- `csd_clean_facts`: 33.7M rows, 39 columns (vs 10 in view)
- `csd_clean_dim_product`: 49,287 rows, 30 columns (vs 2,057 in view)
- `csd_clean_dim_market`: 587 rows, 13 columns (vs 28 in view)

### Type 3: METADATA TABLES — Schema Documentation
- Data dictionary: column names, types, descriptions, null semantics
- Purpose: Schema exploration and documentation only
- Not used in analysis pipelines

---

## Key Discussion Points

### 1. Should Size Be a Limiting Factor?

**No.** Size alone should not define preprocessing strategy.

**Reasoning:**
- More rows = more statistical power for correlation analysis
- More data allows identification of robust feature relationships
- Trade-off: Processing time vs. analytical capability

**Exception:** Only relevant for operational constraints (storage, compute time). If not a bottleneck, use full data.

---

### 2. Should Column Count Be a Limiting Factor?

**No.** More columns are beneficial for preprocessing.

**Reasoning:**
- Statistical feature reduction methods (correlation, PCA, feature importance) work best with many columns
- Larger feature space allows discovery of non-obvious relationships
- Preprocessing pipeline can apply filtering after analysis
- Shows advanced preprocessing skills: justify why features are kept/dropped

**Process:**
1. Load all available columns (raw tables)
2. Apply correlation analysis, variance analysis, domain knowledge filtering
3. Document which columns dropped and why
4. Output engineered feature set with justified selections

---

### 3. Do Join Speeds Matter?

**No,** if:
- No real-time dashboard requirements
- Preprocessing is batch-run (one-time per category)
- Model training is offline

**Therefore:** Use raw tables. Size differences (33.7M vs. 2.5M rows) don't impact one-time preprocessing.

---

### 4. Source of Assumptions (Views vs. Raw)

**Current assumption questioned:** "Views are cleaner, therefore better."

**Source:** None documented. This was inferred optimization, not validated by requirements.

**Actual considerations:**
- Views are pre-filtered by Nielsen (unknown filtering criteria)
- Raw tables preserve full context for domain-driven feature engineering
- No documentation available explaining what views removed or why

**Decision:** Without explicit requirements, use raw tables to preserve full analytical capability.

---

### 5. Data Organization Hierarchy

**Current state:** Views and raw data mixed in `data_csv/` folder

**Proposed structure:**
```
thesis/data/raw_nielsen/
  ├─ data_csv/
  │  ├─ CSD/
  │  │  ├─ views/              (from _v tables)
  │  │  ├─ raw/                (from base tables)
  │  │  └─ metadata/           (from metadata tables)
  │  ├─ Danskvand/
  │  │  ├─ views/
  │  │  ├─ raw/
  │  │  └─ metadata/
  │  ├─ Energidrikke/
  │  │  ├─ views/
  │  │  ├─ raw/
  │  │  └─ metadata/
  │  ... etc
  │
  └─ scripts/
     └─ save_all_datasets.py

thesis/data/preprocessing/
  └─ parquet_nielsen/
     ├─ CSD/
     │  ├─ views/              (cached from raw_nielsen views/)
     │  ├─ raw/                (cached from raw_nielsen raw/)
     │  ├─ metadata/           (cached from raw_nielsen metadata/)
     │  └─ engineered/         (preprocessing pipeline outputs)
     ├─ Danskvand/
     │  ├─ views/
     │  ├─ raw/
     │  ├─ metadata/
     │  └─ engineered/
     ... etc
```

**Rationale:**
- **By category first** (CSD, Danskvand, etc.): Mirrors Nielsen schema organization
- **By data type within category** (views/, raw/, metadata/): Clear purpose for each subset
- **Separation of concern:** Data source vs. engineered outputs

---

## Metadata: Currently Missing

**Observation:** Current preprocessing scripts do NOT save metadata tables.

**What metadata provides:**
- Column descriptions and units
- Data type documentation
- Null value semantics
- Data quality indicators

**Why include:**
- Reproducibility (trace columns back to definitions)
- Data quality validation
- Documentation for future analysts
- Justify feature engineering decisions

**Recommendation:** Save metadata tables as parquet alongside views and raw tables.

---

## Revised Data Usage Strategy

### For Preprocessing Pipelines

**Use: BASE TABLES (raw data)**

**Rationale:**
- Preserve all analytical capability
- Enable statistical feature reduction (correlation, variance, importance)
- Larger feature space = better opportunity to demonstrate preprocessing skills
- Size/speed not limiting factors for batch preprocessing

**Process:**
1. Load raw tables (all columns)
2. Apply domain knowledge + statistical filtering
3. Generate engineered features
4. Document feature selection decisions

### For Reference & Validation

**Save: VIEWS + METADATA**

**Rationale:**
- Views: Show Nielsen's cleaned data for comparison/validation
- Metadata: Document what each column is
- Enable reproducibility: "Feature X came from column Y (defined as Z)"

### Do NOT Use For ML Training

**Base table metadata columns** (audit trails, versioning):
- Drop before training: `last_server_update`, `pipeline_run_at`, `valid_from/to`, `change_detection_hash`
- These are not predictive, only administrative

---

## File Organization Summary

| Location | Contents | Purpose |
|----------|----------|---------|
| `data_csv/CSD/views/` | Nielsen view CSVs | Source reference |
| `data_csv/CSD/raw/` | Nielsen raw table CSVs | Full data source |
| `data_csv/CSD/metadata/` | Nielsen metadata CSVs | Schema documentation |
| `parquet_nielsen/CSD/views/` | Cached views as parquet | Fast reference loading |
| `parquet_nielsen/CSD/raw/` | Cached raw tables as parquet | Fast data loading |
| `parquet_nielsen/CSD/metadata/` | Cached metadata as parquet | Schema reference |
| `parquet_nielsen/CSD/engineered/` | Preprocessed feature matrices | ML training input |

---

## Naming Conventions

### Raw Table Naming (Preserve Source)
```
csd_clean_facts.parquet                    (from csd_clean_facts)
csd_clean_dim_product.parquet              (from csd_clean_dim_product)
csd_clean_dim_period.parquet               (from csd_clean_dim_period)
csd_clean_dim_market.parquet               (from csd_clean_dim_market)
```

### View Naming (Preserve Source)
```
csd_clean_facts_v.parquet                  (from csd_clean_facts_v)
csd_clean_dim_product_v.parquet            (from csd_clean_dim_product_v)
csd_clean_dim_period_v.parquet             (from csd_clean_dim_period_v)
csd_clean_dim_market_v.parquet             (from csd_clean_dim_market_v)
```

### Metadata Naming (Preserve Source)
```
metadata_csd_clean_facts.parquet           (from metadata_csd_clean_facts)
metadata_csd_columns.parquet               (from metadata_csd_columns)
```

### Engineered Output Naming (Drop "Specialized_")
```
csd_feature_matrix.parquet                 (engineered features)
csd_series_index.csv                       (time-series metadata)
csd_split_dates.json                       (train/val/test boundaries)
csd_preprocessing_report.md                (pipeline documentation)
```

---

## Implementation Checklist

- [ ] Update `save_all_datasets.py` to organize CSV output by: category / (views | raw | metadata)
- [ ] Update `preprocessing_csd.py` (and 4 others) to:
  - Load from raw tables (not views)
  - Save raw/views/metadata to parquet cache (not just engineered)
  - Save engineered features with simplified naming
  - Drop audit metadata columns before feature engineering
- [ ] Update `PATHS.py` with helpers for: views_dir, raw_dir, metadata_dir, engineered_dir
- [ ] Update notebooks to load dimension tables from correct parquet paths
- [ ] Document feature selection decisions in preprocessing report

---

## See Also

- `PATHS.py` — Path centralization
- `preprocessing_csd.py` — Current pipeline implementation
- `thesis/data/raw_nielsen/description/SCHEMA_SNAPSHOT.md` — Data schema reference
