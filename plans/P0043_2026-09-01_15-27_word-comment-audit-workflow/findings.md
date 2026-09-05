---
pid: P0043
created: 2026-09-01 15:27:00
updated: 2026-09-05 20:05:00
---

# P0043 — Findings

## F1 — No `.docx` in this repo carries comments (2026-09-01)

All six files in `05_thesis_writing/sections-final/` contain a `word/comments.xml` of
exactly **625 bytes**. Dumped, it is an empty element:

```xml
<?xml version="1.0" encoding="UTF-8"?><w:comments xmlns:w="..." ... />
```

Namespace declarations, no `<w:comment>` children. Byte-identical size across all six
files confirms it is generator boilerplate, not coincidence.

**Also absent:** `word/commentsExtended.xml`, `word/commentsIds.xml`, `word/people.xml`.
Word writes all of these when a human comments and saves. Their absence means these files
have **never been round-tripped through Word** — they are script/pandoc output.

**Implication:** the review copy that actually carries supervisor and Enrico comments lives
outside this repo. Its location is task 1 and gates validation of the whole extractor.

## F2 — The guide's VBA cannot produce two of the most valuable columns (2026-09-01)

Assessed against the Word object model, not tested (no reviewed file available yet):

- `resolved` — stored as `w15:done` in `commentsExtended.xml`. The VBA `Comment.Done`
  property is version-dependent and absent on older documents.
- reply threading — the parent link is `w15:paraIdParent`, also in `commentsExtended.xml`.
  VBA's `Comments` collection presents replies as flat siblings, losing the thread.

Both parts are in the OOXML package and trivially readable by any zip+XML reader. This is
the decisive argument for the Python engine.

## F3 — Page number is genuinely unavailable from OOXML (2026-09-01)

Not a limitation of the approach — pagination is computed by Word's layout engine at render
time and is not persisted in the file. Any tool that reports a page number must ask Word.

Mitigation adopted: `heading_path` + `paragraph_index` as the primary locator. Arguably
better for this use case, since a page number goes stale the moment anyone edits earlier
text, whereas a heading path does not. The VBA fallback exists for when a page number is
specifically wanted.

## F4 — Environment (2026-09-01)

- Interpreter: `Z:\_dev-ssd\thesis-manifold\.venv\Scripts\python.exe`
- `pandas 3.0.1` present
- `python-docx`, `openpyxl`, `lxml` — **all absent**, `ModuleNotFoundError` on each
- `requirements.txt` mentions none of them

Note: `python-docx` does **not** expose comments in its public API. It will be used only
for convenience access to the package; comment parsing goes through `lxml` against the raw
XML parts. Do not plan around a `python-docx` comments API — there isn't one.

---

## F5 — A working stdlib-only extractor exists; no dependency is required for bands 1–2 (2026-09-01, from the P0042 session)

Task 2 proposes installing `python-docx`, `openpyxl` and `lxml`. **`python-docx` and
`lxml` are not needed for the extraction half** — a working prototype is committed
alongside this plan as `prototype_docx_comments.py`, using only `zipfile` and
`xml.etree.ElementTree` from the standard library.

It already produces, verified against all 8 repo `.docx` files:

- `comment_id`, `author`, `initials`, `date` — from `word/comments.xml`
- `comment_text` — concatenated `w:t`, with `w:tab`/`w:br` rendered as whitespace
- **`anchored_text`** — runs between `commentRangeStart`/`commentRangeEnd` matched by id,
  tracked through a document-order walk with an open-range set. This is the column F2
  correctly identifies as the most valuable and the one the guide's VBA omits.
- `paragraph_index` — ordinal of the anchored paragraph
- full body text as a paragraph list, which the drift check below needs

**Why this matters for task 2:** `python-docx` in particular is a poor fit here. It has
no API for comments at all (they are unsupported upstream), so the extractor would end
up reading the XML directly regardless — through a heavier dependency. `openpyxl` *is*
genuinely needed, for the xlsx writer in task 4.

**Recommendation:** narrow task 2 to `openpyxl` only. Keep extraction stdlib-only. Fewer
moving parts on a Windows/OneDrive setup where dependency installs have caused problems
before.

**What the prototype does NOT yet do**, and which this plan's schema correctly requires:
`heading_path` (needs a `w:pStyle` Heading scan), `commentsExtended.xml` parsing for
`w15:done` and `w15:paraIdParent`, `anchor_context`, and the band-3 merge. Those are the
real work of tasks 3–5; the prototype is a starting point, not a replacement.

## F6 — Answering open question 2: per-chapter vs. one document (2026-09-01)

Evidence for the "one merged document" case. Brian is reviewing a **114-page stitched
`.docx`** assembled by Enrico from the section drafts and finals, held in OneDrive,
outside this repo. The per-chapter `.docx` files in `05_thesis_writing/sections-final/`
are **generator output** (F1: empty 625-byte comment stubs, no `commentsExtended.xml`) —
they are not the review surface and never were.

**So `chapter` must be derived from `heading_path`, not from a filename.** The schema's
`heading_path` column is doing double duty as both locator and chapter attribution, which
makes the Heading-scan in task 3 load-bearing rather than nice-to-have.

## F7 — Measured draft-vs-final drift: the audit has a second job (2026-09-01)

Word counts, `sections-drafts/*.md` against `sections-final/*.docx`, measured with the
prototype:

| Chapter | .md draft | .docx final | delta |
|---|---:|---:|---:|
| ch1-introduction | 3,615 | 3,010 | **−605** |
| ch2-literature-review | 7,603 | 6,287 | **−1,316** |
| ch3-methodology | 3,504 | 3,476 | −28 |
| ch4-data-assessment | 4,168 | 3,736 | −432 |
| ch5-framework-design | 2,461 | 2,367 | −94 |
| ch10-conclusion | 946 | 704 | −242 |

Some delta is expected — markdown syntax, bullet scaffolding and code fences do not
survive conversion. But **Ch2 at −1,316 words and Ch1 at −605 are beyond formatting**,
and Ch3's −28 shows what a genuinely-in-sync pair looks like by comparison.

**There are therefore three versions of the thesis in play**: the `.md` drafts (this
repo), the per-chapter `.docx` finals (this repo), and Enrico's 114-page stitched
document (OneDrive). Nothing currently reconciles them.

**Consequence for this plan:** the extractor's paragraph-list output makes a
paragraph-level drift report nearly free once the comment work is done — same parse, same
walk. Worth adding as a task, because a comment triaged against a paragraph that no longer
exists in the authoritative document is wasted effort. Suggested as task 9 rather than
folded into task 3, so it cannot delay the comment workflow.

## F8 — Citation field codes: a detectable, deferrable risk (2026-09-01)

If the stitched document was assembled by copy-paste, Zotero field codes may not have
survived; a pasted citation renders identically to a live one but is inert text the Word
plugin cannot see, so it never reaches the bibliography.

**This is detectable from the same OOXML parse** — live Zotero citations appear as
`w:fldChar`/`w:instrText` runs (or content controls carrying `ADDIN ZOTERO_ITEM`),
whereas pasted text is plain runs. Counting `ADDIN ZOTERO_ITEM` occurrences against the
count of visible `(Author, year)` patterns gives a cheap discrepancy check.

**Brian's decision (2026-09-01): defer.** The plan is to finalise the prose, then do one
manual pass replacing static in-text citations with live fields as the final formatting
step. Recorded here so the check is available when that pass happens, and so the risk is
not rediscovered late. **Do not let this block the comment workflow.**

## F9 — Where the authoritative document lives: snapshot, do not host git in OneDrive (2026-09-01)

**The problem.** The shared 114-page `.docx` must sit in OneDrive to stay shared with
Enrico. This repo sits on an external SSD (`Z:`). Brian proposed a second git repo,
hosted *inside* OneDrive, holding the writing artifacts and added to the same VS Code
workspace.

**Recommendation: do not put a git repo inside OneDrive.** Two independent reasons:

1. **This project has already been bitten by OneDrive sync races.** Tooling issue #1 in
   `.claude/logs/tooling-issues.jsonl` — "OneDrive file sync + CRLF line ending handling
   creates race conditions when writing .py files directly" — is the origin of the
   never-Write-Python-directly rule. A `.git` directory is that same failure mode with
   worse consequences: OneDrive can sync index/object files mid-write, and two machines
   syncing one `.git` produces conflicts git has no way to resolve.
2. **Git cannot diff a `.docx` anyway.** It is a zip of compressed XML; any save rewrites
   the bytes wholesale. Committing it yields `Binary files differ` — version *history*,
   never a readable *diff*. So the second repo would not even buy the thing it was for.

**The alternative — snapshot instead of host:**

| Step | What | Where |
|---|---|---|
| 1 | The live shared `.docx` never moves | OneDrive, unchanged; Enrico's workflow unaffected |
| 2 | A script copies it into this repo on demand, dated | `05_thesis_writing/sections-final/thesis_full_YYYY-MM-DD.docx` |
| 3 | The **same** script extracts text to `.md` beside it | that `.md` is what actually diffs |

Step 3 is the point. The `.docx` gives history; the extracted `.md` gives a readable
line-by-line diff of prose across snapshots. Sharing is untouched, git stays on the SSD,
and checkpoints are one command.

**Open:** the OneDrive path is still needed (P0043 open question 1) — it is the same
blocker as task 1, so one answer unblocks both.

## F10 — Chapter-wise vs. one document: keep BOTH, with one authoritative per purpose (2026-09-01)

Brian raised deleting the per-chapter `.docx` finals once the stitched document is
verified, then questioned whether chapter-level files are better for comparison and
write-up. **Recommendation: keep chapter granularity.** Three reasons, in order of force:

1. **NotebookLM audits are chapter-scoped by design.** A 114-page source buries the
   signal when the question is about one chapter's methodology. The planned verification
   and improvement rounds all operate per chapter.
2. **Drift is only actionable at chapter granularity.** "Ch2 is −1,316 words" (F7) can be
   investigated; "the thesis differs" cannot.
3. **The `.md` ↔ audit comparison is already chapter-scoped** in Brian's own workflow.

**The division of authority that removes the ambiguity:**

| Artifact | Granularity | Authoritative for | Edited by hand? |
|---|---|---|---|
| `sections-drafts/*.md` | chapter | **live working state** — bullets, results, anything re-verifiable in this repo or changed by a re-run | **yes** — this is the working surface |
| stitched `.docx` (OneDrive) | whole thesis | **prose as submitted**, and the comment/review surface | yes, by Brian + Enrico in Word |
| `sections-final/*.docx` | chapter | nothing — **derived artifact** | **no** — regenerate, never hand-edit |
| dated snapshot + extracted `.md` | both (see F11) | the diffable record | no — script output |

**The failure state to avoid is the current one:** three versions, all hand-edited, none
authoritative. The rule above assigns each file exactly one job.

