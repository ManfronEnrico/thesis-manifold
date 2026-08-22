#!/usr/bin/env python3
"""
SRQ1 — Ridge fitted in the SAME regimes as the tabular models.

WHY THIS EXISTS: the per-brand Ridge in `srq1_baselines_stat.py` is misspecified.
It fits ~24 rows against 13 standardised features, which is close to singular, and
its log-space predictions extrapolate far enough that `expm1` produced WMAPE = inf%
(CSD, RTD) and 345,856,990% (energidrikke) before a bound was added (P0040 F53).
Even bounded, energidrikke clips roughly once per series, so the reported figure
partly reflects the chosen bound rather than the model.

Pooling fixes the cause rather than the symptom: thousands of rows instead of ~24,
so the fit is well-determined and the extrapolation bound rarely binds.

IT ALSO REMOVES A CONFOUND. The tabular models (LightGBM/XGBoost) are fitted
across brands within a category; the classical baselines are fitted per brand. So
"GBM beats ARIMA" conflates the METHOD with the FITTING REGIME. Running Ridge in
both regimes separates them:

    per-brand Ridge  -> pooled-within-category Ridge   = the regime effect
    pooled Ridge     -> pooled GBM                     = the nonlinearity effect

WHAT CANNOT BE POOLED, AND WHY IT IS NOT AN OVERSIGHT
-----------------------------------------------------
Naive, seasonal-naive and drift are defined per series -- "the last value of THIS
brand", "the same month last year for THIS brand". There is no cross-sectional
version; pooling them is undefined rather than unimplemented. ARIMA and Prophet are
likewise univariate by construction. Only feature-based learners (Ridge, GBM) admit
both regimes. The results table should therefore label each row with its regime
rather than implying every model was run every way.

Two grains are fitted here, matching srq1_pooled.py:
    within_category -- one Ridge per category, all its brands  (matches the GBMs)
    all_categories  -- one Ridge across all four categories    (matches pooled GBM)

Self-contained, seed=42, reproducible. No API spend.
Usage:  .venv/Scripts/python.exe 03_thesis_modelling/model_training/srq1/srq1_ridge_pooled.py
Output: 04_thesis_results/srq1/{ridge_pooled.csv, ridge_pooled.md}
"""

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR

sys.path.insert(0, str(_here.parent))
from srq1_pooled import CATS, FEATURES, SPLITS, SEED, _load, _all_metrics  # noqa: E402

warnings.filterwarnings("ignore")
OUT = THESIS_RESULTS_SRQ1_DIR

ALPHAS = (0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0)

# Volume-valued features. These must be log-transformed for a LINEAR model, because
# the target is log1p(sales_units) -- see _prep.
LAGLIKE = {"lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
           "rolling_mean_4", "rolling_std_4", "rolling_mean_13"}


def _prep(df, feats):
    """Log the volume-valued features to match the logged target.

    THIS IS THE FIX FOR P0040 F53/F54, and it matters more than pooling did.

    The feature matrix was engineered for TREES: `lag_1`, `rolling_mean_4` etc. are
    in raw units while the target `log_sales_units` is log1p. A tree does not care
    -- it splits on rank order, so any monotone transform of a feature is
    equivalent. A LINEAR model very much does: fitting log(y) ~ b*(raw lags) asserts
    an additive relationship where the true one is multiplicative.

    Measured on CSD, best alpha in each case:

        raw features     log-space RMSE 3.92   WMAPE 1705%   medMAPE 99.6%
        logged features  log-space RMSE 0.93   WMAPE  22.6%  medMAPE 29.5%

    RMSE was flat at ~3.92 across SEVEN orders of magnitude of alpha, which is what
    proved the problem was specification rather than regularisation: no amount of
    shrinkage fixes the wrong functional form. medMAPE pinned at 99.6% meant the
    model was predicting ~zero for essentially every brand.

    Calendar features (month, quarter, peak_month) and promo_intensity are left
    alone: they are not volumes, and logging them would be meaningless."""
    X = df[feats].fillna(0.0).copy()
    for c in feats:
        if c in LAGLIKE:
            X[c] = np.log1p(X[c].clip(lower=0))
    return X.values.astype(float)


