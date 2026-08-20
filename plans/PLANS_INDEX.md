# Plans Index

> **Scheme updated 2026-06-22**: Flat folder layout replaces status-bucket folders.
> New plans: `plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/`
> Archived plans: `plans/.archive/`
> Status tracked in plan frontmatter only — no outcome files, no folder movement on status change.
> Next available P-ID: **P0041**

---

## Active Plans

### Focus / In Progress

| P-ID | Folder | Status | Detail |
|------|--------|--------|--------|
| **P0040** | `P0040_2026-08-20_prometheus-scenarios-d-e/` | **focus** | **Prometheus access landed 2026-08-20.** Extends the SRQ4 ladder from three scenarios to five by adding the real Graph Engine: `D_prometheus` (as shipped, code-as-action) and `E_prometheus_model` (same engine + the `forecast_demand` tool). **D->E is the contribution measured inside the production agent**, and it independently replicates B->C — the same intervention on two different orchestrators. Splitting D from E avoids confounding engine with tool (DEC-SCENARIO-SPLIT, Brian). Engine never enters the repo: proprietary, located via `PROMETHEUS_ROOT` in `.env` (DEC-PROMETHEUS-VENDORING). Data comparability holds — the RU warehouse refreshes monthly and currently sits at July 2026, same as the local snapshot (DEC-PROMETHEUS-DATA, F4). An integration blueprint exists in `.archive/thesis_agents_preintegration/` but **predates engine access** — treat as hypothesis (F1). Also replaces the fabricated `fig4_ram_budget` with real measurement (F5). Tasks 1-3 are free and read-only. 10 tasks. |
| **P0039** | `P0039_2026-08-19_01-45_srq4-system-a-vs-b/` | in_progress | **The A/B/C ladder — delivered.** 18 paid runs, $3.44: `C_model` beat `B_data` on every run (7.7% vs 13.5% median APE), ~28x cheaper and ~22x faster. Tasks 1-6 discharged 2026-08-19; the in-file task table still reads all-pending and is stale. DEC-VENDOR settled: `gpt-5.5-2026-04-23`. Remaining: the optional scale-up (5 brands x 10 repeats, ~$35), an unmeasured Coca Cola `A_plain` (~$1.27), a cheap `C_model` re-run on the re-tuned models (~$0.04), and task 7 (write-up). **Now lower priority than P0040** — the scale-up strengthens a result already established in direction, whereas D/E is the only result nobody else could produce. |
| **P0037** | `P0037_2026-08-12_15-28_serving-interface-refinement/` | in_progress | Tasks 3, 4, 7 delivered 2026-08-19 — `build_service()` runs end to end (230 forecasts), every response carries a trace block, and conformal calibration moved off test residuals. Remaining is cleanup: tasks 2, 6, 8, 9. **Note:** its out-of-scope line "Prometheus/Graph Engine integration (pending NDA)" has expired — that work is P0040, not a reopening of this plan's scope. |
| **P0034** | `P0034_2026-08-01_chapter-number-reconciliation/` | paused | Parked by Brian 2026-08-19 until the pipelines stop moving. Unpauses after the SRQ4 write-up. Its core scope — inventorying hard-coded metrics in the drafts — is now substantially pre-done by `05_thesis_writing/check_chapter_facts.py`, which found **46 factual errors across 9 chapters**, including a five-vs-four category contradiction between Ch1/Ch3/Ch5/Ch10 and Ch4. |

### Blocked / Paused / Backlog

None. **Verified 2026-08-20:** the rows previously listed here (P0001-P0005, P0019,
P0020) reference folders that exist neither in `plans/` nor in `plans/.archive/`.
They were removed from disk without the index being updated, so the index was
advertising plans that could not be opened. If any of that work is still wanted it
needs a fresh P-ID, not a resurrected row.

---

## Archived Plans

See `plans/.archive/README.md` for the full list. Archived: P0006-P0018, P0022-P0033, P0035, P0036, P0038.

**Every archived plan carries a terminal status** (`complete`, `cancelled`, or deliberately
`paused`) — verified 2026-08-20. Only P0025 and P0027 are archived while non-terminal
(`in_progress` / `paused`); both were superseded rather than finished.

---

## How to Create a New Plan

1. Next P-ID: **P0041**
2. Create folder: `plans/P0023_YYYY-MM-DD_HH-mm_<slug>/`
3. Create files: `task_plan.md`, `findings.md`, `progress.md` (use `/planning-with-files` skill)
4. Add to this index
5. Set frontmatter: `pid`, `created`, `updated`, `status`, `focus_detail` (if applicable)

## How to Archive a Plan

Move entire folder to `plans/.archive/` and update this index.

---

**Last updated**: 2026-08-20 (P0040 added — Prometheus scenarios D/E, now the focus. P0039's A/B/C ladder delivered its first paid results and drops to secondary. Index tables rewritten: they had listed P0022-P0038 as active while those folders were already archived on disk.)
