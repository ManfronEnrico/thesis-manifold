"""
Step 01 — Data ingestion (raw).

Pulls source data into the data/raw/ tree as Parquet:
  • Baseline feature matrix (frozen input from 2026-04-13 aggregation)
  • Nielsen raw CSD facts (csd_clean_facts_v) + dim tables — for documentation
  • Indeks Danmark CSVs (data, metadata, codebook)

Design decisions (documented here so Enrico can audit):
  • We do NOT re-aggregate Nielsen from raw facts in this pipeline. The baseline
    feature_matrix.parquet from 2026-04-13 represents the canonical aggregation.
    Re-aggregating risks producing different numbers from baseline, which would
    contaminate the comparison.
  • Nielsen raw is snapshotted for traceability + future feature engineering
    (e.g. brand-level marketing mix that isn't in the baseline FM).
  • Indeks is ingested in full — its role is cross-source feature enrichment
    (brand awareness / penetration) in Step 04.

Usage:
    uv run python -m scripts.ml_retraining.01_ingest_raw
"""
from __future__ import annotations

import hashlib
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import polars as pl
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RESULTS_ROOT = PROJECT_ROOT / "results" / "ml_retrain_2026-04-16"
BASELINE_FM = PROJECT_ROOT / "results" / "phase1" / "feature_matrix.parquet"

