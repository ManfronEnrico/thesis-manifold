"""How predictable is the target at each horizon?

Row count is only half the trade-off. The other half: at H=1 the model predicts
next month from an observed value one month old. At H=12 it must predict a year
ahead, where the most recent observation is 12 months stale. If autocorrelation
decays fast, the extra horizon buys unpredictability, not just fewer rows.

Measures, per category, the pooled within-brand correlation between
log1p(sales) at t and at t+H -- the naive-persistence signal available to any
model at that horizon.
"""
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, r"Z:\_dev-ssd\thesis-manifold")
sys.path.insert(0, r"Z:\_dev-ssd\thesis-manifold\02_thesis_data\_02_preprocessing\nielsen\_shared_modules")
from pipeline_config import CATEGORIES, get_paths

BRAND_COL, DATE_COL, TARGET = "brand", "period_start", "sales_units"

rows = []
for cat in CATEGORIES:
    p = get_paths(cat)
    df = pd.read_parquet(p["step_output_dir"] / "step_1_aggregate_bymonth.parquet")
    date_col = DATE_COL if DATE_COL in df.columns else [c for c in df.columns if "period" in c or "date" in c][0]
    df = df.sort_values([BRAND_COL, date_col])
    y = np.log1p(df[TARGET])
    g = y.groupby(df[BRAND_COL])
    for H in (1, 3, 6, 12):
        fut = g.shift(-H)
        m = fut.notna() & y.notna()
        # Persistence signal: corr(y_t, y_{t+H}) within brand, pooled.
        r_persist = np.corrcoef(y[m], fut[m])[0, 1] if m.sum() > 10 else np.nan
        # Naive-persistence RMSE in log space: the bar a model must beat.
        rmse = float(np.sqrt(((fut[m] - y[m]) ** 2).mean()))
        rows.append({"category": cat, "H": H, "n_pairs": int(m.sum()),
                     "corr_y_t_vs_y_tH": r_persist, "naive_rmse_log": rmse})

out = pd.DataFrame(rows)
for cat in out.category.unique():
    print(f"\n=== {cat} ===")
    print(out[out.category == cat][["H", "n_pairs", "corr_y_t_vs_y_tH", "naive_rmse_log"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

print("\n=== MEAN ACROSS CATEGORIES ===")
print(out.groupby("H")[["corr_y_t_vs_y_tH", "naive_rmse_log"]].mean()
      .to_string(float_format=lambda x: f"{x:.3f}"))
