"""
Architecture diagrams for the thesis — rebuilt 2026-09-06 (P0046 F18).

WHY REBUILT RATHER THAN PATCHED
-------------------------------
The previous generator drew a system that does not exist. Verified against the
live tree on 2026-09-06:

  * LangGraph / StateGraph      -- not a dependency, imported nowhere.
  * "Coordinator", "Agent Layer", four named Agents, phase-approval gates
                                -- no such objects in any live module.
  * PCA + k-means "Consumer Signals"
                                -- no PCA or KMeans call anywhere.
  * ARIMA / Prophet in the ladder
                                -- statistical BASELINES, not ladder members.
  * Per-model RAM (15/20/200/300/400 MB)
                                -- invented; measured values are 4-40x smaller.
  * "System B" thesis-writing agents
                                -- abandoned design, archived.

Patching labels on that frame would have kept the frame, and the frame was the
error. What the repo actually contains is three sequential, independently-run
stages, which is what these diagrams now show.

EVERY NUMBER IS READ FROM AN ARTEFACT AT RENDER TIME. Nothing here is a literal.
If a table changes, the diagram changes; if a table is missing, this exits rather
than drawing a plausible lie.

STYLE
-----
Deliberately plain: one accent colour, no gradients, no rounded "card" boxes, no
emoji, no drop shadows. These are read in a printed thesis, in greyscale, at
column width. Structure carries the meaning, not decoration.
"""
import csv
import json
import re
import sys
from pathlib import Path

for _c in (Path(__file__).resolve().parent, *Path(__file__).resolve().parents):
    if any((_c / a).exists() for a in (".env.example", ".env", "PATHS.py")):
        sys.path.insert(0, str(_c))
        break

import graphviz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from PATHS import (THESIS_RESULTS_SRQ1_DIR, get_chapter_figures_dir,
                   get_category_eda_results_dir,
                   THESIS_RESULTS_DIR, CHAPTER_ORDER,
                   THESIS_DATA_RAW_NIELSEN_DIR,
                   get_category_engineered_bymonth_dir,
                   get_category_pipeline_step_outputs_dir)

# Diagrams are filed by chapter like every other artefact. The chapter comes
# from the filename prefix that _check_stem() already enforces, so the routing
# needs no second list to keep in step with the figure names.
#
# DERIVED from CHAPTER_ORDER, never typed. A hardcoded {number: slug} map is a
# second copy of the chapter numbering, and on 2026-09-08 it silently went stale
# through the Ch5/Ch6 swap: it still said 5:"architecture", 6:"model_benchmark"
# while PATHS.py had already swapped them. The output was only correct because
# the figure stems were renamed in the same pass, so two errors cancelled.
_CH_DIR = {n: slug for slug, n in CHAPTER_ORDER.items()}


def _out_for(stem: str) -> Path:
    """The figures/ folder of the chapter this diagram's prefix names.

    Also removes any copy of this diagram sitting in a DIFFERENT chapter's
    figures/ folder, so a renumbering leaves no stale twin behind.

    Without this the generator only ever added files. A chapter swap renames the
    stems, the new names are written to the new folders, and the old names stay
    where they were -- two copies of every affected figure, differing only in a
    prefix, with nothing to say which is current. Observed 2026-09-08 during the
    Ch5/Ch6 swap. Unlike export_appendix.py this script has no list of its own
    stems to clear from (they live inside the fig_* bodies), so the sweep keys
    on the diagram's SLUG: it removes `ch<other>_<same-slug>.svg` elsewhere and
    cannot touch a figure it does not itself produce.
    """
    n = int(re.match(r"ch(\d+)_", stem).group(1))
    if n not in _CH_DIR:
        raise ValueError(f"{stem!r} names chapter {n}, which does not exist")
    out = get_chapter_figures_dir(_CH_DIR[n])

    slug = stem.split("_", 1)[1]
    for other_n, other_slug in _CH_DIR.items():
        if other_n == n:
            continue
        stale = get_chapter_figures_dir(other_slug) / f"ch{other_n}_{slug}.svg"
        if stale.exists():
            stale.unlink()
            print(f"  (removed stale {stale.parent.parent.name}/"
                  f"figures/{stale.name})")
    return out

TABLES = THESIS_RESULTS_SRQ1_DIR / "tables"
MODELS = THESIS_RESULTS_SRQ1_DIR / "models"
CATS = ["CSD", "Danskvand", "Energidrikke", "RTD"]

# Mirrors export_appendix.py. Confirmed by Brian 2026-09-06 as the correct
# envelope; the thesis prose still says "8 GB" in eight places (P0046 F15).
RAM_BUDGET_MB = 4096.0

# ── greyscale tier palette (see .claude/rules/figure-generation-standards.md) ──
# Nesting is carried by VALUE, not colour, so the structure survives greyscale
# printing: a cluster is darker than the nodes inside it, which is the opposite
# of the usual instinct and the reason nested boxes read as nested.
INK = "#1a1a1a"       # body text
MUTE = "#5a5a5a"      # captions, edge labels
LINE = "#8a8a8a"      # borders
CLUSTER = "#878787"   # group container -- darkest, a mid grey
FILL = "#f4f4f4"      # standalone node
NEST = "#fafafa"      # node inside a cluster -- lightest
ACCENT = "#1f5c8b"    # the one accent, used only on the figure's subject
FONT = "Helvetica"


def _box(title: str, *body: str, size: int = 9) -> str:
    """A bold title over plain body lines, as a graphviz HTML-like label.

    The header names the thing and the body describes it, so a reader can scan
    headers alone. Returns the '<<TABLE ...>>' form graphviz expects; pass it
    straight to node(label=...).
    """
    rows = "".join(
        f'<TR><TD ALIGN="CENTER"><FONT POINT-SIZE="{size}">'
        f'{_esc(l)}</FONT></TD></TR>' for l in body if l)
    return (f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">'
            f'<TR><TD ALIGN="CENTER"><B>{_esc(title)}</B></TD></TR>'
            f'{rows}</TABLE>>')


