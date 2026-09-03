#!/usr/bin/env python
"""Render every tracked metric as thesis-ready appendix tables.

WHY THIS EXISTS
---------------
`summary.md` is a *reading* surface: it answers "which scenario won" in one table
and deliberately hides the rest. An appendix has the opposite job -- an examiner
must be able to check that a reported number came from somewhere, and that needs
the per-run detail, the units, and the provenance of each figure.

Both are generated from the same `runs.csv`, so they cannot disagree.

CONVENTIONS THAT ARE DELIBERATE
-------------------------------
**No table numbers.** Tables are emitted with a title and a caption but never an
"A.4"-style number. Numbering is Word's job: if a table is dropped from the
appendix late, hard-coded numbers silently go stale while Word's field-based
cross-references renumber themselves. The slug in the filename orders them.

**Submission-ready captions, segregated notes.** Everything inside a `.md` file
above the `<!-- REVIEW -->` marker is publishable as-is. Anything for us as
students lives below that marker, in a separate `_review_notes.md` sidecar --
never mixed into a caption, so a screenshot of any table is clean by
construction.

**Percentages are stored as numbers and displayed with a `%` suffix in a header,
not appended per cell.** "WMAPE (%)" with a bare `19.4` is the standard in
forecasting papers (cf. the M4/M5 competition tables): repeating the unit in
every cell adds width without information and breaks numeric alignment. This is
a presentation convention, not a claim about the underlying value.

**Wide over long.** Comparative tables are pivoted so models sit side by side.
Appendices print landscape; a reader comparing four models wants them adjacent,
not 28 rows apart.

No API calls. Free to run, and safe to re-run: it reads only results already on
disk. Missing inputs are skipped with a notice rather than crashing, so this is
runnable before the paid blocks execute.

Usage
-----
    python 03_thesis_modelling/scenario_setup/export_appendix.py

Output: 04_thesis_results/appendix/
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import THESIS_RESULTS_DIR, THESIS_RESULTS_SRQ1_DIR, THESIS_RESULTS_SRQ4_DIR  # noqa: E402

OUT = THESIS_RESULTS_DIR / "appendix"

# Measured allocation of Manifold's production E2B template (alias `prometheus`),
# not a literature estimate. See P0044 findings.
RAM_BUDGET_MB = 4096.0


# ---------------------------------------------------------------------------
# Emit helpers
# ---------------------------------------------------------------------------
_INDEX: list[tuple[str, str]] = []
_SEQ = [0]

# Everything above this marker in a table .md is submission-ready. Everything
# below it is for us. Kept in the SAME file, deliberately: the notes belong at
# the table they describe, and a screenshot cropped to the table cannot capture
# what sits below a horizontal rule.
REVIEW_SEP = "\n---\n\n<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->\n"


def _emit(slug: str, title: str, caption: str, df: pd.DataFrame,
          note: str = "", review: str = "") -> None:
    """Write one table as .md (paste/screenshot) and .csv (trace a number back).

    The FILENAME carries a sequence number so the directory sorts in generation
    order for our own review. The file CONTENT carries none: numbering inside
    the document is Word's job, and a hard-coded number goes stale the moment a
    table is dropped from the appendix."""
    OUT.mkdir(parents=True, exist_ok=True)
    _SEQ[0] += 1
    stem = f"{_SEQ[0]:02d}_{slug}"
    df.to_csv(OUT / f"{stem}.csv", index=False, encoding="utf-8")

    lines = [f"**{title}.** {caption}", "", df.to_markdown(index=False)]
    if note:
        lines += ["", f"*Note.* {note}"]
    if review:
        lines += [REVIEW_SEP, review]
    (OUT / f"{stem}.md").write_text("\n".join(lines) + "\n",
                                    encoding="utf-8", newline="\n")

    _INDEX.append((title, stem))
    print(f"  {stem:42s} {len(df):>4d} rows  {title}")


def _bold_best(df: pd.DataFrame, cols: list[str], lower_is_better=True,
               skip=()) -> pd.DataFrame:
    """Bold the winning value across `cols` in each row.

    Applied only where the values in a row are genuinely comparable -- the same
    measure computed for different models. Bolding down a column of unlike
    quantities would assert a comparison that does not exist."""
    out = df.copy()
    for i in out.index:
        if any(str(out.loc[i, k]) in skip for k in ("Measure", "Metric")
               if k in out.columns):
            continue
        vals = {}
        for c in cols:
            if c not in out.columns:
                continue
            raw = str(out.loc[i, c]).replace(",", "").replace("$", "").replace("%", "")
            raw = raw.replace("x", "").strip()
            try:
                vals[c] = float(raw)
            except (ValueError, TypeError):
                continue
        if len(vals) < 2:
            continue
        best = min(vals, key=vals.get) if lower_is_better else max(vals, key=vals.get)
        # Bold + italic. Markdown has no underline primitive, and the <u> tag
        # that would supply one does not survive the paste into Word, so the
        # two emphases Markdown does define are combined instead.
        out.loc[i, best] = f"***{out.loc[i, best]}***"
    return out


def _fmt(df: pd.DataFrame, spec: dict[str, str]) -> pd.DataFrame:
    """Round for display once, at the edge, so the .csv and the .md never show a
    number that rounds differently in each."""
    out = df.copy()
    for col, f in spec.items():
        if col in out.columns:
            out[col] = out[col].map(lambda v: "" if pd.isna(v) else f.format(v))
    return out


def _titlecase(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={c: c.replace("_", " ").strip().capitalize()
                              for c in df.columns})


# ---------------------------------------------------------------------------
# Metric dictionary
# ---------------------------------------------------------------------------
# Placed first because every later table is unreadable without it. Each entry
# gives the unit, the definition, the direction of improvement, and the field
# the number is computed from.
METRICS = [
    # -- central tendency: what "median" and "mean" mean here, and why both ----
    ("Central tendency", "Median", "--",
     "The middle value once the runs are ordered: half fall below it, half above. "
     "Reported as the headline for error because it is insensitive to outliers -- "
     "a single divergent series shifts a mean without limit but moves a median by "
     "at most one rank position.", "n/a", "computed per table"),
    ("Central tendency", "Mean", "--",
     "The arithmetic average. Reported alongside the median so the gap between the "
     "two is visible: a mean far above its median indicates a right-skewed error "
     "distribution driven by a few large failures.", "n/a", "computed per table"),
    ("Central tendency", "Coefficient of variation (CV)", "%",
     "Standard deviation divided by the mean, expressed as a percentage. A "
     "scale-free measure of dispersion, so series of different volumes are "
     "comparable.", "lower", "computed per table"),

    ("Correctness", "APE -- absolute percentage error", "%",
     "|forecast - actual| / actual for one run.", "lower", "runs.csv: ape"),
    ("Correctness", "Median APE", "%",
     "Median of APE over runs classed ok. The headline correctness figure.",
     "lower", "runs.csv: ape"),
    ("Correctness", "Mean APE", "%",
     "Mean of APE over runs classed ok.", "lower", "runs.csv: ape"),
    ("Correctness", "WMAPE -- weighted MAPE", "%",
     "Sum of absolute errors divided by sum of actuals across series. Weights each "
     "series by its volume, so a large brand is not outvoted by many small ones, "
     "and it stays defined when individual actuals approach zero.", "lower",
     "srq1/stat_baselines.csv: wmape"),

    ("Consistency", "CV across repeats", "%",
     "Per brand, the coefficient of variation of the forecast over repeated runs of "
     "the same prompt, averaged across brands. Measures run-to-run instability at "
     "fixed input.", "lower", "runs.csv: forecast"),
    ("Replicability", "Identical-answer rate", "%",
     "Share of brands whose forecasts across all repeats fall within a 1% band.",
     "higher", "runs.csv: forecast"),
    ("Replicability", "Top-answer agreement rate (1% tolerance)", "ratio",
     "For one brand, the share of repeated runs whose forecast agrees with the most "
     "commonly returned value, within a 1% tolerance; averaged across brands. A "
     "value of 1.00 means every repeat returned effectively the same answer, 0.20 "
     "that five repeats returned five different ones. Reported because LLM outputs "
     "vary between identical requests even at temperature zero (Atil et al., 2025).",
     "higher", "runs.csv: forecast"),

    ("Cost", "Tokens per answer", "tokens",
     "Input plus output tokens for one run.", "lower", "runs.csv: tokens"),
    ("Cost", "Reasoning tokens", "tokens",
     "Tokens the model spends on internal reasoning. Billed at the output rate but "
     "absent from the visible answer, so they are reported separately.", "lower",
     "runs.csv: tokens_reasoning"),
    ("Cost", "Cost per answer (estimated)", "USD",
     "Token counts at published rates. Excludes the code-execution container "
     "charge, which the API does not report per call.", "lower",
     "runs.csv: cost_usd_est"),
    ("Cost", "Cost billed (actual)", "USD",
     "Billed total from the provider's organisation-costs endpoint over the run "
     "window, including container charges. This is the figure reported in the text.",
     "lower", "summary.md: cost reconciliation"),
    ("Latency", "Response time", "s",
     "Wall-clock seconds per run, including tool round-trips.", "lower",
     "runs.csv: latency_s"),

    ("Reliability", "Outcome class", "count",
     "One of: ok, code_error, no_forecast, timeout, implausible. Reported as counts "
     "rather than averaged, because a scenario that answers 60% of the time is not "
     "comparable to one that always answers.", "n/a", "runs.csv: outcome"),
    ("Traceability", "Argument-match rate", "%",
     "Share of tool calls in which the arguments the agent chose named the same "
     "series it was asked about. A mismatch corrupts the accuracy figure without "
     "being visible in the answer text.", "higher",
     "raw_responses/*.json: tool_calls"),

    ("Efficiency", "Peak fit RSS", "MB",
     "Peak resident set size of the process during model fitting, sampled at 5 ms "
     "in an isolated subprocess. Captures allocation by native (C++) libraries.",
     "lower", "srq1/profiling.csv"),
    ("Efficiency", "Peak fit tracemalloc", "MB",
     "Peak Python-heap allocation during fitting. Reported beside RSS for "
     "comparison; it does not observe native allocation.", "lower",
     "srq1/profiling.csv"),
    ("Efficiency", "Fit time", "s",
     "Wall-clock seconds to fit one model on the full training window, given "
     "hyperparameters.", "lower", "srq1/profiling.csv: fit_s"),
    ("Efficiency", "Refit time", "s",
     "Wall-clock seconds to re-estimate model coefficients on updated data while "
     "holding stored hyperparameters fixed.", "lower", "srq1/refit_vs_retune.csv"),
    ("Efficiency", "Re-tune time", "s",
     "Wall-clock seconds to re-run the full hyperparameter search, which repeats a "
     "cross-validated fit for every trial.", "lower", "srq1/refit_vs_retune.csv"),
]


def table_metric_dictionary() -> None:
    df = pd.DataFrame(METRICS, columns=[
        "Dimension", "Metric", "Unit", "Definition", "Better when", "Source"])
    _emit("metric_dictionary", "Metric dictionary",
          "Definition, unit, direction of improvement and source field for every "
          "quantity reported in this appendix.", df,
          note="Percentage-valued metrics are given as numbers with the unit in the "
               "column heading (for example a weighted MAPE of 19.4 denotes 19.4%), "
               "following the convention of the M4 and M5 forecasting competitions.")


# ---------------------------------------------------------------------------
# Substrate: cost of fitting, refitting and re-tuning
# ---------------------------------------------------------------------------
def _retune_costs() -> pd.DataFrame | None:
    """Time and memory for refit vs re-tune at one forecast origin."""
    f = THESIS_RESULTS_SRQ1_DIR / "retune_single_cutoff.csv"
    return pd.read_csv(f) if f.is_file() else None


def _op_label(r) -> str:
    if int(r["trials"]) == 0:
        return "Refit on stored hyperparameters"
    return f"Re-tune, {int(r['trials'])} trials x {int(r['folds'])} folds"


def table_resource_profile() -> None:
    """ONE table for the whole resource question.

    This previously stood as three: a per-model profile, a budget share table,
    and a retraining-cost table. They were separated because they answer
    different questions, but they share a single unit system (seconds and
    megabytes against one budget) and a single subject (what the substrate
    costs to run), so a reader comparing "fit" against "refit" against "re-tune"
    had to hold three tables in view at once. Merged, the comparison the
    appendix exists to support is visible in one screenshot.

    What stays separate is the drift table: its unit is percentage points of
    forecast error across forecast origins, not time or memory, and merging
    unlike quantities into one grid would invite comparison down a column where
    none exists."""
    f = THESIS_RESULTS_SRQ1_DIR / "profiling.csv"
    if not f.is_file():
        print("  (skip resource profile: profiling.csv absent)")
        return
    df = pd.read_csv(f)
    models = list(df.model)

    labels = [
        ("fit_s", "Fit time (s)", "{:.3f}", True),
        ("predict_ms", "Prediction time (ms)", "{:.1f}", True),
        ("peak_fit_RSS_MB", "Peak fit memory, RSS (MB)", "{:.1f}", True),
        ("peak_predict_RSS_MB", "Peak prediction memory, RSS (MB)", "{:.2f}", True),
        ("peak_fit_tracemalloc_MB", "Peak fit memory, Python heap (MB)", "{:.1f}", True),
        ("model_size_MB", "Serialised model size (MB)", "{:.2f}", True),
        ("n_train", "Training rows", "{:.0f}", None),
        ("n_features", "Features", "{:.0f}", None),
    ]

    rows, bold_rows = [], []
    for key, label, fmt, lower in labels:
        if key not in df.columns:
            continue
        r = {"Measure": label}
        for _, m in df.iterrows():
            v = m[key]
            r[m["model"]] = "" if pd.isna(v) else fmt.format(v)
        rows.append(r)
        # The Python-heap row is deliberately NOT bolded. It is shown for
        # comparison against RSS, not as a criterion: bolding it would award
        # "best" to the model whose native allocation that instrument fails to
        # observe, which inverts the very point the row exists to make.
        if lower is not None and key != "peak_fit_tracemalloc_MB":
            bold_rows.append(label)

    # Budget share, same unit system, so it belongs in the same grid.
    r = {"Measure": f"Peak fit memory as share of {RAM_BUDGET_MB:.0f} MB budget (%)"}
    for _, m in df.iterrows():
        r[m["model"]] = f"{float(m['peak_fit_RSS_MB']) / RAM_BUDGET_MB * 100:.2f}"
    rows.append(r)
    bold_rows.append(r["Measure"])

    out = pd.DataFrame(rows)
    # Bold the best model per row, but only on rows where "best" is meaningful:
    # training rows and feature count are identical by construction.
    mask = out["Measure"].isin(bold_rows)
    bolded = _bold_best(out[mask].copy(), models, lower_is_better=True)
    out.loc[mask, :] = bolded

    # Retraining costs share the unit system; appended as their own block.
    rt = _retune_costs()
    extra = []
    if rt is not None:
        base_s = float(rt[rt.trials == 0].seconds.iloc[0]) if (rt.trials == 0).any() else None
        for _, r2 in rt.iterrows():
            extra.append({
                "Operation": _op_label(r2),
                "Elapsed time (s)": f"{float(r2['seconds']):,.2f}",
                "Relative to refit": f"{float(r2['ratio_vs_refit']):.0f}x",
                "Peak memory, RSS (MB)": f"{float(r2['peak_rss_mb']):.1f}",
                "Share of budget (%)": f"{float(r2['peak_rss_mb'])/RAM_BUDGET_MB*100:.2f}",
                "Test WMAPE (%)": f"{float(r2['wmape'])*100:.2f}",
            })

    _emit("substrate_resource_profile",
          "Computational cost of the forecasting substrate",
          "Time and memory required to fit, to serve, and to retrain each "
          "candidate model, measured on the largest category (CSD) at "
          "brand-by-month granularity, and expressed against the memory "
          "available in the production deployment environment. Resident set size "
          "is sampled every 5 ms by a monitoring thread, in a separate process "
          "per model. The lowest value in each row is shown in bold italic.", out,
          note="Resident set size and Python-heap allocation are reported side by "
               "side because they measure different quantities. Python-heap "
               "accounting observes only allocations made through the interpreter, "
               "whereas gradient-boosted ensembles are constructed by native "
               "libraries; the serialised model size provides an independent check "
               "on which of the two reflects the memory a deployment must "
               "provision. Fit time is the cost of a single fit given "
               "hyperparameters; the cost of retraining in service is reported "
               "separately below.",
          review="tracemalloc understates XGBoost by ~266x (0.1 vs 29.2 MB). The "
                 "3.7 MB pickle is the third witness -- a 3.7 MB artefact cannot be "
                 "built in 0.1 MB. Keep both rows so the correction stays "
                 "auditable, but RSS is the headline. P0044 F1-F2.\n\n"
                 "MERGED from three tables (profile + budget share + retraining) "
                 "per Brian 2026-09-03: same unit system, same subject, so the "
                 "comparison belongs in one screenshot. Drift stays separate -- "
                 "its unit is pp of error, not time or memory.")

    if extra:
        e = pd.DataFrame(extra)
        e = _bold_best(e, ["Elapsed time (s)"], lower_is_better=True)
        _emit("retraining_cost", "Cost of retraining a model on request",
              "Elapsed time and peak memory for the two ways of bringing a model "
              "up to date at a single forecast origin: refitting coefficients "
              "while holding stored hyperparameters fixed, against repeating the "
              "hyperparameter search at two search budgets. Measured on CSD with "
              "LightGBM.", e,
              note="Refitting re-estimates model coefficients only. Re-tuning "
                   "repeats a cross-validated fit for every trial of the search, "
                   "so its cost is the cost of one fit multiplied by the number of "
                   "trials and the number of folds. This difference in elapsed "
                   "time, rather than any difference in accuracy, is the basis on "
                   "which refitting on request is adopted and re-tuning on request "
                   "is not: memory remains within budget in every case, and the "
                   "accuracy figures fall within the range produced by changing "
                   "only the random seed of the search, so they cannot separate "
                   "the two strategies.",
              review="Do NOT claim re-tuning is less accurate. Optuna seed alone "
                     "moves test WMAPE by 3.97pp, swamping the ~0.3pp between "
                     "strategies (F21). 100 trials = 417.3 s vs 2.93 s = 142x "
                     "(F28). Memory is NOT the constraint -- peak 2.11% of budget. "
                     "The case is elapsed time alone.")


def table_sandbox_profile() -> None:
    """The same fits, measured inside the deployment target rather than locally."""
    f = THESIS_RESULTS_SRQ1_DIR / "sandbox_profiling.csv"
    if not f.is_file():
        print("  (skip sandbox profile: run measure_sandbox_rss.py)")
        return
    df = pd.read_csv(f)
    lim = float(df.container_limit_mb.iloc[0])
    base = float(df.baseline_rss_mb.iloc[0])
    cpus = int(df.cpus.iloc[0])
    models = list(df.model)

    rows = []
    r = {"Measure": "Fit time (s)"}
    for _, m in df.iterrows():
        r[m["model"]] = f"{float(m['fit_s']):.3f}"
    rows.append(r)
    r = {"Measure": "Peak fit memory, RSS (MB)"}
    for _, m in df.iterrows():
        r[m["model"]] = f"{float(m['peak_fit_RSS_MB']):.1f}"
    rows.append(r)
    r = {"Measure": "Share of container limit (%)"}
    for _, m in df.iterrows():
        r[m["model"]] = f"{float(m['pct_of_limit']):.2f}"
    rows.append(r)

    out = _bold_best(pd.DataFrame(rows), models, lower_is_better=True)

    # Environment facts are not per-model, so they go in the caption, not as
    # rows with a repeated value across every column.
    _emit("sandbox_resource_profile",
          "Resource footprint measured inside the deployment environment",
          "Memory required to fit each model within the production sandbox, "
          "measured in the deployment environment itself rather than on a "
          f"development machine. The container reports a memory limit of "
          f"{lim:,.0f} MB and provides {cpus} processor core; the interpreter and "
          f"its libraries occupy {base:,.1f} MB, or {base/lim*100:.2f}% of that "
          "limit, before any model is fitted. The lowest value in each row is "
          "shown in bold italic.", out,
          note="The limit is read from the container at run time, and so "
               "corroborates the provisioned budget independently of the "
               "deployment configuration. Absolute figures are lower than those "
               "measured on the development machine because the container "
               "provides a single processor core, so the tree-based learners "
               "allocate fewer parallel working buffers. That the interpreter and "
               "its libraries occupy more memory than any model fit is the "
               "expected profile for lightweight models, and confirms that the "
               "constraint operates on the choice of model class rather than on "
               "the footprint of the models finally selected.",
          review="MEASURED 2026-09-03, template `prometheus`. Container limit "
                 "4122 MB independently corroborates 4 GB -- cite ALONGSIDE local "
                 "profiling, not instead. cpus=1 explains lower-than-local RSS; "
                 "state the reason or it reads as a contradiction. Closes N6.")


def table_param_drift() -> None:
    """Does freezing hyperparameters cost accuracy as data ages?"""
    f = THESIS_RESULTS_SRQ1_DIR / "refit_vs_retune.csv"
    if not f.is_file():
        print("  (skip parameter drift: refit_vs_retune.csv absent)")
        return
    d = pd.read_csv(f)
    rows = []
    for _, r in d.iterrows():
        rows.append({
            "Forecast origin": str(r["cutoff"])[:10],
            "Training rows": f"{int(r['n_train']):,}",
            "WMAPE, stored parameters (%)": f"{float(r['wmape_refit'])*100:.2f}",
            "WMAPE, re-tuned (%)": f"{float(r['wmape_retune'])*100:.2f}",
            "Difference (pp)": f"{float(r['delta_pp']):+.2f}",
        })
    out = _bold_best(pd.DataFrame(rows),
                     ["WMAPE, stored parameters (%)", "WMAPE, re-tuned (%)"],
                     lower_is_better=True)
    mean_gap = d["delta_pp"].mean()
    _emit("parameter_drift",
          "Effect of holding hyperparameters fixed as data accrues",
          "Forecast error using stored hyperparameters against error after "
          "repeating the hyperparameter search, at successive monthly forecast "
          "origins. A positive difference indicates that the stored parameters "
          "performed worse. The lower error in each row is shown in bold italic.", out,
          note=f"The mean difference across origins is {mean_gap:+.2f} percentage "
               "points, and individual origins fall on both sides of zero. Over "
               "the period observed there is therefore no detectable penalty from "
               "holding hyperparameters fixed. The window is short and the number "
               "of origins small, so this should be read as an absence of evidence "
               "at this horizon rather than as evidence that no drift occurs over "
               "longer ones.",
          review="INCONCLUSIVE -- do not cite the +0.414 pp/month slope. Carried "
                 "by two opposite outliers (month 4: -3.74, month 7: +3.60) on "
                 "n=7, and three months are exactly 0.00 because re-tuning "
                 "rediscovered the frozen num_leaves=93. Recommend refit-per-query "
                 "+ SCHEDULED re-tune, cadence not optimised. F31.\n\n"
                 "Kept SEPARATE from the merged resource table: unit is pp of "
                 "forecast error across origins, not time/memory.")


def table_baselines_wide() -> None:
    """Pivoted: models as columns, one block per metric.

    The long form ran 28 rows and put the models being compared 7 rows apart.
    Comparison is the entire purpose of the table, so the models sit adjacent."""
    f = THESIS_RESULTS_SRQ1_DIR / "stat_baselines.csv"
    if not f.is_file():
        print("  (skip baselines: stat_baselines.csv absent)")
        return
    df = pd.read_csv(f)

    order = ["Naive", "SeasonalNaive", "Drift", "Ridge", "Ridge(unclipped)",
             "ARIMA", "Prophet"]
    models = [m for m in order if m in set(df.model)] + \
             [m for m in sorted(set(df.model)) if m not in order]

    # Canonical category order, matching the data chapter.
    cat_order = ["CSD", "danskvand", "energidrikke", "RTD"]
    cats = [c for c in cat_order if c in set(df.category)] + \
           [c for c in sorted(set(df.category)) if c not in cat_order]

    def _num(v, fmt="{:.1f}"):
        """Format a percentage, never in scientific notation.

        A diverging fit can produce an error of order 1e13. Rendered as
        `2.8e+13` that is unreadable in a printed table and reads as a typo, so
        magnitudes beyond the plausible range are marked as a divergence and
        carry their order of magnitude rather than a spurious decimal."""
        if pd.isna(v):
            return ""
        v = float(v)
        if abs(v) >= 100000:
            return f"diverged (~1e{int(np.floor(np.log10(abs(v))))})"
        if abs(v) >= 1000:
            return f"{v:,.0f}"
        return fmt.format(v)

    blocks = []
    for metric, label, fmt in (("wmape", "Weighted MAPE (%)", "{:.1f}"),
                               ("median_mape", "Median MAPE (%)", "{:.1f}")):
        if metric not in df.columns:
            continue
        p = df.pivot_table(index="category", columns="model", values=metric,
                           aggfunc="first").reindex(index=cats, columns=models)
        p = p.reset_index().rename(columns={"category": "Category"})
        p.insert(0, "Metric", label)
        for m in models:
            if m in p.columns:
                p[m] = p[m].map(lambda v: _num(v, fmt))
        blocks.append(p)

    if not blocks:
        return
    wide = pd.concat(blocks, ignore_index=True)
    # Bold the best model in each row. Ridge(unclipped) is excluded from the
    # comparison: it is a diagnostic variant of Ridge, not a candidate model, so
    # letting it "win" a row would misrepresent what was selected.
    compare = [m for m in models if m != "Ridge(unclipped)"]
    wide = _bold_best(wide, compare, lower_is_better=True)
    n_series = df.groupby("category").n_series.first().to_dict()
    wide["Category"] = wide["Category"].map(
        lambda c: f"{c} (n={n_series.get(c, '?')})")

    _emit("statistical_baselines", "Statistical and linear baselines by category",
          "Forecast error for each baseline model on the held-out test window, by "
          "product category. Weighted MAPE aggregates errors in proportion to "
          "volume; median MAPE reports the typical per-series error. Lower is "
          "better throughout; n denotes the number of series in each category, and the lowest error in each row is shown in bold italic.",
          wide,
          note="Prophet was evaluated on every category and is reported in full. Its "
               "error is high on three of the four because monthly observations do "
               "not support the weekly-seasonality and holiday-window components "
               "that the method is designed around, leaving a piecewise trend and an "
               "annual seasonal term estimated over a short history (Taylor & "
               "Letham, 2018). The unclipped Ridge variant is reported alongside the "
               "clipped one to show the effect of constraining predictions to be "
               "non-negative. On two categories the unconstrained fit diverges to "
               "an error many orders of magnitude beyond the plausible range; those "
               "entries are marked as divergent and given by order of magnitude, "
               "since a decimal figure would imply a precision the result does not "
               "have.",
          review="Prophet's failure is a RESULT, not a gap -- it IS implemented "
                 "(srq1_baselines_stat.py:236). NLM Section J: PRO-04 Contradicted "
                 "(T&L do NOT exclude monthly data), PRO-05 Not Found (they do not "
                 "prove flat forecasts). Only PRO-06 wording is safe. Taylor & "
                 "Letham (2018) is MISSING from the Ch2 reference list.")


def table_stability() -> None:
    f = THESIS_RESULTS_SRQ1_DIR / "stability.csv"
    if not f.is_file():
        print("  (skip stability: stability.csv absent)")
        return
    d = pd.read_csv(f)
    models = sorted(set(d.model))
    cat_order = ["CSD", "danskvand", "energidrikke", "RTD"]
    cats = [c for c in cat_order if c in set(d.category)] + \
           [c for c in sorted(set(d.category)) if c not in cat_order]

    rows = []
    for metric, label, mul, fmt in (
            ("median_cv", "Median coefficient of variation (%)", 100, "{:.2f}"),
            ("wmape_std", "Standard deviation of WMAPE across seeds (pp)", 1, "{:.2f}"),
            ("wmape_mean", "Mean WMAPE across seeds (%)", 1, "{:.2f}")):
        if metric not in d.columns:
            continue
        for c in cats:
            r = {"Measure": label, "Category": c}
            for m in models:
                sub = d[(d.category == c) & (d.model == m)]
                r[m] = fmt.format(float(sub[metric].iloc[0]) * mul) if len(sub) else ""
            rows.append(r)

    out = _bold_best(pd.DataFrame(rows), models, lower_is_better=True)
    n_seeds = int(d.n_seeds.max()) if "n_seeds" in d.columns else None
    _emit("seed_stability", "Sensitivity of the substrate to random seed",
          "Variation in fitted accuracy across repeated fits that differ only in "
          "the random seed supplied to the training procedure"
          + (f", over {n_seeds} seeds per model and category" if n_seeds else "")
          + ". The more stable model in each row is shown in bold italic.", out,
          note="Models with a stochastic fitting procedure, which includes "
               "gradient-boosted trees, can return different parameters from "
               "identical data. Seed sensitivity is therefore measured rather than "
               "assumed, following the stability criterion of Klee and Xia (2025). "
               "The coefficient of variation measures dispersion of the forecasts "
               "themselves; the standard deviation of WMAPE measures how far the "
               "resulting accuracy moves, and is the quantity against which any "
               "difference between models should be judged material.",
          review="THIS IS THE 3.97pp NUMBER'S HOME. wmape_std here is why we must "
                 "not claim re-tuning is less accurate -- seed noise swamps the "
                 "~0.3pp between refit and re-tune. Cross-ref retraining_cost.")


# ---------------------------------------------------------------------------
# Scenario comparison
# ---------------------------------------------------------------------------
def _tar(vals, tol=0.01):
    vals = [v for v in vals if v is not None and not pd.isna(v)]
    if not vals:
        return np.nan
    best = 0
    for a in vals:
        n = sum(1 for b in vals if abs(b - a) <= abs(a) * tol)
        best = max(best, n)
    return best / len(vals)


HDR = {"C_model": "C - dedicated model", "B_data": "B - code execution",
       "A_plain": "A - no firm data"}
CLASSES = ("ok", "code_error", "no_forecast", "timeout", "implausible")
CLASS_LABEL = {"ok": "Usable answer", "code_error": "Execution error",
               "no_forecast": "No forecast returned", "timeout": "Timed out",
               "implausible": "Implausible value"}


def _current_schema() -> str | None:
    """The prompt schema id the harness would use for a run started now."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import prompts as _p
        return _p.schema_id()
    except Exception:
        return None


