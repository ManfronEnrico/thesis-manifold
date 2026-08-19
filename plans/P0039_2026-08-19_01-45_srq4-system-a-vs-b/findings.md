---
pid: P0039
created: 2026-08-19 01:45:00
updated: 2026-08-19 02:05:00
---

# P0039 Findings

## F1 — the harness is further along than the plan files implied

`03_thesis_modelling/scenario_setup/srq4_experiment.py` already implements the full
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

See DEC-VENDOR in `task_plan.md` for the options. The short version: decide on
**ecological validity** ("this is what firms deploy"), which is both defensible and
reportable. Budget is a real constraint but governs *sample size*, not vendor choice —
see F7, which measures it and corrects the framing here.

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

## F7 — API cost is not the deciding factor at this scale (corrects F4's framing)

Brian clarified (2026-08-19) that the cost point was an **internal budget constraint**,
not a reported argument — the API is paid out of pocket, and ~50 prompts are planned
per system to get a stable estimate from non-deterministic responses.

That is a legitimate constraint and normal to disclose. It is also a different claim
from "pick a weaker model so the result looks better", which was never the intent.
F4's framing conflated the two.

**Measured, the constraint turns out to be small.** Order-of-magnitude from the
harness' own token structure, 50 runs per system (100 conversations):

| Model | System A | System B | Total |
|-------|---------:|---------:|------:|
| claude-sonnet-4-6 | $1.05 | $6.38 | **~$7** |
| GPT-5.x class | $0.59 | $3.50 | **~$4** |
| GPT-5-mini class | $0.12 | $0.70 | **~$1** |

Even at 10x, the vendor difference is tens of euros. **So cost should not decide
DEC-VENDOR** — ecological validity should. Cost governs a different question: how many
runs are affordable, which is a sample-size decision and belongs in the methodology as
a stated limit.

**Where the money actually goes**: System B costs ~6x System A per run. It loops
through several tool-use rounds carrying the brand's history in context and re-installs
statsmodels per sandbox, where System A makes a single tool call. If the design grows,
System B is the line item to watch — and an E2B template with packages pre-installed
is the first optimisation.

Real per-run figures come from `--demo` (task 1). The harness already computes cost
per run via `PRICE_IN_PER_M` / `PRICE_OUT_PER_M`, so if the vendor changes, **update
those constants** or every reported cost will be wrong.


## F8 — the blocker was three problems, not one; two are now fixed

F2 said "the only blocker is credentials". That was true of the *symptom* but not
the cause: the `FileNotFoundError` on import masked two further defects that only
became visible once it was cleared. Fixed 2026-08-19 (commit `63c8a6c`):

| # | Defect | Why it was invisible |
|---|--------|----------------------|
| 1 | `.env` read was unguarded and hard-failed on import | it *was* the visible error |
| 2 | `forecast_service.py` path stale since the P0028 train-vs-serve split — the file lives in `model_serving/`, the harness looked beside itself | masked by #1 |
| 3 | `anthropic` and `e2b-code-interpreter` absent from `requirements.txt` **and** from the environment | both imported lazily *inside* the run functions, so they fail mid-run, not at import |

Defect 3 is the same failure mode as the ML block fixed 2026-08-18: a dependency the
code needs, missing from the manifest, hidden behind a lazy import. Worth treating as
a pattern in this repo rather than three coincidences.

**Now verified without any credentials**: the module imports, and
`_eval_forecast("CSD", "HARBOE")` returns
`forecast_units=4,326,970` with a 90% interval of `[3,259,384 – 5,744,233]`.
System A's forecasting core is sound; the remaining blocker is genuinely
credentials alone.

**Caveat on that number**: the interval is roughly ±30%, far tighter than the
median 3x reported in F6/P0037 F11. HARBOE is a large, stable brand. Do **not**
quote it as representative — F6's median is the honest headline figure.

## F9 — the ANTHROPIC_API_KEY in the repo-root .env is an empty placeholder

The root `.env` contains the literal line `ANTHROPIC_API_KEY=` with no value. A
`grep` for the key name finds it and looks like a working credential; it is not.

Two consequences:

1. **The env loader now skips empty values.** Otherwise `setdefault` locks in the
   empty string and a genuinely exported key can never override it, turning a clear
   auth failure into a confusing one.
2. **The handover's claim needs qualifying.** It tells Enrico he "probably already
   has" an Anthropic key because he built System B. If his `.env` carries the same
   placeholder, that is optimistic. He should check for a *value*, not a key name.

`E2B_API_KEY` is absent entirely from both files.

## F10 — Scenario A cannot retrieve the answer, tested adversarially

