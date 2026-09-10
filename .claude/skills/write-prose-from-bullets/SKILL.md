---
name: write-prose-from-bullets
description: "SKILL - Convert approved bullets, or a chapter's Word comments, into thesis prose with EXACT .docx insertion points. Confirms the snapshot is current for BOTH prose and comments, inventories a chapter's comments before writing, anchors every block to quoted sentences plus their neighbours, offers REWORD for salvageable sentences, flags assets in-text or appendix, and turns every SOURCE comment into a claims-register row. Triggers: write prose, turn bullets into prose, prose for chapter N, work through my comments, address the comments in chapter N, insert into the docx, where do these paragraphs go."
metadata:
  version: "1.1"
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

**First, establish what the newest snapshot is and whether Word has moved since.**
The manifest records both the capture time and the source file's own modified time:

```bash
ls -t 06_thesis_writing/docx-exported-snapshots/ | head -3
grep -E "Captured|Source modified|Comments:"   06_thesis_writing/docx-exported-snapshots/<newest>/MANIFEST.md
```

If **Source modified** is later than **Captured**, the `.docx` has been edited since the
snapshot and anchors may be stale — say so rather than asking a blind question.

**A snapshot carries prose AND comments, and both must be current.** The comment export
is a point-in-time extract; a comment resolved in Word this morning still appears open in
yesterday's snapshot. When a pass is comment-driven, snapshot currency is not a
convenience — a stale extract means working threads the author has already closed.

**Then ask:**

> Newest snapshot is `<name>` (captured `<time>`, source last modified `<time>`,
> `<N>` comments). Regenerate before I start, or work from this one?

To regenerate:

```bash
python utility_scripts/scripts/thesis_snapshot.py --label "<short slug>"
```

`--label` (alias `--slug`) appends to the timestamp:
`06_thesis_writing/docx-exported-snapshots/YYYY-MM-DD_HH-mm_<slug>/`.

**Record which snapshot the prose was written against, in the note's frontmatter.** Every
anchor is only valid relative to it.

### Phase 2 — Read the target sections, and verify the chapter map

**Never guess chapter numbers.** They drift. The snapshot mirrors prose and comments
file for file:

```
<snapshot>/chapters/sections/<NN-chapter>/<section>/<leaf>.md   # the prose
<snapshot>/comments/sections/<NN-chapter>/<section>/<leaf>.md   # objections on it
<snapshot>/comments/<chapter>.md                                # whole-chapter roll-up + tagged index
```

Two things to extract per target section:

1. **The anchor sentence** — the exact text to search for in Word. Quote it verbatim,
   including any typos; that is what makes it findable.
2. **Open comments** — a Word thread anchored on the sentence you are about to change is
   usually the *reason* the change is needed. Name the thread number; closing it is part
   of the deliverable.

#### Phase 2B — For a comment-driven pass: inventory the WHOLE chapter first

When the job is "work through my comments on chapter N", read the chapter-level comment
file **before writing anything**. It carries a tagged index — section, tags, and the
opening words of each thread.

```bash
sed -n '/^## Index/,/^---/p' <snapshot>/comments/ch4-data-assessment.md
```

Then build a table: **thread → section → tag → underlying issue**, and group by the last
column. This is the step that pays for itself — *n* comments frequently reduce to far
fewer facts, and one block can close a whole cluster. Working section by section makes
that structurally invisible.

Each comment carries an `**On:**` field with the anchored text verbatim. **Use it as the
anchor** rather than reconstructing one from the prose file.

Tags observed in this project, and what each implies:

| Tag | Means | Usually produces |
|---|---|---|
| `INCORRECT` | A stated fact is wrong | `REWORD` or `REPLACE` — verify against a result file first |
| `OUTDATED` | Was true, no longer is | `REWORD`, once the current value is confirmed |
| `VERIFY` | The author doubts it | A check, then `VERIFIED-OK` or a fix |
| `SOURCE` | Needs a citation | A **register row**, never an invented citation |
| `APPENDIX` | Table belongs in the appendix | A citation, not inlined prose |
| `PROSE` | Bullets awaiting prose | New paragraphs |
| `CONTEXT` | Needs more explanation | `INSERT AFTER` |
| `FORMATTING` | Presentation only | Usually `NEEDS-BRIAN`; no prose |
| `METADATA` | Internal residue in the text | Deletion — flag it |
| `ACADEMIC` | Register or framing | A judgement call; propose, don't impose |

