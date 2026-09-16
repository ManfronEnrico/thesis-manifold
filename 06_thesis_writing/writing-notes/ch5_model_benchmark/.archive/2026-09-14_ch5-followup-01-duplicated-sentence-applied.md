---
name: 2026-09-14_BRANCH_A_ch5-followup-01-duplicated-sentence
description: FOLLOW-UP - One sentence is printed twice at the opening of 5.4.1. Flagged as a side-note in the consolidated pass and therefore missed; raised here as its own fix so it is not missed again.
category: workflow
applies-to: [ch5_model_benchmark]
triggers: [ch5 prose pass, proofreading]
created: 2026_09_14-12_20
updated: 2026_09_14-12_20
snapshot: 2026-09-14_11-55_ch9-followup-defence-and-anchoring
status: prose ready to paste, awaiting human review
---

# Chapter 5 — follow-up 01, one duplicated sentence

Verified at `41ecb76`, fetch clean. Snapshot
`2026-09-14_11-55_ch9-followup-defence-and-anchoring`.

**Everything in the consolidated pass stands.** All five citation fixes and the
Chapter 6 cross-reference are applied and verified in this snapshot. This
follow-up raises **one item that did not get applied**, and the reason it did not
is a defect in how I wrote the note rather than anything you missed.

| In the consolidated pass | Status |
|---|---|
| Fixes 1–5, the book citations | ✅ **applied** |
| The 5.7 cross-reference, Chapter 7 → Chapter 6 | ✅ **applied** |
| The duplicated sentence in 5.4.1 | ❌ **not applied** — see below |

⚠ **My error, and worth recording as a habit.** I buried this inside Fix 3's
anchor block as a parenthetical — *"delete one of the two while you are in
there"* — rather than giving it its own numbered fix. An instruction inside
another fix's preamble is an instruction that gets read past. **A separate
change needs a separate heading, however small it is.**

---

# The fix

## F1 — 5.4.1 opens by saying the same thing twice

### Anchor

**Section 5.4.1 Why WMAPE is the primary metric.** The **first two sentences** of
the section, immediately after the heading:

> "The choice is not conventional but theoretical. The choice is theoretical
> rather than conventional."

The third sentence, which stays, begins: *"A scoring function determines which
functional of the predictive distribution an optimal forecast reports..."*

### Action

REWORD — delete the second sentence, keep the first.

**Before:**
> "The choice is not conventional but theoretical. The choice is theoretical
> rather than conventional. A scoring function determines which functional..."

**After:**
> "The choice is not conventional but theoretical. A scoring function determines
> which functional..."

### Note — which of the two to keep, and why it is not arbitrary

The two sentences carry identical meaning, so either could go. **Keep the first.**

*"Not conventional but theoretical"* puts the emphasis on the second term, which
is what the paragraph then spends four sentences establishing via Gneiting. *"Theoretical
rather than conventional"* has the same structure but lands the stress on the
contrast rather than on the claim, and it reads as the weaker opening of the two.

Either is defensible. The reason to decide it here rather than leave it open is
that a section opening is the most-read sentence in a section, and this one
currently stutters.

### Note — most likely how it got there

This has the shape of an edit applied twice: a rewrite of the opening sentence
pasted in without the original being removed. Worth a quick look at whether the
same thing happened elsewhere in the chapter — I checked 5.4.1 through 5.5.10
and found no other instance, but I searched for this exact pattern rather than
for duplication generally.
