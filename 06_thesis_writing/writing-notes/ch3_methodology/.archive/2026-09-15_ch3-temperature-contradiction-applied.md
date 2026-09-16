---
name: 2026-09-15_BRANCH_A_ch3-temperature-contradiction
description: FIX - Section 3.6 asserts outputs are reproducible at temperature zero, ten lines after 3.5.4 states decoding is not settable on this model. One reword, and the surrounding argument gets stronger.
category: workflow
applies-to: [ch3_methodology]
triggers: [temperature, decoding, reliability, ch3 prose pass]
created: 2026_09_15-11_20
updated: 2026_09_15-11_20
snapshot: 2026-09-15_10-49_final-comment-sweep
status: prose ready to paste, awaiting human review
---

# Chapter 3 contradicts itself about temperature

Verified at `37a04f0`, fetch clean. Snapshot `2026-09-15_10-49_final-comment-sweep`.

**Found while auditing the Ch8 design-rationale notes.** This is the same false
claim I removed from `export_appendix.py` this session, surviving in a second
place.

---

# The contradiction, ten lines apart

| Where | Says |
|---|---|
| **§3.5.4** (line 61) | *"decoding parameters are **not adjustable on this model**, so run-to-run consistency is a measured outcome rather than a controlled one"* ✅ |
| **§3.6 Validity and Reliability** (line 71) | *"outputs **at temperature zero** are highly reproducible but not guaranteed to be identical across provider versions"* ⚠ |

**§3.5.4 is correct.** `srq4_experiment.py:178-188` records that `gpt-5.5` rejects
both `temperature` and `top_p` with HTTP 400, sets `TEMPERATURE = None`, and
states in a comment that *"Reporting temperature 0 in the methodology would be
false."*

⚠ **§3.6 reports it in the methodology anyway** — which is precisely what the code
comment warns against, in the section whose subject is reliability.

---

# The fix

## F1 — §3.6, the reliability paragraph

### Anchor

**Section 3.6 Validity and Reliability.** The middle of the paragraph beginning
*"**Reliability** is ensured through code versioning..."*. Searchable, verbatim:

> "Language-model non-determinism is a property of the object under study rather than of the evaluation instrument: outputs at temperature zero are highly reproducible but not guaranteed to be identical across provider versions, which is precisely why consistency is measured over repeated runs rather than assumed."

The sentence before it ends *"...is recorded as a limitation."* The sentence after
begins *"Every call is logged with its exact prompt and output..."*

### Action

REWORD — that one sentence. The rest of the paragraph stands.

**Before:**
> "Language-model non-determinism is a property of the object under study rather
> than of the evaluation instrument: outputs at temperature zero are highly
> reproducible but not guaranteed to be identical across provider versions, which
> is precisely why consistency is measured over repeated runs rather than
> assumed."

**After:**
> "Language-model non-determinism is a property of the object under study rather
> than of the evaluation instrument: decoding cannot be constrained on the model
> evaluated here, and outputs are in any case not guaranteed to be identical
> across provider versions, which is precisely why consistency is measured over
> repeated runs rather than assumed."

### Note — the argument survives the correction, and improves

✅ **The conclusion is unchanged**: consistency is measured rather than assumed.
**The premise gets stronger.** Under the old sentence a reader could ask why
repeated runs were needed if temperature zero already made outputs "highly
reproducible". Under the corrected one the necessity is obvious — no decoding
control was available, so measurement was the only option.

⚠ **This matters for Chapter 8's headline finding.** The consistency result — two
scenarios returning an identical figure on every repeat while code-writing
scenarios do not — is *more* impressive when decoding was uncontrolled. Claiming
temperature zero implies the variance survived a control that was never applied.

**The model pin sentence in §3.5.4 needs no change.** It is already correct.

---

# Where else this claim lived

| Location | Status |
|---|---|
| `export_appendix.py:446` | ✅ **fixed this session** — now *"under identical decoding settings"* |
| `export_appendix.py:1431` | ✅ **fixed this session** — the redundant `Temperature` row removed, `Decoding` retained |
| **Ch3 §3.6** | ⚠ **this note** |
| Ch3 §3.5.4 | ✅ already correct |
| Ch6 §6.5 | ✅ already correct — concurs with §3.5.4 |

✅ **After F1 the document and the codebase agree**, and nothing in either claims
a decoding control that does not exist.

---

# Verification

| Claim | Checked against |
|---|---|
| §3.5.4 states decoding not adjustable | snapshot `ch3-methodology.md` line 61, verbatim |
| §3.6 states temperature zero | snapshot `ch3-methodology.md` line 71, verbatim |
| the model rejects both parameters | `srq4_experiment.py:178-188`, at `37a04f0` |
| Ch6 concurs | snapshot `ch6-architecture.md` line 65 |

**No new citation.** The reword removes a false claim and adds none.
