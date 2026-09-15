"""Appendix tables rendered as SVG, with colour and type carrying meaning.

WHY THIS EXISTS ALONGSIDE THE MARKDOWN TABLES
---------------------------------------------
The `.md` tables are kept and are still the default. They paste into Word as a
real table, and their text is searchable in the final PDF -- both of which are
why they were chosen. What they cannot do is encode more than two states:
Markdown defines bold and italic and nothing else, so `_bold_best()` has to
express "the winner" as `***value***` and has no way to say "second best",
"best in class" or "these two rows are a matched pair".

This module renders the SAME DataFrame as an SVG whose cells carry background
shade, text colour, weight, slant and underline independently. It is additive:
a table can be emitted as `.md`, as `.svg`, or as both.

MEASURED, NOT ASSUMED
---------------------
Graphviz HTML-like labels rendered to SVG produce real `<text>` elements:

    <text ... font-weight="bold" text-decoration="underline" ...>17.4%</text>

So the text is selectable, searchable and copy-pasteable in the PDF. **No OCR
step is needed.** That was the open question and the answer is no.

Verified 2026-09-14 in this repository: `font-weight="bold"`,
`font-style="italic"`, `text-decoration="underline"`, per-cell `BGCOLOR` and
arbitrary `COLOR` all survive the SVG render.

WHAT IT COSTS
-------------
An SVG pastes into Word as a picture, not as a table -- so its cells cannot be
edited in the document, and Word's caption/cross-reference numbering treats it
as a figure. That is the trade: richer encoding, less editability. Use it where
the encoding carries an argument the reader would otherwise have to assemble
from the numbers, and keep Markdown where the table is a plain lookup.

THE ENCODING IS A CONTRACT
--------------------------
Every visual channel means exactly one thing, and the legend is rendered from
the same constants that drive the cells -- so a figure cannot acquire a colour
its legend does not explain.
"""
from __future__ import annotations

import sys
from pathlib import Path

import graphviz
import pandas as pd


def _find_repo_root(start: Path) -> Path:
    for cand in (start, *start.parents):
        if any((cand / a).exists() for a in (".env.example", ".env", "PATHS.py")):
            return cand
    raise FileNotFoundError(f"Could not find project root above {start}")


sys.path.insert(0, str(_find_repo_root(Path(__file__).resolve().parent)))
from PATHS import get_chapter_tables_dir  # noqa: E402

__all__ = ["render_table", "BEST", "SECOND", "POOR", "PLAIN"]

# Cambria, not Times New Roman. The Times files are installed in Windows, but
# graphviz ships its own text stack and never sees them: it falls back to a sans
# face for METRICS while the SVG still names Times, so the text would display in
# one font and every column width be computed in another. Cambria loads cleanly,
# is a Microsoft serif designed for body text, and at 9pt measures slightly
# narrower than Times (189 vs 219 on the same string), which helps wide tables.
FONT = "Cambria"
SIZE = "9"

# There is no semi-bold in this toolchain. Measured: "Cambria Semibold" renders
# identically to "Cambria Bold", and so does a deliberately invented font name --
# the matcher maps anything unrecognised to a bold default. Two weights only;
# the contrast between header and first column comes from the BORDERS.
INK = "#1a1a1a"
MUTE = "#5a5a5a"
RULE = "#000000"        # header, first column, last row: structural
GROUP_RULE = "#d0d0d0"  # row-group separators: quieter, they band rather than divide
PAPER = "#ffffff"

# ---------------------------------------------------------------------------
# The encoding. One meaning per channel; the legend is generated from it.
# ---------------------------------------------------------------------------
BEST = {"bg": "#d9ead3", "fg": "#1a7f37", "bold": True, "underline": True,
        "legend": "best across all scenarios"}
SECOND = {"bg": "#fff2cc", "fg": "#8a6100", "bold": True,
          "legend": "second best"}
POOR = {"bg": "#f4cccc", "fg": "#a31515",
        "legend": "criterion not met"}
PLAIN = {"legend": None}

