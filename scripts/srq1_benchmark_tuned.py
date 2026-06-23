#!/usr/bin/env python3
"""
SRQ1 forecasting benchmark — Optuna-tuned LightGBM + XGBoost.

For each (dataset, category): tune on the validation split (objective = WMAPE),
refit the best config on train+val, evaluate once on test. Reports tuned
WMAPE / mean-MAPE / median-MAPE and saves best params for the thesis appendix.
Compares against the untuned run (scripts/srq1_benchmark.py).

Self-contained, seed=42, reproducible. No Prometheus/Nika dependency.
Usage:  .venv/bin/python scripts/srq1_benchmark_tuned.py [--trials 30]
Output: thesis/data/_05_results_srq1/{tuned_metrics.csv, tuned_params.json, tuned_summary.md}
"""

import argparse
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import optuna

warnings.filterwarnings("ignore")
optuna.logging.set_verbosity(optuna.logging.WARNING)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "thesis" / "data" / "_05_results_srq1"
SEED = 42

CATS = {"CSD": "csd", "danskvand": "danskvand", "energidrikke": "energidrikke", "RTD": "rtd"}
DATASETS = {
    "bychain": ROOT / "thesis" / "data" / "_04_engineered_bychain",
    "brand":   ROOT / "thesis" / "data" / "_03_engineered_dvhexclhd",
}
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "holiday_month", "promo_intensity", "weighted_distribution"]


def _wmape(y, yhat):
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    return float(np.abs(y - yhat).sum() / max(y.sum(), 1e-9) * 100)


def _all_metrics(y, yhat):
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    ae = np.abs(y - yhat); ape = ae / np.maximum(y, 1e-9)
    return float(np.mean(ape) * 100), float(np.median(ape) * 100), float(ae.sum() / max(y.sum(), 1e-9) * 100)


def _load(ds, cat, slug):
    sub = "CSD" if cat == "CSD" else cat
    fm = pd.read_parquet(DATASETS[ds] / sub / f"{slug}_feature_matrix.parquet")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    parts = {s: d[d.split == s] for s in ("train", "val", "test")}
    return parts


def _make(model, params):
    if model == "LightGBM":
        from lightgbm import LGBMRegressor
        return LGBMRegressor(random_state=SEED, verbose=-1, **params)
    from xgboost import XGBRegressor
    return XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1, **params)


def _space(trial, model):
    if model == "LightGBM":
        return dict(
            n_estimators=trial.suggest_int("n_estimators", 200, 1200),
            learning_rate=trial.suggest_float("learning_rate", 0.01, 0.15, log=True),
            num_leaves=trial.suggest_int("num_leaves", 15, 128),
            min_child_samples=trial.suggest_int("min_child_samples", 5, 60),
            subsample=trial.suggest_float("subsample", 0.6, 1.0),
            colsample_bytree=trial.suggest_float("colsample_bytree", 0.6, 1.0),
        )
    return dict(
        n_estimators=trial.suggest_int("n_estimators", 200, 1200),
        learning_rate=trial.suggest_float("learning_rate", 0.01, 0.15, log=True),
        max_depth=trial.suggest_int("max_depth", 3, 10),
        min_child_weight=trial.suggest_float("min_child_weight", 1.0, 8.0),
        subsample=trial.suggest_float("subsample", 0.6, 1.0),
        colsample_bytree=trial.suggest_float("colsample_bytree", 0.6, 1.0),
    )


def tune(model, parts, trials):
    tr, va = parts["train"], parts["val"]
    Xtr, ytr = tr[FEATURES].fillna(0.0), tr["log_sales_units"].values
    Xva, yva = va[FEATURES].fillna(0.0), np.expm1(va["log_sales_units"].values)

    def objective(trial):
        m = _make(model, _space(trial, model))
        m.fit(Xtr, ytr)
        return _wmape(yva, np.expm1(m.predict(Xva)))

    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=SEED))
    study.optimize(objective, n_trials=trials, show_progress_bar=False)

    # refit best on train+val, eval on test
    trval = pd.concat([tr, va])
    m = _make(model, study.best_params)
    m.fit(trval[FEATURES].fillna(0.0), trval["log_sales_units"].values)
    te = parts["test"]
    pred = np.expm1(m.predict(te[FEATURES].fillna(0.0)))
    mp, md, wm = _all_metrics(np.expm1(te["log_sales_units"].values), pred)
    return dict(val_wmape=study.best_value, test_wmape=wm, test_mape=mp, test_median=md), study.best_params


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--trials", type=int, default=30)
    trials = ap.parse_args().trials
    OUT.mkdir(parents=True, exist_ok=True)
    rows, params = [], {}
    for ds in DATASETS:
        print(f"\n########## {ds} (trials={trials}) ##########")
        for cat, slug in CATS.items():
            parts = _load(ds, cat, slug)
            if len(parts["train"]) < 30 or len(parts["test"]) == 0:
                continue
            for model in ("LightGBM", "XGBoost"):
                res, best = tune(model, parts, trials)
                rows.append(dict(dataset=ds, category=cat, model=model, **res))
                params[f"{ds}/{cat}/{model}"] = best
                print(f"  {cat:13s} {model:9s} test WMAPE={res['test_wmape']:5.1f}% "
                      f"medMAPE={res['test_median']:5.1f}% (val {res['val_wmape']:5.1f}%)")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "tuned_metrics.csv", index=False)
    (OUT / "tuned_params.json").write_text(json.dumps(params, indent=2))

    lines = ["# SRQ1 benchmark — Optuna-tuned (TPE, seed=42)", "",
             f"Trials per model: {trials}. Tuned on validation (WMAPE), refit on "
             "train+val, evaluated once on test.", ""]
    for ds in DATASETS:
        lines += [f"## Dataset: {ds}", "",
                  "| Category | Model | test WMAPE | test mean MAPE | test median MAPE | val WMAPE |",
                  "|---|---|---|---|---|---|"]
        for _, x in df[df.dataset == ds].iterrows():
            lines.append(f"| {x['category']} | {x['model']} | {x['test_wmape']:.1f}% | "
                         f"{x['test_mape']:.1f}% | {x['test_median']:.1f}% | {x['val_wmape']:.1f}% |")
        lines.append("")
    (OUT / "tuned_summary.md").write_text("\n".join(lines) + "\n")
    print(f"\nSaved tuned_metrics.csv + tuned_params.json + tuned_summary.md in {OUT}")


if __name__ == "__main__":
    main()
