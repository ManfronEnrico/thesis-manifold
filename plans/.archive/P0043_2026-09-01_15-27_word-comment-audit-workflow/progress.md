---
pid: P0043
created: 2026-09-01 15:27:00
updated: 2026-09-05 20:05:00
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

---

## Session 2026-09-05 — the writable half (planning only, no code)

**No code written this session.** Inspected the existing workflow and recorded a design
decision; the plan is now current for cross-session pickup.

**What was inspected:** `thesis_snapshot.py` (450 lines), the `2026-09-01_18-50` snapshot
folder, `comments/ch1-introduction.md` (14 comments), `comments.md`, `MANIFEST.md`, and this
plan's task table.

**Finding.** Brian's stated worry — the markdown will grow "large and unstructured, with
vertical text" — is true of `comments.md` (one file, all chapters) and **not** true of
`comments/chN.md`, which task 15 already split and which caps around 20 entries per chapter.
The extract format needs no reformulation.

The real gap is different and was found by tracing what happened to band 3: F16 deferred the
xlsx (task 4) and superseded the prior-export merge (task 5) on the grounds that `git diff`
between snapshot folders replaces it. That holds for detecting change but not for carrying
decisions forward, and the two were conflated. Band 3 has had no home since. **There is no
writable surface in the workflow at all** — every extract carries a "regenerated on every
snapshot, any edit is lost" header, correctly.

**Decided (F20):** a writable per-chapter ledger at `05_thesis_writing/comment-ledger/chN.md`,
mirroring the existing split. A centralised hub was considered and rejected — it fights the
one-chapter-at-a-time working mode and inherits the same objections that killed the xlsx.

**Recorded:** F19 and F20 in `findings.md`; a "Ledger addendum" section at the end of
`task_plan.md` carrying the artifact-authority table, the entry format, the upsert contract
and tasks 18–21; frontmatter `focus_detail` rewritten for handover.

**Next, in order:**
1. Brian finishes the Word comment pass, Ch2 onward. **This is the gate** — 14 of ~150
   comments exist, so building against Ch1 alone only tests the mechanism.
2. Re-snapshot.
3. Task 18 (`--reconcile`), then 19 (`INDEX.md`), then 20 (seed Ch1), then 21 (document +
   extend `writing-surface-authority.md` to cover comments).

**Note:** still on `plan/p0042-scope-freeze` (carried from the previous session). Nothing
staged.

## 2026-09-05 15:40 — Session 4: re-ran the export; found and fixed a silent structural break

**Trigger:** Brian asked for a re-run against the current thesis. The source had changed
since 2026-09-01 (913,764 → 939,831 bytes) and comments had gone **14 → 167** — Enrico's
full review pass, which is the precondition F18 named for building the ledger.

**The first run produced a wrong snapshot that reported success.** 11 chapters instead of
17, ch1–ch6 missing, `Abstract` at 22,885 words. Discarded, not published.

**Cause (F19):** ch1–ch6 were restyled in Word to a custom `H1-Chapter`. The script matched
hardcoded style *names*, so those headings resolved to no level and their text merged into
the preceding section. The lone guard (`h1_count == 0`) passed, because 11 built-in
Heading 1s remained. **It tested for total failure; the failure was partial.**

**Fix:** `_heading_levels()` now resolves levels from `word/styles.xml` per document —
explicit `outlineLvl`, then the `basedOn` chain, then the name. Custom styles are picked up
with no code edit. Two traps confirm names were never sufficient: `TOCHeading` is
`basedOn="Heading1"` but sets `outlineLvl=9` (not a heading), and `H1-Tables` is
`basedOn="Caption"` (a caption).

**A hand-written list would not have been enough.** I first patched the style names by hand;
that pass still missed **ch6**. The resolver found 10 custom H1 paragraphs where the static
list found 5. The document knew; the script hadn't asked.

**Guards added (F20)** — `_sanity_warnings()` aborts on: no level-1 heading, duplicate
chapter slugs (F11's ch1/ch10 collision), or one section holding >40 % of the words (F19's
shape). Warns on: oversized front matter, empty chapters, unmapped chapters. Front matter
was registered in `CHAPTER_MAP` so that last warning stays meaningful. **The manifest now
records a style-id → level → count table**, so a future restyling is visible as a diff.

