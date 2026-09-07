#!/usr/bin/env python
"""
SRQ1 holiday-enrichment ablation: with vs without, per category, plus SHAP.

WHY A SEPARATE SCRIPT RATHER THAN A FLAG ON srq1_benchmark.py
-------------------------------------------------------------
The benchmark's FEATURES list is the documented feature set behind every SRQ1
number currently in the thesis. Adding the holiday columns to it would change
those numbers as a side effect of running an experiment, and the with/without
comparison would then have no stable reference point.

This script imports the benchmark's model definitions, metrics and loaders
unchanged, and varies ONE thing: whether the three holiday columns are in X.
Same seed, same split, same hyperparameters, same log-scaling. So a difference
in the output is attributable to the features and to nothing else.

THE QUESTION IT ANSWERS
-----------------------
`month`, `quarter` and `peak_month` are already in the feature set, and
Christmas is always December -- so a WMAPE improvement alone does not establish
that the calendar added information rather than re-encoding month-of-year.

Two outputs address that:

  1. Per-category WMAPE delta, reported whatever the sign (P0047 Option C:
     a null result at monthly grain is a finding, not a failure).
  2. SHAP attribution before and after. If holiday attribution rises while
     month/peak_month fall by a comparable amount, it is redistribution. If the
     calendar features earn attribution while the existing calendar features
     hold theirs, it is new signal.

USAGE
    python srq1_holiday_ablation.py                  # all categories
    python srq1_holiday_ablation.py --no-shap        # metrics only, faster
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def _find_repo_root() -> Path:
    """DEC-P0046-ANCHOR: .env.example, walked from __file__."""
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

# Reuse the benchmark verbatim -- same models, same metrics, same seed.
from srq1_benchmark import (  # noqa: E402
    CATS, FEATURES, KEYS, SEED, _fit_predict, _load, _metrics,
    available_features,
)

HOLIDAY_FEATURES = ["days_in_month", "n_holidays", "non_holiday_days"]
CALENDAR_FEATURES = ["month", "quarter", "peak_month"]
MODELS = ["Ridge", "LightGBM", "XGBoost"]
GRAIN = "bymonth"
# Tabular output belongs in the tier's tables/ subfolder, not loose at the
# top of the results dir (DEC-P0046-SINGLE-HOME / the srq1 folder shape).
OUT = get_srq_tables_dir(1)


def _prepare(fm: pd.DataFrame, feats: list[str]):
    """Split and assemble X/y exactly as srq1_benchmark.run_category does."""
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    tr, te = d[d.split == "train"], d[d.split == "test"]
    if len(tr) < 30 or len(te) == 0:
        return None
    cols = [c for c in feats if c in fm.columns]
    return (
        tr[cols].fillna(0.0), tr["log_sales_units"].values,
        te[cols].fillna(0.0), np.expm1(te["log_sales_units"].values),
        cols, len(tr), len(te), d[KEYS[GRAIN]].drop_duplicates().shape[0],
    )


def run_arm(fm: pd.DataFrame, cat: str, feats: list[str], arm: str) -> list[dict]:
    prep = _prepare(fm, feats)
    if prep is None:
        return []
    Xtr, ytr, Xte, ytrue, cols, n_tr, n_te, n_series = prep

    rows = []
    for name in MODELS:
        try:
            pred = np.clip(_fit_predict(name, Xtr, ytr, Xte), 0, None)
            mp, md, wm = _metrics(ytrue, pred)
            rows.append(dict(category=cat, arm=arm, model=name,
                             mape_mean=mp, mape_median=md, wmape=wm,
                             n_features=len(cols), n_train=n_tr, n_test=n_te,
                             n_series=n_series))
        except Exception as exc:  # noqa
            rows.append(dict(category=cat, arm=arm, model=name,
                             mape_mean=np.nan, mape_median=np.nan, wmape=np.nan,
                             n_features=len(cols), n_train=n_tr, n_test=n_te,
                             n_series=n_series, error=str(exc)[:120]))
    return rows


def shap_attribution(fm: pd.DataFrame, feats: list[str]) -> dict[str, float] | None:
    """Mean |SHAP| per feature, normalised to percent of total attribution.

    LightGBM only: it is the model the ablation is judged on, and TreeExplainer
    is exact for it. Percent-of-total rather than raw magnitude so the two arms
    are comparable even though they have different feature counts.
    """
    try:
        import shap
        from lightgbm import LGBMRegressor
    except ImportError:
        return None

    prep = _prepare(fm, feats)
    if prep is None:
        return None
    Xtr, ytr, Xte, _ytrue, cols, *_ = prep

    m = LGBMRegressor(n_estimators=400, learning_rate=0.05, num_leaves=31,
                      subsample=0.8, colsample_bytree=0.8,
                      random_state=SEED, verbose=-1)
    m.fit(Xtr, ytr)
    vals = shap.TreeExplainer(m).shap_values(Xte)
    mean_abs = np.abs(vals).mean(axis=0)
    total = mean_abs.sum()
    if total <= 0:
        return None
    return {c: float(v / total * 100.0) for c, v in zip(cols, mean_abs)}


def main() -> int:
    ap = argparse.ArgumentParser(description="SRQ1 holiday-enrichment ablation")
    ap.add_argument("--no-shap", action="store_true", help="Skip the SHAP pass")
    args = ap.parse_args()

    without = list(FEATURES)
    with_hol = list(FEATURES) + HOLIDAY_FEATURES

    metric_rows, shap_rows = [], []

    for cat, slug in CATS.items():
        fm = _load(GRAIN, cat, slug)
        if fm is None:
            print(f"  {cat:13s} skipped -- no feature matrix")
            continue

        present = [c for c in HOLIDAY_FEATURES if c in fm.columns]
        if not present:
            print(f"  {cat:13s} skipped -- matrix carries no holiday columns. "
                  f"Re-run steps 3-6 with a v1.2 contract.")
            continue

        metric_rows += run_arm(fm, cat, without, "without")
        metric_rows += run_arm(fm, cat, with_hol, "with")
        print(f"  {cat:13s} both arms done ({len(present)} holiday features)")

        if not args.no_shap:
            for arm, feats in (("without", without), ("with", with_hol)):
                att = shap_attribution(fm, feats)
                if att is None:
                    continue
                for feat, pct in att.items():
                    shap_rows.append(dict(category=cat, arm=arm, feature=feat,
                                          shap_pct=pct))

    if not metric_rows:
        print("No categories produced results.")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    met = pd.DataFrame(metric_rows)
    met.to_csv(OUT / "holiday_ablation_metrics.csv", index=False, encoding="utf-8")

    # Per-category delta on WMAPE. Negative = enrichment helped.
    piv = met.pivot_table(index=["category", "model"], columns="arm",
                          values="wmape").reset_index()
    if {"with", "without"} <= set(piv.columns):
        piv["delta_pp"] = piv["with"] - piv["without"]
        piv = piv[["category", "model", "without", "with", "delta_pp"]]
        piv.to_csv(OUT / "holiday_ablation_delta.csv", index=False, encoding="utf-8")
        print("\n=== WMAPE by arm (negative delta = enrichment helped) ===")
        print(piv.to_string(index=False,
                            float_format=lambda v: f"{v:7.2f}"))

    if shap_rows:
        sh = pd.DataFrame(shap_rows)
        sh.to_csv(OUT / "holiday_ablation_shap.csv", index=False, encoding="utf-8")

        # The redistribution test: what happened to the EXISTING calendar
        # features when the holiday ones were added?
        print("\n=== SHAP attribution %, calendar + holiday features ===")
        focus = CALENDAR_FEATURES + HOLIDAY_FEATURES
        sub = sh[sh.feature.isin(focus)]
        tbl = sub.pivot_table(index=["category", "feature"], columns="arm",
                              values="shap_pct").reset_index()
        print(tbl.to_string(index=False, float_format=lambda v: f"{v:6.2f}"))

    print(f"\nWritten -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
