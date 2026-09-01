---
pid: P0043
created: 2026-09-01 15:27:00
updated: 2026-09-01 18:45:00
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