def _coverage(df: pd.DataFrame) -> str:
    """State what the table covers, so a draft screenshot cannot mislead.

    The live `runs.csv` currently holds only the scenario-A pilot. The one
    earlier run that exercised all three scenarios (2026-08-19) is retained
    under `run_2026-08-19_dkk-confound/` and is deliberately NOT aggregated
    here: its prompt asked "what will X sell" without naming a unit, and every
    scenario-A answer came back in currency rather than units, scoring a ~4500%
    error that measured the prompt rather than the scenario. The prompt was
    corrected; those runs cannot be pooled with runs asked a different
    question."""
    got = len(df)
    want = 15 * 5 * 3
    scen = df.system.nunique()
    if got >= want:
        return ""
    bits = [f"Covers {got} of an intended {want} runs "
            "(15 brands x 5 repeats x 3 scenarios)"]
    if scen < 3:
        bits.append("and one of the three scenarios; the remaining scenarios "
                    "have not yet been run at the corrected prompt")
    return " ".join(bits) + "."


def table_scenarios(df: pd.DataFrame) -> None:
    """Pivoted: metrics as rows, scenarios as columns."""
    present = [s for s in ("A_plain", "B_data", "C_model") if s in set(df.system)]
    present += [s for s in df.system.unique() if s not in present]

    stats = {}
    for s in present:
        d = df[df.system == s]
        ok = d[d.outcome == "ok"]
        cv = ok.groupby("brand").forecast.apply(
            lambda x: x.std() / x.mean() if len(x) > 1 and x.mean() else np.nan)
        rep = ok.groupby("brand").forecast.apply(
            lambda x: (x.max() - x.min()) / max(x.mean(), 1e-9) < 0.01)
        tar = ok.groupby("brand").forecast.apply(lambda x: _tar(list(x)))
        stats[s] = {
            "Runs completed": f"{len(d):.0f}",
            "Usable answers": f"{len(ok):.0f}",
            "Median APE (%)": f"{ok.ape.median():.1f}" if len(ok) else "",
            "Mean APE (%)": f"{ok.ape.mean():.1f}" if len(ok) else "",
            "Consistency, CV across repeats (%)": f"{cv.mean()*100:.1f}" if len(cv) else "",
            "Replicability, identical answers (%)": f"{rep.mean()*100:.0f}" if len(rep) else "",
            "Top-answer agreement rate": f"{tar.mean():.2f}" if len(tar) else "",
            "Tokens per answer": f"{d.tokens.mean():,.0f}",
            "of which reasoning tokens": f"{d.tokens_reasoning.mean():,.0f}",
            "Cost per answer, estimated (USD)": f"${d.cost_usd_est.mean():.4f}",
            "Response time (s)": f"{d.latency_s.mean():.1f}",
        }
    rows = [{"Measure": k, **{HDR.get(s, s): stats[s][k] for s in present}}
            for k in next(iter(stats.values()))]

    note = ("The scenarios form an information ladder: A has no access to firm data, "
            "B may execute code against it, and C additionally calls the dedicated "
            "forecasting model. Correctness, consistency and replicability are the "
            "primary dimensions; cost and response time are secondary. The "
            "top-answer agreement rate is the share of repeated runs returning the "
            "most common answer within a 1% tolerance, where 1.00 denotes complete "
            "agreement across repeats.")
    cov = _coverage(df)
    _emit("scenario_comparison", "Comparison of decision-support scenarios",
          "Performance of each scenario across the five evaluation dimensions. "
          + (cov + " " if cov else ""), pd.DataFrame(rows),
          note=note,
          review="'TAR@N' was jargon -- renamed 'top-answer agreement rate' and "
                 "defined inline + in the dictionary. Cite Atil et al. (2025).")

    tax = [{"Outcome": CLASS_LABEL[c],
            **{HDR.get(s, s): (lambda d: f"{int((d.outcome==c).sum())} "
                               f"({int((d.outcome==c).sum())/max(len(d),1)*100:.0f}%)")(
                df[df.system == s]) for s in present}}
           for c in CLASSES]
    _emit("outcome_taxonomy", "Distribution of run outcomes by scenario",
          "Counts and percentages of runs falling into each outcome class.",
          pd.DataFrame(tax),
          note="Failures are reported as classes rather than averaged into the "
               "accuracy figures. A scenario that returns a usable answer in a "
               "fraction of runs is not directly comparable to one that always "
               "answers, and a single implausible value distorts a mean without "
               "bound; classifying such runs preserves both facts.")


