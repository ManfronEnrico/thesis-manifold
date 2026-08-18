---
pid: P0039
created: 2026-08-19 01:45:00
updated: 2026-08-19 01:45:00
---

# P0039 Findings

## F1 — the harness is further along than the plan files implied

`03_thesis_modelling/model_training/srq4_experiment.py` already implements the full
experiment. Read before assuming anything needs building:

- `run_system_a()` — Claude calls `forecast_demand`, backed by the trained XGBoost
- `run_system_b()` — Claude gets `df` in an E2B sandbox and must write its own code
- Both record forecast, input/output tokens, latency
- Both loop up to 8 tool-use rounds
- System B parses a `FORECAST=<number>` sentinel from stdout

The design is clean and single-variable. **What it lacks is execution, not
conception.**

## F2 — the only blocker is credentials

`srq4_experiment.py` line 28 reads `ROOT/.env` for `ANTHROPIC_API_KEY` and
`E2B_API_KEY`. The file is gitignored and absent, so the module raises
`FileNotFoundError` on import.

`forecast_service.py` imports cleanly and `build_service()` runs, so System A's backing
is in place. Nothing else about SRQ4 can be verified until `.env` exists.

## F3 — what E2B is, and what drives its cost

E2B is a disposable cloud sandbox. System B's answer only exists if the model's
self-written code actually *runs*; E2B is where it runs without touching a real
machine. System A does not need it, and **that asymmetry is the experiment**.

Billing is by sandbox uptime (per-second while alive), not per call, with a free tier
that likely covers this workload.

Cost drivers visible in `run_system_b()`:

| Step | Note |
|------|------|
| `Sandbox.create()` | per-run container |
| `pip install statsmodels` | **re-downloaded every single run** — likely the largest fixed cost |
| data load + up to 8 tool rounds | the variable part |
| `sbx.kill()` | ends billing |

If the run count reaches the hundreds, an E2B template with packages pre-installed
removes the repeated install. Not worth doing below that.

## F4 — the vendor choice has no recorded justification

Searched `01_thesis_research/research-questions/` and `00_thesis_context/`. The model
is a hardcoded constant (`MODEL = "claude-sonnet-4-6"`, line 36) with a price comment
and **no argued basis anywhere**.

This is a genuine gap: a reviewer asking "why this model?" currently has no answer in
the thesis.

See DEC-VENDOR in `task_plan.md` for the options and which arguments hold up. The short
version: ecological validity ("this is what firms deploy") is defensible; "cheaper and
weaker flatters our result" is not, and must not reach the write-up.

## F5 — terminology: traceability vs transparency vs determinism

Brian asked whether "traceability" was the right word, wondering if his colleague meant
something else. **The word is correct** — SRQ2 defines it precisely as *"a recorded
mapping from tool call → forecast value → recommendation"*.

What Brian described (deterministic, non-black-box) is a different property. All three
are separate and worth keeping distinct in the write-up:

| Term | Question | Status here |
|------|----------|-------------|
| **traceability** | where did this number come from? | **implemented** 2026-08-19 (P0037 F12) |
| **transparency / interpretability** | *why* this number? | XGBoost is a black box; SHAP approximates it |
| **determinism** | same input → same output? | already true: fixed seed, temperature 0 |

Only traceability is claimed by SRQ2, and it is now the one that is built.

## F6 — the honest intervals reshape what System A can claim

From P0037 F10/F11: once conformal calibration was moved off test residuals, all 230
served forecasts report `Low` confidence and the median 90% interval spans **3× the
forecast** (Danskvand 11.6×, Energidrikke 5.5×, CSD 3.0×, RTD 2.8×).

**Consequence for this experiment**: "System A is more accurate" is a weak thesis, and
possibly a losing one. The strong version is that System A returns a number *with*
calibrated uncertainty *and* provenance, neither of which self-written code can
produce.

This also makes the comparison fairer — System B is no longer competing against a
precision System A does not actually have.
