"""
Architecture & concept diagram generation (graphviz + matplotlib).

Renamed 2026-09-06 from `generate_figures.py`, which said nothing about what it
draws. This emits the six CONCEPTUAL diagrams -- system architecture, agent
workflow, data flow, RAM budget, confidence score, project overview -- not the
empirical result figures (those are srq1_generate_performance_figures.py).

REQUIRES: `pip install graphviz` AND a system graphviz install providing `dot`.
Without the system binary the Python binding imports but fails at render.
- No text/box/arrow overlaps (uses xlabel= for edge annotations, not label=)
- Asymmetric layout: each figure has its own intentional visual hierarchy
- Consistent colour palette across all figures
- Outputs SVG + PNG to THESIS_RESULTS_DIAGRAMS_DIR (05_thesis_results/diagrams/)
"""
import sys
from pathlib import Path

# All output locations resolve through PATHS.py (DEC-P0046-PATHS): no literal
# tier-folder names in generator code.
for _cand in (Path(__file__).resolve().parent, *Path(__file__).resolve().parents):
    if any((_cand / _a).exists() for _a in (".env.example", ".env", "PATHS.py")):
        sys.path.insert(0, str(_cand))
        break
from PATHS import THESIS_RESULTS_DIAGRAMS_DIR, THESIS_RESULTS_SRQ1_DIR