# The ground is white throughout. Row banding by shade was tried and dropped:
# shading is reserved for MEANING (best / second / not-met), and a decorative
# band competes with it. Grouping is shown by the grey top/bottom rules instead.
_PAIR_SHADE = [PAPER]

# A4 landscape, 29.7 x 21 cm, margins 2/2/1/1 -> a 27.7 x 17 cm text block.
# That is 785 x 482 pt and a ratio of 1.63.
#
# A CEILING, NOT A TARGET. Anything wider must be scaled down to fit and becomes
# unreadable; a narrow table stays narrow, because stretching a four-column
# lookup to fill the width adds whitespace rather than information.
PAGE_W_PT = 785.0
PAGE_H_PT = 482.0
PAGE_RATIO = PAGE_W_PT / PAGE_H_PT


def _esc(s) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def _sides(*, top=False, right=False, bottom=False, left=False) -> str:
    """Graphviz SIDES string. Empty means NO SIDE WAS ASKED FOR.

    It does NOT mean "draw nothing" -- see `_border_attrs`, which is the only
    place allowed to turn this into markup. Under CELLBORDER="1" an empty SIDES
    falls back to the graphviz default of ALL FOUR sides, so a cell that omits
    it gets a full box: the grid this styling exists to remove.
    """
    return ("T" if top else "") + ("R" if right else "") + \
           ("B" if bottom else "") + ("L" if left else "")


def _border_attrs(sides: str | None, rule: str) -> str:
    """Per-cell border markup. The ONE place that decides drawn vs not drawn.

    MEASURED 2026-09-15, because the obvious spelling is wrong. Counts below
    exclude the one <polygon> every SVG carries for the graph background:

        CELLBORDER="1" + SIDES=""              -> a full box   (the bug)
        CELLBORDER="1" + SIDES="none" / " "    -> a full box
        CELLBORDER="0" on the table            -> nothing draws, SIDES ignored
        CELLBORDER="1" + BORDER="0" on a cell  -> nothing draws  <-- this one

    So "no border" is a property of the CELL (`BORDER="0"`), not an empty
    SIDES, and it composes: a sibling cell in the same row still renders its
    own `SIDES="B"` rule normally. That is what lets the table keep
    CELLBORDER="1" for the cells that DO carry a rule while the interior stays
    clean.

    COLOR is omitted where nothing is drawn. Naming a colour for an absent
    border is harmless to graphviz and misleading to the next reader.
    """
    if not sides:
        return 'BORDER="0"'
    return f'BORDER="1" SIDES="{sides}" COLOR="{rule}"'


def _cell(value, style: dict, align="LEFT", bg=None, wrap=0,
          sides: str | None = None, rule: str = RULE) -> str:
    """One table cell, with the encoding applied as markup rather than text.

    `wrap` breaks long text across lines. Graphviz sizes a cell to its longest
    unbroken string, so a single 46-character label in the first column sets the
    width of the whole table: measured 2026-09-14, three tables ran past the A4
    cap purely on first-column text while their headers were under ten
    characters. Wrapping the cell fixes what narrowing the header cannot.
    """
    # Borders go through _border_attrs, never spelled inline. A cell that wants
    # no rule needs BORDER="0"; an empty SIDES means all four (F37).
    attrs = (f'ALIGN="{align}" BALIGN="{align}" CELLPADDING="5" '
             + _border_attrs(sides, rule))

    if wrap and len(str(value)) > wrap:
        return (f'<TD BGCOLOR="{style.get("bg") or bg or PAPER}" {attrs}>'
                + "<BR/>".join(_esc(ln) for ln in _wrap(value, wrap))
                + "</TD>")
    txt = _esc(value)
    if style.get("bold"):
        txt = f"<B>{txt}</B>"
    if style.get("italic"):
        txt = f"<I>{txt}</I>"
    if style.get("underline"):
        txt = f"<U>{txt}</U>"
    if style.get("fg"):
        txt = f'<FONT COLOR="{style["fg"]}">{txt}</FONT>'
    fill = style.get("bg") or bg or PAPER
    return f'<TD BGCOLOR="{fill}" {attrs}>{txt}</TD>'


