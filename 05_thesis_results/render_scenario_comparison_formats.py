"""Render the scenario-comparison table in three formats, for a side-by-side choice.

WHY THREE
---------
The appendix tables are Markdown because Markdown pastes into Word as a real,
editable table and stays searchable in the PDF. What Markdown cannot do is encode
more than two states: it defines bold and italic and nothing else, so "best in
class", "second best" and "these rows are a matched pair" all have to collapse
into one `***value***`.

This script writes the SAME DataFrame three ways so the trade-off can be seen
rather than argued:

  .md    what ships today. Two emphases. Pastes as an editable table.
  .svg   graphviz HTML-like labels rendered to vector. Full colour, weight,
         slant and underline per cell. Pastes as a PICTURE.
  .html  a real HTML table. Full styling AND Word pastes it as a native
         editable table, because Word reads HTML from the clipboard.

A CORRECTION WORTH RECORDING
----------------------------
Graphviz "HTML-like labels" are NOT HTML. They are a table syntax that borrows
HTML's spelling and renders only to SVG or PNG -- nothing HTML-ish survives into
the output, and none of it can reach Word as markup. The third format here is a
genuine standalone .html file, which is a different thing and is the one that
pastes as an editable table with its colours intact.

HOW TO PASTE THE .html INTO WORD
--------------------------------
Open it in a browser, select the table, copy, and paste into Word. Word's
clipboard handler reads HTML natively and converts it to a Word table, keeping
cell shading, text colour, bold, italic and underline. It becomes an ordinary
Word table afterwards -- editable, and numbered by Word's caption fields.

Every value and every highlight is computed from the source CSV on each run.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


def _find_repo_root(start: Path) -> Path:
    for cand in (start, *start.parents):
        if any((cand / a).exists() for a in (".env.example", ".env", "PATHS.py")):
            return cand
    raise FileNotFoundError(f"Could not find project root above {start}")


_ROOT = _find_repo_root(Path(__file__).resolve().parent)
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "05_thesis_results"))
from PATHS import THESIS_RESULTS_SRQ4_DIR, get_chapter_figures_dir  # noqa: E402
from styled_tables import render_table, BEST, SECOND, POOR, PLAIN  # noqa: E402

# SUPERSEDED for SVG, 2026-09-14. export_appendix.py now renders a styled SVG
# for every table it emits, including this one, as `11_scenario_comparison.svg`.
# This script kept writing a second, differently-named copy of the same table
# WITHOUT the footnote -- two versions of one table, the worse one unexplained.
#
# What survives here is the HTML writer, which nothing else produces. Run it
# only when an editable-in-Word copy of this table is wanted.
SRC = THESIS_RESULTS_SRQ4_DIR / "tables" / "11_scenario_comparison.csv"
STEM = "ch8_scenario_comparison"
CHAPTER = "experimental_evaluation"

# Which direction is better, per measure. A measure absent from this map is not
# ranked at all -- silence is the correct default, because ranking a row whose
# direction nobody decided is how a table asserts a comparison that does not
# exist.
LOWER_IS_BETTER = {
    "Median APE (%)": True,
    "Mean APE (%)": True,
    "Consistency, CV across repeats (%)": True,
    "Cost per answer, estimated (USD)": True,
    "Response time (s)": True,
    "Tokens per answer": True,
    "Usable answers": False,
    "Replicability, identical answers (%)": False,
    "Top-answer agreement rate": False,
}

# Capability-matched pairs share a shade, so "does the effect survive on the
# production orchestrator" reads down the table instead of being reconstructed
# from the identifiers.
PAIRS = {
    "A_llm_plain": 0,
    "B_llm_data": 1, "D_prometheus_data": 1,
    "C_llm_model": 2, "E_prometheus_model": 2,
    "F_llm_data_model": 3, "G_prometheus_data_model": 3,
}


def _num(v):
    """The numeric value behind a formatted cell, or None if it isn't one."""
    s = str(v).replace(",", "").replace("$", "").replace("%", "").strip()
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def _ranked(df: pd.DataFrame) -> dict:
    """(measure, column) -> 'best' | 'second', computed from the data."""
    cols = [c for c in df.columns if c != "Measure"]
    marks = {}
    for _, r in df.iterrows():
        measure = r["Measure"]
        if measure not in LOWER_IS_BETTER:
            continue
        vals = {c: _num(r[c]) for c in cols}
        vals = {c: v for c, v in vals.items() if v is not None}
        if len(vals) < 3:
            continue
        order = sorted(vals, key=vals.get, reverse=not LOWER_IS_BETTER[measure])
        top = vals[order[0]]
        # A tie for first is marked on EVERY column that achieves it, not
        # skipped. Skipping was the first implementation and it was wrong in a
        # way that hid the thesis's own result: C and E tie at 100%
        # replicability, 0.0% variation and 1.00 agreement -- the three rows
        # where tool-mediated scenarios are perfect -- so the table showed no
        # highlight exactly where the finding is strongest. An unmarked row also
        # cannot be told apart from one nobody chose to rank.
        winners = [c for c in order if vals[c] == top]
        # A near-universal tie is not a distinction. "Usable answers" is 9 for
        # six of seven scenarios, and shading six cells green emphasises
        # nothing while making the one unshaded cell look like the anomaly it
        # already is. Mark a tie only while it still separates.
        if len(winners) > len(vals) / 2:
            continue
        for c in winners:
            marks[(measure, c)] = "best"
        rest = [c for c in order if vals[c] != top]
        if rest:
            runner = vals[rest[0]]
            for c in (c for c in rest if vals[c] == runner):
                marks[(measure, c)] = "second"
    return marks


