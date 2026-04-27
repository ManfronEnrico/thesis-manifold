"""
Nielsen CSD Preprocessing Pipeline
====================================
Extracts brand × market monthly time series from the Nielsen Fabric warehouse,
engineers all features required for the 5 forecasting models, applies the
locked train/val/test split, and saves the feature matrix to disk.

Output files (Parquet, project-root-relative):
  results/phase1/feature_matrix.parquet   — full feature matrix, all series
  results/phase1/series_index.csv         — index of (brand, market) series
  results/phase1/split_dates.json         — locked split boundaries
  results/phase1/preprocessing_report.md — data quality summary

Usage:
  python3 -m ai_research_framework.data.preprocessing
"""

import sys, json, tracemalloc, time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from thesis.data.nielsen.scripts.nielsen_connector import get_connection
from thesis.thesis_agents.ai_research_framework.features.engineer_features import (
    make_calendar,
    filter_series,
    engineer_features,
    apply_split,
    build_series_index,
    DEFAULT_TARGET_MARKET as TARGET_MARKET,
    DEFAULT_MIN_PERIODS as MIN_PERIODS,
    DEFAULT_TRAIN_END as TRAIN_END,
    DEFAULT_VAL_END as VAL_END,
)

OUT = ROOT / "results" / "phase1"
OUT.mkdir(parents=True, exist_ok=True)


# ── 1. Pull raw data from Nielsen ─────────────────────────────────────────────

def pull_raw(conn) -> pd.DataFrame:
    """
    Join facts × product dim × period dim, scoped to TARGET_MARKET.
    Returns one row per (brand, period_year, period_month).
    Aggregates across product_id (sum) so the grain is brand × month.
    """
    sql = f"""
    SELECT
        p.brand,
        t.period_year,
        t.period_month,
        SUM(f.sales_units)           AS sales_units,
        SUM(f.sales_value)           AS sales_value,
        SUM(f.sales_in_liters)       AS sales_liters,
        SUM(COALESCE(f.sales_units_any_promo, 0)) AS promo_units,
        AVG(COALESCE(f.weighted_distribution, 0)) AS weighted_dist
    FROM dbo.csd_clean_facts_v f
    JOIN dbo.csd_clean_dim_product_v p ON f.product_id = p.product_id
    JOIN dbo.csd_clean_dim_period_v  t ON f.period_id  = t.period_id
    JOIN dbo.csd_clean_dim_market_v  m ON f.market_id  = m.market_id
    WHERE m.market_description = '{TARGET_MARKET}'
      AND f.sales_units > 0
    GROUP BY p.brand, t.period_year, t.period_month
    ORDER BY p.brand, t.period_year, t.period_month
    """
    cur = conn.cursor()
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    df = pd.DataFrame([list(r) for r in rows], columns=cols)
    return df


# Steps 2-6 (calendar, series filter, feature engineering, split, series index)
# are imported from thesis.thesis_agents.ai_research_framework.features.engineer_features
# to avoid duplication between the CLI batch script and the LangGraph agent.


# ── 7. Save outputs ────────────────────────────────────────────────────────────

def save_outputs(df: pd.DataFrame, series_idx: pd.DataFrame,
                 all_dates: list, elapsed: float, peak_mb: float):

    df.to_parquet(OUT / "feature_matrix.parquet", index=False)
    series_idx.to_csv(OUT / "series_index.csv", index=False)

    split_dates = {
        "train_start": str(min(all_dates).date()),
        "train_end":   f"{TRAIN_END[0]}-{TRAIN_END[1]:02d}-01",
        "val_start":   f"{TRAIN_END[0]}-{TRAIN_END[1]+1 if TRAIN_END[1]<12 else 1:02d}-01",
        "val_end":     f"{VAL_END[0]}-{VAL_END[1]:02d}-01",
        "test_start":  f"{VAL_END[0]}-{VAL_END[1]+1 if VAL_END[1]<12 else 1:02d}-01",
        "test_end":    str(max(all_dates).date()),
    }
    with open(OUT / "split_dates.json", "w") as f:
        json.dump(split_dates, f, indent=2)

    n_brands = df["brand"].nunique()
    n_rows   = len(df)
    features = [c for c in df.columns
                if c not in ["brand", "date", "period_year", "period_month",
                             "split", "sales_units", "log_sales_units"]]

    report = f"""# Nielsen Preprocessing Report
> Generated: 2026-04-13
> Market scope: {TARGET_MARKET}
> Min periods filter: {MIN_PERIODS}

## Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | {n_brands} |
| Total rows | {n_rows:,} |
| Periods per brand | {n_rows // n_brands} |
| Features engineered | {len(features)} |
| Peak RAM (preprocessing) | {peak_mb:.1f} MB |
| Elapsed time | {elapsed:.1f} s |

## Split Boundaries

| Split | Start | End | Periods |
|---|---|---|---|
| Train | {split_dates["train_start"]} | {split_dates["train_end"]} | {series_idx["train_periods"].iloc[0]} |
| Val | {split_dates["val_start"]} | {split_dates["val_end"]} | {series_idx["val_periods"].iloc[0]} |
| Test | {split_dates["test_start"]} | {split_dates["test_end"]} | {series_idx["test_periods"].iloc[0]} |

## Feature List

{chr(10).join(f"- `{f}`" for f in features)}

## Top 20 Brands by Total Sales Units

{series_idx.head(20).to_markdown(index=False)}
"""
    (OUT / "preprocessing_report.md").write_text(report)
    print(report)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Nielsen Preprocessing Pipeline")
    print(f"Market scope: {TARGET_MARKET}")
    print(f"Output: {OUT}\n")

    tracemalloc.start()
    t0 = time.perf_counter()

    print("Connecting to Nielsen...")
    conn = get_connection()
    print("Connected.\n")

    print("Step 1/5 — Pulling raw data from Nielsen...")
    raw = pull_raw(conn)
    conn.close()
    print(f"  Raw rows: {len(raw):,}  |  Brands: {raw['brand'].nunique()}")

    print("Step 2/5 — Building full calendar index...")
    df, all_dates = make_calendar(raw)
    print(f"  Rows after calendar fill: {len(df):,}")

    print("Step 3/5 — Filtering short series...")
    df = filter_series(df)
    print(f"  Series kept after filter (>= {MIN_PERIODS} non-zero periods): "
          f"{df['brand'].nunique()} brands")

    print("Step 4/5 — Engineering features...")
    df = engineer_features(df)

    print("Step 5/5 — Applying split labels...")
    df = apply_split(df)

    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_mb = peak / 1024 / 1024

    print(f"\nDone in {elapsed:.1f}s  |  Peak RAM: {peak_mb:.1f} MB")

    series_idx = build_series_index(df)
    save_outputs(df, series_idx, all_dates, elapsed, peak_mb)
    print(f"\nOutputs written to {OUT}/")


if __name__ == "__main__":
    main()
