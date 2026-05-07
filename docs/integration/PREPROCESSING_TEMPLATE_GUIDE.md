# Preprocessing Template: How to Apply CSD Pattern to Other 4 Categories

**Reference Script:** `preprocessing_csd.py` (completed)  
**Target Scripts:** preprocessing_danskvand.py, preprocessing_energidrikke.py, preprocessing_rtd.py, preprocessing_totalbeer.py

---

## Pattern Overview

Each preprocessing script follows the same structure:

```
1. Root discovery + dynamic PATHS import
2. Category-specific path configuration
3. Feature engineering (shared library)
4. Data validation
5. Load raw data → Feature engineering pipeline
6. Save raw/views/metadata to parquet
7. Save engineered outputs with simplified naming
```

---

## Step-by-Step Template

### 1. Imports & Path Setup

**What to change:**
- `CATEGORY = "CSD"` → `CATEGORY = "Danskvand"` (or other)
- Input paths reference new category
- Output paths use helper functions

**Template:**
```python
from PATHS import (
    ROOT_DIR,
    THESIS_DATA_PREPROCESSING_DIR,
    THESIS_DATA_NIELSEN_CSV_DIR,
    THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR,
    get_category_raw_dir,
    get_category_views_dir,
    get_category_metadata_dir,
    get_category_engineered_dir,
)

CATEGORY = "Danskvand"  # ← CHANGE THIS

# Input: organized by category and type
INPUT_RAW_DIR = THESIS_DATA_NIELSEN_CSV_DIR / CATEGORY / "raw"
INPUT_VIEWS_DIR = THESIS_DATA_NIELSEN_CSV_DIR / CATEGORY / "views"
INPUT_METADATA_DIR = THESIS_DATA_NIELSEN_CSV_DIR / CATEGORY / "metadata"

# Output: parquet files organized by category and type
OUT_RAW = get_category_raw_dir(CATEGORY)
OUT_VIEWS = get_category_views_dir(CATEGORY)
OUT_METADATA = get_category_metadata_dir(CATEGORY)
OUT_ENGINEERED = get_category_engineered_dir(CATEGORY)

for out_dir in [OUT_RAW, OUT_VIEWS, OUT_METADATA, OUT_ENGINEERED]:
    out_dir.mkdir(parents=True, exist_ok=True)
```

**Key point:** No other changes needed in this section. The category name flows through all paths automatically.

---

### 2. Data Validation

**What to change:**
- File names reference the category (e.g., `danskvand_clean_facts` instead of `csd_clean_facts`)
- Update error message to show category name

**Template:**
```python
def validate_input_data(raw_dir: Path, views_dir: Path) -> bool:
    """Check if all required Nielsen [CATEGORY] CSV files exist."""
    
    required_raw_files = [
        "danskvand_clean_facts.csv",        # ← CHANGE: category prefix
        "danskvand_clean_dim_product.csv",
        "danskvand_clean_dim_period.csv",
        "danskvand_clean_dim_market.csv",
    ]

    required_views_files = [
        "danskvand_clean_facts_v.csv",      # ← CHANGE: category prefix
        "danskvand_clean_dim_product_v.csv",
        "danskvand_clean_dim_period_v.csv",
        "danskvand_clean_dim_market_v.csv",
    ]

    # ... rest is identical
```

**Key point:** Only change the file names (not the logic).

---

### 3. Load Raw Data

**What to change:**
- File names (load from raw, not views)

**Template:**
```python
def load_raw(input_dir: Path) -> pd.DataFrame:
    """Load Nielsen [CATEGORY] raw data from local CSV files."""
    
    print("  Loading raw CSV files...")
    facts = pd.read_csv(input_dir / "danskvand_clean_facts.csv")        # ← CHANGE
    products = pd.read_csv(input_dir / "danskvand_clean_dim_product.csv", on_bad_lines='skip')
    periods = pd.read_csv(input_dir / "danskvand_clean_dim_period.csv")
    markets = pd.read_csv(input_dir / "danskvand_clean_dim_market.csv")
    
    # ... rest is identical (joins, aggregation)
```

**Key point:** Only change file names. The rest of the logic (joins, filtering, aggregation) is identical.

---

### 4. Save Dimension Tables

**What to change:**
- File names (category prefix)

**Template:**
```python
def save_dimension_tables(input_raw_dir: Path, input_views_dir: Path, input_metadata_dir: Path):
    """Save raw tables, views, and metadata as parquet for caching."""
    
    print("\n  Caching raw tables as parquet...")
    for table_name in ["danskvand_clean_facts",              # ← CHANGE
                       "danskvand_clean_dim_product",
                       "danskvand_clean_dim_period",
                       "danskvand_clean_dim_market"]:
        try:
            df = pd.read_csv(input_raw_dir / f"{table_name}.csv")
            df.to_parquet(OUT_RAW / f"{table_name}.parquet", index=False)
            print(f"    ✓ {table_name}: {len(df):,} rows")
        except FileNotFoundError:
            print(f"    ⚠ {table_name}: CSV not found (skipped)")

    print("  Caching view tables as parquet...")
    for table_name in ["danskvand_clean_facts_v",            # ← CHANGE
                       "danskvand_clean_dim_product_v",
                       "danskvand_clean_dim_period_v",
                       "danskvand_clean_dim_market_v"]:
        # ... same pattern

    print("  Caching metadata tables as parquet...")
    for table_name in ["metadata_danskvand_columns"]:        # ← CHANGE (varies by category)
        # ... same pattern
```

**Key point:** 
- Only change file names
- Some categories have fewer metadata tables (e.g., Danskvand has only `metadata_danskvand_columns`, not 5 like CSD)
- Check SCHEMA_SNAPSHOT.md for exact metadata table names per category

