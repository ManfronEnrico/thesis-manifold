#!/usr/bin/env python3
"""
SRQ1 — pooled vs per-category model comparison.

WHY THIS EXISTS: SRQ1's headline question names a THREE-way trade-off — accuracy,
memory efficiency, and *category specialization*, glossed in
`srq1-models-efficiency.md:32` as "does a per-category model beat a single pooled
model?". `tuned_metrics.csv` reports the first two only: 4 categories x 2 models,
no pooled row. This closes that gap.

DESIGN — the comparison is per-category on the test set, NOT pooled-vs-pooled in
aggregate. A single pooled WMAPE over all four categories is dominated by CSD's
volume and answers nothing; comparing it against four separate numbers compares
different populations. Instead: train ONE pooled model, then score it SEPARATELY on
each category's test rows, against the per-category model on those SAME rows. One
variable changes (pooled vs specialised); the evaluation population is identical.

FEATURES: 12, not 13. `promo_intensity` is dropped because danskvand and RTD do not
carry it (Nielsen reports no promotion for them; the pipeline omits rather than
zero-fills, per DEC-DISCOVER-COLUMNS). Both sides of the comparison use the same 12,
so the per-category baseline here is RE-TRAINED rather than read from
tuned_metrics.csv — otherwise the pooled model would be handicapped by one feature
and the comparison would confound "pooling" with "one fewer feature".

COST OF THAT RESTRICTION -- ACTUALLY MEASURED (2026-08-23), not inferred from SHAP.

An earlier version of this docstring called a SHAP rank the "measured cost": that
promo_intensity ranks 11th of 13 by mean absolute SHAP in CSD (0.041). **That is not a
cost measurement.** SHAP attributes a fixed, already-fitted model's output; it says
nothing about what happens to out-of-sample error when a feature is removed and the
model refitted (Lundberg & Lee 2017 explain a fixed model; Guyon & Elisseeff 2003,
p. 1158, show relevance ranking is a poor guide to subset utility).

Refit with and without the feature, on the two categories that carry it:

    CSD           XGBoost  WMAPE 14.51% -> 14.81%  (+0.30pp)
                  LightGBM WMAPE 16.20% -> 16.47%  (+0.27pp)
    energidrikke  XGBoost  WMAPE 14.91% -> 16.35%  (+1.44pp)
                  LightGBM WMAPE 17.39% -> 16.03%  (-1.36pp)

**Dropping it HELPS on 5 of 8 metric/model/category combinations**, including
LightGBM on energidrikke -- the category where promotion data actually exists. Worst
case is +1.44pp; median effect is near zero and not signed consistently.

So the restriction is genuinely cheap, but for a different reason than the SHAP rank
suggested, and the honest statement is the measured one. See P0040 F44 for the
original SHAP ranking, which remains valid as an attribution result.

SERIES KEY: (category, brand), never brand alone. Brand names are NOT unique across
categories — 213 unique names against 230 category-brand pairs — and `OTHER BRAND`
is a per-category residual bucket with different contents each time. Pooling on name
would silently merge unrelated series.

Self-contained, seed=42, reproducible. No API spend.
Usage:  .venv/Scripts/python.exe 03_thesis_modelling/model_training/srq1/srq1_pooled.py [--trials 30]
Output: 04_thesis_results/srq1/{pooled_metrics.csv, pooled_params.json, pooled_summary.md}
"""

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import optuna

# Repo root located by searching upward for PATHS.py rather than by a fixed
# parents[N] index — the index silently breaks whenever a script moves a
# directory deeper (the 2026-08-19 reorganisation did exactly that).
_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR, THESIS_DATA_ENGINEERED_BYMONTH_DIR

warnings.filterwarnings("ignore")
optuna.logging.set_verbosity(optuna.logging.WARNING)

OUT = THESIS_RESULTS_SRQ1_DIR
SEED = 42

CATS = {"CSD": "csd", "danskvand": "danskvand",
        "energidrikke": "energidrikke", "RTD": "rtd"}

