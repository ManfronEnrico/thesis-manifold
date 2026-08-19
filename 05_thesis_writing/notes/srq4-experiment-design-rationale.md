---
name: srq4-experiment-design-rationale
description: RULE - SRQ4 experimental design decisions and their justifications - three-arm information ladder, single prediction prompt archetype, model choice, cost instrumentation, and what was deliberately dropped from the original spec. Write-up material for Ch3/Ch5/Ch8/Ch10.
category: reference
applies-to: [ch3-methodology, ch5-framework-design, ch8-evaluation, ch10-limitations]
triggers: [writing SRQ4 methodology, defending model choice, defending arm design, justifying sample size, writing cost analysis, defending prompt set, explaining what was dropped]
created: 2026_08_19-14_00
updated: 2026_08_19-14_00
---

# SRQ4 Experiment Design — Write-Up Rationale

Decisions taken 2026-08-19 (Brian), revising the 2026-06-19 specification
(`00_thesis_context/methodology/srq4-evaluation-protocol.md`) and the
2026-07-12/13 decisions (DEC-LLM, DEC-ARMS). Each section states **what was
decided, why, and what the defensible challenge is** — the challenges are the
part that gets asked at defence.

---

## 1. Three arms as an information ladder (revises DEC-ARMS)

The original framing was A vs B with C as an optional "floor". That conflates two
distinct things. Reframed, the three arms isolate **two separate increments**:

| Arm | Data access | Forecasting mechanism | Isolates |
|-----|-------------|----------------------|----------|
| **C** | none (open web only) | the LLM's own judgement | what the LLM knows *without* firm data |
| **B** | Nielsen history in a sandbox | writes + runs its own code | what **data access alone** buys |
| **A** | Nielsen history + trained model as a tool | calls `forecast_demand` | what **model integration** adds on top |

**Why this matters for the claim**: a two-arm A-vs-B design cannot separate
"having the data" from "having a trained model on the data". The ladder can.
C to B measures the value of data access; B to A measures the value of the thesis
artefact specifically. The thesis contribution is the second increment, and
without arm C a reviewer can argue the whole effect is just data access.

**Arm C is not a null condition.** With web access it will find public
information — company annual reports, market commentary, stock coverage — and
produce a real, confident forecast. How wrong that is, and how confidently
wrong, is the finding. This is also the arm that answers the practitioner
question *"why can't I just ask ChatGPT?"*, which makes it rhetorically the most
useful arm even though it will be the least accurate.

**Stated limitation (do not let a reviewer find this first)**: because arm C can
browse, it is not a clean "no information" floor. It may encounter genuinely
relevant public data about the brand or category. This *understates* the measured
value of data access (C to B), so the direction of the bias is conservative with
respect to our own claim — say so explicitly.

---

## 2. One prompt archetype: prediction only (replaces the ~50-prompt taxonomy)

The 2026-06-19 spec proposed ~50 prompts across six archetypes: descriptive,
multi-entity comparison, temporal, anomaly, forecasting, forecast-to-decision.
**Approximately 34 of those 50 do not involve forecasting at all** — they are
descriptive queries answerable by ordinary dataframe work.

**Decision: use a single prediction prompt template.**

Reasoning:

1. **The thesis is about prediction.** SRQ4 asks whether dedicated forecasting
   models improve forecast-informed decision support. Descriptive prompts
   ("what was total volume last quarter") test database querying, not
   forecasting.
2. **The non-forecasting prompts dilute the effect.** On those prompts Arm A's
   `forecast_demand` tool is irrelevant — both arms do the same work with the
   same capability. Averaging them into a headline number shrinks any real
   effect toward zero on two-thirds of the sample.
3. **A diluted result is harder to defend, not easier.** "A beats B by 4 points
   across a mixed prompt set" invites the question of where the effect actually
   lives. "A beats B on the prediction task the artefact is built for" is a
   direct answer to the research question.

**What is given up**: the ability to claim tool availability does no *harm* on
non-forecasting tasks. That is a real question but it is not the SRQ4 question,
and it belongs in future work.

---

## 3. Sample design: brands x repeats, not one brand x many repeats

