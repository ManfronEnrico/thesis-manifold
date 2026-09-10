---
name: prose-insertion-discipline
description: RULE - Thesis prose is never delivered as loose paragraphs. Every block carries a verbatim anchor from a named snapshot, an explicit action, and an in-text/appendix decision for every asset.
category: workflow
applies-to: [thesis prose, writing-notes, docx insertion, appendix references]
triggers: [writing prose, converting bullets to prose, preparing paragraphs for Word, citing a table or figure in prose]
created: 2026_09_07-15_00
updated: 2026_09_10-16_50
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
| `git fetch` before verifying any claim | A number verified against a commit that moved hours ago | [Remote currency](#remote-currency) |
| A results file is dated, not just read | A regenerated table pairing fresh structure with a stale number | [Results currency](#results-currency) |
| New snapshot before EVERY follow-up | Anchors quoting text the author already replaced | [Snapshot currency](#snapshot-currency) |
| Zotero re-pulled before checking a citation | A source "verified" against a two-week-old export | [Library currency](#library-currency) |
| Every added citation registered with its claim | A real source cited for something it does not say | [Citations](#citations) |
| Claims awaiting a run recorded when written | A pending number nobody goes back to check | [Pending measurements](#pending-measurements) |
| Anchor names its section and a rendered landmark | An anchor the author cannot search for in Word | [Anchor context](#anchor-context) |
| Comments are read before writing | Rewriting text the author already objected to | [Comment-driven passes](#comment-driven-passes) |
| Chapter's note folder swept before writing | Another session's note silently ignored | [The note folder](#the-note-folder) |
| Applied notes archived, not left in place | Two notes disagreeing, neither marked stale | [The note folder](#the-note-folder) |
| A reviewed note is never edited in place | Silent changes inside a file the author already read | [Follow-up notes](#follow-up-notes-never-edit-a-reviewed-note) |
| No metacomment in pasted prose | "Two clarifications resolve an ambiguity" reaching an examiner | [No metacomment](#no-metacomment-in-the-prose-itself) |
| Relabel, don't delete, when a rerun is in flight | A row deleted today that must be rebuilt tomorrow | [Pending reruns](#prose-against-a-moving-codebase) |
| Structural items go to the deferred list | The same appendix question re-derived every pass | [Deferred decisions](#the-deferred-structural-list) |
| One fix per heading block, ruled off | A wall of prose the author cannot navigate | [Note layout](#note-layout) |
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

### An anchor must be findable in Word, not in the snapshot

The snapshot is markdown; the author is looking at a rendered `.docx`. Anything
that exists only in the markdown — pipe syntax, heading hashes, escape
characters — **cannot be searched for** and is not an anchor.

The failure case, measured: an anchor given as `| Feature | Description |
Models |` for a table header. In Word that row renders as three cells in a
bordered table with no pipes anywhere, so there is nothing to paste into the
find box.

**Every anchor carries three things:**

1. **the section**, by number and title — "Section 4.3 Feature Engineering"
2. **a rendered landmark** the author can see — a table caption, a heading, a
   bolded lead-in line
3. **first and last five words** of running prose, verbatim and searchable

For a table, name the caption above or below it plus a distinctive cell value:

```markdown
### Anchor

**Section 4.3 Feature Engineering.** The table below the bolded line
**"Exogenous Variable Enrichment"**, captioned **"Table 4 - Feature Engineering
Overview"**. Its last row begins *"weighted_distribution"*.
```

The section number matters even when the quoted words are unique, because it
tells the author where to scroll before searching — and it survives the case
where Word finds the same phrase in three chapters.

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

## Remote currency

The snapshot rule covers the `.docx`. **The repository moves too**, and on this
project it moves from three machines — the laptop, the VPS and the HPC — so
"the repository" is not a fixed thing to verify against.

**A pass begins with a fetch**, before any claim is checked:

```bash
git fetch origin && git rev-list --left-right --count origin/main...HEAD
git log origin/main --oneline -10
```

Measured 2026-09-09: a pass verified the model feature set as 13 columns in the
morning, correctly. A commit that afternoon added the holiday and intermittency
groups, making it 18. The follow-up note would have restated 13 with full
confidence, and the chapter would have gone to an examiner wrong — with the
wrongness introduced *by the verification pass itself*, which is the worst kind.

**Name the commit when something landed.** "Verified against the repository" is
not a claim that survives; "verified at `3f8b0a9`" is. When a fetch shows new
commits, read their messages before writing — a commit titled *"holiday +
intermittency columns now reach the model"* is telling you which chapter it
invalidates.

Scan for results-affecting commits too, not only code-shape ones. A commit
fixing category-name casing that "silently dropped two of four categories on
Linux" means every HPC result predating it may cover half the panel. That is a
finding for the pass, not background noise.

### A follow-up needs its own snapshot

**Regenerate before writing a follow-up note, always.** By definition the author
has been working in the document since the pass was written: they have applied
some fixes, skipped others, and usually added comments while reading. All three
change what an anchor must quote.

The failure is silent and specific. A follow-up written against the old snapshot
quotes *"The 17 features comprise six lags"* as its anchor, but the author
already replaced that sentence — so the search fails, and the author cannot tell
whether they missed the paste or the note is wrong.

It also loses new comments. Reading a chapter top to bottom is when most review
comments get written, so the snapshot taken *after* a review round carries the
author's freshest thinking. Skipping it means answering the last round's
questions and none of this one's.

```bash
python utility_scripts/scripts/thesis_snapshot.py --label "<slug>-followup"
```

Then **diff the chapter against the previous snapshot** before writing. What
changed tells you which fixes landed, which were skipped, and — if a fix was
applied differently from how it was proposed — that the author made a decision
worth respecting rather than re-proposing:

```bash
diff <old-snapshot>/chapters/ch4-data-assessment.md \
     <new-snapshot>/chapters/ch4-data-assessment.md
```

A block whose anchor has already gone is **not** re-proposed. Say it landed, and
move on.

**The two currency checks are one habit.** `git fetch` for the code, a new
snapshot for the prose. Both answer the same question — *is what I am about to
verify against still what exists?* — and a pass that skips either produces
confident, checkable, wrong output.

## Results currency

A results table is an artefact with a **date**, and on this project the code that
writes it and the numbers inside it can be regenerated independently. Reading one
is not enough; check when it was written and against what.

**The failure has a shape, and it is not the obvious one.** Table 98 was
regenerated on 2026-09-10 against the current 18-feature set. Its structure
columns updated correctly — feature counts, cluster counts, reduced-set sizes.
Its headline WMAPE pair did not, because those two numbers were never computed
by the generator: they came from a manual validation run four days earlier and
were written into the source as string literals, in three places.

So the table now pairs a **fresh structure with a stale outcome**, which is worse
than either half alone: a table that has visibly been regenerated invites more
trust than one that has not.

**As of 2026-09-10 the generators are governed by a Correctness-tier rule** —
`.claude/rules/generated-artefact-provenance.md` requires every number in a
generated artefact to be computed from an input consumed that run. That closes
the failure at source. This section stays because a prose pass reads artefacts
it did not generate, some written before the rule and some carrying documented
carve-outs, so the reader still checks.

**What to check before citing a results number:**

| Check | How |
|---|---|
| When was the file written | `ls -la`, and compare against the commit that last changed the code path |
| Was the number *computed* or *transcribed* | `grep` the figure in the generator — a literal in the source is a transcription |
| Do its inputs predate it | the upstream `.csv` a table reads from carries its own date |

A generator's own header claiming every value is "computed at run time, not
transcribed" is a claim to verify, not to accept — that exact sentence sat above
a table with hardcoded figures.

**Prefer the count to the mean.** Where a results table carries an internal
review note, read it: one warned *"do NOT quote the mean of this column, it
averages over model families that respond differently, and that difference is
itself the finding."* Aggregates across heterogeneous cells are the easiest
number to quote and the easiest to be wrong about.

**Where two artefacts answer the same question differently, name which one the
prose rests on.** A holiday-feature ablation existed twice — untuned (worse in 8
of 12) and independently tuned (better in 6 of 9). Both are correct experiments;
they answer different questions. Prose saying "an ablation measured this" without
saying which invites a reader to find the other one.

## Library currency

`citations.json` and `bibtex.bib` are **exports**, not the library. They are as
old as the last time someone ran the sync, and a citation checked against a stale
export is not checked.

**Re-pull before any pass that touches citations:**

```bash
python utility_scripts/scripts/zotero_client.py
```

It makes a live call to the group library, writes `bibtex.bib` as the source of
truth and derives `citations.json` from it. Seconds to run.

Measured 2026-09-09: the exports on disk were dated 25 August. Two weeks of
additions by either author would have been invisible, and the failure is
one-directional and silent — a source added to Zotero last week reads as
NOT-IN-ZOTERO, so a pass either omits a citation that exists or, worse, records a
"missing source" task that is already done.

**State the pull time in the note**, the same way a snapshot is named in
frontmatter. "Verified against the library" is not a claim that survives;
"verified against the 2026-09-09 21:00 pull, 86 items" is.

**Check metadata, not only existence.** An item can be present and unusable: a
book entry stored under a single section title, a missing year that renders as
"n.d.", a URL carrying a `utm_source=chatgpt.com` parameter. Record those as
defects to fix in Zotero rather than working around them in prose, because the
bibliography is generated from the library and will carry whatever is there.

## Pending measurements

A claim written against code that is mid-rerun is **provisional**, and the
moment to record that is when the claim is written — not afterwards, when
whoever reads the chapter has no way to know which sentences were provisional.

They go to `06_thesis_writing/writing-notes/post-hpc-validation.md`, cumulative
across chapters, one row per claim:

| Field | Content |
|---|---|
| the claim | quoted as the thesis states it |
| what answers it | the specific artefact — a banner line, a results file, a config value |
| if wrong | what the chapter reverts to |

**Name the artefact, not the activity.** "Check after the run" is not actionable;
"the run prints `[features] n/18 resolved` at start-up, and that line is the
claim" is.

**Mark the gates.** Some items invalidate everything below them — a run that
covered two categories instead of four, or one that did not pin thread count,
makes every downstream number unusable. Say which rows are gates so the list is
worked in the right order.

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

## Note layout

A writing note is read with a Word document open and a finger on the scroll bar.
Its job is to be **navigable**, not merely complete: the author must be able to
find one fix, apply it, and find the next without re-reading what they have
already done.

The heading levels are fixed, so every note in the project looks the same:

| Level | Carries |
|---|---|
| `#` | the note title, and the top-level groupings (`# The fixes`, `# Claims register`, `# Decisions`) |
| `##` | one fix, named by what it repairs — `## Fix 4 - Thread 154, the imputation claim is not implemented` |
| `###` | a sub-fix where one fix has several parts — `### 4a - Replace the stale count paragraph` |
| `####` | the mechanical fields, in this order: **Anchor**, **Action**, **Replace with** |
| `###` | `### Note - <what it is>`, for anything that is not itself an edit |

**Every fix is separated from the next by a horizontal rule (`---`).** Without
it the fixes run together and the author loses their place mid-chapter.

```markdown
## Fix 3 - Thread 186, referring to repository files

### Anchor

Starts: *"They are recorded per category and per horizon in..."*

### Action

REWORD.

#### Replace with

> "The resolved boundaries are written to disk alongside each feature matrix..."

### Note - the general rule

A filename with a wildcard in it is a note to a developer, not a sentence in a
thesis.

---
```

**Why the `### Note` level exists.** Evidence, warnings and recommendations are
not edits, and mixing them into the paste-ready text is how an author pastes a
caveat into their thesis. Keeping them at their own level after the `Replace
with` block means the top of every fix is always something to copy.

**A fix headline names the problem, not the location.** `## Fix 4 - Section 4.3`
tells the author nothing they cannot see; `## Fix 4 - Section 4.3 now
contradicts itself` tells them why they are about to spend five minutes.

**Answer questions above the fixes, not inside them.** A question the author
asked in their last message gets its own `##` block before `# The fixes`, so the
answer is not buried in a block they may skip.

## The note folder

Writing notes live in a per-chapter folder with an archive beside it:

```
06_thesis_writing/writing-notes/
  ch4_data_assessment/
    ch4-verification-pass.md          <- live: not yet applied
    ch4-feature-eligibility.md
    .archive/
      2026-09-08_ch4-comment-pass-applied.md
```

**Anything left in the chapter folder is a claim that it still needs applying.**
That is the whole contract, and both halves of it are load-bearing.

### Sweep the folder before writing

A chapter pass **begins** by listing the chapter's note folder — not by opening
the snapshot. Other sessions write notes into these folders, and a note nobody
reads is worse than no note: it represents work already done that is about to be
done again, differently.

For each live note found, establish which of three states it is in:

| State | How to tell | What to do |
|---|---|---|
| **Applied** | its `Find` strings are gone from the snapshot and the replacements are present | archive it (below) |
| **Partly applied** | some blocks landed, others did not | archive it, and carry the unapplied blocks forward into the new note |
| **Not applied** | anchors still match the snapshot verbatim | leave it, and do not duplicate its blocks |

Check this by **measuring against the snapshot**, never by assuming. A note's own
`status:` frontmatter says what its author intended, not what reached the `.docx`.

### Archive on the way in, not on the way out

When a note has been applied, move it — do not delete it, and do not leave it:

```
writing-notes/<chapter>/.archive/<YYYY-MM-DD>_<original-name>-applied.md
```

Deleting loses the reasoning behind an edit that is now in the thesis with no
record of why. Leaving it in place is worse: the folder then holds two notes
whose anchors contradict each other, and nothing marks which one is stale. The
next session — or the next person — cannot tell them apart.

The date prefix is the date it was **archived**, so the folder reads
chronologically.

### Say what was swept

The new note states what it found, so the author can see that another session's
work was not lost:

```markdown
**Notes swept:** `ch4-comment-pass.md` (applied, archived),
`ch4-feature-eligibility.md` (not applied — its two blocks are carried into
Fix 6 below).
```

## Follow-up notes: never edit a reviewed note

Once the author has read a note, **that file is frozen**. Their workflow is to
read it top to bottom, apply what looks right, and send back comments in one
batch. A note edited in place breaks that in the worst way: the changes are
invisible, scattered, and have nothing to compare against. The author is left
hunting a file they have already read for edits they cannot see.

**Answer review comments in a new file beside it:**

```
writing-notes/<chapter>/
  ch4-prose-pass.md               <- frozen the moment it is read
  ch4-prose-pass-followup-01.md   <- answers the review comments
```

The follow-up opens with **exactly what it supersedes**, so the author knows
which parts of the original are now dead without re-reading it:

```markdown
| In the main pass | Status |
|---|---|
| Fix 3, Anchor - part B | one sentence replaced (F1 below) |
| Fix 4, entire fix | replaced (F2 below) - **do not delete the table rows** |

Everything else in the main pass stands: Fixes 1, 2, 5, 6, 7, 8, 9.
```

It uses **its own numbering** (`F1`, `F2`) rather than reusing the pass's `Fix N`,
so a reference is never ambiguous about which file it lives in. And it is read
top to bottom on its own — quote the author's comment, then answer it, then give
the paste-ready block. It is a note in its own right, not a diff.

**Both files archive together** when the chapter is marked complete, since the
follow-up only makes sense beside what it amends.

**Offer to regenerate, do not assume.** Some authors would rather have one clean
file than a pass plus three follow-ups. Say the offer explicitly and let them
choose; the default is the follow-up, because it is the one that preserves what
they have already reviewed.

### When the author's correction changes your reasoning, say so

A follow-up that quietly writes the corrected version has thrown away the most
useful thing in it. If a review comment revealed a wrong claim, state the
correction plainly, name the evidence, and keep it visible:

```markdown
⚠ Fix 4 said the linear dependence "rules out admitting all three to a linear
model". That is too strong, and your own code is the counterexample:
`srq1_ridge_cv.py:166` fits all three and drops none.
```

The author needs this because they may have already pasted the wrong version.

## No metacomment in the prose itself

Every `Replace with` block is submission-ready text. It is going into a thesis
an examiner reads, not into a note the author reads.

That rules out a whole class of sentence which feels natural to write and is
invisible until someone looks for it — prose that refers to **the document's own
editing history**:

| Never write | Because it tells the examiner |
|---|---|
| "Two clarifications resolve an ambiguity carried by earlier drafts" | there were earlier drafts, and they were ambiguous |
| "Figures verified (resolved)" | this is a task tracker |
| "These figures supersede the all-markets values" | an internal correction happened |
| "Renamed from HOLIDAY_MONTHS (2026-08-18)" | a variable used to be called something |
| "closing the gap previously flagged in §4.6" | the chapter is auditing itself |

The test: **would this sentence make sense to a reader who has never seen a
previous version?** If it only makes sense as a diff, it is a note, not prose.

The same content is usually worth keeping — as a `### Note` under the fix, where
the author reads it and the examiner does not. A renaming that corrected a false
implication is a real methodological point; it just belongs in the note, and the
*conclusion* belongs in the prose:

> **prose:** "The measure is deliberately named for what it detects."
> **note:** "Renamed from HOLIDAY_MONTHS on 2026-08-18 because…"

## Prose against a moving codebase

A pass documents the repository **as it stands**, and sometimes a rerun is
already in flight that will change what stands. The instinct is to delete the
soon-to-be-wrong row and write the future state. Both halves of that are wrong.

**Relabel rather than delete.** A row that is wrong about *how* something is used
survives the rerun with a one-word edit. A deleted row has to be reconstructed
from scratch, by someone who no longer remembers what it said.

**Say what the rerun changes.** The note names the single edit that lands when
the run does, so the author can apply it in seconds:

```markdown
### Note - what the retraining will and will not change

If the holiday columns are promoted, **one word changes**: the `Used by` cell
becomes the model list. The rest of the paragraph holds either way, because the
provenance and the linear dependence are properties of the columns, not of the
experiment.
```

Write the prose so the invariant part carries the paragraph. Provenance,
construction and arithmetic relationships survive a retraining; which model
consumes a column does not.

## The deferred structural list

Table placement, appendix siting, cross-references and chapter ordering are
**not sentence-level fixes**, and a chapter pass must not silently drop them or
re-derive them next time.

They go to `06_thesis_writing/writing-notes/deferred-structural-decisions.md`,
which is **cumulative across chapters** — one file, appended to by every pass,
so the appendix question is answered once with the whole document visible rather
than four times with a quarter of it.

Each item gets an ID (`S1`, `S2`, …), a status (`open` / `recommended` /
`blocked` / `done`) and, wherever possible, **a recommendation rather than a
question**. "Table 2 or appendix?" is work handed back; "delete Table 2, because
an appendix copy would preserve its two superseded figures" is work done.

**Trace a stale cross-reference before reporting it.** `§4.6` does not exist is a
finding; *it pointed at the risks section, which is §4.5 today, and repointing it
would leave two sections citing each other about project history, so delete the
clause* is a decision. The tracing is usually two greps.

Keep `done` rows, with what was decided. The reasoning behind a settled
structural choice is what stops it being reopened.

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

### Register every citation you add, with its claim

A reference that exists is not a reference that says what you need it to say.
Both checks are required and they are independent:

| Check | Answers | Recorded as |
|---|---|---|
| Is it in the library? | can the bibliography resolve it | `IN-ZOTERO` |
| Does it support the claim? | is the citation honest | `NLM-CONFIRMED` |

Every citation a pass adds goes to
`06_thesis_writing/writing-notes/citations-added-register.md` with its Zotero
key, the section it lands in, and **the thesis sentence it is being used to
support, quoted verbatim**. The sentence is the thing being verified; a
paraphrase of a claim can be true when the claim is false.

**Request NotebookLM output in the fixed block format** the register defines —
verdict, claim verbatim, a direct supporting quotation, location, assessment, and
a narrowed rewording only when the verdict is PARTIAL. The quotation is the field
that makes a verdict checkable later; without it the register holds assertions,
which is what it exists to prevent.

`NOT-ADDRESSED` is a distinct verdict from `REFUTED`. A source silent on a claim
is not evidence against it, but cannot be cited for it either.

**Never upload thesis chapters to NotebookLM.** It returns our own wording as a
source, which reads as independent confirmation and is not.

This register and the `CV-NN` claim packs under
`notebookLM/04-Claims_Verification/Chapter <N> - <Name>/<Topic>/claims.md` run in
opposite directions: this one starts from a source and asks whether it supports
the claim; those start from a claim and ask whether a source exists. A pass
usually feeds both, and the packs have their own conventions — read
`Claims_Verification-00-MASTER-verification-brief.md` before adding to them.

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
