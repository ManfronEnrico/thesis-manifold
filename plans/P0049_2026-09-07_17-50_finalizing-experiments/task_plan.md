---
pid: P0049
created: 2026-09-07 17:50:00
updated: 2026-09-10 17:15:00
status: in_progress
focus_detail: "TRAINING IS ON THE HPC (P0053); this plan is the experiment side only. DEC-VENDOR SETTLED 2026-09-10: all scenarios run gpt-5.5-2026-04-23, argued on ecological validity -- the Prometheus engine sets main_agent_model and coder_model to gpt-5.5, so D/E run it regardless, and a vendor split would put model family into the B->C vs D->E comparison. Argument in writing-notes/dec-vendor-model-choice.md; ch3 + ch9 prose awaits approval. NEXT: (1) re-check the 111-run sampling allocation -- F32 took scorable brands 120 -> 168, and the design was frozen against the smaller population; (2) scenarios D/E, which are NOT IMPLEMENTED AT ALL (SCENARIOS holds A/B/C) and need the E2B template first -- Prometheus IS reachable locally at Z:/_dev-ssd/prometheus, so this is a build task rather than a blocked one; (3) smoke test when HPC results land, then the funded set. verify_setup.py 10/10."
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

### Phase 1 — Horizon ✅ DONE (2026-09-07)

It was **three** defects in three layers, not one — see `findings.md` F23. Fixing only
`engineer_features()` would have left the experiment still scoring one month ahead.

1. ✅ `engineer_features()` takes a required `horizon`; every past-derived feature
   shifts by an extra `h − 1`. H=1 is byte-identical to the old definition.
2. ✅ `srq4_experiment.py` scores `test.iloc[HORIZON − 1]`, not `test.iloc[0]`.
   `HORIZON = 3` is one constant selecting both the matrix and the scored month.
3. ✅ Scenario C passes the scored month to the tool; the payload carries
   `months_ahead`. The leakage assert now checks the gap is **exactly** the horizon.
4. ✅ Steps 4–6 re-run, 4 categories × H=1,3. All 8 matrices published and verified:
   `lag_1` differs across horizons and `h3.lag_1 == h1.lag_3` exactly.
5. ✅ `verify_setup.py`: **10/10, no warnings.**

**Still to come: H3 accuracy should worsen after retraining.** Three months ahead is
harder than one. The models on disk are still H=1-trained — that is phase 2.

### Phase 2 — Re-run SRQ1 on both horizons (IN PROGRESS)

**DEC-HORIZON-BOTH (Brian, 2026-09-07): run H=1 and H=3 properly, both.**

The horizon is now a single value per run, `SRQ1_HORIZON` (default 3), read by
`srq1/_horizon.py` and used for **both** the input matrix and the output directory —
so the two can never describe different horizons.

| Horizon | Matrix | Results go to |
|---|---|---|
| **3** (primary) | `*_feature_matrix_h3.parquet` | `srq1_model_performance/{tables,figures,models}/` |
| **1** (secondary) | `*_feature_matrix_h1.parquet` | `srq1_model_performance/h1/{...}/` |

H=3 keeps the unsuffixed paths because `forecast_tool.py`, the SRQ4 harness, the
appendix exporter and the figure generators all read them. **An H=1 run therefore
cannot overwrite an H=3 result** — the property that makes this safe.

Run it: `python model_training/run_both_horizons.py` (`--dry-run`, `--horizon`,
`--only` available). 8 ordered stages × 2 horizons; the order is a dependency chain,
not a bag of scripts.

**Sanity check already passed** (untuned benchmark): H=3 is worse than H=1 in 3 of 4
categories — the plan's own test that the fix took effect. RTD moves the other way;
F26 records why that is real rather than survivorship, and what still needs confirming.

**Training moved to the HPC on 2026-09-08** after three OS memory kills on the laptop
(F27: the suite needs ~282 MB; the machine had ~1.2 GB free with Word, VS Code and two
Claude sessions resident). The run procedure is **P0053**, written to be read from the
HPC with no conversation history.