def _legend_row(styles: list) -> str:
    """The key, built from the same constants that styled the cells."""
    parts = []
    for st in styles:
        if not st.get("legend"):
            continue
        # The swatch keeps all four sides: it is a colour sample, and an
        # unoutlined pale fill on white has no edge to read. The one place a
        # full box is deliberate, so it asks rather than inheriting (F37).
        parts.append(
            f'{_cell(" ", st)}'
            f'<TD BORDER="0" ALIGN="LEFT" CELLPADDING="6">'
            f'<FONT POINT-SIZE="10" COLOR="{MUTE}">{_esc(st["legend"])}</FONT></TD>')
    return "".join(parts)


# Characters per line for the caption and the note. 118 was the first value and
# was too generous: a 115-character line at 10pt is already ~700pt, so the prose
# below a small table still set its width. 78 keeps a caption near the measure
# of running text, which is what it is.
_CAPTION_WRAP = 78
_NOTE_WRAP = 96


def _wrap(text: str, width: int = _NOTE_WRAP) -> list:
    """Greedy wrap. Graphviz does not wrap a label, so an unwrapped note sets
    the figure width and stretches the table above it into a ribbon."""
    words, line, out = str(text).split(), "", []
    for w in words:
        if line and len(line) + 1 + len(w) > width:
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    if line:
        out.append(line)
    return out