# ---------------------------------------------------------------------------
# Format 3: a real HTML table, which Word pastes as an editable Word table.
# ---------------------------------------------------------------------------
_CSS_BEST = "background:#d9ead3;color:#1a7f37;font-weight:700;text-decoration:underline"
_CSS_SECOND = "background:#fff2cc;color:#8a6100;font-weight:700"
_CSS_PLAIN = "color:#1a1a1a"
_SHADES = ["#ffffff", "#f4f4f4", "#ebebeb", "#e2e2e2"]


def write_html(df: pd.DataFrame, marks: dict, out: Path, caption: str) -> Path:
    head = "".join(
        f'<th style="background:#e8e8e8;color:#1a1a1a;border:1px solid #8a8a8a;'
        f'padding:6px 9px;text-align:{"left" if i == 0 else "center"};'
        f'font-family:Helvetica,Arial,sans-serif;font-size:11pt">{c}</th>'
        for i, c in enumerate(df.columns))
    body = []
    for _, r in df.iterrows():
        measure = r["Measure"]
        cells = [
            f'<td style="border:1px solid #8a8a8a;padding:6px 9px;text-align:left;'
            f'font-family:Helvetica,Arial,sans-serif;font-size:11pt;{_CSS_PLAIN}">'
            f'{measure}</td>']
        for c in df.columns[1:]:
            mark = marks.get((measure, c))
            css = {"best": _CSS_BEST, "second": _CSS_SECOND}.get(mark, _CSS_PLAIN)
            shade = _SHADES[PAIRS.get(c, 0) % len(_SHADES)]
            bg = "" if mark else f"background:{shade};"
            cells.append(
                f'<td style="border:1px solid #8a8a8a;padding:6px 9px;'
                f'text-align:center;font-family:Helvetica,Arial,sans-serif;'
                f'font-size:11pt;{bg}{css}">{r[c]}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")

    html = f"""<!doctype html>
<meta charset="utf-8">
<title>Scenario comparison</title>
<body style="font-family:Helvetica,Arial,sans-serif;margin:24px">
<p style="font-size:11pt;color:#1a1a1a;max-width:60em"><b>Comparison of
decision-support scenarios.</b> {caption}</p>
<table style="border-collapse:collapse;border:1px solid #8a8a8a">
<thead><tr>{head}</tr></thead>
<tbody>{''.join(body)}</tbody>
</table>
<p style="font-size:10pt;color:#5a5a5a;margin-top:10px">
<span style="{_CSS_BEST};padding:2px 8px">best</span>
&nbsp;<span style="{_CSS_SECOND};padding:2px 8px">second best</span>
&nbsp;&nbsp;Shared row shading marks capability-matched scenarios
(B/D, C/E, F/G); A is the reference.</p>
<p style="font-size:10pt;color:#5a5a5a">To use: select the table, copy, and
paste into Word. It arrives as an editable Word table with this formatting.</p>
</body>"""
    out.write_text(html, encoding="utf-8", newline="\n")
    print(f"  {out.name}  ({len(df)} rows, HTML -> pastes as an editable table)")
    return out


def main() -> int:
    if not SRC.is_file():
        raise SystemExit(f"missing {SRC}; run export_appendix.py first")
    df = pd.read_csv(SRC)
    marks = _ranked(df)
    caption = ("Performance of each scenario across the evaluation dimensions, "
               "over the 63 funded runs. Best and second-best are computed per "
               "row from the direction that measure improves in.")

    figs = get_chapter_figures_dir(CHAPTER)

    def style_fn(row_label, col, value):
        mark = marks.get((row_label, col))
        return {"best": BEST, "second": SECOND}.get(mark, PLAIN)

    print("Writing the editable-in-Word copy of the scenario comparison:")
    print("  (.md and .svg are both written by export_appendix.py:")
    print("   11_scenario_comparison.md / .svg -- not duplicated here)")
    write_html(df, marks, figs / f"{STEM}.html", caption)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
