---
pid: P0050
created: 2026-09-07 18:40:00
updated: 2026-09-10 19:30:00
status: in_progress
focus_detail: "PHASE 8 COMPLETE (2026-09-10). Tier 05 now carries only reader-facing content and the invariant is ENFORCED, not remembered: 05_thesis_results/check_reader_facing.py exits 1 on any hit, and every appendix producer calls warn_after_run() at the end of its own run. Nine leaks across eight files were fixed at the producer (two more than the eight first measured - RESULTS_2026-08-19.md and pooled_perbrand_summary.md were missed). The 24 editorial notes moved from the flat generated-table-review-notes/ into per-chapter folders; review_notes.py derives the chapter from the artefact's own output path, so a table and its note cannot diverge. Two new chapter folders created (ch2_literature_review, ch3_methodology) per Brian's instruction to create what is missing and orient on chapter names. All 7 producers re-run clean. Blocker unchanged: horizon never reaches feature construction (P0048 F1 / P0049 F22). NEXT ACTION IS PHASE 5 (inventory before citations, F2) -- Phase 8 sits above it in the file only because it was added last. Phases 3b, 5, 6 and 7 remain open. NOTHING IS COMMITTED."
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

### The nine producers

| Producer | Emits | Status |
|----------|-------|--------|
| `generate_architecture_diagrams.py` | 12 diagrams | PASS |
| `generate_methodology_diagram.py` | ch3 methodology figure (F31) | PASS |
| `generate_literature_table.py` | table 89 | PASS |
| `export_appendix.py` | tables 01-15 | PASS |
| `export_holiday_appendix.py` | tables 90-93 | PASS |
| `srq1_export_enrichment_appendix.py` | tables 94-99 | PASS |
| `training_report.py` | `training_report.md` | PASS |
| `srq1_generate_performance_figures.py` | 2 benchmark figures | PASS |
| `srq1_generate_shap_figures.py` | SHAP importance figure | PASS |

The last three were found during the 2026-09-10 audit: they write into tier 05
but import none of the chapter helpers, so the original grep for
`get_chapter_*_dir` missed them. **A producer is anything that writes into tier
05, not anything that imports PATHS in a particular way.**

Verified running in **any order** (F6 made ordering matter once; it no longer
does). 195 live scripts compile; `PATHS OK`.

### The diagram set

**All twelve now carry a chapter prefix** (2026-09-07; methodology added 09-10). The five that did not
were renamed by what they *show*, not by their old name:

| Ch | Diagram |
|----|---------|
| 1 | `ch1_research_questions_tree_v2` |
| 2 | `ch2_gap_diagram_v2` |
| 3 | `ch3_methodology_design_v1` **(new 09-10, F31)** |
| 4 | `ch4_data_pipeline_v1` · `ch4_eda_pipeline_csd_v1` · `ch4_preprocessing_pipeline_v2` · `ch4_raw_schema_v1` |
| 5 | `ch5_modelling_pipeline_v1` · `ch5_model_selection_v2` · `ch5_resource_profile_v2` |
| 6 | `ch6_tool_interface_v1` · `ch6_layered_architecture_v2` |
| 7 | `ch7_scenarios_v2` |

**Ch5 and Ch6 are swapped relative to how this table read before 2026-09-08** —
modelling now sits directly after data assessment. The stems moved with the
chapters, which is why the numbers here differ from earlier sessions' notes.

`_check_stem()` **enforces** the prefix rather than trusting memory: a stem
without `ch<N>_` raises. `fig_resource_profile` saves via matplotlib rather than
`_save()`, so it calls the check explicitly — otherwise that one figure would
escape it.

All twelve are horizontal, carry bold box headers, use the greyscale contrast
tiers, render on a **white** ground (DEC-WHITE-GROUND), and contain **zero**
filenames, step numbers or plan IDs (checked mechanically).

**That clean bill covers the FIGURES only.** The 2026-09-10 audit found plan IDs
and internal decision codes still reaching six tier-05 **table and report** files
in prose an assessor reads (F32). Phase 8b closes that; do not read the line
above as covering the whole tier.

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

### Phase 3d — provenance audit after the HPC re-run — `complete` (09-10)

Triggered by Brian after a cluster re-run added the holiday enrichment: *is
everything in tier 05 computed, with no hardcoded literals?* It was not.

