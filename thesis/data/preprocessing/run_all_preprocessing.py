"""
Unified Nielsen Preprocessing Pipeline Runner
==============================================
Orchestrates all 5 category preprocessing scripts in sequence with
aggregated results, timing, and graceful error handling.

This script runs all Nielsen preprocessing pipelines:
  - CSD
  - Energidrikke
  - Danskvand
  - RTD
  - Totalbeer

Output: Aggregated summary report with timing and status for each category.

Usage:
  python3 run_all_preprocessing.py
"""

import sys, json, time, importlib
from pathlib import Path
from datetime import datetime

# Find project root by locating CLAUDE.md -> works regardless of where script is run from
current = Path.cwd()
while current != current.parent:
    if (current / "CLAUDE.md").exists():
        ROOT_DIR_FINDER = current
        break
    current = current.parent
else:
    raise FileNotFoundError("Could not find project root (CLAUDE.md)")

sys.path.insert(0, str(ROOT_DIR_FINDER))

# Import PATHS module and reload to ensure latest changes
import PATHS
importlib.reload(PATHS)

from thesis.data.preprocessing import (
    preprocessing_csd,
    preprocessing_energidrikke,
    preprocessing_danskvand,
    preprocessing_rtd,
    preprocessing_totalbeer,
)
from PATHS import THESIS_DATA_PREPROCESSING_DIR


def run_category_preprocessing(category_module, category_name: str) -> dict:
    """
    Run a single category preprocessing script and return status.

    Args:
        category_module: The preprocessing module (e.g., preprocessing_csd)
        category_name: Human-readable name (e.g., "CSD")

    Returns:
        Dict with status, elapsed time, and error message (if any)
    """
    print(f"\n{'='*80}")
    print(f"Running: {category_name} Preprocessing")
    print(f"{'='*80}\n")

    t0 = time.perf_counter()
    result = {
        "category": category_name,
        "status": "pending",
        "elapsed_sec": 0,
        "error": None,
    }

    try:
        category_module.main()
        elapsed = time.perf_counter() - t0
        result["status"] = "OK"
        result["elapsed_sec"] = round(elapsed, 2)
        print(f"\n✓ {category_name}: Success ({elapsed:.1f}s)")
        return result

    except Exception as e:
        elapsed = time.perf_counter() - t0
        result["status"] = "ERROR"
        result["elapsed_sec"] = round(elapsed, 2)
        result["error"] = str(e)
        print(f"\n✗ {category_name}: FAILED ({elapsed:.1f}s)")
        print(f"  Error: {e}")
        return result


def main():
    """Run all 5 category preprocessing pipelines."""
    print("="*80)
    print("Nielsen Preprocessing Pipeline Runner")
    print("="*80)
    print(f"Start time: {datetime.now().isoformat()}\n")

    # Define all category modules and their names
    categories = [
        (preprocessing_csd, "CSD"),
        (preprocessing_energidrikke, "Energidrikke"),
        (preprocessing_danskvand, "Danskvand"),
        (preprocessing_rtd, "RTD"),
        (preprocessing_totalbeer, "Totalbeer"),
    ]

    results = []
    t0_total = time.perf_counter()

    # Run each category in sequence
    for category_module, category_name in categories:
        result = run_category_preprocessing(category_module, category_name)
        results.append(result)

    elapsed_total = time.perf_counter() - t0_total

    # Generate summary report
    print(f"\n{'='*80}")
    print("Summary Report")
    print(f"{'='*80}\n")

    print("Results by Category:\n")
    print(f"{'Category':<20} {'Status':<10} {'Time (s)':<12} {'Notes':<40}")
    print("-" * 82)

    ok_count = 0
    error_count = 0

    for result in results:
        status = result["status"]
        if status == "OK":
            ok_count += 1
            notes = "✓"
        elif status == "ERROR":
            error_count += 1
            notes = f"✗ {result['error'][:35]}"
        else:
            notes = "pending"

        print(f"{result['category']:<20} {status:<10} {result['elapsed_sec']:<12} {notes:<40}")

    print("\n" + "="*80)
    print(f"Total: {len(results)} categories | OK: {ok_count} | ERROR: {error_count}")
    print(f"Total elapsed time: {elapsed_total:.1f} seconds ({elapsed_total/60:.1f} minutes)")
    print(f"End time: {datetime.now().isoformat()}")
    print("="*80 + "\n")

    # Save manifest
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "total_categories": len(results),
        "successful": ok_count,
        "failed": error_count,
        "elapsed_seconds": round(elapsed_total, 2),
        "results": results,
    }

    manifest_path = THESIS_DATA_PREPROCESSING_DIR / "preprocessing_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Manifest saved to: {manifest_path}")

    # Exit with appropriate code
    if error_count > 0:
        print(f"\n⚠ {error_count} preprocessing(s) failed. See above for details.")
        return 1
    else:
        print("\n✓ All preprocessing pipelines completed successfully.")
        return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
