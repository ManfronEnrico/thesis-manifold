---
pid: P0033
created: 2026-08-01 00:00:00
updated: 2026-08-11 16:08:00
status: blocked
blocked_by: P0036
focus_detail: "BLOCKED by P0036 (2026-08-11). Still the top priority once unblocked, but mirroring the CSD notebook in its current state would propagate a market-filter defect — it filters to 9 region children of DVH EXCL. HD instead of parent 1256338, yielding all-zero promo columns — to all four categories. Fix CSD first (P0036), then mirror."
---

# P0033 — Mirror CSD EDA to Danskvand / Energidrikke / RTD

> **Independent plan, and the top priority.** This is the critical path to the writing
> phase (harness task B03). It can run in parallel with P0032 and P0034 — but see
> "Coupling" below for the one ordering constraint worth respecting.

## Decision (locked by Brian, 2026-08-01)

**One notebook per category**, exactly as done for CSD. Not a return to flat step scripts.

## Why this is the priority

Ch4 (data assessment) cannot be finished until all four categories have comparable EDA
output. Everything in the writing phase downstream of Ch4 is gated on it. Per Brian:
*"min/max and just mirror what we have right now to the other datasets so we get to the
writing process ASAP."*

## Current state — the structural gap

CSD diverged from the other three on 2026-07-13:

| Category | Shape | Location |
|----------|-------|----------|
| **CSD** | Notebook | `_02_preprocessing/nielsen/CSD/pipeline_step_scripts/pre_processing_notebook_csd.ipynb` (step scripts archived under `.archive/2026_07_13-16_02 - Previous Modularized Step Scripts/`) |
| Danskvand | Flat step scripts | `_02_preprocessing/nielsen/Danskvand/pre_danskvand_0..6.py` |
| Energidrikke | Flat step scripts | `_02_preprocessing/nielsen/Energidrikke/pre_energidrikke_0..6.py` |
| RTD | Flat step scripts | `_02_preprocessing/nielsen/RTD/pre_rtd_0..6.py` |

`PATHS.get_category_preprocessing_scripts_dir()` already handles both layouts transparently
(it probes for a `pipeline_step_scripts/` subfolder), so path resolution is not a blocker.

## Scope boundary — explicit min/max discipline

**In scope:** structural mirroring only. Same cells, same order, same outputs, same
parameters as CSD, adjusted only where a category genuinely differs (e.g. promo-zero
categories, differing period counts, `MIN_PERIODS` feasibility).

**Out of scope — deliberately deferred:**
- The 6 EDA enrichment candidates in `_02_preprocessing/nielsen/_notes/eda-improvement-candidates.md`.
  4 of the 6 require Zotero papers not yet in the library (Hyndman, Bergmeir, Cleveland,
  Ataman). Adding features now would delay Ch4 and force a second pass anyway. **Skip all 6.**
- Any grain other than brand×month (DEC-GRAIN dropped chain/region).
- Totalbeer — excluded from the thesis (see P0034 for the justification wording).

## Coupling with P0032 (the one ordering constraint)

P0032 changes `_shared_modules/engineer_features.py`, which all four categories call.

- **Structural mirroring (tasks 1–5)** — safe to do now, in parallel with P0032.
- **Final production runs (task 6)** — should happen *after* P0032 lands, otherwise the
  three new categories bake in the leaky `promo_intensity` and need re-running.
- danskvand and RTD are **promo-zero**, so they are unaffected by V3 either way and can be
  run to completion at any time. Only **energidrikke** is genuinely order-sensitive here.

## Phases

| Phase | Goal | Tasks |
|-------|------|-------|
| 1 | Establish the CSD template + per-category delta inventory | 1, 2 |
| 2 | Build the three notebooks | 3, 4, 5 |
| 3 | Run to completion + verify parity | 6, 7 |
| 4 | Ch4 inputs ready | 8 |

## Definition of done

- Three notebooks exist, one per category, structurally matching CSD.
- Each runs end-to-end and writes to `_03_engineered/bymonth/{Category}/`.
- Outputs are parity-checked against CSD's output shape (same artefacts, same schema).
- Per-category deltas (parameters that legitimately differ) are documented in `findings.md`.
- Ch4 has everything it needs for all four categories.

## Related

- `harness/thesis_tasks.json` — B03 (`blocked_brian`), the harness's name for this work
- P0030 / P0031 — CSD notebook consolidation + remaining gaps (the template this mirrors)
- `_notes/eda-improvement-candidates.md` — deferred enrichments, explicitly not in scope