**The HPC must be on `ae4c290` or later.** Anything started before `3f8b0a9` is training
on 13 features instead of 18 (F31), and anything before `9745bf3` silently drops
Danskvand and Energidrikke on Linux.

Two defects found while doing this — see `findings.md`:
- **F24** — 13 scripts hardcoded `_h3`; none could produce H=1.
- **F25** — `train_and_persist.py` read its selection inputs from the tier root
  instead of `tables/`, so **model selection silently fell through to a hardcoded
  `"XGBoost"` default** and never consulted the CV study. The default was wrong for
  all four categories.

### Phase 3 — Re-verify the SRQ4 harness

`python 04_SRQ4_Scenario_Experiment/scenario_setup/verify_setup.py`

Required: **10/10 and no `!` warnings**. A warning here means the tool is serving
degraded payloads (see F21). Passing as of 2026-09-07, but **re-run after phase 2** —
the tool loads the persisted model, so retraining changes what it serves.

### Phase 3b — Smoke test ✅ BUILT (2026-09-09)

`04_SRQ4_Scenario_Experiment/scenario_setup/smoke_test.py` — one run per scenario,
**~$0.81**, into a `smoke/` subfolder under a `--budget` cap. Never the results
directory.

`verify_setup.py` never sends a request, so it cannot see what only appears when a
scenario runs. Nine checks, each traceable to a stated requirement rather than chosen
for coverage — see F34. Four come straight from ch2 §2.5's auditability taxonomy.

```bash
python 04_SRQ4_Scenario_Experiment/scenario_setup/smoke_test.py --dry-run   # free
python 04_SRQ4_Scenario_Experiment/scenario_setup/smoke_test.py            # ~$0.81
```

**Run it once the HPC results land**, before phase 4. A defect found here costs $1; the
same defect in phase 4 costs $40.

### Phase 4 — Funded runs

P0042's frozen sampling design: 111 runs, ~$40, allocated inversely to per-run cost
(A n=3, B/C n=10 stratified, C-only cross-category). DEC-VENDOR is settled (2026-09-10).

**The eligible population changed on 2026-09-09.** F32 fixed a `KeyError` that had made
Danskvand and Energidrikke unusable, taking scorable brands from **120 to 168**. The
sampling design was frozen against the smaller population — re-check the per-category
allocation before running.

### Phase 5 — Scenarios D and E (NOT STARTED, and larger than it looks)

**`SCENARIOS` holds A, B and C only. The Prometheus arms are not implemented at all** —
this is a build, not a configuration change. The E2B template is also unbuilt, and
without it scenario D runs without `statsmodels`/`prophet`, so D→E would measure a
missing library rather than the tool.

Why this matters beyond completeness: **B→C and D→E are the same intervention on two
different orchestrators**, and agreement between them is a materially stronger claim
than either alone (`INHERITED_CONTEXT.md` §1). Half that argument does not exist yet.

When they land, add them to `smoke_test.py` first and smoke them before spending.

## Decisions carried in

| ID | Decision | State |
|---|---|---|
| **DEC-VENDOR** | All SRQ4 scenarios run `gpt-5.5-2026-04-23` | **MADE 2026-09-10.** Decided on ecological validity: the Prometheus engine's own config sets `main_agent_model` and `coder_model` to `gpt-5.5`, so D/E run it regardless — a vendor split would put model family into the B→C vs D→E comparison. Argument: `writing-notes/dec-vendor-model-choice.md` |
| **DEC-HORIZON** | Implement both horizons, benchmark both, SRQ4 at 3 months | **MADE** (Brian, via P0048); implemented + verified 2026-09-07 |
| **DEC-HORIZON-BOTH** | H=1 and H=3 both run properly. H=3 primary, keeps the unsuffixed result paths; H=1 writes to `h1/` | **MADE** (Brian, 2026-09-07) |
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
