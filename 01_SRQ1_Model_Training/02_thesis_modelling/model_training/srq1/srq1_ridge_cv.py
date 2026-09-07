#!/usr/bin/env python
"""
Ridge with rolling-origin cross-validated alpha, per category.

WHY THIS EXISTS
---------------
`srq1_benchmark.py` fits `Ridge(alpha=1.0)` -- one hard-coded value, for every
category, chosen by nobody. Alpha is the ONLY hyperparameter Ridge has: it sets
how hard coefficients are shrunk, which is precisely the control that decides
whether a collinear design matrix produces a stable model or a noise-chasing
one. On a feature set where 12-13 of 15 features exceed VIF 10, leaving it
unset is not a neutral default -- it is an unmeasured assumption sitting under
every reported Ridge number.

A single train/val split is not enough to fix it either. With ~29 training
months and ~6 validation months, one split selects alpha against six months of
noise. The estimate is unstable and the selection is not reproducible under a
different cut.

METHOD
------
Rolling-origin cross-validation (also called time-series or forward-chaining
CV): each fold trains on everything up to a cut and validates on the next block,
so training data always precedes validation data.

Ordinary k-fold is INVALID here and the reason is not pedantic: shuffling would
put future months in the training fold and score the model on the past, which
neither matches how the model is deployed nor respects the autocorrelation the
lag features are built from.

Selection uses the mean WMAPE across folds -- the same metric the thesis
reports, so alpha is chosen for the objective actually being optimised. The
test split is untouched by this file.

Reference for the ridge/collinearity relationship: Hastie, Tibshirani &
Friedman, *The Elements of Statistical Learning*, ch. "Linear Methods for
Regression" (in the project library, key LR3KF2SX). NOTE: no threshold in this
file is taken from any source -- alphas are searched, not asserted.

USAGE
    python srq1_ridge_cv.py
    python srq1_ridge_cv.py --folds 5
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def _find_repo_root() -> Path:
    start = Path(__file__).resolve().parent
    for cand in (start, *start.parents):
        if any((cand / a).exists() for a in (".env.example", ".env", "PATHS.py")):
            return cand
    raise FileNotFoundError(f"Could not find project root above {start}")


_REPO_ROOT = _find_repo_root()
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PATHS import get_srq_tables_dir  # noqa: E402
# The active horizon, and the paths that follow from it. ONE source, so the
# matrix read and the results written can never describe different horizons
# (P0049 F24). Set SRQ1_HORIZON=1 to run the secondary horizon.
from _horizon import HORIZON, matrix_path, results_root, banner  # noqa: E402,F401

from srq1_benchmark import CATS, FEATURES, _load, _log_scale, _metrics  # noqa: E402

HOLIDAY_FEATURES = ["days_in_month", "n_holidays", "non_holiday_days"]
GRAIN = "bymonth"
# Tabular output belongs in the tier's tables/ subfolder, not loose at the
# top of the results dir (DEC-P0046-SINGLE-HOME / the srq1 folder shape).
OUT = (results_root() / "tables")

# Searched, not asserted. Wide enough that the optimum is interior rather than
# at a boundary -- an optimum at an endpoint means the grid, not the data,
# chose the value, and that is reported when it happens.
ALPHA_GRID = np.logspace(-3, 4, 40)


def _fit_ridge(Xtr, ytr, Xte, alpha):
    from sklearn.linear_model import Ridge
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    m = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
    m.fit(_log_scale(Xtr), ytr)
    return np.clip(np.expm1(m.predict(_log_scale(Xte))), 0, None)


def rolling_origin_folds(dates: pd.Series, n_folds: int, min_train: int):
    """Yield (train_mask, val_mask) with training always before validation.

    Cuts are placed on the sorted unique months so every fold validates on a
    contiguous block of real calendar months, not on an arbitrary row count.
    """
    months = np.array(sorted(dates.unique()))
    if len(months) < min_train + n_folds:
        return
    block = max(1, (len(months) - min_train) // n_folds)
    for k in range(n_folds):
        cut = min_train + k * block
        if cut + block > len(months):
            break
        tr_months = months[:cut]
        va_months = months[cut:cut + block]
        yield dates.isin(tr_months).values, dates.isin(va_months).values


def cv_select_alpha(d: pd.DataFrame, feats: list[str], n_folds: int,
                    min_train: int) -> tuple[float, pd.DataFrame]:
    """Return (best alpha, per-alpha fold scores) by rolling-origin CV."""
    rows = []
    for alpha in ALPHA_GRID:
        scores = []
        for tr_m, va_m in rolling_origin_folds(d["date"], n_folds, min_train):
            tr, va = d[tr_m], d[va_m]
            if len(tr) < 30 or len(va) == 0:
                continue
            pred = _fit_ridge(tr[feats].fillna(0.0),
                              tr["log_sales_units"].values,
                              va[feats].fillna(0.0), alpha)
            scores.append(_metrics(np.expm1(va["log_sales_units"].values), pred)[2])
        if scores:
            rows.append({"alpha": alpha, "cv_wmape_mean": float(np.mean(scores)),
                         "cv_wmape_std": float(np.std(scores)),
                         "n_folds_used": len(scores)})

    if not rows:
        return float("nan"), pd.DataFrame()
    grid = pd.DataFrame(rows)
    best = grid.loc[grid["cv_wmape_mean"].idxmin(), "alpha"]
    return float(best), grid


def main() -> int:
    ap = argparse.ArgumentParser(description="Ridge with CV-selected alpha")
    ap.add_argument("--folds", type=int, default=4)
    ap.add_argument("--min-train", type=int, default=18,
                    help="Minimum training months in the first fold")
    args = ap.parse_args()

    results, grids = [], []

    for cat, slug in CATS.items():
        fm = _load(GRAIN, cat, slug)
        if fm is None:
            print(f"  {cat:13s} skipped -- no feature matrix")
            continue

        d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
        te = d[d.split == "test"]
        # CV runs on train+val only. Test is never seen during selection.
        dev = d[d.split.isin(["train", "val"])]
        if len(dev) < 30 or len(te) == 0:
            print(f"  {cat:13s} skipped -- insufficient rows")
            continue

        for arm, extra in (("without", []), ("with", HOLIDAY_FEATURES)):
            feats = [c for c in list(FEATURES) + extra if c in fm.columns]

            best, grid = cv_select_alpha(dev, feats, args.folds, args.min_train)
            if not np.isfinite(best):
                continue
            grid.insert(0, "category", cat)
            grid.insert(1, "arm", arm)
            grids.append(grid)

            # Refit on all development data at the selected alpha, score once.
            pred = _fit_ridge(dev[feats].fillna(0.0),
                              dev["log_sales_units"].values,
                              te[feats].fillna(0.0), best)
            mp, md, wm = _metrics(np.expm1(te["log_sales_units"].values), pred)

            # The hard-coded baseline, for comparison on identical inputs.
            pred1 = _fit_ridge(dev[feats].fillna(0.0),
                               dev["log_sales_units"].values,
                               te[feats].fillna(0.0), 1.0)
            _, _, wm1 = _metrics(np.expm1(te["log_sales_units"].values), pred1)

            at_edge = bool(best <= ALPHA_GRID[0] * 1.01
                           or best >= ALPHA_GRID[-1] * 0.99)
            results.append({
                "category": cat, "arm": arm, "alpha_cv": best,
                "test_wmape_cv": wm, "test_wmape_alpha1": wm1,
                "improvement_pp": wm1 - wm, "test_mape_mean": mp,
                "test_mape_median": md, "alpha_at_grid_edge": at_edge,
                "n_features": len(feats),
            })
            print(f"  {cat:13s} {arm:8s} alpha={best:9.3f}  "
                  f"CV-WMAPE={wm:6.2f}  (alpha=1: {wm1:6.2f})"
                  f"{'  [GRID EDGE]' if at_edge else ''}")

    if not results:
        print("No results.")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    res = pd.DataFrame(results)
    res.to_csv(OUT / "ridge_cv_alpha.csv", index=False, encoding="utf-8")
    pd.concat(grids, ignore_index=True).to_csv(
        OUT / "ridge_cv_alpha_grid.csv", index=False, encoding="utf-8")

    print("\n=== Ridge: CV-selected alpha vs hard-coded alpha=1 ===")
    print(res[["category", "arm", "alpha_cv", "test_wmape_alpha1",
               "test_wmape_cv", "improvement_pp"]]
          .to_string(index=False, float_format=lambda v: f"{v:8.2f}"))

    print(f"\nmean improvement from CV-selecting alpha: "
          f"{res['improvement_pp'].mean():+.2f} pp")

    piv = res.pivot_table(index="category", columns="arm", values="test_wmape_cv")
    if {"with", "without"} <= set(piv.columns):
        piv["holiday_delta_pp"] = piv["with"] - piv["without"]
        print("\n=== Holiday effect, both arms properly tuned ===")
        print(piv.to_string(float_format=lambda v: f"{v:8.2f}"))

    if res["alpha_at_grid_edge"].any():
        print("\nWARNING: an alpha landed on the search-grid boundary; widen "
              "ALPHA_GRID before trusting those rows.")

    print(f"\nWritten -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
