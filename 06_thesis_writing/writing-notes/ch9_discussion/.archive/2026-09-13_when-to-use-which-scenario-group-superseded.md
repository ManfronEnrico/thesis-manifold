---
name: when-to-use-which-scenario-group
description: NOTE - The practical deployment guidance the seven-arm ladder produces. No arm wins on every axis, and the shape of that disagreement is the contribution. Scored across accuracy, reliability, cost, latency and stability. Provisional - measured on one run per brand.
category: reference
applies-to: [ch9_discussion, ch10_limitations, ch8_experiment]
triggers: [which scenario is best, deployment guidance, practical recommendation, discussion chapter, contribution]
created: 2026_09_12-20_05
updated: 2026_09_12-20_05
status: bullets, not prose - PROVISIONAL until the funded run lands
---

# When to use which scenario group

**Provenance.** The v6 smoke, 2026-09-12: CSD, three brands (HARBOE, 7-UP,
ØRBÆK), **one run per brand per arm**, 21 runs, $6.34 actual spend.

> ## ⚠ PROVISIONAL
> One run per cell. The B arm's mean APE is 31.3% against a **1.8% median**,
> so one of three brands failed badly — the variance is large and unmeasured.
> Every figure here must be re-derived from the funded run before it reaches
> the thesis. What is likely to survive is the **shape**, not the numbers.

---

## The framing: no arm wins, and that IS the finding

The instinct is to report a winner. The data does not support one, and the
reason is the contribution: **the arms disagree about which axis they optimise**.

- The arm with the best accuracy has the worst reliability.
- The arm with the best cost and speed has middling accuracy and perfect
  reproducibility.
- The arms with the most capability are **worse than their own components**.

A thesis that reports "code-as-action wins" would be discarding the most
interesting result it has. Three separable contributions sit here, and they
should be written as three:

1. **What data access is worth** (A → B), and it is worth a great deal.
2. **What a dedicated model buys** (B → C), which is not accuracy but cost,
   speed and reproducibility.
3. **What happens when you combine them** (C → F, E → G), which in this sample
   is *worse than either alone* — the least expected result of the three.

---

## The measured picture

Median APE, one run per brand. Median rather than mean throughout: a single
divergent series destroys a mean at n=3.

| Arm | Median APE | Mean APE | Cost/run | Latency | Usable |
|---|---|---|---|---|---|
| D_prometheus_data | **1.0%** | 15.6% | $0.6864 | 116s | 3/3 |
| B_llm_data | **1.8%** | 31.3% | $0.4577 | 123s | 3/3 |
| F_llm_data_model | 7.3% | 18.3% | $0.4953 | 122s | 3/3 |
| A_llm_plain | 11.5% | 11.5% | $0.3267 | 96s | **1/3** |
| C_llm_model | 14.6% | 13.1% | **$0.0089** | **8s** | 3/3 |
| E_prometheus_model | 14.6% | 13.1% | $0.2075 | 34s | 3/3 |
| G_prometheus_data_model | 25.3% | 25.3% | $0.5008 | 79s | 2/3 |

**Two integrity signals worth quoting in the text.** C and E return *identical*
accuracy, which is correct — same model, different orchestrator — and is
evidence the harness isolates what it claims to. And the B mean/median gap is
the variance warning, visible in the table rather than asserted.

---

## The guidance, by group

### C and E — the dedicated model alone

**Use when cost or latency dominates, or when the answer must be reproducible.**

- **50–75x cheaper** than any arm that reasons over data. $0.0089 versus $0.46.
- **8 seconds** versus two minutes. An order of magnitude.
- Identical output run to run, and a calibrated interval by construction.
- Middling accuracy (14.6%) — it is beaten by the data arms in this sample.

This is the arm for **interactive use at scale**: a planner asking about many
brands in one session, or any setting where the same question must return the
same answer. The reproducibility is not a tiebreaker, it is what makes the
output auditable, which is the SRQ2 contribution.

### B and D — data plus code-as-action

**Use when accuracy matters more than cost, latency or predictability.**

- Best median accuracy in the sample, 1.0–1.8%.
- **But the mean is 15.6–31.3%.** One brand in three went badly wrong. High
  ceiling, unreliable floor.
- ~50x the cost and ~15x the latency of the model arm.

This is the arm for a **considered, one-off analysis** a human will review —
not for an automated pipeline, and not for anything a planner acts on
unchecked. At n=1 per brand we cannot yet say how often the floor is hit,
which is the single most important thing the funded run will tell us.

### F and G — everything at once

**The disappointment, and the most interesting result.**

- F (7.3%) is **worse than B** (1.8%). G (25.3%) is **worse than D** (1.0%).
- Cost and latency are comparable to the data arms, so the loss buys nothing.
- Handing the agent the model's forecast *alongside* the data appears to pull
  it away from its own better analysis.

**Do not over-claim this yet.** At one run per brand it could be noise. But it
is directionally the opposite of the intuition that more context is better, and
if it survives the funded run it is a real finding about **integration**: a
decision-support layer that presents several sources without a policy for
weighing them may perform worse than any single source.

This is what DEC-COMBINED-INPUT was written to measure. The model's forecast is
deliberately *one input among several*, never a starting point to revise, so
whether the agent defers, overrides or blends is the measurement — traced as
`deviates_from_model`.

### A — no firm data

**Not deployable, and that is the point of including it.**

- **Two of three runs returned implausible values.** It is the only arm that
  failed the plausibility check at all.
- Second most expensive arm, because it is the only one that searches the web.
- It exists to establish the floor: what a capable model does when it has the
  question and nothing else.

---

## The cross-cutting axes

Worth a small table in the discussion, because it makes the "no winner" point
visible at a glance.

| Axis | Best | Worst |
|---|---|---|
| Accuracy (median) | D, B | G, C/E |
| Reliability (usable answers) | B, C, D, E, F | A (1/3), G (2/3) |
| Cost | C ($0.009) | D ($0.69) |
| Latency | C (8s) | B (123s) |
| Reproducibility | C, E (identical) | A (38% CV) |

**No column has the same winner.** The practical recommendation is therefore
conditional on what the deployment values, which is a more useful contribution
than a ranking.

---

## What must be re-derived before this reaches the thesis

- Every number above, from the funded run (3 repeats).
- **The B/D floor**: how often does the good median fail? That is the question
  n=1 cannot answer and n=3 partly can.
- **Whether F and G stay worse than their components.** If yes, it is a
  finding. If the gap closes, it was noise and must be reported as such.
- Whether A's failure rate holds at 2/3.

---

## Related

- [[ad-hoc-data-science-vs-a-trained-pipeline]] — the framing this sits inside;
  the reproducibility axis is the same argument
- [[srq4-interpreting-the-accuracy-gap]] — the four competing explanations for
  an accuracy gap, and why "code beats models" is not the right reading
- [[the-defensible-conclusion-shape]] — accuracy traded for auditability
- [[the-agent-input-contract]] — what the data arms were actually given, and
  why the earlier four-column payload made this comparison meaningless
