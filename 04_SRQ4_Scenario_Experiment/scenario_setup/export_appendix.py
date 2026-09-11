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
    python 04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py

Output: 04_thesis_results/appendix/
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

def _find_repo_root() -> Path:
    """Walk up from this file to the repo root (anchored on .env.example).

    Replaces a hard-coded parents[N] hop, which silently points at the wrong
    directory whenever a script moves between folder depths -- as happened in
    the 2026-09-06 restructure.
    """
    _start = Path(__file__).resolve().parent
    for _cand in (_start, *_start.parents):
        if any((_cand / _a).exists() for _a in (".env.example", ".env", "PATHS.py")):
            return _cand
    raise FileNotFoundError(f"Could not find project root above {_start}")


sys.path.insert(0, str(_find_repo_root()))
from PATHS import (ROOT_DIR, THESIS_RESULTS_DIR, THESIS_RESULTS_SRQ1_DIR,  # noqa: E402
                   THESIS_RESULTS_SRQ4_DIR, CHAPTER_SLUGS,
                   get_category_pipeline_step_outputs_dir,
                   get_category_engineered_bymonth_dir,
                   get_chapter_tables_dir)
sys.path.insert(0, str(_find_repo_root() / "05_thesis_results"))
from review_notes import write_review_note, clear_review_notes  # noqa: E402
from check_reader_facing import warn_after_run  # noqa: E402

# No single OUT any more: tables are written to the chapter that discusses them
# (see _TABLE_CHAPTER below). THESIS_RESULTS_DIR is still imported because the
# run index is written once, at the top of the results tree.

# Measured allocation of Manifold's production E2B template (alias `prometheus`),
# not a literature estimate. See P0044 findings.
RAM_BUDGET_MB = 4096.0


# ---------------------------------------------------------------------------
# Emit helpers
# ---------------------------------------------------------------------------
_INDEX: list[tuple[str, str]] = []
_SEQ = [0]

# Review notes are written BESIDE the table, not INSIDE it -- one .md per table
# in the writing-notes folder of the CHAPTER that discusses the table.
#
# They used to sit below an `<!-- INTERNAL REVIEW -->` marker in the table file
# itself, on the reasoning that a note belongs at the table it describes and a
# screenshot cropped to the table cannot capture what is below a rule. That
# covers screenshots and misses the repository: 05_thesis_results/ ships to
# assessors, so every internal note in it travelled with the thesis. The split
# is now by file, and 06_thesis_writing/ is removed by the submission export.
_PRODUCER = "04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py"


def _write_review_note(slug: str, stem: str, title: str, review: str) -> None:
    write_review_note(slug, _chapter_dir(slug) / f"{stem}.md", title,
                      review, _PRODUCER)


# This script is a CROSS-CUTTING exporter, not a scenario script. It lives with
# the SRQ4 harness for historical reasons, but only 5 of its 15 tables concern
# the scenario experiment -- the rest describe the pipeline, the substrate and
# its cost. Filing them all under SRQ4 put pipeline-execution figures in
# "scenario experiments", so each table now names the chapter that discusses it.
_TABLE_CHAPTER: dict = {
    # Ch4 -- how the data set was built
    "pipeline_execution": "data_assessment",
    "pipeline_data_reduction": "data_assessment",
    "feature_matrix": "data_assessment",
    # Ch5 -- the models, their cost and their stability
    "metric_dictionary": "model_benchmark",
    "statistical_baselines": "model_benchmark",
    "seed_stability": "model_benchmark",
    "parameter_drift": "model_benchmark",
    "substrate_resource_profile": "model_benchmark",
    "retraining_cost": "model_benchmark",
    # Ch7 -- the tool interface in use
    "interval_communication": "decision_synthesis",
    "traceability_record": "decision_synthesis",
    # Ch8 -- the scenario comparison itself
    "scenario_comparison": "experimental_evaluation",
    "outcome_taxonomy": "experimental_evaluation",
    "per_run_record": "experimental_evaluation",
    "run_configuration": "experimental_evaluation",
    "sandbox_resource_profile": "experimental_evaluation",
}


def _chapter_dir(slug: str) -> Path:
    """Where one table belongs. An unmapped slug raises rather than defaulting.

    A default would file a new table in whichever chapter was convenient and let
    it sit there unnoticed; failing loudly costs one line in the map above.
    """
    if slug not in _TABLE_CHAPTER:
        raise KeyError(
            f"table {slug!r} has no chapter in _TABLE_CHAPTER -- add one. "
            f"Known: {sorted(_TABLE_CHAPTER)}")
    return get_chapter_tables_dir(_TABLE_CHAPTER[slug])


