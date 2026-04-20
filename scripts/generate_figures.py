"""
Thesis figure generation — v2
- No text/box/arrow overlaps (uses xlabel= for edge annotations, not label=)
- Asymmetric layout: each figure has its own intentional visual hierarchy
- Consistent colour palette across all figures
- Outputs SVG + PNG to thesis/writing/figures/
"""
import os
import graphviz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUTPUT_DIR = "thesis/writing/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

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
            label="System A  ·  Multi-Agent Research Framework  ·  8 GB RAM Constraint",
            labelloc="b",
            labeljust="c",
        ),
    )

    N = dict(fontname=FONT, fontsize="10", style="filled,rounded",
             penwidth="1.8", margin="0.18,0.12")

    # ── Data sources cluster (top-left weight) ────────────────────────────────
    with g.subgraph(name="cluster_inputs") as c:
        c.attr(label="  Data Sources  ", style="dashed,rounded",
               color=C["blue"], fontcolor=C["blue"], fontname=FONT,
               fontsize="9", bgcolor="#EBF5FB", penwidth="1.2")
        c.node("nielsen",
               "Nielsen / Prometheus\nCSD Star Schema SQL\n36 months · 28 retailers",
               shape="cylinder", fillcolor=C["ice"], color=C["blue"], **N)
        c.node("indeks",
               "Indeks Danmark\nConsumer Survey\n20,134 resp. · 6,364 vars",
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
               "Forecasting Agent\nARIMA → Prophet → LightGBM\n→ XGBoost → Ridge  (sequential)\n≤ 512 MB / model",
               shape="box", fillcolor=C["mint"], color=C["teal"], **N)
        c.node("a_synthesis",
               "Synthesis Agent\n① Ensemble weighting\n② Interval calibration  (Kuleshov 2018)\n③ Consumer signal adjustment\n④ Confidence score  0–100\n⑤ LLM recommendation",
               shape="box", fillcolor=C["mint"], color=C["teal"], **N)
        c.node("a_valid",
               "Validation Agent\nLevel 1 · ML accuracy (MAPE / RMSE)\nLevel 2 · LLM-as-Judge  N = 50\nLevel 3 · RAM + latency profile",
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
    g.edge("indeks",     "coord",      color=C["blue"],  penwidth="1.4", arrowsize="0.8")
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
            ("m_ridge",  "Ridge\n15 MB",     C["ice"]),
            ("m_arima",  "ARIMA\n20 MB",     C["ice"]),
            ("m_prophet","Prophet\n200 MB",  C["mint"]),
            ("m_lgbm",   "LightGBM\n300 MB", C["mint"]),
            ("m_xgb",    "XGBoost\n400 MB",  C["mint"]),
        ]:
            c.node(nid, label, shape="box", fillcolor=ram, color=C["grey"], **Nm)
        c.edge("m_ridge",  "m_arima",   color=C["grey"], penwidth="1.0", arrowsize="0.6")
        c.edge("m_arima",  "m_prophet", color=C["grey"], penwidth="1.0", arrowsize="0.6")
        c.edge("m_prophet","m_lgbm",    color=C["grey"], penwidth="1.0", arrowsize="0.6")
        c.edge("m_lgbm",   "m_xgb",    color=C["grey"], penwidth="1.0", arrowsize="0.6")

    # ── Main flow edges ───────────────────────────────────────────────────────
    g.edge("start",      "n_data",     color=C["charcoal"], penwidth="1.8", arrowsize="0.9")
    g.edge("n_data",     "n_ap1",      color=C["navy"],     penwidth="1.6", arrowsize="0.9")

    # approval → next or retry (use xlabel to keep text off the arrow)
    g.edge("n_ap1", "n_forecast", color=C["teal"],  penwidth="1.6", arrowsize="0.9",
           xlabel="approved")
    g.edge("n_ap1", "n_data",     color=C["red"],   penwidth="1.0", arrowsize="0.7",
           style="dashed", xlabel="retry", constraint="false")

    # dashed connectors to/from sub-cluster
    g.edge("n_forecast", "m_ridge",   color=C["grey"], penwidth="1.0", style="dashed", arrowsize="0.7")
    g.edge("m_xgb",      "n_ap2",     color=C["grey"], penwidth="1.0", style="dashed", arrowsize="0.7")

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
        g.node("raw_indeks",
               "Raw Indeks Danmark\n20,134 rows  ×  6,364 cols\n~ 970 MB",
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
        g.node("signals",
               "Consumer Signals\nPCA  →  k-means  →  segments\nretailer demand index\ntrend direction",
               shape="box", fillcolor=C["mint"], color=C["teal"], **N)
        g.node("quality",
               "Data Quality Report\nmissing values · outliers\ncoverage flags\nSaved → docs/data/",
               shape="note", fillcolor=C["white"], color=C["grey"],
               fontname=FONT, fontsize="9", style="filled", penwidth="1.2",
               margin="0.14,0.10")

    # ── Tier 2: model outputs ─────────────────────────────────────────────────
    g.node("forecasts",
           "5 ×  ModelForecast\npoint  ·  lower_90  ·  upper_90\nMAPE  ·  RMSE  ·  peak_RAM_MB",
           shape="box", fillcolor=C["cream"], color=C["amber"], **N)

    # ── Tier 3: synthesis output ──────────────────────────────────────────────
    g.node("synthesis",
           "SynthesisOutput\nensemble_forecast  ·  calibrated_interval\nconfidence_score  0–100\nrecommendation_text",
           shape="box", fillcolor=C["blush"], color=C["amber"], **N)

    # ── Tier 4: validation report ─────────────────────────────────────────────
    g.node("validation",
           "ValidationReport\nMAPE / RMSE / DM-test\nLLM-as-Judge scores  (N = 50)\nRAM profile  ·  latency",
           shape="note", fillcolor=C["ice"], color=C["blue"],
           fontname=FONT, fontsize="10", style="filled", penwidth="1.8",
           margin="0.18,0.12")

    # ── Edges ─────────────────────────────────────────────────────────────────
    # Sources → processing
    g.edge("raw_nielsen", "feat",     color=C["blue"],  penwidth="1.5", arrowsize="0.8")
    g.edge("raw_indeks",  "signals",  color=C["blue"],  penwidth="1.5", arrowsize="0.8")
    g.edge("raw_nielsen", "quality",  color=C["grey"],  penwidth="1.0", style="dashed", arrowsize="0.7")
    g.edge("raw_indeks",  "quality",  color=C["grey"],  penwidth="1.0", style="dashed", arrowsize="0.7")
    # Sources freed
    g.edge("raw_nielsen", "gc",       color=C["red"],   penwidth="1.0", style="dashed", arrowsize="0.7")
    g.edge("raw_indeks",  "gc",       color=C["red"],   penwidth="1.0", style="dashed", arrowsize="0.7")
    # Features → forecasts
    g.edge("feat",    "forecasts",    color=C["teal"],  penwidth="1.6", arrowsize="0.9")
    g.edge("signals", "forecasts",    color=C["teal"],  penwidth="1.3", style="dashed", arrowsize="0.8")
    # Forecasts → synthesis
    g.edge("forecasts", "synthesis",  color=C["amber"], penwidth="1.6", arrowsize="0.9")
    g.edge("signals",   "synthesis",  color=C["teal"],  penwidth="1.3", style="dashed", arrowsize="0.8")
    # Outputs → validation
    g.edge("forecasts",  "validation",color=C["blue"],  penwidth="1.3", style="dashed", arrowsize="0.8")
    g.edge("synthesis",  "validation",color=C["amber"], penwidth="1.6", arrowsize="0.9")

    save_dot(g, "data_flow_v1")


# ─────────────────────────────────────────────────────────────────────────────
# Fig 4 — RAM Budget  (matplotlib, horizontal grouped + total bar)
# Asymmetry: two column groups (always-on vs. peak phases), distinct colours,
#            large 8 GB limit line, clean minimal style.
# ─────────────────────────────────────────────────────────────────────────────
def fig4_ram_budget():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
    })

    # Components with (label, MB, colour-key, group)
    items = [
        ("Python runtime\n+ libraries",     500,  "blue",  "always"),
        ("LangGraph\nstate",                100,  "blue",  "always"),
        ("Feature matrix\n(post-extract)",  300,  "teal",  "always"),
        ("Active ML model\n(worst case)",   512,  "teal",  "peak"),
        ("Nielsen raw load",               1000,  "navy",  "peak"),
        ("Indeks raw load",                 970,  "navy",  "peak"),
        ("Synthesis state\n+ LLM buffer",   250,  "amber", "peak"),
    ]
    labels = [x[0] for x in items]
    values = [x[1] for x in items]
    colours_map = {"blue": C["blue"], "teal": C["teal"],
                   "navy": C["navy"], "amber": C["amber"]}
    bar_colours = [colours_map[x[2]] for x in items]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    fig.patch.set_facecolor(C["cloud"])
    ax.set_facecolor(C["cloud"])

    y = np.arange(len(items))
    bars = ax.barh(y, values, color=bar_colours, edgecolor="white",
                   linewidth=0.8, height=0.62, zorder=3)

    # 8 GB hard limit
    ax.axvline(8192, color=C["red"], linewidth=2.0, linestyle="--", zorder=4,
               label="8 GB hard limit  (8,192 MB)")
    # 50 % guideline
    ax.axvline(4096, color=C["amber"], linewidth=1.2, linestyle=":",
               zorder=4, label="50 % budget  (4,096 MB)")
    # Peak estimate marker
    total = sum(values)
    ax.axvline(total, color=C["teal"], linewidth=1.5, linestyle="-.",
               zorder=4, label=f"Worst-case peak  ({total:,} MB)")

    # Value labels inside bars (right-aligned)
    for bar, val in zip(bars, values):
        xpos = min(val - 30, val * 0.92)
        ax.text(xpos, bar.get_y() + bar.get_height() / 2,
                f"{val:,} MB", va="center", ha="right",
                fontsize=8.5, color="white", fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_xlabel("Peak RAM  (MB)", fontsize=10, labelpad=8)
    ax.set_xlim(0, 9000)
    ax.set_title("System A  ·  RAM Budget by Component",
                 fontsize=12, fontweight="bold", pad=12)
    ax.tick_params(axis="x", labelsize=9)
    ax.xaxis.grid(True, color="white", linewidth=0.8, zorder=0)

    # Group labels on right margin
    for i, (_, _, _, grp) in enumerate(items):
        colour = C["blue"] if grp == "always" else C["red"]
        ax.text(8900, i, grp, va="center", ha="right",
                fontsize=7.5, color=colour, alpha=0.7)

    ax.legend(loc="lower right", fontsize=8.5, framealpha=0.7,
              facecolor=C["cloud"], edgecolor="none")
    fig.tight_layout(pad=1.5)
    save_mpl(fig, "ram_budget_v1")


# ─────────────────────────────────────────────────────────────────────────────
# Fig 5 — Confidence Score Composition  (matplotlib, card-based)
# Three vertical cards with weights, short description, formula at top,
# tier legend at bottom.  No horizontal bar — each component is its own box.
# ─────────────────────────────────────────────────────────────────────────────
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
            "desc": "Lower spread across\n5 model forecasts\n→ higher confidence",
            "formula": "agreement_score",
            "bg": C["mint"],
            "edge": C["teal"],
            "txt": "#0E6655",
        },
        {
            "pct": "30 %",
            "title": "Consumer Signal\nAlignment",
            "desc": "Indeks Danmark demand\nindex directionally consistent\n→ higher confidence",
            "formula": "signal_score",
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
             "Score  =  0.40 × width_score  +  0.30 × agreement_score  +  0.30 × signal_score",
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
# Fig 6 — Project Overview  (combined System A + System B)
# Layout: two vertical clusters side-by-side (LR rankdir).
#   Left  → System A: research artefact (evaluated in thesis)
#   Right → System B: thesis production scaffolding (invisible to readers)
# Asymmetry: System A has a deeper agent stack; System B has a wider agent fan.
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
            label="Manifold AI Thesis  ·  Predictive Analytics Framework  ·  CBS 2026",
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
            ds.node("a_src_indeks",
                    "Indeks Danmark\n20,134 resp. · 6,364 vars",
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
                    "② Forecasting\nRidge → ARIMA → Prophet\n→ LightGBM → XGBoost\n(sequential, ≤ 512 MB each)",
                    shape="box", fillcolor=C["mint"], color=C["teal"], **NA)
            aa.node("a_ag3",
                    "③ Synthesis\nEnsemble · Calibration\nConsumer signals\nConfidence 0–100 · Claude API",
                    shape="box", fillcolor=C["mint"], color=C["teal"], **NA)
            aa.node("a_ag4",
                    "④ Validation\nLevel 1 · ML accuracy\nLevel 2 · LLM-as-Judge\nLevel 3 · RAM + latency",
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
        ca.edge("a_src_indeks",  "a_coord", color=C["blue"], penwidth="1.3", arrowsize="0.75")
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
    with g.subgraph(name="cluster_sysB") as cb:
        cb.attr(
            label="  System B  ·  Thesis Production System  (scaffolding — not in thesis)  ",
            style="rounded",
            color=C["grey"],
            fontcolor=C["grey"],
            fontname=FONT,
            fontsize="10.5",
            bgcolor="#F4F6F9",
            penwidth="1.8",
        )

        # Thesis state
        cb.node("b_state",
                "ThesisState  (Pydantic JSON)\nsection status · corpus · figures\ncompliance · experiment log",
                shape="box", fillcolor=C["ice"], color=C["blue"],
                fontname=FONT, fontsize="9", style="filled,rounded",
                penwidth="1.6", margin="0.18,0.12")

        # Coordinator
        cb.node("b_coord",
                "Thesis Coordinator\n──────────────\nPlan → Execute → Critic loop\nRetries once on invalid output",
                shape="box", fillcolor=C["navy"], fontcolor=C["white"],
                color=C["charcoal"], penwidth="2.2",
                fontname=FONT, fontsize="9.5", style="filled,rounded",
                margin="0.18,0.12")

        # Planner + Critic row (top tier of agents)
        with cb.subgraph() as s:
            s.attr(rank="same")
            cb.node("b_planner",
                    "Planner\nTaskPlan JSON\n5 priority rules",
                    shape="box", fillcolor=C["cream"], color=C["amber"], **NB)
            cb.node("b_critic",
                    "Critic\nValidates all outputs\nPer-agent validators",
                    shape="box", fillcolor=C["blush"], color=C["red"], **NB)

        # Main agent fan (two columns)
        with cb.subgraph(name="cluster_sysB_agents") as ba:
            ba.attr(label="  Specialist Agents  ", style="dashed,rounded",
                    color=C["grey"], fontcolor=C["grey"],
                    fontname=FONT, fontsize="8.5",
                    bgcolor="#FAFBFC", penwidth="1.0")

            # Column 1
            for nid, lbl in [
                ("b_lit",     "Literature\nCorpus management\nAnnotation tracking"),
                ("b_writing", "Writing\nBullet points only\nNo prose"),
                ("b_comply",  "Compliance\nCBS checks · APA 7\nPage count"),
            ]:
                ba.node(nid, lbl, shape="box", fillcolor=C["white"],
                        color=C["grey"], **NB)

            # Column 2
            for nid, lbl in [
                ("b_diag",    "Diagram\nGraphviz + Matplotlib\nSVG + PNG"),
                ("b_tracker", "Experiment\nTracker\nAppend-only registry"),
                ("b_tables",  "Results\nTables & Viz\nMAPE / RAM / SRQ3"),
            ]:
                ba.node(nid, lbl, shape="box", fillcolor=C["white"],
                        color=C["grey"], **NB)

        # System B internal edges
        cb.edge("b_state",  "b_coord",  color=C["blue"],  penwidth="1.4", arrowsize="0.8")
        cb.edge("b_coord",  "b_planner",color=C["navy"],  penwidth="1.3", arrowsize="0.8")
        cb.edge("b_coord",  "b_critic", color=C["navy"],  penwidth="1.3", arrowsize="0.8")
        for nid in ["b_lit", "b_writing", "b_comply", "b_diag", "b_tracker", "b_tables"]:
            cb.edge("b_coord", nid, color=C["grey"], penwidth="0.9",
                    arrowsize="0.65", style="dashed")

    # ── Cross-system note: System B reads System A outputs ────────────────────
    g.node("note_read",
           "System B reads\nSystem A outputs\n(never modifies)",
           shape="note", fillcolor="#FDFAF0", color=C["amber"],
           fontname=FONT, fontsize="8.5", style="filled",
           penwidth="1.2", margin="0.10,0.08")
    g.edge("a_out",    "note_read", color=C["amber"], penwidth="1.0",
           style="dashed", arrowsize="0.6")
    g.edge("note_read","b_state",   color=C["amber"], penwidth="1.0",
           style="dashed", arrowsize="0.6")

    save_dot(g, "project_overview_v1")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\nGenerating thesis figures  (v2)...\n")
    fig1_system_architecture()
    fig2_agent_workflow()
    fig3_data_flow()
    fig4_ram_budget()
    fig5_confidence_score()
    fig6_project_overview()
    print(f"\nDone — all figures in  {OUTPUT_DIR}/")
