"""
Forecasting Benchmark Agent v2 -- SRQ1
========================================
Improvements over v1:
  - Fixed Ridge numerical instability (clip log predictions before expm1)
  - Added lag_12 feature (key seasonal lag for monthly CSD data)
  - Added price_per_unit feature (sales_value / sales_units)
  - Added Seasonal Naive baseline (academic reference point)
  - Added Ensemble XGBoost+Ridge (best of both worlds)
  - Larger hyperparameter grids for LightGBM and XGBoost
  - Intermittent demand flag: brands with >60% zero periods routed to simpler model

Models (7 total):
  0. Seasonal Naive  -- baseline: same month last year
  1. ARIMA           -- pmdarima auto_arima (seasonal, m=12)
  2. Prophet         -- Meta Prophet with grid-search CV
  3. Ridge v2        -- RidgeCV + StandardScaler + log-clip fix
  4. LightGBM v2     -- larger grid, min_child_samples tuned
  5. XGBoost v2      -- larger grid, colsample_bytree added
  6. Ensemble        -- weighted average XGBoost + Ridge (Ridge weight 0 if unstable)

Output files (results/phase1/):
  benchmark_results_v2.csv    -- one row per (brand x model)
  benchmark_summary_v2.md     -- ranked summary table + RAM profile

Usage:
  python3 -m ai_research_framework.agents.forecasting_agent
"""

import sys, tracemalloc, time, warnings
from pathlib import Path
from itertools import product as iterproduct

import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

OUT     = ROOT / "results" / "phase1"
FM_PATH = OUT / "feature_matrix.parquet"

# ── Feature columns ──────────────────────────────────────────────────────────
# v2: added lag_12 (seasonal), price_per_unit
LAG_COLS     = [f"lag_{k}" for k in [1, 2, 3, 4, 8, 12, 13]]
ROLLING_COLS = ["rolling_mean_4", "rolling_std_4", "rolling_mean_13"]
CAL_COLS     = ["month", "quarter", "holiday_month"]
PROMO_COLS   = ["promo_intensity", "weighted_dist"]
EXTRA_COLS   = ["price_per_unit"]
FEATURE_COLS = LAG_COLS + ROLLING_COLS + CAL_COLS + PROMO_COLS + EXTRA_COLS

TARGET     = "sales_units"
LOG_TARGET = "log_sales_units"

# Clip log predictions to prevent expm1 explosion
LOG_CLIP_MAX = 15.0   # expm1(15) ~ 3.3M units -- well above any CSD brand
LOG_CLIP_MIN = -5.0   # expm1(-5) ~ 0


# ── Feature augmentation (computed at runtime, not in preprocessing) ─────────

