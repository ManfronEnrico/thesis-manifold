"""Third constraint: does an evaluable test window survive at each horizon?

The panel keys on (period_year, period_month) -- there is no date column.
With a ~15% test share, a horizon longer than the test window leaves no
forecast origin whose target falls inside the window, so the horizon cannot be
evaluated at all without enlarging the test share (which shrinks training).
"""
import sys, pandas as pd
sys.path.insert(0, r"Z:\_dev-ssd\thesis-manifold")
sys.path.insert(0, r"Z:\_dev-ssd\thesis-manifold\02_thesis_data\_02_preprocessing\nielsen\_shared_modules")
from pipeline_config import CATEGORIES, get_paths

for cat in CATEGORIES:
    p = get_paths(cat)
    df = pd.read_parquet(p["step_output_dir"] / "step_1_aggregate_bymonth.parquet")
    per = (df.period_year.astype(int) * 12 + df.period_month.astype(int)).unique()
    per = sorted(per)
    n = len(per)
    lo, hi = min(per), max(per)
    fmt = lambda m: f"{m // 12}-{m % 12 or 12:02d}"
    n_test = round(n * 0.15); n_val = round(n * 0.15)
    print(f"\n{cat}: {n} months, {fmt(lo)} -> {fmt(hi)}")
    print(f"  at 70/15/15: train={n - n_val - n_test}, val={n_val}, test={n_test} months")
    for H in (1, 3, 6, 12):
        origins = n_test - H + 1
        print(f"    H={H:2d}: " + (f"{origins} evaluable test origins" if origins > 0
                                   else "NO EVALUABLE ORIGIN in a 15% test window"))
