---
pid: P0046
created: 2026-09-05 20:40:00
updated: 2026-09-05 21:05:00
status: in_progress
focus_detail: "Phase 1 complete (F1-F9). Phase 2 DECIDED 2026-09-05: produce-where-it-lives / promote-what-ships, PATHS centralisation, per-file restore-or-retire (F11-F13). Next session starts at Phase 3 (PATHS.py constants) — no file moves until then."
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

### Phase 3 — Centralise paths in `PATHS.py` — `pending` — **start here next session**

Per DEC-P0046-PATHS (F13). Constants first, moves second: adding the constants is
reversible and touches no artefacts, so it is the safe half to do before any of
the destructive steps in Phase 4.

- [ ] Add the eight constants/helpers listed in findings F13
- [ ] Fix the stale tier-map docstring at `PATHS.py:28` — it still advertises
      `sections-final/`, archived 2026-09-01
- [ ] Repoint `04_thesis_results/generate_figures.py` from its hard-coded
      `"05_thesis_writing/figures"` to `THESIS_RESULTS_DIAGRAMS_DIR` (this both
      removes the CWD-relative string *and* stops it writing into tier 05,
      which the curation contract forbids)
- [ ] Repoint `05_thesis_writing/figures/generate_systemB_diagram.py` likewise —
      and relocate the script itself out of tier 05
- [ ] Replace `export_appendix.py`'s inline `OUT = THESIS_RESULTS_DIR / "appendix"`
      with `THESIS_RESULTS_APPENDIX_DIR` (same destination, no behaviour change)
- [ ] Point `srq1_figures.py` / `srq1_shap.py` at `THESIS_RESULTS_SRQ1_FIGURES_DIR`
- [ ] Delete the byte-identical shadow copy at
      `utility_scripts/scripts/generate_systemB_diagram.py` (md5 `cc6f393695…`)
- [ ] Leave removal-notes at each former literal-string site, following the
      convention already used at `PATHS.py:185-197, 356-360, 662-665`

### Phase 4 — Regenerate and reconcile — `pending`

- [ ] Re-run the free generators: `srq1_figures.py`, `srq1_shap.py`,
      `training_report.py`, `export_appendix.py`
- [ ] **Hold `generate_figures.py`** until `ram_budget_v1` is rewired to the real
      measurements in `04_thesis_results/appendix/02_substrate_resource_profile`
      and `04_sandbox_resource_profile` — re-running it as-is regenerates P0040
      F5's fabricated numbers (F5)
- [ ] Update the six graphviz label sets in `generate_figures.py` so
      `system_architecture_v1` / `data_flow_v1` carry current information
- [ ] Delete zombies (`fig2_granularity.png`), archive superseded
- [ ] Fix the broken `![...](../figures/...)` references in the drafts

### Phase 5 — Citation sweep + validate in-text tables — `pending`

Two jobs, and the first unblocks a Phase 2 leftover.

- [ ] **Citation sweep**: which figures/tables do the chapters actually cite?
      This is the input F12 needs — it decides restore-vs-retire for each of the
      18 ORPHAN-DERIVED files, and it decides what the curation script promotes.
- [ ] Fill in the 18-row restore-or-retire table (F12)
- [ ] Diff each in-text thesis table against its generated counterpart
- [ ] Record every mismatch (do not silently "fix" the thesis — a mismatch may
      mean the artefact is wrong, not the prose)

### Phase 6 — Curation script + manifest — `pending`

The mechanism that makes DEC-P0046-CURATION real. Without it, tier 05 is just
another folder somebody copies into by hand.

- [ ] Write the curation script — the single writer into
      `05_thesis_writing/{figures,tables}/`
- [ ] Emit `05_thesis_writing/MANIFEST.md`: artefact → producer → source data →
      citing chapter → content hash
- [ ] Verify the invariant holds: every file in tier 05 has a manifest row, and
      every row's hash matches. A file that fails either check is the
      `fig2_granularity` failure mode caught automatically instead of by hand.

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
| DEC-P0046-ORPHAN-EXIT | ORPHAN-DERIVED files get a per-file RESTORE or RETIRE call, decided after the Phase 5 citation sweep. RETIRE archives the image *and* leaves the notebook archived — both halves move together. | The archived notebooks are adaptable, not broken, so a bulk verdict would discard recoverable work. Leaving a retired image in a live folder is the `fig2_granularity` failure mode. Brian, F12. | 2026-09-05 |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| `grep -rIl` over repo root timed out at 120s | 1 | Network drive (Z:) is slow on full-tree walks. Used the Grep tool instead, which is ripgrep-backed and respects ignore files. |
