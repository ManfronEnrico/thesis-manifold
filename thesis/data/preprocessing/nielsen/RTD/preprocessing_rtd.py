#!/usr/bin/env python3
"""
Nielsen RTD Preprocessing Orchestrator

Runs all 7 preprocessing steps for RTD in sequence:
  - Step 0: Cache view and metadata tables as parquet (conditional: skipped if cache exists)
  - Step 1: Load and aggregate
  - Step 2: Build calendar
  - Step 3: Filter series
  - Step 4: Engineer features
  - Step 5: Apply split
  - Step 6: Save outputs

CACHING STRATEGY (Smart):
  Default: Checks for existing cached parquet; skips step 0 if found (fast path)
  --run-raw: Forces execution of step 0 (re-caches even if exists)
  --re-cache: Removes existing cache and re-generates (full cache refresh)

Use --run-step N to run only step N (must use --run-raw if step N is 0).

Usage:
  python preprocessing_RTD.py                     # Run steps 1-6 (uses cached parquet if available)
  python preprocessing_RTD.py --run-raw           # Force step 0 caching (re-cache existing)
  python preprocessing_RTD.py --re-cache          # Clear cache, then re-generate and run steps 0-6
  python preprocessing_RTD.py --run-step 4        # Re-run feature engineering only
  python preprocessing_RTD.py --run-step 0 --run-raw  # Re-run step 0 only
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

from PATHS import get_category_preprocessing_scripts_dir

# ============================================================================
# CONFIGURATION
# ============================================================================

CATEGORY = "RTD"
SCRIPTS_DIR = get_category_preprocessing_scripts_dir(CATEGORY)
STEPS = [0, 1, 2, 3, 4, 5, 6]

STEP_NAMES = {
	0: "Cache Raw Data",
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
	"""Check if view parquet cache already exists."""
	views_dir = Path(ROOT_DIR) / "thesis" / "data" / "preprocessing" / "nielsen" / CATEGORY / "views"
	cache_files = [
		views_dir / "RTD_clean_facts_v.parquet",
		views_dir / "RTD_clean_dim_product_v.parquet",
		views_dir / "RTD_clean_dim_period_v.parquet",
		views_dir / "RTD_clean_dim_market_v.parquet"
	]
	return all(f.exists() for f in cache_files)


def run_step(step_num: int, run_raw: bool = False, force_step0: bool = False) -> bool:
	"""
	Run a single step script.

	Args:
		step_num: Step number (0-6)
		run_raw: If True, force execution of step 0; if False, use smart caching
		force_step0: If True, override default and run step 0 regardless of cache state

	Returns:
		True if successful, False if skipped, raises exception on failure
	"""
	if step_num == 0:
		if force_step0:
			print(f"â–¶ Running step {step_num} (forced via --run-raw or --re-cache)")
		elif cache_exists():
			print(f"âœ“ Step {step_num} skipped (parquet cache already exists)")
			return False
		else:
			print(f"âŠ˜ Step {step_num} skipped (cache exists; use --run-raw to force)")
			return False

	# Find step script
	script = list(SCRIPTS_DIR.glob(f"pre_{CATEGORY.lower()}_{step_num}_*.py"))
	if not script:
		raise FileNotFoundError(f"Step {step_num} script not found in {SCRIPTS_DIR}")

	script = script[0]

	print(f"\n{'='*80}")
	print(f"Step {step_num}: {STEP_NAMES.get(step_num, 'Unknown')}")
	print(f"{'='*80}")

	result = subprocess.run(
		[sys.executable, str(script)],
		cwd=ROOT_DIR
	)

	if result.returncode != 0:
		raise RuntimeError(f"Step {step_num} failed with exit code {result.returncode}")

	return True


def main():
	parser = argparse.ArgumentParser(
		description=f"Run {CATEGORY} preprocessing pipeline",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Examples:
  python preprocessing_RTD.py                    # Run steps 1-6 (skip caching)
  python preprocessing_RTD.py --run-raw          # Run all steps 0-6 (include caching)
  python preprocessing_RTD.py --run-step 4       # Run only step 4
  python preprocessing_RTD.py --run-step 0 --run-raw  # Run only step 0
		"""
	)
	parser.add_argument(
		"--run-raw",
		action="store_true",
		help="Force execution of step 0 (re-cache parquet files)"
	)
	parser.add_argument(
		"--re-cache",
		action="store_true",
		help="Remove existing cache and regenerate all parquet files (implies --run-raw)"
	)
	parser.add_argument(
		"--run-step",
		type=int,
		default=None,
		help="Run only this step (0-6); if not specified, run all"
	)
	args = parser.parse_args()

	# --re-cache implies --run-raw
	if args.re_cache:
		args.run_raw = True

	# Validate --run-step argument
	if args.run_step is not None:
		if args.run_step not in STEPS:
			print(f"Error: --run-step must be 0-6, got {args.run_step}")
			sys.exit(1)
		# Step 0 requires --run-raw
		if args.run_step == 0 and not args.run_raw:
			print(f"Error: Step 0 requires --run-raw flag")
			sys.exit(1)

	# Handle --re-cache: clear existing cache
	if args.re_cache:
		cache_dirs = [
			Path(ROOT_DIR) / "thesis" / "data" / "preprocessing" / "nielsen" / CATEGORY / "views",
			Path(ROOT_DIR) / "thesis" / "data" / "preprocessing" / "nielsen" / CATEGORY / "metadata",
		]
		for dir_path in cache_dirs:
			if dir_path.exists():
				parquet_files = list(dir_path.glob("*.parquet"))
				if parquet_files:
					print(f"Removing {len(parquet_files)} cached parquet files from {dir_path.name}...")
					for f in parquet_files:
						f.unlink()

	# Run orchestration
	pipeline_start = time.perf_counter()

	try:
		if args.run_step is not None:
			# Run single step
			print(f"\n{'='*80}")
			print(f"Running {CATEGORY} step {args.run_step} only")
			print(f"{'='*80}")

			run_step(args.run_step, run_raw=args.run_raw, force_step0=args.run_raw)
		else:
			# Run all steps (smart caching: step 0 conditional)
			print(f"\n{'='*80}")
			print(f"Nielsen {CATEGORY} Preprocessing Pipeline")
			print(f"Cache status: {'FRESH (will regenerate)' if args.re_cache else 'SMART (use cached if available)'}")
			print(f"{'='*80}")

			for step in STEPS:
				run_step(step, run_raw=args.run_raw, force_step0=args.run_raw)

			# Final summary
			pipeline_elapsed = time.perf_counter() - pipeline_start

			print(f"\n{'='*80}")
			print(f"âœ“ {CATEGORY} preprocessing complete")
			print(f"  Total elapsed: {pipeline_elapsed:.1f}s")
			print(f"{'='*80}\n")

	except Exception as e:
		print(f"\n{'='*80}")
		print(f"âœ— Pipeline failed: {e}")
		print(f"{'='*80}\n")
		sys.exit(1)


if __name__ == "__main__":
	main()