**Corrected numbers.** Ch6's **−1,911 drift (F15) was an artifact of this bug** — its text
sat in ch5. Task 14 is void. Real deltas: ch5 **+1,079** (not +5,348), ch6 **+258**. The
one genuine negative is **ch3 at −1,991**.

**Verified:** guards tested individually against synthetic inputs (all four fire); real
document runs clean with no warnings; 17 chapters, 167 comments across 6 chapter files.

**Delivered snapshot:** `docx-exported-snapshots/2026-09-05_15-54/`. The broken intermediate
runs were removed.

**Tooling:** hit the heredoc escape-collapse class again (issue #25) — this time `\b`
became a literal backspace (`\x08`) inside a regex, which would have silently matched
nothing. Caught by inspecting `repr()` of the written line rather than trusting the write.

**Still on `plan/p0042-scope-freeze`**, nothing committed.

**Next:** task 20 — reconcile the 167 comments into the F18 ledger, now that its
precondition is met.

## 2026-09-05 16:38 — Session 5: table rendering

**Trigger:** Brian asked how `.docx` tables convert to `.md`, and what happens to comments
anchored on table content. Both were broken; neither had been noticed.

**Tables.** `body.iter(w:p)` recurses into `w:tbl`, so all **28 tables** had been flattened
into loose cell values with row/column structure lost — every snapshot to date. Now walks
direct children and renders `w:tbl` as markdown pipe tables (F21).

**Table-anchored comments.** 4 of them (139, 168, 222, 256). Never lost, but quoted back as
run-together text (`RTD37930 ⚠️425895112,19344,449`) — unactionable. `_scan_ranges()` now
emits separators at cell/row boundaries.

**Separators are ASCII 31/30, not pipes** — the metrics table defines WMAPE as
`Σ|y−ŷ| / Σ|y|`, and a pipe separator split that formula apart. Rendered as ` | ` / ` || `
only at the end, with trimming done on placeholders so content pipes survive.

**Two ordering traps hit and fixed:** `\s+` matches chr(30)/chr(31) and ate the sentinels;
and trimming with `[ |]+$` stripped the closing pipe off `Σ|y|`.

**Also:** ch7–ch10 headings lost their `Chapter N -` prefix (same restyling as ch1–ch6). The
unmapped-chapter WARN from task 19 caught it — the guard doing its job on its first outing.
`CHAPTER_MAP` extended.

**Mid-session churn:** the source grew 939,831 → 946,614 bytes and comments went 167 → 204
while working. Enrico is editing live; treat any count as a point-in-time reading.

**Incident:** a heredoc-authored patch broke the script, and I ran `git checkout --` on it,
which discarded this session's uncommitted resolver + guards. Recovered in full from a
scratchpad backup taken moments earlier. **Nothing was lost, but the reflex was wrong** —
`git checkout --` on a file with uncommitted work from the current session is destructive.
Committing at the end of each working session would have made this a non-event.

**Verified:** unit cases for `_tidy_anchor`; 28 separator rows with 0 column mismatches; the
4 table anchors read correctly; clean run with no warnings.

**Delivered:** `docx-exported-snapshots/2026-09-05_16-38/` — 17 chapters, 28 tables,
204 comments over 7 chapter files.

**Still on `plan/p0042-scope-freeze`**, nothing committed.

## 2026-09-05 17:23 — Session 5 (cont.): verified snapshot, plan updated

**Re-ran the export** after the table work. Clean run, no warnings:
`docx-exported-snapshots/2026-09-05_17-23/` — 30,070 words, **17 chapters**, **28 tables**,
**217 comments over 8 chapter files**, sha `1419443b…`.

**Table handling confirmed dynamic, not patched per-table.** Verified three ways:
1. The 28 real tables span **18 distinct shapes** (2×3 up to 9×4), all from one code path.
2. Synthetic `.docx` files with shapes the thesis has never contained (4-col, **12-col**,
   a cell holding `S|y-yhat| / S|y|`) render correctly with no code change.
3. A synthetic comment spanning an unseen table quotes back as
   `Scenario | Model | WMAPE | Notes || C | LightGBM | S|y|/S|y| | best` — cells, rows and
   content-pipes all distinguished.

**Merged cells closed as out of scope (F22).** Brian confirmed they are not used; verified
`gridSpan: 0 / vMerge: 0`. Task 22 stays *deferred*, not *done* — the padding path is
unproven rather than proven-unnecessary.

**Document churn explained.** 167 → 204 → 217 comments inside ~90 minutes was Brian working
through the document alongside code changes and investigations, not instability. Every
snapshot is a point-in-time reading by design; that is what the timestamped folders are for.

**Comment distribution recorded as F23**, because it sets the order for task 20: **ch6 (48)**
and **ch4 (42)** carry 41 % of the load and are both results-bearing. **Ch8 has 4 and
ch9/ch10 have none — that is under-written, not agreed**, the same misreading F20 warned
about for absent drift rows.

**Drift baseline is now trustworthy** (post-F19). `ch3-methodology` at **−1,991** is the
only genuine negative; every other delta is the `.docx` outgrowing bullet drafts, which is
expected. Task 14 reframed from the void Ch6 figure onto ch3.

**Still on `plan/p0042-scope-freeze`, nothing committed** — now carrying two sessions of
uncommitted work on `thesis_snapshot.py` (heading resolver, sanity guards, table rendering),
which the near-miss earlier this session showed is a real exposure.

**Next:** task 20 — build the F18 ledger, ch6 and ch4 first.

---

## Session 2026-09-05 (b) — threading review (planning only, no code)

Reviewed the parallel session's work and the `2026-09-05_17-23` snapshot. **No code
written**; this session's output is F26–F28 and a revised ledger addendum.

**State found.** The other session hardened extraction substantially — heading levels
resolved from `styles.xml`, `_sanity_warnings()`, 28 tables rendered as markdown pipes. The
Word pass is complete: **217 comments, 8 chapters, 200 Brian / 17 Guest User, 27 replies**.
The ledger itself is not built; `comment-ledger/` does not exist yet.

**Numbering collision fixed.** Both sessions allocated F19/F20 and tasks 18–21. The ledger
set was renumbered (**F24/F25**, tasks **23–28**) because the hardening findings are already
cited by number elsewhere. A note was left at both sites.

**F26 — the substantive finding.** `read_docx()` parses `w15:paraIdParent` into
`parent_by_para` and then discards it, setting only a boolean `is_reply`. The extract knows
*that* a comment is a reply but not *what it replies to*, so c54/c55 and c56/c57/c58 render
as flat siblings when they are conversations. Since a thread's conclusion lives in its last
message, a per-comment ledger files the answer separately from the question. Enrico's 17
comments are almost entirely replies — per-comment `owner` would be wrong the moment it was
written. **The ledger's unit must be the thread.** Task 23 now blocks the rest.

**F27 — tabular, reconsidered at 217.** One of F16's original reasons has expired (14 was a
15× underestimate) and real aggregation needs now exist. But the framing was wrong: a status
roll-up and a decision record are two artifacts. Adopted the table as a **generated view**
(`INDEX.md`, upgraded from "counts" to a per-thread status table) and rejected it as
storage. It must carry no `resolution` prose.

