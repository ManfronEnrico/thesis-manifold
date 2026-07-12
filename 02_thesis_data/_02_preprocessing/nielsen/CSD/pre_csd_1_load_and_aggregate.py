#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Step 1: Load and Aggregate

PURPOSE
=======
Load all Nielsen CSD view parquet files (validated by Step 0), join them into a
complete merged dataset, and aggregate to brand × region × period granularity.
This step produces an intermediate aggregate table that feeds into Steps 2-6 for
calendar fill, series filtering, feature engineering, split application, and indexing.

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
  - Aggregated to brand × market_id × period granularity
  - Filtered to 9 DVH EXCL. HD geographic regions (REG. 1–9, mutually exclusive)
  - Columns: brand, market_id, market_description, period_year, period_month,
    sales_units, sales_value, sales_liters, promo_units, weighted_dist

GRAIN DECISION (P0026, 2026-06-30)
===================================
  brand × region × period chosen over brand × period because:
  - Enables regional predictive questions for Prometheus (e.g. "Forecast Faxe Kondi
    sales in Copenhagen next quarter")
  - 9 geographic regions are mutually exclusive → no double-counting
  - Brand-total forecast = sum of regional forecasts
  - 55% of brand×region series have ≥24 non-zero periods (viable for ML)
  - Size tiers excluded (overlap with regions → double-count); Phase 2 enhancement

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
sys.path.insert(0, str(ROOT_DIR_FINDER / "02_thesis_data" / "_02_preprocessing" / "nielsen" / "_shared_modules"))
from terminal_utils import (
	step_execution, print_file_load, print_file_save, print_data_preview,
	print_step_summary, print_info
)
from timing_utils import log_step_timing

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
#   - market_description: Retail outlet types. Filter to "DVH EXCL. HD" — Nielsen's
#     standard Danish grocery scope (supermarkets excl. hard discounters Aldi/Lidl).
#     Per Nielsen metadata: "Unless the user specifies a particular market, always use DVH EXCL. HD".
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

# 9 mutually exclusive geographic regions within DVH EXCL. HD scope.
# Excludes size tiers (Superettes/Small/Large/Hypermarkets) and rollups
# (EAST/WEST, national DVH EXCL. HD total) to prevent double-counting.
DVH_REGION_IDS = {
    1586000,  # DVH EXCL. HD - REG. 2 - KBH
    1585996,  # DVH EXCL. HD - REG. 1 - SJÆLLAND NORD
    1586002,  # DVH EXCL. HD - REG. 3 - SJÆLLAND SYD
    1647654,  # DVH EXCL. HD - REG. 4 - SJÆLLAND VEST
    1586001,  # DVH EXCL. HD - REG. 5 - FYN
    1585998,  # DVH EXCL. HD - REG. 6 - SYD JYLLAND
    1586003,  # DVH EXCL. HD - REG. 7 - ØST JYLLAND
    1585997,  # DVH EXCL. HD - REG. 8 - NORD JYLLAND
    1585999,  # DVH EXCL. HD - REG. 9 - VEST JYLLAND
}

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
		  - market_id: Region identifier (one of 9 DVH EXCL. HD geographic regions)
		  - market_description: Region name (e.g. "DVH EXCL. HD - REG. 2 - KBH")
		  - period_year: Year (from period dimension)
		  - period_month: Month (from period dimension)
		  - sales_units: Summed sales units within region
		  - sales_value: Summed sales value (DKK) within region
		  - sales_liters: Summed sales volume (liters) within region
		  - promo_units: Summed promotional units within region
		  - weighted_dist: Mean ACV-weighted distribution within region

	NOTES
	-----
	Aggregates to brand × region × period (not brand × period as previously).
	Regions are mutually exclusive geographic segments — summing across regions
	gives the correct national total without double-counting.
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

	# Join facts × product × period × market
	df = facts.merge(products[["product_id", "brand"]], on="product_id")
	df = df.merge(periods[["period_id", "period_year", "period_month"]], on="period_id")
	df = df.merge(markets[["market_id", "market_description"]], on="market_id")

	# Filter to the 9 mutually exclusive geographic regions within DVH EXCL. HD.
	df = df[df["market_id"].isin(DVH_REGION_IDS)].copy()

	# Filter to positive sales only.
	df = df[df["sales_units"] > 0].copy()

	# Aggregate by brand × region × period.
	agg_dict = {
		"sales_units": "sum",
		"sales_value": "sum",
		"sales_in_liters": "sum",
		"sales_units_any_promo": lambda x: sum(pd.Series(x).fillna(0)),
		"weighted_distribution": "mean",
	}

	aggregated = (
		df.groupby(["brand", "market_id", "market_description", "period_year", "period_month"])
		.agg(agg_dict)
		.reset_index()
	)
	aggregated.columns = [
		"brand", "market_id", "market_description", "period_year", "period_month",
		"sales_units", "sales_value", "sales_liters", "promo_units", "weighted_dist",
	]

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
		print_info(f"Unique regions: {df['market_id'].nunique()}")
		if len(df) > 0:
			df_sorted = df.sort_values(["period_year", "period_month"])
			first, last = df_sorted.iloc[0], df_sorted.iloc[-1]
			print_info(f"Date range: {int(first.period_year)}-{int(first.period_month):02d} to {int(last.period_year)}-{int(last.period_month):02d}")
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
