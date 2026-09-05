---
pid: P0046
created: 2026-09-05 20:40:00
updated: 2026-09-05 21:05:00
---

# P0046 — Progress Log

## Session 1 — 2026-09-05 20:40

**Branch:** `thesis/draft-bullet-reconstruction` (inherited from the P0045
session; this plan did not create a branch of its own. Worth splitting if
Phase 3+ execution starts, since P0045's working tree is already dirty.)

**Goal for session:** trace and classify every figure/table Brian listed; do not
move or delete anything yet.

### Done

- Created plan folder `P0046_2026-09-05_20-40_figure-table-provenance-centralisation`.
- Phase 1 complete. Findings F1–F10 written.
- Classified the listed artefacts. Headline counts:
  - **LIVE / healthy:** the four-category EDA layer (~240 files) and the
    12-table appendix. Both fully regenerable, both current.
  - **REGENERABLE-STALE:** `fig1_model_ladder`, `fig3_forecast_overlay` (both
    2026-07-11, while their sibling tables are 2026-08-24), plus
    `system_architecture_v1`, `data_flow_v1`, `ram_budget_v1`.
  - **ZOMBIE:** `fig2_granularity.png` — producing code deliberately removed by
    P0035; depicts a comparison the project decided to stop making.
  - **ORPHAN-CONCEPTUAL:** `ch2_gap_diagram`, `ch5_architecture_v1`.
  - **ORPHAN-DERIVED (cannot ship):** `05_thesis_writing/analysis/figures/` (11)
    and `analysis/figures_agentic/` (7) — traced to Enrico's archived notebooks.
  - **ORPHAN + stale content:** `ch1_research_questions_tree`.

### Key realisations

1. Brian's guess that some artefacts are "AI-generated with no source" was
   close but not quite right for the `analysis/` sets — they *had* a real
   producer (Enrico's notebooks), it was just archived and machine-pinned. The
   practical consequence is the same (unrunnable), but the framing matters for
   how they get cited or retired.
2. Three of the four "needs information update" figures are regenerable, meaning
   their fix is editing graphviz node labels, not redrawing. Much cheaper than
   the triage folders implied.
3. The most dangerous artefact found (`fig2_granularity.png`) was in the *right*
   folder with the *right* name. This is the argument for a provenance manifest
   over a tidier folder tree — see findings F10.
4. `ram_budget_v1` must NOT be fixed by simply re-running `generate_figures.py`:
   the script still contains the fabricated numbers P0040 F5 flagged. Real
   measurements now exist in the appendix and it needs rewiring to them.

### Not done / deliberately deferred

- No files moved, deleted or regenerated. Phase 2 is blocked on Brian's answers
  to the four open questions in findings.md.
- In-text thesis tables not yet diffed against generated artefacts (Phase 5).
- Danskvand and RTD have 7 EDA plots vs CSD/Energidrikke's 8 — noted, not yet
  explained.

### Errors

| Error | Attempt | Resolution |
|-------|---------|------------|
| `grep -rIl` over the repo root exceeded the 120s Bash timeout | 1 | Z: is a slow network drive for full-tree walks. Switched to the Grep tool (ripgrep-backed, honours ignore files) — returned in ~2s. Recorded for `/errors-log`. |

### Session 1b — Brian's decisions (same evening)

Brian reviewed the findings and settled three of the four open questions. Written
up as F11, F12, F13; Phase 2 closed; Phases 3-7 rewritten to match.

**What changed in the plan as a result:**

1. **F11 — the appendix folder is not exempt.** I had held up
   `04_thesis_results/appendix/` as the model to copy (F7) without noticing that
   under Brian's own contract it is a *production* site, not a publication one.
   Its name made it look like a destination. Brian caught this: "the scripts
   writing the current appendix folder should also follow the same logic." The
   sharpened invariant is that **no generator writes into tier 05** — only the
   curation script does. That single-writer rule is what makes the manifest
   trustworthy, so it is worth more than the folder layout it implies.

2. **F12 — the ORPHAN-DERIVED verdict was too blunt.** I wrote that those 18
   files "cannot ship", which is true of the files but slid into implying the
   notebooks were unusable. Brian pushed back correctly: they are archived, not
   broken, and the blockers (a macOS `FIGURE_DIR`, a pre-four-category scope) are
   edits. So the class now has two exits, RESTORE and RETIRE, decided per file —
   with the pairing rule that RETIRE archives the image too, since a stale image
   left in a live folder is precisely the `fig2_granularity` trap.

3. **F13 — PATHS centralisation accepted**, and reading the file end to end
   turned up an extra defect: the tier-map docstring at `PATHS.py:28` still lists
   `sections-final/`, archived 2026-09-01. The file that exists to be the
   authority on repo layout is advertising a directory that no longer exists.

**Phase ordering consequence:** Phase 5 grew a citation sweep and now feeds
Phase 2's leftover — the restore-or-retire table cannot be filled in without
knowing what the chapters cite. A new Phase 6 holds the curation script and
manifest; the style pass moved to Phase 7.

### Next session starts here

**Phase 3 — `PATHS.py` constants.** Chosen as the entry point because it is the
only phase that is purely additive: no artefact is moved, deleted or regenerated,
so nothing is at risk if the approach needs adjusting. Everything destructive
(Phase 4) waits until the constants exist.

Order within Phase 3:
1. Add the eight constants/helpers (findings F13 table).
2. Fix the stale `sections-final/` docstring line.
3. Repoint the two generators that hard-code `"05_thesis_writing/figures"` —
   this is the change that stops tier 05 being written by anything but curation.
4. Delete the byte-identical shadow copy under `utility_scripts/scripts/`.

Still open for Brian (findings "Open questions"): `ch1_research_questions_tree`
redraw-vs-generate, zombie delete-vs-archive, and whether
`04_thesis_results/diagrams/` is the right production home for the two diagram
generators.
