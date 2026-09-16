#!/usr/bin/env python3
"""The SRQ4 prompt schema as a composition matrix, for the thesis appendix.

WHY A MATRIX AND NOT THE PROMPTS
--------------------------------
`prompts.py` is the experimental instrument, and the obvious way to show it is to
print it. That was tried and rejected: quoted whole it runs to several pages, and
quoted in abbreviated form -- first and last ten words of every block -- it is
still a wall of text a reader has to assemble a mental model from.

The thing a reader actually needs is not the wording. It is **what varies between
the seven arms and what does not**, because that is the single-variable design
the whole experiment rests on. That is a matrix: one row per prompt component,
one column per scenario, a mark where the arm receives the block.

Read down a column and you see one arm's capability envelope. Read across a row
and you see which arms share a component -- and therefore that B and D's coder
receive byte-identical data and deliverable blocks, which is what makes B->D
isolate the orchestrator rather than confounding it with wording.

EVERY CELL IS DERIVED, NOT TYPED
--------------------------------
Membership is computed by containment against the assembled prompt strings, so a
change to how an arm is composed changes this table. Word counts are `len(split())`
on the component itself. Nothing here is transcribed, and the schema id is the
harness's own hash over every string that reaches the model.

Reads:  04_SRQ4_Scenario_Experiment/scenario_setup/prompts.py (imported)
Writes: 05_thesis_results/08_experimental_evaluation/tables/
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


def _find_repo_root(start: Path) -> Path:
    for cand in (start, *start.parents):
        if any((cand / a).exists() for a in (".env.example", ".env", "PATHS.py")):
            return cand
    raise FileNotFoundError(f"Could not find project root above {start}")


ROOT = _find_repo_root(Path(__file__).resolve().parent)
sys.path.insert(0, str(ROOT))
from PATHS import SRQ4_SCENARIO_SETUP_DIR  # noqa: E402

sys.path.insert(0, str(SRQ4_SCENARIO_SETUP_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prompts as P  # noqa: E402
from styled_tables import render_table, PLAIN  # noqa: E402

# One bit of information, one visual channel. "yes" in a green fill, bold AND
# underlined spent four channels saying the same thing ten times a row, and the
# repetition was most of what made the figure heavy. A bullet reads as a mark
# without asking to be read as a word.
MARK = "•"          # receives this component
CODER_MARK = "c"         # reaches the nested coder only, not the user agent
BLANK = ""


def _components() -> list:
    """(display name, the string) for every composable block, in prompt order.

    Order follows how a prompt is assembled: what every arm gets, then the
    capability blocks that are the treatment, then the per-orchestrator notes.
    """
    return [
        ("The question", P.USER_QUESTION),
        ("Output exemplar", P.OUTPUT_EXEMPLAR),
        ("Sentinel instruction", P.SENTINEL_INSTRUCTION),
        ("No firm data", P.SCENARIO_A_NOTE),
        ("Sales history + schema", P.DATA_BLOCK),
        ("Model forecast payload", P.MODEL_BLOCK),
        ("Forecast tool", P.MODEL_TOOL_BLOCK),
        ("Analysis task", P.ANALYSIS_TASK),
        ("Analysis task, with model", P.ANALYSIS_TASK_WITH_MODEL),
        ("Do not query warehouse", P.NO_WAREHOUSE),
        ("Route to analysis engine", P.ENGINE_NOTE),
    ]


# Which components every arm receives regardless of capability. Kept as a set
# rather than a row count so inserting a component cannot silently shift the
# group boundary.
_UNIVERSAL = {"The question", "Output exemplar", "Sentinel instruction"}


def _arms() -> list:
    """(column label, the assembled string) for each prompt actually sent.

    D, E and G are two prompts each: a user-facing message to the conversational
    agent and a brief to the nested coder. Both are shown, because the coder
    brief is where those arms' data and deliverable live -- collapsing them
    would hide exactly the blocks the matrix exists to compare.
    """
    return [
        ("A", P.SCENARIO_A_NOTE),
        ("B", P.SCENARIO_B_NOTE),
        ("C", P.SCENARIO_C_NOTE),
        ("D user", P.SCENARIO_D_NOTE),
        ("D coder", P.SCENARIO_D_CODER),
        ("E user", P.SCENARIO_E_NOTE),
        ("E coder", P.SCENARIO_E_CODER),
        ("F", P.SCENARIO_F_NOTE),
        ("G user", P.SCENARIO_G_NOTE),
        ("G coder", P.SCENARIO_G_CODER),
    ]


def _receives(name: str, frag: str, assembled: str) -> bool:
    """Does this prompt carry this component?

    The shared parts are appended by the prompt FUNCTIONS rather than composed
    into the capability note, so containment against the note reports them
    absent. Every arm receives them by construction; the first row group says
    so, and the note states it.
    """
    return True if name in _UNIVERSAL else bool(frag and frag in assembled)


def build() -> pd.DataFrame:
    """One row per component, one column per SCENARIO -- not per prompt.

    D, E and G send two prompts each, and showing both doubled the table to ten
    columns of near-identical marks. The split is not lost: a block reaching
    only the nested coder is marked "c", so the column still says where in the
    orchestrator the component lands, in one character instead of a column.
    """
    comps = _components()
    pairs = {}                      # scenario letter -> [(side, assembled)]
    for label, assembled in _arms():
        letter, _, side = label.partition(" ")
        pairs.setdefault(letter, []).append((side or "", assembled))

    rows = []
    for name, frag in comps:
        # The stub column's header is a NON-BREAKING SPACE, not an empty
        # string. render_table bolds every header, and an empty one emits
        # `<B></B>`, which graphviz's HTML-like parser rejects outright:
        # "syntax error ... <B></B> ... in label of node t", and nothing is
        # written. A blank corner still reads as the stub column of a matrix.
        r = {" ": name}
        for letter, sides in pairs.items():
            hits = [side for side, asm in sides if _receives(name, frag, asm)]
            if not hits:
                r[letter] = BLANK
            elif len(hits) == len(sides) or "" in hits:
                r[letter] = MARK
            else:
                # Reaches only the nested coder, not the user-facing agent.
                r[letter] = CODER_MARK
        rows.append(r)
    return pd.DataFrame(rows)


def _group(label) -> int:
    """Shared-by-all, then the capability blocks that are the treatment."""
    return 0 if str(label) in _UNIVERSAL else 1


def composition() -> dict:
    """The schema as data: each arm, the components it carries, in order.

    This is the compact machine-readable twin of the figure. It deliberately
    holds NO prompt text -- an abbreviated-text version was tried and was still
    a wall of prose. What a reader or an agent needs from the schema is the
    COMPOSITION, and that is a dozen lists of keys.
    """
    comps = _components()
    # Each arm lists only what it ADDS. The three universal components are
    # stated once in `shared_by_every_arm`; repeating them in all ten arms was
    # 30 of ~90 lines saying nothing that varies -- the same redundancy the
    # figure was carrying as ten identical marks a row.
    arms = {}
    for label, assembled in _arms():
        arms[label] = [name for name, frag in comps
                       if name not in _UNIVERSAL
                       and _receives(name, frag, assembled)]
    return {
        "schema": P.schema_id(),
        "shared_by_every_arm": [n for n, _ in comps if n in _UNIVERSAL],
        "component_words": {name: len(str(frag).split()) for name, frag in comps},
        "arms_add": arms,
    }


def main() -> None:
    df = build()
    n_arms = len([c for c in df.columns if c.strip()])

    def style(_row, _col, _val):
        # PLAIN throughout. The bullet already says "present", and a green
        # fill behind it would be a second channel carrying the same one bit --
        # the redundancy that made the first version of this figure heavy.
        # Semantic colour is reserved for tables that rank something; this one
        # states membership, which has no winner.
        return PLAIN

    # Bound once, so the SVG and the .md cannot state different things. The
    # contract is that neither rendering silently drops a caveat the other
    # carries, and passing these inline twice is how that drift starts.
    title = "Composition of the scenario prompts"
    # Short deliberately. A graph label is laid out as one line per wrapped
    # segment and sets a FLOOR on the figure's width, so a five-line caption
    # under a narrow matrix stretches it; the rest belongs in the chapter.
    caption = ("Prompt components by scenario. Only the blocks below the rule "
               "differ between arms; those are the treatment.")
    note = (
        f"• the arm receives this component; c reaches only the nested "
        f"coder, not the conversational agent. Membership is computed from the "
        f"assembled prompts, so an arm cannot appear to share a component it "
        f"does not. Schema {P.schema_id()}.")

    out = render_table(
        df,
        # No sequence prefix. The appendix exporter assigns those dynamically
        # from generation order, and a typed one collided with
        # `28_per_run_record_p6` the moment that split grew a part -- F6 again,
        # a generation-order prefix used as an identity. This producer runs
        # separately, so its table sorts by name rather than by number.
        stem="prompt_schema_composition",
        chapter="experimental_evaluation",
        title=title,
        caption=caption,
        style_fn=style,
        row_group=_group,
        legend=(),
        note=note)
    # The .md twin, so this table is readable and greppable like every other
    # appendix table and carries the SAME note the SVG does. The contract is
    # that neither rendering may silently drop a caveat the other states.
    md = out.with_suffix(".md")
    md.write_text(
        "\n".join([f"**{title}.** {caption}", "", df.to_markdown(index=False),
                   "", f"*Note.* {note}"]) + "\n",
        encoding="utf-8", newline="\n")
    df.to_csv(out.with_suffix(".csv"), index=False, encoding="utf-8")

    # The compact JSON twin: the composition as data, no prompt text. Written
    # beside the figure rather than in tables/, because it is a source for an
    # agent reading the schema rather than an appendix artefact itself.
    src = out.parent.parent / ".source_md"
    src.mkdir(parents=True, exist_ok=True)
    (src / "prompt_schema_composition.json").write_text(
        json.dumps(composition(), indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")

    print(f"  {out.relative_to(ROOT)}")
    print(f"  {len(df)} components x {n_arms} prompts, schema {P.schema_id()}")

    try:
        from check_reader_facing import warn_after_run
        warn_after_run()
    except ImportError:
        pass


if __name__ == "__main__":
    main()
