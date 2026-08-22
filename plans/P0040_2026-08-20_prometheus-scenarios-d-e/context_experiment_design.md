---
pid: P0040
created: 2026-08-22 17:30:00
updated: 2026-08-22 17:30:00
status: proposed
---

# Context-and-predictions experiment — design

Brian, 2026-08-22: *"perhaps we should have some options so we can test on a small
scale whether this hypothesis of ours even holds -> e.g. multi predictions and
improved contextual payload = better prediction. I would assume that more context =
better response, but we don't know."*

**That reframing resolves an objection this plan had raised.** The earlier argument
against adding brand-level context was that each unmeasured payload change makes
`B->C` and `D->E` harder to attribute. But Brian is not proposing to *quietly add*
context -- he is proposing to *measure* it. The objection does not apply to a
measured intervention.

## Two factors, not one

The proposal contains two independent interventions that could interact:

| Factor | Levels |
|--------|--------|
| **Prediction count** | 1 (specialised only) · 2 (pooled + specialised) |
| **Context depth** | minimal · + category accuracy · + brand-level context |

A full factorial is 2 x 3 = 6 cells, and doubling across orchestrators would make 12.
**Reject that**: at ~$8/cell it reaches ~$96, and the effects being tested are small
enough that between-repeat noise would likely swamp the differences.

## The efficient design -- 5 cells, one variable per arrow

| Scenario | Predictions | Context | The arrow that uses it |
|----------|:-----------:|---------|------------------------|
| `C_model` | 1 | point + interval only | baseline |
| `C_ctx` | 1 | + historical accuracy, both metrics, both baselines | `C -> C_ctx`: **does accuracy context alone help?** |
| `C_ctx_brand` | 1 | + brand volume tercile + within-tercile accuracy | `C_ctx -> C_ctx_brand`: **does brand-level resolution add more?** |
| `F_ensemble` | 2 | point + interval only | `C -> F`: **does a second prediction help?** |
| `F_ctx` | 2 | + historical accuracy | `F -> F_ctx` vs `C -> C_ctx`: **do the two effects interact or overlap?** |

Five cells instead of six. `C -> C_ctx` and `C -> F` are independent main effects;
comparing `F -> F_ctx` against `C -> C_ctx` gives the interaction. If context helps
in the single-prediction arm but not in the two-prediction arm, the second prediction
was already supplying what the context added.

## Run on GPT only -- not both orchestrators

The question concerns the **interface**, not the engine. `D -> E` already replicates
the tool intervention across two orchestrators, which is the structural claim the
thesis needs. Adding Prometheus variants here would double the cost to re-answer a
question already answered.

State this explicitly in the methodology so the asymmetry reads as a design decision
rather than an omission.

## Pilot first -- this is the important part

**Before committing ~$40 to five cells, run one brand x one repeat x five cells
(~$2).**

The decision rule: **compare the spread ACROSS cells against the spread BETWEEN
repeats of the same cell.** If across-cell variation is smaller than within-cell
variation, the effect is below the noise floor and the full run would produce an
uninterpretable table. Knowing that for $2 is worth far more than discovering it
after spending $40.

This is a real possibility, not a formality. The interventions are payload fields;
LLM output variance across repeats on the same prompt is substantial.

## The hypothesis may be wrong, and that is fine

Brian's prior -- more context produces better responses -- is reasonable but not
safe. Two counter-mechanisms:

1. **Context dilution.** Longer payloads can degrade attention to the parts that
   matter. There is a literature on this (see P0041 citation register, Group 6).
2. **Harmful second-guessing.** Telling a model "this forecast has 48% median error"
   may induce it to *override* an accurate forecast with a worse guess of its own.
   The information is true; acting on it may still hurt.

**A null or negative result is publishable and useful** -- it would say a
well-calibrated point estimate suffices, and that interface complexity is not
automatically an improvement. Design the write-up so that outcome is a finding
rather than a disappointment.

## Cost

| Item | Cost |
|------|------|
| Pilot (1 brand x 1 repeat x 5 cells) | ~$2 |
| Full run (12 brands x 5 repeats x 3 NEW cells) | ~$25-30 |
| **Total additional** | **~$30** |

`C_model` already exists; `F_ensemble` was already budgeted at ~$8-10 (F55). The
genuinely new spend is `C_ctx`, `C_ctx_brand` and `F_ctx`.

## Sequencing

1. Lock B/C/D/E and run them.
2. Run the **pilot**. Stop here if the effect is below the noise floor.
3. Run the full context ladder only if the pilot shows separation.
4. Run `A_plain` last (most expensive, no tools).

## COST IS THE DECIDING CONSTRAINT (Brian, 2026-08-22)

*"I really like the idea, but I am worried about the additional cost, even if we only
go for the GPT route. We would have to test this. If it is too expensive, we just drop
it and make it so that we only have the category accuracy as those are both in the
regular and ensemble scenarios."*

### The fallback, if cost or the pilot rules the full ladder out

Drop `C_ctx_brand` and `F_ctx`. Keep **category accuracy context in BOTH `C_model` and
`F_ensemble`**, identically:

| Scenario | Predictions | Context |
|----------|:-----------:|---------|
| `C_model` | 1 | + category accuracy |
| `F_ensemble` | 2 | + category accuracy |

`C -> F` then still isolates **one clean variable -- the second prediction** -- because
context is held constant across both. **Nothing is lost from the SRQ4 ladder**; only
the context-depth question goes unanswered, and that was always the nice-to-have.

Cost of the fallback: **$0 additional** beyond `F_ensemble`, already budgeted. The
accuracy fields are already implemented (task 13).

### Decision sequence

1. Run the **pilot** (~$2, 1 brand x 1 repeat x 5 cells).
2. **If** across-cell spread < within-cell spread across repeats -> effect is under the
   noise floor. **Take the fallback.** Do not spend $30 measuring noise.
3. **If** the pilot separates AND budget allows -> run the full five-cell ladder.
4. **If** the pilot separates but budget is tight -> take the fallback, record the
   context-depth question as further work, cite the pilot as preliminary evidence.

**The fallback is not a failure state.** It answers the sharper question (does a second
prediction help?) with a cleaner design at no extra cost. The full ladder only adds the
softer question of whether context *depth* matters.

## What must be built first

- `forecast_demand(..., context_level=)` -- one parameter selecting the payload
  depth, so all five cells run off one code path and cannot drift apart.
- Brand volume tercile + within-tercile median error (needed only for
  `C_ctx_brand`).
- Pooled model loaded alongside the specialised one (needed for `F_*`).

**One caution:** the tercile boundaries are another arbitrary choice, like the 3x
Ridge bound. Derive them from the training data and state that they are ours (see
P0041 Group 5).
