#!/usr/bin/env python3
"""
Nielsen Feature-Matrix Builder — brand × RETAIL CHAIN × month (DVH EXCL. HD)

PURPOSE
=======
Sibling of `build_feature_matrix.py`. That builder collapses DVH EXCL. HD to a
single national series per brand (brand × month). This builder instead keeps a
retail-chain dimension, producing brand × chain × month series — ~6x more rows
per category — while staying inside the DVH EXCL. HD universe (no double-count).

WHY THIS EXISTS
===============
The brand × month matrices are small (CSD 3,077 rows; RTD 1,543). Disaggregating
to the individual store chains that sit INSIDE DVH EXCL. HD multiplies the row
count without re-introducing the hierarchical double-count: the chains are
mutually-exclusive leaf outlets, not nested roll-ups. To keep all four categories
trainable by identical code, we use only the chains PRESENT IN ALL FOUR.

CHAIN SET (11 leaf chains common to CSD, danskvand, energidrikke, RTD)
=====================================================================
BILKA, FØTEX, NETTO, KVICKLY, SUPERBRUGSEN, BRUGSEN, MENY, SPAR, MIN KØBMAND,
REMA 1000, NEMLIG.COM. These are individual store chains (no group aggregates
such as COOP/SALLING GROUP/DAGROFA, no grand-total roll-ups, no hard discount,
no petrol/convenience). They cover ~87-91% of each category's DVH EXCL. HD volume;
the residual ~10% is small independents not common to all four and is excluded so
the four datasets stay homogeneous.

SCOPE / DEDUP CORRECTNESS
=========================
The market/product/period dimensions are slowly-changing (valid_from/valid_to)
and carry duplicate ids; every dimension is de-duplicated on its id BEFORE the
merge, otherwise the join fans out and inflates volumes (~7x for CSD). This
mirrors the dedup in build_feature_matrix.py.

OUTPUT
======
thesis/data/_04_engineered_bychain/<Category>/<slug>_feature_matrix.parquet
  one row per (brand, chain, period) on the full monthly grid; same 22 feature
  columns as the brand-level matrices PLUS a `chain` column. NaN in lag/rolling/
  target columns is by design (grid gaps exposed for correct lags).

USAGE
=====
  .venv/bin/python thesis/data/preprocessing/nielsen_dvh/build_feature_matrix_bychain.py
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[4]
DATA_RAW = ROOT / "data" / "raw"
OUT_DIR = ROOT / "thesis" / "data" / "_04_engineered_bychain"

CATEGORIES = {"CSD": "csd", "danskvand": "danskvand",
              "energidrikke": "energidrikke", "RTD": "rtd"}

# 11 leaf chains common to all four categories (verified on data/raw)
LEAF_CHAINS = ["BILKA", "FØTEX", "NETTO", "KVICKLY", "SUPERBRUGSEN", "BRUGSEN",
               "MENY", "SPAR", "MIN KØBMAND", "REMA 1000", "NEMLIG.COM"]

KEYS = ["brand", "chain"]            # series key (one time series per brand×chain)
MIN_PERIODS = 30                     # min observed months per series
LAGS = (1, 2, 3, 4, 8, 13)
HOLIDAY_MONTHS = {3, 6, 12}
VAL_SIZE = 6


def _test_size(n_periods: int) -> int:
    return 12 if n_periods >= 42 else 8


# ----------------------------------------------------------------------------
# STEP 1-2 — LOAD AND SCOPE TO THE COMMON LEAF CHAINS
# ----------------------------------------------------------------------------
def load_scoped_facts(slug: str) -> pd.DataFrame:
    base = DATA_RAW / f"nielsen_{slug}_clean"
    facts = pd.read_parquet(f"{base}_facts_v.parquet")
    market = pd.read_parquet(f"{base}_dim_market.parquet")
    product = pd.read_parquet(f"{base}_dim_product.parquet")
    period = pd.read_parquet(f"{base}_dim_period.parquet")

    # De-dup slowly-changing dimensions on their id (prevents merge fan-out).
    market = market.drop_duplicates("market_id")[["market_id", "market_description"]]
    product = product.drop_duplicates("product_id")[["product_id", "brand"]]
    period = period.drop_duplicates("period_id")[["period_id", "period_year", "period_month"]]

    chain_ids = market[market.market_description.isin(LEAF_CHAINS)]
    present = sorted(chain_ids.market_description.unique())
    missing = sorted(set(LEAF_CHAINS) - set(present))
    if missing:
        raise ValueError(f"slug '{slug}' missing common chains: {missing}")

    f = facts[facts.market_id.isin(chain_ids.market_id)].copy()

    if "sales_units_any_promo" in f.columns:
        f["promo_units"] = f["sales_units_any_promo"].fillna(0)
    else:
        f["promo_units"] = 0.0

    f = (f.merge(chain_ids.rename(columns={"market_description": "chain"}), on="market_id", how="left")
           .merge(product, on="product_id", how="left")
           .merge(period, on="period_id", how="left"))
    keep = ["brand", "chain", "period_year", "period_month",
            "sales_units", "promo_units", "weighted_distribution"]
    return f[keep]


# ----------------------------------------------------------------------------
# STEP 3 — AGGREGATE TO brand × chain × month (positive sales only)
# ----------------------------------------------------------------------------
def aggregate_series_month(f: pd.DataFrame) -> pd.DataFrame:
    f = f[f.sales_units > 0]
    agg = f.groupby(KEYS + ["period_year", "period_month"], as_index=False).agg(
        sales_units=("sales_units", "sum"),
        promo_units=("promo_units", "sum"),
        weighted_distribution=("weighted_distribution", "mean"),
    )
    return agg


# ----------------------------------------------------------------------------
# STEP 4 — FILTER SERIES BY MIN_PERIODS
# ----------------------------------------------------------------------------
def filter_min_periods(agg: pd.DataFrame, min_periods: int) -> pd.DataFrame:
    counts = agg.groupby(KEYS).size()
    keep = counts[counts >= min_periods].index
    return agg.set_index(KEYS).loc[keep].reset_index()


# ----------------------------------------------------------------------------
# STEP 5 — REINDEX EACH SERIES TO THE FULL MONTHLY GRID
# ----------------------------------------------------------------------------
def build_calendar(agg: pd.DataFrame) -> pd.DataFrame:
    periods = (agg[["period_year", "period_month"]]
               .drop_duplicates()
               .sort_values(["period_year", "period_month"])
               .reset_index(drop=True))
    periods["period_index"] = range(len(periods))
    return periods


def reindex_to_grid(agg: pd.DataFrame, periods: pd.DataFrame) -> pd.DataFrame:
    series = agg[KEYS].drop_duplicates()
    grid = (series.assign(_k=1)
                  .merge(periods.assign(_k=1), on="_k")
                  .drop(columns="_k"))
    out = grid.merge(agg, on=KEYS + ["period_year", "period_month", "period_index"]
                     if "period_index" in agg.columns else KEYS + ["period_year", "period_month"],
                     how="left")
    return out.sort_values(KEYS + ["period_index"]).reset_index(drop=True)


# ----------------------------------------------------------------------------
# STEP 6 — FEATURE ENGINEERING (per brand×chain series; leakage-safe)
# ----------------------------------------------------------------------------
def engineer_features(grid: pd.DataFrame) -> pd.DataFrame:
    g = grid.copy()
    gb = g.groupby(KEYS, sort=False)["sales_units"]

    for k in LAGS:
        g[f"lag_{k}"] = gb.shift(k)

    past = gb.shift(1)
    roll_keys = [g[c] for c in KEYS]
    g["rolling_mean_4"] = past.groupby(roll_keys, sort=False).rolling(4, min_periods=1).mean().reset_index(level=list(range(len(KEYS))), drop=True)
    g["rolling_std_4"] = past.groupby(roll_keys, sort=False).rolling(4, min_periods=2).std().reset_index(level=list(range(len(KEYS))), drop=True)
    g["rolling_mean_13"] = past.groupby(roll_keys, sort=False).rolling(13, min_periods=1).mean().reset_index(level=list(range(len(KEYS))), drop=True)

    g["month"] = g["period_month"]
    g["quarter"] = ((g["period_month"] - 1) // 3 + 1)
    g["holiday_month"] = g["period_month"].isin(HOLIDAY_MONTHS).astype(int)
    g["log_sales_units"] = np.log(g["sales_units"].where(g["sales_units"] > 0))
    g["promo_intensity"] = (g["promo_units"] / g["sales_units"]).clip(0, 1)
    return g


# ----------------------------------------------------------------------------
# STEP 7 — FORWARD-CHAINING SPLIT (by date)
# ----------------------------------------------------------------------------
def assign_split(g: pd.DataFrame, periods: pd.DataFrame):
    n = len(periods)
    test = _test_size(n)
    train = n - VAL_SIZE - test
    if train < 24:
        print(f"    WARNING: train window = {train} months (<24; short series)")
    idx_train_end = train - 1
    idx_val_end = train + VAL_SIZE - 1

    def _label(pi):
        if pi <= idx_train_end:
            return "train"
        if pi <= idx_val_end:
            return "val"
        return "test"

    g["split"] = g["period_index"].map(_label)

    def _ym(i):
        row = periods.loc[periods.period_index == i].iloc[0]
        return f"{int(row.period_year)}-{int(row.period_month):02d}"

    split_dates = {
        "n_periods": int(n), "train": int(train), "val": int(VAL_SIZE), "test": int(test),
        "train_start": _ym(0), "train_end": _ym(idx_train_end),
        "val_start": _ym(idx_train_end + 1), "val_end": _ym(idx_val_end),
        "test_start": _ym(idx_val_end + 1), "test_end": _ym(n - 1),
    }
    return g, split_dates


# ----------------------------------------------------------------------------
# ORCHESTRATION
# ----------------------------------------------------------------------------
def build_category(category: str, slug: str) -> dict:
    print(f"\n=== {category} ===")
    facts = load_scoped_facts(slug)
    agg = aggregate_series_month(facts)
    agg = filter_min_periods(agg, MIN_PERIODS)
    periods = build_calendar(agg)
    agg = agg.merge(periods, on=["period_year", "period_month"], how="left")
    grid = reindex_to_grid(agg, periods)
    feats = engineer_features(grid)
    feats, split_dates = assign_split(feats, periods)

    out = OUT_DIR / category
    out.mkdir(parents=True, exist_ok=True)
    feats.to_parquet(out / f"{slug}_feature_matrix.parquet", index=False)
    with open(out / f"{slug}_split_dates.json", "w") as fh:
        json.dump(split_dates, fh, indent=2)

    n_series = feats[KEYS].drop_duplicates().shape[0]
    observed = int(feats["sales_units"].notna().sum())
    print(f"    series(brand×chain)={n_series} brands={feats.brand.nunique()} "
          f"periods={split_dates['n_periods']} grid_rows={len(feats)} observed={observed} "
          f"split={split_dates['train']}/{split_dates['val']}/{split_dates['test']}")
    return {"category": category, "series": n_series, "brands": int(feats.brand.nunique()),
            "periods": split_dates["n_periods"], "grid_rows": len(feats),
            "observed": observed, "split": f"{split_dates['train']}/{split_dates['val']}/{split_dates['test']}"}


def main():
    print("Nielsen feature-matrix regeneration — brand × chain × month, scope = DVH EXCL. HD")
    summaries = [build_category(cat, slug) for cat, slug in CATEGORIES.items()]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# Feature-matrix regeneration report (brand × chain × month, DVH EXCL. HD, MIN_PERIODS=30)",
             "",
             "| Category | Series (brand×chain) | Brands | Periods | Grid rows | Observed | Split (tr/val/te) |",
             "|---|---|---|---|---|---|---|"]
    for s in summaries:
        lines.append(f"| {s['category']} | {s['series']} | {s['brands']} | {s['periods']} "
                     f"| {s['grid_rows']} | {s['observed']} | {s['split']} |")
    lines += ["", f"Chains (common to all four): {', '.join(LEAF_CHAINS)}"]
    (OUT_DIR / "regeneration_report.md").write_text("\n".join(lines) + "\n")
    print(f"\nDone. Outputs in {OUT_DIR}")


if __name__ == "__main__":
    main()