INDEKS_DIR = PROJECT_ROOT / "Thesis" / "indeksdanmark"
INDEKS_FILES = {
    "indeks_data": INDEKS_DIR / "indeksdanmark_data.csv",
    "indeks_metadata": INDEKS_DIR / "indeksdanmark_metadata.csv",
    "indeks_codebook": INDEKS_DIR / "official_codebook.csv",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def log_append(msg: str) -> None:
    with open(RESULTS_ROOT / "run_log.txt", "a") as f:
        f.write(msg + "\n")


def header(title: str) -> None:
    print("\n" + "=" * 72)
    print(f"  {title}")
    print("=" * 72)


# ---------------------------------------------------------------------------
# 1. Baseline feature matrix (frozen input)
# ---------------------------------------------------------------------------
def ingest_baseline() -> dict:
    header("1/3 Baseline feature matrix")
    src = BASELINE_FM
    dst = RAW_DIR / "feature_matrix_baseline.parquet"
    shutil.copy2(src, dst)
    df = pl.read_parquet(dst)
    info = {
        "source": str(src.relative_to(PROJECT_ROOT)),
        "target": str(dst.relative_to(PROJECT_ROOT)),
        "rows": df.height,
        "cols": df.width,
        "size_mb": dst.stat().st_size / 1e6,
        "sha256": sha256(dst),
    }
    print(f"  ✅ {info['rows']:,} rows × {info['cols']} cols  →  "
          f"{info['target']}  ({info['size_mb']:.2f} MB)")
    print(f"     sha256={info['sha256'][:16]}…")
    return info


# ---------------------------------------------------------------------------
# 2. Nielsen raw snapshot (CSD facts + dim tables)
# ---------------------------------------------------------------------------
def ingest_nielsen() -> list[dict]:
    header("2/3 Nielsen raw snapshot (CSD + dims)")
    # Import here so that module loads even if .env is misconfigured
    sys.path.insert(0, str(PROJECT_ROOT))
    from datasets.nielsen_connector import get_connection

    # Which tables to pull. We grab the CSD aggregate + its dim tables.
    # Kept small to avoid a 2.5M-row dump for nothing.
    tables = [
        ("csd_clean_facts_v", None),       # full facts table — the core
        ("csd_clean_dim_brand", None),     # brand metadata
        ("csd_clean_dim_product", None),   # product metadata
        ("csd_clean_dim_market", None),    # market metadata
        ("csd_clean_dim_period", None),    # period/date metadata
    ]
    out: list[dict] = []
    conn = get_connection()
    try:
        for table, where in tables:
            t0 = time.time()
            query = f"SELECT * FROM dbo.{table}"
            if where:
                query += f" WHERE {where}"
            try:
                df = pd.read_sql(query, conn)
            except Exception as e:
                print(f"  ⚠️  {table}: query failed ({e})")
                continue
            # Convert to polars for consistent parquet write
            pdf = pl.from_pandas(df)
            dst = RAW_DIR / f"nielsen_{table}.parquet"
            pdf.write_parquet(dst, compression="snappy")
            info = {
                "table": table,
                "rows": pdf.height,
                "cols": pdf.width,
                "size_mb": dst.stat().st_size / 1e6,
                "sha256": sha256(dst),
                "elapsed_s": round(time.time() - t0, 1),
            }
            print(f"  ✅ {table:30s}  {info['rows']:>10,} rows × {info['cols']:>3} cols  "
                  f"{info['size_mb']:>7.2f} MB  ({info['elapsed_s']}s)")
            out.append(info)
    finally:
        conn.close()
    return out


# ---------------------------------------------------------------------------
# 3. Indeks Danmark (CSV → Parquet via Polars)
# ---------------------------------------------------------------------------
def ingest_indeks() -> list[dict]:
    header("3/3 Indeks Danmark (CSV → Parquet via polars)")
    out: list[dict] = []
    for name, src in INDEKS_FILES.items():
        t0 = time.time()
        # Polars handles the 266 MB data.csv far faster than pandas, with
        # automatic type inference. infer_schema_length=10000 gives stable
        # types for wide columns (6,364 in the big file).
        try:
            df = pl.read_csv(
                src,
                infer_schema_length=10000,
                ignore_errors=True,
                truncate_ragged_lines=True,
            )
        except Exception as e:
            print(f"  ⚠️  {name}: polars read failed, falling back to pandas ({e})")
            pdf = pd.read_csv(src, low_memory=False)
            df = pl.from_pandas(pdf)
        dst = RAW_DIR / f"{name}.parquet"
        df.write_parquet(dst, compression="snappy")
        info = {
            "name": name,
            "source_csv": str(src.relative_to(PROJECT_ROOT)),
            "target_parquet": str(dst.relative_to(PROJECT_ROOT)),
            "rows": df.height,
            "cols": df.width,
            "csv_mb": src.stat().st_size / 1e6,
            "parquet_mb": dst.stat().st_size / 1e6,
            "compression_ratio": round(src.stat().st_size / dst.stat().st_size, 1),
            "sha256": sha256(dst),
            "elapsed_s": round(time.time() - t0, 1),
        }
        print(f"  ✅ {name:20s}  {info['rows']:>6,} rows × {info['cols']:>5} cols  "
              f"CSV {info['csv_mb']:>6.1f} MB → Parquet {info['parquet_mb']:>5.1f} MB  "
              f"({info['compression_ratio']}x, {info['elapsed_s']}s)")
        out.append(info)
    return out


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def write_report(baseline: dict, nielsen: list[dict], indeks: list[dict]) -> Path:
    header("Ingestion report")
    report_path = RESULTS_ROOT / "ingestion_report.md"
    lines: list[str] = []
    lines.append("# Step 01 — Ingestion report")
    lines.append(f"_Generated {datetime.now().isoformat(timespec='seconds')}_\n")

    lines.append("## Baseline feature matrix (frozen input)")
    lines.append(f"- Source: `{baseline['source']}`")
    lines.append(f"- Target: `{baseline['target']}`")
    lines.append(f"- Size: {baseline['size_mb']:.2f} MB  ({baseline['rows']:,} rows × {baseline['cols']} cols)")
    lines.append(f"- SHA256: `{baseline['sha256']}`\n")

    lines.append("## Nielsen raw tables")
    lines.append("| Table | Rows | Cols | Size (MB) | SHA256 (prefix) |")
    lines.append("|---|---:|---:|---:|:---|")
    for t in nielsen:
        lines.append(f"| {t['table']} | {t['rows']:,} | {t['cols']} | {t['size_mb']:.2f} | `{t['sha256'][:16]}…` |")
    lines.append("")

    lines.append("## Indeks Danmark")
    lines.append("| File | Rows | Cols | CSV (MB) | Parquet (MB) | Ratio | SHA256 (prefix) |")
    lines.append("|---|---:|---:|---:|---:|---:|:---|")
    for t in indeks:
        lines.append(f"| {t['name']} | {t['rows']:,} | {t['cols']} | "
                     f"{t['csv_mb']:.1f} | {t['parquet_mb']:.1f} | "
                     f"{t['compression_ratio']}x | `{t['sha256'][:16]}…` |")
    lines.append("")

    lines.append("## Design decisions\n")
    lines.append("- Baseline FM is the frozen input for modelling. Raw Nielsen is snapshotted for audit + future FE.")
    lines.append("- Nielsen re-aggregation deliberately NOT performed (would risk drift from baseline numbers).")
    lines.append("- Indeks converted to Parquet via `polars` for 5–10× read speedup downstream.")
    lines.append("- All artefacts idempotent: re-running overwrites safely.")

    report_path.write_text("\n".join(lines))
    print(f"  ✅ {report_path.relative_to(PROJECT_ROOT)}")
    return report_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    t_start = time.time()
    log_append(f"\n=== Step 01 INGEST @ {datetime.now().isoformat(timespec='seconds')} ===")

    try:
        baseline = ingest_baseline()
        nielsen = ingest_nielsen()
        indeks = ingest_indeks()
        report = write_report(baseline, nielsen, indeks)
    except Exception as e:
        log_append(f"FAIL: {type(e).__name__}: {e}")
        print(f"\n  ❌ Step 01 FAILED: {type(e).__name__}: {e}")
        return 1

    elapsed = time.time() - t_start
    log_append(f"OK — baseline + {len(nielsen)} Nielsen tables + {len(indeks)} Indeks files  ({elapsed:.1f}s)")

    print("\n" + "=" * 72)
    print(f"  ✅ STEP 01 COMPLETE  ({elapsed:.1f}s)  — ready for Step 02")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
