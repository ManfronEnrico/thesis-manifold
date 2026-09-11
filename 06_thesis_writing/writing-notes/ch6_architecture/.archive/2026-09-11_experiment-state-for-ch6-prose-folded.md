---
name: 2026-09-11_experiment-state-for-ch6-prose
description: RULE - What the first paid five-scenario run (2026-09-11) establishes, and the four Chapter 6 claims it contradicts or outruns. Read before writing Ch6 prose.
category: reference
applies-to: [ch6-architecture, ch8-experimental-evaluation, ch10-limitations]
triggers: [writing Ch6 prose, describing the tool interface, describing the code-as-action baseline, quoting decoding settings, quoting the scenario count, writing the interval limitation, defending conformal calibration]
created: 2026_09_11-17_30
updated: 2026_09_11-17_30
---

# Experiment state for the Chapter 6 prose pass

**Snapshot this is written against:** `2026-09-11_15-41_ch5-applied-review`.
**Repository state:** `e53f316`, all work pushed.
**Notes swept:** `sample-size-and-tool-interface-rationale.md` — not applied, left
in place, and nothing here duplicates it. Its own banner already warns that every
count in it is superseded; that warning still stands and is unrelated to this note.

Chapter 6 is a design specification, and its §6.1 note is careful to say which
layers are implemented. **All of them now are.** The first paid five-scenario run
completed on 2026-09-11. This note says what that establishes, and flags four
places where the chapter's current text no longer matches the artefact.

---

# What the run established

CSD / HARBOE, target month 2026-03, held-out actual 6,365,900 units. One run per
scenario. **$1.83 billed**, reconciled against the OpenAI organisation costs
endpoint, not estimated.

| Scenario | What it has | Forecast | Error | Latency | Cost |
|---|---|---|---|---|---|
| A | no firm data, web search | 3,900,000 | 38.7% | 102 s | $0.52 |
| B | history + code sandbox | 6,300,000 | **1.0%** | 98 s | $0.23 |
| C | trained model behind the tool | 4,969,050 | 21.9% | 8 s | $0.01 |
| D | B's task, on Prometheus | 6,463,116 | **1.5%** | 145 s | $0.55 |
| E | C's task, on Prometheus | 4,969,050 | 21.9% | 46 s | $0.21 |

Every arm produced a point forecast, a 90% range, a stated confidence, a planner
recommendation and a machine-readable sentinel. All five answered about the same
month. Verified individually, not assumed.

**Single brand, single month, single run. None of these numbers is a result
yet.** They are sufficient to say the pipeline works end to end, and to flag one
direction that needs explaining before the funded set.

---

# Fix 1 — §6.5 states a decoding setting the model does not support

### Anchor

**Section 6.5 The Bounded Tool-Using Agentic Layer**, second paragraph, the
sentence beginning *"The layer embodies a delegation-over-generation
principle"*. The clause to change is at the end of that paragraph:

> "Decoding is configured for reproducibility (temperature zero)."

**Next sentence begins:**

> "This separation of a generative orchestrator from deterministic predictive
> components..."

### Action

REWORD.

#### Replace with

> "Decoding parameters are left at the provider's defaults: the pinned model
> does not expose temperature or top-p, so reproducibility is pursued through a
> fixed model snapshot and a recorded prompt registry rather than through
> decoding control."

### Note — why this matters more than a wording fix

`temperature=0` is **not settable on this model**. The harness records the fact
on every run as `temperature/top_p unsupported by the model; defaults used`, and
`verify_setup.py` asserts that the recorded claim matches reality before any
paid run. The chapter currently claims a control the artefact does not have.

An examiner reading "temperature zero" will expect determinism. What the
artefact actually offers is a pinned dated snapshot (`gpt-5.5-2026-04-23`) plus
a SHA-256 prompt-schema identity recorded on every run — which is a *different*
and arguably stronger reproducibility story, because it survives a provider
changing its defaults. Claim the one that is true.

---

# Fix 2 — §6.4's reliability claim is now measured, and should say so

### Anchor

**Section 6.4 The Structured Forecast-Tool Interface (SRQ2)**, the bolded
paragraph beginning:

> "**Reliability**, by validating the agent's stated numbers against the source
> forecast values before delivery, so that the agent reports the model's numbers
> rather than its own."

### Action

INSERT AFTER — a single sentence appended to that same paragraph.

#### Replace with

> "In the pilot run this validation was exercised: the agent's reported figure
> and the model's own output agreed exactly, and the recorded tool-call span
> confirmed that the agent queried the series it was asked about at the intended
> horizon."

### Note — the evidence, and why it is worth one sentence

The claim in the chapter is a *design intention*. It is now a measurement, and
it is cheap to say so:

- Scenario C's answer and Scenario E's answer were **identical to the decimal**
  (4,969,049.5) despite different orchestrators, because both are the same
  model call relayed by different agents.
- The tool-call span recorded `args_match_request=True` and `months_ahead=3`,
  i.e. the LLM queried the right brand, the right category, and the right
  horizon.

Do **not** overclaim from one run. "Was exercised" is the right strength; "is
guaranteed" is not.

---

# Fix 3 — §6.4 and §6.7 carry stale cross-references

### Anchor

Two sentences, in different sections, both ending in a section number:

**§6.4**, last paragraph:
> "...it is instead the baseline against which the artefact is compared (Section 5.7)."

**§6.2**, the paragraph beginning *"The layers are coordinated by a lightweight
Python coordinator"*:
> "...that production substrate is the object of the integration-readiness assessment (SRQ3, Section 5.6), not the evaluated implementation."

### Action

REWORD both, in one pass.

