---
name: p0042-findings
description: RULE - Measured cost findings and the frozen SRQ4 sampling design for the funded phase.
category: reference
applies-to: [srq4, scenario_setup, 04_thesis_results]
triggers: [planning a paid scenario run, budgeting API spend, writing the SRQ4 methodology]
created: 2026_09_01-00_00
updated: 2026_09_01-00_00
---

# P0042 — Findings

## F1. The billed/estimate multiplier is scenario-specific, not global (2026-09-01)

The 2026-08-19 reconciliation showed $3.08 estimated against $13.77 billed — a
4.47x gap. **That ratio must not be applied uniformly.** It is composed of two
surcharges the response API does not report per call, and each belongs to one
scenario:

| Surcharge | Billed | Which scenario incurs it |
|---|---:|---|
| web search tool calls | $1.06 | `A_plain` only |
| Code Interpreter container | not itemised per response | `B_data` only |

`C_model` issues one tool call (578 input tokens, 129 output), runs no sandbox
and performs no web search. **Its logged estimate is therefore close to its true
cost**, while A and B carry a real multiplier. The $13.77 also spans the whole
billing window, including the discarded DKK-confound run.

**Implication:** budgeting every scenario at 4.5x overstates the cost of the
cheapest arm by roughly two orders of magnitude and would force an unnecessarily
small experiment. Budget A and B at the multiplier; budget C near its estimate.

## F2. Measured per-run cost, from 29 logged non-zero runs (2026-09-01)

| Scenario | n | mean est. | median est. | notes |
|---|---:|---:|---:|---|
| `A_plain` | 17 | $0.4277 | $0.4558 | + web search surcharge |
| `B_data` | 6 | $0.2664 | $0.2669 | + container surcharge |
| `C_model` | 6 | $0.0068 | $0.0068 | no surcharge |

Source: every `runs.csv` under `04_thesis_results/srq4/`, zero-cost rows excluded.
These are measurements, not estimates — do not re-derive them.

**`A_plain` is ~63x the cost of `C_model` per run.** That ratio is the single most
important number for allocating the budget.

## F3. Model pinning verified clean (2026-09-01)

All 30 raw response files and all 27 CSV rows across the three pilot run folders
carry `gpt-5.5-2026-04-23` at `reasoning_effort=medium`. No endpoint drift
occurred during the pilot. Re-check this after any multi-day run before analysing.

## F4. Pre-flight passes on everything except credentials (2026-09-01)

`verify_setup.py` reports PASS on: feature matrices (all 4 categories), **leakage
guard** (8 brand-series, target month absent from every history), **all scenarios
target the same month** (history `2026-01` == tool `forecast_month=2026-01`), tool
payload completeness, and target month named in every prompt. Decoding claim
matches reality (temperature not settable on this model).

The two FAILs are `OPENAI_API_KEY` absent from the shell environment — an env
issue at launch time, not a configuration defect.

## F5. Stratified selection resolves to real brands across the volume range

`--brand-strategy stratified` picks highest / median / lowest-volume among brands
with a fully non-zero test window (so every cell yields a defined APE):

| Category | Scorable pool | Stratified pick |
|---|---:|---|
| CSD | 76 of 95 | HARBOE, NIKOLINE, VOELKEL |
| danskvand | 21 of 29 | HARBOE, PERRIER, THY |
| energidrikke | 27 of 44 | RED BULL, STATE VITAMIN, MANA ENERGY |
| RTD | 44 of 62 | BREEZER, FUNKIN, AERIS |

**Expect the stratified aggregate to look worse than the pilot's figures.** The
pilot measured HARBOE and COCA COLA — ranks 1 and 2 of 95. VOELKEL is rank 76.
Thin series are a harder forecasting problem for *every* scenario; a narrowing
B/C gap there is a finding to report, not a defect. Do not present the stratified
aggregate beside the pilot's volume-based APE as though they measure the same
population.