- [x] Audit all nine producers for typed values. **Three stale literals** found
      and made dynamic (F26); two correctly-literal constants confirmed
- [x] Three figures regenerated — they showed a **superseded model selection**
      even though the generator was right (F26)
- [x] Three orphan SVGs from the Ch5/Ch6 swap deleted; no producer emits them
      and the stale-twin sweep cannot see same-folder twins (F26)
- [x] `cv_summary.md` confirmed **current**, not stale; regenerated from stored
      CSVs without re-running the benchmark (F27)
- [x] **63 PNGs → SVG** across three producers plus the promotion step (F28)
- [x] **24 internal-note blocks** moved out of tier 05 into per-table sidecars
      under `writing-notes/` (F28)
- [x] `review_notes.py` moved out of `utility_scripts/` — a tree the submission
      export deletes — into `05_thesis_results/`, which ships (F28)
- [x] Model selection verified dynamic and correct by independent recomputation
      (F29); category casing normalised at the display edge
- [x] Backgrounds switched to white at all five call sites (F30)
- [x] New `generate_methodology_diagram.py`, parsing the ch3 prose (F31)

**Carry into the prose (Phase 5 / P0048):** energidrikke and RTD are selected by
only 0.7 and 0.4 cross-validated points. Worth a sentence; presenting the
category split as settled would overstate it.

### Phase 8 — tier 05 is reader-facing only; notes live per chapter — `complete`

Brian, 2026-09-10, correcting a misread of the previous instruction. The point is
about **content**, not about import graphs:

> "I only want any output in `05_thesis_results/` to be submission ready, meaning
> only descriptions that are meant to be read by the reader of the thesis / the
> assessors."

**Nothing student-facing may appear anywhere in tiers 01-05**, whether or not the
file ships and whether or not it is marked. The earlier fix moved the
`INTERNAL REVIEW` blocks but stopped at the marker; it did not look for internal
content that was never marked in the first place.

