# %% [markdown]
# # OVERVIEW & SET-UP: Thesis Notebook — SRQ1 FINAL COMPARISON
# 
# **Scope**: Aggregate the outputs of all **7 model notebooks** into the headline tables
# and figures for Chapter 6 of the thesis.
# 
# **Inputs** (7 model notebooks — must be run before this one):
# 
# | Notebook | Output dir |
# |----------|-----------|
# | `thesis_notebook.ipynb` (CSD) | `outputs/` |
# | `thesis_notebook_danskvand.ipynb` | `outputs_danskvand/` |
# | `thesis_notebook_energidrikke.ipynb` | `outputs_energidrikke/` |
# | `thesis_notebook_rtd.ipynb` | `outputs_rtd/` |
# | `thesis_notebook_totalbeer.ipynb` | `outputs_totalbeer/` |
# | `thesis_notebook_pooled_4.ipynb` | `outputs_pooled_4/` |
# | `thesis_notebook_pooled_5.ipynb` | `outputs_pooled_5/` |
# 
# **Outputs** (saved to `outputs_final/`):
# - `headline_table.csv` — single CSV with all 7 models × 4 metrics
# - `pool_vs_spec.csv` — per-category specialized-vs-pooled comparison
# - `figures/fig_headline.png` — bar chart of all 7 models
# - `figures/fig_pool_vs_spec_heatmap.png` — heatmap pool vs spec deltas
# - `chapter6_table.md` — pre-formatted Markdown table for direct paste in thesis

# %% [markdown]
# ---
# 
# ## § 0.0 - Dynamic Centralized "path.py" Setup
# 
# **Why**: imports + paths. Define what categories were specialized vs pooled.
# 
# **How?**: finds project root based on "CLAUDE.md", then imports the paths.py

# %%
# Import the config file from the project root to centralize all directories
from pathlib import Path   
import importlib

# Find project root by locating CLAUDE.md -> helps dynamically finding the project root regardless of where the script is run from                                                                                                                                                                                                                                                          
current = Path.cwd()
while current != current.parent:
    if (current / "CLAUDE.md").exists():
        ROOT_DIR_FINDER = current
        break
    current = current.parent
else:
    raise FileNotFoundError("Could not find project root (CLAUDE.md)")

import sys
print(f"Project root found at: {ROOT_DIR_FINDER}")
sys.path.insert(0, str(ROOT_DIR_FINDER))


import paths
importlib.reload(paths)  # Reload the config module to ensure we have the latest changes

from paths import *

# %% [markdown]
# ## § 0.1 - Hard Code Notebook Specific Paths

# %%
# Import Notebook Specific Paths

# Sub-research question (e.g. "SRQ_1", or "SRQ_1_and_2")
CURRENT_NOTEBOOK_SRQ_ID = "SRQ_1"

# Notebook subfolder name
CURRENT_NOTEBOOK_FOLDER_NAME = "comparison"

# Notebook identifier (used in outputs)
CURRENT_NOTEBOOK_NAME = "comparison"

# %%
# Building Notebook Specific Paths Dynamically
CURRENT_NOTEBOOK_DIR = THESIS_MODELLING_NOTEBOOKS_DIR / CURRENT_NOTEBOOK_SRQ_ID / CURRENT_NOTEBOOK_FOLDER_NAME
print(CURRENT_NOTEBOOK_DIR)

CURRENT_NOTEBOOK_OUTPUTS_DIR = CURRENT_NOTEBOOK_DIR / f"{CURRENT_NOTEBOOK_NAME}_outputs"
print(CURRENT_NOTEBOOK_OUTPUTS_DIR)

CURRENT_NOTEBOOK_FIGURES_DIR = CURRENT_NOTEBOOK_OUTPUTS_DIR / "figures"
print(CURRENT_NOTEBOOK_FIGURES_DIR)

# %%
# Create directories
CURRENT_NOTEBOOK_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
CURRENT_NOTEBOOK_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## § 0.3 - Import Modelling Libraries

# %%
import sys, json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# ## § 0.4 - Testing Paths & Aggregate Notebooks
# 
# - All 7 outputs present? If any ✗, **run that notebook first**.
# - Ready to aggregate.

# %%
def get_upstream_notebook_outputs_dir(notebook_name: str, srq_id: str = "SRQ_1") -> Path:
    """
    Resolve the outputs directory for an upstream notebook.

    Args:
        notebook_name: e.g., "specialized_CSD", "pooled_4"
        srq_id: research question (default "SRQ_1")

    Returns:
        Path to {notebook_name}_outputs/
    """
    return THESIS_MODELLING_NOTEBOOKS_DIR / srq_id / notebook_name / f"{notebook_name}_outputs"


