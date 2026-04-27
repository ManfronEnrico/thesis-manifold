"""
Step 04 — Feature engineering.

Extends the baseline feature matrix (22 cols) with new engineered features
motivated by the EDA findings (STL seasonality + PACF autocorrelation):

  • Additional causal lags (lag_6, lag_12) — suggested by ACF tail.
  • Additional rolling stats (3-/6-month window means, medians, std).
  • Year-over-year growth (yoy_growth_12).
  • Cyclical month encoding (month_sin / month_cos) — replaces raw month.
  • Linear trend (months_since_start).
  • Unit price proxy (sales_value / sales_units).
  • Promo momentum (rolling mean of promo_intensity, 3 months).
  • Brand-level aggregates (mean/std/rank of sales) — TRAIN-only to avoid
    leakage.

All features are causal (past-only) so walk-forward validation in Step 05
remains honest.

Usage:
    uv run python -m scripts.ml_retraining.04_feature_engineering
"""
from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import polars as pl
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CLEAN_DIR = PROJECT_ROOT / "data" / "clean"
FEATURES_DIR = PROJECT_ROOT / "data" / "features"
RESULTS_ROOT = PROJECT_ROOT / "results" / "ml_retrain_2026-04-16"


def header(t: str) -> None:
    print("\n" + "=" * 72)
    print(f"  {t}")
    print("=" * 72)


def log(msg: str) -> None:
    with open(RESULTS_ROOT / "run_log.txt", "a") as f:
        f.write(msg + "\n")


# ---------------------------------------------------------------------------
# Feature builders (pandas for clarity — 3,234 rows is tiny)
# ---------------------------------------------------------------------------
def add_lags(df: pd.DataFrame, col: str, lags: list[int]) -> pd.DataFrame:
    for k in lags:
        name = f"{col}_lag_{k}"
        if name not in df.columns:
            df[name] = df.groupby("brand")[col].shift(k)
    return df


def add_rolling(df: pd.DataFrame, col: str, windows: list[int]) -> pd.DataFrame:
    for w in windows:
        # Causal rolling: shift by 1 so current row isn't part of its own mean.
        grp = df.groupby("brand")[col]
        df[f"{col}_rm_{w}"] = grp.transform(
            lambda s: s.shift(1).rolling(w, min_periods=1).mean()
        )
        df[f"{col}_rstd_{w}"] = grp.transform(
            lambda s: s.shift(1).rolling(w, min_periods=2).std()
        )
        df[f"{col}_rmedian_{w}"] = grp.transform(
            lambda s: s.shift(1).rolling(w, min_periods=1).median()
        )
    return df


def add_yoy(df: pd.DataFrame) -> pd.DataFrame:
    # Causal YoY growth: ratio of lag_1 to lag_13 (NOT current period vs lag_12,
    # which would leak the target). At forecast time for t, both lag_1 (= y_{t-1})
    # and lag_13 (= y_{t-13}) are known.
    df["sales_units_yoy_growth_lag1"] = df.groupby("brand")["sales_units"].transform(
        lambda s: (s.shift(1) - s.shift(13)) / s.shift(13).replace(0, np.nan)
    )
    return df


def add_cyclical(df: pd.DataFrame) -> pd.DataFrame:
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    return df


def add_trend(df: pd.DataFrame) -> pd.DataFrame:
    start = df["date"].min()
    df["months_since_start"] = (
        (df["date"].dt.year - start.year) * 12 + (df["date"].dt.month - start.month)
    )
    return df


def add_price_proxy(df: pd.DataFrame) -> pd.DataFrame:
    # Causal: unit price of previous month (shift by 1) to avoid leakage.
    grp = df.groupby("brand")
    prev_value = grp["sales_value"].shift(1)
    prev_units = grp["sales_units"].shift(1).replace(0, np.nan)
    df["unit_price_lag_1"] = prev_value / prev_units
    return df


def add_promo_momentum(df: pd.DataFrame) -> pd.DataFrame:
    df["promo_momentum_3"] = df.groupby("brand")["promo_intensity"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean()
    )
    return df


