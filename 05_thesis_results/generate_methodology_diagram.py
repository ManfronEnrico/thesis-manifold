"""The methodology figure: how Design Science Research structures this thesis.

WHY THIS GENERATOR IS DIFFERENT FROM THE OTHERS
-----------------------------------------------
Every other producer in this tier reads a measured artefact -- a results CSV, a
parquet matrix, a run manifest. There is no such artefact behind a methodology
chapter: the chapter IS the source, and it is prose.

So this reads the prose. Section numbers and titles are parsed from the current
methodology chapter in the newest docx snapshot, and the figure is built from
what the parse returns. Rename a section in Word, re-run the snapshot, re-run
this, and the figure follows. That is the same contract the other generators
hold -- read the source at render time, never type its content here -- applied
to the one chapter whose source happens to be written rather than computed.

WHAT IS PARSED AND WHAT IS CURATED
----------------------------------
Parsed, and therefore incapable of drifting from the chapter:

  * the section numbers and titles of chapter 3
  * which sub-questions the chapter names, and the chapter each DSR process
    activity is mapped onto, both read from the running text

Curated, because no artefact states it:

  * the SHAPE -- that 3.1-3.2 are foundations, 3.3-3.5 the design, 3.6-3.7 the
    bounds. That grouping is an editorial reading of the chapter, and it is
    declared in _GROUPS below rather than inferred, so a reader of this file
    can see exactly which claim is ours.
  * the one-line gloss under each section title, which compresses a
    several-hundred-word section into something that fits a box.

A guard fails the run if the chapter contains a section this file has not
grouped, so a new section cannot be silently dropped from the figure.

USAGE
    python 05_thesis_results/generate_methodology_diagram.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

for _c in (Path(__file__).resolve().parent, *Path(__file__).resolve().parents):
    if any((_c / a).exists() for a in (".env.example", ".env", "PATHS.py")):
        sys.path.insert(0, str(_c))
        break

from PATHS import THESIS_WRITING_SNAPSHOTS_DIR  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
# The house style lives with the architecture diagrams; importing it keeps ONE
# palette, one caption rule and one save path for every figure in the thesis.
# A second copy of _stack/_g here would drift the moment either was adjusted.
from generate_architecture_diagrams import (  # noqa: E402
    _stack, _g, _caption, _save, CLUSTER, LINE, ACCENT)
from review_notes import write_review_note  # noqa: E402

_PRODUCER = "05_thesis_results/generate_methodology_diagram.py"

# The editorial reading: which sections form which phase of the argument.
# Declared, not inferred -- see the module docstring.
_GROUPS = [
    ("Foundations", ["3.1", "3.2"],
     "why this methodology, and on what philosophical grounds"),
    ("Research design", ["3.3", "3.4", "3.5"],
     "what is studied, with which data, and how each question is answered"),
    ("Quality and bounds", ["3.6", "3.7"],
     "what the design secures, and what it cannot claim"),
]

# One line per section. Compresses the section; does not reinterpret it.
_GLOSS = {
    "3.1": "pragmatism: an artefact is judged by whether it works",
    "3.2": "build an artefact, then evaluate it against stated objectives",
    "3.3": "controlled experiment inside a single embedded case",
    "3.4": "one commercial scanner panel, used under confidentiality",
    "3.5": "a distinct evaluation protocol for each sub-question",
    "3.6": "internal, external and construct validity, and reliability",
    "3.7": "confidentiality, series length, pilot scale, sequential execution",
}


def _snapshot() -> Path:
    """The newest docx snapshot on disk.

    Newest by NAME, not mtime: snapshot folders are stamped
    `YYYY-MM-DD_HH-MM_<slug>`, so lexical order is chronological order, and a
    folder copied or touched later does not thereby become the current one.
    """
    snaps = sorted(p for p in THESIS_WRITING_SNAPSHOTS_DIR.glob("20*_*")
                   if p.is_dir())
    if not snaps:
        # The snapshot tree is part of the writing harness and is not
        # distributed, so this is the expected state in a released copy of the
        # repository rather than a fault. Say so, instead of naming a tool that
        # copy does not contain.
        raise SystemExit(
            f"no chapter snapshot under {THESIS_WRITING_SNAPSHOTS_DIR}. "
            f"This figure is built from the methodology chapter text, which is "
            f"part of the writing workspace rather than the distributed code.")
    return snaps[-1]


def _methodology_file(snap: Path) -> Path:
    """The methodology chapter, found by SUBJECT rather than by number.

    Chapter numbers move -- Ch5 and Ch6 were swapped on 2026-09-08 -- so a
    hardcoded `ch3-methodology.md` would silently read the wrong chapter after
    a reorder, or fail. The subject is the stable half of the filename.
    """
    hits = sorted((snap / "chapters").glob("ch*-methodology.md"))
    if not hits:
        raise SystemExit(f"no methodology chapter in {snap / 'chapters'}")
    return hits[0]


def _sections(text: str) -> dict:
    """{number: title} for every `## 3.N Title` heading, in document order."""
    out = {}
    for num, title in re.findall(r"^##\s+(3\.\d+)\s+(.+?)\s*$", text, flags=re.M):
        out.setdefault(num, title.strip())
    return out


def _chapter_number(path: Path) -> str:
    """The chapter's number, from its snapshot filename."""
    m = re.match(r"ch(\d+)-", path.name)
    return m.group(1) if m else "3"


