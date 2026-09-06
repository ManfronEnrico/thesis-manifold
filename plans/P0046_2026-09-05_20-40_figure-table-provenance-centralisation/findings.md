---
pid: P0046
created: 2026-09-05 20:40:00
updated: 2026-09-06 19:00:00
---

# P0046 — Findings

> Condensed 2026-09-06 from 946 lines. Superseded findings are dropped, not
> archived — the decisions they led to are in `task_plan.md`. Full history in git.

---

## The artefact map — where everything is now

| Group | Was (pre-09-06) | Now | Count | Regenerable |
|---|---|---|---|---|
| Appendix tables | `04_thesis_results/appendix/` | `05_thesis_results/appendix/` | 25 | **YES, tested** |
| SRQ1 results | `04_thesis_results/srq1/` | `05_thesis_results/srq1_model_performance/` | 37 | **YES, tested** |
| SRQ1 figures | `…/srq1/figures/` (4) | same, minus zombie | 3 | **YES, tested** |
| SRQ2 results | `04_thesis_results/srq2/` | `…/srq2_structured_tool_interface/` | 5 | **NO — zero producers** |
| SRQ4 aggregation | `04_thesis_results/srq4/` | `…/srq4_scenario_experiments/` | 5 | yes (paid re-run) |
| SRQ4 runs + raw | `…/srq4/{run_*,raw_responses}` | `04_SRQ4_Scenario_Experiment/runs/` | 4 dirs | n/a — raw evidence |
| Conceptual diagrams | `05_thesis_writing/figures/` | `05_thesis_results/diagrams/` | 1 of 6 | **BLOCKED — system `dot`** |
| EDA `.md` + `.png` | pipeline outputs | still there, promotion pending | 119 + 30 | yes (pipeline) |
| EDA `.csv` | pipeline outputs | **stays** (DEC-EDA-SPLIT) | 119 | yes (pipeline) |
| Enrico notebook figures | `05_thesis_writing/analysis/` | `06_thesis_writing/analysis/` | 18 | **NO — archived notebooks** |
| Triage figures | `05_thesis_writing/figures/{unsure,update_*}` | `06_thesis_writing/figures/…` | 12 | 6 pairs from the diagram generator |

**Nothing was lost.** Every artefact is accounted for.

### Archived this session (never deleted — DEC-ARCHIVE-NOT-DELETE)

| Item | To | Why |
|------|----|-----|
| `fig2_granularity.png` | `srq1_model_performance/.archive/zombie_…_2026-09/` | F1 |
| `phase3_result.json` | `05_thesis_results/.archive/phase3_region_grain_2026-09/` | producer archived by P0035 |
| `generate_systemB_diagram.py` | `05_thesis_results/.archive/systemb_…_2026-09/` | F4 |
| shadow copy of same | `.archive/shadow_scripts_2026-09/` | byte-identical duplicate |
| `ml_retraining/` (11 scripts) | `.archive/ml_retraining_2026-09/` | F5 |
| SPSS / Indeks Danmark | `.archive/spss_indeksdanmark_2026-09/` | F6 |

Each carries a README: what it is, why it moved, how to recover it.

---

## F1 — The zombie: `fig2_granularity.png`

The most dangerous artefact found, because it looked correct — right folder,
right name, same 2026-07-11 date as its legitimate siblings. It depicts a
brand-vs-chain grain comparison DEC-GRAIN (2026-07-12) decided to stop making.
P0035 deleted the producing code; `srq1_generate_performance_figures.py` still
carries the note *"fig2_granularity.png is no longer produced."* The image
outlived its producer by two months.

Verified before archiving: committed at git `4c7a98b`; **cited by zero
chapters**; re-running the producer yields 3 figures and does not recreate it.

**The general lesson**: a tidier folder tree would not have caught this. Only a
producer→artefact mapping does. That is why Phase 6's invariant is *every
artefact has a live producer*, not *every folder is neat*.

## F2 — 32 of 34 PATHS constants were silently dead

The 2026-09-06 SRQ restructure broke every tier constant. `import PATHS`
still succeeded because `Path()` never validates — nothing fails until a script
reads or writes.

**This vindicated DEC-PATHS more sharply than tidiness ever could**: one file
needed repair instead of forty, and a single probe enumerated the blast radius.
Constants for genuinely-removed directories (`THESIS_MODELLING_SERVING_*`,
`THESIS_DATA_ASSESSMENT_DIR`, the four SPSS ones) were **removed, not
repointed** — a constant aimed at a missing path is how this went unnoticed.

Now: 39/39 resolve, `print_all_paths()` clean.

## F3 — Hardcoded paths: 43 scripts → 10

Audited every live `.py` for five defect classes. All 77 compile. The `CLAUDE.md`
→ `.env.example` anchor swap (Brian: the repo ships to assessors and shouldn't
name the assistant) exposed two defects that were *not* the anchor:

1. **`.gitignore`'s `.env.*` excluded `.env.example`.** An uncommitted anchor
   cannot anchor a fresh clone — the swap would have been *worse* than
   `CLAUDE.md`, which was at least committed. Fixed with `!.env.example`.
2. **Every inline finder walked from `Path.cwd()`, not `__file__`** — so the root
   depended on where python was invoked, and runs from outside the repo failed.

`parents[N]` hops replaced in 17 scripts: they encode folder *depth*, which the
restructure changed — same silent-breakage class as F2, one level down.

**The 10 survivors are all legitimate**: `PATHS.py`'s own literals (it is the
authority), a docstring about the old anchor, `thesis_snapshot.py`'s OneDrive
default (outside the repo by nature), two sibling-relative `parents[1]` uses, and
3 scripts already dead from importing a long-removed module.

The rule is now a check, not an intention: *no live script contains a literal
tier name, a `CLAUDE.md` anchor, or a `parents[N]` repo-root hop.*

