---
pid: P0047
created: 2026-09-05 21:10:00
updated: 2026-09-06 15:30:00
status: in_progress
focus_detail: "Option C DECIDED and BUILT 2026-09-06: DK holiday enrichment ships via Nager.Date, contract v1.2, appendix tables generated. Remaining: re-run step 3 for 4 categories to emit v1.2 contracts, retrain, report per-category delta + SHAP, close 5 Word threads. Upstream of P0042's funded runs."
---

# P0047 — Exogenous enrichment: holiday calendar

> **P-ID NOTE.** Created as P0046, which collided with
> `P0046_2026-09-05_20-40_figure-table-provenance-centralisation` (parallel
> session, same day). Renumbered **P0047** here; the folder name still says
> P0046. Rename the folder when convenient — the other plan is referenced by
> DEC-P0046-* decision IDs and should keep the number.

## Why this is not part of P0043

The Word review objects in five threads that the thesis **claims** exogenous
enrichment it does not **have**: ch1 15/18/20, ch2 66/69, ch3 127, ch4 177,
ch5 207 (`MISSING: the holiday api enrichment`).

P0043 closes threads by editing prose. These five cannot be closed that way,
because the honest fix has two branches and only one is writing:

- **Withdraw** the claim → prose fix → P0043's job
- **Deliver** the enrichment → new feature → retrain → every WMAPE in ch6/8/9/10 changes

The second branch touches SRQ1 results and the funded SRQ4 runs, so it lives here.

## Decision — Option C, upstream of the funded runs

**Brian, 2026-09-05.** Build it, benchmark with and without, and report the delta
whatever it is.

Not Option B (build, mention if favourable): the delta is genuinely unknown —
F1 corrected establishes no real calendar has ever been tested here — so
committing in advance to reporting either result is what keeps it honest. A null
at monthly grain is a publishable finding; a positive one improves the models.

Not Option A (withdraw): stays only as fallback if the retrain cannot fit.

**Deadline drives sequencing.** P0042 blocks 1–3 are ~111 runs at ~$40. Spending
that against a feature set the thesis then abandons is the outcome to avoid, so
enrichment is **upstream** of those runs, not parallel to them.

## What was built (2026-09-06)

| component | location |
|---|---|
| Fetch + cache + manifest | `01_SRQ1_.../\_00_raw/holidays/fetch_holidays.py` |
| Features | `engineer_features.py::add_holiday_features` |
| Decision point | `step_3_derive_params.py::derive_holiday_enrichment` (contract v1.2) |
| Application | `step_4_engineer_features.py` (accepts v1.1 + v1.2) |
| Auto-refresh hook | `save_all_datasets.py::_refresh_holidays` |
| Appendix tables | `\_00_raw/holidays/export_holiday_appendix.py` → tables 90–93 |

Features: `days_in_month`, `n_holidays`, `non_holiday_days`. See F4–F7.

## Tasks

| # | task | blocked by | status |
|---|---|---|---|
| 1 | Ground truth: what IS exogenous in the live feature set | — | complete |
| 2 | Size Option C against the P0042 schedule | 1 | complete |
| 3 | DECISION GATE → Option C, before the funded runs | 2 | complete |
| 9 | Record corrected F1/F2 reasoning in `writing-notes/` | — | complete |
| 5 | Build the feature + fetch + contract wiring | 3 | complete |
| 10 | Appendix tables per DEC-P0046-PATHS / -ROUTING | 5 | complete |
| 11 | Re-run step 3 × 4 categories → v1.2 contracts | 5 | **next** |
| 6 | Re-run SRQ1 benchmark with/without; delta per category + SHAP | 11 | pending |
| 7 | Regenerate affected tables/figures; update staleness audit | 6 | pending |
| 12 | Writing notes: reproducibility limit, proxy caveat, future work | 6 | pending |
| 8 | Close the five Word threads with the outcome | 7 | pending |
| 4 | *(fallback only)* If A: narrow claims, hand prose to P0043 | — | n/a |

**Task 11 is the gate.** Existing v1.1 contracts keep running unenriched — correct,
but the enrichment does nothing until step 3 re-runs.

## Reporting requirement (task 6)

Report the per-category delta **whatever it is**, and compare SHAP before/after.
`month`/`quarter`/`peak_month` already exist, so a naive "WMAPE improved" invites
the reply that month-of-year was re-encoded. The rebuttal is empirical: if holiday
attribution rises while `month`/`peak_month` fall by the same amount it is
redistribution; if they hold it is new signal.

Appendix table 92 is the structural half of that argument — see F7.

## Non-goals

- **Weather / macro data.** The comments name a holiday calendar. Note as future
  work (task 12); do not expand scope now.
- **School holidays.** No free API found (Brian, 2026-09-06). Out of scope by data
  availability — record it, don't leave it silent.
- **Re-opening the grain.** Brand × month is locked (DEC-GRAIN).
- **Retro-fitting.** If A ever runs, the claim is withdrawn, not softened.
- **Arguing from the 2026-08-18 rename.** It was a naming fix on a mislabelled
  peak-month rule, not a negative result (F1). Do not cite it either way.

## Related

- `plans/P0043_.../` — writing-side plan; the five threads (F47)
- `plans/P0042_.../` — funded runs; this plan is upstream of them
- `plans/P0046_..._figure-table-provenance-centralisation/` — DEC-P0046-PATHS,
  -ROUTING, -SINGLE-HOME, -ANCHOR govern the appendix generator
- `06_thesis_writing/writing-notes/exogenous-enrichment-and-the-holiday-question.md`
