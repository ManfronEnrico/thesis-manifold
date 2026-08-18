#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Step 3: Filter Series

Input:  Step 2 output (calendar_filled_{grain}.parquet)
		- Calendar-filled brand × month data with NaN for missing periods

Output: Step 3 output (filtered_series_{grain}.parquet)
		- Same data but only series with >= min_periods non-zero periods retained
		- Removes series with sparse data (not enough historical observations)

Logic:
  - Count non-NaN sales_units per group_keys (e.g. brand, for bymonth grain)
  - Keep only groups with count >= GRAIN_CONFIG[grain]["min_periods"]
  - Drop other groups entirely

CATEGORY-SPECIFIC NOTES (CSD EDA):
  - bymonth MIN_PERIODS = 40, re-derived 2026-07-12 directly from the leakage-fixed
    brand x month data (see GRAIN_CONFIG rationale in pre_csd_1_load_and_aggregate.py) —
    NOT the original EDA notebook's "40", which was computed on brand x region grain
    and measures a different quantity.

USAGE
=====
  python pre_csd_3_filter_series.py [--grain bymonth] [--grains bymonth,bychain]
"""

import argparse
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
from engineer_features import filter_series as shared_filter_series
from terminal_utils import (
	step_execution, print_file_load, print_file_save, print_data_preview,
	print_step_summary, print_info
)
from timing_utils import log_step_timing

# Import GRAIN_CONFIG from Step 1
sys.path.insert(0, str(Path(__file__).parent))
from pre_csd_1_load_and_aggregate import GRAIN_CONFIG, DEFAULT_GRAIN, IMPLEMENTED_GRAINS

# ============================================================================
# METADATA DEFINITIONS
# ============================================================================
# This step filters calendar-filled data by minimum non-zero periods per series.
# Key filtering logic:
#
#   - Counts non-NaN sales_units per group_keys combination
#   - Drops groups with fewer than min_periods historical observations
#   - Rationale: Sparse series insufficient for reliable time-series modeling
#
#   - NaN semantics preserved: Non-NaN count only includes observed data points
#   - Weighted_distribution not used for filtering (nullable column, ~16.7% missing)
#
# OUTPUT (this step):
#   - Reduced series set (high-frequency series only)
#   - All other columns unchanged; NaN pattern preserved from step 2

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "CSD"
STEP_NUM = 3
STEP_NAME = "Filter Series"

STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"


def input_parquet_for_grain(grain: str) -> Path:
	return STEP_OUTPUT_DIR / f"step_2_calendar_filled_{grain}.parquet"


def output_parquet_for_grain(grain: str) -> Path:
	return STEP_OUTPUT_DIR / f"step_{STEP_NUM}_filtered_series_{grain}.parquet"

# ============================================================================
# STEP LOGIC
# ============================================================================

def run_step(grain: str):
	"""Execute step 3 for a single grain."""
	if grain not in IMPLEMENTED_GRAINS:
		raise NotImplementedError(
			f"Grain '{grain}' is not yet implemented. See plans/P0027 Phase 4b (deferred)."
		)

	grain_cfg = GRAIN_CONFIG[grain]
	group_keys = grain_cfg["group_keys"]
	min_periods = grain_cfg["min_periods"]
	if min_periods is None:
		raise ValueError(
			f"GRAIN_CONFIG['{grain}']['min_periods'] is not yet derived. "
			f"Cannot filter series without a data-driven threshold."
		)

	input_parquet = input_parquet_for_grain(grain)
	output_parquet = output_parquet_for_grain(grain)

	step_start = time.perf_counter()

	if not input_parquet.exists():
		raise FileNotFoundError(f"Input missing: {input_parquet}")

	print(f"Loading calendar-filled data for grain='{grain}' from step 2...")
	load_start = time.perf_counter()
	df = pd.read_parquet(input_parquet)
	load_elapsed = time.perf_counter() - load_start

	input_shape = df.shape
	print_file_load(input_parquet, input_shape, load_elapsed)

	series_before = df[group_keys].drop_duplicates().shape[0]
	print_info(f"Series before filter: {series_before}")

	print(f"\nFiltering series with < {min_periods} non-zero periods...")
	process_start = time.perf_counter()

	df = shared_filter_series(df, min_periods=min_periods, group_keys=group_keys)

	process_elapsed = time.perf_counter() - process_start
	series_after = df[group_keys].drop_duplicates().shape[0]
	series_removed = series_before - series_after

	print(f"  ✓ Filter applied in {process_elapsed:.2f}s")
	print_info(f"Series after filter: {series_after} (removed {series_removed})")

	print(f"\nSaving filtered series data ({grain})...")
	STEP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

	save_start = time.perf_counter()
	df.to_parquet(output_parquet, index=False)
	save_elapsed = time.perf_counter() - save_start

	output_shape = df.shape
	print_file_save(output_parquet, output_shape, save_elapsed)

	print("\nData preview:")
	print_data_preview(df, title=f"{CATEGORY} Filtered Series ({grain})", max_rows=10)

	step_elapsed = time.perf_counter() - step_start
	log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, output_shape[0], LOG_FILE,
				   input_cols=input_shape[1], output_cols=output_shape[1])

	print_step_summary(
		STEP_NUM, STEP_NAME, step_elapsed,
		input_rows=input_shape[0],
		output_rows=output_shape[0],
		input_cols=input_shape[1],
		output_cols=output_shape[1],
		output_file=output_parquet
	)


def main():
	"""Execute step 3: Filter series."""
	parser = argparse.ArgumentParser(description="CSD Step 3: Filter Series")
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
		for grain in grains:
			print(f"\n{'=' * 60}")
			print(f"Grain: {grain}")
			print(f"{'=' * 60}")
			run_step(grain)


if __name__ == "__main__":
	main()
