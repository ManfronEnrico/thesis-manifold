"""
Step 07 — Baseline models (sanity gate G2).

Trains four baselines on TRAIN, evaluates on VAL (untouched until Step 10):

  • SeasonalNaive   — y_hat_t = y_{t-12}  (per brand, deterministic)
  • NaiveMean       — y_hat_t = mean(train_y) per brand
  • OLS (global)    — LinearRegression on pipe_linear features
  • Ridge (global)  — RidgeCV on pipe_linear features (alphas = log-spaced)
  • ARIMA (per-brand top-10) — statsmodels SARIMAX(1,1,1)(1,1,1,12), only the
    10 highest-volume brands to keep runtime bounded.

Metrics (macro across brands, on VAL):
  median MAPE, mean MAPE, WAPE, RMSE, MAE

Outputs:
  thesis/analysis/outputs/ml_retrain_2026-04-16/baselines_val.csv       # per-brand / per-model rows
  thesis/analysis/outputs/ml_retrain_2026-04-16/baselines_summary.md    # ranking table
  thesis/analysis/outputs/ml_retrain_2026-04-16/models/*.pkl            # fitted pipelines (linear / ridge)

Usage:
    uv run python -m scripts.ml_retraining.07_baselines
"""
from __future__ import annotations

import json
import pickle
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.pipeline import Pipeline

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SPLITS_DIR = PROJECT_ROOT / "data" / "splits"
PIPELINES_DIR = PROJECT_ROOT / "pipelines"
RESULTS_ROOT = PROJECT_ROOT / "results" / "ml_retrain_2026-04-16"
MODELS_DIR = RESULTS_ROOT / "models"


def header(t: str) -> None:
    print("\n" + "=" * 72)
    print(f"  {t}")
    print("=" * 72)


def log(msg: str) -> None:
    with open(RESULTS_ROOT / "run_log.txt", "a") as f:
        f.write(msg + "\n")


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def mape(y_true, y_pred) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    mask = y_true > 0
    if mask.sum() == 0:
        return float("nan")
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def wape(y_true, y_pred) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    denom = np.abs(y_true).sum()
    if denom == 0:
        return float("nan")
    return float(np.abs(y_true - y_pred).sum() / denom * 100)


def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)))


def mae(y_true, y_pred) -> float:
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


# ---------------------------------------------------------------------------
# Per-brand baselines
# ---------------------------------------------------------------------------
def predict_seasonal_naive(train_full: pd.DataFrame, val: pd.DataFrame) -> pd.Series:
    """y_hat(brand, t) = actual sales 12 months earlier."""
    hist = pd.concat([train_full, val], axis=0).sort_values(["brand", "date"])
    hist["y_lag_12"] = hist.groupby("brand")["sales_units"].shift(12)
    # Pick the lag values at val rows
    val_idx = val.set_index(["brand", "date"]).index
    hist_idx = hist.set_index(["brand", "date"])
    preds = hist_idx.loc[val_idx, "y_lag_12"].values
    return pd.Series(preds, index=val.index, name="SeasonalNaive")


def predict_naive_mean(train: pd.DataFrame, val: pd.DataFrame) -> pd.Series:
    brand_mean = train.groupby("brand")["sales_units"].mean()
    return val["brand"].map(brand_mean).rename("NaiveMean")


