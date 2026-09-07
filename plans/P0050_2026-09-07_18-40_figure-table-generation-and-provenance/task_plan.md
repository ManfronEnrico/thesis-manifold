---
pid: P0050
created: 2026-09-07 18:40:00
updated: 2026-09-07 18:40:00
status: in_progress
focus_detail: "HANDOFF PLAN for the account switch - read START_HERE.md first. Owns every figure, table and diagram: 11 diagrams + 25 appendix tables from 5 producers, all regenerating in any order, all data-driven, all restyled to the new house standard (horizontal, bold headers, greyscale tiers, transparent, submission-ready captions). Supersedes the figure/table half of P0046. NEXT: Phase 5 - publish the inventory, THEN choose citations. One inherited blocker: the horizon is never applied to feature construction (P0048 F1 / P0049 F22), so the reduction table's horizon column carries a DO-NOT-PUBLISH warning until that fix lands."
---

# P0050 — Figure, table and diagram generation

> **Handoff plan.** Written 2026-09-07 for an account switch that loses session
> history. Read [START_HERE.md](START_HERE.md) first.

## Goal

Every figure, table and diagram is **regenerable from current data by a live
script**, or is a deliberate hand-made artefact whose staleness is a human
judgement. Then: one predictable location, one consistent style, captions an
assessor can read without the repository.

## Method — inventory first, citations second

1. Make the pipelines log properly and consume their own logs. ✅
2. Make every table, figure and diagram data-driven and regenerable. ✅
3. **Then** decide what to cite, in-text or as appendix. ← next
4. **Then** audit the draft's figure references against that inventory.

"Is it already cited?" is not the test. The draft is provisional; the citation
set is an **output** of this work, not an input to it (F2).

---

## Relationship to the other active plans

| Plan | Owns | Boundary with this one |
|------|------|------------------------|
| **P0046** figure-table-provenance | *superseded by this plan* | its figure/table threads moved here; leave it closed |
| **P0047** exogenous enrichment | holiday calendar decision | numbers locked; its tables (94-99) regenerate here |
| **P0048** remaining prose | prose insertion, in-text citations | it consumes this plan's inventory; found the horizon bug |
| **P0049** finalizing experiments | funded runs, SRQ1 determinism | horizon fix lives there; blocks the reduction table's label |

---

## Status quo — verified by running, not by reading

### The five producers

| Producer | Emits | Status |
|----------|-------|--------|
| `generate_architecture_diagrams.py` | 11 diagrams | PASS |
| `generate_literature_table.py` | table 89 | PASS |
| `export_appendix.py` | tables 01-14 | PASS |
| `export_holiday_appendix.py` | tables 90-93 | PASS |
| `srq1_export_enrichment_appendix.py` | tables 94-99 | PASS |

Verified running in **any order** (F6 made ordering matter once; it no longer
does). 195 live scripts compile; `PATHS OK`.

### The diagram set

**System (5):** `pipeline_v2` · `model_selection_v2` · `scenarios_v2` ·
`resource_profile_v2` · `layered_architecture_v2`

**Chapter (6):** `ch1_research_questions_tree_v2` · `ch2_gap_diagram_v2` ·
`ch4_data_pipeline_v1` · `ch4_eda_pipeline_csd_v1` · `ch5_tool_interface_v1` ·
`ch6_modelling_pipeline_v1`

All eleven are horizontal, carry bold box headers, use the greyscale contrast
tiers, render on a transparent ground, and contain **zero** filenames, step
numbers or plan IDs (checked mechanically).

### No hand-drawn figure is current

All three in `diagrams/orphan_conceptual/` are superseded and each contains at
least one claim the code contradicts. **Do not paste them.** Their README says
which generated figure replaces each.

---

## Phases

### Phase 1-3 — trace, layout, paths — `complete`

`PATHS.py` rebuilt for the SRQ tiers (39/39 resolve); `.env.example` root anchor
walked from `__file__`; hardcoded paths audited 43→10 (survivors legitimate);
generators renamed to say what they emit; `requirements.txt` completed.

### Phase 3b — staleness triage + per-SRQ shape — `in_progress`

- [x] Archive-not-delete for every stale artefact, each with a recovery README
- [x] SRQ1 reshaped into `figures/ tables/ models/`, models per category
- [x] EDA promoted to tier 05 (149 files) with a sync function
- [x] LLM-judge artefacts retired (design decided against it)
- [ ] Apply the same `figures/ tables/ models/` shape to SRQ2 and SRQ4

### Phase 3c — pipeline logging — `complete`

- [x] `run_manifest.json` — per category, merged by horizon, never overwritten
- [x] Content metrics extracted from what each step **already returns** (F7)
- [x] Appendix consumes both: an execution table and a data-reduction table
- [x] Clean-slate re-run: 4 categories × 2 horizons = 8 runs, all passing
- [x] Modelling-layer provenance audited — **2 of 21 scripts stamp anything**
      (F8). Recommendation scoped, deliberately not executed

