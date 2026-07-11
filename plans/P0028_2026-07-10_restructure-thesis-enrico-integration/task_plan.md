---
pid: P0028
created: 2026-07-10 16:00:00
updated: 2026-07-11 19:30:00
status: in_progress
focus_detail: "Phases 2, 3, 4, 4b, 5, 6, and 7 all COMPLETE. Root now contains only the numbered tree (00_thesis_context through 05_thesis_writing) plus .archive/, with zero stale thesis/ path bugs in live code and the new structure locked/documented via .claude/rules/repo-tier-structure.md. Phase 7's blocker turned out stale -- a merge to main (4324605) had already absorbed the unrelated 232-path uncommitted state before this session resumed -- so Phase 7 committed cleanly on a new branch (chore/p0028-phase5-6-docs) in 3 chunks. Next: Phase 8 (docs updates) on that same branch, then PR/merge back to main."
---

## What's Left (as of end of Session 6, 2026-07-10 21:45) — read this first when resuming

**Done**: Phases 1–4. The full locked tree physically exists at repo root. All PATHS.py constants resolve to real, populated folders. All 12 relocated scripts compile from their new locations. Nothing has been deleted anywhere — every old-location original (`thesis/`, root `results/`, root `reports/`, `utility_scripts/scripts/` originals, `user-docs/literature/` originals) is still on disk untouched.

**DONE — Phase 5 (cross-reference sweep, Session 8, 2026-07-11)**:
- Repo-wide grep for all old-style path patterns across `.py`/`.md`/`.ipynb`. Fixed 4 live-code bugs (`OUTPUT_DIR` in `generate_figures.py` x2 copies and `generate_systemB_diagram.py` x2 copies, all pointed at the deleted `thesis/thesis-writing/figures/`) — now point at `05_thesis_writing/figures/`. Everything else matched was cosmetic-only (docstrings/comments/frozen notebook output cells), verified not to affect live path logic (`PATHS.py` constants confirmed resolving correctly via `python3 -c` import check; 5 scripts spot-checked clean with `py_compile`).
- `user-docs/contributing/repository_map.md` vs `user-docs/dev/repository_map.md` found to have **diverged** (not simple duplicates), both stale — flagged for Phase 6/8 reconciliation rather than patched piecemeal.

**DONE — Phase 7 (git commits, Session 9, 2026-07-11)**:
- Resumed to find the Phase 7 blocker (232-path unrelated uncommitted state) already resolved: merge `4324605` ("merge: thesis/csd-eda-rerun -> main") had landed on `main` between sessions and absorbed it. Working tree at resume held only this plan's own Phase 5/6 changes.
- Was on `main` directly (not a feature branch) — confirmed with user before proceeding per branch-strategy Trust-tier rule; created `chore/p0028-phase5-6-docs` off `main`.
- Committed in 3 chunks (originally planned as 5; folder-copy and cross-ref-fix chunks were already covered by the `4324605` merge): `c890b41` (PATHS.py structure-lock docstring), `1be23ea` (4 OUTPUT_DIR script fixes, py_compile-verified), `aa612c6` (docs/rules: repo-tier-structure.md, CLAUDE.md reference, handover pointer-note).
- Plan tracking files (this file, progress.md, tasks/14.json, tasks/15.json, tasks/16.json) committed separately as the final Phase 7 chunk.
- `AGENTS.md` (root) found stale on far more than just `thesis/` paths (still references nonexistent `docs/`/`.Codex/` predating the `docs`→`user-docs` rename) — flagged for the broader docs pass, out of scope for a path-string sweep.
- `user-docs/handover/2026-07-01_enrico-to-brian-merge-handover.md` — left as a dated historical snapshot (not rewritten), added a pointer note at the top referencing this plan for the old→new path mapping.

