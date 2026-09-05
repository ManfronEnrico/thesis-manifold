---
pid: P0043
created: 2026-09-01 15:27:00
updated: 2026-09-05 20:05:00
status: in_progress
focus_detail: "THREAD HANDOVER 2026-09-05 (findings F26-F28; the 'Ledger addendum' section at the END of task_plan.md is the spec). WORD PASS IS DONE -- snapshot 2026-09-05_17-23 has 217 comments over 8 chapters, 200 Brian / 17 Guest User (Enrico), 27 replies. Extraction is hardened (styles.xml heading levels, sanity guards, markdown tables). || THE FINDING THIS SESSION (F26): read_docx() parses w15:paraIdParent into parent_by_para then DISCARDS it, keeping only a boolean is_reply. The extract knows THAT a comment is a reply, not WHAT it replies to. So c54/c55 and c56/c57/c58 render as flat siblings when they are conversations, and a thread's CONCLUSION lives in its last message -- a per-comment ledger files the answer separately from the question. ~190 threads, not 217 items. Enrico's 17 are almost all replies (already-delivered answers), so per-comment `owner` would be wrong on arrival. || DECISION: the ledger's unit is the THREAD, keyed by root comment id, replies nested inside. TASK 23 (emit parent_comment_id + thread_id + reply_count) BLOCKS EVERYTHING -- seeding per-comment and re-keying later means re-filing every decision by hand. || TABULAR, settled (F27): adopt the table as a GENERATED VIEW (INDEX.md, task 26 -- per-thread status table with a gist, NO resolution prose), reject it as storage. Ledger stays markdown: must read beside the prose, and threads are dialogue that no cell holds. || F28: w15:done is live after all, contra F12 -- keep `word_resolved` as a field distinct from ledger `status` (stopped arguing != thesis changed). || TASK/FINDING NUMBERS 18-22 and F19-F23 were double-allocated by two parallel sessions; the ledger set was renumbered to 23-28 and F24/F25. || NEXT: task 23, then 24-26, then seed ch6 (48) and ch4 (42) -- 41% of load, results-bearing. NOT ch1: premise-level, blocked on results."

---

# P0043 — Word comment audit workflow (docx → Excel)

## Why this plan exists

The thesis is written in this repo but reviewed in a **shared Word document** outside it.
**Brian and Enrico are the only two people in this loop** (F12) — there is no supervisor or
external reviewer. Comments are the two authors talking to each other in a 114-page stitched
document. Today those are read one-by-one in Word, which does not scale and leaves no record
of what was addressed, by whom, or when.

The goal is a **repeatable export** turning every comment into one spreadsheet row with
enough metadata to triage it — and, critically, a **round-trip** so that triage decisions
made in round *N* survive into the round *N+1* export instead of being retyped.

This is a **tooling plan**, not thesis content. It produces a script and a documented
workflow, not prose.

---

## Ground truth established 2026-09-01 (read before coding)

These were verified on disk this session, not assumed.

| Fact | Evidence | Consequence |
|---|---|---|
| **No repo `.docx` carries comments** | All 6 files in `05_thesis_writing/sections-final/` have a `word/comments.xml` of exactly **625 bytes** — an empty `<w:comments/>` stub with namespace declarations only. | The extractor cannot be validated against these. Task 1 must obtain the real review copy. |
| **No `commentsExtended.xml` in any repo docx** | `unzip -l` on all 6 shows only `word/comments.xml`. | These are generator output (pandoc-style), not Word-round-tripped files. Resolved-status parsing is untestable until a real reviewed file exists. |
| **`.venv` is the interpreter** | `Z:\_dev-ssd\thesis-manifold\.venv\Scripts\python.exe` | Install deps there, not into system Python. |
| **`python-docx`, `openpyxl`, `lxml` all absent** | `ModuleNotFoundError` on all three. `pandas 3.0.1` present. | Task 2 installs them and adds them to `requirements.txt`. |
| **`05_thesis_writing/analysis/`** exists with `figures/`, `outputs/`, `figures_agentic/`, `outputs_agentic/` | `ls` | Audits get a new sibling `comment-audits/`, not a new tier. |

---

## The engine decision (settled 2026-09-01)

The attached guide's VBA macro was evaluated and rejected as the *primary* engine.

**What VBA cannot do**, and why it matters here:

- **Resolved / open status** — not reliably exposed by the Word object model. `Comment.Done`
  exists in recent builds but is inconsistent across versions and absent for older files.
  It lives in `word/commentsExtended.xml` as `w15:done`.