# Define upstream notebook names
SPECIALIZED = ["specialized_CSD", "specialized_danskvand", "specialized_energidrikke", "specialized_rtd", "specialized_totalbeer"]
POOLED = ["pooled_4", "pooled_5"]
ALL_UPSTREAM_NOTEBOOKS = SPECIALIZED + POOLED

# %%
print("Checking upstream notebook outputs:")
for notebook_name in ALL_UPSTREAM_NOTEBOOKS:
    outputs_dir = get_upstream_notebook_outputs_dir(notebook_name)
    metrics_file = outputs_dir / "all_models_metrics.csv"
    status = "✓" if metrics_file.exists() else "✗ MISSING"
    print(f"  {notebook_name:<25s} {status}  {metrics_file.relative_to(ROOT_DIR_FINDER)}")

# %%
# Check if any upstream data exists
missing_count = sum(1 for nb in ALL_UPSTREAM_NOTEBOOKS
                    if not (get_upstream_notebook_outputs_dir(nb) / "all_models_metrics.csv").exists())

if missing_count == len(ALL_UPSTREAM_NOTEBOOKS):
    print("⚠️   WARNING: No upstream notebook outputs found.")
    print("This notebook requires outputs from 7 specialized + pooled notebooks:")
    for nb in ALL_UPSTREAM_NOTEBOOKS:
        print(f"   - {nb}")
    print("\nNext steps:")
    print("1. Run each upstream notebook first")
    print("2. Ensure they produce: {notebook_name}_outputs/all_models_metrics.csv")
    print("3. Then re-run this notebook")
    print("\n" + "="*60)
elif missing_count > 0:
    print(f"⚠️   WARNING: {missing_count} upstream notebooks are missing.")
    print("Some results will be incomplete.")
else:
    print("✅ All upstream data found. Ready to aggregate.")

# %% [markdown]
# # >>> FIXED ABOVE BUT NOT BELOW (FOLDER AND FILE PATHING)
# 
# ---

# %% [markdown]
# ---
# 
# # MAIN CODE
# 
# ## §1 — Headline aggregate table
# 
# **Why**: single table with all 7 models × 4 metrics (median MAPE, mean MAPE, WAPE, RMSE).
# This is the master table for Chapter 6.

# %%
# §1 — Headline table
rows = []
for n in ALL_UPSTREAM_NOTEBOOKS:
    p = get_upstream_notebook_outputs_dir(n) / f"{CURRENT_NOTEBOOK_NAME}_all_models_metrics.csv"
    if not p.exists():
        print(f"⚠ Skipping {n} (no output)")
        continue
    metrics = pd.read_csv(p)
    for _, r in metrics.iterrows():
        # Identify the model variant (LightGBM_global vs LightGBM_pooled)
        model_name = r["model"]
        rows.append({
            "notebook": n,
            "scope": "specialized" if n in SPECIALIZED else "pooled",
            "model": model_name,
            "mape_median": r.get("mape_median"),
            "mape_mean": r.get("mape_mean"),
            "wape": r.get("wape"),
            "rmse": r.get("rmse"),
        })

headline = pd.DataFrame(rows)
print(f"[Headline table — {len(headline)} model results across {headline['notebook'].nunique()} notebooks]")
print(headline.to_string(index=False, float_format=lambda x: f"{x:,.2f}" if isinstance(x, float) else str(x)))
headline.to_csv(CURRENT_NOTEBOOK_OUTPUTS_DIR / f"{CURRENT_NOTEBOOK_NAME}_headline_table.csv", index=False)
print(f"\n✅ Saved: {CURRENT_NOTEBOOK_OUTPUTS_DIR.name}/headline_table.csv")


# %% [markdown]
# ### §1 — Observations + Decisions
# 
# - _Best LGB across all 7: ..._
# - _Best XGB across all 7: ..._
# - _Worst (apart from baselines): ..._

# %% [markdown]
# ---
# 
# # §2 — Pool vs Spec — the SRQ1 answer table
# 
# **Why**: the central comparison. For each category, compare:
# - Specialized model performance (from per-category notebook)
# - Pooled-4 performance restricted to that category (only for the 4 new categories)
# - Pooled-5 performance restricted to that category
# 
# Negative delta = pooling **wins**. Positive delta = specialized **wins**.

# %%
# §2 — Pool vs Spec
def per_brand_mape_filtered(predictions_df, pred_col):
    """Per-brand median MAPE on a subset (e.g. one category)."""
    if len(predictions_df) == 0: return float("nan")
    mapes = []
    for b in predictions_df["brand"].unique():
        sub = predictions_df[predictions_df["brand"] == b]
        yt, yp = sub["sales_units"].values, sub[pred_col].values
        mask = yt > 0
        if mask.sum() == 0: continue
        ape = np.abs((yt[mask] - yp[mask]) / yt[mask]) * 100
        mapes.append(float(np.median(ape)))
    return float(np.median(mapes)) if mapes else float("nan")

