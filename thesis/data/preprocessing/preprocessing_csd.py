"""
Nielsen CSD Preprocessing Pipeline
====================================
Reads raw Nielsen CSD data from local JSONL files, engineers all features
required for the 5 forecasting models, applies the locked train/val/test split,
and saves the feature matrix to disk in Parquet format.

Input files (from raw_nielsen/data_jsonl/CSD/):
  views/csd_clean_facts_v.jsonl
  views/csd_clean_dim_product_v.jsonl
  views/csd_clean_dim_period_v.jsonl
  views/csd_clean_dim_market_v.jsonl

Output files (Parquet, in preprocessing/parquet_nielsen/):
  specialized_CSD_feature_matrix.parquet
  series_index.csv
  split_dates.json
  preprocessing_report.md

Usage:
  python3 preprocessing_csd.py
"""

import sys, json, tracemalloc, time, importlib
from pathlib import Path

import pandas as pd

# ============================================================================
# CENTRALIZED PATHS
# ============================================================================

# Find project root by locating CLAUDE.md -> works regardless of where script is run from
current = Path.cwd()
while current != current.parent:
    if (current / "CLAUDE.md").exists():
        ROOT_DIR_FINDER = current
        break
    current = current.parent
else:
    raise FileNotFoundError("Could not find project root (CLAUDE.md)")

print(f"Project root found at: {ROOT_DIR_FINDER}")
sys.path.insert(0, str(ROOT_DIR_FINDER))

# Import paths module and reload to ensure latest changes
import PATHS
importlib.reload(PATHS)

from PATHS import (
    ROOT_DIR,
    THESIS_DATA_PREPROCESSING_DIR,
    THESIS_DATA_NIELSEN_JSONL_DIR,
    THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR,
    get_category_raw_dir,
    get_category_views_dir,
    get_category_metadata_dir,
    get_category_engineered_dir,
)

# ============================================================================
# CATEGORY CONFIGURATION
# ============================================================================

CATEGORY = "CSD"

# ============================================================================
# INPUT/OUTPUT PATHS (Dynamic from PATHS.py)
# ============================================================================

# Input: Nielsen JSONL files organized by type
INPUT_VIEWS_DIR = THESIS_DATA_NIELSEN_JSONL_DIR / CATEGORY / "views"
INPUT_METADATA_DIR = THESIS_DATA_NIELSEN_JSONL_DIR / CATEGORY / "metadata"

# Output: parquet files organized by category and type
OUT_RAW = get_category_raw_dir(CATEGORY)
OUT_VIEWS = get_category_views_dir(CATEGORY)
OUT_METADATA = get_category_metadata_dir(CATEGORY)
OUT_ENGINEERED = get_category_engineered_dir(CATEGORY)

# Create all output directories
for out_dir in [OUT_RAW, OUT_VIEWS, OUT_METADATA, OUT_ENGINEERED]:
    out_dir.mkdir(parents=True, exist_ok=True)

print(f"Input (Views): {INPUT_VIEWS_DIR.resolve()}")
print(f"Output (Engineered): {OUT_ENGINEERED.resolve()}")

# ============================================================================
# FEATURE ENGINEERING IMPORTS
# ============================================================================

from thesis.thesis_agents.ai_research_framework.features.engineer_features import (
    make_calendar,
    filter_series,
    engineer_features,
    apply_split,
    build_series_index,
    DEFAULT_TARGET_MARKET as TARGET_MARKET,
    DEFAULT_MIN_PERIODS as MIN_PERIODS,
    DEFAULT_TRAIN_END as TRAIN_END,
    DEFAULT_VAL_END as VAL_END,
)

# ============================================================================
# DATA VALIDATION
# ============================================================================

