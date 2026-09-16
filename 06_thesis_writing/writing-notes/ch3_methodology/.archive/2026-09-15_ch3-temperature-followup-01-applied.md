---
name: 2026-09-15_BRANCH_A_ch3-temperature-followup-01
description: FOLLOW-UP - The temperature fix was added rather than substituted, so 3.6 now asserts both that outputs are reproducible at temperature zero and that the model has no temperature parameter. The new sentence also drops a "not", inverting its meaning. One passage replaces both.
category: workflow
applies-to: [ch3_methodology]
triggers: [temperature, decoding, reliability, ch3]
created: 2026_09_15-12_20
updated: 2026_09_15-12_20
snapshot: 2026-09-15_12-14_post-temperature-fix
status: prose ready to paste, awaiting human review
---

# The temperature fix landed beside the old claim, not over it

Verified at `b2e366a`, fetch clean. Snapshot
`2026-09-15_12-14_post-temperature-fix`.

**This supersedes `2026-09-15_BRANCH_A_ch3-temperature-contradiction.md`**, which
stays live until this is applied. Its diagnosis was right; its fix was a REWORD of
one sentence, and what reached the document was an INSERT after that sentence. So
the false clause survives alongside the correction.

---

# What §3.6 says right now, verbatim

> "Language-model non-determinism is a property of the object under study rather
> than of the evaluation instrument: **outputs at temperature zero are highly
> reproducible** but not guaranteed to be identical across provider versions.
> **Especially in the case of the evaluated LLM model gpt-5.5-2026-04-23, it does
> allow the parameter temperature at all inside the payload**, which is precisely
> why consistency is measured over repeated runs rather than assumed."

**Two defects, and the second is the serious one.**

## 1 — the original false claim is still present

*"outputs at temperature zero are highly reproducible"* asserts a decoding control
this model does not offer. `srq4_experiment.py:178-188` records that `gpt-5.5`
rejects both `temperature` and `top_p` with HTTP 400, and states in a comment that
*"Reporting temperature 0 in the methodology would be false."*

## 2 — ⚠ the new sentence says the opposite of what it means

> "it **does allow** the parameter temperature at all inside the payload"

**A "not" is missing.** As written this says the model *does* allow temperature —
which contradicts both the intent and the sentence before it. The construction
"at all" only works with a negative: *does **not** allow … at all*.

⚠ **Read literally, the paragraph now claims the model both has and has not got a
temperature parameter, in consecutive sentences.** This is more visible than the
original defect, not less.

**Also:** *"the evaluated LLM model gpt-5.5-2026-04-23"* reads as a stacked label
("LLM model"), and the model identifier is already given in §3.5.4, so §3.6 does
not need to repeat it.

---

# The fix

## F1 — replace both sentences with one

### Anchor

**Chapter 3, Section 3.6 Validity and Reliability**, inside the paragraph
beginning **"Reliability is ensured through code versioning..."**. The span runs
from *"Language-model non-determinism"* to *"...rather than assumed."*

Searchable, verbatim — the whole span to replace:

> "Language-model non-determinism is a property of the object under study rather than of the evaluation instrument: outputs at temperature zero are highly reproducible but not guaranteed to be identical across provider versions. Especially in the case of the evaluated LLM model gpt-5.5-2026-04-23, it does allow the parameter temperature at all inside the payload, which is precisely why consistency is measured over repeated runs rather than assumed."

The sentence before it ends *"...is recorded as a limitation."* The sentence after
begins *"Every call is logged with its exact prompt and output..."*

### Action

REPLACE — the full span above, both sentences, with the single sentence below.

#### Replace with

> Language-model non-determinism is a property of the object under study rather
> than of the evaluation instrument: the evaluated model rejects the temperature
> and top-p parameters outright, so decoding cannot be constrained and outputs are
> in any case not guaranteed to be identical across provider versions, which is
> precisely why consistency is measured over repeated runs rather than assumed.

### Note — what this keeps and what it drops

✅ **Keeps the conclusion unchanged** — consistency is measured, not assumed — and
keeps the provider-version point, which is a second, independent reason.

✅ **States the mechanism plainly**: the parameters are rejected. That is stronger
than "cannot be constrained" alone, because it says why.

**Drops the model identifier**, which §3.5.4 already gives two sections earlier
along with the reasoning-effort setting. Repeating it here adds nothing and
invites the two statements to drift apart.

⚠ **Do not reintroduce "temperature zero" anywhere in the thesis.** After this
edit the phrase appears nowhere in any chapter — I checked all seventeen files.

---

# Why this matters beyond tidiness

**It is Chapter 8's headline finding that depends on this sentence.** The
consistency result — the tool-backed scenarios returning an identical figure on
every repeat while the code-writing scenarios do not — is *more* impressive when
decoding was uncontrolled.

⚠ **Claiming temperature zero implies the variance survived a control that was
never applied**, which is both false and a weaker claim than the truth.

---

# Verification

| Claim | Checked against |
|---|---|
| the span as quoted | snapshot `ch3-methodology.md` line 77, verbatim |
| the model rejects both parameters | `srq4_experiment.py:178-188`, at `b2e366a` |
| §3.5.4 already carries the model pin | snapshot `ch3-methodology.md` line 67 |
| "temperature zero" appears nowhere else | grep across all 17 chapter files — one hit, this one |

**No new citation.** The replacement removes a false claim and adds none.
