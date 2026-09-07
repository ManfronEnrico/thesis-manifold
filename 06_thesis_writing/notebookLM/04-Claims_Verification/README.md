---
name: claims-verification-readme
description: How this folder is organised - chapter/topic subfolders for claims raised by prose, the two briefing documents, and where NotebookLM output goes.
created: 2026_09_07-15_15
updated: 2026_09_07-15_15
---

# 04 — Claims Verification

Claims that entered the thesis **without a source**, quarantined here until each is
sourced or reworded.

This differs from folders `01-` and `02-`: those check claims **against a known source**
("does the paper say what we say it says?"). Here there is no source yet — the question
is **whether a citable one exists at all**, and *"no source exists"* is a valid, useful
answer.

## Layout

```
04-Claims_Verification/
├── Claims_Verification-00-MASTER-verification-brief.md   the five claims, CV-01..CV-05
├── Claims_Verification-01-HOW-TO-RUN.md                  procedure; two-notebook split
├── Candidate Sources/          PDFs downloaded to answer them (candidates, not sources)
├── NLM Review/                 raw NotebookLM output lands here
└── Chapter <N> - <Name>/
    └── <Topic>/
        └── claims.md           claims raised by one prose block
```

**Chapter/topic subfolders are populated by the `write-prose-from-bullets` skill.** When
prose is written and carries a claim that cannot be verified, it is marked inline as
`(Author, Year UNVERIFIED)` and a `claims.md` is written to the folder for that
chapter and topic. This keeps a claim next to the prose that depends on it.

## Current contents

| Folder | Claims | Notebook |
|---|---|---|
| `Chapter 4 - Data Assessment/Holiday Enrichment/` | CV-03 Lukkeloven, CV-05 Store Bededag | B (factual) |
| `Chapter 6 - Model Benchmark/Holiday Enrichment/` | CV-01 VIF, CV-02 Spearman | **A (statistical)** |
| `Chapter 6 - Model Benchmark/Execution Determinism/` | CV-04 XGBoost mechanism | B (factual) |

## The two authorities

- **`writing-notes/unverified-claims-to-check.md`** is the register — the single source of
  truth for what is still open. Update status there; never delete a row.
- **This folder** is the instrument — the briefing packs and the per-chapter detail.

## The rule behind all of it

**If a source is not in the Zotero library, it is not a source.** Write the claim into
the register instead.

This exists because a plausible-looking reference (Hair et al., 2019) was once written
from memory into a code comment, and read as though it had been verified. A citation
invented to justify a threshold is more dangerous than a wrong number, because a reader
cannot check it against the data.

## Related

- `.claude/skills/write-prose-from-bullets/SKILL.md` — writes into these subfolders
- `.claude/rules/prose-insertion-discipline.md` — the marking and routing rule
- `06_thesis_writing/writing-notes/unverified-claims-to-check.md` — the register