- **Reply threading** — VBA flattens a thread into sibling comments. The parent/child link
  is `w15:paraIdParent` in `commentsExtended.xml`.
- **Headless execution** — VBA needs the document open in Word on one machine. It cannot
  run from this repo, cannot be diffed, cannot be re-run over a batch of chapters.

**What VBA has that OOXML does not:** *page number*. Word computes pagination at layout
time; it is not stored in the file. This is a real loss and the reason for the fallback macro.

**Decision:** Python OOXML reader is canonical. A thin VBA macro is kept for the one case
where page numbers are wanted and the doc is already open in Word; its output is a
two-column `comment_id → page` CSV that the Python tool can left-join. Do not grow the VBA
beyond that — every other field belongs in Python.

---

## Column schema

Split into three bands. Bands 1–2 are machine-written on every export and must never be
hand-edited; band 3 is yours and is preserved across re-exports.

### Band 1 — identity and location

| Column | Source | Notes |
|---|---|---|
| `comment_id` | `w:comment/@w:id` | Join key. Stable within a file; **not** stable if the reviewer re-creates a comment. |
| `para_id` | `w:p/@w14:paraId` inside the comment | More stable than `comment_id`; used as secondary join key. |
| `chapter` | source filename | Which chapter the export came from. |
| `heading_path` | nearest preceding `w:pStyle` Heading 1/2/3 before the anchor | e.g. `3 Methodology > 3.2 Research design`. **This replaces page number** as the primary locator and is more robust — it survives repagination. |
| `paragraph_index` | ordinal of the anchored paragraph in `document.xml` | Gives a sortable within-chapter order. |
| `page` | VBA fallback CSV only | Blank unless the macro was run. |
| `snapshot_id` | the dated snapshot folder this row came from | *(added 2026-09-01, F13)* Makes each audit self-describing and lets rows from different snapshots be compared without ambiguity. |

### Band 2 — comment content

| Column | Source | Notes |
|---|---|---|
| `author` | `w:comment/@w:author` | |
| `initials` | `w:comment/@w:initials` | |
| `date` | `w:comment/@w:date` | ISO 8601, kept as a real datetime in Excel so it sorts. |
| `comment_text` | concatenated `w:t` in the comment | |
| `anchored_text` | `document.xml` runs between `commentRangeStart` and `commentRangeEnd` | **The single most valuable column, and the guide omits it.** What the reviewer was pointing at. |
| `anchor_context` | ~200 chars either side of the anchor | For when `anchored_text` is a single word and meaningless alone. |
| `is_reply` | `w15:paraIdParent` present | |
| `parent_comment_id` | resolved from `w15:paraIdParent` | Lets the sheet be grouped by thread. |
| `thread_id` | root comment of the thread | Group/filter key. |
| `reply_count` | derived | On the root row only. |
| `resolved` | `w15:done` in `commentsExtended.xml` | `TRUE`/`FALSE`. Unavailable via VBA. |
| `comment_length_chars` | derived | Cheap proxy for effort; long comments are usually substantive, one-liners usually typos. |

### Band 3 — triage (yours, preserved across rounds)

| Column | Values | Notes |
|---|---|---|
| `triage_status` | `NEW` / `ACCEPTED` / `REJECTED` / `DONE` / `DEFERRED` / `NEEDS-DISCUSSION` | Data-validated dropdown. |
| `owner` | `Brian` / `Enrico` | Who must act. Distinct from `author`, who raised it (F12) — this is the ask/answer protocol for a two-person team. |
| `action_taken` | free text | What you actually changed. |
| `commit_ref` | free text | Git SHA or branch where the fix landed — this is the link back into the repo and the reason the workflow is worth building. |
| `round_first_seen` | auto | Which export round the comment first appeared in. |
| `delta` | auto: `NEW` / `UNCHANGED` / `CHANGED` / `GONE` | Computed against the previous export. `CHANGED` means same id, different text — i.e. the reviewer edited their comment. |

### Additional metrics recommended beyond the guide

Answering the question directly — the guide gives page/text/author/date. Worth adding
beyond those, in rough order of value:

1. **`anchored_text`** — highest value by far; a comment without its referent is unusable.
2. **`heading_path`** — better than page number, survives edits, groups by thesis section.
3. **`resolved`** — lets a round's export filter to open items only.
4. **`thread_id` / `parent_comment_id` / `reply_count`** — Enrico's comment plus your reply plus his counter-reply is *one* issue, not three rows to triage.
5. **`commit_ref`** — closes the loop between the review document and this repo.
6. **`delta`** — tells you what is actually new since last round; this is what makes round *N+1* fast.
7. **`comment_length_chars`** — cheap triage signal for sorting.