**Give every comment a verdict** (ADDRESSED / VERIFIED-OK / FLAGGED / REGISTERED /
NEEDS-BRIAN) — see `prose-insertion-discipline`. A comment silently skipped reads as a
comment overlooked.

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
> **Closes Word threads:** <N, N, N> — <what they ask>
> **Verified against:** <result file the numbers came from>

**Anchor** — <where in the section: "end of the paragraph beginning ...">:
> "<verbatim sentence from the .docx>"

**Following text begins:**            [when inserting a new paragraph]
> "<first sentence of the next paragraph>"

**Action:** REPLACE | INSERT AFTER | APPEND | EDIT-THEN-INSERT | REWORD

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
| `REWORD` | One sentence rewritten in place — give **before and after in full** |

**Prefer `REWORD` to `REPLACE` when a sentence is salvageable.** A wrong clause needs the
clause fixed, not the paragraph rewritten; replacing wholesale discards approved prose and
makes the change impossible to check by eye.

**Quote the neighbours, not just the anchor.** For a new paragraph, quote the last
sentence of the paragraph before *and* the first sentence of the one after. For a sentence
inside a paragraph, quote both sides of the seam. The human is scanning a Word document,
and a single sentence rarely identifies a position unambiguously.

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

#### Every `SOURCE` comment becomes a register row

A comment tagged `SOURCE` is a **verification request**. Answering it with a citation
written from memory is exactly the failure that created CV-01, so the answer is never a
citation — it is a row in `writing-notes/unverified-claims-to-check.md` stating what a
verification run must establish.

Write the row as a **yes/no question against a document**:

```markdown
| N | <the claim as the thesis states it> | ch4 §4.4, Word thread 184 | **To verify:**
does an authoritative source state a minimum series length for ARIMA parameter
estimation, and is it ~24 periods? |
```

Bare `SOURCE` comments carrying no text are common — the claim is in the comment's
`**On:**` field. Read the anchored sentence and write the question from that.

Then add the supporting material to the chapter's verification folder:

```
06_thesis_writing/notebookLM/04-Claims_Verification/Chapter <N> - <Name>/<Topic>/
```

so a NotebookLM run can be pointed at it. Two standing constraints from the existing
briefs, which the pack already encodes:

- **Never upload thesis chapters.** The notebook will return our own wording as a
  source — the failure that created CV-01.
- **Group by literature type, not by chapter.** A statistics question and a legal
  question in one notebook retrieve against each other's documents.

**The register is the queue.** A claim named only in a writing note will not be
verified, because the register is what gets worked through.

### Phase 7 — Report

State plainly:

- Which snapshot the anchors are valid against
- **Every comment in scope, with its verdict** — ADDRESSED / VERIFIED-OK / FLAGGED /
  REGISTERED / NEEDS-BRIAN. A comment with no verdict reads as one overlooked
- Which Word threads this closes
- Which claims went to the register, and what each asks
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
| Answering a `SOURCE` comment with a citation | Invents the source the comment asked for | Write a register row stating what to verify |
| Replacing a paragraph to fix one clause | Discards approved prose; diff is unreadable | `REWORD` the sentence |
| Quoting only the anchor sentence | Mid-paragraph anchors are ambiguous | Quote the neighbouring sentences too |
| Reading comments section by section | Cannot see that 8 threads are 1 fact | Inventory the whole chapter first (Phase 2B) |

---

## Definition of done

- [ ] Snapshot decision made **by the user**, and the snapshot named in frontmatter
- [ ] Every block has a verbatim anchor + an explicit action
- [ ] Every number traced to a result file, and verified programmatically where possible
- [ ] Every asset marked in-text or appendix
- [ ] Every unverified citation marked inline **and** filed under `04-Claims_Verification/`
- [ ] Every `SOURCE` comment has a register row saying what to verify
- [ ] Every comment in scope has a verdict — none silently skipped
- [ ] Every insertion quotes its neighbouring sentences, not just the anchor
- [ ] Word comment threads this closes are named
- [ ] Blocked blocks stated as blocked, with the dependency

---

## Where everything lives

