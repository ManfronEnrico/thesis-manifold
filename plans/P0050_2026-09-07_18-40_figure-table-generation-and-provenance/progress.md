---
pid: P0050
created: 2026-09-07 18:40:00
updated: 2026-09-07 18:40:00
---

# P0050 — Progress

## Session log

### 2026-09-05 → 09-07 (carried over from P0046, now archived)

Traced every figure and table to a producer; rebuilt `PATHS.py` for the SRQ
tiers; moved the root anchor off `CLAUDE.md`; archived stale artefacts with
recovery READMEs; reshaped SRQ1 into `figures/ tables/ models/`; promoted 149
EDA artefacts; rebuilt the diagram set after finding it depicted a system that
was never built (F1).

Added `run_manifest.json` and per-step content metrics to the preprocessing
pipeline, and made the appendix consume both. Clean-slate re-run: 4 categories ×
2 horizons, 8 runs, all passing.

**Two live bugs were fixed as side effects of the path work**, both worth knowing
about because they sat in code other plans also touch:

- **Scenario C could not start.** `srq4_experiment.py` loaded its forecast tool
  from `model_serving_interface/scenario_c_forecast/`, a directory the
  restructure removed — it would have raised `FileNotFoundError` at import.
  Now `SRQ2_DIR / "forecast_tool.py"`, and it fails with a message naming the
  missing file rather than a traceback. Verified still in place 2026-09-07
  (`srq4_experiment.py:147`).
- **`fig1_model_ladder` rendered empty** under a title asserting a result the
  data contradicted (a grain-tag mismatch selected zero rows). The chart now
  raises if the filter is empty, and the title is derived from the data.

Also: `requirements.txt` was missing `graphviz`, `matplotlib` and `statsmodels`,
so a fresh clone could reproduce **no figure at all** (F4).

### 2026-09-07 — chapter figures and the style pass

Built the six chapter figures Brian asked for, plus the literature → design map.
Then a full style pass after his review.

**Delivered**

| Artefact | Facts read from |
|----------|-----------------|
| `ch1_research_questions_tree_v2` | the current research-question set |
| `ch2_gap_diagram_v2` | §2.7's four literatures + the RAM constant |
| `ch4_data_pipeline_v1` | each category's own step-4 execution log |
| `ch4_eda_pipeline_csd_v1` | section names read off the EDA's own tables |
| `ch5_tool_interface_v1` | a deployed model's own record |
| `ch6_modelling_pipeline_v1` | metrics, profiling, metadata, pooled CSVs |
| `89_literature_design_map` | parsed from Ch2 + a curated design column |

**Style contract written and applied.** `.claude/rules/figure-generation-standards.md`:
horizontal layouts, bold box headers, no step numbers, greyscale contrast tiers,
transparent backgrounds, submission-ready captions, values read from artefacts,
and "open the rendered file and look at it".

All eleven figures now comply. Checked mechanically: a regex over the rendered
SVGs for filenames, step numbers, plan IDs and internal variant tags
(`(tuned)`, `(unclipped)`) returns **zero** hits. All eleven are horizontal.

**Corrected against the code** — three claims that read as measured but were not:
the 8 GB envelope (it is 4 GB), Ch5's "five lightweight models" and its agentic
layer (the ladder is four; the layer does not exist), and "18 EDA sections"
(counted: 16). See F10.

**Caught and fixed a collision I introduced**: the new literature table at prefix
`89` was being silently deleted by `export_appendix.py`'s cleanup bound of
`<= 89`. It survived only by the order I happened to run things in (F6).

**Verification**: 5 producers run clean in any order; 11 diagrams; 25 appendix
tables; 195 live scripts compile; `PATHS OK`.

### 2026-09-07 (later) — chapter prefixes, and the tier-05 restructure scoped

Brian: `appendix/` is an artefact of earlier table generation; tier 05 should
mirror the thesis, chapter by chapter, so he can decide later what goes in the
appendix. **DEC-CHAPTER-FOLDERS.**

**Deliberately not started.** He is reworking the Word export so headings carry
their numbers ("Chapter 2 | Literature Review"), and the folder names should come
from that export rather than from a guess at the numbering. Scoped in F19, with
the two routing conflicts that make "file it where it originates" insufficient:
`export_appendix.py` is cross-cutting rather than scenario-specific, and the
holiday tables split Ch4 (source) from Ch6 (ablation).