Deliberately **not** included: sentiment/priority scoring inferred from comment text. It
would be a guess presented as data on your co-author's words. Priority is a human call and
belongs in `triage_status`.

---

## Where the authoritative document lives

Settled 2026-09-01 — see findings F9, F10, F11. Each artifact gets exactly one job, which
is what removes the current three-hand-edited-versions ambiguity.

| Artifact | Granularity | Authoritative for | Hand-edited? |
|---|---|---|---|
| `sections-drafts/*.md` | chapter | live working state — bullets, results, anything a re-run changes | **yes** |
| stitched `.docx` (OneDrive) | whole thesis | prose as submitted; the review/comment surface | yes, in Word |
| `sections-final/*.docx` | chapter | nothing — derived | **no** |
| dated snapshot + extracted `.md` | both | the diffable record | no — script output |

**Git must not be hosted inside OneDrive** (F9): tooling issue #1 already documents
OneDrive sync races on this project, and git cannot diff a `.docx` regardless. Snapshot
into this repo instead; the extracted `.md` is what carries a readable diff.

---

### The snapshot contract (F13, adopted 2026-09-01)

Brian's proposed flow — shared `.docx` → snapshot of **comment and prose state together** →
per-chapter `.md` split → diff against the WIP drafts — is adopted. The key refinement over
the earlier wording: comments and prose are captured in **one operation**, because a comment
is only interpretable against the prose it was anchored to *at that moment*, and F5's walk
already emits both from a single parse.

One snapshot = one folder = one self-consistent checkpoint:

```
05_thesis_writing/docx-exported-snapshots/YYYY-MM-DD_HH-mm/
  thesis_full.docx          <- byte copy of the OneDrive file  (GITIGNORED)
  thesis_full.md            <- extracted prose, whole document
  chapters/ch3-methodology.md   <- Heading-1 split, READ-ONLY
  comments.xlsx             <- the audit, band 3 merged from the previous snapshot
  comments.csv              <- same rows, plain text, so git diffs the comment stream
  manifest.json             <- source path, mtime, sha256, counts, heading map used
```

**Gitignore the `.docx`.** The `.md` is the diffable artifact; the manifest's sha256
preserves provenance without committing 114 pages of binary per snapshot.

**Normalise before diffing.** The WIP `.md` drafts carry bullets, code fences and markdown
the Word document never had (F7: Ch2 −1,316 words). A raw line diff will be almost entirely
formatting noise on the first run. Strip markdown, collapse whitespace, split to one
sentence per line, then compare **sentences**. Skipping this is the most likely way the
tool gets built and then abandoned.

**The snapshot `.md` are read-only.** Write a `DO-NOT-EDIT` header into each. Editing a
snapshot instead of the source is how a fourth version appears (F10).

---

## Tasks

