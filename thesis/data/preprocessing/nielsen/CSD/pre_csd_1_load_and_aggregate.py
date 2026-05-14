#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Step 1: Load and Aggregate

PURPOSE
=======
Load all Nielsen CSD view parquet files (validated by Step 0), join them into a
complete merged dataset, and aggregate to brand × period granularity. This step
produces an intermediate aggregate table that feeds into Steps 2-6 for calendar
fill, series filtering, feature engineering, split application, and indexing.

INPUT
=====
From Step 0 (cached parquet views):
  - csd_clean_facts_v.parquet
  - csd_clean_dim_product_v.parquet
  - csd_clean_dim_period_v.parquet
  - csd_clean_dim_market_v.parquet

OUTPUT
======
Step 1 output (aggregate.parquet):
  - Aggregated to brand × period granularity
  - Joined across all market types (retail outlet types)
  - Columns: brand, period_year, period_month, sales_units, sales_value,
    sales_liters, promo_units, weighted_dist

LOGIC
=====
  - Call Step 0 to validate parquet cache exists
  - Load all 4 view parquet files
  - Join facts × product × period × market (complete merged table)
  - Filter to positive sales (non-zero units)
  - Aggregate by brand × period (combining across all market types)

DEPENDENCIES
============
This step depends on Step 0 completion:
  thesis/data/preprocessing/nielsen/CSD/pre_csd_0_cache.py

Step 0 validates that all required parquet view files exist in:
  thesis/data/converted/nielsen/parquet_nielsen/CSD/views/

USAGE
=====
  python pre_csd_1_load_and_aggregate.py
