---
name: repo-tier-structure
description: RULE - Locked numbered-tier repo structure from the P0028 restructure; what belongs in each tier and what NOT to mistake for bloat
category: reference
applies-to: [repo-structure, file-placement, cleanup]
triggers: [where-does-this-go, is-this-bloat, new-srq-results, restructure-question]
created: 2026_07_11-18_02
updated: 2026_07_12-00_00
---

# Repo Tier Structure (Locked, P0028)

As of the P0028 restructure (2026-07-11), the repo root is organized into six
numbered tiers, `00_thesis_context/` through `05_thesis_writing/`. The old
`thesis/` folder segment no longer exists — everything under it was flattened
to root. `PATHS.py` mirrors this same structure in its constants; see its
top-of-file docstring for the same map in one place.

## Quick Reference

| Tier | Purpose | Key subfolders |
|------|---------|----------------|
| `00_thesis_context/` | Thesis topic, scope, compliance | `thesis-topic/`, `formal-requirements/`, `methodology/`, `prometheus-integration/` |
| `01_thesis_research/` | Research questions + literature | `research-questions/`, `literature/` |
| `02_thesis_data/` | Data pipeline, raw → engineered | `_00_raw/` .. `_03_engineered/`, `preprocessing/` |
| `03_thesis_modelling/` | Model training + serving | `model_training/`, `model_serving/`, `notebooks/`, `prompts/` |
| `04_thesis_results/` | Final SRQ results | `srq1/`, `srq2/`, `srq4/` (one folder per SRQ) |
| `05_thesis_writing/` | Thesis prose + figures | `sections-drafts/`, `sections-final/`, `figures/`, `analysis/` |

Non-thesis governance/tooling (`utility_scripts/`, `plans/`, `user-docs/`,
`.claude/`) sits outside this numbered scheme by design — do not try to force
these into a tier.

---

## Rules

### New SRQ results always go in `04_thesis_results/srq{N}/`

Never create a new top-level tier for a new SRQ's output. If SRQ5 lands,
its results go in `04_thesis_results/srq5/`, matching the existing
`srq1/`, `srq2/`, `srq4/` pattern.

### `scenario_setup/` holds experiment running and logging, not models

Added 2026-08-19. `03_thesis_modelling/` now has three sibling folders with
three distinct concerns:

| Folder | Concern |
|--------|---------|
| `model_training/` | training the ML/statistical models (SRQ1 benchmarks, tuning, calibration, SHAP) |
| `model_serving/` | making a trained model reachable at inference time |
| `scenario_setup/` | running scenarios against those models, and logging what happened |

`03_thesis_modelling/notebooks/` and `03_thesis_modelling/prompts/` no longer
exist -- both were archived 2026-08-19 to `03_thesis_modelling/.archive/`, and
their `PATHS.py` constants were removed rather than left resolving to missing
directories. The notebooks predate the four-category scope (6 of 10 reference
the dropped `totalbeer`), the H=3 horizon and the 2026-08-18 leakage fixes. The
prompts folder holds Enrico's SRQ2/SRQ3 set and a partially-executed human-eval
pilot -- a different research question from SRQ4, gitignored, and existing only
on the machine that produced it. Read `.archive/README.md` before touching
either.

The three scenarios are named A (plain LLM), B (LLM + data & code execution),
C (LLM + trained models) -- ordered as an information ladder of increasing
capability, so A -> B measures what data access buys and B -> C measures what
the thesis artefact adds. Do not reintroduce the earlier "arm" vocabulary or the
earlier lettering, which ran the other way.

`srq4_experiment.py` and `srq4_tier2.py` moved out of `model_training/` because
they train nothing -- they run the three-arm SRQ4 comparison against models
trained elsewhere. When adding a script, ask which of the three verbs it does:
train, serve, or run-a-scenario.

`scenario_setup/` also holds `prompts.py` (every prompt in one auditable place,
never inline in the harness), `verify_setup.py` (free pre-flight checks) and
`inspect_runs.py` (read back logged runs). See its README for the full contract.

### `model_training/` vs `model_serving/` is a train-vs-serve split, not a naming convenience

`03_thesis_modelling/model_training/` holds one-off training/benchmark/calibration
scripts (e.g. `srq1_benchmark.py`, `srq1_baselines_stat.py`, `srq1_calibration.py`).
`03_thesis_modelling/model_serving/` holds the code that serves a trained model at
inference time (e.g. `system_a_forecast/forecast_service.py`,
`system_b_conversational/`). When adding a new script, ask "does this train
something, or does it run something already trained?" — that answers which
folder it belongs in.

### `utility_scripts/` is tooling-only, never thesis content

Helper scripts for data/setup automation live here, not thesis pipeline logic.
If a script under `utility_scripts/scripts/` starts producing thesis
deliverables directly (rather than supporting infrastructure), it likely
belongs in `02_thesis_data/`, `03_thesis_modelling/`, or `04_thesis_results/`
instead.

### `preprocessing/` inside `02_thesis_data/` holds per-category scripts, not data

`02_thesis_data/preprocessing/nielsen_dvh/` and
`02_thesis_data/_02_preprocessing/nielsen/{Category}/` hold the pipeline
*scripts* (`pre_{category}_N_*.py`, orchestrators). Actual pipeline *data*
lives in the numbered `_0N_*` tier folders — don't confuse the two when
looking for a script vs. looking for its output.

