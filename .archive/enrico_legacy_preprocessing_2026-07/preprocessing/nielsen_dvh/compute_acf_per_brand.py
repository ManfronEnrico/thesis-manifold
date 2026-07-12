#!/usr/bin/env python3
"""
Per-Brand ACF Computation — replaces the pooled brand-demeaned ACF method

WHY THIS EXISTS
===============
eda_findings_dvhexclhd.md previously reported ACF (lag1/lag3/lag13) computed
by concatenating all brands' demeaned log-sales series into one pooled series
and running a single ACF across it. This has two concrete statistical flaws:

  1. Boundary contamination: concatenating brand A's series directly before
     brand B's series makes a standard ACF correlate brand A's last observation
     against brand B's first, as if they were consecutive real observations of
     the same entity. With dozens of brands per category, every lag is
     contaminated by these spurious cross-brand pairs.
  2. Heteroscedasticity: demeaning removes each brand's level but not its
     variance. High-volume/high-variance brands dominate the pooled ACF
     (a variance-weighted statistic), so the result is not a genuine
     "average brand" autocorrelation.

It was also not reproducible from any committed script — the numbers were a
one-off manual calculation.

FIX
===
Compute ACF within each brand's own time-ordered series only (no cross-brand
concatenation), then aggregate across brands via mean, median, and IQR. This
treats every brand equally regardless of size/variance and cannot mix brand
boundaries by construction.

USAGE
=====
  python thesis/data/preprocessing/nielsen_dvh/compute_acf_per_brand.py

Reads the same market-scoped brand x (year, month) aggregation logic as
build_feature_matrix.py (DVH EXCL. HD, positive sales only), from whichever
raw/converted data tier is available locally.

KNOWN LIMITATION (documented, not silently omitted)
====================================================
As of 2026-07-10, this repo checkout has:
  - CSD: `_01_converted` parquet views present locally, 44 raw periods on file
    (matches the canonical script's reported period count) -> HIGH confidence.
  - energidrikke: `_01_converted` parquet views present locally, but only 29
    raw periods on file, vs. 39 periods claimed by build_feature_matrix.py's
    regeneration_report.md -> this is a STALE/PARTIAL local snapshot, not the
    same data build_feature_matrix.py ran against. Results here are run with
    a relaxed MIN_PERIODS threshold for a directional comparison only, and are
    explicitly LOWER CONFIDENCE than CSD's.
  - danskvand, RTD: no `_01_converted` parquet views present in this checkout
    at all -> CANNOT be computed here. Do not fabricate values for these
    categories; re-run this script in an environment with their raw/converted
    data present, or once `data/raw/` (build_feature_matrix.py's expected
    input) is available.
"""

import numpy as np
import pandas as pd
from pathlib import Path

_cur = Path(__file__).resolve()
for _p in [_cur, *_cur.parents]:
    if (_p / "CLAUDE.md").exists():
        ROOT = _p
        break
else:
    ROOT = Path.cwd()

PARQ = ROOT / "thesis" / "data" / "_01_converted" / "nielsen" / "parquet_nielsen"

MARKET_SCOPE = "DVH EXCL. HD"
LAGS = (1, 3, 13)
MIN_LEN_FOR_LAG = {1: 5, 3: 8, 13: 20}  # per-lag minimum series length to compute meaningfully

# category_key -> (parquet dir name, MIN_PERIODS to use, confidence note)
# MIN_PERIODS=30 is the canonical production threshold (build_feature_matrix.py).
# Categories whose local data tier doesn't reach that scale are run at a relaxed
# threshold for a directional check only, and flagged accordingly.
CAT_CONFIG = {
    "CSD": {"dir": "CSD", "min_periods": 30, "confidence": "high (local snapshot period count matches canonical script)"},
    "energidrikke": {"dir": "Energidrikke", "min_periods": 20, "confidence": "LOW (local snapshot has 29 periods vs 39 claimed by build_feature_matrix.py - stale/partial data)"},
    # "danskvand" and "RTD" intentionally omitted: no _01_converted parquet views
    # present in this checkout as of 2026-07-10. Add once data becomes available.
}


def acf_single(x: np.ndarray, lag: int) -> float | None:
    """Sample ACF for a single brand's own series only (no cross-brand concatenation)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n <= lag:
        return None
    xm = x - x.mean()
    den = np.sum(xm ** 2)
    if den == 0:
        return None
    num = np.sum(xm[: n - lag] * xm[lag:])
    return float(num / den)


def compute_category(cat_key: str, cfg: dict) -> dict:
    cat_dir = cfg["dir"]
    min_periods = cfg["min_periods"]
    base = PARQ / cat_dir / "views"
    slug = cat_dir.lower()

    facts = pd.read_parquet(base / f"{slug}_clean_facts_v.parquet")
    dim_market = pd.read_parquet(base / f"{slug}_clean_dim_market_v.parquet")
    dim_period = pd.read_parquet(base / f"{slug}_clean_dim_period_v.parquet")
    dim_product = pd.read_parquet(base / f"{slug}_clean_dim_product_v.parquet")

    market_ids = dim_market.loc[dim_market["market_description"] == MARKET_SCOPE, "market_id"].unique()
    if len(market_ids) == 0:
        raise RuntimeError(f"[{cat_key}] no market_id found for '{MARKET_SCOPE}'")

    f = facts[facts["market_id"].isin(market_ids)].copy()
    f = f[f["sales_units"] > 0]
    f = f.merge(dim_period[["period_id", "period_year", "period_month"]], on="period_id", how="left")
    f = f.merge(dim_product[["product_id", "brand"]], on="product_id", how="left")
    f = f.dropna(subset=["brand"])

    g = f.groupby(["brand", "period_year", "period_month"], as_index=False)["sales_units"].sum()
    g["period_key"] = g["period_year"] * 100 + g["period_month"]
    g = g.sort_values(["brand", "period_key"])

    counts = g.groupby("brand")["period_key"].nunique()
    keep_brands = counts[counts >= min_periods].index
    g = g[g["brand"].isin(keep_brands)]

    per_brand_acf = {lag: [] for lag in LAGS}
    excluded_counts = {lag: 0 for lag in LAGS}

    for _, sub in g.groupby("brand"):
        sub = sub.sort_values("period_key")
        log_sales = np.log(sub["sales_units"].to_numpy())
        n = len(log_sales)
        for lag in LAGS:
            if n < MIN_LEN_FOR_LAG[lag]:
                excluded_counts[lag] += 1
                continue
            val = acf_single(log_sales, lag)
            if val is not None:
                per_brand_acf[lag].append(val)
            else:
                excluded_counts[lag] += 1

    row = {"category": cat_key, "n_brands": len(keep_brands), "confidence": cfg["confidence"]}
    for lag in LAGS:
        vals = np.array(per_brand_acf[lag])
        if len(vals) == 0:
            row[f"lag{lag}_mean"] = None
            row[f"lag{lag}_median"] = None
            row[f"lag{lag}_iqr"] = None
        else:
            q75, q25 = np.percentile(vals, [75, 25])
            row[f"lag{lag}_mean"] = round(float(vals.mean()), 4)
            row[f"lag{lag}_median"] = round(float(np.median(vals)), 4)
            row[f"lag{lag}_iqr"] = round(float(q75 - q25), 4)
        row[f"lag{lag}_n_brands_used"] = len(vals)
        row[f"lag{lag}_excluded"] = excluded_counts[lag]

    return row


def main():
    results = []
    for cat_key, cfg in CAT_CONFIG.items():
        results.append(compute_category(cat_key, cfg))

    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    return df


if __name__ == "__main__":
    main()
