---
name: pptx-exported-snapshots-readme
description: REFERENCE - Why deck snapshots exist, how to make one, and why the folder is gitignored.
category: reference
applies-to: [oral defence, slide deck]
triggers: [snapshot the deck, what changed in the deck, deck drift]
created: 2026_09_20-14_50
updated: 2026_09_20-19_25
---

# Deck snapshots

**Everything in this folder except this file is gitignored and regenerable.**

```bash
python utility_scripts/scripts/deck_snapshot.py --label "<what-changed>" --diff
```

## Why this exists

The authoritative deck is the **OneDrive `.pptx`**, shared between both
authors — exactly like the thesis `.docx`. And exactly like the `.docx`, it is
a zip of compressed XML, so git can neither diff nor merge it.

The specific drift this prevents: `slide-plan.md` carries speaker notes and the
thesis section grounding each claim; the `.pptx` carries the slides actually
being presented. **Nothing connects them.** A number corrected on a slide and
not in the plan — or the reverse — is invisible until someone reads both side
by side.

## What a snapshot contains

| File | What it is |
|---|---|
| `deck.pptx` | verbatim copy — the history |
| `deck.md` | every slide in presentation order, one document |
| `slides/NN-kw-title.md` | one file per slide — **this is what diffs cleanly** |
| `notes.md` | speaker notes only, for rehearsal |
| `MANIFEST.md` | provenance, counts, and the **missing-alt-text audit** |

## Filenames carry the section, then the header

Three segments, each from something the author set rather than something
inferred: **slide number**, the **"Add Section"** it belongs to, and the
**`KEYWORD | Title`** header.

```
04-[01_BG]-our_interest-embedding_forecasting_into_llms.md
09-[02_LIT]-five_strands-what_each_supplies_and_where_it_stops.md
31-[APNX_MODELLING]-model_selection.md
```

The section is **bracketed and upper-cased** so a listing groups visually at a
glance. Square brackets are legal on Windows — only `< > : " / \ | ? *` are
reserved — and they sort before alphanumerics, so the numeric prefix keeps
doing the ordering.

⚠ **One consequence:** `[` and `]` are glob metacharacters in bash and
PowerShell, so `ls 05-[01_BG]*` matches a *character class*, not the literal
text. Quote the pattern (`ls '05-[01_BG]'*`) or use `find -name`. Tab
completion handles it correctly.

A directory listing then sorts in presentation order *and* reads as the
outline. Each segment degrades independently — no section, or no pipe in the
title, drops that segment rather than inventing an empty one. `Default Section`
is PowerPoint's name for "never sectioned", so it earns no prefix, and a
section name repeated as the slide title is not stuttered twice.

Sections live in a `p14:sectionLst` extension on the presentation part, and
`MANIFEST.md` groups its slide table by them.

## The old convention

Slides are titled `KEYWORD | Title` — so `THE GAP | Extending AI Agents with
dedicated ML Models` exports as:

```
11-the_gap-extending_ai_agents_with_dedicated_ml_models.md
```

Both halves are kept because they mean different things: the keyword is the
section, the remainder is the claim. A directory listing then reads as an
outline. A slide with no pipe degrades to `NN-title.md` rather than inventing
an empty segment; only the **first** pipe splits.

## Reading order is computed from position, not XML order

**You do not need to maintain Reading Order in PowerPoint for this export.**

Shapes are stored in *z-order*, which is not reading order, and three things
follow from that:

1. **XML order can run bottom-to-top.** Slide 5's three boxes were stored Goal
   (y=5.79in) → Current Capabilities (y=3.82) → Offering (y=1.56).
2. **Groups get flattened by a naive walk**, interleaving a heading with
   whatever the document order happens to hold next.
3. **Inside a group the order is arbitrary too** — slide 5's groups store their
   *bullets* before their *title*, so "Goal" printed after its own bullets and
   looked as though it belonged to the box above.

**PowerPoint's Reading Order pane reorders only top-level shapes**, so it
cannot fix (3). That is why hand-tuning it did not move that heading.

The export instead walks the shape tree recursively, keeps each group whole,
and derives order from geometry.

### Columns, and why (top, left) is not enough

Sorting strictly top-to-bottom is right for a stack and wrong for columns.
Slide 15 is three columns — RESEARCH / FORECASTING / DESIGN SCIENCE, each a
heading at y=1.53 above its own bullets at y=2.6. Strict top-to-bottom emits
all three headings, then all three bullet lists, so **every bullet appears to
belong to the last heading printed**.

Two rules handle it:

1. **Row bands.** Shapes whose vertical extents overlap form a band; within a
   band, read left-to-right. A single column collapses to one shape per band,
   which is the stacked case unchanged.
2. **Column-major across bands.** Where the same left edges recur band after
   band — slide 25 puts both headings in one band and both bullet lists in the
   next — the whole layout is columnar, so read all of column 1 top-to-bottom,
   then column 2.

Shapes with no explicit position inherit one and sort last.

### The audit that keeps this honest