## F6. E2B sandbox cost for D/E is NOT yet measured (2026-09-01)

`D_prometheus` is the D-analogue of `B_data`: the engine writes and executes code
in an E2B sandbox. E2B bills **sandbox runtime**, a resource `srq4_experiment.py`
cannot see. `measure_e2b_cost.py` exists specifically to measure it.

**Do not commit a D/E repeat count before running it.** Assuming D is as cheap as
C would repeat, in a more expensive place, exactly the estimate-vs-billed error
F1 documents.

## F7. E2B sandbox cost MEASURED — negligible, and not the D/E cost driver (2026-09-01)

`measure_e2b_cost.py` run against E2B's **default base image** (no template):

```
[1] sandbox created in   0.69s
[2] code executed in     0.99s
[4] sandbox killed in    0.21s
BILLABLE WALL CLOCK:     1.88s for one sandbox lifecycle
```

Converted at E2B's published per-second rates (vCPU $0.000014/s + RAM
$0.0000045/GiB/s):

| Sandbox | Rate/s | 1.88s lifecycle | held 120s | held 600s (max) |
|---|---:|---:|---:|---:|
| base 2vCPU/1GiB | $0.0000325 | $0.00006 | $0.0040 | $0.0196 |
| prometheus 4GiB | $0.0000740 | $0.00014 | $0.0090 | $0.0445 |

**Even the worst case — a 4GiB template sandbox left idle for the full 600s
timeout — costs under 4.5 cents per run.** Against `A_plain` at $0.4277 and
`B_data` at $0.2664, E2B is not a cost driver. It is noise.

**Conclusion for gate 1:** E2B does not constrain the D/E repeat count. Choose it
to match the B/C core block (3 brands x 10 reps) for comparability, and budget
D/E on **LLM tokens**, which is where the money actually is. This supersedes F6's
caution — the number now exists.

## F8. The default sandbox is missing every library Prometheus needs (2026-09-01)

The probe's availability check, which is the more consequential half of the run:

```
pandas 2.2.3          <- present
MISSING pyodbc        <- warehouse driver
MISSING sqlalchemy
MISSING statsmodels
MISSING xgboost
MISSING prophet
```

Only `pandas` and `numpy` exist in the base image. **`pyodbc` absent means the RU
warehouse is unreachable from a default sandbox** — a warehouse query would fail
*inside* the sandbox rather than at connection time, which is the hard-to-diagnose
failure mode F27 warned about.

**Implication:** `PROMETHEUS_TEMPLATE_ID` (or an equivalent custom template) is
**required** for `D_prometheus` if D is to query the warehouse. F29's correction
(that `AsyncSandbox.create(None, ...)` is legal and the template is optional) is
true about the *API* but not about *capability* — the call succeeds and yields a
sandbox that cannot do the work.

The template build cost (apt-get + five pip layers on a 4GiB box) is a one-off and
still unmeasured. It is the remaining E2B unknown, not per-run cost.

## F9. `E_prometheus_model` requires no sandbox at all — E is not D-minus-tokens

Corrects a loose phrasing from this session's discussion. `forecast_demand` runs
**in-process**, not in the sandbox (P0040 F27's table states this explicitly):

| Scenario | Needs E2B? | Why |
|---|---|---|
| `D_prometheus` | **yes** | code-as-action *is* sandbox execution |
| `E_prometheus_model` | **no** | the tool executes in-process |

So E's saving over D is **not** a shorter sandbox lifetime — it is the absence of
a sandbox plus the collapse in reasoning tokens (C spent 20 reasoning tokens
against B's 5,634, a 280x drop). E should mirror that.

**Watch for this during B4:** if `E_prometheus_model` creates a sandbox anyway,
the engine is provisioning one per conversation regardless of whether the tool
path uses it. That would be a finding about the engine's architecture, and it
should be logged rather than optimised away.
