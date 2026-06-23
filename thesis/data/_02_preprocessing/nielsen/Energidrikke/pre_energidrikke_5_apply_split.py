#!/usr/bin/env python3
"""
Nielsen Energidrikke Preprocessing — Step 5: Apply Split

Input:  Step 4 output (engineered_features.parquet)
		- Calendar-filled, filtered, feature-engineered brand × month data

Output: Step 5 output (split_applied.parquet)
		- Same data plus 'split' column (train, val, or test)
		- Split boundaries locked: train ≤ 2025-02, val 2025-03–2025-08, test ≥ 2025-09

Logic:
  - Import apply_split() from shared codebase
  - Apply locked train/val/test split dates
  - Add split column to DataFrame
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

from PATHS import THESIS_DATA_PREPROCESSING_DIR, get_category_pipeline_step_outputs_dir
from METADATA import describe_column
from thesis.thesis_agents.ai_research_framework.features.engineer_features import (
	apply_split as shared_apply_split,
	DEFAULT_TRAIN_END as TRAIN_END,
	DEFAULT_VAL_END as VAL_END,
)
from thesis.data.preprocessing.nielsen.shared.terminal_utils import (
	step_execution, print_file_load, print_file_save, print_data_preview,
	print_step_summary, print_info
)
from thesis.data.preprocessing.nielsen.shared.timing_utils import log_step_timing

# ============================================================================
# METADATA DEFINITIONS
# ============================================================================
# This step applies time-series train/val/test splits based on locked date boundaries.
# Key split semantics:
#
# SPLIT BOUNDARIES (locked per research design):
#   - Train: period_year-period_month ≤ 2025-02 (2022-10 to 2025-02)
#   - Val: 2025-03 ≤ period_year-period_month ≤ 2025-08 (2025-03 to 2025-08)
#   - Test: 2025-09 ≤ period_year-period_month (2025-09 to 2026-03)
#
# IMPORTANT NOTES:
#   - Splits applied on TIME, not random sampling (time-series integrity required)
#   - NaN values in sales_units/features carry forward to split column
#   - Do NOT use split for any null-handling decisions; NaN pattern from steps 2–4 preserved
#
# OUTPUT (this step):
#   - New column 'split': categorical values 'train', 'val', 'test'
#   - All other columns unchanged; no new NaNs introduced
#   - Train/val/test counts logged; should match step 6 report

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "Energidrikke"
STEP_NUM = 5
STEP_NAME = "Apply Split"

# Input/Output paths
STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
INPUT_ENGINEERED_FEATURES_PARQUET = STEP_OUTPUT_DIR / f"step_4_engineered_features.parquet"
OUTPUT_SPLIT_APPLIED_PARQUET = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_split_applied.parquet"
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"

# ============================================================================
# STEP LOGIC
# ============================================================================

def main():
	"""Execute step 5: Apply split."""
	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		step_start = time.perf_counter()

		# Validate input
		if not INPUT_ENGINEERED_FEATURES_PARQUET.exists():
			raise FileNotFoundError(f"Input missing: {INPUT_ENGINEERED_FEATURES_PARQUET}")

		# Load
		print("Loading engineered features from step 4...")
		load_start = time.perf_counter()
		df = pd.read_parquet(INPUT_ENGINEERED_FEATURES_PARQUET)
		load_elapsed = time.perf_counter() - load_start

		input_shape = df.shape
		print_file_load(INPUT_ENGINEERED_FEATURES_PARQUET, input_shape, load_elapsed)

		# Process
		print(f"\nApplying train/val/test split...")
		print_info(f"Train end: {TRAIN_END[0]}-{TRAIN_END[1]:02d}")
		print_info(f"Val end: {VAL_END[0]}-{VAL_END[1]:02d}")

		process_start = time.perf_counter()

		df = shared_apply_split(df)

		process_elapsed = time.perf_counter() - process_start
		print(f"  ✓ Split applied in {process_elapsed:.2f}s")

		# Show split distribution
		if "split" in df.columns:
			split_dist = df["split"].value_counts().to_dict()
			print_info(f"Split distribution: {split_dist}")

		# Save
		print(f"\nSaving split-applied data...")
		STEP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

		save_start = time.perf_counter()
		df.to_parquet(OUTPUT_SPLIT_APPLIED_PARQUET, index=False)
		save_elapsed = time.perf_counter() - save_start

		output_shape = df.shape
		print_file_save(OUTPUT_SPLIT_APPLIED_PARQUET, output_shape, save_elapsed)

		# Preview
		print("\nData preview:")
		cols_to_show = ["brand", "period_year", "period_month", "sales_units", "split"]
		cols_available = [c for c in cols_to_show if c in df.columns]
		df_preview = df[cols_available].head(10)
		print_data_preview(df_preview, title=f"{CATEGORY} Split Applied", max_rows=10)

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
			output_file=OUTPUT_SPLIT_APPLIED_PARQUET
		)


if __name__ == "__main__":
	main()