# Load specialized predictions per category
spec_preds = {}
for cat in SPECIALIZED:
    p = CURRENT_NOTEBOOK_OUTPUTS_DIR(cat) / f"{CURRENT_NOTEBOOK_NAME}_predictions_val_all.parquet"
    if p.exists():
        spec_preds[cat] = pd.read_parquet(p)

# Load pooled predictions
pool_preds = {}
for pool in POOLED:
    p = CURRENT_NOTEBOOK_OUTPUTS_DIR(pool) / f"{CURRENT_NOTEBOOK_NAME}_predictions_val_all.parquet"
    if p.exists():
        pool_preds[pool] = pd.read_parquet(p)

# Build the comparison table
rows = []
for cat in SPECIALIZED:
    if cat not in spec_preds:
        continue
    spec_df = spec_preds[cat]
    spec_lgb_mape = per_brand_mape_filtered(spec_df, "LightGBM_global")
    spec_xgb_mape = per_brand_mape_filtered(spec_df, "XGBoost_global")

    row = {
        "category": cat,
        "n_brands": spec_df["brand"].nunique(),
        "n_rows_val": len(spec_df),
        "spec_LGB": spec_lgb_mape,
        "spec_XGB": spec_xgb_mape,
    }

    for pool in POOLED:
        if pool not in pool_preds:
            row[f"{pool}_LGB"] = np.nan
            row[f"{pool}_XGB"] = np.nan
            continue
        pool_df = pool_preds[pool]
        # Filter pooled predictions to this category only
        if "category" in pool_df.columns:
            pool_cat = pool_df[pool_df["category"] == cat]
        else:
            pool_cat = pool_df  # fallback if category col missing
        row[f"{pool}_LGB"] = per_brand_mape_filtered(pool_cat, "LightGBM_pooled")
        row[f"{pool}_XGB"] = per_brand_mape_filtered(pool_cat, "XGBoost_pooled")

    # Compute deltas (negative = pooling wins for that category)
    if not np.isnan(row.get("pooled_4_LGB", np.nan)):
        row["delta_pool4_LGB_pp"] = row["pooled_4_LGB"] - row["spec_LGB"]
    if not np.isnan(row.get("pooled_5_LGB", np.nan)):
        row["delta_pool5_LGB_pp"] = row["pooled_5_LGB"] - row["spec_LGB"]

    rows.append(row)

cmp_df = pd.DataFrame(rows)
cmp_df.to_csv(CURRENT_NOTEBOOK_OUTPUTS_DIR / f"{CURRENT_NOTEBOOK_NAME}_pool_vs_spec.csv", index=False)
print("[Pool vs Spec — per-brand median MAPE per category]")
print(cmp_df.to_string(index=False, float_format=lambda x: f"{x:,.2f}" if isinstance(x, float) else str(x)))
print("\nNegative delta = POOLING wins for that category.")
print("Positive delta = SPECIALIZED wins.")


# %% [markdown]
# ### §2 — Observations + Decisions
# 
# **The answer to SRQ1**:
# - _For X categories pooling helps (negative delta)._
# - _For Y categories specialized wins (positive delta)._
# - _Weighted average: pool vs spec overall ..._

# %% [markdown]
# ---
# 
# # §3 — Headline figure 1: bar chart of all 7 models
# 
# **Why**: single visual to show the model landscape — baselines (SeasonalNaive, Ridge) at
# the top of the bars, then specialized (5 models), then pooled (2 models). Color-coded.

# %%
# §3 — Headline bar chart
sns.set_theme(style="whitegrid", context="paper")

# Filter to LightGBM/XGBoost only (the meaningful models)
plot_df = headline[headline["model"].str.contains("LightGBM|XGBoost", case=False)].copy()
# Order: specialized first (5), then pooled (2), per algo
plot_df["scope_model"] = plot_df["scope"] + " | " + plot_df["model"].str.extract(r"(LightGBM|XGBoost)", expand=False)
plot_df["label"] = plot_df["notebook"] + "\n" + plot_df["model"].str.extract(r"(LightGBM|XGBoost)", expand=False)

fig, ax = plt.subplots(figsize=(11, 5.5))
sns.barplot(
    data=plot_df,
    x="label", y="mape_median",
    hue="scope",
    palette={"specialized": "#3b7ddd", "pooled": "#d97706"},
    ax=ax,
)
ax.set_title("Headline: VAL median MAPE — all 7 model setups (specialized vs pooled, LGB vs XGB)")
ax.set_ylabel("VAL median MAPE (%)")
ax.set_xlabel("")
ax.tick_params(axis="x", rotation=20, labelsize=8)
ax.legend(title="Scope", loc="upper right")
plt.tight_layout()
plt.savefig(CURRENT_NOTEBOOK_FIGURES_DIR / "fig_headline.png", dpi=150, bbox_inches="tight")
plt.show()
print(f"✅ Saved: {CURRENT_NOTEBOOK_FIGURES_DIR.name}/fig_headline.png")


