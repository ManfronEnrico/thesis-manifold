#!/usr/bin/env python3
"""
Nielsen Feature-Matrix Builder — DVH EXCL. HD scope (scope-corrected regeneration)

PURPOSE
=======
Regenerate the per-category forecasting feature matrices for the four Nielsen
beverage categories (CSD, danskvand, energidrikke, RTD) under the CORRECT market
scope, replacing the inherited pipeline output that summed across all 28 market
types and therefore double-counted sales.

WHY THIS EXISTS (DESIGN RATIONALE)
==================================
The inherited Step 1 (`pre_<cat>_1_load_and_aggregate.py`) aggregated sales across
ALL market_description values ("All Markets"). Those values are HIERARCHICAL, not
mutually exclusive: individual chains (REMA 1000, NETTO, ...) are nested inside
group aggregates (COOP, SALLING GROUP, DAGROFA) which are nested inside grand-total
roll-ups (DVH EXCL. HD, DVH/CONVENIENCE INCL. HD, ...). Summing all of them counts
the same sale at every level. Verified on the CSD facts table: the all-markets sum
(168.6B units) is 5.24x the true total (32.2B units).

FIX: scope to the single Nielsen-recommended market level `DVH EXCL. HD`
(one market_id, no cross-market summation -> double-counting impossible by
construction, and a clean branded-demand signal excluding hard discount).

A second correction: a global MIN_PERIODS of 40 is INFEASIBLE for danskvand,
energidrikke and RTD (they only have 37-39 monthly periods, so a >=40 filter
retains zero brands). A single global threshold of 30 is therefore used for all
categories — feasible everywhere and more defensible than a mixed 40/30 rule.

ARCHITECTURE (per category)
===========================
  Step 1  load clean star schema (facts + market/product/period dims) from data/raw/
  Step 2  scope facts to market_description == "DVH EXCL. HD"
  Step 3  aggregate to brand x (period_year, period_month), positive sales only
  Step 4  filter brands with >= MIN_PERIODS observed months
  Step 5  reindex each brand to the full monthly grid (expose gaps for correct lags)
  Step 6  engineer features (lags, rolling, calendar, log target, promo intensity)
  Step 7  assign a forward-chaining train/val/test split by date
  Step 8  save {cat}_feature_matrix.parquet + {cat}_split_dates.json + a report

DOCUMENTED CHOICES (where the inherited implementation detail was unconfirmed)
=============================================================================
  - No leakage: lag_k = sales_units.shift(k); rolling features are computed on
    sales_units.shift(1) (past only), so the current month never leaks into its
    own predictors. (Matches the audit note "shift(1) used correctly".)
  - log_sales_units is the LOG TARGET (models predict in log space, then exp);
    it is NOT used as an input feature (that would be trivial leakage).
  - promo_intensity is treated as a KNOWN/planned exogenous for the month
    (promotional calendars are planned in advance) — consistent with the
    inherited feature set. Promo is structurally zero for danskvand and RTD.
  - These choices are leakage-safe; final alignment against Brian's exact code is
    pending, but the market scope and MIN_PERIODS corrections above are definitive.

USAGE
=====
  python thesis/data/preprocessing/nielsen_dvh/build_feature_matrix.py
  # writes to thesis/data/_03_engineered_dvhexclhd/<category>/
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

# ============================================================================
# PROJECT ROOT (find by walking up to CLAUDE.md — mirrors the inherited pipeline)
# ============================================================================
_cur = Path(__file__).resolve()
for _p in [_cur, *_cur.parents]:
    if (_p / "CLAUDE.md").exists():
        ROOT = _p
        break
else:
    ROOT = Path.cwd()

# ============================================================================
# CONFIGURATION
# ============================================================================
DATA_RAW = ROOT / "data" / "raw"
OUT_DIR = ROOT / "thesis" / "data" / "_03_engineered_dvhexclhd"

# Category -> filename slug used in data/raw/nielsen_<slug>_clean_*.parquet
CATEGORIES = {
    "CSD": "csd",
    "danskvand": "danskvand",
    "energidrikke": "energidrikke",
    "RTD": "rtd",
}  # totalbeer excluded: facts table absent at source

MARKET_SCOPE = "DVH EXCL. HD"        # single Nielsen market level (no summation)
MIN_PERIODS = 30                     # global, feasible for all categories (37-42 periods)
LAGS = (1, 2, 3, 4, 8, 13)           # months
ROLLING_WINDOWS = (4, 13)            # 4-month + ~annual
HOLIDAY_MONTHS = {3, 6, 12}          # CSD-derived peak months (>75th pct)
VAL_SIZE = 6                         # validation months


def _test_size(n_periods: int) -> int:
    """Test-window length: 12 months if the series is long enough (>=42), else 8."""
    return 12 if n_periods >= 42 else 8


# ============================================================================
# STEP 1-2 — LOAD AND SCOPE TO DVH EXCL. HD
# ============================================================================
def load_scoped_facts(slug: str) -> pd.DataFrame:
    """
    Load the clean star schema for one category and scope it to DVH EXCL. HD.

    PARAMETERS
    ----------
    slug : str
        Filename slug (e.g. "csd") used in data/raw/nielsen_<slug>_clean_*.parquet.

    RETURNS
    -------
    DataFrame with columns [brand, period_year, period_month, sales_units,
    promo_units, weighted_distribution] for the single DVH EXCL. HD market.
    """
    base = DATA_RAW / f"nielsen_{slug}_clean"
    facts = pd.read_parquet(f"{base}_facts_v.parquet")
    market = pd.read_parquet(f"{base}_dim_market.parquet")
    product = pd.read_parquet(f"{base}_dim_product.parquet")
    period = pd.read_parquet(f"{base}_dim_period.parquet")

    # Dimensions are slowly-changing (valid_from/valid_to) -> keep one row per id.
    market = market.drop_duplicates("market_id")[["market_id", "market_description"]]
    product = product.drop_duplicates("product_id")[["product_id", "brand"]]
    period = period.drop_duplicates("period_id")[["period_id", "period_year", "period_month"]]

    scope_ids = market.loc[market.market_description == MARKET_SCOPE, "market_id"].unique()
    if len(scope_ids) == 0:
        raise ValueError(f"'{MARKET_SCOPE}' not found in market dimension for slug '{slug}'")

    f = facts[facts.market_id.isin(scope_ids)].copy()

    # Promo coverage varies by category: CSD and energidrikke expose
    # `sales_units_any_promo`; danskvand and RTD do not (promo-zero in our framing),
    # so promotional units are set to 0 and promo_intensity collapses to 0 there.
    if "sales_units_any_promo" in f.columns:
        f["promo_units"] = f["sales_units_any_promo"].fillna(0)
    else:
        f["promo_units"] = 0.0

    f = f.merge(product, on="product_id", how="left").merge(period, on="period_id", how="left")
    keep = ["brand", "period_year", "period_month", "sales_units",
            "promo_units", "weighted_distribution"]
    return f[keep]


# ============================================================================
# STEP 3 — AGGREGATE TO BRAND x MONTH (positive sales only)
# ============================================================================
def aggregate_brand_month(f: pd.DataFrame) -> pd.DataFrame:
    """Aggregate products up to brand x (year, month); keep positive-sales rows only."""
    f = f[f.sales_units > 0]
    agg = f.groupby(["brand", "period_year", "period_month"], as_index=False).agg(
        sales_units=("sales_units", "sum"),
        promo_units=("promo_units", "sum"),
        weighted_distribution=("weighted_distribution", "mean"),  # ACV metric: mean, not sum
    )
    return agg


# ============================================================================
# STEP 4 — FILTER BRANDS BY MIN_PERIODS
# ============================================================================
def filter_min_periods(agg: pd.DataFrame, min_periods: int) -> pd.DataFrame:
    """Keep only brands observed in at least `min_periods` distinct months."""
    counts = agg.groupby("brand").size()
    keep = counts[counts >= min_periods].index
    return agg[agg.brand.isin(keep)].copy()


# ============================================================================
# STEP 5 — REINDEX EACH BRAND TO THE FULL MONTHLY GRID
# ============================================================================
def build_calendar(agg: pd.DataFrame):
    """Return the ordered list of (year, month) periods and a 0..N-1 index map."""
    periods = (agg[["period_year", "period_month"]]
               .drop_duplicates()
               .sort_values(["period_year", "period_month"])
               .reset_index(drop=True))
    periods["period_index"] = range(len(periods))
    return periods


def reindex_to_grid(agg: pd.DataFrame, periods: pd.DataFrame) -> pd.DataFrame:
    """
    Reindex every retained brand to all N periods so that gaps are explicit.
    Correct lags require a regular monthly grid (a missing month must not shift
    a lag_1 into being a lag_2-in-calendar).
    """
    brands = agg["brand"].unique()
    full = (pd.MultiIndex.from_product([brands, periods["period_index"]],
                                       names=["brand", "period_index"]).to_frame(index=False))
    full = full.merge(periods, on="period_index", how="left")
    grid = full.merge(agg, on=["brand", "period_year", "period_month"], how="left")
    return grid.sort_values(["brand", "period_index"]).reset_index(drop=True)


# ============================================================================
# STEP 6 — FEATURE ENGINEERING
# ============================================================================
def engineer_features(grid: pd.DataFrame) -> pd.DataFrame:
    """
    Build the leakage-safe feature set per brand on the regular monthly grid.

    Features: lag_{1,2,3,4,8,13}, rolling_mean_4, rolling_std_4, rolling_mean_13,
    month, quarter, holiday_month, promo_intensity. Target: sales_units and its
    log (log_sales_units). See module docstring for the no-leakage conventions.
    """
    g = grid.copy()
    gb = g.groupby("brand", sort=False)["sales_units"]

    # Lags of raw sales (past values only -> no leakage)
    for k in LAGS:
        g[f"lag_{k}"] = gb.shift(k)

    # Rolling stats on PAST values (shift(1) first, then roll) to exclude current month
    past = gb.shift(1)
    g["rolling_mean_4"] = past.groupby(g["brand"], sort=False).rolling(4, min_periods=1).mean().reset_index(level=0, drop=True)
    g["rolling_std_4"] = past.groupby(g["brand"], sort=False).rolling(4, min_periods=2).std().reset_index(level=0, drop=True)
    g["rolling_mean_13"] = past.groupby(g["brand"], sort=False).rolling(13, min_periods=1).mean().reset_index(level=0, drop=True)

    # Calendar features
    g["month"] = g["period_month"]
    g["quarter"] = ((g["period_month"] - 1) // 3 + 1)
    g["holiday_month"] = g["period_month"].isin(HOLIDAY_MONTHS).astype(int)

    # Log target (modelling target in log space) — NOT an input feature
    g["log_sales_units"] = np.log(g["sales_units"].where(g["sales_units"] > 0))

    # Promotional intensity (known/planned exogenous); structurally 0 for danskvand/RTD
    g["promo_intensity"] = (g["promo_units"] / g["sales_units"]).clip(0, 1)

    return g


# ============================================================================
# STEP 7 — FORWARD-CHAINING TRAIN/VAL/TEST SPLIT (by date)
# ============================================================================
def assign_split(g: pd.DataFrame, periods: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Label rows train/val/test by period using contiguous, no-look-ahead blocks."""
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


