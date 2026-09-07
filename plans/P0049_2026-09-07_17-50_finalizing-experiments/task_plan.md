---
pid: P0049
created: 2026-09-07 17:50:00
updated: 2026-09-07 18:15:00
status: in_progress
focus_detail: "CONSOLIDATION PLAN for the account switch — read START_HERE.md first. Collects every open experimental thread from P0039/P0040/P0042/P0044/P0047 into one ordered sequence. Two headline facts: (1) SRQ1 numbers are now deterministic (XGB_N_JOBS=1, F18) and the model-equivalence verdict survived (F19); (2) but engineer_features() never receives the horizon, so h1 and h3 are the SAME one-month task and published results are H1 mislabelled as H3 (F22, found by P0048). The horizon fix is upstream of the ~111 funded runs. Also fixed today: forecast_tool.py was reading its track record from the wrong directory and silently serving forecasts with NO historical_* fields (F21) — that would have invalidated the B->C comparison the funded runs are meant to measure."
---

# P0049 — Finalizing experiments

> **Figures, tables and diagrams are owned by
> [P0050](../P0050_2026-09-07_18-40_figure-table-generation-and-provenance/START_HERE.md)**
> (also written for this account switch). Any artefact you need to cite, or find
> stale, belongs to that plan — 11 diagrams and 25 appendix tables regenerate
> from 5 scripts.


## Goal

Get the SRQ1 model numbers to a state that is **both reproducible and correctly
labelled**, then run the funded SRQ4 scenarios against them.

Reproducibility is done. Labelling is not.

## Why this plan exists

Seven plans were active at once, each holding part of the experimental picture, and the
account switch loses the conversation that held them together. This plan is the join:
one ordered sequence, with the blockers stated as they actually are rather than as the
older plans describe them.

Two of those older descriptions were **wrong when checked**:

- P0039 says it is blocked on `03_thesis_modelling/.env`. That path does not exist;
  `.env` is at the repo root and `verify_setup.py` passes 10/10.
- `LOCKED_STATE.md` said the funded runs were unblocked. The horizon defect is upstream
  of them.

Checking a stated blocker before acting on it is the main lesson of this plan.

## Phases

### Phase 1 — Horizon (BLOCKING everything downstream)

1. Decide the fix: at horizon *h*, lags become `shift(lag + h − 1)`; rolling windows
   shift with them.
2. Implement in `engineer_features()`, which currently has no `horizon` parameter.
3. Re-run preprocessing steps 3–6 for 4 categories × H=1,3.
4. Confirm the matrices now differ: `lag_1` must **not** be identical across h1/h3.

**Expect H3 accuracy to worsen.** Three months ahead is harder than one. If it does not
change, the fix has not taken effect.

### Phase 2 — Re-run SRQ1 on both horizons

Full benchmark, tuned benchmark, CV, stability, ablation, appendix tables.
All already deterministic, so a re-run is mechanical — but it is not cheap in wall-clock
(the tuned ablation is ~24 Optuna studies; stability is 40).

Produces the first genuine **dual-horizon** results table.

### Phase 3 — Re-verify the SRQ4 harness

`python 04_SRQ4_Scenario_Experiment/scenario_setup/verify_setup.py`

Required: **10/10 and no `!` warnings**. A warning here means the tool is serving
degraded payloads (see F21).

### Phase 4 — Funded runs

P0042's frozen sampling design: 111 runs, ~$40, allocated inversely to per-run cost
(A n=3, B/C n=10 stratified, C-only cross-category). Decide DEC-VENDOR first.

Then D/E (P0040) — build the E2B template first, or D is silently handicapped.

## Decisions carried in

| ID | Decision | State |
|---|---|---|
| **DEC-VENDOR** | Claude vs GPT for SRQ4 | **OPEN.** ~$7 vs ~$4 for 50 runs — decide on ecological validity, not cost |
| **DEC-HORIZON** | Implement both horizons, benchmark both, SRQ4 at 3 months | **MADE** (Brian, via P0048) |
| **DEC-DETERMINISM** | Accuracy at `n_jobs=1`; resource profiling at `-1` | **MADE**, implemented, verified |
| **DEC-GRAIN** | brand × month | Locked, earlier |

## What this plan does NOT cover

- **Prose insertion** — P0048, parallel session.
- **Word comment threads / claims verification** — Brian's, tracked in P0047.
- **Figure/table provenance Phase 5** — P0046.

## Related

- `START_HERE.md` — read first
- `../.archive/P0046_2026-09-05_21-10_exogenous-enrichment-decision/LOCKED_STATE.md` — the numbers
- `../.archive/P0046_2026-09-05_21-10_exogenous-enrichment-decision/findings.md` — F18–F22
- `../P0048_2026-09-07_13-51_remaining-prose-and-results-citations/START_HERE.md` — horizon origin