# ---------------------------------------------------------------------------
# Global linear baselines
# ---------------------------------------------------------------------------
def fit_global_linear(train: pd.DataFrame, val: pd.DataFrame, target: str = "log_sales_units"):
    """Fits OLS + RidgeCV on pipe_linear, predicts on val. Returns (ols_pred, ridge_pred, models)."""
    with open(PIPELINES_DIR / "pipe_linear.pkl", "rb") as f:
        pre = pickle.load(f)
    X_train = pre.transform(train)
    X_val = pre.transform(val)
    y_train_log = train[target].values
    y_train_log = np.where(np.isfinite(y_train_log), y_train_log, 0.0)

    ols = LinearRegression()
    ols.fit(X_train, y_train_log)
    ridge = RidgeCV(alphas=np.logspace(-2, 3, 20))
    ridge.fit(X_train, y_train_log)

    # Back-transform log1p → sales_units
    ols_pred = np.expm1(ols.predict(X_val))
    ridge_pred = np.expm1(ridge.predict(X_val))
    # Clip negatives to 0 (no negative sales)
    ols_pred = np.clip(ols_pred, 0, None)
    ridge_pred = np.clip(ridge_pred, 0, None)
    return ols_pred, ridge_pred, {"ols": ols, "ridge": ridge, "ridge_alpha": float(ridge.alpha_)}


# ---------------------------------------------------------------------------
# ARIMA on top-10 volume brands
# ---------------------------------------------------------------------------
def fit_arima_top10(train: pd.DataFrame, val: pd.DataFrame) -> pd.Series:
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    top10 = (
        train.groupby("brand")["sales_units"].sum().nlargest(10).index.tolist()
    )
    print(f"  ARIMA on top-10 brands: {top10}")
    preds = pd.Series(np.nan, index=val.index, name="ARIMA")
    for b in top10:
        y_tr = train[train["brand"] == b].sort_values("date").set_index("date")["sales_units"].asfreq("MS").fillna(0)
        y_val = val[val["brand"] == b].sort_values("date")
        if len(y_tr) < 24:
            continue
        try:
            mod = SARIMAX(y_tr, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12),
                          enforce_stationarity=False, enforce_invertibility=False)
            res = mod.fit(disp=False)
            fc = res.forecast(steps=len(y_val))
            preds.loc[y_val.index] = np.clip(fc.values, 0, None)
        except Exception as e:
            print(f"    ARIMA failed for brand {b}: {type(e).__name__}")
    return preds


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
def evaluate(val: pd.DataFrame, preds: dict[str, pd.Series]) -> pd.DataFrame:
    rows: list[dict] = []
    for name, pred in preds.items():
        val_df = val.copy()
        val_df["y_pred"] = pred.values
        # Per-brand metrics
        for brand, g in val_df.groupby("brand"):
            yt, yp = g["sales_units"].values, g["y_pred"].values
            if np.isnan(yp).all():
                continue
            rows.append({
                "model": name,
                "brand": brand,
                "mape": mape(yt, yp),
                "wape": wape(yt, yp),
                "rmse": rmse(yt, yp),
                "mae": mae(yt, yp),
                "n": int(len(g)),
            })
    return pd.DataFrame(rows)


def summarise(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("model")
        .agg(
            n_brands=("brand", "nunique"),
            median_mape=("mape", "median"),
            mean_mape=("mape", "mean"),
            median_wape=("wape", "median"),
            mean_rmse=("rmse", "mean"),
            mean_mae=("mae", "mean"),
        )
        .sort_values("median_mape")
        .reset_index()
    )


def write_summary(summary: pd.DataFrame) -> Path:
    path = RESULTS_ROOT / "baselines_summary.md"
    lines = []
    lines.append("# Step 07 — Baselines Summary (VAL set)")
    lines.append(f"_Generated {datetime.now().isoformat(timespec='seconds')}_\n")
    lines.append("Evaluation window: VAL (Mar 2025 – Aug 2025, 6 months, 77 brands).")
    lines.append("Metric convention: median MAPE across brands (robust to outliers).\n")
    lines.append("## Ranking\n")
    cols = list(summary.columns)
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("|" + "|".join(["---"] * len(cols)) + "|")
    for _, row in summary.iterrows():
        vals = [
            f"{row[c]:.2f}" if isinstance(row[c], float) else str(row[c])
            for c in cols
        ]
        lines.append("| " + " | ".join(vals) + " |")
    lines.append("\n## Reference (Phase-1 benchmark, per-brand best-of)\n")
    lines.append("| Model         | Median MAPE |")
    lines.append("|---|---:|")
    lines.append("| LightGBM      | 31.03 |")
    lines.append("| Ensemble      | 31.59 |")
    lines.append("| XGBoost       | 32.84 |")
    lines.append("| Ridge (local) | 39.90 |")
    lines.append("| SeasonalNaive | 49.37 |")
    lines.append("| ARIMA         | 49.60 |")
    lines.append("| Prophet       | 58.61 |")
    path.write_text("\n".join(lines))
    return path


