---
name: review-comment-keywords
description: REFERENCE - The ALL-CAPS keyword vocabulary used in Word review comments, what each tag obliges, and how the export parses them. A bare tag is a complete instruction.
category: reference
applies-to: [comment triage, chapter revision, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9, ch10]
triggers: [working a comment thread, reading comments/sections/, planning a chapter revision, interpreting a bare keyword, extending the vocabulary]
created: 2026_09_05-20_05
updated: 2026_09_05-20_05
---

# Review Comment Keywords

Brian's review vocabulary, written during the whole-thesis comment pass of 2026-09-05.
Comments open with one or more ALL-CAPS keywords, sometimes followed by a colon and
additional text.

> **A bare keyword is a complete instruction, not an unfinished one.**
>
> The tags exist to avoid retyping the same request 111 times. A comment reading only
> `PROSE` means "these are bullet points I agree with, or a section too short to stand" —
> it is not missing context. Extra prose appears **only** where the tag alone was
> insufficient.
>
> This is why the exporter quotes the full anchored passage (up to 2,000 characters): with a
> bare tag, **the anchored text is the entire specification of the work item**.

---

## The vocabulary

| tag | what it obliges |
|---|---|
| **VERIFY** | Check against the current state of the code and repository whether the claim still holds or needs updating. |
| **SOURCE** | Either no source is cited where one is needed, **or** a source is cited that must be confirmed to exist in the Zotero library. Claims attributed to a paper should be checked against the paper via NotebookLM — attributions can be hallucinated. Build a list for individual NLM processing. |
| **METACOMMENT** | Non-submission-ready text left over from project notes or task lists. Remove it, or rewrite it to academic standard if it is genuinely relevant to an assessor. Also covers references to repository artefacts and hard-coded section numbers (e.g. `§6.2.0`). **No in-repository reference belongs in the thesis** — every reference must point to a table, figure, prose section or appendix inside the thesis document. |
| **TABLE REFERENCE** | A table appears in the text with no in-prose reference to it. Academic rigour requires pointing to each named table where it is discussed. |
| **PROSE** | Only bullet points where prose is needed, or a section too thin to justify its heading. Every heading-guided section (e.g. an H3) should carry at least a few paragraphs. |
| **NAMING** | Usually attached to a dynamically formatted table or figure whose title was guessed from surrounding context and needs a considered name. |
| **FORMATTING** | Formatting is not ideal — most often a table that would benefit from splitting merged values into their own columns so the data is clean and table-conformant. |
| **MATH** | A broken or plain-text formula that must become a proper Word formula (Unicode/LaTeX). Word toggles between **Professional** (rendered) and **Linear** (source) display. Linear example: `{\left(x+a\right)}^{n}=\sum_{k=0}^{n} \binom{n}{k}x^{k}a^{n-k}` |
| **WATERMARK** | Artefacts that read as obviously AI-written. Must be rewritten, removed or otherwise addressed. |
| **ACADEMIC** | Writing style is not at submission-ready academic level. Often downstream of METACOMMENT or WATERMARK problems. |
| **OUTDATED** | A fact or reference known to be stale, from an earlier run or a superseded decision. |
| **INCORRECT** | A fact or reference known to be wrong. Closely related to OUTDATED. |
| **APPENDIX** | Content that likely belongs in an appendix rather than in-text — e.g. a full system-prompt schema, which is neither helpful nor readable inline. Better referenced from the appendix, with specific excerpts discussed in-text. |
| **INTERNALREFERENCES** | A reference intended to point at a chapter in the document (e.g. "are in Ch8 §8.3.4") that is currently static. Must become a dynamic Word cross-reference so it does not break on every edit. |

### Also present in the document

These appear in the pass and are parsed, though they were not part of the original list:

| tag | meaning in use |
|---|---|
| **CONTEXT** | Background Brian is supplying to whoever works the thread — usually a fact the prose omits. |
| **UPDATE** | A specific value or statement that needs refreshing. |
| **MISSING** | Something absent that should be present. |
| **VALIDATE** | Used interchangeably with VERIFY; parsed as VERIFY. |

---

## Current distribution

Measured on snapshot `2026-09-05_19-52_complete-review-pass` — **254 threads, 214 tagged,
40 untagged**. A thread counts once per tag.

