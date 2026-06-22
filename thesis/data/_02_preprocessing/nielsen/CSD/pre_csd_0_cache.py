#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing Pipeline — Step 0: Verify Parquet Cache

PURPOSE
=======
This step verifies that the Parquet cache (produced by Stage 1 JSONL → Parquet
conversion) exists and is complete for the given Nielsen category. It acts as a
validation gate before downstream preprocessing steps attempt to load data.

DESIGN RATIONALE
================
Rather than duplicating the JSONL → Parquet conversion logic, this step delegates
that responsibility to the Stage 1 orchestrator (run_all_conversions.py), which is
purpose-built for handling large-scale conversions with proper memory management
and error recovery. This separation of concerns:

  1. Reduces code duplication
  2. Allows Stage 1 to handle OOM gracefully (critical for large categories like Totalbeer)
  3. Provides clear error messages if cache is missing
  4. Makes the preprocessing pipeline modular and testable

ARCHITECTURE
============
Step 0 validates that these files exist:
  Input (checked):  thesis/data/converted/nielsen/parquet_nielsen/{category}/views/
    - {category}_clean_facts_v.parquet
    - {category}_clean_dim_product_v.parquet
    - {category}_clean_dim_period_v.parquet
    - {category}_clean_dim_market_v.parquet

  Output:  None (validation only; no files created)

DEPENDENCIES
============
This step depends on Stage 1 completion:
  thesis/data/converted/nielsen/jsonl_to_parquet/run_all_conversions.py

If the cache is missing, the step fails and instructs the user to run Stage 1 first.

USAGE
=====
  # Validate cache for CSD
  python pre_csd_0_cache.py

  # If cache missing, instructions printed to console
  # If cache exists, proceeds silently with status summary