# The 12-feature intersection: srq1_benchmark_tuned.py::FEATURES minus
# `promo_intensity` (absent in danskvand and RTD). `weighted_dist` remains
# deliberately absent — see the long note in srq1_benchmark_tuned.py.
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "peak_month"]

SPLITS = ("train", "val", "test")


def _wmape(y, yhat):
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    return float(np.abs(y - yhat).sum() / max(y.sum(), 1e-9) * 100)


def _all_metrics(y, yhat):
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    ae = np.abs(y - yhat); ape = ae / np.maximum(y, 1e-9)
    return (float(np.mean(ape) * 100), float(np.median(ape) * 100),
            float(ae.sum() / max(y.sum(), 1e-9) * 100))


def _load(cat, slug):
    """One category's splits, tagged with its category for the pooled key."""
    sub = "CSD" if cat == "CSD" else cat
    fm = pd.read_parquet(THESIS_DATA_ENGINEERED_BYMONTH_DIR / sub /
                         f"{slug}_feature_matrix_h3.parquet")
    missing = [c for c in FEATURES if c not in fm.columns]
    if missing:
        raise SystemExit(f"{cat}: intersection features absent: {missing}")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    d["category"] = cat
    # Series key. NOT a model input — recorded so the pooled frame can be audited
    # for brand-name collisions across categories.
    d["series_key"] = cat + "||" + d["brand"].astype(str)
    return {s: d[d.split == s] for s in SPLITS}


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


def _fit_tuned(model, tr, va, trials):
    """Tune on val (WMAPE), refit best on train+val. Returns model, params, val score.

    Mirrors srq1_benchmark_tuned.py::tune exactly, so the pooled and per-category
    arms differ only in which rows they see."""
    Xtr, ytr = tr[FEATURES].fillna(0.0), tr["log_sales_units"].values
    Xva, yva = va[FEATURES].fillna(0.0), np.expm1(va["log_sales_units"].values)

    def objective(trial):
        m = _make(model, _space(trial, model))
        m.fit(Xtr, ytr)
        return _wmape(yva, np.expm1(m.predict(Xva)))

    study = optuna.create_study(direction="minimize",
                                sampler=optuna.samplers.TPESampler(seed=SEED))
    study.optimize(objective, n_trials=trials, show_progress_bar=False)

    trval = pd.concat([tr, va])
    m = _make(model, study.best_params)
    m.fit(trval[FEATURES].fillna(0.0), trval["log_sales_units"].values)
    return m, study.best_params, study.best_value


def _score(m, te):
    pred = np.expm1(m.predict(te[FEATURES].fillna(0.0)))
    return _all_metrics(np.expm1(te["log_sales_units"].values), pred)