**F28 — `resolved` is live.** Contradicts F12's prediction. `word_resolved` is kept as a
field distinct from ledger `status`: *stopped arguing* ≠ *thesis changed*.

**Sequencing corrected.** The old "finish the Word pass" gate has cleared. Seeding starts at
**ch6 (48)** and **ch4 (42)** — 41 % of the load, both results-bearing — explicitly **not**
ch1, whose premise-level comments depend on results not yet in.

**Next (for the Word-workflow session):** task 23 → 24 → 25 → 26 → 27.

## 2026-09-05 17:45 — Session 5 (cont.): read and verified the parallel session's cross-check

**Read** F24–F28 and tasks 23–29, written by a parallel session against snapshot
`2026-09-05_17-23`. Numbering is clean — that session renumbered its own findings to F24/F25
on discovering F19–F23 were already taken, and its tasks 23–28 depend correctly on 18–22.

**Verified every claim against the code and the snapshot rather than accepting it (F29).**
Four hold, one does not:

- **F24 (band 3 homeless), F25 (per-chapter ledger), F27 (table as generated view)** — hold.
- **F26 (threads are the unit of triage)** — holds, and it is a real defect in my code:
  `parent_by_para[pid]` is populated at line 304 and then used only as a membership test at
  309, so the parent id is thrown away. The extract knows a comment *is* a reply but not
  *what it answers*. Confirmed 27 replies, 200 Brian / 17 Enrico.
  - **One correction:** F26 implies the `reply` marker is missing from the output. It is
    not — all 27 render as `` `reply` ``. Only the parent id is missing. (My own first grep
    said zero replies; that was a wrong pattern, not a bug.)