def table_interval_comm() -> None:
    """Whether the agent communicated uncertainty, not just whether it was right."""
    f = THESIS_RESULTS_SRQ4_DIR / "interval_communication.csv"
    if not f.is_file():
        print("  (skip interval communication: run "
              "score_interval_communication.py)")
        return
    d = pd.read_csv(f)
    crit = [("states_interval", "States a range"),
            ("interval_faithful", "Range matches the tool output"),
            ("states_confidence", "States confidence")]
    scen = sorted(d.scenario.unique())

    # n goes in the column header, so every percentage in the column carries its
    # own denominator and no cell can be read without it.
    hdr = {s_: f"{s_} (n={len(d[d.scenario == s_])})" for s_ in scen}

    rows = []
    for key, label in crit:
        if key not in d.columns:
            continue
        r = {"Criterion": label}
        for s_ in scen:
            sub = d[d.scenario == s_]
            r[hdr[s_]] = f"{sub[key].sum():.0f} of {len(sub)} ({sub[key].mean()*100:.0f})" \
                if len(sub) else ""
        rows.append(r)
    r = {"Criterion": "Mean criteria met (of 3)"}
    for s_ in scen:
        sub = d[d.scenario == s_]
        r[hdr[s_]] = f"{sub[[c for c, _ in crit]].sum(axis=1).mean():.2f}" if len(sub) else ""
    rows.append(r)

    _emit("interval_communication",
          "Communication of forecast uncertainty by scenario",
          "Number of answers satisfying each criterion for conveying "
          "uncertainty, with the percentage in parentheses, scored against the "
          "payload the forecasting tool returned. n denotes the number of "
          "answers scored in each scenario.",
          pd.DataFrame(rows),
          note="Goodwin, Onkal and Thomson (2010) find that a prediction interval "
               "presented as a bare numeric range does not improve decisions and "
               "can degrade them, because the step from interval to decision is "
               "left to the reader. These criteria record whether that step was "
               "supplied: whether a range was stated, whether it corresponds to "
               "the one the model produced, and whether the associated confidence "
               "was reported. Each is evaluated by direct comparison of the "
               "numbers in the answer against the numbers the tool returned, "
               "with a five per cent tolerance; no judgement is involved. A "
               "scenario with no access to the forecasting tool cannot satisfy "
               "the second criterion, which requires a retrieved source against "
               "which a stated range can be checked. These measures concern what "
               "the system communicated. Whether such communication improves the "
               "decisions of human planners is not examined in this thesis and "
               "would require a controlled decision experiment with human "
               "participants.",
          review="Closes the Ch2 sec 2.3 / SRQ4 gap (N9/N10 Option 2). Scored "
                 "retrospectively from already-logged runs -- NO new API spend. "
                 "All checks deterministic (regex + numeric comparison vs the "
                 "tool payload), no judge, consistent with N5b.\n\n"
                 "DROPPED the 'gives a recommendation' criterion: the shared "
                 "prompt asks for 'the number, a range, and how confident you "
                 "are' and never asks for a recommendation, so scoring it "
                 "measured compliance with an instruction never given. The 33% "
                 "figure from the first pilot must NOT be cited. If we want it, "
                 "the prompt has to ask for it -- and that changes the "
                 "single-variable design, so it is a deliberate decision, not a "
                 "scorer tweak.\n\n"
                 "Do NOT claim improved human decisions; needs Goodwin's design "
                 "+ ethics approval (cf. MR-10).")


