---
pid: P0046
created: 2026-09-05 20:40:00
updated: 2026-09-06 19:00:00
status: in_progress
focus_detail: "Phases 1-3 complete. Repo restructured to SRQ tiers; PATHS.py rebuilt (39/39 resolve); every live script routes through PATHS; generators renamed and tested. BLOCKER: system graphviz `dot` not installed -> 6 diagrams unbuildable. Next: Phase 3b (SRQ1 folder shape, SRQ2 orphan triage, EDA promotion)."
---

# P0046 — Figure, Table & Graph Provenance and Centralisation

## Goal

Every figure, table and diagram that could enter the thesis must be either
**regenerable** (a live script reproduces it from current data) or
**deliberately hand-made** (a conceptual diagram whose staleness is a human
judgement). Anything else cannot be defended. Then: one predictable location,
one consistent style.

---

## STATUS QUO (2026-09-06) — read this first

### Architecture, settled

| Rule | Decision |
|------|----------|
| **Ships to assessors** | tiers `01_SRQ1_*` .. `05_thesis_results/` |
| **Excluded** | `00_thesis_context/` + `06_thesis_writing/` (AI-writing harness) |
| **Artefacts live once** | all in `05_thesis_results/`; tier 06 holds NO figures/tables |
| **Routing** | producer tier decides: data→`01_`, modelling→`01_`, scenarios→`04_`, general diagrams→`05_` |
| **Raw runs** | live with their experiment, never in results |
| **EDA split** | `.csv` stays at pipeline (downstream steps read it); `.md`+`.png` promote |
| **Paths** | no literal tier name / `CLAUDE.md` anchor / `parents[N]` hop in any live script |
| **Root anchor** | `.env.example` → `.env` → `PATHS.py`, walked from `__file__` |

### Regenerability — TESTED by running, not assumed

| Generator | Emits | Status |
|-----------|-------|--------|
| `export_appendix.py` | 25 appendix files | **PASS** (byte-identical) |
| `srq1_generate_performance_figures.py` | 3 figures | **PASS** |
| `srq1_generate_shap_figures.py` | shap png + csv | **PASS** (after adding shap) |
| `training_report.py` | training_report.md | **PASS** |
| `generate_architecture_diagrams.py` | 6 diagrams | **BLOCKED — system `dot` missing** |
| SRQ2's 5 result files | — | **NO PRODUCER** — all archived (F28) |
| 18 `analysis/figures*` | — | **NO PRODUCER** — Enrico's archived notebooks (F12) |

### The one blocker

`winget install Graphviz.Graphviz` (then reopen the shell so `dot` is on PATH).
The Python binding is installed and declared; only the system executable is
missing. Until then `05_thesis_results/diagrams/` holds 1 of 6 diagrams.

---

## Phases

### Phase 1 — Trace and classify — `complete`
7-8 live producers, not 70. Findings F1-F10.

### Phase 2 — Decide the target layout — `complete`
Superseded same-day by F14-F22 (see Decisions).

### Phase 3 — Centralise paths — `complete`
- PATHS.py rebuilt for SRQ tiers; 39/39 constants resolve
- `CLAUDE.md` → `.env.example` anchor across 7 scripts + shared finder
- `parents[N]` hops replaced in 17 scripts
- `zotero_client.py`, `thesis_snapshot.py` repointed
- 77 live scripts compile; audit 43 flagged → 10 (all legitimate, F25)
- Generators renamed to say what they emit (F30)
- `requirements.txt`: added `graphviz`, `matplotlib`, `statsmodels` (F27)

### Phase 3b — Staleness triage + per-SRQ shape — `in_progress`

- [x] Archive (not delete): zombie figure, phase3 leftover, System B generator,
      shadow copy, `ml_retraining/`, SPSS data — each with a recovery README
- [ ] **Install system graphviz**, then re-run the diagram generator
- [ ] **SRQ2 orphan triage** (F28) — 5 files, zero live producers. 3 are
      LLM-as-Judge (dropped design), 2 are synthesis outputs possibly still
      valid. Needs Phase 5's citation sweep to decide restore vs archive.
- [ ] **SRQ1 folder shape** — 33 loose top-level files → `figures/ tables/ models/`
- [ ] **Promote EDA** — 119 `.md` + 30 `.png` → `05_thesis_results/eda/{category}/`

