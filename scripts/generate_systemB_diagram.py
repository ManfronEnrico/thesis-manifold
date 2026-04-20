"""
System B — Thesis Production System diagram.
Clean top-to-bottom flow, no overlaps.
Output: thesis/thesis-writing/figures/system_b_overview.{svg,png}
Run: python3 scripts/generate_systemB_diagram.py
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUTPUT_DIR = "thesis/thesis-writing/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NAVY   = "#1B3A5C"
BLUE   = "#2E86AB"
TEAL   = "#1A936F"
AMBER  = "#C17817"
ORANGE = "#D35400"
PURPLE = "#6C3483"
GREY   = "#95A5A6"
CLOUD  = "#F2F4F7"
ICE    = "#EAF4FB"
MINT   = "#E8F8F1"
BLUSH  = "#FEF5E7"
LAVEN  = "#F5EEF8"
WHITE  = "#FFFFFF"
DARK   = "#2C3E50"
LGREY  = "#ECF0F1"

FONT = "DejaVu Sans"


def rbox(ax, cx, cy, w, h, lines, bg, border, fc=DARK, fs=8.2, lw=1.8):
    """Rounded box centred at (cx, cy)."""
    p = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                       boxstyle="round,pad=0.003,rounding_size=0.012",
                       facecolor=bg, edgecolor=border, linewidth=lw, zorder=3)
    ax.add_patch(p)
    ax.text(cx, cy, lines, ha="center", va="center", fontsize=fs,
            color=fc, fontfamily=FONT, linespacing=1.45, zorder=4)


def arr(ax, x0, y0, x1, y1, color=DARK, dashed=False, lw=1.5, rad=0.0):
    ls = (0, (5, 3)) if dashed else "solid"
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls,
                                connectionstyle=f"arc3,rad={rad}"),
                zorder=2)


def label(ax, x, y, txt, color=DARK, fs=7.5, ha="center", va="center",
          italic=False, bold=False):
    ax.text(x, y, txt, ha=ha, va=va, fontsize=fs, color=color,
            fontfamily=FONT, fontstyle="italic" if italic else "normal",
            fontweight="bold" if bold else "normal", zorder=5)


def panel(ax, x, y, w, h, title, color, alpha=0.45):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle="round,pad=0.004,rounding_size=0.018",
                       facecolor=color, edgecolor=GREY, linewidth=0.9,
                       linestyle="dashed", zorder=1, alpha=alpha)
    ax.add_patch(p)
    label(ax, x + w/2, y + h - 0.01, title, color=GREY, fs=7.5,
          va="top", italic=True)


def build():
    # Canvas: wide landscape
    fig, ax = plt.subplots(figsize=(18, 10))
    fig.patch.set_facecolor(CLOUD)
    ax.set_facecolor(CLOUD)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ── Title ─────────────────────────────────────────────────────────────────
    label(ax, 0.5, 0.975, "System B — Thesis Production System",
          color=DARK, fs=14, bold=True)
    label(ax, 0.5, 0.952,
          "Plan  →  Execute  →  Critic  |  Human approval required at every phase transition",
          color=GREY, fs=9.5, italic=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # ROW HEIGHTS (y = centre of box)
    # R1  y=0.845   YOU  +  Coordinator  +  State
    # R2  y=0.700   Planner
    # R3  y=0.570   ── separator ──
    # R4  y=0.560–0.270   Agents (7, spaced 0.07 apart)
    # R5  y=0.700   Critic  (same row as Planner)
    # R6  y=0.845   Human Approval  (same row as Coordinator)
    # Bottom band y=0.05–0.19  Skill Agents
    # ═══════════════════════════════════════════════════════════════════════════

    # ── Column X positions ────────────────────────────────────────────────────
    C0 = 0.06   # YOU
    C1 = 0.21   # Coordinator
    C2 = 0.37   # Planner
    C3 = 0.55   # Agents (centre)
    C4 = 0.73   # Critic
    C5 = 0.89   # Human Approval

    BW  = 0.12   # standard box width
    BH  = 0.075  # standard box height
    BHS = 0.058  # small box height

    # ── Panels ────────────────────────────────────────────────────────────────
    panel(ax, C3 - 0.095, 0.19, 0.19, 0.72,
          "Production Agents", MINT)
    panel(ax, 0.02, 0.02, 0.96, 0.145,
          "Skill Agents  —  invoked directly via slash command", LAVEN)

    # ── YOU ───────────────────────────────────────────────────────────────────
    rbox(ax, C0, 0.72, BW, 0.19,
         "YOU\n(Enrico / Brian)\n─────────────\n/write-section\n/find-papers\n/cite\n/update-outline",
         NAVY, DARK, fc=WHITE, fs=8.0)

    # ── COORDINATOR ───────────────────────────────────────────────────────────
    rbox(ax, C1, 0.72, BW+0.01, 0.21,
         "Thesis Coordinator\n─────────────────\n(1) Load thesis_state.json\n(2) Call Planner - TaskPlan\n(3) Route task to agent\n(4) Validate with Critic\n(5) Persist updated state\n(6) Present for approval",
         NAVY, DARK, fc=WHITE, fs=8.0)

    # ── STATE ─────────────────────────────────────────────────────────────────
    rbox(ax, C1, 0.91, BW+0.01, BHS,
         "thesis_state.json  |  Chapter statuses  |  Literature corpus  |  Figures",
         BLUSH, AMBER, fc=DARK, fs=7.8)

    # ── PLANNER ───────────────────────────────────────────────────────────────
    rbox(ax, C2, 0.72, BW, 0.10,
         "Planner Agent\n─────────────\nReads state + outline\nDecides priorities\nReturns ordered TaskPlan",
         ICE, BLUE, fc=DARK, fs=8.0)

    # ── PRODUCTION AGENTS ─────────────────────────────────────────────────────
    agents = [
        ("Writing Agent",          "Bullet points only  (never prose)"),
        ("Literature Agent",       "Searches papers · annotates corpus · gap analysis"),
        ("Compliance Agent",       "CBS rules · APA 7 · em-dash · page budget"),
        ("Diagram Agent",          "Graphviz + Matplotlib  ->  SVG + PNG"),
        ("Experiment Tracking",    "experiment_registry.json + run summaries"),
        ("Results Visualisation",  "Data charts for Ch.6-8"),
        ("Results Tables",         "Markdown tables for thesis chapters"),
    ]
    n = len(agents)
    y_top, y_bot = 0.88, 0.235
    ys_ag = [y_bot + i * (y_top - y_bot) / (n - 1) for i in range(n)]

    for (name, desc), y in zip(agents, ys_ag):
        rbox(ax, C3, y, 0.165, BHS,
             f"{name}\n{desc}",
             MINT, TEAL, fc=DARK, fs=7.8, lw=1.5)

    # ── CRITIC ────────────────────────────────────────────────────────────────
    rbox(ax, C4, 0.72, BW, 0.14,
         "Critic Agent\n─────────────\nScores every output\nFlags issues\nConfidence score 0-1\nRetry once if invalid",
         BLUSH, ORANGE, fc=DARK, fs=8.0)

    # ── HUMAN APPROVAL ────────────────────────────────────────────────────────
    rbox(ax, C5, 0.72, BW-0.01, 0.14,
         "HUMAN\nAPPROVAL\n─────────────\n[OK] approve\n[NO] revise\nRequired before\nevery phase\ntransition",
         AMBER, ORANGE, fc=WHITE, fs=8.0)

    # ── SKILL AGENTS ──────────────────────────────────────────────────────────
    skill_xs = [0.20, 0.50, 0.80]
    skills = [
        ("/update-outline",
         "Outline Agent\n─────────────\nOnly agent that owns outline.md\nNo other agent writes it"),
        ("/cite",
         "APA Citation Agent\n─────────────\nOnly agent that owns references.md\nFormats APA 7  |  Verifies via NotebookLM"),
        ("/write-section",
         "Thesis Writer Agent\n─────────────\nBullets -> CBS-compliant prose\nCompliance gate  |  Human approval  ->  .docx"),
    ]
    for sx, (cmd, desc) in zip(skill_xs, skills):
        label(ax, sx, 0.155, cmd, color=PURPLE, fs=8.0, bold=True)
        rbox(ax, sx, 0.085, BW + 0.07, 0.10,
             desc, LAVEN, PURPLE, fc=DARK, fs=7.8, lw=1.3)

    # ══════════════════════════════════════════════════════════════════════════
    # ARROWS
    # ══════════════════════════════════════════════════════════════════════════

    # YOU -> Coordinator
    arr(ax, C0 + BW/2, 0.72, C1 - (BW+0.01)/2, 0.72, color=NAVY, lw=1.8)
    label(ax, (C0+C1)/2, 0.735, "request / command",
          color=NAVY, fs=7.5, italic=True)

    # Coordinator -> State (up)
    arr(ax, C1, 0.83, C1, 0.878, color=AMBER, dashed=True, lw=1.3)
    label(ax, C1 + 0.015, 0.858, "read / write", color=AMBER, fs=7, italic=True, ha="left")

    # Coordinator -> Planner
    arr(ax, C1 + (BW+0.01)/2, 0.72, C2 - BW/2, 0.72, color=BLUE, lw=1.8)
    label(ax, (C1+C2)/2 + 0.005, 0.735, "(1) plan",
          color=BLUE, fs=7.5, italic=True)

    # Planner -> Coordinator (dashed return above)
    arr(ax, C2 - BW/2, 0.735, C1 + (BW+0.01)/2, 0.735,
        color=BLUE, dashed=True, lw=1.3)
    label(ax, (C1+C2)/2 + 0.005, 0.748, "TaskPlan",
          color=BLUE, fs=7, italic=True)

    # Coordinator -> each agent
    for y in ys_ag:
        arr(ax, C2 + BW/2, 0.72, C3 - 0.165/2, y,
            color=TEAL, lw=1.1)
    label(ax, (C2+C3)/2 - 0.01, 0.82, "(2) route tasks",
          color=TEAL, fs=7.5, italic=True)

    # Agents -> Critic
    for y in ys_ag:
        arr(ax, C3 + 0.165/2, y, C4 - BW/2, 0.72,
            color=TEAL, lw=1.1)
    label(ax, (C3+C4)/2 + 0.01, 0.82, "output",
          color=TEAL, fs=7.5, italic=True)

    # Critic -> Coordinator (curved retry loop)
    arr(ax, C4 - BW/2, 0.72, C1 + (BW+0.01)/2, 0.695,
        color=ORANGE, dashed=True, lw=1.5, rad=-0.3)
    label(ax, (C1+C4)/2, 0.59, "(3) valid / retry",
          color=ORANGE, fs=7.5, italic=True)

    # Coordinator -> Human Approval
    arr(ax, C4 + BW/2, 0.72, C5 - (BW-0.01)/2, 0.72, color=AMBER, lw=1.8)
    label(ax, (C4+C5)/2, 0.735, "(4) present", color=AMBER, fs=7.5, italic=True)

    # Human Approval -> YOU (result, curved over the top)
    arr(ax, C5, 0.79, C0, 0.815, color=TEAL, dashed=True, lw=1.5, rad=-0.25)
    label(ax, 0.50, 0.90, "result returned to user",
          color=TEAL, fs=7.5, italic=True)

    # YOU -> Skill agents (dashed, going down)
    for sx in skill_xs:
        arr(ax, C0, 0.625, sx, 0.138, color=PURPLE, dashed=True, lw=1.1)

    # ── Legend ────────────────────────────────────────────────────────────────
    legend = [
        (NAVY,   "Core orchestration"),
        (TEAL,   "Production agents"),
        (PURPLE, "Skill agents (slash commands)"),
        (AMBER,  "State / approval"),
        (ORANGE, "Critic / retry"),
    ]
    for i, (c, lbl_txt) in enumerate(legend):
        bx = 0.03 + i * 0.19
        p = FancyBboxPatch((bx, 0.003), 0.012, 0.012,
                           boxstyle="round,pad=0.001",
                           facecolor=c, edgecolor=DARK, linewidth=0.7,
                           transform=ax.transData, zorder=5)
        ax.add_patch(p)
        label(ax, bx + 0.017, 0.009, lbl_txt, color=DARK, fs=7.5, ha="left")

    # ── Save ──────────────────────────────────────────────────────────────────
    plt.tight_layout(pad=0)
    for ext in ["png", "svg"]:
        path = os.path.join(OUTPUT_DIR, f"system_b_overview.{ext}")
        fig.savefig(path, format=ext, dpi=180, bbox_inches="tight",
                    facecolor=CLOUD)
        print(f"  system_b_overview.{ext}")
    plt.close(fig)


if __name__ == "__main__":
    build()