# ============================================================================
# ORCHESTRATION
# ============================================================================
def build_category(category: str, slug: str) -> dict:
    """Run the full Step 1-8 build for one category; return a summary dict."""
    print(f"\n=== {category} ===")
    facts = load_scoped_facts(slug)
    agg = aggregate_brand_month(facts)
    agg = filter_min_periods(agg, MIN_PERIODS)
    periods = build_calendar(agg)
    grid = reindex_to_grid(agg, periods)
    feats = engineer_features(grid)
    feats, split_dates = assign_split(feats, periods)

    out = OUT_DIR / category
    out.mkdir(parents=True, exist_ok=True)
    feats.to_parquet(out / f"{slug}_feature_matrix.parquet", index=False)
    with open(out / f"{slug}_split_dates.json", "w") as fh:
        json.dump(split_dates, fh, indent=2)

    summary = {
        "category": category,
        "brands": int(feats.brand.nunique()),
        "periods": int(len(periods)),
        "grid_rows": int(len(feats)),
        "observed_rows": int(feats.sales_units.notna().sum()),
        "split": f"{split_dates['train']}/{split_dates['val']}/{split_dates['test']}",
        "test_window": f"{split_dates['test_start']}..{split_dates['test_end']}",
    }
    print(f"    brands={summary['brands']} periods={summary['periods']} "
          f"grid_rows={summary['grid_rows']} observed={summary['observed_rows']} "
          f"split={summary['split']}")
    return summary


def main():
    print("Nielsen feature-matrix regeneration — scope = DVH EXCL. HD, MIN_PERIODS = 30")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summaries = [build_category(cat, slug) for cat, slug in CATEGORIES.items()]

    # Write a small markdown report alongside the outputs
    lines = ["# Feature-matrix regeneration report (DVH EXCL. HD, MIN_PERIODS=30)", "",
             "| Category | Brands | Periods | Grid rows | Observed rows | Split (tr/val/te) | Test window |",
             "|---|---|---|---|---|---|---|"]
    for s in summaries:
        lines.append(f"| {s['category']} | {s['brands']} | {s['periods']} | {s['grid_rows']} | "
                     f"{s['observed_rows']} | {s['split']} | {s['test_window']} |")
    (OUT_DIR / "regeneration_report.md").write_text("\n".join(lines) + "\n")
    print(f"\nDone. Outputs in {OUT_DIR}")


if __name__ == "__main__":
    main()
