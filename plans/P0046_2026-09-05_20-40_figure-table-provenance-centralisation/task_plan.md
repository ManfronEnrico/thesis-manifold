---
pid: P0046
created: 2026-09-05 20:40:00
updated: 2026-09-07 18:40:00
status: complete
completed: 2026-09-07 18:40:00
outcome_summary: "Superseded by P0050. Delivered: PATHS.py rebuilt for the SRQ tiers (39/39 resolve), root anchor moved off CLAUDE.md, stale artefacts archived with recovery READMEs, SRQ1 reshaped, 149 EDA artefacts promoted, the diagram set rebuilt after it was found to depict a system never built, pipeline execution + content logging added and consumed by the appendix, and six chapter figures built. Open work (Phase 5 inventory, Phase 6 invariants, Phase 7 style) moved to P0050 along with all findings."
---

# P0046 — Figure, Table & Graph Provenance and Centralisation

> **⚠ SUPERSEDED 2026-09-07 by
> [P0050](../P0050_2026-09-07_18-40_figure-table-generation-and-provenance/START_HERE.md).**
> Its findings were consolidated and rewritten there; this plan is kept as the
> record of how the work was done, not as a live task list. Do not resume here.


## Goal

Every figure, table and diagram must be **regenerable from current data** by a
live script, or be a deliberate hand-made artefact whose staleness is a human
judgement. Then: one predictable location, one consistent style.

**Method (corrected 2026-09-06, F19)** — build the regenerable inventory FIRST,
choose citations SECOND:

1. Make the EDA and modelling pipelines log properly and consume their own logs.
2. Make every table/figure/diagram data-driven and regenerable on demand.
3. *Then* decide what to cite, in-text or as appendix.
4. *Then* audit the snapshot comments against that inventory.

"Is it already cited?" is not the test. The draft is provisional — sections are
being removed, and the citation set is an **output** of this work.

---

## STATUS QUO (2026-09-07) — read this first

### Architecture, settled

| Rule | Decision |
|------|----------|
| **Ships to assessors** | tiers `01_SRQ1_*` .. `05_thesis_results/` |
| **Excluded** | `00_thesis_context/` + `06_thesis_writing/` (writing harness) |
| **Artefacts live once** | all in `05_thesis_results/`; tier 06 holds NO figures/tables |
| **Routing** | producer tier decides; tier 05 always receives |
| **Raw runs** | live with their experiment, never in results |
| **EDA split** | `.csv` stays at pipeline; `.md`+`.png` promote |
| **Per-SRQ shape** | `figures/ tables/ models/` — no `raw/` |
| **Paths** | no literal tier name / `CLAUDE.md` anchor / `parents[N]` hop |
| **Root anchor** | `.env.example` → `.env` → `PATHS.py`, walked from `__file__` |
| **RAM envelope** | **4096 MB** (confirmed). Thesis prose says "8 GB" in 8 places — prose fix outstanding |

### Everything regenerates — tested by running, not by reading

| Generator | Emits | Status |
|-----------|-------|--------|
| `export_appendix.py` | 14 tables (01-14) | PASS — reads `srq1/tables/`; clears its own block first |
| `export_holiday_appendix.py` | 4 tables (90-93) | PASS |
| `srq1_export_enrichment_appendix.py` | 6 tables (94-99) | PASS |
| `generate_literature_table.py` | 1 table (89) | PASS — parsed from Ch2 + curated column (F28) |
| `srq1_generate_performance_figures.py` | 3 figures | PASS |
| `srq1_generate_shap_figures.py` | shap png + csv | PASS |
| `training_report.py` | training_report.md | PASS |
| `generate_architecture_diagrams.py` | **11 diagrams** | PASS — needs Graphviz bin on PATH (see Errors) |
| `run_preprocessing.py` | pipeline + EDA + manifest + metrics | PASS — 8/8 runs OK 09-07 |
| SRQ2's 2 surviving files | — | **NO live producer** (F8) |
| 18 `analysis/figures*` | — | **NO producer** — Enrico's archived notebooks |

### Current diagram set (all data-driven)

**System (5):** `pipeline_v2` · `model_selection_v2` · `scenarios_v2` ·
`resource_profile_v2` · `layered_architecture_v2`

**Chapter (6):** `ch1_research_questions_tree_v2` · `ch2_gap_diagram_v2` ·
`ch4_data_pipeline_v1` · `ch4_eda_pipeline_csd_v1` · `ch5_tool_interface_v1` ·
`ch6_modelling_pipeline_v1`

**Appendix output-directory block allocation** (F29 — keep in step when adding
a producer): `01-49` export_appendix · `89` literature table · `90-93` holidays ·
`94-99` enrichment.

Every value is read from an artefact at render time; the generator **exits rather
than drawing** if a source table is missing.

---

## Phases

### Phase 1 — Trace and classify — `complete`
### Phase 2 — Decide the target layout — `complete`

### Phase 3 — Centralise paths — `complete`