- `(Section 5.7)` → `(Section 6.7)`
- `(SRQ3, Section 5.6)` → `(SRQ3, Section 6.6)`

### Note

These are Ch5/Ch6 swap residue: the sections they point at are 6.7 and 6.6 in
this document. The prose around them is correct; only the numbers are wrong.
**Word will not update these automatically** — they are typed text, not field
references.

⚠️ §6.1 also says the substrate is *"benchmarked across the five categories"*
and §6.10 repeats *"benchmarked in Chapter 6"*. The scope is **four** categories
(CSD, Danskvand, Energidrikke, RTD), and the substrate chapter is Chapter 5.
Establish what "five" was counting before amending — the dropped `totalbeer`
category is the likely origin, and if so the correct word is simply "four".

---

# Fix 4 — §6.7 describes three scenarios; there are five

### Anchor

**Section 6.7 The Code-as-Action Baseline (SRQ4)**, first paragraph, the
sentence beginning:

> "To evaluate whether dedicated-model integration is warranted at all, the
> architecture includes a **code-as-action baseline**: a general-purpose LLM
> that, given the same data access and the same prompts, writes, executes, and
> self-corrects its own forecasting and analysis code in a sandboxed environment
> (for example, E2B as it is used in our testing scenarios), without a dedicated
> pre-built model (Wang et al., 2024)."

### Action

BLOCKED — do not rewrite this yet. See the note.

### Note — what changed, and why the rewrite should wait

The chapter describes a **two-way comparison**: artefact versus code-as-action
baseline. The experiment is now a **five-rung ladder**, and the addition is
load-bearing rather than cosmetic:

| | scenario | adds |
|---|---|---|
| A | plain LLM | — |
| B | + history and a code sandbox | what data access buys |
| C | + the trained model behind the tool | what the artefact adds |
| D | B's task on Prometheus | the production orchestrator |
| E | C's task on Prometheus | both, on production |

**B→C and D→E are the same intervention on two different orchestrators.** Their
agreeing is a materially stronger claim than either alone, and it is the reason
D and E exist. The pilot supports this: B and D landed within 0.5 pp of each
other, and C and E were identical.

One factual correction for whenever this is rewritten: the sandbox is
**OpenAI's Code Interpreter**, not E2B. E2B is not used anywhere in the harness.

**Why blocked:** a sixth and seventh rung (an arm holding data, code *and* the
model simultaneously) is under active consideration and would change what this
section enumerates. Rewriting now risks rewriting twice. The decision is
expected before the funded set.

---

# The finding Chapter 6 should be ready for

**On this brand-month, the code-writing scenarios beat the trained model by
roughly twenty percentage points**, on both orchestrators.

This runs against the direction §6.4 implies when it adopts function-calling
"rather than code-as-action". It does **not** invalidate that choice, and the
chapter's own reasoning is the defence: §6.4 justifies the interface on
**reliability, reproducibility and auditability**, not on accuracy. The pilot is
consistent with that framing — Scenario C answered in 8 seconds for $0.01 with a
fully traceable tool call, against 98 seconds and $0.23 for B.

Two things to hold in mind while writing:

1. **Do not pre-emptively soften §6.4.** One brand-month is not evidence, and a
   chapter that hedges against a result it has not yet reported reads as
   uncertain rather than careful.
2. **Do not add an accuracy claim to §6.4 either.** The current text does not
   claim the interface is more accurate. That restraint is now load-bearing and
   should survive the pass.

Why B did well, from its cached code: it fitted **exponential smoothing across
four configurations, SARIMA over a 72-model grid, and OLS/Ridge with month
dummies and promotion intensity**, backtested the lot at two earlier cutoffs,
then reported the **median across models**. That is a small automated model
competition, not a naive extrapolation. Scenario C is a single tuned booster
chosen category-wide. The comparison may be measuring *per-series adaptation*
rather than *code versus model*, which is a Chapter 8 discussion point and a
Chapter 10 limitation, not a Chapter 6 one.

---

# The interval limitation — settled, with numbers

Relevant to §6.4's **Uncertainty** paragraph, which currently says interval
calibration "is treated as a design target, not an empirically validated
property of the current prototype".

**That sentence is now too weak in one direction and too strong in the other,
but it should NOT be changed in this pass.** The calibration has been validated
and the finding belongs in Chapter 8 and Chapter 10, not here. Recorded so the
prose does not accidentally contradict it:

- The split conformal interval **achieves its marginal guarantee**: observed
  coverage 85.1–92.5% against a 90% target across four categories.
- It is nonetheless **uninformative per brand**: median width 5.9–18.2x the
  point forecast. Scenario C's HARBOE interval was 654,488 to 37,726,335.
- Cause: one quantile is pooled over brands spanning **six orders of
  magnitude**, and each brand contributes only 6–7 validation months.
- **Three alternative schemes were implemented and measured. None improved
  coverage and width together in more than two of four categories.** Size
  bucketing fails because only 0–4 brands per category exceed 1M units/month
  (RTD has none). Per-brand normalisation covers 68.8–80.2%.
- It is a **sample-size limit of the reduced dataset**, not a defect, and not
  fixable by retraining.

Full measurements and the script that produced them:
`plans/P0049_2026-09-07_17-50_finalizing-experiments/findings.md` F50 and F52,
and `2026-09-11_eval_calibration_schemes.py` in the same folder.

A tested negative result is a contribution. It is also the honest answer to
"why is the interval so wide", which a reader will ask on seeing Table C.

---

# Deferred

Added to `deferred-structural-decisions.md` rather than decided here: whether
§6.7 keeps the "baseline" framing at all once the ladder has five or seven
rungs. "Baseline" implies one comparator; the design now has a ladder in which
every rung is a comparator for the one below.
