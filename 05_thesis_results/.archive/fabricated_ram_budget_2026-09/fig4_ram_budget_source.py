"""Removed from generate_architecture_diagrams.py on 2026-09-06 (P0046).
Preserved verbatim. See README.md in this folder for why.
"""

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
               label=f"{RAM_BUDGET_MB/1024:.0f} GB hard limit  ({RAM_BUDGET_MB:,.0f} MB)")
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