| What | Path |
|---|---|
| **Authoritative prose** | the OneDrive `.docx` — never edited by this skill |
| Snapshots | `06_thesis_writing/docx-exported-snapshots/YYYY-MM-DD_HH-mm_<slug>/` |
| ↳ manifest (capture time, source mtime, comment count) | `<snapshot>/MANIFEST.md` |
| ↳ prose, per chapter | `<snapshot>/chapters/<chN>.md` |
| ↳ prose, per section | `<snapshot>/chapters/sections/<NN-chapter>/<section>/<leaf>.md` |
| ↳ **comments, per chapter** (tagged index) | `<snapshot>/comments/<chN>.md` |
| ↳ **comments, per section** (mirrors prose paths) | `<snapshot>/comments/sections/<NN-chapter>/…` |
| Snapshot generator | `utility_scripts/scripts/thesis_snapshot.py --label "<slug>"` |
| Staged prose + placement contracts | `06_thesis_writing/writing-notes/<slug>.md` |
| Planning bullets (**never prose**) | `06_thesis_writing/sections-drafts/*.md` |
| **Claims register** (the verification queue) | `06_thesis_writing/writing-notes/unverified-claims-to-check.md` |
| Verification packs, per chapter | `06_thesis_writing/notebookLM/04-Claims_Verification/Chapter <N> - <Name>/` |
| ↳ how to run a verification | `…/Claims_Verification-01-HOW-TO-RUN.md` |
| The Zotero library — the only citable source | `06_thesis_writing/citations/citations.json` |
| Figures, diagrams, appendix tables | owned by **P0050**; check before citing |

`comments/` mirrors `chapters/` file for file, so the objections on a section are always
at the same path under a different root.

---

## Related

- `.claude/rules/prose-insertion-discipline.md` — the rule this skill implements
- `.claude/rules/writing-surface-authority.md` — why the `.docx` is authoritative
- `utility_scripts/scripts/thesis_snapshot.py` — snapshot generator (`--label`)
- `06_thesis_writing/notebookLM/04-Claims_Verification/` — unverified-citation destination

## Note layout

Writing notes use a fixed heading structure so every note in the project reads
the same way: `#` for the title and top-level groupings, `##` for one fix, `###`
for a sub-fix, `####` for **Anchor** / **Action** / **Replace with**, and
`### Note - ...` for anything that is not itself an edit. Every fix is separated
from the next by a horizontal rule.

See `.claude/rules/prose-insertion-discipline.md` -> **Note layout** for the
full pattern and the reasoning behind each level.

## The note folder

A chapter pass **starts** by listing `writing-notes/<chapter>/`, before opening
the snapshot. Other sessions write notes there, and a note nobody reads means the
same work gets done twice, differently.

For each live note, measure its anchors against the current snapshot to decide
whether it is applied, partly applied, or untouched — the note's own `status:`
field records intent, not what reached the `.docx`.

Applied notes move to `writing-notes/<chapter>/.archive/<YYYY-MM-DD>_<name>-applied.md`.
Not deleted (the reasoning behind a shipped edit is worth keeping) and not left in
place (two notes with contradicting anchors, neither marked stale). Unapplied blocks
from a partly-applied note are carried forward into the new note.

State what was swept at the top of the new note, so the author can see another
session's work was not dropped.

See `.claude/rules/prose-insertion-discipline.md` -> **The note folder**.

## Prose is submission-ready, never a diff

Every `Replace with` block goes to an examiner, so it must not refer to the
document's own editing history. "Two clarifications resolve an ambiguity carried
by earlier drafts", "Figures verified (resolved)", "Renamed from HOLIDAY_MONTHS
(2026-08-18)", "closing the gap flagged in §4.6" — each tells a reader there
were earlier versions, which is not information the thesis owes them.

The test: would this sentence make sense to someone who has never seen a
previous draft? If it only reads as a diff, it belongs in a `### Note` under the
fix. Keep the *conclusion* in the prose and the *history* in the note.

## When a rerun is in flight, relabel rather than delete

A pass documents the repository as it stands. If training or regeneration is
already running and will change what stands, do not delete the row that is about
to become wrong, and do not write the future state as though it were true.

Relabel it, and state in a note the single edit that lands when the run does.
Write the prose so the invariant carries the paragraph — provenance,
construction and arithmetic survive a rerun; which model consumes a column does
not.

## Structural items go to the cumulative deferred list

Table placement, appendix siting, cross-references and chapter ordering are not
sentence-level fixes. They go to
`06_thesis_writing/writing-notes/deferred-structural-decisions.md`, which is one
file appended to by every chapter pass — so the appendix question is answered
once with the whole document visible.

Give each item an ID, a status, and **a recommendation rather than a question**.
And trace a stale cross-reference before reporting it: "§4.6 does not exist" is a
finding, "it pointed at the risks section, now §4.5, so delete the clause rather
than repoint it" is a decision.

See `.claude/rules/prose-insertion-discipline.md` -> **No metacomment in the
prose itself**, **Prose against a moving codebase**, **The deferred structural
list**.

## A note the author has read is frozen

Their workflow is: read the note top to bottom, apply what looks right, send
back comments in one batch. Editing that file in place makes your changes
invisible and scattered, with nothing to compare against.

