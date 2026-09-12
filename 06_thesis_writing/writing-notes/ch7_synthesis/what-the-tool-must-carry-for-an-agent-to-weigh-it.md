---
name: what-the-tool-must-carry-for-an-agent-to-weigh-it
description: NOTE - The combined arms received the model payload and still overrode it. That is an interface finding, not an accuracy one - a tool that reports confidence without a weighting policy leaves the agent to invent one. Independent of the funded run's numbers.
category: reference
applies-to: [ch7_synthesis, ch6_architecture, ch9_discussion]
triggers: [tool interface, SRQ2, confidence tier, why did the agent override the model, decision support, weighting]
created: 2026_09_12-20_40
updated: 2026_09_12-20_40
status: bullets, not prose - the ARGUMENT is final, the numbers are provisional
---

# What the tool must carry for an agent to weigh it

**This note does not depend on the funded run.** The behaviour it describes was
observed on every combined-arm run so far, and the argument stands whichever
way the accuracy numbers land.

---

## The observation

Scenarios F and G receive the trained model's forecast **alongside** the brand
history and a code sandbox. They are told to weigh the evidence and give their
own answer — deliberately, per DEC-COMBINED-INPUT: the model's output is one
input among several, never a starting point to revise, because an agent handed
a number and told it may keep it will almost always keep it. That measures
deference, not integration.

**Both arms overrode the model.** `deviates_from_model = True` throughout. And
they cited the payload's own fields as the reason — the **Low confidence tier**
and the **width of the 90% interval**.

## What that tells the interface, and it is not about accuracy

The agent read the confidence signal and acted on it. That is the SRQ2
contribution working exactly as designed: the forecast reached the agent with
its uncertainty and its track record attached, and the agent used them.

**But it had no policy for what to do next.** It knew the model was uncertain.
It did not know *how much to discount it*, because nothing in the payload says
that. So it invented a weighting — and in this sample, the invented weighting
made things worse than either source alone.

> A tool that reports its own uncertainty honestly, without saying what to do
> with it, transfers the weighting decision to the caller. If the caller is
> non-deterministic, the weighting is non-deterministic too.

That is an **interface finding**, and it belongs in the chapter that specifies
the interface rather than in the results chapter.

---

## Why the gap is a real design question, not an oversight

Forecast combination is well-established theory — Hyndman and Athanasopoulos
(2021, §13.4) report it as near-unanimously beneficial, with a simple average
"hard to beat". But combination works when the components are **comparable in
quality and their errors are imperfectly correlated**.

The combined arms are not combining peers:

- the agent's in-session ensemble, fitted **to the single brand in the prompt**;
- against one model fitted **across the whole category**, flagged Low
  confidence, with a wide interval.

Averaging those without weights drags a bespoke estimate toward a general one.
The conclusion is not "context hurts", it is **"unweighted combination of
unequal sources hurts"**, which is a much more actionable claim.

---

## The design implication

`srq2_synthesis.py` already implements **inverse-MAPE weighting** for its own
ensemble. The forecast payload does not expose anything equivalent to the
agent. Three options, in increasing strength:

| Option | What the tool carries | Cost |
|---|---|---|
| **Report** (current) | point, interval, confidence tier, historical WMAPE | none |
| **Advise** | a recommended weight, derived from historical WMAPE | small |
| **Gate** | a tier at which the caller should not override | policy decision |

**"Advise" is the defensible middle**, and it follows directly from what the
tool already computes: it knows its own historical error on this series, so it
can say what that error implies for how far its number should move. It does not
remove the agent's judgement; it gives the judgement a basis other than
intuition.

**"Gate" is worth naming and rejecting**, or the chapter looks naive. A hard
override rule makes the system deterministic again, but it forfeits the reason
an agent is there: the agent may hold context the model cannot see — a delisting,
a promotion, a supply constraint. Hyndman and Athanasopoulos (§6.7) treat
judgmental adjustment as legitimate *when it is informed*, which is the same
position.

---

## How this lands in Chapter 7

Three moves, in order:

1. **State the design as built**: the forecast crosses the interface with its
   interval, confidence tier and provenance, so the caller can weigh it. That
   is the contribution.
2. **Report that a caller with all of it still needed more**: it used the
   signals to decide *whether* to trust the number, but had no basis for
   deciding *how much*.
3. **Name the extension**: a recommended weight derived from the model's own
   measured error, and say why gating is rejected.

This strengthens the chapter rather than weakening it. An interface that was
never tested against an agent free to disagree with it has not been evaluated —
this one was, and the disagreement is what exposed the missing field.

---

## Careful

- **Do not claim the override was wrong.** On one brand the combined arm beat
  its own data-only counterpart. Overriding is sometimes right, which is exactly
  why a gate is the wrong fix.
- **Do not report accuracy numbers here.** This note is about the interface
  contract; the numbers live in Chapter 8 and are provisional until the funded
  run is read.
- **The grain asymmetry may explain part of the effect** — see
  [[the-result-hinges-on-forecasting-practice]]. If the model were fitted per
  brand, it and the agent's ensemble would be closer to peers, and unweighted
  combination might stop hurting. State that as an alternative explanation,
  not a certainty.

---

## Related

- [[the-result-hinges-on-forecasting-practice]] — the grain and combination
  asymmetries that bound this reading
- [[when-to-use-which-scenario-group]] — where F and G sit in the deployment
  guidance
- [[ad-hoc-data-science-vs-a-trained-pipeline]] — why a non-deterministic
  weighting is a product problem, not only an accuracy one
- `02_SRQ2_Tool_Interface/forecast_tool.py` — the payload as built