| # | Task | Depends on | Status |
|---|---|---|---|
| 1 | ~~Establish the path to the real reviewed `.docx`~~ | — | **DONE 2026-09-01** (F12/F14). OneDrive `MSc. Data Science - 175888 and 176171 - Master Thesis.docx`: **14 comments**, `commentsExtended.xml` **present** (3,429 B), so resolved-status is now testable |
| 2 | ~~Install `openpyxl`~~ | — | **DROPPED 2026-09-01** (F16). With the xlsx writer deferred, the entire pipeline is stdlib-only — no dependency install is on the critical path at all. |
| 3 | Write `utility_scripts/scripts/word_comment_audit.py` — OOXML extractor, bands 1–2. **Start from `prototype_docx_comments.py`** (F5): comment_id/author/date/comment_text/anchored_text/paragraph_index already work. Remaining: `heading_path`, `commentsExtended.xml` (`w15:done`, `w15:paraIdParent`), `anchor_context` | — | pending |
| 4 | ~~xlsx writer~~ | 3 | **DEFERRED 2026-09-01** (F16). `.md` wins on both stated goals: chapter-iteration context reads better beside the prose, and **NotebookLM ingests text, not `.xlsx`**. Revisit at ~50+ comments with both authors active. |
| 5 | ~~Prior-export merge for band 3~~ | 4 | **SUPERSEDED 2026-09-01** (F16). With `.md` output the cross-snapshot delta is `git diff` between dated folders — no merge routine to write. |
| 6 | Write the thin VBA fallback macro (page numbers only) + `--page-map` join flag | 3 | pending |
| 7 | Validate end-to-end against the real reviewed document | 5 | **unblocked** — expected shape already extracted to `docx-exported-snapshots/2026-09-01_16-24/comments.md` (F14) |
| 8 | Document the workflow in `user-docs/integration/`; consider a `/comment-audit` skill | 7 | pending |
| 9 | *(added 2026-09-01)* Sentence-level drift report: snapshot `chapters/*.md` vs. `sections-drafts/*.md`, **normalised first** (strip markdown, one sentence per line) or the output is unreadable noise | 3, 11 | pending |
| 10 | Snapshot script — one operation capturing **prose and comments together** into `docx-exported-snapshots/YYYY-MM-DD_HH-mm/`, with `manifest.json` (sha256 + counts) and the `.docx` gitignored (F9, F13) | 3 | **partial** — `thesis_snapshot.py` built, committed and run (F12): copy-then-read, comments + chapters + drift table, `.docx` gitignored. **`HH-mm` folder stamp DONE 2026-09-01** (F17), and the folder renamed `snapshots/` → `docx-exported-snapshots/`. **Still to add:** sha256 in the manifest. |
| 11 | *(added 2026-09-01)* Extend the snapshot to **split on Heading-1 into per-chapter read-only `.md`** (F11). Shares the Heading-scan with task 3; needs an explicit heading→filename map, a `DO-NOT-EDIT` header, and must fail loudly if no headings match | 3, 10 | **partial** — 17 sections split cleanly, aborts on zero Heading-1. **Still to add:** the `DO-NOT-EDIT` header |
| 15 | **Split `comments.md` per chapter** into `comments/chN.md`, sharing the slug map so it pairs with `chapters/chN.md` | 11 | **DONE 2026-09-01** (F16) |
| 16 | Index table per comments file (id · section · opening line) + stable `<a id="cNN">` anchors | 15 | **DONE 2026-09-01** (F16) |
| 17 | *(added 2026-09-01)* `DO-NOT-EDIT` header on chapter files; **SHA-256 in the manifest** — closes the outstanding items on tasks 10 and 11 | 10, 11 | **DONE 2026-09-01** (F17) |
| 12 | **Test the heading→filename map.** The ch1/ch10 prefix collision shipped despite F11 explicitly warning about it — care was not enough (F16) | 11 | **partly covered 2026-09-05** — task 19's duplicate-slug guard now aborts on that exact collision, but there is still no test file |
| 13 | Decide snapshot retention — every run writes a dated folder, nothing prunes; 20 `.md` each | 10 | pending |
| 14 | ~~Investigate **Ch6's −1,911-word drift**~~ → **investigate `ch3-methodology` at −1,991** instead, the only genuine negative drift row (F23) | 9 | **REFRAMED 2026-09-05** — the Ch6 figure was a parser artifact (F19); ch6 now reads **+709** |
| 18 | *(added 2026-09-05)* **Resolve heading levels from `word/styles.xml`** (outlineLvl → basedOn → name) instead of hardcoded style names | — | **DONE 2026-09-05** (F19) |
| 19 | *(added 2026-09-05)* **`_sanity_warnings()`** — abort/warn on a structurally implausible parse; record the resolved style table in the manifest | 18 | **DONE 2026-09-05** (F20) |
| 20 | *(added 2026-09-05)* **Reconcile the comments into the F18 ledger.** Word pass complete: **217 comments over 8 chapters** at snapshot `2026-09-05_17-23`. Start with **ch6 (48)** and **ch4 (42)** — 41 % of the load, both results-bearing (F23) | 18, 19, 21 | **pending — next** |
| 21 | *(added 2026-09-05)* **Render `w:tbl` as markdown tables** + cell/row separators in comment anchor text (28 tables, 4 table-anchored comments) | — | **DONE 2026-09-05** (F21) |
| 22 | *(added 2026-09-05)* Merged cells (`w:gridSpan` padding) are **untested** — confirmed by Brian as unused, and `gridSpan: 0 / vMerge: 0` at 17:23 (F22) | 21 | **deferred — out of scope**, no action unless a merged cell appears |

~~**Task 1 is the gate.**~~ **Cleared 2026-09-01** — the real reviewed document is
located, readable and parsed, so no synthetic fixture is needed and task 7 can validate
against 14 real comments.

**Read `findings.md` F12–F18 (the HANDOVER section) before starting.** The snapshot and
extraction half is already built and committed; tasks 10 and 11 are marked *partial*
rather than done because this plan's refined spec (`manifest.json` + sha256, `HH-mm`
folders, `DO-NOT-EDIT` headers) goes beyond what shipped.

---

## Open questions for Brian