import os
import graphviz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUTPUT_DIR = str(THESIS_RESULTS_DIAGRAMS_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Measured facts, loaded from artefacts (P0046, 2026-09-06)
# ---------------------------------------------------------------------------
# Every model name and MB figure below used to be a hardcoded guess -- the RAM
# numbers in fig2 (Ridge 15 / ARIMA 20 / Prophet 200 / LightGBM 300 / XGBoost
# 400 MB) were invented and overstated the truth by 4-40x, and the model set
# included Prophet, which is a statistical BASELINE, not part of the ladder.
# These now read the same tables the thesis cites, so a re-run cannot drift from
# the results.
import csv as _csv
import json as _json

_PROFILING = THESIS_RESULTS_SRQ1_DIR / "tables" / "profiling.csv"
_METRICS = THESIS_RESULTS_SRQ1_DIR / "tables" / "metrics.csv"
_MODELS_DIR = THESIS_RESULTS_SRQ1_DIR / "models"


def _load_profiling() -> dict:
    """model -> {fit_s, peak_fit_RSS_MB, model_size_MB} from profiling.csv."""
    if not _PROFILING.is_file():
        raise SystemExit(f"missing {_PROFILING}; run srq1_profiling.py first")
    out = {}
    with _PROFILING.open(encoding="utf-8") as fh:
        for row in _csv.DictReader(fh):
            out[row["model"]] = row
    return out


def _load_ladder() -> list:
    """The model ladder actually benchmarked, ordered simple -> complex."""
    if not _METRICS.is_file():
        raise SystemExit(f"missing {_METRICS}; run srq1_benchmark.py first")
    with _METRICS.open(encoding="utf-8") as fh:
        found = {r["model"] for r in _csv.DictReader(fh)}
    order = ["SeasonalNaive", "Ridge", "LightGBM", "XGBoost"]
    return [m for m in order if m in found] + sorted(found - set(order))


def _load_served() -> dict:
    """category -> model name actually persisted for serving."""
    out = {}
    for meta in sorted(_MODELS_DIR.glob("*/metadata.json")):
        d = _json.loads(meta.read_text(encoding="utf-8"))
        out[meta.parent.name] = d.get("model", "?")
    return out


# RAM budget: mirrors export_appendix.py's RAM_BUDGET_MB so the diagrams and the
# appendix tables cannot disagree. NOTE (P0046): the thesis prose says "8 GB"
# while the exporter computes shares against 4096 MB -- a real inconsistency,
# flagged in the plan. This follows the exporter, which is what the appendix
# tables were computed with.
RAM_BUDGET_MB = 4096.0

PROF = _load_profiling()
LADDER = _load_ladder()
SERVED = _load_served()


def _ram(model: str) -> str:
    """Measured peak fit RSS for a model, as a label fragment."""
    r = PROF.get(model)
    return f"{float(r['peak_fit_RSS_MB']):.0f} MB" if r else "n/a"


def _ladder_label(sep: str = " \u2192 ") -> str:
    """The benchmarked ladder as a label, e.g. 'Ridge -> LightGBM -> XGBoost'."""
    return sep.join(m for m in LADDER if m != "SeasonalNaive")


def _max_fit_ram() -> str:
    """Largest measured peak fit RSS across the ladder, for a '<= N MB' claim."""
    vals = [float(PROF[m]["peak_fit_RSS_MB"]) for m in LADDER if m in PROF]
    return f"{max(vals):.0f} MB" if vals else "n/a"

# ── Shared palette ────────────────────────────────────────────────────────────
C = {
    "navy":     "#1B3A5C",
    "blue":     "#2E86AB",
    "teal":     "#1A936F",
    "amber":    "#C17817",
    "red":      "#C0392B",
    "grey":     "#5D6D7E",
    "ice":      "#EAF4FB",
    "mint":     "#E8F8F1",
    "cream":    "#FDFAF0",
    "blush":    "#FDEBD0",
    "cloud":    "#F4F6F9",
    "white":    "#FFFFFF",
    "charcoal": "#2C3E50",
}

FONT = "Helvetica Neue"


def save_dot(dot, name):
    path = os.path.join(OUTPUT_DIR, name)
    dot.render(path, format="svg", cleanup=True)
    dot.render(path, format="png", cleanup=True)
    print(f"  ✅  {name}.svg  +  {name}.png")


def save_mpl(fig, name):
    for ext in ["svg", "png"]:
        fig.savefig(os.path.join(OUTPUT_DIR, f"{name}.{ext}"),
                    format=ext, dpi=180, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✅  {name}.svg  +  {name}.png")


# ─────────────────────────────────────────────────────────────────────────────
# Fig 1 — System Architecture
# Layout: vertical spine (Coordinator centre), data sources top-left,
#         agents cascade right-of-centre, Claude API satellite right,
#         output bottom-centre.  No edge labels — all info is in nodes.
# ─────────────────────────────────────────────────────────────────────────────
def fig1_system_architecture():
    g = graphviz.Digraph(
        "system_architecture",
        graph_attr=dict(
            rankdir="TB",
            splines="spline",          # spline avoids ortho label-overlap warnings
            nodesep="0.55",
            ranksep="0.75",
            pad="0.4",
            fontname=FONT,
            fontsize="13",
            bgcolor=C["cloud"],
            label=f"System A  ·  Multi-Agent Research Framework  ·  {RAM_BUDGET_MB/1024:.0f} GB RAM Constraint",
            labelloc="b",
            labeljust="c",
        ),
    )

    N = dict(fontname=FONT, fontsize="10", style="filled,rounded",
             penwidth="1.8", margin="0.18,0.12")

    # ── Data sources cluster (top-left weight) ────────────────────────────────
    # Indeks Danmark node removed 2026-09-06 (P0046 F6): the dataset was never
    # used and is archived. An empty placeholder box is worse than no box.
    with g.subgraph(name="cluster_inputs") as c:
        c.attr(label="  Data Sources  ", style="dashed,rounded",
               color=C["blue"], fontcolor=C["blue"], fontname=FONT,
               fontsize="9", bgcolor="#EBF5FB", penwidth="1.2")
        c.node("nielsen",
               "Nielsen / Prometheus\nCSD Star Schema SQL\n36 months · 28 retailers",
               shape="cylinder", fillcolor=C["ice"], color=C["blue"], **N)
        
    # ── Coordinator (central spine) ───────────────────────────────────────────
    g.node("coord",
           "Coordinator\n──────────────\nLangGraph StateGraph\nPhase routing · State mgmt\nHuman approval gates",
           shape="box", fillcolor=C["navy"], fontcolor=C["white"],
           color=C["charcoal"], penwidth="2.5",
           fontname=FONT, fontsize="10", style="filled,rounded", margin="0.22,0.15")

    # ── Agent cluster (cascades down-right) ───────────────────────────────────
    with g.subgraph(name="cluster_agents") as c:
        c.attr(label="  Agent Layer  ", style="rounded",
               color=C["teal"], fontcolor=C["teal"], fontname=FONT,
               fontsize="9", bgcolor="#EEF9F4", penwidth="1.5")

        c.node("a_data",
               "Data Assessment Agent\nLoad · Validate · Feature Eng.\nPCA + k-means  ·  ~2 GB peak",
               shape="box", fillcolor=C["mint"], color=C["teal"], **N)
        c.node("a_forecast",
               f"Forecasting Agent\n{_ladder_label()}\n(sequential)\n\u2264 {_max_fit_ram()} peak fit RSS",
               shape="box", fillcolor=C["mint"], color=C["teal"], **N)
        c.node("a_synthesis",
               "Synthesis Agent\n① Inverse-WMAPE ensemble\n② Split-conformal 90% interval\n③ Confidence score  0–100\n④ LLM recommendation",
               shape="box", fillcolor=C["mint"], color=C["teal"], **N)
        c.node("a_valid",
               "Validation Agent\nLevel 1 · ML accuracy (WMAPE / MASE)\nLevel 2 · interval calibration\nLevel 3 · RAM + latency profile",
               shape="box", fillcolor=C["mint"], color=C["teal"], **N)

    # ── Claude API satellite (right) ──────────────────────────────────────────
    g.node("claude",
           "Claude API\nsonnet-4-6  ·  T = 0\n~0 MB local RAM",
           shape="diamond", fillcolor=C["blush"], color=C["amber"],
           fontname=FONT, fontsize="9", style="filled", penwidth="1.8",
           margin="0.14,0.10")

    # ── Output (bottom) ───────────────────────────────────────────────────────
    g.node("output",
           "Decision Output\nCalibrated forecast  +  90% interval\nConfidence score  ·  Natural language recommendation",
           shape="note", fillcolor=C["cream"], color=C["amber"],
           fontname=FONT, fontsize="10", style="filled", penwidth="1.8",
           margin="0.18,0.12")

    # ── Edges (no label= — all info lives in nodes) ───────────────────────────
    g.edge("nielsen",    "coord",      color=C["blue"],  penwidth="1.4", arrowsize="0.8")
    g.edge("coord",      "a_data",     color=C["navy"],  penwidth="1.6", arrowsize="0.9")
    g.edge("a_data",     "coord",      color=C["grey"],  penwidth="1.0", style="dashed", arrowsize="0.7")
    g.edge("coord",      "a_forecast", color=C["navy"],  penwidth="1.6", arrowsize="0.9")
    g.edge("a_forecast", "coord",      color=C["grey"],  penwidth="1.0", style="dashed", arrowsize="0.7")
    g.edge("coord",      "a_synthesis",color=C["navy"],  penwidth="1.6", arrowsize="0.9")
    g.edge("a_synthesis","claude",     color=C["amber"], penwidth="1.3", style="dashed", arrowsize="0.7")
    g.edge("claude",     "a_synthesis",color=C["amber"], penwidth="1.3", style="dashed", arrowsize="0.7")
    g.edge("a_synthesis","coord",      color=C["grey"],  penwidth="1.0", style="dashed", arrowsize="0.7")
    g.edge("coord",      "a_valid",    color=C["navy"],  penwidth="1.6", arrowsize="0.9")
    g.edge("a_valid",    "coord",      color=C["grey"],  penwidth="1.0", style="dashed", arrowsize="0.7")
    g.edge("coord",      "output",     color=C["amber"], penwidth="2.0", arrowsize="1.0")

    save_dot(g, "system_architecture_v1")


# ─────────────────────────────────────────────────────────────────────────────
# Fig 2 — LangGraph Execution Workflow
# Layout: left-to-right main spine; sequential model sub-cluster BELOW
#         the forecasting node (vertical drop, then right); retry arcs loop
#         back above the main spine.  xlabel= for all annotations.
# ─────────────────────────────────────────────────────────────────────────────
def fig2_agent_workflow():
    g = graphviz.Digraph(
        "agent_workflow",
        graph_attr=dict(
            rankdir="LR",
            splines="spline",
            nodesep="0.6",
            ranksep="1.1",
            pad="0.45",
            fontname=FONT,
            fontsize="13",
            bgcolor=C["cloud"],
            label="System A  ·  LangGraph Execution Workflow",
            labelloc="b",
            labeljust="c",
        ),
    )

    N = dict(fontname=FONT, fontsize="10", style="filled,rounded", penwidth="1.8", margin="0.16,0.11")
    Nd = dict(fontname=FONT, fontsize="10", style="filled", penwidth="2.0", margin="0.12,0.10")

    # ── Terminal nodes ────────────────────────────────────────────────────────
    g.node("start", "START", shape="circle", fillcolor=C["charcoal"],
           fontcolor=C["white"], width="0.65", height="0.65",
           fontname=FONT, fontsize="10", style="filled", fixedsize="true", penwidth="0")
    g.node("end", "END", shape="doublecircle", fillcolor=C["charcoal"],
           fontcolor=C["white"], width="0.65", height="0.65",
           fontname=FONT, fontsize="10", style="filled", fixedsize="true", penwidth="0")

    # ── Phase nodes ───────────────────────────────────────────────────────────
    g.node("n_data",
           "Data Assessment\nPhase 1",
           shape="box", fillcolor=C["ice"], color=C["blue"], **N)

    g.node("n_ap1", "APPROVAL\nPhase 1→2",
           shape="diamond", fillcolor=C["white"], color=C["red"],
           fontcolor=C["red"], **Nd)

    g.node("n_forecast",
           "Forecasting\nPhase 2",
           shape="box", fillcolor=C["mint"], color=C["teal"], **N)

    g.node("n_ap2", "APPROVAL\nPhase 2→3",
           shape="diamond", fillcolor=C["white"], color=C["red"],
           fontcolor=C["red"], **Nd)

    g.node("n_synthesis",
           "Synthesis\nPhase 3",
           shape="box", fillcolor=C["cream"], color=C["amber"], **N)

    g.node("n_ap3", "APPROVAL\nPhase 3→4",
           shape="diamond", fillcolor=C["white"], color=C["red"],
           fontcolor=C["red"], **Nd)

    g.node("n_valid",
           "Validation\nPhase 4",
           shape="box", fillcolor=C["blush"], color=C["red"], **N)

    # ── Sequential model sub-cluster (below forecasting node) ─────────────────
    with g.subgraph(name="cluster_seq") as c:
        c.attr(label="  Sequential execution  ·  load → fit → predict → del → gc.collect()  ",
               style="dashed,rounded", color=C["grey"], fontcolor=C["grey"],
               fontname=FONT, fontsize="8.5", bgcolor="#F8F9FA", penwidth="1.0")
        Nm = dict(fontname=FONT, fontsize="9", style="filled,rounded",
                  penwidth="1.2", margin="0.12,0.08", width="1.0", height="0.55", fixedsize="true")
        for nid, label, ram in [
            # Measured: node set from metrics.csv, MB from profiling.csv (P0046).
            *[(f"m_{mdl.lower()}", f"{mdl}\n{_ram(mdl)}", C["ice"])
              for mdl in LADDER if mdl != "SeasonalNaive"],
        ]:
            c.node(nid, label, shape="box", fillcolor=ram, color=C["grey"], **Nm)
        # Chain derived from LADDER, like the nodes above. Was a hardcoded
        # ridge->arima->prophet->lgbm->xgb sequence, which kept referencing
        # m_arima/m_prophet after those nodes were removed -- graphviz then
        # silently created empty unlabelled nodes for the dangling ids.
        _chain = [f"m_{m.lower()}" for m in LADDER if m != "SeasonalNaive"]
        for _a, _b in zip(_chain, _chain[1:]):
            c.edge(_a, _b, color=C["grey"], penwidth="1.0", arrowsize="0.6")

    # ── Main flow edges ───────────────────────────────────────────────────────
    g.edge("start",      "n_data",     color=C["charcoal"], penwidth="1.8", arrowsize="0.9")
    g.edge("n_data",     "n_ap1",      color=C["navy"],     penwidth="1.6", arrowsize="0.9")

    # approval → next or retry (use xlabel to keep text off the arrow)
    g.edge("n_ap1", "n_forecast", color=C["teal"],  penwidth="1.6", arrowsize="0.9",
           xlabel="approved")
    g.edge("n_ap1", "n_data",     color=C["red"],   penwidth="1.0", arrowsize="0.7",
           style="dashed", xlabel="retry", constraint="false")

    # dashed connectors to/from sub-cluster
    g.edge("n_forecast", _chain[0],   color=C["grey"], penwidth="1.0", style="dashed", arrowsize="0.7")
    g.edge(_chain[-1],   "n_ap2",     color=C["grey"], penwidth="1.0", style="dashed", arrowsize="0.7")

    g.edge("n_ap2", "n_synthesis", color=C["amber"], penwidth="1.6", arrowsize="0.9",
           xlabel="approved")
    g.edge("n_ap2", "n_forecast",  color=C["red"],   penwidth="1.0", arrowsize="0.7",
           style="dashed", xlabel="retry", constraint="false")

    g.edge("n_synthesis", "n_ap3",   color=C["navy"],  penwidth="1.6", arrowsize="0.9")
    g.edge("n_ap3", "n_valid",       color=C["red"],   penwidth="1.6", arrowsize="0.9",
           xlabel="approved")
    g.edge("n_ap3", "n_synthesis",   color=C["red"],   penwidth="1.0", arrowsize="0.7",
           style="dashed", xlabel="retry", constraint="false")

    g.edge("n_valid", "end", color=C["charcoal"], penwidth="1.8", arrowsize="0.9")

    save_dot(g, "agent_workflow_v1")


# ─────────────────────────────────────────────────────────────────────────────
# Fig 3 — Data Flow
# Layout: two sources at top (slightly asymmetric widths), processing tier
#         in middle, outputs fanning out at bottom.  GC node placed as a
#         right-side satellite off the sources tier.  No edge labels.
# ─────────────────────────────────────────────────────────────────────────────
def fig3_data_flow():
    g = graphviz.Digraph(
        "data_flow",
        graph_attr=dict(
            rankdir="TB",
            splines="spline",
            nodesep="0.7",
            ranksep="0.8",
            pad="0.45",
            fontname=FONT,
            fontsize="13",
            bgcolor=C["cloud"],
            label="System A  ·  Data Flow through LangGraph ResearchState",
            labelloc="b",
            labeljust="c",
        ),
    )

    N = dict(fontname=FONT, fontsize="10", style="filled,rounded",
             penwidth="1.8", margin="0.18,0.12")

    # ── Tier 0: raw sources ───────────────────────────────────────────────────
    with g.subgraph() as s:
        s.attr(rank="same")
        g.node("raw_nielsen",
               "Raw Nielsen\nfacts + dimensions\n~ 500 MB – 1 GB",
               shape="cylinder", fillcolor=C["ice"], color=C["blue"], **N)
        
    # ── GC satellite (right of sources) ──────────────────────────────────────
    g.node("gc",
           "del  +  gc.collect()\n~ 1.5 GB freed",
           shape="hexagon", fillcolor="#FDECEA", color=C["red"],
           fontname=FONT, fontsize="9", style="filled", penwidth="1.5",
           margin="0.10,0.08")

    # ── Tier 1: processed features ────────────────────────────────────────────
    with g.subgraph() as s:
        s.attr(rank="same")
        g.node("feat",
               "Feature Matrix\nbrand × retailer × period\nlag / rolling / promo / calendar\n~ 200–300 MB",
               shape="box", fillcolor=C["mint"], color=C["teal"], **N)
        # "Consumer Signals" (PCA -> k-means on the survey) removed with the Indeks
        # source it derived from: no survey, no segments. P0046 F6.
        g.node("quality",
               "Data Quality Report\nmissing values · outliers\ncoverage flags\nSaved → docs/data/",
               shape="note", fillcolor=C["white"], color=C["grey"],
               fontname=FONT, fontsize="9", style="filled", penwidth="1.2",
               margin="0.14,0.10")

    # ── Tier 2: model outputs ─────────────────────────────────────────────────
    g.node("forecasts",
           f"{len([m for m in LADDER if m != 'SeasonalNaive'])} \u00d7  ModelForecast\npoint  \u00b7  lower_90  \u00b7  upper_90\nWMAPE  \u00b7  MASE  \u00b7  peak_RAM_MB",
           shape="box", fillcolor=C["cream"], color=C["amber"], **N)

    # ── Tier 3: synthesis output ──────────────────────────────────────────────
    g.node("synthesis",
           "SynthesisOutput\nensemble_forecast  ·  calibrated_interval\nconfidence_score  0–100\nrecommendation_text",
           shape="box", fillcolor=C["blush"], color=C["amber"], **N)

    # ── Tier 4: validation report ─────────────────────────────────────────────
    g.node("validation",
           "ValidationReport\nWMAPE / MASE / DM-test\nsplit-conformal interval coverage\nRAM profile  \u00b7  latency",
           shape="note", fillcolor=C["ice"], color=C["blue"],
           fontname=FONT, fontsize="10", style="filled", penwidth="1.8",
           margin="0.18,0.12")

    # ── Edges ─────────────────────────────────────────────────────────────────
    # Sources → processing
    g.edge("raw_nielsen", "feat",     color=C["blue"],  penwidth="1.5", arrowsize="0.8")
    g.edge("raw_nielsen", "quality",  color=C["grey"],  penwidth="1.0", style="dashed", arrowsize="0.7")
    # Sources freed
    g.edge("raw_nielsen", "gc",       color=C["red"],   penwidth="1.0", style="dashed", arrowsize="0.7")
    # Features → forecasts
    g.edge("feat",    "forecasts",    color=C["teal"],  penwidth="1.6", arrowsize="0.9")
    # Forecasts → synthesis
    g.edge("forecasts", "synthesis",  color=C["amber"], penwidth="1.6", arrowsize="0.9")
    # Outputs → validation
    g.edge("forecasts",  "validation",color=C["blue"],  penwidth="1.3", style="dashed", arrowsize="0.8")
    g.edge("synthesis",  "validation",color=C["amber"], penwidth="1.6", arrowsize="0.9")

    save_dot(g, "data_flow_v1")


# ─────────────────────────────────────────────────────────────────────────────
# Fig 4 — RAM Budget  (matplotlib, horizontal grouped + total bar)
# Asymmetry: two column groups (always-on vs. peak phases), distinct colours,
#            large 8 GB limit line, clean minimal style.
# ─────────────────────────────────────────────────────────────────────────────
# fig4_ram_budget() REMOVED 2026-09-06 (P0046). Brian: "archive, we don't need
# that diagram either way." Its seven bar values were fabricated (P0040 F5) and
# included an "Indeks raw load" bar for a dataset that was never used. The real
# resource numbers live in 05_thesis_results/appendix/{02_substrate,
# 04_sandbox}_resource_profile and in srq1_model_performance/tables/profiling.csv,
# which is what fig1/fig2/fig6 now read. Source preserved at
# 05_thesis_results/diagrams/.archive/fabricated_ram_budget_2026-09/.


def fig5_confidence_score():
    plt.rcParams.update({"font.family": "sans-serif"})

    components = [
        {
            "pct": "40 %",
            "title": "Calibrated\nInterval Width",
            "desc": "Narrower 90 % prediction\ninterval → higher confidence\n(Kuleshov et al., 2018)",
            "formula": "width_score",
            "bg": C["ice"],
            "edge": C["blue"],
            "txt": C["navy"],
        },
        {
            "pct": "30 %",
            "title": "Inter-Model\nAgreement",
            "desc": f"Lower spread across\n{len([m for m in LADDER if m != 'SeasonalNaive'])} model forecasts\n\u2192 higher confidence",
            "formula": "agreement_score",
            "bg": C["mint"],
            "edge": C["teal"],
            "txt": "#0E6655",
        },
        {
            "pct": "30 %",
            "title": "Model\nAccuracy",
            "desc": "Lower historical WMAPE\nacross the ensemble\n→ higher confidence",
            "formula": "accuracy_score",
            "bg": C["blush"],
            "edge": C["amber"],
            "txt": "#784212",
        },
    ]

    fig = plt.figure(figsize=(11, 5.5))
    fig.patch.set_facecolor(C["cloud"])

    # Title row
    fig.text(0.5, 0.96,
             "Composite Confidence Score  ·  Range 0 – 100",
             ha="center", va="top", fontsize=13, fontweight="bold",
             color=C["charcoal"])

    # Formula row
    fig.text(0.5, 0.89,
             "Score  =  0.40 × width_score  +  0.30 × agreement_score  +  0.30 × accuracy_score",
             ha="center", va="top", fontsize=10, color=C["grey"],
             fontfamily="monospace")

    # Three cards
    card_w, card_h = 0.26, 0.56
    starts_x = [0.07, 0.37, 0.67]
    card_bottom = 0.14

    for i, comp in enumerate(components):
        x0 = starts_x[i]

        # Card rectangle
        rect = mpatches.FancyBboxPatch(
            (x0, card_bottom), card_w, card_h,
            boxstyle="round,pad=0.015",
            linewidth=2.2,
            edgecolor=comp["edge"],
            facecolor=comp["bg"],
            transform=fig.transFigure,
            zorder=2,
        )
        fig.add_artist(rect)

        cx = x0 + card_w / 2

        # Weight (large)
        fig.text(cx, card_bottom + card_h - 0.065, comp["pct"],
                 ha="center", va="top", fontsize=26, fontweight="bold",
                 color=comp["edge"], transform=fig.transFigure)

        # Divider line (drawn as a thin rectangle)
        div = mpatches.Rectangle(
            (x0 + 0.02, card_bottom + card_h - 0.17), card_w - 0.04, 0.004,
            facecolor=comp["edge"], alpha=0.35,
            transform=fig.transFigure, zorder=3,
        )
        fig.add_artist(div)

        # Title
        fig.text(cx, card_bottom + card_h - 0.20, comp["title"],
                 ha="center", va="top", fontsize=10.5, fontweight="bold",
                 color=comp["txt"], transform=fig.transFigure)

        # Description
        fig.text(cx, card_bottom + card_h - 0.34, comp["desc"],
                 ha="center", va="top", fontsize=8.8, color=C["grey"],
                 transform=fig.transFigure, linespacing=1.5)

        # Formula term
        fig.text(cx, card_bottom + 0.03, comp["formula"],
                 ha="center", va="bottom", fontsize=8.5,
                 color=comp["edge"], fontfamily="monospace",
                 transform=fig.transFigure)

    # Tier legend at bottom
    tier_data = [
        (0.18, "≥ 70", "High confidence",     C["teal"]),
        (0.50, "40–69", "Moderate confidence", C["amber"]),
        (0.82, "< 40",  "Low confidence",      C["red"]),
    ]
    fig.text(0.5, 0.08, "Score tiers:", ha="center", va="top",
             fontsize=8.5, color=C["grey"], transform=fig.transFigure)
    for tx, score, label, col in tier_data:
        fig.text(tx, 0.04, f"{score}\n{label}", ha="center", va="top",
                 fontsize=8, color=col, fontweight="bold",
                 transform=fig.transFigure)

    save_mpl(fig, "confidence_score_v1")


# ─────────────────────────────────────────────────────────────────────────────
# Fig 6 — Project Overview  (System A; System B removed 2026-09-06, P0046 F4)
# Layout: two vertical clusters side-by-side (LR rankdir).
#   Left  → System A: research artefact (evaluated in thesis)
# ─────────────────────────────────────────────────────────────────────────────
def fig6_project_overview():
    g = graphviz.Digraph(
        "project_overview",
        graph_attr=dict(
            rankdir="LR",
            splines="spline",
            nodesep="0.5",
            ranksep="1.2",
            pad="0.5",
            fontname=FONT,
            fontsize="14",
            bgcolor=C["cloud"],
            label="Manifold AI Thesis  ·  System A Predictive Analytics Framework  ·  CBS 2026",
            labelloc="b",
            labeljust="c",
        ),
    )

    NA = dict(fontname=FONT, fontsize="9.5", style="filled,rounded",
              penwidth="1.6", margin="0.16,0.10")
    NB = dict(fontname=FONT, fontsize="9",   style="filled,rounded",
              penwidth="1.4", margin="0.14,0.09")

    # ── Anchor nodes (invisible) force side-by-side layout ────────────────────
    g.node("anchor_a", "", shape="point", width="0", style="invis")
    g.node("anchor_b", "", shape="point", width="0", style="invis")
    with g.subgraph() as s:
        s.attr(rank="same")
        s.node("anchor_a")
        s.node("anchor_b")
    g.edge("anchor_a", "anchor_b", style="invis", weight="10")

    # ══════════════════════════════════════════════════════════════════════════
    # SYSTEM A  — left cluster
    # ══════════════════════════════════════════════════════════════════════════
    with g.subgraph(name="cluster_sysA") as ca:
        ca.attr(
            label="  System A  ·  Research Framework  (thesis artefact)  ",
            style="rounded",
            color=C["navy"],
            fontcolor=C["navy"],
            fontname=FONT,
            fontsize="10.5",
            bgcolor="#EAF2FB",
            penwidth="2.2",
        )

        # Coordinator spine
        ca.node("a_coord",
                "Coordinator\n──────────────\nLangGraph StateGraph\nPhase routing\nHuman approval gates",
                shape="box", fillcolor=C["navy"], fontcolor=C["white"],
                color=C["charcoal"], penwidth="2.5",
                fontname=FONT, fontsize="9.5", style="filled,rounded",
                margin="0.20,0.14")

        # Data sources sub-cluster
        with ca.subgraph(name="cluster_sysA_data") as ds:
            ds.attr(label="  Data Sources  ", style="dashed,rounded",
                    color=C["blue"], fontcolor=C["blue"],
                    fontname=FONT, fontsize="8.5",
                    bgcolor="#EBF5FB", penwidth="1.0")
            ds.node("a_src_nielsen",
                    "Nielsen CSD\n28 retailers · 36 months",
                    shape="cylinder", fillcolor=C["ice"], color=C["blue"], **NA)
            
        # Agent stack
        with ca.subgraph(name="cluster_sysA_agents") as aa:
            aa.attr(label="  Agent Layer  ", style="rounded",
                    color=C["teal"], fontcolor=C["teal"],
                    fontname=FONT, fontsize="8.5",
                    bgcolor="#EEF9F4", penwidth="1.3")
            aa.node("a_ag1",
                    "① Data Assessment\nLoad · Validate · Feature Eng.\nPCA + k-means  ·  ~2 GB peak",
                    shape="box", fillcolor=C["mint"], color=C["teal"], **NA)
            aa.node("a_ag2",
                    f"\u2461 Forecasting\n{_ladder_label()}\n(sequential, \u2264 {_max_fit_ram()} peak RSS)",
                    shape="box", fillcolor=C["mint"], color=C["teal"], **NA)
            aa.node("a_ag3",
                    "③ Synthesis\nInverse-WMAPE ensemble\nSplit-conformal interval\nConfidence 0–100 · Claude API",
                    shape="box", fillcolor=C["mint"], color=C["teal"], **NA)
            aa.node("a_ag4",
                    "\u2463 Validation\nLevel 1 \u00b7 ML accuracy\nLevel 2 \u00b7 interval calibration\nLevel 3 \u00b7 RAM + latency",
                    shape="box", fillcolor=C["mint"], color=C["teal"], **NA)
            aa.edge("a_ag1", "a_ag2", color=C["teal"], penwidth="1.2", arrowsize="0.7")
            aa.edge("a_ag2", "a_ag3", color=C["teal"], penwidth="1.2", arrowsize="0.7")
            aa.edge("a_ag3", "a_ag4", color=C["teal"], penwidth="1.2", arrowsize="0.7")

        # Output node
        ca.node("a_out",
                "Decision Output\nCalibrated forecast  +  90% PI\nConfidence score  ·  Recommendation",
                shape="note", fillcolor=C["cream"], color=C["amber"],
                fontname=FONT, fontsize="9", style="filled",
                penwidth="1.8", margin="0.16,0.10")

        # System A internal edges
        ca.edge("a_src_nielsen", "a_coord", color=C["blue"], penwidth="1.3", arrowsize="0.75")
        ca.edge("a_coord", "a_ag1", color=C["navy"], penwidth="1.5", arrowsize="0.85")
        ca.edge("a_ag4",   "a_out", color=C["amber"], penwidth="1.7", arrowsize="0.9")
        # Return arcs (dashed)
        ca.edge("a_ag1", "a_coord", color=C["grey"], penwidth="0.9",
                style="dashed", arrowsize="0.6", constraint="false")
        ca.edge("a_ag4", "a_coord", color=C["grey"], penwidth="0.9",
                style="dashed", arrowsize="0.6", constraint="false")

    # ══════════════════════════════════════════════════════════════════════════
    # SYSTEM B  — right cluster
    # ══════════════════════════════════════════════════════════════════════════
    # System B block REMOVED 2026-09-06 (P0046 F4). It depicted the multi-agent
    # THESIS WRITING system -- Thesis Coordinator, Writing/Critic/Planner/Diagram
    # agents -- which was never built; its standalone diagram was archived the
    # same day. Roughly half this figure was scaffolding for an abandoned design,
    # labelled "not in thesis" while sitting in a thesis figure.
    # The figure is now System A only, which is the actual artefact.

    save_dot(g, "project_overview_v1")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\nGenerating thesis figures  (v2)...\n")
    fig1_system_architecture()
    fig2_agent_workflow()
    fig3_data_flow()
    fig5_confidence_score()
    fig6_project_overview()
    print(f"\nDone — all figures in  {OUTPUT_DIR}/")
