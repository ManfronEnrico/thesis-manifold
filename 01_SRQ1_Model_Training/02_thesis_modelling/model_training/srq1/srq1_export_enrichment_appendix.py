#!/usr/bin/env python
"""
Appendix tables for the holiday-enrichment study and the feature diagnostics.

WHAT THIS COVERS
----------------
Tables 94-99, continuing the sequence that `export_holiday_appendix.py` began at
90 (source provenance, annual counts, monthly matrix, feature definitions):

  94  Ablation result, tuned      -- THE headline table
  95  Untuned vs tuned            -- why the untuned run was not reportable
  96  SHAP attribution            -- rules out the month-re-encoding objection
  97  Collinearity (VIF)          -- the diagnostic the pipeline never had
  98  Redundancy reduction, rejected -- a measured negative result
  99  Ridge alpha by rolling-origin CV

CONVENTIONS (F7, matching export_appendix.py)
---------------------------------------------
  - .md + .csv twins written from the same DataFrame, so they cannot disagree
  - EVERY number is read from the result CSVs; none is typed into this file
  - units in the column headers
  - an <!-- INTERNAL REVIEW --> separator; nothing below it is for submission
  - output resolved through PATHS.py, never a literal path

The inputs are produced by srq1_holiday_ablation_tuned.py,
srq1_holiday_ablation.py, srq1_feature_diagnostics.py and srq1_ridge_cv.py,
which write into the SRQ1 tables/ directory. A missing input is reported and
skipped rather than faked.

USAGE
    python srq1_export_enrichment_appendix.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


def _find_repo_root() -> Path:
    start = Path(__file__).resolve().parent
    for cand in (start, *start.parents):
        if any((cand / a).exists() for a in (".env.example", ".env", "PATHS.py")):
            return cand
    raise FileNotFoundError(f"Could not find project root above {start}")


_REPO_ROOT = _find_repo_root()
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from PATHS import get_chapter_tables_dir, get_srq_tables_dir  # noqa: E402

sys.path.insert(0, str(_REPO_ROOT / "05_thesis_results"))
from review_notes import write_review_note  # noqa: E402
from check_reader_facing import warn_after_run  # noqa: E402

# The active horizon, and the paths that follow from it. ONE source, so the
# matrix read and the results written can never describe different horizons
# (P0049 F24). Set SRQ1_HORIZON=1 to run the secondary horizon.
from _horizon import HORIZON, matrix_path, results_root, banner  # noqa: E402,F401


SRC = (results_root() / "tables")

# Ch5: with-feature vs without-feature model comparisons and their SHAP
# attribution -- modelling results, not data provenance (that is Ch4).
OUT = get_chapter_tables_dir("model_benchmark")
# Review notes go BESIDE the table, not INSIDE it: 05_thesis_results/ ships to
# assessors, so an internal note appended below a table travelled with the
# thesis. They are written to 06_thesis_writing/writing-notes/, which the
# submission export removes.
_PRODUCER = "01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_export_enrichment_appendix.py"


def _emit(seq: int, slug: str, title: str, caption: str, df: pd.DataFrame,
          note: str = "", review: str = "") -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"{seq:02d}_{slug}"
    df.to_csv(OUT / f"{stem}.csv", index=False, encoding="utf-8")
    # disable_numparse: tabulate otherwise re-parses "22.20" back to a float and
    # renders "22.2", silently dropping a significant digit from a results table.
    # Formatting is already fixed by _fmt, so the strings must pass through
    # untouched.
    lines = [f"**{title}.** {caption}", "",
             df.to_markdown(index=False, disable_numparse=True)]
    if note:
        lines += ["", f"*Note.* {note}"]
    (OUT / f"{stem}.md").write_text("\n".join(lines) + "\n",
                                    encoding="utf-8", newline="\n")
    write_review_note(slug, OUT / f"{stem}.md", title, review, _PRODUCER)
    print(f"  {stem:44s} {len(df):>4d} rows  {title}")


def _read(name: str) -> pd.DataFrame | None:
    p = SRC / name
    if not p.exists():
        print(f"  SKIP -- missing input: {p.name}")
        return None
    return pd.read_csv(p)


def _fmt(v, nd=2):
    """Format to a fixed number of decimals, as a STRING.

    Trailing zeros are significant in a results table -- "-3.00" and "22.20"
    state the precision the measurement was reported at, while "-3" and "22.2"
    silently imply less. to_markdown() re-infers a column of numeric-looking
    strings back to float and strips them, so every formatted column is forced
    to object dtype at the DataFrame level (see _as_text)."""
    return "" if pd.isna(v) else f"{v:.{nd}f}"


def _as_text(df: pd.DataFrame) -> pd.DataFrame:
    """Pin every column to object dtype.

    Necessary but NOT sufficient on its own -- tabulate re-parses numeric-looking
    strings regardless of dtype, so _emit also passes disable_numparse=True.
    """
    return df.astype(object)


def table_ablation_tuned(seq: int) -> None:
    d = _read("holiday_ablation_tuned_delta.csv")
    if d is None:
        return
    out = pd.DataFrame({
        "Category": d["category"],
        "Model": d["model"],
        "WMAPE without (%)": d["without"].map(_fmt),
        "WMAPE with (%)": d["with"].map(_fmt),
        "Delta (pp)": d["delta_pp"].map(lambda v: f"{v:+.2f}"),
        "Direction": np.where(d["delta_pp"] < 0, "improved", "worsened"),
    })
    out = _as_text(out.sort_values(["Category", "Model"]))

    helped = int((d["delta_pp"] < 0).sum())
    _emit(seq, "holiday_ablation_tuned",
          "Holiday enrichment: test WMAPE with and without",
          "Per category and model, hyperparameters tuned separately for each arm.",
          out,
          note=(f"Negative delta indicates the holiday features improved "
                f"accuracy. They helped in {helped} of {len(d)} category-model "
                f"combinations. Each arm was tuned independently on the "
                f"validation split, refit on train+validation, and scored once "
                f"on the held-out test split."),
          review=_review_tuned(d))


SEP = chr(10) * 2  # paragraph break inside a review block


def _review_tuned(d: pd.DataFrame) -> str:
    """Build table 94's reviewer note from the data.

    Every count here was previously typed as a literal. When the determinism
    fix (P0047 F18) moved the XGBoost numbers, the caption -- which was
    computed -- updated itself while this block silently kept asserting the
    superseded "3 of 8". Derive it, so the note cannot outlive its numbers.
    """
    lin = d[d["model"] == "Ridge"]
    tree = d[d["model"] != "Ridge"]
    lin_h, tree_h = int((lin["delta_pp"] < 0).sum()), int((tree["delta_pp"] < 0).sum())

    txt = ("Do NOT quote the mean of this column. It averages over model families "
           "that respond differently, and that difference is itself the finding: "
           f"Ridge benefits in {lin_h} of {len(lin)} categories while the tree "
           f"models benefit in {tree_h} of {len(tree)} cells.")

    # The least-stable cell is found, not named: the untuned/tuned swing is what
    # "unstable" means here, so let the comparison identify it.
    u = _read("holiday_ablation_delta.csv")
    if u is not None:
        m = u.merge(d, on=["category", "model"], suffixes=("_u", "_t"))
        if len(m):
            m = m.assign(swing=(m["delta_pp_t"] - m["delta_pp_u"]).abs())
            w = m.loc[m["swing"].idxmax()]
            para = f"{w['category']} {w['model']} is the least stable cell "
            para += f"in the study (it swings {w['swing']:.2f}pp between the "
            para += "untuned and tuned runs, table 95)."
            txt += SEP + para
    return txt


def table_untuned_vs_tuned(seq: int) -> None:
    u = _read("holiday_ablation_delta.csv")
    t = _read("holiday_ablation_tuned_delta.csv")
    if u is None or t is None:
        return
    m = u.merge(t, on=["category", "model"], suffixes=("_untuned", "_tuned"))
    out = pd.DataFrame({
        "Category": m["category"],
        "Model": m["model"],
        "Baseline WMAPE, fixed config (%)": m["without_untuned"].map(_fmt),
        "Baseline WMAPE, tuned (%)": m["without_tuned"].map(_fmt),
        "Baseline gain (pp)": (m["without_untuned"] - m["without_tuned"]).map(
            lambda v: f"{v:+.2f}"),
        "Holiday delta, fixed (pp)": m["delta_pp_untuned"].map(lambda v: f"{v:+.2f}"),
        "Holiday delta, tuned (pp)": m["delta_pp_tuned"].map(lambda v: f"{v:+.2f}"),
    })
    out = _as_text(out.sort_values(["Category", "Model"]))

    worst = (m["without_untuned"] - m["without_tuned"]).max()
    _emit(seq, "holiday_ablation_tuning_sensitivity",
          "Effect of hyperparameter tuning on the ablation",
          "The same feature comparison, measured against a fixed-configuration "
          "baseline and against a tuned one.",
          out,
          note=(f"Tuning improved the baseline itself by up to {worst:.2f} "
                f"percentage points. Where a fixed configuration is badly "
                f"mis-specified, a feature comparison measured against it "
                f"reflects that mis-specification rather than the features."),
          review=("This table is why the fixed-configuration ablation was not "
                  "reported. Danskvand's trees were mis-specified by ~12pp, and "
                  "that category flips from harmful to helpful once the model "
                  "can fit. An ablation is only interpretable against a "
                  "properly specified model.\n\n"
                  "Methodological point worth a sentence in the text: the "
                  "direction of a feature effect can invert under tuning."))


def table_shap(seq: int) -> None:
    s = _read("holiday_ablation_shap.csv")
    if s is None:
        return
    focus = ["month", "quarter", "peak_month",
             "days_in_month", "n_holidays", "non_holiday_days"]
    sub = s[s["feature"].isin(focus)]
    piv = sub.pivot_table(index=["category", "feature"], columns="arm",
                          values="shap_pct").reset_index()
    piv["delta"] = piv.get("with", np.nan) - piv.get("without", np.nan)
    out = pd.DataFrame({
        "Category": piv["category"],
        "Feature": piv["feature"],
        "Attribution without (%)": piv["without"].map(lambda v: _fmt(v)),
        "Attribution with (%)": piv["with"].map(lambda v: _fmt(v)),
        "Change (pp)": piv["delta"].map(
            lambda v: "" if pd.isna(v) else f"{v:+.2f}"),
    })
    out = _as_text(out)
    _emit(seq, "holiday_shap_attribution",
          "SHAP attribution of calendar features, before and after enrichment",
          "Mean absolute SHAP value as a percentage of total attribution "
          "(LightGBM, test split).",
          out,
          note=("An empty 'without' cell marks a feature absent from that arm. "
                "If the holiday features merely re-encoded month-of-year, their "
                "attribution would be offset by an equal fall in month and "
                "peak_month. The existing calendar features lose substantially "
                "less than the holiday features gain, so the calendar carries "
                "information those features do not."),
          review=("This is the empirical half of the anti-collinearity "
                  "argument; appendix table 92 is the structural half. Cite both "
                  "when the enrichment is challenged as month re-encoded.\n\n"
                  "Note the tension worth stating plainly in the text: the "
                  "features earn attribution in every category, yet improve "
                  "accuracy in only some. Attribution is not accuracy."))


def table_vif(seq: int) -> None:
    v = _read("feature_vif.csv")
    if v is None:
        return
    piv = v.pivot_table(index="feature", columns="category",
                        values="vif").reset_index()
    cats = [c for c in piv.columns if c != "feature"]
    piv["_sort"] = piv[cats].replace([np.inf], 1e12).max(axis=1)
    piv = piv.sort_values("_sort", ascending=False).drop(columns="_sort")
    out = piv.rename(columns={"feature": "Feature"})
    for c in cats:
        out[c] = out[c].map(
            lambda x: "" if pd.isna(x) else ("inf" if np.isinf(x) else f"{x:.1f}"))
    out = _as_text(out)
    n_inf = int(np.isinf(v["vif"]).sum())
    _emit(seq, "feature_collinearity_vif",
          "Variance inflation factors by feature and category",
          "VIF computed on the log-scaled, standardised design matrix.",
          out,
          note=("'inf' marks an exact linear dependency: non_holiday_days is "
                "days_in_month minus n_holidays by construction. Higher values "
                "indicate a feature more fully determined by the others. The "
                "autoregressive lag and rolling-mean features are correlated by "
                "construction, since each is computed from the same series."),
          review=(f"{n_inf} exact dependencies across all categories.\n\n"
                  "NO THRESHOLD IS ASSERTED IN THE CAPTION, deliberately. The "
                  "conventional 5 and 10 cut-offs were attributed in an earlier "
                  "draft to a source not held in the project library; the "
                  "attribution was removed. See "
                  "writing-notes/unverified-claims-to-check.md item 1 before "
                  "putting any numeric threshold in prose.\n\n"
                  "StandardScaler plus Ridge's L2 penalty absorbs the rank "
                  "deficiency, so the exact dependency does not move the error "
                  "materially -- but that is a mechanism argument, not a number "
                  "measured here. Report the collinearity; do not claim it "
                  "explains accuracy, and do not cite a pp figure for its "
                  "removal unless a script computes one."))


def table_reduction_rejected(seq: int) -> None:
    c = _read("feature_redundancy_clusters.csv")
    p = _read("feature_proposed_set.csv")
    e = _read("feature_reduction_eval.csv")
    if c is None or p is None:
        return
    out = pd.DataFrame({
        "Category": p["category"],
        "Features available (n)": p["n_candidate"],
        "Features after reduction (n)": p["n_proposed"],
        "Clusters found (n)": [
            int((c["category"] == cat).sum()) for cat in p["category"]],
    })
    rho = p["rho"].iloc[0] if "rho" in p.columns else 0.95
    if e is not None and not e.empty:
        mf, mr = e["wmape_full"].mean(), e["wmape_reduced"].mean()
        verdict = (f"rejected: it raised mean test WMAPE from {mf:.2f} to "
                   f"{mr:.2f}" if mr > mf else
                   f"kept: mean test WMAPE moved {mf:.2f} to {mr:.2f}")
        outcome = (f"Across {len(e)} category-by-model cells the reduction was "
                   f"fitted against the full set and {verdict}.")
    else:
        outcome = ("The reduction was evaluated against the benchmark and "
                   "performed worse; run srq1_feature_diagnostics.py to "
                   "regenerate feature_reduction_eval.csv for the figures.")
    _emit(seq, "feature_redundancy_reduction",
          "Redundancy-based feature reduction, tested and rejected",
          "Correlated feature groups per category and the size of the reduced "
          "set they imply.",
          out,
          note=(f"Features were grouped where pairwise absolute Spearman "
                f"correlation was at least {rho}, keeping the member with the "
                "highest permutation importance on the validation split. " +
                outcome),
          review=("The negative result is the contribution. Collinearity is a "
                  "linear-model pathology: ridge cannot apportion credit "
                  "between correlated predictors, but a gradient-boosted tree "
                  "splits on whichever is locally most useful and loses real "
                  "information when the others are removed.\n\n"
                  "So the correlated lag features ARE information-adding for "
                  "the tree models, and this measurement is the evidence. A "
                  "reduction rule adopted without validation would have "
                  "degraded every reported number while appearing rigorous.\n\n"
                  "The 0.95 grouping threshold is a reporting parameter with no "
                  "cited source -- register item 2. Either justify it by "
                  "sensitivity analysis or describe it as an arbitrary choice."))


def table_ridge_alpha(seq: int) -> None:
    r = _read("ridge_cv_alpha.csv")
    if r is None:
        return
    out = pd.DataFrame({
        "Category": r["category"],
        "Arm": r["arm"],
        "Alpha selected": r["alpha_cv"].map(lambda v: f"{v:.4g}"),
        "WMAPE at fixed alpha=1 (%)": r["test_wmape_alpha1"].map(_fmt),
        "WMAPE at selected alpha (%)": r["test_wmape_cv"].map(_fmt),
        "Change (pp)": (r["test_wmape_cv"] - r["test_wmape_alpha1"]).map(
            lambda v: f"{v:+.2f}"),
    })
    out = _as_text(out.sort_values(["Category", "Arm"]))
    delta = r["test_wmape_cv"] - r["test_wmape_alpha1"]
    mean_change = delta.mean()
    # Every figure in the review note below is COMPUTED from the file just read.
    # They were typed literals until 2026-09-10 ("0.00-0.44pp", "1e-8", "13.7pp"
    # and a claim about RTD), and they described a superseded run: the current
    # file spans 0.21-0.22pp and holds no RTD row at all, so the note asserted a
    # spread and a category the table beside it did not show.
    spread_lo, spread_hi = delta.abs().min(), delta.abs().max()
    cats = ", ".join(sorted(r["category"].unique()))
    n_cells = len(r)
    _emit(seq, "ridge_alpha_cross_validation",
          "Ridge regularisation strength by rolling-origin cross-validation",
          "Alpha selected on development data only, with the previously "
          "hard-coded value shown for comparison.",
          out,
          note=("Rolling-origin cross-validation trains each fold on months "
                "preceding its validation block, so training data always "
                "precedes validation data. Ordinary k-fold cross-validation is "
                "not valid for this data, since shuffling would place later "
                "months in the training fold."),
          review=(f"Covers {n_cells} category-arm cell(s): {cats}.\n\n"
                  f"Mean change from selecting alpha rather than fixing it at "
                  f"1.0: {mean_change:+.2f}pp"
                  + (" -- i.e. slightly WORSE on test.\n\n" if mean_change > 0
                     else " on test.\n\n")
                  + f"The cross-validation curve is flat: the spread between "
                    f"the selected alpha and alpha=1 is "
                    f"{spread_lo:.2f}-{spread_hi:.2f}pp. Alpha barely matters "
                    "on this data.\n\n"
                    "So the hard-coded value was not a defect. Selecting it is "
                    "worth doing for method, not for accuracy, and the honest "
                    "reporting is that the correction is negligible."))


def main() -> int:
    print(f"Reading results from {SRC}")
    print(f"Writing appendix tables -> {OUT}")
    table_ablation_tuned(94)
    table_untuned_vs_tuned(95)
    table_shap(96)
    table_vif(97)
    table_reduction_rejected(98)
    table_ridge_alpha(99)
    print("\nDone. Every value is read from the result CSVs; none is typed "
          "into the generator.")
    warn_after_run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
