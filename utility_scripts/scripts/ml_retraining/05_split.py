"""
Step 05 — Dataset splitting.

Applies the frozen SRQ1 split from thesis/analysis/outputs/phase1/split_dates.json and
produces walk-forward CV folds on the TRAIN window for hyperparameter
tuning in Step 08.

Splits:
  • train: 2022-10 → 2025-02  (29 months)
  • val  : 2025-03 → 2025-08  ( 6 months)
  • test : 2025-09 → 2026-03  ( 7 months) — held out, never touched in Step 06–09
  • CV   : 5 expanding-window folds inside TRAIN (each val horizon = 3 months)

Outputs:
  data/splits/feature_matrix_v3_split.parquet   # adds 'cv_fold' column
  data/splits/split_manifest.json                # dates, row counts, brand counts

Usage:
    uv run python -m scripts.ml_retraining.05_split
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FEATURES_DIR = PROJECT_ROOT / "data" / "features"
SPLITS_DIR = PROJECT_ROOT / "data" / "splits"
RESULTS_ROOT = PROJECT_ROOT / "results" / "ml_retrain_2026-04-16"
SPLIT_DATES = PROJECT_ROOT / "results" / "phase1" / "split_dates.json"


def header(t: str) -> None:
    print("\n" + "=" * 72)
    print(f"  {t}")
    print("=" * 72)


def log(msg: str) -> None:
    with open(RESULTS_ROOT / "run_log.txt", "a") as f:
        f.write(msg + "\n")


# ---------------------------------------------------------------------------
# Walk-forward CV fold assignment (within TRAIN only)
# ---------------------------------------------------------------------------
def assign_cv_folds(train_df: pd.DataFrame, n_folds: int = 5, horizon: int = 3) -> pd.Series:
    """
    Expanding-window folds:
      fold 0: train up to (train_end - 5*horizon), val = next `horizon` months
      ...
      fold 4: train up to (train_end - 1*horizon), val = next `horizon` months
      Rows outside any validation window get cv_fold = -1 (train-only).
    """
    fold = pd.Series(-1, index=train_df.index, dtype="int8")
    dates_sorted = sorted(train_df["date"].unique())
    # Month positions
    for i in range(n_folds):
        # Validation window = months [-(n_folds-i)*horizon : -(n_folds-i-1)*horizon)
        lo_idx = len(dates_sorted) - (n_folds - i) * horizon
        hi_idx = lo_idx + horizon
        if lo_idx < 0:
            continue
        val_months = set(dates_sorted[lo_idx:hi_idx])
        mask = train_df["date"].isin(val_months)
        fold.loc[mask] = i
    return fold


def main() -> int:
    t0 = time.time()
    log(f"\n=== Step 05 SPLIT @ {datetime.now().isoformat(timespec='seconds')} ===")

    header("1/2 Applying frozen split + CV folds")
    split_dates = json.loads(SPLIT_DATES.read_text())
    print(f"  Frozen split from {SPLIT_DATES.relative_to(PROJECT_ROOT)}:")
    for k, v in split_dates.items():
        print(f"    {k:12s} {v}")

    src = FEATURES_DIR / "feature_matrix_v3.parquet"
    df = pd.read_parquet(src)
    df["date"] = pd.to_datetime(df["date"])

    # Re-derive split just to be safe (matches the 'split' column from baseline)
    train_end = pd.to_datetime(split_dates["train_end"])
    val_start = pd.to_datetime(split_dates["val_start"])
    val_end = pd.to_datetime(split_dates["val_end"])
    test_start = pd.to_datetime(split_dates["test_start"])

    derived = np.where(
        df["date"] <= train_end, "train",
        np.where(df["date"] < test_start, "val", "test"),
    )
    # Report mismatch vs existing 'split' column if any
    mismatch = int((derived != df["split"]).sum())
    print(f"  Derived vs existing split column — mismatches: {mismatch}")

    # Assign CV folds on TRAIN rows only
    df["cv_fold"] = -1
    train_mask = df["split"] == "train"
    df.loc[train_mask, "cv_fold"] = assign_cv_folds(df[train_mask], n_folds=5, horizon=3).values

    # Row counts by split
    by_split = df["split"].value_counts().to_dict()
    by_fold = df.loc[train_mask, "cv_fold"].value_counts().sort_index().to_dict()
    print(f"  Rows by split: {by_split}")
    print(f"  CV fold counts (within TRAIN): {by_fold}")

    # Sanity: no brand should be missing from train
    train_brands = set(df.loc[train_mask, "brand"].unique())
    all_brands = set(df["brand"].unique())
    missing_brands = all_brands - train_brands
    print(f"  Brands in TRAIN: {len(train_brands)}/{len(all_brands)}  missing={sorted(missing_brands) or 'none'}")

    # Write
    SPLITS_DIR.mkdir(parents=True, exist_ok=True)
    out = SPLITS_DIR / "feature_matrix_v3_split.parquet"
    df.to_parquet(out, engine="pyarrow", compression="snappy", index=False)
    print(f"  ✅ {out.relative_to(PROJECT_ROOT)}  ({df.shape[0]:,} rows)")

    header("2/2 Split manifest")
    manifest = {
        "split_dates": split_dates,
        "rows_per_split": by_split,
        "brands_per_split": {
            s: int(df.loc[df["split"] == s, "brand"].nunique())
            for s in ("train", "val", "test")
        },
        "cv_folds": {
            "scheme": "expanding_window",
            "n_folds": 5,
            "horizon_months": 3,
            "counts": {int(k): int(v) for k, v in by_fold.items()},
        },
        "output_file": str(out.relative_to(PROJECT_ROOT)),
        "derivation_mismatch": mismatch,
    }
    manifest_path = SPLITS_DIR / "split_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str))
    print(f"  ✅ {manifest_path.relative_to(PROJECT_ROOT)}")

    elapsed = time.time() - t0
    log(f"OK — split + 5 CV folds  ({elapsed:.1f}s)")
    print("\n" + "=" * 72)
    print(f"  ✅ STEP 05 COMPLETE  ({elapsed:.1f}s)  — ready for Step 06")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