### `02_thesis_data/_03_engineered/nielsen/` — deleted 2026-07-12, do not recreate as scaffolding

`02_thesis_data/_03_engineered/` was expected to contain only `bymonth/` and
`bychain/` per the original P0028 plan. It briefly also contained a `nielsen/`
subfolder with real, non-empty CSD feature matrices — leftover from when
`_03_engineered/` was copied wholesale from the old `thesis/data/_03_engineered/`
tree. Between 2026-07-10 and 2026-07-12 the project explicitly decided to leave
it in place (see P0028 findings.md, Session 6 finding #4) rather than archive it,
on the reasoning that it was real data, not bloat.

**That decision was superseded on 2026-07-12**: a same-session comparison
(P0027 findings.md, "2026-07-12 Session") confirmed `_03_engineered/bymonth/CSD/`
was a byte-identical-content, one-day-newer regeneration of `nielsen/CSD/`'s
feature matrix — i.e. `nielsen/CSD/` was fully superseded, not a unique data
source. The other 3 categories (Danskvand/Energidrikke/RTD) never had a real
feature matrix in `nielsen/` at all (split-dates metadata only, matching
`bymonth/`'s equally-empty state for those categories — Phase 5 of P0027 hasn't
run for them yet). With no unique content remaining, the user deleted
`02_thesis_data/_03_engineered/nielsen/` directly.

**Implication for future sessions**: if you see a `nielsen/` subfolder reappear
under `_03_engineered/` (e.g. from restoring an old branch/backup), do not assume
it needs preserving by default the way this rule used to say — check whether its
content is genuinely unique (i.e., not already superseded by `bymonth/`) before
deciding.

> **Superseded by P0035 (2026-08-01):** the `get_category_engineered_dir()`
> deprecated alias no longer exists — it was removed along with
> `get_category_engineered_bychain_dir()`. Call
> `get_category_engineered_bymonth_dir()` explicitly. See the next section.

### `_03_engineered/` holds `bymonth/` only — brand × month is the locked grain

**DEC-GRAIN** (Enrico, 2026-07-12) fixed the modelling grain to **brand × month**.
The chain and region grains became a documented limitation + future work rather
than an active result, and `_03_engineered/bychain/` was deleted from disk.

P0035 (2026-08-01) then removed the code half of that state, which had been left
resolving to a directory that no longer existed:

- `PATHS.py`: `THESIS_DATA_ENGINEERED_BYCHAIN_DIR`,
  `get_category_engineered_bychain_dir()` and the deprecated
  `get_category_engineered_dir()` alias were all removed. Explanatory comments
  were left at their former locations.
- Model training/serving scripts no longer register a `bychain` dataset; the
  `danskvand` category, previously pinned to the chain grain, now reads
  brand × month like every other category.
- `04_thesis_results/srq1/` no longer carries chain-grain entries. The originals
  are preserved at
  `plans/P0035_2026-08-01_grain-artifact-removal/preserved_chain_grain_results/`.
- `phase3_region_grain_test.py` and the stale `utility_scripts/scripts/` shadow
  copies were archived to `.archive/grain_artifacts_p0035_2026-08/` (with a
  README explaining why) rather than deleted — they are the evidence behind the
  grain decision.

**What was deliberately NOT removed**: the `group_keys` parameter in
`_02_preprocessing/nielsen/_shared_modules/engineer_features.py`. It is
grain-*capable*, not grain-*committed* — its default is already `["brand"]`, and
the chain grain was invoked by *passing* `["brand", "market_id"]`, not by a
separate code path. Likewise the `--grain/--grains` CLI switches survive so a
future grain can be registered. **If you reintroduce a grain, add it to
`DATASETS`/`GRAIN_CONFIG` — do not resurrect the deleted PATHS helpers.**

### `02_thesis_data/` also carries legacy leftovers alongside the new tiers

`nielsen/`, `preprocessing/` (top-level, distinct from the one inside a
tier), and `assessment/` sit next to the `_00_raw/` .. `_03_engineered/`
tier folders. These predate the P0028 numbered-tier convention. Treat them
as known-legacy, not automatically safe to delete — verify against the
plan's decision log before removing anything here.

---

## Related

- `PATHS.py` — top-of-file docstring mirrors this same structure map; all path constants resolve into these tiers
- `plans/P0028_2026-07-10_restructure-thesis-enrico-integration/task_plan.md` — full restructure history, old→new path mapping, decision log
- `plans/P0028_2026-07-10_restructure-thesis-enrico-integration/findings.md` — Session 6 finding #4 (original `_03_engineered/nielsen/` stray-but-real-data callout, since superseded)
- `plans/P0027_2026-07-10_15-30_csd-eda-reconciliation/findings.md` — 2026-07-12 session, confirms `nielsen/CSD/` was a superseded duplicate of `bymonth/CSD/`, documents the deletion
- `plans/P0035_2026-08-01_grain-artifact-removal/` — removed the chain/region grain from live code, paths, results and docs per DEC-GRAIN; `findings.md` F6 records why `03_thesis_modelling/` (not `utility_scripts/scripts/`) is the canonical script tree
- `.archive/grain_artifacts_p0035_2026-08/` — archived region-grain test + stale shadow scripts, with a README explaining the grain decision
- `.claude/rules/root-documentation-boundary.md` — root-level file placement rules (documentation, not data/code tiers)
