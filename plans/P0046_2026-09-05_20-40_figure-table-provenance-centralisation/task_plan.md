---
pid: P0046
created: 2026-09-05 20:40:00
updated: 2026-09-06 16:00:00
status: in_progress
focus_detail: "Repo restructured to SRQ-aligned tiers 2026-09-06, which broke 32 of 34 PATHS constants. PATHS.py rewritten and verified (3 remaining misses are pre-existing SPSS placeholders); results folders slugged; SRQ4 runs moved beside the harness. Next: Phase 3 remainder (repoint the two diagram generators, add RQ tree figure), then Phase 3b staleness triage of srq1/srq2."
---

# P0046 — Figure, Table & Graph Provenance and Centralisation

## Goal

Every figure, table and graph that could enter the thesis must be one of two
things, with nothing in between:

1. **Regenerable** — a script under version control produces it, and re-running
   that script reproduces it from current data.
2. **Deliberately hand-made** — a conceptual diagram with no data behind it,
   whose source-of-truth is recorded and whose staleness is a human judgement.

Anything that is neither is an artefact nobody can defend to an examiner. The
job of this plan is to find those, label them, and then make the surviving set
land in one predictable place with one consistent style.

## Why now

The thesis has a complete draft. Chapters cite figures by relative path into
`05_thesis_writing/figures/`, and several of those paths no longer resolve
because a previous session sorted the files into triage subfolders
(`unsure/`, `update_formatting/`, `update_information/`) without updating the
references. Separately, the drafts carry in-text tables whose numbers have never
been checked against the generated artefacts on disk.

## Scope

**In scope**
- Tracing every figure/table path Brian listed to its producing script (or
  proving none exists).
- Classifying each into the taxonomy below.
- Proposing (and, once approved, executing) a centralised layout.
- Making the generators write to that layout via `PATHS.py` constants rather
  than hard-coded relative strings.
- Validating in-text thesis tables against the generated artefacts.

**Out of scope**
- Rewriting thesis prose. Prose lives in the OneDrive `.docx`
  (see `.claude/rules/writing-surface-authority.md`); this plan touches
  artefacts and the code that emits them, not sentences.
- Re-running any paid experiment. Regeneration here is free/local only.
- Re-designing the conceptual diagrams' *content* — that is a separate
  judgement call per figure, tracked but not executed here.

## Classification taxonomy

Every artefact gets exactly one label:

| Label | Meaning | Action |
|-------|---------|--------|
| **LIVE** | Script exists, output current | Keep; point generator at central dir |
| **REGENERABLE-STALE** | Script exists, output predates a scope change | Re-run, then keep |
| **ZOMBIE** | Output on disk, producing code deleted | Delete the file |
| **ORPHAN-CONCEPTUAL** | No producer, but a legitimate hand-drawn diagram | Adopt: record source, decide keep/redraw |
| **ORPHAN-DERIVED** | No *live* producer, but depicts *data* | Per-file RESTORE or RETIRE (see below) |
| **SUPERSEDED** | A newer artefact covers the same ground | Archive |

The critical distinction is ORPHAN-CONCEPTUAL vs ORPHAN-DERIVED. A hand-drawn
architecture diagram with no script is fine — diagrams of ideas have no dataset.
A *chart of numbers* with no script is not fine, regardless of how good it looks,
because nobody can say which data produced it.

ORPHAN-DERIVED describes **the file on disk, not its producer's fate** (F12). An
archived producer may be adaptable, so each such file gets one of two exits:

- **RESTORE** — port the archived producer to a live script under `PATHS.py` and
  re-run it against current data. Right when the figure shows something no live
  script covers and a chapter wants it.
- **RETIRE** — leave the producer archived and archive the stale image *beside
  it*. Both halves move together: an image left in a live folder next to a
  retired producer is the `fig2_granularity` failure mode (F4).

## Phases

### Phase 1 — Trace and classify — `complete`

Establish, for each of the ~70 listed artefacts, whether a producer exists.

- [x] Enumerate all live `savefig` / `to_markdown` producers
- [x] Map `generate_figures.py` emitted names to disk
- [x] Trace `analysis/figures/` and `analysis/figures_agentic/`
- [x] Trace the three triage subfolders under `05_thesis_writing/figures/`
- [x] Check EDA pipeline output coverage across all four categories
- [x] Timestamp-check `04_thesis_results/srq1/` for staleness
- [x] Detect duplicate/shadow generator copies

Result: findings.md F1–F9.

### Phase 2 — Decide the target layout — `complete`

Decided by Brian 2026-09-05. See findings F11-F13.