def validate_input_data(raw_dir: Path, views_dir: Path) -> bool:
    """
    Check if all required Nielsen CSD JSONL files exist in raw and views directories.
    If any are missing, print instructions on how to download them.
    Returns True if at least raw tables exist, False otherwise.
    """
    required_raw_files = [
        "csd_clean_facts.jsonl",
        "csd_clean_dim_product.jsonl",
        "csd_clean_dim_period.jsonl",
        "csd_clean_dim_market.jsonl",
    ]

    required_views_files = [
        "csd_clean_facts_v.jsonl",
        "csd_clean_dim_product_v.jsonl",
        "csd_clean_dim_period_v.jsonl",
        "csd_clean_dim_market_v.jsonl",
    ]

    missing_raw = [f for f in required_raw_files if not (raw_dir / f).exists()]
    missing_views = [f for f in required_views_files if not (views_dir / f).exists()]

    if missing_views:
        print("=" * 80)
        print("ERROR: Missing required Nielsen JSONL view files!")
        print("=" * 80)
        print(f"\nViews location: {views_dir.resolve()}\n")
        print("Missing view files:")
        for f in missing_views:
            print(f"  - {f}")
        print("\n" + "=" * 80)
        print("SOLUTION: Download Nielsen data from Fabric warehouse")
        print("=" * 80)
        print("\nRun the following command from the project root:")
        print("\n  python thesis/data/raw_nielsen/scripts/save_all_datasets.py\n")
        print("This requires:")
        print("  - .env file in project root with RU_* credentials")
        print("  - ODBC Driver 18 for SQL Server")
        print("  - pip install pyodbc azure-identity python-dotenv\n")
        print("Script location: thesis/data/raw_nielsen/scripts/save_all_datasets.py")
        print("=" * 80)
        return False

    if missing_raw:
        print(f"⚠ Warning: Raw tables not found, will skip caching raw tables")
        return True  # Can still proceed if views exist

    print(f"✓ Input validation: All required view files found")
    return True


# ============================================================================
# PIPELINE STEPS
# ============================================================================

# ── 1. Load raw data from local JSONL files ─────────────────────────────────

def load_raw(input_dir: Path) -> pd.DataFrame:
    """
    Load Nielsen CSD data from local JSONL view files.
    Reads facts × product dim × period dim (from views, which are cleaned/reduced).
    Filters to TARGET_MARKET, then aggregates to brand × month grain.
    """
    print("  Loading view JSONL files...")
    facts = pd.read_json(input_dir / "csd_clean_facts_v.jsonl", lines=True)
    products = pd.read_json(input_dir / "csd_clean_dim_product_v.jsonl", lines=True)
    periods = pd.read_json(input_dir / "csd_clean_dim_period_v.jsonl", lines=True)
    markets = pd.read_json(input_dir / "csd_clean_dim_market_v.jsonl", lines=True)

    print(f"  Facts shape: {facts.shape}")
    print(f"  Products shape: {products.shape}")
    print(f"  Periods shape: {periods.shape}")
    print(f"  Markets shape: {markets.shape}")

    # Join facts × product × period × market
    df = facts.merge(products[["product_id", "brand"]], on="product_id")
    df = df.merge(periods[["period_id", "period_year", "period_month"]], on="period_id")
    df = df.merge(markets[["market_id", "market_description"]], on="market_id")

    # Filter to target market
    df = df[df["market_description"] == TARGET_MARKET].copy()

    # Filter to positive sales
    df = df[df["sales_units"] > 0].copy()

    # Aggregate by brand × period
    agg_dict = {
        "sales_units": "sum",
        "sales_value": "sum",
        "sales_in_liters": "sum",
        "sales_units_any_promo": lambda x: sum(pd.Series(x).fillna(0)),
        "weighted_distribution": "mean",
    }

    raw = df.groupby(["brand", "period_year", "period_month"]).agg(agg_dict).reset_index()
    raw.columns = ["brand", "period_year", "period_month", "sales_units", "sales_value",
                   "sales_liters", "promo_units", "weighted_dist"]

    print("\n  ✓ Aggregated data (first 10 rows):")
    print(raw.head(10).to_string(index=False))

    return raw


# Steps 2-6 (calendar, series filter, feature engineering, split, series index)
# are imported from thesis.thesis_agents.ai_research_framework.features.engineer_features
# to avoid duplication between the CLI batch script and the LangGraph agent.


# ── 2. Save raw/views/metadata to parquet cache ──────────────────────────

