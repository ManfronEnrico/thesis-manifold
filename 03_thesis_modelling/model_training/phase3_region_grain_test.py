#!/usr/bin/env python3
"""
Phase 3 — Region-Grain WMAPE Test for CSD

Load the region-grain CSD feature matrix (brand×region×period, 25.1k rows),
tune XGBoost and LightGBM on validation split (objective=WMAPE),
refit on train+val, evaluate on test.

Compare test WMAPE against the 16.5% brand×month baseline.

Usage:  python phase3_region_grain_test.py [--trials 30]
Output: Phase 3 result in terminal (+ optional CSV)
"""

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import optuna

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import THESIS_DATA_ENGINEERED_BYMONTH_DIR

warnings.filterwarnings("ignore")
optuna.logging.set_verbosity(optuna.logging.WARNING)

SEED = 42
BASELINE_WMAPE = 16.5  # Brand×month tuned baseline from SRQ1

FEATURES = [
    "lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
    "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
    "month", "quarter", "holiday_month", "promo_intensity", "weighted_dist"
]


def wmape(y, yhat):
    """Weighted Mean Absolute Percentage Error"""
    y = np.asarray(y, float)
    yhat = np.clip(np.asarray(yhat, float), 0, None)
    return float(np.abs(y - yhat).sum() / max(y.sum(), 1e-9) * 100)


def load_region_grain():
    """Load the region-grain feature matrix"""
    fm_path = THESIS_DATA_ENGINEERED_BYMONTH_DIR / "CSD" / "csd_feature_matrix.parquet"
    if not fm_path.exists():
        raise FileNotFoundError(f"Feature matrix not found at {fm_path}")

    fm = pd.read_parquet(fm_path)
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()

    parts = {s: d[d["split"] == s] for s in ("train", "val", "test")}
    return parts


def tune_model(model_name, parts, trials):
    """Tune XGBoost or LightGBM on validation split, refit on train+val, eval on test"""
    tr, va = parts["train"], parts["val"]
    Xtr, ytr = tr[FEATURES].fillna(0.0), tr["log_sales_units"].values
    Xva, yva = va[FEATURES].fillna(0.0), np.expm1(va["log_sales_units"].values)

    if model_name == "LightGBM":
        from lightgbm import LGBMRegressor
        def make_model(params):
            return LGBMRegressor(random_state=SEED, verbose=-1, **params)

        def space(trial):
            return dict(
                n_estimators=trial.suggest_int("n_estimators", 200, 1200),
                learning_rate=trial.suggest_float("learning_rate", 0.01, 0.15, log=True),
                num_leaves=trial.suggest_int("num_leaves", 15, 128),
                min_child_samples=trial.suggest_int("min_child_samples", 5, 60),
                subsample=trial.suggest_float("subsample", 0.6, 1.0),
                colsample_bytree=trial.suggest_float("colsample_bytree", 0.6, 1.0),
            )
    else:
        from xgboost import XGBRegressor
        def make_model(params):
            return XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1, **params)

        def space(trial):
            return dict(
                n_estimators=trial.suggest_int("n_estimators", 200, 1200),
                learning_rate=trial.suggest_float("learning_rate", 0.01, 0.15, log=True),
                max_depth=trial.suggest_int("max_depth", 3, 10),
                min_child_weight=trial.suggest_float("min_child_weight", 1.0, 8.0),
                subsample=trial.suggest_float("subsample", 0.6, 1.0),
                colsample_bytree=trial.suggest_float("colsample_bytree", 0.6, 1.0),
            )

    def objective(trial):
        m = make_model(space(trial))
        m.fit(Xtr, ytr)
        return wmape(yva, np.expm1(m.predict(Xva)))

    print(f"  {model_name}: tuning on validation ({trials} trials)...", end=" ", flush=True)
    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=SEED))
    study.optimize(objective, n_trials=trials, show_progress_bar=False)

    # Refit on train+val
    trval = pd.concat([tr, va])
    m = make_model(study.best_params)
    m.fit(trval[FEATURES].fillna(0.0), trval["log_sales_units"].values)

    # Eval on test
    te = parts["test"]
    pred = np.expm1(m.predict(te[FEATURES].fillna(0.0)))
    yte = np.expm1(te["log_sales_units"].values)
    test_wmape = wmape(yte, pred)

    print(f"✓ test WMAPE={test_wmape:.1f}% (val {study.best_value:.1f}%)")
    return test_wmape, study.best_value, study.best_params


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=30, help="Optuna trials per model")
    args = ap.parse_args()

    print("\n" + "="*70)
    print("PHASE 3: Region-Grain WMAPE Test — CSD")
    print("="*70)

    # Load region-grain data
    print("\nLoading region-grain feature matrix (brand×region×period)...", end=" ", flush=True)
    try:
        parts = load_region_grain()
        print(f"✓")
        print(f"  Train: {len(parts['train']):,} rows")
        print(f"  Val:   {len(parts['val']):,} rows")
        print(f"  Test:  {len(parts['test']):,} rows")
    except FileNotFoundError as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)

    # Tune models
    print(f"\nTuning models on validation (objective=WMAPE, {args.trials} trials each)...")
    results = {}
    for model in ("XGBoost", "LightGBM"):
        test_wmape, val_wmape, params = tune_model(model, parts, args.trials)
        results[model] = {
            "test_wmape": test_wmape,
            "val_wmape": val_wmape,
            "params": params,
        }

    # Summary
    print("\n" + "="*70)
    print("PHASE 3 RESULT")
    print("="*70)
    print(f"\nBaseline (brand×month, tuned):    {BASELINE_WMAPE:.1f}%\n")

    winner_model = min(results, key=lambda m: results[m]["test_wmape"])
    winner_wmape = results[winner_model]["test_wmape"]

    print(f"Region-grain results:")
    for model, res in sorted(results.items(), key=lambda x: x[1]["test_wmape"]):
        win_marker = "← WINNER" if model == winner_model else ""
        print(f"  {model:10s}: {res['test_wmape']:5.1f}% {win_marker}")

    print("\n" + "-"*70)
    if winner_wmape < BASELINE_WMAPE:
        print(f"✓ REGION WINS: {winner_wmape:.1f}% < {BASELINE_WMAPE:.1f}%")
        print("  → Recommendation: Switch to region grain for Phase 4-5")
    else:
        print(f"← BASELINE HOLDS: {winner_wmape:.1f}% ≥ {BASELINE_WMAPE:.1f}%")
        print("  → Recommendation: Keep brand×month grain as documented limitation")
    print("="*70 + "\n")

    # Save results
    output_dir = Path("04_thesis_results") / "phase3_region_grain_test"
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = output_dir / "phase3_result.json"
    summary_path.write_text(json.dumps({
        "baseline_wmape": BASELINE_WMAPE,
        "winner_model": winner_model,
        "winner_wmape": winner_wmape,
        "results": {
            m: {
                "test_wmape": r["test_wmape"],
                "val_wmape": r["val_wmape"],
                "params": r["params"],
            }
            for m, r in results.items()
        },
    }, indent=2))

    print(f"Results saved to: {summary_path}")


if __name__ == "__main__":
    main()
