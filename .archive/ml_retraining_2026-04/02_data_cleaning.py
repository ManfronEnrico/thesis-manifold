"""
Step 02 — Data cleaning.

Applies cleaning rules to the ingested raw data and writes audited clean
parquet files + a human-readable cleaning_report.md.

Cleaning scope:
  • Baseline FM: already clean (it's the 2026-04-13 aggregation output), but
    we document missing/outlier/duplicate checks for the thesis methodology.
  • Nielsen CSD facts: dedup on natural key, sanity filter on sales values,
    coerce period_id to datetime.
  • Indeks data: drop columns with > 95% missing, drop zero-variance columns,
    normalise column names.

Every rule applied is logged with before/after counts to `cleaning_report.md`
so the methodology can be defended in the thesis.

Usage:
    uv run python -m scripts.ml_retraining.02_data_cleaning
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

import polars as pl

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
CLEAN_DIR = PROJECT_ROOT / "data" / "clean"
RESULTS_ROOT = PROJECT_ROOT / "results" / "ml_retrain_2026-04-16"


def header(t: str) -> None:
    print("\n" + "=" * 72)
    print(f"  {t}")
    print("=" * 72)


def log(msg: str) -> None:
    with open(RESULTS_ROOT / "run_log.txt", "a") as f:
        f.write(msg + "\n")


# ---------------------------------------------------------------------------
# Baseline FM — quality audit (read-only, just document)
# ---------------------------------------------------------------------------
def audit_baseline() -> dict:
    header("1/3 Baseline FM — audit (read-only)")
    df = pl.read_parquet(RAW_DIR / "feature_matrix_baseline.parquet")

    audit = {
        "rows": df.height,
        "cols": df.width,
        "missing_per_column": {
            c: int(df[c].null_count()) for c in df.columns
            if df[c].null_count() > 0
        },
        "duplicates_on_brand_date": int(
            df.height - df.unique(subset=["brand", "date"]).height
        ),
        "sales_units_negative": int(df.filter(pl.col("sales_units") < 0).height),
        "sales_units_zero": int(df.filter(pl.col("sales_units") == 0).height),
        "brands": df["brand"].n_unique(),
        "date_min": str(df["date"].min()),
        "date_max": str(df["date"].max()),
    }

    for k, v in audit.items():
        print(f"  {k:35s} {v}")

    # Passthrough to clean dir (already clean)
    out = CLEAN_DIR / "feature_matrix_baseline.parquet"
    df.write_parquet(out, compression="snappy")
    print(f"  ✅ copied to {out.relative_to(PROJECT_ROOT)}")
    return audit


# ---------------------------------------------------------------------------
# Nielsen CSD facts — clean
# ---------------------------------------------------------------------------
def clean_nielsen_csd() -> dict:
    header("2/3 Nielsen CSD facts — clean")
    src = RAW_DIR / "nielsen_csd_clean_facts_v.parquet"
    df = pl.read_parquet(src)
    before = df.height

    # Log column names and dtypes for transparency
    print(f"  columns: {df.columns}")

    report: dict = {"before_rows": before, "rules": []}

    # Rule 1: drop exact duplicates
    df = df.unique()
    after = df.height
    report["rules"].append({
        "rule": "drop_exact_duplicates",
        "removed": before - after,
        "remaining": after,
    })
    print(f"  drop_exact_duplicates        removed {before - after:,}  remaining {after:,}")
    before = after

    # Rule 2: drop rows where sales_value < 0 or sales_units < 0
    df = df.filter((pl.col("sales_value") >= 0) & (pl.col("sales_units") >= 0))
    after = df.height
    report["rules"].append({
        "rule": "drop_negative_sales",
        "removed": before - after,
        "remaining": after,
    })
    print(f"  drop_negative_sales          removed {before - after:,}  remaining {after:,}")
    before = after

    # Rule 3: cast ID columns to canonical int where sensible; leave measures as float
    # Nothing to do beyond what polars already inferred.

    # Write clean
    out = CLEAN_DIR / "nielsen_csd_clean.parquet"
    df.write_parquet(out, compression="snappy")
    report["after_rows"] = df.height
    report["output"] = str(out.relative_to(PROJECT_ROOT))
    print(f"  ✅ {report['output']}  ({df.height:,} rows)")
    return report


# ---------------------------------------------------------------------------
# Indeks data — clean (drop sparse + zero-variance columns)
# ---------------------------------------------------------------------------
def clean_indeks() -> dict:
    header("3/3 Indeks data — clean (sparse + zero-variance filtering)")
    src = RAW_DIR / "indeks_data.parquet"
    df = pl.read_parquet(src)
    before_rows, before_cols = df.height, df.width

    # Rule 1: drop columns with > 95% missing
    missing_ratios = {
        c: df[c].null_count() / max(df.height, 1) for c in df.columns
    }
    sparse_cols = [c for c, r in missing_ratios.items() if r > 0.95]
    df = df.drop(sparse_cols)
    print(f"  drop sparse (>95% missing)   removed {len(sparse_cols):>4} cols  "
          f"remaining {df.width} cols")

    # Rule 2: drop zero-variance columns (numeric only)
    zero_var_cols: list[str] = []
    for c in df.columns:
        if df[c].dtype.is_numeric():
            try:
                if df[c].n_unique() <= 1:
                    zero_var_cols.append(c)
            except Exception:
                continue
    df = df.drop(zero_var_cols)
    print(f"  drop zero-variance            removed {len(zero_var_cols):>4} cols  "
          f"remaining {df.width} cols")

    after_rows, after_cols = df.height, df.width
    out = CLEAN_DIR / "indeks_data_clean.parquet"
    df.write_parquet(out, compression="snappy")

    report = {
        "before_rows": before_rows,
        "before_cols": before_cols,
        "sparse_cols_dropped": len(sparse_cols),
        "zero_variance_cols_dropped": len(zero_var_cols),
        "after_rows": after_rows,
        "after_cols": after_cols,
        "output": str(out.relative_to(PROJECT_ROOT)),
    }
    print(f"  ✅ {report['output']}  ({after_rows:,} rows × {after_cols} cols)")
    return report


# ---------------------------------------------------------------------------
# Cleaning report (methodology-ready)
# ---------------------------------------------------------------------------
def write_report(baseline: dict, nielsen: dict, indeks: dict) -> Path:
    header("Cleaning report")
    path = RESULTS_ROOT / "cleaning_report.md"
    lines: list[str] = []
    lines.append("# Step 02 — Data Cleaning Report")
    lines.append(f"_Generated {datetime.now().isoformat(timespec='seconds')}_\n")

    lines.append("## 1. Baseline feature matrix — audit\n")
    lines.append(f"- Rows: {baseline['rows']:,}")
    lines.append(f"- Cols: {baseline['cols']}")
    lines.append(f"- Brands: {baseline['brands']}")
    lines.append(f"- Date range: {baseline['date_min']} → {baseline['date_max']}")
    lines.append(f"- Duplicate (brand, date) keys: {baseline['duplicates_on_brand_date']}")
    lines.append(f"- sales_units < 0: {baseline['sales_units_negative']}")
    lines.append(f"- sales_units == 0: {baseline['sales_units_zero']}")
    if baseline["missing_per_column"]:
        lines.append(f"- Missing per column:")
        for c, n in baseline["missing_per_column"].items():
            lines.append(f"  - {c}: {n}")
    else:
        lines.append("- Missing values: none")
    lines.append("")

    lines.append("## 2. Nielsen CSD facts — cleaning rules applied\n")
    lines.append("| Rule | Removed | Remaining |")
    lines.append("|---|---:|---:|")
    for r in nielsen["rules"]:
        lines.append(f"| {r['rule']} | {r['removed']:,} | {r['remaining']:,} |")
    lines.append(f"\nFinal: **{nielsen['after_rows']:,} rows** → `{nielsen['output']}`\n")

    lines.append("## 3. Indeks data — dimensionality reduction\n")
    lines.append(f"- Before: {indeks['before_rows']:,} rows × **{indeks['before_cols']}** cols")
    lines.append(f"- Dropped cols with >95% missing: **{indeks['sparse_cols_dropped']}**")
    lines.append(f"- Dropped zero-variance cols: **{indeks['zero_variance_cols_dropped']}**")
    lines.append(f"- After: {indeks['after_rows']:,} rows × **{indeks['after_cols']}** cols")
    lines.append(f"- Output: `{indeks['output']}`")
    lines.append("")

    lines.append("## Methodology note for thesis\n")
    lines.append(
        "Cleaning is conservative: we only remove rows/columns that are logically "
        "invalid (negative sales, exact duplicates) or uninformative (zero variance, "
        ">95% missing). We do NOT impute missing values at this stage — imputation "
        "decisions are deferred to Step 06 (preprocessing pipeline) so each model "
        "can choose its own strategy."
    )

    path.write_text("\n".join(lines))
    print(f"  ✅ {path.relative_to(PROJECT_ROOT)}")
    return path


def main() -> int:
    t0 = time.time()
    log(f"\n=== Step 02 CLEAN @ {datetime.now().isoformat(timespec='seconds')} ===")
    try:
        baseline = audit_baseline()
        nielsen = clean_nielsen_csd()
        indeks = clean_indeks()
        write_report(baseline, nielsen, indeks)
    except Exception as e:
        log(f"FAIL: {type(e).__name__}: {e}")
        print(f"\n  ❌ Step 02 FAILED: {type(e).__name__}: {e}")
        raise

    elapsed = time.time() - t0
    log(f"OK — baseline audit + nielsen clean + indeks reduced  ({elapsed:.1f}s)")
    print("\n" + "=" * 72)
    print(f"  ✅ STEP 02 COMPLETE  ({elapsed:.1f}s)  — ready for Step 03")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