The held-out months are historical, so Scenario A could in principle look up the
figure instead of estimating it. Tested directly rather than assumed: the model
was asked point-blank to *find* the Nielsen-reported January 2026 unit sales for
a named brand, with web search enabled.

It searched and returned **NOT FOUND**. What it surfaced instead were
annual-report aggregates citing NIQ ("Danish soft drinks +2.6%, FMCG incl. HD,
W16 2026") — category-level growth rates, not brand-level monthly units.

**Why**: Nielsen scanner data is a paid commercial product. Brand x month unit
sales are not published anywhere the model can reach.

**Consequence for the design**: the "do NOT search for a published figure"
instruction was removed from Scenario A's prompt. It was doing no work, and it
made A's prompt structurally different from B's and C's, which is a confound.
`used_web`, the search queries and `retrieval_suspected` are still logged every
run, so the claim rests on evidence rather than on the model obeying an
instruction.

State this in the limitations as a *tested* control, not an assumed one.

## F11 — the prompts were not equivalent; now they are

Found by reading the logged prompts rather than the code. The three scenarios
were receiving materially different instructions:

- A: the question + a paragraph forbidding search
- B: the question + method guidance + the CSV
- C: one bare sentence

Any measured accuracy difference therefore partly reflected **prompt wording**,
not the mechanism under test — which is precisely what the single-variable
design exists to exclude.

Rewritten so all three receive the **same user question verbatim**:

> What will {brand} sell in the {category} category in Danish retail in
> {target}? Give the number, a range, and how confident you are.

Only the capability note differs, and that note *is* the treatment: A is told it
has no internal data, B is given the history and told to run code, C is told a
`forecast_demand` tool exists and not to compute the number itself.

"Do not compute it yourself" is retained for C and must be disclosed: without
it the model may ignore the tool and hand-compute, collapsing C into B.

## F12 — Scenario B's advantage did not replicate; its inconsistency is the finding

Three runs, identical prompt and brand (CSD/HARBOE, target 2026-01):

| Run | B forecast | B's chosen method | B APE | C APE |
|-----|-----------:|-------------------|------:|------:|
| 1 | 4,009,826 | inverse-RMSE ensemble of ETS + regression | 16.1% | 17.5% |
| 2 | 4,143,790 | rolling-origin ensemble, ETS + month/trend | 13.3% | 17.5% |
| 3 | 3,931,319 | log-linear OLS with monthly seasonality | 17.7% | 17.5% |

**Scenario C returned 3,943,859.8 every single time.**

The logs show B genuinely tries hard — ExponentialSmoothing, SARIMAX, ARIMA, OLS
and Ridge appear across its generated code, with rolling-origin backtesting and
inverse-RMSE ensembling. It is not doing something naive.

But it **selects a different model on each run**, and the spread (3.93M–4.14M,
~5%) is comparable to the accuracy gap being measured. The earlier "B beats C"
reading was run-to-run variance in an n=1 sample, not a better method.

This is the consistency metric appearing early, and it favours C on grounds that
survive B occasionally winning on accuracy:

| | Scenario B | Scenario C |
|---|---|---|
| Same answer twice? | no | yes, identical |
| Method | varies per run | fixed, recorded |
| Cost per run | ~$0.27 | ~$0.007 (~40x cheaper) |
| Latency | ~143 s | ~6.6 s (~22x faster) |
| Provenance | none | model, training cutoff, calibration split |

**Do not over-read n=3.** The point is that the design now measures the right
thing; the scaled run settles the magnitude.

## F13 — compute cost is measured in the serving path, not only offline

The thesis claims these models run in a compute-limited environment (~8 GB per
query), so `_eval_forecast` now records peak RAM and wall-clock for the code path
actually used at serve time: **~3-4 MB and ~1.1 s** per forecast, against an 8 GB
budget — about 0.05%.

Offline profiling (`srq1_profiling.py`) independently reports peak fit RAM of
5.5 MB (Ridge), 8.0 MB (LightGBM), 0.1 MB (XGBoost), 0.3 MB (ARIMA).

`tracemalloc` measures Python allocations only, so both figures are lower bounds
on the Python side; they are directly comparable to each other because they
measure the same quantity the same way. Say so rather than implying a total
process footprint.

**Scenarios A and B log no RAM, correctly**: their computation happens on
OpenAI's infrastructure and is already priced into the token and container
charges. There is no local process to measure, and inventing one would be
guesswork. The honest cross-scenario compute comparison is therefore
**cost and latency**, both of which are measured — with the asymmetry itself
being a finding, since C's compute is ours to control and B's is not.