---

### 5. Save Engineered Outputs

**What to change:**
- Output filenames (use lowercase category name)

**Template:**
```python
def save_engineered_outputs(df: pd.DataFrame, series_idx: pd.DataFrame,
                           all_dates: list, elapsed: float, peak_mb: float):
    """Save engineered features with simplified naming."""
    
    # Feature matrix
    df.to_parquet(OUT_ENGINEERED / f"{CATEGORY.lower()}_feature_matrix.parquet", index=False)
    
    # Series index
    series_idx.to_csv(OUT_ENGINEERED / f"{CATEGORY.lower()}_series_index.csv", index=False)
    
    # Split dates
    with open(OUT_ENGINEERED / f"{CATEGORY.lower()}_split_dates.json", "w") as f:
        json.dump(split_dates, f, indent=2)
    
    # Report
    (OUT_ENGINEERED / f"{CATEGORY.lower()}_preprocessing_report.md").write_text(report)
```

**Key point:** `CATEGORY.lower()` automatically converts "Danskvand" → "danskvand". No hardcoding.

---

### 6. Main Function

**What to change:**
- Input directory names

**Template:**
```python
def main():
    print("=" * 80)
    print(f"Nielsen {CATEGORY} Preprocessing Pipeline")
    print("=" * 80)
    # ... header (identical)

    # Validate input data
    if not validate_input_data(INPUT_RAW_DIR, INPUT_VIEWS_DIR):  # ← USE NEW PATHS
        print("\nAbort: Input validation failed.")
        return

    # Step 0: Cache raw/views/metadata
    print("\nStep 0/6 — Caching Nielsen data as parquet...")
    save_dimension_tables(INPUT_RAW_DIR, INPUT_VIEWS_DIR, INPUT_METADATA_DIR)  # ← USE NEW PATHS

    # ... rest is identical (feature engineering pipeline)

    # Step 1: Load raw data
    print("\nStep 1/6 — Loading raw data from CSV files...")
    raw = load_raw(INPUT_RAW_DIR)  # ← USE NEW PATH
```

**Key point:** Only change path variable names at the call sites.

---

## Category-Specific Notes

### Metadata Tables

Different categories have different metadata tables. Check `SCHEMA_SNAPSHOT.md`:

| Category | Metadata Tables |
|----------|-----------------|
| CSD | metadata_csd_clean_facts, metadata_csd_clean_dim_product, metadata_csd_clean_dim_period, metadata_csd_clean_dim_market, metadata_csd_columns |
| Danskvand | metadata_danskvand_columns |
| Energidrikke | metadata_energidrikke_columns |
| RTD | metadata_rtd_columns |
| Totalbeer | metadata_totalbeer_columns |

**Update save_dimension_tables()** to include only the metadata tables that exist for that category.

---

## Naming Conventions

### Raw Table Names (Source)
```
csd_clean_facts.csv
csd_clean_dim_product.csv
csd_clean_dim_period.csv
csd_clean_dim_market.csv
```

### View Table Names (Source)
```
csd_clean_facts_v.csv
csd_clean_dim_product_v.csv
csd_clean_dim_period_v.csv
csd_clean_dim_market_v.csv
```

### Engineered Output Names (Simplified)
```
csd_feature_matrix.parquet
csd_series_index.csv
csd_split_dates.json
csd_preprocessing_report.md
```

**Pattern:** `{category_lower}_*`

---

## Quick Checklist (Per Script)

- [ ] Update CATEGORY variable
- [ ] Update file names in validate_input_data() (raw tables)
- [ ] Update file names in validate_input_data() (view tables)
- [ ] Update file names in load_raw()
- [ ] Update table names in save_dimension_tables() (raw)
- [ ] Update table names in save_dimension_tables() (views)
- [ ] Update table names in save_dimension_tables() (metadata) — **check category-specific list**
- [ ] Verify output filenames use `CATEGORY.lower()` (should be automatic if using template)
- [ ] Update main() to use INPUT_RAW_DIR, INPUT_VIEWS_DIR, INPUT_METADATA_DIR
- [ ] Test: Import PATHS, verify no errors

---

## Common Mistakes to Avoid

❌ **Don't:** Forget to update file names in load_raw()
```python
# WRONG: This loads from views, not raw
facts = pd.read_csv(input_dir / "danskvand_clean_facts_v.csv")
```

✅ **Do:** Load from raw tables
```python
# CORRECT: Load from raw
facts = pd.read_csv(input_dir / "danskvand_clean_facts.csv")
```

---

❌ **Don't:** Hardcode category name in output filenames
```python
# WRONG: Won't work if CATEGORY changes
df.to_parquet(OUT_ENGINEERED / "danskvand_feature_matrix.parquet")
```

✅ **Do:** Use CATEGORY variable
```python
# CORRECT: Works for any category
df.to_parquet(OUT_ENGINEERED / f"{CATEGORY.lower()}_feature_matrix.parquet")
```

---

❌ **Don't:** Miss category-specific metadata tables
```python
# WRONG: CSD has 5 metadata tables, but Danskvand only has 1
for table_name in ["metadata_category_clean_facts", ...]:  # Don't assume
```

✅ **Do:** Check SCHEMA_SNAPSHOT.md and only save what exists
```python
# CORRECT: Only save what exists for this category
for table_name in ["metadata_danskvand_columns"]:  # Danskvand only
```

---

## See Also

- `preprocessing_csd.py` — Completed template (reference)
- `SCHEMA_SNAPSHOT.md` — Nielsen schema (for metadata table names)
- `docs/integration/IMPLEMENTATION_SUMMARY_20260505.md` — What was done & why
