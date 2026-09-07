---
pid: P0050
created: 2026-09-07 18:40:00
updated: 2026-09-07 18:40:00
status: in_progress
focus_detail: "Diagrams are DONE: 11 chapter-prefixed SVGs, house style applied and enforced in code. Tier 05 is now CHAPTER-KEYED (01_introduction .. 09_discussion, each with figures/ tables/ models/); the SRQ, appendix and diagrams folders are gone. Folder numbers derive from CHAPTER_SLUGS, so a chapter reorder is a one-tuple edit. All 5 producers run clean; every *_DIR resolves. NEXT: Phase 5 — publish the inventory, THEN choose citations. Blocker unchanged: the horizon never reaches feature construction (P0048 F1 / P0049 F22)."
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

**All eleven now carry a chapter prefix** (2026-09-07). The five that did not
were renamed by what they *show*, not by their old name:

| Ch | Diagram |
|----|---------|
| 1 | `ch1_research_questions_tree_v2` |
| 2 | `ch2_gap_diagram_v2` |
| 4 | `ch4_data_pipeline_v1` · `ch4_eda_pipeline_csd_v1` · `ch4_preprocessing_pipeline_v2` |
| 5 | `ch5_tool_interface_v1` · `ch5_layered_architecture_v2` |
| 6 | `ch6_modelling_pipeline_v1` · `ch6_model_selection_v2` · `ch6_resource_profile_v2` |
| 7 | `ch7_scenarios_v2` |

`_check_stem()` **enforces** the prefix rather than trusting memory: a stem
without `ch<N>_` raises. `fig_resource_profile` saves via matplotlib rather than
`_save()`, so it calls the check explicitly — otherwise that one figure would
escape it.

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

### Phase 4b — chapter-keyed tier 05 — `complete`

- [x] All eleven diagrams chapter-prefixed, enforced by `_check_stem()` (F20)
- [x] **Restructure tier 05 by chapter** (DEC-CHAPTER-FOLDERS, F19). `appendix/`
      is an outdated name over correct content — "appendix" is a *routing
      decision*, and Phase 5 is where that decision gets made, so it must not be
      pre-committed in a path
- [x] ~~Waiting on the Word export~~ — landed 2026-09-07 16:53; chapter names taken from it — headings will carry their
      numbers ("Chapter 2 | Literature Review", "2.8 Design Science Research"),
      and the folder names should come from that, not from a guess
- [x] Two routing conflicts honoured (F19): `export_appendix.py`
      is a cross-cutting exporter, not a scenario script (6 of its 14 tables are
      pipeline/model tables); and the holiday tables split Ch4 source vs Ch6
      ablation
- [x] **Consumers repointed** — incl. 3 broken draft image links found at EOD — F5's lesson; this move touches
      all five producers plus `PATHS.py`

### Phase 5 — inventory → citation decisions — `pending` — **START HERE**

- [ ] Publish the complete regenerable inventory: 11 diagrams, 25 tables,
      4 SRQ1 figures, 149 EDA artefacts, each with its producer
- [ ] Decide per artefact: in-text, appendix, or neither
- [ ] **Then** audit the draft's existing figure references against it
- [ ] **The 18 `analysis/figures*`** (F17) — decide per file on regenerability,
      not on citation. Archived notebooks with hardcoded
      `/Users/enricomanfron/Desktop/…` paths: blockers are edits, not rewrites.
      **RETIRE archives the image too** — a stale image beside a retired producer
      is the trap that started this whole effort
- [ ] **SRQ2's two surviving files** (F16) — `synthesis.csv` +
      `synthesis_summary.md` have no live producer but are cited by Ch7 §7.2.
      Either restore `srq2_synthesis.py` (deterministic, free) to a live location,
      or withdraw those numbers. **Undecided — needs Brian**
- [ ] Confirm nothing in `diagrams/.archive/` has leaked back into use (F15) —
      all three archives are do-not-paste, the RAM one because its numbers are
      fabricated

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
| DEC-CHAPTER-FOLDERS | Tier 05 is keyed by thesis chapter, mirroring the final document, with `figures/ tables/` beneath each. Chapter beats producer where they disagree | 09-07 |
| DEC-CHAPTER-PREFIX | Every diagram filename declares its chapter; `diagrams/` stays flat | 09-07 |
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
5. ~~**P-ID collision**~~ — resolved 2026-09-07. Both `P0046_*` folders are now
   in `.archive/`, so the collision affects no active plan. Noted in
   `PLANS_INDEX.md`; the archived folder names are left as they are.
6. **SRQ2's two files** (F16): `synthesis.csv` and `synthesis_summary.md` are
   cited by Ch7 §7.2 but no live script produces them. Restore
   `srq2_synthesis.py` — deterministic and free to re-run — or withdraw the
   §7.2 numbers. A cited table whose producer is archived cannot be defended if
   an examiner asks how it was computed.

## Errors worth not repeating

| Error | Note |
|-------|------|
| `grep -rn` over the repo times out at 120s | Five sessions running. It walks `.venv` (~40k files). **Use the Grep tool**, or exclude `.venv .git __pycache__` |
| Generated Python through a shell heredoc | `\n` inside the generated string collapsed to a real newline, twice; a repair heuristic then mangled 7 good lines. Recovered with `git checkout --`. **Use the Edit tool for code containing escapes** |
| A move repointed producers but not consumers | Half the appendix vanished into "(skip ...absent)" notices with exit 0. Grep for *readers* of any path that moves |
| `rank="same"` to force figure rows | Fights the layout: produced a column and a staircase. Let graphviz assign ranks |
| Graphviz not on PATH in a fresh shell | `winget` installed `dot.exe` to `C:\Program Files\Graphviz\bin` without adding it. Prepend it before running the diagram generator. Not a code defect |
| A heredoc turned `\b` into a backspace inside a plan file | A Windows path written into a Python string inside a heredoc. Python warned (`SyntaxWarning: invalid escape sequence`) and the control char landed in the `.md`, where Edit could then not match the line. The warning is the tell |
| Plugin hook flags `focus_detail` frontmatter | False positive — the field is required by `workflow-planning-with-files.md`. Do not strip it |