- **F28 (`resolved` is live data)** — **contradicted.** Measured from
  `commentsExtended.xml`: `done: 0` across all 217 comments. The `w15:done` parse and the
  `✔` renderer both exist but have **never fired on real data**; presence of the code was
  mistaken for presence of the data. **F12's original prediction still stands** — deletion,
  not Resolve, is how these two authors settle a comment. Added **task 29** so the reconcile
  contract is not built on a signal that does not exist.

**Net effect on sequencing:** task 20 (reconcile) is now correctly blocked by **task 23**
(carry `parent_comment_id` / `thread_id` / `reply_count` through the extract). Seeding a
per-comment ledger before threading exists would file ~190 threads as 217 items and assign
Enrico 17 open items that are actually his answers to Brian's questions.

**No code changed this session.** The snapshot at 17:23 stands as delivered.

## 2026-09-05 17:44 — Session 5 (cont.): threading implemented (tasks 23, 24, 26)

**Task 23 — threading through the extract.** `parent_by_para` is no longer discarded. A
`paraId -> comment id` map resolves `w15:paraIdParent` to the comment it answers, and
`parent_id`, `thread_id`, `reply_count` and `thread_pos` now reach the extract — the band 2
fields specified long ago and dropped when the xlsx went.

Chain walk guards against cycles and orphans; a reply whose parent was deleted roots itself
rather than vanishing. **0 orphans measured.** Word threads turn out to be flat (both
replies in the largest thread point at the root, not at each other), but the walk handles
arbitrary depth regardless.

**Task 24 — threads render as threads.** One `##` per thread, replies nested as `###`.
**All 223 anchors preserved** (196 roots + 27 replies), so no existing `#cNN` link breaks.
The chapter split is now thread-aware: a thread is filed under its *root's* chapter, so a
reply anchored elsewhere travels with its conversation.

**Task 26 — `comments/INDEX.md`.** The generated table F27 asked for: thread · chapter ·
section · opened by · replies · **last voice** · gist. No `resolution` prose, by design.
`last voice` is the queue — Enrico last means it is waiting on Brian. All **196 links
verified** to resolve to a real anchor (0 broken).

**The numbers confirm F26:** 223 comments = **196 threads**. But the distribution is the
more useful finding (F30): ch1 (33→14) and ch2 (26→18) are genuinely two-sided, while
**ch3–ch8 are 164 comments in 164 threads — 1:1, no replies at all.** Enrico's pass has not
reached them. Reading that as consensus would be the same mistake F23 flagged for ch8/9/10.

**Delivered:** `docx-exported-snapshots/2026-09-05_17-44/` — 17 chapters, 28 tables,
223 comments in 196 threads, clean run.

**Next:** task 25 (`--reconcile` into the writable ledger), which is now unblocked. Task 29's
constraint stands: do not key the contract on Word-resolved status — still `done: 0`.

**Still on `plan/p0042-scope-freeze`, nothing committed.**

## 2026-09-05 17:57 — Session 5 (cont.): bold/italic preserved (task 30)

**Trigger:** Brian asked whether bolding could be represented in the exported `.md`.

**It could, and it was being thrown away** — 458 bold and 153 italic runs. `_text()`
flattened to `w:t` and dropped every run property. Now walks runs and emits `**`/`*`/`***`
(F32). Result: 325 bold spans, 0 stray markers, **0 unbalanced lines across 9,359**.

**Four traps handled, each caught by testing rather than by reasoning about the format:**
headings are bold *by style definition* (13 also carry an explicit `<w:b>`, which would have
produced `## **Chapter 3**`); `<w:b w:val="0"/>` means OFF; markers must hug their text;
adjacent same-format runs produce `**a****b**` and the seam must be closed **without** a
naive double-replace, which ate legitimate pairs on the first attempt.

