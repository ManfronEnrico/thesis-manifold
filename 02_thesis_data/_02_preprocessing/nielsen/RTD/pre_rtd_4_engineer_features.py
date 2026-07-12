#!/usr/bin/env python3
"""
Nielsen RTD Preprocessing â€” Step 4: Engineer Features

Input:  Step 3 output (filtered_series.parquet)
		- Calendar-filled, filtered brand Ã— month data

Output: Step 4 output (engineered_features.parquet)
		- Same data plus engineered features:
		  - Lags: lag_1, lag_2, lag_3, lag_4, lag_8, lag_13
		  - Rolling: rolling_mean_4, rolling_mean_13, rolling_std_4
		  - Calendar: month, quarter, holiday_month (1,4,6,10,12)
		  - Transformation: log_sales_units

Logic:
  - Import engineer_features() from shared codebase
  - Apply RTD-specific feature engineering (lags, rolling windows, holidays, promo)
  - Add log transformation of sales_units
"""

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

from PATHS import THESIS_DATA_PREPROCESSING_DIR, get_category_pipeline_step_outputs_dir
from utility_scripts.scripts.METADATA import describe_column
from thesis.thesis_agents.ai_research_framework.features.engineer_features import (
	engineer_features as shared_engineer_features
)
from thesis.data._02_preprocessing.nielsen.shared.terminal_utils import (
	step_execution, print_file_load, print_file_save, print_data_preview,
	print_step_summary, print_info
)
from thesis.data._02_preprocessing.nielsen.shared.timing_utils import log_step_timing

# ============================================================================
# METADATA DEFINITIONS
# ============================================================================
# This step engineers time-series features from RTD sales data via shared function.
# Key column transformations:
#
# INPUT (from step 3):
#   - sales_units: Non-nullable in observed periods; NaN in missing periods.
#     Will use log transformation; NaN preserved during lag/rolling operations.
#
# FEATURES ENGINEERED (via shared_engineer_features):
#   - Lags: lag_1, lag_2, lag_3, lag_4, lag_8, lag_13 (1, 2, 3, 4, 8, 13 months back)
#   - Rolling: rolling_mean_4, rolling_mean_13, rolling_std_4 (4-month and 13-month windows)
#   - Calendar: month (1â€“12), quarter (1â€“4), holiday_month (binary: 1/4/6/10/12)
#   - Transformation: log_sales_units = ln(sales_units) for positive values; NaN for non-positive
#
# NaN HANDLING:
#   - Lags/rolling: NaN propagates where source is NaN (no forward-fill; preserves gaps)
#   - Log transform: NaN for sales_units â‰¤ 0 or missing (safe: ln(NaN) = NaN)
#   - Do NOT fill lags with 0; missing lags = missing data (required for proper time-series modeling)
#
# OUTPUT (this step):
#   - Lags, rolling averages, calendar features added
#   - log_sales_units added (transformation of sales_units)
#   - NaN pattern preserved for downstream modeling (do NOT impute in earlier steps)

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "RTD"
STEP_NUM = 4
STEP_NAME = "Engineer Features"

# RTD-specific feature engineering parameters
RTD_LAG_WINDOWS = [1, 2, 3, 4, 8, 13]
RTD_ROLLING_WINDOWS = [4, 13]
RTD_HOLIDAY_MONTHS = {1, 4, 6, 10, 12}  # Jan, Apr, Jun, Oct, Dec
RTD_PROMO_CLIPPING = 1.0  # Clip promo intensity to [0, 1]

# Input/Output paths
STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
INPUT_FILTERED_SERIES_PARQUET = STEP_OUTPUT_DIR / f"step_3_filtered_series.parquet"
OUTPUT_ENGINEERED_FEATURES_PARQUET = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_engineered_features.parquet"
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"

# ============================================================================
# STEP LOGIC
# ============================================================================

def engineer_RTD_features(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Engineer RTD-specific features.

	Uses shared engineer_features() function from codebase.
	Applies RTD-specific lags, rolling windows, and holiday definitions.

	Args:
		df: DataFrame with brand, period_year, period_month, sales_units columns

	Returns:
		DataFrame with engineered features added
	"""
	# Create date column from period_year and period_month for shared function
	df["date"] = pd.to_datetime(
		df["period_year"].astype(str) + "-" + df["period_month"].astype(str).str.zfill(2),
		format="%Y-%m"
	)

	# Call shared feature engineering (uses DEFAULT_ constants from codebase)
	df = shared_engineer_features(df)

	# Add log transformation
	df["log_sales_units"] = df["sales_units"].apply(lambda x: float('nan') if pd.isna(x) else float(x)).apply(
		lambda x: float('nan') if x <= 0 else np.log(x)
	)

	return df


def main():
	"""Execute step 4: Engineer features."""
	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		step_start = time.perf_counter()

		# Validate input
		if not INPUT_FILTERED_SERIES_PARQUET.exists():
			raise FileNotFoundError(f"Input missing: {INPUT_FILTERED_SERIES_PARQUET}")

		# Load
		print("Loading filtered series from step 3...")
		load_start = time.perf_counter()
		df = pd.read_parquet(INPUT_FILTERED_SERIES_PARQUET)
		load_elapsed = time.perf_counter() - load_start

		input_shape = df.shape
		print_file_load(INPUT_FILTERED_SERIES_PARQUET, input_shape, load_elapsed)

		# Process
		print(f"\nEngineering features for {CATEGORY}...")
		print_info(f"Lag windows: {RTD_LAG_WINDOWS}")
		print_info(f"Rolling windows: {RTD_ROLLING_WINDOWS}")
		print_info(f"Holiday months: {RTD_HOLIDAY_MONTHS}")

		process_start = time.perf_counter()

		df = engineer_RTD_features(df)

		process_elapsed = time.perf_counter() - process_start
		print(f"  âœ“ Feature engineering complete in {process_elapsed:.2f}s")
		print_info(f"Output columns: {df.shape[1]}")

		# Save
		print(f"\nSaving engineered features...")
		STEP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

		save_start = time.perf_counter()
		df.to_parquet(OUTPUT_ENGINEERED_FEATURES_PARQUET, index=False)
		save_elapsed = time.perf_counter() - save_start

		output_shape = df.shape
		print_file_save(OUTPUT_ENGINEERED_FEATURES_PARQUET, output_shape, save_elapsed)

		# Preview
		print("\nData preview (selected columns):")
		cols_to_show = ["brand", "period_year", "period_month", "sales_units", "log_sales_units",
					   "lag_1", "rolling_mean_4", "month", "holiday_month"]
		cols_available = [c for c in cols_to_show if c in df.columns]
		df_preview = df[cols_available].head(10)
		print_data_preview(df_preview, title=f"{CATEGORY} Engineered Features", max_rows=10)

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
			output_file=OUTPUT_ENGINEERED_FEATURES_PARQUET
		)


if __name__ == "__main__":
	main()

