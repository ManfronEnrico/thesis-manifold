---
name: p0056-progress
description: LOG - Session log for oral defence preparation.
pid: P0056
created: 2026_09_15-17_36
updated: 2026_09_20-14_15
---

# P0056 — Progress

## Session 1 — 2026-09-15, from 17:36

### `/re-snap` — 3 of 4 steps run, 1 skipped with reason

| Step | Result |
|---|---|
| 1. `git fetch` | clean. `83689d3`, 6 ahead of `origin/main`, nothing incoming |
| 2. snapshot | `2026-09-15_17-43_oral-exam-prep` — 47,299 words, 17 chapters, 1 comment, 143 leaf sections |
| 3. diff vs previous | **skipped deliberately** — thesis is submitted, no pending pass to check landings for |
| 4. Zotero re-pull | 88 items; `bibtex.bib` + `citations.json` written, then a cosmetic crash (see task_plan errors) |

Snapshot warned: 2 chapters not in `CHAPTER_SUBJECTS` (Table of Appendices,
Chapter 7). Known — P0052's concern, harmless here.

### Read

Submitted: abstract, Ch1, Ch8, Ch9, Ch10, the Ch8 comment thread, MANIFEST.
Repo: `PLANS_INDEX.md`, P0055 `task_plan.md` + `findings.md`,
`anticipated-assessor-questions.md`, `deferred-structural-decisions.md`,
canonical research questions, `22_scenario_comparison.csv`, the 87-SVG inventory,
submission-repo tier comparison.

### Decisions

| | |
|---|---|
| Deck before NotebookLM corpus before drill | Brian's choice; the deck forces the emphasis decisions the others inherit |
| Two deck variants, not one strategy | Brian declined both flaw options and asked for a transparent and a silent version |
| Deck reuses existing SVGs | 87 already generated and consistent with the submitted numbers (F7) |
| Numbers come from `05_thesis_results/`, never from the prose | Correctness-tier rule; also caught that "roughly fifty" is 51.3× (F3) |

### Phase 2 + 3 delivered (Session 1, 18:05–18:35)

All under `06_thesis_writing/defence/` — a new folder, with a README stating why
it sits in tier 06 and confirming no artefact is produced there (the decks
reference `05_thesis_results/` SVGs by path, never copy them).

| File | Lines of substance |
|---|---|
| `deck-variant-T-transparent.html` | 10 content slides, per-slide timings, speaker split, say-this text, reserve answers in notes |
| `deck-variant-S-silent.html` | 9 content slides; defect slide removed, 90 s returned to slides 6 and 10, both marked |
| `qa-drill.md` | 21 drilled questions + 8 one-liners, 20-second answer format, printable |
| `notebooklm/01_thesis-in-brief.md` | whole thesis in ~1,200 words |
| `notebooklm/02_the-ladder.md` | SRQ4 design, controls, the audit that caught drifted prompts |
| `notebooklm/03_every-number.md` | every figure, sourced from artefacts |
| `notebooklm/04_known-flaws.md` | 12 defects with cause + answer, plus 6 things NOT to concede |
| `README.md` | what to use when, and the two easy-to-break rules |

**Phase 4 is effectively delivered inside `qa-drill.md`** rather than as a
separate pass — it extends `anticipated-assessor-questions.md` (Part 2 carries
the six F6 gaps plus F9) instead of rebuilding it. Phase 5 (rehearsal support)
is partly inside the decks: timings, speaker split, handover notes. A separate
timing script was not written.

---

## Session 2 — 2026-09-19

### Git state settled first

The branch work from session 1 was pushed, merged and tagged before this
session's work began:

| Step | Result |
|---|---|
| Tag submission boundary | `submission-2026-09-15` at `9746b44` |
| Push branch | `83689d3..88692ed` |
| Merge `--no-ff` into main | `b9dbfd4` |
| Push main + tag | done |
| Switch to `main` | clean, `0 0` with `origin/main` |

