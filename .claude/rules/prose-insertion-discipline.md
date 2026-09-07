---
name: prose-insertion-discipline
description: RULE - Thesis prose is never delivered as loose paragraphs. Every block carries a verbatim anchor from a named snapshot, an explicit action, and an in-text/appendix decision for every asset.
category: workflow
applies-to: [thesis prose, writing-notes, docx insertion, appendix references]
triggers: [writing prose, converting bullets to prose, preparing paragraphs for Word, citing a table or figure in prose]
created: 2026_09_07-15_00
updated: 2026_09_07-16_40
---

# Prose insertion discipline

Prose that does not say **where it goes** is unfinished work. The reader of a writing
note is a human with a Word document open; delivering paragraphs without placement moves
the hard part — locating the seam — onto them.

## Quick Reference

| Requirement | Failure it prevents | Detail |
|---|---|---|
| Anchor is a verbatim quote | "Add to Ch6" — the human hunts for the spot | [Anchors](#anchors) |
| Anchor carries its neighbours | The human cannot tell one paragraph from the next | [Anchor context](#anchor-context) |
| Snapshot named in frontmatter | Anchors that no longer exist | [Snapshot currency](#snapshot-currency) |
| Comments are read before writing | Rewriting text the author already objected to | [Comment-driven passes](#comment-driven-passes) |
| Explicit action verb | Ambiguity between adding and replacing | [Actions](#actions) |
| REWORD offered where a sentence is salvageable | A whole paragraph rewritten to fix six words | [Actions](#actions) |
| Asset marked in-text or appendix | 12-row grids inlined into paragraphs | [Assets](#assets) |
| Unverified citations marked, filed AND registered | Invented sources reaching the thesis | [Citations](#citations) |
| Blocked blocks declared | Silent omission of unfinished work | [Blocking](#blocking) |

---

## Anchors

Every prose block quotes the **exact existing sentence** it attaches to, copied verbatim
from the snapshot — including typos, which are what make it findable by search.

```markdown
**Anchor:**
> "The feature matrix contains 22 columns: 14 modelling features per observation"

**Action:** EDIT-THEN-INSERT
```

An anchor is required even when appending to a section's end: quote the last sentence.

**Never cite a chapter number from memory.** Read `<snapshot>/chapters/sections/`.
Numbering drifts, and a confident wrong number sends the human to the wrong chapter.

## Anchor context

A bare sentence is not enough to place a paragraph. The human is scrolling a Word
document looking for a seam, and "insert after this sentence" is ambiguous the moment
the sentence sits mid-paragraph.

**Every anchor names its position in the paragraph, and quotes what surrounds it.**

| Insertion | What to quote |
|---|---|
| A **new paragraph** between two existing ones | The **last sentence of the preceding paragraph**, plus the first sentence of the following one |
| A sentence **inside** a paragraph | The sentence before *and* after, so the seam is unambiguous |
| A **replacement** of existing text | The full span being replaced, start to end |
| A **reword** of one sentence | That sentence alone, plus a note of which paragraph it sits in |

```markdown
**Anchor** — end of the paragraph beginning "The panel is filtered to...":
> "...leaving 95 brands that satisfy the minimum-history requirement."

**Next paragraph begins:**
> "Feature construction proceeds from this filtered panel."

**Action:** INSERT AFTER — new paragraph between the two.
```

Quoting the following sentence costs one line and removes the commonest failure: prose
landing in the right section but the wrong seam.

## Comment-driven passes

When a chapter is being revised against the author's own Word comments, the comments are
**read first, in full, for the whole chapter** — before any prose is written.

Comments are exported by the snapshot to `<snapshot>/comments/`, mirroring
`chapters/` file for file, and each carries an `**On:**` field holding the anchored text
verbatim. **That field is the anchor** — do not reconstruct one by hand when the export
already has it.

Reading a whole chapter's comments before writing is what reveals that *n* comments are
one underlying issue. Eight `INCORRECT` threads on a split definition are one fact and
one replacement block, not eight edits. Section-by-section reading cannot see that.

Each comment gets an explicit verdict, and unaddressed is not a verdict:

| Verdict | Meaning |
|---|---|
| **ADDRESSED** | Prose in this note fixes it; name the block |
| **VERIFIED-OK** | Checked against a result file; the text is already correct. Say what was checked |
| **FLAGGED** | Real, but out of scope or blocked. Name the dependency |
| **REGISTERED** | A `SOURCE` comment; routed to the claims register (see below) |
| **NEEDS-BRIAN** | A decision only the author can make |

## Snapshot currency

Anchors are only valid against the document they were read from. The writing note's
frontmatter names the snapshot:

```yaml
snapshot: 2026-09-07_14-29_holiday-enrichment
```

**Ask the user whether to regenerate before writing** — they know whether Word has been
edited since. Do not decide this unilaterally in either direction: regenerating
needlessly is noise, and skipping when the file has moved produces anchors that cannot
be found.

```bash
python utility_scripts/scripts/thesis_snapshot.py --label "<slug>"
```

## Actions

| Action | Meaning |
|---|---|
| `REPLACE` | Anchor text is removed; prose takes its place |
| `INSERT AFTER` | Anchor untouched; prose follows |
| `APPEND` | Added to the end of the named section |
| `EDIT-THEN-INSERT` | Anchor changes first (a count, a table row), *then* prose is added — spell out both steps |
| `REWORD` | One sentence is rewritten in place. Give **before and after in full**, so the human can compare and paste |

**Offer `REWORD` whenever a sentence is salvageable.** A comment saying a clause is wrong,
unsourced or clumsy usually needs that clause changed — not the paragraph replaced.
Replacing a whole paragraph to fix six words discards prose the author already approved
and makes the diff impossible to check.

```markdown
**Action:** REWORD

**Before:**
> "The split is fixed by calendar date and locked as a pre-specified design decision."

**After:**
> "The split is defined proportionally, with each category's panel divided by share of
> its available periods rather than by a fixed calendar date."
```

When several rewords land in one paragraph, say so — the human applies them in one pass
rather than hunting the same paragraph four times.

**Match the target's form.** A bullet-list section takes bullets. Check the snapshot
before writing paragraphs into a list.

## Assets

Every table, figure or diagram gets a decision, stated in the block:

- **In-text** — the argument fails without it. Keep it small; a 3–5 row summary beats
  the full grid.
- **Appendix, cite don't inline** — provenance, full grids, diagnostics. Cite by number.

When a new body table is introduced, state **what it renumbers**, and warn that
plain-text table callouts do not update automatically the way Word field references do.

## Citations

Any citation not verified against the Zotero library is marked inline and filed:

```
(Ma et al., 2021 UNVERIFIED)
```

→ `06_thesis_writing/notebookLM/04-Claims_Verification/Chapter <N> - <Name>/<Topic>/`
→ and the register at `writing-notes/unverified-claims-to-check.md`

### A `SOURCE` comment is a verification request, not a prose problem

A Word comment tagged `SOURCE` says *this assertion needs a citation*. Answering it by
writing a citation from memory is the precise failure that created CV-01.

**Every `SOURCE` comment produces a register row instead**, stating exactly what a
verification run must establish — phrased so it can be answered **yes or no** against a
document:

```markdown
| N | <the claim, as the thesis states it> | ch4 §4.4, Word thread 184 | **To verify:** does an
authoritative source state a minimum series length for ARIMA parameter estimation, and is
it ~24 periods? |
```

The row records the *question*, not a guessed answer. The verification run then either
finds a source — which the author adds to Zotero and cites — or does not, and the claim
is reworded to stand on measured project data.

Bare `SOURCE` comments with no comment text are common; the `**On:**` field carries the
claim. Read the anchored sentence and write the question from that.

**The register is the single queue.** A claim named in a writing note but absent from
`unverified-claims-to-check.md` will not be verified, because the register is what gets
worked through.

**Prefer avoidance to marking.** Prose resting on measured project data carries no debt
and can be pasted immediately. An `UNVERIFIED` tag is a promise to come back.

**If a source is not in the library, it is not a source.** This rule exists because a
plausible-looking reference was once written from memory and read as though verified.

## Blocking

A block whose evidence is not ready is **declared blocked, with its dependency** — never
quietly dropped and never written speculatively.

```markdown
**Action:** BLOCKED until `srq1_stability.py` finishes (task 21).
Two sentences in §6.5.9 and §6.6 are false as written until it lands.
```

Stating that existing prose is *currently wrong* is part of the deliverable. A human who
does not know a sentence is false will leave it in.

## Found discrepancies

Stale numbers in the surrounding text are **flagged, not fixed**. You rarely know what a
count was originally measuring, and a silent amendment replaces a known-stale number with
a confidently-wrong one.

```markdown
⚠ "22 columns" — the matrix has 54. Establish what it was counting before amending.
```

---

## Where the surfaces live

| Surface | Path | Editable? |
|---|---|---|
| Authoritative prose | the OneDrive `.docx` | **only here** |
| Snapshot (read-only mirror) | `06_thesis_writing/docx-exported-snapshots/<stamp>_<slug>/` | never |
| ↳ prose per section | `<snapshot>/chapters/sections/<NN-chapter>/<section>/` | never |
| ↳ **comments per section** | `<snapshot>/comments/sections/<same path>` | never |
| ↳ **comments per chapter** (tagged index) | `<snapshot>/comments/<chN>.md` | never |
| Staged prose + placement contracts | `06_thesis_writing/writing-notes/` | yes |
| Planning bullets | `06_thesis_writing/sections-drafts/` | yes — **no prose** |
| Claims register | `writing-notes/unverified-claims-to-check.md` | yes |
| Verification packs | `notebookLM/04-Claims_Verification/Chapter <N> - <Name>/` | yes |
| The library | `06_thesis_writing/citations/citations.json` | via Zotero export |

Comments mirror prose file for file. **Both come from the same snapshot run**, so a
snapshot that is current for prose is current for comments — and one that is stale is
stale for both.

---

## Related

- `.claude/skills/write-prose-from-bullets/SKILL.md` — the workflow implementing this
- `.claude/rules/writing-surface-authority.md` — the `.docx` is authoritative; notes stage
- `.claude/rules/rule-priority-hierarchy.md` — bullets-before-prose (Quality tier)