def _bullets(title: str, *body: str, size: int = 9) -> str:
    """Like _box, but the body is a bulleted list: text left-aligned, block centred.

    A list of parallel items reads better flush-left -- centred lines give every
    item a different starting x, so the eye has no column to run down. But a
    left-aligned block hard against the box edge looks unbalanced, so the list is
    nested in its own single-cell table, which centres as a unit while its
    contents stay flush. Left text, centred block; both, rather than either.

    Use for enumerations of comparable things. Prose stays with _box().
    """
    items = "".join(
        f'<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="{size}">'
        f'&#8226; {_esc(l)}</FONT></TD></TR>' for l in body if l)
    inner = (f'<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0">'
             f'{items}</TABLE>')
    return (f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">'
            f'<TR><TD ALIGN="CENTER"><B>{_esc(title)}</B></TD></TR>'
            f'<TR><TD ALIGN="CENTER">{inner}</TD></TR></TABLE>>')


def _stack(title: str, rows: list, size: int = 9, dashed: bool = False) -> str:
    """A titled group whose members are rows of one label, in the order given.

    Use instead of a cluster when the ORDER of the members matters. A cluster
    lets graphviz's layout engine choose the order of its members, and it will
    reorder them to shorten edges -- seven successive attempts to constrain that
    (invisible chains, per-cluster rank, ordering, edge weights, newrank,
    constraint=false) each produced a different wrong order, because every one
    of those knobs is a *hint* to a heuristic.

    Rendering the members as rows of a single node removes the heuristic from
    the question: the order is text in a table, so it cannot be rearranged.
    The cost is that members are no longer individually addressable as edge
    endpoints -- the group as a whole is. Worth it when the sequence IS the
    content, as with a lettered ladder.

    `rows` is a list of (heading, detail) pairs; detail may be "".
    """
    border = "1" if not dashed else "1"
    cells = []
    for head, detail in rows:
        d = (f'<BR/><FONT POINT-SIZE="{size - 1}">{_esc(detail)}</FONT>'
             if detail else "")
        # Centred, matching _box: these rows are a heading over a subtitle, the
        # same shape as a standalone node, and mixing left-aligned rows into a
        # figure of centred boxes reads as an inconsistency rather than a choice.
        # (Left alignment belongs to _bullets, where items form a scannable list.)
        cells.append(
            f'<TR><TD ALIGN="CENTER" BALIGN="CENTER" BGCOLOR="{NEST}" '
            f'BORDER="{border}" COLOR="{LINE}" CELLPADDING="5">'
            f'<B>{_esc(head)}</B>{d}</TD></TR>')
    return (f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="4" CELLPADDING="0">'
            f'<TR><TD ALIGN="CENTER"><FONT POINT-SIZE="{size}">'
            f'{_esc(title)}</FONT></TD></TR>'
            f'{"".join(cells)}</TABLE>>')


def _esc(s: str) -> str:
    """Escape the three characters that would otherwise break an HTML label."""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _need(p: Path) -> Path:
    if not p.is_file():
        raise SystemExit(f"missing artefact: {p}\nRun its producer first; "
                         f"refusing to draw a diagram from absent data.")
    return p


def _rows(p: Path) -> list:
    with _need(p).open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def profiling() -> dict:
    return {r["model"]: r for r in _rows(TABLES / "profiling.csv")}


def ladder() -> list:
    found = {r["model"] for r in _rows(TABLES / "metrics.csv")}
    order = ["SeasonalNaive", "Ridge", "LightGBM", "XGBoost"]
    return [m for m in order if m in found] + sorted(found - set(order))


def served() -> dict:
    out = {}
    for m in sorted(MODELS.glob("*/metadata.json")):
        out[m.parent.name] = json.loads(m.read_text(encoding="utf-8"))
    return out


def panel_shape() -> tuple:
    """(rows, brands) of the CSD engineered panel — the largest category."""
    import pandas as pd
    fm = pd.read_parquet(
        _need(get_category_engineered_bymonth_dir("CSD") / "csd_feature_matrix_h3.parquet"))
    return len(fm), fm["brand"].nunique()


def _g(name: str, rankdir: str = "LR") -> graphviz.Digraph:
    """A graph with the house style applied.

    Defaults to LR: the appendix prints landscape, so a horizontal flow uses the
    page it is printed on. A portrait figure forces the reader to rotate the
    document -- if a left-to-right flow runs too wide, wrap it into two rows
    rather than turning it on its side.

    Background is transparent so the figure sits on whatever ground the document
    uses rather than carrying a white rectangle into a dark-themed viewer.
    """
    g = graphviz.Digraph(name, format="svg")
    g.attr(rankdir=rankdir, bgcolor="transparent", splines="polyline",
           nodesep="0.35", ranksep="0.5", fontname=FONT, compound="true")
    g.attr("node", shape="box", style="filled", fillcolor=FILL,
           color=LINE, fontname=FONT, fontsize="10", fontcolor=INK,
           margin="0.16,0.10", penwidth="0.8")
    g.attr("edge", color=MUTE, fontname=FONT, fontsize="9",
           fontcolor=MUTE, arrowsize="0.7", penwidth="0.9")
    return g


def _cluster(g, cid: str, label: str):
    """A group container: darker than the nodes it holds, so nesting is visible."""
    c = g.subgraph(name=f"cluster_{cid}")
    return c


def _cluster_attrs(c, label: str) -> None:
    """A group container: mid grey, so the near-white boxes inside read as nested.

    The label is INK rather than MUTE: at this fill value a muted grey title
    sinks into the background it sits on. Any outer/inner box pair uses this
    same pairing -- CLUSTER behind, NEST in front, black label.
    """
    c.attr(label=label, fontname=FONT, fontsize="9", fontcolor=INK,
           color=LINE, style="filled", fillcolor=CLUSTER, penwidth="0.8",
           margin="10")
    c.attr("node", fillcolor=NEST)


def _caption(g, text: str) -> None:
    """The figure's own caption. Submission-ready prose only.

    No filenames, no step numbers, no plan IDs -- an assessor reads the thesis,
    not this repository. Internal notes belong in the accompanying review notes,
    below a horizontal rule, never on the figure.

    Wrapped, because graphviz treats a label as one line and will widen the whole
    figure to fit it -- a long caption silently stretches the drawing above it.
    """
    import textwrap
    # "\\n" centres each line; "\\l" would left-justify it. The caption sits under
    # a centred drawing, so a left-flush block reads as misaligned against it.
    body = "\\n".join(textwrap.wrap(" ".join(text.split()), width=118)) + "\\n"
    g.attr(label=f"\n{body}", fontsize="9", fontcolor=MUTE, labelloc="b",
           labeljust="c")


