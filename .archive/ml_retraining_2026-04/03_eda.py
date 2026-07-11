"""
Step 03 — Exploratory Data Analysis.

Focuses on the baseline feature matrix (what we'll train on), produces:
  • Distributions (histograms + KDE) of sales_units, log_sales_units
  • Correlation heatmap of 21 numerical features
  • Seasonality decomposition on aggregate series
  • Brand-level volume distribution
  • ACF / PACF on aggregate sales (motivates lag choices)

All figures saved to reports/eda/ as PNG, plus an HTML index.

Usage:
    uv run python -m scripts.ml_retraining.03_eda
"""
from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # non-interactive backend, safe on headless runs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CLEAN_DIR = PROJECT_ROOT / "data" / "clean"
EDA_DIR = PROJECT_ROOT / "reports" / "eda"
RESULTS_ROOT = PROJECT_ROOT / "results" / "ml_retrain_2026-04-16"

sns.set_theme(style="whitegrid", context="paper")


def header(t: str) -> None:
    print("\n" + "=" * 72)
    print(f"  {t}")
    print("=" * 72)


def log(msg: str) -> None:
    with open(RESULTS_ROOT / "run_log.txt", "a") as f:
        f.write(msg + "\n")


def save_fig(fig, name: str) -> Path:
    path = EDA_DIR / f"{name}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"    → {path.relative_to(PROJECT_ROOT)}")
    return path


# ---------------------------------------------------------------------------
# 1. Load baseline FM
# ---------------------------------------------------------------------------
def load_baseline() -> pd.DataFrame:
    df = pd.read_parquet(CLEAN_DIR / "feature_matrix_baseline.parquet")
    df["date"] = pd.to_datetime(df["date"])
    return df


# ---------------------------------------------------------------------------
# 2. Distributions
# ---------------------------------------------------------------------------
def plot_distributions(df: pd.DataFrame) -> list[Path]:
    header("1/5 Distributions")
    paths: list[Path] = []

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(df["sales_units"], bins=60, kde=True, ax=axes[0], color="#3b7ddd")
    axes[0].set_title("sales_units (raw)")
    axes[0].set_xlabel("sales_units")
    sns.histplot(df["log_sales_units"], bins=60, kde=True, ax=axes[1], color="#d97706")
    axes[1].set_title("log(sales_units) (log1p)")
    axes[1].set_xlabel("log_sales_units")
    paths.append(save_fig(fig, "01_sales_distribution"))

    # Brand-level volume distribution (total sales per brand)
    fig, ax = plt.subplots(figsize=(10, 4))
    brand_totals = (
        df.groupby("brand")["sales_units"].sum().sort_values(ascending=False)
    )
    ax.bar(range(len(brand_totals)), brand_totals.values, color="#3b7ddd")
    ax.set_title(f"Total sales_units per brand (n={len(brand_totals)})")
    ax.set_xlabel("Brand rank")
    ax.set_ylabel("Total sales_units")
    ax.set_yscale("log")
    paths.append(save_fig(fig, "02_brand_volume_distribution"))
    return paths


# ---------------------------------------------------------------------------
# 3. Correlation heatmap
# ---------------------------------------------------------------------------
def plot_correlation(df: pd.DataFrame) -> Path:
    header("2/5 Correlation heatmap")
    num_df = df.select_dtypes(include=[np.number]).drop(columns=["month", "quarter", "holiday_month"], errors="ignore")
    corr = num_df.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
        linewidths=0.3, cbar_kws={"shrink": 0.7}, ax=ax,
    )
    ax.set_title("Correlation — numerical features")
    return save_fig(fig, "03_correlation_heatmap")


# ---------------------------------------------------------------------------
# 4. Seasonality decomposition (aggregate)
# ---------------------------------------------------------------------------
def plot_seasonality(df: pd.DataFrame) -> Path:
    header("3/5 Seasonality decomposition (aggregate)")
    agg = (
        df.groupby("date")["sales_units"].sum().asfreq("MS").fillna(0)
    )
    from statsmodels.tsa.seasonal import STL

    stl = STL(agg, period=12, robust=True).fit()
    fig = stl.plot()
    fig.set_size_inches(11, 7)
    fig.suptitle("STL decomposition — aggregate monthly sales_units", y=1.02)
    return save_fig(fig, "04_stl_decomposition")