def _srqs(text: str) -> list:
    """The sub-questions the chapter names, with the subject of each.

    Read from the bolded `**SRQN** - **subject.**` lead-ins that open each
    protocol in the analytical-approach section, so the figure names exactly
    the questions the chapter sets out to answer.
    """
    found = {}
    # The exported prose separates the bold runs with stray markup, so the
    # pattern tolerates whatever sits between the label and its subject.
    for n, subject in re.findall(
            r"\*\*SRQ(\d)\*\*.{0,12}?\*\*\s*(.+?)\.\*\*", text, flags=re.S):
        subject = re.sub(r"[*_]", "", subject)
        subject = re.sub(r"\s+", " ", subject).strip()
        # The chapter writes "**SRQ1** **-** **subject.**", so the separating
        # dash lands at the head of the captured subject. Strip it: the figure
        # already separates label from subject by putting them on two lines,
        # and a leading "- " there reads as a bullet that is not one.
        subject = re.sub(r"^[-‐-―]\s*", "", subject).strip()
        found.setdefault(n, subject)
    return [(n, found[n]) for n in sorted(found)]


def _activity_chapters(text: str) -> list:
    """The six DSR process activities and the chapter(s) each is realised in.

    Parsed from the sentences that map an activity onto a chapter, so the
    figure cannot claim a mapping the chapter does not make.
    """
    acts = [
        ("Problem identification", r"[Pp]roblem identification and motivation"),
        ("Objectives", r"definition of objectives for a solution"),
        ("Design and development", r"[Dd]esign and development"),
        ("Demonstration", r"[Dd]emonstration, the fourth activity"),
        ("Evaluation", r"[Ee]valuation, the fifth activity"),
        ("Communication", r"[Cc]ommunication, the sixth activity"),
    ]
    out = []
    for label, pat in acts:
        m = re.search(pat + r"(.{0,240}?)(?:\.\s|$)", text, flags=re.S)
        where = ""
        if m:
            tail = m.group(1)
            if (c := re.search(r"Chapters?\s+(\d+)(?:\s*(?:through|and)\s*(\d+))?",
                               tail)):
                where = (f"Chapters {c.group(1)}-{c.group(2)}" if c.group(2)
                         else f"Chapter {c.group(1)}")
            elif re.search(r"subsidiary research questions", tail):
                # Not every activity is realised in a chapter. The chapter maps
                # the objectives activity onto the sub-questions themselves, so
                # the figure says that rather than inventing a chapter number.
                where = "the four sub-questions"
            elif re.search(r"this thesis", tail):
                where = "this thesis"
        out.append((label, where))
    return out


