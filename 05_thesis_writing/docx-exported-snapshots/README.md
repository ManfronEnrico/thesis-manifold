# Docx-Exported Snapshots — How to Re-Run

> **Everything in this folder is generated and read-only.** Never edit a file here.
> Script: [`utility_scripts/scripts/thesis_snapshot.py`](../../utility_scripts/scripts/thesis_snapshot.py)
> Plan: `plans/P0043_2026-09-01_15-27_word-comment-audit-workflow/`

---

## Re-run the export

From the repo root (`Z:\_dev-ssd\thesis-manifold`). **PowerShell:**

```powershell
.venv\Scripts\python.exe utility_scripts\scripts\thesis_snapshot.py
```

**Bash / from inside Claude Code with the `!` prefix:**

```bash
.venv/Scripts/python.exe utility_scripts/scripts/thesis_snapshot.py
```

That's the whole thing. It reads the shared OneDrive `.docx`, writes a new folder stamped
`YYYY-MM-DD_HH-mm`, and prints what it wrote. Takes a second or two. **Safe to run any
time** — it only ever creates a new folder, never touches an existing one.

### Variations

| Need | Command |
|---|---|
| Snapshot a different file | `... thesis_snapshot.py --source "C:\path\to\other.docx"` |
| Skip the drift table (faster) | `... thesis_snapshot.py --no-drift` |
| Force a specific folder name | `... thesis_snapshot.py --stamp 2026-09-01_18-50` |
| See all options | `... thesis_snapshot.py --help` |

**Close the document in Word first if you can.** Not strictly required — the script copies
the file before parsing it, precisely because Word holds an exclusive lock — but you will
snapshot unsaved edits otherwise.

---

## What each run produces

```
2026-09-01_18-50/
├── thesis_full.docx              verbatim copy of the source   (GITIGNORED)
├── thesis_full.md                whole document as text        ~232 KB
├── chapters/
│   ├── ch1-introduction.md       one file per Heading 1        (17 files)
│   ├── ch3-methodology.md
│   └── …
├── comments.md                   every Word comment, all chapters
├── comments/
│   └── ch1-introduction.md       the same comments, split per chapter
└── MANIFEST.md                   counts, SHA-256, and the drift table
```

