#!/usr/bin/env python3
"""
SRQ1 — per-brand breakdown of the pooled-vs-per-category difference.

WHY THIS EXISTS: `srq1_pooled.py` found that pooling wins on WMAPE for the two
data-poor categories and loses for the two data-rich ones (P0040 F49), but that
median MAPE DISAGREES in 2 of 8 cells, with disagreements (>11pp) far larger than
any WMAPE delta (<=2.5pp) (F50).

The proposed explanation was that WMAPE is volume-weighted, so pooling must be
helping large series and hurting small ones WITHIN a category. That was an
inference from two aggregate metrics. This script tests it directly: compute the
pooled-minus-per-category error difference for EACH brand, and correlate it against
that brand's own training rows and volume.

If the explanation holds, the correlation is negative and clear: brands with more
history/volume benefit less (or are harmed) by pooling, small brands benefit more.
If it does not hold, the aggregate disagreement needs a different account -- and
knowing that is worth more than an untested story in the write-up.

METHOD: refits the exact same models as srq1_pooled.py (same 12 features, same
protocol, same seed), then scores per brand rather than per category. Brands with a
zero-actual test window are reported but excluded from MAPE-based statistics, since
APE is undefined there rather than merely large -- the same scorability filter used
for SRQ4 brand selection.

Self-contained, seed=42, reproducible. No API spend.
Usage:  .venv/Scripts/python.exe 03_thesis_modelling/model_training/srq1/srq1_pooled_perbrand.py [--trials 30]
Output: 04_thesis_results/srq1/{pooled_perbrand.csv, pooled_perbrand_summary.md}
"""

import argparse
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR

# Reuse the sibling script's definitions verbatim so the two cannot drift: same
# FEATURES, same CATS, same tuning protocol, same seed. Importing beats copying.
sys.path.insert(0, str(_here.parent))
from srq1_pooled import (  # noqa: E402
    CATS, FEATURES, SPLITS, SEED, _load, _fit_tuned, _all_metrics,
)

warnings.filterwarnings("ignore")

OUT = THESIS_RESULTS_SRQ1_DIR


def _brand_rows(parts, cat):
    """Training-row count and mean test volume per brand, for the x-axis."""
    tr = pd.concat([parts[cat]["train"], parts[cat]["val"]])
    n_train = tr.groupby("brand").size().rename("n_train")
    vol = (np.expm1(parts[cat]["test"]["log_sales_units"])
           .groupby(parts[cat]["test"]["brand"]).mean().rename("mean_test_units"))
    return pd.concat([n_train, vol], axis=1)


