# P0028 Findings — Thesis Restructure + Enrico Integration

## Session 6 — Phase 4 Execution Discoveries (2026-07-10 21:00–21:45)

Things found during the physical copy that weren't anticipated in the locked tree, and are NOT yet resolved:

### 1. Root-level `integrations/` folder — unaccounted for, not touched
`Z:/_dev-ssd/thesis-manifold/integrations/` contains `__init__.py` and `google_drive_integration.py`. This duplicates `utility_scripts/src/google_drive_integration.py` (the copy already accounted for in the locked tree as real tooling). Not in the original plan's audit. **Not moved, archived, or deleted — needs a decision next session**: almost certainly a stray duplicate safe to delete, but should diff the two files first to confirm they're identical before removing either.

### 2. `00_thesis_context/` has 2 subfolders not in the locked tree diagram
`thesis/thesis-context/` contained `methodology/` and `prometheus-integration/` in addition to the documented `formal-requirements/` and `thesis-topic/`. Both were copied as-is into `00_thesis_context/` since they're clearly context-tier content, but the task_plan.md target tree diagram doesn't list them. **Cosmetic gap only** — no action needed, just noting the diagram is incomplete vs. what's actually on disk now.

### 3. Literature version conflict — resolved with a dated dual-copy, needs manual reconciliation
`user-docs/literature/{bibtex.bib,citations.json}` (dated 2026-06-30, 28 citations) is NOT a duplicate of `thesis/literature/{bibtex.bib,citations.json}` (dated 2026-07-10, 25 citations, likely a curated trim) — they genuinely differ. Per user's direction, both now live in `01_thesis_research/literature/`:
- `bibtex.bib` / `citations.json` — the Jul 10 (newer, trimmed) version, treated as current
- `2026-06-30_bibtex.bib` / `2026-06-30_citations.json` — the Jun 30 version, kept for reference

**Not yet done**: nobody has actually reconciled WHY they differ (3 extra citations in the older file — were they cut deliberately, or lost accidentally?). This needs a manual diff/review, not a Claude decision — flagging for the user.