**A fifth trap surfaced only from validating real output:** a bold superscript footnote
marker inside an italic quotation split it as `...variables.**1* *This element...`.
Superscripts now carry no emphasis. It was the *only* unbalanced line in the document —
a balance check over every output line is what found it, not reading the code.

**Word counts and drift are unaffected** (`_words` splits on whitespace, so `**word**` is
still one word); drift figures byte-identical to 17:44. `_plain()` strips markers for index
gists, where fixed-width truncation could cut through a `**`.

**Left unconverted, deliberately:** colour (69 runs) and highlight (28) have no portable
markdown; strikethrough (4) did not justify the tilde-mangling risk.

**Delivered:** `docx-exported-snapshots/2026-09-05_17-57/` — 237 comments in 210 threads,
17 chapters, 28 tables.

**Still on `plan/p0042-scope-freeze`, nothing committed.** Now four sessions of uncommitted
work on `thesis_snapshot.py`.

## 2026-09-05 18:04 — Session 5 (cont.): `--label`, and the identity finding that reshapes the ledger

**`--label` shipped (task 31).** `--label "First Complete Audit"` →
`2026-09-05_18-04_first-complete-audit`, and the label is written into `MANIFEST.md` so the
intent survives inside the snapshot, not only in the folder name. Milestone runs are now
distinguishable from routine and test runs.

**Then the important part.** Before designing the tracking system Brian asked for, I checked
whether a comment even *has* a stable identity across snapshots. **It does not, under the id
we have been using** (F33):

```
17-44 -> 18-04 (20 minutes apart)
  shared w:id values: 122  --  of which 120 now hold a DIFFERENT comment
  all 223 w:id renumbered;  all 223 w14:paraId held
```

Comment `16` was Enrico's exogenous-variable reply; it is now Brian's enrichment objection.
**A ledger keyed on `C22` would silently misfile decisions** — still resolving to *a*
comment, just the wrong one. The F25 schema had exactly this defect, and so did the
`thread_id` shipped earlier today.

**Fixed (task 32):** `para_id` and `thread_para_id` now carried through the extract. Proof:
keyed on paraId, the pair reports **196 threads carried forward, 16 new, 0 gone** — what
actually happened. Keyed on `w:id` it reports 81 stable, which is noise.

**Design written up as F34** — the claim ledger, and what was/is/should actually requires:
- **was** = anchor text frozen at the snapshot where the thread opened (written once)
- **is** = anchor text in the current snapshot (rewritten every reconcile)
- **should** = the thread's conclusion + linked plans (**human-written**)

`was != is` means the prose moved under the comment — Brian's "quoted sections change from
iteration to iteration". Reconcile marks it `DRIFTED` rather than guessing whether the
objection still stands.

**Open question recorded as task 35:** `w14:paraId` is a Microsoft extension. Untested
whether it survives a round-trip through Google Docs or Word Online. `author+date+text` is
the fallback at 93 % coverage.

**Delivered:** `2026-09-05_18-04_first-complete-audit/` — 239 comments in 212 threads.

**Next:** task 33, the ledger itself. **Still nothing committed** — five sessions of work on
`thesis_snapshot.py` now sitting on `plan/p0042-scope-freeze`.

## 2026-09-05 18:13 — Session 5 (cont.): resolved comments confirmed working; italics verified

**Brian resolved a test comment in Word.** It round-trips end-to-end:

```
commentEx: 239 | done: 1 | paraId 1DE68C76
comments.md -> ## [5] Brian Rohde -- Abstract  `RESOLVED`   (checkmark in the index)
```

**This settles F12 / F28 / F29, and all three were partly wrong (F35).** F12's prediction
(they will delete, not resolve) was a guess now overtaken. F28 described a real capability
but cited it as observed data when `done` was still 0. **My F29 measured correctly and then
over-concluded** — `done: 0` meant *untested*, and I read it as *unused*. A zero only
distinguishes "absent" from "impossible" once something has been tried.