Answer review comments in a **new file beside it** —
`ch4-prose-pass-followup-01.md` next to `ch4-prose-pass.md`. Open with a table
of exactly what it supersedes, so the author knows which parts of the original
are dead without re-reading it. Use your own numbering (`F1`, `F2`) rather than
reusing the pass's `Fix N`. Quote the author's comment, then answer it, then
give the paste-ready block.

Both files archive together when the chapter is marked complete. Offer to
regenerate one clean file instead, but default to the follow-up — it preserves
what they already reviewed.

When a review comment reveals that you were wrong, **say so plainly and name the
evidence**. The author may already have pasted the wrong version.

See `.claude/rules/prose-insertion-discipline.md` -> **Follow-up notes**.

## Fetch before you verify

The snapshot check covers the `.docx`. The repository moves too, from three
machines, so start every pass with:

```bash
git fetch origin && git rev-list --left-right --count origin/main...HEAD
git log origin/main --oneline -10
```

Read the messages of anything new before writing. A pass once verified the
feature set as 13 columns correctly in the morning; a commit that afternoon made
it 18, and the note would have restated 13 with full confidence. Name the commit
you verified against, and treat a results-affecting commit as a finding for the
pass, not background noise.

## Anchors are searched in Word, not in the snapshot

Pipe syntax, heading hashes and escape characters exist only in the markdown
mirror. The author is looking at a rendered document and cannot search for any
of them.

Every anchor carries the **section number and title**, a **rendered landmark**
they can see (a caption, heading or bolded lead-in), and **first and last five
words** of running prose. For a table, name its caption and a distinctive cell
value — never the header row's pipes.

See `.claude/rules/prose-insertion-discipline.md` -> **Remote currency** and
**An anchor must be findable in Word**.

## Regenerate the snapshot before every follow-up

Not only before the first pass. By the time a follow-up is needed the author has
applied some fixes, skipped others, and usually added comments while reading —
so anchors written against the old snapshot may quote text that no longer
exists, and the pass would miss the newest comments entirely.

```bash
python utility_scripts/scripts/thesis_snapshot.py --label "<slug>-followup"
```

Then diff the chapter against the previous snapshot to see which fixes landed,
which were skipped, and which were applied differently from how they were
proposed. **Do not re-propose a block whose anchor is already gone** — say it
landed and move on.

Pair it with `git fetch`: snapshot for the prose, fetch for the code. Both
answer "is what I am about to verify against still what exists?"

## Re-pull Zotero before checking any citation

`citations.json` is an export, as old as the last sync. Measured once at two
weeks stale.

```bash
python utility_scripts/scripts/zotero_client.py
```

State the pull time and item count in the note, the way a snapshot is named in
frontmatter. Check metadata too, not only existence — a missing year, a book
stored under a section title, or a tracking parameter in a URL all reach the
bibliography unchanged.

## Two registers, both cumulative, both at the writing-notes root

**`citations-added-register.md`** — every citation a pass adds, with its Zotero
key and the thesis sentence it supports, quoted verbatim. Existence in the
library and support for the claim are separate checks. Request NotebookLM output
in the fixed block format the register defines: verdict, claim verbatim, direct
supporting quotation, location, assessment. The quotation is what makes the
verdict checkable later. Never upload thesis chapters to NotebookLM.

**`post-hpc-validation.md`** — claims written against code that is mid-rerun.
Record the row when writing the claim, not afterwards. Name the artefact that
answers it (a banner line, a results file, a config value), what the chapter
reverts to if it fails, and which rows are gates that invalidate everything below
them.

See `.claude/rules/prose-insertion-discipline.md` -> **Library currency**,
**Pending measurements**, **Register every citation you add**.

## Date a results file before citing it

A results table can be regenerated in part. Table 98 refreshed its structure
columns against the new feature set while still printing a WMAPE pair that was
hardcoded in the generator four days earlier — fresh structure, stale outcome,
and more convincing than either half alone.

Before quoting a number from a results file: check the file's date against the
commit that last changed the code path, `grep` the figure in the generator to see
whether it is computed or a literal, and check whether the upstream `.csv` it
reads predates it.

Read the `INTERNAL REVIEW` note if the table has one. One said *"do NOT quote the
mean of this column"* — and the mean was the easiest number to reach for.

Where two artefacts answer the same question differently (an untuned and a tuned
ablation, say), **name which one the prose rests on**. Both may be correct
experiments answering different questions.

See `.claude/rules/prose-insertion-discipline.md` -> **Results currency**.