def save_dimension_tables(input_raw_dir: Path, input_views_dir: Path, input_metadata_dir: Path):
    """
    Save raw tables, views, and metadata as parquet for caching and reference.

    These are cached copies of Nielsen data (not engineered—used for validation,
    analysis, and reproducibility).
    """
    print("\n  Caching raw tables as parquet...")

    # Raw tables (full granularity)
    for table_name in ["csd_clean_facts", "csd_clean_dim_product",
                       "csd_clean_dim_period", "csd_clean_dim_market"]:
        try:
            df = pd.read_json(input_raw_dir / f"{table_name}.jsonl", lines=True)
            df.to_parquet(OUT_RAW / f"{table_name}.parquet", index=False)
            print(f"    ✓ {table_name}: {len(df):,} rows")
        except FileNotFoundError:
            print(f"    ⚠ {table_name}: JSONL not found (skipped)")

    print("  Caching view tables as parquet...")

    # Views (cleaned, column-reduced)
    for table_name in ["csd_clean_facts_v", "csd_clean_dim_product_v",
                       "csd_clean_dim_period_v", "csd_clean_dim_market_v"]:
        try:
            df = pd.read_json(input_views_dir / f"{table_name}.jsonl", lines=True)
            df.to_parquet(OUT_VIEWS / f"{table_name}.parquet", index=False)
            print(f"    ✓ {table_name}: {len(df):,} rows")
        except FileNotFoundError:
            print(f"    ⚠ {table_name}: JSONL not found (skipped)")

    print("  Caching metadata tables as parquet...")

    # Metadata (schema documentation)
    for table_name in ["metadata_csd_clean_facts", "metadata_csd_clean_dim_product",
                       "metadata_csd_clean_dim_period", "metadata_csd_clean_dim_market",
                       "metadata_csd_columns"]:
        try:
            df = pd.read_json(input_metadata_dir / f"{table_name}.jsonl", lines=True)
            df.to_parquet(OUT_METADATA / f"{table_name}.parquet", index=False)
            print(f"    ✓ {table_name}: {len(df):,} rows")
        except FileNotFoundError:
            print(f"    ⚠ {table_name}: JSONL not found (skipped)")


# ── 3. Save engineered outputs ───────────────────────────────────────────────

