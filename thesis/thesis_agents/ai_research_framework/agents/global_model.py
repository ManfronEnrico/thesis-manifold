"""
Global Forecasting Model -- SRQ1 improvement
==============================================
Trains ONE LightGBM on all 77 brands simultaneously (global model approach).
Brand encoded as categorical feature so the model learns cross-brand patterns.

Key insight: instead of 77 models × 35 rows = 35 rows per brand,
we use 1 model × 77 brands = 2,695 rows -- dramatically more signal.

This mirrors the approach that won the M5 Competition (Makridakis et al., 2022).

Output files (thesis/analysis/outputs/phase1/):
  global_results.csv      -- per-brand test MAPE (global vs per-brand)
  global_summary.md       -- comparison table for thesis

Usage:
  python3 -m ai_research_framework.agents.global_model
"""

import sys, time, warnings
from pathlib import Path
from itertools import product as iterproduct

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import TimeSeriesSplit

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

OUT     = ROOT / "results" / "phase1"
FM_PATH = OUT / "feature_matrix.parquet"

LAG_COLS     = [f"lag_{k}" for k in [1, 2, 3, 4, 8, 12, 13]]
ROLLING_COLS = ["rolling_mean_4", "rolling_std_4", "rolling_mean_13"]
CAL_COLS     = ["month", "quarter", "holiday_month"]
PROMO_COLS   = ["promo_intensity", "weighted_dist"]
EXTRA_COLS   = ["price_per_unit", "brand_enc"]   # brand_enc = categorical brand id
FEATURE_COLS = LAG_COLS + ROLLING_COLS + CAL_COLS + PROMO_COLS + EXTRA_COLS

TARGET     = "sales_units"
LOG_TARGET = "log_sales_units"
LOG_CLIP   = (-5.0, 15.0)


# ── Metrics ───────────────────────────────────────────────────────────────────

def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true, dtype=float), np.array(y_pred, dtype=float)
    mask = y_true > 0
    if mask.sum() == 0:
        return np.nan
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)

def rmse(y_true, y_pred):
    from sklearn.metrics import mean_squared_error
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


# ── Feature augmentation ─────────────────────────────────────────────────────

def augment(df):
    df = df.copy()
    g = df.groupby("brand")
    df["lag_12"] = g[TARGET].shift(12)
    df["price_per_unit"] = np.where(
        df["sales_units"] > 0,
        df["sales_value"] / df["sales_units"].clip(lower=1), np.nan
    )
    df["price_per_unit"] = g["price_per_unit"].transform(
        lambda s: s.ffill().bfill().fillna(0)
    )
    le = LabelEncoder()
    df["brand_enc"] = le.fit_transform(df["brand"]).astype(float)
    return df, le


# ── Global LightGBM ───────────────────────────────────────────────────────────