**The producer scripts may live wherever is convenient** (Brian: "they can also
live in the same folder at root. I don't mind honestly"). The only requirement on
them is that they consume real sources and regenerate when the pipeline output
changes. So `DEC-SHIPPED-IMPORTS` and the `review_notes.py` relocation were
solving a problem that was not asked about — harmless, and now beside the point.

#### 8a — Move the notes into their chapter folders — `complete`

- [x] Route each note by the chapter that owns its artefact. **Better than
      planned**: rather than passing `_TABLE_CHAPTER` in, `review_notes.py`
      derives the chapter from the artefact's own output path (`chapter_of`),
      which already encodes it as `05_thesis_results/{NN}_{slug}/`. A producer
      therefore *cannot* file a table in one chapter and its note in another,
      and a re-routed table takes its note with it for free
- [x] Folder name derived from `CHAPTER_ORDER`, never typed —
      `get_chapter_notes_dir()` / `get_chapter_generated_notes_dir()` in `PATHS.py`
- [x] Existing folders reconciled. **My report of a space in `ch5_model benchmark`
      was wrong** — it is `ch5_model_benchmark`, an underscore, and always was.
      All five existing folders matched the derived name exactly, so **nothing was
      renamed**. Brian's call: create what is missing, orient on chapter names.
      Two folders created: `ch2_literature_review`, `ch3_methodology`
- [x] `generated-table-review-notes/` deleted, after verifying all 24 notes had a
      per-chapter twin (`comm` over the two listings, zero orphans)

Notes land in a `generated/` subfolder, so a regenerated note can never overwrite
something a human wrote. Two abbreviations Brian and Enrico already navigate
(`ch7_synthesis`, `ch8_experiment`) are kept via `_CHAPTER_NOTES_FOLDER` rather
than renamed to the full slug.

Final distribution: ch2 1, ch3 1, ch4 7, ch5 11, ch7 1, ch8 3 = 24.

#### 8b — Sweep tiers 01-05 for UNMARKED student-facing content — `complete`

**The measured count was wrong, and low.** Nine lines across **eight** files, not
eight across six. The two missed by the first sweep:

| File | Leak | Why it was missed |
|---|---|---|
| `08_experimental_evaluation/RESULTS_2026-08-19.md` | `F17 sizes this` | a bare `F17`, no plan ID beside it |
| `05_model_benchmark/tables/pooled_perbrand_summary.md` | `Tests the F50 explanation` | same shape |

Both are the *hardest* class: a finding number used as an ordinary noun, in a
sentence that reads as prose. This is F32's lesson recurring inside the fix for
F32 — which is the argument for 8c.

- [x] Fixed at the producer: `training_report.py` (3), `srq1_baselines_stat.py`,
      `srq1_ridge_pooled.py` (2 lines, one sentence), `srq1_pooled_perbrand.py`,
      `srq4_experiment.py`, `export_appendix.py`
- [x] Reasoning kept, citation dropped. `training_report.py`'s
      `(DEC-DISCOVER-COLUMNS)` became "by intersecting what every category
      actually provides"; the metric argument kept its whole sentence and lost
      only `(P0038 F75)`
- [x] Two files are **hand-written, not generated** — `models/README.md` and
      `RESULTS_2026-08-19.md`. Fixed in place, since there is no producer to fix.
      `models/README.md` also cited the pre-rename `04_thesis_results/srq1/` path,
      corrected in the same pass
- [x] `APPENDIX_TABLES.md`'s whole header block addressed the authors, not an
      assessor ("Do not edit these files by hand", "for our own review", "the
      folder you open is the chapter you are writing"). Rewritten reader-facing
- [x] Re-run and re-scanned to zero

**Four outputs could not be regenerated** — `srq1_baselines_stat`,
`srq1_ridge_pooled` and `srq1_pooled_perbrand` refit models, which is hours. The
identical substitution was applied to their `.md` outputs instead, verified
character-for-character against what the fixed producer now emits, so the next
real run is a no-op rather than a revert.

#### 8c — Make the invariant checkable, not remembered — `complete`

- [x] `05_thesis_results/check_reader_facing.py` — exit 1 on any hit, naming the
      file, line and *which* class it matched. Patterns: plan ID, `DEC-` code,
      finding number, submission marker, "for our own review", author name, and
      a path into `06_thesis_writing/`
- [x] **Both**, not either. It runs standalone, and every appendix producer calls
      `warn_after_run()` at the end of its own run — so the check reports without
      anyone deciding to run it. The producer path *warns* rather than raising: a
      generator that has just written 15 correct tables should not exit non-zero
      over a sentence, and the run that finds a leak is rarely the run that
      introduced it
- [x] Verified by planting one line of each class and confirming all five were
      caught with exit 1, then confirming a producer surfaced a planted leak
      mid-run. **A check that has never failed proves nothing**
- [x] `figure-generation-standards.md` rewritten: a new "Tiers 01-05 carry no
      internal content at all" section, the marker-versus-content lesson, the
      keep-the-reasoning rule, and the Quick Reference row changed from
      "Internal notes: separated" to "Internal content: none in tiers 01-05"

Deliberately **not** scanned: `.py` files (source comments are a different
audience — P0054's pass) and `.archive/` folders, whose READMEs exist precisely
to record which plan retired an artefact.

#### 8d — Reconsider what the earlier session decided — `complete`

- [x] `DEC-SHIPPED-IMPORTS` — **dropped as a decision, kept as a note.** It
      states something true about the import graph, but it was recorded as though
      it answered Brian's question and it did not. Leaving it in the decisions
      table implies the requirement was about which tree ships, which is exactly
      the misread F32 exists to correct
- [x] `review_notes.py` stays in `05_thesis_results/` — now on ordinary grounds.
      It is a helper beside the generators that call it, and
      `check_reader_facing.py` joined it there, imported by the same five
      producers. Two related helpers beside their callers is the plain reading;
      the ship-scope argument is no longer doing any work

> **Reading order note.** Phase 8 was added last and sits above Phases 5-7
> because it was urgent, not because those are done. **The next action is Phase 5**,
> and the standing rule still governs it: publish the regenerable inventory
> FIRST, choose citations SECOND (F2). Phase 3b and Phase 7 are also open.

### Phase 5 — inventory → citation decisions — `pending`

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

### Phase 6 — manifest + invariant checks — `pending` (one delivered early)

**The first invariant check already exists.** Phase 8 built
`05_thesis_results/check_reader_facing.py` and wired `warn_after_run()` into
every appendix producer, which is the pattern the rest of this phase should
follow: a script that fails, called at the end of the run that could break it,
rather than a rule someone remembers. Reuse its shape -- named patterns, a hit
that says which class it matched, and a probe test proving it can fail.

- [x] Check: no internal content in any tier-05 artefact (`check_reader_facing.py`)
- [ ] `05_thesis_results/MANIFEST.md`: artefact → producer → source → status
- [ ] Check: every tier-05 artefact has a live producer
- [ ] Check: `PATHS.py` self-test asserting every `*_DIR` exists
- [ ] Check: no two files in a generated directory share an identity prefix (F6)
- [ ] Check: a producer reports "N written, M skipped" so a structural break is
      loud rather than a run of polite notices (F5)

### Phase 7 — style pass — `partly complete`

- [x] Export format policy settled: **SVG only**, no PNG twin (DEC-SVG-ONLY, F28)
- [x] Background policy settled: **white**, never transparent (DEC-WHITE-GROUND, F30)
- [ ] Shared matplotlib style matching the graphviz palette — the four
      matplotlib producers still carry library defaults for colour and font;
      only ground and format are unified so far

---

## Decisions

| ID | Decision | Date |
|----|----------|------|
| DEC-INVENTORY-FIRST | Build the regenerable inventory, then choose citations. Never the reverse | 09-06 |
| DEC-SINGLE-HOME | Artefacts live once, in `05_thesis_results/`; the writing tier holds none | 09-06 |
| DEC-SHIP-SCOPE | Tiers 01-05 ship to assessors; 00 and 06 are the writing harness | 09-06 |
| DEC-EDA-SPLIT | `.csv` stays at the pipeline; `.md` and `.svg` promote to tier 05 (was `.png` until DEC-SVG-ONLY) | 09-06 |
| DEC-PATHS | Every output path resolves through `PATHS.py` | 09-06 |
| DEC-ANCHOR | Root anchor is `.env.example`, walked from `__file__` — never `CLAUDE.md` | 09-06 |
| DEC-ARCHIVE-NOT-DELETE | Stale artefacts move to a level-appropriate `.archive/` with a README | 09-06 |
| DEC-DIAGRAMS-FROM-CODE | Diagrams read artefacts at render time and refuse to draw from absent data | 09-06 |
| DEC-RAM-4GB | 4096 MB is the envelope. Thesis prose still says "8 GB" in 8 places | 09-06 |
| DEC-GENERATE-ALL | Generate every figure programmatically; hand redrawing afterwards is Brian's option, not a reason to leave one ungenerated | 09-07 |
| DEC-CHAPTER-FOLDERS | Tier 05 is keyed by thesis chapter, mirroring the final document, with `figures/ tables/` beneath each. Chapter beats producer where they disagree | 09-07 |
| DEC-CHAPTER-PREFIX | Every diagram filename declares its chapter; `diagrams/` stays flat | 09-07 |
| DEC-FIGURE-STYLE | Horizontal, bold headers, no step numbers, greyscale tiers, **white ground**, submission-ready captions — `.claude/rules/figure-generation-standards.md` | 09-07 |
| DEC-WHITE-GROUND | Figures paint a white background, never transparent: the greyscale palette assumes a light ground and inverts on a dark one (F30). Supersedes the transparent half of DEC-FIGURE-STYLE | 09-10 |
| DEC-SVG-ONLY | Every generated image is SVG. No PNG twin, anywhere, including the EDA plots (F28) | 09-10 |
| DEC-READER-FACING-ONLY | **Tier 05 output contains only what a thesis reader should see** — no plan IDs, no internal decision codes, no notes to ourselves, marked or unmarked. This is the actual requirement; the note relocation is one consequence of it, not the whole of it (F32) | 09-10 |
| DEC-NOTES-BY-CHAPTER | Editorial notes live in `06_thesis_writing/writing-notes/` in the **chapter folder** they serve, routed by the same slug that routes the table. Grouping by chapter serves the person writing; grouping by producer serves the producer (F33) | 09-10 |
| ~~DEC-NOTES-OUT-OF-TIER-05~~ | ~~one flat sidecar directory, one file per table~~ — superseded by DEC-NOTES-BY-CHAPTER: the destination was the wrong shape (F33) | 09-10 |
| DEC-SHIPPED-IMPORTS | *Under review (Phase 8d).* A true property, but recorded as though it answered the question about student-facing content, which it did not. Producer location is explicitly free (F32) | 09-10 |

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
