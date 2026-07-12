#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Step 1b: Rollup to Brand x Month

PURPOSE
=======
Step 1 aggregates to brand x region x period (9 mutually exclusive DVH EXCL. HD
regions) for the region-grain capability described in P0026. As of 2026-07-12,
the thesis's active SRQ1 scope was locked to brand x month only (region/chain
grain deferred to future work -- see plans/P0027 Phase 4b). This step rolls
Step 1's region-grain output back up to brand x month so Steps 2-6 can run on
the actual production/thesis grain without needing region-aware logic.

INPUT
=====
Step 1 output (step_1_aggregate.parquet): brand x market_id x period

OUTPUT
======
Step 1b output (step_1b_brand_month.parquet): brand x period
  - sales_units, sales_value, sales_liters, promo_units: summed across regions
  - weighted_dist: re-averaged across regions (ACV metric, not additive)

LOGIC
=====
  - Sum additive measures (sales_units, sales_value, sales_liters, promo_units)
    across all regions for each (brand, period_year, period_month)
  - Re-average weighted_dist across regions (mean of means is an approximation;
    exact would require weighting by store count per region, not available here)
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

from PATHS import get_category_pipeline_step_outputs_dir
from terminal_utils import (
	step_execution, print_file_load, print_file_save, print_data_preview,
	print_step_summary, print_info
)
from timing_utils import log_step_timing

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "CSD"
STEP_NUM = "1b"
STEP_NAME = "Rollup to Brand x Month"

STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
INPUT_AGGREGATE_PARQUET = STEP_OUTPUT_DIR / "step_1_aggregate.parquet"
OUTPUT_BRAND_MONTH_PARQUET = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_brand_month.parquet"
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"

# ============================================================================
# STEP LOGIC
# ============================================================================

def rollup_to_brand_month(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Collapse brand x region x period rows to brand x period.

	Args:
		df: DataFrame with brand, market_id, period_year, period_month,
			sales_units, sales_value, sales_liters, promo_units, weighted_dist

	Returns:
		DataFrame with brand, period_year, period_month and the same measure
		columns, summed (additive measures) or re-averaged (weighted_dist)
		across regions.
	"""
	rolled = (
		df.groupby(["brand", "period_year", "period_month"])
		.agg(
			sales_units=("sales_units", "sum"),
			sales_value=("sales_value", "sum"),
			sales_liters=("sales_liters", "sum"),
			promo_units=("promo_units", "sum"),
			weighted_dist=("weighted_dist", "mean"),
		)
		.reset_index()
	)
	return rolled


def main():
	"""Execute step 1b: Rollup to brand x month."""
	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		step_start = time.perf_counter()

		if not INPUT_AGGREGATE_PARQUET.exists():
			raise FileNotFoundError(f"Input missing: {INPUT_AGGREGATE_PARQUET}")

		print("Loading brand x region aggregate from step 1...")
		load_start = time.perf_counter()
		df = pd.read_parquet(INPUT_AGGREGATE_PARQUET)
		load_elapsed = time.perf_counter() - load_start

		input_shape = df.shape
		print_file_load(INPUT_AGGREGATE_PARQUET, input_shape, load_elapsed)

		print_info(f"Brands: {df['brand'].nunique()}")
		print_info(f"Regions: {df['market_id'].nunique()}")
		print_info(f"Input series (brand x region): {df.groupby(['brand', 'market_id']).ngroups}")

		print("\nRolling up to brand x month...")
		process_start = time.perf_counter()

		df_rolled = rollup_to_brand_month(df)

		process_elapsed = time.perf_counter() - process_start
		print(f"  Rollup applied in {process_elapsed:.2f}s")
		print_info(f"Output series (brand): {df_rolled['brand'].nunique()}")

		print("\nSaving brand x month data...")
		STEP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

		save_start = time.perf_counter()
		df_rolled.to_parquet(OUTPUT_BRAND_MONTH_PARQUET, index=False)
		save_elapsed = time.perf_counter() - save_start

		output_shape = df_rolled.shape
		print_file_save(OUTPUT_BRAND_MONTH_PARQUET, output_shape, save_elapsed)

		print("\nData preview:")
		print_data_preview(df_rolled, title=f"{CATEGORY} Brand x Month Rollup", max_rows=10)

		step_elapsed = time.perf_counter() - step_start
		log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, output_shape[0], LOG_FILE,
					   input_cols=input_shape[1], output_cols=output_shape[1])

		print_step_summary(
			STEP_NUM, STEP_NAME, step_elapsed,
			input_rows=input_shape[0],
			output_rows=output_shape[0],
			input_cols=input_shape[1],
			output_cols=output_shape[1],
			output_file=OUTPUT_BRAND_MONTH_PARQUET
		)


if __name__ == "__main__":
	main()