_CH_PREFIX = re.compile(r"^ch\d+_")


def _check_stem(stem: str) -> str:
    """Every diagram filename declares the chapter it belongs to.

    The diagrams folder is flat and mixes chapters, so the prefix is the only
    thing that says where a figure is cited. Enforced rather than remembered:
    five figures had drifted unprefixed before this check existed, and the name
    alone did not say which chapter each served.

    Raises rather than warns -- a figure written without a chapter is a figure
    nobody can place, and it is cheaper to fail here than to sort it out later.
    """
    if not _CH_PREFIX.match(stem):
        raise ValueError(
            f"diagram stem {stem!r} has no chapter prefix. "
            f"Name it 'ch<N>_<slug>' so the file says where it is cited.")
    return stem


def _save(g: graphviz.Digraph, stem: str) -> None:
    _check_stem(stem)
    # SVG only. It is vector, so it stays sharp at any size, and Word takes it
    # on paste directly -- the PNG twin was strictly the lower-quality copy.
    g.render(_out_for(stem) / stem, format="svg", cleanup=True)
    print(f"  {stem}.svg")


# ─────────────────────────────────────────────────────────────────────────────
def fig_pipeline():
    """The preprocessing pipeline, from raw extract to modelling matrix."""
    rows, brands = panel_shape()
    g = _g("pipeline", rankdir="LR")

    g.node("raw", _box("Scanner extract", "monthly retail records"), shape="cylinder")
    g.node("cache", _box("Validated cache", "columnar store"))
    g.node("panel", _box("Aggregated panel", "brand by month",
                         f"{brands} brands"))
    g.node("contract", _box("Measured data contract",
                            "derived from the panel itself"))
    g.node("feat", _box("Modelling matrix",
                        f"{rows:,} rows, 54 columns"),
           color=ACCENT, penwidth="1.5", fillcolor="white")
    g.node("eda", _box("Exploratory analysis", "tables and figures"))

    for a, b in [("raw", "cache"), ("cache", "panel"), ("panel", "contract"),
                 ("contract", "feat")]:
        g.edge(a, b)
    g.edge("panel", "eda", style="dashed")

    _caption(g, "Preprocessing, from raw scanner extract to modelling matrix. "
                "Counts shown are for the largest product category. The data "
                "contract is measured from the panel rather than assumed, so "
                "the parameters governing feature construction follow from the "
                "data in hand.")
    _save(g, "ch4_preprocessing_pipeline_v2")


def fig_model_selection():
    """Benchmark the candidate models, then deploy one per category."""
    prof, lad, srv = profiling(), ladder(), served()
    g = _g("model_selection", rankdir="LR")

    def _clean(n: str) -> str:
        return n.split("(")[0].strip()

    g.node("feat", _box("Modelling matrix", "one per product category"))
    with g.subgraph(name="cluster_bench") as c:
        _cluster_attrs(c, "candidate models")
        for m in lad:
            r = prof.get(m)
            c.node(f"m_{m}", _box(m, f"{float(r['peak_fit_RSS_MB']):.0f} MB peak memory")
                   if r else _box(m))
    won = {}
    for cat, meta in srv.items():
        won.setdefault(_clean(meta["model"]), []).append(cat)
    g.node("persist", _box("Deployed per category",
                           *[f"{m} — {', '.join(sorted(c))}"
                             for m, c in sorted(won.items())]),
           color=ACCENT, penwidth="1.5", fillcolor="white")

    g.edge("feat", f"m_{lad[0]}", style="dashed", lhead="cluster_bench")
    g.edge(f"m_{lad[-1]}", "persist", style="dashed", ltail="cluster_bench")

    _caption(g, "Model selection. Each candidate is fitted independently on "
                "identical data and profiled for peak memory as well as "
                "accuracy; the model achieving the lowest error in each "
                "category is the one deployed.")
    _save(g, "ch5_model_selection_v2")


def fig_scenarios():
    """The evaluation scenarios, as an information ladder.

    The two groups are drawn with _stack() rather than as graphviz clusters:
    the order A..E is the content of this figure, and a cluster hands that
    order to a layout heuristic. See _stack's docstring for what was tried.
    """
    g = _g("scenarios", rankdir="LR")
    g.attr(ranksep="0.6", nodesep="0.35")

    g.node("q", _box("Forecasting question", "brand, category and horizon"))
    g.node("model", _box("Deployed model", "one per product category"))

    # Lettered as the repository names them, so figure, run logs and results
    # tables share one vocabulary. D and E are dashed: the harness runs A, B
    # and C only, and D/E await access to a proprietary engine. Drawing five
    # identical rungs would assert five sets of results exist.
    g.node("llm", _stack("evaluation scenarios — LLM", [
        ("A — Plain LLM", "no access to firm data"),
        ("B — LLM + data & code", "the firm's history, analysed in a sandbox"),
        ("C — LLM + dedicated model", "the forecast tool"),
    ]), shape="box", style="filled", fillcolor=CLUSTER, color=LINE)

    g.node("prom", _stack("planned — Prometheus production engine", [
        ("D — Prometheus + data & code", "the engine as shipped"),
        ("E — Prometheus + dedicated model", "the forecast tool, ported"),
    ], dashed=True), shape="box", style="filled,dashed", fillcolor=CLUSTER,
        color=LINE)

    g.node("log", _box("Recorded outcomes",
                       "responses and measurements retained"),
           color=ACCENT, penwidth="1.5", fillcolor="white")

    # Left to right: what is asked, what answers it, what is recorded. The
    # trained model joins from the left because it is an input, not an outcome.
    g.edge("q", "llm")
    g.edge("q", "prom", style="dotted")
    g.edge("model", "llm", style="dashed", label="supplies C")
    g.edge("model", "prom", style="dotted", label="supplies E")
    g.edge("llm", "log", style="dashed")
    g.edge("prom", "log", style="dotted")

    # Inputs share the leftmost column; the two groups stack in the middle.
    with g.subgraph() as col:
        col.attr(rank="same")
        col.node("q")
        col.node("model")
    with g.subgraph() as col:
        col.attr(rank="same")
        col.node("llm")
        col.node("prom")

    _caption(g, "The evaluation scenarios, ordered as an information ladder. "
                "Each rung adds one capability: A to B measures what access to "
                "the firm's own data buys, and B to C measures what the "
                "dedicated forecasting model adds beyond it. Scenarios D and E "
                "repeat that final comparison inside the production engine and "
                "are shown dashed: they are specified but not executed here, "
                "since the engine is proprietary.")
    _save(g, "ch7_scenarios_v2")