| tag | threads | concentrated in |
|---|---:|---|
| **VERIFY** | 111 | ch6 (39), ch4 (19), ch8 (16) |
| **PROSE** | 72 | ch6 (23), ch7 (10), ch8 (10) |
| **SOURCE** | 37 | ch6 (18), ch4 (8) |
| **OUTDATED** | 34 | ch8 (10), ch4 (9), ch3 (7) |
| **METACOMMENT** | 25 | ch6 (6), ch9 (4), AI declaration (4) |
| **FORMATTING** | 17 | ch7 (5), ch6 (4) |
| **CONTEXT** | 16 | ch3 (6), ch4 (4), ch5 (4) |
| **NAMING** | 13 | ch6 (6), ch7 (4) |
| **INCORRECT** | 11 | ch4 (5), ch7 (3) |
| **APPENDIX** | 8 | ch4 (4), ch3 (2) |
| **ACADEMIC** | 7 | ch6 (2) |
| **TABLE-REFERENCE** | 7 | ch6 (5) |
| **WATERMARK** | 6 | **ch3 (4)**, ch6 (2) |
| UPDATE / MATH | 2 each | — |
| MISSING / INTERNALREFERENCES | 1 each | — |

**The 40 untagged threads are not untriaged work.** They are the threads where Brian wrote
the instruction out in prose instead of tagging it. Read them; do not try to classify them.

---

## What the tags imply about who does the work

The vocabulary splits three ways, and the split fell out of the data rather than being
imposed on it:

| tags | resolved using | by |
|---|---|---|
| VERIFY, OUTDATED, INCORRECT, UPDATE | the repository — script code and generated artefacts | Claude (repo-aware) |
| SOURCE | Zotero + NotebookLM against the cited papers | Claude + NLM, human approval |
| PROSE, ACADEMIC, WATERMARK, NAMING | writing judgement | Brian / Enrico, Claude drafting |
| METACOMMENT, APPENDIX, FORMATTING, TABLE-REFERENCE, MATH, INTERNALREFERENCES | editorial mechanics in Word | Brian |

**PROSE and VERIFY are one pass, not two.** Of 72 PROSE threads, **56 also carry VERIFY** and
only 6 are PROSE alone. Establish what is true from the repository, then write it — opening
the same paragraph twice is wasted work.

---

## Verification precedence

A VERIFY thread is **not** closed by finding the claim restated somewhere else. Precedence:

1. **Script code** — the logic as it actually runs
2. **Generated artefacts** — EDA graphs, result tables, model performance outputs (the same
   files destined for the appendices)
3. **`writing-notes/`** — the argument and its rationale; useful for *finding* a claim fast
4. **Thesis prose** — what is currently asserted, and the thing under review

**Levels 3 and 4 are not evidence.** The notes declare their own staleness
(`sample-size-and-tool-interface-rationale`: *"all counts are snapshot-specific and superseded
by the 2026-08-12 re-pull"*), and the staleness audit records the sharper case:
*"ch6 passes the checker and is wrong throughout"* — prose that survives an automated check
while being false.

A resolution should therefore cite **the script or artefact** it was checked against, never
the note that explained it.

---

## How the export parses this

`utility_scripts/scripts/thesis_snapshot.py` reads the tags into `KEYWORDS` and surfaces them
in three places:

- **per comment** — in the section header of `comments/chN.md` and `comments/sections/…`
- **per section** — as a tag list in each `chapters/sections/…` file
- **per chapter** — as the *Work type by chapter* matrix in `comments/INDEX.md`

Matching rules, and why they are what they are:

- Only the **first 120 characters** of a comment are scanned. These words occur naturally in
  ordinary prose further down, where they are not tags.
- Variants are folded to a canonical spelling: `SOURCES` → SOURCE, `VALIDATE` → VERIFY, and
  the `METACOMMMENT` typo present in the document → METACOMMENT.
- A thread's tags are the **union** of its root and replies — a reply can introduce a type the
  root did not name.

**To add a keyword:** add it to `KEYWORDS` in the script, add a row to the vocabulary table
above, and note who resolves it in the split table. Both halves matter — a tag the script
parses but this file does not define is a tag a future session cannot act on.

---

## Related

- `05_thesis_writing/docx-exported-snapshots/README.md` — how to re-run the export
- `plans/P0043_2026-09-01_15-27_word-comment-audit-workflow/` — F38 (parsing), F39 (PROSE/VERIFY coupling), F44 (precedence), F45 (bare tags)
- `05_thesis_writing/writing-notes/2026_08_22-21_00-chapter-staleness-audit.md` — which chapters contradict the artefacts on disk
