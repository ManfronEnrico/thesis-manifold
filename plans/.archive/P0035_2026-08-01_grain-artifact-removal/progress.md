---
pid: P0035
created: 2026-08-01 00:00:00
updated: 2026-08-01 00:00:00
---

# P0035 — Progress Log

## 2026-08-01 — Plan created

- Verified `_03_engineered/bychain/` already deleted from disk; only `bymonth/` remains
- Found ~20 live files still referencing chain/region grain (paths, FEATURES, results, docs)
- Verified P0027's groupby leakage bug is already fixed (`group_keys` threaded throughout)
- Decided `group_keys` parameter stays — grain-capable, not grain-committed
- Flagged `utility_scripts/scripts/` vs `03_thesis_modelling/` duplication as a
  determine-canonical-first hazard
- Tasks 1–8 decomposed; nothing removed yet

## Session log

### 2026-08-01 — Execution session (worktree `p0035-grain-artifact-removal`, branch `chore/p0035-grain-artifact-removal`)

All 8 tasks executed. Changes left **uncommitted** in the working tree for review,
per instruction. Nothing outside the worktree was touched.

**Task 1 — inventory.** Repo-wide grep for `bychain|by_chain|region.grain|market_id`
excluding `.archive/`, `plans/.archive/`, `harness/`. Classified into path
constants, obsolete script, consumers, results, docs. Note: `market_id` hits are a
raw Nielsen **column**, not the modelling grain (finding F9) — excluded.

**Task 2 — canonical tree = `03_thesis_modelling/`.** See F6 for full evidence
(git history divergence, feature-refactor diff, zero inbound references,
tier-structure rule). `utility_scripts/scripts/` copies archived, not edited.

**Task 3 — `PATHS.py`.** Removed `THESIS_DATA_ENGINEERED_BYCHAIN_DIR`,
`get_category_engineered_bychain_dir()`, the deprecated
`get_category_engineered_dir()` alias, and the `__main__` debug print. Updated the
`_03_engineered` docstring. Left explanatory comments at each removal site.
Verified: `import PATHS` succeeds.

**Task 4 — archived.** `git mv` (history preserved) of
`phase3_region_grain_test.py` + 8 shadow scripts to
`.archive/grain_artifacts_p0035_2026-08/`, with a `README.md` recording what each
file was and why it was archived rather than deleted.

**Task 5 — consumers cleaned.** 8 files; `danskvand` unpinned from `bychain` in
the 3 `SELECTED`/`CAT_FILE` tables. `srq1_figures.py` needed judgement (F10):
Fig 1 repointed to the brand grain, Fig 2 (a two-grain comparison) removed.
`engineer_features.py` deliberately **untouched** — `group_keys` stays (F1/F12).

**Task 6 — results purged.** 8 `bychain/*` keys removed from `tuned_params.json`
(8 `brand/*` kept); `## Dataset: bychain` table removed from `tuned_summary.md`
with a pointer note appended. Originals preserved verbatim at
`preserved_chain_grain_results/` with a README highlighting the danskvand
22.0% (chain) vs 23.8% (brand×month) figures P0034 needs.

**Task 7 — docs.** `repository_map.md` `_03_engineered` tree corrected (it was
doubly stale — also still listed the deleted `nielsen/`).
`repo-tier-structure.md` gained a new section documenting the locked grain, what
P0035 removed, and explicitly what must NOT be removed (`group_keys`,
`--grain` switches).

**Task 8 — REGRESSION GATE: STATIC ONLY. Did not really run.**

Attempted: `python preprocessing_csd.py --run-step 4`
Result: **exit 1** — `ERROR: Stage 1 Parquet cache not found!`
Cause: `*.parquet` and `.env` are gitignored, so a fresh worktree has no pipeline
inputs; they live only in the main folder, which this session could not touch (F11).

Static checks that **did** pass, and what each proves:

| Check | Result |
|---|---|
| `grep` for live `bychain` refs | Zero. All remaining hits are explanatory comments or untouched `harness/` audit trail |
| `python -m py_compile` on all 10 modified `.py` | All pass |
| `import PATHS` | OK; `THESIS_DATA_ENGINEERED_BYMONTH_DIR` resolves |
| Import-execute `srq1_benchmark` | OK, `DATASETS == ['bymonth']` |
| Import-execute `forecast_service` | OK, `SELECTED` tags == `['bymonth']` |
| Import-execute `srq1_profiling` | OK |
| Import `engineer_features` | OK; `group_keys` default `['brand']` at all sites |
| Notebook JSON re-parses | OK, 65 cells; diff is 4+/14- (no reformat) |
| `_03_engineered/` on disk | contains `bymonth/` only |