def main() -> int:
    t0 = time.time()
    log(f"\n=== Step 07 BASELINES @ {datetime.now().isoformat(timespec='seconds')} ===")

    header("1/3 Loading split data")
    df = pd.read_parquet(SPLITS_DIR / "feature_matrix_v3_split.parquet")
    df["date"] = pd.to_datetime(df["date"])
    train = df[df["split"] == "train"].reset_index(drop=True)
    val = df[df["split"] == "val"].reset_index(drop=True)
    train_full = df[df["split"].isin(["train"])].copy()
    print(f"  train={len(train):,}  val={len(val):,}  brands={df['brand'].nunique()}")

    header("2/3 Fitting baselines")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    t_sn = time.time()
    sn_pred = predict_seasonal_naive(train_full, val)
    print(f"  SeasonalNaive  ({time.time()-t_sn:.1f}s)")

    t_nm = time.time()
    nm_pred = predict_naive_mean(train, val)
    print(f"  NaiveMean      ({time.time()-t_nm:.1f}s)")

    t_lin = time.time()
    ols_pred, ridge_pred, lin_models = fit_global_linear(train, val)
    print(f"  OLS + Ridge    ({time.time()-t_lin:.1f}s)  ridge α={lin_models['ridge_alpha']:.3g}")
    with open(MODELS_DIR / "ols.pkl", "wb") as f:
        pickle.dump(lin_models["ols"], f)
    with open(MODELS_DIR / "ridge.pkl", "wb") as f:
        pickle.dump(lin_models["ridge"], f)

    t_ar = time.time()
    arima_pred = fit_arima_top10(train, val)
    print(f"  ARIMA top-10   ({time.time()-t_ar:.1f}s)")

    # Fill NaNs in pred Series with NaN (handled in evaluate)
    preds = {
        "SeasonalNaive": sn_pred,
        "NaiveMean": nm_pred,
        "OLS_global": pd.Series(ols_pred, index=val.index, name="OLS_global"),
        "Ridge_global": pd.Series(ridge_pred, index=val.index, name="Ridge_global"),
        "ARIMA_top10": arima_pred,
    }

    header("3/3 Evaluating + writing reports")
    per_brand = evaluate(val, preds)
    per_brand_path = RESULTS_ROOT / "baselines_val.csv"
    per_brand.to_csv(per_brand_path, index=False)
    print(f"  ✅ {per_brand_path.relative_to(PROJECT_ROOT)}  ({len(per_brand)} rows)")

    summary = summarise(per_brand)
    print("\n  Ranking (median MAPE):")
    print(summary.to_string(index=False))

    summary_path = write_summary(summary)
    print(f"\n  ✅ {summary_path.relative_to(PROJECT_ROOT)}")

    # Save preds for Step 10 plotting
    pred_df = val[["brand", "date", "sales_units"]].copy()
    for name, p in preds.items():
        pred_df[name] = p.values
    pred_df.to_parquet(RESULTS_ROOT / "baselines_predictions.parquet", index=False)
    print(f"  ✅ baselines_predictions.parquet ({len(pred_df):,} rows)")

    elapsed = time.time() - t0
    log(f"OK — {len(preds)} baselines evaluated  ({elapsed:.1f}s)")
    print("\n" + "=" * 72)
    print(f"  ✅ STEP 07 COMPLETE  ({elapsed:.1f}s)  — ready for Step 08")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
