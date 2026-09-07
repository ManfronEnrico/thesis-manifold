---
name: prose-insertion-discipline
description: RULE - Thesis prose is never delivered as loose paragraphs. Every block carries a verbatim anchor from a named snapshot, an explicit action, and an in-text/appendix decision for every asset.
category: workflow
applies-to: [thesis prose, writing-notes, docx insertion, appendix references]
triggers: [writing prose, converting bullets to prose, preparing paragraphs for Word, citing a table or figure in prose]
created: 2026_09_07-15_00
updated: 2026_09_07-15_00
---

# Prose insertion discipline

Prose that does not say **where it goes** is unfinished work. The reader of a writing
note is a human with a Word document open; delivering paragraphs without placement moves
the hard part — locating the seam — onto them.

## Quick Reference

| Requirement | Failure it prevents | Detail |
|---|---|---|
| Anchor is a verbatim quote | "Add to Ch6" — the human hunts for the spot | [Anchors](#anchors) |
| Snapshot named in frontmatter | Anchors that no longer exist | [Snapshot currency](#snapshot-currency) |
| Explicit action verb | Ambiguity between adding and replacing | [Actions](#actions) |
| Asset marked in-text or appendix | 12-row grids inlined into paragraphs | [Assets](#assets) |
| Unverified citations marked + filed | Invented sources reaching the thesis | [Citations](#citations) |
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

## Related

- `.claude/skills/write-prose-from-bullets/SKILL.md` — the workflow implementing this
- `.claude/rules/writing-surface-authority.md` — the `.docx` is authoritative; notes stage
- `.claude/rules/rule-priority-hierarchy.md` — bullets-before-prose (Quality tier)