**Done now, since it is independent of the numbering:** all eleven diagrams carry
a chapter prefix. The five that lacked one were renamed by what each figure
*shows* — read from its body, not inferred from its name. `_check_stem()` now
enforces the convention and raises on a stem without `ch<N>_`.

The guard caught the case that mattered: `fig_resource_profile` saves through
matplotlib rather than `_save()`, so a check placed only in `_save()` would have
missed exactly the figure whose predecessor carried fabricated numbers.

Verified: guard rejects 3 bad stems and accepts 2 good ones; 11 diagrams
regenerate; no unprefixed file remains; live consumers repointed (the Ch5 draft
had **two** stale references, one of them still naming the archived
`ch5_architecture_v1`).

### 2026-09-07 (evening) — chapter-keyed tier 05, and the diagram polish pass

**Diagrams finished.** Chapter prefixes on all eleven, enforced by
`_check_stem()`. Captions centred, PNG output dropped (SVG is vector and pastes
into Word; the twin was the lower-quality copy). Cluster fill darkened to
`#878787` with a black label so nesting reads. EDA groups switched to bulleted
lists — left-aligned text in a centred block, via a nested table. Ch5 and Ch7
scenario labels aligned to the repository's own A/B/C/D/E vocabulary, then Ch5
generalised to "Plain agent / Agent + data & code / Agent + models" so it covers
all five scenarios without duplicating Ch7's mapping (F24).

**Aspect ratios measured against A4.** Nine of eleven now fit a portrait column
or a landscape page. `ch4_data_pipeline_v1` went 4.4 → 1.16 by folding its two
phases into a stack. `ch4_preprocessing_pipeline_v2` (4.45) is the sole outlier
and is superseded in substance by `ch4_data_pipeline_v1` — a Phase 5
retire-or-fix decision, not a layout fix (F22).

**`_stack()` replaced clusters where order matters** after seven attempts to
constrain graphviz's ordering each failed differently (F23). Two of those
failures were silent: `rank="same"` across clusters re-parents its members and
the cluster boxes vanish with no error, which was also the cause of the
"contract box escaping its outer box" bug — graphviz had been warning about it
and the warning was being filtered out of the output.

**Tier 05 restructured to chapter folders** (F25). `01_introduction` …
`09_discussion`, each with `figures/ tables/ models/`. The SRQ folders,
`appendix/` and `diagrams/` are gone; quarantined material is in `.archive/`.

The move cost far less than the ~30 producer scripts suggested, because most
already went through `get_srq_*_dir()` — repointing three helpers moved ~25
scripts untouched. The ones that needed editing were exactly those that had
built paths inline.

Folder numbers are **derived** from position in `CHAPTER_SLUGS` via one private
helper, so reordering the tuple renumbers the tree. Verified against Brian's own
proposed swap.

**Two near-misses worth recording:**

- `srq1_model_performance/` reappeared after the move with four `cv_*` files. I
  nearly deleted it as leftover — they turned out to be **19 hours newer** than
  the chapter-folder copies (a benchmark had run mid-session and written through
  the old path). Merged the newer ones in. Compare before deleting.
- The draft image references were repointed to `introduction/` *before* the
  numeric prefixes were added, leaving three **broken links** that resolved to
  nothing. Caught at end-of-day by re-resolving every image path in the drafts.

---

## Next session starts here

**Phase 5 — publish the inventory, THEN choose citations** (F2, never the
reverse):

1. Publish the complete regenerable inventory — 11 diagrams, 25 tables, 4 SRQ1
   figures, 149 EDA artefacts, each with its producer.
2. Decide per artefact: in-text, appendix, or neither.
3. **Then** audit the draft's existing figure references against it.
4. Decide the 18 `analysis/figures*` on regenerability — they are Enrico's
   archived notebooks and have no live producer.

**Then** Phase 6 (MANIFEST + invariant checks) and Phase 7 (style pass on the
matplotlib figure).

### Environment

The diagram generator needs Graphviz's `bin` on PATH — winget installed it but
did not add it:

