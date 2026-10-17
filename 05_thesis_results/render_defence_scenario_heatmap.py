"""Render the scenario comparison as a four-frame heatmap build for the defence deck.

Frame 1 is the plain table. Frames 2-4 add the worst, middle and best tiers in
turn (red, then yellow, then green), each frame keeping the colours of the one
before, so clicking through the slides builds the heatmap up.

A cell's tier sets a light fill with darker text of the same colour. The best and
worst value in each row (ties included) get a darker gradient fill and black, bold
text, as does the best of the middle tier in each row. In the middle frames, cells not yet coloured fade to grey; a key under the
table gains each colour as it appears.

Values are read from the chapter's scenario-comparison CSV on every run, and the
row-wise best and worst are computed from them. The tier grid below is editorial:
the authors' own reading of which cells count as worst, middle and best, so it is
typed rather than computed. Guards check that it covers every scenario and measure,
and that every computed best is green and every computed worst is red.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
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

# Column order on the slide: the GPT-5.5 orchestrator, then Prometheus.
LEFT, RIGHT = ["A", "B", "C", "F"], ["D", "E", "G"]
RUNS_IN = {"A": "GPT 5.5", "B": "GPT 5.5", "C": "GPT 5.5", "F": "GPT 5.5",
           "D": "Prometheus", "E": "Prometheus", "G": "Prometheus"}
# What each scenario receives, as a vertical gradient (top, bottom) with white text,
# so the comparable scenarios on either side of the divider read as pairs.
RECEIVES_FILL = {"Data + code": ("#2E6DA4", "#7393B3"), "Our model": ("#9C2A96", "#B86BB3"),
                 "All three": ("#4A4A4A", "#0D0D0D")}
RECEIVES = {"A": "Nothing", "B": "Data + code", "C": "Our model", "F": "All three",
            "D": "Data + code", "E": "Our model", "G": "All three"}

# Editorial tier grid: R/O/G = worst/middle/best (O renders yellow).
TIERS = {
    "Usable answers":           dict(A="R", B="G", C="G", F="G", D="G", E="G", G="G"),
    "Median APE":               dict(A="R", B="G", C="O", F="O", D="G", E="O", G="G"),
    "Mean APE":                 dict(A="R", B="R", C="G", F="O", D="R", E="G", G="G"),
    "Variation across repeats": dict(A="R", B="O", C="G", F="O", D="R", E="G", G="O"),
    "Identical on repeat":      dict(A="R", B="R", C="G", F="O", D="R", E="G", G="O"),
    "Cost per answer":          dict(A="R", B="R", C="G", F="R", D="R", E="O", G="R"),
    "Latency":                  dict(A="O", B="R", C="G", F="R", D="R", E="O", G="R"),
}
# Which direction is better, per row; drives the computed best and worst.
HIGHER_IS_BETTER = {"Usable answers", "Identical on repeat"}

# Red / yellow / green as tints over white. The middle tier is yellow rather than the
# theme's orange: at light tints orange and red were too close to tell apart.
# Standout cells get a diagonal gradient between two darker tints (top-left darker).
_BASE = {"R": "#FF0000", "O": "#FFC000", "G": "#196B24"}
_LIGHT = 0.32
# Text on light cells: a dark shade of the same colour (the spreadsheet
# "light fill, dark text" convention), so the tier reads from the text as well.
_TEXT = {"R": "#9C0006", "O": "#7A5C00", "G": "#0E4A17"}
# In the middle frames, cells not yet coloured fade to grey so the eye goes to
# the newly coloured tier. The first (plain) and last (complete) frames stay full.
_FADED = "#B4B4B4"
# Underline the row-wise best and worst on top of bold. Off: bold carries it.
UNDERLINE = False
_KEY = [("R", "Worst"), ("O", "Middle"), ("G", "Best")]
_DARK_FROM, _DARK_TO = 0.70, 0.45


def _tint(hex_colour: str, share: float) -> str:
    rgb = [int(hex_colour[i:i + 2], 16) for i in (1, 3, 5)]
    mixed = [round(255 - (255 - c) * share) for c in rgb]
    return "#" + "".join(f"{c:02X}" for c in mixed)


def _money(x: str) -> str:
    v = float(str(x).replace("$", ""))
    return f"$ {v:.3f}" if v < 0.1 else f"$ {v:.2f}"


def _values(df: pd.DataFrame) -> tuple[dict[str, dict[str, str]], set[tuple[str, str]]]:
    row = df.set_index("Measure")
    pick = lambda prefix: row.loc[[i for i in row.index if i.startswith(prefix)][0]]  # noqa: E731
    runs, usable = pick("Runs completed"), pick("Usable answers")
    out = {
        "Usable answers": {s: f"{int(usable[s])}/{int(runs[s])}" for s in RUNS_IN},
        "Median APE": {s: f"{float(pick('Median APE')[s]):.1f} %" for s in RUNS_IN},
        "Mean APE": {s: f"{float(pick('Mean APE')[s]):.1f} %" for s in RUNS_IN},
        "Variation across repeats": {s: f"{float(pick('Consistency')[s]):.1f} %" for s in RUNS_IN},
        "Identical on repeat": {s: f"{float(pick('Replicability')[s]):.0f} %" for s in RUNS_IN},
        "Cost per answer": {s: _money(pick("Cost per answer")[s]) for s in RUNS_IN},
        "Latency": {s: f"{float(pick('Response time')[s]):.1f} s" for s in RUNS_IN},
    }
    missing = [(m, s) for m in out for s in RUNS_IN if s not in TIERS.get(m, {})]
    if missing:
        raise SystemExit(f"Tier grid does not cover: {missing}")

    nums = {
        "Usable answers": pick("Usable answers"), "Median APE": pick("Median APE"),
        "Mean APE": pick("Mean APE"), "Variation across repeats": pick("Consistency"),
        "Identical on repeat": pick("Replicability"),
        "Cost per answer": pick("Cost per answer").str.replace("$", "", regex=False),
        "Latency": pick("Response time"),
    }
    standouts, wrong = set(), []
    for measure, series in nums.items():
        v = {s: float(series[s]) for s in RUNS_IN}
        best = max if measure in HIGHER_IS_BETTER else min
        worst = min if measure in HIGHER_IS_BETTER else max
        for pick_fn, tier in ((best, "G"), (worst, "R")):
            edge = pick_fn(v.values())
            for s, x in v.items():
                if x == edge:
                    standouts.add((measure, s))
                    if TIERS[measure][s] != tier:
                        wrong.append((measure, s, TIERS[measure][s], tier))
    if wrong:
        raise SystemExit(f"Computed best/worst disagrees with the tier grid: {wrong}")

    # The best of the middle (yellow) tier in each row is highlighted too, ties
    # included, to guide the eye through the middle as well as the extremes.
    for measure, series in nums.items():
        mid = {s: float(series[s]) for s in RUNS_IN if TIERS[measure][s] == "O"}
        if mid:
            edge = (max if measure in HIGHER_IS_BETTER else min)(mid.values())
            standouts |= {(measure, s) for s, x in mid.items() if x == edge}
    values = {m: {s: float(series[s]) for s in RUNS_IN} for m, series in nums.items()}
    return out, standouts, values


def _within_arms(nums: dict) -> tuple[dict, set]:
    """Trial variant: rank each arm against baseline A, not the whole row.

    Each arm (A + the GPT-5.5 scenarios, A + the Prometheus scenarios) gets green
    for its best value, red for its worst and yellow for anything between, ties
    included. Best and worst are bold. A sits in both arms, so it must come out
    in the same tier from both; the run stops if it does not.
    """
    tiers, standouts, clash = {}, set(), []
    for measure, v in nums.items():
        better = max if measure in HIGHER_IS_BETTER else min
        worse = min if measure in HIGHER_IS_BETTER else max
        row = {}
        for arm in (LEFT, ["A", *RIGHT]):
            vals = {s: v[s] for s in arm}
            hi, lo = better(vals.values()), worse(vals.values())
            for s, x in vals.items():
                tier = "G" if x == hi else "R" if x == lo else "O"
                if s in row and row[s] != tier:
                    clash.append((measure, s, row[s], tier))
                row[s] = tier
                if tier != "O":
                    standouts.add((measure, s))
        tiers[measure] = row
    if clash:
        raise SystemExit(f"Baseline A lands in different tiers per arm: {clash}")
    return tiers, standouts


def _gradient(ax, x, y, w, h, top: str, bottom: str, diagonal: bool = False) -> None:
    """Fill a rectangle with a gradient from `top` (top or top-left) to `bottom`."""
    from matplotlib.colors import LinearSegmentedColormap
    import numpy as np
    cmap = LinearSegmentedColormap.from_list("cell", [top, bottom])
    ramp = np.linspace(0, 1, 64)
    field = (ramp[:, None] + ramp[None, :]) / 2 if diagonal else ramp.reshape(-1, 1)
    ax.imshow(field, cmap=cmap, aspect="auto",
              extent=(x, x + w, y + h, y), interpolation="bicubic", zorder=1)


def _render(values: dict, standouts: set, shown: set[str], path: Path,
            tiers: dict = TIERS,
            note: str = "Bold = best and worst in the row, best of the middle") -> None:
    plt.rcParams.update({"svg.fonttype": "none", "font.family": "Calibri"})
    label_w, col_w, gap, row_h, pad = 2.3, 1.15, 0.18, 0.42, 0.05
    cols = LEFT + RIGHT
    x0 = {s: label_w + i * col_w + (gap if i else 0) + (gap if s in RIGHT else 0)
          for i, s in enumerate(cols)}
    width = label_w + len(cols) * col_w + 2 * gap
    rows = ["Runs in", "Receives", *TIERS]
    table_h = (len(rows) + 2) * row_h
    height = table_h + row_h * 1.1
    fade = bool(shown) and shown != {c for c, _ in _KEY}

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
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

    underline = []
    for r, measure in enumerate(rows):
        y = (r + 2) * row_h
        text(0.08, y + row_h / 2, measure, bold=True, size=10.5)
        for s in cols:
            if measure == "Runs in":
                cell, tier = RUNS_IN[s], ""
            elif measure == "Receives":
                cell, tier = RECEIVES[s], ""
            else:
                cell, tier = values[measure][s], tiers[measure][s]
            if measure == "Receives" and cell in RECEIVES_FILL:
                _gradient(ax, x0[s] + pad, y + pad, col_w - 2 * pad, row_h - 2 * pad,
                          *RECEIVES_FILL[cell])
                text(x0[s] + 0.12, y + row_h / 2, cell, bold=True, size=10.5, colour="white")
                continue
            colour, strong = tier, (measure, s) in standouts
            on = colour in shown
            if on and strong:
                _gradient(ax, x0[s] + pad, y + pad, col_w - 2 * pad, row_h - 2 * pad,
                          _tint(_BASE[colour], _DARK_FROM), _tint(_BASE[colour], _DARK_TO),
                          diagonal=True)
            elif on:
                ax.add_patch(Rectangle((x0[s] + pad, y + pad), col_w - 2 * pad, row_h - 2 * pad,
                                       facecolor=_tint(_BASE[colour], _LIGHT), edgecolor="none"))
            faded = fade and not on and measure in TIERS
            ink = _TEXT[colour] if on and not strong else (_FADED if faded else "black")
            label = text(x0[s] + 0.12, y + row_h / 2, cell, bold=on and strong, size=10.5,
                         colour=ink)
            if on and strong and UNDERLINE:
                underline.append(label)

    ax.plot([label_w - 0.02, label_w - 0.02], [0, table_h], color="black", lw=0.8)

    # Key: each entry appears with its colour, in fixed slots so nothing shifts.
    key_y = table_h + row_h * 0.6
    for i, (code, word) in enumerate(_KEY):
        if code not in shown:
            continue
        kx = label_w + 0.12 + i * 1.0
        ax.add_patch(Rectangle((kx, key_y - 0.1), 0.32, 0.2, edgecolor="none",
                               facecolor=_tint(_BASE[code], _DARK_TO)))
        text(kx + 0.42, key_y, word, size=10)
    if shown:
        text(label_w + 0.12 + 3 * 1.0 + 0.2, key_y, note, bold=True, size=10)
    for after in ("A", LEFT[-1]):
        divider_x = x0[after] + col_w + gap / 2
        ax.plot([divider_x, divider_x], [row_h, table_h], color="#7F7F7F", lw=0.8)
    # Separates who-gets-what (Runs in, Receives) from the measured results.
    ax.plot([0, width], [row_h * 4, row_h * 4], color="black", lw=0.8)

    # Underline the standout values; matplotlib text has no underline, so draw it.
    renderer = fig.canvas.get_renderer()
    to_data = ax.transData.inverted()
    for label in underline:
        box = label.get_window_extent(renderer)
        (x_a, y_b), (x_b, _) = to_data.transform([(box.x0, box.y0), (box.x1, box.y1)])
        ax.plot([x_a, x_b], [y_b + 0.01, y_b + 0.01], color="black", lw=0.9)

    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    fig.savefig(path, format="svg", facecolor="white", transparent=False, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"Missing source table: {SOURCE}")
    values, standouts, nums = _values(pd.read_csv(SOURCE, dtype=str))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    frames = [set(), {"R"}, {"R", "O"}, {"R", "O", "G"}]
    for i, shown in enumerate(frames, start=1):
        out = OUT_DIR / f"{STEM}_{i}.svg"
        _render(values, standouts, shown, out)
        print(f"wrote {out.relative_to(_ROOT)}")

    # Trial: the complete frame, coloured within each arm against baseline A.
    arm_tiers, arm_standouts = _within_arms(nums)
    out = OUT_DIR / f"{STEM}_4_within_arms.svg"
    _render(values, arm_standouts, {"R", "O", "G"}, out, tiers=arm_tiers,
            note="Coloured within each arm against baseline A; bold = best and worst")
    print(f"wrote {out.relative_to(_ROOT)}")


if __name__ == "__main__":
    main()