def save_engineered_outputs(df: pd.DataFrame, series_idx: pd.DataFrame,
                           all_dates: list, elapsed: float, peak_mb: float):
    """
    Save engineered features, metadata, and report to engineered/ directory.
    Uses simplified naming (category only, no "specialized_" prefix).
    """

    # Feature matrix
    df.to_parquet(OUT_ENGINEERED / f"{CATEGORY.lower()}_feature_matrix.parquet", index=False)

    # Series index
    series_idx.to_csv(OUT_ENGINEERED / f"{CATEGORY.lower()}_series_index.csv", index=False)

    # Split dates
    split_dates = {
        "train_start": str(min(all_dates).date()),
        "train_end":   f"{TRAIN_END[0]}-{TRAIN_END[1]:02d}-01",
        "val_start":   f"{TRAIN_END[0]}-{TRAIN_END[1]+1 if TRAIN_END[1]<12 else 1:02d}-01",
        "val_end":     f"{VAL_END[0]}-{VAL_END[1]:02d}-01",
        "test_start":  f"{VAL_END[0]}-{VAL_END[1]+1 if VAL_END[1]<12 else 1:02d}-01",
        "test_end":    str(max(all_dates).date()),
    }
    with open(OUT_ENGINEERED / f"{CATEGORY.lower()}_split_dates.json", "w") as f:
        json.dump(split_dates, f, indent=2)

    # Preprocessing report
    n_brands = df["brand"].nunique()
    n_rows   = len(df)
    features = [c for c in df.columns
                if c not in ["brand", "date", "period_year", "period_month",
                             "split", "sales_units", "log_sales_units"]]

    report = f"""# Nielsen {CATEGORY} Preprocessing Report

**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Category:** {CATEGORY}
**Market Scope:** {TARGET_MARKET}
**Min Periods Filter:** {MIN_PERIODS}

## Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | {n_brands} |
| Total rows | {n_rows:,} |
| Periods per brand | {n_rows // n_brands} |
| Features engineered | {len(features)} |
| Peak RAM (preprocessing) | {peak_mb:.1f} MB |
| Elapsed time | {elapsed:.1f} s |

## Split Boundaries

| Split | Start | End | Periods |
|---|---|---|---|
| Train | {split_dates["train_start"]} | {split_dates["train_end"]} | {series_idx["train_periods"].iloc[0]} |
| Val | {split_dates["val_start"]} | {split_dates["val_end"]} | {series_idx["val_periods"].iloc[0]} |
| Test | {split_dates["test_start"]} | {split_dates["test_end"]} | {series_idx["test_periods"].iloc[0]} |

## Engineered Features

{chr(10).join(f"- `{f}`" for f in features)}

## Top 20 Brands by Total Sales Units

{series_idx.head(20).to_markdown(index=False)}
"""
    (OUT_ENGINEERED / f"{CATEGORY.lower()}_preprocessing_report.md").write_text(report)
    print(report)


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print(f"Nielsen {CATEGORY} Preprocessing Pipeline")
    print("=" * 80)
    print(f"Category: {CATEGORY}")
    print(f"Market scope: {TARGET_MARKET}")
    print(f"Min periods: {MIN_PERIODS}\n")

    # Validate input data exists
    if not validate_input_data(INPUT_VIEWS_DIR, INPUT_VIEWS_DIR):
        print("\nAbort: Input validation failed.")
        return

    # Step 0: Cache views/metadata as parquet (one-time setup)
    print("\nStep 0/6 — Caching Nielsen data as parquet...")
    save_dimension_tables(INPUT_VIEWS_DIR, INPUT_VIEWS_DIR, INPUT_METADATA_DIR)

    tracemalloc.start()
    t0 = time.perf_counter()

    print("\nStep 1/6 — Loading raw data from JSONL files...")
    raw = load_raw(INPUT_VIEWS_DIR)
    print(f"  Raw rows: {len(raw):,}  |  Brands: {raw['brand'].nunique()}\n")

    print("Step 2/6 — Building full calendar index...")
    df, all_dates = make_calendar(raw)
    print(f"  Rows after calendar fill: {len(df):,}")
    print(f"  Date range: {min(all_dates).date()} to {max(all_dates).date()}")
    print("  ✓ Calendar-filled data (first 10 rows):")
    print(df.head(10).to_string(index=False))
    print()

    print("Step 3/6 — Filtering short series...")
    df = filter_series(df)
    print(f"  Series kept after filter (>= {MIN_PERIODS} non-zero periods): "
          f"{df['brand'].nunique()} brands")
    print("  ✓ Filtered data (first 10 rows):")
    print(df.head(10).to_string(index=False))
    print()

    print("Step 4/6 — Engineering features...")
    df = engineer_features(df)
    print(f"  Feature engineering complete")
    print(f"  Columns: {df.shape[1]}")
    print("  ✓ Feature-engineered data (first 5 rows, selected columns):")
    cols_to_show = ["brand", "date", "sales_units", "log_sales_units", "lag_1", "rolling_mean_4", "month", "holiday_month"]
    print(df[cols_to_show].head(5).to_string(index=False))
    print()

    print("Step 5/6 — Applying split labels...")
    df = apply_split(df)
    print(f"  Split labels applied")
    print(f"  Split distribution: {df['split'].value_counts().to_dict()}")
    print("  ✓ Final feature matrix (first 5 rows):")
    print(df[["brand", "date", "sales_units", "split"]].head(5).to_string(index=False))
    print()

    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_mb = peak / 1024 / 1024

    print(f"Done in {elapsed:.1f}s  |  Peak RAM: {peak_mb:.1f} MB\n")

    print("Step 6/6 — Saving engineered features...")
    series_idx = build_series_index(df)
    save_engineered_outputs(df, series_idx, all_dates, elapsed, peak_mb)

    print(f"\nOutputs summary:")
    print(f"  Raw tables:       {OUT_RAW}/")
    print(f"  View tables:      {OUT_VIEWS}/")
    print(f"  Metadata tables:  {OUT_METADATA}/")
    print(f"  Engineered data:  {OUT_ENGINEERED}/")


if __name__ == "__main__":
    main()
