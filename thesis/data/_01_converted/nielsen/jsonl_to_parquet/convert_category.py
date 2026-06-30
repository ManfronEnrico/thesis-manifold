"""
Stage 1 — JSONL → Parquet Cache (Single Category)
==================================================
Converts all Nielsen JSONL files for one category into Parquet, mirroring
filenames and folder structure.

Input  (read):  thesis/data/raw/nielsen/data_jsonl/{Category}/{views,metadata}/*.jsonl
Output (write): thesis/data/converted/nielsen/parquet_nielsen/{Category}/{views,metadata}/*.parquet

The Parquet outputs are read by the Stage 2 feature-engineering scripts
(`preprocessing_<category>.py`). Stage 2 hard-fails if these files are missing.

Idempotent: skips conversion when the destination Parquet exists and is newer
than the source JSONL. Pass --force to re-convert unconditionally.

Usage:
  python convert_category.py --category CSD
  python convert_category.py --category Energidrikke --force
"""

import sys
import argparse
import importlib
import time
from pathlib import Path

import pandas as pd

# ============================================================================
# CENTRALIZED PATHS
# ============================================================================

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

from PATHS import (
    THESIS_DATA_RAW_NIELSEN_JSONL_DIR,
    get_category_views_dir,
    get_category_metadata_dir,
)

VALID_CATEGORIES = ["CSD", "Energidrikke", "Danskvand", "RTD", "Totalbeer"]


# ============================================================================
# CONVERSION
# ============================================================================

def _is_up_to_date(src_jsonl: Path, dst_parquet: Path) -> bool:
    """True if dst exists and is newer than src."""
    if not dst_parquet.exists():
        return False
    return dst_parquet.stat().st_mtime >= src_jsonl.stat().st_mtime


def convert_one(src_jsonl: Path, dst_parquet: Path, force: bool) -> dict:
    """Convert a single JSONL → Parquet. Uses chunked reading for large files."""
    if not force and _is_up_to_date(src_jsonl, dst_parquet):
        return {"status": "skipped", "rows": None, "elapsed": 0.0}

    t0 = time.perf_counter()
    dst_parquet.parent.mkdir(parents=True, exist_ok=True)

    size_mb = src_jsonl.stat().st_size / (1024 * 1024)
    if size_mb > 100:
        # Chunked path for large files — avoids loading everything into RAM at once
        import pyarrow as pa
        import pyarrow.parquet as pq

        writer = None
        total_rows = 0
        for chunk in pd.read_json(src_jsonl, lines=True, chunksize=200_000):
            table = pa.Table.from_pandas(chunk, preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(dst_parquet, table.schema)
            writer.write_table(table)
            total_rows += len(chunk)
        if writer:
            writer.close()
        rows = total_rows
    else:
        df = pd.read_json(src_jsonl, lines=True)
        df.to_parquet(dst_parquet, index=False)
        rows = len(df)

    return {"status": "converted", "rows": rows, "elapsed": time.perf_counter() - t0}


def convert_subdir(src_dir: Path, dst_dir: Path, label: str, force: bool) -> int:
    """Convert every *.jsonl in src_dir to *.parquet in dst_dir. Returns count converted."""
    if not src_dir.exists():
        print(f"  ⚠ {label}: source dir not found ({src_dir}) — skipping")
        return 0

    jsonl_files = sorted(src_dir.glob("*.jsonl"))
    if not jsonl_files:
        print(f"  ⚠ {label}: no JSONL files in {src_dir} — skipping")
        return 0

    print(f"\n  {label}: {len(jsonl_files)} JSONL file(s) found")
    n_converted = 0
    for src in jsonl_files:
        dst = dst_dir / (src.stem + ".parquet")
        result = convert_one(src, dst, force)
        if result["status"] == "skipped":
            print(f"    · {src.name}: up-to-date (skipped)")
        else:
            print(f"    ✓ {src.name} → {dst.name}: "
                  f"{result['rows']:,} rows in {result['elapsed']:.1f}s")
            n_converted += 1
    return n_converted


def convert_category(category: str, force: bool = False) -> dict:
    """Convert all views/ + metadata/ JSONL files for one category."""
    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"Unknown category '{category}'. Expected one of: {VALID_CATEGORIES}"
        )

    src_views = THESIS_DATA_RAW_NIELSEN_JSONL_DIR / category / "views"
    src_metadata = THESIS_DATA_RAW_NIELSEN_JSONL_DIR / category / "metadata"
    dst_views = get_category_views_dir(category)
    dst_metadata = get_category_metadata_dir(category)

    print("=" * 80)
    print(f"Stage 1 — Converting JSONL → Parquet: {category}")
    print("=" * 80)
    print(f"  Source views:    {src_views}")
    print(f"  Source metadata: {src_metadata}")
    print(f"  Dest views:      {dst_views}")
    print(f"  Dest metadata:   {dst_metadata}")
    print(f"  Force re-convert: {force}")

    t0 = time.perf_counter()
    n_views = convert_subdir(src_views, dst_views, "views", force)
    n_meta = convert_subdir(src_metadata, dst_metadata, "metadata", force)
    elapsed = time.perf_counter() - t0

    print(f"\n  ✓ {category}: converted {n_views + n_meta} file(s) "
          f"({n_views} views + {n_meta} metadata) in {elapsed:.1f}s\n")

    return {"category": category, "views_converted": n_views,
            "metadata_converted": n_meta, "elapsed": elapsed}


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Convert Nielsen JSONL files to Parquet for one category."
    )
    parser.add_argument(
        "--category",
        required=True,
        choices=VALID_CATEGORIES,
        help="Category to convert.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-convert even if Parquet is newer than JSONL.",
    )
    args = parser.parse_args()

    convert_category(args.category, force=args.force)


if __name__ == "__main__":
    main()
