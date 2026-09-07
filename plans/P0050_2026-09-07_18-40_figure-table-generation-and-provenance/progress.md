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