## F4 — `generate_systemB_diagram.py` drew the abandoned writing system

Brian's suspicion about "System A/B" scripts was right and sharper than expected.
It renders a multi-agent **thesis writing** system — Thesis Coordinator, Writing
Agent ("Bullet points only (never prose)"), Critic Agent, APA Citation Agent —
the abandoned promise, not the SRQ2/SRQ4 artefact the thesis presents.

Searching its output name `system_b_overview` returned three files: the script,
its shadow copy, and this plan. **Zero chapters.** Archived with a README.

`generate_architecture_diagrams.py`'s six diagrams are different — they depict
real architecture and are worth *updating*, not dropping.

## F5 — `ml_retraining/` archived rather than repointed

11 scripts reading `results/phase1/`, `data/raw/`, and `Thesis/indeksdanmark` —
none of which exist (`Thesis/` went in P0028). Repointing would have manufactured
PATHS constants for folders nobody maintains: the exact failure this plan
removes, and the same reasoning that deleted the serving constants in F2.

## F6 — SPSS dropped; the abstract still claims it

Indeks Danmark was never used. Data archived, four constants removed (three
already resolved to nothing).

**Open item**: the abstract still names it as part of the empirical base — twice,
in the authoritative `.docx`. That is a claim about *what data the study rests
on*, in the section examiners read first. Verified scope: **abstract only** (Ch3
and Ch4 are clean), so it is a two-sentence correction. Tracked at
`06_thesis_writing/writing-notes/indeks-danmark-claim-must-be-corrected.md`.

## F7 — Regenerability tested, not assumed → a reproducibility defect

Every free generator was **run**, not inspected.

| Generator | Result |
|-----------|--------|
| `export_appendix.py` | PASS — 12 tables, byte-identical bar the timestamp |
| `srq1_generate_performance_figures.py` | PASS — 3 figures |
| `srq1_generate_shap_figures.py` | PASS after installing `shap` |
| `training_report.py` | PASS |
| `generate_architecture_diagrams.py` | **FAIL — system `dot` missing** |

`requirements.txt` omitted `graphviz` entirely (undeclared *and* uninstalled),
plus `matplotlib` and `statsmodels` (undeclared, coincidentally present). **An
assessor cloning the repo and running `pip install -r requirements.txt` could
reproduce no figure at all** — a defect in the deliverable, not a convenience
issue, and invisible to code reading. Now declared, with a comment warning that
the Python binding alone is insufficient: graphviz needs a system `dot`.

Also fixed: `export_appendix.py`'s generated README hardcoded a producer path
dead since the restructure — the index told readers to run a script that no
longer exists. Now derived from `Path(__file__).relative_to(ROOT_DIR)`.

## F8 — SRQ2's results are entirely orphaned

| File | Date | Status |
|------|------|--------|
| `judge_scores.csv` | 07-10 | LLM-as-Judge — **dropped design** |
| `recommendations.csv` | 07-10 | judge era |
| `llm_summary.md` | 07-11 | judge era |
| `synthesis.csv` | 08-19 | synthesis engine |
| `synthesis_summary.md` | 08-19 | synthesis engine |

Searching `THESIS_RESULTS_SRQ2_DIR` across live code returns **zero producers** —
only `PATHS.py` and four archived copies. Brian flagged the judge files; the
finding is broader: *all five* are orphaned, because the synthesis scripts were
archived in the August reorganisation too.

Two distinct problems: 3 files describe a **dropped design** (same class as the
zombie); 2 may be **valid results nothing can reproduce**. Phase 5's citation
sweep decides restore-vs-archive.

## F9 — `05_thesis_results/srq1_model_performance/` is not yet browsable

33 loose top-level files — `metrics.csv` beside `tuned_metrics.csv` beside
`cv_metrics.csv`, nothing saying which a chapter should cite — while `figures/`
holds 3. Since tier 05 is now the tree humans browse to pick artefacts,
centralising the destination without imposing a shape inside it relocates the
disorder rather than fixing it. Target: `figures/ tables/ models/` (no `raw/` —
raw material never reaches this tier).

## F10 — Generator names now state what they emit

`generate_figures.py` said nothing about *which* figures, and sat beside
`srq1_figures.py`, which produced entirely different ones.

| Was | Now |
|-----|-----|
| `generate_figures.py` | `generate_architecture_diagrams.py` |
| `srq1_figures.py` | `srq1_generate_performance_figures.py` |
| `srq1_shap.py` | `srq1_generate_shap_figures.py` |

`export_appendix.py` and `training_report.py` already said what they do.
References updated in `README.md`, `CHEATSHEET.md`, `repository_map.md`,
`requirements.txt`.

## F11 — Enrico's 18 notebook figures (unresolved)

`06_thesis_writing/analysis/figures/` (11) and `figures_agentic/` (7) trace to
archived notebooks that hardcode `/Users/enricomanfron/Desktop/…`. They are
**archived, not broken** — the blockers are edits, not rewrites. Per-file
RESTORE or RETIRE after the citation sweep, with the pairing rule that RETIRE
archives the *image* too: a stale image left beside a retired producer is exactly
the F1 trap.

## F12 — `ram_budget_v1` must not be naively re-run

The diagram generator still holds P0040-F5's fabricated numbers. Real
measurements now exist in `05_thesis_results/appendix/`
(`02_substrate_resource_profile`, `04_sandbox_resource_profile`). Rewire before
regenerating, or the fabrication is reproduced.

---

## Open questions

1. **SRQ2 restore-or-archive** (F8) — needs the Phase 5 citation sweep.
2. **The 18 `analysis/figures*`** (F11) — same.
3. **Abstract correction** (F6) — Brian's prose call, in the `.docx`.
