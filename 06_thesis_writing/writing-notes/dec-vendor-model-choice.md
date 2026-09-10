---
name: dec-vendor-model-choice
description: NOTE - DEC-VENDOR resolved. Why the SRQ4 scenarios run gpt-5.5-2026-04-23, argued on ecological validity rather than cost, with the evidence from the Prometheus engine's own configuration.
category: workflow
applies-to: [chapter 3 methodology, chapter 8 experimental evaluation, SRQ4]
triggers: [writing the SRQ4 method, justifying the model choice, an examiner asking why this LLM]
created: 2026_09_10-17_10
updated: 2026_09_10-17_10
---

# DEC-VENDOR — resolved 2026-09-10

**Decision: all SRQ4 scenarios run `gpt-5.5-2026-04-23`.**

The harness has been pinned to that snapshot since 2026-08-19. What was missing
was the *argument*, and an unargued default is what an examiner probes first.

---

## The question this answers

*Why is the LLM in every scenario GPT rather than Claude, Gemini or an open
model?*

The wrong answer is cost. At ~$7 (Claude) against ~$4 (GPT) for fifty runs, the
difference is under three dollars across the whole study — smaller than the
variance between two repeats of Scenario A. **Cost cannot discriminate here, so
citing it would be a rationalisation rather than a reason.**

---

## The argument: ecological validity

The thesis does not ask *which LLM forecasts best*. It asks whether a
**production-oriented agentic system that lacks native predictive capability can
be extended with a forecasting substrate** (SRQ3/SRQ4, ch2 §2.7). That framing
makes the choice a question about the deployment target, not about model quality.

The deployment target is the **Prometheus graph engine**, and it is not
hypothetical — it is the real system this integration is designed for. Its own
configuration answers the question:

```python
# graph-engine/data_agents/projects/prometheus/prometheus.py:64-65
main_agent_model="gpt-5.5",
coder_model="gpt-5.5",
```

**Both the conversational agent and the code-as-action coder run gpt-5.5.**
Scenarios D and E use that engine as shipped, so they run gpt-5.5 whether the
thesis chooses it or not.

That is what forces the decision. The five-scenario ladder isolates **one**
variable — how the forecast is produced. Running A/B/C on Claude while D/E run
gpt-5.5 would put a second variable, the model family, into the comparison that
matters most:

| Comparison | One variable? |
|---|---|
| B → C, both gpt-5.5 | yes — the tool |
| D → E, both gpt-5.5 (engine default) | yes — the tool |
| **B → C on Claude, D → E on gpt-5.5** | **no — tool AND model family** |

The design's strongest claim is that **B→C and D→E are the same intervention on
two different orchestrators**, so agreement between them is more than either
alone. A vendor split breaks exactly that claim: a difference between the two
ladders could then be the orchestrator, the model, or both, and nothing in the
data would separate them.

**So the choice is not "GPT is better". It is that the deployment target fixes
D/E, and holding the model constant across all five is what keeps the ladder a
single-variable design.**

---

## What is held constant, and where it is recorded

| Parameter | Value | Recorded in |
|---|---|---|
| Model | `gpt-5.5-2026-04-23` — a **dated snapshot**, never the floating alias | `MODEL`, and every run's trace |
| Temperature | not settable on this model | `TEMPERATURE = None` + `DECODING_NOTE` |
| Reasoning effort | `medium` (API default, stated explicitly) | `REASONING_EFFORT` |
| Prompt set | SHA-256 over every prompt string sent | `prompt_schema_id` in every trace |

The alias pin matters for reproducibility: `gpt-5.5` silently re-points as
OpenAI ships updates, so a study running the alias could not be re-run against
the same model months later. `verify_setup.py` asserts the snapshot is reachable
and that the decoding claim matches reality.

---

## The honest limitation

**This is a single-vendor study, and the thesis must say so rather than let a
reader assume generality.** The findings are about *this* orchestrator with *this*
model; whether a different family behaves the same way is untested.

That limitation is **narrower than it looks**, because the reproducible tier
(A/B/C) exists precisely so someone else can re-run the ladder on another model
with the repository and an API key. Cross-vendor replication is therefore stated
as further work with a concrete route, not as an acknowledged hole.

Two related boundaries worth stating in the same paragraph:

- **Temperature is not settable**, so run-to-run variation is whatever the model
  does by default. The design answers this by measuring it — repeats per cell,
  with `TAR` (total agreement rate) reported — rather than by suppressing it.
- **D and E are not reproducible by an examiner**, since Prometheus is
  proprietary. That is a deliberate two-tier design (ch2 §2.6): A–C reproducible,
  D–E ecological, and two tiers that agree beats pretending the whole ladder is
  reproducible.

---

## Where this goes in the thesis

**Bullets only in this note; prose is written on approval** (bullets-first,
Quality tier).

| Destination | What lands there |
|---|---|
| **Ch3 Methodology**, SRQ4 experimental design | the ecological-validity argument and the held-constant table — 1–2 paragraphs |
| **Ch9 Discussion**, limitations | the single-vendor limitation plus the replication route — 1 short paragraph |
| **Appendix** | the held-constant table, if it is not inlined in ch3 |

**Do not write the cost comparison into the thesis.** It is not the reason, and
including it invites the examiner to ask whether a three-dollar difference drove
a design decision.

---

## Provenance

- Prometheus configuration read from `Z:\_dev-ssd\prometheus\prometheus-graph-engine`
  on 2026-09-10; `main_agent_model` and `coder_model` both `gpt-5.5`, and these
  are the only two model-selection sites in the engine's project configs
- Harness pin: `srq4_experiment.py` `MODEL`, under `DEC-LLM 2026-07-12`,
  confirmed `B-DEC-1 2026-08-19`
- Reachability and the decoding claim: `verify_setup.py`, 10/10 as of 2026-09-10

## Related

- `plans/P0049_.../task_plan.md` — DEC-VENDOR in the decisions table
- `04_SRQ4_Scenario_Experiment/scenario_setup/srq4_experiment.py` — the pin and
  the ladder's single-variable rationale
- `.claude/rules/prose-insertion-discipline.md` — this note stages; the `.docx`
  is authoritative