```powershell
$env:PATH += ";C:\Program Files\Graphviz\bin"
```

### Blocked, not by this plan

The reduction table's "Horizon (months)" column carries a DO-NOT-PUBLISH warning
until P0049's horizon fix lands. Nothing else here depends on it.

### Deferred deliberately

Modelling-layer provenance (F8) — real, but it is our audit trail rather than a
blocker on any thesis artefact, and every tier-05 artefact already has a verified
live producer.

### Still uncommitted

Several sessions of moves, rewrites and regenerated artefacts. **Worth committing
before further work** — and especially before the account switch.

---

## Session 2026-09-10 — provenance audit after the HPC re-run

Triggered by Brian: *is everything in `05_thesis_results/` computed, with no
hardcoded literals?*, asked because a high-performance-cluster re-run had added
the holiday enrichment. It was not. Four separate classes of problem, all now
fixed at the producer rather than in the output.

### Delivered

| | |
|---|---|
| **Three stale literals** now computed | F26 — ridge-alpha spread, split ratios, plateau tolerance |
| **Three superseded figures** regenerated | model selection had moved energidrikke XGBoost → LightGBM |
| **Three orphan SVGs** deleted | Ch5/Ch6 swap leftovers no producer emits |
| **63 PNGs → SVG** | 3 producers + the promotion step; every deletion has a replacement |
| **24 internal-note blocks** moved out of tier 05 | one sidecar per table under `writing-notes/` |
| **Backgrounds white**, not transparent | 5 call sites + the standards rule |
| **New methodology figure** | parses ch3 prose; ratio 2.71 |
| Category casing normalised | `RTD, energidrikke` → `Energidrikke, RTD` |

Nine producers now run clean end to end, `PATHS.py` included.

### What each question turned up

**"Is it all dynamic?"** Three typed values had gone stale (F26). The worst was
not a literal at all: three figures still named the pre-re-run model selection,
because the generator was right and its output had simply never been rebuilt.

**"Was `cv_summary.md` regenerated on the HPC?"** Yes — and my first answer
saying otherwise was wrong (F27). Its numbers matched the source CSV exactly;
only the plateau sentence was wrong, which was the generator defect. Regenerated
from stored CSVs without re-running the hours-long benchmark.

**"Why are there still PNGs?"** Because there were 33, not the 3 first reported,
and a *second* hardcoded `glob("*.png")` in the promotion step silently discarded
the SVGs on the first conversion attempt (F28).

**"Are the metanotes out of the submitted repo?"** They are now — and the follow-up
question caught a real defect: `review_notes.py` first lived in `utility_scripts/`,
which the submission export deletes, so all four importing producers would have
failed on import in the submitted repo. Moved to `05_thesis_results/` (F28).

**"Is model selection dynamic, and does it still hold?"** Yes to both, verified by
recomputing it independently from `cv_metrics.csv` (F29). Worth carrying into the
prose: energidrikke and RTD are decided by 0.7 and 0.4 points.

### Near-misses worth keeping

- **A generator that is correct can still have stale output.** Nothing in the repo
  reported the gap between the two; mtime actively pointed at the wrong file,
  since the orphans were newer than their replacements.
- **A dangling graphviz edge endpoint creates an empty node instead of erroring.**
  Renaming a node left an edge pointing at the old name and a blank box rendered.
  Caught by looking at the render, not by the run.
- **`git status` showed 66 deletions.** Verified before proceeding: 63 PNGs each
  with an SVG replacement, 3 orphans. Nothing lost.

### Deliberately not done

The methodology figure is **not yet cited** anywhere in the prose — that belongs
to Phase 5, which owns citation decisions across the whole inventory.

`cv_summary.md`'s numbers were left as they are: they are current, and re-running
the benchmark to refresh a timestamp would be hours of compute for no change.

### Still uncommitted

Everything above, plus the earlier sessions' work. Now a large diff (~66 deletions,
~64 modifications, ~65 new files, most of them the SVG replacements).

---

## Session 2026-09-10 (later) — the requirement restated, and what it reopens

Brian corrected a misread. Recorded as its own entry because the previous entry
reports a fix to the wrong problem, and a future session reading only that entry
would think the matter closed.

### The correction

The rule is about **content anywhere in tiers 01-05**, not about which tree the
submission export deletes:

> "I only want any output in `05_thesis_results/` to be submission ready, meaning
> only descriptions that are meant to be read by the reader of the thesis / the
> assessors."

And producer location is explicitly free: *"the scripts ... can also live in the
same folder at root. I don't mind honestly. As long as they all consume actual
sources and dynamically re-generate the appendices."*

So the `review_notes.py` relocation and `DEC-SHIPPED-IMPORTS`, reported last
entry as the answer, were a real fix to a question that was not asked (F32).

### What this reopened

Phase 3d stopped at the `INTERNAL REVIEW` **marker**. Searching for a marker
finds the notes that were honest about being notes; it cannot find a sentence
that reads as ordinary prose and happens to cite a plan file. Measured after the
correction: **8 lines, 6 files, 5 producers** still carrying plan IDs and
internal decision codes into tier-05 output.

`training_report.md` is the worst of them, with three separate leaks in prose an
assessor would read as ordinary methodological explanation.

### Written, not executed

Phase 8 added to `task_plan.md` with four parts: refile the notes per chapter
(8a), sweep tiers 01-05 for unmarked internal content (8b), make the invariant a
check rather than a memory (8c), and revisit the two decisions the previous
session overstated (8d). F32 and F33 record the reasoning.

**Nothing in Phase 8 has been executed** — Brian asked for the plan first, then a
compaction, then the work.

### One question to put to Brian before 8a runs

The existing note folders are `ch4_data_assessment`, `ch5_model benchmark` (a
space, not an underscore), `ch6_architecture`, `ch7_synthesis`, `ch8_experiment`.
None match `CHAPTER_SLUGS`; two abbreviate; one has a space; and the two chapters
that own tables but have no folder (literature review, methodology) would need
new ones. These are folders Brian and Enrico open by hand, so **ask before
renaming** rather than normalising them on the way past.

### Still uncommitted

Everything from both of today's sessions. ~67 new files, ~66 deletions, ~68
modifications, most of them the PNG-to-SVG replacements.

---

## Session 2026-09-10 (Phase 8) — executed

Brian answered the folder question ("just create a chapter folder if you are
missing one, orient yourself on the chapter names not the numbers") and asked for
the rest to run unattended. All four sub-parts are complete.

### What was built

`05_thesis_results/check_reader_facing.py` — the invariant as a check rather than
a habit. Seven patterns over every `.md` and `.csv` in the results tree, exit 1
on any hit, each hit naming which class it matched. Every appendix producer calls
`warn_after_run()` at the end of its own run.

`PATHS.get_chapter_notes_dir()` / `get_chapter_generated_notes_dir()` — editorial
notes filed by chapter, folder name derived from `CHAPTER_ORDER`.

`review_notes.chapter_of()` — derives the owning chapter from the artefact's own
output path rather than taking it as an argument, so a table and its note cannot
end up in different chapters.

### What was verified, not assumed

- Planted one line of each leak class; all five caught, exit 1
- Planted a leak and ran a producer; the mid-run warning fired
- `comm` over the flat and per-chapter listings before deleting anything: 24
  against 24, zero orphans
- All seven producers re-run end to end after the `_save` signature change

### Two corrections to what I reported earlier

**The leak count was 9 across 8 files, not 8 across 6** (F34). The two extra were
bare finding numbers reading as ordinary prose -- the same class of miss that
created F32, recurring inside the fix for F32.

**`ch5_model benchmark` has an underscore, not a space** (F35). I reported it as
a space twice, including as a reason renaming might be needed. Nothing was
renamed; all five existing folders already matched the derived name.

### Judgement calls

`warn_after_run()` warns rather than raising. A generator that has just written
15 correct tables should not exit non-zero over one sentence, and the run that
finds a leak is rarely the run that introduced it. The standalone check is the
one that fails.

Three SRQ1 outputs could not be regenerated without refitting models. The
identical substitution was applied to their `.md` files, checked
character-for-character against what the fixed producer now emits, so the next
real run is a no-op rather than a revert.

`.py` files and `.archive/` folders are deliberately out of scope -- source
comments are a different audience, and archive READMEs exist to record which plan
retired an artefact.

### Still uncommitted

Everything from all three of today's sessions.