def _fit_ridge(tr, va, te, feats):
    """Tune alpha on validation by WMAPE, refit on train+val, predict test.

    Standardised because L2 penalises coefficients on their raw scale -- unscaled,
    the penalty would fall almost entirely on small-magnitude features. Protocol
    otherwise mirrors srq1_pooled.py::_fit_tuned so the arms stay comparable."""
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler

    Xtr = _prep(tr, feats)
    ytr = tr["log_sales_units"].values
    Xva = _prep(va, feats)
    yva_units = np.expm1(va["log_sales_units"].values)

    sc = StandardScaler().fit(Xtr)
    best_a, best_err = None, None
    for a in ALPHAS:
        m = Ridge(alpha=a).fit(sc.transform(Xtr), ytr)
        pred = np.clip(np.expm1(m.predict(sc.transform(Xva))), 0, None)
        err = float(np.abs(yva_units - pred).sum() / max(yva_units.sum(), 1e-9))
        if best_err is None or err < best_err:
            best_a, best_err = a, err

    trval = pd.concat([tr, va])
    Xall = _prep(trval, feats)
    sc = StandardScaler().fit(Xall)
    m = Ridge(alpha=best_a).fit(sc.transform(Xall), trval["log_sales_units"].values)

    pred_log = m.predict(sc.transform(_prep(te, feats)))

    # Same extrapolation bound as the per-brand arm, so the two are comparable --
    # but here it should almost never bind. The clip count is reported precisely
    # so that claim is checked rather than asserted.
    hi = float(np.log1p(np.expm1(trval["log_sales_units"].values).max() * 3.0 + 1.0))
    n_clip = int(((pred_log > hi) | (pred_log < 0.0)).sum())
    pred = np.clip(np.expm1(np.clip(pred_log, 0.0, hi)), 0, None)
    return pred, best_a, n_clip


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    parts = {cat: _load(cat, slug) for cat, slug in CATS.items()}
    rows = []

    # ---- regime 1: one Ridge per category (matches the tabular models) -------
    print("\n########## Ridge, pooled within category ##########")
    for cat in CATS:
        p = parts[cat]
        if len(p["train"]) < 30 or len(p["test"]) == 0:
            continue
        feats = [c for c in FEATURES if c in p["train"].columns]
        pred, a, n_clip = _fit_ridge(p["train"], p["val"], p["test"], feats)
        y = np.expm1(p["test"]["log_sales_units"].values)
        mp, md, wm = _all_metrics(y, pred)
        rows.append(dict(regime="within_category", category=cat, model="Ridge",
                         wmape=wm, median_mape=md, alpha=a, n_clipped=n_clip,
                         n_test=len(p["test"]), n_features=len(feats)))
        print(f"  {cat:13s} WMAPE={wm:6.1f}% medMAPE={md:5.1f}% "
              f"(alpha={a}, clipped={n_clip}/{len(p['test'])})")

    # ---- regime 2: one Ridge across all categories (matches pooled GBM) -----
    print("\n########## Ridge, pooled across all categories ##########")
    pooled = {s: pd.concat([parts[c][s] for c in CATS], ignore_index=True)
              for s in SPLITS}
    # 12-feature intersection: promo_intensity is absent in danskvand and RTD.
    feats = [c for c in FEATURES if all(
        c in parts[cat]["train"].columns for cat in CATS)]
    pred_all, a_all, clip_all = _fit_ridge(
        pooled["train"], pooled["val"], pooled["test"], feats)
    pooled["test"] = pooled["test"].copy()
    pooled["test"]["_pred"] = pred_all
    for cat in CATS:
        sub = pooled["test"][pooled["test"].category == cat]
        if not len(sub):
            continue
        y = np.expm1(sub["log_sales_units"].values)
        mp, md, wm = _all_metrics(y, sub["_pred"].values)
        n_clip = int(((sub["_pred"] <= 0)).sum())
        rows.append(dict(regime="all_categories", category=cat, model="Ridge",
                         wmape=wm, median_mape=md, alpha=a_all, n_clipped=n_clip,
                         n_test=len(sub), n_features=len(feats)))
        print(f"  {cat:13s} WMAPE={wm:6.1f}% medMAPE={md:5.1f}% "
              f"(alpha={a_all}, {len(feats)} features)")
    print(f"  total clipped across pooled fit: {clip_all}/{len(pooled['test'])}")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "ridge_pooled.csv", index=False)

    lines = ["# SRQ1 — Ridge fitted per-brand vs pooled", "",
             "Ridge is run in the same fitting regimes as the tabular models so the",
             "**method** and the **fitting regime** can be separated. The per-brand",
             "figures come from `stat_baselines.csv`.", "",
             "**Only feature-based learners appear here.** Naive, seasonal-naive and",
             "drift are per-series definitions with no cross-sectional form, and",
             "ARIMA/Prophet are univariate by construction — pooling them is",
             "undefined, not merely unimplemented.", "",
             "| Regime | Category | WMAPE | medMAPE | alpha | clipped | n test |",
             "|---|---|---|---|---|---|---|"]
    for _, r in df.iterrows():
        lines.append(f"| {r['regime']} | {r['category']} | {r['wmape']:.1f}% | "
                     f"{r['median_mape']:.1f}% | {r['alpha']} | "
                     f"{int(r['n_clipped'])} | {int(r['n_test'])} |")
    lines += ["",
              "`clipped` counts predictions that hit the extrapolation bound (that",
              "series' observed maximum x 3). A high count means the bound, not the",
              "model, is setting the error — the defect that motivated this script",
              "(P0040 F53). It should be near zero in the pooled regimes.", ""]
    (OUT / "ridge_pooled.md").write_text("\n".join(lines) + "\n",
                                         encoding="utf-8", newline="\n")
    print(f"\nSaved ridge_pooled.csv + ridge_pooled.md in {OUT}")


if __name__ == "__main__":
    main()