def add_brand_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Brand-level mean/std/rank computed on TRAIN rows only (no leakage)."""
    train = df[df["split"] == "train"]
    brand_stats = train.groupby("brand")["sales_units"].agg(
        brand_mean_sales="mean",
        brand_std_sales="std",
    )
    brand_stats["brand_rank"] = brand_stats["brand_mean_sales"].rank(
        method="dense", ascending=False
    ).astype(int)
    # Left join back onto the full df (test rows inherit brand-level priors).
    df = df.merge(brand_stats, on="brand", how="left")
    return df


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def build_features() -> dict:
    header("1/1 Building engineered feature matrix (v3)")
    src = CLEAN_DIR / "feature_matrix_baseline.parquet"
    df = pd.read_parquet(src)
    df = df.sort_values(["brand", "date"]).reset_index(drop=True)
    start_cols = df.shape[1]

    # 1. More causal lags motivated by ACF tail
    df = add_lags(df, "sales_units", [6, 12])
    # 2. Additional rolling windows
    df = add_rolling(df, "sales_units", [3, 6])
    # 3. YoY growth
    df = add_yoy(df)
    # 4. Cyclical seasonality
    df = add_cyclical(df)
    # 5. Linear trend
    df = add_trend(df)
    # 6. Unit price proxy (lagged)
    df = add_price_proxy(df)
    # 7. Promo momentum
    df = add_promo_momentum(df)
    # 8. Brand-level aggregates (train only)
    df = add_brand_aggregates(df)

    added_cols = df.shape[1] - start_cols
    print(f"  Added {added_cols} new columns (was {start_cols}, now {df.shape[1]})")

    out = FEATURES_DIR / "feature_matrix_v3.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, engine="pyarrow", compression="snappy", index=False)
    print(f"  ✅ {out.relative_to(PROJECT_ROOT)}  ({df.shape[0]:,} rows × {df.shape[1]} cols)")

    # Count missing per new column (for report)
    new_cols = [c for c in df.columns if c not in pd.read_parquet(src).columns]
    missing = {c: int(df[c].isna().sum()) for c in new_cols}

    return {
        "output": str(out.relative_to(PROJECT_ROOT)),
        "rows": int(df.shape[0]),
        "cols_before": start_cols,
        "cols_after": int(df.shape[1]),
        "new_columns": new_cols,
        "missing_per_new_col": missing,
    }


def write_report(info: dict) -> Path:
    path = RESULTS_ROOT / "feature_engineering_report.md"
    lines: list[str] = []
    lines.append("# Step 04 — Feature Engineering Report")
    lines.append(f"_Generated {datetime.now().isoformat(timespec='seconds')}_\n")
    lines.append(f"- Rows: {info['rows']:,}")
    lines.append(f"- Columns before: {info['cols_before']}")
    lines.append(f"- Columns after: {info['cols_after']}")
    lines.append(f"- Output: `{info['output']}`\n")
    lines.append("## New features added\n")
    lines.append("| Feature | Missing | Rationale |")
    lines.append("|---|---:|---|")
    rationale = {
        "sales_units_lag_6": "Half-year lag suggested by PACF shape.",
        "sales_units_lag_12": "Annual seasonality suggested by ACF peak at 12.",
        "sales_units_rm_3": "Short-run momentum (causal 3-month mean).",
        "sales_units_rstd_3": "Short-run volatility.",
        "sales_units_rmedian_3": "Robust short-run central tendency.",
        "sales_units_rm_6": "Medium-run trend.",
        "sales_units_rstd_6": "Medium-run volatility.",
        "sales_units_rmedian_6": "Robust medium-run central tendency.",
        "sales_units_yoy_growth_lag1": "Causal YoY growth: (lag_1 - lag_13)/lag_13.",
        "month_sin": "Cyclical seasonality encoding (sin component).",
        "month_cos": "Cyclical seasonality encoding (cos component).",
        "months_since_start": "Linear trend regressor.",
        "unit_price_lag_1": "Causal price proxy (sales_value / units, shifted).",
        "promo_momentum_3": "Rolling 3m promo intensity (causal).",
        "brand_mean_sales": "Brand-level baseline (TRAIN only, no leakage).",
        "brand_std_sales": "Brand-level dispersion (TRAIN only).",
        "brand_rank": "Brand volume rank (TRAIN only, dense rank).",
    }
    for c in info["new_columns"]:
        lines.append(f"| `{c}` | {info['missing_per_new_col'][c]} | {rationale.get(c, '—')} |")
    lines.append("")
    lines.append("## Leakage safeguards\n")
    lines.append("- All lags/rollings use causal shift (past-only).")
    lines.append("- Brand aggregates computed on TRAIN rows only, then broadcast.")
    lines.append("- Unit price proxy uses shift(1) — no contemporaneous info.")
    path.write_text("\n".join(lines))
    print(f"  ✅ {path.relative_to(PROJECT_ROOT)}")
    return path


def main() -> int:
    t0 = time.time()
    log(f"\n=== Step 04 FE @ {datetime.now().isoformat(timespec='seconds')} ===")
    try:
        info = build_features()
        write_report(info)
    except Exception as e:
        log(f"FAIL: {type(e).__name__}: {e}")
        print(f"\n  ❌ Step 04 FAILED: {type(e).__name__}: {e}")
        raise

    elapsed = time.time() - t0
    log(f"OK — feature_matrix_v3.parquet  ({elapsed:.1f}s)")
    print("\n" + "=" * 72)
    print(f"  ✅ STEP 04 COMPLETE  ({elapsed:.1f}s)  — ready for Step 05")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