PATHS.py rebuilt for SRQ tiers (39/39 resolve); `.env.example` anchor across 7
scripts; `parents[N]` hops replaced in 17; 77 live scripts compile; audit 43→10
(survivors all legitimate); generators renamed to say what they emit;
`requirements.txt` completed (`graphviz`, `matplotlib`, `statsmodels`).

### Phase 3b — Staleness triage + per-SRQ shape — `in_progress`

- [x] Archive-not-delete: zombie figure, phase3 leftover, System B generator,
      shadow copy, `ml_retraining/`, SPSS data — each with a recovery README
- [x] Graphviz installed → all diagrams render
- [x] **Diagrams rebuilt** (F18) — the old set depicted a system never built
- [x] **`ch5_architecture_v1` → `layered_architecture_v2`** (F21)
- [x] **SRQ1 reshaped** — 36 loose → figures/3 tables/33 models/13, zero loose
- [x] **`models/` per-category** (F17) — matches `eda/`; `forecast_tool.py`
      repointed with legacy fallback; all 4 categories verified loading
- [x] **EDA promoted** (F14) — 149 files + `promote_eda_artifacts()` sync
- [x] **SRQ2 judge retired** (F8) — design decided against; producers stay archived
- [x] **`fig1_model_ladder` fixed** (F16) — was rendering empty; title now derived
- [ ] Apply `figures/ tables/ models/` to SRQ2 and SRQ4

### Phase 3c — Pipeline logging — `complete`

Per the corrected method (F19), this comes before any citation decision.

- [x] Audit the EDA/preprocessing pipeline (F20)
- [x] **`run_manifest.json`** — the orchestrator timed every step and then only
      *printed* it; now persisted with step, status, seconds, detail, `ok` roll-up
- [x] **Two bugs found writing the consumer** (F22) — the first draft filed every
      category under `results[0]`'s folder (so `--all-categories` put RTD's record
      in CSD's), and overwrote, so running H=1 erased the H=3 record. Now grouped
      per category and merged by horizon
- [x] **`export_appendix.py` consumes it** — new `table_pipeline_execution()`.
      Step names come from the manifest, not a list in the exporter, so a renamed
      step cannot leave the table describing a pipeline that no longer exists
- [x] **Verified end-to-end** — real CSD H=3 run (steps 3-6, 15.7s, all passed)
      → manifest → appendix table with real timings
- [x] **Per-step content metrics** (F25) — `_step_metrics()` extracts from the
      value each step ALREADY returns, so there is no second code path to drift.
      Lands in the manifest, the `StepResult` and one console line per step
- [x] **Clean slate re-run** — all 4 categories × H=1 and H=3, steps 0-6, 8 runs,
      **all OK**. 149 EDA artefacts promoted to tier 05
- [x] **Second appendix table** — `pipeline_data_reduction`, kept separate from
      the timing table because the units differ (rows/brands vs seconds)
- [x] **Audit the modelling pipeline** (F26) — **2 of 21 scripts record any
      provenance.** Result CSVs carry data columns only: no timestamp, no
      producing script, no input identity. `train_and_persist.py`'s per-model
      `metadata.json` is the good pattern and already exists. Recommendation
      scoped but NOT done: one shared stamp helper, not 19 edits. Ranked below
      Phases 4-6 — it is our audit trail, not a blocker on any thesis artefact

### Phase 4 — Regenerate and reconcile — `complete`

DEC-GENERATE-ALL (Brian, 09-07): generate every figure programmatically; hand
redrawing afterwards is his option, not a reason to leave one ungenerated.

- [x] `ch1_research_questions_tree_v2` — built; the hand-drawn one showed a
      superseded RQ set
- [x] `ch2_gap_diagram_v2` — **rebuilt**, not adopted. The hand-drawn one said
      8 GB; the envelope is 4096 MB
- [x] Both broken `../figures/` refs fixed (ch1, ch5) + an asset note recording
      what was corrected
- [x] **Ch5's caption corrected** — claimed five models, human-in-the-loop
      checkpoints and an agentic layer; the ladder is four and the other two do
      not exist
- [x] Five requested chapter figures built (F27)
- [x] Literature -> design map (F28), a new generator with two provenances
- [x] Orphan README records all three as superseded, do-not-paste

### Phase 5 — Inventory → citation decisions — `pending` — **START HERE**

Reframed by F19. Only after Phases 3c/4:

- [ ] Publish the complete regenerable inventory
- [ ] Decide per artefact: in-text, appendix, or neither
- [ ] Then audit snapshot comments against it
- [ ] Decide the 18 `analysis/figures*` on regenerability, not on citation

### Phase 6 — Manifest + invariant checks — `pending`

- [ ] `05_thesis_results/MANIFEST.md`: artefact → producer → source → status
- [ ] Check: every tier-05 artefact has a live producer
- [ ] Check: `PATHS.py` self-test asserting every `*_DIR` exists
- [ ] Check: no live script holds a literal tier name (the F3 audit script)
- [ ] Check: no two files in a generated directory share an identity prefix (F24)
- [ ] Check: a producer reports "N written, M skipped" so a structural break is
      loud rather than a run of polite notices (F23)

### Phase 7 — Style pass — `pending`