Roughly **470 KB tracked per snapshot** (the ~914 KB `.docx` is gitignored — the `.md` is
the diffable artifact, and the manifest's SHA-256 proves which source file it came from).

> `du -sh` reports ~22 MB for a snapshot folder. That is filesystem *cluster allocation*
> across many small files, not real bytes. The true total is ~1.34 MB.

### Where to look for what

| You want | Open |
|---|---|
| One chapter's prose | `chapters/ch3-methodology.md` |
| Every objection against one chapter | `comments/ch3-methodology.md` |
| All comments at once | `comments.md` |
| Every thread, sortable, with who spoke last | `comments/INDEX.md` |
| What changed vs. the working drafts | `MANIFEST.md` → *Drift* table |
| Proof of which `.docx` this came from | `MANIFEST.md` → SHA-256 |

Each comments file opens with an **index table** (id · section · opening line) and every
comment carries a stable anchor, so you can link to a single objection:

```markdown
See [comment 22](comments/ch1-introduction.md#c22) on the RAM-budget premise.
```

---

## Heading levels are read from the document

Chapter splitting does **not** rely on a hardcoded list of Word style names. Each run reads
`word/styles.xml` and resolves every style to a level from its explicit `outlineLvl`, then
its `basedOn` chain, then its name. A custom style (`H1-Chapter`) or a newly invented one is
picked up with no change to the script.

Each `MANIFEST.md` records the result as a **Heading styles resolved** table. If a snapshot
ever looks wrong, diff that table against an earlier one — a style that disappeared means
the document was restyled.

> Why this matters: on 2026-09-05 chapters 1–6 were restyled in Word and the old
> name-matching logic silently merged them into the Abstract, reporting success with an
> `Abstract` of 22,885 words. The run now aborts if any one section holds more than 40 % of
> the document.

---

## Three levels, two of them section-divided

| level | prose | objections |
|---|---|---|
| whole document | `thesis_full.md` | `comments.md` |
| chapter | `chapters/chN.md` | `comments/chN.md` |
| **leaf section** | `chapters/sections/…` | `comments/sections/…` |

The two section trees share the same relative path, so a section and the comments against it
pair up exactly, and each file points at the other:

```
chapters/sections/10-ch6-model-benchmark/05-results/01-tabular-model-benchmark.md
comments/sections/10-ch6-model-benchmark/05-results/01-tabular-model-benchmark.md
```

An H2 with sub-headings becomes a folder; an H2 without becomes a file. Numeric prefixes keep
document order. All 154 prose sections are written; only the ~138 that carry comments get a
comment file.

**Use the section level** to compare one section across snapshots, or to load just that
section and its objections:

```bash
diff old-snapshot/chapters/sections/<path>.md new-snapshot/chapters/sections/<path>.md
```

Section files carry comment **counts and tags**, never comment ids — Word renumbers ids on
every insertion, which would make every file differ on every snapshot.

---

## Threads

Word comments are grouped into **threads**: one `##` section per thread, replies nested as
`###` beneath the root. A thread is one decision, and its conclusion lives in its last
message — so 223 comments read as **196 threads**.

Every comment keeps its own `#cNN` anchor, replies included, so links stay stable.

`comments/INDEX.md` is the generated overview — one row per thread, with a **last voice**
column: a thread where Enrico spoke last is waiting on you, and vice versa. It is derived
from the document on every run and carries no decisions of its own.

> A chapter with as many threads as comments has had **no replies yet** — that is an
> unfinished review pass, not agreement.

---

## Formatting

**Bold** and *italic* survive the conversion — 325 bold spans in the current document.
Emphasis is load-bearing in this thesis (paragraph lead-ins, table headers, emphasised
claims), so it is preserved rather than flattened.

Deliberately **not** marked:

- **headings** — already bold by Word style, so marking would give `## **Chapter 3**`
- **superscripts** — a bold footnote marker inside an italic quote would split it
- **colour, highlight, strikethrough** — no portable markdown equivalent

Word counts and the drift table are computed on plain text, so markers never distort them.

---

## Tables

Word tables are rendered as **markdown pipe tables**, one per `w:tbl`, and `MANIFEST.md`
records how many were found. The document currently has 28.

A pipe inside a cell (the WMAPE definition is `Σ|y−ŷ| / Σ|y|`) is escaped as `\|`, so it
does not split the column.

**Comments anchored on table content** quote back with cell and row boundaries marked —
` | ` between cells, ` || ` between rows:

> **On:** "RTD | 37 | 93 | 0 ⚠️ | 42 | 589 | 511 | 2,193 | 44,449"

Without those separators the same anchor reads `RTD37930 ⚠️425895112,19344,449`, which is
what four table-anchored comments looked like before 2026-09-05.

**Known limitation:** merged cells are not reconstructed. Horizontally merged cells
(`w:gridSpan`) are padded with blank columns to keep the grid aligned; vertically merged
cells (`w:vMerge`) repeat or blank. Markdown cannot express either. This document has no
merged cells today, so that path is **untested** — check the rendering if one appears.

---

## Why markdown and not Excel

Deliberate, and revisited on 2026-09-01 (plan finding F16). The short version:

- **NotebookLM ingests text, not `.xlsx`.** A spreadsheet would have to be converted back
  to markdown before it could be an NLM source.
- **The comments are arguments, not tickets.** Several run to 200 words across multiple
  paragraphs. No spreadsheet cell renders that readably.
- **`git diff` between two dated folders** *is* the change report, so there is no
  merge-forward machinery to maintain.

Revisit if comment volume passes ~50 with both authors active.

---

## Which file is authoritative for what

The rule that keeps three copies of the thesis from becoming ambiguous:

| Artifact | Authoritative for | Hand-edited? |
|---|---|---|
| `sections-drafts/*.md` | live working state — bullets, results, anything a re-run changes | **yes** |
| the OneDrive `.docx` | prose as submitted; the comment surface | yes, in Word |
| `sections-final/*.docx` | **nothing** — stale generator output | **no** |
| everything in this folder | the diffable record | **no** — regenerate instead |

**If you want to change something, change the OneDrive `.docx` or `sections-drafts/*.md`,
then re-run.** Editing a snapshot creates a fourth version and loses the edit on the next
run anyway.

---

## Housekeeping

Nothing prunes old snapshots — each run adds a folder. At ~470 KB tracked apiece that is
slow growth, but keep the ones tied to a review round and delete idle re-runs:

```powershell
Remove-Item -Recurse -Force "05_thesis_writing\docx-exported-snapshots\2026-09-01_18-42"
```

> If deletion reports **"Device or resource busy"** while the folder is already empty,
> Windows is briefly holding the directory handle (indexer/sync). It clears on its own —
> don't retry in a loop. (Tooling issue #27.)

---

## Troubleshooting

| Symptom | Cause & fix |
|---|---|
| `ERROR: source not found` | The OneDrive path moved or is not synced locally. Confirm the file exists, or pass `--source`. |
| `ABORT: no headings resolved to level 1` | Almost certainly the wrong file. Heading levels are read from the document's own `word/styles.xml`, so custom styles resolve automatically. |
| `ABORT: '<X>' holds N of M words (P%)` | Chapters merged into one because a heading style did not resolve. Compare the manifest's *Heading styles resolved* table against the previous snapshot's. |
| `ABORT: two chapters share a filename` | Two headings map to the same slug; the later would overwrite the earlier. Add distinguishing `CHAPTER_MAP` entries. |
| `WARN ... not in CHAPTER_MAP` | A new or renamed chapter heading. Add it to `CHAPTER_MAP`, or it will not pair with `sections-drafts/`. |
| A table looks garbled | Check for merged cells in Word (`gridSpan`/`vMerge`) — these are not reconstructed. |
| `PermissionError` on the source | Word has it locked in a way the copy could not bypass. Close Word and re-run. |
| A chapter is missing from the drift table | There is no matching `sections-drafts/<slug>.md`. **Ch7 and Ch8 currently have none** — absence reads like agreement but isn't. |
| A chapter file has the wrong content | The heading → filename map (`CHAPTER_MAP`) needs an entry. Check `MANIFEST.md`'s chapter table first. |
| A chapter is missing entirely | Should now abort rather than happen silently. If it does occur, diff the manifest's *Heading styles resolved* table against an earlier snapshot — a style that vanished means the document was restyled. |