def render_table(df: pd.DataFrame, *, stem: str, chapter: str, title: str,
                 caption: str, style_fn=None, row_group=None,
                 legend=(BEST, SECOND, POOR), note: str = "") -> Path:
    """Render `df` as a styled SVG under the chapter's figures directory.

    Args:
      style_fn: (row_label, column, value) -> style dict. Called per cell, so
        the encoding is computed from the data on every run and cannot be
        typed in. Omit it for a lookup table: the house styling still applies,
        and no cell claims a comparison the table does not make.
      row_group: optional (row_label) -> int, selecting a background shade so
        related rows read as a block.
      note: the same footnote the .md carries. Without it the SVG silently
        drops the caveats the Markdown states -- which is how the scenario
        table shipped an "unknown" cell with nothing to explain it.
    """
    if style_fn is None:
        def style_fn(_row, _col, _val):
            return PLAIN
        legend = ()
    cols = list(df.columns)
    n_rows = len(df)

    # Header: bold, white ground, a black rule underneath and nothing else.
    # With the first column's right-hand rule and the last row's underline this
    # forms the "H" the styling contract asks for -- structure carried by rules
    # rather than by fills, which stay free to mean something.
    head = "".join(
        f'<TD BGCOLOR="{PAPER}" ALIGN="LEFT" BALIGN="LEFT" CELLPADDING="5" '
        + _border_attrs(_sides(bottom=True, right=(i == 0)), RULE)
        + f'><B>{_esc(c)}</B></TD>'
        for i, c in enumerate(cols))
    rows = [f"<TR>{head}</TR>"]

    # Wrap only where a column actually runs long. Measured per column so a
    # table of short values is never broken up for a rule that does not bind.
    widths = {c: int(df[c].astype(str).str.len().max() or 0) for c in cols}
    wrap_at = {c: (34 if widths[c] > 34 else 0) for c in cols}

    # Where consecutive rows change group, the boundary gets a light rule: the
    # band is shown by separating it, not by shading it.
    groups = [row_group(r[cols[0]]) if row_group else 0
              for _, r in df.iterrows()]

    for i, (_, r) in enumerate(df.iterrows()):
        label = r[cols[0]]
        last = (i == n_rows - 1)
        starts_group = row_group is not None and i > 0 and groups[i] != groups[i - 1]

        def _side(col_i: int) -> str:
            return _sides(
                top=starts_group,
                # First column carries the vertical rule that separates the
                # row label from the values it labels.
                right=(col_i == 0),
                bottom=last,
            )

        def _colour(col_i: int) -> str:
            # A group boundary is quieter than the table's own structure, but
            # the first column's rule and the final underline stay black.
            return RULE if (col_i == 0 or last) else (
                GROUP_RULE if starts_group else RULE)

        cells = [_cell(label, {**PLAIN, "bold": True}, align="LEFT",
                       bg=PAPER, wrap=wrap_at[cols[0]],
                       sides=_side(0), rule=_colour(0))]
        for j, c in enumerate(cols[1:], start=1):
            cells.append(_cell(r[c], style_fn(label, c, r[c]), align="LEFT",
                               bg=PAPER, wrap=wrap_at[c],
                               sides=_side(j), rule=_colour(j)))
        rows.append("<TR>" + "".join(cells) + "</TR>")

    # The legend and the note are CHROME, not data: they sit below the last
    # row's rule and carry no border of their own. Each spacer and each block
    # therefore states BORDER="0" -- inheriting the table's CELLBORDER="1"
    # default drew a rectangle around both, which read as a second table
    # rather than as a footnote (G6).
    key = _legend_row(list(legend))
    if key:
        rows.append(f'<TR><TD COLSPAN="{len(cols)}" BORDER="0" '
                    f'CELLPADDING="2"></TD></TR>')
        rows.append(f'<TR><TD COLSPAN="{len(cols)}" BORDER="0" ALIGN="LEFT">'
                    f'<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">'
                    f'<TR>{key}</TR></TABLE></TD></TR>')

    # The note travels INSIDE the table, not in the graph caption: a graphviz
    # label is centred under the drawing and cannot be left-aligned per line,
    # and a multi-sentence caveat set centred reads as a pull-quote.
    #
    # Wrapped to the TABLE'S OWN width, not a fixed column. A constant wrap ran
    # both ways and both were wrong: too narrow and a wide table's note sat in a
    # ribbon down one third of it; too wide and a small table's note set the
    # figure width itself -- measured, the 96-character note was what held
    # 12_outcome_taxonomy at 1.84 after its headers had already been fixed.
    #
    # Roughly two characters per unit of column width at 9pt, floored so a
    # one-column table still gets a readable measure.
    if note:
        note_wrap = max(60, min(_NOTE_WRAP, sum(
            max(len(str(c)), widths[c]) + 3 for c in cols)))
        body = "".join(
            f'<TR><TD ALIGN="LEFT" CELLPADDING="1">'
            f'<FONT POINT-SIZE="9" COLOR="{MUTE}">{_esc(ln)}</FONT></TD></TR>'
            for ln in _wrap(f"Note. {note}", note_wrap))
        rows.append(f'<TR><TD COLSPAN="{len(cols)}" BORDER="0" '
                    f'CELLPADDING="3"></TD></TR>')
        rows.append(f'<TR><TD COLSPAN="{len(cols)}" BORDER="0" ALIGN="LEFT">'
                    f'<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">'
                    f'{body}</TABLE></TD></TR>')

    label = (f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" '
             f'CELLPADDING="0" COLOR="{RULE}">{"".join(rows)}</TABLE>>')

    g = graphviz.Digraph(stem)
    g.attr(bgcolor="white", fontname=FONT)
    g.attr("node", shape="plaintext", fontname=FONT, fontcolor=INK,
           fontsize="11")
    g.node("t", label)
    # Wrap the caption BEFORE graphviz sees it. A graph label is laid out as one
    # unbroken line, so it sets the figure width directly: measured 2026-09-14,
    # a 452-character caption produced a 1700pt-wide figure at ratio 7.00 for a
    # three-row table. The table itself was never the problem -- neither header
    # length nor cell length, both of which were tried first and moved nothing.
    cap_wrap = max(56, min(_CAPTION_WRAP, sum(
        max(len(str(c)), widths[c]) + 3 for c in cols)))
    g.attr(label="\n" + "\n".join(_wrap(caption, cap_wrap)),
           labelloc="b", labeljust="c", fontsize="10", fontcolor=MUTE)

    # A rendered table belongs with the tables, not with the figures. figures/
    # holds DIAGRAMS -- flowcharts and conceptual drawings; a table stays a
    # table whichever format it is written in.
    out = get_chapter_tables_dir(chapter) / f"{stem}.svg"
    g.render(out.with_suffix(""), format="svg", cleanup=True)
    print(f"  {stem}.svg  ({len(df)} rows, styled)")
    return out