def table_per_run(df: pd.DataFrame) -> None:
    cols = ["category", "brand", "system", "rep", "actual", "forecast", "ape",
            "outcome", "latency_s", "tokens_in", "tokens_out", "tokens_reasoning",
            "cost_usd_est"]
    d = df[[c for c in cols if c in df.columns]].copy()
    d["system"] = d.system.map(lambda s: HDR.get(s, s))
    disp = _fmt(d, {"actual": "{:,.0f}", "forecast": "{:,.0f}", "ape": "{:.1f}",
                    "latency_s": "{:.1f}", "cost_usd_est": "${:.4f}"}).rename(columns={
        "category": "Category", "brand": "Brand", "system": "Scenario", "rep": "Repeat",
        "actual": "Actual (units)", "forecast": "Forecast (units)", "ape": "APE (%)",
        "outcome": "Outcome", "latency_s": "Response time (s)",
        "tokens_in": "Tokens in", "tokens_out": "Tokens out",
        "tokens_reasoning": "Reasoning tokens", "cost_usd_est": "Cost (USD)"})
    cov = _coverage(df)
    _emit("per_run_record", "Complete record of individual runs",
          "Every run logged, with its forecast, error, outcome class, response time "
          "and cost. This is the evidence base from which the aggregate figures are "
          "computed. " + cov, disp,
          note="The full response for each run, including any code generated and "
               "the reasoning summary returned by the model, is retained alongside "
               "these records.",
          review=(f"Currently {len(df)} rows because only a scenario-A pilot has run "
                  "(CSD, 2 brands, 3 reps). Intended full size is 225 rows: 15 "
                  "brands x 5 repeats x 3 scenarios. Blocked on API credit (P0042 "
                  "blocks 1-3, ~$40). NOT the final length."))


