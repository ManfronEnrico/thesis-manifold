# Orphan conceptual diagrams

Hand-made diagrams with **no producing script**. They are legitimate — a diagram
of an idea has no dataset behind it — but their staleness is a human judgement,
not something a re-run can fix. Moved here 2026-09-06 from
`05_thesis_writing/figures/{unsure,update_formatting,update_information}/`
(P0046 DEC-SINGLE-HOME: artefacts live in the results tier, never the writing tier).

| File | Prior triage folder | State |
|------|--------------------|-------|
| `ch2_gap_diagram` | `unsure/` | content unreviewed |
| `ch5_architecture_v1` | `update_formatting/` | content OK, formatting flagged |
| `ch1_research_questions_tree` | `update_information/` | **content stale** — the RQ/SRQ set has changed since it was drawn |

None is cited by filename in any chapter (checked against the 2026-09-05 snapshot).

## `ch1_research_questions_tree` — decided, not yet built

Brian's call (P0046 F18): **add it to `generate_architecture_diagrams.py`** as a
seventh graphviz figure rather than redraw by hand. The RQ set has already moved
once; a node list is a cheap edit next time it moves, whereas a hand-drawn tree
goes stale silently and nothing detects it. Until that lands, the PNG/SVG here
are the only copies and they show the OLD research questions — do not paste them
into the thesis.

## The other two

`ch2_gap_diagram` and `ch5_architecture_v1` have no such decision yet. Either
adopt them (record their source, accept manual upkeep) or rebuild them in the
generator. `ch5_architecture_v1` overlaps `system_architecture_v1`, which IS
generated — worth checking whether it is redundant before investing in it.

---

## 2026-09-07 — all three are now superseded by generated figures

Brian's call (P0046 Phase 4): **generate everything programmatically.** All
three hand-drawn diagrams now have a generated replacement in the parent
`diagrams/` folder, produced by `generate_architecture_diagrams.py`:

| Hand-drawn (here) | Generated replacement | Why the hand-drawn one is wrong |
|---|---|---|
| `ch1_research_questions_tree` | `ch1_research_questions_tree_v2` | showed a superseded RQ set |
| `ch2_gap_diagram` | `ch2_gap_diagram_v2` | stated the envelope as **8 GB**; it is 4096 MB |
| `ch5_architecture_v1` | `ch5_layered_architecture_v2` | claimed a five-model substrate, human-in-the-loop checkpoints and a LangGraph deployment — none of which exist |

**These files are kept as the record of what was drawn before, and must not be
pasted into the thesis.** Every one of them contains at least one claim the code
contradicts. Re-run the generator instead; it reads its numbers from artefacts
at render time and refuses to draw when a source table is missing.
