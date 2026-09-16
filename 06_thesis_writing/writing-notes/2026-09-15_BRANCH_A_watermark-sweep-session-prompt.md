---
name: 2026-09-15_BRANCH_A_watermark-sweep-session-prompt
description: HANDOFF - A ready-to-paste prompt for a fresh Claude session that builds the tooling and procedure for the machine-writing style sweep. Carries the repo's own traps, the measurement problem the snapshot cannot solve, and the rule against batch replacement.
category: workflow
applies-to: [all chapters, style sweep]
triggers: [watermark sweep, claude patterns, style pass, em dash]
created: 2026_09_15-12_00
updated: 2026_09_15-12_00
snapshot: 2026-09-15_11-51_post-consolidated-fixes
status: handoff prompt, ready to paste into a new session
---

# Prompt for a new session — the style sweep

**Paste everything below the line into a fresh Claude Code session started in
`Z:\_dev-ssd\thesis-manifold`.**

⚠ **Start that session only when the thesis document is otherwise locked.** The
sweep reads the whole document and proposes hundreds of small edits; if chapters
are still moving underneath it, its line references go stale as it works.

---

I need you to build the tooling and the procedure for a machine-writing style
sweep over a 46,000-word master's thesis, and then run the analysis half of it.
**You are not editing the thesis.** You produce a prioritised, reviewable list of
candidate edits that a human applies by hand in Word.

## Context you need before starting

**Read these first, in this order:**

1. `CLAUDE.md` — the project's navigation hub
2. `.claude/rules/prose-insertion-discipline.md` — how a writing note must be
   structured, what an anchor is, and why an anchor must be findable in Word
   rather than only in the snapshot
3. `06_thesis_writing/writing-notes/2026-09-14_BRANCH_A_watermark-patterns-to-remove.md`
   — the seven patterns, P1 through P7, already catalogued with examples

**The authoritative prose is a OneDrive `.docx`.** It is the only editable copy.
`06_thesis_writing/docx-exported-snapshots/<stamp>/` is a read-only mirror for
grepping and diffing. **Never edit a snapshot and never convert one back.**

Regenerate the snapshot before you start:

```bash
python utility_scripts/scripts/thesis_snapshot.py --label "watermark-sweep"
```

## The problem, stated precisely

The thesis was drafted with AI assistance. That is declared, and it is not the
issue. The issue is that certain sentence shapes recur at a frequency no human
writer produces, and an assessor who reads two hundred pages a year notices
rhythm before they notice content. **The goal is to break the rhythm without
flattening the prose into something worse.**

## Three traps this repository has already hit

**1 — The snapshot cannot measure em dashes.** The exporter renders U+2014 as a
plain hyphen, so `grep` for the character returns zero in every chapter while the
`.docx` is full of them. **Em-dash density must be counted in Word itself**, or
by reading the `.docx` XML directly rather than the markdown mirror. Solve this
first; if you cannot measure it, say so plainly rather than reporting zero.

**2 — A raw pattern count is an upper bound, not a defect count.** The
colon-elaboration pattern (`clause: clause`) also matches legitimate list
colons, quotation colons and ratio notation. A previous pass reported ~199 hits
across eleven chapters, of which an unknown majority were real. **Your tooling
must classify, not just count**, and it must report its own false-positive rate
on a hand-checked sample.

**3 — Batch replacement is forbidden.** These patterns are sometimes the right
construction. *"The retention threshold is not chosen; it is derived"* is a
precise sentence doing real work. A find-and-replace over the document would
destroy good prose to fix a rhythm problem, and the damage would be invisible
until an assessor read it. **Every candidate is reviewed individually by a
human.**

## What to build

**A script**, placed under `utility_scripts/scripts/` and resolving every path
through `PATHS.py` (never a string literal — the repo has been reorganised four
times and every hardcoded path broke silently). It should:

- read the current snapshot's `chapters/*.md`
- detect each pattern from the catalogue, plus any further ones you identify
  empirically by looking for over-represented sentence shapes
- **classify each hit** as LIKELY / POSSIBLE / LEGITIMATE, with the reasoning
  attached to each classification, so a human reviews the LIKELY set first
- report per-chapter density, so the worst chapter can be swept first
- emit a reviewable artefact: chapter, section, the sentence verbatim, the
  pattern, the classification, and — where you are confident — a suggested
  rewrite

**Do not emit the artefact into `05_thesis_results/`.** That tree is
reader-facing and assessors see it. This is an internal working file; it belongs
under `06_thesis_writing/writing-notes/`.

## What matters about the rewrites

**A rewrite must not cost precision.** The commonest failure is replacing a
colon-elaboration with a flatter sentence that loses the logical relation the
colon was carrying. If a pattern instance is doing real work, the correct output
is LEGITIMATE — leave it.

**Vary the repair, don't apply one substitution.** If every colon-elaboration
becomes a sentence starting "This", you have swapped one detectable rhythm for
another.

**Preserve the author's voice.** This thesis is written plainly, with short
declaratives and occasional dry understatement. Rewrites should sound like the
surrounding paragraphs, not like generic academic prose.

## The measurement question worth answering

Before proposing any edit, establish **what normal looks like**. Human-written
academic prose contains colons, em dashes and not-X-but-Y constructions; the
signal is density, not presence. If you can find a defensible baseline — a
published thesis in a similar field, or the author's own earlier writing — say
what the target density is and measure against it. **If you cannot establish a
baseline, say so** and fall back to relative density: sweep the chapters that
are outliers against the document's own mean.

## Deliverables

1. **The script**, working and documented
2. **A writing note** under `06_thesis_writing/writing-notes/`, following
   `prose-insertion-discipline.md`: one fix per heading block, ruled off, with a
   verbatim anchor that is findable by search in Word, before-and-after text for
   every proposed reword, and the pattern named
3. **A summary** stating: which patterns are real problems in this document,
   which are noise, the per-chapter priority order, and how long the human pass
   will take
4. **The em-dash count**, measured in the `.docx` rather than the snapshot — or
   an explicit statement that you could not measure it and why

## How to report

Tell me what you verified versus what you inferred. If a pattern turns out to be
rarer than the catalogue suggests, say so — the catalogue was written from
impression, not measurement, and correcting it is useful. **Do not pad the list
to look thorough.** Forty real candidates I will actually work through beat four
hundred I will abandon.