1. **Where is the shared review document?** *Partially answered 2026-09-01:* it is a
   **114-page stitched `.docx` in a OneDrive folder of Brian's**, assembled by Enrico from
   the section drafts and finals. Exact path still needed. Brian is weighing a separate
   OneDrive-hosted writing repo added to the same VS Code workspace — see "Where the
   authoritative document lives" below.
2. ~~**One document or per-chapter files?**~~ **Answered 2026-09-01 (F6): one merged
   document.** The per-chapter `.docx` in `sections-final/` are generator output with empty
   comment stubs and were never the review surface. `chapter` must therefore derive from
   `heading_path`, which makes the Heading-scan in task 3 load-bearing.
3. **Do you and Enrico use Word's Resolve button, or just delete settled comments?**
   *Reframed 2026-09-01 (F12): there is no external reviewer — this is a two-author habit
   question.* Co-authors typically delete rather than resolve, in which case `delta = GONE`
   is the real "dealt with" signal and `resolved` is near-dead weight. Keep the column (it is
   nearly free once `commentsExtended.xml` is parsed) but do not build the workflow on it.

---

## Non-goals

- Writing comments *back* into the `.docx`. Read-only, in this plan.
- Replacing the NotebookLM review workflow (`05_thesis_writing/notebookLM/`). That is a
  different review channel — literature/methodology verification — and stays separate.
- Any thesis prose changes.

---

## Related

- `05_thesis_writing/sections-final/` — generated chapter docx (comment-free; not the review copy)
- `05_thesis_writing/analysis/` — parent of the new `comment-audits/` output folder
- `05_thesis_writing/notebookLM/` — the *other* review channel, deliberately separate
- `.claude/rules/repo-tier-structure.md` — why the script goes in `utility_scripts/`, not a thesis tier
- `plans/P0042_.../` — the review-rounds workstream this tooling serves

---

## Ledger addendum (2026-09-05) — the writable half

**Read F19 and F20 in `findings.md` before touching this section.**

The extraction half of this plan is built and working. What was missing is a place for
**band 3** (`triage_status`, `owner`, `action_taken`, `commit_ref`) to live: it was
specified as spreadsheet columns, and when task 4 deferred the spreadsheet nothing inherited
the job. The snapshot extract cannot hold it — it is regenerated on every run by contract.

**Decision (F20): a writable per-chapter ledger at
`05_thesis_writing/comment-ledger/chN.md`**, mirroring the existing `comments/chN.md` split.
Not a centralised hub — see F20 for why the hub was rejected.

### Artifact authority, extended

| Artifact | Job | Hand-edited? |
|---|---|---|
| OneDrive `.docx` | prose as submitted; where comments are **written and replied to** | yes, in Word |
| `docx-exported-snapshots/*/comments/chN.md` | read-only extract of what the comments **say** | **no** — regenerated |
| `comment-ledger/chN.md` | **what we decided to do about each one** | **yes** — this is the writable surface |
| `sections-drafts/chN.md` | live working state; bullets, status, provenance | yes |

The ledger is to the comment extract what `sections-drafts/` is to the prose snapshot: the
mutable sibling of a read-only derivative. Same division-of-authority principle as F10 and
`.claude/rules/writing-surface-authority.md`.

### Ledger entry format

**Revised 2026-09-05 for threads (F26).** The unit is a *thread*, keyed by its root
comment id — not a comment. Replies are nested inside the entry, never promoted to siblings.

```markdown
## T56 — Is NotebookLM use declarable?
- **status:** OPEN | ACCEPTED | DONE | REJECTED | DEFERRED | NEEDS-ENRICO
- **owner:** Brian
- **section:** Literature Review
- **anchor:** "The search was conducted using Google Scholar and NotebookLM…"
- **scope:** LOCAL | SECTION | CHAPTER | THESIS-WIDE
- **related:** T22, T25
- **word_resolved:** false        <- w15:done, the reviewers' own marker (F28)
- **thread:**
  - C56 Brian 09-01: flags the tooling admission as possibly not defensible
  - C57 Enrico 09-02: same for me, thought NLM was fine since Abid advised it
  - C58 Brian 09-03: declare it, and specify exactly what it was used for
- **resolution:**
- **commit:**
```

Two fields earn their place beyond band 3:

- **`scope` / `related`** — C18/19/20/22/25 are *one* argument (the RAM premise is unearned)
  spanning Ch1, Ch3 §3.7, Ch5 §5.1 and Ch10. One decision, four chapters.
- **`word_resolved`** — distinct from `status` (F28). Word-resolved means *the authors
  stopped arguing*; ledger `DONE` means *the thesis was changed*. The gap between the two
  is worth being able to see.

