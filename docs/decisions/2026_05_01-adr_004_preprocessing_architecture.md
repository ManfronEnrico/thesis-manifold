---
title: "ADR-004: Data Preprocessing Pipeline Architecture"
type: decision
status: accepted
created: 2026-05-01
author: Brian (with analysis of Enrico's original preprocessing.py)
---

# ADR-004: Data Preprocessing Pipeline Architecture

**Status**: ACCEPTED — implemented per discussion 2026-05-01
**Date**: 2026-05-01
**Deciders**: Brian

---

## Context

The thesis requires converting raw Nielsen and Indeks Danmark data sources into optimized Parquet feature matrices for consumption by 10+ Jupyter modelling notebooks. A preprocessing pipeline (`preprocessing.py`) was originally written by Enrico as a single monolithic script targeting only CSD (Carbonated Soft Drinks) data.

Current state:
- One `preprocessing.py` handling only CSD category
- Output path outdated (`results/phase1/` — no longer valid)
- Not integrated with centralized `paths.py`
- Multiple data categories (CSD, danskvand, energidrikke, rtd, totalbeer, etc.) need similar pipelines
- No category parameterization or flexibility

---

## Preprocessing Pipeline: What It Does

The pipeline is a **one-time, irreversible data transformation** with these steps:

### Step 1: Pull Raw Data (SQL)
- Connects to Nielsen Fabric warehouse via ODBC
- Executes SQL JOIN: facts × product_dim × period_dim × market_dim
- Filters to ONE market category (e.g., "Carbonated Soft Drinks")
- Aggregates across products to grain: brand × period_month
- Extracts: sales_units, sales_value, sales_liters, promo_units, weighted_distribution

### Step 2: Build Calendar (external function)
- For each brand, fills missing months with zeros
- Creates complete time series (no gaps)
- Ensures all brands have uniform date coverage

### Step 3: Filter Short Series (external function)
- Removes brands with < MIN_PERIODS (e.g., 12) non-zero observations
- Rationale: Too few data points → unreliable forecasting models
- Result: ~300 brands → ~200 brands (for CSD)

### Step 4: Engineer Features (external function)
- Computes derived features: lags, moving averages, seasonality, growth rates, transformations
- Scales raw sales values → modelling-ready feature matrix
- Output: one row per (brand, period) with all engineered features

### Step 5: Apply Train/Val/Test Split (external function)
- Locks temporal boundaries:
  - Train: 2019-2021
  - Val: 2022
  - Test: 2023-2024
- Adds "split" column (categorical: train/val/test)

### Step 6: Save Outputs
Four files per category:
- **feature_matrix.parquet** — all rows, all features; consumed by modelling notebooks
- **series_index.csv** — one row per brand; metadata (total_sales, periods_per_split, etc.)
- **split_dates.json** — train/val/test date boundaries; used by notebooks for reproducibility
- **preprocessing_report.md** — human-readable summary (brands kept, feature count, RAM usage, elapsed time)

**Note**: This is a **batch, irreversible operation**. It's not designed to be incremental or re-runnable with new data (that would require versioning + backfill logic).

---

## Decision Options

### Option A: Single Parameterized Script
- One `preprocessing.py` with `CATEGORY` as CLI argument
- Pros: DRY (Don't Repeat Yourself); shared logic; easier to update common steps
- Cons: Script grows complex; hard to debug category-specific issues; risk of one category breaking others; harder to maintain

### Option B: One Script Per Category
- `preprocessing_csd.py`, `preprocessing_danskvand.py`, `preprocessing_energidrikke.py`, etc.
- Keep `preprocessing_csd_old.py` as frozen backup/reference
- Pros: Simple; isolated; easy to debug; easy to extend (add category-specific logic without touching others); one-to-one mapping (category ↔ script)
- Cons: Code duplication; updating shared logic requires 6+ edits

### Option C: Hybrid — One Master Script + Category Runners
- `preprocessing_runner.py` — orchestrates all categories sequentially
- `preprocessing_csd.py`, etc. — individual category scripts (can also run standalone)
- Pros: Best of both worlds (DRY for the runner, isolation for each category)
- Cons: Extra complexity; two layers to maintain

---

## Decision

**Chosen option**: Option B — One script per category

**Rationale**:
1. **Maintenance ease**: Each script is independent; a bug in CSD preprocessing doesn't risk danskvand
2. **Debugging**: Category-specific issues are isolated; easier to trace root cause
3. **Extensibility**: Adding category-specific logic (e.g., special handling for outliers, different feature engineering) doesn't require refactoring shared code
4. **Clarity**: One-to-one mapping (category → script) is immediately obvious
5. **Backup safety**: Original `preprocessing_csd_old.py` serves as frozen reference; easy rollback if needed
6. **Team collaboration**: Enrico (original author) and Brian (refactorer) can work on different categories in parallel without merge conflicts

**Implementation plan**:
1. Rename current file: `preprocessing.py` → `preprocessing_csd_old.py` (frozen backup)
2. Create `preprocessing_csd.py` (duplicate of old; adapted to new architecture)
   - Import from `paths.py` (ROOT_DIR, THESIS_DATA_NIELSEN_PARQUET_DIR, THESIS_MODELLING_NOTEBOOKS_DIR)
   - Add CATEGORY="CSD" constant
   - Fix output paths: use new hierarchy `thesis/modelling/notebooks/SRQ_1/specialized_CSD/specialized_CSD_outputs/`
   - Test with real Nielsen data
3. Once CSD works, duplicate → `preprocessing_danskvand.py`, etc. (update CATEGORY + market name)
4. All 6 scripts tested and working
5. Delete `preprocessing_csd_old.py` (backup no longer needed)

**Future Option**: If a common-logic update is needed (e.g., new feature engineering step), create `preprocessing_shared.py` as a module; all scripts import from it. This preserves isolation while reducing duplication.

---

## Consequences

### Positive
- Each category pipeline is independently debuggable
- No risk of one category breaking others
- Easy to add category-specific preprocessing without affecting others
- Clear code ownership: one script per category
- Team can work on multiple categories in parallel

### Negative
- Code duplication across 6 scripts (mitigated by modularizing shared logic later if needed)
- Must test all 6 scripts (not just one parameterized script)
- If core Nielsen connector changes, must update 6 imports (manageable with IDE refactoring tools)

---

## References

- `thesis/data/preprocessing/preprocessing.py` — original monolithic script (now to be backed up as `preprocessing_csd_old.py`)
- `paths.py` — centralized path definitions (to be imported by all preprocessing scripts)
- P0017 Plan (Jupyter notebook path centralization) — defines new notebook output hierarchy
- Nielsen connector: `thesis/data/nielsen/scripts/nielsen_connector.py` — ODBC wrapper

---

## Related Decisions

- ADR-003 (Builder Agent Fate) — may depend on preprocessed parquet availability
- P0017 (Jupyter notebook path centralization) — defines output folder structure that preprocessing scripts must respect
