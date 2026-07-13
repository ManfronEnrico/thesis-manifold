#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Step 4: Engineer Features

Input:  Step 3 output (filtered_series_{grain}.parquet)
		- Calendar-filled, filtered brand × month data

Output: Step 4 output (engineered_features_{grain}.parquet)
		- Same data plus engineered features:
		  - Lags: lag_1, lag_2, lag_3, lag_4, lag_8, lag_13
		  - Rolling: rolling_mean_4, rolling_mean_13, rolling_std_4
		  - Calendar: month, quarter, holiday_month (3, 6, 12)
		  - Transformation: log_sales_units

Logic:
  - Import engineer_features() from shared codebase
  - Apply CSD-specific feature engineering (lags, rolling windows, holidays, promo)
  - Add log transformation of sales_units

USAGE
=====
  python pre_csd_4_engineer_features.py [--grain bymonth] [--grains bymonth,bychain]
"""

import argparse
import sys, time
from pathlib import Path
import pandas as pd
import numpy as np

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
from engineer_features import engineer_features as shared_engineer_features
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
# This step engineers time-series features from CSD sales data via shared function.
# Key column transformations:
#
# INPUT (from step 3):
#   - sales_units: Non-nullable in observed periods; NaN in missing periods.
#     Will use log transformation; NaN preserved during lag/rolling operations.
#
# FEATURES ENGINEERED (via shared_engineer_features):
#   - Lags: lag_1, lag_2, lag_3, lag_4, lag_8, lag_13 (1, 2, 3, 4, 8, 13 months back)
#   - Rolling: rolling_mean_4, rolling_mean_13, rolling_std_4 (4-month and 13-month windows)
#   - Calendar: month (1–12), quarter (1–4), holiday_month (binary: {3, 6, 12} for CSD)
#     NOTE: CSD holiday months empirically differ from colleague's default {1, 4, 6, 10, 12}
#     CSD peaks: March (10.7%, Easter), June (8.8%, Summer), December (12.2%, Holidays)
#   - Transformation: log_sales_units = ln(sales_units) for positive values; NaN for non-positive
#
# NaN HANDLING:
#   - Lags/rolling: NaN propagates where source is NaN (no forward-fill; preserves gaps)
#   - Log transform: NaN for sales_units ≤ 0 or missing (safe: ln(NaN) = NaN)
#   - Do NOT fill lags with 0; missing lags = missing data (required for proper time-series modeling)
#
# OUTPUT (this step):
#   - Lags, rolling averages, calendar features added
#   - log_sales_units added (transformation of sales_units)
#   - NaN pattern preserved for downstream modeling (do NOT impute in earlier steps)

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "CSD"
STEP_NUM = 4
STEP_NAME = "Engineer Features"

# CSD-specific feature engineering parameters (from CSD EDA analysis) — apply
# to all grains; only group_keys (from GRAIN_CONFIG) varies by grain.
CSD_LAG_WINDOWS = [1, 2, 3, 4, 8, 13]           # Cell 5: Weekly to yearly dependencies
CSD_ROLLING_WINDOWS = [4, 13]                    # Cell 6: Nielsen calendar + quarterly
CSD_HOLIDAY_MONTHS = {3, 6, 12}                  # Cell 4: March (Easter), June (Summer), Dec (Holidays)
                                                  # ⚠️ NOTE: Different from default {1, 4, 6, 10, 12}
CSD_PROMO_CLIPPING = 1.0  # Clip promo intensity to [0, 1]

STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"


def input_parquet_for_grain(grain: str) -> Path:
	return STEP_OUTPUT_DIR / f"step_3_filtered_series_{grain}.parquet"


def output_parquet_for_grain(grain: str) -> Path:
	return STEP_OUTPUT_DIR / f"step_{STEP_NUM}_engineered_features_{grain}.parquet"

# ============================================================================
# STEP LOGIC
# ============================================================================

def engineer_csd_features(df: pd.DataFrame, group_keys: list) -> pd.DataFrame:
	"""
	Engineer CSD-specific features with empirically-justified parameters.

	Uses shared engineer_features() function from codebase.
	Applies CSD-specific lags, rolling windows, and holiday definitions from EDA analysis.

	Args:
		df: DataFrame with group_keys, period_year, period_month, sales_units columns
		group_keys: Series-identifying columns for this grain (see GRAIN_CONFIG)

	Returns:
		DataFrame with engineered features added

	CATEGORY-SPECIFIC NOTES (CSD EDA):
		- LAGS: (1,2,3,4,8,13) from autocorrelation analysis (Cell 5)
		- ROLLING_WINDOWS: (4,13) aligned to Nielsen calendar & quarters (Cell 6)
		- HOLIDAY_MONTHS: {3,6,12} empirical peaks — March (Easter), June (Summer), Dec (Holidays)
		  ⚠️ Different from colleague's default {1,4,6,10,12}
		- Rationale: CSD shows March peak (10.7%), not April (8.4%)
	"""
	# Create date column from period_year and period_month for shared function
	df["date"] = pd.to_datetime(
		df["period_year"].astype(str) + "-" + df["period_month"].astype(str).str.zfill(2),
		format="%Y-%m"
	)

	# Call shared feature engineering with CSD-specific parameters
	df = shared_engineer_features(
		df,
		lags=CSD_LAG_WINDOWS,
		rolling_windows=CSD_ROLLING_WINDOWS,
		holiday_months=CSD_HOLIDAY_MONTHS,
		group_keys=group_keys,
	)

	# Add log transformation
	df["log_sales_units"] = df["sales_units"].apply(lambda x: float('nan') if pd.isna(x) else float(x)).apply(
		lambda x: float('nan') if x <= 0 else np.log(x)
	)

	return df


def run_step(grain: str):
	"""Execute step 4 for a single grain."""
	if grain not in IMPLEMENTED_GRAINS:
		raise NotImplementedError(
			f"Grain '{grain}' is not yet implemented. See plans/P0027 Phase 4b (deferred)."
		)

	group_keys = GRAIN_CONFIG[grain]["group_keys"]
	input_parquet = input_parquet_for_grain(grain)
	output_parquet = output_parquet_for_grain(grain)

	step_start = time.perf_counter()

	if not input_parquet.exists():
		raise FileNotFoundError(f"Input missing: {input_parquet}")

	print(f"Loading filtered series for grain='{grain}' from step 3...")
	load_start = time.perf_counter()
	df = pd.read_parquet(input_parquet)
	load_elapsed = time.perf_counter() - load_start

	input_shape = df.shape
	print_file_load(input_parquet, input_shape, load_elapsed)

	print(f"\nEngineering features for {CATEGORY} ({grain})...")
	print_info(f"Lag windows: {CSD_LAG_WINDOWS}")
	print_info(f"Rolling windows: {CSD_ROLLING_WINDOWS}")
	print_info(f"Holiday months: {CSD_HOLIDAY_MONTHS}")
	print_info(f"Group keys: {group_keys}")

	process_start = time.perf_counter()

	df = engineer_csd_features(df, group_keys)

	process_elapsed = time.perf_counter() - process_start
	print(f"  ✓ Feature engineering complete in {process_elapsed:.2f}s")
	print_info(f"Output columns: {df.shape[1]}")

	print(f"\nSaving engineered features ({grain})...")
	STEP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

	save_start = time.perf_counter()
	df.to_parquet(output_parquet, index=False)
	save_elapsed = time.perf_counter() - save_start

	output_shape = df.shape
	print_file_save(output_parquet, output_shape, save_elapsed)

	print("\nData preview (selected columns):")
	cols_to_show = group_keys + ["period_year", "period_month", "sales_units", "log_sales_units",
				   "lag_1", "rolling_mean_4", "month", "holiday_month"]
	cols_available = [c for c in cols_to_show if c in df.columns]
	df_preview = df[cols_available].head(10)
	print_data_preview(df_preview, title=f"{CATEGORY} Engineered Features ({grain})", max_rows=10)

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
	"""Execute step 4: Engineer features."""
	parser = argparse.ArgumentParser(description="CSD Step 4: Engineer Features")
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