def _emit(slug: str, title: str, caption: str, df: pd.DataFrame,
          note: str = "", review: str = "") -> None:
    """Write one table as .md (paste/screenshot) and .csv (trace a number back).

    The FILENAME carries a sequence number so the directory sorts in generation
    order for our own review. The file CONTENT carries none: numbering inside
    the document is Word's job, and a hard-coded number goes stale the moment a
    table is dropped from the appendix."""
    out = _chapter_dir(slug)
    out.mkdir(parents=True, exist_ok=True)
    _SEQ[0] += 1
    stem = f"{_SEQ[0]:02d}_{slug}"
    df.to_csv(out / f"{stem}.csv", index=False, encoding="utf-8")

    lines = [f"**{title}.** {caption}", "", df.to_markdown(index=False)]
    if note:
        lines += ["", f"*Note.* {note}"]
    (out / f"{stem}.md").write_text("\n".join(lines) + "\n",
                                    encoding="utf-8", newline="\n")

    _write_review_note(slug, stem, title, review)
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
    f = THESIS_RESULTS_SRQ1_DIR / "tables" / "retune_single_cutoff.csv"
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
    f = THESIS_RESULTS_SRQ1_DIR / "tables" / "profiling.csv"
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
          review="tracemalloc materially understates the native-library models: "
                 "the serialised model size is the independent witness that RSS, "
                 "not the Python-heap figure, is what a deployment must provision "
                 "(P0044 F1-F2). Keep both rows so the correction stays auditable, "
                 "but RSS is the headline. All three figures are in the table -- "
                 "do not restate them here.\n\n"
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
                     "moves test WMAPE by more than the gap between the two "
                     "strategies (F21), and the accuracy figures sit inside the "
                     "seed-variance band. The case for refit-not-retune is elapsed "
                     "time alone: re-tuning multiplies one fit by trials and folds "
                     "(F28), while peak memory stays a small fraction of budget in "
                     "every row above. The time and memory numbers are in the "
                     "table -- do not restate them here.")


def table_sandbox_profile() -> None:
    """The same fits, measured inside the deployment target rather than locally."""
    f = THESIS_RESULTS_SRQ1_DIR / "tables" / "sandbox_profiling.csv"
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
    f = THESIS_RESULTS_SRQ1_DIR / "tables" / "refit_vs_retune.csv"
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
          review="INCONCLUSIVE -- do not fit or cite a per-month drift slope. The "
                 "origins fall on both sides of zero, the window is a handful of "
                 "months, and some origins are exactly zero because re-tuning "
                 "rediscovered the frozen parameters. Recommend refit-per-query "
                 "+ SCHEDULED re-tune, cadence not optimised. F31. The per-origin "
                 "differences are in the table; the mean is in the note.\n\n"
                 "Kept SEPARATE from the merged resource table: unit is pp of "
                 "forecast error across origins, not time/memory.")


def table_baselines_wide() -> None:
    """Pivoted: models as columns, one block per metric.

    The long form ran 28 rows and put the models being compared 7 rows apart.
    Comparison is the entire purpose of the table, so the models sit adjacent."""
    f = THESIS_RESULTS_SRQ1_DIR / "tables" / "stat_baselines.csv"
    if not f.is_file():
        print("  (skip baselines: stat_baselines.csv absent)")
        return
    df = pd.read_csv(f)

    order = ["Naive", "SeasonalNaive", "Drift", "Ridge", "Ridge(unclipped)",
             "ARIMA", "Prophet"]
    models = [m for m in order if m in set(df.model)] + \
             [m for m in sorted(set(df.model)) if m not in order]

    # Canonical category order, matching the data chapter.
    cat_order = ["CSD", "Danskvand", "Energidrikke", "RTD"]
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