**Brian's preference now governs:** resolve over delete, because the comment disappears from
view while its history survives. **Task 29's constraint is withdrawn**; the reconcile may key
on `resolved`, and `GONE (verify)` drops to the anomalous case. Word-resolved and ledger
`DONE` stay distinct (F28's good distinction survives) — the gap between them is the queue.

**Task 35 closed** as not applicable: Brian confirmed all work finishes in desktop Word, so
the `paraId` round-trip question cannot arise.

**Italics verified (F36).** 311 bold, 129 italic, 2 bold+italic, all balanced; italic already
carries identifiers like `product_id`. **But the document does not yet apply the convention
Brian described** — `XGBoost` is italic in 1 of 51 occurrences, `tracemalloc` and `Prophet`
in 0. The exporter is faithful, not normative; adopting the convention is a Word formatting
pass, not a script change. **Recommended a character style rather than direct italics** —
one global change, survives restyling, and lets the exporter tell "italic because term" from
"italic because quotation". Logged as task 37, awaiting Brian's decision.

**Delivered:** `docx-exported-snapshots/2026-09-05_18-13/` — 239 comments, 212 threads,
1 resolved.

## 2026-09-05 18:51 — Session 5 (cont.): complete review pass exported; Term style + keyword taxonomy

**Brian finished the whole-thesis comment pass.** Exported as
`2026-09-05_18-51_complete-review-pass/` — **268 comments in 241 threads over 12 chapters**,
30,082 words, 28 tables, 1 resolved.

**`Term` character style found and wired in (F37).** Brian applied it to `CSD` (x2),
`danskvand`, `energidrikke`, `RTD`. **It was invisible to the exporter** — the style supplies
the italic, so those runs carry no direct `<w:i>` and emphasis detection (which read direct
run properties only) skipped them entirely. Now reads `w:rStyle` too. Word created it as a
*linked* style, so the character half is `TermChar`; both names accepted.

Terms render as `` `danskvand` `` rather than italics — the F36 distinction realised: a term
is now unambiguous, and `*...*` stays a quotation. **Applying `Term` in Word is now the whole
workflow**; no script change per term.

**Keyword vocabulary parsed (F38).** Brian's ALL-CAPS prefixes are consistent enough to be
machine-read: **201 of 268 comments tagged**. `KEYWORDS` handles variants including the
`METACOMMMENT` typo; matched only in the first 120 chars, because the same words appear in
ordinary prose later.

Surfaced in the per-chapter index, the comment header, and a new **Work type by chapter**
matrix in `INDEX.md`. That matrix turns the review into a plan:

- **VERIFY 111** (ch6: 39, ch4: 19) — claims to re-check against code. The repository work.
- **PROSE 71** (ch6: 23) — writing, Brian's.
- **OUTDATED 34 + INCORRECT 11** (ch8/ch4/ch3) — the factual-correction queue.
- **WATERMARK 6**, mostly ch3 — localised AI-tone problem, not diffuse.

**The three-way split for the ledger fell out of this data** rather than being designed:
repo-checkable (VERIFY/OUTDATED/INCORRECT) → Claude; SOURCE → NotebookLM/Zotero;
PROSE/ACADEMIC/WATERMARK → human. Recorded as task 40.

**From Brian's review notes, recorded but not actioned (task 39):** cross-chapter repetition
and weak handovers. The per-chapter export scopes *away* from that problem, so it needs its
own pass.

**Also from those notes, now answered:** "The current word export workflow does not transfer
any bolding into the converted .md chapters" — it does as of this session (F32/F36/F37):
311 bold, 129 italic, 5 terms.

## 2026-09-05 19:10 — Session 5 (cont.): PROSE/VERIFY coupling measured; working order recommended

**Brian asked how to restructure the export and how to start working the comments.** Checked
the data before answering.

**PROSE and VERIFY are one pass (F39).** Of 71 PROSE threads, **56 also carry VERIFY** and
only **6 are PROSE alone**. Splitting them into separate queues would double-handle 56
threads. Brian's instinct — "most of the time it is coupled with a verification pass, which
you would need to do in the repository anyways" — is exactly what the tags say.

**No section-level batching exists.** 126 PROSE/VERIFY threads spread over **99 sections**,
median one each. The working unit is the **chapter**, which the export already produces.

**Comments are often bare tags.** Thread 237 reads, in full, `VERIFY, SOURCES, PROSE`. The
instruction lives in Brian's keyword notes; **the anchored passage is the whole work item**.
That made the 400-char anchor cap a real defect — 78 of 268 cut mid-passage. **Raised to
2,000 with head+tail excerpting: 265 of 268 now complete** (task 41), the other 3 state how
much was elided. One anchor is 56k characters — a whole section selected.

**Recommended order (F40):** commit a baseline, then **ch6 first** (48 threads, 39 VERIFY,
23 PROSE, 18 SOURCE — the densest coupled work, and results-bearing so errors are wrong
*findings*), then ch4, ch3 (4 of 6 WATERMARK tags), ch7, ch8, ch5, ch2, ch1.

**On the de-watermark pipeline:** Brian's order (draft → strip → humanise) is right, and for
a stronger reason than efficiency — a human rewrite *after* stripping reintroduces text that
must be re-stripped, so it is the only stable order. **Flagged plainly:** the tool removes
provenance marks, not AI voice, and its own docs call detector evasion best-effort. The
human pass is what ships; planning as if the tool were sufficient would leave WATERMARK prose
in the submission.

**Task 39 re-sequenced:** the cross-chapter duplication problem from Brian's notes is
*entrenched* by a chapter-at-a-time loop. Right moment is after ch6+ch4, before the rest are
rewritten around text that may move.

**Delivered:** `2026-09-05_19-10_complete-review-pass/` — 277 comments, 250 threads, full
anchors.

**Still nothing committed.** This is now the blocking item: the baseline for every future
`was → is` comparison is an uncommitted folder.

## 2026-09-05 19:29 — Session 5 (cont.): `sections/` tree + writing-notes folded in

**`sections/` built to Brian's design (F41, task 44).** The heading tree mirrored as nested
folders: an H2 with H3 children becomes a folder, an H2 without becomes a file.
**154 leaf files** from 63 leaf-H2 + 70 H3 + preambles. `chapters/` is untouched — this is
in addition, as Brian asked.

The document is well-formed for it: 17 H1 / 78 H2 / 70 H3 with **zero skipped levels**.

**Why it matters, in one number:** median H3 body is **98 words** vs 3,000–6,000 for a
chapter file. "How did 4.1.1 change between two snapshots" is now a 98-word diff, and a
Claude session can load one section instead of a whole chapter.

**One flaw caught by actually running the diff:** the first version listed comment ids per
section, which made *every* section file diff on *every* snapshot, because `w:id` is
renumbered on each insertion (F33). It destroyed precisely the signal the tree exists to
give. Section files now carry **counts and work-type tags** (stable) instead. After the fix,
67 of 154 sections differ between the 17:23 and 19:10 snapshots — concentrated in front
matter and abstract, where the editing actually happened; ch6 results are byte-identical.

**Brian corrected my framing of was/is.** He does not want deterministic comparison — he
wants a Claude session to be able to read a past section beside the current one. That is
weaker and more useful, and `sections/` + `diff` satisfies it. **Consequence: the ledger's
`was`/`is` become snapshot pointers, not stored copies of text** (task 46) — which makes
task 33 simpler than designed.

**`writing-notes/` inspected and promoted to a first-class input (F42, task 45).** Eight
files, ~2,900 lines, each with `applies-to` frontmatter mapping to chapters. The staleness
audit independently confirms the ch6-first call: *"THE CRITICAL FINDING: ch6 passes the
checker and is wrong throughout"* (42 ERROR, 6 CHECK, 2026-08-22).

**But they declare their own staleness** — `sample-size-and-tool-interface-rationale` says
its counts are *"superseded by the 2026-08-12 re-pull"*. Precedence for the loop is
**repo artefacts > writing-notes > thesis prose**: use the notes to find the argument fast,
use the code to confirm it still holds.

**On the bare tags:** Brian confirmed these are deliberate — a lone `PROSE` means "bullets I
agree with, or too short", and extra text appears only where more specification was needed.
So an untagged-but-short comment is not missing information; the tag *is* the instruction.

**Delivered:** `2026-09-05_19-29_complete-review-pass/` — 281 comments, 254 threads,
154 section files.

## 2026-09-05 19:52 — Session 5 (cont.): final export shape; baseline regenerated

**Brian moved `sections/` under `chapters/` by hand** and asked whether comments should mirror
it. Both adopted (F43). His reasoning is right: it is chapter content divided by section, so
it belongs under `chapters/`.

**Final shape — three levels, the lower two section-divided:**

| level | prose | comments |
|---|---|---|
| whole document | `thesis_full.md` | `comments.md` (281) |
| chapter | `chapters/chN.md` (17) | `comments/chN.md` (13) |
| leaf section | `chapters/sections/…` (154) | `comments/sections/…` (138) |

**Why the mirror was worth building:** before it, a section file said *"4 comments — VERIFY,
TABLE-REFERENCE, SOURCE, METACOMMENT"* and sent the reader to a **48-thread** chapter file to
find them. Now the same relative path holds prose on one side and objections on the other,
each pointing at the other.

**Both trees come from one `_section_tree()`**, so they cannot drift. Verified: 0 comment
files without a prose twin; **280 of 281 comments land in a leaf section** (the 1 remaining
is anchored at chapter level and correctly stays there). Deliberate asymmetry: all 154 prose
leaves are written, only the 138 comment-bearing ones — 154 near-empty comment files would
bury the ones that matter.

**Matching is on the full heading path**, not the last heading: "Results" appears under
several chapters and a loose match would file a ch6 objection under ch8.

**Verification precedence recorded as a rule (F44, task 49)** at Brian's instruction:
**script code > generated artefacts > writing-notes > thesis prose**. Nothing at levels 3–4
is evidence. A VERIFY thread is closed by the code path or artefact that produces the number
— not by finding the claim restated in a note. The staleness audit is the cautionary case:
*"ch6 passes the checker and is wrong throughout"*.

**Keyword bareness generalised (F45):** a bare `VERIFY` or `OUTDATED` is a complete
instruction for *any* tag, not just PROSE. **The keyword dictionary needs to live in the repo**
(task 47) — it is currently only in Brian's message, and it is workflow, not background.
Note also that the 40 untagged threads are the ones where prose carries the instruction; they
need reading, not classification.

**Old snapshots deleted** at Brian's request; the tree was regenerated so the new shape is in
it. **Baseline: `2026-09-05_19-52_complete-review-pass/`** — 30,119 words, 17 chapters,
281 comments, 254 threads, 154 prose sections, 138 comment sections, 28 tables.

This is the "was" the chapter work starts from.

## 2026-09-05 20:05 — Session 5 (cont.): keyword dictionary committed (task 47)

Written to `05_thesis_writing/writing-notes/review_comment_keywords.md` — Brian asked for it
by name. Placed in `writing-notes/` alongside the other `applies-to`-tagged references;
`05_thesis_writing/` itself holds only folders.

Carries Brian's definitions verbatim, the measured distribution at the baseline, the
three-way split of who resolves what, the F44 precedence rule, and the parsing rules with
their reasons.

**Checked the numbers before writing them:** 254 threads / 214 tagged / 40 untagged;
72 PROSE of which 56 also VERIFY and 6 PROSE-only; all 17 parsed keys documented. The file
also states the maintenance rule — a tag the script parses but the dictionary omits is a tag
a future session cannot act on, so both halves must be updated together.

**The export is now self-describing**: snapshot README explains the shape, this file explains
the vocabulary, `INDEX.md` shows the distribution.

**Next:** ch6 — 48 threads, 39 VERIFY, 23 PROSE, 18 SOURCE, and a writing-note already
stating it "passes the checker and is wrong throughout".

## Session — 2026-09-05, second session (assessment only, no workflow code)

Read `2026-09-05_19-52_complete-review-pass` cold and audited the comment corpus. No
changes to `thesis_snapshot.py` or the export — this session's writing went to P0045 and
P0046.

- Recorded **F47** and a task_plan section: the review pass is complete (281 comments /
  254 threads / 13 chapters, up from 217 / ~190 / 8).
- **49% of threads are bare tag stamps.** Corroborates F39's account of why; adds the
  ledger consequence — seed from the ~130 substantive threads, sweep-list the rest.
- All 17 reply threads are in ch1-ch2; chapters 3-10 have had one reader.
- 1 word-resolved thread in 281, and it is the test comment.
- Four cross-chapter arguments identified and ranked by whether the answer exists today.
  LLM-as-judge (ch3 x9, ch7 x7, ch8 x10, ch9, ch10) is unblocked and highest-value.
- Split the holiday-API enrichment argument out to **P0046** — it is an experiment
  change, not a prose fix.

Arrived at "ch6 first" and "bare tags are the norm" independently of F39/F40, which were
written in the parallel session and not visible at the time. Treated as corroboration;
only the non-overlapping half was appended.