def train_global_lgbm(train_df, param_grid=None):
    """
    Train one LightGBM on all brands. Returns fitted model + scaler info.
    Walk-forward CV on the full multi-brand training set.
    """
    from lightgbm import LGBMRegressor

    feats = [c for c in FEATURE_COLS if c in train_df.columns]

    if param_grid is None:
        param_grid = {
            "n_estimators":     [200, 500],
            "max_depth":        [4, 6],
            "learning_rate":    [0.03, 0.05],
            "num_leaves":       [31, 63],
            "colsample_bytree": [0.8],
            "min_child_samples":[5, 10],
        }

    # Walk-forward CV on global training set
    # Split by time (date), not by row index, to respect temporal order
    all_dates = sorted(train_df["date"].unique())
    n_dates   = len(all_dates)
    n_folds   = 3
    fold_size = max(n_dates // 6, 3)

    best_params = None
    best_err    = np.inf

    print(f"    Grid search: {sum(len(v) for v in param_grid.values())} params, "
          f"{len(list(iterproduct(*param_grid.values())))} combos, {n_folds} folds...")

    param_keys = list(param_grid.keys())
    for combo in iterproduct(*param_grid.values()):
        params = dict(zip(param_keys, combo))
        errors = []

        for fold in range(n_folds):
            split_idx = n_dates - (n_folds - fold) * fold_size
            if split_idx < 10:
                continue
            cv_cutoff  = all_dates[split_idx - 1]
            val_cutoff = all_dates[min(split_idx + fold_size - 1, n_dates - 1)]

            cv_train = train_df[train_df["date"] <= cv_cutoff]
            cv_val   = train_df[(train_df["date"] > cv_cutoff) &
                                (train_df["date"] <= val_cutoff)]
            if len(cv_val) == 0:
                continue

            X_tr = cv_train[feats].fillna(0).values
            y_tr = cv_train[LOG_TARGET].values
            X_vl = cv_val[feats].fillna(0).values
            y_vl = cv_val[TARGET].values

            try:
                m = LGBMRegressor(**params, random_state=42, verbose=-1)
                m.fit(X_tr, y_tr)
                log_p = np.clip(m.predict(X_vl), *LOG_CLIP)
                preds = np.maximum(np.expm1(log_p), 0)
                err = mape(y_vl, preds)
                if not np.isnan(err):
                    errors.append(err)
            except Exception:
                pass

        if errors:
            mean_err = float(np.mean(errors))
            if mean_err < best_err:
                best_err   = mean_err
                best_params = params

    if best_params is None:
        best_params = {k: v[0] for k, v in param_grid.items()}

    print(f"    Best params (CV MAPE={best_err:.1f}%): {best_params}")

    # Final fit on full training set
    model = LGBMRegressor(**best_params, random_state=42, verbose=-1)
    model.fit(train_df[feats].fillna(0).values, train_df[LOG_TARGET].values)
    return model, feats


def predict_global(model, df, feats):
    log_p = np.clip(model.predict(df[feats].fillna(0).values), *LOG_CLIP)
    return np.maximum(np.expm1(log_p), 0)


# ── Evaluate per brand ────────────────────────────────────────────────────────

def evaluate_per_brand(df, model, feats, split="test"):
    results = []
    for brand in sorted(df["brand"].unique()):
        bdf      = df[(df["brand"] == brand) & (df["split"] == split)]
        train_b  = df[(df["brand"] == brand) & (df["split"].isin(["train","val"]))]
        if len(bdf) == 0 or len(train_b) == 0:
            continue
        preds    = predict_global(model, bdf, feats)
        y_true   = bdf[TARGET].values
        # Cap at 3x brand training max
        train_max = float(train_b[TARGET].max())
        preds     = np.minimum(preds, train_max * 3)
        results.append({
            "brand":       brand,
            "test_mape":   mape(y_true, preds),
            "test_rmse":   rmse(y_true, preds),
            "n_test":      len(bdf),
        })
    return pd.DataFrame(results)


# ── Feature importance ────────────────────────────────────────────────────────

def feature_importance(model, feats):
    imp = pd.Series(model.feature_importances_, index=feats)
    return imp.sort_values(ascending=False)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("Global LightGBM -- SRQ1")
    print("=" * 65)

    df = pd.read_parquet(FM_PATH)
    df, le = augment(df)

    train_df   = df[df["split"] == "train"]
    trainval_df = df[df["split"].isin(["train", "val"])]
    val_df     = df[df["split"] == "val"]
    test_df_all = df[df["split"] == "test"]

    print(f"\nTraining set (global):  {len(train_df):,} rows "
          f"({train_df['brand'].nunique()} brands × ~{len(train_df)//train_df['brand'].nunique()} periods)")
    print(f"Val set:                {len(val_df):,} rows")
    print(f"Test set:               {len(test_df_all):,} rows")

    # ── Step 1: Validate on val set (train only) ──────────────────────────────
    print("\n[1/2] Training global model on TRAIN, evaluating on VAL...")
    t0 = time.perf_counter()
    model_val, feats = train_global_lgbm(train_df)
    val_results = evaluate_per_brand(df, model_val, feats, split="val")
    print(f"    Val results: {len(val_results)} brands  |  "
          f"Median MAPE: {val_results['test_mape'].median():.1f}%  |  "
          f"Time: {time.perf_counter()-t0:.0f}s")

    # ── Step 2: Final model on train+val, evaluate test ───────────────────────
    print("\n[2/2] Retraining on TRAIN+VAL, evaluating on TEST...")
    t0 = time.perf_counter()
    model_final, feats = train_global_lgbm(trainval_df)
    test_results = evaluate_per_brand(df, model_final, feats, split="test")
    elapsed = time.perf_counter() - t0
    print(f"    Test results: {len(test_results)} brands  |  "
          f"Median MAPE: {test_results['test_mape'].median():.1f}%  |  "
          f"Time: {elapsed:.0f}s")

    # ── Feature importance ─────────────────────────────────────────────────────
    print("\n    Feature importance (top 10):")
    imp = feature_importance(model_final, feats)
    for feat, score in imp.head(10).items():
        print(f"      {feat:<25} {score:>6}")

    # ── Compare against per-brand XGBoost ─────────────────────────────────────
    per_brand = pd.read_csv(OUT / "test_results.csv")
    xgb_pb = (per_brand[per_brand["model"] == "XGBoost"]
               [["brand","test_mape"]]
               .rename(columns={"test_mape": "xgb_perbrand_mape"}))

    comparison = test_results.merge(xgb_pb, on="brand", how="left")
    comparison["delta"] = comparison["test_mape"] - comparison["xgb_perbrand_mape"]
    comparison["winner"] = np.where(
        comparison["test_mape"] < comparison["xgb_perbrand_mape"],
        "GlobalLGB", "XGB_PerBrand"
    )

    global_wins = (comparison["winner"] == "GlobalLGB").sum()
    perbrand_wins = (comparison["winner"] == "XGB_PerBrand").sum()

    print(f"\n=== GLOBAL vs PER-BRAND (XGBoost) ===")
    print(f"Global LightGBM  median MAPE: {comparison['test_mape'].median():.1f}%")
    print(f"XGBoost per-band median MAPE: {comparison['xgb_perbrand_mape'].median():.1f}%")
    print(f"Global wins: {global_wins}/77  |  Per-brand wins: {perbrand_wins}/77")
    print(f"\nBrands where Global wins (delta < 0):")
    wins = comparison[comparison["winner"]=="GlobalLGB"].sort_values("delta")
    print(wins[["brand","test_mape","xgb_perbrand_mape","delta"]].head(15).to_string(index=False))

    # Volume-weighted MAPE
    fm = pd.read_parquet(FM_PATH)
    vol = fm[fm["split"].isin(["train","val"])].groupby("brand")["sales_units"].sum()
    comp_vol = comparison.merge(vol.rename("vol").reset_index(), on="brand")
    wm_global = (comp_vol["test_mape"] * comp_vol["vol"]).sum() / comp_vol["vol"].sum()
    wm_xgb    = (comp_vol["xgb_perbrand_mape"] * comp_vol["vol"]).sum() / comp_vol["vol"].sum()
    print(f"\nVolume-weighted MAPE:  Global={wm_global:.1f}%  |  XGBoost per-brand={wm_xgb:.1f}%")

    # Top 10 by volume
    top10 = vol.nlargest(10).index.tolist()
    t10_g = comparison[comparison["brand"].isin(top10)]["test_mape"].median()
    t10_x = comparison[comparison["brand"].isin(top10)]["xgb_perbrand_mape"].median()
    print(f"Top-10 brands MAPE:    Global={t10_g:.1f}%  |  XGBoost per-brand={t10_x:.1f}%")

    # Save
    comparison.to_csv(OUT / "global_results.csv", index=False)

    report = f"""# Global LightGBM Results -- SRQ1
> Generated: 2026-04-13
> Architecture: 1 model trained on all {train_df['brand'].nunique()} brands simultaneously
> Training rows: {len(trainval_df):,} (train+val)  |  Test rows: {len(test_df_all):,}

## Summary

| Metric | Global LightGBM | XGBoost (per-brand) |
|---|---|---|
| Median MAPE (test) | {comparison['test_mape'].median():.1f}% | {comparison['xgb_perbrand_mape'].median():.1f}% |
| Volume-weighted MAPE | {wm_global:.1f}% | {wm_xgb:.1f}% |
| Top-10 brands MAPE | {t10_g:.1f}% | {t10_x:.1f}% |
| Brands where Global wins | {global_wins}/77 | {perbrand_wins}/77 |

## Feature Importance (Top 10)

{imp.head(10).to_frame("importance").to_markdown()}

## Per-Brand Comparison

{comparison[["brand","test_mape","xgb_perbrand_mape","delta","winner"]].sort_values("delta").to_markdown(index=False)}

## Interpretation

The global model trains on {len(trainval_df):,} rows vs ~35 rows per brand for per-brand models.
Cross-brand learning allows the model to borrow statistical strength from major brands
(Coca-Cola, Pepsi) to improve forecasts for smaller brands -- the M5 Competition winning approach.
"""
    (OUT / "global_summary.md").write_text(report)
    print(f"\nSaved: {OUT / 'global_results.csv'}")
    print(f"Saved: {OUT / 'global_summary.md'}")
    print("\nDone.")


if __name__ == "__main__":
    main()