"""

import sys, time, importlib
from pathlib import Path
import pandas as pd

# ============================================================================
# PROJECT INITIALIZATION
# ============================================================================

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

# Reload PATHS module to ensure latest configuration.
import PATHS
importlib.reload(PATHS)

from PATHS import THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR, get_category_pipeline_step_outputs_dir
from thesis.data.preprocessing.nielsen.shared.terminal_utils import (
	step_execution, print_file_load, print_file_save, print_data_preview,
	print_step_summary, print_info
)
from thesis.data.preprocessing.nielsen.shared.timing_utils import log_step_timing

# Import Step 0 validation function
sys.path.insert(0, str(Path(__file__).parent))
from pre_csd_0_cache import validate_parquet_cache

# ============================================================================
# METADATA DEFINITIONS
# ============================================================================
# This step joins Facts × Product × Period × Market dimensions and aggregates
# to brand × period granularity. All four Nielsen view tables are merged to
# create a complete dataset before aggregation.
#
# FACTS TABLE (source columns):
#   - sales_units: Total sales out of store (consumer purchase units). Non-nullable.
#   - sales_value: Total sales value in DKK. Non-nullable.
#   - sales_in_liters: Total sales volume in liters. Non-nullable.
#   - sales_units_any_promo: Sales units with any promotion applied. Nullable; 0 = no data.
#   - weighted_distribution: ACV-weighted store reach (0–1 fraction). Nullable (~16.7%).
#     NOT additive across products.
#
# PRODUCT DIMENSION:
#   - brand: Brand name (5-level hierarchy: category → manufacturer → brand → variant → UPC).
#     Never sum/aggregate across hierarchy levels.
#
# PERIOD DIMENSION:
#   - period_year, period_month: Non-nullable integers (safe for calculations).
#     Range: 2022-10 to 2026-03 (42 monthly periods on Nielsen 4-4-5 week calendar).
#
# MARKET DIMENSION:
#   - market_description: Retail outlet types (28 types: REMA 1000, NETTO, e-commerce, etc.).
#     NOT a country filter (all data is Denmark). Aggregated across all markets.
#
# OUTPUT (this step):
#   - Aggregates to brand × period granularity
#   - Combines sales across all market types (retail outlet channels)
#   - Promo units filled with 0 for missing (no promo data = no promo units)
#   - weighted_distribution averaged (ACV metric, valid operation on store samples)

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "CSD"
STEP_NUM = 1
STEP_NAME = "Load and Aggregate"

# Parquet cache location validated by Step 0
CACHE_VIEWS_DIR = THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / CATEGORY / "views"

# Output paths
STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
OUTPUT_AGGREGATE_PARQUET = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_aggregate.parquet"
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"

# ============================================================================
# STEP LOGIC
# ============================================================================

def load_and_aggregate(parquet_dir: Path) -> pd.DataFrame:
	"""
	Load Nielsen CSD parquet view files and merge into complete dataset.

	PARAMETERS
	----------
	parquet_dir : Path
		Directory containing all 4 Nielsen CSD view parquet files.
		Typically: thesis/data/converted/nielsen/parquet_nielsen/CSD/views/

	RETURNS
	-------
	pd.DataFrame
		Aggregated data with columns:
		  - brand: Brand identifier (from product dimension)
		  - period_year: Year (from period dimension)
		  - period_month: Month (from period dimension)
		  - sales_units: Summed sales units across all market types
		  - sales_value: Summed sales value (DKK) across all market types
		  - sales_liters: Summed sales volume (liters) across all market types
		  - promo_units: Summed promotional units across all market types
		  - weighted_dist: Mean ACV-weighted distribution across all market types

	NOTES
	-----
	This step merges all 4 Nielsen view tables (facts + 3 dimensions) into one
	complete dataset. The merge preserves all rows from facts and joins relevant
	dimensions. After joining, data is filtered to positive sales (non-zero units)
	and then aggregated to brand × period granularity, combining data across all
	market types (retail outlet channels like REMA 1000, NETTO, e-commerce, etc.).

	The output is an intermediate aggregate ready for downstream feature engineering
	(calendar fill, series filtering, feature creation, split application, indexing).
	"""

	print("  Loading view parquet files...")
	facts = pd.read_parquet(parquet_dir / "csd_clean_facts_v.parquet")
	products = pd.read_parquet(parquet_dir / "csd_clean_dim_product_v.parquet")
	periods = pd.read_parquet(parquet_dir / "csd_clean_dim_period_v.parquet")
	markets = pd.read_parquet(parquet_dir / "csd_clean_dim_market_v.parquet")

	print(f"  Facts shape: {facts.shape}")
	print(f"  Products shape: {products.shape}")
	print(f"  Periods shape: {periods.shape}")
	print(f"  Markets shape: {markets.shape}")

	# Join facts × product × period × market to create complete merged dataset.
	# All dimensions are joined to preserve complete context before aggregation.
	df = facts.merge(products[["product_id", "brand"]], on="product_id")
	df = df.merge(periods[["period_id", "period_year", "period_month"]], on="period_id")
	df = df.merge(markets[["market_id", "market_description"]], on="market_id")

	# Filter to positive sales (non-zero units). Rows with zero sales are noise
	# and excluded from aggregation.
	df = df[df["sales_units"] > 0].copy()

	# Aggregate by brand × period, combining across all market types.
	# This creates a monolithic dataset at brand × period granularity.
	agg_dict = {
		"sales_units": "sum",
		"sales_value": "sum",
		"sales_in_liters": "sum",
		"sales_units_any_promo": lambda x: sum(pd.Series(x).fillna(0)),
		"weighted_distribution": "mean",
	}

	aggregated = df.groupby(["brand", "period_year", "period_month"]).agg(agg_dict).reset_index()
	aggregated.columns = ["brand", "period_year", "period_month", "sales_units", "sales_value",
						 "sales_liters", "promo_units", "weighted_dist"]

	return aggregated


def main():
	"""
	Execute Step 1: Load, merge, and aggregate Nielsen CSD data.

	FLOW
	----
	1. Call Step 0 to validate parquet cache exists
	2. Load all 4 view parquet files
	3. Join them into a complete merged dataset
	4. Filter to positive sales
	5. Aggregate by brand × period
	6. Save aggregated output
	7. Log timing and row counts
	"""

	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		step_start = time.perf_counter()

		# ────────────────────────────────────────────────────────────────────
		# VALIDATION PHASE: Call Step 0 to verify parquet cache exists
		# ────────────────────────────────────────────────────────────────────

		print("\nValidating parquet cache (Step 0)...")
		validation = validate_parquet_cache(CATEGORY, CACHE_VIEWS_DIR)

		if not validation["valid"]:
			print_info("Step 0 validation failed. Parquet cache is missing.")
			print_info("Aborting Step 1 — run Step 0 first to validate cache.")
			return

		print_info(validation["message"])

		# ────────────────────────────────────────────────────────────────────
		# LOADING PHASE: Read parquet files and merge
		# ────────────────────────────────────────────────────────────────────

		print("\nLoading and merging view files...")
		load_start = time.perf_counter()
		df = load_and_aggregate(CACHE_VIEWS_DIR)
		load_elapsed = time.perf_counter() - load_start

		input_shape = df.shape
		print_file_load(CACHE_VIEWS_DIR, input_shape, load_elapsed)
		print_info(f"Unique brands: {df['brand'].nunique()}")
		if len(df) > 0:
			month_min = int(df['period_month'].min())
			month_max = int(df['period_month'].max())
			print_info(f"Date range: {df['period_year'].min()}-{month_min:02d} to {df['period_year'].max()}-{month_max:02d}")
		else:
			print_info(f"Date range: (no data)")

		# ────────────────────────────────────────────────────────────────────
		# SAVING PHASE: Write aggregated output
		# ────────────────────────────────────────────────────────────────────

		print(f"\nSaving aggregated data...")
		STEP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

		save_start = time.perf_counter()
		df.to_parquet(OUTPUT_AGGREGATE_PARQUET, index=False)
		save_elapsed = time.perf_counter() - save_start

		output_shape = df.shape
		print_file_save(OUTPUT_AGGREGATE_PARQUET, output_shape, save_elapsed)

		# ────────────────────────────────────────────────────────────────────
		# PREVIEW & LOGGING PHASE
		# ────────────────────────────────────────────────────────────────────

		print("\nData preview:")
		print_data_preview(df, title=f"{CATEGORY} Aggregated Data", max_rows=10)

		# Record execution timing
		step_elapsed = time.perf_counter() - step_start
		log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, output_shape[0], LOG_FILE,
					   input_cols=None, output_cols=output_shape[1])

		print_step_summary(
			STEP_NUM, STEP_NAME, step_elapsed,
			input_rows=input_shape[0],
			output_rows=output_shape[0],
			input_cols=None,
			output_cols=output_shape[1],
			output_file=OUTPUT_AGGREGATE_PARQUET
		)


if __name__ == "__main__":
	main()
