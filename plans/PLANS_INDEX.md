# Plans Index

> **Scheme updated 2026-06-22**: Flat folder layout replaces status-bucket folders.
> New plans: `plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/`
> Archived plans: `plans/.archive/`
> Status tracked in plan frontmatter only — no outcome files, no folder movement on status change.
> Next available P-ID: **P0043**

---

## Active Plans

### Focus / In Progress

| P-ID | Folder | Status | Detail |
|------|--------|--------|--------|
| **P0042** | `P0042_2026-08-25_12-45_funded-testing-and-review-sequencing/` | **focus** | **Sequencing for the funded phase.** Two parallel workstreams: (A) NotebookLM review rounds — methodology verification against the 14 Saunders chapters, then per-section *improvement* questions (a different exercise from verification, which cannot find uncited claims or wrong framing); (B) the remaining scenario runs. **Corrects a sequencing error:** the A/B/C ladder is already delivered, so funding unblocks D/E + the optional scale-up, not the first result. Names three gates: freeze D/E scope in writing first, use measured costs not estimates, and decide now what a D→E / B→C disagreement would mean. | **2026-09-01: gate 1 discharged for the A/B/C half.** Sampling design frozen in `2026-09-01_DOC-srq4-sampling-design.md`: 111 runs, $11.06 est / **~$40 realistic**, against a ~$50 ceiling. Allocation is inversely proportional to per-run cost — measured A $0.4277 / B $0.2664 / C $0.0068, so A is ~63x C and equal-n would spend the budget on the least contested arm. A at n=3 (floor), B/C at n=10 stratified over CSD ranks 1/41/76 (the CI block), C-only across the other three categories for ~$0.50 (generalisation). Corrects a prior error: the 4.47x billed/estimate multiplier is **scenario-specific** — web search bills A only, the container bills B only, C carries no surcharge (F1). **Gate 1 for D/E stays OPEN**: `measure_e2b_cost.py` has never been run, and the "~$0.0001/run" E2B figure in the old gate 2 is not a measurement (F6). Free checks all pass — leakage guard clean, model pinning clean across 30 responses (F3, F4).
| **P0041** | `P0041_2026-08-22_16-00_citation-sourcing/` | in_progress | **Citation verification — literature + modelling rounds complete and merged (2026-08-25).** Five Contradicted claims corrected in Ch1/Ch2; the unsourced ≤15% accuracy target withdrawn from Ch6/Ch9/Ch10; the fabricated "Bürger & Pauli (2024)" purged from the live docs. Ch2 and Ch6 now pass `check_chapter_facts.py` clean. Remaining: the methodology round (see P0042 A1) and a second download batch for Ouyang/Atıl/Schwartz/Chen, cited in §2.5 with no PDF. |
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

1. Next P-ID: **P0043**
2. Create folder: `plans/P0023_YYYY-MM-DD_HH-mm_<slug>/`
3. Create files: `task_plan.md`, `findings.md`, `progress.md` (use `/planning-with-files` skill)
4. Add to this index
5. Set frontmatter: `pid`, `created`, `updated`, `status`, `focus_detail` (if applicable)

## How to Archive a Plan

Move entire folder to `plans/.archive/` and update this index.

---

**Last updated**: 2026-09-01 (P0042 gate 1 frozen for A/B/C; see its findings F1-F6). 2026-08-22 (P0041 added -- citation sourcing register, maintained alongside P0040 rather than replacing it: every methodological claim needing an academic source, tracked as VERIFIED / PROSPECTIVE / UNSOURCED / UNSOURCEABLE for export to NotebookLM. Prompted by an unsourceable "50-200 HPO trials" claim caught before it reached the prose.) (2026-08-20: P0040 added — Prometheus scenarios D/E, now the focus. P0039's A/B/C ladder delivered its first paid results and drops to secondary. Index tables rewritten: they had listed P0022-P0038 as active while those folders were already archived on disk.)
