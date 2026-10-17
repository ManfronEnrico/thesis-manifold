"""Render the scenario comparison as a four-frame heatmap build for the defence deck.

Frame 1 is the plain table. Frames 2-4 add the worst, middle and best tiers in
turn (red, then orange, then green), each frame keeping the colours of the one
before, so clicking through the slides builds the heatmap up.

Text is black throughout. A cell's tier sets its fill; the standout cells within
a tier get a darker shade of that fill and bold text.

Values are read from the chapter's scenario-comparison CSV on every run. The tier
grid below is editorial: the authors' own reading of which cells count as worst,
middle and best, so it is typed rather than computed. A guard checks that it
covers every scenario and measure the CSV carries.
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
RECEIVES = {"A": "Nothing", "B": "Data + code", "C": "Our model", "F": "All three",
            "D": "Data + code", "E": "Our model", "G": "All three"}

# Editorial tier grid: R/O/G = worst/middle/best; a trailing * = standout (darker, bold).
TIERS = {
    "Usable answers":           dict(A="R*", B="G*", C="G*", F="G*", D="G*", E="G*", G="G*"),
    "Median APE":               dict(A="R*", B="G*", C="O*", F="O",  D="G*", E="O*", G="G"),
    "Mean APE":                 dict(A="R*", B="R",  C="G*", F="O*", D="R",  E="G*", G="G"),
    "Variation across repeats": dict(A="R*", B="O",  C="G*", F="O*", D="R",  E="G*", G="O"),
    "Identical on repeat":      dict(A="R*", B="R*", C="G*", F="O*", D="R*", E="G*", G="O*"),
    "Cost per answer":          dict(A="R",  B="R",  C="G*", F="R",  D="R*", E="O*", G="R"),
    "Latency":                  dict(A="O",  B="R*", C="G*", F="R",  D="R",  E="O*", G="R"),
}

# Theme colours (red, accent2 orange, accent3 green) as (light, dark) tints over white.
_BASE = {"R": "#FF0000", "O": "#E97132", "G": "#196B24"}
_LIGHT, _DARK = 0.30, 0.55


def _tint(hex_colour: str, share: float) -> str:
    rgb = [int(hex_colour[i:i + 2], 16) for i in (1, 3, 5)]
    mixed = [round(255 - (255 - c) * share) for c in rgb]
    return "#" + "".join(f"{c:02X}" for c in mixed)


def _money(x: str) -> str:
    v = float(str(x).replace("$", ""))
    return f"$ {v:.3f}" if v < 0.1 else f"$ {v:.2f}"


def _values(df: pd.DataFrame) -> dict[str, dict[str, str]]:
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
    return out


def _render(values: dict, shown: set[str], path: Path) -> None:
    plt.rcParams.update({"svg.fonttype": "none", "font.family": "Calibri"})
    label_w, col_w, gap, row_h, pad = 2.3, 1.15, 0.18, 0.42, 0.03
    cols = LEFT + RIGHT
    x0 = {s: label_w + i * col_w + (gap if s in RIGHT else 0) for i, s in enumerate(cols)}
    width = label_w + len(cols) * col_w + gap
    rows = ["Runs in", "Receives", *TIERS]
    height = (len(rows) + 2) * row_h

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax.axis("off")

    def text(x, y, s, bold=False, size=11, ha="left"):
        ax.text(x, y, s, ha=ha, va="center", fontsize=size, color="black",
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
            if measure == "Runs in":
                cell, tier = RUNS_IN[s], ""
            elif measure == "Receives":
                cell, tier = RECEIVES[s], ""
            else:
                cell, tier = values[measure][s], TIERS[measure][s]
            colour, strong = tier[:1], tier.endswith("*")
            on = colour in shown
            if on:
                ax.add_patch(Rectangle((x0[s] + pad, y + pad), col_w - 2 * pad, row_h - 2 * pad,
                                       facecolor=_tint(_BASE[colour], _DARK if strong else _LIGHT),
                                       edgecolor="none"))
            text(x0[s] + 0.12, y + row_h / 2, cell, bold=on and strong, size=10.5)

    divider_x = label_w + len(LEFT) * col_w + gap / 2
    ax.plot([label_w - 0.02, label_w - 0.02], [0, height], color="black", lw=0.8)
    ax.plot([divider_x, divider_x], [row_h * 2, height], color="#7F7F7F", lw=0.8)

    fig.savefig(path, format="svg", facecolor="white", transparent=False, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"Missing source table: {SOURCE}")
    values = _values(pd.read_csv(SOURCE, dtype=str))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    frames = [set(), {"R"}, {"R", "O"}, {"R", "O", "G"}]
    for i, shown in enumerate(frames, start=1):
        out = OUT_DIR / f"{STEM}_{i}.svg"
        _render(values, shown, out)
        print(f"wrote {out.relative_to(_ROOT)}")


if __name__ == "__main__":
    main()
