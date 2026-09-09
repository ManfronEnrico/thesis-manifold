#!/usr/bin/env python
"""
Holiday-enrichment ablation on the TUNED benchmark. These are the thesis numbers.

WHY THIS SUPERSEDES srq1_holiday_ablation.py
--------------------------------------------
The first ablation ran against `srq1_benchmark.py`, whose hyperparameters are
fixed (LightGBM n_estimators=400, lr=0.05, num_leaves=31; XGBoost n_estimators
=500, lr=0.05, max_depth=6). Measuring a FEATURE change on a model whose
CAPACITY is frozen confounds the two: three extra columns at fixed capacity can
degrade a model that would have absorbed them at a slightly different depth or
leaf count, and the untuned result cannot distinguish "the feature is unhelpful"
from "the fixed configuration could not accommodate it".

`srq1_benchmark_tuned.py` is the track the thesis reports, so the ablation has
to run there: tune each arm SEPARATELY with its own Optuna study, then compare.
Tuning only the enriched arm (or only the baseline) would hand one side an
advantage that has nothing to do with the features.

PROTOCOL (inherited unchanged from srq1_benchmark_tuned.tune)
------------------------------------------------------------
  - hyperparameters chosen on VALIDATION only
  - best configuration refit on train+val
  - test scored exactly once per (category, model, arm)
  - same seed for both arms, so the search paths are comparable

Ridge is included via `srq1_ridge_cv`, whose alpha is chosen by rolling-origin
CV -- otherwise the linear track would be the only untuned model in the table.

USAGE
    python srq1_holiday_ablation_tuned.py                # 30 trials/arm
    python srq1_holiday_ablation_tuned.py --trials 50
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

import srq1_benchmark_tuned as TUNED  # noqa: E402
import srq1_ridge_cv as RCV  # noqa: E402
from srq1_benchmark import CATS, FEATURES, _load as _load_fm, _metrics  # noqa: E402

HOLIDAY_FEATURES = ["days_in_month", "n_holidays", "non_holiday_days"]
GRAIN = "bymonth"
# Tabular output belongs in the tier's tables/ subfolder, not loose at the
# top of the results dir (DEC-P0046-SINGLE-HOME / the srq1 folder shape).
OUT = (results_root() / "tables")
TREE_MODELS = ["LightGBM", "XGBoost"]

# The two benchmarks key the SAME directory under different names --
# srq1_benchmark uses "bymonth", srq1_benchmark_tuned uses "brand". Resolve it
# from the module rather than hard-coding either, so this keeps working if
# a grain is ever renamed or added on one side only.
TUNED_GRAIN = next(iter(TUNED.DATASETS))


def _arm_features(fm: pd.DataFrame, with_holiday: bool) -> list[str]:
    """Discovered from the matrix, never asserted (DEC-DISCOVER-COLUMNS).

    The arms are derived by SUBTRACTION. FEATURES used to be 13 and excluded the
    holiday columns, so "with" was FEATURES + HOLIDAY_FEATURES. Since the
    centralization fix (P0049 F31) the canonical set is 18 and already contains
    them, so that addition duplicated three columns and LightGBM rejected the run:
    `Feature (days_in_month) appears more than one time.` (P0053 F3).
    """
    wanted = (list(FEATURES) if with_holiday
              else [c for c in FEATURES if c not in set(HOLIDAY_FEATURES)])
    return [c for c in wanted if c in fm.columns]


def ridge_arm(fm: pd.DataFrame, feats: list[str], folds: int, min_train: int):
    """Ridge with rolling-origin CV alpha. Same selection protocol as the trees:
    hyperparameter on development data only, test scored once."""
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    dev, te = d[d.split.isin(["train", "val"])], d[d.split == "test"]
    if len(dev) < 30 or len(te) == 0:
        return None

    alpha, _grid = RCV.cv_select_alpha(dev, feats, folds, min_train)
    if not np.isfinite(alpha):
        return None

    pred = RCV._fit_ridge(dev[feats].fillna(0.0),
                          dev["log_sales_units"].values,
                          te[feats].fillna(0.0), alpha)
    mp, md, wm = _metrics(np.expm1(te["log_sales_units"].values), pred)
    return {"test_wmape": wm, "test_mape": mp, "test_median": md,
            "hyperparams": f"alpha={alpha:.4g}"}


def main() -> int:
    ap = argparse.ArgumentParser(description="Tuned holiday ablation")
    ap.add_argument("--trials", type=int, default=30,
                    help="Optuna trials per arm per model (default 30)")
    ap.add_argument("--folds", type=int, default=4, help="Ridge CV folds")
    ap.add_argument("--min-train", type=int, default=18)
    args = ap.parse_args()

    rows = []

    for cat, slug in CATS.items():
        fm = _load_fm(GRAIN, cat, slug)
        if fm is None:
            print(f"  {cat:13s} skipped -- no feature matrix")
            continue
        if not any(c in fm.columns for c in HOLIDAY_FEATURES):
            print(f"  {cat:13s} skipped -- no holiday columns; re-run steps 3-6")
            continue

        for arm, with_hol in (("without", False), ("with", True)):
            feats = _arm_features(fm, with_hol)

            # Trees: a separate Optuna study per arm, same seed.
            parts, _disc = TUNED._load(TUNED_GRAIN, cat, slug)
            for model in TREE_MODELS:
                res, best = TUNED.tune(model, parts, feats, args.trials)
                rows.append(dict(category=cat, arm=arm, model=model,
                                 n_features=len(feats),
                                 val_wmape=res["val_wmape"],
                                 test_wmape=res["test_wmape"],
                                 test_mape=res["test_mape"],
                                 test_median=res["test_median"],
                                 hyperparams=str(best)))
                print(f"  {cat:13s} {arm:8s} {model:9s} "
                      f"test WMAPE={res['test_wmape']:6.2f}")

            r = ridge_arm(fm, feats, args.folds, args.min_train)
            if r:
                rows.append(dict(category=cat, arm=arm, model="Ridge",
                                 n_features=len(feats), val_wmape=np.nan,
                                 **r))
                print(f"  {cat:13s} {arm:8s} {'Ridge':9s} "
                      f"test WMAPE={r['test_wmape']:6.2f}")

    if not rows:
        print("No results.")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "holiday_ablation_tuned_metrics.csv", index=False,
              encoding="utf-8")

    piv = df.pivot_table(index=["category", "model"], columns="arm",
                         values="test_wmape").reset_index()
    if {"with", "without"} <= set(piv.columns):
        piv["delta_pp"] = piv["with"] - piv["without"]
        piv = piv[["category", "model", "without", "with", "delta_pp"]]
        piv.to_csv(OUT / "holiday_ablation_tuned_delta.csv", index=False,
                   encoding="utf-8")

        print("\n=== TUNED: test WMAPE by arm (negative delta = holiday helped) ===")
        print(piv.to_string(index=False, float_format=lambda v: f"{v:7.2f}"))

        helped = int((piv["delta_pp"] < 0).sum())
        print(f"\nhelped in {helped} of {len(piv)} category x model combinations")
        print(f"mean delta: {piv['delta_pp'].mean():+.2f} pp")
        print("\nPer-category and per-model deltas are the result. Do NOT quote "
              "the mean alone:\nit averages over model families that respond "
              "differently, which is itself a finding.")

    print(f"\nWritten -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
