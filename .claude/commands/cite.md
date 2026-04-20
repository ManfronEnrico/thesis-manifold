# /cite

Triggers the APA Citation Skill to format, verify, and insert a citation into the thesis.

## When to use
- You have a paper to cite and want it formatted in APA 7
- You pasted a _REV or _REV-brian note and want the citation extracted
- You have a DOI, title, or raw bibliographic data to format
- You want to insert a citation into a specific section file
- You want to add a paper to `thesis/thesis-writing/references.md`

## Do NOT use for
- Bulk verification of existing citations in a prose section → use `/verify-citations` instead
- Finding new papers → use `/find-papers` instead

## How to invoke

```
/cite                          # paste paper data in the next message
/cite ch2-literature-review    # specify target section
/cite [paste _REV note here]   # inline input
```

## Inputs accepted (in order of preference)
1. Full `_REV` or `_REV-brian` Obsidian note (copy-paste from Obsidian)
2. Paper title + first author (skill queries NotebookLM)
3. DOI (skill resolves metadata)
4. Raw bibliographic data (authors, year, title, journal, volume, pages)

## What happens
1. Skill extracts metadata from input
2. Skill verifies against NotebookLM notebook `48697de0-f0a5-4e66-918e-531abea82c20`
3. Skill formats in-text citation + full References entry (APA 7)
4. Skill checks `thesis/thesis-writing/references.md` for duplicates
5. Skill shows full output in chat — **awaits confirmation before writing to files**
6. On confirmation: appends to `thesis/thesis-writing/references.md` + inserts in-text citation in section file (if specified)

## Output
- In-text citation: `(Author et al., Year)`
- References entry: full APA 7 formatted string
- Verification status: ✅ VERIFIED / ⚠️ IMPRECISE / ❌ NOT FOUND

## Hard rules
- Never writes to files without showing output first
- ❌ NOT FOUND citations are never written to files without explicit human approval
- Duplicates in `thesis/thesis-writing/references.md` are flagged, not silently skipped
- APA 7 sentence case for titles, title case for journals — always
