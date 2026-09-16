---
name: 2026-09-15_NLM_ch1-citation-verification-pass-followup-01
description: FOLLOWUP - Withdraws F2 from the Chapter 1 pass. The Liu 2025 repoint it proposed cannot be done, because that source is not in the library at all. Replaces it with a fix that works today.
category: workflow
applies-to: [ch1_introduction]
triggers: [ch1 citations, liu 2024, edge AI citation, ch1 followup]
created: 2026_09_15-12_55
updated: 2026_09_15-12_55
snapshot: 2026-09-15_10-49_final-comment-sweep
status: prose ready to paste, awaiting human review
---

# Follow-up 01 to the Chapter 1 pass

Verified at `37a04f0`, fetch clean. Same snapshot
`2026-09-15_10-49_final-comment-sweep`, same Zotero pull (10:49:34, 92 items).

**Why this is a separate file:** you have read the main pass, so that file is
frozen. Editing F2 in place would hide a correction inside a document you have
already worked through.

| In the main pass | Status |
|---|---|
| **F2** | ⚠ **withdrawn and replaced** — see W1 below |
| Everything else — F1, F3, F4, F5, F6, the rejections, the register rows | ✅ **stands unchanged** |

---

# W1 — ⚠ I was wrong about F2, and you may have pasted it

**F2 said the fix was a one-character year change**, `(Liu et al., 2024)` →
`(Liu et al., 2025)`, on the reasoning that Ch2 §2.2 already cites an edge-AI
`Liu et al. (2025)`. I marked it NEEDS-BRIAN pending one lookup.

**I have now done that lookup properly, and the answer kills the fix.**

## The evidence

I parsed **all 92 `bibtex.bib` entries** for any author named Liu, and searched
both exports for quantisation, distillation, edge deployment, compression and
resource constraints. **The entire library contains exactly one Liu:**

```
[liu_a_2024]  "A Dynamic LLM-Powered Agent Network for
               Task-Oriented Agent Collaboration"     (DyLAN, arXiv:2310.02170)
```

⚠ **There is no `Liu et al. (2025)` to repoint to.** Ch2 §2.2 is citing a source
we do not have — which is now F1 in the Chapter 2 note, alongside Semerikov et
al. (2025), equally absent.

**So F2 as written would have replaced a citation pointing at the wrong paper
with a citation pointing at no paper.** That is worse, and it is worse in the
harder-to-detect direction: the reference list would silently drop it.

## What is still true

✅ **The defect F2 identified is real and unchanged.** Ch1 §1.1 cites
`liu_a_2024` — a multi-agent collaboration preprint — for a claim about hardware
memory budgets in the edge-AI literature. It cannot support that claim.

---

# The replacement fix — works today, needs no new source

### Anchor

**Chapter 1, Section 1.1** — the paragraph beginning **"Yet the practical
deployment of predictive AI systems in business settings faces a constraint..."**.
Searchable, verbatim:

> "this differential compounds into an order-of-magnitude difference in operating cost, which is why resource-efficient deployment is treated as a first-order constraint in the edge and resource-constrained AI literature (Liu et al., 2024)."

**The sentence after it begins:**
> "Ng (2017), working with four terabytes of Nielsen weekly scanner data..."

### Action

REWORD — drop the citation, keep the sentence.

#### Replace with

> "this differential compounds into an order-of-magnitude difference in operating cost, which is why resource-efficient deployment is treated as a first-order constraint in the edge and resource-constrained AI literature."

### Note — why removing beats substituting

✅ **The claim does not need this citation.** The very next sentence cites Ng
(2017) for exactly the same point with a source we own and have read, and §1.4
cites Ng again for the formal design criterion. The paragraph is not left
unsupported.

✅ **Ch2 §2.2 is where the edge-AI literature is properly reviewed.** Chapter 1 is
motivation; it does not owe a survey citation here.

⚠ **If you prefer to keep a citation**, the honest options are to resolve Ch2's
missing sources first (Ch2 note, F1) and then cite whichever real paper replaces
Liu 2025 — or to cite Ng (2017) here too. **Do not restore the 2024.**

---

# One more thing this turned up — a bad year in the library

⚠ **`liu_a_2024` carries `2026` in its bibtex year field**, while the reference
list renders it as 2024 and both chapters cite it as 2024.

```
[liu_a_2024] 2026 | Liu Zijun, Zhang Yanzhe, Li Peng, Liu Yang, Yang Diyi
```

**Fix the year in Zotero before generating the dynamic reference list**
(thread 277), or the bibliography will print 2026 against in-text citations that
say 2024. This is the same class of problem as the missing years on the
*Elements of Statistical Learning* records.

---

# Corrected register rows

The main pass filed F2's dependency as *"check whether Liu 2025 is in the group
library"*. **That is now answered: it is not.** The row is replaced by:

| Claim | Where | To verify |
|---|---|---|
| *"quantisation and distillation... substantial accuracy preserved at sharply reduced memory footprints"* | **Ch2 §2.2**, not Ch1 | **Which real source states this?** Cited as Liu et al. (2025); absent from the library |

→ **Ch1 no longer carries a citation debt here** once W1 is pasted. The debt
moves to Chapter 2, where the claim actually lives.