- [x] Centralisation target confirmed: **produce where it lives, promote what
      ships**. `05_thesis_writing/{figures,tables}/` holds only the selected set,
      written by a curation script that is the *only* writer into tier 05.
- [x] EDA plots/tables **stay** where the pipeline writes them; they get promoted,
      not moved.
- [x] `04_thesis_results/appendix/` is subject to the same rule — it is a
      production site despite its name (Brian's catch, F11).
- [x] ORPHAN-DERIVED reframed: **per-file restore-or-retire**, not a bulk verdict
      (F12). The table itself is deferred to Phase 5, which supplies the citation
      data needed to decide.
- [x] All output paths centralise in `PATHS.py` (F13).
- [ ] ZOMBIE disposition — still open (delete vs archive), see open question 2.

### Phase 3 — Centralise paths in `PATHS.py` — `complete`

Overtaken by events: the 2026-09-06 SRQ restructure (F19) broke 32 of 34
directory constants, turning this phase from planned tidying into urgent repair.
Done in that pass:

- [x] Repoint every tier constant onto the new SRQ-aligned layout (F19)
- [x] Rewrite the tier-map docstring — now documents the SRQ tiers, the
      DEC-P0046-SHIP-SCOPE boundary and the DEC-P0046-SINGLE-HOME artefact rule
      (this also retired the stale `sections-final/` line flagged in F13)
- [x] Remove `THESIS_MODELLING_SERVING_*` and `THESIS_DATA_ASSESSMENT_DIR`
      rather than repoint them — no live directory exists (F19)
- [x] Add `THESIS_RESULTS_{APPENDIX,DIAGRAMS,EDA}_DIR`, the slugged
      `THESIS_RESULTS_SRQ{1,2,3,4}_DIR`, `SRQ{1,2,3,4}_DIR`,
      `SRQ4_SCENARIO_SETUP_DIR`, `SRQ4_RUNS_DIR`,
      `THESIS_WRITING_{CITATIONS,DRAFTS,SNAPSHOTS}_DIR`,
      `THESIS_CONTEXT_{RESEARCH_QUESTIONS,METHODOLOGY,REQUIREMENTS}_DIR`
- [x] Add `get_srq_results_dir(n)`, `get_category_eda_plots_dir(cat)`,
      `get_category_eda_tables_dir(cat)`, `get_category_eda_results_dir(cat)`
- [x] Verify: 43 constants, 3 misses, all pre-existing SPSS placeholders
- [x] Slug the results folders + create `diagrams/`, `eda/`,
      `srq3_integration_readiness/` (F20)
- [x] Move SRQ4 `run_*` + `raw_responses` to `04_SRQ4_Scenario_Experiment/runs/` (F20)

**Phase 3 COMPLETE 2026-09-06.** Remaining items all done:

- [x] Repoint `generate_figures.py` -> `THESIS_RESULTS_DIAGRAMS_DIR`
- [x] Relocate + repoint `generate_systemB_diagram.py` out of tier 06 into
      `05_thesis_results/`, with a staleness warning (F26)
- [x] Archive the byte-identical shadow copy (F8)
- [x] Repoint `zotero_client.py` and `thesis_snapshot.py` (F24) — the latter
      generates the snapshot mirror the comment-audit workflow reads
- [x] Swap the `CLAUDE.md` root anchor to `.env.example` across 7 scripts +
      the shared finder; fix `.gitignore` so the anchor is actually committed;
      re-anchor from `__file__` instead of `cwd` (F25)
- [x] Replace `parents[N]` repo-root hops in 17 scripts (F25)
- [x] Archive the dead `ml_retraining/` pipeline (F25)
- [x] Verify: 77 live scripts compile, 39/39 PATHS constants resolve, audit
      down from 43 flagged scripts to 10 (all legitimate — see F25 table)

Deferred to Phase 4 (needs a generator run, not a path edit):

- [ ] Add `ch1_research_questions_tree` to `generate_figures.py` (F18)
- [ ] Point `srq1_figures.py` / `srq1_shap.py` at the slugged SRQ1 constant —
      they resolve via `THESIS_RESULTS_SRQ1_DIR`, so this is a re-run, not a fix
- [ ] Repoint the EDA writers to also emit `.md`/`.png` into
      `get_category_eda_results_dir(cat)` (F21)

### Phase 3b — Staleness triage + per-SRQ shape — `pending`

The substantive half of the plan. Two jobs:

**0. Decide `generate_systemB_diagram.py`** (F26) — it diagrams the abandoned
multi-agent writing system and no chapter cites it. Recommendation: delete.

**1. Staleness triage.** Brian's assessment: `appendix/` and
`srq4_scenario_experiments/` are current; `srq1_model_performance/` and
`srq2_structured_tool_interface/` are stale to unknown degrees — srq2 still
carries LLM-as-Judge outputs from a design that was dropped, which also suggests
it was generated by Enrico rather than by the current pipeline.

- [ ] Per-file: current / stale-but-regenerable / drop, for srq1 and srq2
- [ ] Confirm which producer emits each file (feeds the F19 self-check)
- [ ] Drop artefacts of dropped designs (LLM-as-Judge) rather than regenerating

**2. Per-SRQ shape** — `figures/`, `tables/`, `models/`. No `raw/`: per
DEC-P0046-RUNS-WITH-EXPERIMENT raw material never reaches this tier (F20).

- [ ] Reorganise `srq1_model_performance/`'s 36 top-level files into it
- [ ] Delete `05_thesis_results/phase3_region_grain_test/phase3_result.json` —
      P0035 archived the producing script but left the output (F16)
- [ ] Remove `05_thesis_results/__pycache__/`, confirm gitignored

### Phase 4 — Regenerate and reconcile — `pending`

- [ ] Re-run the free generators: `srq1_figures.py`, `srq1_shap.py`,
      `training_report.py`, `export_appendix.py`
- [ ] **Hold `generate_figures.py`** until `ram_budget_v1` is rewired to the real
      measurements in `04_thesis_results/appendix/02_substrate_resource_profile`
      and `04_sandbox_resource_profile` — re-running it as-is regenerates P0040
      F5's fabricated numbers (F5)
- [ ] Update the six graphviz label sets in `generate_figures.py` so
      `system_architecture_v1` / `data_flow_v1` carry current information
- [ ] Delete `fig2_granularity.png` outright — recoverable from git `4c7a98b`,
      cited by no chapter (F17). No archive copy.
- [ ] Fix the broken `![...](../figures/...)` references in the drafts —
      they now point into tier 04, not a tier-05 figures folder (F14)

### Phase 5 — Citation sweep + validate in-text tables — `pending`

Two jobs, and the first unblocks a Phase 2 leftover.

- [ ] **Citation sweep**: which figures/tables do the chapters actually cite?
      This is the input F12 needs — it decides restore-vs-retire for each of the
      18 ORPHAN-DERIVED files, and it decides what the curation script promotes.
- [ ] Fill in the 18-row restore-or-retire table (F12)
- [ ] Diff each in-text thesis table against its generated counterpart
- [ ] Record every mismatch (do not silently "fix" the thesis — a mismatch may
      mean the artefact is wrong, not the prose)

### Phase 6 — Provenance manifest — `pending`

**Reduced in scope by F14.** The curation script is gone: with no second copy of
any artefact, there is nothing to keep in sync, so the manifest is an index
rather than a correctness mechanism.

- [ ] Emit `04_thesis_results/MANIFEST.md`: artefact → producer script → source
      data → citing chapter
- [ ] Verify the invariant that replaces F11's: **every artefact in tier 04 has a
      live producer**. A file failing that check is the `fig2_granularity` case
      (F4) or the `phase3_result.json` case (F16), caught automatically rather
      than by a manual sweep months later.
- [ ] Confirm no generator writes into `05_thesis_writing/` (F14's boundary)

### Phase 7 — Style pass — `pending`

- [ ] One shared matplotlib style module; consistent DPI, fonts, palette
- [ ] Decide export format policy (PNG for Word, SVG retained for scaling)
- [ ] Apply the `export_appendix.py` table conventions (no hard-coded numbers,
      `<!-- REVIEW -->` marker, units in headers) to every table generator (F7)

## Decisions

| ID | Decision | Rationale | Date |
|----|----------|-----------|------|
| DEC-P0046-TAXONOMY | Split "orphan" into CONCEPTUAL vs DERIVED | A diagram of an idea needs no dataset; a chart of numbers does. Collapsing them would either delete good diagrams or ship undefendable charts. | 2026-09-05 |
| DEC-P0046-CURATION | Produce where it lives; promote only what ships. `05_thesis_writing/` is written **exclusively** by the curation script — no generator writes there. `04_thesis_results/appendix/` is a production site too, despite its name. | Keeps diagnostic artefacts next to the step that made them (traceable), keeps tier 05 small enough to review, and makes "one writer" the invariant the manifest depends on. Brian, F11. | 2026-09-05 |
| DEC-P0046-PATHS | No output location may be a literal string in a generator; all resolve through `PATHS.py`. | Output locations are currently expressed three different ways, which is the structural cause of the sprawl. Centralising files without centralising the constant would re-sprawl. Brian, F13. | 2026-09-05 |
| DEC-P0046-SINGLE-HOME | **Supersedes the promotion half of DEC-P0046-CURATION.** Tier 05 holds no figures/tables/diagrams at all — only writing apparatus (citations, snapshots, notebookLM, drafts, notes). Every artefact lives exactly once, in `04_thesis_results/`. | Removes the second copy rather than defending it with a manifest: a copy not machine-linked to its producer *is* the `fig2_granularity` failure mode. Also reduces the clean-repo rule to "tiers 00-04 ship, 05 does not". Brian, F14. | 2026-09-06 |
| DEC-P0046-ROUTING | Producer tier decides: data-processing figures come from `02_thesis_data/`, modelling/serving/orchestration from `03_thesis_modelling/`, general diagrams from scripts in `04_thesis_results/` — all writing into `04_thesis_results/`. EDA volume is the one exception (stays at the pipeline, only candidates promoted). | Extends the existing train-vs-serve test from `repo-tier-structure.md` to outputs, so one rule covers scripts and artefacts. Semantic fit is carried by producer location + subfolder name, not by output tier. Brian, F15. | 2026-09-06 |
| DEC-P0046-ZOMBIE | `fig2_granularity.png` deleted outright, no archive copy. | Verified committed at git `4c7a98b`, and cited by zero chapters. Archiving into a tier-05 folder that is never shared protects against a reader who cannot see it. F17. | 2026-09-06 |
| DEC-P0046-ANCHOR | Root discovery anchors on `.env.example` (then `.env`, then `PATHS.py`), walking up from `__file__`. Never `CLAUDE.md`, never `Path.cwd()`, never `parents[N]`. | The repo ships to assessors and should not carry an anchor naming the assistant. The `__file__`/hop-count halves are correctness fixes found while doing it: cwd-anchoring failed from outside the repo, and hop counts encode folder depth, which the restructure changed. Brian + F25. | 2026-09-06 |
| DEC-P0046-DROP-SPSS | Indeks Danmark / SPSS data archived to `.archive/spss_indeksdanmark_2026-09/`; all four PATHS constants removed. | Never used, and will not be in the 9 days to submission. Archived not deleted, being real licensed source data. Leaves an open correction: the abstract still names it as an empirical source (F23). Brian. | 2026-09-06 |
| DEC-P0046-SHIP-SCOPE | **Corrects DEC-P0046-SINGLE-HOME's boundary claim.** Tiers 01-05 (the four SRQ tiers + results) ship to assessors. Tier 00 (context) and tier 06 (writing) are both excluded as AI-guided writing harness. | The shipped set is exactly the work; the excluded set is exactly the apparatus for writing about it. I had wrongly written "00-04 ship". Brian, F22. | 2026-09-06 |
| DEC-P0046-SRQ-TIERS | Top-level folders map one-to-one onto research questions (`01_SRQ1_Model_Training/` .. `04_SRQ4_Scenario_Experiment/`), with data + modelling nested under SRQ1. | A script's location now states which SRQ it answers, extending the existing train-vs-serve test to the whole tree. Brian, F19. | 2026-09-06 |
| DEC-P0046-SLUGS | Results folders carry descriptive slugs: `srq1_model_performance/`, `srq2_structured_tool_interface/`, `srq3_integration_readiness/`, `srq4_scenario_experiments/`. | Bare `srq1/` says nothing at a glance in the tree humans browse to pick artefacts. Brian, F20. | 2026-09-06 |
| DEC-P0046-RUNS-WITH-EXPERIMENT | Raw per-run material lives with the experiment that produced it; only the aggregation across runs reaches the results tier. | Settles the srq4-layout question better than either option offered: the runs do not belong in results at all. Also explains why the per-SRQ shape has no `raw/`. Brian, F20. | 2026-09-06 |
| DEC-P0046-EDA-SPLIT | EDA `.csv` stays in `pipeline_step_outputs/` (downstream steps consume it); `.md` tables and `.png` plots promote to `05_thesis_results/eda/{category}/`. ~38 files/category, ~150 total. | Splits by what consumes each file rather than by hand-picked judgement, so it needs no decision per file and no citation sweep first. Brian, F21. | 2026-09-06 |
| DEC-P0046-ORPHAN-EXIT | ORPHAN-DERIVED files get a per-file RESTORE or RETIRE call, decided after the Phase 5 citation sweep. RETIRE archives the image *and* leaves the notebook archived — both halves move together. | The archived notebooks are adaptable, not broken, so a bulk verdict would discard recoverable work. Leaving a retired image in a live folder is the `fig2_granularity` failure mode. Brian, F12. | 2026-09-05 |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| `grep -rIl` over repo root timed out at 120s | 1 | Network drive (Z:) is slow on full-tree walks. Used the Grep tool instead, which is ripgrep-backed and respects ignore files. |
