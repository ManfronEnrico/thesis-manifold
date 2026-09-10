---
name: generated-artefact-provenance
description: RULE - Every number in a generated table, report, appendix or figure is computed from a consumed input at generation time. No result is a hardcoded literal - not in a caption, not in a body cell, not in an internal review note.
category: governance
applies-to: [any script that writes a .md/.csv/.svg thesis artefact - results tables, appendix exporters, training_report.py, generate_*.py, export_appendix.py]
triggers: [writing a number into a generated table, citing a WMAPE/pp/percentage in a caption, adding a review note with a measurement, a re-run did not update a figure it should have]
created: 2026_09_10-14_40
updated: 2026_09_10-14_40
---

# Generated artefacts: compute every number, hardcode none

`figure-generation-standards.md` says this for figures. It holds for **every**
generated artefact — results tables, appendix exporters, `training_report.md`,
the `_emit(...)` captions and `review=` blocks in `export_appendix.py`.

A hardcoded result is a lie waiting to happen. It was true when it was typed;
the next re-run changes the inputs and the number stays. P0053 F8: appendix
table 98 cited *"raised mean test WMAPE from 26.44 to 28.82"* — a measurement
from a 2026-09-06 run on a 16-feature set, written into the source as a string.
The feature set became 18, the script was re-run, the table's structure updated,
and the number did not, because nothing computed it.

## Quick Reference

| Kind of number | Rule |
|---|---|
| A metric in a table cell | computed from the input CSV this run, formatted at write time (`f"{x:.1f}"`) |
| A metric in a caption / `note=` | same — read the value, or a delta of two read values, never a literal |
| A metric in a `review=` / "INTERNAL REVIEW" block | **same.** Not-for-submission is not not-for-accuracy. It ships in the file. |
| A count ("18 features", "4 categories", "16 studies") | `len(...)` of the actual thing, never a digit |
| A comparison the script asserts but does not run ("reduction made it worse: 26.4 → 28.8") | **the script must run the comparison** and write both numbers, or the claim comes out entirely |
| A design boundary ("the 0.95 threshold", "H=3") | a named constant at the top of the file, echoed into the output from that constant |
| Historical narrative ("an earlier draft claimed 13.7pp; that was read off the test split and was wrong") | allowed — it describes a corrected mistake, not a current result. Keep it short and clearly past-tense. |

## The test

For every number a generator emits, ask: **"if the input data changed, would
this number change with it?"**

- Yes, because it's `read_csv(...)["wmape"]` formatted at write time → correct.
- No, because it's a string literal → **wrong**, regardless of which section it
  sits in.

## If a number cannot be computed here

Two honest options, pick one — never a third that leaves a stale literal:

1. **Make it computable.** If table 98 wants a reduced-vs-full WMAPE, the script
   that proposes the reduced set also *fits both and measures*, writes the
   result to a CSV, and the exporter reads it. Cost: a function. Benefit: the
   table is never wrong again.
2. **Remove the number.** State the finding qualitatively — *"the reduced set
   was evaluated and performed worse"* — and let the reader take the direction
   without a decimal. A directional claim survives a data change; a decimal from
   stale data does not.

## How to apply

- **Writing a generator:** every `f"...{...}"` that emits a result interpolates a
  variable traceable to an input read this run. Grep your own diff for a digit
  followed by `pp`, `%`, `x`, or `.` inside a plain string — each one is a
  question to answer.
- **Reviewing a re-run:** open the regenerated file and check that the numbers
  moved. A table whose structure updated but whose headline figure did not is
  F8 again.
- **Auditing an existing generator:** `grep -nE '"[^"]*[0-9]+\.[0-9]+' the_file.py`,
  then classify every hit against the table above.

## Known open work (P0053, 2026-09-10)

Full catalogue in `plans/P0053_2026-09-08_15-40_vps-hpc-model-training/findings.md`
F8 and F10. Not yet all converted: several `review=` blocks in
`04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` cite
finding-specific numbers (3.97pp, 417.3 s, 142x, 2.11%) as literals.

## See Also

- `.claude/rules/figure-generation-standards.md` — the Provenance section this
  generalises
- `.claude/rules/path-handling.md` — sibling rule; the *paths* to inputs go
  through `PATHS.py`, the *values* from those inputs are computed not typed
- `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` — `REVIEW_SEP`
  and the submission/internal split