### Phase 4 — chapter figures — `complete`

- [x] All six chapter figures built and data-driven
- [x] Both broken draft image references repaired
- [x] Literature → design map, with its two provenances marked (F9)
- [x] House style written to `.claude/rules/figure-generation-standards.md`
      and applied to all eleven figures (F10-F13)

### Phase 5 — inventory → citation decisions — `pending` — **START HERE**

- [ ] Publish the complete regenerable inventory: 11 diagrams, 25 tables,
      4 SRQ1 figures, 149 EDA artefacts, each with its producer
- [ ] Decide per artefact: in-text, appendix, or neither
- [ ] **Then** audit the draft's existing figure references against it
- [ ] Decide the 18 `analysis/figures*` on regenerability, not on citation —
      they are Enrico's archived notebooks and have **no live producer**

### Phase 6 — manifest + invariant checks — `pending`

- [ ] `05_thesis_results/MANIFEST.md`: artefact → producer → source → status
- [ ] Check: every tier-05 artefact has a live producer
- [ ] Check: `PATHS.py` self-test asserting every `*_DIR` exists
- [ ] Check: no two files in a generated directory share an identity prefix (F6)
- [ ] Check: a producer reports "N written, M skipped" so a structural break is
      loud rather than a run of polite notices (F5)

### Phase 7 — style pass — `pending`

- [ ] Shared matplotlib style matching the graphviz palette
- [ ] Export format policy (PNG for Word, SVG retained)

---

## Decisions

| ID | Decision | Date |
|----|----------|------|
| DEC-INVENTORY-FIRST | Build the regenerable inventory, then choose citations. Never the reverse | 09-06 |
| DEC-SINGLE-HOME | Artefacts live once, in `05_thesis_results/`; the writing tier holds none | 09-06 |
| DEC-SHIP-SCOPE | Tiers 01-05 ship to assessors; 00 and 06 are the writing harness | 09-06 |
| DEC-EDA-SPLIT | `.csv` stays at the pipeline; `.md` and `.png` promote to tier 05 | 09-06 |
| DEC-PATHS | Every output path resolves through `PATHS.py` | 09-06 |
| DEC-ANCHOR | Root anchor is `.env.example`, walked from `__file__` — never `CLAUDE.md` | 09-06 |
| DEC-ARCHIVE-NOT-DELETE | Stale artefacts move to a level-appropriate `.archive/` with a README | 09-06 |
| DEC-DIAGRAMS-FROM-CODE | Diagrams read artefacts at render time and refuse to draw from absent data | 09-06 |
| DEC-RAM-4GB | 4096 MB is the envelope. Thesis prose still says "8 GB" in 8 places | 09-06 |
| DEC-GENERATE-ALL | Generate every figure programmatically; hand redrawing afterwards is Brian's option, not a reason to leave one ungenerated | 09-07 |
| DEC-FIGURE-STYLE | Horizontal, bold headers, no step numbers, greyscale tiers, transparent, submission-ready captions — `.claude/rules/figure-generation-standards.md` | 09-07 |

---

## Open for Brian

1. **The five new chapter figures are ready to look at.** If any should be
   redrawn by hand, the generated one is the reference for the facts.
2. **"8 GB" → 4 GB** in Ch6 prose (8 occurrences) and Ch2 (note N11).
3. **The abstract claims Indeks Danmark** as an empirical source; it was never
   used. 2 occurrences, abstract only — Ch3/Ch4 are clean. Note at
   `06_thesis_writing/writing-notes/indeks-danmark-claim-must-be-corrected.md`.
4. **Ch8 §8.3 / Table 21** comes out with the retired LLM judge.
5. **P-ID collision**: `P0046_..._exogenous-enrichment-decision/` declares
   `pid: P0047` in its frontmatter but sits in a `P0046_` folder. Rename the
   folder when convenient.

## Errors worth not repeating

| Error | Note |
|-------|------|
| `grep -rn` over the repo times out at 120s | Five sessions running. It walks `.venv` (~40k files). **Use the Grep tool**, or exclude `.venv .git __pycache__` |
| Generated Python through a shell heredoc | `\n` inside the generated string collapsed to a real newline, twice; a repair heuristic then mangled 7 good lines. Recovered with `git checkout --`. **Use the Edit tool for code containing escapes** |
| A move repointed producers but not consumers | Half the appendix vanished into "(skip ...absent)" notices with exit 0. Grep for *readers* of any path that moves |
| `rank="same"` to force figure rows | Fights the layout: produced a column and a staircase. Let graphviz assign ranks |
| Plugin hook flags `focus_detail` frontmatter | False positive — the field is required by `workflow-planning-with-files.md`. Do not strip it |
