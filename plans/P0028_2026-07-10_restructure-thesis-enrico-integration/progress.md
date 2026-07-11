# P0028 Progress Log

## 2026-07-10

### Session 1: Planning & Audit (Complete)

**Time**: 16:00–17:30 (90 min)

**What was done**:
1. ✅ Reviewed Enrico's merge (commit 63a424d, 10+ new commits, SRQ1–4 integrated)
2. ✅ Audited folder bloat: 7 data tiers, hardcoded paths in 8 scripts
3. ✅ Investigated `PATHS.py` — found tier 1–4 coverage, gaps at tier 5–6
4. ✅ Ran `grep -r "_03_engineered_dvhexclhd"` → confirmed all 8 scripts
5. ✅ User confirmed renaming + restructuring plan (via direct convo)
6. ✅ Created `task_plan.md` (8-phase rollout, 45 min–1.5 hr per phase)
7. ✅ Created `findings.md` (issue analysis, decision log, risk table)
8. ✅ Created this `progress.md`

**Decisions made**:
- Separate tier for results (05_thesis_results) — cleaner than living in modelling/
- Rename confusing tiers (`_03_engineered_dvhexclhd` → `_03_engineered/bymonth`)
- Archive (don't delete) thesis_agents for reference
- 8-phase approach with testing per phase (low-risk rollout)

**Blockers**: None. User fully aligned. Ready for Phase 2.

**Next**: Start Phase 2 (PATHS.py updates) in next session.

---

## Upcoming Phases

- **Phase 2** (~1 hr): Update PATHS.py with new tier constants + helpers
- **Phase 3** (~2 hr): Resolve open items (ml_retraining, ambiguous tests, user-docs/literature); update 14 scripts to use PATHS.py
- **Phase 4** (~1.5 hr): Execute full-repo folder moves (git mv, careful ordering)
- **Phase 5** (~1.5 hr): Update cross-references in code/docs/notebooks
- **Phase 6** (45 min): Document new tier structure in PATHS.py + lock via `.claude/rules/`
- **Phase 7** (~1.5 hr): Git commit in 5 reviewed chunks + verification
- **Phase 8** (45 min): Update broader docs (repository_map.md, README, handover notes)

**Estimated total**: ~9.5 hours (grew from original 6 hr — scope expanded from `thesis/data/`-only to full repo root across sessions 2–4)

---

## 2026-07-10

### Session 2–4: Tree Design & Critique (Complete)

**Time**: 17:30–19:30 (~2 hr, across 3 rounds of back-and-forth with user)

**What was done**:
1. ✅ User did their own pruning pass: deleted `.obsidian/`, `INDEX.md`, `Untitled.canvas`, `_claude-brain/`; created `utility_scripts/` and moved former root `scripts/`, `src/`, `tests/` into it; deleted `.claude/plans`
2. ✅ Traced root `results/` and `reports/` origin via git blame — both confirmed Enrico, both stale (April ML retrain, pre-merge draft reports)
3. ✅ Full inventory + sort of `utility_scripts/scripts/` (25 files) into tooling-stays vs. pipeline-code-moves
4. ✅ Round 1 critique: initial tree proposed (thesis/ prefix kept, writing before results, `01_thesis_literature`)
5. ✅ Round 2 critique: user disagreed on writing-tier position and literature naming; both corrected (writing → last, literature → research); `thesis/` flatten to root confirmed as the right call; `.archive` not delete for results/reports; began scripts/serving-layer discussion
6. ✅ Round 3 critique: resolved `model_serving` naming (vs. sharing/accessibility); resolved RQ move into research tier; user confirmed archive `.claude/plans` deleted, ignored `.agents`/`.codex`
7. ✅ Round 4 (this exchange): resolved final 2 placements (`generate_figures.py` → results tier, `generate_systemB_diagram.py` → system_b_conversational) — no unclarities remain
8. ✅ Rewrote `task_plan.md` wholesale (scope grew from `thesis/data/`-only to full repo root; phases 2–8 rewritten; Decision Log added; Open Items table added)
9. ✅ Appended Round 2/3 findings section to `findings.md` (kept original hardcoded-path table as valid background)
10. ✅ Updated this progress.md

**Decisions made** (full list in task_plan.md Decision Log):
- Tier order: context(00) → research(01) → data(02) → modelling(03) → results(04) → writing(05)
- `thesis/` segment removed entirely — everything flattens to repo root
- `model_training/` + `model_serving/` split inside modelling tier; `model_serving/system_a_forecast/` + `system_b_conversational/` (placeholder)
- Root `results/` + `reports/` → archived (not deleted) to `.archive/enrico_legacy_*`
- `utility_scripts/` trimmed to ~9-13 real tooling scripts; 14 thesis-pipeline scripts relocated
- `METADATA.py` → `02_thesis_data/`; `generate_figures.py` → `04_thesis_results/`; `generate_systemB_diagram.py` → `model_serving/system_b_conversational/`

**Open items NOT yet resolved** (logged in task_plan.md, to resolve at start of Phase 3):
- `utility_scripts/ml_retraining/` — move, archive, or delete? (needs grep for live references first)
- `test_agent_system_comprehensive.py`, `test_group.py` — unclear what they test; read before placing
- `user-docs/literature/` — check for stray `.bib`/`.json` files that repeat the Enrico mistake

**Blockers**: None. Tree design fully settled across 4 rounds. Ready for Phase 2.

**Next**: Compact context, then start Phase 2 (PATHS.py updates) in the execution session.

---

## Notes for Next Session

- Start with Phase 2 (PATHS.py edits — safest change, purely additive)
- Verify imports work with `python3 -c "from PATHS import ROOT_DIR, THESIS_DATA_DIR, THESIS_MODELLING_TRAINING_DIR, THESIS_RESULTS_SRQ1_DIR, THESIS_RESEARCH_QUESTIONS_DIR; print('OK')"` — paths print fine even before folders physically exist
- Resolve the 3 open items (Phase 3, top of phase) BEFORE any folder move — don't guess on ml_retraining/ambiguous tests/user-docs literature
- Do NOT move folders until Phase 3 scripts are tested and open items resolved
- Commit in 5 reviewed chunks per Phase 7, not one giant commit — easier to review/revert
- Watch for cross-references in notebooks (Phase 5) — check `.ipynb` JSON string literals, not just Python imports
- Order care in Phase 4 step 1: do the `thesis/*` top-level renames BEFORE relocating scripts into folders that don't exist yet under the old names (see task_plan.md note under Phase 4 step 1)

---

## Testing Checklist

- [ ] Phase 2: `python3 -c "from PATHS import ROOT_DIR, THESIS_RESULTS_SRQ1_DIR, THESIS_MODELLING_TRAINING_DIR; print('OK')"`
- [ ] Phase 3: `grep -rn "ml_retraining"` sweep; read the 2 ambiguous test files; `ls user-docs/literature/`; `python3 -m py_compile` on all 14 relocatable scripts
- [ ] Phase 4: `git status` after EVERY numbered step, not just at the end — confirm only expected moves
- [ ] Phase 5: `grep -rn "thesis/data\|thesis/modelling\|thesis-writing\|thesis-context"` finds nothing outside historical docs/handovers
- [ ] Phase 7: 5 separate reviewed commits; final selftest passes; `find . -maxdepth 1 -type d | sort` matches target tree exactly

---

**Sessions 1–4 complete (planning + full tree design)**: 2026-07-10 19:30. Ready to compact and begin execution (Phase 2) in next session.

---

## 2026-07-10 (continued)

### Session 5: Task Decomposition + Execution Strategy Change (Complete)

**Time**: 19:45–20:00

**What was done**:
1. ✅ Ran `/task-decomposition` on Phase 2 + Phase 3 — produced 10 atomic tasks (T1–T10), persisted to `tasks/1.json` through `tasks/10.json`
2. ✅ User introduced a new constraint: to avoid interfering with other concurrent Claude Code sessions that may be reading old paths, Phase 4 folder operations change from `git mv` to **copy-and-defer-delete** — old paths stay in place until user confirms other sessions are done, then a follow-up cleanup pass removes the stale originals
3. ✅ Updated `task_plan.md` with an "Execution Strategy Note" documenting this change; noted it only affects Phase 4 (Phase 2/3 are purely additive and unaffected)
4. ✅ Confirmed native `TaskCreate`/`TaskList`/`TaskUpdate` tools are not available in this session's environment — the `tasks/*.json` files ARE the durable task record for this session, no in-memory duplicate exists

**Task breakdown persisted** (`tasks/` folder):
- T1: Add tier-root constants to PATHS.py (context/research/data/modelling/results/writing)
- T2: Add model_training/model_serving/results sub-constants
- T3: Add engineered bymonth/bychain constants + helpers, resolve `get_category_engineered_dir()`
- T4: Update PATHS.py docstrings + Phase 2 verification (blocked by T1–T3)
- T5: Resolve `ml_retraining` open item (grep-based)
- T6: Read ambiguous test files, decide placement
- T7: Check `user-docs/literature/` for stray data files
- T8: Update 6 `model_training` scripts (srq1_*) to use PATHS.py constants (blocked by T3)
- T9: Update srq2/srq4/forecast_service scripts (blocked by T2, T3)
- T10: Phase 3 verification sweep + progress.md update (blocked by T5–T9)

**Blockers**: None. Ready to execute T1 first.

**Next**: Execute T1 → T2/T3 (parallel-safe) → T4 → T5/T6/T7 (parallel-safe, independent of T1-T4) → T8/T9 (parallel-safe once T2/T3 done) → T10.

---

### Session 5 (continued): Full Phase 2 + Phase 3 Execution (Complete)

**Time**: 20:00–20:45

**T1-T4 (Phase 2, PATHS.py)** — all verified via direct Python import after each step:
- T1: Added `THESIS_CONTEXT_DIR`, `THESIS_RESEARCH_DIR` (+ `_QUESTIONS_DIR`/`_LITERATURE_DIR`), `THESIS_RESULTS_DIR`, `THESIS_WRITING_DIR`; renamed `THESIS_DATA_DIR` → `02_thesis_data`, `THESIS_MODELLING_DIR` → `03_thesis_modelling`; kept `THESIS_DIR` as a plain alias for `ROOT_DIR` (not removed) for backwards compat
- T2: Added `THESIS_MODELLING_TRAINING_DIR`, `THESIS_MODELLING_SERVING_DIR` (+ system_a/system_b sub-dirs), `THESIS_RESULTS_SRQ1_DIR`/`SRQ2_DIR`/`SRQ4_DIR`
- T3: Added `THESIS_DATA_ENGINEERED_BYMONTH_DIR`/`BYCHAIN_DIR` + `get_category_engineered_bymonth_dir()`/`bychain_dir()` helpers; repointed (not just deprecated) `get_category_engineered_dir()` to the bymonth helper so it never silently returns a dead path
- T4: Updated all stale `thesis\\...` docstring examples; expanded `print_all_paths()` to include every new constant
- Final Phase 2 verification: all 18 new/renamed constants import cleanly; `print_all_paths()` runs end-to-end and prints correct (pre-existence) paths

**T5-T7 (Phase 3, open items)** — all resolved, recorded in task_plan.md's Open Items table and findings.md:
- T5: `ml_retraining/` — grepped, zero external references, **decision: archive** (same treatment as root `results/`)
- T6: Read both ambiguous test files — `test_agent_system_comprehensive.py` tests the archived pre-integration `thesis_agents/` LangGraph skeleton (**decision: archive alongside it**); `test_group.py` is a live Zotero connectivity test (**decision: keep in utility_scripts/scripts/**)
- T7: `user-docs/literature/` contains `bibtex.bib` + `citations.json` — confirmed the Enrico working-data-in-docs mistake repeated (**decision: copy to `01_thesis_research/literature/` in Phase 4**)

**T8-T9 (Phase 3, script updates)** — **scope grew from the planned 11 scripts to 12** during execution:
- Updated all 6 planned `srq1_*` scripts (baselines_stat, benchmark, benchmark_tuned, calibration, profiling, shap) to import `get_category_engineered_bymonth_dir()`/`bychain_dir()` from PATHS.py
- **Discovered `srq1_figures.py`** had the same hardcoded pattern but wasn't in the original plan list — fixed it too
- Updated `srq2_agent.py`, `srq2_synthesis.py` (`THESIS_RESULTS_SRQ2_DIR` + tag-based engineered-dir dispatch), `srq4_experiment.py` (`THESIS_RESULTS_SRQ1_DIR`/`SRQ4_DIR` + tag dispatch, also fixed `forecast_service.py` import path since both live in the same current folder), `forecast_service.py` (`THESIS_RESULTS_SRQ1_DIR` + `THESIS_MODELLING_SERVING_SYSTEM_A_DIR` as its output dir, matching Decision Log #9's eventual placement)
- **Discovered `srq4_tier2.py`** also had a hardcoded `_08_results_srq4` path that the original plan's grep pattern (`_05_results|_06_results`) never would have caught — fixed it too, now uses `THESIS_RESULTS_SRQ4_DIR`
- Also updated stale docstring `Output:` lines in all 9 result-writing scripts to reference the new `04_thesis_results/srq{N}/` paths instead of old `_05_/_06_/_07_/_08_results*` strings
- **Bug fixed as a side effect**: several scripts had `ROOT = Path(__file__).resolve().parents[1]` which resolves to `utility_scripts/`, not repo root — meaning their hardcoded `thesis/data/...` path construction was already broken (off-by-one) even in the CURRENT unmoved location. The PATHS.py import approach sidesteps this entirely since `PATHS.py`'s own `ROOT_DIR` is self-relative to wherever `PATHS.py` lives.

**T10 (final verification)**:
- Combined grep sweep across all of `utility_scripts/scripts/` for every old-style path pattern (`_03_engineered_dvhexclhd`, `_04_engineered_bychain`, `_05_results`, `_06_results`, `_07_forecast`, `_08_results_srq4`) — zero matches
- `python3 -m py_compile` on all 12 touched scripts — all compile cleanly
- Updated `task_plan.md` frontmatter to reflect Phase 2+3 complete

**Blockers**: None. **Phase 2 and Phase 3 are both fully complete.**

**Next**: Phase 4 — physical folder restructure. Per the updated execution strategy (Execution Strategy Note in task_plan.md), this uses **copy, not git mv**: populate every new-tier location via copy while leaving old-location originals in place, deferring deletion until the user confirms other concurrent Claude Code sessions have finished. Should confirm with the user before starting Phase 4, since it's the first phase that touches the filesystem layout other sessions might be reading.

---

### Session 6: Phase 4 Execution — Physical Folder Copy (Complete)

**Time**: 21:00–21:45

**Pre-flight check**: `git status --short` showed 232 changed paths (192 deletions, 34 modifications, 6 untracked) — all pre-existing from the user's own earlier pruning pass (deleting `.obsidian/`, `docs/` → `user-docs/` rename, `scripts/`/`src/`/`tests/` → `utility_scripts/` move showing as delete+untracked-add since it wasn't done via `git mv`). Confirmed none of this was caused by this session; proceeded without touching any of it.

**Execution** (copy, not move — originals untouched everywhere):
1. `00_thesis_context/` ← `thesis/thesis-context/` (includes 2 subfolders not in the original plan tree: `methodology/`, `prometheus-integration/` — copied as-is)
2. `01_thesis_research/literature/` ← `thesis/literature/`; `01_thesis_research/research-questions/` ← `00_thesis_context/research-questions/` (moved per Decision Log #1, removed from context after copy)
3. `02_thesis_data/` ← `thesis/data/{_00_raw, _01_converted, _02_preprocessing, assessment, nielsen, preprocessing, spss_indeksdanmark, __init__.py}` — **_00_raw alone is 16GB**; full copy took several minutes, ran in background
4. `02_thesis_data/_03_engineered/{bymonth,bychain}/` ← `thesis/data/{_03_engineered_dvhexclhd, _04_engineered_bychain}/`
5. `04_thesis_results/{srq1,srq2}/` ← `thesis/data/{_05_results_srq1, _06_results_srq2}/`; `srq4/` created empty (placeholder, no results yet)
6. `03_thesis_modelling/{notebooks,prompts}/` ← `thesis/modelling/`; `03_thesis_modelling/model_training/` ← the 11 updated scripts from `utility_scripts/scripts/`; `model_serving/system_a_forecast/forecast_service.py` and `model_serving/system_b_conversational/generate_systemB_diagram.py` placed per Decision Log #9/#10/#13
7. `02_thesis_data/METADATA.py` and `04_thesis_results/generate_figures.py` copied per Decision Log #11/#12
8. `05_thesis_writing/` ← `thesis/thesis-writing/*` (skipped the Word `~$...docx` lock file — not real content)
9. `.archive/thesis_agents_preintegration/` ← `thesis/thesis_agents/` + the archived `test_agent_system_comprehensive.py` (T6 resolution); `.archive/enrico_legacy_results_2026-04/` ← root `results/`; `.archive/enrico_legacy_reports_2026-07/` ← root `reports/`; `.archive/ml_retraining_2026-04/` ← `utility_scripts/scripts/ml_retraining/` (T5 resolution)

**Decisions made mid-execution** (user consulted via AskUserQuestion, both resolved):
- **Data-volume check**: flagged that `_00_raw` alone is 16GB before continuing the full data-tier copy (would roughly double disk usage). User confirmed: proceed with full copy anyway.
- **Literature version conflict**: `user-docs/literature/{bibtex.bib,citations.json}` (Jun 30, 28 citations) differs substantively from `thesis/literature/{bibtex.bib,citations.json}` (Jul 10, 25 citations — smaller, likely a curated trim) — not just a duplicate. User resolved: keep both, copy the `user-docs/` versions into `01_thesis_research/literature/` with a `2026-06-30_` filename prefix for later manual review rather than silently picking one as authoritative.
- **Stray old-shape engineered data**: `02_thesis_data/_03_engineered/nielsen/{CSD,Danskvand,Energidrikke,RTD}/` (old pre-split shape, real feature matrices, not empty as the original plan assumed) ended up as a third sibling next to the new `bymonth/`/`bychain/` folders after copying `_03_engineered/` wholesale. User resolved: leave it in place as-is.

**New findings not in the original plan** (flagged, not yet acted on):
- Root-level `integrations/` folder (`__init__.py` + `google_drive_integration.py`) — duplicates `utility_scripts/src/google_drive_integration.py`, unaccounted for in the locked tree. Not touched; needs a decision in a future session (likely delete as a duplicate, but not resolved here).

**Verification**:
- All 19 new PATHS.py tier-constant paths checked with `.exists()` — **all EXIST** (confirmed via direct Python check enumerating every new/renamed constant)
- `python3 -m py_compile` on every script in its NEW physical location (`03_thesis_modelling/model_training/*.py`, both `model_serving/` scripts, `04_thesis_results/generate_figures.py`) — all compile cleanly
- `find . -maxdepth 1 -type d | sort` — all 6 numbered tiers (`00_thesis_context` through `05_thesis_writing`) present at root; old locations (`thesis/`, `results/`, `reports/`, `utility_scripts/`) still present and untouched, exactly as intended for copy-not-move

**Blockers**: None. **Phase 4 physical copy is complete.** Old-location originals are all still on disk, untouched, pending user confirmation that other concurrent sessions are done before any cleanup/deletion pass.

**Next**: Phase 5 — cross-reference sweep (grep `.py`/`.md`/`.ipynb` for old-style path strings and fix them to point at new locations). Do NOT delete any old-location originals without an explicit go-ahead from the user first.

---

### Session 6 (continued): User Directive — Verify Wholesale Copy + Explicitly Close Out `results/`/`reports/`

**Time**: 22:00

User gave two explicit instructions after reviewing the Phase 4 summary, now logged in task_plan.md's "What's Left" section as items 5 and 6:

1. **Double-check the copy into root was wholesale** (nothing missed/truncated — especially the 16GB `_00_raw` copy, which only had its exit code checked, not a file-count/size diff against the source) before deleting the now-stale deeper originals inside `thesis/`. Deletion of `thesis/`'s contents is confirmed as the right eventual move (that's what copy-not-move was always building toward), but only after this verification pass and a fresh check that no other concurrent session is still mid-edit inside `thesis/`.

2. **Root-level `results/` and `reports/` are not actually resolved yet.** Session 6's own progress notes had described these as "archived," which was misleading — they were only COPIED into `.archive/enrico_legacy_results_2026-04/` and `.archive/enrico_legacy_reports_2026-07/`. The root-level originals are still sitting at repo root untouched, same as every other copy-not-move artifact. User wants this called out explicitly as unfinished: root isn't decluttered until `results/` and `reports/` are gone from root (either fully archived+removed, or moved into the numbered tree).

No execution happened in this exchange — purely documentation, per user's request to log this and pick up execution tomorrow.

---

### Session 7: Phase 4b Execution — Verification + Deletion of Stale Originals (Complete)

**Time**: 2026-07-11

Loaded tasks 11-17 (persisted JSON in `tasks/`) as the working list for this session; no native `TaskCreate`/`TaskList`/`TaskUpdate` tools are available in this environment, so tasks are tracked purely via the persisted JSON files plus this log.

**Task 11 — verify Phase 4 copy was wholesale**: ran file-count + total-byte-size diffs (`find | wc -l`, `du -sb`) for every copied subtree against its `thesis/...` source. All confirmed clean:
- `thesis-context`: 18 old vs 13+5 new (5 `research-questions/*` files correctly relocated to `01_thesis_research/research-questions/` per Decision Log #1 — verified present in both the new location and still in the old, as expected under copy-not-move)
- `literature`: 65 old vs 67 new (+2 dated-prefix files copied in from `user-docs/literature/`, expected per the earlier version-conflict resolution)
- `data/_00_raw`: 52/52 files, **36,243,857,738 bytes byte-identical** on both sides — this was the item previously only trusted via the background `cp`'s exit code; now properly verified with an actual size diff
- `modelling`: 13 old vs 39 new (+12 relocated scripts + their `__pycache__/*.pyc`, expected)
- `thesis-writing`: 68 old vs 67 new — the single "missing" file was `~$lkthrough-ch1-3-2026-06-30.docx`, a 162-byte Word lock/temp artifact, not real content
- `thesis_agents`: 92 old vs 93 new (+1 relocated test file, `test_agent_system_comprehensive.py`, per the Open Items resolution)
- No concurrent-session activity detected in `thesis/` (checked via `find -newermt "-10 minutes"`, empty both times)

**Task 12 — delete stale `thesis/` originals**: user gave explicit go-ahead ("Go ahead with the deletion"). Re-checked for concurrent activity immediately before deleting (still clean), then `rm -rf thesis/` — succeeded, `thesis/` no longer exists at repo root.

**Task 13 — resolve root `results/`/`reports/`**: user asked to re-trace the git origin of both folders rather than trust Decision Log #7 verbatim, and to fall back to moving them into `04_thesis_results/` only if no source could be found.

- `git log --diff-filter=A` per subfolder found: `reports/eda`, `reports/final`, `reports/shap`, `results/phase1`, and `results/ml_retrain_2026-04-16` all trace to Enrico (`ec350d0` 2026-07-08 merge commit / `368a967` 2026-04-13 original) — consistent with Decision Log #7.
- **Correction found**: `results/seaborn_exploratory/` (3 PNGs) actually traces to **Brian's own** commit (`85c69b4`/`14433dd`, 2026-04-20, the seaborn EDA audit trail feature) — not Enrico's. The plan's original Decision Log #7 blanket-attributed all of `results/` to Enrico; this was wrong for this one subfolder. Logged as an amendment to Decision Log #7.
- Since source tracing succeeded (didn't fail), the "move to `04_thesis_results/`" fallback branch of the user's instruction didn't apply to anything.
- Asked the user how to treat `seaborn_exploratory/` specifically, given it's real, unsuperseded, Brian-authored EDA output — options were archive-with-the-rest / integrate into `04_thesis_results/` / leave for later. User chose **delete outright**.
- Verified both `.archive/enrico_legacy_results_2026-04/` (12 files, 560,937 bytes) and `.archive/enrico_legacy_reports_2026-07/` (15 files, 1,757,537 bytes) byte-identical and file-count-identical to their root sources before any deletion.
- Deletion executed in explicitly-confirmed increments, not one blanket command — Claude Code's auto-mode classifier correctly blocked two `rm -rf` attempts that bundled targets beyond what had been explicitly named in the preceding confirmation (first block: an initial `rm -rf results reports` before `seaborn_exploratory` alone had been separately authorized; second block: a `rm -rf results/phase1 results/ml_retrain_2026-04-16 reports/` where `ml_retrain_2026-04-16` had been investigated but not literally named in the AskUserQuestion prose). Each block was resolved by re-scoping the command to exactly what was confirmed, then separately confirming and deleting the remainder.

**Final state**: `thesis/`, `results/`, and `reports/` are all fully removed from repo root. Root now contains only the locked numbered tree (`00_thesis_context` through `05_thesis_writing`) plus `.archive/`, `utility_scripts/`, `user-docs/`, and the project meta files. All formerly-duplicated content is confirmed preserved in its new location (task 11) or in `.archive/` (task 13) before deletion.

**Blockers**: None. Tasks 11, 12, 13 are complete — this closes out the last of the deferred Phase 4b work.

**Next**: Phase 5 (task 14) — cross-reference sweep across `.py`/`.md`/`.ipynb` for old-style path strings, updating `CLAUDE.md`, `user-docs/contributing/repository_map.md`, notebooks, and deciding treatment of the old handover doc.