# %% [markdown]
# ### §3 — Observations + Decisions
# 
# - _Visual takeaway: ..._

# %% [markdown]
# ---
# 
# # §4 — Headline figure 2: pool vs spec heatmap
# 
# **Why**: compact heatmap of the per-category deltas. Green cells = pool wins. Red = spec wins.
# Goes directly into Chapter 6 as the SRQ1 answer figure.

# %%
# §4 — Heatmap of deltas
delta_cols = [c for c in cmp_df.columns if c.startswith("delta_")]
if delta_cols:
    heat = cmp_df.set_index("category")[delta_cols].T

    fig, ax = plt.subplots(figsize=(8, 3))
    sns.heatmap(
        heat, annot=True, fmt=".2f", cmap="RdYlGn_r", center=0,
        cbar_kws={"label": "Δ MAPE (pp)\n(negative = pool wins)"},
        ax=ax,
    )
    ax.set_title("Pool vs Spec — per-brand MAPE delta (pp)")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(CURRENT_NOTEBOOK_FIGURES_DIR / "fig_pool_vs_spec_heatmap.png", dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✅ Saved: {CURRENT_NOTEBOOK_FIGURES_DIR.name}/fig_pool_vs_spec_heatmap.png")
else:
    print("(No deltas computed — run pooled notebooks first)")


# %% [markdown]
# ### §4 — Observations + Decisions
# 
# - _Pool wins on N out of 5 categories (LGB)._
# - _Average delta: ..._

# %% [markdown]
# ---
# 
# # §5 — Pre-formatted Markdown table for Chapter 6
# 
# **Why**: produce a markdown table ready to paste directly into the thesis Chapter 6.
# Columns: Category | Spec LGB | Pool-4 LGB | Pool-5 LGB | Δ.

# %%
# §5 — Markdown table for thesis paste
md_lines = ["# Chapter 6 — SRQ1 Headline Table\n"]
md_lines.append("Per-brand median MAPE on validation set (lower is better).\n")
md_lines.append("| Category | n brands | n rows | Spec LGB | Pool-4 LGB | Pool-5 LGB | Δ pool-5 vs spec |")
md_lines.append("|----------|---------:|-------:|---------:|-----------:|-----------:|-----------------:|")

for _, r in cmp_df.iterrows():
    spec   = f"{r['spec_LGB']:.2f}%"   if not pd.isna(r["spec_LGB"])   else "—"
    pool4  = f"{r.get('pooled_4_LGB', np.nan):.2f}%" if not pd.isna(r.get("pooled_4_LGB", np.nan)) else "—"
    pool5  = f"{r.get('pooled_5_LGB', np.nan):.2f}%" if not pd.isna(r.get("pooled_5_LGB", np.nan)) else "—"
    delta5 = r.get("delta_pool5_LGB_pp", np.nan)
    delta_str = f"{delta5:+.2f} pp" if not pd.isna(delta5) else "—"
    md_lines.append(f"| {r['category']} | {r['n_brands']} | {r['n_rows_val']:,} | {spec} | {pool4} | {pool5} | {delta_str} |")

md_lines.append("\n## Interpretation")
md_lines.append("- Negative Δ → pooling improves accuracy for that category (knowledge transfers across categories).")
md_lines.append("- Positive Δ → category-specialized model is better (category patterns are too distinct to share).")
md_lines.append("- The choice of model for production should follow the per-category winner.")

md_text = "\n".join(md_lines)
print(md_text)
(CURRENT_NOTEBOOK_OUTPUTS_DIR / "chapter6_table.md").write_text(md_text, encoding="utf-8")
print(f"\n✅ Saved: {CURRENT_NOTEBOOK_OUTPUTS_DIR.name}/chapter6_table.md (paste into thesis)")


# %% [markdown]
# ### §5 — Observations + Decisions
# 
# - _Headline message for the thesis: ..._

# %% [markdown]
# ---
# 
# # §6 — Wrap-up
# 
# All artefacts saved to `outputs_final/`:
# - `headline_table.csv` — full results matrix
# - `pool_vs_spec.csv` — per-category deltas
# - `figures/fig_headline.png` — bar chart all 7
# - `figures/fig_pool_vs_spec_heatmap.png` — delta heatmap
# - `chapter6_table.md` — paste-ready markdown table
# 
# **Next steps**:
# 1. Paste `chapter6_table.md` into thesis Chapter 6
# 2. Use both PNGs as Figure 6.1 + 6.2
# 3. Update SRQ2 agentic notebook to load the model with the best per-category MAPE