def table_traceability(df: pd.DataFrame) -> None:
    rows = []
    for f in sorted((THESIS_RESULTS_SRQ4_DIR / "raw_responses").glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        tr = d.get("trace") or {}
        for tc in (d.get("tool_calls") or []):
            out = tc.get("tool_output") or {}
            iv = out.get("interval_90") or [None, None]
            rows.append({
                "Run": f.stem,
                "Series requested": f"{tc.get('requested_category')} / {tc.get('requested_brand')}",
                "Series queried by agent": f"{tc.get('llm_arg_category')} / {tc.get('llm_arg_brand')}",
                "Match": "yes" if tc.get("args_match_request") else "NO",
                "Forecast returned (units)": out.get("forecast_units"),
                "90% interval": (f"{iv[0]:,.0f} - {iv[1]:,.0f}"
                                 if iv and iv[0] is not None else ""),
                "Confidence": out.get("confidence"),
                "Timestamp": tr.get("run_at")})
    if not rows:
        print("  (skip traceability: no dedicated-model tool calls logged yet)")
        return
    disp = _fmt(pd.DataFrame(rows), {"Forecast returned (units)": "{:,.0f}",
                                     "Confidence": "{:.1f}"})
    _emit("traceability_record", "Traceability record for forecasting tool calls",
          "For every call the agent made to the dedicated forecasting model: the "
          "series it was asked about, the series its arguments actually named, "
          "whether these matched, and the forecast, interval and confidence "
          "returned.", disp,
          note="Recording the arguments the agent selected, rather than only the "
               "answer it produced, makes it possible to detect a call directed at "
               "the wrong series. Such a call yields a well-formed answer about "
               "different data and is not otherwise visible in the output.")


def table_config(df: pd.DataFrame) -> None:
    tr = {}
    for v in df.get("trace", pd.Series(dtype=str)).dropna().head(50):
        try:
            tr = json.loads(v)
            break
        except Exception:
            continue
    rows = [("Language model", tr.get("model", "n/a")),
            ("Reasoning effort", tr.get("reasoning_effort", "n/a")),
            ("Temperature", str(tr.get("temperature", "n/a"))),
            ("Decoding", tr.get("decoding", "n/a")),
            ("Categories evaluated", ", ".join(sorted(df.category.dropna().unique()))),
            ("Distinct brands", str(df.brand.nunique())),
            ("Repeats per brand", str(int(df.rep.max()) + 1 if len(df) else 0)),
            ("Total runs", str(len(df))),
            ("First run timestamp", str(tr.get("run_at", "n/a")))]
    _emit("run_configuration", "Experimental configuration",
          "The parameters under which the scenario comparison was run. Each is "
          "recorded with every individual run, so any result can be tied to the "
          "configuration that produced it.",
          pd.DataFrame(rows, columns=["Parameter", "Value"]),
          note="Temperature and nucleus-sampling parameters are not supported by "
               "the model used; this is recorded explicitly rather than implying a "
               "setting that was never applied.")


# ---------------------------------------------------------------------------
def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Writing appendix tables to {OUT}\n")

    table_metric_dictionary()
    table_resource_profile()
    table_sandbox_profile()
    table_param_drift()
    table_baselines_wide()
    table_stability()

    runs = THESIS_RESULTS_SRQ4_DIR / "runs.csv"
    if runs.is_file():
        df = pd.read_csv(runs)
        # Report only the current prompt schema. Answers to different questions
        # cannot be pooled, and an appendix that silently mixed them would
        # aggregate incomparable runs into one figure. Superseded rows stay on
        # disk for the record; they are simply not reported as results.
        if "schema" in df.columns and len(df):
            cur = _current_schema()
            if cur and (df.schema == cur).any():
                dropped = int((df.schema != cur).sum())
                df = df[df.schema == cur]
                if dropped:
                    print(f"  ({dropped} row(s) at a superseded prompt schema "
                          "excluded from the scenario tables)")
            else:
                print(f"  (WARNING: no rows at the current prompt schema "
                      f"{cur}; reporting {sorted(set(df.schema))} instead -- "
                      "these predate the current question)")
        table_scenarios(df)
        table_interval_comm()
        table_per_run(df)
        table_traceability(df)
        table_config(df)
    else:
        print("  (skip scenario tables: srq4/runs.csv absent -- run the experiment first)")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    idx = ["# Appendix tables", "",
           f"Generated by `03_thesis_modelling/scenario_setup/export_appendix.py`, {stamp}.",
           "",
           "Do not edit these files by hand -- re-run the exporter. Each table is "
           "written as `.md` (to paste or screenshot) and `.csv` (to trace a figure "
           "back to source).", "",
           "**Tables are deliberately unnumbered.** Insert them in Word and let its "
           "caption/cross-reference fields do the numbering, so that dropping a "
           "table from the appendix renumbers the rest automatically.", "",
           "Each table's own `.md` carries its internal review notes **below a "
           "horizontal rule**, under an `INTERNAL REVIEW` marker. Everything above "
           "that rule is submission-ready; a screenshot cropped to the table and "
           "its note cannot capture what sits below it. Keep the notes there: they "
           "belong beside the table they describe.", "",
           "**Filenames are numbered, table content is not.** The `NN_` prefix "
           "gives the directory a stable generation order for our own review; the "
           "document itself carries no table number, so Word's caption fields stay "
           "authoritative.", "",
           "| # | Table | File |", "|---|---|---|"]
    for i, (title, stem) in enumerate(_INDEX, 1):
        idx.append(f"| {i} | {title} | `{stem}.md` / `{stem}.csv` |")
    (OUT / "README.md").write_text("\n".join(idx) + "\n",
                                   encoding="utf-8", newline="\n")

    print(f"\n{len(_INDEX)} tables written.")
    print(f"  index: {OUT / 'README.md'}")
    print("  each table .md carries its review notes below a horizontal rule.")


if __name__ == "__main__":
    main()