def main():
    ap = argparse.ArgumentParser(description="Per-brand pooled-vs-per-category delta")
    ap.add_argument("--trials", type=int, default=30)
    trials = ap.parse_args().trials
    OUT.mkdir(parents=True, exist_ok=True)

    parts = {cat: _load(cat, slug) for cat, slug in CATS.items()}
    pooled = {s: pd.concat([parts[c][s] for c in CATS], ignore_index=True)
              for s in SPLITS}

    rows = []
    for model in ("LightGBM", "XGBoost"):
        print(f"\n########## {model} (trials={trials}) ##########")
        pm, _, _ = _fit_tuned(model, pooled["train"], pooled["val"], trials)

        for cat in CATS:
            p = parts[cat]
            if len(p["train"]) < 30 or len(p["test"]) == 0:
                continue
            cm, _, _ = _fit_tuned(model, p["train"], p["val"], trials)
            meta = _brand_rows(parts, cat)
            te = p["test"]

            for brand, g in te.groupby("brand"):
                y = np.expm1(g["log_sales_units"].values)
                # APE is undefined against a zero actual -- not merely large.
                # Flag rather than silently averaging a divide-by-zero.
                scorable = bool((y > 0).all())
                p_pred = np.expm1(pm.predict(g[FEATURES].fillna(0.0)))
                c_pred = np.expm1(cm.predict(g[FEATURES].fillna(0.0)))
                p_mape, p_med, p_wm = _all_metrics(y, p_pred)
                c_mape, c_med, c_wm = _all_metrics(y, c_pred)
                m = meta.loc[brand] if brand in meta.index else None
                rows.append(dict(
                    model=model, category=cat, brand=str(brand),
                    n_test=len(g), scorable=scorable,
                    n_train=int(m["n_train"]) if m is not None and pd.notna(m["n_train"]) else 0,
                    mean_test_units=float(m["mean_test_units"]) if m is not None else np.nan,
                    pooled_wmape=p_wm, percat_wmape=c_wm,
                    delta_wmape=p_wm - c_wm,
                    pooled_mape=p_mape, percat_mape=c_mape,
                    delta_mape=p_mape - c_mape,
                ))
            print(f"  {cat:13s} {len(te.groupby('brand'))} brands scored")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "pooled_perbrand.csv", index=False)

    # ---- the actual test of the F50 explanation ---------------------------
    lines = ["# SRQ1 — per-brand pooled-vs-per-category breakdown", "",
             "Tests the F50 explanation directly: *does pooling help large series",
             "and hurt small ones within a category?*", "",
             "`delta` = pooled error - per-category error. **Negative = pooling is",
             "better for that brand.** If the explanation holds, delta should rise",
             "with brand size (pooling helps small brands, hurts large ones), i.e.",
             "a **positive** correlation between delta and size.", ""]

    ok = df[df.scorable].copy()
    lines += [f"Brands scored: {len(df)} rows "
              f"({df.brand.nunique()} distinct brands x {df.model.nunique()} models). "
              f"Excluded as unscorable (zero actual in test window): "
              f"{int((~df.scorable).sum())} rows.", ""]

    lines += ["## Correlation of delta with brand size", "",
              "| Model | vs log(train rows) | vs log(mean test units) | n |",
              "|---|---|---|---|"]
    for model in ("LightGBM", "XGBoost"):
        d = ok[(ok.model == model) & (ok.mean_test_units > 0) & (ok.n_train > 0)]
        if len(d) < 5:
            continue
        r_rows = float(np.corrcoef(np.log(d.n_train), d.delta_wmape)[0, 1])
        r_vol = float(np.corrcoef(np.log(d.mean_test_units), d.delta_wmape)[0, 1])
        lines.append(f"| {model} | {r_rows:+.3f} | {r_vol:+.3f} | {len(d)} |")
    lines.append("")

    # Tercile view: more legible than a correlation for the write-up.
    lines += ["## Delta by volume tercile (WMAPE percentage points)", "",
              "| Model | Volume tercile | median delta | mean delta | n | pooling wins |",
              "|---|---|---|---|---|---|"]
    for model in ("LightGBM", "XGBoost"):
        d = ok[(ok.model == model) & (ok.mean_test_units > 0)].copy()
        if len(d) < 9:
            continue
        d["tercile"] = pd.qcut(d.mean_test_units, 3,
                               labels=["small", "medium", "large"])
        for t in ("small", "medium", "large"):
            g = d[d.tercile == t]
            if not len(g):
                continue
            win = int((g.delta_wmape < 0).sum())
            lines.append(f"| {model} | {t} | {g.delta_wmape.median():+.1f} | "
                         f"{g.delta_wmape.mean():+.1f} | {len(g)} | "
                         f"{win}/{len(g)} ({100*win/len(g):.0f}%) |")
    lines.append("")

    lines += ["## Per-category, per-tercile (WMAPE pp, median)", "",
              "| Model | Category | small | medium | large |",
              "|---|---|---|---|---|"]
    for model in ("LightGBM", "XGBoost"):
        for cat in CATS:
            d = ok[(ok.model == model) & (ok.category == cat) &
                   (ok.mean_test_units > 0)].copy()
            if len(d) < 6:
                continue
            d["tercile"] = pd.qcut(d.mean_test_units, 3,
                                   labels=["small", "medium", "large"])
            vals = [d[d.tercile == t].delta_wmape.median() for t in
                    ("small", "medium", "large")]
            lines.append(f"| {model} | {cat} | " +
                         " | ".join(f"{v:+.1f}" if pd.notna(v) else "--"
                                   for v in vals) + " |")
    lines.append("")

    (OUT / "pooled_perbrand_summary.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    # Console verdict.
    #
    # Judged on the WIN-RATE trend across terciles, not on the correlation. The
    # correlation is not trustworthy here: medians and means diverge sharply
    # (outlier brands move the mean and with it r), so a flat tercile table can
    # still produce r = +0.14. Win-rate is immune to outlier magnitude -- it asks
    # only "for how many brands did pooling win", which is the question.
    print("\n" + "=" * 72)
    for model in ("LightGBM", "XGBoost"):
        d = ok[(ok.model == model) & (ok.mean_test_units > 0) & (ok.n_train > 0)]
        if len(d) < 9:
            continue
        r = float(np.corrcoef(np.log(d.mean_test_units), d.delta_wmape)[0, 1])
        d = d.copy()
        d["tercile"] = pd.qcut(d.mean_test_units, 3,
                               labels=["small", "medium", "large"])
        wr = {t: (d[d.tercile == t].delta_wmape < 0).mean()
              for t in ("small", "medium", "large")}
        spread = wr["small"] - wr["large"]
        # Monotone decline of >=10pp in win-rate from small to large brands.
        verdict = ("SUPPORTS (pooling helps small brands more)"
                   if spread >= 0.10 and wr["small"] > wr["medium"] > wr["large"]
                   else "CONTRADICTS (pooling helps large brands more)"
                   if spread <= -0.10
                   else "NULL -- no size relationship")
        print(f"{model:9s} win-rate small/med/large = "
              f"{wr['small']:.0%}/{wr['medium']:.0%}/{wr['large']:.0%}  "
              f"(r={r:+.3f})  {verdict}")
    print("=" * 72)
    print("Verdict uses win-rate monotonicity, not r -- see the note above.")
    print(f"Saved pooled_perbrand.csv + pooled_perbrand_summary.md in {OUT}")


if __name__ == "__main__":
    main()
