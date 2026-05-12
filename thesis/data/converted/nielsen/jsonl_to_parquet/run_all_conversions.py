"""
Stage 1 Orchestrator — Convert All Categories
==============================================
Runs `convert_category.convert_category` for each Nielsen category.

Idempotent: per-file skip-if-newer check inside convert_category.
Pass --force to re-convert all files unconditionally.

Usage:
  python run_all_conversions.py
  python run_all_conversions.py --force
  python run_all_conversions.py --only CSD Energidrikke
"""

import sys
import argparse
import importlib
import time
import json
from pathlib import Path

current = Path.cwd()
while current != current.parent:
    if (current / "CLAUDE.md").exists():
        ROOT_DIR_FINDER = current
        break
    current = current.parent
else:
    raise FileNotFoundError("Could not find project root (CLAUDE.md)")

sys.path.insert(0, str(ROOT_DIR_FINDER))

import PATHS
importlib.reload(PATHS)

from PATHS import THESIS_DATA_PREPROCESSING_DIR

# Stage 1 lives next to this file; import the convert_category module from there.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from convert_category import convert_category, VALID_CATEGORIES


def main():
    parser = argparse.ArgumentParser(
        description="Convert Nielsen JSONL → Parquet for all categories."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-convert even if Parquet is newer than JSONL.",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        choices=VALID_CATEGORIES,
        help="Restrict to a subset of categories.",
    )
    args = parser.parse_args()

    categories = args.only if args.only else VALID_CATEGORIES

    t0 = time.perf_counter()
    results = []
    for cat in categories:
        try:
            res = convert_category(cat, force=args.force)
            res["error"] = None
        except Exception as e:
            res = {"category": cat, "views_converted": 0,
                   "metadata_converted": 0, "elapsed": 0.0, "error": str(e)}
            print(f"  ✗ {cat} FAILED: {e}\n")
        results.append(res)

    elapsed = time.perf_counter() - t0

    print("=" * 80)
    print("Stage 1 Summary")
    print("=" * 80)
    n_ok = sum(1 for r in results if r["error"] is None)
    n_fail = len(results) - n_ok
    for r in results:
        status = "✓" if r["error"] is None else "✗"
        files = r["views_converted"] + r["metadata_converted"]
        msg = f"{status} {r['category']}: {files} file(s) in {r['elapsed']:.1f}s"
        if r["error"]:
            msg += f"  [{r['error']}]"
        print(f"  {msg}")
    print(f"\n  Total: {n_ok} ok, {n_fail} failed, {elapsed:.1f}s elapsed")

    manifest = {
        "stage": "1_jsonl_to_parquet",
        "categories": results,
        "total_elapsed_seconds": elapsed,
    }
    manifest_path = THESIS_DATA_PREPROCESSING_DIR / "jsonl_to_parquet_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"  Manifest written to {manifest_path}")

    if n_fail > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
