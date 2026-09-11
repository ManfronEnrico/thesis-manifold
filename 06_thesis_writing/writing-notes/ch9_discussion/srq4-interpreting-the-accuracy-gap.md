---
name: srq4-interpreting-the-accuracy-gap
description: REFERENCE - Why the pilot's accuracy gap is not "code beats models", the four competing explanations and how each is separable by measurement, and the restatement the discussion chapter must make before any interpretation. Routed from the experiment session.
category: reference
applies-to: [ch9-discussion, ch8-evaluation, ch10-limitations]
triggers: [interpreting the SRQ4 result, writing the discussion, an arm beats the artefact, explaining why the code scenarios win, defending the architecture on non-accuracy grounds]
created: 2026_09_11-20_55
updated: 2026_09_11-20_55
---

# Interpreting the accuracy gap

**Routed here from the experiment session (P0049 F53).** It is a Chapter 9
argument, not a Chapter 6 one, and it had no chapter note of its own.

⚠ **Nothing here may be written into prose yet.** One brand, one month, one or
two repeats per arm. This records the *interpretation* to be ready with, and the
trap to avoid, when the funded set lands.

---

# The restatement that has to come first

The obvious reading of the pilot is that a language model writing its own code
beat the dedicated model. **That reading is wrong, and it is the headline an
examiner will reach for if the discussion does not pre-empt it.**

What actually happened:

> **A model fitted to one series beat a model fitted to a category.**

Read from the code the scenario actually wrote and cached, not inferred:

| What the code-writing arm did | |
|---|---|
| exponential smoothing | four configurations, additive and multiplicative seasonality, damped and undamped trend |
| SARIMA | a 72-model grid, ranked by information criterion |
| linear models | ordinary and ridge regression with month dummies, a time trend and promotion intensity, in linear and log space with a smearing correction |
| validation | backtested at two earlier cutoffs against months it had not seen |
| final answer | the median across all fitted models |

That is a small automated model competition fitted to one brand's own 39 months.
The dedicated model is a single gradient-boosted model whose hyperparameters were
tuned once for the whole category, serving 95 brands from one configuration.

**The comparison may be measuring per-series adaptation rather than
code-versus-model.** Those are different claims and the thesis must not conflate
them.

---

# Four explanations, and how each is separated

| | Explanation | How the funded set separates it |
|---|---|---|
| **1** | **Per-series beats per-category.** A category-tuned model is pulled toward brands unlike the one being forecast | Compare the dedicated model's error on large against small brands. The pilot brand is the **largest** in its category, so a category-tuned model is fitted largely to brands nothing like it. Systematically worse error at the extremes of the size distribution is the signature |
| **2** | **Ensembling beats a single model.** The code arm averaged roughly eighty models; the artefact serves one | Check whether the code arm's own per-model spread brackets the dedicated model's answer. This is a **genuine advantage of code-as-action**, not an artefact of the design |
| **3** | **Luck.** One brand, one month | The repeats answer this directly, and the pilot already suggests it matters — see below |
| **4** | **Horizon interaction.** A per-series method may degrade more slowly as the horizon lengthens | Only separable if the secondary horizon is also run. **Out of scope unless that is funded** |

⚠ **Explanations 1 and 2 are not competing; they are additive**, and both are
real advantages of the code-writing arm. A discussion that treats them as rival
hypotheses to be adjudicated has misread them. The question is how much of the
gap each contributes, not which is true.

---

# What the pilot already shows about explanation 3

**Within-arm variation is comparable to between-arm gaps**, which is the single
most important fact for anyone tempted to rank the arms now.

| Arm | Across two runs on identical prompts |
|---|---|
| plain language model | 38.7% then 23.0% |
| code-as-action | 1.0% then 5.2% |
| code-as-action, in production | 1.5% then 0.2% |
| **dedicated model** | **21.9% then 21.9%** |
| **dedicated model, in production** | **21.9% then 21.9%** |

⚠ **Any accuracy ranking read off the pilot is noise.** The spread within the
plain arm alone is 15.7 percentage points.

**But the table also contains a result that does not depend on sample size.** The
two tool-backed arms returned the identical figure every time, to the decimal,
on two different orchestrators. The code-writing arms did not. That is the
reproducibility property the interface was designed for, and it is visible at
n=2 because it is a property of the mechanism rather than of the data.

---

# Why this does not undermine the artefact

Chapter 6 justifies the structured interface on **reliability, reproducibility
and auditability**, and never on accuracy. That restraint was deliberate and is
now load-bearing.

| | dedicated model | code-as-action |
|---|---|---|
| latency | 7 s | 91 s |
| cost per answer | $0.009 | $0.224 |
| answer stability across runs | identical to the decimal | varies |
| auditability | one tool call, arguments verified against the request | ten opaque code blocks |

**The cost and latency gap is two orders of magnitude and will not reverse**,
because it is structural: one model inference against roughly eighty model fits
plus a sandbox.

---

# The conclusion shape to build toward

> **Dedicated models trade accuracy for auditability and cost at this data scale.**

⚠ **Do not write this sentence until the funded set has run.** It is recorded so
the discussion is not improvised.

Why it is a better claim than a clean win:

- **It survives the result that threatens the obvious version.** An arm beating
  the artefact on accuracy is the trade becoming visible, which is evidence *for*
  this sentence.
- **It is falsifiable in both directions.** If the funded set shows the dedicated
  model also wins on accuracy, a stronger sentence replaces this one. If cost and
  latency converge, it is wrong the other way. Both are measurable.
- **It is decision-useful.** A practitioner can act on "at this data scale", which
  the thesis quantifies.

⚠ **"At this data scale" is load-bearing and must carry its numbers every time it
appears**: 39 months, 95 brands in the category, one category-tuned model. Without
them the claim degrades into the universal one the evidence cannot support.

---

# The trap, stated plainly

**Do not let "the code arm won" become the headline without the restatement.** As
a bare fact it invites the reader to conclude the artefact is unnecessary. The
measured claim is narrower, more defensible and more useful:

> At 39 months and 95 brands, a per-series ensemble outperforms a category-tuned
> booster on accuracy, while costing roughly twenty-five times more, taking
> twelve times longer, and producing no auditable tool call.

⚠ **Every multiplier in that sentence must be recomputed from the funded set
before it is written.** The ones above come from a two-run pilot and are
illustrative only.

---

# Related

- `ch8_experiment/the-defensible-conclusion-shape.md` — the same conclusion from
  the evidence side, with its falsification conditions
- `ch8_experiment/brand-sampling-and-inclusion-criteria.md` — why the sample is
  what it is, which explanation 1 depends on
- `anticipated-assessor-questions.md` — Q4.2 is this argument compressed to a
  defence answer
- P0049 `findings.md` F53, F54 — the source, with the cached code blocks