def table_pipeline_execution() -> None:
    """Which preprocessing steps ran, for which category and horizon, and how long.

    Reads the `run_manifest.json` written by `run_preprocessing.py`. Before that
    manifest existed the run record lived only as prose inside a console log, so
    "did every step pass for every category?" could not be answered without a
    human reading four log files (P0046 F20).

    This is a REPRODUCIBILITY table, not a performance claim. Wall-clock seconds
    on one laptop are not a benchmark: they are evidence that the stated pipeline
    is the pipeline that ran, and that no step was quietly skipped. The step names
    come from the manifest rather than from a list held here, so a renamed or
    reordered step cannot leave this table describing a pipeline that no longer
    exists.
    """
    manifests = []
    for cat in ("CSD", "Danskvand", "Energidrikke", "RTD"):
        f = get_category_pipeline_step_outputs_dir(cat) / "run_manifest.json"
        if f.is_file():
            try:
                manifests.append(json.loads(f.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, OSError) as exc:
                print(f"  (skip {cat} manifest, unreadable: {exc})")

    if not manifests:
        print("  (skip pipeline execution: no run_manifest.json found -- "
              "re-run run_preprocessing.py to produce one)")
        return

    # Step identity comes from the manifest, so this cannot drift from PIPELINE.
    step_names: dict[int, str] = {}
    for m in manifests:
        for run in m.get("runs", []):
            for st in run.get("steps", []):
                step_names.setdefault(st["step"], st.get("name", ""))

    rows, skipped, failed = [], 0, 0
    for m in manifests:
        for run in sorted(m.get("runs", []), key=lambda r: r.get("horizon", 0)):
            by_step = {st["step"]: st for st in run.get("steps", [])}
            row = {"Category": m.get("category", "?"),
                   "Horizon (months)": run.get("horizon", "")}
            for num in sorted(step_names):
                st = by_step.get(num)
                if st is None:
                    row[f"Step {num}"] = "--"        # not part of this run
                elif st["status"] == "ok":
                    row[f"Step {num}"] = f"{st['seconds']:.1f}"
                else:
                    row[f"Step {num}"] = st["status"]
                    skipped += st["status"] == "skipped"
                    failed += st["status"] == "failed"
            row["Total (s)"] = f"{run.get('total_seconds', 0):.1f}"
            row["All steps passed"] = "yes" if run.get("ok") else "no"
            rows.append(row)

    df = pd.DataFrame(rows)
    legend = "; ".join(f"step {n} — {step_names[n]}" for n in sorted(step_names))
    stamps = sorted({m.get("written_at_utc", "")[:10] for m in manifests if m.get("written_at_utc")})
    when = stamps[0] if len(stamps) == 1 else f"{stamps[0]} to {stamps[-1]}"

    note = (f"Cell values are elapsed seconds for that step. {legend}. "
            "An em dash marks a step outside the range of that run; "
            "\"skipped\" marks a horizon-independent step deliberately not "
            "repeated on a second horizon (steps 0-2 build the same panel "
            "regardless of horizon).")
    if failed:
        note += (f" {failed} step(s) recorded a failure and are named in the "
                 "corresponding manifest.")

    _emit("pipeline_execution",
          "Preprocessing pipeline execution by category and horizon",
          "Execution record of the Nielsen preprocessing pipeline, taken from "
          "the run manifest each run writes. Timings are wall-clock on the "
          "development machine and are reported to evidence that every step "
          "ran, not as a performance benchmark.", df,
          note=note,
          review=f"Generated from run_manifest.json across {len(manifests)} of 4 "
                 f"categories ({len(df)} runs), written {when}. Regenerate by "
                 "re-running run_preprocessing.py; the manifest merges horizons "
                 "rather than overwriting, so H=1 and H=3 accumulate. A category "
                 "absent here has simply not been re-run since the manifest was "
                 "added (P0046 F20) -- it is not evidence of a failure."
                 + (f" {skipped} skipped step(s) present." if skipped else ""))


def table_pipeline_data_reduction() -> None:
    """How the panel narrows from raw aggregation to modelling matrix.

    The companion to `table_pipeline_execution`, deliberately kept SEPARATE
    rather than adding columns to it: that table's unit is seconds, this one's is
    rows and brands. Mixing them would put two incompatible units in one row and
    invite a reader to compare down a column of unlike quantities.

    This is the table that answers "what was excluded, and where". A pipeline
    that silently drops 80% of its brands at step 3 and one that keeps them all
    look identical in a timing log; they differ here.
    """
    # Read step 4's OWN log, not the run manifest's summary. Step 4 records the
    # full reduction chain (rows_in -> rows_calendar -> rows_filtered -> rows_out
    # with brand counts at each stage); the manifest only carries the endpoints,
    # which would hide the calendar-fill stage that explains why the matrix has
    # MORE rows than the panel it came from.
    rows = []
    for cat in ("CSD", "Danskvand", "Energidrikke", "RTD"):
        d = get_category_pipeline_step_outputs_dir(cat)
        for log in sorted(d.glob("step_4_log_h*.json")):
            try:
                s = json.loads(log.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            r = s.get("result", {})
            if not r:
                continue
            rows.append({
                "Category": s.get("category", cat),
                "Horizon (months)": s.get("forecast_horizon", ""),
                "Panel rows": r.get("rows_in"),
                "Panel brands": r.get("brands_in"),
                "After calendar fill": r.get("rows_calendar"),
                "Matrix rows": r.get("rows_out"),
                "Matrix brands": r.get("brands_out"),
                "Matrix columns": r.get("cols_out"),
            })

    if not rows:
        print("  (skip data reduction: no step_4_log_h*.json found -- "
              "re-run run_preprocessing.py)")
        return
    rows.sort(key=lambda x: (x["Category"], x["Horizon (months)"]))

    df = pd.DataFrame(rows)
    # Drop columns no manifest populated, rather than printing a column of blanks.
    df = df.dropna(axis=1, how="all")
    for c in df.columns:
        if c not in ("Category", "Horizon (months)"):
            df[c] = df[c].map(lambda v: "" if pd.isna(v) else f"{int(v):,}")

    _emit("pipeline_data_reduction",
          "Panel size through the preprocessing pipeline",
          "Rows and brands at each stage of matrix construction, per category "
          "and horizon. The panel is aggregated at step 1; step 4 then completes "
          "each brand's month grid and applies the contract measured at step 3, "
          "producing the modelling matrix.", df,
          note="Matrix rows EXCEED panel rows while brand counts fall. Both "
               "follow from step 4: each retained brand's month grid is "
               "completed before features are built, so that a lag refers to "
               "the previous month rather than to the previous observed row, "
               "which adds rows; and brands whose series is too short to satisfy "
               "the contract's minimum-periods requirement are excluded, which "
               "removes them. Exclusion is by the measured contract, not by "
               "manual selection.",
          review="Read from step_4_log_h{N}.json, which step 4 writes itself -- "
                 "NOT from the run manifest, whose summary carries only the "
                 "endpoints and would hide the calendar-fill stage. Values are "
                 "the ones the step computed, so this cannot drift from the "
                 "pipeline (P0046 F25).\n\n"
                 "** DO NOT PUBLISH THE HORIZON COLUMN AS-IS.** P0048 F1 / P0049 "
                 "F22: engineer_features() takes no horizon argument, so the h1 "
                 "and h3 matrices encode the SAME one-month prediction task and "
                 "differ only in their split dates. The row counts below are "
                 "real, but labelling one of them '3' asserts a horizon the "
                 "feature construction never applied. Re-run this table after "
                 "the horizon fix lands.")


def table_stability() -> None:
    f = THESIS_RESULTS_SRQ1_DIR / "tables" / "stability.csv"
    if not f.is_file():
        print("  (skip stability: stability.csv absent)")
        return
    d = pd.read_csv(f)
    models = sorted(set(d.model))
    cat_order = ["CSD", "Danskvand", "Energidrikke", "RTD"]
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
          review="The WMAPE-sd column here is the seed-noise magnitude that the "
                 "retraining_cost table's caveat rests on: it is larger than the "
                 "refit-vs-retune accuracy gap, which is why that gap cannot be "
                 "called material. Cross-ref retraining_cost. Read the number off "
                 "this table, do not transcribe it into prose.")


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


# Retired 2026-09-11 with the arm rename. The key IS the label now, so a
# reader of the appendix and a reader of runs.csv see the same seven strings.
# Kept as a comment because the descriptive glosses are still the right words
# for PROSE -- they just must not be a second naming system in generated output.
#   A_llm_plain  no firm data          D_prometheus_data        B on Prometheus
#   B_llm_data   code execution        E_prometheus_model       C on Prometheus
#   C_llm_model  dedicated model       G_prometheus_data_model  F on Prometheus
#   F_llm_data_model  data + model + code
HDR = {}
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
    present = [s for s in ("A_llm_plain", "B_llm_data", "C_llm_model") if s in set(df.system)]
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
def _clear_previous() -> int:
    """Delete this exporter's own previously-written tables before regenerating.

    The `NN_` prefix is a GENERATION-ORDER number, not a stable identity: if one
    table's input is missing, every later table shifts up. Writing without
    clearing therefore leaves the previous run's files behind under their old
    numbers, and a prefix stops identifying a table -- observed 2026-09-07, when
    three different tables were all called `02_` (P0046 F23).

    Matched by SLUG, not by prefix range. The old scheme reserved numeric blocks
    per producer (01-49 here, 89 the literature table, 90-99 the holiday and
    enrichment exporters) because every producer wrote into one flat appendix
    directory, and a whole-directory wipe would have destroyed output this
    script cannot regenerate. That was fragile in both directions: the bound was
    once set to 89 and silently deleted the literature table, and a new producer
    picking an unclaimed number was a matter of remembering to look.

    Under DEC-CHAPTER-FOLDERS each table is written to its chapter, and this
    removes exactly the files it is about to rewrite -- `NN_<slug>.md|csv` for
    slugs in `_TABLE_CHAPTER`. It cannot reach another producer's output even if
    they share a directory, so no block allocation needs maintaining.
    """
    removed = 0
    for slug, chapter in _TABLE_CHAPTER.items():
        for f in get_chapter_tables_dir(chapter).glob(f"[0-9][0-9]_{slug}.*"):
            if f.suffix not in (".md", ".csv"):
                continue
            try:
                f.unlink()
                removed += 1
            except OSError:
                continue
    # The sidecar review notes are this exporter's output too, so they are
    # cleared on the same terms -- by slug, never by directory.
    removed += clear_review_notes(_TABLE_CHAPTER)
    return removed


# Role of every column in the modelling matrix. The manifest's `features` list
# is authoritative for WHICH columns are model inputs; this only names the role
# of each, and the roles are assigned by rule below rather than listed by hand.
_FM_CATEGORY = "CSD"
_FM_HORIZON = 3


def _fm_role(col: str, features: set) -> str:
    """The role a matrix column plays, derived from its name and the manifest.

    Every column must match a rule. `table_feature_matrix` asserts that none
    falls through, so a column added upstream fails loudly here rather than
    being silently filed as "other" in a table an assessor reads.
    """
    if col in ("date", "brand"):
        return "Identifier"
    if col == "sales_units":
        return "Target"
    if col == "log_sales_units":
        return "Target, transformed"
    if col == "split":
        return "Split label"
    if col == "period_index":
        return "Ordering"
    if col in ("period_year", "period_month"):
        return "Raw date part, superseded"
    if col in features:
        if col.startswith(("lag_", "rolling_")):
            return "Feature - autoregressive"
        if col in ("month", "quarter", "peak_month", "days_in_month",
                   "n_holidays", "non_holiday_days"):
            return "Feature - calendar"
        if col.startswith("zero_run"):
            return "Feature - series quality"
        if ("promo" in col or "tpr" in col or "disp" in col
                or "feat" in col):
            return "Feature - promotional"
        if ("distribution" in col or "dist" in col or "stores" in col
                or "items" in col):
            return "Feature - distribution"
        return ""                       # caught by the assert in the caller
    return "Excluded - contemporaneous"


def table_feature_matrix() -> None:
    """What the modelling matrix actually contains, column by column.

    Reads the matrix and its manifest rather than describing them: the feature
    count in particular has been wrong in the prose more than once (13, then 14,
    then 16, now 34 after the holiday enrichment), because it was written down
    instead of counted.

    The important content is not the feature list -- it is the EXCLUDED block.
    Fourteen contemporaneous sales and baseline columns are carried in the
    matrix for traceability and are not model inputs; a reader who assumes every
    column is a feature would conclude the model sees same-period sales, which
    would make the whole benchmark meaningless.
    """
    d = get_category_engineered_bymonth_dir(_FM_CATEGORY)
    slug = _FM_CATEGORY.lower()
    mf = d / f"{slug}_manifest_h{_FM_HORIZON}.json"
    pq = d / f"{slug}_feature_matrix_h{_FM_HORIZON}.parquet"
    if not (mf.is_file() and pq.is_file()):
        print(f"  (skip feature matrix: {_FM_CATEGORY} h{_FM_HORIZON} absent)")
        return

    man = json.loads(mf.read_text(encoding="utf-8"))
    df = pd.read_parquet(pq)
    features = set(man["features"])

    rows = []
    for c in df.columns:
        role = _fm_role(c, features)
        assert role, (f"column {c!r} matched no role rule -- add one rather "
                      f"than letting it fall through into the appendix")
        nn = df[c].notna().sum()
        rows.append({"Column": c, "Role": role,
                     "Type": str(df[c].dtype),
                     "Populated": f"{nn / len(df) * 100:.0f}%"})
    out = pd.DataFrame(rows)

    # Order by role so the table reads as a grouping, with features together.
    order = ["Identifier", "Target", "Target, transformed", "Split label",
             "Ordering", "Feature - autoregressive", "Feature - calendar",
             "Feature - distribution", "Feature - promotional",
             "Feature - series quality", "Raw date part, superseded",
             "Excluded - contemporaneous"]
    out["_k"] = out.Role.map({r: i for i, r in enumerate(order)})
    assert out._k.notna().all(), "a role is missing from the display order"
    out = out.sort_values(["_k", "Column"]).drop(columns="_k")

    sd = man["split_dates"]
    sh = man["shape"]
    n_feat, n_excl = len(features), int((out.Role.str.startswith("Excluded")).sum())

    _emit("feature_matrix",
          "Composition of the modelling matrix",
          f"Every column of the {_FM_CATEGORY} feature matrix at a "
          f"{man['forecast_horizon']}-month forecast horizon, with the role it "
          f"plays in training. The matrix holds {sh['rows']:,} brand-months "
          f"across {sh['brands']} brands in {sh['columns']} columns, of which "
          f"{n_feat} are model inputs.", out,
          note=f"The target is {man['target_col']}, modelled as log1p and "
               f"inverted for reporting. Splits are chronological: training "
               f"{sd['train_start']} to {sd['train_end']}, validation "
               f"{sd['val_start']} to {sd['val_end']}, test "
               f"{sd['test_start']} to {sd['test_end']}. The "
               f"{n_excl} columns marked excluded are same-period sales and "
               f"baseline measures, retained so a prediction can be traced "
               f"back to the observation it was made from; they are not "
               f"available to the model, which would otherwise observe the "
               f"quantity it is asked to predict. Populated is the share of "
               f"rows with a value: autoregressive features are empty for a "
               f"brand's earliest months by construction.",
          review=f"Read from {pq.name} and {mf.name} at render time; the "
                 f"feature list is the manifest's own, not a copy. Role "
                 f"assignment is BY RULE (_fm_role) and asserts that no column "
                 f"falls through -- a column added upstream fails the export "
                 f"rather than appearing unclassified. Counts here supersede "
                 f"the 13/14/16-feature figures in earlier drafts (P0048 F3, "
                 f"F10): the current matrix carries {n_feat} features after the "
                 f"holiday enrichment. CSD is shown as the worked category; the "
                 f"other three differ in the promotional block, which is absent "
                 f"at source for the promo-zero categories.")


def main() -> None:
    _chapters = sorted(set(_TABLE_CHAPTER.values()))
    print(f"Writing tables into {len(_chapters)} chapter folders under "
          f"{THESIS_RESULTS_DIR.name}/: {', '.join(_chapters)}\n")
    if (n := _clear_previous()):
        print(f"  (cleared {n} file(s) from the previous run)\n")

    table_metric_dictionary()
    table_pipeline_execution()
    table_pipeline_data_reduction()
    table_feature_matrix()
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
           f"Generated by `{Path(__file__).resolve().relative_to(ROOT_DIR).as_posix()}`, {stamp}.",
           "",
           "Every table is regenerated from the pipeline and experiment outputs it "
           "describes, so no value here is transcribed by hand. Each is written as "
           "`.md` for reading and `.csv` so any figure can be traced back to its "
           "source.", "",
           "**Table content carries no numbers.** Numbering is applied by the "
           "thesis document itself, so that the appendix and the text cannot "
           "disagree about which table is which. The `NN_` filename prefix orders "
           "this directory and is not a table number.", "",
           "Tables are filed under the **chapter that discusses them**, rather "
           "than under the script that produced them.", "",
           "| # | Chapter | Table | File |", "|---|---|---|---|"]
    for i, (title, stem) in enumerate(_INDEX, 1):
        ch = _TABLE_CHAPTER[stem.split("_", 1)[1]]
        idx.append(f"| {i} | {ch} | {title} | `{ch}/tables/{stem}.md` |")
    index_path = THESIS_RESULTS_DIR / "APPENDIX_TABLES.md"
    index_path.write_text("\n".join(idx) + "\n",
                          encoding="utf-8", newline="\n")

    print(f"\n{len(_INDEX)} tables written.")
    print(f"  index: {index_path}")
    print("  review notes: 06_thesis_writing/writing-notes/"
          "<chapter>/generated/ (never shipped).")
    # Runs on every export, so the invariant does not depend on being recalled.
    warn_after_run()


if __name__ == "__main__":
    main()
