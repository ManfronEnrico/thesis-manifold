#!/usr/bin/env python3
"""
Nielsen CSD Preprocessing Orchestrator

Runs all 7 preprocessing steps for CSD in sequence:
  - Step 0: Cache view and metadata tables as parquet (conditional: skipped if cache exists)
  - Step 1: Load and aggregate
  - Step 2: Build calendar
  - Step 3: Filter series
  - Step 4: Engineer features
  - Step 5: Apply split
  - Step 6: Save outputs

Step scripts live one level deeper, in pipeline_step_scripts/ (regrouped
2026-07-13) — resolved via PATHS.get_category_preprocessing_scripts_dir(),
which is layout-aware and works whether or not a category has been regrouped.

CACHING STRATEGY (Smart):
  Default: Checks for existing cached parquet; skips step 0 if found (fast path)
  --run-raw: Forces execution of step 0 (re-caches even if exists)
  --re-cache: Removes existing cache and re-generates (full cache refresh)

GRAIN (--grain / --grains, default "bymonth"):
  Steps 1-6 are grain-aware (see pipeline_step_scripts/pre_csd_1_load_and_aggregate.py's
  GRAIN_CONFIG). Only "bymonth" is implemented today; "bychain"/"byregion" raise
  NotImplementedError (see plans/P0027 Phase 4b, deferred). Pass a comma-separated
  list to --grains to run multiple grains in one invocation, once more than
  "bymonth" is implemented.

Use --run-step N to run only step N (must use --run-raw if step N is 0).

Usage:
  python preprocessing_csd.py                        # Run steps 1-6, grain=bymonth (uses cached parquet if available)
  python preprocessing_csd.py --grain bymonth         # Explicit grain
  python preprocessing_csd.py --grains bymonth,bychain  # Multiple grains (bychain not yet implemented)
  python preprocessing_csd.py --run-raw               # Force step 0 caching (re-cache existing)
  python preprocessing_csd.py --re-cache               # Clear cache, then re-generate and run steps 0-6
  python preprocessing_csd.py --run-step 4             # Re-run feature engineering only
  python preprocessing_csd.py --run-step 0 --run-raw   # Re-run step 0 only
"""

import sys, argparse, subprocess, time
from pathlib import Path

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

from PATHS import get_category_preprocessing_scripts_dir, THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "CSD"
SCRIPTS_DIR = get_category_preprocessing_scripts_dir(CATEGORY)
STEPS = [1, 2, 3, 4, 5, 6]
GRAIN_AWARE_STEPS = {1, 2, 3, 4, 5, 6}  # all steps except 0 (cache validation, grain-independent)
DEFAULT_GRAIN = "bymonth"

STEP_NAMES = {
	0: "Cache Raw Data (moved to Stage 1 — converted/nielsen/jsonl_to_parquet/)",
	1: "Load and Aggregate",
	2: "Build Calendar",
	3: "Filter Series",
	4: "Engineer Features",
	5: "Apply Split",
	6: "Save Outputs",
}

# ============================================================================
# ORCHESTRATION
# ============================================================================

def cache_exists() -> bool:
	"""Check if Stage 1 view parquet cache already exists in converted tier."""
	views_dir = THESIS_DATA_CONVERTED_NIELSEN_PARQUET_DIR / CATEGORY / "views"
	cache_files = [
		views_dir / "csd_clean_facts_v.parquet",
		views_dir / "csd_clean_dim_product_v.parquet",
		views_dir / "csd_clean_dim_period_v.parquet",
		views_dir / "csd_clean_dim_market_v.parquet"
	]
	return all(f.exists() for f in cache_files)


