#!/usr/bin/env python3
"""
Nielsen Preprocessing -- Step 0: Validate Parquet Cache

Shared across all categories; select with --category.

Input:  The 4 Nielsen view parquet files for the category, produced by Stage 1
        (JSONL -> Parquet conversion). Read-only -- this step opens nothing.
Output: step_0_console.log, step_0_log.json  (validation only, no data written)

Logic:
  - Resolve paths from --category
  - Assert all 4 required view parquet files exist and are non-empty
  - Fail loudly with the exact remediation command if any are missing

WHY VALIDATION IS ITS OWN STEP
------------------------------
Step 1 merges 4 files. If one is missing, the pandas error names a path but not
the cause; if one is present-but-empty, the merge silently yields 0 rows and the
failure surfaces several steps later as an unrelated statistic. Checking up
front converts both into one actionable message.

Ported from the CSD notebook cells "Step 0.4 - Cache Validation" (P0038).
The notebook's `%pip install` cells were dropped -- dependencies belong in
requirements.txt, not in a pipeline step.
"""

import argparse
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root discovery (same idiom as every other step script)
# ---------------------------------------------------------------------------
current = Path.cwd()
while current != current.parent:
	if (current / "CLAUDE.md").exists():
		ROOT_DIR = current
		break
	current = current.parent
else:
	raise FileNotFoundError("Could not find project root (CLAUDE.md)")

sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "02_thesis_data" / "_02_preprocessing" / "nielsen" / "_shared_modules"))

from capture_utils import tee_console
from pipeline_config import (
	FORECAST_HORIZON,
	CATEGORIES,
	get_paths,
	normalise_category,
	print_target_definition,
	suppress_warnings,
	view_filenames,
)
from terminal_utils import print_info, step_execution
from timing_utils import log_step_timing

STEP_NUM = 0
STEP_NAME = "Validate Parquet Cache"


# ============================================================================
# VALIDATION
# ============================================================================

def validate_parquet_cache(category: str, cache_dir: Path) -> dict:
	"""Check that all required view parquet files exist and are non-empty.

	The size check is the addition over the notebook version, which tested
	.exists() only. A 0-byte parquet is what a conversion run interrupted
	mid-write leaves behind: it passes an existence test, then fails inside
	pandas at step 1 with an opaque error.
	"""
	required = view_filenames(category)

	missing: list[str] = []
	empty: list[str] = []
	found: list[str] = []

	for fname in required:
		fpath = cache_dir / fname
		if not fpath.exists():
			missing.append(fname)
		elif fpath.stat().st_size == 0:
			empty.append(fname)
		else:
			found.append(fname)

	problems = missing + empty
	if problems:
		parts = []
		if missing:
			parts.append(f"{len(missing)} missing")
		if empty:
			parts.append(f"{len(empty)} empty")
		message = (
			f"[{category}] {' and '.join(parts)} of {len(required)} "
			f"required parquet view files"
		)
	else:
		message = f"[{category}] All {len(required)} required parquet view files present"

	return {
		"valid": not problems,
		"category": category,
		"cache_dir": str(cache_dir),
		"required": required,
		"missing": missing,
		"empty": empty,
		"found": found,
		"message": message,
	}


def report(validation: dict) -> None:
	"""Print the cache verification summary (notebook parity)."""
	print()
	print("=" * 80)
	print("CACHE VERIFICATION SUMMARY")
	print("=" * 80)
	print(f"Category:       {validation['category']}")
	print(f"Cache location: {validation['cache_dir']}")

	if validation["valid"]:
		print(f"Status: OK -- {validation['message']}")
		for f in sorted(validation["found"]):
			size_mb = 0.0
			fp = Path(validation["cache_dir"]) / f
			if fp.exists():
				size_mb = fp.stat().st_size / (1024 * 1024)
			print(f"  {f}  ({size_mb:.1f} MB)")
	else:
		print(f"Status: FAILED -- {validation['message']}")
		for f in sorted(validation["found"]):
			print(f"  found:   {f}")
		for f in sorted(validation["empty"]):
			print(f"  EMPTY:   {f}")
		for f in sorted(validation["missing"]):
			print(f"  MISSING: {f}")

	print("=" * 80)


# ============================================================================
# MAIN
# ============================================================================

def run(category: str) -> dict:
	"""Validate one category. Returns the validation dict; raises if invalid."""
	suppress_warnings()
	category = normalise_category(category)
	paths = get_paths(category)
	paths["step_output_dir"].mkdir(parents=True, exist_ok=True)

	log_path = paths["step_output_dir"] / f"step_{STEP_NUM}_console.log"

	with tee_console(log_path):
		with step_execution(STEP_NUM, STEP_NAME, category):
			step_start = time.perf_counter()

			print(f"\n{'=' * 80}")
			print(f"{category} Preprocessing Configuration")
			print("=" * 80)
			print(f"  Category:        {category}")
			print(f"  Views dir:       {paths['views_dir']}")
			print(f"  Step outputs:    {paths['step_output_dir']}")
			print(f"  Output findings: {paths['findings_json_for'](FORECAST_HORIZON)}")
			print(f"  Plots directory: {paths['plots_dir']}")
			print()
			print_target_definition()

			validation = validate_parquet_cache(category, paths["views_dir"])
			report(validation)

			if not validation["valid"]:
				raise FileNotFoundError(
					f"Parquet cache incomplete for {category}. "
					f"Run Stage 1 (JSONL -> Parquet) first: run_all_conversions.py, "
					f"under THESIS_DATA_CONVERTED_NIELSEN_DIR."
				)

			elapsed = time.perf_counter() - step_start
			log_step_timing(
				STEP_NUM,
				STEP_NAME,
				category,
				elapsed,
				len(validation["found"]),
				paths["step_output_dir"] / f"step_{STEP_NUM}_log.json",
			)
			print_info(f"Console log: {log_path}")

	return validation


def main() -> int:
	parser = argparse.ArgumentParser(
		description="Validate the Nielsen parquet view cache for a category."
	)
	parser.add_argument(
		"--category",
		required=True,
		help=f"Category to validate. One of: {', '.join(CATEGORIES)}",
	)
	args = parser.parse_args()

	run(args.category)
	return 0


if __name__ == "__main__":
	sys.exit(main())