### Phase 4 — Regenerate and reconcile — `pending`
- [ ] Add `ch1_research_questions_tree` to the diagram generator (F18)
- [ ] **Hold**: `ram_budget_v1` still carries P0040-F5's fabricated numbers —
      rewire to the real appendix measurements before re-running (F5)
- [ ] Update graphviz labels so `system_architecture_v1` / `data_flow_v1` are current
- [ ] Fix broken `![](../figures/...)` references in drafts

### Phase 5 — Citation sweep + validate in-text tables — `pending`
- [ ] Which figures/tables do chapters actually cite? (unblocks F12 + F28)
- [ ] Fill the 18-row restore-or-retire table
- [ ] Diff in-text tables against artefacts; record mismatches, don't silently "fix"

### Phase 6 — Manifest + invariant checks — `pending`
- [ ] `05_thesis_results/MANIFEST.md`: artefact → producer → source → citing chapter
- [ ] Check: every tier-05 artefact has a live producer
- [ ] Check: `PATHS.py` self-test asserting every `*_DIR` exists
- [ ] Check: no live script holds a literal tier name (the F25 audit script)

### Phase 7 — Style pass — `pending`
- [ ] Shared matplotlib style; DPI/font/palette consistency
- [ ] Export format policy (PNG for Word, SVG retained)
- [ ] Generalise `export_appendix.py`'s table conventions to every generator

---

## Decisions

| ID | Decision | Date |
|----|----------|------|
| DEC-P0046-TAXONOMY | Split "orphan" into CONCEPTUAL (no dataset, fine) vs DERIVED (chart of numbers, must have a producer) | 09-05 |
| DEC-P0046-SINGLE-HOME | Tier 06 holds no artefacts; everything lives once in `05_thesis_results/`. Removes the second copy rather than policing it | 09-06 |
| DEC-P0046-SHIP-SCOPE | Tiers 01-05 ship; 00 and 06 are the writing harness and are excluded | 09-06 |
| DEC-P0046-SRQ-TIERS | Top-level folders map 1:1 onto research questions | 09-06 |
| DEC-P0046-SLUGS | Results folders carry descriptive slugs (`srq1_model_performance`, …) | 09-06 |
| DEC-P0046-ROUTING | Producer tier decides where a script lives; tier 05 always receives | 09-06 |
| DEC-P0046-RUNS-WITH-EXPERIMENT | Raw per-run material stays with its experiment; only aggregation reaches results | 09-06 |
| DEC-P0046-EDA-SPLIT | `.csv` stays at pipeline, `.md`+`.png` promote — split by what consumes each | 09-06 |
| DEC-P0046-PATHS | Every output path resolves through `PATHS.py`; stated as a greppable check | 09-06 |
| DEC-P0046-ANCHOR | Root anchor is `.env.example`, walked from `__file__` | 09-06 |
| DEC-P0046-ARCHIVE-NOT-DELETE | Stale artefacts move to level-appropriate `.archive/` with a README, never deleted | 09-06 |
| DEC-P0046-DROP-SPSS | Indeks Danmark archived; leaves an open abstract correction (F23) | 09-06 |
| DEC-P0046-ORPHAN-EXIT | ORPHAN-DERIVED files get per-file RESTORE or RETIRE after the citation sweep | 09-05 |
| DEC-P0046-NAMES | Generator filenames state what they emit, not that they "generate" | 09-06 |

---

## Open items

1. **System graphviz install** — the only hard blocker.
2. **Abstract correction** (F23) — the thesis claims Indeks Danmark as an
   empirical source; it was never used. Note at
   `06_thesis_writing/writing-notes/indeks-danmark-claim-must-be-corrected.md`.
   Prose edit, `.docx`, Brian's call.
3. **SRQ2 restore-or-archive** (F28) — blocked on Phase 5.
4. **18 `analysis/figures*`** (F12) — blocked on Phase 5.
5. **P-ID collision** — a second `P0046_..._exogenous-enrichment-decision/`
   folder exists; one should be renumbered.

## Errors

| Error | Resolution |
|-------|------------|
| `grep -rn` over repo times out at 120s (3 sessions running) | Z: is slow on full-tree walks. Use the Grep tool. Logged repeatedly and still reached for `grep` — worth a `/errors-log` entry |
| Bulk-edit scripts broke syntax twice (block inside a function; paren after a comment) | The compile sweep caught both immediately. Keep it as a gate on any bulk edit |
