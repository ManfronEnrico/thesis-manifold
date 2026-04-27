"""
Step 08 — Advanced models (core thesis comparison).

Four families, all trained on TRAIN, tuned on CV folds, evaluated on VAL:

  1. LightGBM (global, all brands)   — tuned via walk-forward CV on cv_fold
  2. XGBoost  (global, all brands)   — tuned via walk-forward CV on cv_fold
  3. PyMC hierarchical Bayesian      — partial pooling by brand, top-10 vol
                                        (ADVI for runtime); produces intervals
  4. aeon TimeCNN (per-brand, top-10) — deep learning univariate regressor
                                        as a modern benchmark

Target: log_sales_units; predictions back-transformed via expm1 and clipped ≥ 0.

Outputs:
  results/ml_retrain_2026-04-16/advanced_val.csv             # per-brand metrics
  results/ml_retrain_2026-04-16/advanced_predictions.parquet # merged predictions
  results/ml_retrain_2026-04-16/models/{lightgbm,xgboost}.pkl
  results/ml_retrain_2026-04-16/advanced_summary.md

Usage:
    uv run python -m scripts.ml_retraining.08_advanced_models
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

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

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
# Metrics (duplicated from Step 07 to keep step self-contained)
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
# Data loading helpers
# ---------------------------------------------------------------------------
def transform_tree(df: pd.DataFrame) -> np.ndarray:
    with open(PIPELINES_DIR / "pipe_tree.pkl", "rb") as f:
        pre = pickle.load(f)
    return pre.transform(df)


# ---------------------------------------------------------------------------
# 1. LightGBM global with walk-forward CV
# ---------------------------------------------------------------------------
def fit_lightgbm(train: pd.DataFrame, val: pd.DataFrame) -> tuple[np.ndarray, dict, object]:
    import lightgbm as lgb

    X_train = transform_tree(train)
    y_train = train["log_sales_units"].values

    X_val = transform_tree(val)

    # Small, defensible grid (keep training fast; matches Phase-1 search spirit)
    grid = [
        {"num_leaves": 31, "learning_rate": 0.05, "n_estimators": 800, "feature_fraction": 0.9, "min_data_in_leaf": 20},
        {"num_leaves": 63, "learning_rate": 0.05, "n_estimators": 600, "feature_fraction": 0.8, "min_data_in_leaf": 10},
        {"num_leaves": 15, "learning_rate": 0.08, "n_estimators": 500, "feature_fraction": 0.9, "min_data_in_leaf": 30},
        {"num_leaves": 31, "learning_rate": 0.03, "n_estimators": 1200, "feature_fraction": 0.85, "min_data_in_leaf": 20},
    ]

    fold_col = train["cv_fold"].values
    best_cfg, best_score = None, np.inf
    for cfg in grid:
        fold_scores = []
        for f in sorted(set(fold_col)):
            if f == -1:
                continue
            tr_mask = fold_col < f  # expanding window: all prior dates
            va_mask = fold_col == f
            if tr_mask.sum() < 100 or va_mask.sum() < 10:
                continue
            mdl = lgb.LGBMRegressor(
                objective="regression",
                random_state=42,
                verbose=-1,
                **cfg,
            )
            mdl.fit(X_train[tr_mask], y_train[tr_mask])
            y_pred_log = mdl.predict(X_train[va_mask])
            y_true = np.expm1(y_train[va_mask])
            y_pred = np.clip(np.expm1(y_pred_log), 0, None)
            fold_scores.append(mape(y_true, y_pred))
        cv_score = float(np.nanmedian(fold_scores)) if fold_scores else np.inf
        print(f"    cfg {cfg}  →  median CV MAPE {cv_score:.2f}")
        if cv_score < best_score:
            best_score, best_cfg = cv_score, cfg
    print(f"  best LGBM cfg: {best_cfg}  cv_median_mape={best_score:.2f}")

    # Refit on full TRAIN
    final = lgb.LGBMRegressor(objective="regression", random_state=42, verbose=-1, **best_cfg)
    final.fit(X_train, y_train)
    y_val_pred = np.clip(np.expm1(final.predict(X_val)), 0, None)
    return y_val_pred, {"best_cfg": best_cfg, "cv_median_mape": best_score}, final


# ---------------------------------------------------------------------------
# 2. XGBoost global with walk-forward CV
# ---------------------------------------------------------------------------
def fit_xgboost(train: pd.DataFrame, val: pd.DataFrame) -> tuple[np.ndarray, dict, object]:
    import xgboost as xgb

    X_train = transform_tree(train)
    y_train = train["log_sales_units"].values
    X_val = transform_tree(val)

    grid = [
        {"max_depth": 6, "learning_rate": 0.05, "n_estimators": 800, "subsample": 0.8, "colsample_bytree": 0.9},
        {"max_depth": 4, "learning_rate": 0.08, "n_estimators": 500, "subsample": 0.9, "colsample_bytree": 0.9},
        {"max_depth": 8, "learning_rate": 0.03, "n_estimators": 1200, "subsample": 0.8, "colsample_bytree": 0.8},
    ]

    fold_col = train["cv_fold"].values
    best_cfg, best_score = None, np.inf
    for cfg in grid:
        fold_scores = []
        for f in sorted(set(fold_col)):
            if f == -1:
                continue
            tr_mask = fold_col < f
            va_mask = fold_col == f
            if tr_mask.sum() < 100 or va_mask.sum() < 10:
                continue
            mdl = xgb.XGBRegressor(
                objective="reg:squarederror",
                random_state=42,
                tree_method="hist",
                verbosity=0,
                **cfg,
            )
            mdl.fit(X_train[tr_mask], y_train[tr_mask])
            y_pred_log = mdl.predict(X_train[va_mask])
            y_true = np.expm1(y_train[va_mask])
            y_pred = np.clip(np.expm1(y_pred_log), 0, None)
            fold_scores.append(mape(y_true, y_pred))
        cv_score = float(np.nanmedian(fold_scores)) if fold_scores else np.inf
        print(f"    cfg {cfg}  →  median CV MAPE {cv_score:.2f}")
        if cv_score < best_score:
            best_score, best_cfg = cv_score, cfg
    print(f"  best XGB cfg: {best_cfg}  cv_median_mape={best_score:.2f}")

    final = xgb.XGBRegressor(
        objective="reg:squarederror",
        random_state=42,
        tree_method="hist",
        verbosity=0,
        **best_cfg,
    )
    final.fit(X_train, y_train)
    y_val_pred = np.clip(np.expm1(final.predict(X_val)), 0, None)
    return y_val_pred, {"best_cfg": best_cfg, "cv_median_mape": best_score}, final


# ---------------------------------------------------------------------------
# 3. PyMC hierarchical Bayesian (top-10 brands)
# ---------------------------------------------------------------------------
def fit_pymc_hier(train: pd.DataFrame, val: pd.DataFrame) -> pd.Series:
    """
    Partial-pooling model on top-10 brands.
    log_y = α_brand + β_trend * t + γ_brand_sin * month_sin + γ_brand_cos * month_cos + ε

    Fit with ADVI (fast) — we take posterior mean for point forecasts.
    """
    import pymc as pm

    top10 = (
        train.groupby("brand")["sales_units"].sum().nlargest(10).index.tolist()
    )
    print(f"  PyMC on top-10 brands: {top10}")

    tr = train[train["brand"].isin(top10)].copy()
    va = val[val["brand"].isin(top10)].copy()

    brand_codes, brand_uniq = pd.factorize(tr["brand"])
    tr["brand_code"] = brand_codes
    va["brand_code"] = va["brand"].map({b: i for i, b in enumerate(brand_uniq)}).astype(int)

    # Standardize t (months since start) for numerical stability
    t_tr = tr["months_since_start"].values.astype(float)
    t_mean, t_std = t_tr.mean(), max(t_tr.std(), 1.0)
    t_tr_z = (t_tr - t_mean) / t_std
    t_va_z = (va["months_since_start"].values - t_mean) / t_std

    y_tr = tr["log_sales_units"].values.astype(float)

    # Empirical prior on brand intercept — keeps ADVI from diverging
    y_mean, y_std = float(np.mean(y_tr)), float(max(np.std(y_tr), 0.5))

    with pm.Model() as model:
        # Hyperpriors centred on empirical log-mean (top-10 brands, so y ~ 10–13)
        mu_alpha = pm.Normal("mu_alpha", y_mean, 2.0 * y_std)
        sigma_alpha = pm.HalfNormal("sigma_alpha", 2.0 * y_std)
        alpha = pm.Normal("alpha", mu_alpha, sigma_alpha, shape=len(brand_uniq))

        beta_trend = pm.Normal("beta_trend", 0.0, 1.0)

        mu_sin = pm.Normal("mu_sin", 0.0, 1.0)
        mu_cos = pm.Normal("mu_cos", 0.0, 1.0)
        sigma_sc = pm.HalfNormal("sigma_sc", 0.5)
        gamma_sin = pm.Normal("gamma_sin", mu_sin, sigma_sc, shape=len(brand_uniq))
        gamma_cos = pm.Normal("gamma_cos", mu_cos, sigma_sc, shape=len(brand_uniq))

        sigma = pm.HalfNormal("sigma", y_std)

        mu = (
            alpha[tr["brand_code"].values]
            + beta_trend * t_tr_z
            + gamma_sin[tr["brand_code"].values] * tr["month_sin"].values
            + gamma_cos[tr["brand_code"].values] * tr["month_cos"].values
        )
        pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y_tr)

        # ADVI for speed (production thesis run could escalate to NUTS)
        approx = pm.fit(n=30000, method="advi", progressbar=False, random_seed=42)
        trace = approx.sample(1000, random_seed=42)

    # Posterior means
    alpha_hat = trace.posterior["alpha"].mean(("chain", "draw")).values
    beta_trend_hat = float(trace.posterior["beta_trend"].mean(("chain", "draw")).values)
    gamma_sin_hat = trace.posterior["gamma_sin"].mean(("chain", "draw")).values
    gamma_cos_hat = trace.posterior["gamma_cos"].mean(("chain", "draw")).values

    mu_val = (
        alpha_hat[va["brand_code"].values]
        + beta_trend_hat * t_va_z
        + gamma_sin_hat[va["brand_code"].values] * va["month_sin"].values
        + gamma_cos_hat[va["brand_code"].values] * va["month_cos"].values
    )
    y_val_pred_log = mu_val
    y_val_pred = np.clip(np.expm1(y_val_pred_log), 0, None)

    # Return predictions aligned to full val index (NaN for non-top10)
    out = pd.Series(np.nan, index=val.index, name="PyMC_hier")
    out.loc[va.index] = y_val_pred
    return out


# ---------------------------------------------------------------------------
# 4. aeon TimeCNN (per-brand, top-10)
# ---------------------------------------------------------------------------
def fit_aeon_topk(train: pd.DataFrame, val: pd.DataFrame, top_k: int = 10) -> pd.Series:
    """Univariate per-brand regression via aeon's RocketRegressor.

    Originally planned TimeCNNRegressor, but tensorflow/Keras lacks Python 3.13
    support (soft dependency blocked at install time). Rocket is a strong
    non-DL alternative: fits very fast using random convolutional kernels.

    Uses a short lookback window (12 months), targets the next month.
    """
    try:
        from aeon.regression.convolution_based import RocketRegressor
        model_cls = RocketRegressor
        model_name = "aeon_Rocket"
    except ImportError as e:
        print(f"  ⚠️  aeon Rocket import failed: {e}")
        return pd.Series(np.nan, index=val.index, name="aeon_Rocket")

    top = train.groupby("brand")["sales_units"].sum().nlargest(top_k).index.tolist()
    print(f"  {model_name} on top-{top_k} brands: {top}")

    out = pd.Series(np.nan, index=val.index, name=model_name)
    lookback = 12

    for brand in top:
        y_tr = train[train["brand"] == brand].sort_values("date")["log_sales_units"].values
        y_va = val[val["brand"] == brand].sort_values("date")
        if len(y_tr) < lookback + 2:
            continue

        # Build sliding windows on TRAIN
        X = []
        y = []
        for i in range(len(y_tr) - lookback):
            X.append(y_tr[i:i + lookback])
            y.append(y_tr[i + lookback])
        X = np.asarray(X).reshape(-1, 1, lookback)  # (n, 1 channel, window)
        y = np.asarray(y)

        try:
            mdl = model_cls(n_kernels=2000, random_state=42)
            mdl.fit(X, y)
        except Exception as e:
            print(f"    {model_name} fit failed for {brand}: {type(e).__name__}: {e}")
            continue

        # Roll out forecasts for VAL horizon
        history = list(y_tr)
        for idx in y_va.index:
            window = np.asarray(history[-lookback:]).reshape(1, 1, lookback)
            try:
                pred_log = float(mdl.predict(window)[0])
            except Exception:
                pred_log = history[-12] if len(history) >= 12 else history[-1]
            out.loc[idx] = np.clip(np.expm1(pred_log), 0, None)
            # Append the actual observation for next step (oracle rollout on log-scale)
            # For autoregressive pure forecast, use pred_log instead.
            # Here we use pure autoregressive to keep the forecast honest.
            history.append(pred_log)

    return out


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
def evaluate(val: pd.DataFrame, preds: dict[str, np.ndarray]) -> pd.DataFrame:
    rows = []
    for name, pred in preds.items():
        val_df = val.copy()
        val_df["y_pred"] = pred
        for brand, g in val_df.groupby("brand"):
            yt, yp = g["sales_units"].values, g["y_pred"].values
            if np.isnan(yp).all():
                continue
            # Allow partial-NaN (aeon/PyMC only cover top-10)
            mask = ~np.isnan(yp)
            if mask.sum() == 0:
                continue
            rows.append({
                "model": name,
                "brand": brand,
                "mape": mape(yt[mask], yp[mask]),
                "wape": wape(yt[mask], yp[mask]),
                "rmse": rmse(yt[mask], yp[mask]),
                "mae": mae(yt[mask], yp[mask]),
                "n": int(mask.sum()),
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


def write_summary(summary: pd.DataFrame, meta: dict) -> Path:
    path = RESULTS_ROOT / "advanced_summary.md"
    lines = []
    lines.append("# Step 08 — Advanced Models Summary (VAL set)")
    lines.append(f"_Generated {datetime.now().isoformat(timespec='seconds')}_\n")
    lines.append("## Ranking (median MAPE, lower is better)\n")
    cols = list(summary.columns)
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("|" + "|".join(["---"] * len(cols)) + "|")
    for _, row in summary.iterrows():
        vals = [
            f"{row[c]:.2f}" if isinstance(row[c], float) else str(row[c])
            for c in cols
        ]
        lines.append("| " + " | ".join(vals) + " |")
    lines.append("\n## Training metadata\n")
    lines.append("```json")
    lines.append(json.dumps(meta, indent=2))
    lines.append("```")
    path.write_text("\n".join(lines))
    return path


def main() -> int:
    t0 = time.time()
    log(f"\n=== Step 08 ADVANCED @ {datetime.now().isoformat(timespec='seconds')} ===")

    header("1/5 Loading split data")
    df = pd.read_parquet(SPLITS_DIR / "feature_matrix_v3_split.parquet")
    df["date"] = pd.to_datetime(df["date"])
    train = df[df["split"] == "train"].reset_index(drop=True)
    val = df[df["split"] == "val"].reset_index(drop=True)
    print(f"  train={len(train):,}  val={len(val):,}  brands={df['brand'].nunique()}")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    preds: dict[str, np.ndarray] = {}
    meta: dict = {}

    # ------------------------------------------------------------------
    header("2/5 LightGBM global (walk-forward CV tuning)")
    try:
        t = time.time()
        lgb_pred, lgb_meta, lgb_model = fit_lightgbm(train, val)
        preds["LightGBM_global"] = lgb_pred
        meta["LightGBM_global"] = {**lgb_meta, "elapsed_s": round(time.time() - t, 1)}
        with open(MODELS_DIR / "lightgbm.pkl", "wb") as f:
            pickle.dump(lgb_model, f)
        print(f"  ✅ LightGBM  ({time.time()-t:.1f}s)")
    except Exception as e:
        log(f"LightGBM FAILED: {type(e).__name__}: {e}")
        print(f"  ⚠️  LightGBM failed: {e}")

    # ------------------------------------------------------------------
    header("3/5 XGBoost global (walk-forward CV tuning)")
    try:
        t = time.time()
        xgb_pred, xgb_meta, xgb_model = fit_xgboost(train, val)
        preds["XGBoost_global"] = xgb_pred
        meta["XGBoost_global"] = {**xgb_meta, "elapsed_s": round(time.time() - t, 1)}
        with open(MODELS_DIR / "xgboost.pkl", "wb") as f:
            pickle.dump(xgb_model, f)
        print(f"  ✅ XGBoost  ({time.time()-t:.1f}s)")
    except Exception as e:
        log(f"XGBoost FAILED: {type(e).__name__}: {e}")
        print(f"  ⚠️  XGBoost failed: {e}")

    # ------------------------------------------------------------------
    header("4/5 PyMC hierarchical Bayesian (top-10)")
    try:
        t = time.time()
        pymc_pred = fit_pymc_hier(train, val)
        preds["PyMC_hier_top10"] = pymc_pred.values
        meta["PyMC_hier_top10"] = {"elapsed_s": round(time.time() - t, 1)}
        print(f"  ✅ PyMC  ({time.time()-t:.1f}s)")
    except Exception as e:
        log(f"PyMC FAILED: {type(e).__name__}: {e}")
        print(f"  ⚠️  PyMC failed: {type(e).__name__}: {e}")

    # ------------------------------------------------------------------
    header("5/5 aeon Rocket (top-10)")
    try:
        t = time.time()
        aeon_pred = fit_aeon_topk(train, val, top_k=10)
        preds["aeon_Rocket_top10"] = aeon_pred.values
        meta["aeon_Rocket_top10"] = {"elapsed_s": round(time.time() - t, 1)}
        print(f"  ✅ aeon Rocket  ({time.time()-t:.1f}s)")
    except Exception as e:
        log(f"aeon FAILED: {type(e).__name__}: {e}")
        print(f"  ⚠️  aeon failed: {type(e).__name__}: {e}")

    # ------------------------------------------------------------------
    header("Evaluation")
    per_brand = evaluate(val, preds)
    per_brand_path = RESULTS_ROOT / "advanced_val.csv"
    per_brand.to_csv(per_brand_path, index=False)
    print(f"  ✅ {per_brand_path.relative_to(PROJECT_ROOT)}  ({len(per_brand)} rows)")

    summary = summarise(per_brand)
    print("\n  Ranking (median MAPE):")
    print(summary.to_string(index=False))

    summary_path = write_summary(summary, meta)
    print(f"\n  ✅ {summary_path.relative_to(PROJECT_ROOT)}")

    # Save all predictions for Step 09 / 10
    pred_df = val[["brand", "date", "sales_units"]].copy()
    for name, p in preds.items():
        pred_df[name] = p
    pred_df.to_parquet(RESULTS_ROOT / "advanced_predictions.parquet", index=False)
    print(f"  ✅ advanced_predictions.parquet")

    elapsed = time.time() - t0
    log(f"OK — {len(preds)} advanced models  ({elapsed:.1f}s)")
    print("\n" + "=" * 72)
    print(f"  ✅ STEP 08 COMPLETE  ({elapsed:.1f}s)  — ready for Step 09")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