⚠ **Now working on `main`, which contradicts the Trust-tier rule** ("never
commit directly to `main`; one branch per session"). Brian's reasoning: nothing
further will change anything that would have reached the submitted repo, and
defence work lives in `06_thesis_writing/defence/`, a folder with no counterpart
in the clean repo. **This is a deliberate exception, recorded here so it is not
read later as drift.** `thesis/svg-table-styling` is fully merged and can be
deleted.

### Reference deck read and measured → F11

Brian supplied a top-grade printed handout with speaker notes from Max's group.
Extracted with `pypdf` (35 pages, OCR, poor inside tables but structure legible).

**The measurement that matters: 13 presented slides, 22 reserve slides behind a
single "Let's discuss!" wall.** Full analysis, including three moves to copy and
three places the analogy breaks, in `findings.md` **F11**.

### Decision — restructure both decks onto a seven-section spine

Brian's chosen order: Background & Motivation / Literature Review / Methodology /
Architecture & Experiment / Most Relevant Findings / Limitations & Conclusion /
Discussion. Recorded as Phase **2b** in `task_plan.md`, with each of the seven
sections mapped to the slides that already exist.

| | |
|---|---|
| Presented sections get *fewer* figures, not more | timing is unchanged at ~15 min; adding a section adds no time |
| Section 07 is a wall, not a slide | one "Let's discuss" slide, then ~20 reserve slides, each titled as the question it answers |
| Reserve slides reference existing SVGs only | 87 verified on disk 2026-09-19; **no new figure is generated**, nothing is copied into tier 06 |
| Section 02 must be authored | it is the only section with no existing slide; `ch2_gap_diagram_v2.svg` is the anchor |

**Why the wall is worth building here specifically:** F6 item 4 already notes
the thesis cites ~2 figures against 87 generated. The reserve wall turns that
surplus from a question we can be asked into the way we answer questions. F9
(the two-table memory discrepancy) gets a reserve slide rather than a presented
one, as F9 itself directs.

---

## Session 3 — 2026-09-20

### `/re-snap` — all four steps run, none skipped

| Step | Result |
|---|---|
| 1. `git fetch` | clean. `b9dbfd4`, branch `main`, **0 ahead / 0 behind**, nothing incoming |
| 2. snapshot | `2026-09-20_14-09_defence-deck-citation-audit` — 47,139 words, 17 chapters, 142 leaf sections, **0 comments** |
| 3. diff vs previous | **run this time** — and it is what produced F12 |
| 4. Zotero re-pull | 88 items; both exports written, then the known cosmetic `KeyError: 'year'` (F10) |

**Session 1 skipped step 3 on the reasoning "the thesis is submitted, so there
is no pending pass." That reasoning was wrong and it cost a day.** The document
moved after submission.

### What the diff found

| Chapter | 09-15 | 09-20 | Δ |
|---|---:|---:|---:|
| reference-list | 934 | 1,642 | **+708** |
| table-of-contents | 829 | 109 | −720 |
| ch4-data-assessment | 5,689 | 5,647 | −42 |
| ch2-literature-review | 6,331 | 6,316 | −15 |
| *(six others)* | | | ±1–8 |

The reference list went from **34 entries to 61**. Everything else is field
re-rendering noise (the TOC collapsed because its field was not expanded at
export time).

### F12 — I corrected my own finding

On 2026-09-19 I audited citations against the 09-15 snapshot, found 35
reference entries against ~68 in-text citations, and told Brian his slide's
"**61 sources cited**" did not match the document.

**The slide was right. My audit was stale.** The bibliography field had not been
refreshed when the submission snapshot was taken. The fresh snapshot shows
exactly 61.

The lesson is narrower than "the .docx is ground truth" — I did apply that rule.
**It is that a snapshot is not the document.** A five-day-old mirror is a stale
surface, and `/re-snap` exists for precisely this. Recorded as F12; F1's
currency block is marked superseded so nobody trusts the 09-15 numbers again.

### Consequence

- **Brian's literature-review slide needs no change.** My recommendation to drop
  the number is withdrawn.
- Residual after the fix: 13 in-text citations without an exact match, but 8 are
  year variants where the source *is* listed. **Atıl (2025) and Schwartz (2020)
  are in neither the reference list nor Zotero** — the only genuine unknowns,
  both in Ch3. No action; the thesis is closed.

### PDF section split re-run

Source: `…/Drafts/MSc. Data Science - 175888 and 176171 - Master Thesis.pdf`,
**136 pages**, dated 2026-09-16. The previous split ran against a **142-page**
version — so the PDF was regenerated post-submission as well as the `.docx`.

| Mode | Units | Coverage |
|---|---:|---|
| `--chapters-only` | 13 | 133/136 |
| `--chapters-and-h2` | 73 | 133/136 |

Pages 1–3 (title, TOC) are excluded by design. Reference List is now 5 pages
(120–124), consistent with the 61 entries.

⚠ **Eight stale PDFs from the old run had to be deleted by hand** — the script
writes but never deletes. Six carried *off-by-one section numbers* after Ch5
gained §5.2 Modelling Pipeline, so they looked current and were not. Recorded as
**F13**, including that this is the defect `figure-generation-standards.md`
already names ("a generator must delete, not only write"). All eight were
verified absent from both regenerated indexes before removal.

---

## Session 4 — 2026-09-20 (later)

### The deck exists, and it is ahead of the plan

Brian pointed at the real `.pptx`. **39 slides, 15 with notes, 36 media.** It is
substantially built and its structure is the authors' own, not the slide plan's.

| | Deck as built |
|---|---|
| 1–2 | Title, agenda (6 sections, matching the screenshot) |
| 3–6 | Background & Motivation — incl. a Forbes cost-of-AI hook and the Manifold business case |
| 7–13 | Literature Review — review approach, **five** strands, RQ, gap, RQ tree |
| 14–16 | Methodology — academic grounding, summarised approach |
| 17–21 | Modelling, Architecture & Experiment — pipeline, EDA, combined overview, performance |
| 22–23 | Most Relevant Findings — one table, SRQ1–SRQ4 |
| 24–25 | Limitations & Conclusion — limitations + future work |
| **26** | **"Let's discuss!"** |
| 27–34 | **Reserve wall, already built** — pipeline, schema, model selection, resource profile, performance, forecast overlay |
| 35–39 | Spare title/agenda/appendix variants |

**The reserve wall was already their idea and is already in place.** F11's
recommendation was, in effect, already implemented.

### Where the deck is BETTER than `slide-plan.md`

- **Slide 23** collapses all four SRQs into one *finding / qualification we
  report* table. That is tighter than the plan's three separate findings slides
  and it foregrounds the qualification, which is the thesis's own framing.
- **Slide 9** carries **five** literature strands, not four — it adds retail
  demand forecasting ("gradient boosting dominates at scale; cross-learning
  beats series-by-series … nothing on serving the forecast"). Ch2 §2.7 names
  four; the fifth is defensible from Ch1 §1.1 (M4/M5, Ma et al.).
- **Slide 4** opens on a Forbes piece about AI costing more than the staff it
  replaced. That is a better hook than the plan's M4/M5 opening and reaches the
  same place — cost as the binding constraint.

### Verified against the artefacts

Slide 21's table matches `22_scenario_comparison.csv` exactly (502.2 / 2.9 /
14.6, 26.7 / 4.1 / 0.0, $0.38 / $0.4667 / $0.0091, 69.5 / 123.8 / 6.0 s).
Slide 23 quotes **35 MB**, which is the abstract's own rounding of 34.5 and
therefore sidesteps the F9 discrepancy rather than inheriting it. Slide 8 says
**61 sources**, confirmed correct by F12.

### Built: `deck_snapshot.py` — the `.pptx` sibling of `thesis_snapshot.py`

Brian asked for re-snap logic for the deck so slides and notes cannot drift
from the plan. Written, run, and proven:

| | |
|---|---|
| Script | `utility_scripts/scripts/deck_snapshot.py` |
| Output | `06_thesis_writing/defence/pptx-exported-snapshots/<stamp>_<label>/` |
| Contents | `deck.pptx`, `deck.md`, `slides/NN_<slug>.md`, `notes.md`, `MANIFEST.md` |
| PATHS | `THESIS_DEFENCE_DIR`, `THESIS_DECK_SNAPSHOTS_DIR` added |
| gitignore | folder ignored except its README, matching the `.docx` snapshot rule |

**Two design points that came from this session's own failures:**

1. **The deck can stay open.** A `.pptx` open in PowerPoint is locked — the
   first read attempt here died on `PermissionError`. The script copies to a
   temp path and reads the copy, so snapshotting never requires closing the
   deck. The common case is snapshotting mid-edit.
2. **Slide order comes from `sldIdLst`, not filenames.** `slide12.xml` sorts
   before `slide2.xml`, and PowerPoint reorders slides without renaming parts.

**One slide per file is what makes the diff useful** — an edit localises to one
slide instead of showing the whole deck as changed. Proven live: a test
snapshot two minutes after the first correctly reported `~ edited slide 4`
(media 36→37), because Brian was editing while it ran.

### `deck_snapshot.py` extended — structure, alt text, naming convention

Brian's four asks, all implemented and verified against the real deck:

| Ask | Where PowerPoint keeps it | Result |
|---|---|---|
| **Bullet points** | `a:pPr/a:buChar`, depth on `@lvl` | 44 bullet paragraphs detected, nested by level |
| **Table structure** | `a:tblPr/@firstRow` — *on the table, not the row* | 5 tables; header separator emitted only where flagged |
| **Image alt text** | `p:cNvPr/@descr` | captured, plus `@title`; missing ones listed in MANIFEST |
| **`KEYWORD \| Title` filenames** | the deck's own header convention | `11-the_gap-extending_ai_agents_with_dedicated_ml_models.md` |

**Design notes worth keeping:**

- `marL` is **not** treated as evidence of a bullet. It is set on plenty of
  non-bulleted paragraphs for pure indentation, so keying on it would have
  marked body text as list items.
- Multi-paragraph table cells join with `<br>`, not a newline — a raw newline
  breaks a markdown table row.
- Only the **first** pipe splits a title; a title with further pipes keeps them
  in the second half rather than being chopped into three.
- A slide with no pipe degrades to `NN-title.md` rather than inventing an empty
  keyword segment.

**Alt text is the provenance channel.** 38 of 66 images carry `descr`, but 37 of
those are the CBS logo's stock text. **Exactly one is real** — slide 11,
*"The Research Gap Figure"* — which Brian added and which the extractor picks up
correctly. MANIFEST lists every image still missing one, so the gap is a
worklist rather than a silence.

Recommended to Brian: write alt text that names the **source artefact**, e.g.
*"Research gap as the intersection of five literatures. Source:
`05_thesis_results/02_literature_review/figures/ch2_gap_diagram_v2.svg`"*. That
is what makes the deck checkable against the thesis artefacts without opening
PowerPoint. `Logo_CBS` and `Plassholder for innhold 12` do not need alt text —
the audit is a worklist, not a checklist to zero out.

### `deck_snapshot.py` — comments and typography

Two more extensions, both verified against the real deck.

**Comments, with their anchor resolved.** PowerPoint 2018+ keeps comments in
`ppt/comments/`, not in the slide, and anchors them by **character range**:
`ac:spMk/@id` names the shape, `ac:txMk/@cp @len` the offset and length. The
snapshot resolves that range back to the quoted text.

That resolution is the whole value. Enrico's comment on slide 8 reads:

> **enrico manfron** · 2026-09-19 15:35 — On: *"→ 61 sources cited,"*
> "not sure of the numbers"

Without the anchor, "not sure of the numbers" names no number. ⚠ **He flagged
the exact figure I wrongly disputed in F12** — 61 is correct, confirmed against
the refreshed reference list. That comment can be resolved.

Offsets are measured against paragraphs joined by a single `
`, which is how
PowerPoint counts them; getting that wrong silently shifts every anchor.

The legacy `<p:cmLst>` format is deliberately **not** handled — this deck does
not use it, and an untested path would look supported while producing nothing.

**Character formatting + typography audit.** Bold, italic, underline, size and
typeface, read from `a:rPr` on the **run** — not the paragraph, because one
line mixes styles (the deck's own `**KEYWORD |** Title` headers do exactly
this). Adjacent runs sharing a style are merged before rendering, or PowerPoint's
habit of splitting runs on every edit produces `**b****o****ld**`.

Measured: **180 bold · 31 italic · 16 underline** runs, 12 distinct sizes.

⚠ **The audit found a real inconsistency:** `-apple-system` on 16 runs against
`Inter` on 198, confined to slide 9's table. A paste artefact, invisible slide
by slide and obvious in aggregate. The audit flags any typeface under 25% of
the dominant one.

**A bug caught while building it:** the first audit walked `blocks` but not
table cells, so it reported only Inter and missed the very inconsistency it
exists to find. Table runs are now collected alongside the rendered rows.

Inherited sizes are **not** resolved through layout/master. Reporting a number
nobody set deliberately is noise; absent is reported as absent.

### Title detection was wrong — fixed using the typography just added

Brian caught it: slide 4 exported as
`04-ai_generated_image_based_on_real_article.md`, having taken an image caption
as the slide title. The real headline was **"OUR INTEREST | Embedding
Forecasting into LLMs"**.

**Cause:** `_title_of` returned the first text-bearing shape in XML order.
**Shapes are stored in z-order, not reading order**, so a 10pt caption at
y=6.86in preceded the 32pt headline at y=0.27in. The heuristic had no notion of
where text sits or how big it is — it only looked plausible because most slides
happen to store the title first.

**Fix — three passes, in order of authority:**

1. **A real title placeholder** (`ph type="title"`/`ctrTitle`). 11 slides have
   one; where PowerPoint has been told what the title is, that is the answer.
2. **Largest explicit font size**, but only on a *clear* win. A tie is not
   evidence — six agenda items all at 24pt are a list, not six candidate
   headlines — so ties fall through.
3. **Highest on the slide** (`a:off/@y`, EMU → inches). This catches slides
   where every shape inherits its size, which is most of the free-form ones.

**Two edge cases the first fix missed, both found by checking rather than
assuming:** slide 2 (six agenda items tied at 24pt, with "Agenda" itself
inheriting its size) and slide 25 (no shape carries an explicit size at all).
Pass 3 resolves both.

Brian's own suggestion — *"if we could pull and match the font and size, it
would become clearer what is the major headline"* — is exactly the fix, and the
typography extraction added an hour earlier is what made it available.

**Result:** every one of the 40 titles is now correct. `02-agenda`,
`04-our_interest-embedding_forecasting_into_llms`,
`05-business_case-manifold_ai_quantitative_ai_agents`,
`15-methdology-central_academic_grounding` and `25-limitations` all corrected
themselves.

### Alt text complete

**66 of 68** images carry alt text. The two without are `Logo_CBS` and an empty
`Plassholder` — neither should have any; a screen reader announcing a logo on
every slide is noise. **This is done.**

Current snapshot: `2026-09-20_18-16_title_fix_v2`. Superseded ones pruned.

### Sections in the filename, and two real bugs found doing it

**Sections.** PowerPoint's "Add Section" lives in a `p14:sectionLst` extension
on the presentation part. Brian had already numbered them, so they map straight
onto a filename prefix:

```
04-01_background_motivation-our_interest-embedding_forecasting_into_llms.md
```

Three segments, each authored rather than inferred: number, section, header.
A directory listing now sorts in presentation order *and* reads as the outline.
`Default Section` earns no prefix (it is the absence of a choice), and a
section name repeated as the slide title is not stuttered. MANIFEST groups its
slide table by section.

**Reading order.** Brian's fix worked — headings now group with their bullets
("Offering" → its three items) instead of interleaving.

**Bug 1 — alt text was under-reported by two thirds.** `_images` read only
`p:pic`. But 17 descriptions sit on **groups** (several shapes described as one
figure) and 4 on **graphic frames**. The audit said 28 of 68 and implied Brian
had not written the text; he had. Groups and frames are now read, and a
described group suppresses its child pictures so a figure is counted once.

**Bug 2 — chrome detection keyed on the wrong field.** Matching repeated
visuals by shape *name* failed: the CBS logo is `Picture 15` on one slide and
`Picture 43` on the next. It now keys on the **media file**, which is stable.
The logo is excluded once and named, rather than listed 38 times burying the
real gaps.

Also fixed: slide-number/date/footer placeholders were leaking a bare `"5"`
into 9 slide exports. They render a field and carry no authored content, so
they are skipped — and they would have produced diff noise on every renumber.

**Result: 34 of 41 real visuals carry alt text.** The rest are decorative or on
backup slides. Brian's group-level descriptions carry genuine argumentative
content — the two Prometheus ones note that Manifold's own site claims
"enhances forecasting accuracy" where no dedicated modelling exists, which is
part of the thesis's justification.

### ⚠ Two things for Brian in the section names

1. **`05_Discusssion_Limitations`** — three s's.
2. **Section 05 is "Discussion & Limitations" and section 06 is "Limitations &
   Conclusion"** — limitations appear in both, and the agenda slide lists six
   sections with neither pair matching this split. Worth reconciling before the
   deck is printed, since section names are visible in presenter view.

### Reading order — the real cause, and why hand-tuning could not fix it

Brian asked what dictates the order text is read in, having tuned both
"Reading Order" and "Selection" on slide 5 without the heading moving.

**The export was walking `root.iter(sp)` — every shape anywhere in the tree, in
raw XML order.** Three things follow, and all three bit slide 5:

| | |
|---|---|
| XML order is **z-order**, not reading order | slide 5's boxes stored Goal (y=5.79in) → Current (y=3.82) → Offering (y=1.56), i.e. bottom-to-top |
| `iter()` **flattens groups** | a heading and its bullets are one visual unit; flattening interleaves them |
| **Inside** a group the order is arbitrary | slide 5's groups store bullets BEFORE title |

**PowerPoint's Reading Order pane reorders only top-level shapes**, so it
cannot reach the third — which is exactly why Brian's change had no effect on
that heading. His edits *did* land (the top-level order reversed, and the
shapes are now helpfully named "TextBox 35: Title: Goal"), but the within-group
order is not something the pane exposes.

**Fix:** walk the shape tree recursively, keep each group whole, sort every
level by position (top-to-bottom, then left-to-right). Group children do carry
explicit offsets, so the title at y=5,342,205 now precedes its bullets at
y=5,829,074.

Slide 5 now reads Offering → its 3 bullets, Current Capabilities → its 2,
Goal → its 2. **No manual Reading Order upkeep is needed for the export.**

**Also fixed: the diff was keyed on filename.** Renaming a section rewrites
every filename in it, so the diff reported the whole deck as removed-and-added
and buried the one slide that changed. It now keys on **slide number** and
reports renames separately (`» renamed`).

### Bracketed, upper-cased section prefixes

Brian asked for visual grouping in the filenames.

```
04-[01_BG]-our_interest-embedding_forecasting_into_llms.md
09-[02_LIT]-five_strands-what_each_supplies_and_where_it_stops.md
31-[APNX_MODELLING]-model_selection.md
```

**Square brackets are legal on Windows** — only `< > : " / \ | ? *` are
reserved — verified by writing the files before relying on it. They sort before
alphanumerics, so the numeric prefix keeps doing the ordering.

⚠ **Caveat worth knowing:** `[` and `]` are glob metacharacters in bash and
PowerShell, so `ls 05-[01_BG]*` matches a character class rather than the
literal text. Quote the pattern or use `find -name`. Recorded in the README;
not a reason to avoid brackets, since tab completion handles it.

Brian also shortened the section names in PowerPoint (`01_Background &
Motivation` → `01_BG`), which is what makes the prefixes scan cleanly.

**The slide-number-keyed diff proved its worth immediately:** the bracket
change renamed all 40 files, and the diff reported 40 renames rather than 40
deletions plus 40 additions.

### Alt text complete — 39 of 41

Final snapshot `2026-09-20_19-08_alt_text_restored`. The two without alt text
are the ones that should not have it:

| Slide | Shape | Why it stays blank |
|---|---|---|
| 1 | `Logo_CBS` | the CBS logo — a screen reader announcing it is noise |
| 37 | `Table 15` | on a **backup** title-slide variant; slide 1's equivalent is labelled |

**Two of the descriptions name their source artefact**, which is the pattern
worth repeating — it makes the deck checkable against the thesis without
opening PowerPoint:

> `Graphic 3 — Main RQs and 4 Sub RQs: Source File = 05_thesis_results_introductionigures\ch1_research_questions_tree_v2.svg`
> `Graphic 3 — Preprocessing Pipeline. Source = 05_thesis_results_data_assessmentigures\ch4_preprocessing_pipeline_v2.svg`

The rest identify the figure without the path (`Data Pipeline.`, `Model
Selection`, `Resource Profile`, `Forecast Overlay`). Adding the source path to
those would close the loop, but is optional.

The methodology slide's group descriptions carry real content — *"Modest
realism: demand exists independently; the panel reaches it through an
instrument that carries its own assumptions"*, *"Out-of-sample evaluation:
expanding-window cross-validation; the test split is never observed during
selection"*. That is the defence answer to a methodology question, sitting in
the deck rather than only in the drill.

### Multi-column reading order — and a standing audit so it stays fixed

Brian found slide 15's bullets all attributed to the first heading, and asked
whether there is a **systematic** way to stop this recurring.

**Cause.** Slide 15 is three columns — RESEARCH / FORECASTING / DESIGN SCIENCE
— each a heading box at y=1.53 above its own bullets at y=2.6. Sorting by
(top, left) emits all three headings, then all three bullet lists, so every
bullet reads as belonging to the last heading printed. Correct for a stack,
wrong for columns.

**Fix, two rules:**

1. **Row bands.** Shapes whose vertical extents overlap form a band; read
   left-to-right within it. A stack collapses to one shape per band, unchanged.
2. **Column-major across bands.** Where the same left edges recur band after
   band, the layout is columnar end-to-end — slide 25 puts both headings in one
   band (y=0.18) and both bullet lists in the next (y=0.80) — so read column 1
   fully, then column 2.

Verified on all three shapes of layout: slide 15 (3 columns), slide 25
(2 columns x 2 bands), slide 5 (stacked, unchanged).

**The systematic part.** Reading order is *inferred*, so it can be wrong on a
layout nobody anticipated. `MANIFEST.md` now carries a **layout audit** naming
every slide whose order came from geometry rather than a simple stack — 8 of
40 here. That is the honest answer to Brian's question: not a claim the
heuristic is complete, but a standing list of exactly where it is load-bearing,
to be re-checked whenever the deck changes.

**A false lead worth recording:** a crude text-level audit (bold heading with
no following bullets) flagged slides 2, 8, 25, 27 and 39. Only 25 was real; the
rest were agenda lists and title slides with no sub-headings. Geometry is the
reliable signal here, not the rendered markdown.

### Open for Brian

1. **Phase 0 compliance** — CBS requires informing supervisor *and* censor of GenAI use in defence preparation. Outside party; cannot be done from here.
2. **F5** — the lag-13 defect is already in the submitted Ch9 §9.4, so "transparent vs silent" is not confess-vs-conceal. Changes the choice.
3. **F8** — was Ch8's Table 24 regenerated before submission (comment 279)?
4. Defence date/time — not yet known; available on Digital Exam ≤8 days prior.

---

## Session 4 (cont.) — 2026-09-20 19:24 — Deck review pass 01

Snapshot `2026-09-20_19-24_review_pass` taken with `--diff`: **no change** since
`19-14_layout_audit`, so the review ran against a deck confirmed current.

**Deliverable:** `06_thesis_writing/defence/slide-review/2026-09-20_deck-review-pass-01.md`
— slide-by-slide, with paste-ready replacement text, speaker-note bullets for the
four un-noted presented slides, and prepared answers for three probes the deck
invites.

Two verification agents ran in parallel against the thesis snapshot and the
results artefacts. Recorded as **F15**.

### What the pass established

**The numbers are sound.** All 21 cells of slide 21 match
`22_scenario_comparison.csv` exactly; all four rows of slide 23 trace to Ch9/Ch10.
Nothing in the evidence base needs changing.

**Ten defects found**, none of them measurement errors: a wrong citation year
(Saunders 2021 → 2023, where slide 8 already has it right), inflated screening
counts (~150/~60 → ~100/~40), a reference count matching nothing (61 vs 62 vs 42),
a memory figure stated three ways (34 / 34.5 / 35 MB), a misattributed framework
(Hevner et al. 2004 → Hevner 2007), an invented abbreviation (`MdAPE`), a
non-verbatim RQ presented in quotation marks, and two unsupported cells on slide 9.

**I corrected F12.** Its table reported 61 reference entries; the count missed
Klee & Xia, whose date is `(2025, July 30)` rather than a bare year. The list
holds **62**, so F12's headline — "the slide was right, my audit was stale" — was
itself wrong on the point it was correcting. The stale-snapshot lesson stands;
the exoneration of the 61 does not. **Enrico's comment was right to query it.**
Note added in place at F12 as well as in F15.

### The structural finding

**13 of the 15 noted slides carry a pasted figure caption, not speech.** The four
densest presented slides — 9, 15, 23, 25 — have no notes at all, while appendix
slides carry 81–89 words each. Alt text already holds each figure's provenance and
source path, so the captions are duplicated into the one field that cannot be
duplicated from anywhere else.

### Not done, surfaced as observations

- Reserve wall is 8 slides against the planned 20; all 20 artefacts verified
  present on disk, so the gap is authoring, not generation.
- Planned slide 06.x (the lag-12/13 provenance defect) was not built. Treated as
  a decision to confirm, not an omission — Ch9 §9.4 already states the defect.
- Three thesis-side defects found in passing (two missing references in Ch2 §2.5,
  a wrong cross-reference in §2.10, and Ch3 calling Ch2 "systematic" where Ch2
  says it is not). All unfixable post-submission; recorded so they are drilled
  rather than raised.

---

## Session 5 — 2026-10-10 — Deck finalisation pass (review pass 02)

Brian: finalise the deck; the two of them will split the speaking themselves. Asked
for help with the comments, speaker notes and fact-checking, **not** time
optimisation ("your estimates are always wrong") and **not** design ("we can do
that ourselves" — suggestions only).

**Currency:** deck snapshot `2026-10-10_16-39_finalise_and_divide` — slide content
identical to 20 Sept, only three new comments by Brian (slides 13, 23, 25). Thesis
snapshot `2026-10-10_16-42_deck-finalisation` — byte-identical to 20 Sept. Zotero
88 items (the client crashes in its sample-print on an item with no `year`, *after*
writing both exports). Repo `b9a97fc`, in sync.

**So pass 01 stands in full and none of its fixes are applied yet.**

**Deliverable:** `06_thesis_writing/defence/slide-review/2026-10-10_deck-review-pass-02.md`
— a follow-up beside pass 01, which stays frozen. Checklist of pass-01 items still
open; answers to the three comments; new findings; speaker notes for all 16
presented content slides, each bullet tagged with its thesis section; design
suggestions.

**New findings:**
- Slide 13 is an empty skeleton → delete.
- Slide 23: all four rows confirmed against Ch10 §10.1. Omits SRQ1's third clause —
  category specialisation (pooling wins on the two smallest panels by 4.5–5.7 pp,
  Ch9 §9.1.1).
- Slide 25 follows **Ch9** §9.4/§9.5, not Ch10. 9 of 10 faithful. Item 5 joins two
  unrelated limitations (planner decisions + hierarchical structure); splitting it
  surfaces the limitation→future-work pairing §9.5 is built on. "Asymmetry inside the
  substrate" is the lag-13 defect, already on the slide.
- Slide 20's "34 MB" comes from `generate_architecture_diagrams.py` formatting 34.5
  with `:.0f` — Python rounds half to even.
- Slide 4: Stackpole, Gartner, Newmark and Green (Forbes) are **not in the thesis**.
  Slide 5 names Royal Unibrew; the thesis names no client.
- **The deck never shows the five design principles (Ch9 §9.2.2, DP1–DP5)**, which
  the abstract lists as a contribution and which are DSR's "transferable design
  knowledge" that slide 15 promises. Also absent: §9.1.5's deployment
  recommendation.
- Design audit: **slide 15's third column overflows the slide by 0.42 in**; slide 9's
  table is entirely `-apple-system` (24 runs; MANIFEST's typography audit reported
  16 — an undercount worth checking in `deck_snapshot.py` later).

---

## Session 6 — 2026-10-12 — Defect-disclosure strategy decided

**Decision (Brian):** don't volunteer weaknesses; keep them in the limitations
slide and the appendix in non-prominent form. Rationale given: two peers'
defences went the same way, the supervisor is time-constrained, and the external
examiner has no forecasting/statistics background.

**Operationalised as "don't volunteer, never deny":**
- Slide 25 keeps "Forecasting Practice and Asymmetry inside the Substrate" as
  worded; the speaker note no longer says the lag defect out loud. A 20-second
  plain-English answer is held in reserve (pass-02 §4.16).
- No slide 06.x (the "what we applied / where the chain broke" slide stays unbuilt).
- ACF/PACF goes in the deck appendix under a neutral title ("Autocorrelation by
  brand"), not as "lag-12 evidence". Top-brands timeseries in the appendix too.
  ECDF and decomposition stay out.
- **Honesty floor:** if asked directly, answer plainly. The written record
  already discloses it (Ch9 §9.4), so the thesis is not hiding anything; the
  presentation simply doesn't lead with it.

**Residual risk, stated for the record:** Ch9 §9.4 states the defect, and an
AI-generated summary of the thesis is likely to surface a limitations section.
So "unlikely to be asked" is not "won't be asked" — the reserve answer must be
rehearsed.

The academically precise account stays in findings **F14** and **F16**; the
plain-English version was given to Brian in R-1012-01.