`scope` and `related` are the fields that earn the format. C18/19/20/22/25 are **one
argument** — the RAM premise is unearned — spanning Ch1, Ch3 §3.7, Ch5 §5.1 and Ch10.
Resolving them one at a time would produce four inconsistent edits.

### Reconcile contract (non-negotiable)

`--reconcile` **upserts and never destroys**:

| Situation | Behaviour |
|---|---|
| thread root in snapshot, not in ledger | append a stub, `status: OPEN` |
| root in both | leave `status`, `owner`, `resolution`, `commit` **untouched**; refresh only the machine-owned `thread:` block and `word_resolved` |
| root in ledger, gone from snapshot | flag `GONE (verify)` — **do not delete** |
| **new reply on an existing thread** | append the reply line to `thread:`; leave `status` alone but mark the entry `↻ new reply since last reconcile` |

The last row is load-bearing: F12 established that the two authors delete settled comments
rather than resolving them, so a disappearance means "check whether this was handled", not
"this is done".

### New tasks

> **Renumbered 2026-09-05.** A parallel session allocated tasks 18–22 to the
> extraction-hardening work. The ledger tasks below were originally numbered 18–21 and are
> now **23–28**. Findings `F19`/`F20` written in this section were likewise renumbered to
> **F24/F25**.

