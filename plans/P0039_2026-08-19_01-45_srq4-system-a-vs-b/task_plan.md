---
pid: P0039
created: 2026-08-19 01:45:00
updated: 2026-08-19 01:45:00
status: focus
focus_detail: "THE THESIS PREMISE. Does exposing a trained model as a tool improve an LLM's answers, versus letting it write its own forecasting code? Harness exists and is sound; blocked only on 03_thesis_modelling/.env (LLM key + E2B_API_KEY). Open decision DEC-VENDOR: which LLM is primary, and on what stated grounds. Under a month to submission with 120 pages outstanding, so scope is deliberately narrow: CSD primary, one category as robustness."
---

# P0039 — SRQ4: dedicated model vs code-as-action

## Goal

Answer the thesis' central question with evidence:

> Does having a trained forecasting model **available as a tool** improve an LLM's
> answers, compared with giving the LLM the raw data and letting it write its own
> forecasting code?

**One variable under test: how the agent produces a forecast.** Everything else —
model, prompts, temperature, brand, horizon — held constant.

| | System A (Oracle) | System B (Prometheus-style) |
|---|---|---|
| Mechanism | calls a `forecast_demand` tool | writes and runs its own code |
| Backing | pre-trained XGBoost via `forecast_service.py` | brand history in an E2B sandbox |
| Code written by the LLM | none | all of it |

## Why this plan exists now

P0038 finished the data pipeline and P0037 delivered the serving interface (tasks 3,
4, 7). Every dependency this experiment had is discharged **except credentials**. With
under a month to submission and 120 pages unwritten, this is the last piece of
technical work that the thesis genuinely requires.

## Context inherited (do not re-derive)

| Fact | Where it came from |
|------|--------------------|
| Feature matrices, 4 categories × 2 horizons, verified 8/8 | P0038 |
| H=3 is the primary horizon | DEC-HORIZON |
| `forecast_service.build_service()` produces 230 forecasts across 4 categories | P0037 F13 |
| Every forecast carries a `trace` block (model, cutoff, calibration split) | P0037 F12 |
| Intervals are honestly calibrated and **wide** — median 3× the forecast | P0037 F10, F11 |
| Prophet diverges on individual series; report medMAPE, not WMAPE | P0038 F72 |

## Open decisions

### DEC-VENDOR — which LLM is primary? (Brian + Enrico)

**Status: OPEN. Blocks task 1.**

The harness hardcodes `claude-sonnet-4-6` (line 36) and **no justification is recorded
anywhere in the thesis docs**. That is an unargued default, and unargued defaults are
what reviewers probe.

Brian favours GPT. Two of his reasons are not equally strong:

| Argument | Verdict |
|----------|---------|
| "GPT is what most firms actually deploy" | **Strong.** Ecological validity. If the thesis advises firms to expose models as tools, it matters that the finding holds for the LLM they use. |
| "GPT is cheaper and less accurate, which improves our results" | **Do not use.** Choosing a weaker comparator so the intervention looks better is the same move as capping Prophet, which was rejected on 2026-08-18. It discredits the comparison if spotted. |

**A stronger framing exists**: the premise is about *model availability*, not about any
vendor. If it holds only for one, it is a vendor finding, not a thesis. Running the
full experiment on one and a cross-check on the other converts a single-vendor result
into a claim about LLMs.

**Implementation note**: the harness is written against Anthropic's API shape (message
format, tool-call structure, token accounting). A GPT run needs a small adapter at the
two call sites (lines ~149 and ~181), which are near-identical, so one abstraction
covers both.

**Decide before task 1**, because it determines whether the smoke test runs as-is or
after the adapter.

### DEC-SCOPE-SRQ4 — how much to run? (settled 2026-08-19)

**CSD primary**, one other category as robustness.