- [ ] Shared matplotlib style; DPI/font/palette consistency
- [ ] Export format policy (PNG for Word, SVG retained)
- [ ] Generalise `export_appendix.py`'s table conventions

---

## Decisions

| ID | Decision | Date |
|----|----------|------|
| DEC-TAXONOMY | Orphan split: CONCEPTUAL (no dataset, fine) vs DERIVED (chart of numbers, needs a producer) | 09-05 |
| DEC-SINGLE-HOME | Tier 06 holds no artefacts; everything lives once in `05_thesis_results/` | 09-06 |
| DEC-SHIP-SCOPE | Tiers 01-05 ship; 00 and 06 are the writing harness | 09-06 |
| DEC-SRQ-TIERS | Top-level folders map 1:1 onto research questions | 09-06 |
| DEC-SLUGS | Results folders carry descriptive slugs | 09-06 |
| DEC-ROUTING | Producer tier decides where a script lives; tier 05 receives | 09-06 |
| DEC-RUNS-WITH-EXPERIMENT | Raw per-run material stays with its experiment | 09-06 |
| DEC-EDA-SPLIT | `.csv` stays at pipeline, `.md`+`.png` promote | 09-06 |
| DEC-PATHS | Every output path resolves through `PATHS.py`; stated as a greppable check | 09-06 |
| DEC-ANCHOR | Root anchor `.env.example`, walked from `__file__` | 09-06 |
| DEC-ARCHIVE-NOT-DELETE | Stale artefacts → level-appropriate `.archive/` + README | 09-06 |
| DEC-DROP-SPSS | Indeks Danmark archived; abstract correction outstanding | 09-06 |
| DEC-NAMES | Generator filenames state what they emit | 09-06 |
| DEC-RAM-4GB | 4096 MB is the envelope; thesis prose needs correcting | 09-06 |
| DEC-JUDGE-RETIRED | LLM-as-Judge decided against; artefacts + producers archived | 09-06 |
| DEC-DIAGRAMS-FROM-CODE | Diagrams read artefacts at render time and refuse to draw from absent data. No literals | 09-06 |
| DEC-INVENTORY-FIRST | Build the regenerable inventory, then choose citations. Never the reverse | 09-06 |

---

## Open items for Brian

1. **Abstract correction** — the thesis claims Indeks Danmark as an empirical
   source; it was never used. Abstract only (2 occurrences); Ch3/Ch4 are clean.
   Note at `06_thesis_writing/writing-notes/indeks-danmark-claim-must-be-corrected.md`.
   Prose edit in the `.docx`.
2. **"8 GB" → 4 GB in Ch6** — eight occurrences. Changes a stated claim.
3. **Ch8 §8.3 / Table 21** — the LLM-as-Judge section comes out; the artefacts
   are already archived.
4. **`ch2_gap_diagram`** — adopt as hand-made, or rebuild in the generator?
5. **P-ID collision** — a second `P0046_..._exogenous-enrichment-decision/`
   folder exists; one should be renumbered.

## Errors

| Error | Note |
|-------|------|
| `grep -rn/-rl` over the repo times out at 120s | **Five sessions running.** Z: is slow on full-tree walks. Reached for `grep -rln` again on 09-07; the Grep tool then answered the same question instantly. Root cause is that `rglob`/`-r` walks `.venv` (~40k files) — any sweep must exclude `.venv`, `.git`, `__pycache__`. Genuine `/errors-log` material |
| Bulk-edit script broke the SAME file 3x (09-07) | `\n` inside a heredoc-generated Python string collapsed to a real newline, twice; the third attempt's repair heuristic then mangled 7 innocent lines including the module docstring. Fix: `git checkout --` and use the **Edit tool**, which takes text literally. Rule: never generate Python source through a shell heredoc when the source itself contains escapes |
| Graphviz not on PATH in a fresh shell | `winget install` put `dot.exe` at `C:/Program Files/Graphviz/bin` but did not add it to this shell's PATH, so the diagram generator raised `ExecutableNotFound`. Prepend that dir before running it. Code issue: none |
| A shell heredoc turned `\b` into a backspace in a plan file | Writing a Windows path inside a Python string in a heredoc. Python warned (`SyntaxWarning: invalid escape sequence`) and the control char landed in the .md, where the Edit tool then could not match the line. Avoid backslash paths in generated strings; the warning is the tell |
| Reshape repointed producers but not consumers | Moving SRQ1 output into `tables/` left `export_appendix.py` reading the flat root. It failed *silently* — six "(skip …absent)" notices, exit 0, half the appendix gone. A move is not done until every reader is repointed; skip-on-missing hides exactly this |
| Bulk-edit scripts broke syntax 4x | Block inside a function; paren after a comment; `\n` written as real newlines twice. The compile sweep caught each immediately — keep it as a gate on every bulk edit |
| Verified dataclass fields by inspection, not execution | `write_run_manifest()` first used `st.reason` and treated `st.step` as a string; both wrong. Round-tripping real objects caught it |
| Plugin hook flags `focus_detail` frontmatter | False positive: the field is required by `workflow-planning-with-files.md`. Not stripped |
