---
name: 2026-09-15_BRANCH_A_ch1-chapter-count
description: FIX - Section 1.5 still says the thesis is organised into nine chapters. There are ten, and 1.5's own map lists Chapter 10. Carried forward from the consolidated note, which was archived with this one fix outstanding.
category: workflow
applies-to: [ch1_introduction]
triggers: [chapter count, 1.5, thesis structure]
created: 2026_09_15-12_05
updated: 2026_09_15-12_05
snapshot: 2026-09-15_11-51_post-consolidated-fixes
status: prose ready to paste, awaiting human review
---

# Section 1.5 undercounts the chapters by one

Verified at `b2e366a`, fetch clean. Snapshot
`2026-09-15_11-51_post-consolidated-fixes`.

**Carried forward from `2026-09-15_BRANCH_A_CONSOLIDATED-remaining-fixes.md`
(F3), which is archived.** Every other fix in that document is applied and
verified; this one is not.

✅ **You rewrote the second half of this sentence** — it now maps onto *"the six
activities of the Design Science Research process"* rather than claiming one
chapter per phase, which is the more accurate framing. **The count at the front of
the sentence was not changed with it.**

---

# The fix

## F1 — §1.5, the chapter count

### Anchor

**Chapter 1, Section 1.5 Thesis Structure**, the opening sentence. Searchable,
verbatim:

> "The remainder of this thesis is organised into nine chapters, that map onto the six activities of the Design Science Research process (Peffers et al., 2007)."

### Action

REWORD — `nine` → `ten`.

**After:**
> "The remainder of this thesis is organised into ten chapters, that map onto the
> six activities of the Design Science Research process (Peffers et al., 2007)."

### Note — ten is correct, verified two ways

✅ **The document has ten numbered chapters.** Chapter 1 through Chapter 10, one
file each in the snapshot.

✅ **§1.5's own map lists eight entries, Chapter 2 through Chapter 10** — because
it does not describe Chapter 1, which is the chapter the reader is already in.
Eight entries plus the current chapter plus Chapter 4, which the map covers, is
ten.

⚠ **"The remainder" does not rescue "nine".** If the count were meant to exclude
Chapter 1, the map beneath would list nine entries; it lists eight. The sentence
counts the whole thesis, so it must say ten.

---

# Verification

| Claim | Checked against |
|---|---|
| the sentence as quoted | snapshot `ch1-introduction.md` line 87, verbatim |
| ten chapter files exist | snapshot `chapters/`, ch1 through ch10 |
| §1.5's map runs Chapter 2 to Chapter 10 | snapshot `ch1-introduction.md` lines 87-110 |

**No new citation.** The Peffers reference already in the sentence is unchanged.
