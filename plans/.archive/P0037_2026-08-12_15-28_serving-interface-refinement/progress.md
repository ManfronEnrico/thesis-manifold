---
pid: P0037
created: 2026-08-12 15:28:00
updated: 2026-08-12 15:28:00
status: in_progress
---

# Progress — P0037

## Session 1 — 2026-08-12 15:28

**Branch:** `thesis/serving-interface-refinement` (created from `main`; per Trust-tier
branch rule, no work on `main`).

### Done

- Read `model_serving/` in full (2 files), `model_training/srq2_agent.py`,
  `srq4_experiment.py`, `srq2_synthesis.py`
- Read SRQ2 + SRQ4 scope files and `sample-size-and-tool-interface-rationale.md`
- Verified the ChatGPT analysis claim-by-claim against the repo (F8)
- Wrote findings F1-F9, task plan with 9 tasks across 3 phases

### Verified defects (not inferred — checked on disk)

| ID | Check run | Result |
|---|---|---|
| F2 | `ls model_training/forecast_service.py` | No such file — import in `srq4_experiment.py` is broken |
| F4 | `ls model_serving/system_a_forecast/*.csv` | No `forecasts.csv` — never built |
| F5 | Read both calibration blocks | `build_service` uses test residuals; `_eval_forecast` uses val |
| F6 | Read tool schema in `run_system_a` | Schema is `{category, brand}` only — no horizon param |

### Open

- **DEC-HORIZON is blocking** tasks 4-6. Recommendation in task_plan.md is option D
  (recursive, capped, declared), fallback A (restrict to h=1). Needs Brian's call.

### Notes for next session

- The `fs` import in `srq4_experiment.py` is broken *and* unused — `run_system_a` calls
  the local `_eval_forecast()`. Fixing it is therefore not urgent for SRQ4 *results*,
  but the module still fails to import, so nothing in that file runs.
- Do not adopt the ChatGPT feature taxonomy verbatim: it classes promo as
  future-known, which in this pipeline is the V3 target-leakage defect the thesis
  claims credit for fixing.