def fig_methodology() -> None:
    snap = _snapshot()
    path = _methodology_file(snap)
    text = path.read_text(encoding="utf-8")

    secs = _sections(text)
    if not secs:
        raise SystemExit(f"parsed no sections from {path.name} -- "
                         f"has the chapter's heading structure changed?")

    # A section present in the chapter but absent from the curated grouping
    # would vanish from the figure with nothing to report it. Fail instead.
    grouped = {n for _, nums, _ in _GROUPS for n in nums}
    if missing := sorted(set(secs) - grouped):
        raise SystemExit(
            f"{path.name} has section(s) {', '.join(missing)} that _GROUPS does "
            f"not place: {[secs[n] for n in missing]}. Add them to a group (and "
            f"give each a line in _GLOSS) rather than letting the figure drop them.")

    srqs = _srqs(text)
    if len(srqs) != 4:
        raise SystemExit(
            f"parsed {len(srqs)} sub-question(s) from {path.name}, expected 4. "
            f"The chapter's '**SRQN** - **subject.**' lead-ins have changed "
            f"shape; fix _srqs rather than shipping a figure missing a question.")

    acts = _activity_chapters(text)
    if blank := [a for a, w in acts if not w]:
        raise SystemExit(
            f"no realisation parsed for DSR activity/activities {blank} in "
            f"{path.name}. An activity drawn with an empty right-hand side "
            f"reads as unrealised; fix _activity_chapters or the chapter.")

    chn = _chapter_number(path)

    g = _g("methodology", rankdir="LR")
    g.attr(ranksep="0.55", nodesep="0.4")

    # Left to right: the grounds, the design, the bounds. One cluster per phase,
    # each holding its sections as rows in declaration order -- _stack rather
    # than a cluster of nodes, because 3.1 before 3.2 IS the argument.
    SW = {"width": "3.0", "fixedsize": "false"}
    prev = None
    for gi, (label, nums, gloss) in enumerate(_GROUPS):
        nid = f"grp{gi}"
        rows = [(f"{n} {secs[n]}", _GLOSS.get(n, "")) for n in nums if n in secs]
        g.node(nid, _stack(gloss, rows), shape="box", style="filled",
               fillcolor=CLUSTER, color=LINE, **SW)
        if prev:
            g.edge(prev, nid, color=LINE, arrowsize="0.7")
        prev = nid

    # The six DSR activities, and where each is realised. This is the spine the
    # chapter builds its design on, so it sits beneath the phases it produces.
    # The six activities as ONE node. Splitting them across two boxes was tried
    # and reverted: under rankdir=LR graphviz stacked the two boxes vertically,
    # so activities 4-6 rendered ABOVE 1-3 and the sequence read backwards. The
    # order is the content here, so it cannot be handed to the layout engine --
    # the same reasoning _stack's docstring records.
    #
    # Height is controlled instead by dropping the activity list into the same
    # column as the first phase, which is where the chapter puts it: the process
    # model is what the foundations sections adopt.
    # Pinned to the first phase's rank rather than left to find its own column.
    # Unpinned it added a seventh column and took the figure to a 5.17 ratio;
    # sharing grp0's rank puts it where the chapter puts it -- the process model
    # the foundations sections adopt -- and holds the width.
    with g.subgraph() as col:
        col.attr(rank="same")
        col.node("dsr", _stack("the DSR process (Peffers et al., 2007), "
                               "and where each activity is realised",
                               [(a, w) for a, w in acts]),
                 shape="box", style="filled", fillcolor=CLUSTER, color=LINE,
                 **SW)
        col.node("grp0")

    # The four sub-questions, each with its own evaluation protocol. Drawn as
    # the outcome: this is what the methodology exists to answer.
    if srqs:
        g.node("srq", _stack("one evaluation protocol per sub-question",
                             [(f"SRQ{n}", s) for n, s in srqs]),
               shape="box", style="filled", fillcolor="white", color=ACCENT,
               penwidth="1.5", width="3.4", fixedsize="false")
        g.edge(prev, "srq", color=ACCENT, arrowsize="0.7")

    g.edge("dsr", "grp0", color=LINE, style="dashed", arrowsize="0.7")

    _caption(g, "Methodological structure of the thesis. A pragmatist position "
                "grounds the choice of Design Science Research, whose six "
                "process activities are realised across the chapters named; the "
                "research design then specifies what is studied and with which "
                "data, and commits each subsidiary research question to its own "
                "evaluation protocol before the validity conditions and the "
                "bounds of the resulting claims are stated.")

    stem = f"ch{chn}_methodology_design_v1"
    svg = _save(g, stem)

    n_sec, n_act = len(secs), sum(1 for _, w in acts if w)
    write_review_note(
        "methodology_design",
        svg,
        "Methodological structure of the thesis",
        f"Parsed from `{path.relative_to(snap.parent.parent.parent).as_posix()}` "
        f"in snapshot `{snap.name}`: {n_sec} sections, {len(srqs)} sub-questions, "
        f"{n_act} of {len(acts)} DSR activities carrying an explicit chapter.\n\n"
        "Two halves, different provenance. PARSED: section numbers and titles, "
        "the sub-question subjects, and the activity-to-chapter mapping -- all "
        "re-read on every run, so a chapter edit cannot leave them stale. "
        "CURATED: the three-phase grouping in `_GROUPS` and the one-line gloss "
        "per section in `_GLOSS`. Those are an editorial reading of the chapter "
        "and there is no artefact to derive them from.\n\n"
        "The generator FAILS if the chapter gains a section that `_GROUPS` does "
        "not place, so a new section cannot silently vanish from the figure. It "
        "reads the newest snapshot by folder name -- re-run "
        "`thesis_snapshot.py` before regenerating after editing the chapter in "
        "Word, or this reads the previous export.\n\n"
        "Chapter number comes from the snapshot filename, so a reorder in Word "
        "refiles the figure by itself.",
        _PRODUCER)


def main() -> None:
    print("Building the methodology diagram from the current chapter prose...\n")
    fig_methodology()
    print("\nDone.")


if __name__ == "__main__":
    main()
