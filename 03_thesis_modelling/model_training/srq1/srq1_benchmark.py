#!/usr/bin/env python3
"""
SRQ1 forecasting benchmark — grain-aware, corrected DVH EXCL. HD matrices.

Trains, per category, on the regenerated feature matrices and reports test-set
accuracy for a baseline ladder:
    SeasonalNaive (lag_13 -> fallback lag_1) | Ridge | LightGBM | XGBoost
Metrics: median per-series MAPE, mean MAPE, and WMAPE (volume-weighted — the
business metric). Forward-chaining split is already encoded in the `split` column.

Grain: brand x month only. DEC-GRAIN (2026-07-12) locked the thesis grain to
brand x month; the chain and region grains were dropped to a documented
limitation + future work, and `_03_engineered/bychain/` was deleted from disk
(P0035, 2026-08-01). The --grain/--grains switch is retained so a future grain
can be registered in DATASETS, but `bymonth` is currently the only valid value.

Self-contained: reads only local parquet matrices. No Prometheus/Nika dependency.

Usage:  .venv/bin/python scripts/srq1_benchmark.py
        .venv/bin/python scripts/srq1_benchmark.py --grain bymonth
Output: 04_thesis_results/srq1/{metrics.csv, summary.md}
"""

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

# Repo root located by searching upward for PATHS.py rather than by a fixed
# parents[N] index: the index silently breaks whenever a script moves a
# directory deeper, which is exactly what happened in the 2026-08-19
# reorganisation (ModuleNotFoundError: No module named 'PATHS').
_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR, THESIS_DATA_ENGINEERED_BYMONTH_DIR

warnings.filterwarnings("ignore")

OUT = THESIS_RESULTS_SRQ1_DIR
SEED = 42

CATS = {"CSD": "csd", "danskvand": "danskvand",
        "energidrikke": "energidrikke", "RTD": "rtd"}

DATASETS = {
    "bymonth": THESIS_DATA_ENGINEERED_BYMONTH_DIR,
}
DEFAULT_GRAINS = ["bymonth"]

# weighted_dist is deliberately ABSENT from this list (P0036 task 7, 2026-08-19).
#
# Not because it leaks -- it was tested and cleared. It is never lagged, which
# made it a candidate, but it is structural and barely moves: corr(wd[t], wd[t-1])
# = 0.976, corr(wd[t], wd[t+3]) = 0.946, median month-on-month change 0.00114 on a
# 0-1 scale. Month t's value is a sound proxy for t+3 because it essentially is
# t+3's value.
#
# It is absent because it does not improve out-of-sample accuracy. Fit with and
# without (LightGBM, 300 trees, seeds 42/7/2024 -- identical, deterministic):
#
#     category        without    with     lagged
#     CSD              17.20%   18.24%   18.32%
#     Danskvand        33.39%   34.36%   32.89%
#     Energidrikke     17.40%   16.94%   16.86%
#     RTD              31.83%   32.54%   31.26%
#
# Worse in 3 of 4 categories. Carrying an unlagged contemporaneous measure that
# does not help means defending "why does your feature read the month it
# predicts?" for no measured benefit.
#
# The column REMAINS in the feature matrix -- distribution is descriptively
# important and appears in the data chapter. This removes it only from what the
# models consume. If reintroduced, use the LAGGED form, which was better in 3 of
# 4 and removes the timing objection entirely.
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "peak_month",
            "promo_intensity"]

def available_features(fm, wanted=None):
	"""Return the wanted features that this matrix actually contains.

	DEC-OPEN-WORLD: categories differ in capability, not just in values.
	Danskvand and RTD carry no `promo_units` (Nielsen does not report promotion
	for them), so the pipeline omits `promo_intensity` for those categories
	rather than zero-filling -- a constant-zero column would assert "no
	promotion ran", which the data does not support.

	Indexing by a fixed list therefore raises KeyError on exactly the categories
	whose capability differs. Selecting by intersection trains each category on
	what it has, and picks up new columns without a code change.

	The order of `wanted` is preserved so feature-importance output stays
	comparable across runs.
	"""
	wanted = FEATURES if wanted is None else wanted
	return [c for c in wanted if c in fm.columns]


# series key per dataset
KEYS = {"bymonth": ["brand"]}


def _load(ds: str, cat: str, slug: str) -> pd.DataFrame | None:
    sub = "CSD" if (cat == "CSD") else cat
    p = DATASETS[ds] / sub / f"{slug}_feature_matrix_h3.parquet"
    if not p.exists():
        return None
    return pd.read_parquet(p)


