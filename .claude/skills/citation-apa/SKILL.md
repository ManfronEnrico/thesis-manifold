---
name: citation-apa
description: >
  Format, verify, and insert APA 7 citations into the thesis. Activate whenever the user
  provides a paper to cite — from an Obsidian _REV note, a NotebookLM source, a DOI,
  or raw bibliographic data pasted in chat. Also activate when the user says "cite this",
  "add this reference", "format this in APA", "insert citation for", or pastes a paper title,
  DOI, or _REV note. Produces an in-text citation AND a formatted References section entry,
  verifies both against NotebookLM, and writes output to the active section file and to
  thesis/thesis-writing/references.md. Do NOT use for /verify-citations (that command handles
  bulk citation checking on existing prose — this skill handles new citation insertion).
---

# APA Citation Skill

Formats and inserts APA 7 citations into the thesis production pipeline.
Operates within System B (thesis_production_system). Never touches System A.

---

## Input Sources (in priority order)

1. **Obsidian _REV note (standard)** — produced by the `_REV` command.
   Extract metadata from the note's standard fields (authors, year, title, journal, DOI, volume, pages).

2. **Obsidian _REV-brian note** — produced by the `_REV-brian` command. Same structure as _REV
   but includes a `%%FILE NAME: ...%%` header line. Strip that header before extracting metadata —
   it is a file naming convention, not bibliographic data.

3. **NotebookLM source** — user references a paper by title or topic already in the notebook
   `48697de0-f0a5-4e66-918e-531abea82c20`. Query NotebookLM to retrieve full metadata.

4. **Raw input** — DOI, title, or pasted bibliographic data. Extract metadata directly.
   If metadata is incomplete, flag missing fields before proceeding.

---

## Files This Skill Reads

| File | Purpose |
|---|---|
| User-provided _REV note or raw input | Primary citation data |
| `thesis/thesis-writing/references.md` | Existing reference list — check for duplicates before appending |
| `thesis/thesis-writing/sections-drafts/{chapter_id}.md` | Active section — for in-text citation placement |

## Files This Skill Writes

| File | What |
|---|---|
| `thesis/thesis-writing/sections-drafts/{chapter_id}.md` | In-text citation inserted at the correct position |
| `thesis/thesis-writing/references.md` | Full APA 7 reference appended (if not already present) |

---

## Step 1 — Extract Metadata

From whichever input source is provided, extract:

```
authors: [Last, F. I., Last, F. I., ...]
year: YYYY
title: Full article title (sentence case)
journal: Journal Name (title case)
volume: N
issue: N (if present)
pages: NNN–NNN (if present)
doi: https://doi.org/...
```

If any required field is missing → flag it explicitly. Do not invent metadata.
If DOI is missing but journal + year + title are present → flag DOI as unverified.

---

## Step 2 — Verify Against NotebookLM

Query NotebookLM notebook `48697de0-f0a5-4e66-918e-531abea82c20` with the paper title and first author.

Classify the result:

| Status | Meaning | Action |
|---|---|---|
| ✅ VERIFIED | Paper found, metadata matches | Proceed |
| ⚠️ IMPRECISE | Paper found but metadata differs (year, volume, etc.) | Use NotebookLM version, flag discrepancy to user |
| ❌ NOT FOUND | Paper not in notebook | Mark citation as `[CITATION UNVERIFIED]`, trigger `/find-papers` suggestion |

Do not block output for ⚠️ — correct and continue.
For ❌ — produce the citation with `[CITATION UNVERIFIED]` tag appended, and tell the user to run `/find-papers`.

---

## Step 3 — Format APA 7

### In-text citation

**Single author**: (Last, Year)
**Two authors**: (Last & Last, Year)
**Three or more authors**: (Last et al., Year)
**Direct quote**: (Last et al., Year, p. N)
**No author**: (Title fragment in italics or "Title", Year)

### References section entry

**Journal article (standard)**:
```
Last, F. I., Last, F. I., & Last, F. I. (Year). Title of article in sentence case.
Journal Name in Title Case, Volume(Issue), pages. https://doi.org/...
```

**Journal article (no issue number)**:
```
Last, F. I., & Last, F. I. (Year). Title of article in sentence case.
Journal Name in Title Case, Volume, pages. https://doi.org/...
```

**6+ authors**: List first 20, then `...` then last author.

Read `references/apa7-rules.md` for edge cases (books, chapters, conference papers, reports, websites, software).

---

## Step 4 — Check for Duplicate

Before appending to `thesis/thesis-writing/references.md`:
- Search for the DOI or author+year combination in the existing file.
- If already present → use the existing formatted entry, do not append again.
- If present but formatted differently → flag the discrepancy, ask user which to keep.

---

## Step 5 — Produce Output

Show in chat before writing to files:

```
## Citation Output

**In-text**: (Last et al., Year)

**Sentence example**:
"[phrase provided by user or suggested placeholder with citation inserted]"

**References entry**:
Last, F. I., Last, F. I., & Last, F. I. (Year). Title. Journal, Volume, pages. https://doi.org/...

**Verification**: ✅ VERIFIED / ⚠️ IMPRECISE [note] / ❌ NOT FOUND [action required]

**Written to**:
- thesis/thesis-writing/sections-drafts/{chapter_id}.md — in-text citation inserted
- thesis/thesis-writing/references.md — reference appended
```

Then write to both files. Do not write if verification status is ❌ — show output for human review first.

---

## Mandatory Rules

- Never invent author names, years, volume numbers, page ranges, or DOIs
- Always check `thesis/thesis-writing/references.md` for duplicates before appending
- ❌ NOT FOUND citations must never be written to files without human approval
- APA 7 formatting is non-negotiable — sentence case for titles, title case for journals
- If the user provides a phrase/sentence to cite, insert the in-text citation at the end of that sentence
- If no phrase is provided, produce the formatted citation only — do not invent surrounding prose