Stated grounds: **CSD has the most brands (95 vs Danskvand's 29)**, so per-brand
results carry the most statistical weight. This is deliberately a power argument, not
a familiarity one — "we know CSD best" invites "so you tuned for it".

Brands, prompts per brand, and repeats per prompt must be **fixed in writing before
running** and not changed afterwards. Changing the design after seeing results forfeits
the claim.

## Phases

| Phase | Focus | Tasks |
|-------|-------|-------|
| 1 | Unblock and smoke-test | 1, 2 |
| 2 | Instrument before running | 3, 4 |
| 3 | Run and analyse | 5, 6 |
| 4 | Write | 7 |

## Tasks

| # | Task | Phase | Depends on | Status |
|---|------|-------|-----------|--------|
| 1 | Add `.env`; run `--demo` end to end | 1 | DEC-VENDOR | pending |
| 2 | Record real cost + latency per run; sanity-check the schedule | 1 | 1 | pending |
| 3 | Implement the System B failure taxonomy | 2 | 1 | pending |
| 4 | Fix the experiment scope in writing (brands/prompts/repeats) | 2 | 2 | pending |
| 5 | Run the experiment; log everything, keep raw responses | 3 | 3, 4 | pending |
| 6 | Analyse against the pre-stated claims | 3 | 5 | pending |
| 7 | Write the results section; then unpause P0034 | 4 | 6 | pending |

### Task 1 — Unblock

`03_thesis_modelling/.env`:

```
ANTHROPIC_API_KEY=...   # or OPENAI_API_KEY, per DEC-VENDOR
E2B_API_KEY=...
```

Then:

```bash
python 03_thesis_modelling/model_training/srq4_experiment.py --demo
```

One brand, one prompt, both systems. **Do not skip to the full run.** This is the step
that reveals whether the sandbox works, what a run costs, and how long it takes — on
day one rather than day twelve.

### Task 3 — The failure taxonomy (must precede any real run)

System B writes its own code, so it fails in ways System A cannot. **Those failures are
the finding**, not noise: "code-as-action failed 12% of the time" is a stronger claim
about production readiness than a small accuracy gap.

Classify every run:

| Class | Meaning |
|-------|---------|
| `ok` | produced a parseable numeric forecast |
| `code_error` | the model's code raised |
| `no_forecast` | ran, but never printed the sentinel |
| `timeout` | exhausted the 8 tool-use rounds |
| `implausible` | returned a number outside a stated sanity bound |

`implausible` exists because of P0038 F72: Prophet forecast 101M against 301k actual.
Averaged in, one such answer destroys a mean; recorded as a class, it is a result.

**Retrofitting this after the runs means re-running them.**

### Task 6 — Analyse against pre-stated claims

Four candidate claims. Instrumented status differs, so state only what is measured:

| Claim | Evidence | Status |
|-------|----------|--------|
| A is more **accurate** | forecast error vs held-out actual | instrumented |
| A is more **consistent** | spread across repeats at temperature 0 | instrumented |
| A is **cheaper / faster** | tokens and latency | instrumented |
| A is more **traceable** | model id, cutoff, calibration split | **now implemented** (P0037 F12) |

### A framing worth carrying into the write-up

System A's honest pitch is **not** "more accurate". P0037 F11 established that the
intervals are wide — median 3× the forecast — once calibrated honestly.

The defensible pitch is **a number, plus calibrated uncertainty, plus provenance**.
System B can produce a number; it cannot produce the other two, because self-written
code has no recorded lineage and no calibration set. That argument survives System B
occasionally winning on accuracy, which a pure accuracy claim would not.

## Definition of done

- `--demo` runs both systems end to end
- Failure taxonomy recorded for every run
- Scope fixed in writing before running, and unchanged afterwards
- Results reported against pre-stated claims, with System B failures as a category
- Prophet/interval caveats carried into the limitations section
- P0034 unpaused with final numbers

## Explicitly out of scope

Further EDA work. The pipeline is verified and its remaining gap is reporting-level
(cross-brand heterogeneity is not quantified — P0031 task 3, recorded as a
limitation). With the deadline where it is, more EDA trades directly against the 120
pages and against this experiment.
