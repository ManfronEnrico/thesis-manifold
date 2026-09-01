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
| What changed vs. the working drafts | `MANIFEST.md` → *Drift* table |
| Proof of which `.docx` this came from | `MANIFEST.md` → SHA-256 |

Each comments file opens with an **index table** (id · section · opening line) and every
comment carries a stable anchor, so you can link to a single objection:

```markdown
See [comment 22](comments/ch1-introduction.md#c22) on the RAM-budget premise.
```

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
| `ABORT: no Heading 1 paragraphs found` | The document uses custom styles instead of built-in Heading 1. Extend `H1_STYLES` in the script — do **not** accept one undivided file. |
| `PermissionError` on the source | Word has it locked in a way the copy could not bypass. Close Word and re-run. |
| A chapter is missing from the drift table | There is no matching `sections-drafts/<slug>.md`. **Ch7 and Ch8 currently have none** — absence reads like agreement but isn't. |
| A chapter file has the wrong content | The Heading-1 → filename map (`CHAPTER_MAP` in the script) needs an entry. Check `MANIFEST.md`'s chapter table first. |
