#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing — Step 5: Apply Split

Input:  Step 4 output (engineered_features_{grain}.parquet)
		- Calendar-filled, filtered, feature-engineered brand × month data

Output: Step 5 output (split_applied_{grain}.parquet)
		- Same data plus 'split' column (train, val, or test)
		- Split boundaries from CSD EDA analysis: train ≤ 2024-10, val ≤ 2025-04, test ≥ 2025-04

Logic:
  - Import apply_split() from shared codebase
  - Apply CSD-specific train/val/test split dates (from EDA, Cell 7)
  - Add split column to DataFrame

CATEGORY-SPECIFIC NOTES (CSD EDA):
  - TRAIN_END = (2024, 10): 24 months training data for stable pattern learning
  - VAL_END = (2025, 4): 6 months validation for tuning
  - TEST: Remaining 13 months (2025-04 to 2026-04) for final evaluation
  - Rationale: Data-driven split vs arbitrary defaults, maximizes test data
  - Split dates are time-based (not group-key-based) and apply identically
    across grains — only the input/output path changes per grain.

USAGE
=====
  python pre_csd_5_apply_split.py [--grain bymonth] [--grains bymonth,bychain]
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
from engineer_features import apply_split as shared_apply_split
from terminal_utils import (
	step_execution, print_file_load, print_file_save, print_data_preview,
	print_step_summary, print_info
)
from timing_utils import log_step_timing

# Import GRAIN_CONFIG from Step 1
sys.path.insert(0, str(Path(__file__).parent))
from pre_csd_1_load_and_aggregate import DEFAULT_GRAIN, IMPLEMENTED_GRAINS

# ============================================================================
# METADATA DEFINITIONS
# ============================================================================
# This step applies time-series train/val/test splits based on locked date boundaries.
# Key split semantics:
#
# SPLIT BOUNDARIES (per CSD EDA analysis — Cell 7):
#   - Train: 2022-10 to 2024-10 (24 months — 2 years for stable pattern learning)
#   - Val: 2024-10 to 2025-04 (6 months — tuning window)
#   - Test: 2025-04 to 2026-04 (13 months — final evaluation)
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

CATEGORY = "CSD"
STEP_NUM = 5
STEP_NAME = "Apply Split"

# CSD-specific split dates (from EDA analysis, Cell 7) — time-based, grain-independent
CSD_TRAIN_END = (2024, 10)  # 24 months training data
CSD_VAL_END = (2025, 4)     # 6 months validation data
# Test automatically: remaining data (2025-04 to 2026-05)

STEP_OUTPUT_DIR = get_category_pipeline_step_outputs_dir(CATEGORY)
LOG_FILE = STEP_OUTPUT_DIR / f"step_{STEP_NUM}_log.json"


def input_parquet_for_grain(grain: str) -> Path:
	return STEP_OUTPUT_DIR / f"step_4_engineered_features_{grain}.parquet"


def output_parquet_for_grain(grain: str) -> Path:
	return STEP_OUTPUT_DIR / f"step_{STEP_NUM}_split_applied_{grain}.parquet"

# ============================================================================
# STEP LOGIC
# ============================================================================

def run_step(grain: str):
	"""Execute step 5 for a single grain."""
	if grain not in IMPLEMENTED_GRAINS:
		raise NotImplementedError(
			f"Grain '{grain}' is not yet implemented. See plans/P0027 Phase 4b (deferred)."
		)

	input_parquet = input_parquet_for_grain(grain)
	output_parquet = output_parquet_for_grain(grain)

	step_start = time.perf_counter()

	if not input_parquet.exists():
		raise FileNotFoundError(f"Input missing: {input_parquet}")

	print(f"Loading engineered features for grain='{grain}' from step 4...")
	load_start = time.perf_counter()
	df = pd.read_parquet(input_parquet)
	load_elapsed = time.perf_counter() - load_start

	input_shape = df.shape
	print_file_load(input_parquet, input_shape, load_elapsed)

	print(f"\nApplying train/val/test split (CSD EDA-driven)...")
	print_info(f"Train end: {CSD_TRAIN_END[0]}-{CSD_TRAIN_END[1]:02d} (24 months)")
	print_info(f"Val end: {CSD_VAL_END[0]}-{CSD_VAL_END[1]:02d} (6 months)")
	print_info(f"Test: Remaining data until 2026-04")

	process_start = time.perf_counter()

	df = shared_apply_split(df, train_end=CSD_TRAIN_END, val_end=CSD_VAL_END)

	process_elapsed = time.perf_counter() - process_start
	print(f"  ✓ Split applied in {process_elapsed:.2f}s")

	if "split" in df.columns:
		split_dist = df["split"].value_counts().to_dict()
		print_info(f"Split distribution: {split_dist}")

	print(f"\nSaving split-applied data ({grain})...")
	STEP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

	save_start = time.perf_counter()
	df.to_parquet(output_parquet, index=False)
	save_elapsed = time.perf_counter() - save_start

	output_shape = df.shape
	print_file_save(output_parquet, output_shape, save_elapsed)

	print("\nData preview:")
	cols_to_show = ["brand", "period_year", "period_month", "sales_units", "split"]
	cols_available = [c for c in cols_to_show if c in df.columns]
	df_preview = df[cols_available].head(10)
	print_data_preview(df_preview, title=f"{CATEGORY} Split Applied ({grain})", max_rows=10)

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
	"""Execute step 5: Apply split."""
	parser = argparse.ArgumentParser(description="CSD Step 5: Apply Split")
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