def run_step(step_num: int, grains_arg: str) -> bool:
	"""
	Run a single preprocessing step script.

	Args:
		step_num: Step number (1-6; stage 1 is handled separately by converted/nielsen/jsonl_to_parquet/)
		grains_arg: Comma-separated grain list to pass as --grains (ignored for step 0)

	Returns:
		True if successful, raises exception on failure
	"""
	# Find step script
	script = list(SCRIPTS_DIR.glob(f"pre_{CATEGORY.lower()}_{step_num}_*.py"))
	if not script:
		raise FileNotFoundError(f"Step {step_num} script not found in {SCRIPTS_DIR}")

	script = script[0]

	print(f"\n{'='*80}")
	print(f"Step {step_num}: {STEP_NAMES.get(step_num, 'Unknown')}")
	print(f"{'='*80}")

	cmd = [sys.executable, str(script)]
	if step_num in GRAIN_AWARE_STEPS:
		cmd += ["--grains", grains_arg]

	result = subprocess.run(cmd, cwd=ROOT_DIR)

	if result.returncode != 0:
		raise RuntimeError(f"Step {step_num} failed with exit code {result.returncode}")

	return True


def main():
	parser = argparse.ArgumentParser(
		description=f"Run {CATEGORY} preprocessing pipeline (Stage 2 — Feature Engineering)",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Examples:
  python preprocessing_csd.py                    # Run steps 1-6, grain=bymonth (requires Stage 1 cache)
  python preprocessing_csd.py --run-step 4       # Run only step 4
  python preprocessing_csd.py --grains bymonth,bychain  # Multiple grains (bychain not yet implemented)
		"""
	)
	parser.add_argument(
		"--run-step",
		type=int,
		default=None,
		help="Run only this step (1-6); if not specified, run all"
	)
	parser.add_argument("--grain", type=str, default=None, help=f"Single grain (default: {DEFAULT_GRAIN})")
	parser.add_argument("--grains", type=str, default=None, help="Comma-separated list of grains")
	args = parser.parse_args()

	# Validate --run-step argument
	if args.run_step is not None:
		if args.run_step not in STEPS:
			print(f"Error: --run-step must be in {STEPS}, got {args.run_step}")
			sys.exit(1)

	if args.grains:
		grains_arg = args.grains
	elif args.grain:
		grains_arg = args.grain
	else:
		grains_arg = DEFAULT_GRAIN

	# Check that Stage 1 cache exists before proceeding
	if not cache_exists():
		print("=" * 80)
		print("ERROR: Stage 1 Parquet cache not found!")
		print("=" * 80)
		print(f"\nExpected cache location: thesis/data/converted/nielsen/parquet_nielsen/{CATEGORY}/views/")
		print("\nThis stage (Stage 2) depends on Stage 1 (JSONL → Parquet conversion) being complete.")
		print("\nTo generate the cache, run:")
		print(f"  python thesis/data/converted/nielsen/jsonl_to_parquet/run_all_conversions.py --only {CATEGORY}")
		print("=" * 80)
		sys.exit(1)

	# Run orchestration
	pipeline_start = time.perf_counter()

	try:
		if args.run_step is not None:
			# Run single step
			print(f"\n{'='*80}")
			print(f"Running {CATEGORY} step {args.run_step} only (grain(s): {grains_arg})")
			print(f"{'='*80}")

			run_step(args.run_step, grains_arg)
		else:
			# Run all steps
			print(f"\n{'='*80}")
			print(f"Nielsen {CATEGORY} Preprocessing Pipeline (Stage 2 — Feature Engineering)")
			print(f"Grain(s): {grains_arg}")
			print(f"{'='*80}")

			for step in STEPS:
				run_step(step, grains_arg)

			# Final summary
			pipeline_elapsed = time.perf_counter() - pipeline_start

			print(f"\n{'='*80}")
			print(f"✓ {CATEGORY} preprocessing complete (grain(s): {grains_arg})")
			print(f"  Total elapsed: {pipeline_elapsed:.1f}s")
			print(f"{'='*80}\n")

	except Exception as e:
		print(f"\n{'='*80}")
		print(f"✗ Pipeline failed: {e}")
		print(f"{'='*80}\n")
		sys.exit(1)


if __name__ == "__main__":
	main()
