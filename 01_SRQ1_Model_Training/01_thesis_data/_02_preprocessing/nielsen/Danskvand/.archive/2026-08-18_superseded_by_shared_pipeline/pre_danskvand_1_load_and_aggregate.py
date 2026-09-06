#!/usr/bin/env python3
"""
Nielsen Danskvand Preprocessing â€” Step 1: Load and Aggregate

Input:  Step 0 output or raw Nielsen JSONL view files
		- danskvand_clean_facts_v.jsonl
		- danskvand_clean_dim_product_v.jsonl
		- danskvand_clean_dim_period_v.jsonl
		- danskvand_clean_dim_market_v.jsonl

Output: Step 1 output (aggregate.parquet)
		- Aggregated to brand Ã— period granularity
		- Filtered to target market (Denmark)
		- Columns: brand, period_year, period_month, sales_units, sales_value, sales_liters, promo_units, weighted_dist

Logic:
  - Load fact and dimension tables from views (cleaned, column-reduced)
  - Join facts Ã— product Ã— period Ã— market
  - Filter to target market
  - Aggregate by brand Ã— period
"""

import sys, time
from pathlib import Path
import pandas as pd

# Find project root
current = Path.cwd()
while current != current.parent:
	if (current / "CLAUDE.md").exists():
		ROOT_DIR = current
		break
	current = current.parent
else:
	raise FileNotFoundError("Could not find project root")

sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "02_thesis_data" / "_02_preprocessing" / "nielsen" / "_shared_modules"))

from PATHS import THESIS_DATA_RAW_NIELSEN_JSONL_DIR, THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR, get_category_pipeline_step_outputs_dir
from utility_scripts.scripts.METADATA import get_column_definition, describe_column
from terminal_utils import (
	step_execution, print_file_load, print_file_save, print_data_preview,
	print_step_summary, print_info
)
from timing_utils import log_step_timing

# ============================================================================
# METADATA DEFINITIONS
# ============================================================================
# This step joins Facts Ã— Product Ã— Period Ã— Market dimensions and aggregates to brand Ã— period.
# Key column definitions from Nielsen metadata:
#
# FACTS TABLE (source columns):
#   - sales_units: Total sales out of store (consumer purchase units). Non-nullable.
#   - sales_value: Total sales value in DKK. Non-nullable.
#   - sales_in_liters: Total sales volume in liters. Non-nullable.
#   - sales_units_any_promo: Sales units with any promotion applied. Nullable; 0 = no data.
#   - weighted_distribution: ACV-weighted store reach (0â€“1 fraction). Nullable (~16.7%). NOT additive across products.
#
# PRODUCT DIMENSION:
#   - brand: Brand name (5-level hierarchy: category â†’ manufacturer â†’ brand â†’ variant â†’ UPC).
#     Never sum/aggregate across hierarchy levels.
#
# PERIOD DIMENSION:
#   - period_year, period_month: Non-nullable integers (safe to use directly for calculations).
#     Range: 2022-10 to 2026-03 (42 monthly periods on Nielsen 4-4-5 week calendar).
#
# MARKET DIMENSION:
#   - market_description: Retail outlet types. Filter to "DVH EXCL. HD" — Nielsen's
#     standard Danish grocery scope (supermarkets excl. hard discounters Aldi/Lidl).
#     Per Nielsen metadata: "Unless the user specifies a particular market, always use DVH EXCL. HD".
#
# OUTPUT (this step):
#   - Aggregates to brand Ã— period granularity
#   - Null-safe: Keeps NaN from sales_units for missing observations (used in step 2 calendar fill)
#   - Null-safe: Promo units filled with 0 for missing (no promo data = no promo units)
#   - weighted_distribution averaged (ACV metric, valid operation on store samples)

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "Danskvand"
STEP_NUM = 1
STEP_NAME = "Load and Aggregate"

# Nielsen standard scope: Danish grocery retail excl. hard discounters (Aldi/Lidl)
TARGET_MARKET = "DVH EXCL. HD"

# Input paths (Nielsen view files)
INPUT_VIEWS_DIR = THESIS_DATA_RAW_NIELSEN_JSONL_DIR / CATEGORY / "views"

# Cached parquet from step 0
CACHED_PARQUET_VIEWS_DIR = THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / CATEGORY / "views"

# Output paths
STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
OUTPUT_AGGREGATE_PARQUET = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_aggregate.parquet"
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"

# ============================================================================
# STEP LOGIC
# ============================================================================