The initial instinct was one prompt repeated ~50 times on one brand, to average
over LLM non-determinism. **Revised to ~10 brands x 5 repeats** (same total run
count per arm).

**Why**: repeating one brand 50 times measures non-determinism precisely but
confounds the result with that brand's characteristics. A large, stable series
(e.g. HARBOE) is easy to forecast; a small volatile one is not. A finding from a
single brand is a finding about that brand.

Ten brands x five repeats retains enough repetition to estimate run-to-run
spread (the *consistency* metric) while making the accuracy claim
cross-sectional. Same cost, materially harder to attack.

**Brand selection must be stated in advance and not changed after seeing
results.** Selecting top-N by volume would bias toward easily-forecast series —
prefer a stated stratification across volume/volatility.

---

## 4. Base model: `gpt-5.5-2026-04-23` (confirms DEC-LLM)

DEC-LLM (2026-07-12) fixed the base LLM as gpt-5.5 on ecological-validity
grounds: it is the production model of the agentic system Arm B represents.
Re-examined 2026-08-19 against the current model landscape and **confirmed**.

**Use the dated snapshot, not the `gpt-5.5` alias.** An alias silently
re-points; a dated snapshot is citable and reproducible. Verified present on the
project account 2026-08-19.

Reasoning for not moving to the newer 5.6 line:

1. **Construct validity** — Arm B is meant to represent the production agent.
   Using its production model is more defensible than retrospectively picking
   the newest release.
2. **Experimental isolation** — changing the base model changes coding
   competence and tool-use reliability, which are the very mechanisms that
   produce the between-arm difference.
3. **Reproducibility** — the 5.6 line exposes no dated snapshots.
4. **Researcher degrees of freedom** — switching models after preliminary runs
   looks outcome-contingent unless a migration rule was fixed beforehand.
5. **No cost advantage** — 5.5 and 5.6-sol carry the same published token rates.

**Optional**: a smaller, explicitly labelled robustness replication on
`gpt-5.6-sol`. It must not replace the primary analysis.

**Correction to note**: the GPT-5.6 line comprises three variants —
`gpt-5.6-luna`, `-sol`, `-terra` (cost/capability tiers, not task
specialisations). There is **no plain `gpt-5.6` model ID**; it returns 404 on
this account, contrary to some vendor documentation.

### Parameters that must be frozen and reported

Beyond temperature, the Responses API exposes settings that materially change
cost and behaviour and default silently:

- `reasoning.effort` — **defaults to `"medium"`**. In a trivial test call, 66 of
  73 output tokens were *reasoning* tokens, billed at the full output rate.
  Freeze and report this.
- `service_tier` (default `"default"`), model snapshot, tool definitions, SDK
  version, container memory limit, execution dates.

**Temperature 0 does not guarantee identical outputs.** This is why run-to-run
consistency remains a meaningful measured outcome rather than an assumed
constant.

---

## 5. Execution environment: Code Interpreter, not hosted shell

Arm B runs in the hosted `code_interpreter` tool (`container: auto`), not the
hosted shell.

**Why**: a shell grants arbitrary terminal access — package installs, network,
multi-file projects — that arms A and C do not have. That would move a second
variable alongside the one the design isolates. Code Interpreter is the tight
analogue of the intended condition: *a Python sandbox with a dataframe in it*.

It also protects the failure taxonomy. Arm B's failure modes are part of the
result; a shell environment lets the model work around its own failures
(retry installs, shell out), suppressing exactly the signal being measured.

**Each observation must start from a fresh container.** Reusing a live container
across runs would allow state to carry between observations.

---

## 6. Cost and latency instrumentation

The SRQ4 wording is *"at justified cost and latency"*, so cost is a **primary**
outcome, not the secondary metric the 2026-06-19 spec made it.

Measured properties of the Responses API (verified 2026-08-19):

| Quantity | Available? | Where |
|----------|-----------|-------|
| input / output tokens | yes, exact | `response.usage` |
| cached input tokens | yes | `usage.input_tokens_details.cached_tokens` |
| **reasoning tokens** | yes, broken out | `usage.output_tokens_details.reasoning_tokens` |
| wall-clock latency | yes | measured locally |
| container id | yes | `code_interpreter_call.container_id` |
| **container duration / memory / charge** | **no** | absent from the response |