### 4. Stray old-shape engineered data left in place inside the new `_03_engineered/`
When `_03_engineered/` was copied wholesale from `thesis/data/_03_engineered/`, it brought along a `nielsen/{CSD,Danskvand,Energidrikke,RTD}/` subfolder with REAL feature matrices (not empty scaffolding, contrary to the original plan's assumption). This now sits inside `02_thesis_data/_03_engineered/` as a third sibling next to the intended `bymonth/` and `bychain/` folders. Per user's direction: **left in place, not archived**. This is technically off-plan (the locked tree only shows `bymonth/` and `bychain/` as children of `_03_engineered/`) — worth a note in Phase 6's structure-lock rule so a future session doesn't assume `nielsen/` is stray bloat and delete it without checking.

### 5. Uncommitted repo-wide state predates this session — confirmed safe, not touched
`git status --short` at the start of Phase 4 showed 232 changed paths (192 deletions, 34 modifications, 6 untracked). Traced and confirmed: this is entirely the user's own earlier pruning pass (deleting `.obsidian/`, renaming `docs/` → `user-docs/`, moving `scripts/`/`src/`/`tests/` → `utility_scripts/` via raw filesystem move rather than `git mv`, which is why git shows delete+untracked-add pairs instead of renames). None of it was caused by this session. Not staged, not committed, not touched — purely a pre-flight sanity check.

### 6. Scripts had a pre-existing off-by-one path bug, fixed as a side effect of the PATHS.py migration
Several of the 12 relocated scripts (`srq1_benchmark.py`, `srq1_benchmark_tuned.py`, etc.) had `ROOT = Path(__file__).resolve().parents[1]`, which resolves to `utility_scripts/` (one level too shallow) rather than repo root, even in their PRE-restructure location. Their hardcoded `thesis/data/...` string construction was therefore already broken before P0028 touched anything. Replacing this with a `PATHS.py` import (which is self-relative to wherever `PATHS.py` lives) fixes the bug as a side effect rather than propagating it into the new locations.

---

## Session 5 — Open Items Resolution (2026-07-10 20:15)

Ran the 3 open-item checks specified in task_plan.md Phase 3 gate:

**`ml_retraining` grep**: `grep -rln "ml_retraining" --include="*.py" --include="*.ipynb" .` from repo root returned 12 files, all inside `utility_scripts/scripts/ml_retraining/` itself:
```
./utility_scripts/scripts/ml_retraining/00_setup.py
./utility_scripts/scripts/ml_retraining/01_ingest_raw.py
./utility_scripts/scripts/ml_retraining/02_data_cleaning.py
./utility_scripts/scripts/ml_retraining/03_eda.py
./utility_scripts/scripts/ml_retraining/04_feature_engineering.py
./utility_scripts/scripts/ml_retraining/05_split.py
./utility_scripts/scripts/ml_retraining/06_preprocessing_pipeline.py
./utility_scripts/scripts/ml_retraining/07_baselines.py
./utility_scripts/scripts/ml_retraining/08_advanced_models.py
./utility_scripts/scripts/ml_retraining/09_shap_explain.py
./utility_scripts/scripts/ml_retraining/10_publication_figures.py
./utility_scripts/scripts/ml_retraining/__init__.py
```
No file outside this folder references it. Confirmed dead/superseded code (April ML retrain pass, same era as archived root `results/phase1`). Decision: archive, not delete — consistent with the root `results/`/`reports/` precedent (Decision Log #7).

**`test_agent_system_comprehensive.py`**: Read in full. Header comment: "Validates that Enrico's original LangGraph research framework still works." Imports `from thesis.ai_research_framework.core.coordinator import build_research_graph` and `from thesis.ai_research_framework.state.research_state import ResearchState` — both part of the pre-integration System A skeleton that lives in `thesis_agents/` (already archived to `.archive/thesis_agents_preintegration/`). This test exercises archived code, so it moves there too rather than remaining in active `utility_scripts/tests/`.

**`test_group.py`**: Read in full. Straightforward live Zotero group-library connectivity smoke test — loads `ZOTERO_GROUP_ID`/`ZOTERO_API_KEY` from `.env`, connects via `pyzotero.Zotero`, lists items. Genuine active tooling, no ambiguity. Stays in `utility_scripts/scripts/`.

**`user-docs/literature/`**: `ls -la` shows exactly two files: `bibtex.bib` (54,469 bytes) and `citations.json` (57,626 bytes) — both working data, not prose/docs. This is the exact mistake previously flagged in Enrico's handover (working data living in a user-facing docs folder). Both files move to `01_thesis_research/literature/` in Phase 4.

All resolutions also recorded in task_plan.md's Open Items table.

---

## Key Discoveries

### 1. Hardcoded Paths (8 scripts, 100% recoverable)
All found via `grep -r "_03_engineered_dvhexclhd\|_04_engineered_bychain\|_05_results"`:

| Script | Hardcoded Paths | Fix | Priority |
|--------|-----------------|-----|----------|
| `scripts/srq1_benchmark.py` | `_03_engineered_dvhexclhd`, `_04_engineered_bychain` | Use `get_category_engineered_bymonth_dir()`, `get_category_engineered_bychain_dir()` | P0 |
| `scripts/srq1_benchmark_tuned.py` | Same as above | Same fix | P0 |
| `scripts/srq1_baselines_stat.py` | `_03_engineered_dvhexclhd` | Same bymonth fix | P0 |
| `scripts/srq1_calibration.py` | `_03_engineered_dvhexclhd` | Same bymonth fix | P0 |
| `scripts/forecast_service.py` | `_03_engineered_dvhexclhd`, `_04_engineered_bychain` | Use new constants + helper functions | P0 |
| `scripts/srq2_synthesis.py` | `_05_results_srq1` | Use `THESIS_RESULTS_SRQ1_DIR` | P0 |
| `scripts/srq4_tier2.py` | `_05_results_srq1`, `_06_results_srq2` | Use `THESIS_RESULTS_SRQ1_DIR`, `THESIS_RESULTS_SRQ2_DIR` | P0 |
| `scripts/srq4_experiment.py` | Same as srq4_tier2 | Same fix | P0 |

**Impact if not fixed**: Any folder reorganization breaks all 8 scripts; scripts become "brittle" to future structure changes.

---

### 2. PATHS.py Coverage Gap
Existing PATHS.py has:
- ✅ `THESIS_DATA_RAW_DIR`, `THESIS_DATA_CONVERTED_DIR`, `THESIS_DATA_PREPROCESSING_DIR`
- ✅ `THESIS_DATA_ENGINEERED_DIR` (points to `_03_engineered/`)
- ✅ `get_category_engineered_dir()` (returns `_03_engineered/nielsen/{cat}/`)
- ❌ No `THESIS_DATA_ENGINEERED_BYMONTH_DIR`, `THESIS_DATA_ENGINEERED_BYCHAIN_DIR`
- ❌ No `THESIS_RESULTS_DIR`, `THESIS_RESULTS_SRQ1_DIR`, `THESIS_RESULTS_SRQ2_DIR`
- ❌ No helper functions for new granularities

**Fix scope**: Add 7 constants + 2 helper functions (non-breaking, additive only).

---

### 3. Folder Structure Issues (Confirmed)

#### Bloat Tier Count
- Current: 7 top-level tiers under `thesis/data/`
  - `_00_raw`, `_01_converted`, `_02_preprocessing`, `_03_engineered` (mostly empty)
  - `_03_engineered_dvhexclhd`, `_04_engineered_bychain` (new, confusing names)
  - Separate: `_05_results_srq1`, `_06_results_srq2`, `_07_forecast_service` (not in thesis/data — floating)
- Target: 4 tiers + 1 results parent
  - `_00_raw`, `_01_converted`, `_02_preprocessing`, `_03_engineered/` (with sub-granularities)
  - `05_thesis_results/` (parent, outside data/)

#### Legacy Folders (Redundant)
| Folder | Status | Action |
|--------|--------|--------|
| `thesis/data/assessment/` | Pre-restructure, unused | Delete |
| `thesis/data/nielsen/` | Superseded by `_00_raw/nielsen/` | Delete |
| `thesis/data/preprocessing/` | Superseded by `_02_preprocessing/` | Delete |
| `thesis/data/spss_indeksdanmark/` | Superseded by `_00_raw/spss_indeksdanmark/` | Delete |

#### Thesis Folder (No Numbering)
Current:
```
thesis/
├─ .obsidian/          ← deleted by user
├─ data/               ← will rename to 02_thesis_data
├─ literature/         ← will rename to 01_thesis_literature
├─ modelling/          ← will rename to 03_thesis_modelling
├─ thesis_agents/      ← will move to .archive/ (pre-integration)
├─ thesis-context/     ← will rename to 00_thesis_context
├─ thesis-writing/     ← will restructure + rename to 04_thesis_writing
├─ _claude-brain/      ← deleted by user
├─ INDEX.md            ← deleted by user
└─ Untitled.canvas     ← deleted by user
```

Target:
```
thesis/
├─ 00_thesis_context/
├─ 01_thesis_literature/
├─ 02_thesis_data/
├─ 03_thesis_modelling/
├─ 04_thesis_writing/
│  ├─ 01_writing_agents/       (NEW — LLM conversational layer)
│  └─ 02_writing_results/      (current thesis-writing content)
├─ 05_thesis_results/           (NEW — SRQ1–4 outputs)
└─ .archive/
   └─ thesis_agents_preintegration/
```

---

### 4. The "Writing Agents" Confusion
User asked: "Do we have a folder for langchain/langgraph/chatGPT creation?"

**Current state**: No dedicated folder. System A/B agents currently live in `thesis/thesis_agents/` (will be archived).

**User's vision**: 
- `04_thesis_writing/01_writing_agents/` should hold LLM-as-conversational-agent code
  - This is **NOT** the same as System A/B agents (those are research harnesses for SRQ4)
  - This is the **Prometheus bridge** — code to make trained models available to a conversational LLM (GPT for now, Prometheus later)

**Status**: Placeholder folder created in Phase 4; code to be written after Prometheus access is gained or GPT fallback is ready.

---

### 5. Results Tier Rationale
User asked: "Should results live in modelling/ or have their own tier?"

**Analysis**:

| Option | Pros | Cons |
|--------|------|------|
| **modelling/** | Closer to model code; "generation" flows downward | Mixes training code with outputs; hard to scale (SRQ3/4 results pile up) |
| **05_thesis_results/** (separate) | Clean separation of concerns; scales to N SRQs; answers RQs (not just ML) | Slight distance from model code; requires cross-tier imports |

**Recommendation**: Separate tier (05_thesis_results/) wins because:
- Results answer research questions (RQ1, RQ2, RQ4) — not just model artifacts
- Results often combine insights from multiple models + literature + synthesis
- SRQ3/4/5 results would add to the same tier without folder explosion
- Clean for publication: grab `05_thesis_results/srq{1-4}/` for figures + tables

**Decision**: Implemented in Phase 4. System A/B agents (research harnesses, not conversational) stay archived.

---

### 6. Enrico's Work Integration
All Enrico's changes are **already in main** (commit 63a424d). Restructure is **orthogonal** — we're just reorganizing where his outputs live, not re-running anything.

| Component | Status | Location (Before) | Location (After) |
|-----------|--------|-------------------|------------------|
| SRQ1 results | ✅ Done, committed | `_05_results_srq1/` | `05_thesis_results/srq1/` |
| SRQ2 results | ✅ Done, committed | `_06_results_srq2/` | `05_thesis_results/srq2/` |
| SRQ4 harness | ✅ Harness built, demo run | `thesis/scripts/srq4_*` | Same (no move) |
| Chapters 1–10 | ✅ Drafted | `thesis-writing/` | `04_thesis_writing/02_writing_results/` |
| System A/B agents | ✅ Skeletal | `thesis/thesis_agents/` | `.archive/thesis_agents_preintegration/` |

No re-running, no re-validation. Pure reorganization.

---

### 7. Git Implications
- **Folder moves**: Use `git mv` (preserves history) or careful `git add` after moves
- **Scripts changed**: 8 files, all import-only (no logic changes)
- **PATHS.py**: Additive only (new constants + functions)
- **Commit size**: Medium (100+ paths moved, 8 scripts updated, ~10 doc updates)
- **Risk**: Low (moving, not deleting; testing before commit)

**Recommendation**: Single commit per phase to avoid confusion; don't squash. History should show: (1) PATHS.py additions, (2) script updates, (3) folder reorganization, (4) doc updates, (5) rules added.

---

### 8. Path Centralization Best Practices (Discovered)
Enrico created good structure but forgot the PATHS.py binding. Going forward:

**Rule**: Any new tier, any new results folder → **update PATHS.py first**, then use the constant/function in scripts.

**Prevention**: Add to `.claude/rules/data-tier-structure.md`:
- Define all tiers in one place (PATHS.py)
- Forbid hardcoded paths in scripts
- CI check: `grep -r "thesis/data/_0[0-9]" scripts/` should find nothing (only valid references like `from PATHS import ...`)

---

## Decision Log

| Decision | Rationale | Owner | Date |
|----------|-----------|-------|------|
| Move results out of `thesis/data/` | Results are outputs, not data; cleaner separation | Brian | 2026-07-10 |
| Rename `_03_engineered_dvhexclhd` → `_03_engineered/bymonth` | Clearer naming; groups related granularities | Brian | 2026-07-10 |
| Create `04_thesis_writing/01_writing_agents/` | Placeholder for Prometheus bridge code (GPT fallback for now) | Brian | 2026-07-10 |
| Archive `thesis_agents/` (don't delete) | Pre-integration state; may need for reference | Brian | 2026-07-10 |
| 8-phase rollout with testing per phase | Reduce risk of breaking scripts; verify each step | Claude + Brian | 2026-07-10 |

---

## External References

- **Folder audit**: `C:\Users\brian\AppData\Local\Temp\claude\...\FOLDER_STRUCTURE_AUDIT.md`
- **Handover (updated)**: `docs/handover/2026-07-01_enrico-to-brian-merge-handover.md`
- **Merge review**: `C:\Users\brian\AppData\Local\Temp\claude\...\ENRICO_MERGE_REVIEW.md`
- **Git commit count** (affected): 14 scripts + PATHS.py + docs + full-repo folder moves (grew from original 8-script/`thesis/data`-only scope — see Round 2/3 section below)

---

## Round 2/3 Findings — Scope Expansion to Full Repo Root

Everything above this section was written when scope was `thesis/data/` tiers only. User's own pruning pass + 3 rounds of tree critique expanded scope to the entire repo root. This section captures what changed and why; `task_plan.md` Context section is the authoritative current-state reference — this is the discovery trail behind it.

### Root-level slop traced and confirmed

| Folder | Origin (git blame) | What it is | Verdict |
|--------|---------------------|------------|---------|
| `results/` | Enrico, commit `368a967`, 2026-04-13 | Old April ML-retraining pass: `ml_retrain_2026-04-16/` (COMPARISON.md, MANIFEST.json, cleaning/ingestion/feature-eng reports), `phase1/` (preprocessing_report.md), `seaborn_exploratory/` (3 PNGs, no code alongside) | Archive (user overrode "delete" recommendation) → `.archive/enrico_legacy_results_2026-04/` |
| `reports/` | Enrico, commit `ec350d0`, 2026-07-08 (pre-merge working-tree commit) | Draft EDA/SHAP/final report set: `eda/` (6 PNGs + index.html), `shap/` (3 PNGs + index.html), `final/` (4 PNGs) — un-versioned precursor to what's now the proper `_05_results_srq1/figures/` | Archive → `.archive/enrico_legacy_reports_2026-07/` |

Neither folder is referenced by any current script (dates alone confirm — both pre-date the July SRQ1–4 rewrite that superseded them).

### `utility_scripts/` audit — the real split

User moved former root `scripts/`, `src/`, `tests/` into `utility_scripts/` and asked Claude to sort what's actually tooling vs. thesis-pipeline code, using the test: *does this script help you work ON the thesis, or IS it the thesis pipeline?*

Full inventory of `utility_scripts/scripts/` (25 files) sorted by verdict:

**Real tooling (stays)**: `dynamically_find_root_directory.py`, `gdrive_citation_matcher.py`, `notebooklm_ingestion.py`, `set_all_citation_keys.py`, `unified_sync_check.py`, `zotero_client.py`, `zotero_gdrive_filename_validator.py`, `zotero_sync_phase1.py`, plus `test_group.py` (ambiguous, see Open Items).

**Thesis-pipeline code (moves out)**: `srq1_baselines_stat.py`, `srq1_benchmark.py`, `srq1_benchmark_tuned.py`, `srq1_calibration.py`, `srq1_figures.py`, `srq1_profiling.py`, `srq1_shap.py`, `srq2_agent.py`, `srq2_synthesis.py`, `srq4_experiment.py`, `srq4_tier2.py` → `03_thesis_modelling/model_training/`. Plus `forecast_service.py` → `model_serving/system_a_forecast/`, `generate_systemB_diagram.py` → `model_serving/system_b_conversational/`, `generate_figures.py` → `04_thesis_results/` (runs after training, writes result figures — not training code itself), `METADATA.py` → `02_thesis_data/` (Nielsen schema reference, data documentation not modelling code).

`utility_scripts/src/google_drive_integration.py` and the 4 files in `utility_scripts/tests/` were also reviewed — `test_agent_system_comprehensive.py` and `test_group.py` have ambiguous names (testing the archived pre-integration `thesis_agents/`? testing something else?) and are logged as Open Items rather than guessed at.

### Naming decision: `model_serving` settled over 2 alternatives

User asked Claude to choose between `serving` / `sharing` / `accessibility` for the folder housing `forecast_service.py` (System A) and the future conversational-LLM bridge (System B). Reasoning for `model_serving`:
- Standard ML-engineering term, pairs with `model_training/` as a recognized train→serve pipeline split
- Directly names the thesis's own core comparison (two model-serving strategies: dedicated model vs. code-as-action LLM) — reinforces the RQ vocabulary rather than being generic
- `accessibility` rejected: collides with disability/UX accessibility as an established term of art, would confuse readers
- `sharing` rejected: too vague (file sharing? weight sharing? results sharing? unclear which)

### Tier reordering: writing moved from position 4 to position 5 (last)

Original draft plan put `04_thesis_writing` before `05_thesis_results`. User caught this: writing is the *last* consumer in the pipeline (it depends on context + research + data + modelling + results), so it can't be numbered before its last upstream dependency exists. Reordered: context(00) → research(01) → data(02) → modelling(03) → results(04) → writing(05).

This reordering is also why the earlier plan draft's `04_thesis_writing/01_writing_agents/` placeholder (for the Prometheus/GPT bridge) was wrong — that component isn't writing-adjacent at all, it's a *serving* concern, which is what led to the `model_serving/system_b_conversational/` placement instead.

### `01_thesis_literature` → `01_thesis_research`, and RQs move in

Once research questions were identified as belonging in this tier (not in `00_thesis_context`, which now holds only hard requirements + topic overview), "literature" was too narrow a label for a tier holding both RQs and the lit corpus — hence the rename to "research", with `literature/` surviving as an internal subfolder.

### `.claude/plans` and `.agents`/`.codex` — resolved without action from Claude

`.claude/plans` was flagged as a possible second plan-tracking location (competing with `plans/`); user deleted it directly, no reconciliation work needed. `.agents/` and `.codex/` root folders were flagged as likely leftover scaffolding from a different AI tool, but user explicitly said to ignore them — out of scope for P0028, not investigated further.

---

## External References (Round 2/3 additions)

- **Origin trace commands used**: `git log --diff-filter=A --oneline --all -- "results/phase1"` and equivalent for `reports/eda` — both point to single-commit Enrico additions, confirmed via `git log -1 --format="%an <%ae>"` on each commit SHA.
- **`utility_scripts/` full listing**: captured via `ls utility_scripts/scripts/`, `ls utility_scripts/src/`, `ls utility_scripts/tests/` during this session — see task_plan.md target tree for the sorted result.

---

**Last updated**: 2026-07-10 19:30  
**Status**: Findings complete through 3 rounds of critique. Open items logged in task_plan.md must be resolved in Phase 3 before Phase 4 folder moves execute.
