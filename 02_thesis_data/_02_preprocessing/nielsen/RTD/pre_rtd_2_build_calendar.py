#!/usr/bin/env python3
"""
Nielsen RTD Preprocessing â€” Step 2: Build Calendar

Input:  Step 1 output (aggregate.parquet)
		- Brand-period aggregation with sales units, value, etc.

Output: Step 2 output (calendar_filled.parquet)
		- Same data but with all months from 2022-10 to 2026-03 (gaps filled with NaN)
		- All brands Ã— all months in complete date range

Logic:
  - Create full date range (monthly granularity, 2022-10 to 2026-03)
  - Create complete brand Ã— month index
  - Reindex aggregated data to include all months (NaN for missing)
  - NaN indicates zero/missing sales for that brand-month
"""

import sys, time
from pathlib import Path
import pandas as pd
from datetime import datetime

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

from PATHS import THESIS_DATA_PREPROCESSING_DIR, get_category_pipeline_step_outputs_dir
from utility_scripts.scripts.METADATA import describe_column
from thesis.data._02_preprocessing.nielsen.shared.terminal_utils import (
	step_execution, print_file_load, print_file_save, print_data_preview,
	print_step_summary, print_info
)
from thesis.data._02_preprocessing.nielsen.shared.timing_utils import log_step_timing

# ============================================================================
# METADATA DEFINITIONS
# ============================================================================
# This step creates a complete brand Ã— month calendar (2022-10 to 2026-03) and reindexes aggregated data.
# Key null semantics:
#
#   - sales_units: NaN indicates zero sales OR missing observation (non-observable zero).
#     Important: Do NOT fill with 0. NaN preserves missing-ness for downstream analysis.
#
#   - sales_value, sales_in_liters: Same as sales_units. NaN = missing/not observed.
#
#   - promo_units: Filled with 0 during aggregation (no data = no promo). Safe to fill with 0.
#
#   - weighted_distribution: Nullable metric (~16.7% NULL in source). After reindex, will be
#     NaN for missing brand-months. Do NOT impute; leave as NaN (indicates no store data).
#
# OUTPUT (this step):
#   - All brand Ã— (2022-10 to 2026-03) combinations present in index
#   - Missing observations marked with NaN (sales_units, sales_value, sales_in_liters, weighted_dist)
#   - NaN preserved: Required downstream for distinguishing zero-sales from missing-data

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "RTD"
STEP_NUM = 2
STEP_NAME = "Build Calendar"

# Calendar bounds are derived from the data in main() — no hardcoded dates.

# Input/Output paths
STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
INPUT_AGGREGATE_PARQUET = STEP_OUTPUT_DIR / f"step_1_aggregate.parquet"
OUTPUT_CALENDAR_FILLED_PARQUET = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_calendar_filled.parquet"
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"

# ============================================================================
# STEP LOGIC
# ============================================================================

def build_calendar_index(df: pd.DataFrame, start_date: tuple, end_date: tuple) -> pd.DataFrame:
	"""
	Fill calendar gaps in aggregated data.

	Input: df with (brand, period_year, period_month, sales_units, ...)
	Output: df with all months from start_date to end_date, NaN for missing months

	Args:
		df: Aggregated data with brand, period_year, period_month columns
		start_date: Tuple (year, month) for calendar start
		end_date: Tuple (year, month) for calendar end

	Returns:
		DataFrame with all months filled, NaN for missing brand-month combinations
	"""
	# Create full date range
	months = pd.period_range(
		start=f"{start_date[0]}-{start_date[1]:02d}",
		end=f"{end_date[0]}-{end_date[1]:02d}",
		freq="M"
	)

	# Create full index (brand Ã— month)
	brands = df["brand"].unique()
	full_index = pd.MultiIndex.from_product(
		[brands, months],
		names=["brand", "period"]
	)

	# Convert period columns to period dtype for joining
	df["period"] = pd.PeriodIndex(
		df["period_year"].astype(str) + "-" + df["period_month"].astype(str).str.zfill(2),
		freq="M"
	)

	# Set index to brand, period for reindexing
	df_indexed = df.set_index(["brand", "period"])

	# Reindex to full calendar (NaN for missing periods)
	df_reindexed = df_indexed.reindex(full_index)

	# Reset index to get brand, period columns back
	df_filled = df_reindexed.reset_index()

	# Add year/month columns from period
	df_filled["period_year"] = df_filled["period"].dt.year
	df_filled["period_month"] = df_filled["period"].dt.month

	# Reorder columns to match original (minus period)
	cols = ["brand", "period_year", "period_month"] + [c for c in df_filled.columns
														if c not in ["brand", "period_year", "period_month", "period"]]
	df_filled = df_filled[cols]

	return df_filled


def main():
	"""Execute step 2: Build calendar."""
	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		step_start = time.perf_counter()

		# Validate input
		if not INPUT_AGGREGATE_PARQUET.exists():
			raise FileNotFoundError(f"Input missing: {INPUT_AGGREGATE_PARQUET}")

		# Load
		print("Loading aggregate data from step 1...")
		load_start = time.perf_counter()
		df = pd.read_parquet(INPUT_AGGREGATE_PARQUET)
		load_elapsed = time.perf_counter() - load_start

		input_shape = df.shape
		print_file_load(INPUT_AGGREGATE_PARQUET, input_shape, load_elapsed)

		if len(df) > 0:
			df_sorted = df.sort_values(["period_year", "period_month"])
			first = df_sorted.iloc[0]
			last = df_sorted.iloc[-1]
			cal_start = (int(first["period_year"]), int(first["period_month"]))
			cal_end = (int(last["period_year"]), int(last["period_month"]))
			print_info(f"Date range: {cal_start[0]}-{cal_start[1]:02d} to {cal_end[0]}-{cal_end[1]:02d}")
		else:
			print_info(f"Date range: (no data)")
			raise ValueError("No data in step 1 output — cannot build calendar.")
		print_info(f"Unique brands: {df['brand'].nunique()}")

		# Process
		print(f"\nBuilding calendar index ({cal_start[0]}-{cal_start[1]:02d} to {cal_end[0]}-{cal_end[1]:02d})...")
		process_start = time.perf_counter()

		df = build_calendar_index(df, cal_start, cal_end)

		process_elapsed = time.perf_counter() - process_start
		print(f"  âœ“ Calendar filled in {process_elapsed:.2f}s")

		# Save
		print(f"\nSaving calendar-filled data...")
		STEP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

		save_start = time.perf_counter()
		df.to_parquet(OUTPUT_CALENDAR_FILLED_PARQUET, index=False)
		save_elapsed = time.perf_counter() - save_start

		output_shape = df.shape
		print_file_save(OUTPUT_CALENDAR_FILLED_PARQUET, output_shape, save_elapsed)

		# Preview
		print("\nData preview:")
		print_data_preview(df, title=f"{CATEGORY} Calendar-Filled Data", max_rows=10)

		# Summary
		step_elapsed = time.perf_counter() - step_start
		log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, output_shape[0], LOG_FILE,
					   input_cols=input_shape[1], output_cols=output_shape[1])

		print_step_summary(
			STEP_NUM, STEP_NAME, step_elapsed,
			input_rows=input_shape[0],
			output_rows=output_shape[0],
			input_cols=input_shape[1],
			output_cols=output_shape[1],
			output_file=OUTPUT_CALENDAR_FILLED_PARQUET
		)


if __name__ == "__main__":
	main()

