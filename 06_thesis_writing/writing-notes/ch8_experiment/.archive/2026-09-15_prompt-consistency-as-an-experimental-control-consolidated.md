---
name: prompt-consistency-as-an-experimental-control
description: NOTE - Comparable arms had drifted apart in wording, so B-to-D and C-to-E were not isolating the orchestrator. Found and corrected before the funded run. The correction is evidence of rigour and should be owned in the text, not hidden.
category: reference
applies-to: [ch8_experiment, ch6_architecture, ch7_synthesis, ch10_limitations]
triggers: [experimental control, prompt design, single-variable design, what makes the arms comparable, methodological rigour]
created: 2026_09_12-20_10
updated: 2026_09_12-20_10
status: bullets, not prose
---

# Prompt consistency as an experimental control

**Found by Brian, 2026-09-12**, reading the prompt module before the funded
run. Corrected the same day, prompt schema v5 → v6, **before any funded money
was spent**.

**Where this belongs.** The chapters that discuss the interface, the serving
layer and the experiment — 6, 7 and 8. Not the data-assessment chapter: at that
point in the thesis only the models were being trained, and the prompt is a
constructed instrument of the *experiment* phase.

---

## The design claim the experiment rests on

Every arm is asked the **identical user question**. That is deliberate and
load-bearing: an earlier version gave each scenario differently-worded
instructions, so any accuracy difference partly measured **prompt wording**
rather than the mechanism under test.

The arms are then supposed to differ in **exactly one thing** — the capability
envelope:

```
A -> B   what data access buys
B -> C   what the dedicated model adds        (the thesis contribution)
C -> F   what code on top of the model does
D -> E -> G   the same three rungs, production orchestrator
```

The B/D, C/E and F/G pairs exist so those rungs can be read **column-wise**:
each pair differs only in the orchestrator.

## The defect: the capability notes had quietly undone it

The shared question was held constant. The **capability notes were not** — they
were hand-written per arm, so comparable arms drifted:

| | B (bare API) | D (Prometheus) |
|---|---|---|
| Names the five libraries | yes | **no** |
| Asks for a 90% interval | **no** | yes |
| Asks for a confidence statement | **no** | yes |
| Prescribes mechanics (`io.StringIO`) | no | yes |

And separately: **E glossed every field of the model payload; C, which receives
the same fields through the tool response, got no gloss.**

**Why this matters more than it looks.** Both B and D are scored on interval
communication, and only D was *told* to produce an interval. A difference in
that score between them would have been partly an artefact of the instruction,
not of the orchestrator. The same logic applies to the library list and to the
payload gloss.

So **B→D and C→E were not isolating the orchestrator.** Wording travelled with
it — the exact confound the shared question exists to remove, reintroduced one
layer down.

---

## The correction: compose, do not write

v6 builds every capability note from **shared components**:

`DATA_BLOCK`, `MODEL_BLOCK`, `MODEL_TOOL_BLOCK`, `ANALYSIS_TASK`,
`ANALYSIS_TASK_WITH_MODEL`, `NO_WAREHOUSE`, `ENGINE_NOTE`

Assembled per arm. A difference between two arms is now visible as a
**different component**, not as a turn of phrase that nobody diffs.

**What is still permitted to differ, and nothing else:**

1. **Which capability the arm has.** That is the treatment.
2. **The warehouse instruction, D/E/G only.** Those arms run on a nested coder
   with SQL tools registered at module scope in the vendor tree. B/C/F have no
   such tools, so the sentence would describe a capability they do not have —
   adding it "for symmetry" would be adding words, not removing a difference.
3. **A short conversational-agent note for D/E/G**, because the orchestrator is
   two agents and the nested coder never sees the user message.

**No gloss on C or E** (decision: neither, not both). Minimal input; reading the
payload is part of what is being measured.

---

## The control is now enforced, not remembered

Two mechanisms, because "remember to keep them in step" is what failed:

- `python prompts.py` renders **all seven arms** and runs a
  **shared-component check** asserting the pairs are byte-identical. The v5
  demo printed three arms, which is precisely how the drift survived unseen.
- `schema_id()` hashes every prompt string, so any edit changes the run
  identity automatically and old rows stop pooling. There is no way to alter a
  prompt and forget to bump the version.

---

## How to write this

**Own it.** A thesis that reports a control it later found to be imperfect, and
says how it was detected and fixed, is more credible than one that asserts the
control held. The correction landed **before** the funded run, so no reported
result rests on the defective instrument.

Suggested shape, two short paragraphs:

1. State the single-variable design and why the pairs exist.
2. State that an audit before the funded run found the capability notes had
   drifted, name the concrete case (one arm instructed to produce an interval
   while its pair was not, with both scored on interval communication), and
   state the fix: notes composed from shared blocks, with an automated check.

**Do not** write it as an apology, and do not bury it in limitations. It is a
methods paragraph.

**The v5 and earlier runs are NOT reported.** Brian, 2026-09-12: every run on
the old schema and the old four-column payload is **useless and must not appear
in the thesis**. They were asked an internally inconsistent set of questions
over a payload that starved the data arms, so they do not measure what the
experiment claims to measure. The schema id keeps them mechanically unpoolable;
the editorial decision is stronger than that — they are not results, and they
are not reported as superseded findings either.

**Every chapter after Chapter 5 must reflect the corrected architecture and the
v6 results** wherever it reports or refers to them. Chapter 5 is model training
and is unaffected.

---

## Related

- [[the-agent-input-contract]] — the other half of the v6 change; both landed
  together because a schema id cannot be bumped twice for one run
- [[srq4-experiment-design-rationale]] — the single-variable design this
  protects
- [[prometheus-scenarios-design-rationale]] — why D/E/G need the warehouse
  instruction and B/C/F do not
