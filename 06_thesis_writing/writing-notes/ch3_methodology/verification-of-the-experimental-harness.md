---
name: verification-of-the-experimental-harness
description: REFERENCE - Four defects the pre-flight checks caught or missed before the funded run, what each cost or would have cost, and the rigour argument the methodology chapter can make from them. Routed from the experiment session.
category: reference
applies-to: [ch3-methodology, ch8-evaluation, ch10-limitations]
triggers: [writing the methodology's validity section, defending experimental rigour, describing pre-flight checks, answering "how do you know the harness is correct"]
created: 2026_09_11-21_00
updated: 2026_09_11-21_00
---

# Verifying the harness before spending money

**Routed here from the experiment session (P0049 F51, F55, F56, F59).** These are
methodology material and had no chapter note.

The thesis runs a paid experiment that cannot be repeated cheaply, so the
correctness of the harness is a **methodological claim in its own right**, not an
engineering footnote. Four defects found in one day make that case with evidence
rather than assertion.

---

# The four, and what each would have cost

| | Defect | Caught | Would have cost |
|---|---|---|---|
| **1** | A pre-flight check passed on an all-empty list | before the funded run | a silently unverified horizon on every run |
| **2** | A check read a field from the wrong place and failed a correct run | same day | a correct run discarded as broken |
| **3** | The summary table relettered the scenarios under an older scheme | during a rename | published tables contradicting the chapter's own naming |
| **4** | The brand-count flag was independent of the brand-selection strategy | in the dry run, one step before launch | ~33% more spend, on a different sample than the one the text justifies |

**Defect 4 is the one worth telling.** Asking for a three-brand stratified sample
returned **four brands**, silently, because the count came from a different flag
than the strategy and nothing related them. Nothing errored. The run would have
cost a third more and measured a sample the methodology section does not
describe.

---

# The transferable pattern: a check that cannot find its evidence must say so

Defects 1 and 2 are the same bug in opposite directions, and both sat **inside
the checks that exist to catch bugs**.

- A check of the form "every recorded horizon equals the intended horizon" is
  **vacuously true over an empty list**. The field it read lives on the tool-call
  record rather than the run record, so it found nothing and passed. The horizon
  was in fact correct, verified elsewhere — but the check could not have told
  anyone otherwise.
- The mirror image: another check read a column that does not exist in the run
  file, got the empty default, and **failed a run in which every arm agreed**.

**Both now treat "I could not find the evidence" as a failure with its own
message**, distinct from "I found the evidence and it disagrees".

⚠ **This is the single most reusable lesson in the project** and it generalises
past this thesis: *an automated check that silently passes when its input is
missing is worse than no check, because it converts an unknown into a false
assurance.* It is worth one sentence in the methodology chapter's validity
discussion.

---

# What the methodology chapter can claim, and how

The defensible claim is **not** "the harness is correct". It is:

> The experimental apparatus was verified before it was used, the verification
> itself was audited, and both the defects found and the cost of finding them
> late are documented.

Three things make that claim concrete:

1. **Pre-flight checks run without spending anything**, so contract violations
   surface before any request is issued.
2. **A smoke run exercises every arm once**, because checks that never send a
   request cannot see anything that only appears when a scenario actually runs.
3. **A dry run prints the resolved configuration** rather than assuming it —
   which is how defect 4 was caught, one step before launch.

⚠ **Point 3 is the one to emphasise.** Printing what a flag resolved to, instead
of trusting that it resolved as intended, is what converted a silent 33 per cent
overspend into a caught defect. The general form: *a parameter that is derived
rather than given must be displayed, not assumed.*

---

# The honest limitation

⚠ **All four defects were found by inspection and by one person's dry run, not by
an automated test suite.** There is no test coverage over the experiment harness,
and the thesis should say so rather than implying a testing regime it does not
have.

The honest framing: the harness is verified by **pre-flight contract checks, a
cheap end-to-end smoke, and a printed dry run**, which is a weaker guarantee than
unit tests and a stronger one than nothing. The four defects above are evidence
that the regime finds real problems, and equally that it depends on someone
looking.

---

# Related

- `ch8_experiment/brand-sampling-and-inclusion-criteria.md` — the sampling
  criteria defect 4 threatened
- `anticipated-assessor-questions.md` — the defence-facing version
- P0049 `findings.md` F51, F55, F56, F59 — the sources, with the code
