#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Step 3: Filter Series

Input:  Step 2 output (calendar_filled.parquet)
		- Calendar-filled brand × month data with NaN for missing periods

Output: Step 3 output (filtered_series.parquet)
		- Same data but only brands with ≥ min_periods non-zero periods retained
		- Removes brands with sparse data (not enough historical observations)

Logic:
  - Count non-NaN sales_units per brand
  - Keep only brands with count >= min_periods (default 40 for thesis quality focus)
  - Drop other brands entirely

CATEGORY-SPECIFIC NOTES (CSD EDA):
  - MIN_PERIODS = 40 selected via brand stability analysis
  - Result: 62 brands retained (43.4% of 143 total)
  - Rationale: Thesis proof-of-concept with high-quality data (40+ periods each)
  - vs production approach: 84 brands (58.7%) with ≥30 periods
  - Downstream impact: Feature engineering and forecasting on clean dataset
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

from PATHS import THESIS_DATA_PREPROCESSING_DIR, get_category_pipeline_step_outputs_dir
from utility_scripts.scripts.METADATA import describe_column
from terminal_utils import (
	step_execution, print_file_load, print_file_save, print_data_preview,
	print_step_summary, print_info
)
from timing_utils import log_step_timing

# ============================================================================
# METADATA DEFINITIONS
# ============================================================================
# This step filters calendar-filled data by minimum periods per brand.
# Key filtering logic:
#
#   - Counts non-NaN sales_units per brand (observations where sales were recorded)
#   - Drops brands with fewer than min_periods historical observations
#   - Rationale: Sparse series (< 30 months) insufficient for reliable time-series modeling
#
#   - NaN semantics preserved: Non-NaN count only includes observed data points
#   - Weighted_distribution not used for filtering (nullable column, ~16.7% missing)
#
# OUTPUT (this step):
#   - Reduced brand set (high-frequency series only)
#   - All other columns unchanged; NaN pattern preserved from step 2

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "CSD"
STEP_NUM = 3
STEP_NAME = "Filter Series"

# Minimum non-zero periods per brand×region series.
# 24 = 2 full years — captures seasonality twice, empirically defensible for ML.
# (Previous value was 40 at brand×period grain; now operating at brand×region grain
# where series are naturally sparser — 24 is the appropriate floor.)
DEFAULT_MIN_PERIODS = 24

# Input/Output paths
STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
INPUT_CALENDAR_FILLED_PARQUET = STEP_OUTPUT_DIR / f"step_2_calendar_filled.parquet"
OUTPUT_FILTERED_SERIES_PARQUET = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_filtered_series.parquet"
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"

# ============================================================================
# STEP LOGIC
# ============================================================================

def filter_series(df: pd.DataFrame, min_periods: int) -> pd.DataFrame:
	"""
	Filter brands with insufficient historical data.

	Keeps only brands with >= min_periods non-NaN sales_units observations.

	Args:
		df: DataFrame with brand, period columns and sales data
		min_periods: Minimum number of non-NaN sales_units per brand

	Returns:
		DataFrame with only brands meeting the threshold
	"""
	# Count non-NaN sales_units per brand × region series
	series_counts = df[df["sales_units"].notna()].groupby(["brand", "market_id"]).size()

	# Keep only series with sufficient observations
	valid_series = series_counts[series_counts >= min_periods].index

	# Filter to keep only valid brand × region combinations
	df_filtered = df.set_index(["brand", "market_id"])
	df_filtered = df_filtered[df_filtered.index.isin(valid_series)].reset_index()

	return df_filtered


def main():
	"""Execute step 3: Filter series."""
	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		step_start = time.perf_counter()

		# Validate input
		if not INPUT_CALENDAR_FILLED_PARQUET.exists():
			raise FileNotFoundError(f"Input missing: {INPUT_CALENDAR_FILLED_PARQUET}")

		# Load
		print("Loading calendar-filled data from step 2...")
		load_start = time.perf_counter()
		df = pd.read_parquet(INPUT_CALENDAR_FILLED_PARQUET)
		load_elapsed = time.perf_counter() - load_start

		input_shape = df.shape
		print_file_load(INPUT_CALENDAR_FILLED_PARQUET, input_shape, load_elapsed)

		brands_before = df["brand"].nunique()
		series_before = df.groupby(["brand", "market_id"]).ngroups if "market_id" in df.columns else brands_before
		print_info(f"Brands before filter: {brands_before}")
		print_info(f"Series (brand×region) before filter: {series_before}")

		# Process
		print(f"\nFiltering series with < {DEFAULT_MIN_PERIODS} non-zero periods...")
		process_start = time.perf_counter()

		df = filter_series(df, DEFAULT_MIN_PERIODS)

		process_elapsed = time.perf_counter() - process_start
		brands_after = df["brand"].nunique()
		series_after = df.groupby(["brand", "market_id"]).ngroups if "market_id" in df.columns else brands_after
		series_removed = series_before - series_after

		print(f"  ✓ Filter applied in {process_elapsed:.2f}s")
		print_info(f"Brands after filter: {brands_after}")
		print_info(f"Series (brand×region) after filter: {series_after} (removed {series_removed})")

		# Save
		print(f"\nSaving filtered series data...")
		STEP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

		save_start = time.perf_counter()
		df.to_parquet(OUTPUT_FILTERED_SERIES_PARQUET, index=False)
		save_elapsed = time.perf_counter() - save_start

		output_shape = df.shape
		print_file_save(OUTPUT_FILTERED_SERIES_PARQUET, output_shape, save_elapsed)

		# Preview
		print("\nData preview:")
		print_data_preview(df, title=f"{CATEGORY} Filtered Series", max_rows=10)

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
			output_file=OUTPUT_FILTERED_SERIES_PARQUET
		)


if __name__ == "__main__":
	main()