Two import failures were investigated and are **pre-existing environment gaps,
not regressions**: `srq1_benchmark_tuned` needs `optuna` (not installed) and
`srq4_tier2` needs `03_thesis_modelling/.env` (gitignored, main-folder only).

**A human must re-run the real gate from the main folder after merge:**
```
python 02_thesis_data/_02_preprocessing/nielsen/CSD/preprocessing_csd.py
python 03_thesis_modelling/model_training/srq1_benchmark.py
```
Expect the CSD brand×month feature matrix to regenerate identically and the
benchmark to run on grain `bymonth` alone.

**Open items flagged for human review:** F13 (the `brand` vs `bymonth` tag-name
split — a silent-fallback trap), F10 (`fig2_granularity.png` left on disk because
Ch6 prose still cites it), and the four remaining non-grain shadow scripts in
`utility_scripts/scripts/` (out of scope, noted in the archive README).

---

### 2026-08-06 — Independent verification + session cut short

Session hit its limit before P0035 could be closed out. **Nothing was committed.**
The reviewing session spot-checked the execution agent's report rather than
accepting it, since it was a report about deletions.

**Independently confirmed:**

| Claim | Verification |
|---|---|
| Work landed on the right branch | `git branch --show-current` → `chore/p0035-grain-artifact-removal` |
| Archival preserved history | `git status` shows all 9 moves as `R` (rename), not delete+add |
| `PATHS.py` still imports | `import PATHS` → OK; `[a for a in dir(PATHS) if 'chain' in a.lower()]` → `[]` |
| No live `bychain` code refs | grep returns only explanatory comments + untouched `harness/` |
| Preserved results exist | `preserved_chain_grain_results/` contains `README.md`, `tuned_params.PRE-P0035.json`, `tuned_summary.PRE-P0035.md` |
| Scope respected | No files touched under `05_thesis_writing/`, `.archive/**` (beyond the new archive folder), or `plans/.archive/**` |

**Correction made this session:** `tasks/8.json` was marked `completed` by the
execution agent (with a caveat note). Downgraded to **`blocked`** — the plan's
definition of done requires the CSD pipeline to actually run end-to-end, and it
did not. A caveat inside a `completed` status is too easy to miss when scanning.
`task_plan.md` frontmatter likewise moved `in_progress` → `blocked` with a
`blocked_reason`.

**Scale of the uncommitted diff:** 9 renames (archival), 24 modified files,
2 new untracked paths (`.archive/grain_artifacts_p0035_2026-08/README.md`,
`preserved_chain_grain_results/`).

#### To resume

1. **Review the diff before committing** — `git diff` in the worktree. Nothing is
   staged beyond what `git mv` implies. Pay particular attention to
   `srq1_figures.py` (Fig 1 was *repointed* from chain to brand grain — a
   behavioural change to a Ch6 figure, not a deletion) and to the notebook diff.
2. **Commit on the feature branch**, explicit paths only (never `git add -A`).
3. **Merge, then run the real gate from the MAIN folder** (not the worktree):
   ```
   python 02_thesis_data/_02_preprocessing/nielsen/CSD/preprocessing_csd.py
   python 03_thesis_modelling/model_training/srq1_benchmark.py
   ```
   Expect the brand×month matrix to regenerate identically and the benchmark to
   run on grain `bymonth` alone. Only then mark task 8 / the plan complete.
4. **Decide F13** (the `brand` vs `bymonth` tag-name split). This is the one
   finding that can fail *silently*: regenerating `tuned_params.json` with the
   current `srq1_benchmark.py` writes `bymonth/...` keys, so every `brand/...`
   lookup returns `{}` — untuned defaults, no error raised.

#### Environment notes for whoever resumes

- A worktree was created at `worktrees/p0035-grain-artifact-removal`, based on
  `main` @ `958787b` — deliberately NOT on the main folder's working tree, which
  other sessions (P0032/P0033/P0034) were actively switching branches in.
- Creating it required a `safe.directory` entry (Z: drive records no ownership).
  Noted in passing: the global gitconfig already contained a bare `*`
  safe.directory wildcard from an earlier session, which trusts every repo on the
  machine. Unrelated to P0035, but worth cleaning up.
- `git worktree add` timed out at ~36% but the checkout **did** complete — verify
  with `git status`, don't re-run it.