# ---------------------------------------------------------------------------
# 5. ACF / PACF (motivates lag choices)
# ---------------------------------------------------------------------------
def plot_acf_pacf(df: pd.DataFrame) -> Path:
    header("4/5 ACF / PACF")
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

    agg = df.groupby("date")["sales_units"].sum().asfreq("MS").fillna(0)
    # PACF requires lags < 50% of sample size → cap at 20 for our 42-month series
    nlags = min(20, len(agg) // 2 - 1)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    plot_acf(agg, lags=nlags, ax=axes[0])
    axes[0].set_title(f"ACF (aggregate sales_units, lags={nlags})")
    plot_pacf(agg, lags=nlags, ax=axes[1], method="ywm")
    axes[1].set_title(f"PACF (aggregate sales_units, lags={nlags})")
    return save_fig(fig, "05_acf_pacf")


# ---------------------------------------------------------------------------
# 6. Brand snapshots (top 6 by volume)
# ---------------------------------------------------------------------------
def plot_brand_snapshots(df: pd.DataFrame) -> Path:
    header("5/5 Brand snapshots (top 6 by total volume)")
    top6 = (
        df.groupby("brand")["sales_units"].sum().sort_values(ascending=False).head(6).index.tolist()
    )
    fig, axes = plt.subplots(2, 3, figsize=(15, 7), sharex=True)
    for ax, brand in zip(axes.flat, top6):
        sub = df[df["brand"] == brand].sort_values("date")
        ax.plot(sub["date"], sub["sales_units"], color="#3b7ddd", lw=1.5)
        ax.set_title(f"{brand}  (n={len(sub)})")
        ax.grid(alpha=0.3)
    fig.suptitle("Top-6 brands — monthly sales_units", y=1.02)
    return save_fig(fig, "06_top_brands_timeseries")


# ---------------------------------------------------------------------------
# Summary stats & HTML index
# ---------------------------------------------------------------------------
def summary_stats(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "brands": df["brand"].nunique(),
        "date_range": f"{df['date'].min().date()} → {df['date'].max().date()}",
        "periods": df["date"].nunique(),
        "mean_sales_units": float(df["sales_units"].mean()),
        "median_sales_units": float(df["sales_units"].median()),
        "std_sales_units": float(df["sales_units"].std()),
        "skew_sales_units": float(df["sales_units"].skew()),
        "zero_sales_count": int((df["sales_units"] == 0).sum()),
    }


def write_html_index(figs: list[Path], stats: dict) -> Path:
    path = EDA_DIR / "index.html"
    rows = "\n".join(
        f'  <div class="fig"><h3>{f.stem}</h3><img src="{f.name}" /></div>'
        for f in figs
    )
    stats_table = "\n".join(
        f"  <tr><td>{k}</td><td>{v}</td></tr>" for k, v in stats.items()
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>EDA — Baseline feature matrix</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 1100px; margin: 2em auto; padding: 0 1em; color: #222; }}
h1 {{ border-bottom: 2px solid #3b7ddd; padding-bottom: .3em; }}
.fig {{ margin: 2em 0; }}
.fig img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 6px; }}
table {{ border-collapse: collapse; margin: 1em 0; }}
th, td {{ padding: .4em 1em; border: 1px solid #ddd; text-align: left; }}
th {{ background: #f4f6f8; }}
</style>
</head>
<body>
<h1>EDA — Baseline feature matrix</h1>
<p>Generated {datetime.now().isoformat(timespec='seconds')}</p>
<h2>Summary statistics</h2>
<table><tbody>
{stats_table}
</tbody></table>
<h2>Figures</h2>
{rows}
</body>
</html>
"""
    path.write_text(html)
    print(f"  ✅ {path.relative_to(PROJECT_ROOT)}")
    return path


def main() -> int:
    t0 = time.time()
    log(f"\n=== Step 03 EDA @ {datetime.now().isoformat(timespec='seconds')} ===")

    df = load_baseline()
    stats = summary_stats(df)
    print(f"  loaded {stats['rows']} rows  |  {stats['brands']} brands  |  {stats['date_range']}")

    figs: list[Path] = []
    plot_jobs = [
        ("distributions", lambda: figs.extend(plot_distributions(df))),
        ("correlation", lambda: figs.append(plot_correlation(df))),
        ("seasonality", lambda: figs.append(plot_seasonality(df))),
        ("acf_pacf", lambda: figs.append(plot_acf_pacf(df))),
        ("brand_snapshots", lambda: figs.append(plot_brand_snapshots(df))),
    ]
    for name, job in plot_jobs:
        try:
            job()
        except Exception as e:
            log(f"PARTIAL FAIL {name}: {type(e).__name__}: {e}")
            print(f"  ⚠️  {name} failed: {type(e).__name__}: {e}")

    write_html_index(figs, stats)

    elapsed = time.time() - t0
    log(f"OK — {len(figs)} figures  ({elapsed:.1f}s)")
    print("\n" + "=" * 72)
    print(f"  ✅ STEP 03 COMPLETE  ({elapsed:.1f}s)  — {len(figs)} figures in reports/eda/")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
