"""Render the scenario comparison as a four-frame heatmap build for the defence deck.

Each row is coloured on a spreadsheet-style three-colour scale (green best,
yellow middle, red worst) by the rank of its seven scenarios. Rank rather than
value, because one baseline value (502 % median error) would otherwise squash
the other six into a single colour. Ties share their average rank.

The build: frame 1 is the plain table; frames 2-4 reveal the worst third of the
scale, then the middle third, then the best, each frame keeping what the one
before showed. Cells not yet revealed fade to grey so the eye goes to the new
colour. A best-to-worst scale bar under the table appears from frame 2.

Every value and every colour is computed from the chapter's scenario-comparison
CSV on each run; nothing is typed.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402


def _find_repo_root(start: Path) -> Path:
    for cand in (start, *start.parents):
        if any((cand / a).exists() for a in (".env.example", ".env", "PATHS.py")):
            return cand
    raise FileNotFoundError(f"Could not find project root above {start}")


_ROOT = _find_repo_root(Path(__file__).resolve().parent)
sys.path.insert(0, str(_ROOT))
from PATHS import THESIS_RESULTS_SRQ4_DIR, get_chapter_figures_dir  # noqa: E402

SOURCE = THESIS_RESULTS_SRQ4_DIR / "tables" / "22_scenario_comparison.csv"
OUT_DIR = get_chapter_figures_dir("experimental_evaluation")
STEM = "defence_scenario_heatmap"
# Outputs of earlier trial variants, removed on every run so no stale copy survives.
RETIRED = [f"{STEM}_4_within_arms.svg", f"{STEM}_4_colour_scale.svg",
           f"{STEM}_4_draft_borders_dimmed.svg"]

# Column order on the slide: the GPT-5.5 orchestrator, then Prometheus.
LEFT, RIGHT = ["A", "B", "C", "F"], ["D", "E", "G"]
RUNS_IN = {"A": "GPT 5.5", "B": "GPT 5.5", "C": "GPT 5.5", "F": "GPT 5.5",
           "D": "Prometheus", "E": "Prometheus", "G": "Prometheus"}
RECEIVES = {"A": "Nothing", "B": "Data + code", "C": "Our model", "F": "All three",
            "D": "Data + code", "E": "Our model", "G": "All three"}
# What each scenario receives, as a vertical gradient (top, bottom) with white text,
# so the comparable scenarios on either side of the divider read as pairs.
RECEIVES_FILL = {"Data + code": ("#2E6DA4", "#7393B3"), "Our model": ("#9C2A96", "#B86BB3"),
                 "All three": ("#4A4A4A", "#0D0D0D")}

MEASURES = ["Usable answers", "Median APE", "Mean APE", "Variation across repeats",
            "Identical on repeat", "Cost per answer", "Latency"]
# Which direction is better, per row; drives the ranking.
HIGHER_IS_BETTER = {"Usable answers", "Identical on repeat"}

# The default spreadsheet three-colour scale: best, midpoint, worst.
SCALE = [(0.0, "#63BE7B"), (0.5, "#FFEB84"), (1.0, "#F8696B")]
# Build order: which third of the scale each frame reveals.
FRAMES = [set(), {"worst"}, {"worst", "middle"}, {"worst", "middle", "best"}]
_FADED = "#B4B4B4"
# Prometheus columns are drawn lighter: they follow B, C, F but run on a
# proprietary platform, so the openly replicable GPT-5.5 arm carries the eye.
DIM_COLS = set(RIGHT)
DIM_SHARE = 0.45  # share of white blended into a dimmed column's fills

# Draft: per frame, the cells its speaker notes point at, outlined.
# Each entry is (scenario, first row, last row); a single cell repeats the row.
DRAFT_BORDERS = [
    [],
    [("A", "Usable answers", "Usable answers"), ("A", "Median APE", "Median APE"),
     ("B", "Identical on repeat", "Identical on repeat"),
     ("D", "Identical on repeat", "Identical on repeat"),
     ("D", "Cost per answer", "Cost per answer"), ("B", "Latency", "Latency")],
    [("F", "Usable answers", "Latency"), ("G", "Usable answers", "Latency")],
    [("C", "Mean APE", "Latency"), ("E", "Mean APE", "Latency"),
     ("B", "Median APE", "Median APE"), ("D", "Median APE", "Median APE")],
]
BORDER_LW = 1.3

# Draft: the row-reveal build, one group of rows per click (first click plain).
ROW_GROUPS = [
    [],
    ["Usable answers"],                                   # does it answer at all
    ["Median APE", "Mean APE"],                           # accuracy, the axis usually reported
    ["Variation across repeats", "Identical on repeat"],  # replicability
    ["Cost per answer"],
    ["Latency"],
]
# Rows revealed on an earlier click recede: this share of white is blended into
# their fills, and their text greys, so the current group carries the eye.
INACTIVE_SHARE = 0.60
_INACTIVE_INK = "#7F7F7F"
# Closing frame: the full table, nothing receding, with what to look at outlined.
CONCLUSION_BORDERS = [("C", "Mean APE", "Latency"), ("E", "Mean APE", "Latency"),
                      ("B", "Median APE", "Median APE"), ("D", "Median APE", "Median APE")]


def _money(x: str) -> str:
    v = float(str(x).replace("$", ""))
    return f"$ {v:.3f}" if v < 0.1 else f"$ {v:.2f}"


def _read(df: pd.DataFrame) -> tuple[dict, dict]:
    """Display strings and numeric values per measure and scenario."""
    row = df.set_index("Measure")

    def pick(prefix: str) -> pd.Series:
        hits = [i for i in row.index if i.startswith(prefix)]
        if not hits:
            raise SystemExit(f"No row starting {prefix!r} in {SOURCE.name}")
        return row.loc[hits[0]]

    runs, usable = pick("Runs completed"), pick("Usable answers")
    raw = {
        "Usable answers": usable, "Median APE": pick("Median APE"),
        "Mean APE": pick("Mean APE"), "Variation across repeats": pick("Consistency"),
        "Identical on repeat": pick("Replicability"),
        "Cost per answer": pick("Cost per answer").str.replace("$", "", regex=False),
        "Latency": pick("Response time"),
    }
    nums = {m: {s: float(raw[m][s]) for s in RUNS_IN} for m in MEASURES}
    text = {
        "Usable answers": {s: f"{int(usable[s])}/{int(runs[s])}" for s in RUNS_IN},
        "Median APE": {s: f"{nums['Median APE'][s]:.1f} %" for s in RUNS_IN},
        "Mean APE": {s: f"{nums['Mean APE'][s]:.1f} %" for s in RUNS_IN},
        "Variation across repeats": {s: f"{nums['Variation across repeats'][s]:.1f} %" for s in RUNS_IN},
        "Identical on repeat": {s: f"{nums['Identical on repeat'][s]:.0f} %" for s in RUNS_IN},
        "Cost per answer": {s: _money(raw["Cost per answer"][s]) for s in RUNS_IN},
        "Latency": {s: f"{nums['Latency'][s]:.1f} s" for s in RUNS_IN},
    }
    return text, nums


def _mix(a: str, b: str, f: float) -> str:
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * f):02X}" for x, y in zip(ca, cb))


def _colour_scale(nums: dict) -> tuple[dict, dict]:
    """Fill colour and build third ("best"/"middle"/"worst") for every cell."""
    fills, third = {}, {}
    for measure, v in nums.items():
        ranked = pd.Series(v).rank(ascending=measure not in HIGHER_IS_BETTER, method="average")
        span = max(ranked.max() - ranked.min(), 1)
        for s, r in ranked.items():
            pos = (r - ranked.min()) / span
            (p0, c0), (p1, c1) = (SCALE[0], SCALE[1]) if pos <= 0.5 else (SCALE[1], SCALE[2])
            fills[(measure, s)] = _mix(c0, c1, (pos - p0) / (p1 - p0))
            third[(measure, s)] = "best" if pos < 1 / 3 else "worst" if pos > 2 / 3 else "middle"
    return fills, third


def _gradient(ax, x, y, w, h, top: str, bottom: str) -> None:
    """Fill a rectangle with a vertical gradient from `top` to `bottom`."""
    cmap = LinearSegmentedColormap.from_list("cell", [top, bottom])
    ax.imshow(np.linspace(0, 1, 64).reshape(-1, 1), cmap=cmap, aspect="auto",
              extent=(x, x + w, y + h, y), interpolation="bicubic", zorder=1)


def _render(text_of: dict, fills: dict, third: dict, shown: set[str], path: Path,
            dim: set[str] = frozenset(), borders: list = (),
            rows_shown: set[str] | None = None, active: set[str] | None = None) -> None:
    """`active`, when given, is also outlined as one band across the whole table."""
    plt.rcParams.update({"svg.fonttype": "none", "font.family": "Calibri"})
    label_w, col_w, gap, row_h, pad = 2.3, 1.15, 0.18, 0.42, 0.05
    cols = LEFT + RIGHT
    x0 = {s: label_w + i * col_w + (gap if i else 0) + (gap if s in RIGHT else 0)
          for i, s in enumerate(cols)}
    width = label_w + len(cols) * col_w + 2 * gap
    rows = ["Runs in", "Receives", *MEASURES]
    table_h = (len(rows) + 2) * row_h
    height = table_h + row_h * 1.1
    if rows_shown is not None:
        fade = bool(rows_shown) and rows_shown != set(MEASURES)
    else:
        fade = bool(shown) and shown != FRAMES[-1]

    fig, ax = plt.subplots(figsize=(width, height))
    ax.axis("off")

    def text(x, y, s, bold=False, size=11, ha="left", colour="black"):
        return ax.text(x, y, s, ha=ha, va="center", fontsize=size, color=colour,
                       fontweight="bold" if bold else "normal")

    text(label_w + (width - label_w) / 2, row_h * 0.5, "Scenarios", bold=True, size=13, ha="center")
    ax.plot([label_w, width], [row_h, row_h], color="black", lw=0.8)
    text(0.08, row_h * 1.5, "Measure", bold=True, size=13)
    for s in cols:
        text(x0[s] + 0.12, row_h * 1.5, s, bold=True, size=13)
    ax.plot([0, width], [row_h * 2, row_h * 2], color="black", lw=1.4)

    for r, measure in enumerate(rows):
        y = (r + 2) * row_h
        text(0.08, y + row_h / 2, measure, bold=True, size=10.5)
        for s in cols:
            cx, cy, cw, ch = x0[s] + pad, y + pad, col_w - 2 * pad, row_h - 2 * pad
            if measure == "Runs in":
                text(x0[s] + 0.12, y + row_h / 2, RUNS_IN[s], size=10.5)
            elif measure == "Receives":
                cell = RECEIVES[s]
                if cell in RECEIVES_FILL:
                    top, bottom = RECEIVES_FILL[cell]
                    if s in dim:
                        top, bottom = _mix(top, "#FFFFFF", DIM_SHARE), _mix(bottom, "#FFFFFF", DIM_SHARE)
                    _gradient(ax, cx, cy, cw, ch, top, bottom)
                    text(x0[s] + 0.12, y + row_h / 2, cell, bold=True, size=10.5, colour="white")
                else:
                    text(x0[s] + 0.12, y + row_h / 2, cell, size=10.5)
            else:
                on = (measure in rows_shown) if rows_shown is not None else third[(measure, s)] in shown
                if on:
                    fill = fills[(measure, s)]
                    if s in dim:
                        fill = _mix(fill, "#FFFFFF", DIM_SHARE)
                    if active is not None and measure not in active:
                        fill = _mix(fill, "#FFFFFF", INACTIVE_SHARE)
                    ax.add_patch(Rectangle((cx, cy), cw, ch, facecolor=fill, edgecolor="none"))
                ink = _FADED if fade and not on else "black"
                if on and active is not None and measure not in active:
                    ink = _INACTIVE_INK
                text(x0[s] + 0.12, y + row_h / 2, text_of[measure][s], size=10.5, colour=ink)

    ax.plot([label_w - 0.02, label_w - 0.02], [0, table_h], color="black", lw=0.8)
    for after in ("A", LEFT[-1]):
        divider_x = x0[after] + col_w + gap / 2
        ax.plot([divider_x, divider_x], [row_h, table_h], color="#7F7F7F", lw=0.8)
    if active:
        idx = sorted(rows.index(m) for m in active)
        top, bottom = (idx[0] + 2) * row_h + pad / 2, (idx[-1] + 3) * row_h - pad / 2
        ax.add_patch(Rectangle((0.02, top), width - 0.04, bottom - top,
                               facecolor="none", edgecolor="black", lw=BORDER_LW, zorder=5))
    for s, first, last in borders:
        top = (rows.index(first) + 2) * row_h + pad
        bottom = (rows.index(last) + 3) * row_h - pad
        ax.add_patch(Rectangle((x0[s] + pad, top), col_w - 2 * pad, bottom - top,
                               facecolor="none", edgecolor="black", lw=BORDER_LW, zorder=5))
    # Separates who-gets-what (Runs in, Receives) from the measured results.
    ax.plot([0, width], [row_h * 4, row_h * 4], color="black", lw=0.8)

    # Scale bar, best to worst, from the first coloured frame on.
    if (rows_shown if rows_shown is not None else shown):
        key_y, bar_x, bar_w = table_h + row_h * 0.6, label_w + 0.85, 2.4
        text(label_w + 0.12, key_y, "Best", bold=True, size=10)
        cmap = LinearSegmentedColormap.from_list("scale", [c for _, c in SCALE])
        ax.imshow(np.linspace(0, 1, 128).reshape(1, -1), cmap=cmap, aspect="auto",
                  extent=(bar_x, bar_x + bar_w, key_y + 0.1, key_y - 0.1), zorder=1)
        text(bar_x + bar_w + 0.1, key_y, "Worst", bold=True, size=10)
        text(bar_x + bar_w + 0.8, key_y, "Ranked across all seven scenarios, per row", size=10)

    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    fig.savefig(path, format="svg", facecolor="white", transparent=False, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"Missing source table: {SOURCE}")
    text_of, nums = _read(pd.read_csv(SOURCE, dtype=str))
    fills, third = _colour_scale(nums)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name in RETIRED:
        (OUT_DIR / name).unlink(missing_ok=True)
    for i, shown in enumerate(FRAMES, start=1):
        out = OUT_DIR / f"{STEM}_{i}.svg"
        _render(text_of, fills, third, shown, out)
        print(f"wrote {out.relative_to(_ROOT)}")

    # Draft: reveal by row, grouped into the four axes of the Ch9 trade-off.
    revealed: set[str] = set()
    for i, group in enumerate(ROW_GROUPS, start=1):
        revealed |= set(group)
        out = OUT_DIR / f"{STEM}_rows_{i}.svg"
        _render(text_of, fills, third, set(), out, dim=DIM_COLS, rows_shown=set(revealed),
                active=set(group) if group else None)
        print(f"wrote {out.relative_to(_ROOT)}")
    out = OUT_DIR / f"{STEM}_rows_{len(ROW_GROUPS) + 1}.svg"
    _render(text_of, fills, third, set(), out, dim=DIM_COLS, rows_shown=set(MEASURES),
            borders=CONCLUSION_BORDERS)
    print(f"wrote {out.relative_to(_ROOT)}")

    for i, (shown, borders) in enumerate(zip(FRAMES, DRAFT_BORDERS), start=1):
        out = OUT_DIR / f"{STEM}_draft_{i}.svg"
        _render(text_of, fills, third, shown, out, dim=DIM_COLS, borders=borders)
        print(f"wrote {out.relative_to(_ROOT)}")


if __name__ == "__main__":
    main()