Reading order is **inferred**, so it can be wrong on a layout nobody
anticipated. `MANIFEST.md` therefore lists every slide whose order came from
geometry rather than from a simple stack:

```
| Slide | Title                            | Layout                            |
| 15    | METHDOLOGY | Central Academic ... | 6 columns (left-to-right in row)  |
| 25    | limitations                      | 2 columns x 2 bands (column-major)|
```

**Check those slides when the deck changes.** The rest are stacked and cannot
reorder. This is the systematic answer to "how do we stop this recurring": not
a promise that the heuristic is complete, but a standing list of where it is
load-bearing.

## What is extracted from the slide XML

| Structure | Where PowerPoint keeps it | Why it matters |
|---|---|---|
| **Bullets + nesting** | `a:pPr/a:buChar`, depth on `@lvl` | flattening a list loses the distinction between a heading and its items |
| **Table headers** | `a:tblPr/@firstRow`, *not* on the row | without it a table exports as an unreadable wall of pipes |
| **Image alt text** | `@descr` on `p:pic`, **`p:grpSp` and `p:graphicFrame`** | **this is where a figure's provenance lives** |
| **Sections** | `p14:sectionLst` on the presentation | the author's own outline |
| **Bold / italic / underline** | `a:rPr/@b @i @u` — on the **run**, not the paragraph | shows what the deck is emphasising; one line can mix styles |
| **Font + size** | `a:rPr/@sz` (hundredths of a pt), `a:latin/@typeface` | feeds the consistency audit |
| **Comments** | `ppt/comments/`, anchored by character range | a comment without its anchor is unusable |

## Comments carry their anchor

PowerPoint 2018+ stores comments outside the slide, in `ppt/comments/`, with
the anchor as a **character range**: `<ac:spMk id=…>` names the shape and
`<ac:txMk cp=… len=…>` the offset and length within it. The snapshot resolves
that range back to the quoted text, so a comment reads as:

> **enrico manfron** · 2026-09-19 15:35
> On: *“→ 61 sources cited,”*
> not sure of the numbers

Without the anchor, "not sure of the numbers" names no number. They collect in
`comments.md` as well as on each slide file, because hunting a worklist across
40 files is the friction that leaves it unactioned.

The legacy `<p:cmLst>` format is **not** handled — this deck does not use it,
and an untested path would look supported while silently producing nothing.

## The typography audit

`MANIFEST.md` reports every typeface and size in use, with the slides each
appears on, and flags **minority typefaces** — a font on 16 runs against one on
198 is a paste artefact, not a design decision. That is invisible slide by
slide and obvious in aggregate.

Runs with no explicit `sz` inherit from the layout or theme. The inheritance
chain is **not** resolved: reporting a number nobody set deliberately would be
noise, so absent is reported as absent.

`marL` is deliberately *not* treated as evidence of a bullet — it is set on
plenty of non-bulleted paragraphs purely for indentation.

Multi-paragraph table cells are joined with `<br>` so the row stays on one
markdown line; a raw newline would break the table.

## Alt text is the provenance channel

Every image without alt text is listed in `MANIFEST.md`, so the gap is a
worklist rather than a silence.

**Alt text is not only on `p:pic`.** A described **group** (several shapes that
are one figure) and a **graphic frame** (chart, SmartArt) carry it too. Reading
only `p:pic` reported 28 of 68 here and looked like the author had not written
the text — when 17 group and 4 frame descriptions were simply never inspected.
Where a group is described, its child pictures are not listed separately; the
group's text describes the whole figure.

**Template chrome is excluded and named.** A visual appearing on most slides is
a logo, not a figure; listing it 38 times buries the handful of real gaps.
Chrome is matched on the **media file**, not the shape name — the same logo is
`Picture 15` on one slide and `Picture 43` on the next. Writing alt text that names the source figure —
e.g. *"Scenario ladder, from
`05_thesis_results/07_decision_synthesis/figures/ch7_scenarios_v2.svg`"* — means
the snapshot records **what each slide shows**, not merely that an image is
present. That is what lets the deck be checked against the thesis artefacts
without opening PowerPoint.

## Two things the script handles that matter

**The deck can stay open.** A `.pptx` open in PowerPoint is locked on Windows;
reading it raises `PermissionError`. The script copies to a temp path first and
reads the copy, so you never have to close the deck to snapshot it.

**Slide order is read from `sldIdLst`, not filenames.** `slide12.xml` sorts
before `slide2.xml`, and PowerPoint reorders slides without renaming parts. The
presentation's own order list is the only authority.

## The diff

`--diff` compares against the previous snapshot and reports added, removed and
edited slides. Because each slide is its own file, an edit localises to one
slide instead of showing the whole deck as changed.

## Related

- `06_thesis_writing/defence/slide-plan.md` — the plan this deck is checked against
- `utility_scripts/scripts/thesis_snapshot.py` — the `.docx` sibling
- `.claude/skills/re-snap/SKILL.md` — the currency discipline this follows
