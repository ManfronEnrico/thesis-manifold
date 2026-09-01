---
pid: P0043
created: 2026-09-01 15:27:00
updated: 2026-09-01 17:00:00
status: in_progress
focus_detail: "SNAPSHOT HANDOVER 2026-09-01 (findings F12-F18): thesis_snapshot.py built, committed, run. Task 1 CLEARED -- real .docx located, 14 comments, commentsExtended.xml present so resolved-status is testable. Tasks 10/11 partial. || Build a Word->Excel comment audit workflow for the shared 114-page stitched thesis .docx. TWO AUTHORS ONLY (Brian + Enrico), no supervisor -- comments are the two of them talking to each other, so the band-3 triage merge and `author`/`owner` split matter more than `resolved`, which co-authors tend to bypass by deleting settled comments (F12). Adopted 2026-09-01: the snapshot contract (F13) -- one dated folder per snapshot capturing prose AND comments in one parse, split on Heading-1 into read-only per-chapter .md, diffed sentence-wise against the WIP sections-drafts/*.md. Extraction is stdlib-only (F5 prototype works); openpyxl is the sole new dependency. Gitignore the snapshot .docx, keep the sha256 in manifest.json. BLOCKER task 1: the OneDrive path to the stitched .docx."
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
| 12 | **Test the heading→filename map.** The ch1/ch10 prefix collision shipped despite F11 explicitly warning about it — care was not enough (F16) | 11 | pending |
| 13 | Decide snapshot retention — every run writes a dated folder, nothing prunes; 20 `.md` each | 10 | pending |
| 14 | Investigate **Ch6's −1,911-word drift**, the only signal F17 leaves standing | 9 | pending |

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
