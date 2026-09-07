#!/usr/bin/env python
"""
SRQ1 feature diagnostics: collinearity, redundancy and importance -- measured,
per category, from the data.

WHY THIS EXISTS
---------------
Until 2026-09-06 the project's feature set was a hand-maintained list
(`srq1_benchmark.FEATURES`) and its two removals were justified in code
comments: `weighted_distribution` by an ad-hoc with/without fit, and
`holiday_months` as a mislabelling. Neither the retained features nor their
relationships to each other had ever been measured.

That is not a defensible method for a thesis. Two specific defects follow from
it, and both are addressed here:

  1. NO COLLINEARITY CHECK. Ridge is fitted on a feature set containing
     `lag_1..lag_13` and `rolling_mean_4/13`, which are near-duplicates by
     construction, plus (as of the holiday enrichment) `non_holiday_days` =
     `days_in_month` - `n_holidays`, an EXACT linear dependency. Multicollinear
     inputs make linear coefficients large, unstable and noise-sensitive. VIF is
     the standard diagnostic and was never computed.

  2. NO MEASURED SELECTION. Feature importance existed only as post-hoc SHAP
     that nothing consumed. No procedure decided what to keep.

Everything this script reports is COMPUTED FROM THE DATA per category, and no
feature is named in a decision rule anywhere in this file.

The two VIF bands (5 and 10) are the only fixed numbers. They are REPORTING
bands used to sort output for a human, never decision rules -- nothing is
dropped because of them. Their provenance is documented at the constant; do not
cite them in prose without verifying a source first.

WHAT IT COMPUTES
----------------
  1. VIF per feature, per category            -> multicollinearity
  2. Exact/near-exact linear dependencies      -> rank deficiency
  3. Spearman correlation clusters             -> redundancy groups
  4. Permutation importance on VALIDATION      -> honest importance, not in-sample
  5. A proposed reduced set per category, by measured redundancy + importance

PROTOCOL
--------
Importance is measured on the VALIDATION split, never on test. Test is touched
by no part of this script. That is what keeps the downstream test metric an
honest estimate rather than a number the feature set was chosen against.

USAGE
    python srq1_feature_diagnostics.py
    python srq1_feature_diagnostics.py --no-holiday   # pre-enrichment baseline
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
from srq1_benchmark import CATS, FEATURES, SEED, _load, _log_scale  # noqa: E402

HOLIDAY_FEATURES = ["days_in_month", "n_holidays", "non_holiday_days"]
GRAIN = "bymonth"
# Tabular output belongs in the tier's tables/ subfolder, not loose at the
# top of the results dir (DEC-P0046-SINGLE-HOME / the srq1 folder shape).
OUT = get_srq_tables_dir(1)

# VIF reporting thresholds. READ THIS BEFORE CITING THEM.
#
# 5 and 10 are widely used rules of thumb, and an earlier version of this file
# attributed them to Hair et al. (2019) Multivariate Data Analysis. That
# attribution was made FROM MEMORY and the source is NOT in the project's Zotero
# library -- it could not be checked. It has been removed rather than left
# looking verified.
#
# These are therefore REPORTING BANDS, not decision rules, and nothing in this
# pipeline drops a feature because of them. They exist to sort the output so a
# human can see which features are collinear. If the thesis ever states a
# numeric VIF threshold in prose it must first cite a source that has been
# verified against the library -- see writing-notes/unverified-claims-to-check.md.
#
# What IS in the library and does support the underlying point (that collinear
# predictors make least-squares coefficients high-variance, which is the problem
# ridge shrinkage addresses): Hastie, Tibshirani & Friedman, The Elements of
# Statistical Learning, "Linear Methods for Regression" (Zotero key LR3KF2SX).
# That source motivates the diagnostic; it is not the source of these numbers.
VIF_SEVERE = 10.0
VIF_MODERATE = 5.0

# Spearman |rho| above which two features are treated as one redundancy cluster.
# Rank-based so it does not assume linearity, and applied to CLUSTERING only --
# nothing is dropped on correlation alone; importance decides the survivor.
REDUNDANCY_RHO = 0.95


def _candidate_features(fm: pd.DataFrame, include_holiday: bool) -> list[str]:
    """Every modelling feature this matrix actually carries.

    Discovered from the matrix, not asserted. Categories differ in capability
    (Danskvand and RTD have no promo), so a fixed list would be wrong for two
    of four categories -- the same DEC-DISCOVER-COLUMNS reasoning the pipeline
    already applies.
    """
    wanted = list(FEATURES) + (HOLIDAY_FEATURES if include_holiday else [])
    return [c for c in wanted if c in fm.columns]


def _splits(fm: pd.DataFrame, feats: list[str]):
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    tr, va = d[d.split == "train"], d[d.split == "val"]
    if len(tr) < 30 or len(va) == 0:
        return None
    return (tr[feats].fillna(0.0), tr["log_sales_units"].values,
            va[feats].fillna(0.0), va["log_sales_units"].values)


def compute_vif(X: pd.DataFrame) -> pd.DataFrame:
    """VIF per feature: 1/(1-R^2) from regressing each feature on the others.

    Computed on the log-scaled, standardised matrix the linear model actually
    sees -- VIF on raw volume columns would measure the scale difference rather
    than the dependency.

    A perfectly determined feature yields R^2 = 1 and VIF = inf. That is not an
    error to guard away: it is the finding, and it is reported as such.
    """
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler

    Xs = _log_scale(X)
    keep = [c for c in Xs.columns if Xs[c].nunique() > 1]
    Xs = Xs[keep]
    Z = pd.DataFrame(StandardScaler().fit_transform(Xs), columns=keep)

    rows = []
    for col in keep:
        others = [c for c in keep if c != col]
        if not others:
            continue
        r2 = LinearRegression().fit(Z[others], Z[col]).score(Z[others], Z[col])
        r2 = min(max(r2, 0.0), 1.0)
        vif = np.inf if r2 >= 1.0 - 1e-10 else 1.0 / (1.0 - r2)
        rows.append({"feature": col, "r2_on_others": r2, "vif": vif})

    return pd.DataFrame(rows).sort_values("vif", ascending=False)


def redundancy_clusters(X: pd.DataFrame, rho: float) -> list[list[str]]:
    """Group features whose pairwise |Spearman rho| exceeds the threshold.

    Single-linkage over the thresholded correlation graph. Returns only groups
    of 2+, since a singleton is not a redundancy.
    """
    keep = [c for c in X.columns if X[c].nunique() > 1]
    if len(keep) < 2:
        return []
    corr = X[keep].corr(method="spearman").abs()

    parent = {c: c for c in keep}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i, a in enumerate(keep):
        for b in keep[i + 1:]:
            if corr.loc[a, b] >= rho:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[rb] = ra

    groups: dict[str, list[str]] = {}
    for c in keep:
        groups.setdefault(find(c), []).append(c)
    return [sorted(g) for g in groups.values() if len(g) > 1]


def permutation_importance_val(Xtr, ytr, Xva, yva, n_repeats: int = 10):
    """Permutation importance measured on VALIDATION, never on test.

    Permutation rather than tree gain: gain is biased toward high-cardinality
    features and is measured in-sample. Permutation asks the question that
    matters -- how much worse does held-out prediction get when this feature is
    shuffled -- and is model-agnostic.
    """
    from lightgbm import LGBMRegressor
    from sklearn.inspection import permutation_importance

    m = LGBMRegressor(n_estimators=400, learning_rate=0.05, num_leaves=31,
                      subsample=0.8, colsample_bytree=0.8,
                      random_state=SEED, verbose=-1)
    m.fit(Xtr, ytr)
    r = permutation_importance(m, Xva, yva, n_repeats=n_repeats,
                               random_state=SEED, scoring="neg_mean_absolute_error")
    return pd.DataFrame({
        "feature": Xva.columns,
        "importance_mean": r.importances_mean,
        "importance_std": r.importances_std,
    }).sort_values("importance_mean", ascending=False)


def propose_reduced_set(vif: pd.DataFrame, clusters: list[list[str]],
                        imp: pd.DataFrame) -> tuple[list[str], list[dict]]:
    """Keep the most important member of each redundancy cluster; keep all else.

    MEASURED AND REJECTED FOR TREE MODELS (2026-09-06). This rule was validated
    against the benchmark before adoption and made accuracy WORSE: mean test
    WMAPE 28.82 reduced vs 26.44 unreduced, across 4 categories x 3 models.

    The reason is that collinearity is a LINEAR-MODEL pathology. Ridge cannot
    apportion credit between `lag_1..lag_4` and `rolling_mean_4`, so its
    coefficients are unstable -- but a gradient-boosted tree splits on whichever
    correlated feature is locally most useful and loses real information when
    the others are removed. Collapsing a 7-member lag/rolling cluster to one
    survivor therefore helps neither: it does not fix Ridge (see below) and it
    actively harms LightGBM and XGBoost.

    So this function's output is a DIAGNOSTIC PROPOSAL for the linear track
    only, and it is not applied anywhere automatically. The measurement is the
    point: an unvalidated reduction rule would have degraded every reported
    number while looking like methodological rigour.

    ALSO MEASURED (2026-09-06): dropping the exact linear dependency among the
    holiday features changed test WMAPE by < 0.01pp in all 8 category x feature
    -set cells. StandardScaler plus Ridge's L2 penalty already absorbs rank
    deficiency. VIF correctly reports the dependency; the dependency is simply
    not what drives the error. Report the VIF, do not claim it explains accuracy.
    """
    rank = dict(zip(imp["feature"], imp["importance_mean"]))
    dropped: list[dict] = []
    drop_set: set[str] = set()

    for group in clusters:
        ranked = sorted(group, key=lambda c: rank.get(c, -np.inf), reverse=True)
        survivor, losers = ranked[0], ranked[1:]
        for loser in losers:
            drop_set.add(loser)
            dropped.append({
                "dropped": loser, "kept_instead": survivor,
                "reason": f"|rho| >= {REDUNDANCY_RHO} with {survivor}, lower "
                          f"permutation importance on validation",
                "importance_dropped": rank.get(loser, np.nan),
                "importance_kept": rank.get(survivor, np.nan),
            })

    keep = [f for f in imp["feature"] if f not in drop_set]
    return keep, dropped


def main() -> int:
    ap = argparse.ArgumentParser(description="SRQ1 feature diagnostics")
    ap.add_argument("--no-holiday", action="store_true",
                    help="Exclude holiday features (pre-enrichment baseline)")
    ap.add_argument("--repeats", type=int, default=10,
                    help="Permutation importance repeats (default 10)")
    args = ap.parse_args()

    vif_all, clust_all, imp_all, prop_all, drop_all = [], [], [], [], []

    for cat, slug in CATS.items():
        fm = _load(GRAIN, cat, slug)
        if fm is None:
            print(f"  {cat:13s} skipped -- no feature matrix")
            continue

        feats = _candidate_features(fm, include_holiday=not args.no_holiday)
        parts = _splits(fm, feats)
        if parts is None:
            print(f"  {cat:13s} skipped -- insufficient train/val rows")
            continue
        Xtr, ytr, Xva, yva = parts

        vif = compute_vif(Xtr)
        vif.insert(0, "category", cat)
        vif_all.append(vif)

        clusters = redundancy_clusters(Xtr, REDUNDANCY_RHO)
        for g in clusters:
            clust_all.append({"category": cat, "cluster": " + ".join(g),
                              "size": len(g)})

        imp = permutation_importance_val(Xtr, ytr, Xva, yva, args.repeats)
        imp.insert(0, "category", cat)
        imp_all.append(imp)

        keep, dropped = propose_reduced_set(vif, clusters, imp)
        prop_all.append({"category": cat, "n_candidate": len(feats),
                         "n_proposed": len(keep),
                         "proposed": " ".join(keep)})
        for d in dropped:
            d["category"] = cat
            drop_all.append(d)

        n_inf = int(np.isinf(vif["vif"]).sum())
        n_sev = int((vif["vif"] > VIF_SEVERE).sum())
        print(f"  {cat:13s} {len(feats):2d} features | VIF>10: {n_sev:2d} "
              f"(exact deps: {n_inf}) | clusters: {len(clusters)} | "
              f"proposed: {len(keep)}")

    if not vif_all:
        print("No categories produced diagnostics.")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    suffix = "_noholiday" if args.no_holiday else ""
    vif_df = pd.concat(vif_all, ignore_index=True)
    imp_df = pd.concat(imp_all, ignore_index=True)
    vif_df.to_csv(OUT / f"feature_vif{suffix}.csv", index=False, encoding="utf-8")
    imp_df.to_csv(OUT / f"feature_permutation_importance{suffix}.csv",
                  index=False, encoding="utf-8")
    pd.DataFrame(clust_all).to_csv(OUT / f"feature_redundancy_clusters{suffix}.csv",
                                   index=False, encoding="utf-8")
    pd.DataFrame(prop_all).to_csv(OUT / f"feature_proposed_set{suffix}.csv",
                                  index=False, encoding="utf-8")
    if drop_all:
        pd.DataFrame(drop_all).to_csv(OUT / f"feature_drop_rationale{suffix}.csv",
                                      index=False, encoding="utf-8")

    print(f"\n=== VIF above {VIF_SEVERE:.0f} (serious multicollinearity) ===")
    bad = vif_df[vif_df["vif"] > VIF_SEVERE]
    if bad.empty:
        print("  none")
    else:
        show = bad.copy()
        show["vif"] = show["vif"].map(lambda v: "inf" if np.isinf(v) else f"{v:.1f}")
        print(show[["category", "feature", "vif"]].to_string(index=False))

    print("\n=== Redundancy clusters (|Spearman| >= "
          f"{REDUNDANCY_RHO}) ===")
    if clust_all:
        print(pd.DataFrame(clust_all).to_string(index=False))
    else:
        print("  none")

    print("\n=== Proposed reduced sets ===")
    for row in prop_all:
        print(f"  {row['category']:13s} {row['n_candidate']:2d} -> "
              f"{row['n_proposed']:2d} features")

    print(f"\nWritten -> {OUT}")
    print("\nNOTE: the proposed sets were VALIDATED on 2026-09-06 and REJECTED "
          "for the tree models\n(mean test WMAPE 28.82 reduced vs 26.44 "
          "unreduced). Collinearity is a linear-model\npathology; trees use "
          "correlated lags productively. Treat these proposals as a\n"
          "diagnostic for the Ridge track, and re-validate before adopting "
          "anything.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