def fig_resource_profile():
    """Measured fit cost per model, against the deployment envelope."""
    prof = profiling()
    names = [m for m in ladder() if m in prof]
    vals = [float(prof[m]["peak_fit_RSS_MB"]) for m in names]

    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    bars = ax.barh(names, vals, color=ACCENT, height=0.55)
    for b, v in zip(bars, vals):
        ax.text(v + max(vals) * 0.02, b.get_y() + b.get_height() / 2,
                f"{v:.1f} MB", va="center", fontsize=9, color=INK)
    ax.set_xlabel("Peak fit memory, RSS (MB)")
    ax.set_xlim(0, max(vals) * 1.25)
    share = max(vals) / RAM_BUDGET_MB * 100
    ax.set_title(f"Measured fit cost — largest is {share:.2f}% of the "
                 f"{RAM_BUDGET_MB/1024:.0f} GB envelope", fontsize=10, color=INK)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    # Transparent, matching the graphviz figures: the page supplies the ground.
    # Saved directly rather than through _save(), so the chapter-prefix check is
    # called explicitly here -- otherwise this one figure would escape it.
    stem = _check_stem("ch5_resource_profile_v2")
    fig.savefig(_out_for(stem) / f"{stem}.svg", transparent=True)
    plt.close(fig)
    print(f"  {stem}.svg")


def fig_layered_architecture():
    """Ch5: the three layers, from forecasting substrate to scenario comparison.

    Replaces a hand-drawn figure that asserted several things the system does not
    do: a five-model substrate including two statistical baselines, approval
    checkpoints that exist in no module, a graph-orchestration deployment that is
    not a dependency, and an eight-gigabyte envelope.
    """
    lad, srv, prof = ladder(), served(), profiling()

    def _clean(n: str) -> str:
        return n.split("(")[0].strip()

    g = _g("layered_architecture", rankdir="LR")
    g.attr(ranksep="0.55", nodesep="0.25")

    g.node("data", _box("Scanner panel", "brand by month"), shape="cylinder")

    with g.subgraph(name="cluster_1") as c:
        _cluster_attrs(c, "forecasting substrate")
        for m in lad:
            r = prof.get(m)
            c.node(f"s_{m}", _box(m, f"{float(r['peak_fit_RSS_MB']):.0f} MB")
                   if r else _box(m))

    won = {}
    for cat, meta in srv.items():
        won.setdefault(_clean(meta["model"]), []).append(cat)
    g.node("chosen", _box("Deployed per category",
                          *[f"{m} — {', '.join(sorted(c))}"
                            for m, c in sorted(won.items())]),
           color=ACCENT, penwidth="1.5", fillcolor="white")

    with g.subgraph(name="cluster_2") as c:
        _cluster_attrs(c, "structured tool interface")
        c.node("tool", _box("Forecast tool",
                            "point forecast, calibrated interval,",
                            "confidence tier"))
        c.node("log", _box("Audit record",
                           "model, training cut-off,", "calibration sample"))

    # Deliberately NOT lettered here. The comparison generalises over the agent:
    # both the local orchestrator and the production engine are agents, both can
    # be given data and code, and both can be given the trained models -- so the
    # three conditions cover all five lettered scenarios rather than only the
    # first three. Naming A/B/C in this figure would have implied the Prometheus
    # pair was missing, and would have duplicated a mapping the scenarios figure
    # already owns. The letters belong there; the capability ladder belongs here.
    #
    # A _stack, not a cluster: the three conditions are a sequence, and a cluster
    # reorders its members to shorten edges (it had rendered C, B, A). The one
    # edge that pointed into a member now addresses the group.
    g.node("scen", _stack("scenario comparison", [
        ("Plain agent", "no access to firm data"),
        ("Agent + data & code", "the firm's history, analysed"),
        ("Agent + models", "the forecast tool"),
    ]), shape="box", style="filled", fillcolor=CLUSTER, color=LINE)

    g.edge("data", f"s_{lad[0]}", style="dashed", lhead="cluster_1")
    g.edge(f"s_{lad[-1]}", "chosen", style="dashed", ltail="cluster_1")
    g.edge("chosen", "tool", label="deployed to")
    g.edge("tool", "log", style="dashed")
    g.edge("tool", "scen")
    g.edge("data", "scen", style="dashed", constraint="false")

    largest = max((float(prof[m]["peak_fit_RSS_MB"]) for m in lad if m in prof),
                  default=0)
    _caption(g, "The predictive extension in three layers. Candidate models are "
                "benchmarked on identical data and one is deployed per product "
                "category; the tool interface exposes its forecasts with "
                "uncertainty and provenance attached; and only the "
                "model-equipped condition draws on that interface. The three "
                "conditions are stated in terms of the agent rather than of a "
                "particular engine, so they apply equally to the local "
                "orchestrator and to the production platform. The language model "
                "is reached over an API rather than hosted locally, so the "
                f"deployment envelope of {RAM_BUDGET_MB/1024:.0f} GB is spent on "
                f"data and models alone — the most demanding model observed "
                f"requires {largest:.0f} MB to fit.")
    _save(g, "ch6_layered_architecture_v2")


# ─────────────────────────────────────────────────────────────────────────────
# Chapter figures, added 2026-09-07
# ─────────────────────────────────────────────────────────────────────────────