def _metrics(y, yhat):
    """Return (mean MAPE %, median per-row APE %, WMAPE %)."""
    y = np.asarray(y, float); yhat = np.asarray(yhat, float)
    ae = np.abs(y - yhat)
    ape = ae / np.maximum(y, 1e-9)
    return float(np.mean(ape) * 100), float(np.median(ape) * 100), float(ae.sum() / max(y.sum(), 1e-9) * 100)


# Volume-valued features are in RAW UNITS while the target is LOG. Tree models
# are invariant to monotone transforms of a feature, so they never noticed. A
# LINEAR model cannot bridge the two: fitting log(y) on raw x forces the
# coefficient to approximate a logarithm with a straight line, and it
# extrapolates catastrophically outside the training range.
#
# Measured on the untransformed features (2026-08-19), Ridge produced test
# WMAPE of 446.7% / 7392.6% / 2669.4% / 1121.4% -- on danskvand it predicted
# 1.9e9 units against a 3.85e6 actual. Log-scaling these columns brings it to
# 21.9% / 19.2% / 20.8% / 57.3%.
#
# This matters beyond tidiness: at 19.2% on danskvand, Ridge BEATS tuned
# XGBoost (32.6%). The broken baseline was concealing a linear model that wins
# a category, which changes the SRQ1 model-selection claim.
LOG_SCALE_FEATURES = ("lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
                      "rolling_mean_4", "rolling_std_4", "rolling_mean_13")


def _log_scale(X):
    """log1p the volume-valued columns, leaving calendar/flag columns alone.

    Only linear models need this. Applied inside _fit_predict rather than to the
    matrix so tree models keep training on exactly the features documented
    elsewhere, and the two model families stay comparable on the same inputs."""
    X = X.copy()
    for c in LOG_SCALE_FEATURES:
        if c in X.columns:
            X[c] = np.log1p(X[c].clip(lower=0))
    return X


def _fit_predict(model_name, Xtr, ytr_log, Xte):
    """Train in log space, return predictions on the original scale."""
    if model_name == "Ridge":
        from sklearn.linear_model import Ridge
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        # See LOG_SCALE_FEATURES above: without this the baseline is meaningless.
        Xtr, Xte = _log_scale(Xtr), _log_scale(Xte)
        m = make_pipeline(StandardScaler(), Ridge(alpha=1.0, random_state=SEED))
        m.fit(Xtr, ytr_log)
        return np.expm1(m.predict(Xte))
    if model_name == "LightGBM":
        from lightgbm import LGBMRegressor
        m = LGBMRegressor(n_estimators=400, learning_rate=0.05, num_leaves=31,
                          subsample=0.8, colsample_bytree=0.8, random_state=SEED, verbose=-1)
        m.fit(Xtr, ytr_log)
        return np.expm1(m.predict(Xte))
    if model_name == "XGBoost":
        from xgboost import XGBRegressor
        m = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6,
                         subsample=0.8, colsample_bytree=0.8, random_state=SEED,
                         verbosity=0, n_jobs=-1)
        m.fit(Xtr, ytr_log)
        return np.expm1(m.predict(Xte))
    raise ValueError(model_name)


def run_category(ds: str, cat: str, slug: str) -> list[dict]:
    fm = _load(ds, cat, slug)
    if fm is None:
        print(f"  {cat:13s} skipped — no feature matrix at grain='{ds}' yet")
        return []

    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    tr = d[d.split == "train"]
    te = d[d.split == "test"]
    rows = []
    if len(tr) < 30 or len(te) == 0:
        return rows

    Xtr = tr[available_features(fm)].fillna(0.0); ytr_log = tr["log_sales_units"].values
    Xte = te[available_features(fm)].fillna(0.0); ytrue = np.expm1(te["log_sales_units"].values)

    # Baseline: seasonal naive (same month last year), fallback last month
    sn = te["lag_13"].fillna(te["lag_1"]).fillna(0.0).values
    for name, pred in [("SeasonalNaive", sn)]:
        mp, md, wm = _metrics(ytrue, pred)
        rows.append(dict(dataset=ds, category=cat, model=name,
                         mape_mean=mp, mape_median=md, wmape=wm,
                         n_train=len(tr), n_test=len(te), n_series=d[KEYS[ds]].drop_duplicates().shape[0]))

    for name in ["Ridge", "LightGBM", "XGBoost"]:
        try:
            pred = _fit_predict(name, Xtr, ytr_log, Xte)
            pred = np.clip(pred, 0, None)
            mp, md, wm = _metrics(ytrue, pred)
            rows.append(dict(dataset=ds, category=cat, model=name,
                             mape_mean=mp, mape_median=md, wmape=wm,
                             n_train=len(tr), n_test=len(te), n_series=d[KEYS[ds]].drop_duplicates().shape[0]))
        except Exception as e:  # noqa
            rows.append(dict(dataset=ds, category=cat, model=name, error=str(e)[:120],
                             mape_mean=np.nan, mape_median=np.nan, wmape=np.nan,
                             n_train=len(tr), n_test=len(te), n_series=np.nan))
    return rows


