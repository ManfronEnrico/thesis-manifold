#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Step 1: Load and Aggregate

PURPOSE
=======
Load all Nielsen CSD view parquet files (validated by Step 0), join them into a
complete merged dataset, and aggregate directly to the requested grain. This step
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
Step 1 output (step_1_aggregate_{grain}.parquet):
  - bymonth: aggregated to brand x period, columns:
    brand, period_year, period_month, sales_units, sales_value, sales_liters,
    promo_units, weighted_dist
  - bychain / byregion: not yet implemented (raises NotImplementedError)

GRAIN HISTORY
=============
  P0026 (2026-06-30) chose brand x region x period over brand x period for
  regional Prometheus queries. That grain is deferred (plans/P0027 Phase 4b) —
  SRQ1 scope is locked to brand x month only (2026-07-12). This step now
  aggregates natively to brand x month; the interim rollup bridge
  (pre_csd_1b_rollup_to_brand_month.py) is no longer needed and has been removed.

USAGE
=====
  python pre_csd_1_load_and_aggregate.py [--grain bymonth] [--grains bymonth,bychain]
"""

import argparse
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
# This step joins Facts x Product x Period x Market dimensions and aggregates
# to the requested grain. All four Nielsen view tables are merged to create a
# complete dataset before aggregation.
#
# FACTS TABLE (source columns):
#   - sales_units: Total sales out of store (consumer purchase units). Non-nullable.
#   - sales_value: Total sales value in DKK. Non-nullable.
#   - sales_in_liters: Total sales volume in liters. Non-nullable.
#   - sales_units_any_promo: Sales units with any promotion applied. Nullable; 0 = no data.
#   - weighted_distribution: ACV-weighted store reach (0-1 fraction). Nullable (~16.7%).
#     NOT additive across products.
#
# PRODUCT DIMENSION:
#   - brand: Brand name (5-level hierarchy: category -> manufacturer -> brand -> variant -> UPC).
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
#   - bymonth: aggregates to brand x period granularity, combining across all markets
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
# Retained for byregion's future implementation (Phase 4b, deferred).
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

# ----------------------------------------------------------------------------
# GRAIN_CONFIG — single source of truth for grain-specific settings across
# Steps 1-6. Only "bymonth" is implemented today (SRQ1 scope locked to brand x
# month, 2026-07-12, plans/P0027 Phase 4a-ii). "bychain"/"byregion" are stubbed
# so the CLI surface and downstream code exist, but will raise
# NotImplementedError until Phase 4b is picked up.
#
# min_periods for "bymonth" was re-derived (2026-07-12 continuation) directly
# from the leakage-fixed brand x month rollup (140 brands, 44 months,
# non-zero-sales-month counts), NOT copied from the CSD EDA notebook's original
# "40" — that number was computed on brand x region grain (step_1_aggregate.parquet,
# groupby('brand') pooling all 9 regions), which measures a different quantity
# than true brand x month non-zero-months. Re-running the identical
# high/medium/low quality-tier method (Cell 5 of pre_csd_1.5_eda.py) on the
# corrected brand x month data independently confirms 40 as the entry point
# into the "High" quality tier (>35 non-zero months out of 44 possible),
# retaining 58/140 brands (41.4%). Same value as before, but now for a
# data-driven reason instead of a grain-mismatched coincidence.
# ----------------------------------------------------------------------------
GRAIN_CONFIG = {
    "bymonth": {
        "group_keys": ["brand"],
        "min_periods": 40,
        "min_periods_rationale": (
            "58/140 brands (41.4%) have >=40 non-zero sales-months out of 44 "
            "possible, the entry point into the 'High' data-quality tier "
            "(>35 non-zero months) per CSD EDA's brand-stability-analysis method "
            "(pre_csd_1.5_eda.py Cell 5), re-run against true brand x month grain "
            "(leakage-fixed, 2026-07-12) rather than the brand x region grain the "
            "original EDA cell used."
        ),
    },
    "bychain": {
        "group_keys": ["brand", "chain_id"],
        "min_periods": None,  # not yet derived — Phase 4b, deferred
    },
    "byregion": {
        "group_keys": ["brand", "market_id"],
        "min_periods": None,  # not yet derived — Phase 4b, deferred
        "region_ids": DVH_REGION_IDS,
    },
}

DEFAULT_GRAIN = "bymonth"
IMPLEMENTED_GRAINS = {"bymonth"}

# Parquet cache location validated by Step 0
CACHE_VIEWS_DIR = THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / CATEGORY / "views"

# Output paths
STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"


def output_parquet_for_grain(grain: str) -> Path:
	return STEP_OUTPUT_DIR / f"step_{STEP_NUM}_aggregate_{grain}.parquet"


# ============================================================================
# STEP LOGIC
# ============================================================================

def _load_merged(parquet_dir: Path) -> pd.DataFrame:
	"""Load and merge the 4 Nielsen CSD view parquet files (grain-independent)."""
	print("  Loading view parquet files...")
	facts = pd.read_parquet(parquet_dir / "csd_clean_facts_v.parquet")
	products = pd.read_parquet(parquet_dir / "csd_clean_dim_product_v.parquet")
	periods = pd.read_parquet(parquet_dir / "csd_clean_dim_period_v.parquet")
	markets = pd.read_parquet(parquet_dir / "csd_clean_dim_market_v.parquet")

	print(f"  Facts shape: {facts.shape}")
	print(f"  Products shape: {products.shape}")
	print(f"  Periods shape: {periods.shape}")
	print(f"  Markets shape: {markets.shape}")

	df = facts.merge(products[["product_id", "brand"]], on="product_id")
	df = df.merge(periods[["period_id", "period_year", "period_month"]], on="period_id")
	df = df.merge(markets[["market_id", "market_description"]], on="market_id")

	# Filter to the 9 mutually exclusive geographic regions within DVH EXCL. HD.
	df = df[df["market_id"].isin(DVH_REGION_IDS)].copy()

	# Filter to positive sales only.
	df = df[df["sales_units"] > 0].copy()

	return df


def load_and_aggregate(parquet_dir: Path, grain: str) -> pd.DataFrame:
	"""
	Load Nielsen CSD parquet view files, merge, and aggregate to the requested grain.

	PARAMETERS
	----------
	parquet_dir : Path
		Directory containing all 4 Nielsen CSD view parquet files.
	grain : str
		One of GRAIN_CONFIG's keys. Only "bymonth" is implemented; other grains
		raise NotImplementedError.

	RETURNS
	-------
	pd.DataFrame
		bymonth: brand x period_year x period_month aggregation with columns
		brand, period_year, period_month, sales_units, sales_value, sales_liters,
		promo_units, weighted_dist.
	"""
	if grain not in GRAIN_CONFIG:
		raise ValueError(f"Unknown grain '{grain}'. Valid grains: {list(GRAIN_CONFIG)}")
	if grain not in IMPLEMENTED_GRAINS:
		raise NotImplementedError(
			f"Grain '{grain}' is not yet implemented for Step 1 aggregation. "
			f"See plans/P0027 Phase 4b (deferred, region/chain grains)."
		)

	df = _load_merged(parquet_dir)

	agg_dict = {
		"sales_units": "sum",
		"sales_value": "sum",
		"sales_in_liters": "sum",
		"sales_units_any_promo": lambda x: sum(pd.Series(x).fillna(0)),
		"weighted_distribution": "mean",
	}

	if grain == "bymonth":
		aggregated = (
			df.groupby(["brand", "period_year", "period_month"])
			.agg(agg_dict)
			.reset_index()
		)
		aggregated.columns = [
			"brand", "period_year", "period_month",
			"sales_units", "sales_value", "sales_liters", "promo_units", "weighted_dist",
		]

	return aggregated


def main():
	"""
	Execute Step 1: Load, merge, and aggregate Nielsen CSD data to the requested grain(s).

	FLOW
	----
	1. Parse --grain/--grains
	2. Call Step 0 to validate parquet cache exists
	3. Load all 4 view parquet files
	4. Join them into a complete merged dataset
	5. Filter to positive sales
	6. Aggregate to each requested grain
	7. Save aggregated output(s)
	8. Log timing and row counts
	"""
	parser = argparse.ArgumentParser(description="CSD Step 1: Load and Aggregate")
	parser.add_argument("--grain", type=str, default=None, help=f"Single grain (default: {DEFAULT_GRAIN})")
	parser.add_argument("--grains", type=str, default=None, help="Comma-separated list of grains")
	args = parser.parse_args()

	if args.grains:
		grains = [g.strip() for g in args.grains.split(",") if g.strip()]
	elif args.grain:
		grains = [args.grain]
	else:
		grains = [DEFAULT_GRAIN]

	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		step_start = time.perf_counter()

		print("\nValidating parquet cache (Step 0)...")
		validation = validate_parquet_cache(CATEGORY, CACHE_VIEWS_DIR)

		if not validation["valid"]:
			print_info("Step 0 validation failed. Parquet cache is missing.")
			print_info("Aborting Step 1 — run Step 0 first to validate cache.")
			return

		print_info(validation["message"])

		for grain in grains:
			print(f"\n{'=' * 60}")
			print(f"Grain: {grain}")
			print(f"{'=' * 60}")

			print("\nLoading, merging, and aggregating view files...")
			load_start = time.perf_counter()
			df = load_and_aggregate(CACHE_VIEWS_DIR, grain)
			load_elapsed = time.perf_counter() - load_start

			input_shape = df.shape
			print_file_load(CACHE_VIEWS_DIR, input_shape, load_elapsed)
			print_info(f"Unique brands: {df['brand'].nunique()}")
			if len(df) > 0:
				df_sorted = df.sort_values(["period_year", "period_month"])
				first, last = df_sorted.iloc[0], df_sorted.iloc[-1]
				print_info(f"Date range: {int(first.period_year)}-{int(first.period_month):02d} to {int(last.period_year)}-{int(last.period_month):02d}")
			else:
				print_info(f"Date range: (no data)")

			print(f"\nSaving aggregated data ({grain})...")
			STEP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

			output_parquet = output_parquet_for_grain(grain)
			save_start = time.perf_counter()
			df.to_parquet(output_parquet, index=False)
			save_elapsed = time.perf_counter() - save_start

			output_shape = df.shape
			print_file_save(output_parquet, output_shape, save_elapsed)

			print("\nData preview:")
			print_data_preview(df, title=f"{CATEGORY} Aggregated Data ({grain})", max_rows=10)

			step_elapsed = time.perf_counter() - step_start
			log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, output_shape[0], LOG_FILE,
						   input_cols=None, output_cols=output_shape[1])

			print_step_summary(
				STEP_NUM, STEP_NAME, step_elapsed,
				input_rows=input_shape[0],
				output_rows=output_shape[0],
				input_cols=None,
				output_cols=output_shape[1],
				output_file=output_parquet
			)


if __name__ == "__main__":
	main()
