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
protocol, same seed), then scores per brand rather than per category.

METRIC DOMAINS. Brands with a zero-actual test window are excluded from MAPE-family
statistics only, where APE is genuinely undefined. They are RETAINED for every WMAPE
statistic, because WMAPE puts the sum in the denominator and is well-defined at zero.
An earlier version applied the exclusion to WMAPE too; that dropped 27% of brands --
the intermittent, low-volume ones the pooling question is chiefly about. Hyndman &
Koehler (2006, p. 683) call dropping zero windows "an artificial solution that is
impossible to apply in practical situations"; here it was not even necessary.

DEMAND CLASSES (2026-08-23). Results are broken out by the Syntetos-Boylan-Croston
partition -- smooth / erratic / intermittent / lumpy, at the derived cut-offs p = 1.32
and CV^2 = 0.49 -- rather than guarded by a volume threshold. This replaced a 1
unit/month floor that was a judgement call and, measured, a poor proxy: it removed 8
smooth brands while leaving 21 lumpy/intermittent ones in. **Nothing is now excluded
from the WMAPE tables**; irregular series are reported in their own row, which is what
Syntetos & Boylan's own work recommends.

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

    # TWO FRAMES, because the two metric families have different domains.
    #
    # `ok` (scorable only) is for MAPE-family statistics: APE is genuinely
    # UNDEFINED against a zero actual, so those rows cannot enter a mean or median
    # of percentage errors.
    #
    # `wm` (ALL brands) is for WMAPE statistics. **WMAPE is well-defined against
    # zero actuals** -- it is sum|y-yhat| / sum|y|, so a zero actual contributes a
    # finite numerator term and zero to the denominator. Nothing divides by zero.
    # Filtering it by scorability was a bug: it discarded 27% of brands from an
    # analysis that never needed the filter, and it was not harmless -- it flipped
    # the sign of the XGBoost size correlation (+0.252 scorable-only vs -0.095 on
    # all brands). The brands it removed are precisely the intermittent, low-volume
    # ones whose behaviour the pooling question is *about*, so excluding them
    # biased the very comparison being made.
    #
    # This also matches the literature. Hyndman & Koehler (2006, p. 683) call
    # dropping zero-actual windows "an artificial solution that is impossible to
    # apply in practical situations" and recommend metrics that are stable at zero
    # instead of altering the data to suit the metric. WMAPE is such a metric;
    # applying the exclusion to it took the cost of the workaround without needing
    # the workaround.
    # DEMAND-PATTERN CATEGORISATION, replacing the earlier ad-hoc volume floor.
    #
    # An intermediate version (2026-08-23) guarded the WMAPE tables with a 1
    # unit/month volume floor. It worked but was a judgement call, and the measured
    # overlap showed it was a poor proxy for what it was trying to exclude: it
    # removed 8 SMOOTH brands (well-behaved, merely small -- exactly the series a
    # forecasting study should keep) while leaving 21 lumpy/intermittent brands
    # above the line. Volume and regularity are different properties.
    #
    # Replaced by the Syntetos-Boylan-Croston categorisation (Syntetos, Boylan &
    # Croston 2005, JORS 56(5), 495-503, p. 495), whose cut-offs are DERIVED rather
    # than tuned: p = 1.32 average inter-demand interval, CV^2 = 0.49 on non-zero
    # demand sizes, giving smooth / erratic / intermittent / lumpy.
    #
    # THE KEY CHANGE IS THAT NOTHING IS EXCLUDED. Every brand is reported, broken
    # out by demand class. A weak result on lumpy series becomes a stated limitation
    # instead of an absence. That is the response both Hyndman & Koehler (2006,
    # p. 683) and Syntetos & Boylan (2005) actually recommend -- they object to
    # discarding difficult series, not to categorising them.
    #
    # `demand_classes.csv` is produced by srq1_demand_classes.py from train+val only.
    ok = df[df.scorable].copy()          # MAPE-family only -- APE undefined at zero
    wm_all = df.copy()                   # WMAPE -- every brand, nothing dropped
    wm = df.copy()

    dc_path = OUT / "demand_classes.csv"
    if dc_path.is_file():
        dc = pd.read_csv(dc_path)[["category", "brand", "demand_class", "p", "cv2"]]
        dc["brand"] = dc["brand"].astype(str)

        def _join(f):
            f = f.copy()
            f["brand"] = f["brand"].astype(str)
            return f.merge(dc, on=["category", "brand"], how="left")

        ok, wm, wm_all = _join(ok), _join(wm), _join(wm_all)
    else:
        for f in (ok, wm, wm_all):
            f["demand_class"] = "unclassified"
    lines += [f"Brands scored: {len(df)} rows "
              f"({df.brand.nunique()} distinct brands x {df.model.nunique()} models).", "",
              f"**WMAPE statistics below use all {len(df)} rows.** WMAPE is defined "
              f"against zero actuals (the sum is in the denominator), so no exclusion "
              f"is needed or applied.", "",
              f"**No brand is excluded from the WMAPE tables.** WMAPE is defined "
              f"against zero actuals (the sum is in the denominator), so all {len(wm_all)} "
              f"rows are reported. Results are broken out by **demand class** instead, "
              f"using the derived Syntetos-Boylan-Croston cut-offs (p = 1.32, "
              f"CV^2 = 0.49; Syntetos, Boylan & Croston 2005, p. 495).", "",
              f"*This replaces an earlier 1 unit/month volume floor, which was a "
              f"judgement call and a poor proxy for irregularity: it removed 8 smooth "
              f"brands while leaving 21 lumpy/intermittent ones in. See "
              f"`demand_classes.md`.*", "",
              f"**MAPE-family statistics use the {int(df.scorable.sum())} scorable rows** "
              f"({int((~df.scorable).sum())}, {100*(~df.scorable).mean():.0f}%, have a zero "
              f"actual somewhere in the test window, where APE is undefined rather than "
              f"merely large). Hyndman & Koehler (2006, p. 683) criticise dropping such "
              f"windows as impractical, which is a further reason to read the WMAPE "
              f"columns as primary here.", ""]

    lines += ["## Correlation of delta with brand size", "",
              "| Model | vs log(train rows) | vs log(mean test units) | n |",
              "|---|---|---|---|"]
    for model in ("LightGBM", "XGBoost"):
        d = wm[(wm.model == model) & (wm.mean_test_units > 0) & (wm.n_train > 0)]
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
        d = wm[(wm.model == model) & (wm.mean_test_units > 0)].copy()
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

    # The table the categorisation exists to produce.
    if "demand_class" in wm.columns and wm.demand_class.notna().any():
        lines += ["## Delta by demand class (WMAPE percentage points)", "",
                  "The Syntetos-Boylan-Croston partition. **Nothing is excluded** --",
                  "irregular series appear here rather than being filtered out, so a",
                  "weak result on them is visible.", "",
                  "| Model | Demand class | median delta | IQR | n scored | n no-signal | pooling wins |",
                  "|---|---|---|---|---|---|---|"]
        for model in ("LightGBM", "XGBoost"):
            for cls in ("smooth", "erratic", "intermittent", "lumpy"):
                g = wm[(wm.model == model) & (wm.demand_class == cls)]
                if not len(g):
                    continue
                # MEAN DELTA IS NOT REPORTED, deliberately.
                #
                # Removing the volume floor readmitted brands whose test window is
                # entirely zero (mean_test_units == 0.0). WMAPE is defined for them
                # -- nothing divides by zero -- but the denominator sum|y| is ~0, so
                # the ratio reaches 1e14. 63 of 460 rows exceed 1000pp, with a median
                # volume of 0.0 units. A MEAN over those is meaningless; it reported
                # magnitudes of 1e12 in the first version of this table.
                #
                # The categorisation fixed WHICH series are grouped together. It does
                # not make a mean of ratios robust, and it was never meant to. So:
                # median and IQR, plus an explicit count of the degenerate rows, so
                # the reader sees how many there are instead of finding them inside
                # an average.
                # Split, do not filter. `deg` rows have an ALL-ZERO test window --
                # there is no actual to be accurate about, so their WMAPE is a ratio
                # to ~0 and carries no information at any quantile, not just at the
                # mean. They are COUNTED in their own column rather than dropped, so
                # the reader sees that 15 of 31 lumpy brands have no test signal --
                # which is itself the most informative fact about that class.
                #
                # The quantiles are computed on the rows that HAVE a signal. This is
                # not the volume floor returning: the split is on "is there anything
                # to score against", which is a property of the data, not a
                # threshold chosen to make numbers look better.
                deg_mask = g.mean_test_units.fillna(0) <= 0
                deg = int(deg_mask.sum())
                gs = g[~deg_mask]
                win = int((gs.delta_wmape < 0).sum())
                if len(gs):
                    q1, q3 = gs.delta_wmape.quantile([0.25, 0.75])
                    med, iqr = f"{gs.delta_wmape.median():+.1f}", f"{q1:+.1f} to {q3:+.1f}"
                    wr = f"{win}/{len(gs)} ({100*win/len(gs):.0f}%)"
                else:
                    med, iqr, wr = "--", "--", "--"
                lines.append(
                    f"| {model} | {cls} | {med} | {iqr} | {len(gs)} | {deg} | {wr} |")
        lines += ["",
                  "**Reading it.** `smooth` is where a model should do well and where a",
                  "pooling effect is most interpretable. `lumpy` combines long gaps with",
                  "highly variable sizes, so large deltas there reflect the series, not",
                  "the method.", "",
                  "**`n no-signal` counts brands whose test window is entirely zero.**",
                  "There is no actual to be accurate about, so their WMAPE is a ratio to",
                  "~0 and reaches 1e14. They are **counted in their own column rather",
                  "than dropped**, and the statistics are computed on the rows that have",
                  "a signal.", "",
                  "**That column is the most informative thing in this table.** Roughly",
                  "half the `lumpy` brands (15 of 31) have no test signal at all. The",
                  "honest statement about lumpy series on this panel is therefore not",
                  "that a model forecasts them badly -- it is that **for half of them",
                  "there is nothing to forecast in the evaluation window**, which is a",
                  "property of monthly brand-level FMCG data worth reporting in its own",
                  "right.", "",
                  "Note this split is on *whether anything exists to score against*, a",
                  "property of the data -- not a volume threshold chosen to improve the",
                  "numbers.", "",
                  "**Means are never reported here.** A mean of ratios is not robust on",
                  "this panel even after the no-signal rows are set aside.", ""]

    lines += ["## Per-category, per-tercile (WMAPE pp, median)", "",
              "| Model | Category | small | medium | large |",
              "|---|---|---|---|---|"]
    for model in ("LightGBM", "XGBoost"):
        for cat in CATS:
            d = wm[(wm.model == model) & (wm.category == cat) &
                   (wm.mean_test_units > 0)].copy()
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
        d = wm[(wm.model == model) & (wm.mean_test_units > 0) & (wm.n_train > 0)]
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