This supersedes the earlier suggestion (P0042 discussion) that the stitched `.docx`
becomes authoritative for a chapter "once stitched in" and the `.md` only for unstitched
chapters. Brian's framing is better and is adopted: **the `.md` stays live for anything
that changes with the pipeline** — EDA, training results, re-runs — because those must
stay verifiable against the repo, and a Word document cannot be.

## F11 — Splitting a snapshot into per-chapter `.md` by heading is feasible (2026-09-01)

Brian asked whether the snapshot script can split the stitched `.docx` on headings into
per-chapter `.md` automatically. **Yes**, and it needs no new dependency — the same
document-order walk the comment extractor already performs (F5).

**Mechanism:** paragraphs carry `w:pStyle` values (`Heading1`, `Heading2`, …). Walking
`document.xml` in order and cutting at each Heading-1 yields chapter boundaries; the
heading text names the file. This is the *same* Heading-scan task 3 needs for
`heading_path`, so the work is shared, not duplicated.

**What it delivers:** a semi-automatic per-chapter snapshot, so the chapter-wise
comparison F10 argues for stays possible even though the authoritative prose lives in one
114-page file. Diff `snapshot/ch3-methodology.md` against
`sections-drafts/ch3-methodology.md` and the drift is localised immediately.

**Caveats to build in, not discover later:**

- **Heading style names vary.** Enrico's document may use custom styles or outline levels
  rather than the built-in `Heading1`. The splitter must report what styles it found and
  fail loudly on zero matches rather than emitting one giant file.
- **Chapter numbering must map to the repo's filenames**, or the diff pairs nothing. Needs
  an explicit mapping (`"3 Methodology" -> ch3-methodology`), not string-similarity guessing.
- **Round-tripping is one-way.** These `.md` are *read-only* snapshots for diffing. Never
  edit them and never convert back — that would create a fourth version and reintroduce
  exactly the ambiguity F10 removes.
- **Word-count deltas are a weak signal on their own** (F7): formatting loss is real. Use
  paragraph-level comparison for anything actionable.

## F12 — Two-author team, no external reviewer: what this changes in the schema (2026-09-01)

Brian confirmed: **only Brian and Enrico work with the comments.** There is no supervisor
or external reviewer in this loop. Comments are the two authors talking to each other in
the shared document, not feedback arriving from outside.

This is a substantive correction to the plan's framing, which was written assuming an
inbound-review model ("supervisor and Enrico comments arrive"). Consequences:

1. **`author` becomes a genuinely high-value column, not a formality.** With two known
   authors it partitions cleanly into "my open items" vs. "Enrico's", which is the primary
   filter a two-person team actually uses. With `owner` in band 3 it supports a simple
   ask/answer protocol: `author` = who raised it, `owner` = who must act.
2. **`resolved` (`w15:done`) is probably weak here — see open question 3.** Two co-authors
   editing the same document tend to *delete* a settled comment rather than resolve it. If
   so, `delta = GONE` is the real signal that something was dealt with, and `triage_status`
   carries the load. Keep the `resolved` column (it is nearly free once
   `commentsExtended.xml` is parsed) but do not design the workflow around it.
3. **The band-3 merge is now the most important feature, not a convenience.** With no
   external reviewer imposing rounds, "rounds" are whatever cadence the two of you snapshot
   at. Triage state that survives re-export is the only thing making that cadence cheap.
4. **`commit_ref` stays valuable and arguably rises.** It is how one author shows the other
   that a comment was actioned, without a meeting.
5. **Do not add reviewer-management fields.** No due dates, no severity assigned by a
   third party, no round-robin. Two people who talk to each other do not need workflow
   ceremony.

The plan's "Why this plan exists" section should be reworded away from "supervisor" —
tracked in progress.md rather than rewritten mid-session.

## F13 — Assessment of the proposed snapshot → split → diff flow (2026-09-01)

Brian proposed: shared `.docx` (114 pages) → snapshot capturing **both comment and prose
state** → split into per-chapter snapshot `.md` → diff/audit/improve against the WIP `.md`
chapter drafts.

**Verdict: sound, and it is the right shape.** It is already what F9 + F10 + F11 describe,
with one genuine addition — that the snapshot captures comments *and* prose **in the same
operation**. That addition is correct and should be adopted explicitly, because:

- Both come from **one parse of one file** (F5's walk already emits comments and the
  paragraph list together). Splitting them into two scripts run at different times would
  let them drift out of step.
- A comment is only interpretable against the prose it was anchored to **at that moment**.
  Snapshotting the comment without its prose state produces exactly the wasted effort F7
  warns about: triaging a comment against a paragraph that has since changed.
- It makes the snapshot a genuine **checkpoint**: one dated, self-consistent record of
  "what the document said and what we said about it".

**Therefore: `snapshot_id` (the dated snapshot the row came from) should be added to band 1**,
and the audit `.xlsx` should be written *into* the snapshot, not into a separate folder
keyed only by date. One snapshot = one folder = docx + whole `.md` + per-chapter `.md` +
comment audit. That is a stronger contract than tasks 10/11 currently state.

**Proposed snapshot layout** (supersedes the looser wording in F9 step 2):

```
05_thesis_writing/snapshots/YYYY-MM-DD_HH-mm/
  thesis_full.docx          <- byte copy of the OneDrive file
  thesis_full.md            <- extracted prose, whole document
  chapters/ch3-methodology.md   <- Heading-1 split, read-only
  comments.xlsx             <- the audit, band 3 merged from the previous snapshot
  comments.csv              <- same rows, plain text, so git diffs the comment stream
  manifest.json             <- source path, mtime, sha256, counts, heading map used
```

**Three risks worth stating before building it:**

1. **The diff is one-way and must stay one-way.** `chapters/*.md` are read-only artifacts.
   The temptation to fix a typo in the snapshot instead of the source is exactly how a
   fourth version appears (F10). Consider writing a `DO-NOT-EDIT` header line into each.
2. **`.md`-vs-`.md` diff will be noisy on first run.** The WIP drafts carry bullets, code
   fences and markdown syntax the Word document never had (F7: Ch2 −1,316 words). Expect the
   first diff to be mostly formatting. Mitigation: normalise both sides before diffing
   (strip markdown syntax, collapse whitespace, one sentence per line) and compare
   *sentences*, not lines. Without that, the first diff is unreadable and the tool gets
   abandoned.
3. **Snapshot size.** The stitched `.docx` is 114 pages; `ch5-framework-design.docx` alone
   is 263 KB in this repo. Committing a full binary copy per snapshot grows the repo
   steadily. Options: keep the `.docx` out of git (gitignore it, keep only `.md` + `.csv` +
   `manifest.json`, with sha256 in the manifest proving which file it came from), or accept
   the growth. **Recommend gitignoring the `.docx`** — the `.md` is the diffable artifact,
   and the manifest hash preserves provenance without the bytes.

**What the flow does not solve, and should not be asked to:** it will not tell you whether
a change was an *improvement*. It localises difference. Judging the difference stays a
human read, and that is the correct division of labour.

---

# HANDOVER — snapshot work moved to this plan (2026-09-01, from the P0042 session)

Everything below was built and run in the P0042 session before ownership of the
snapshot/extraction work moved here. It is committed and working; treat it as a
starting point to refine, not as a design to re-derive.

## F12 — `thesis_snapshot.py` exists, runs, and is committed

`utility_scripts/scripts/thesis_snapshot.py`. Stdlib only (`zipfile` +
`xml.etree`). Run bare — the OneDrive path is the default:

```
.venv/Scripts/python.exe utility_scripts/scripts/thesis_snapshot.py
```

