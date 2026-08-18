"""Measure how forecast horizon trades against training rows and test coverage.

Horizon H enters the row budget twice, which is the part that is easy to miss:
  1. usable_rows(brand) = n_months - MAX_LAG - H      (one row lost per step of H)
  2. the target itself becomes y_{t+H}, so the *last* H months of every brand
     yield no target at all.

It also changes what is being learned: H=1 predicts next month from last month's
observed value (lag_1 is highly informative); H=12 must predict a year ahead,
where lag_1 is stale and the seasonal term carries the load.
"""
import sys
from pathlib import Path

sys.path.insert(0, r"Z:\_dev-ssd\thesis-manifold")
sys.path.insert(0, r"Z:\_dev-ssd\thesis-manifold\02_thesis_data\_02_preprocessing\nielsen\_shared_modules")

import pandas as pd
from pipeline_config import CATEGORIES, get_paths, DVH_PARENT_MARKET_ID

BRAND_COL = "brand"

def load_panel(category: str) -> pd.DataFrame:
    p = get_paths(category)
    cache = p["step_output_dir"] / "step_1_aggregate_bymonth.parquet"
    if not cache.exists():
        return None
    return pd.read_parquet(cache)

MAX_LAG = 13

rows = []
for cat in CATEGORIES:
    df = load_panel(cat)
    if df is None:
        print(f"  {cat}: no step-1 cache, skipping")
        continue
    counts = df.groupby(BRAND_COL).size()
    n_brands = len(counts)
    for H in (1, 3, 6, 12):
        # A brand contributes max(0, n - MAX_LAG - H) rows.
        usable = (counts - MAX_LAG - H).clip(lower=0)
        min_periods = MAX_LAG + H + 1
        rows.append({
            "category": cat,
            "H": H,
            "MIN_PERIODS": min_periods,
            "brands_total": n_brands,
            "brands_kept": int((counts >= min_periods).sum()),
            "train_rows": int(usable.sum()),
        })

out = pd.DataFrame(rows)
# Express each horizon relative to H=1 within its category.
base = out[out.H == 1].set_index("category")["train_rows"]
out["pct_of_H1"] = out.apply(lambda r: 100 * r.train_rows / base[r.category], axis=1)
out["brand_pct"] = 100 * out.brands_kept / out.brands_total

pd.set_option("display.width", 200)
for cat in out.category.unique():
    sub = out[out.category == cat]
    print(f"\n=== {cat} ===")
    print(sub[["H", "MIN_PERIODS", "brands_kept", "brands_total", "brand_pct", "train_rows", "pct_of_H1"]]
          .to_string(index=False, float_format=lambda x: f"{x:.1f}"))

print("\n=== TOTALS ACROSS ALL FOUR CATEGORIES ===")
tot = out.groupby("H").agg(train_rows=("train_rows", "sum"),
                           brands_kept=("brands_kept", "sum"),
                           brands_total=("brands_total", "sum")).reset_index()
tot["pct_of_H1"] = 100 * tot.train_rows / tot.train_rows.iloc[0]
print(tot.to_string(index=False, float_format=lambda x: f"{x:.1f}"))
