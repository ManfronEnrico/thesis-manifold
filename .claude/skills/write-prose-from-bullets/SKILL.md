---
name: write-prose-from-bullets
description: "SKILL - Convert an approved bullet skeleton into thesis prose with EXACT .docx insertion points. Regenerates the snapshot, reads the target sections, writes paragraphs anchored to quoted sentences, flags every asset as in-text or appendix, and routes unverified citations to the NotebookLM claims folder. Triggers: write prose, turn bullets into prose, prose for chapter N, insert into the docx, where do these paragraphs go."
metadata:
  version: "1.0"
  last_updated: "2026-09-07"
  status: active
  related_rules:
    - writing-surface-authority
    - prose-insertion-discipline
---

# Write prose from bullets

Converts an approved bullet skeleton into prose that a human can paste into the OneDrive
`.docx` **without having to work out where it goes**.

The deliverable is not paragraphs. It is *paragraphs plus a placement contract*: for each
block, the exact sentence to search for, what to do relative to it, and which tables and
figures to cite in-text versus send to the appendix.

---

## The rule this exists to serve

Prose lives in **one** place: the OneDrive `.docx` (see `writing-surface-authority`).
This skill never edits the `.docx` and never edits a snapshot. It produces a staging
document under `06_thesis_writing/writing-notes/` that the human executes by hand.

**Prose requires explicit human approval** (bullets-first, Quality tier). Do not run
Phase 3 without it.

---

## Phases

### Phase 0 — Bullets must exist and be approved

Confirm a bullet `.md` exists in `06_thesis_writing/writing-notes/`. If not, write the
bullets first and stop for approval.

**Do not proceed to prose on an implied yes.** "Write this up" authorises bullets. Prose
needs the user to say so.

### Phase 1 — Decide the snapshot (ASK, do not assume)

Prose must be anchored to the *current* document, and the anchors are quoted sentences.
A stale snapshot produces anchors that no longer exist.

**Ask exactly this:**

> Should I regenerate the `.docx` snapshot first? Regenerate if the Word file has been
> edited since `<newest snapshot folder name>`; skip if nothing has changed and I can
> read that one.

To regenerate:

```bash
python utility_scripts/scripts/thesis_snapshot.py --label "<short slug>"
```

`--label` (alias `--slug`) appends to the timestamp:
`06_thesis_writing/docx-exported-snapshots/YYYY-MM-DD_HH-mm_<slug>/`.

**Record which snapshot the prose was written against, in the note's frontmatter.** Every
anchor is only valid relative to it.

### Phase 2 — Read the target sections, and verify the chapter map

**Never guess chapter numbers.** They drift. Read:

```
<snapshot>/chapters/sections/          # numbered dirs, one per Heading 1
<snapshot>/chapters/sections/<NN-chapter>/<section>/   # leaf .md per heading
<snapshot>/comments/sections/<same path>               # objections on that section
```

Two things to extract per target section:

1. **The anchor sentence** — the exact text to search for in Word. Quote it verbatim,
   including any typos; that is what makes it findable.
2. **Open comments** — a Word thread anchored on the sentence you are about to change is
   usually the *reason* the change is needed. Name the thread number; closing it is part
   of the deliverable.

### Phase 3 — Write prose against the real text

Read the target section's existing prose before writing, and match its register,
paragraph length and terminology. Prose that reads as an insert defeats the purpose.

**While writing, check every factual claim the surrounding text already makes.** Counts,
totals and cross-references in the anchor paragraph are frequently stale. Report what you
find; do not silently amend a number you have not verified — see Anti-patterns.

### Phase 4 — Produce the placement contract

For every block:

```markdown
### P<n> — <Chapter> §<section> <title>

> **File:** <path within the snapshot>
> **Word comment <N>** is anchored here — <what it asks>  [if applicable]

**Anchor:**
> "<verbatim sentence from the .docx>"

**Action:** REPLACE | INSERT AFTER | APPEND | EDIT-THEN-INSERT

**Assets:**
- **In-text:** <table/figure to place in the body, with its content if new>
- **Appendix, cite don't inline:** <numbered appendix tables>
- **Figure:** <needed / not needed, and why>
```

**Actions mean exactly:**

| Action | Meaning |
|---|---|
| `REPLACE` | The anchor sentence/paragraph goes away, prose takes its place |
| `INSERT AFTER` | Anchor stays untouched; prose follows it |
| `APPEND` | Add to the end of the named section |
| `EDIT-THEN-INSERT` | Anchor needs a small change **first** (a count, a table row), then prose is added. Spell out both steps separately. |

**Match the target's form.** A section that is a bullet list takes bullets, not
paragraphs. Check before writing.

### Phase 5 — Assets: in-text or appendix

Decide for every asset, and say which:

- **In-text** — the reader cannot follow the argument without it. Keep it small: a
  3–5 row summary beats a 12-row grid.
- **Appendix** — completeness, provenance, full grids, diagnostics. Cite by number;
  never inline.

If a new body table is introduced, state **what it renumbers** and warn that plain-text
table callouts (as opposed to Word field references) will not update automatically.

### Phase 6 — Route unverified citations

Any in-text citation not verified against the Zotero library is marked inline:

```
(Ma et al., 2021 UNVERIFIED)
```

and written to a claims file under:

```
06_thesis_writing/notebookLM/04-Claims_Verification/Chapter <N> - <Name>/<Topic>/
```

**Prefer avoidance to marking.** If a claim can be written so it rests on measured
project data rather than a remembered citation, write it that way — an
`UNVERIFIED` tag is a debt, and prose with no debt can be pasted immediately.

Also update the register at `writing-notes/unverified-claims-to-check.md`.

### Phase 7 — Report

State plainly:

- Which snapshot the anchors are valid against
- Which Word threads this closes
- **What is blocked and why** — never silently omit a block whose evidence is not ready
- Any discrepancy found in the existing text, as a flag, not a fix

---

## Anti-patterns

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| "Add this to Chapter 6" | The human has to find the spot; numbering drifts | Quote the anchor sentence |
| Guessing chapter numbers from memory | Ch6 may be Benchmark, not Discussion | Read `chapters/sections/` |
| Writing prose against an old snapshot | Anchors will not be findable | Ask about regeneration first |
| Silently correcting a stale number | You may be wrong about what it counted | Flag it; let the human decide |
| Inlining a 12-row grid | Unreadable in a body paragraph | Summary in-text, full grid in appendix |
| Inventing a citation to support a sentence | This is the failure the claims folder exists for | Write from measured data, or mark UNVERIFIED |
| Pasting prose into a section that is bullets | Breaks the section's form | Match the target |
| Editing the `.docx` or a snapshot | Both are off-limits | Stage in writing-notes |

---

## Definition of done

- [ ] Snapshot decision made **by the user**, and the snapshot named in frontmatter
- [ ] Every block has a verbatim anchor + an explicit action
- [ ] Every number traced to a result file, and verified programmatically where possible
- [ ] Every asset marked in-text or appendix
- [ ] Every unverified citation marked inline **and** filed under `04-Claims_Verification/`
- [ ] Word comment threads this closes are named
- [ ] Blocked blocks stated as blocked, with the dependency

---

## Related

- `.claude/rules/prose-insertion-discipline.md` — the rule this skill implements
- `.claude/rules/writing-surface-authority.md` — why the `.docx` is authoritative
- `utility_scripts/scripts/thesis_snapshot.py` — snapshot generator (`--label`)
- `06_thesis_writing/notebookLM/04-Claims_Verification/` — unverified-citation destination