**Source (task 1's blocker — now answered):**

```
C:\Users\brian\OneDrive\Documents\02-Areas\MSc. Data Science\
  2026-03 - CBS Master Thesis\Drafts\
  MSc. Data Science - 175888 and 176171 - Master Thesis.docx
```

**Writes** `05_thesis_writing/snapshots/YYYY-MM-DD/`:

| File | Contents |
|---|---|
| `thesis_full.docx` | verbatim copy — **gitignored**, git cannot diff it |
| `thesis_full.md` | whole-document text |
| `chapters/*.md` | one file per Heading 1, 17 of them |
| `comments.md` | every comment + anchored text + section path + resolved |
| `MANIFEST.md` | capture metadata + the drift table |

## F13 — Copy-then-read is REQUIRED, not a convenience

The first read attempt failed:

```
PermissionError: [Errno 13] Permission denied: '...Master Thesis.docx'
```

**Word holds an exclusive lock on an open document.** `zipfile` cannot open the
original while Brian has it open; `shutil.copy2` succeeds regardless. The script
therefore copies first and parses the copy — which additionally guarantees the
archived `.docx` and the extracted text are the *same bytes*, not two reads of a
file that may have been saved in between.

**Do not "optimise" this into a direct read.** It will work whenever Word is
closed and fail exactly when it is open, which is most of the time.

## F14 — The real document's structure (measured, supersedes assumptions)

| Property | Value |
|---|---|
| Size | 913,764 bytes |
| Words (extracted text) | 31,870 |
| Heading 1 sections | **17** — clean built-in `Heading1`, no custom styles |
| Comments | **14**, all authored by Brian Rohde |
| `word/commentsExtended.xml` | **present**, 3,429 bytes |
| `word/commentsIds.xml`, `commentsExtensible.xml`, `people.xml` | all present |

Style census: `Heading1` 17, `Heading2` 86, `Heading3` 70, `ListParagraph` 321,
`TOC1/2/3` 17/86/70, `AppendixFigure` 2, `ReferenceList` 1, unstyled 1,036.

**This unblocks the plan's central untestable:** F1 said resolved-status parsing
could not be validated because no repo `.docx` had `commentsExtended.xml`. The
real review copy **does**, so `w15:done` and `w15:paraIdParent` are now testable.
Task 7 is no longer gated on finding a file.

The 17 Heading-1 sections are: Table of Contents, Table of Figures, Table of
Tables, Abstract, Chapters 1–10, Reference List, AI Use Declaration, Appendix.

## F15 — Extraction already implemented; what remains for tasks 3–5

Working in `thesis_snapshot.py::read_docx()`:

- `comment_id`, `author`, `date`, `comment_text`
- **`anchored_text`** — document-order walk with an open-range set
- **`heading_path`** — a heading stack (H1–H5), so `chapter` derives from
  content, which F6 established is required for a single merged document
- `resolved` (`w15:done`) and `is_reply` (`w15:paraIdParent`), joined via the
  comment's `w14:paraId`
- per-chapter split on Heading 1, plus the drift table

**Still to build for the Excel workflow:** `para_id` as a first-class column,
`anchor_context` (~200 chars either side), `thread_id`/`parent_comment_id`
resolution to a comment id rather than a paraId, `reply_count`,
`comment_length_chars`, band 3 and the prior-export merge, and the xlsx writer.
`openpyxl` is the only dependency needed (F5).

## F16 — Two bugs found by running it; one is a warning about the other guard

1. **`_slug` mapped "Chapter 10 - Conclusion" to `ch1-introduction`.** Plain
   `startswith` matched because `"chapter 1"` is a prefix of `"chapter 10"`. It
   silently **overwrote ch1's file with ch10's text** and reported a nonsense
   −2,733-word drift. Fixed: longest key first, and reject a match whose
   remainder starts with a digit. **This is exactly the caveat F11 warned about,
   and it still shipped — the lesson is that the heading→filename map needs a
   test, not just care.**
2. **`srq4_experiment.py` key mapping** (unrelated to this plan, recorded for
   completeness): it mapped `thesis_manifold_prompts` while `.env` stores
   `thesis_manifold_openai_prompts`, so `.env` was silently ignored. Both
   spellings now accepted.

## F17 — Measured drift CORRECTS the earlier alarm in F7

F7 compared `sections-drafts/*.md` against the stale per-chapter
`sections-final/*.docx` and reported Ch2 at −1,316. **Against the actual stitched
document, Ch2 is −199.** The repo's per-chapter finals were simply out of date;
they were never the review surface (F6).

| chapter | draft `.md` | stitched snapshot | delta |
|---|---:|---:|---:|
| ch6-model-benchmark | 6,155 | 4,244 | **−1,911** |
| ch4-data-assessment | 4,168 | 3,701 | −467 |
| ch1-introduction | 3,615 | 3,390 | −225 |
| ch2-literature-review | 7,603 | 7,404 | −199 |
| ch5-framework-design | 2,461 | 2,320 | −141 |
| ch9-discussion | 1,274 | 1,173 | −101 |
| ch3-methodology | 3,504 | 3,406 | −98 |
| ch10-conclusion | 946 | 882 | −64 |
| abstract | 438 | 358 | −80 |

**Only Ch6 (−1,911) is worth investigating.** Everything else is within what
markdown-syntax loss explains. Ch7/Ch8 have no draft counterpart to compare.

**Reinforces F10's authority table:** `sections-final/*.docx` are stale derived
artifacts. Nothing should be measured against them, and F7's table should not be
quoted — F17 supersedes it.

## F18 — Page count: 31,870 words is consistent with Brian's 114 pages

The extraction yields ~71 pages at CBS formatting (~450 words/page). Word reports
114. The difference is what extraction deliberately excludes — TOC (913 words of
entries), Table of Figures/Tables, Reference List (1,317), AI Use Declaration
(530), Appendix, plus figures/tables/page breaks that occupy pages but few words.

**Do not treat 31,870 as the thesis's word count against the 120-page target.**
It is body prose only. `user-docs/integrations/thesis-writing-process.md` records
the 120-page position; the open question flagged there — whether "120 pages of
content" counts front/back matter — is what decides which number matters.

## Suggested next steps for this session

1. **Task 7 is unblocked** — validate the extractor against the real 14 comments.
   Expected shape is in `05_thesis_writing/snapshots/2026-09-01/comments.md`.
2. **Add a test for the heading→filename map** (F16). The ch1/ch10 collision
   would have been caught by one assertion.
3. **Decide whether snapshots are committed every run or only at milestones.**
   Currently every run writes a dated folder; nothing prunes them. The `.docx`
   is gitignored, but 20 `.md` files per snapshot accumulate.
4. **Ch6's −1,911** is the one real drift signal. Worth a paragraph-level diff
   (task 9) rather than a word-count guess.

## F14 — Snapshot script shipped and validated against the real document (2026-09-01)

`utility_scripts/scripts/thesis_snapshot.py` exists, runs, and has been executed against
the authoritative OneDrive file. **Task 1 is discharged** — the blocker is gone:

```
C:\Users\brian\OneDrive\Documents\02-Areas\MSc. Data Science
  \2026-03 - CBS Master Thesis\Drafts
  \MSc. Data Science - 175888 and 176171 - Master Thesis.docx
```

Measured on the 2026-09-01 16:24 snapshot: 913,764 bytes, **31,870 words, 17 Heading-1
sections, 14 comments**, and — importantly — **`commentsExtended.xml` is present**, so
`resolved` and reply threading are genuinely readable. F1's concern ("untestable until a
real reviewed file exists") is resolved: the real file carries what the schema needs.

Note the document is **114 pages but only ~31.9k words**, i.e. figure- and table-heavy.

Two implementation details in the script worth preserving, both non-obvious:

1. **Copy first, then parse the copy.** Word holds an exclusive lock on an open document;
   `zipfile` raises `PermissionError` on the original while `shutil.copy2` succeeds. Parsing
   the copy also guarantees the archived `.docx` and the extracted text are the same bytes.
2. **`_slug` matches longest-key-first and rejects a trailing digit.** A plain `startswith`
   maps "Chapter 10 - Conclusion" onto `ch1-introduction` (since "chapter 1" prefixes
   "chapter 10"), silently overwriting ch1 with ch10's text and reporting a nonsense drift.

## F15 — Revised drift numbers supersede F7 (2026-09-01)

F7 measured `sections-drafts/*.md` against the **per-chapter `sections-final/*.docx`** —
which F6 later established were never the review surface. Measured against the
**authoritative stitched document**, the picture changes materially:

| Chapter | F7 (vs. sections-final) | F15 (vs. authoritative) |
|---|---:|---:|
| ch1-introduction | −605 | **−225** |
| ch2-literature-review | **−1,316** | **−199** |
| ch3-methodology | −28 | −98 |
| ch4-data-assessment | −432 | −467 |
| ch5-framework-design | −94 | −141 |
| ch10-conclusion | −242 | −64 |
| ch6-model-benchmark | *(not measured)* | **−1,911** |

**Ch2 was a false alarm** — −1,316 against a stale artifact, −199 against the real
document. **Ch6 is the actual outlier at −1,911** and was invisible before, because no
`ch6` file exists in `sections-final/`. This is a concrete vindication of F10's rule that
`sections-final/*.docx` is authoritative for nothing.

Chapters 7 and 8 have no `sections-drafts/*.md` counterpart at all and so produce no drift
row — worth noting, since absence from the table reads like agreement.

## F16 — Comments as `.md` beats `.xlsx` for this workflow; keep both, but `.md` is primary (2026-09-01)

Brian asked whether the current `.md` comment export is preferable to the planned Excel
route, **given that the stated goal is semi-automatic context for chapter iteration and
NotebookLM audits**. That goal statement settles it, and it reverses the plan's earlier
default.

**Evidence from the real 14 comments** (not a general argument):

- They are **long-form reasoning, not tickets.** Comment [22] runs ~200 words across five
  paragraphs and proposes an experiment-design change. Comment [20] is a technical
  correction about where RAM is actually consumed. These do not fit a spreadsheet cell, and
  Excel's wrap-text renders them unreadable at any column width.
- **All 14 are authored by Brian.** The `author` column — which F12 promoted to a primary
  filter — is currently constant. Sorting and filtering, Excel's main advantage, has
  nothing to act on yet.
- **They are already chapter-grouped and heading-pathed**, which is the grouping that
  matters for both stated purposes.

**Decisive argument: neither stated goal is a spreadsheet use case.**

1. *Context for chapter iteration* — the useful artifact is "here is ch1's prose and here
   is every objection raised against it", read together. `.md` sits next to
   `chapters/ch1-introduction.md`; a spreadsheet row does not.
2. *NotebookLM audits* — **NotebookLM ingests `.md`/text, not `.xlsx`.** An Excel export
   would have to be converted back to text before it could be a source. This alone is
   near-dispositive.

Add to that: `.md` diffs in git (so `delta` across snapshots is `git diff`, not a merge
routine), needs no `openpyxl`, and is readable in the editor already open.

**Where `.xlsx` would genuinely win, and does not yet apply:** many comments (100+),
multiple authors to filter by, and a triage workflow where status is tracked per row rather
than acted on immediately.

**Decision:** `.md` is the primary and only required output. **Task 4's xlsx writer drops
from "required" to "optional, deferred"** — build it if and when comment volume crosses
roughly 50 with both authors active. `openpyxl` (task 2) is therefore **not currently
needed**; extraction stays stdlib-only, which also removes the last dependency install from
the critical path.

**What to add to `comments.md` instead** — the triage value the spreadsheet was for, in a
form `.md` supports:

- **Split by chapter** into `comments/ch1-introduction.md`, so a chapter's prose and its
  objections are one directory apart and a NotebookLM source can be scoped to one chapter.
- **An index/summary table at the top** — id, section, first line — since 14 comments
  already require scrolling.
- **A stable anchor per comment** (`<a id="c22">`) so a draft or plan can link to a
  specific objection.
- **`resolved` / reply markers** — already implemented, now confirmed available.

## F17 — Snapshot folders renamed and timestamped to the minute (2026-09-01)

Two changes applied at Brian's request, both correcting real ambiguity:

1. **`snapshots/` → `docx-exported-snapshots/`.** The old name did not distinguish these
   read-only derived artifacts from `sections-drafts/*.md`, the live working files. The new
   name states the provenance in the path, which matters because F10's whole
   division-of-authority rests on never confusing the two.
2. **Folder stamp `YYYY-MM-DD` → `YYYY-MM-DD_HH-mm`.** Date-only granularity silently
   overwrites a snapshot taken earlier the same day — the exact failure mode for a workflow
   whose cadence is "snapshot before and after a working session". The `--date` flag is
   kept as an alias of the new `--stamp` so existing muscle memory does not break.

`.gitignore` was updated to the new path (`docx-exported-snapshots/*/thesis_full.docx`) and
the existing snapshot was renamed to `2026-09-01_16-24`. Re-run verified clean: 17 chapters,
14 comments, 31,870 words.

## F24 — Band 3 was left homeless when Excel was dropped (2026-09-05)

> *Renumbered from F19 on 2026-09-05: a parallel session independently allocated
> F19-F23 to the extraction-hardening findings. This pair was written first but
> is renumbered because the later findings are already cited by number in the
> task table and progress log.*

**The gap, stated plainly.** F16 deferred the `.xlsx` writer (task 4) and superseded the
prior-export merge (task 5), on the reasoning that with `.md` output the cross-snapshot
delta is just `git diff` between dated folders. That reasoning is correct for *detecting
change* and wrong for *carrying decisions forward*, and the two were conflated.

Band 3 -- `triage_status`, `owner`, `action_taken`, `commit_ref` -- was specified in this
plan's column schema as spreadsheet columns "preserved across re-exports". When the
spreadsheet went, nothing inherited that job. The snapshot extract cannot inherit it: every
`comments/*.md` carries a "Read-only extract. Reply in Word, not here -- this file is
regenerated on every snapshot and any edit is lost" header, which is the correct contract
for a derived artifact and precisely why it cannot hold state.

**Consequence:** as of this session there is no writable surface anywhere in the workflow.
The 14 Ch1 comments can be read but their disposition cannot be recorded.

**What was NOT the problem.** Brian's concern was that the markdown "will become large and
unstructured, with vertical text". That is true of `comments.md` (all chapters, one file),
which is already a wall at 14 comments and would be unusable at ~150. It is *not* true of
`comments/chN.md`, which task 15 already split per chapter and which caps at roughly 20
entries. The per-chapter extract format needs no reformulation -- it needs a writable
sibling.

## F25 — Decision: a writable per-chapter ledger, not a centralised hub (2026-09-05)

Brian raised a "centralized comment hub" with per-comment status tracking. Rejected in
favour of a per-chapter ledger mirroring the existing split.

**Why not a hub.** Two reasons, both about how the work actually happens:

1. Brian's stated working mode is one chapter at a time for optimal context. A hub forces a
   filter-to-one-chapter step at the start of every session, and puts the chapter's prose,
   its objections and its decisions in three unrelated places.
2. The xlsx rejection reasons from F16 still hold and apply equally to any single-table
   format: the ledger has to read *beside* the prose, and NotebookLM ingests text, not
   `.xlsx`.

**The shape adopted:**

```
05_thesis_writing/comment-ledger/
  ch1-introduction.md      <- WRITABLE; survives snapshots
  ch3-methodology.md
  INDEX.md                 <- generated roll-up: per-chapter status counts + THESIS-WIDE list
```

One entry per comment, keyed by `comment_id`, carrying band 3 plus two fields that are new
to this plan:

```markdown
## C22 -- RAM constraint not properly elaborated
- **status:** OPEN | ACCEPTED | DONE | REJECTED | DEFERRED | NEEDS-ENRICO
- **owner:** Brian
- **section:** 1.1 Background and Motivation
- **anchor:** "...deployed under a fixed RAM budget"
- **scope:** THESIS-WIDE
- **related:** C18, C19, C20, C25
- **resolution:**
- **commit:**
```

**Three properties that make it work:**

1. **The ledger is writable; the extract stays read-only.** The two artifacts keep separate
   jobs, which is the same division-of-authority principle as F10 and
   `writing-surface-authority.md`. Nothing regenerates over a decision.
2. **Reconcile, never regenerate.** New comment ids get a stub appended at `status: OPEN`.
   Ids that have vanished from the `.docx` are flagged `GONE (verify)` and **not deleted** --
   F12 established that co-authors delete rather than resolve, so a disappearance is a
   signal to check, not proof of completion.
3. **`scope` and `related` carry the real payload.** C18/19/20/22/25 are one argument -- the
   RAM premise is unearned -- spanning Ch1, Ch3 s3.7, Ch5 s5.1 and Ch10. That is a single
   decision touching five comments across four chapters. A flat list hides the cluster and a
   hub table cannot express it either; explicit cross-links between per-chapter files can.

**Load note.** This is being built for 14 comments when the eventual load is ~150. That is
deliberate -- Brian is about to generate the rest -- but it means the sequencing is: finish
the Word comment pass first, then re-snapshot, then reconcile. Building the ledger against
Ch1 alone only validates the mechanism.

---

## F19 — Heading levels must be resolved from `styles.xml`, never from style names (2026-09-05)

**The break.** The 2026-09-05 re-run produced a structurally wrong snapshot that
*reported success*: 11 chapters instead of 17, chapters 1–6 absent, and an `Abstract`
of **22,885 words**. Nothing errored.

**Cause.** Chapters 1–6 had been restyled in Word from the built-in `Heading1` to a
custom `H1-Chapter`. The script matched on a hardcoded set of style *names*
(`H1_STYLES = {"Heading1", ...}`), so those headings resolved to no level, never opened
a new chapter, and their text flowed into the preceding section.

**Why the existing guard missed it.** The only check was `if d["h1_count"] == 0: abort`.
There were 11 built-in Heading 1s left in the front matter and later chapters, so the
count was non-zero and the run passed. **The guard tested for total failure; the actual
failure was partial.** That distinction is the whole lesson.

**Fix — ask the document, don't hardcode.** `word/styles.xml` states every style's level.
`_heading_levels()` now resolves each `styleId` by three sources, most authoritative first:

1. **explicit `w:outlineLvl`** on the style (0-based; `9` is Word's "not in the outline"
   sentinel and means *not a heading*)
2. **the `w:basedOn` chain** — `H1-Chapter` is `basedOn="Heading1"`, which is precisely
   how a custom style declares its level without restating it
3. **the style name/id** (`"heading 3"`, `"H3 - Chapter"`) as a last resort

Two traps in this document prove name-matching could never have worked:

| style | looks like | actually is |
|---|---|---|
| `TOCHeading` | `basedOn="Heading1"` → level 1 | `outlineLvl=9` → **not a heading** |
| `H1-Tables` | name starts `H1` → level 1 | `basedOn="Caption"` → **a caption** |

**A hand-written style list is not a smaller version of this fix — it is a wrong one.**
Proof: the manual patch applied earlier the same session added `H1-Chapter` and still
missed **ch6**, which only appeared once levels were resolved from the file. The static
list found 5 custom H1s; the resolver found 10.

**Consequence for the drift table.** Ch6's text had been folded into ch5. The corrected
run reports ch5 at **+1,079** (not +5,348) and ch6 at **+258** — so **F15's −1,911 Ch6
outlier, and task 14 built on it, were measurement artifacts of the same class of bug.**

## F20 — The workflow's failure mode is silent success, so the guards target implausibility

A snapshot that aborts is harmless; a snapshot that is quietly wrong gets used. Every new
check therefore targets a parse that is **non-empty but misshapen**, which is what both
known breakages (the ch1/ch10 slug collision in F11, and F19) actually looked like.

`_sanity_warnings()`, in order — exact structural checks before statistical ones, because
a short document can legitimately trip a ratio:

| check | action | catches |
|---|---|---|
| no level-1 heading at all | **ABORT** | wrong file; no level-1 style |
| two chapters share a slug | **ABORT** | F11's ch1/ch10 collision — the later silently overwrote the earlier |
| one section holds >40 % of words (≥5 chapters) | **ABORT** | F19 exactly: neighbours merged in |
| front matter >2,000 words | WARN | the 22,885-word `Abstract`, caught earlier and more legibly |
| empty chapter | WARN | heading present, body lost |
| chapter absent from `CHAPTER_MAP` | WARN | a genuinely new chapter, or a renamed heading |

**The manifest now records how the document was interpreted** — a `Heading styles resolved`
table of style id → level → paragraph count. This is the durable half of the fix: a
restyling shows up as a **diff between two manifests** rather than as a number nobody
checks. Front matter was added to `CHAPTER_MAP` so the unmapped-chapter warning stays
meaningful instead of firing six times per run.

**Residual limitation.** Direct paragraph-level `outlineLvl` overrides (a heading formatted
ad hoc rather than via a style) are still not read. Not seen in this document; would need
`w:pPr/w:outlineLvl` on the paragraph itself.

---

## F21 — Tables were flattened into loose cell values; 28 tables and 4 comments affected (2026-09-05)

**The break.** `read_docx()` walked `body.iter(w:p)`, which **recurses into `w:tbl`**. Every
table cell paragraph therefore arrived looking exactly like a body paragraph, and the
row/column structure was discarded. All **28 tables** in the thesis came out as a vertical
stream of orphaned values:

```
Component
Peak RAM (RSS)
When
Python runtime and libraries (numpy, pandas, LightGBM, ...)
~194 MB
Always
```

`~194 MB` is no longer attached to the component it measures. Prose that says "summarised in
Table 6" was followed by unreadable rubble. This had been true of every snapshot to date.

**Fix.** Walk the body's **direct children** and handle `w:tbl` as a unit, rendering a
markdown pipe table. Document order is preserved, which matters because comment ranges are
tracked positionally.

**The second half: comments anchored in tables.** Four comments (139, 168, 222, 256) anchor
inside a table. They were never lost, but their quoted text was unusable, because anchor
text is collected from raw `w:t` nodes which carry no cell boundary:

| | before | after |
|---|---|---|
| c139 | `RTD37930 ⚠️425895112,19344,449` | `RTD ǀ 37 ǀ 93 ǀ 0 ⚠️ ǀ 42 ǀ 589 ǀ 511 ǀ 2,193 ǀ 44,449` |
| c168 | `RTDnone (promo-zero)DecemberBREEZERp = 0.000...` | `RTD ǀ none (promo-zero) ǀ December ǀ BREEZER ǀ p = 0.000 ǀ ...` |

`_scan_ranges()` now emits a separator when a `w:tc` or `w:tr` closes.

**A pipe separator was the wrong choice, and the document proved it.** The metrics table
defines WMAPE as `Σ|y−ŷ| / Σ|y| × 100` — **content pipes**. Using `|` as the boundary marker
split that formula into `Σ | y−ŷ | / Σ | y |`. The separators are therefore ASCII **unit
(31)** and **record (30)** control characters, rendered as ` | ` / ` || ` only in
`_tidy_anchor()` at the very end. Trimming operates on the placeholders, never on pipes, so
content pipes survive.

**Two ordering traps, both hit during implementation:**

1. `re.sub(r"\s+", " ")` **matches chr(30) and chr(31)** and silently ate the sentinels.
   They must be swapped for placeholders *before* whitespace is collapsed.
2. Trimming dangling separators with a `[ |]+$` character class stripped the closing pipe
   off `Σ|y|`. Trim the placeholders, not the rendered output.

**Verified** with unit cases (row+cells, pipes-in-content, dangling separators, plain prose)
and against the document: 28 separator rows emitted, **0 header/column-count mismatches**.

**Not implemented, and honestly so:** `w:gridSpan` is handled by padding blank columns, but
this document contains **no** merged cells (`gridSpan` 0, `vMerge` 0, nested tables 0), so
that path is **untested against real data**. `vMerge` (vertical merge) is not reconstructed
at all. Markdown cannot express either, so text is kept and the span is lost.

---

## F22 — Merged cells confirmed out of scope (2026-09-05, Brian)

Brian: *"We dont really use merged cells in any of the tables so we should be good."*
Verified against the 2026-09-05 17:23 snapshot — `gridSpan: 0`, `vMerge: 0` across all
28 tables.

**Task 22 stays deferred rather than closed.** The `gridSpan` padding path exists but has
never executed on real data, so it is unproven, not proven-unnecessary. The distinction
matters only if a merged cell is ever introduced: the table will still render, but check it
before trusting it. Nothing to build now.

## F23 — Comment volume and distribution at the close of Enrico's review pass

Snapshot `2026-09-05_17-23` is the first stable reading after the document stopped moving
mid-session (F21 recorded 167 → 204 → 217 within ~90 minutes, because Brian was working
through the document alongside code changes and investigations — expected, not drift).

**217 comments over 8 chapters:**

| chapter | comments | | chapter | comments |
|---|---:|---|---|---:|
| ch1-introduction | 33 | | ch5-framework-design | 16 |
| ch2-literature-review | 26 | | ch6-model-benchmark | **48** |
| ch3-methodology | 31 | | ch7-decision-synthesis | 17 |
| ch4-data-assessment | **42** | | ch8-experimental-evaluation | 4 |

**Two things this table says about sequencing task 20:**

1. **Ch6 (48) and Ch4 (42) carry 41 % of the load between them.** Both are results-bearing
   chapters, which is where a comment is most likely to force a re-run rather than a
   re-write. They should be reconciled first.
2. **Ch8 has 4 comments and ch9/ch10 have none.** That is not agreement — those chapters are
   the least written, so there was less to object to. Do not read a low count as a clean
   bill of health (the same trap F20 flagged for missing drift rows).

**Drift, corrected and stable** (F19's parser bug is gone from these numbers). The upward
deltas are the `.docx` outgrowing bullet drafts, which is expected under
`writing-surface-authority.md`. **`ch3-methodology` at −1,991 is the one genuine negative**
and the only drift row worth investigating.

## F26 — Threads are the unit of triage, not comments (2026-09-05)

The 2026-09-05_17-23 snapshot changes the problem. **217 comments across 8 chapters**, and
for the first time the review is genuinely two-sided: **200 Brian, 17 Guest User (Enrico)**,
with **27 comments carrying the `reply` marker**.

**The structural finding.** `read_docx()` parses `w15:paraIdParent` into `parent_by_para`
and then throws the parent id away -- it uses it only to set a boolean:

```python
if pid in parent_by_para:
    c["is_reply"] = True
```

So the extract knows *that* a comment is a reply and not *what it replies to*. The rendered
output shows this: c54 (Enrico) and c55 (Brian) are consecutive `## [n]` sections at the same
level, distinguishable as a conversation only by reading them and noticing they share an
anchor. Nothing in the data says c55 answers c54.

**Why this matters more than it looks.** A thread is one decision. c56/c57/c58 is a single
question -- whether NotebookLM use belongs in the AI declaration -- that took three comments
and reached a conclusion in the last one ("mention that in the AI statement... specify
precisely what we used it for"). Triaging it as three rows produces three partial records of
one resolved decision. At 27 reply comments that is roughly **190 threads, not 217 items**,
and the count is not the point: the *conclusion of a thread lives in its last message*, so a
per-comment ledger systematically files the answer separately from the question.

**A second, sharper consequence.** Enrico's 17 comments are almost entirely replies, not
originations. He is answering Brian, and several of those answers settle the matter
("open to discuss abt it together", "let's check Max's"). A ledger keyed per comment would
create 17 open items for Enrico that are in fact already-delivered answers to Brian's
questions. `owner` becomes wrong at the moment it is written.

**Consequence for the schema:** the ledger's unit must be the **thread**, keyed by the root
comment id, with replies nested inside the entry rather than promoted to siblings. The
`is_reply` boolean is not sufficient input -- `parent_comment_id` and a derived `thread_id`
must be carried through into the extract first. This was already specified in this plan's
band 2 column schema (`parent_comment_id`, `thread_id`, `reply_count`) and was simply not
implemented when the xlsx was dropped.

## F27 — Tabular processing, revisited at 217 comments (2026-09-05)

Brian asked for a critical reflection on the tabular option, which F16 rejected at 14
comments and F25 rejected again as a centralised hub. **At 217 the argument is closer than
it was, and one of the original reasons has expired -- but the conclusion holds.**

**What changed in favour of a table.** F16's "14 comments already require scrolling"
understated the eventual load by 15x. Real table-shaped needs now exist: *how many open
items are left in ch6*, *what is assigned to Enrico*, *which threads are unresolved*. Those
are aggregations, and markdown answers them only by reading everything.

**What has NOT changed.** The two reasons that killed the xlsx both still hold, and the
second has strengthened:

1. **The ledger must read beside the prose.** Resolution happens by looking at the comment,
   the paragraph it anchors to, and the decision together. A spreadsheet is a different
   application from the one holding the other two.
2. **Comment text is long-form prose, and now dialogue.** c22 is ~200 words; c58 is a
   multi-clause decision. Word-wrapped into a cell these are unreadable, and threading makes
   it worse -- a spreadsheet's answer to a thread is either one row per message (losing the
   thread) or a merged mega-cell (losing the rows).

**The reflection that actually matters:** the choice was framed as *markdown vs. table*, and
that framing is wrong. **A status roll-up and a decision record are two artifacts with two
different jobs**, and trying to satisfy both with one file is what makes either option feel
inadequate:

| Need | Right shape | Written by |
|---|---|---|
| "what is left, where, and whose" | table -- counts, filters, sort | **generated**, never hand-edited |
| "what did we decide about this thread and why" | prose under a stable key | **hand-written** |

`INDEX.md` (task 19 of the ledger addendum) is already the first of these and was
under-specified as "counts". It should be a genuine per-thread status table -- thread id,
chapter, section, owner, status, reply count, one-line gist -- generated from the ledger's
own front-matter on every reconcile. That is the tabular view Brian wants, and because it is
*derived* it cannot drift from the ledger and costs nothing to regenerate.

**So: adopt the table as a generated view, reject it as the storage format.** This is the
same authority split the plan already applies to prose (`.docx` authoritative, snapshot
derived) and to comments (Word authoritative, extract derived). The ledger is authoritative
for decisions; `INDEX.md` is its derived table.

**One thing the table must not do:** it must not carry `resolution` text. The moment a
decision's wording exists in two places, they diverge -- exactly the drift that
`writing-surface-authority.md` was written to prevent. The table carries keys, status and a
gist; the reasoning lives in the ledger only.

## F28 — `resolved` is now live data, not the dead weight F12 assumed (2026-09-05)

F12 predicted that two co-authors would delete settled comments rather than pressing
Resolve, making `w15:done` near-useless and `delta = GONE` the real signal. The 17:23
snapshot contradicts this: the extractor parses `w15:done` and the renderer emits a `✔`
marker for it, so resolved state is being read out of a document where both authors have
now worked.

This matters for the reconcile contract in the ledger addendum, which was written on F12's
assumption. Revised behaviour:

- A comment marked resolved in Word arrives with `resolved: true` -- that is a *reviewer*
  signal, distinct from the ledger's own `status`, and both should be recorded. Word-resolved
  means "the authors stopped arguing"; ledger `DONE` means "the thesis was changed".
  They are not the same claim and the gap between them is worth seeing.
- The `GONE (verify)` rule stays as written. It is now a fallback rather than the primary
  signal, and costs nothing to keep.

---

## F29 — Verification of the cross-check findings F24–F28 (2026-09-05)

Each claim in the parallel session's F24–F28 was checked against the code and the 17:23
snapshot rather than accepted on assertion. **Four hold; one is contradicted by the data.**

| finding | verdict | evidence |
|---|---|---|
| F24 — band 3 has no writable home | **holds** | every `comments/*.md` carries the read-only header; no writable surface exists in the repo |
| F25 — per-chapter ledger over a hub | **holds** | consistent with the F16/F10 authority split; no code implication |
| F26 — threads are the unit of triage | **holds** (see correction below) | `parent_by_para[pid]` is populated at line 304 then used only as a membership test at 309; the parent id is discarded |
| F27 — table as generated view, not storage | **holds** | no code implication; `INDEX.md` remains unbuilt |
| F28 — `resolved` is now live data | **CONTRADICTED** | see below |

### F28 is wrong on the facts

F28 states that resolved status "is being read out of a document where both authors have
now worked", and revises the reconcile contract on that basis. Measured directly from
`word/commentsExtended.xml` in the 17:23 snapshot:

```
commentEx entries: 217 | done: 0 | with paraIdParent: 27
```

**Zero comments are resolved.** The extractor does parse `w15:done` and the renderer does
emit `✔`, but that path has never fired on real data — presence of the *code* was mistaken
for presence of the *data*. `grep -c '✔' comments.md` returns 0.

**F12's original prediction therefore still stands** and should not have been revised:
co-authors are deleting settled comments rather than pressing Resolve, so `delta = GONE`
remains the primary "handled" signal, not a fallback. F28's distinction between
"Word-resolved" and ledger `DONE` is a good one and worth keeping in the schema — but it is
a design provision for a signal that does not yet exist, not a description of current data.

### Correction to F26's supporting detail

F26 says 27 comments carry "the `reply` marker". The **structural claim is correct** — 27
replies exist and the parent id is discarded — but the marker is *not* missing from the
output: `comments.md` renders `` `reply` `` on all 27 (e.g. `## [16] Guest User —
Introduction  \`reply\``). What is missing is only the *parent id*, so the extract can say a
comment is a reply but not what it answers. That is the gap task 23 must close.

**Author split confirmed:** 200 Brian, 17 Guest User (Enrico) — matches F26.

---

## F30 — Threading implemented; 223 comments are 196 threads (2026-09-05)

Tasks 23, 24 and 26 shipped. F26's structural claim is confirmed by the numbers: at snapshot
`2026-09-05_17-44` the document holds **223 comments in 196 threads** — 27 replies folded
into their roots.

**What changed in `read_docx()`.** `parent_by_para` is no longer discarded. A
`paraId -> comment id` map resolves `w15:paraIdParent` to the comment it answers, and four
fields now reach the extract, as band 2 originally specified:

| field | meaning |
|---|---|
| `parent_id` | the comment this one replies to (`None` for a root) |
| `thread_id` | root of the chain; equals `id` for a root |
| `reply_count` | carried on **every** member, so a row reads standalone |
| `thread_pos` | document order within the thread |

The chain walk is guarded against **cycles** and **orphans**: a reply whose parent was
deleted keeps a dangling `parent_id`, so it roots itself rather than disappearing. Measured:
**0 orphan replies** at 17:44.

**Word threads are flat, not nested.** In the largest thread (root 15) both replies carry
`parent=15`, not `16 -> 17`. The walk handles arbitrary depth anyway, since nothing
guarantees Word keeps that shape.

**Rendering (task 24).** One `##` per thread, replies nested as `###` beneath their root.
**Every comment keeps its own `<a id="cNN">` anchor, replies included** — 223 anchors for
223 comments — so existing `#cNN` links from drafts and plans stay valid.

**Thread-aware chapter split.** A thread is filed under its **root's** chapter, so a reply
anchored in a different chapter travels with its conversation instead of being orphaned into
another file as an unexplained fragment.

**Discussion is concentrated, and the shape is informative:**

| chapter | comments | threads | |
|---|---:|---:|---|
| ch1-introduction | 33 | 14 | genuinely two-sided |
| ch2-literature-review | 26 | 18 | two-sided |
| ch3 – ch8 | 164 | 164 | **1:1 — Enrico has not replied yet** |

Everything from ch3 onward is one comment per thread. That is not consensus; it is a review
pass that has not reached those chapters. Same misreading trap as F23's ch8/ch9/ch10 note.

## F31 — `comments/INDEX.md` is the generated table F27 specified

Task 26 shipped as a **derived** artifact, regenerated on every snapshot, never hand-edited.
Per F27 it carries keys, counts and a gist — and deliberately **no `resolution` prose**, so
a decision's wording cannot exist in two places and diverge.

Columns: `thread · chapter · section · opened by · replies · last voice · gist`.

**`last voice` is the column that earns its place.** A thread where Enrico spoke last is
waiting on Brian; one where Brian spoke last is waiting on Enrico. That is the queue, and it
is derivable — so it is computed rather than tracked by hand.

All **196 thread links verified to resolve** to a real `<a id="cNN">` anchor in the right
per-chapter file (0 broken).

**This closes the tabular question** (F16 → F25 → F27) without contradicting any of it: the
table exists, it is generated, and the ledger remains the writable surface for decisions.

---

## F32 — Bold and italic now survive the conversion (2026-09-05)

`_text()` concatenated `w:t` nodes and dropped every run property, so **458 bold and 153
italic runs** were silently flattened. Emphasis in this document is load-bearing: paragraph
lead-ins (`**Selection criteria**:`), table header rows, and the emphasised claim in a
findings sentence all lost their signal.

`_text(el, emphasis=True)` now walks **runs** rather than flattening to `w:t`, and wraps
bold as `**`, italic as `*`, both as `***`. Result: **325 bold spans**, 0 stray markers,
0 unbalanced lines across 9,359 lines of output.

**Four traps, each found by testing rather than reasoning:**

1. **Headings are bold by style definition.** `Heading1`, `H2-Chapter`, `H1-Tables` and 12
   others declare `<w:b>` in `styles.xml`, and **13 heading runs additionally carry an
   explicit `<w:b>`**. Marking naively yields `## **Chapter 3**`. Emphasis is therefore
   suppressed inside any paragraph that resolves to a heading level — verified 0 headings
   contain markers.
2. **`<w:b w:val="0"/>` means bold OFF.** Word cancels inherited bold this way, so presence
   of the element is not enough; `_on()` tests the value.
3. **Markers must hug their text.** `** bold **` is not emphasis in markdown, so leading and
   trailing whitespace is moved outside the markers.
4. **Adjacent runs with identical formatting** produce `**a****b**`. The seam is closed with
   a regex anchored on 4+ asterisks — a naive `replace("**"*2, "")` also eats the halves of
   a legitimate pair, which is exactly what the first implementation did.

**A fifth, found only by validating the real output:** a **bold superscript footnote marker
inside an italic quotation** splits it as `...variables.**1* *This element...` — correct per
run, unreadable as prose. Superscripts and subscripts now carry no emphasis of their own.
That single case was the only unbalanced output in the document, and would have been
invisible without the balance check.

**Deliberately still plain:** `_text()` defaults to `emphasis=False`, because slugs, word
counts and drift comparison must not see marker characters. Verified: drift figures are
byte-identical to the 17:44 snapshot. `_plain()` strips markers for index gists, where a
fixed-width truncation could otherwise cut through a `**` and italicise the rest of a row.

**Not converted:** `color` (69 runs), `highlight` (28) and `strike` (4). Markdown has no
portable syntax for the first two; `~~strike~~` exists but 4 instances did not justify the
risk of mangling a formula containing tildes.

---

## F33 — Word's `w:id` is a position, not an identity. The ledger must key on `w14:paraId` (2026-09-05)

**This is the finding the whole tracking system depends on, and it invalidates the schema
proposed in F25.** The ledger design keys entries as `## C22 -- RAM constraint not properly
elaborated`, i.e. on the comment id shown in the extract. Measured across two snapshots
20 minutes apart:

```
2026-09-05_17-44  ->  2026-09-05_18-04
shared w:id values: 122
  ... of which the SAME id now holds a DIFFERENT comment: 120
all 223 w:id values renumbered;  all 223 w14:paraId values held
```

Comment `16` **was** Enrico's exogenous-variable reply and is **now** Brian's enrichment
objection: inserting one comment earlier in the document shifts every id after it.

**A ledger keyed on `C22` would therefore rot silently** — it would still resolve to *a*
comment, just the wrong one, and nothing in the file would look broken. Given the stated
goal of tracking a claim across iterations, this is the difference between a working system
and one that quietly misfiles decisions.

**`w14:paraId` is the stable key.** It is a Word-generated GUID on the comment's first
paragraph, and it survives renumbering, reordering and insertion:

| candidate key | unique | stable across the pair |
|---|---|---|
| `w:id` | yes | **0 of 223** — pure position |
| `author + date` | **no** (170 keys for 223 comments) | 170 |
| `author + date + text` | near (208/223) | 208 — but **breaks the moment a comment is edited** |
| **`w14:paraId`** | **yes** | **223 of 223** |

**Consequences for the design:**

1. **Ledger entries key on `paraId`**, with the human-facing `w:id` carried as a *display*
   field that is refreshed on every reconcile, never matched on.
2. **`thread_id` must also be a `paraId`**, not a comment id — F30 currently derives it from
   `w:id`, which means thread identity is as unstable as the ids it is built from. This is a
   defect in shipped code, not a future concern.
3. **NEW / GONE detection becomes trustworthy**: 16 new and 0 gone across the pair, computed
   on `paraId`. Under `w:id` the same comparison is noise.

**Caveat, untested:** whether `paraId` survives a document round-tripped through a different
editor (Google Docs, LibreOffice, Word Online). It is a Microsoft extension. If a co-author
ever edits outside desktop Word, re-verify before trusting the key. `author+date+text` is
the fallback reconciliation, at 93 % coverage.

---

## F34 — Design: the claim ledger, and what "was / is / should" actually requires (2026-09-05)

Brian's requirement: a base on which **the human writers, repo-aware Claude, and NotebookLM**
can collaborate per claim and per section, pointing precisely into chapter snapshots, and
able to compare **was** (previous snapshots) → **is** (current) → **should** (unresolved
comments, plans, open decisions).

### The three surfaces, and why none of the existing ones can do this

| surface | holds | can it carry state? |
|---|---|---|
| OneDrive `.docx` | prose + comments | yes, but only Word can read it, and only while a comment exists |
| `docx-exported-snapshots/*` | was + is | **no** — regenerated; the DO-NOT-EDIT header is the contract |
| `sections-drafts/*.md` | planning bullets | yes, but per *section*, not per *claim* |

**"Should" has no home at all.** That is F24's gap, restated precisely: the moment a thread
is resolved in Word by deleting it, the decision and its reasoning vanish from every surface
in the repo. The snapshot preserves the *text* of a deleted comment only in whichever dated
folder predates the deletion — findable only if you already know when it was deleted.

### What the data supports (measured, not assumed)

- **Identity**: `w14:paraId` — stable across renumbering (F33).
- **Location**: `heading_path` (e.g. `Introduction > Background and Motivation`) is stable
  under text edits and survives chapter renames better than a slug.
- **The quoted text**: `anchor` is the *volatile* field by design — it is the "was" of the
  prose. Storing it in the ledger and diffing it against the current snapshot is exactly the
  was→is comparison; it must be **stored per snapshot**, not overwritten.

### Shape

```
05_thesis_writing/comment-ledger/
  ch1-introduction.md          <- WRITABLE. One entry per THREAD, keyed by root paraId
  ...
  INDEX.md                     <- generated: status roll-up (F31 already builds this shape)
```

Entry, revised from F25 to key on paraId and to carry the was/is/should triple:

```markdown
## T-38BC720B  --  no exogenous enrichment
- **thread:** 38BC720B            <!-- root paraId; the stable key -->
- **display:** c15 (snapshot 2026-09-05_18-04)   <!-- refreshed, never matched on -->
- **section:** Introduction > Background and Motivation
- **status:** OPEN | ACCEPTED | DONE | REJECTED | DEFERRED | NEEDS-ENRICO
- **owner:** Brian
- **scope:** THESIS-WIDE
- **related:** T-6A1F..., T-9C02...
- **was:** "enriched with exogenous contextual features substantially outperform..."
           @ 2026-09-05_17-44
- **is:**  (auto: current anchor text, or GONE)
- **should:** add one exogenous variable (holiday API) -- Brian, thread reply c17
- **resolution:**
- **commit:**
```

**`was` / `is` / `should` map onto three different mechanisms**, which is why they cannot be
one field:

| | source | written by |
|---|---|---|
| **was** | anchor text at the snapshot when the thread was opened | reconcile, **once**, then frozen |
| **is** | anchor text in the current snapshot | reconcile, **every run** |
| **should** | the thread's conclusion + linked plans | **human** (or Claude proposing, human approving) |

When `was != is`, the prose moved under the comment — that is precisely the case Brian
raised ("the underlying quoted sections would change significantly"). The reconcile marks it
`DRIFTED` rather than guessing whether the objection still applies.

### Why this serves all three consumers

- **Human**: one file per chapter, decisions beside the objection that prompted them.
- **Claude**: `paraId` is greppable and stable, so "what is unresolved in ch6" is a
  deterministic query, not a judgement call. `related` links express clusters (the RAM
  argument spans four chapters) that no flat list can.
- **NotebookLM**: markdown, and per chapter, so a chapter's prose + objections + decisions
  can be fed as one scoped source — the same reason F16 rejected `.xlsx`.

### The one thing this design refuses to do

**No status is ever inferred from the document.** A vanished comment becomes `GONE (verify)`,
never `DONE` — F12 established that these two authors delete rather than resolve, and F29
confirmed `done: 0` across 217 comments. Deletion is a prompt to record a decision, not
evidence that one was made.

### Sequencing

Task 23's `thread_id` must move to `paraId` **before** any ledger is seeded (F33 point 2),
or the ledger inherits an unstable key from day one.

---

## F35 — Resolved comments DO round-trip; F28 was right and F29's correction was too strong (2026-09-05)

Brian resolved one comment in Word as a live test. It came through end-to-end:

```
commentEx: 239 | done: 1 | resolved paraId: 1DE68C76
comments.md:  ## [5] Brian Rohde -- Abstract  `RESOLVED`     (index shows a checkmark)
parsed:       para_id=1DE68C76  author=Brian Rohde  text='Test Comment Resolved'
```

**This settles the F12 -> F28 -> F29 disagreement, and all three were partly wrong:**

- **F12** predicted co-authors would delete rather than resolve, making `w15:done` dead
  weight. **Wrong as a prediction** — it was a guess about behaviour, now overtaken.
- **F28** claimed resolved status "is being read out of a document where both authors have
  worked". **Right about the mechanism, wrong about the evidence** — at the time `done: 0`,
  so it described a capability, not observed data.
- **F29** (mine) corrected F28 by measurement and concluded F12 "still stands". **The
  measurement was correct and the conclusion was too strong**: absence of resolved comments
  reflected that nobody had resolved one *yet*, not that the workflow would not use them.

**The lesson worth keeping:** `done: 0` meant "untested", and I read it as "unused". A
zero measurement distinguishes *absent* from *impossible* only when something has actually
been tried.

**Brian's stated preference now governs the design** (2026-09-05): *"Resolving is preferred
to deleting, as it is not visible to a human anymore but the history is preserved (good for
tracking progress too)."*

**Consequences for the ledger (F34), which was written on F12's assumption:**

1. **`resolved: true` is the primary handled-signal**, not `delta = GONE`. GONE becomes the
   rare, anomalous case — a genuinely deleted comment — and keeps its `GONE (verify)`
   treatment precisely because it is now unusual.
2. **Resolved threads stay in the document**, so their text, replies and anchor remain
   available to every future snapshot. The ledger's `was` field is no longer the only
   surviving record of a settled thread; the reconcile can keep reading the real thing.
3. **Word-resolved and ledger-`DONE` remain distinct** — F28's distinction survives intact.
   Word-resolved = "the authors stopped arguing"; ledger `DONE` = "the thesis was changed".
   The gap between them is the actionable queue.
4. **Task 29's constraint is withdrawn.** The reconcile contract *may* key on resolved
   status. It still must not infer `DONE` from it.

## F36 — Italic works; the document does not yet use it consistently (2026-09-05)

Brian asked whether the emphasis work covers italics, with a view to a convention: **bold**
for important highlights, *italic* for model names, metrics and domain terminology
(`XGBoost`, `tracemalloc`, `lag_1`, `accuracy`).

**The mechanism handles it.** Current export: **311 bold, 129 italic, 2 bold+italic** spans,
all balanced. Italic already carries identifiers such as `product_id` and `Catalog SKUs`.

**The document does not yet apply the convention**, which is the real answer to the question:

| term | occurrences | italicised |
|---|---:|---:|
| `XGBoost` | 51 | 1 |
| `LightGBM` | 58 | 1 |
| `tracemalloc` | 11 | 0 |
| `Prophet` | 15 | 0 |
| `lag_1` | 4 | 0 |
| `Ridge` | 25 | 1 |

The exporter is **faithful, not normative** — it carries whatever Word contains. Adopting the
convention is a formatting pass in Word across 200+ instances, not a change to this script.

**Recommendation if the convention is adopted:** apply it with a Word *character style*
(e.g. `Term`) rather than direct italic formatting. A style is one Find-and-Replace to
change globally, survives a restyle, and — because `_heading_levels()` already reads
`styles.xml` — the exporter could then distinguish "italic because it is a term" from
"italic because it is a quotation", which direct formatting cannot express. That distinction
is worth having before 200 instances are set the other way.

---

## F37 — The `Term` character style works, and needed a code change to be seen (2026-09-05)

Brian applied a Word character style `Term` to `CSD` (x2), `danskvand`, `energidrikke` and
`RTD` — the recommendation from F36, adopted.

**It was invisible to the exporter.** The style supplies the italic (`Term` defines `i`), so
the runs carry **no direct `<w:i>` at all**: `direct-bold=False direct-italic=False` on all
five. Emphasis detection read direct run properties only, so styled terms exported as plain
text. Fixed by reading `w:rStyle` alongside the direct properties.

**Word created it as a linked style**, so the character half is `TermChar`, not `Term`.
`TERM_STYLES` accepts both — a linked style is what you get from the normal Word UI, so this
is the expected shape, not an edge case.

**Terms render as `` `code` ``, not italics.** This is the distinction F36 argued for, now
realised: `` `danskvand` `` is unambiguously a term, while `*...*` remains a quotation or
emphasis. Direct italic formatting cannot express that difference, which is why the style
matters more than the appearance.

**Consequence:** applying `Term` in Word is now the whole workflow. No script change is
needed per term, and the 200+ instance pass (`XGBoost` 1 of 51, F36) can proceed knowing the
export will carry it.

## F38 — Brian's keyword vocabulary is machine-readable and becomes the work plan (2026-09-05)

Brian's whole-thesis review used ALL-CAPS keyword prefixes (`VERIFY & APPENDIX: ...`). Parsed
across the 268-comment pass: **201 tagged, 40 threads untagged**.

| tag | threads | | tag | threads |
|---|---:|---|---|---:|
| VERIFY | 111 | | APPENDIX / FORMATTING | 8 each |
| PROSE | 71 | | ACADEMIC / TABLE-REFERENCE | 7 each |
| SOURCE | 37 | | WATERMARK | 6 |
| OUTDATED | 34 | | UPDATE / MATH | 2 each |
| METACOMMENT | 21 | | MISSING / INTERNALREFERENCES | 1 each |
| CONTEXT | 16 | | NAMING | 13 |
| INCORRECT | 11 | | | |

**Implementation:** `KEYWORDS` maps canonical tags to accepted variants, including the
`METACOMMMENT` typo and the `SOURCES`/`SOURCE` and `VERIFY`/`VALIDATE` pairs. Matched **only
in the first 120 characters**, because these are written as prefixes and the same words occur
naturally in later prose, where they are not tags.

Tags are attached per comment, unioned per thread (a reply can introduce a type the root did
not name), and surfaced in three places: the per-chapter index, the comment section header,
and a new **Work type by chapter** matrix in `INDEX.md`.

**Why this matters more than a convenience.** It converts the review from 241 prose objections
into a routable plan. The matrix reads directly as sequencing:

- **VERIFY (111)** is the dominant tag and is concentrated in **ch6 (39)** and **ch4 (19)** —
  claims to re-check against code and results. This is the work that needs the repository,
  i.e. the work Claude is actually positioned to do.
- **PROSE (71)**, heaviest in **ch6 (23)**, is writing work — Brian's, not automatable.
- **OUTDATED (34)** clusters in **ch8 (10), ch4 (9), ch3 (7)** and pairs with INCORRECT (11)
  as the factual-correction queue.
- **WATERMARK (6)** sits mostly in **ch3 (4)** — a localised AI-tone problem, not diffuse.

**The tags map onto Brian's own review notes**, which distinguish work needing the repository
(VERIFY, OUTDATED, INCORRECT), work needing NotebookLM/Zotero (SOURCE), and work needing a
human writer (PROSE, ACADEMIC, WATERMARK). **That three-way split is the natural division of
labour for the ledger**, and it fell out of the data rather than being imposed on it.

**Open, from Brian's notes, not yet actionable here:** cross-chapter repetition and weak
handovers ("an artifact from us writing each chapter with AI individually"). That is a
structural problem the per-chapter export makes *harder* to see, since it scopes to one
chapter at a time. Worth a dedicated cross-chapter duplication check later; noted as task 39.

---

## F39 — PROSE and VERIFY are one pass, not two (2026-09-05, measured)

Brian: *"PROSE is actually something that I want your help with as well. Most of the time it
is coupled with a verification pass, which you would need to do in the repository anyways."*

**The data agrees, decisively.** Of 71 PROSE threads:

| combination | threads |
|---|---:|
| PROSE + VERIFY | 28 |
| PROSE + SOURCE + VERIFY | 17 |
| OUTDATED + PROSE + VERIFY | 4 |
| other PROSE + VERIFY variants | 7 |
| **PROSE together with VERIFY** | **56 of 71** |
| **PROSE alone** | **6** |

Splitting them into a "writing queue" and a "checking queue" would therefore double-handle
56 threads: the same paragraph would be opened twice, once to confirm the claim and again to
write it. **They are one operation** — establish what is true from the repo, then write it.

**A second measurement kills the obvious alternative.** The 126 PROSE/VERIFY threads spread
across **99 distinct sections** — a median of one per section. There is no section-level
cluster to batch, so the working unit has to be the **chapter**, which is also the unit the
export already produces and the unit Brian says he works in.

**Third, and the reason the export needed changing:** these comments are frequently *bare
tags*. Thread 237 reads, in full, `VERIFY, SOURCES, PROSE`. The instruction lives in Brian's
keyword notes, not in the comment. **The anchored text is therefore the entire specification
of the work item**, which made the 400-character anchor cap a real defect, not cosmetic:
78 of 268 anchors were cut mid-passage. Raised to 2,000 with head-and-tail excerpting;
**265 of 268 now complete**, and the 3 that remain say how much was elided and why.

## F40 — Recommended working order, and why it is not the obvious one

Brian's stated pipeline: **Claude drafts prose → `watermarks-remover` strips AI provenance →
human pass to humanise.** He notes the already-prosed chapters were themselves Claude-written
originally, so this is not a change of authorship, it is finishing an existing draft.

**The order is right, and the reason is stronger than efficiency.** De-watermarking is a
*text transformation*; if a human rewrite follows it, the human reintroduces their own
phrasing and the strip must be re-run. If it precedes drafting, there is nothing to strip.
The order draft → strip → humanise is the only one where each step's output is stable for the
next. **This also means the human pass must be last, and must be the thing that ships** — a
de-watermarked but un-humanised chapter is not finished.

**One caveat worth stating plainly:** `watermarks-remover` removes *provenance marks* —
invisible Unicode, metadata, some statistical signal. It does not make AI-written prose read
as human, and its own documentation calls detector evasion best-effort. The humanising pass
is doing the real work; the tool is hygiene, not disguise. Planning as if the tool were
sufficient would leave WATERMARK-tagged prose in the submission.

### Recommended sequence

**Phase 0 — commit, then freeze a baseline.** The `2026-09-05_19-10_complete-review-pass`
snapshot is the "was". Nothing else can be measured against it if it is not committed.

**Phase 1 — ch6 first (48 threads, 39 VERIFY, 23 PROSE).** It is the largest concentration
of exactly the coupled work above, and it is results-bearing, so a wrong claim there is a
wrong finding, not a wrong sentence. It also has the most SOURCE tags (18), so the
NotebookLM/Zotero work batches with it.

**Then ch4 (42), ch3 (31), ch7 (17), ch8, ch5, ch2, ch1.** Roughly by volume, except that
**ch3 carries 4 of the 6 WATERMARK tags** — worth doing while the de-watermarking workflow is
fresh rather than as an afterthought.

### Per chapter, the loop

1. **Read** `comments/chN.md` (objections, threaded, with full anchors) beside
   `chapters/chN.md` (the prose as it stands).
2. **Resolve VERIFY/OUTDATED/INCORRECT from the repository** — these are answerable from code
   and results, and are the part Claude is positioned to do.
3. **Draft PROSE** for the same passages in the same pass, grounded in what step 2 established.
4. **Record the decision in the ledger** (task 33), keyed on `paraId`, with `should` filled.
5. **Brian applies to the `.docx`** and marks the thread resolved in Word (F35 — resolve, do
   not delete).
6. **Re-snapshot.** `was != is` on the anchor confirms the passage actually changed.

### What must NOT be restructured

The export stays **read-only and regenerable**. The temptation, now that it carries tags and
threads, is to let it hold status. It must not: that is the ledger's job, and the separation
is what keeps a re-run from destroying a decision (F24, F34, `writing-surface-authority.md`).

### The one gap this order does not close

Brian's own review note — cross-chapter repetition and weak handovers — is invisible to a
chapter-at-a-time loop, and the loop will actively *entrench* it by improving each chapter in
isolation. It needs a dedicated cross-chapter pass (task 39), and the right moment is **after
ch6 and ch4** (where the duplication is densest) but **before** the remaining chapters are
rewritten around text that may later move.

---

## F41 — `sections/`: the heading tree mirrored as nested folders (2026-09-05, Brian's design)

Brian: *"a .md file for each 'only' H2 header section ... and another folder for H2 headers
that have more than H2 level ... That way we have precise (sub)section comparability across
snapshots."* **Adopted as specified, as an addition — `chapters/` is unchanged.**

**The document supports it cleanly.** 17 H1, 78 H2, 70 H3, and **zero skipped levels**
(no H1 → H3 jumps), so the tree is well-formed with no special-casing:

```
sections/08-ch4-data-assessment/
  00-preamble.md
  01-overview-and-data-strategy/          <- H2 WITH H3 children -> folder
    00-intro.md                           <- the H2's own body text
    01-source-type-and-access.md          <- H3 leaf -> file
    ... 05-forecasting-suitability.md
  02-csd-worked-category-eda-and-parameters/
  03-feature-engineering-forecasting-substrate.md   <- H2, no children -> file
```

**63 leaf H2s became files, 15 parent H2s became folders**, holding 70 H3 files:
**154 leaf files**. Numeric prefixes preserve document order (without them
`10-conclusion` sorts before `2-literature-review`).

**Why it earns its place, in one number:** median H3 body is **98 words**. A chapter file is
3,000–6,000. Asking "how did *4.1.1 Source, Type, and Access* change between two snapshots"
is now a 98-word diff instead of a 3,700-word one — and a Claude session can load the single
section it needs rather than a whole chapter.

**One design correction made during implementation.** The first version listed comment ids
per section. That would have made **every section file diff on every snapshot** — `w:id` is
renumbered on each insertion (F33), so the ids churn even when the prose is untouched,
destroying exactly the signal this tree exists to give. Verified in the wild: a diff of
`4.1.3 Overall Suitability` across two snapshots showed *only* the id line changing. Section
files now carry **comment counts and work-type tags** (stable) and point at
`comments/chN.md` for the detail.

**Measured after the fix:** between the 17:23 and 19:10 snapshots, **67 of 154 sections
differ**, concentrated in front matter and the abstract — where the editing actually
happened. ch6's results sections are byte-identical. That is the tool doing its job.

**On Brian's framing of "was vs is":** he explicitly does *not* want a deterministic
comparison — *"its rather that the snapshots give a Claude session agent the ability to
compare a past chapter with the most current snapshot chapter."* That is a weaker and more
useful requirement than the F34 ledger's `was`/`is` fields imply, and `sections/` satisfies
it with ordinary `diff`. **The ledger's `was`/`is` should therefore be understood as
provenance pointers (which snapshot), not as stored copies of the text.**

## F42 — `05_thesis_writing/writing-notes/` is a first-class input to the revision workflow

Brian flagged eight files (~2,900 lines) written by Claude sessions while he worked through
the codebase. They are **not** informal notes — each carries `applies-to` frontmatter mapping
it to chapters, and they are the reasoning behind decisions the thesis asserts.

| note | applies to |
|---|---|
| `2026_08_22-21_00-chapter-staleness-audit` | ch3–ch10 (all) |
| `sample-size-and-tool-interface-rationale` (978 lines) | ch4, ch5, ch6, ch7, ch8, ch10 |
| `srq1-model-ladder-and-baselines` | ch5, ch6 |
| `srq1-pooled-vs-per-category` | ch6, ch8 |
| `srq1-tuning-and-validation-protocol` | ch5 |
| `srq4-experiment-design-rationale` | ch3, ch5, ch8, ch10 |
| `srq4-first-results-and-interpretation` | ch8, ch9, ch10 |
| `prometheus-scenarios-design-rationale` | ch7, ch8 |

**The staleness audit is the important one for sequencing.** It states:
*"THE CRITICAL FINDING: ch6 passes the checker and is wrong throughout"* — 42 ERROR, 6 CHECK
as of 2026-08-22. That is independent confirmation of the ch6-first recommendation (F40),
reached from a different direction than the comment tags.

**But the notes have their own staleness**, and it is declared in their own frontmatter:
`sample-size-and-tool-interface-rationale` says *"all counts are snapshot-specific and
superseded by the 2026-08-12 re-pull"*. **They are evidence to check against the repo, not
authority to copy from.** The precedence for the revision loop is: **code and artefacts on
disk > writing-notes > current thesis prose**.

**Revised chapter loop** (supersedes F40 step 2): read `comments/chN.md` + `chapters/chN.md`,
**then the writing-notes whose `applies-to` names this chapter**, then resolve VERIFY against
the repo — using the notes to find the argument quickly, and the code to confirm it is still
true.

---

## F43 — Final export shape: three levels, two of them section-divided (2026-09-05, Brian)

Brian moved `sections/` under `chapters/` by hand and asked whether comments should mirror
it. **Both adopted.** The reasoning he gave is the right one: it is *chapter content divided
by section*, so it belongs under `chapters/`, not beside it.

```
2026-09-05_19-52_complete-review-pass/
  thesis_full.md                        whole document          <- level 1
  chapters/chN.md                       17 chapter files        <- level 2
  chapters/sections/<ch>/<h2>/<h3>.md   154 leaf sections       <- level 3
  comments.md                           all 281 comments        <- level 1
  comments/chN.md                       13 chapter files        <- level 2
  comments/sections/<ch>/<h2>/<h3>.md   138 sections w/ comments <- level 3
  comments/INDEX.md                     254 threads + work matrix
```

**Why the comment mirror matters, concretely.** Before it, a section file said *"4 comments
-- VERIFY, TABLE-REFERENCE, SOURCE, METACOMMENT"* and then sent the reader to a **48-thread**
chapter file to find them. The pairing closes that: identical relative path, one file holding
prose and the other the objections, each pointing at the other.

**Both trees share one `_section_tree()`**, so they cannot drift apart — a single traversal
produces the keys for both. Verified: **0 comment-section files without a prose twin**, and
**280 of 281 comments land in a leaf section** (the 1 remaining is anchored at chapter level
and stays in `comments/chN.md`, correctly).

**One deliberate asymmetry:** `chapters/sections/` writes all 154 leaves; `comments/sections/`
writes only the 138 that carry comments. Emitting 154 mostly-empty comment files would bury
the ones that matter.

**Matching is on the full heading path, not the last heading.** "Results" appears under
several chapters; a loose match would file a ch6 objection under ch8.

## F44 — Verification precedence, stated as a rule (2026-09-05, Brian)

Brian: *"any note or claim should be verified each time and not taken for granted. The most
up to date and accurate state is always inside the repository in the script code, or saved to
script output files."*

**The precedence, in order:**

1. **Script code** -- the logic, as it actually runs
2. **Generated artefacts** -- EDA graphs, result tables, model performance outputs; the same
   files destined for the appendices
3. **`writing-notes/`** -- the argument and its rationale, useful for *finding* the claim fast
4. **Thesis prose** -- what is currently asserted, and the thing under review

**Nothing at level 3 or 4 is evidence.** The notes declare their own staleness
(`sample-size-and-tool-interface-rationale`: *"superseded by the 2026-08-12 re-pull"*), and
the staleness audit records the sharper case: *"ch6 passes the checker and is wrong
throughout"* -- prose that survives an automated check while being false.

**Operationally this means a VERIFY thread is not closed by finding the claim in a note.** It
is closed by finding the code path or the artefact that produces the number, and confirming
the number in the thesis matches it today. Where the two disagree, the artefact wins and the
prose changes.

**This also constrains what "done" means for the ledger:** a VERIFY resolution should cite
the script or artefact it was checked against, not the note that explained it.

## F45 — Keyword bareness is the convention, not an omission (2026-09-05, Brian)

Brian: *"This bareness with meaning does not only extend to PROSE, but any comment. Thats why
I had the keyword dictionary accompanied in my notes."*

A bare `VERIFY` or `OUTDATED` is a **complete instruction**, resolved against the keyword
dictionary in Brian's review notes plus the anchored passage. Additional prose appears only
where the tag alone was insufficient.

**Two consequences already handled, and one still open:**

- The anchor cap had to rise (F39): with a bare tag, the anchored passage is the entire
  specification. Done -- 265 of 268 anchors now complete.
- The keyword dictionary must be treated as **part of the workflow**, not as background
  reading. It is currently only in Brian's message and paraphrased in F38; it should live in
  the repo as the canonical definition. **Open -- task 47.**
- **Do not treat an untagged comment as untagged work.** 40 threads carry no keyword; those
  are the ones where the prose text carries the whole instruction, so they need reading, not
  classification.

---

## F46 — The keyword dictionary is now in the repo (2026-09-05)

Written to `05_thesis_writing/writing-notes/review_comment_keywords.md`, alongside the other
`applies-to`-tagged workflow references rather than at the `05_thesis_writing/` root (which
holds only folders).

**Why it had to be committed:** the exporter parses 17 tags and renders them in three places,
but nothing in the repository said what they *mean*. A future session would have had
`VERIFY` on 111 threads and no definition of what discharges it. The tags are the instruction
(F45), so the dictionary is executable workflow, not background reading.

**Contents:** Brian's definitions verbatim (including the MATH linear-formula example and the
METACOMMENT rule that no in-repository reference may appear in the thesis), the measured
distribution at the 19-52 baseline, the three-way split of who resolves what, the F44
verification precedence, and the parsing rules with their rationale (120-character window,
variant folding, thread-level union).

**Verified before committing** rather than asserted: 72 PROSE threads of which 56 also carry
VERIFY and 6 are PROSE alone; 254 threads, 214 tagged, 40 untagged; and **every one of the 17
keys in `KEYWORDS` is documented** — a tag the script parses but the dictionary omits would be
a tag a future session cannot act on. The file states that rule for whoever extends it.
