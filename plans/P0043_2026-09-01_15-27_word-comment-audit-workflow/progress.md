---
pid: P0043
created: 2026-09-01 15:27:00
updated: 2026-09-01 18:45:00
---

# P0043 — Progress log

## 2026-09-01 15:27 — Session 1: scoping

**Branch:** `plan/p0042-scope-freeze` (carried over from prior session; a dedicated
branch should be cut before any code lands).

**Trigger:** Brian wants a Word→Excel comment export workflow to speed up revision rounds
on the shared thesis document, and asked which metrics to include beyond the four in the
guide he attached (page / text / author / date).

**Done:**

- Surveyed the repo for `.docx` files and inspected their OOXML parts.
- Established F1–F4 in `findings.md` — most importantly that **no repo `.docx` carries
  comments**, so the extractor has nothing real to test against yet.
- Confirmed `python-docx` / `openpyxl` / `lxml` are all missing from `.venv`.
- Settled three design decisions with Brian:
  1. **Engine** — Python OOXML primary + thin VBA fallback for page numbers.
  2. **Output** — timestamped `.xlsx` in `05_thesis_writing/analysis/comment-audits/`.
  3. **Round-trip** — re-export merges prior triage by comment id, flags `NEW`/`CHANGED`/`GONE`.
- Designed the three-band column schema (identity/location, content, triage) in
  `task_plan.md`, and answered the "which other metrics" question there.

**Not done:** no code written, no dependencies installed. A `pip install` was started and
cancelled in favour of writing this plan first.

**Blocker:** task 1 — the path to the real reviewed document. Everything downstream can be
built against a synthetic fixture, but nothing can be validated without it.

**Next session should:**
1. Get an answer to the three open questions at the foot of `task_plan.md`.
2. Cut a branch, e.g. `config/word-comment-audit`.
3. Install deps (task 2), then build the extractor against a hand-authored test fixture
   while waiting on the real file.

## 2026-09-01 16:55 — Session 2: re-read plan, two new facts folded in

**Context:** Brian added F5–F11 and `prototype_docx_comments.py` from a parallel session,
then supplied two facts that change the plan's framing.

**Fact 1 — two authors, no reviewer.** Only Brian and Enrico touch the comments. The plan
was written assuming inbound supervisor review. Recorded as **F12**; the "Why this plan
exists" section and open question 3 were reworded. Net effect on the schema: `author` and
the band-3 merge rise in importance, `resolved` falls (co-authors delete rather than
resolve, so `delta = GONE` is the real "handled" signal), and no reviewer-management fields
should be added.

**Fact 2 — the proposed snapshot → split → diff flow.** Assessed and **adopted** as
**F13**. It is the right shape and matches F9/F10/F11, with one genuine addition worth
making explicit: prose and comments are captured in the *same* operation, from the same
parse. Formalised as "the snapshot contract" in `task_plan.md` — one dated folder holding
`thesis_full.docx` (gitignored) + `thesis_full.md` + `chapters/*.md` + `comments.xlsx` +
`comments.csv` + `manifest.json`.

**Schema change:** `snapshot_id` added to band 1.

**Tasks 9–11 rewritten:** task 9 is now sentence-level (was paragraph-level) and depends on
task 11, because the normalisation step is what makes the diff readable at all.

**Three risks recorded in F13:** one-way diff discipline (`DO-NOT-EDIT` headers), first-run
diff noise from markdown syntax (normalise before comparing), and repo growth from binary
snapshots (gitignore the `.docx`, keep sha256 in the manifest).

**Still blocked:** task 1 — the OneDrive path to the stitched `.docx`. Now the only
outstanding blocker; open question 2 is answered (F6) and 3 is reframed (F12).

**Still true from session 1:** no code written, no dependencies installed, still on
`plan/p0042-scope-freeze`.

## 2026-09-01 18:45 — Session 3: reviewed `thesis_snapshot.py`, applied Brian's three requests

**Reviewed:** `utility_scripts/scripts/thesis_snapshot.py` (written in a parallel session)
and its output at `docx-exported-snapshots/2026-09-01_16-24/`. It works and has run against
the real OneDrive document — **task 1's blocker is gone** (F14). 31,870 words, 17 Heading-1
sections, 14 comments, `commentsExtended.xml` present.

**Request 1 — rename `snapshots/` → `docx-exported-snapshots/`.** Done (F17). Script
constant, docstring, `.gitignore` path and the existing folder all updated. The name now
states provenance, which is what keeps these derived files distinct from the live
`sections-drafts/*.md`.

**Request 2 — minute-level timestamps.** Done (F17). Folder stamp is now
`YYYY-MM-DD_HH-mm`; `--date` kept as an alias of the new `--stamp`. Date-only granularity
silently overwrote a same-day snapshot, which is the exact failure mode for a
snapshot-before-and-after-session cadence.

**Request 3 — `.md` or Excel?** Assessed against the real 14 comments and answered in
**F16: keep `.md`, defer the xlsx.** The decisive point is Brian's own stated goal —
NotebookLM ingests text, not `.xlsx`, so a spreadsheet would have to be converted back
before it could be a source. The comments are also long-form reasoning (comment [22] is
~200 words proposing an experiment-design change), which no spreadsheet cell renders
readably, and all 14 share one author, so Excel's filtering advantage has nothing to act on.
**Tasks 2, 4 and 5 were dropped/deferred/superseded as a result** — the pipeline is now
stdlib-only with no dependency install on the critical path.

**Also implemented this session (task 15, and part of 11/10):**

- **Per-chapter comment files** — `comments/ch1-introduction.md` alongside the combined
  `comments.md`, sharing the same slug map so `comments/chN.md` pairs with `chapters/chN.md`.
- **Index table** at the top of each comments file (id · section · opening line) with
  **stable `<a id="cNN">` anchors**, so a plan or draft can link to one specific objection.
- **`DO-NOT-EDIT` header** on every chapter file (task 11's remaining item).
- **SHA-256 in `MANIFEST.md`** (task 10's remaining item) — provenance for the gitignored
  `.docx`.

Verified by re-running end-to-end: 17 chapters, 14 comments over 1 chapter file, sha
`2ce1b0cd…`. Test snapshots removed afterwards; only `2026-09-01_16-24` remains.

**F15 supersedes F7's drift numbers.** Measured against the authoritative document rather
than the stale `sections-final/*.docx`: **Ch2 was a false alarm** (−1,316 → −199) and
**Ch6 is the real outlier at −1,911**, previously invisible because no ch6 file exists in
`sections-final/`. Ch7 and Ch8 have no draft counterpart and so produce no row at all.

**Tooling issues logged** (#25–27): backslash-escape collapse when authoring Python through
a bash heredoc, mixed CRLF/LF defeating line-based repair, and a benign
"Device or resource busy" on an already-emptied directory.

**Still on `plan/p0042-scope-freeze`** — a dedicated branch should be cut before committing.

**Next:** task 16 (per-chapter index is done; anchors done — remaining is wiring links from
drafts), task 14 (**investigate Ch6 −1,911**), task 12 (test the heading→filename map), and
task 13 (snapshot retention: nothing prunes yet).
