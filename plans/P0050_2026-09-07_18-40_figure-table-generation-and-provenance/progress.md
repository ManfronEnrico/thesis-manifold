---
pid: P0050
created: 2026-09-07 18:40:00
updated: 2026-09-07 18:40:00
---

# P0050 — Progress

## Session log

### 2026-09-05 → 09-07 (carried over from P0046)

Traced every figure and table to a producer; rebuilt `PATHS.py` for the SRQ
tiers; moved the root anchor off `CLAUDE.md`; archived stale artefacts with
recovery READMEs; reshaped SRQ1 into `figures/ tables/ models/`; promoted 149
EDA artefacts; rebuilt the diagram set after finding it depicted a system that
was never built (F1).

Added `run_manifest.json` and per-step content metrics to the preprocessing
pipeline, and made the appendix consume both. Clean-slate re-run: 4 categories ×
2 horizons, 8 runs, all passing.

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