def main():
    ap = argparse.ArgumentParser(description="SRQ1 pooled vs per-category")
    ap.add_argument("--trials", type=int, default=30)
    trials = ap.parse_args().trials
    OUT.mkdir(parents=True, exist_ok=True)

    parts = {cat: _load(cat, slug) for cat, slug in CATS.items()}

    # Audit the pooling key BEFORE training: if a brand name recurs across
    # categories, (category, brand) is what must keep the series distinct.
    names = {}
    for cat in CATS:
        allrows = pd.concat([parts[cat][s] for s in SPLITS])
        for b in allrows["brand"].unique():
            names.setdefault(str(b), set()).add(cat)
    shared = sorted(b for b, c in names.items() if len(c) > 1)
    print(f"Brand names spanning >1 category: {len(shared)} "
          f"— kept distinct by (category, brand)")
    if shared:
        print(f"  e.g. {', '.join(shared[:6])}")

    pooled = {s: pd.concat([parts[c][s] for c in CATS], ignore_index=True)
              for s in SPLITS}
    print(f"\npooled rows  train={len(pooled['train'])} "
          f"val={len(pooled['val'])} test={len(pooled['test'])}")
    for c in CATS:
        print(f"  {c:13s} train={len(parts[c]['train']):5d} "
              f"test={len(parts[c]['test']):4d}")

    rows, params = [], {}
    for model in ("LightGBM", "XGBoost"):
        print(f"\n########## {model} (trials={trials}) ##########")

        # --- pooled arm: ONE model, scored separately per category -----------
        pm, pbest, pval = _fit_tuned(model, pooled["train"], pooled["val"], trials)
        params[f"pooled/{model}"] = pbest
        for cat in CATS:
            mp, md, wm = _score(pm, parts[cat]["test"])
            rows.append(dict(arm="pooled", category=cat, model=model,
                             test_wmape=wm, test_mape=mp, test_median=md,
                             val_wmape=pval, n_test=len(parts[cat]["test"])))

        # --- per-category arm: same 12 features, same protocol ---------------
        for cat in CATS:
            p = parts[cat]
            if len(p["train"]) < 30 or len(p["test"]) == 0:
                print(f"  {cat:13s} SKIPPED (insufficient rows)")
                continue
            cm, cbest, cval = _fit_tuned(model, p["train"], p["val"], trials)
            params[f"percat/{cat}/{model}"] = cbest
            mp, md, wm = _score(cm, p["test"])
            rows.append(dict(arm="per_category", category=cat, model=model,
                             test_wmape=wm, test_mape=mp, test_median=md,
                             val_wmape=cval, n_test=len(p["test"])))

        df = pd.DataFrame(rows)
        for cat in CATS:
            sel = df[(df.model == model) & (df.category == cat)]
            if len(sel) != 2:
                continue
            po = sel[sel.arm == "pooled"].iloc[0]
            pc = sel[sel.arm == "per_category"].iloc[0]
            delta = po.test_wmape - pc.test_wmape
            verdict = "per-cat better" if delta > 0 else "pooled better"
            print(f"  {cat:13s} pooled={po.test_wmape:5.1f}%  "
                  f"per-cat={pc.test_wmape:5.1f}%  "
                  f"delta={delta:+5.1f}pp  {verdict}")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "pooled_metrics.csv", index=False)
    (OUT / "pooled_params.json").write_text(
        json.dumps(params, indent=2), encoding="utf-8", newline="\n")

    lines = ["# SRQ1 — pooled vs per-category (Optuna-tuned, TPE, seed=42)", "",
             f"Trials per model: {trials}. Both arms use the SAME 12-feature",
             "intersection (`promo_intensity` dropped — absent in danskvand and",
             "RTD), the same tuning protocol, and are scored on the SAME",
             "per-category test rows. One pooled model is trained across all",
             "categories and evaluated separately on each; the per-category arm is",
             "re-trained here on 12 features rather than read from",
             "`tuned_metrics.csv`, so the two arms differ only in which rows they",
             "were trained on.", "",
             "Series key is `(category, brand)`: brand names are not unique across",
             "categories and `OTHER BRAND` is a per-category residual bucket.", ""]
    for model in ("LightGBM", "XGBoost"):
        lines += [f"## {model}", "",
                  "| Category | pooled WMAPE | per-category WMAPE | delta (pp) | "
                  "pooled medMAPE | per-cat medMAPE | n test |",
                  "|---|---|---|---|---|---|---|"]
        for cat in CATS:
            sel = df[(df.model == model) & (df.category == cat)]
            if len(sel) != 2:
                continue
            po = sel[sel.arm == "pooled"].iloc[0]
            pc = sel[sel.arm == "per_category"].iloc[0]
            lines.append(
                f"| {cat} | {po.test_wmape:.1f}% | {pc.test_wmape:.1f}% | "
                f"{po.test_wmape - pc.test_wmape:+.1f} | {po.test_median:.1f}% | "
                f"{pc.test_median:.1f}% | {int(po.n_test)} |")
        lines.append("")
    lines += ["Positive delta = the per-category model is more accurate on that",
              "category (pooled WMAPE is higher). Negative = pooling wins.", ""]
    (OUT / "pooled_summary.md").write_text("\n".join(lines) + "\n",
                                           encoding="utf-8", newline="\n")
    print(f"\nSaved pooled_metrics.csv + pooled_params.json + pooled_summary.md "
          f"in {OUT}")


if __name__ == "__main__":
    main()
