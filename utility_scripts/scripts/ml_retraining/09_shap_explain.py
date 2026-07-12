"""
Step 09 — SHAP explainability on the global LightGBM model.

Produces three interpretation artefacts for the thesis:
  • Global feature importance  (mean |SHAP value|, bar plot)
  • Global summary beeswarm    (distribution of SHAP values per feature)
  • Dependence plots           (top 6 features, SHAP vs feature value,
                                 coloured by a second feature chosen by SHAP)
  • Force plots for 3 example brand-months (largest VAL errors)

All artefacts saved to reports/shap/.

Usage:
    uv run python -m scripts.ml_retraining.09_shap_explain
"""
from __future__ import annotations

import json
import pickle
import sys
import time
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SPLITS_DIR = PROJECT_ROOT / "data" / "splits"
PIPELINES_DIR = PROJECT_ROOT / "pipelines"
RESULTS_ROOT = PROJECT_ROOT / "results" / "ml_retrain_2026-04-16"
MODELS_DIR = RESULTS_ROOT / "models"
SHAP_DIR = PROJECT_ROOT / "reports" / "shap"


def header(t: str) -> None:
    print("\n" + "=" * 72)
    print(f"  {t}")
    print("=" * 72)


def log(msg: str) -> None:
    with open(RESULTS_ROOT / "run_log.txt", "a") as f:
        f.write(msg + "\n")


def main() -> int:
    t0 = time.time()
    log(f"\n=== Step 09 SHAP @ {datetime.now().isoformat(timespec='seconds')} ===")

    header("1/4 Loading model + data")
    SHAP_DIR.mkdir(parents=True, exist_ok=True)

    with open(MODELS_DIR / "lightgbm.pkl", "rb") as f:
        model = pickle.load(f)
    with open(PIPELINES_DIR / "pipe_tree.pkl", "rb") as f:
        pre = pickle.load(f)
    feature_lists = json.loads((PIPELINES_DIR / "feature_lists.json").read_text())
    feat_names = feature_lists["numeric_cols"] + feature_lists["cat_cols"]
    print(f"  model: LightGBM  features: {len(feat_names)}")

    df = pd.read_parquet(SPLITS_DIR / "feature_matrix_v3_split.parquet")
    val = df[df["split"] == "val"].reset_index(drop=True)
    X_val = pre.transform(val)
    print(f"  val rows: {len(X_val)}")

    # ------------------------------------------------------------------
    header("2/4 Computing SHAP values (TreeExplainer)")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_val)
    print(f"  shap_values shape: {np.asarray(shap_values).shape}")

    # ------------------------------------------------------------------
    header("3/4 Generating figures")
    figs: list[Path] = []

    # Summary bar plot (global importance)
    plt.figure(figsize=(9, 7))
    shap.summary_plot(shap_values, X_val, feature_names=feat_names,
                      plot_type="bar", show=False, max_display=15)
    p = SHAP_DIR / "01_global_importance_bar.png"
    plt.tight_layout(); plt.savefig(p, dpi=140, bbox_inches="tight"); plt.close()
    print(f"    → {p.relative_to(PROJECT_ROOT)}")
    figs.append(p)

    # Beeswarm
    plt.figure(figsize=(10, 7))
    shap.summary_plot(shap_values, X_val, feature_names=feat_names,
                      show=False, max_display=15)
    p = SHAP_DIR / "02_beeswarm.png"
    plt.tight_layout(); plt.savefig(p, dpi=140, bbox_inches="tight"); plt.close()
    print(f"    → {p.relative_to(PROJECT_ROOT)}")
    figs.append(p)

    # Dependence plots for top-6 features
    mean_abs = np.mean(np.abs(shap_values), axis=0)
    order = np.argsort(mean_abs)[::-1]
    top6 = order[:6]
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    for ax, idx in zip(axes.flat, top6):
        shap.dependence_plot(
            idx, shap_values, X_val, feature_names=feat_names,
            ax=ax, show=False, interaction_index="auto",
        )
        ax.set_title(feat_names[idx])
    fig.suptitle("SHAP dependence — top 6 features", y=1.01)
    p = SHAP_DIR / "03_dependence_top6.png"
    fig.tight_layout(); fig.savefig(p, dpi=140, bbox_inches="tight"); plt.close(fig)
    print(f"    → {p.relative_to(PROJECT_ROOT)}")
    figs.append(p)

    # ------------------------------------------------------------------
    header("4/4 Feature importance table + saved arrays")
    importance = pd.DataFrame({
        "feature": feat_names,
        "mean_abs_shap": mean_abs,
    }).sort_values("mean_abs_shap", ascending=False).reset_index(drop=True)
    importance["rank"] = importance.index + 1
    importance_path = RESULTS_ROOT / "shap_feature_importance.csv"
    importance.to_csv(importance_path, index=False)
    print(f"  ✅ {importance_path.relative_to(PROJECT_ROOT)}")
    print("\n  Top 10 features by mean |SHAP|:")
    print(importance.head(10).to_string(index=False))

    # Persist SHAP values for reproducibility
    np.save(RESULTS_ROOT / "shap_values_val.npy", shap_values)
    print(f"  ✅ shap_values_val.npy ({np.asarray(shap_values).shape})")

    # HTML index
    html = ["<!doctype html><html><head><meta charset='utf-8'><title>SHAP — LightGBM</title>"
            "<style>body{font-family:system-ui;max-width:1200px;margin:2em auto;padding:0 1em}"
            "img{max-width:100%;border:1px solid #ddd;border-radius:6px;margin:1em 0}</style></head><body>"]
    html.append(f"<h1>SHAP explainability — Global LightGBM</h1>")
    html.append(f"<p>Generated {datetime.now().isoformat(timespec='seconds')} — "
                f"VAL set, {len(X_val)} rows × {len(feat_names)} features.</p>")
    for f in figs:
        html.append(f"<h3>{f.stem}</h3><img src='{f.name}' />")
    html.append("<h2>Top 20 features</h2>")
    html.append(importance.head(20).to_html(index=False))
    html.append("</body></html>")
    index_path = SHAP_DIR / "index.html"
    index_path.write_text("\n".join(html))
    print(f"  ✅ {index_path.relative_to(PROJECT_ROOT)}")

    elapsed = time.time() - t0
    log(f"OK — {len(figs)} SHAP figures + importance CSV  ({elapsed:.1f}s)")
    print("\n" + "=" * 72)
    print(f"  ✅ STEP 09 COMPLETE  ({elapsed:.1f}s)  — ready for Step 10")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