def main():
    parser = argparse.ArgumentParser(description="SRQ1 forecasting benchmark")
    parser.add_argument("--grain", type=str, default=None, help="Single grain (default: bymonth)")
    parser.add_argument("--grains", type=str, default=None, help="Comma-separated list of grains")
    args = parser.parse_args()

    if args.grains:
        grains = [g.strip() for g in args.grains.split(",") if g.strip()]
    elif args.grain:
        grains = [args.grain]
    else:
        grains = DEFAULT_GRAINS

    unknown = [g for g in grains if g not in DATASETS]
    if unknown:
        raise ValueError(f"Unknown grain(s) {unknown}. Valid grains: {list(DATASETS)}")

    OUT.mkdir(parents=True, exist_ok=True)
    all_rows = []
    for ds in grains:
        print(f"\n########## DATASET = {ds} ##########")
        for cat, slug in CATS.items():
            r = run_category(ds, cat, slug)
            all_rows += r
            best = min([x for x in r if x["model"] != "SeasonalNaive" and not np.isnan(x.get("wmape", np.nan))],
                       key=lambda x: x["wmape"], default=None)
            naive = next((x for x in r if x["model"] == "SeasonalNaive"), None)
            if best and naive:
                print(f"  {cat:13s} best={best['model']:9s} WMAPE={best['wmape']:5.1f}% "
                      f"(naive {naive['wmape']:5.1f}%)  medMAPE={best['mape_median']:5.1f}%")

    if not all_rows:
        print("\nNo rows produced — no feature matrices found for the requested grain(s).")
        return

    df = pd.DataFrame(all_rows)
    df.to_csv(OUT / "metrics.csv", index=False)

    # summary.md
    # `mean MAPE` is deliberately absent from this table (P0038 F75). MAPE
    # divides by the actual, guarded as max(y, 1e-9), and 13.8% of CSD's test
    # rows have exactly zero sales at parent scope -- so a one-unit error there
    # scores 1e11 %. The mean carries that; the median does not. It read 1e12 -
    # 1e15 % for every model INCLUDING SeasonalNaive, which is uninterpretable
    # rather than merely unflattering. Still computed and written to metrics.csv,
    # because the raw numbers are evidence; just not reported as a headline.
    lines = ["# SRQ1 benchmark — corrected DVH EXCL. HD matrices", "",
             "Test-set accuracy. WMAPE = volume-weighted (business metric); "
             "medMAPE = median per-row APE. Models trained in log space, seed=42.", ""]
    for ds in grains:
        sub = df[df.dataset == ds]
        if sub.empty:
            continue
        lines += [f"## Dataset: {ds}", "",
                  "| Category | Model | WMAPE | median MAPE | n_train | n_test | n_series |",
                  "|---|---|---|---|---|---|---|"]
        for cat in CATS:
            for _, x in sub[sub.category == cat].iterrows():
                wm = f"{x['wmape']:.1f}%" if pd.notna(x.get("wmape")) else "ERR"
                mp = f"{x['mape_mean']:.1f}%" if pd.notna(x.get("mape_mean")) else "-"
                md = f"{x['mape_median']:.1f}%" if pd.notna(x.get("mape_median")) else "-"
                lines.append(f"| {cat} | {x['model']} | {wm} | {md} | "
                             f"{int(x['n_train'])} | {int(x['n_test'])} | "
                             f"{int(x['n_series']) if pd.notna(x.get('n_series')) else '-'} |")
        lines.append("")
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"\nSaved metrics.csv + summary.md in {OUT}")


if __name__ == "__main__":
    main()