| # | Task | Depends on | Status |
|---|---|---|---|
| 23 | **Carry threading through the extract.** `read_docx()` already parses `w15:paraIdParent` into `parent_by_para` and then discards it, keeping only `is_reply` as a boolean (F26). Emit `parent_comment_id`, a derived `thread_id` (root comment of the chain) and `reply_count` — all three were specified in band 2 and never implemented. **Blocks everything else here** | 21 | **DONE 2026-09-05** (F30) |
| 24 | **Render threads as threads** in `comments/chN.md`: one `##` section per *thread*, replies nested beneath the root with author and date, rather than 217 flat sibling sections | 23 | **DONE 2026-09-05** (F30) |
| 25 | Add `--reconcile` — upsert snapshot **threads** into `comment-ledger/chN.md` per the contract below. Non-destructive; safe to re-run | 23 | **pending — next**; threading now available (F30), and task 29's constraint applies |
| 26 | `INDEX.md` generator — **a real per-thread status table** (F27), not just counts: thread id, chapter, section, owner, status, replies, one-line gist. Generated from ledger front-matter on every reconcile; carries **no `resolution` prose** | 25 | **DONE 2026-09-05** (F31) |
| 27 | Seed the ledger from snapshot `2026-09-05_17-23`. Start with **ch6 (48)** and **ch4 (42)** — 41 % of the load and both results-bearing (F23). Link the RAM cluster via `related` | 25 | pending |
| 28 | Document in `user-docs/integration/`; extend `.claude/rules/writing-surface-authority.md` with the authority table above so the rule covers comments, not only prose | 25, 26 | pending |
| 29 | ~~Do not build the reconcile contract on Word-resolved status~~ — **WITHDRAWN 2026-09-05** (F35): Brian resolved a test comment and it round-trips correctly; resolve is now the preferred workflow over delete | 25 | **withdrawn** |
| 30 | *(added 2026-09-05)* **Preserve bold/italic** through the conversion (458 bold + 153 italic runs were being dropped); suppress inside headings and superscripts | 21 | **DONE 2026-09-05** (F32) |
| 31 | *(added 2026-09-05)* **`--label` / `--slug`** — name a snapshot (`--label "First Complete Audit"` → `2026-09-05_18-04_first-complete-audit`); recorded in `MANIFEST.md` so milestone runs are distinguishable from routine and test runs | — | **DONE 2026-09-05** |
| 32 | *(added 2026-09-05)* **Key threads on `w14:paraId`, not `w:id`** — `w:id` is a position and is renumbered on every insertion (F33). `para_id` / `thread_para_id` now carried through the extract | 23 | **DONE 2026-09-05** (F33) |
| 33 | *(added 2026-09-05)* **Build the claim ledger** per F34: `comment-ledger/chN.md`, one entry per thread keyed on root `paraId`, carrying **was / is / should** + status + `related`. Supersedes the F25 schema, which keyed on the unstable `w:id` | 32 | pending — **the next real piece of work** |
| 34 | *(added 2026-09-05)* `--reconcile`: upsert threads into the ledger; freeze `was` once, refresh `is` every run, mark `DRIFTED` when they diverge, `GONE (verify)` when a thread disappears. **Never infer status from the document** (F29, F12) | 33 | pending |
| 36 | *(added 2026-09-05)* **Reconcile keys on `resolved`** as the primary handled-signal (F35), with `GONE (verify)` demoted to the anomalous case. Word-resolved ≠ ledger `DONE` — keep both | 33 | pending |
| 37 | **Terminology convention** — `Term` character style for model names / metrics / domain terms; exporter renders them as `` `code` `` | — | **ADOPTED 2026-09-05** (F37). Style applied to 5 runs so far; the ~200-instance pass is Brian's, in Word |
| 38 | *(added 2026-09-05)* **Parse Brian's review keyword vocabulary** (VERIFY / PROSE / SOURCE / OUTDATED / …) into typed tags; surface per comment, per thread, and as a **Work type by chapter** matrix in `INDEX.md` | — | **DONE 2026-09-05** (F38) |
| 39 | *(added 2026-09-05, from Brian's review notes)* **Cross-chapter duplication check.** Insights repeated across chapters with weak handovers. The per-chapter loop **entrenches** this by improving chapters in isolation, so it needs its own pass — **after ch6 + ch4, before the rest are rewritten** around text that may move | 42 | pending — sequencing matters |
| 40 | *(added 2026-09-05)* Route the ledger by tag: **VERIFY/OUTDATED/INCORRECT** → repo-checkable (Claude); **SOURCE** → NotebookLM/Zotero; **PROSE/ACADEMIC/WATERMARK** → human writing. The split fell out of F38's data | 33, 38 | pending |
| 41 | *(added 2026-09-05)* **Anchor excerpt raised to 2,000 chars** with head+tail and an explicit elision note — the anchored passage IS the work item for a PROSE/VERIFY thread; 400 chars cut 78 of 268 mid-passage (F39) | — | **DONE 2026-09-05** |
| 42 | *(added 2026-09-05)* **Chapter working loop** per F40: read `comments/chN.md` beside `chapters/chN.md` → resolve VERIFY/OUTDATED/INCORRECT from the repo → draft PROSE in the same pass → record in ledger → Brian applies + resolves in Word → re-snapshot to confirm `was != is`. **Start with ch6** (48 threads, 39 VERIFY, 23 PROSE, 18 SOURCE) | 33 | pending — the main work |
| 43 | *(added 2026-09-05)* **De-watermark + humanise pipeline.** Order is draft → `watermarks-remover` → human pass, and must stay in that order: a human rewrite after stripping reintroduces text that must be re-stripped. **The tool is hygiene, not disguise** — it removes provenance marks, not AI voice; the human pass is what ships (F40) | 42 | pending |
| 44 | *(added 2026-09-05, Brian's design)* **`sections/` — heading tree as nested folders**, one file per leaf section (154 files: 63 leaf-H2 + 70 H3 + preambles/intros). Enables precise cross-snapshot section diffs; `chapters/` unchanged | 41 | **DONE 2026-09-05** (F41) |
| 45 | *(added 2026-09-05)* **`writing-notes/` enters the revision loop.** 8 files, ~2,900 lines, `applies-to` frontmatter maps them to chapters. Precedence: **repo artefacts > writing-notes > thesis prose** — the notes declare their own staleness | 42 | pending — fold into the chapter loop |
| 46 | *(added 2026-09-05)* Revisit the F34 ledger's `was`/`is`: Brian wants **agent-readable before/after**, not deterministic comparison (F41). Store them as **snapshot pointers**, not copies of the text | 33, 44 | pending — simplifies task 33 |
| 47 | **Keyword dictionary committed to the repo** — `05_thesis_writing/writing-notes/review_comment_keywords.md`: Brian's definitions verbatim, measured distribution, the who-resolves-what split, verification precedence, and how the exporter parses tags | 38 | **DONE 2026-09-05** (F46) |
| 48 | *(added 2026-09-05)* **`comments/sections/` mirror** of `chapters/sections/`, same relative key, cross-linked both ways; 138 of 154 leaves carry comments | 44 | **DONE 2026-09-05** (F43) |
| 49 | *(added 2026-09-05)* **Verification precedence is a rule** (F44): script code > generated artefacts > writing-notes > thesis prose. A VERIFY resolution must cite the script or artefact, never the note | 45 | pending — governs the chapter loop |
| 35 | ~~Verify `w14:paraId` survives a non-desktop-Word round-trip~~ | 32 | **CLOSED 2026-09-05** — Brian: work finishes in desktop Word as-is; no round-trip will occur |

### The tabular question, settled (F27)

Brian raised tabular processing again. The framing *markdown vs. table* is the wrong
question — **a status roll-up and a decision record are two artifacts with two jobs**, and
forcing one file to do both is why either option feels inadequate:

| Need | Right shape | Written by |
|---|---|---|
| "what is left, where, whose" | table — counts, filters, sort | **generated**, never hand-edited |
| "what did we decide about this thread and why" | prose under a stable key | **hand-written** |

**Adopt the table as a generated view; reject it as the storage format.** `INDEX.md`
(task 26) becomes a real per-thread status table rather than the "counts" it was originally
specified as. Because it is derived, it cannot drift and costs nothing to regenerate.

**It must not carry `resolution` text.** The moment a decision's wording lives in two places
they diverge — the exact failure `writing-surface-authority.md` exists to prevent. Keys,
status and a one-line gist only.

Why the storage format stays markdown, at 217 comments and not 14:

- The ledger must read **beside the prose**; a spreadsheet is a different application from
  the one holding the comment and the paragraph.
- Comment text is long-form and now **dialogue**. A spreadsheet's answer to a thread is one
  row per message (losing the thread) or a merged mega-cell (losing the rows).

### Sequencing

**Superseded 2026-09-05.** The gate has cleared — the Word pass is done: **217 comments,
8 chapters, 200 Brian / 17 Enrico, 27 replies** at snapshot `2026-09-05_17-23`.

1. ~~Finish the Word comment pass~~ — **done**.
2. ~~Re-snapshot~~ — **done** (`2026-09-05_17-23`).
3. **Task 23 first, and it is not optional.** Threading must reach the extract before
   anything reconciles. Seeding a per-comment ledger and re-keying it to threads later means
   re-filing every decision by hand.
4. Then 24 → 25 → 26, then seed (27) starting with **ch6 (48)** and **ch4 (42)**.
5. **Resolve thread by thread, chapter by chapter**, working `comments/chN.md` (what was
   said), `chapters/chN.md` (the prose it was said about) and `comment-ledger/chN.md` (what
   we decided) side by side.

**Do not start at ch1.** It is the most-commented early chapter but its comments are
premise-level (the RAM cluster) and depend on decisions the results have not yet settled.
Ch6 and ch4 are results-bearing and answerable now.

Seeding Ch1 (task 20) before step 1 validates the mechanism only — it is not the audit.

### Deliberately still out of scope

- Writing decisions **back** into the `.docx` as replies. Read-only remains the contract.
- Inferring priority or sentiment from comment text (already rejected in the column schema
  above — it would present a guess about a co-author's words as data).

---

## First complete review pass — assessment (2026-09-05, second session)

Findings F47. The Word pass is **done**: 281 comments, 254 threads, all 13 content
chapters plus abstract / AI declaration / reference list. The 217-comment state was a
review in progress.

### What this adds to the F40 sequence

F40's order stands. Two amendments, both about *recording* rather than ordering:

1. **Seed the ledger from the ~130 substantive threads only.** 124 of 254 are bare tag
   stamps (F47). They are legitimate work items — F39 explains why — but they are one
   instruction repeated, not 124 decisions. Ch6 alone is 45 stamps and 4 arguments.
   Give them a sweep list keyed by section; keep the ledger for threads that carry a
   claim someone has to accept, reject or verify.

2. **`owner: Enrico` / `NEEDS-ENRICO` is only meaningful in ch1-ch2.** All 17 reply
   threads live there. Chapters 3-10 have had one reader, so an owner field elsewhere
   records an assumption.

### Suggested first three work items, by whether the answer exists today

| | work | threads | blocked on |
|---|---|---:|---|
| 1 | Strip LLM-as-judge from ch3/7/8/9/10 | ~28 | nothing |
| 2 | Fix grain / split descriptions | ~6 | nothing |
| 3 | Mechanical sweeps (9 subtitles, 6 watermarks, 8 appendix) | ~23 | nothing |

Item 1 is text that is factually wrong about the thesis's own method, in the chapters
read for method validity, and the answer is already known. It is the cheapest large win
in the corpus and it is independent of every pending result.

Items 4-6 (exogenous enrichment, then the ch6/8/9 verify+source+prose bulk, then the RAM
premise) are unchanged from F40's ordering and are blocked on a scope decision, on SRQ4
results, and on P0044 respectively.

### Handover note

The enrichment argument (ch1 x11, ch2 x6, ch4, ch5 `MISSING: the holiday api
enrichment`) is **not a writing task**. It changes feature engineering, hence model
training, hence every reported number. It moved to **P0046**; do not attempt to resolve
those threads from inside this plan.
