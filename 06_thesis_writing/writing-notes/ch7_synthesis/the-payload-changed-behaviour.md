---
name: the-payload-changed-behaviour
description: REFERENCE - Both combined arms departed from the model's forecast and named its own reported uncertainty as the reason. The strongest SRQ2 evidence the project has, it does not depend on sample size, and it survives even though the confidence index is degenerate.
category: reference
applies-to: [ch7-tool-interface, ch8-evaluation, ch9-discussion]
triggers: [writing the uncertainty section, defending the typed payload, arguing what the interface contributes, answering why ship a broken confidence index]
created: 2026_09_11-21_05
updated: 2026_09_11-21_05
---

# The typed payload changed what the agent did

**Routed here from the experiment session (P0049 F54).** It is an SRQ2 result and
belongs with the tool interface, not with Chapter 6's architecture or Chapter 8's
accuracy comparison.

**Verified independently in both raw traces**, not taken from the finding.

---

# What happened

Both combined arms were given the dedicated model's forecast alongside the
history and an execution sandbox. **Neither returned the model's number.**

| Arm | Given | Returned | Code executions |
|---|---|---|---|
| combined | 4,969,050 | **6,200,000** | 12 |
| combined, in production | 4,969,050 | **5,604,800** | 2 |

For contrast, the two tool-only arms relayed 4,969,050 exactly, on both
orchestrators, on every run.

---

# The part that matters: they said why, unprompted

Neither arm was asked to justify departing from the model. Both did, and both
named **the model's own reported uncertainty** as the reason:

> "...the history is short, 2025 was volatile, and the dedicated model's own
> confidence is low with a very wide interval."

> "...the dedicated model is low-confidence with a wide interval; March history
> supports the midpoint, but recent sales are volatile and likely
> promotion-sensitive."

**The payload carried decision-relevant information rather than a bare number,
and that information changed the decision.** That is precisely what Chapter 7
claims the interface is for.

---

# Why this is the strongest SRQ2 evidence the project has

⚠ **It does not depend on sample size the way an accuracy ranking does.**

An accuracy comparison at n=1 is noise, and the pilot proves it: within-arm
spread across identical prompts reaches 15.7 percentage points. **This result is
different in kind.** It is a claim about *mechanism* — whether a consumer of the
payload can act on the uncertainty channel — and a single clean instance
demonstrates the mechanism exists. More runs would establish how often, not
whether.

Three properties make it defensible now:

- **Both arms did it independently**, on two different orchestrators.
- **Neither was prompted to.** The reasoning is unelicited, which rules out the
  obvious confound.
- **They cited the specific fields the interface supplies** — the confidence tier
  and the interval width — not vague hedging.

---

# The uncomfortable part, which makes it stronger

⚠ **The confidence index is mathematically degenerate.** It returns one of four
values across every brand in the panel, all tiering "Low", for reasons recorded in
`ch7-confidence-index-decision.md`. It cannot distinguish one brand from another.

**And it still worked here.** On this brand, "low confidence with a wide interval"
was the *correct* signal: the interval genuinely was enormous, the history
genuinely is short, and weighing the model rather than adopting it was the right
response.

This is worth stating carefully, because it can be misread in two directions:

| Do NOT conclude | Do conclude |
|---|---|
| the index works, so the defect does not matter | the **uncertainty channel** works; the index is one degenerate input to it |
| the index should be kept as it is | a constant "low" is right by accident here and would be wrong wherever confidence should vary |

**The honest formulation:** the interval width did the work, and the confidence
tier agreed with it because both derive from the same per-category quantile. An
index that cannot discriminate happened to be correct on a brand where the
uninformative answer was the true one. **That is not a defence of the index.**

⚠ **If the index is ever repaired, this result must be re-examined**, because the
agent's stated reason would then rest on a different signal.

---

# What to write, and when

**Not yet.** One brand-month, one run per combined arm.

When the funded set lands, the claim this supports is:

> The interface's uncertainty channel is consumed rather than ignored: agents
> given a forecast with its interval and a confidence qualifier weigh it against
> other evidence instead of adopting it, and cite the qualifier when they do.

**What must be measured before writing it:** how often the combined arms depart
from the model, and whether they cite the uncertainty fields when they do. Both
are already recorded on every run, so the funded set answers this without any
additional instrumentation.

⚠ **Do not claim the agents were *right* to depart.** On this brand they were —
both landed closer than the model. That is an accuracy claim and needs the funded
set. The SRQ2 claim is about the channel being used, which is separable and much
better supported.

---

# One design decision this validates

The combined arms supply the model's forecast as **one input among several**,
never as a starting figure to revise. The reasoning was that an agent handed a
number and permitted to keep it will usually keep it, so the arm would measure
deference rather than integration.

**Measured: both arms departed.** Had the framing been "here is the forecast,
revise if needed", the near-certain outcome was both arms returning the model's
number unchanged and the arm establishing nothing.

⚠ **This is a methodological point, not a result.** It belongs in Chapter 3 or in
Chapter 8's design description — it says the instrument measures what it was
built to measure.

---

# Related

- `ch7-confidence-index-decision.md` — why the index is degenerate and cannot be
  repaired by re-tiering
- `ch9_discussion/srq4-interpreting-the-accuracy-gap.md` — the accuracy side,
  which this is deliberately kept separate from
- `anticipated-assessor-questions.md` — Q3.3 uses this as the unexpected defence
  of shipping a broken index
- P0049 `findings.md` F54 — the source