"""

import sys
import time
import importlib
from pathlib import Path

# ============================================================================
# PROJECT INITIALIZATION
# ============================================================================
# Find project root by searching for CLAUDE.md. This allows the script to be
# run from any working directory without requiring PATH manipulation.

current = Path.cwd()
while current != current.parent:
	if (current / "CLAUDE.md").exists():
		ROOT_DIR = current
		break
	current = current.parent
else:
	raise FileNotFoundError("Could not find project root (CLAUDE.md)")

sys.path.insert(0, str(ROOT_DIR))

# Reload PATHS module to ensure latest configuration (mirrors Stage 1 approach).
# This is important if PATHS.py has been updated during development.
import PATHS
importlib.reload(PATHS)

from PATHS import THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR, get_category_pipeline_step_outputs_dir

# Import shared utilities for consistent logging and timing across all preprocessing steps.
from thesis.data._02_preprocessing.nielsen.shared.terminal_utils import (
	step_execution, print_info, print_warning
)
from thesis.data._02_preprocessing.nielsen.shared.timing_utils import log_step_timing

# ============================================================================
# CONFIGURATION
# ============================================================================
# Step identifier and category. These are used for logging and path construction.
# The category is hardcoded to CSD for this script; to support other categories,
# modify this constant or convert to a command-line argument.

CATEGORY = "CSD"  # Nielsen data category
STEP_NUM = 0      # Pipeline step number
STEP_NAME = "Verify Parquet Cache"  # Human-readable step name

# Cache location produced by Stage 1 (JSONL → Parquet conversion).
# This path is dynamically constructed from PATHS.py to allow configuration changes
# without modifying this script.
CACHE_VIEWS_DIR = THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / CATEGORY / "views"

# Log file path for recording step execution (timing, row counts, errors).
# Stored alongside other pipeline step logs for audit trail.
LOG_FILE = get_category_pipeline_step_outputs_dir(CATEGORY) / f"step_{STEP_NUM}_log.json"


# ============================================================================
# VALIDATION LOGIC
# ============================================================================

def validate_parquet_cache(category: str, cache_dir: Path) -> dict:
	"""
	Validate that all required view parquet files exist in the cache.

	PARAMETERS
	----------
	category : str
		Nielsen category name (e.g., "CSD", "Energidrikke", "Totalbeer").
		Used for constructing error messages and logging.

	cache_dir : Path
		Directory path where parquet view files are expected.
		Typically: thesis/data/converted/nielsen/parquet_nielsen/{category}/views/

	RETURNS
	-------
	dict
		Validation result with keys:
		  - "valid" (bool): True if all required files exist, False otherwise
		  - "missing" (list): Names of missing parquet files
		  - "found" (list): Names of parquet files found in cache
		  - "message" (str): Human-readable status message

	NOTES
	-----
	This step validates ONLY the view tables (cleaned, column-reduced versions
	of Nielsen data). Raw tables are not cached (file size too large). Metadata
	tables are not cached (lightweight, optional for downstream processing).

	The required files are hardcoded based on Nielsen schema (facts table +
	3 dimension tables: product, period, market). These are the minimum set
	needed for Step 1 (load and aggregate).
	"""

	# Define required parquet files. These correspond to the Nielsen view tables
	# produced by Stage 1. Each file is a cleaned, column-reduced view of the
	# corresponding Nielsen table.
	required_view_files = [
		f"{category.lower()}_clean_facts_v.parquet",           # Fact table: sales transactions
		f"{category.lower()}_clean_dim_product_v.parquet",     # Dimension: product/brand hierarchy
		f"{category.lower()}_clean_dim_period_v.parquet",      # Dimension: time periods (Nielsen 4-4-5 calendar)
		f"{category.lower()}_clean_dim_market_v.parquet",      # Dimension: retail outlet types
	]

	# Check which files exist in the cache directory.
	# Missing files indicate Stage 1 has not been run or failed.
	missing = [f for f in required_view_files if not (cache_dir / f).exists()]
	found = [f for f in required_view_files if (cache_dir / f).exists()]

	# Return validation result. If any files are missing, set valid=False and
	# provide actionable error message.
	if missing:
		return {
			"valid": False,
			"missing": missing,
			"found": found,
			"message": f"[{category}] Missing {len(missing)} of {len(required_view_files)} required parquet view files"
		}

	return {
		"valid": True,
		"missing": [],
		"found": found,
		"message": f"[{category}] All {len(required_view_files)} required parquet view files found"
	}


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
	"""
	Execute Step 0: Verify parquet cache exists and is complete.

	FLOW
	----
	1. Validate that all required parquet files exist in the cache
	2. If missing: Print actionable error message with Stage 1 instructions
	3. If present: Print summary and proceed to next step
	4. Log execution timing (for performance monitoring)

	EXIT BEHAVIOR
	-------------
	- No exception raised; uses context manager (step_execution) for clean logging
	- If validation fails, prints instructions and returns silently
	- If validation passes, prints summary and returns normally
	"""

	with step_execution(STEP_NUM, STEP_NAME, CATEGORY):
		step_start = time.perf_counter()

		# ────────────────────────────────────────────────────────────────────
		# VALIDATION PHASE: Check cache exists
		# ────────────────────────────────────────────────────────────────────

		print("\nValidating parquet cache...")
		validation = validate_parquet_cache(CATEGORY, CACHE_VIEWS_DIR)

		# Handle validation failure: print diagnostic and instructions
		if not validation["valid"]:
			print_warning(f"\n{validation['message']}")
			print_warning(f"Cache location: {CACHE_VIEWS_DIR}")

			# Show what was found vs. missing (helps user diagnose partial failures)
			print_warning(f"\nFound {len(validation['found'])}/{len(validation['found']) + len(validation['missing'])} files:")
			for f in sorted(validation["found"]):
				print_warning(f"  ✓ {f}")

			if validation["missing"]:
				print_warning(f"\nMissing {len(validation['missing'])} files:")
				for f in sorted(validation["missing"]):
					print_warning(f"  ✗ {f}")

			# Print actionable solution (run Stage 1)
			print("\n" + "=" * 80)
			print("SOLUTION: Run Stage 1 (JSONL → Parquet conversion) first")
			print("=" * 80)
			print(f"\nFrom the project root:")
			print(f"  # Convert only {CATEGORY}:")
			print(f"  python thesis/data/converted/nielsen/jsonl_to_parquet/run_all_conversions.py --only {CATEGORY}")
			print(f"\n  # Or convert all categories:")
			print(f"  python thesis/data/converted/nielsen/jsonl_to_parquet/run_all_conversions.py")
			print("\n" + "=" * 80)
			return

		# ────────────────────────────────────────────────────────────────────
		# SUCCESS PHASE: Cache validated, report status
		# ────────────────────────────────────────────────────────────────────

		print_info(validation["message"])
		print_info(f"Cache location: {CACHE_VIEWS_DIR}")

		# Record execution timing for pipeline performance monitoring
		step_elapsed = time.perf_counter() - step_start
		LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
		log_step_timing(STEP_NUM, STEP_NAME, CATEGORY, step_elapsed, 0, LOG_FILE)

		# Print summary showing cache status and which files were verified
		print("\n" + "=" * 80)
		print("CACHE VERIFICATION SUMMARY")
		print("=" * 80)
		print(f"Category: {CATEGORY}")
		print(f"Status: ✓ Cache verified")
		print(f"Files: {len(validation['found'])} view parquet files")
		for f in sorted(validation["found"]):
			print(f"  ✓ {f}")
		print(f"Location: {CACHE_VIEWS_DIR}")
		print(f"Elapsed time: {step_elapsed:.1f}s")
		print("=" * 80)
		print_info("Step 0 complete. Parquet cache ready for Step 1.")


if __name__ == "__main__":
	main()