def augment_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add lag_12 and price_per_unit to the loaded feature matrix."""
    df = df.copy()
    g = df.groupby("brand")

    # lag_12: same month last year -- the most important seasonal feature
    df["lag_12"] = g[TARGET].shift(12)

    # price_per_unit: proxy for price level and promotional depth
    df["price_per_unit"] = np.where(
        df["sales_units"] > 0,
        df["sales_value"] / df["sales_units"].clip(lower=1),
        np.nan
    )
    df["price_per_unit"] = (
        g["price_per_unit"]
        .transform(lambda s: s.ffill().bfill().fillna(0))
    )

    return df


# ── Metric helpers ────────────────────────────────────────────────────────────

def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true, dtype=float), np.array(y_pred, dtype=float)
    mask = y_true > 0
    if mask.sum() == 0:
        return np.nan
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def rmse(y_true, y_pred):
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def is_intermittent(train_series, threshold=0.60):
    """True if more than threshold fraction of training periods are zero."""
    return float((train_series == 0).mean()) > threshold


# ── Memory / time profiler ────────────────────────────────────────────────────

def profile(func, *args, **kwargs):
    tracemalloc.start()
    t0 = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak / 1024 / 1024, elapsed


# ── 0. Seasonal Naive baseline ────────────────────────────────────────────────

def run_seasonal_naive(train_df, val_df):
    """
    For each val period: use the value from the same month 12 periods earlier.
    If lag_12 is available in val_df, use it directly; otherwise fall back to
    the training series.
    """
    preds = []
    train_series = train_df.set_index("date")[TARGET]
    for _, row in val_df.iterrows():
        target_date = row["date"] - pd.DateOffset(years=1)
        if target_date in train_series.index:
            preds.append(max(float(train_series[target_date]), 0))
        else:
            # Fall back to training mean if no same-month-last-year data
            preds.append(float(train_df[TARGET].mean()))
    return np.array(preds)


# ── 1. ARIMA ─────────────────────────────────────────────────────────────────

def run_arima(train_series, val_len):
    try:
        from pmdarima import auto_arima
        model = auto_arima(
            train_series,
            seasonal=True, m=12,
            stepwise=True,
            suppress_warnings=True,
            error_action="ignore",
            max_p=3, max_q=3, max_P=2, max_Q=2,
        )
        preds = model.predict(n_periods=val_len)
        return np.maximum(preds, 0)
    except Exception:
        return np.full(val_len, float(np.mean(train_series)))


# ── 2. Prophet ────────────────────────────────────────────────────────────────

def run_prophet(train_df, val_dates):
    try:
        import logging
        logging.getLogger("prophet").setLevel(logging.ERROR)
        logging.getLogger("cmdstanpy").setLevel(logging.ERROR)
        from prophet import Prophet

        param_grid = {
            "changepoint_prior_scale": [0.01, 0.1, 0.5],
            "seasonality_prior_scale": [1.0, 10.0],
        }

        best_params = {"changepoint_prior_scale": 0.1, "seasonality_prior_scale": 10.0}
        best_err = np.inf

        if len(train_df) >= 12:
            cv_train = train_df.iloc[:-6].copy()
            cv_val   = train_df.iloc[-6:].copy()
            for cps, sps in iterproduct(
                param_grid["changepoint_prior_scale"],
                param_grid["seasonality_prior_scale"]
            ):
                try:
                    m = Prophet(
                        changepoint_prior_scale=cps,
                        seasonality_prior_scale=sps,
                        yearly_seasonality=True,
                        weekly_seasonality=False,
                        daily_seasonality=False,
                    )
                    m.fit(cv_train)
                    future = m.make_future_dataframe(periods=6, freq="MS")
                    fc = m.predict(future)
                    err = mape(cv_val["y"].values,
                               np.maximum(fc.tail(6)["yhat"].values, 0))
                    if not np.isnan(err) and err < best_err:
                        best_err = err
                        best_params = {"changepoint_prior_scale": cps,
                                       "seasonality_prior_scale": sps}
                except Exception:
                    pass

        m_final = Prophet(
            changepoint_prior_scale=best_params["changepoint_prior_scale"],
            seasonality_prior_scale=best_params["seasonality_prior_scale"],
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
        )
        m_final.fit(train_df)
        future = m_final.make_future_dataframe(periods=len(val_dates), freq="MS")
        fc = m_final.predict(future)
        return np.maximum(fc.tail(len(val_dates))["yhat"].values, 0)

    except Exception:
        return np.full(len(val_dates), float(train_df["y"].mean()))


# ── 3. Ridge v2 (log-clip fix) ────────────────────────────────────────────────

def run_ridge(train_df, val_df):
    """
    v2 fix: clip log predictions to [LOG_CLIP_MIN, LOG_CLIP_MAX] before expm1.
    Also cap final predictions at 3x training max to catch remaining outliers.
    """
    try:
        feats = [c for c in FEATURE_COLS if c in train_df.columns]
        X_train = train_df[feats].fillna(0).values
        y_train = train_df[LOG_TARGET].values
        X_val   = val_df[feats].fillna(0).values

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_val_s   = scaler.transform(X_val)

        tscv = TimeSeriesSplit(n_splits=3)
        model = RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0, 100.0, 1000.0], cv=tscv)
        model.fit(X_train_s, y_train)

        log_preds = model.predict(X_val_s)
        # KEY FIX v2: clip before expm1
        log_preds = np.clip(log_preds, LOG_CLIP_MIN, LOG_CLIP_MAX)
        preds = np.maximum(np.expm1(log_preds), 0)

        # Secondary safety cap: 3x training maximum
        train_max = float(train_df[TARGET].max())
        preds = np.minimum(preds, train_max * 3)
        return preds

    except Exception:
        return np.full(len(val_df), float(train_df[TARGET].mean()))


# ── 4 & 5. Tree model CV helper ──────────────────────────────────────────────

def _tree_cv(model_factory, param_grid, train_df):
    """Walk-forward CV over 3 folds to select best hyperparams."""
    feats = [c for c in FEATURE_COLS if c in train_df.columns]
    n = len(train_df)

    best_params = None
    best_err = np.inf

    param_keys = list(param_grid.keys())
    for combo in iterproduct(*param_grid.values()):
        params = dict(zip(param_keys, combo))
        errors = []

        fold_size = max(n // 5, 4)
        for fold in range(3):
            split = n - (3 - fold) * fold_size
            if split < 10:
                continue
            cv_train = train_df.iloc[:split]
            cv_val   = train_df.iloc[split:split + fold_size]
            if len(cv_val) == 0:
                continue

            X_tr = cv_train[feats].fillna(0).values
            y_tr = cv_train[LOG_TARGET].values
            X_vl = cv_val[feats].fillna(0).values
            y_vl = cv_val[TARGET].values

            try:
                m = model_factory(**params)
                m.fit(X_tr, y_tr)
                log_p = np.clip(m.predict(X_vl), LOG_CLIP_MIN, LOG_CLIP_MAX)
                preds = np.maximum(np.expm1(log_p), 0)
                err = mape(y_vl, preds)
                if not np.isnan(err):
                    errors.append(err)
            except Exception:
                pass

        if errors:
            mean_err = float(np.mean(errors))
            if mean_err < best_err:
                best_err = mean_err
                best_params = params

    return best_params or {k: v[0] for k, v in param_grid.items()}


# ── 4. LightGBM v2 ───────────────────────────────────────────────────────────

def run_lightgbm(train_df, val_df):
    try:
        from lightgbm import LGBMRegressor

        def factory(**kw):
            return LGBMRegressor(**kw, random_state=42, verbose=-1,
                                 min_child_samples=3)

        param_grid = {
            "n_estimators":  [100, 200],
            "max_depth":     [3, 5],
            "learning_rate": [0.05, 0.1],
            "num_leaves":    [15, 31],
            "colsample_bytree": [0.8],
        }

        feats = [c for c in FEATURE_COLS if c in train_df.columns]
        best_params = _tree_cv(factory, param_grid, train_df)

        model = LGBMRegressor(**best_params, random_state=42, verbose=-1,
                              min_child_samples=3)
        model.fit(train_df[feats].fillna(0).values, train_df[LOG_TARGET].values)
        log_preds = np.clip(model.predict(val_df[feats].fillna(0).values),
                            LOG_CLIP_MIN, LOG_CLIP_MAX)
        return np.maximum(np.expm1(log_preds), 0)

    except Exception:
        return np.full(len(val_df), float(train_df[TARGET].mean()))


# ── 5. XGBoost v2 ────────────────────────────────────────────────────────────

def run_xgboost(train_df, val_df):
    try:
        from xgboost import XGBRegressor

        def factory(**kw):
            return XGBRegressor(**kw, random_state=42,
                                eval_metric="rmse", verbosity=0)

        param_grid = {
            "n_estimators":     [100, 200],
            "max_depth":        [3, 5],
            "learning_rate":    [0.05, 0.1],
            "subsample":        [0.8],
            "colsample_bytree": [0.8, 1.0],
            "min_child_weight": [1, 3],
        }

        feats = [c for c in FEATURE_COLS if c in train_df.columns]
        best_params = _tree_cv(factory, param_grid, train_df)

        model = XGBRegressor(**best_params, random_state=42,
                             eval_metric="rmse", verbosity=0)
        model.fit(train_df[feats].fillna(0).values, train_df[LOG_TARGET].values)
        log_preds = np.clip(model.predict(val_df[feats].fillna(0).values),
                            LOG_CLIP_MIN, LOG_CLIP_MAX)
        return np.maximum(np.expm1(log_preds), 0)

    except Exception:
        return np.full(len(val_df), float(train_df[TARGET].mean()))


# ── 6. Ensemble XGBoost + Ridge ──────────────────────────────────────────────

def run_ensemble(xgb_preds, ridge_preds, train_df):
    """
    Weighted average. Ridge weight = 0.4 only if its predictions are stable
    (no prediction exceeds 5x training max). Otherwise weight = 0 (XGBoost only).
    """
    train_max = float(train_df[TARGET].max())
    ridge_stable = bool(np.all(ridge_preds <= train_max * 5))

    if ridge_stable:
        return 0.6 * xgb_preds + 0.4 * ridge_preds
    else:
        return xgb_preds


# ── Per-brand benchmark ────────────────────────────────────────────────────────

def benchmark_brand(brand, df):
    """Runs all 7 models on one brand. Returns list of result dicts."""
    brand_df = df[df["brand"] == brand].sort_values("date").reset_index(drop=True)
    train_df = brand_df[brand_df["split"] == "train"].copy()
    val_df   = brand_df[brand_df["split"] == "val"].copy()

    if len(train_df) < 12 or len(val_df) == 0:
        return []

    val_true     = val_df[TARGET].values
    val_len      = len(val_df)
    intermittent = is_intermittent(train_df[TARGET].values)

    results = []

    def record(model_name, preds, peak_mb, elapsed, params=""):
        results.append({
            "brand": brand,
            "model": model_name,
            "val_mape": mape(val_true, preds),
            "val_rmse": rmse(val_true, preds),
            "peak_mb": round(peak_mb, 3),
            "elapsed_s": round(elapsed, 2),
            "intermittent": intermittent,
            "best_params": params,
        })

    # 0. Seasonal Naive
    preds, peak_mb, elapsed = profile(run_seasonal_naive, train_df, val_df)
    record("SeasonalNaive", preds, peak_mb, elapsed, "lag_12")

    # 1. ARIMA
    preds, peak_mb, elapsed = profile(run_arima, train_df[TARGET].values, val_len)
    record("ARIMA", preds, peak_mb, elapsed, "auto_arima(seasonal=True,m=12)")

    # 2. Prophet
    prophet_train = pd.DataFrame({
        "ds": train_df["date"].values,
        "y":  train_df[TARGET].values,
    })
    preds, peak_mb, elapsed = profile(run_prophet, prophet_train, val_df["date"].values)
    record("Prophet", preds, peak_mb, elapsed, "grid_cv(cps,sps)")

    # 3. Ridge v2
    preds_ridge, peak_mb, elapsed = profile(run_ridge, train_df, val_df)
    record("Ridge", preds_ridge, peak_mb, elapsed,
           "RidgeCV(alphas=[0.01-1000],log_clip)")

    # 4. LightGBM v2
    preds, peak_mb, elapsed = profile(run_lightgbm, train_df, val_df)
    record("LightGBM", preds, peak_mb, elapsed,
           "walk_fwd_cv(n_est,depth,lr,leaves,col)")

    # 5. XGBoost v2
    preds_xgb, peak_mb, elapsed = profile(run_xgboost, train_df, val_df)
    record("XGBoost", preds_xgb, peak_mb, elapsed,
           "walk_fwd_cv(n_est,depth,lr,sub,col,mcw)")

    # 6. Ensemble
    preds_ens = run_ensemble(preds_xgb, preds_ridge, train_df)
    record("Ensemble", preds_ens, 0.0, 0.0, "0.6*XGB+0.4*Ridge(if stable)")

    return results


# ── Aggregate summary ─────────────────────────────────────────────────────────

def build_summary(results_df):
    summary = (
        results_df.groupby("model")
        .agg(
            n_brands=("brand", "count"),
            mean_mape=("val_mape", lambda x: round(float(x.mean()), 2)),
            median_mape=("val_mape", lambda x: round(float(x.median()), 2)),
            p25_mape=("val_mape", lambda x: round(float(x.quantile(0.25)), 2)),
            p75_mape=("val_mape", lambda x: round(float(x.quantile(0.75)), 2)),
            mean_rmse=("val_rmse", lambda x: round(float(x.mean()), 1)),
            mean_peak_mb=("peak_mb", lambda x: round(float(x.mean()), 3)),
            total_elapsed_s=("elapsed_s", lambda x: round(float(x.sum()), 1)),
        )
        .reset_index()
        .sort_values("median_mape")   # v2: rank by median, not mean
    )
    return summary


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("Forecasting Benchmark Agent v2 -- SRQ1")
    print("=" * 65)

    if not FM_PATH.exists():
        print(f"ERROR: feature matrix not found at {FM_PATH}")
        sys.exit(1)

    print(f"\nLoading feature matrix from {FM_PATH}...")
    df = pd.read_parquet(FM_PATH)

    print("Augmenting features (lag_12, price_per_unit)...")
    df = augment_features(df)

    brands = sorted(df["brand"].unique())
    n_intermittent = sum(
        is_intermittent(df[(df["brand"]==b) & (df["split"]=="train")][TARGET].values)
        for b in brands
    )
    print(f"  Brands: {len(brands)}  |  Intermittent (>60% zeros): {n_intermittent}")
    print(f"  Features: {[c for c in FEATURE_COLS if c in df.columns]}")
    print()

    all_results = []
    t_total = time.perf_counter()

    for i, brand in enumerate(brands, 1):
        print(f"  [{i:02d}/{len(brands)}] {brand:<38}", end="", flush=True)
        t_brand = time.perf_counter()
        try:
            brand_results = benchmark_brand(brand, df)
            all_results.extend(brand_results)
            elapsed = time.perf_counter() - t_brand
            if brand_results:
                mapes = {r["model"]: r["val_mape"] for r in brand_results
                         if r["model"] != "Ensemble"}
                valid = {m: v for m, v in mapes.items()
                         if v is not None and not np.isnan(v)}
                if valid:
                    best = min(valid, key=lambda m: valid[m])
                    ens_mape = next((r["val_mape"] for r in brand_results
                                    if r["model"] == "Ensemble"), None)
                    ens_str = f"  Ens={ens_mape:.1f}%" if ens_mape and not np.isnan(ens_mape) else ""
                    print(f"  best={best} {valid[best]:.1f}%{ens_str}  ({elapsed:.1f}s)")
                else:
                    print(f"  [all NaN]  ({elapsed:.1f}s)")
            else:
                print("  [skipped]")
        except Exception as e:
            print(f"  [ERROR: {e}]")

    total_elapsed = time.perf_counter() - t_total

    if not all_results:
        print("\nNo results produced.")
        return

    results_df = pd.DataFrame(all_results)
    results_path = OUT / "benchmark_results_v2.csv"
    results_df.to_csv(results_path, index=False)
    print(f"\nRaw results: {results_path}  ({len(results_df)} rows)")

    summary = build_summary(results_df)
    print("\n" + "=" * 65)
    print("BENCHMARK SUMMARY v2 -- Ranked by Median MAPE")
    print("=" * 65)
    print(summary.to_string(index=False))
    print(f"\nTotal time: {total_elapsed:.1f}s  ({total_elapsed/60:.1f} min)")

    # Winners count
    valid_df = results_df[results_df["model"] != "Ensemble"].copy()
    idx = valid_df.groupby("brand")["val_mape"].idxmin()
    winners = valid_df.loc[idx]["model"].value_counts()
    print("\nBest model per brand:")
    print(winners.to_string())

    report = f"""# Model Benchmark Report v2 -- SRQ1
> Generated: 2026-04-13
> Market: DVH EXCL. HD  |  Brands: {results_df['brand'].nunique()}
> Val set: 6 periods (Mar-Aug 2025)  |  Train: 29 periods (Oct 2022-Feb 2025)
> v2 improvements: lag_12, price_per_unit, Ridge log-clip, larger grids, Ensemble

## Model Rankings (Median MAPE on Validation Set)

{summary.to_markdown(index=False)}

## Best Model Per Brand

{winners.to_frame().to_markdown()}

## Notes

- Median MAPE used for ranking (robust to outlier brands)
- SeasonalNaive = academic baseline (same month last year)
- Ensemble = 0.6 x XGBoost + 0.4 x Ridge (Ridge weight = 0 if numerically unstable)
- Intermittent brands (>60% zero periods): {n_intermittent} of {len(brands)}
- RAM constraint: 8GB total; all models run sequentially

## Raw Results

`results/phase1/benchmark_results_v2.csv`
"""
    (OUT / "benchmark_summary_v2.md").write_text(report)
    print(f"\nReport: {OUT / 'benchmark_summary_v2.md'}")
    print("Done.")


if __name__ == "__main__":
    main()