**DONE — Phase 6 (document + lock the structure, Session 8, 2026-07-11)**:
- Added a structure-map comment to `PATHS.py`'s module docstring (tier 00-05, what belongs in each, pointer to the new rule file).
- Created `.claude/rules/repo-tier-structure.md` — the authoritative locked-structure reference: tier quick-reference table, "new SRQ results always go in `04_thesis_results/srq{N}/`" rule, `model_training/` vs `model_serving/` train-vs-serve rule, `utility_scripts/` tooling-only scope rule, `02_thesis_data/preprocessing/` scripts-not-data clarification, and the explicit do-not-delete callout for `02_thesis_data/_03_engineered/nielsen/` (citing findings.md Session 6 #4) plus a note on `02_thesis_data/`'s other legacy leftovers (`nielsen/`, `preprocessing/`, `assessment/`).
- Updated CLAUDE.md's Key References table with a new row pointing at the rule file (its Quick Start/Folder Map sections were already current from an earlier session).

**Not started — Phase 7 (git commit)**:
- Cannot start yet — nothing has been staged. Also: the pre-existing 232-path uncommitted repo state (see findings.md Session 6 #5) needs to be reviewed/handled by the user before any P0028 commit, since it's unrelated prior work sitting in the same working tree.
- When ready: 5 reviewed commits per the original plan (PATHS.py additions → script updates → folder copies → cross-ref fixes → docs/rules).

**Not started — Phase 8 (broader docs)**:
- `user-docs/contributing/repository_map.md`, `README.md`, handover docs.

**Explicitly NOT part of Phase 5–8 — deferred, needs its own decision point**:
- **The actual cleanup/deletion of old-location originals.** This whole restructure used copy-not-move specifically so other concurrent Claude Code sessions wouldn't have files yanked out from under them. Old locations stay on disk until the user explicitly confirms those other sessions are done. This is being tracked as an unscheduled "Phase 4b" — not yet created as a real phase, add it when the user gives the go-ahead.

**New loose ends surfaced during Phase 4 execution, not yet resolved** (full detail in findings.md "Session 6" section):
1. Root-level `integrations/` folder (duplicate of `utility_scripts/src/google_drive_integration.py`) — not in the locked tree, not touched, needs a diff + delete-or-keep decision.
2. `00_thesis_context/` actually has `methodology/` and `prometheus-integration/` subfolders in addition to the two documented in the tree diagram — cosmetic gap in this plan's tree diagram vs. reality, no action needed, just noting it.
3. Literature version conflict in `01_thesis_research/literature/` — both the Jul 10 (current) and Jun 30 (dated-prefix) versions of `bibtex.bib`/`citations.json` are preserved, but nobody has manually reconciled why 3 citations differ. Needs human review, not a Claude decision.
4. `02_thesis_data/_03_engineered/nielsen/{CSD,Danskvand,Energidrikke,RTD}/` — old-shape engineered data (real, not empty) now sits as a third sibling next to `bymonth/`/`bychain/`. Left in place per user's direction. Should get an explicit callout in the Phase 6 structure-lock rule so it's not mistaken for bloat later.

**Two explicit action items from the user (2026-07-10, end of Session 6) — RESOLVED (Session 7, 2026-07-11):**

5. ✅ **RESOLVED — Phase 4 copy into root verified wholesale, stale `thesis/` originals deleted.** Every copied subtree re-diffed against its `thesis/...` source using file-count + total-byte-size comparisons (task 11). All checked out: `thesis-context` (18 old vs 13+5, the 5 being `research-questions/*` correctly relocated to `01_thesis_research/research-questions/` per Decision Log #1), `literature` (65 vs 67, +2 dated-prefix files from `user-docs/literature/`, expected), `_00_raw` (52/52 files, 36,243,857,738 bytes byte-identical — this was previously only exit-code-trusted, now properly verified), `modelling` (13 vs 39, +12 relocated scripts + `__pycache__`, expected), `thesis-writing` (68 vs 67, the one "missing" file was a 162-byte Word `~$` lock/temp artifact, not real content), `thesis_agents` (92 vs 93, +1 relocated test file). No concurrent-session activity detected in `thesis/` (checked twice, no mtimes in the prior 10 minutes). User gave explicit go-ahead; `thesis/` deleted in full.

6. ✅ **RESOLVED — root-level `results/` and `reports/` fully removed from root.** User asked for the git origin to be re-traced rather than trusting Decision Log #7 verbatim. **Correction surfaced**: `results/seaborn_exploratory/` (3 PNGs) actually traces to **Brian's own** commit (`85c69b4`/`14433dd`, 2026-04-20, the seaborn EDA audit trail) — NOT Enrico's, contrary to the original blanket attribution in Decision Log #7. Everything else (`reports/eda`, `reports/final`, `reports/shap`, `results/phase1`, `results/ml_retrain_2026-04-16`) traces cleanly to Enrico's commits (`ec350d0` 2026-07-08 merge / `368a967` 2026-04-13 original). Archive copies (`.archive/enrico_legacy_results_2026-04/`, `.archive/enrico_legacy_reports_2026-07/`) verified byte-identical/file-count-identical before any deletion. User was asked how to treat `seaborn_exploratory/` specifically (archive / integrate into `04_thesis_results/` / leave) and chose **delete outright** — the plan's own "move to `04_thesis_results/` if source can't be traced" fallback did not apply since tracing succeeded. Deletions executed in explicitly-confirmed chunks after Claude Code's auto-mode classifier correctly blocked two overly-broad `rm -rf` attempts that bundled targets not yet named in the confirmation (`ml_retrain_2026-04-16` was investigated but not confirmed in the first pass — confirmed and deleted in an explicit follow-up). **Final state**: `results/`, `reports/`, and `thesis/` are all gone from root; only `04_thesis_results/` (the correct new location) remains.

---

## Execution Strategy Note (added before execution start)

**Phase 4 changes from `git mv` to copy-and-defer-delete.** Reason: other Claude Code sessions may be actively working against the current (pre-restructure) paths. A destructive `git mv` would yank files out from under them mid-session. Instead:

1. Physically **copy** (not move) every file/folder to its new target location per the locked tree.
2. Leave the old-location originals in place, untouched, for now.
3. `PATHS.py` and updated scripts point at the **new** locations (this is still safe — new constants point to freshly-copied content).
4. Once the user confirms all other concurrent sessions have wrapped up, run a follow-up cleanup pass that deletes the stale old-location originals (tracked as a new Phase 4b, not yet created — will be added when the user gives the go-ahead).
5. This does **not** change Phase 2 or Phase 3 at all — both are purely additive (new PATHS.py constants, updated import statements in scripts still sitting in their current location). The copy-vs-move distinction only matters starting at Phase 4.
6. `git mv` in the Phase 4 code blocks below should be read as superseded — treat every `git mv src dst` as `cp -r src dst` (or Windows equivalent) until the cleanup pass is greenlit.

# P0028: Root Restructure + Enrico Integration

## Goal

Flatten and renumber the entire repo root (not just `thesis/`) into a clean, logically-ordered hierarchy with **zero hardcoded paths** — all path logic centralized in `PATHS.py`. Eliminate structural bloat, duplicate/legacy folders, and Enrico's stray root-level artifacts. Split `utility_scripts/` into real tooling vs. thesis-pipeline code and relocate the latter.

**Scope grew significantly since Phase 1**: originally scoped to `thesis/data/` tier cleanup; now covers the full repo root after user's own pruning pass surfaced `results/`, `reports/`, and `utility_scripts/` as additional bloat, and after 3 rounds of tree critique changed the final shape substantially. Treat the "Context" section below as authoritative over any earlier phase text — phases 2–8 below have been rewritten to match.

---

## Context (current, authoritative — supersedes all earlier versions in this file)

### Why the scope expanded

1. User's own pruning pass deleted `.obsidian/`, `INDEX.md`, `Untitled.canvas`, `_claude-brain/` from `thesis/` and root — all confirmed Enrico slop or stale AI-tool scaffolding.
2. User traced two more root folders and asked Claude to confirm origin:
   - `results/` — **confirmed**: Enrico, commit `368a967` (2026-04-13), an old April ML-retraining pass (`ml_retrain_2026-04-16/`, `phase1/`, `seaborn_exploratory/`). Superseded by `_05_results_srq1/` (now `04_thesis_results/srq1/`).
   - `reports/` — **confirmed**: Enrico, commit `ec350d0` (2026-07-08), pre-merge working-tree commit. Contains `eda/`, `shap/`, `final/` PNGs + `index.html` — an earlier, un-versioned draft of what's now properly tracked in the SRQ1 results tier.
   - Decision: **archive both, don't delete** — `.archive/enrico_legacy_results_2026-04/` and `.archive/enrico_legacy_reports_2026-07/`. Git history alone wasn't judged sufficient; user wants them physically out of the way but retrievable without a git archaeology exercise.
3. User created `utility_scripts/` and moved former root `scripts/`, `src/`, `tests/` into it, correctly identifying that most of `scripts/` isn't "utility" — it's the actual thesis ML/agentic pipeline (SRQ1/2/4 code) miscategorized by whoever (Enrico) put it in a generic `scripts/` folder.
4. Three rounds of tree critique (see Decision Log) changed: tier ordering (writing now last, not before results), tier naming (`literature` → `research`), `thesis/` flattened to root, and the serving-layer naming settled on `model_serving` (not `model_accessibility` or `model_sharing`).

### Final target structure (locked)

```
thesis-manifold/                              (root — "thesis/" segment removed entirely)
├── PATHS.py                                  ← single source of truth for all paths
├── CLAUDE.md
├── README.md
├── requirements.txt
│
├── 00_thesis_context/                        (was: thesis/thesis-context)
│   ├── thesis-topic/                         (project-state.md etc.)
│   └── formal-requirements/                  (compliance.md, CBS requirements)
│   # NOTE: research-questions/ MOVES OUT to 01_thesis_research (see Decision Log #1)
│
├── 01_thesis_research/                       (renamed from "literature" — was: thesis/literature)
│   ├── research-questions/                   (MOVED IN from 00_thesis_context)
│   └── literature/                           (bibtex.bib, citations.json — the real, working-data versions)
│
├── 02_thesis_data/                           (was: thesis/data)
│   ├── _00_raw/                              (Tier 1: raw Nielsen JSONL, SPSS CSV)
│   ├── _01_converted/                        (Tier 2: Parquet caches)
│   ├── _02_preprocessing/                    (Tier 3: preprocessing scripts + step outputs; EDA scripts live here, e.g. pre_csd_1.5_eda.py — NOT in modelling)
│   ├── _03_engineered/                       (Tier 4: feature matrices, split by granularity)
│   │   ├── bymonth/                          (was: _03_engineered_dvhexclhd)
│   │   └── bychain/                          (was: _04_engineered_bychain)
│   └── METADATA.py                           (MOVED IN from utility_scripts/scripts/ — Nielsen column reference = data documentation)
│
├── 03_thesis_modelling/                      (was: thesis/modelling)
│   ├── notebooks/                            (existing — possibly stale, verify later, out of scope for P0028)
│   ├── prompts/                              (existing)
│   ├── model_training/                       (NEW — MOVED IN from utility_scripts/scripts/)
│   │   ├── srq1_baselines_stat.py
│   │   ├── srq1_benchmark.py
│   │   ├── srq1_benchmark_tuned.py
│   │   ├── srq1_calibration.py
│   │   ├── srq1_profiling.py
│   │   ├── srq1_shap.py
│   │   ├── srq2_agent.py
│   │   ├── srq2_synthesis.py
│   │   ├── srq4_experiment.py
│   │   └── srq4_tier2.py
│   └── model_serving/                        (NEW — settled name, see Decision Log #5)
│       ├── system_a_forecast/                (forecast_service.py — dedicated ML model, System A Oracle)
│       └── system_b_conversational/           (placeholder — GPT fallback → Prometheus bridge; empty for now)
│           └── generate_systemB_diagram.py    (documents this component — MOVED IN from utility_scripts/scripts/)
│
├── 04_thesis_results/                        (was: floating _05_results_srq1, _06_results_srq2, _07_forecast_service)
│   ├── srq1/                                 (forecasting benchmark, tuned models, SHAP)
│   ├── srq2/                                 (synthesis + LLM-as-Judge outputs)
│   ├── srq4/                                 (code-as-action results — placeholder, TBD after prompt review)
│   └── generate_figures.py                   (MOVED IN from utility_scripts/scripts/ — reads results, writes figures; runs AFTER training)
│
├── 05_thesis_writing/                        (was: thesis/thesis-writing — MOVED LAST, see Decision Log #2)
│   ├── sections-drafts/
│   ├── sections-final/
│   └── references.md                         (IF it still exists — user believes they deleted it; not chased further, see Decision Log #6)
│
├── .archive/
│   ├── thesis_agents_preintegration/          (was: thesis/thesis_agents — pre-integration System A/B skeleton)
│   ├── enrico_legacy_results_2026-04/         (was: root results/ — archived, not deleted)
│   └── enrico_legacy_reports_2026-07/         (was: root reports/ — archived, not deleted)
│
├── user-docs/                                 (was: docs/ — renamed by user for clarity; verify no working-data files like .bib/.json lurking in user-docs/literature/, see Decision Log #7)
│
├── utility_scripts/                           (TRIMMED — only real tooling remains, ~9-13 scripts not 25)
│   ├── scripts/
│   │   ├── dynamically_find_root_directory.py
│   │   ├── gdrive_citation_matcher.py
│   │   ├── notebooklm_ingestion.py
│   │   ├── set_all_citation_keys.py
│   │   ├── test_group.py                     (verify: testing what? before finalizing placement)
│   │   ├── unified_sync_check.py
│   │   ├── zotero_client.py
│   │   ├── zotero_gdrive_filename_validator.py
│   │   └── zotero_sync_phase1.py
│   ├── src/
│   │   └── google_drive_integration.py
│   ├── tests/
│   │   ├── test_agent_system_comprehensive.py  (verify: testing what system? before finalizing)
│   │   ├── test_builder_integration.py
│   │   ├── test_notebooklm_scanning.py
│   │   └── test_unified_sync.py
│   └── ml_retraining/                          (SAME ERA as archived root results/phase1 — audit before deciding move vs. archive; may be dead code, see open item)
│
└── plans/
    └── P0028_.../  (this plan)
```

### Data tier hierarchy (Tier 1–4, inside `02_thesis_data/`)

Unchanged in substance from the original plan — only the parent path changed (`02_thesis_data/` instead of `thesis/data/`):

```
_00_raw/            Tier 1 — raw Nielsen JSONL, SPSS CSV (source of truth, never modified)
_01_converted/      Tier 2 — Parquet caches (Stage 1 conversion output)
_02_preprocessing/   Tier 3 — preprocessing scripts + step outputs (includes EDA scripts)
_03_engineered/      Tier 4 — feature matrices, split by granularity
  ├─ bymonth/        DVH EXCL. HD, brand×month (was _03_engineered_dvhexclhd)
  └─ bychain/        DVH EXCL. HD, brand×chain (was _04_engineered_bychain)
```

---

## Decision Log (chronological, all rounds of critique)

| # | Decision | Rationale | Round |
|---|----------|-----------|-------|
| 1 | Research questions move from `00_thesis_context` to `01_thesis_research` | RQs are research content, not project meta/scoping. Context folder keeps only hard requirements + topic overview, which can reference RQs by link. | 3 |
| 2 | `thesis_writing` renumbered to LAST tier (05), not tier 04 | Writing consumes everything upstream (context, research, data, modelling, results) — numbering it before its last dependency (results) was backwards. | 2 |
| 3 | `01_thesis_literature` renamed to `01_thesis_research` | "Research" is the right altitude once RQs move in — literature alone was too narrow a label for a tier that now holds both RQs and lit corpus. | 2 |
| 4 | `thesis/` segment removed; all subfolders flatten to repo root | Every `PATHS.py` path was `ROOT_DIR / "thesis" / ...` — pure ceremony, no sibling project it disambiguates from. Shortens every path, zero information loss. | 2 |
| 5 | Serving-layer folder named `model_serving/` (not `model_accessibility/` or `model_sharing/`) | "Serving" is the standard ML-engineering term, pairs cleanly with `model_training/` (train → serve pipeline), and directly names the thesis's own RQ (comparing two model-serving strategies: dedicated vs. code-as-action). "Accessibility" collides with disability/UX accessibility as a term of art; "sharing" is too vague (file sharing? weight sharing? results sharing?). | 3 |
| 6 | `references.md` — not chased further | User believes they already deleted it as suspected slop. Low stakes either way; if it resurfaces, rule is it lives at the writing tier's root (consumed by all chapters), not nested in a subfolder. | 2 |
| 7 | Root `results/` and `reports/` — archived, not deleted | Traced and confirmed as Enrico's stale artifacts (April ML retrain pass; pre-merge draft EDA/SHAP report set). User overrode Claude's "delete outright" recommendation — wants them retrievable without a git archaeology exercise. **Amended Session 7**: `results/seaborn_exploratory/` was actually Brian's own work (commit `85c69b4`/`14433dd`), not Enrico's — re-traced on user request, user then chose to delete it outright rather than archive/integrate. | 3 (amended 7) |
| 8 | `utility_scripts/` split: real tooling stays, thesis-pipeline code moves out | User's dividing line: does this script help you WORK ON the thesis (tooling) or IS it the thesis pipeline (content)? Applied to all 25 scripts in `utility_scripts/scripts/` — 12 SRQ1/2/4 scripts + `forecast_service.py` + `generate_figures.py` + `generate_systemB_diagram.py` + `METADATA.py` all move out; 9 remain (Zotero/GDrive/NotebookLM integration helpers, root-finder, sync checks). | 3 |
| 9 | `forecast_service.py` → `03_thesis_modelling/model_serving/system_a_forecast/` | Reads engineered feature matrices, serves forecasts — downstream of training, not an output artifact (it's a live service), not writing/prose. | 3 |
| 10 | `system_b_conversational/` created as sibling placeholder (empty for now) | Second serving layer: GPT fallback → Prometheus bridge for conversational LLM access to trained models. Same tier as system_a for symmetry; avoided inventing a new numbered top-level tier for one empty placeholder. | 3 |
| 11 | `METADATA.py` → `02_thesis_data/` | It's Nielsen column/schema documentation — data documentation, not modelling code. | 3 |
| 12 | `generate_figures.py` → `04_thesis_results/` | Reads results, writes figures; runs after training completes — belongs with outputs, not with training code. | 4 (this round) |
| 13 | `generate_systemB_diagram.py` → `03_thesis_modelling/model_serving/system_b_conversational/` | Documents that specific component; not general-purpose enough for `05_thesis_writing/`. | 4 (this round) |
| 14 | `.claude/plans` — deleted by user (confirmed no duplicate plan-tracking location) | Was flagged as a possible second plan store; user resolved directly. | 3 |
| 15 | `.agents/` and `.codex/` root folders — explicitly ignored per user instruction | Flagged as possible slop (leftover Codex/other-AI-tool scaffolding) but user said to ignore; not in scope for P0028. | 3 |

---

## Open Items — RESOLVED (Session 5, 2026-07-10 20:15)

| Item | Resolution |
|------|-----------|
| `utility_scripts/ml_retraining/` — move, archive, or delete? | **RESOLVED: archive.** `grep -rln "ml_retraining" --include="*.py" --include="*.ipynb"` across the whole repo found matches only inside `ml_retraining/` itself (self-references, `__init__.py` imports between its own numbered scripts). Zero external references. Same era/treatment as archived root `results/phase1` (April ML retrain, superseded by the SRQ1 pipeline). **Phase 4 action**: copy `utility_scripts/ml_retraining/` → `.archive/ml_retraining_2026-04/` (leave original in place per copy-not-move strategy). |
| `utility_scripts/tests/test_agent_system_comprehensive.py` — tests what system? | **RESOLVED: archive.** Read in full — it tests `thesis.ai_research_framework.core.coordinator` / `build_research_graph()`, the pre-integration LangGraph System A skeleton. That module lives under the now-archived `thesis_agents/` (→ `.archive/thesis_agents_preintegration/`). **Phase 4 action**: copy this test file into `.archive/thesis_agents_preintegration/` alongside the code it tests, rather than leaving it in active `utility_scripts/tests/`. |
| `utility_scripts/scripts/test_group.py` — same ambiguity | **RESOLVED: keep in place.** Read in full — it's a live Zotero group-library connection smoke test (uses `pyzotero`, reads `ZOTERO_GROUP_ID`/`ZOTERO_API_KEY` from `.env`). Genuine active tooling. **Phase 4 action**: none — stays in `utility_scripts/scripts/`. |
| `user-docs/literature/` — contents unknown | **RESOLVED: move confirmed.** `ls` shows `bibtex.bib` (54KB) and `citations.json` (57KB) — exactly the Enrico mistake repeated (working data in a user-facing docs folder). **Phase 4 action**: copy both files to `01_thesis_research/literature/` (leave originals in `user-docs/literature/` in place per copy-not-move strategy, until confirmed safe to clean up). |
| `03_thesis_modelling/notebooks/` — stale? | Still deferred — out of scope for P0028, flagged for a future session. |

All Phase 3 open items are now resolved. No blockers remain for Phase 4 planning. See `findings.md` for the raw grep/read evidence.

---

## Phases

### Phase 1: Audit & Planning ✅ DONE
- [x] Identify all hardcoded paths in 8 scripts (now: applies to the 12 scripts moving into `model_training/` + `forecast_service.py`)
- [x] Audit `PATHS.py` for missing tier definitions
- [x] Document folder structure audit (bloat, legacy, naming issues) — see FOLDER_STRUCTURE_AUDIT.md (scratchpad)
- [x] Trace origin of root `results/` and `reports/` — confirmed Enrico, see Decision Log #7
- [x] 3 rounds of tree critique with user — final structure locked (Decision Log)
- [x] User's own pruning pass: `utility_scripts/` created, `.claude/plans` deleted, `.obsidian` etc. deleted

**Output**: This plan document (rewritten), findings.md, progress.md.

---

### Phase 2: Update PATHS.py (New Tiers + Helper Functions)
**Objective**: Centralize every new path so nothing in Phase 3 needs to hardcode a folder string.

**Tasks**:
1. Update `THESIS_DIR` — remove the `thesis/` segment: `THESIS_DIR: Path = ROOT_DIR` (or deprecate the constant name entirely if cleaner — decide during implementation whether keeping `THESIS_DIR` as an alias for `ROOT_DIR` causes confusion vs. just inlining `ROOT_DIR` everywhere downstream).
2. Add new tier-root constants:
   - `THESIS_CONTEXT_DIR` = `ROOT_DIR / "00_thesis_context"`
   - `THESIS_RESEARCH_DIR` = `ROOT_DIR / "01_thesis_research"`
   - `THESIS_RESEARCH_QUESTIONS_DIR` = `THESIS_RESEARCH_DIR / "research-questions"`
   - `THESIS_RESEARCH_LITERATURE_DIR` = `THESIS_RESEARCH_DIR / "literature"`
   - `THESIS_DATA_DIR` = `ROOT_DIR / "02_thesis_data"` (rename from old `THESIS_DIR / "data"`)
   - `THESIS_MODELLING_DIR` = `ROOT_DIR / "03_thesis_modelling"` (rename)
   - `THESIS_MODELLING_TRAINING_DIR` = `THESIS_MODELLING_DIR / "model_training"` (NEW)
   - `THESIS_MODELLING_SERVING_DIR` = `THESIS_MODELLING_DIR / "model_serving"` (NEW)
   - `THESIS_MODELLING_SERVING_SYSTEM_A_DIR` = `THESIS_MODELLING_SERVING_DIR / "system_a_forecast"` (NEW)
   - `THESIS_MODELLING_SERVING_SYSTEM_B_DIR` = `THESIS_MODELLING_SERVING_DIR / "system_b_conversational"` (NEW)
   - `THESIS_RESULTS_DIR` = `ROOT_DIR / "04_thesis_results"` (renumbered from earlier draft's 05)
   - `THESIS_RESULTS_SRQ1_DIR` = `THESIS_RESULTS_DIR / "srq1"`
   - `THESIS_RESULTS_SRQ2_DIR` = `THESIS_RESULTS_DIR / "srq2"`
   - `THESIS_RESULTS_SRQ4_DIR` = `THESIS_RESULTS_DIR / "srq4"` (placeholder)
   - `THESIS_WRITING_DIR` = `ROOT_DIR / "05_thesis_writing"` (renumbered, rename from old `thesis-writing`)

3. Add data tier 4 split constants (as before, just re-parented under new `THESIS_DATA_DIR`):
   - `THESIS_DATA_ENGINEERED_BYMONTH_DIR` = `THESIS_DATA_ENGINEERED_DIR / "bymonth"`
   - `THESIS_DATA_ENGINEERED_BYCHAIN_DIR` = `THESIS_DATA_ENGINEERED_DIR / "bychain"`

4. Add helper functions (non-breaking additions):
   - `get_category_engineered_bymonth_dir(category)` → `bymonth/{category}/`
   - `get_category_engineered_bychain_dir(category)` → `bychain/{category}/`
   - Decide: deprecate old `get_category_engineered_dir()` (pointed at `_03_engineered/nielsen/{category}/`, a path shape that no longer exists post-flatten) or repoint it — do NOT leave it silently pointing at a dead path.

5. Update all existing docstrings/examples in PATHS.py that reference `C:\\dev\\thesis-manifold\\thesis\\...` — every example path loses the `thesis\` segment.

6. Verify: `python3 -c "from PATHS import ROOT_DIR, THESIS_DATA_DIR, THESIS_RESULTS_SRQ1_DIR; print(ROOT_DIR, THESIS_DATA_DIR, THESIS_RESULTS_SRQ1_DIR)"` — paths print correctly even before folders physically exist (Path objects don't require the target to exist).

**Files changed**: `PATHS.py` only.

**Estimated time**: 1 hour (grew from 45 min — more constants than originally scoped).

---

### Phase 3: Resolve Open Items + Update Scripts to Use PATHS.py
**Objective**: Close the 4 open items above, then update every script that will move (12 model_training scripts + forecast_service.py + generate_figures.py + generate_systemB_diagram.py) to import from PATHS.py instead of hardcoding folder strings.

**Tasks**:
1. **Resolve open items first** (grep-based, ~20 min):
   - `grep -rn "ml_retraining" --include="*.py" --include="*.ipynb"` across the repo — if zero live references outside itself, recommend archive (same treatment as root `results/`); if referenced, keep in place and note why.
   - Read `test_agent_system_comprehensive.py` and `test_group.py` — identify what they actually test; decide archive vs. keep in `utility_scripts/tests/`.
   - `ls user-docs/literature/` — if any `.bib`/`.json`/data files present, flag for move to `01_thesis_research/literature/` in Phase 4.

2. **Update the 12 model_training scripts + forecast_service.py** — replace hardcoded `_03_engineered_dvhexclhd`, `_04_engineered_bychain`, `_05_results_srq1`, `_06_results_srq2` strings with the new PATHS.py constants/functions from Phase 2.

3. **Verification**:
   - `grep -rn "_03_engineered_dvhexclhd\|_04_engineered_bychain\|_05_results\|_06_results\|_07_forecast" utility_scripts/ 03_thesis_modelling/ 04_thesis_results/ 2>/dev/null` → should find nothing once done (note: these scripts haven't moved yet at this point in the phase order — grep them in their CURRENT location `utility_scripts/scripts/`).
   - `python3 -m py_compile` on each updated script.

**Files changed**: ~14 scripts (imports/path logic only, no behavior changes).

**Estimated time**: 2 hours (grew from 1.5 hr — open-item resolution + 6 more scripts than original 8).

---

### Phase 4: Execute the Folder Moves
**Objective**: Physically restructure the repo per the locked target tree. This is the big one — do it in one sitting, verify after every major step, don't leave the repo half-moved between sessions.

**Order matters. Move code/scripts to their new homes BEFORE renaming their old parent folders out from under them.**

1. **Move thesis-pipeline scripts out of `utility_scripts/` first** (while PATHS.py already knows the destinations from Phase 2):
   ```bash
   mkdir -p 03_thesis_modelling/model_training
   mkdir -p 03_thesis_modelling/model_serving/system_a_forecast
   mkdir -p 03_thesis_modelling/model_serving/system_b_conversational
   mkdir -p 04_thesis_results

   git mv utility_scripts/scripts/srq1_baselines_stat.py   03_thesis_modelling/model_training/
   git mv utility_scripts/scripts/srq1_benchmark.py         03_thesis_modelling/model_training/
   git mv utility_scripts/scripts/srq1_benchmark_tuned.py   03_thesis_modelling/model_training/
   git mv utility_scripts/scripts/srq1_calibration.py       03_thesis_modelling/model_training/
   git mv utility_scripts/scripts/srq1_profiling.py         03_thesis_modelling/model_training/
   git mv utility_scripts/scripts/srq1_shap.py              03_thesis_modelling/model_training/
   git mv utility_scripts/scripts/srq2_agent.py             03_thesis_modelling/model_training/
   git mv utility_scripts/scripts/srq2_synthesis.py         03_thesis_modelling/model_training/
   git mv utility_scripts/scripts/srq4_experiment.py        03_thesis_modelling/model_training/
   git mv utility_scripts/scripts/srq4_tier2.py             03_thesis_modelling/model_training/

   git mv utility_scripts/scripts/forecast_service.py       03_thesis_modelling/model_serving/system_a_forecast/
   git mv utility_scripts/scripts/generate_systemB_diagram.py 03_thesis_modelling/model_serving/system_b_conversational/
   git mv utility_scripts/scripts/generate_figures.py       04_thesis_results/
   git mv utility_scripts/scripts/METADATA.py               02_thesis_data/   # 02_thesis_data doesn't exist yet at this sub-step order — see note below
   ```
   **Note**: `METADATA.py`'s destination (`02_thesis_data/`) doesn't exist until step 3 renames `thesis/data/` — either do step 3 first, or `git mv` into a path that will shortly be renamed (git tracks the rename fine either order, but do it in an order that never leaves a dangling reference mid-phase). Recommend: do the top-level `thesis/*` renames (step 3 below) FIRST, then come back and do this script-relocation step. Revise execution order at implementation time: **step 3 → step 1 → step 2 → step 4 → step 5**.

2. **Resolve open items from Phase 3** (archive/move ml_retraining and the two ambiguous test files per what was decided).

3. **Rename+flatten top-level `thesis/*` folders to root, dropping the `thesis/` segment**:
   ```bash
   git mv thesis/thesis-context   00_thesis_context
   git mv thesis/literature       01_thesis_research
   git mv thesis/data             02_thesis_data
   git mv thesis/modelling        03_thesis_modelling
   git mv thesis/thesis-writing   05_thesis_writing

   # RQs move from context into research (Decision Log #1)
   git mv 00_thesis_context/research-questions   01_thesis_research/research-questions
   ```

4. **Data tier flatten** (inside `02_thesis_data/`):
   ```bash
   cd 02_thesis_data
   git mv _03_engineered_dvhexclhd  _03_engineered/bymonth
   git mv _04_engineered_bychain    _03_engineered/bychain
   cd ..
   ```

5. **Move results into the new tier**:
   ```bash
   git mv 02_thesis_data/_05_results_srq1  04_thesis_results/srq1
   git mv 02_thesis_data/_06_results_srq2  04_thesis_results/srq2
   mkdir 04_thesis_results/srq4   # placeholder, empty
   ```

6. **Archive**:
   ```bash
   mkdir -p .archive
   git mv thesis/thesis_agents          .archive/thesis_agents_preintegration
   git mv results                       .archive/enrico_legacy_results_2026-04
   git mv reports                       .archive/enrico_legacy_reports_2026-07
   ```

7. **Delete confirmed-dead legacy folders** (verify empty/superseded first, per original Phase 1 audit):
   ```bash
   rm -rf 02_thesis_data/{assessment,nielsen,preprocessing,spss_indeksdanmark}
   ```

8. **Remove the now-empty `thesis/` shell** once every subfolder has moved out.

**Verification after every numbered step above** (not just at the end):
- `git status` after each step — confirm only the expected moves appear, no surprise content loss
- `ls -la thesis/` should be empty (or gone) after step 8
- Final: `find . -maxdepth 1 -type d | sort` matches the locked target tree exactly

**Files affected**: ~150+ paths (moves only, no content changes).

**Estimated time**: 1.5 hours (grew from 30 min — root-level scope, not just `thesis/data/`, plus the ordering care needed).

---

### Phase 5: Update All Cross-References in Code + Docs
**Objective**: Every remaining hardcoded string reference to an old path (`thesis/data`, `thesis/modelling`, `thesis/thesis-writing`, `thesis/thesis-context`, `thesis/literature`, `scripts/srq1_*`, `utility_scripts/scripts/forecast_service.py`, etc.) gets found and fixed.

**Search targets**:
- `grep -rn "thesis/data\|thesis/modelling\|thesis/thesis-writing\|thesis/thesis-context\|thesis/literature\|thesis-context\|thesis_agents" --include="*.py" --include="*.md" --include="*.ipynb"`
- `grep -rn "utility_scripts/scripts/\(srq\|forecast_service\|generate_figures\|generate_systemB\|METADATA\)"` — catches anything that referenced the old utility_scripts location by string path rather than import
- `CLAUDE.md`, `user-docs/contributing/repository_map.md`, any architecture diagrams
- Notebook cells with hardcoded path strings (not just Python imports — check `.ipynb` JSON for string literals too)

**Verification**:
- `python3 -c "from PATHS import ROOT_DIR, THESIS_DATA_DIR, THESIS_MODELLING_TRAINING_DIR, THESIS_RESULTS_SRQ1_DIR, THESIS_RESEARCH_QUESTIONS_DIR; print('OK')"`
- Spot-check 3–4 moved scripts actually run (or at least `py_compile` cleanly) from their new location

**Files affected**: ~25–35 files (grew — root-level scope pulls in more docs/notebooks than the original `thesis/data`-only sweep).

**Estimated time**: 1.5 hours.

---

### Phase 6: Document the New Structure in PATHS.py + Lock via Rule
**Objective**: Make the final structure legible to future sessions (yours, Enrico's, or a fresh Claude instance) so this doesn't drift back into bloat.

**Tasks**:
1. Add a top-of-file structure map comment in `PATHS.py` mirroring the target tree in this plan's Context section.
2. Create `.claude/rules/repo-tier-structure.md` — the authoritative, locked structure reference. Should state explicitly:
   - The numbered tier order (00–05) and what belongs in each
   - The rule that produced `model_training/` vs `model_serving/` split (train vs. serve)
   - The rule that new SRQ results always go in `04_thesis_results/srq{N}/`, never a new numbered top-level tier
   - The rule that `utility_scripts/` is for tooling-that-helps-you-work-on-the-thesis only, never thesis-pipeline code
3. Update `CLAUDE.md` "Quick References" section — all paths in that file currently point at old locations.

**Files changed**: `PATHS.py`, new `.claude/rules/repo-tier-structure.md`, `CLAUDE.md`.

**Estimated time**: 45 min.

---

### Phase 7: Git Commit + Verification
**Objective**: Stage, review, and commit. Given the size of this change, commit in logical chunks rather than one giant commit — easier to review, easier to revert a single chunk if something breaks.

**Suggested commit sequence**:
1. `PATHS.py` additions (Phase 2) — standalone commit, purely additive, zero risk.
2. Script updates to use PATHS.py (Phase 3) — still in old locations at this point, so this commit is pure import-logic change.
3. The folder moves (Phase 4) — large commit, mostly renames; `git mv` preserves rename detection so `git log --follow` still works per-file afterward.
4. Cross-reference fixes (Phase 5).
5. Documentation + rule lock (Phase 6).

**Verification before each commit**:
- `git status` reviewed manually, not blindly `git add -A`
- `python3 -m py_compile` on every touched script
- Final full-tree check: `find . -maxdepth 1 -type d | sort` matches target

**Estimated time**: 1.5 hours (grew — 5 reviewed commits instead of 1).

---

### Phase 8: Update Broader Documentation
**Objective**: Anything outside PATHS.py/CLAUDE.md that still describes the old structure.

**Files to update**:
1. `user-docs/contributing/repository_map.md`
2. `README.md` (if it has a structure diagram)
3. Any handover docs that reference old paths (note: `docs/handover/2026-07-01_enrico-to-brian-merge-handover.md` already references `_03_engineered_dvhexclhd`-style paths from before this restructure — decide whether to retroactively edit historical handovers or leave them as a dated snapshot with a pointer to this plan for "what changed since")

**Estimated time**: 45 min.

---

## Known Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Scripts break after path changes | HIGH | py_compile + spot-run every touched script before each commit (Phase 7) |
| Folder move corrupts git history / loses rename detection | MEDIUM | Use `git mv` throughout Phase 4, not raw `mv` + `git add` |
| Cross-references become stale (docs, notebooks) | MEDIUM | Dedicated Phase 5 grep sweep across `.py`/`.md`/`.ipynb`, not just scripts |
| `METADATA.py` move ordering creates a dangling path mid-phase | LOW | Explicit note in Phase 4 step 1 — do folder renames before script relocation into data tier |
| Open items (ml_retraining, ambiguous tests, user-docs/literature) get moved before being understood | MEDIUM | Phase 3 explicitly resolves these BEFORE Phase 4 executes any moves |
| Structure drifts back into bloat after P0028 closes | MEDIUM | `.claude/rules/repo-tier-structure.md` (Phase 6) — explicit rule against ad-hoc new top-level tiers |
| Historical handover docs now describe a structure that no longer exists | LOW | Explicit decision point in Phase 8 — likely leave as dated snapshot, don't rewrite history |

---

## Success Criteria

- [ ] Phase 1: ✅ Audit + 3 rounds of tree critique complete, structure locked
- [ ] Phase 2: PATHS.py has all new tier constants + helper functions; imports work pre-move
- [ ] Phase 3: Open items resolved; all 14 scripts use PATHS.py, zero hardcoded old-style paths remain
- [ ] Phase 4: Full target tree exists; `thesis/` shell removed; `git status` clean; no content loss
- [ ] Phase 5: No broken cross-references anywhere in `.py`/`.md`/`.ipynb`
- [ ] Phase 6: `.claude/rules/repo-tier-structure.md` exists and is authoritative; CLAUDE.md updated
- [ ] Phase 7: 5 reviewed commits, each independently sane; final selftest passes
- [ ] Phase 8: All broader docs reflect new structure or explicitly note they're historical snapshots

---

## Dependencies

- User confirms folder reorganization plan — ✅ DONE, 3 rounds of critique concluded, structure locked this session
- PATHS.py modifications reviewed (Phase 2)
- Open items resolved before any physical move (Phase 3 gate on Phase 4)
- Git safe to move folders (Phase 4) — no uncommitted work should be lost; run `git status` before starting Phase 4 in the execution session

---

## Notes for Future Sessions

- **P0028 is purely structural** — no logic changes, no re-running of SRQ1–4 results, no thesis content edits.
- Enrico's actual research output (results, chapters, harness code) is untouched in content — only its address in the filesystem changes.
- After P0028 closes, next priorities (per user's stated project priorities, tracked separately): region-grain WMAPE test, Ch4 EDA extensions for danskvand/energidrikke/RTD (see P0027).
- Any new SRQ3/5 results in the future go to `04_thesis_results/srq{N}/` — never a new numbered top-level tier. This is the whole point of Phase 6's rule lock.
- If `03_thesis_modelling/notebooks/` turns out to be stale on inspection, that's a separate future plan, not part of P0028.

---

**Last updated**: 2026-07-10 19:30
**Status**: In progress — Phase 1 + tree design ✅ complete. Phase 2 (PATHS.py) starts next, immediately after this update, before context compaction.