`response.tool_usage` reports `image_gen` and `web_search` only — there is **no
`code_interpreter` entry**. `response.billing` carries only `{"payer": ...}`.

**Consequence**: token cost is deterministic per run; container cost is not
derivable from the response object. Container charges are published per
container-session (by memory tier, billed by the minute with a minimum), and
appear in the organisation usage endpoint under
`assistant_code_interpreter_data` — which requires an admin-scoped key, not a
project key.

**Approach adopted**: log a programmatic per-run token cost from `usage`, plus a
container-cost *estimate* from wall-clock against the published rate, then
**reconcile the total against the billing export** at the end of the run. Report
the reconciled figure; label the per-run number as an estimate.

**Only Arm B incurs container charges** — that asymmetry is part of the treatment
and belongs in the arm-level cost comparison, not netted out.

---

## 7. LLM-as-judge: dropped

The 2026-06-19 spec included an optional LLM judge for qualitative dimensions
(clarity, actionability). **Dropped 2026-08-19.**

Reasoning:

1. **It does not test the hypothesis.** SRQ4 asks about *correctness,
   consistency, replicability, cost and latency*. All five are measurable
   programmatically against ground truth. "Clarity" is not in the research
   question.
2. **It adds an attack surface for no claim strength.** A defensible judge
   protocol requires cross-family selection, blinding, order randomisation, a
   rubric, and human-validated agreement statistics (kappa or ICC) on a
   stratified subset. That is substantial work defending a measurement that does
   not answer the question. Nobody can attack MAPE against a held-out actual on
   the same grounds.
3. **Scope.** With the submission deadline where it is, this is the cleanest
   available cut that costs nothing in claim strength.

**If arms A and B land on similar accuracy**, the fallback is *not* "A's answers
read better". It is the structural argument: A returns a number **with
calibrated uncertainty and recorded provenance**, neither of which self-written
code produces. That argument survives arm B occasionally winning on accuracy,
which a pure accuracy claim would not.

**Consequence**: no judge means no cross-family judge requirement, which removes
the only methodological reason to retain a second LLM vendor.

---

## 8. What the intervals can and cannot claim

Carried from P0037 F10/F11 — relevant here because it constrains what Arm A is
allowed to claim.

Once conformal calibration was moved off test residuals onto validation
residuals, all 230 served forecasts report **Low** confidence and the median 90%
interval spans roughly **3x the point forecast** (by category: Danskvand 11.6x,
Energidrikke 5.5x, CSD 3.0x, RTD 2.8x).

**Do not quote a single brand as typical.** A spot check on CSD/HARBOE returned
a 90% interval of roughly +/-30% — far tighter than the median, because HARBOE is
large and stable. The median is the honest headline.

**Consequence for the SRQ4 write-up**: "System A is more accurate" is a weak and
possibly losing thesis. The defensible claim is *a number, plus calibrated
uncertainty, plus provenance*.

---

## 9. Open items

| Item | State |
|------|-------|
| Verified token pricing for `gpt-5.5-2026-04-23` | **unverified** — no pricing endpoint exists on the API; vendor-quoted figures must be checked against the published pricing page before entering any cost table |
| `reasoning.effort` value to freeze | not yet chosen (currently defaulting to `medium`) |
| Brand selection + stratification for the 10 brands | not yet fixed in writing |
| Admin-scoped key for billing reconciliation | not yet obtained; project key returns 403 on `/v1/organization/costs` |

---

## Related

- `00_thesis_context/methodology/srq4-evaluation-protocol.md` — the 2026-06-19 spec this revises
- `user-docs/handovers/2026-07-13_harness-and-srq4-decisions-handover-brian.md` — DEC-LLM, DEC-ARMS, OPEN-PARAMS
- `plans/P0039_2026-08-19_01-45_srq4-system-a-vs-b/` — execution plan and findings
- `05_thesis_writing/notes/sample-size-and-tool-interface-rationale.md` — Ch4/Ch5 data-side rationale