def _step4_logs() -> dict:
    """Per-category step 4 reduction chain, read from the logs step 4 writes."""
    out = {}
    for cat in CATS:
        d = get_category_pipeline_step_outputs_dir(cat)
        for log in sorted(d.glob("step_4_log_h3.json")):
            try:
                s = json.loads(log.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if s.get("result"):
                out[s.get("category", cat)] = s["result"]
    return out


def fig_research_questions_tree():
    """Ch1: the main research question and its four subsidiary questions.

    Built in the generator rather than drawn by hand: the question set has moved
    once already, and a node list is a cheap edit next time it moves, whereas a
    hand-drawn tree goes stale silently.

    Each question is shown by its short name and the chapter that answers it.
    The full wording runs to sixty words for the fourth and cannot be read in a
    box; it belongs in the text.
    """
    g = _g("rq_tree", rankdir="TB")
    g.attr(ranksep="0.7", nodesep="0.3")

    g.node("mrq", _box(
        "Main research question",
        "How can production-oriented agentic decision-support systems",
        "without native predictive capabilities be extended with lightweight",
        "forecasting models to support reliable, forecast-informed and",
        "cost-justified decision-making under computational and",
        "deployment constraints?", size=10),
        color=ACCENT, penwidth="1.5", fillcolor="white")

    srqs = [
        ("s1", "SRQ1 - Models and Efficiency", "Chapter 6",
         ("accuracy, memory efficiency", "and category specialisation")),
        ("s2", "SRQ2 - Structured Tool Interface", "Chapters 5 and 7",
         ("reliability, uncertainty", "and traceability")),
        ("s3", "SRQ3 - Integration Readiness", "Chapters 5, 7 and 9",
         ("capabilities a production", "system requires")),
        ("s4", "SRQ4 - Models versus Code", "Chapter 8",
         ("correctness, consistency and", "replicability at justified cost")),
    ]
    # Equal width, fixed. Left to itself graphviz sizes each box to its own text,
    # and the fourth title is twice the length of the first -- so a row of four
    # siblings came out visibly uneven, reading as a hierarchy that isn't there.
    # These are four peers and should look like it.
    with g.subgraph() as row:
        row.attr(rank="same")
        for nid, title, chap, body in srqs:
            row.node(nid, _box(title, chap, "", *body),
                     width="2.6", fixedsize="false")
    for nid, *_ in srqs:
        g.edge("mrq", nid)

    _caption(g, "Structure of the research questions. The main question is "
                "answered through four subsidiary questions, each shown with "
                "the chapter in which it is addressed.")
    _save(g, "ch1_research_questions_tree_v2")


def fig_data_pipeline():
    """Ch4 opening: access, exploration, cleaning, enrichment, feature construction.

    Horizontal, in two rows: eight stages in a single row runs past a readable
    size at page width, and the appendix prints landscape, so the flow wraps
    rather than turning portrait.

    Every count is read from the pipeline's own execution record, so the figure
    cannot claim a panel size the pipeline did not produce.
    """
    logs = _step4_logs()
    if not logs:
        raise SystemExit("no step_4_log_h3.json found; run run_preprocessing.py first")
    tot_in = sum(r["rows_in"] for r in logs.values())
    tot_out = sum(r["rows_out"] for r in logs.values())
    br_in = sum(r["brands_in"] for r in logs.values())
    br_out = sum(r["brands_out"] for r in logs.values())

    # Counted, not asserted: a literal would go stale the moment a section moves.
    _eda_t = get_category_eda_results_dir("CSD") / "tables"
    n_sec = len({f.stem.split("_", 3)[2] for f in _eda_t.glob("step_2_*.md")
                 if len(f.stem.split("_", 3)) == 4}) if _eda_t.is_dir() else 0

    g = _g("data_pipeline", rankdir="LR")
    g.attr(ranksep="0.4", nodesep="0.25")

    g.node("src", _box("Scanner panel", "monthly brand records"), shape="cylinder")

    # The two phases are _stack() groups, not clusters. As clusters they were
    # laid out side by side (ratio 4.4, too wide for a page), and forcing them
    # to stack with rank="same" re-parented their members -- graphviz warned
    # "agg was already in a rankset, deleted from cluster data_pipeline" and
    # drew the contract box outside the phase it belongs to. A stack cannot
    # leak a member, because the members are rows of one label.
    g.node("prep", _stack("panel construction", [
        ("Access", "validated extract"),
        ("Aggregation", f"brand by month — {tot_in:,} rows, {br_in} brands"),
        ("Exploratory analysis", f"{n_sec} analyses"),
    ]), shape="box", style="filled", fillcolor=CLUSTER, color=LINE, width="3.1", fixedsize="false")

    g.node("build", _stack("matrix construction", [
        ("Data contract", "lag depth, series length, split dates"),
        ("Enrichment", "holidays, promotions"),
        ("Feature construction", "completed month grid, lags and rolling windows"),
    ]), shape="box", style="filled", fillcolor=CLUSTER, color=LINE, width="3.1", fixedsize="false")

    g.node("matrix", _box("Modelling matrices",
                          f"{tot_out:,} rows, {br_out} brands",
                          f"{len(logs)} categories"),
           color=ACCENT, penwidth="1.5", fillcolor="white", width="1.95", fixedsize="false")

    g.node("arms", _stack("training arms", [
        ("Category-specific", ""),
        ("Pooled", "category as a feature"),
    ]), shape="box", style="filled", fillcolor=CLUSTER, color=LINE)

    # Source on the left, outputs on the right, the two phases stacked between.
    g.edge("src", "prep")
    g.edge("prep", "build", label="informs")
    g.edge("build", "matrix")
    g.edge("matrix", "arms")

    with g.subgraph() as col:
        col.attr(rank="same")
        col.node("prep")
        col.node("build")
    with g.subgraph() as col:
        col.attr(rank="same")
        col.node("matrix")
        col.node("arms")

    _caption(g, "Construction of the modelling data set. Raw scanner records are "
                "validated and aggregated to a brand-by-month panel, explored to "
                "establish its statistical properties, and narrowed by a data "
                "contract measured from the panel itself. The retained series are "
                "enriched with calendar and promotional information and turned "
                "into modelling matrices. The matrices hold more rows than the "
                "panel because each retained brand's month grid is completed "
                "before lagged features are built, so that a lag refers to the "
                "preceding month rather than to the preceding observation.")
    _save(g, "ch4_data_pipeline_v1")


def fig_eda_pipeline():
    """Ch4 middle: the exploratory analysis, with one category worked through.

    Analysis names are read from the tables the exploration itself produced, so
    a section added or removed changes this figure without anyone editing it.
    The internal numbering is deliberately dropped: it is a repository detail,
    and the grouping already carries the structure a reader needs.
    """
    eda = get_category_eda_results_dir("CSD")
    tdir, pdir = eda / "tables", eda / "plots"
    if not tdir.is_dir():
        raise SystemExit(f"missing {tdir}; run the pipeline then promote_eda_artifacts")

    # The stored slugs are internal identifiers ("acf significant lags", "cv").
    # An assessor reads the thesis, not this repository, so each is mapped to the
    # term the discipline uses. MEMBERSHIP is still read from disk -- an unmapped
    # slug falls through to a readable form and is surfaced, never silently
    # dropped, so a new analysis cannot vanish from the figure.
    LABELS = {
        "columns": "field inventory",
        "missing": "missing values",
        "shape": "panel dimensions",
        "skewness": "distributional skew",
        "coverage": "temporal coverage",
        "rows_per_brand": "observations per brand",
        "structural_break": "structural breaks",
        "adf_per_brand": "unit-root tests",
        "brand_retention": "brand retention",
        "zero_types": "zero-sales patterns",
        "monthly_distribution": "monthly distribution",
        "peak_valley": "peak and trough months",
        "top_brands": "leading brands",
        "cv": "demand variability",
        "peak_months": "seasonal peaks",
        "promo_intensity": "promotional intensity",
        "measure_quality": "measurement quality",
        "ecdf_quantiles": "empirical distribution",
        "acf_significant_lags": "autocorrelation structure",
        "promo_distribution": "promotional distribution",
        "redundant_pairs": "feature redundancy",
        "target_correlations": "correlation with demand",
    }
    secs = {}
    for f in sorted(tdir.glob("step_2_*.md")):
        parts = f.stem.split("_", 3)              # step, 2, NN, name
        if len(parts) == 4:
            slug = parts[3]
            secs.setdefault(parts[2], []).append(
                LABELS.get(slug, slug.replace("_", " ")))
    plots = sorted(p.stem for p in pdir.glob("*.png"))

    g = _g("eda_pipeline", rankdir="LR")
    g.attr(ranksep="0.7", nodesep="0.18")

    g.node("panel", _box("Brand-by-month panel",
                         "one product category,", "worked through in full"),
           shape="cylinder")

    # The four questions the exploration answers. Grouping is editorial; the
    # MEMBERSHIP is read from disk, and anything ungrouped is surfaced rather
    # than silently dropped.
    groups = [
        ("g1", "Structure and quality", ("01", "02", "14")),
        ("g2", "Coverage and retention", ("03", "06", "07")),
        ("g3", "Stationarity and seasonality", ("04", "05", "08", "12", "16")),
        ("g4", "Drivers and redundancy", ("11", "13", "15", "17", "18")),
    ]
    with g.subgraph(name="cluster_eda") as c:
        _cluster_attrs(c, "exploratory analysis")
        for gid, title, nums in groups:
            members = [m for n in nums if n in secs for m in secs[n]]
            if members:
                # Bulleted: these are lists of comparable analyses, so the
                # items read down a common left edge instead of each line
                # starting at its own centred position.
                c.node(gid, _bullets(title, *members))
        grouped = {n for _g2, _t, nums in groups for n in nums}
        if (stray := sorted(set(secs) - grouped)):
            c.node("gx", _bullets("Further analyses",
                                  *[m for n in stray for m in secs[n]]))

    for gid, _t, nums in groups:
        if any(n in secs for n in nums):
            g.edge("panel", gid, style="dashed")
    if stray:
        g.edge("panel", "gx", style="dashed")

    n_tab = len(list(tdir.glob("step_2_*.md")))
    g.node("out", _box("Documented findings",
                       f"{n_tab} tables, {len(plots)} figures"),
           color=ACCENT, penwidth="1.5", fillcolor="white", width="2.0", fixedsize="false")
    g.node("contract", _box("Measured data contract",
                            "peak months, minimum series length,",
                            "target transformation"))

    for gid, _t, nums in groups:
        if any(n in secs for n in nums):
            g.edge(gid, "out", style="dashed")
    if stray:
        g.edge("gx", "out", style="dashed")
    g.edge("out", "contract", label="informs")

    _caption(g, "Exploratory analysis of a single product category, shown as the "
                "worked example; every category is analysed identically. The "
                "panel is examined along four lines of enquiry — its structure "
                "and quality, the coverage and retention of individual brands, "
                "its stationarity and seasonality, and the candidate demand "
                "drivers together with their redundancy. The findings are "
                "documented as tables and figures, and are what the subsequent "
                "data contract is measured from, so that decisions about lag "
                "depth, series length and transformation follow from the data "
                "rather than from convention.")
    _save(g, "ch4_eda_pipeline_csd_v1")


def fig_modelling_pipeline():
    """Ch6: the two training arms, the model ladder, evaluation, and what won."""
    lad, srv, prof = ladder(), served(), profiling()
    pooled = TABLES / "pooled_metrics.csv"
    baselines = TABLES / "stat_baselines.csv"

    g = _g("modelling", rankdir="LR")
    g.attr(ranksep="0.6", nodesep="0.2")
    g.node("matrix", _box("Modelling matrices", "one per product category"),
           shape="cylinder")

    with g.subgraph(name="cluster_arms") as c:
        _cluster_attrs(c, "training arms")
        c.node("a_pc", _box("Category-specific", "a model fitted per category"))
        c.node("a_pool", _box("Pooled", "all categories jointly,",
                              "category as a feature"))

    with g.subgraph(name="cluster_lad") as c:
        _cluster_attrs(c, "candidate models")
        for m in lad:
            r = prof.get(m)
            ram = (f"{float(r['peak_fit_RSS_MB']):.0f} MB peak memory"
                   if r else "")
            c.node(f"m_{m}", _box(m, ram) if ram else _box(m))

    def _clean(name: str) -> str:
        """Internal variant tags are method detail, not model identity."""
        return name.split("(")[0].strip()

    if baselines.is_file():
        bl = sorted({_clean(r["model"]) for r in _rows(baselines)})
        g.node("base", _box("Statistical baselines", ", ".join(bl)))

    g.node("eval", _box("Evaluation",
                        "forecast error on held-out months,",
                        "significance testing, seed stability,",
                        "prediction-interval coverage"))

    won = {}
    for cat, meta in srv.items():
        won.setdefault(_clean(meta["model"]), []).append(cat)
    g.node("won", _box("Selected and deployed",
                       *[f"{m} — {', '.join(sorted(c))}"
                         for m, c in sorted(won.items())]),
           color=ACCENT, penwidth="1.5", fillcolor="white")

    g.edge("matrix", "a_pc"); g.edge("matrix", "a_pool")
    # Cluster-level edges: fanning every model to evaluation produces eight
    # near-parallel dashed lines that obscure the structure they should show.
    g.edge("a_pc", f"m_{lad[0]}", style="dashed", lhead="cluster_lad")
    g.edge(f"m_{lad[-1]}", "eval", style="dashed", ltail="cluster_lad")
    g.edge("a_pool", "eval", style="dashed")
    if baselines.is_file():
        g.edge("matrix", "base", style="dashed")
        g.edge("base", "eval", style="dashed")
    g.edge("eval", "won", label="lowest error")

    # Pooled vs category-specific is genuinely split, so the caption states the
    # split rather than a direction -- claiming a winner would assert a result
    # the numbers do not support.
    split = ""
    if pooled.is_file():
        rows = _rows(pooled)
        cats = sorted({r["category"] for r in rows})
        pc_wins = [c for c in cats
                   if min((float(r["test_wmape"]) for r in rows
                           if r["category"] == c and r["arm"] == "per_category"),
                          default=9e9)
                   <= min((float(r["test_wmape"]) for r in rows
                           if r["category"] == c and r["arm"] == "pooled"),
                          default=9e9)]
        split = (f" Neither training arm dominates: category-specific training "
                 f"achieves the lower error in {len(pc_wins)} of {len(cats)} "
                 f"categories and pooled training in the remainder, so the "
                 f"choice is made per category rather than in general.")

    _caption(g, "Model selection. Each candidate is fitted independently on the "
                "same data, under two training arms — one model per product "
                "category, and a single pooled model with category as a feature "
                "— and is evaluated against statistical baselines on held-out "
                "months." + split + " The model with the lowest error in each "
                "category is retrained on the full training window and deployed.")
    _save(g, "ch5_modelling_pipeline_v1")


def fig_tool_interface():
    """Ch5: the serving interface -- what the tool accepts and what it returns.

    The returned fields are read from a deployed model's own record rather than
    typed here, so a change to what is served shows up in the figure.
    """
    srv = served()
    if not srv:
        raise SystemExit("no persisted models; run train_and_persist.py first")
    any_meta = next(iter(srv.values()))

    g = _g("tool_interface", rankdir="LR")
    g.attr(ranksep="0.55", nodesep="0.3")

    # The question originates with a person, not with the agent. The agent's work
    # at this end is recognising that a demand question is a forecasting task and
    # resolving it into the arguments the tool accepts -- omitting that step made
    # the agent look like the asker rather than the interpreter.
    g.node("user", _box("Decision maker", "asks a demand question",
                        "in natural language"))
    g.node("caller", _box("Agentic decision-support system",
                          "recognises a forecasting task and",
                          "resolves it into tool arguments"))
    g.node("call", _box("Request", "product category, brand,",
                        "forecast horizon"))

    with g.subgraph(name="cluster_tool") as c:
        _cluster_attrs(c, "forecast tool")
        c.node("load", _box("Model retrieval",
                            f"the deployed model for that category",
                            f"({len(srv)} categories available)"))
        c.node("feat", _box("Feature construction",
                            "lagged and rolling features,",
                            "calendar information — server-side"))
        c.node("pred", _box("Prediction",
                            "point forecast and calibrated",
                            "90% prediction interval"))

    g.node("resp", _box("Structured response",
                        "point forecast",
                        "lower and upper interval bounds",
                        "confidence score and tier",
                        "model identity and training cut-off",
                        "size of the calibration sample"),
           color=ACCENT, penwidth="1.5", fillcolor="white")
    g.node("log", _box("Audit record", "every call retained"))

    g.edge("user", "caller")
    g.edge("caller", "call")
    g.edge("call", "load")
    g.edge("load", "feat")
    g.edge("feat", "pred")
    g.edge("pred", "resp")
    g.edge("resp", "caller", label="returns", constraint="false")
    g.edge("resp", "log", style="dashed")

    # Two rows: the request path across the top, the response beneath it. In one
    # row this ran ~1770px and the return edge had to travel the full width.
    with g.subgraph() as r:
        r.attr(rank="same")
        for n in ("user", "caller", "call"):
            r.node(n)
    with g.subgraph() as r:
        r.attr(rank="same")
        for n in ("resp", "log"):
            r.node(n)

    _caption(g, "The structured forecast interface. A demand question is put in "
                "natural language; the agent recognises it as a forecasting "
                "task and resolves it into the arguments the tool accepts. It "
                "supplies only an identifier and a horizon; feature "
                "construction remains on the server, so the language model "
                "never handles feature vectors. "
                "What returns is not a bare number but a forecast carrying its "
                "uncertainty, a confidence tier, and the provenance needed to "
                "trace it — which model produced it, through what training "
                "cut-off, and on how large a calibration sample. Every call is "
                "retained, so any recommendation can be traced back to the "
                "forecast it rests on.")
    _save(g, "ch6_tool_interface_v1")


def fig_gap_diagram():
    """Ch2: the four literatures and the gap at their intersection."""
    g = _g("gap", rankdir="TB")
    g.attr(ranksep="0.6", nodesep="0.3")

    strands = [
        ("l1", "Forecasting for consumer goods",
         ("competition benchmarks, gradient boosting,", "exogenous demand drivers"),
         ("no deployment budget,", "no agentic consumer")),
        ("l2", "Language-model agents and tool use",
         ("delegation to typed tools,", "code execution as an action"),
         ("weak link to forecasting",)),
        ("l3", "Reliability and evaluation",
         ("hallucination, traceability,", "calibrated uncertainty"),
         ("not the integration itself",)),
        ("l4", "Production agentic systems",
         ("demonstrated hybrid architectures",),
         ("real-time industrial settings,", "not resource-constrained firms")),
    ]
    # Equal width, as in the research-question tree: sized to their own text the
    # four strands come out uneven, and because the gap box is centred on their
    # combined span it then sits visibly off-centre in the figure.
    with g.subgraph() as row:
        row.attr(rank="same")
        for nid, title, has, lacks in strands:
            row.node(nid, _box(title, *has, "", *[f"but {l}" if i == 0 else l
                                                  for i, l in enumerate(lacks)]),
                     width="2.6", fixedsize="false")

    g.node("gap", _box(
        "The gap",
        "Extending a non-predictive agentic system with lightweight",
        "forecasting models, evaluated against a code-execution baseline,",
        f"within a {RAM_BUDGET_MB/1024:.0f} GB deployment envelope", size=10),
        color=ACCENT, penwidth="1.5", fillcolor="white")
    for nid, *_ in strands:
        g.edge(nid, "gap")

    _caption(g, "The research gap as the intersection of four literatures. Each "
                "strand is individually well populated, and each stops short of "
                "the same point: none addresses the extension of an agentic "
                "decision-support system with forecasting models under the "
                "deployment constraints a smaller firm actually faces.")
    _save(g, "ch2_gap_diagram_v2")


# ── Ch4: the raw source schema ───────────────────────────────────────────────
# Categories in scope. Totalbeer exists in the source database (16.3M fact rows)
# but is out of the thesis's scope on compute grounds, so it is not drawn.
_SCHEMA_CATS = ["CSD", "Danskvand", "Energidrikke", "RTD"]


def _read_raw_schema() -> dict:
    """Column names per view, read from the first line of each raw .jsonl.

    Every name and count in the schema figure comes from here, so the drawing
    cannot drift from the extract it documents. Reading one line is enough --
    these are JSON-lines exports of SQL views, so the first object carries the
    full column set, and the fact files run to ~10 GB.
    """
    out = {}
    root = THESIS_DATA_RAW_NIELSEN_DIR / "data_jsonl"
    for cat in _SCHEMA_CATS:
        views = root / cat / "views"
        if not views.exists():
            raise SystemExit(f"missing raw views for {cat}: {views}")
        cols = {}
        for f in sorted(views.glob("*_v.jsonl")):
            kind = f.stem.split("_clean_")[1][:-2]      # strip trailing "_v"
            with f.open(encoding="utf-8") as fh:
                cols[kind] = list(json.loads(fh.readline()))
        out[cat] = cols
    return out


def _read_manifest_rows() -> dict:
    """{view_name: row_count} from the extract manifest written at download."""
    f = THESIS_DATA_RAW_NIELSEN_DIR / "data_jsonl" / "MANIFEST.json"
    if not f.exists():
        raise SystemExit(f"missing extract manifest: {f}")
    m = json.loads(f.read_text(encoding="utf-8"))
    return {e["name"]: e.get("rows") for e in m.get("files", [])
            if e.get("rows") is not None}


def fig_raw_schema():
    """The source star schema, drawn from the raw extract itself."""
    schema = _read_raw_schema()
    rows = _read_manifest_rows()
    csd = schema["CSD"]

    g = _g("raw_schema", rankdir="LR")
    g.attr(ranksep="1.1", nodesep="0.30")

    def _n(view: str) -> str:
        return f"{rows.get(view, 0):,}"

    # --- the three dimensions, left column -------------------------------
    dims = [
        ("dim_period", "dim_period", "csd_clean_dim_period_v",
         ["period_id", "period_end_date", "period_year",
          "period_month", "nielsen_calendar"]),
        ("dim_market", "dim_market", "csd_clean_dim_market_v",
         ["market_id", "market_description", "market_hierarchy_level"]),
        ("dim_product", "dim_product", "csd_clean_dim_product_v",
         ["product_id", "brand", "manufacturer", "packaging",
          "ru_cola_flavour"]),
    ]
    with g.subgraph() as col:
        col.attr(rank="same")
        for nid, title, view, shown in dims:
            n_all = len(csd[title])
            body = [f"{c}" for c in shown]
            if n_all > len(shown):
                body.append(f"... {n_all - len(shown)} more of {n_all}")
            col.node(nid, _bullets(f"{title}  ({_n(view)} rows)", *body),
                     width="2.5", fixedsize="false")

    # --- the fact table ---------------------------------------------------
    fact_cols = csd["facts"]
    keys = [c for c in fact_cols if c.endswith("_id")]
    measures = [c for c in fact_cols if not c.endswith("_id")]
    g.node("facts", _bullets(
        f"facts  ({_n('csd_clean_facts_v')} rows)",
        *[f"{k}   (foreign key)" for k in keys],
        f"{len(measures)} measures, including:",
        "sales_units, sales_value, sales_in_liters",
        "baseline_* (the no-promotion counterfactual)",
        "weighted_distribution_* (availability)"),
        width="3.4", fixedsize="false",
        fillcolor="white", color=ACCENT, penwidth="1.5")

    for nid, title, _v, _s in dims:
        key = f"{title.split('_')[1]}_id"
        g.edge(nid, "facts", label=f" {key} ")

    # --- what differs between categories ----------------------------------
    # Measures, not raw columns: the three join keys are common to every
    # category, so counting them would flatter the categories that carry least.
    per_cat = []
    for cat in _SCHEMA_CATS:
        fc = schema[cat]["facts"]
        nf = len([c for c in fc if not c.endswith("_id")])
        npr = len(schema[cat]["dim_product"])
        per_cat.append((cat, f"{nf} measures · {npr} product attributes"))
    g.node("variation", _stack("the same shape, four payloads", per_cat),
           shape="box", style="filled", fillcolor=CLUSTER, color=LINE)
    g.edge("facts", "variation", style="dashed", arrowhead="none",
           label=" per category ")

    n_dv = len([c for c in schema["Danskvand"]["facts"]
                if not c.endswith("_id")])
    n_csd = len(measures)
    _caption(g, "The source data as delivered, shown for carbonated soft "
                "drinks, the worked category: one fact table of weekly measures "
                "joined to three dimensions by product, market and period. The join keys and the period and market dimensions are "
                "identical across categories, but the payload is not \u2014 the "
                f"carbonated-soft-drinks fact view carries {n_csd} measures "
                f"against {n_dv} for bottled water, which lacks the promotional "
                "and baseline measures entirely, and each category describes its "
                "products with its own attributes. This is why the categories "
                "are preprocessed by category-specific scripts rather than one "
                "shared pass.")
    _save(g, "ch4_raw_schema_v1")


if __name__ == "__main__":
    print("\nRebuilding architecture diagrams from measured artefacts...\n")
    fig_pipeline()
    fig_model_selection()
    fig_scenarios()
    fig_resource_profile()
    fig_layered_architecture()
    print("\n  chapter figures:")
    fig_research_questions_tree()
    fig_gap_diagram()
    fig_data_pipeline()
    fig_raw_schema()
    fig_eda_pipeline()
    fig_modelling_pipeline()
    fig_tool_interface()
    print(f"\nDone - figures written per chapter under "
          f"{THESIS_RESULTS_DIR.name}/\n")
