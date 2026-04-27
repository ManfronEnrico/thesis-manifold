"""
Step 06 — Preprocessing pipeline (scikit-learn).

Builds two preprocessing pipelines, fit on TRAIN only, and saves them as
pickles for reuse in Steps 07–09:

  • pipe_linear: for linear/classical models (OLS, Ridge, ARIMA exogenous)
      – median impute → StandardScaler for numerics
      – one-hot encode 'brand' (drop first to avoid collinearity)
  • pipe_tree: for tree ensembles (LightGBM, XGBoost)
      – median impute → passthrough (no scaling)
      – OrdinalEncoder for 'brand' (trees handle this natively)

We also define feature column lists (`FEATURE_COLS_NUMERIC`, `FEATURE_COLS_CAT`)
so Steps 07–08 can import them.

Usage:
    uv run python -m scripts.ml_retraining.06_preprocessing_pipeline
"""
from __future__ import annotations

import json
import pickle
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SPLITS_DIR = PROJECT_ROOT / "data" / "splits"
PIPELINES_DIR = PROJECT_ROOT / "pipelines"
RESULTS_ROOT = PROJECT_ROOT / "results" / "ml_retrain_2026-04-16"

# Columns that are NOT features: target, identifiers, splits, *contemporaneous
# functions of the target* (would leak the answer). These are the columns Phase-1
# v2 also excluded (see ai_research_framework/agents/global_model_v2.py:38–45).
NON_FEATURES = {
    # Identifiers / bookkeeping
    "date", "brand", "split", "cv_fold",
    # Target (raw + log)
    "sales_units", "log_sales_units",
    # Contemporaneous functions of the target — LEAKAGE if used as features
    "sales_value",     # = price × sales_units at time t
    "sales_liters",    # = volume-per-unit × sales_units at time t
    "promo_units",     # = promo share × sales_units at time t
}


def header(t: str) -> None:
    print("\n" + "=" * 72)
    print(f"  {t}")
    print("=" * 72)


def log(msg: str) -> None:
    with open(RESULTS_ROOT / "run_log.txt", "a") as f:
        f.write(msg + "\n")


def build_pipelines(train_df: pd.DataFrame) -> dict:
    numeric_cols = [
        c for c in train_df.columns
        if c not in NON_FEATURES and train_df[c].dtype.kind in ("i", "f", "b")
    ]
    cat_cols = ["brand"]
    print(f"  numeric features ({len(numeric_cols)}): {numeric_cols[:8]}...")
    print(f"  categorical features: {cat_cols}")

    # Linear pipeline: standardize numerics, one-hot encode brand
    pipe_linear = ColumnTransformer(
        [
            ("num", Pipeline([
                ("imp", SimpleImputer(strategy="median")),
                ("sc", StandardScaler()),
            ]), numeric_cols),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False),
             cat_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    # Tree pipeline: impute only; ordinal encode brand
    pipe_tree = ColumnTransformer(
        [
            ("num", SimpleImputer(strategy="median"), numeric_cols),
            ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
             cat_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    # Fit on TRAIN
    pipe_linear.fit(train_df)
    pipe_tree.fit(train_df)

    # Sanity shape checks
    X_linear = pipe_linear.transform(train_df)
    X_tree = pipe_tree.transform(train_df)
    print(f"  pipe_linear output shape: {X_linear.shape}")
    print(f"  pipe_tree   output shape: {X_tree.shape}")

    return {
        "pipe_linear": pipe_linear,
        "pipe_tree": pipe_tree,
        "numeric_cols": numeric_cols,
        "cat_cols": cat_cols,
        "out_shape_linear": list(X_linear.shape),
        "out_shape_tree": list(X_tree.shape),
    }


def main() -> int:
    t0 = time.time()
    log(f"\n=== Step 06 PIPELINE @ {datetime.now().isoformat(timespec='seconds')} ===")

    header("1/2 Fitting preprocessing pipelines on TRAIN")
    df = pd.read_parquet(SPLITS_DIR / "feature_matrix_v3_split.parquet")
    train_df = df[df["split"] == "train"].reset_index(drop=True)
    print(f"  TRAIN rows: {len(train_df):,}  cols: {len(train_df.columns)}")

    pipes = build_pipelines(train_df)

    header("2/2 Saving pipelines + feature lists")
    PIPELINES_DIR.mkdir(parents=True, exist_ok=True)

    linear_path = PIPELINES_DIR / "pipe_linear.pkl"
    tree_path = PIPELINES_DIR / "pipe_tree.pkl"
    with open(linear_path, "wb") as f:
        pickle.dump(pipes["pipe_linear"], f)
    with open(tree_path, "wb") as f:
        pickle.dump(pipes["pipe_tree"], f)
    print(f"  ✅ {linear_path.relative_to(PROJECT_ROOT)}")
    print(f"  ✅ {tree_path.relative_to(PROJECT_ROOT)}")

    # Save feature lists as JSON for easy consumption in Steps 07–08
    feature_lists = {
        "numeric_cols": pipes["numeric_cols"],
        "cat_cols": pipes["cat_cols"],
        "non_features": sorted(NON_FEATURES),
        "target_raw": "sales_units",
        "target_log": "log_sales_units",
        "out_shape_linear": pipes["out_shape_linear"],
        "out_shape_tree": pipes["out_shape_tree"],
    }
    features_json = PIPELINES_DIR / "feature_lists.json"
    features_json.write_text(json.dumps(feature_lists, indent=2))
    print(f"  ✅ {features_json.relative_to(PROJECT_ROOT)}")

    elapsed = time.time() - t0
    log(f"OK — pipe_linear + pipe_tree  ({elapsed:.1f}s)")
    print("\n" + "=" * 72)
    print(f"  ✅ STEP 06 COMPLETE  ({elapsed:.1f}s)  — ready for Step 07")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