def load_and_aggregate(input_dir: Path, target_market: str, cached_parquet_dir: Path = None) -> pd.DataFrame:
	"""
	Load Nielsen Danskvand data from parquet cache (if available) or JSONL files.

	Tries cached parquet first (from step 0, if available). Falls back to JSONL.
	"""
	# Try cached parquet first
	if cached_parquet_dir and (cached_parquet_dir / "danskvand_clean_facts_v.parquet").exists():
		print("  Loading view parquet files (cached from step 0)...")
		facts = pd.read_parquet(cached_parquet_dir / "danskvand_clean_facts_v.parquet")
		products = pd.read_parquet(cached_parquet_dir / "danskvand_clean_dim_product_v.parquet")
		periods = pd.read_parquet(cached_parquet_dir / "danskvand_clean_dim_period_v.parquet")
		markets = pd.read_parquet(cached_parquet_dir / "danskvand_clean_dim_market_v.parquet")
	else:
		# Fallback to JSONL
		print("  Loading view JSONL files...")
		facts = pd.read_json(input_dir / "danskvand_clean_facts_v.jsonl", lines=True)
		products = pd.read_json(input_dir / "danskvand_clean_dim_product_v.jsonl", lines=True)
		periods = pd.read_json(input_dir / "danskvand_clean_dim_period_v.jsonl", lines=True)
		markets = pd.read_json(input_dir / "danskvand_clean_dim_market_v.jsonl", lines=True)

	print(f"  Facts shape: {facts.shape}")
	print(f"  Products shape: {products.shape}")
	print(f"  Periods shape: {periods.shape}")
	print(f"  Markets shape: {markets.shape}")

	# Join facts × product × period × market
	df = facts.merge(products[["product_id", "brand"]], on="product_id")
	df = df.merge(periods[["period_id", "period_year", "period_month"]], on="period_id")
	df = df.merge(markets[["market_id", "market_description"]], on="market_id")

	# Filter to DVH EXCL. HD — Nielsen's standard Danish grocery scope.
	# Excludes hierarchical aggregate rows (totals, groups) that would double-count sales.
	df = df[df["market_description"] == TARGET_MARKET].copy()

	# Filter to positive sales (non-zero units)
	df = df[df["sales_units"] > 0].copy()

	# Aggregate by brand Ã— period
	# Note: Not all Nielsen categories have promo columns; build agg_dict dynamically
	agg_dict = {
		"sales_units": "sum",
		"sales_value": "sum",
		"sales_in_liters": "sum",
		"weighted_distribution": "mean",
	}

	# Add promo column if it exists in data
	if "sales_units_any_promo" in df.columns:
		agg_dict["sales_units_any_promo"] = lambda x: sum(pd.Series(x).fillna(0))

	aggregated = df.groupby(["brand", "period_year", "period_month"]).agg(agg_dict).reset_index()

	# Rename columns consistently
	col_mapping = {
		"sales_units": "sales_units",
		"sales_value": "sales_value",
		"sales_in_liters": "sales_liters",
		"weighted_distribution": "weighted_dist",
	}
	if "sales_units_any_promo" in aggregated.columns:
		col_mapping["sales_units_any_promo"] = "promo_units"
	else:
		# No promo data available; fill with zeros
		aggregated["promo_units"] = 0

	aggregated = aggregated.rename(columns=col_mapping)
	aggregated = aggregated[["brand", "period_year", "period_month", "sales_units", "sales_value",
							 "sales_liters", "promo_units", "weighted_dist"]]

	return aggregated


def main():
	"""Execute step 1: Load and aggregate."""
	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		step_start = time.perf_counter()

		# Validate input
		if not INPUT_VIEWS_DIR.exists():
			raise FileNotFoundError(f"Input not found: {INPUT_VIEWS_DIR}")

		# Load
		print("\nLoading view files...")
		load_start = time.perf_counter()
		df = load_and_aggregate(INPUT_VIEWS_DIR, TARGET_MARKET, CACHED_PARQUET_VIEWS_DIR)
		load_elapsed = time.perf_counter() - load_start

		input_shape = df.shape
		print_file_load(INPUT_VIEWS_DIR, input_shape, load_elapsed)
		print_info(f"Target market: {TARGET_MARKET}")
		print_info(f"Unique brands: {df['brand'].nunique()}")
		if len(df) > 0:
			month_min = int(df['period_month'].min())
			month_max = int(df['period_month'].max())
			print_info(f"Date range: {df['period_year'].min()}-{month_min:02d} to {df['period_year'].max()}-{month_max:02d}")
		else:
			print_info(f"Date range: (no data)")

		# Save
		print(f"\nSaving aggregated data...")
		STEP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

		save_start = time.perf_counter()
		df.to_parquet(OUTPUT_AGGREGATE_PARQUET, index=False)
		save_elapsed = time.perf_counter() - save_start

		output_shape = df.shape
		print_file_save(OUTPUT_AGGREGATE_PARQUET, output_shape, save_elapsed)

		# Preview
		print("\nData preview:")
		print_data_preview(df, title=f"{CATEGORY} Aggregated Data", max_rows=10)

		# Summary
		step_elapsed = time.perf_counter() - step_start
		log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, output_shape[0], LOG_FILE,
					   input_cols=None, output_cols=output_shape[1])

		print_step_summary(
			STEP_NUM, STEP_NAME, step_elapsed,
			input_rows=input_shape[0],
			output_rows=output_shape[0],
			input_cols=None,  # Views are aggregated; no direct input cols tracked
			output_cols=output_shape[1],
			output_file=OUTPUT_AGGREGATE_PARQUET
		)


if __name__ == "__main__":
	main()

