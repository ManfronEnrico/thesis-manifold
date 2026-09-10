---
pid: P0054
created: 2026-09-10 15:35:00
updated: 2026-09-10 15:35:00
status: in_progress
focus_detail: "Designing the export procedure + /submission-export skill. Nothing executes until the thesis repo is frozen."
---

# P0054 — Submission-ready repository export

## What this produces

A **separate, clean repository** containing only what a CBS assessor needs to
read the code alongside the thesis document and, in principle, re-run the
pipeline. The working repository is untouched: the export is a one-way
transform into a new folder, never an in-place cleanup.

**Two deliverables, both built now, executed later:**

1. `.claude/skills/submission-export/SKILL.md` — the repeatable procedure
2. A manifest file (`submission_manifest.yaml`) listing every path as
   `ship` / `drop` / `rewrite`, so the decision set is reviewable in one place
   rather than re-derived each run

## Why a separate repo, not an in-place clean

Three reasons, and the first is decisive:

- **The meta-comments are load-bearing for us.** `DEC-GRAIN`, `P0035`, `F63`
  are how this project has avoided re-litigating settled decisions for five
  months. Stripping them from the working repo destroys that. Stripping them
  from a *copy* costs nothing.
- **Git history is itself meta.** 500+ commits saying "docs: close chapter 4",
  "fix: zotero export dropped computerProgram" narrate a Claude-assisted
  workflow. The export starts a fresh history with one initial commit.
- **Reversibility.** If an assessor asks a question the stripped comment
  answered, the working repo still has the answer.

---

## Phase 0 — Preconditions (gate; do not start before all four hold)

| # | Precondition | Check |
|---|---|---|
| 0.1 | All model training runs final; no rerun in flight | `05_thesis_results/05_model_benchmark/` mtimes stable; `post-hpc-validation.md` has no open gates |
| 0.2 | All chapter writing notes applied and archived | every `writing-notes/ch*/` folder holds only `.archive/` |
| 0.3 | Thesis `.docx` frozen | Brian confirms; no pending prose pass |
| 0.4 | Every generated artefact regenerated post-freeze | `generated-artefact-provenance.md` audit passes |

Executing before 0.1 is the expensive failure: a retrain changes results
tables, and the export would ship stale numbers under a clean-looking surface.

---

## Phase 1 — Decide the file set (manifest)

Build `submission_manifest.yaml` in this plan folder. Every top-level path gets
a verdict. Current proposal, from the 2026-09-10 survey:

### SHIP — code an assessor runs or reads

| Path | Why |
|---|---|
| `PATHS.py` | every script resolves paths through it; nothing runs without it |
| `01_SRQ1_Model_Training/01_thesis_data/_00_raw/**/*.py` | Nielsen connector, holiday fetch |
| `01_SRQ1_Model_Training/01_thesis_data/_01_converted/**/*.py` | jsonl → parquet conversion |
| `01_SRQ1_Model_Training/01_thesis_data/_02_preprocessing/**/*.py` | the 7-step preprocessing pipeline |
| `01_SRQ1_Model_Training/01_thesis_data/_03_engineered/bymonth/**` | the engineered matrices — the only training input |
| `01_SRQ1_Model_Training/02_thesis_modelling/model_training/**` | SRQ1 benchmarks, tuning, calibration, SHAP |
| `02_SRQ2_Tool_Interface/forecast_tool.py` | the SRQ2 tool interface |
| `04_SRQ4_Scenario_Experiment/scenario_setup/**` | SRQ4 harness, prompts, appendix exporter |
| `05_thesis_results/**` | figures, tables, models — the numbers the thesis cites |
| `requirements.txt`, `requirements.lock`, `pyproject.toml`, `.env.example` | reproducibility |
| `README.md` | **rewritten** — see Phase 3 |

### DROP — Claude/collaboration infrastructure

| Path | Why it must not ship |
|---|---|
| `.claude/`, `.agents/`, `.codex/` | rules, skills, hooks, agents — pure AI-workflow infrastructure |
| `CLAUDE.md`, `AGENTS.md`, `.claudeignore`, `skills-lock.json` | same |
| `plans/` (427 tracked files) | P-ID session plans, findings, task JSON — the collaboration record |
| `user-docs/` (94 files) | handovers, tooling-issues log, git-worktree guides |
| `.archive/`, every nested `*/.archive/` | superseded work, by definition |
| `06_thesis_writing/` | writing notes, docx snapshots, notebookLM packs, citations register, `thesis_inspiration/` PDFs |
| `00_thesis_context/` | RQ working docs, methodology notes, Prometheus analysis, compliance drafts |
| `03_SRQ3_Integration_Readiness/` | empty; SRQ3 scoped to a readiness assessment with no code |
| `worktrees/`, `__pycache__/`, `.venv/` | working state |
| `thesis-manifold.code-workspace` | editor config |

### DROP — utility scripts that are tooling, not thesis

All of `utility_scripts/` goes, on inspection. It contains Zotero sync,
NotebookLM ingestion, Google Drive integration, the thesis snapshot exporter,
draft hollow-section checks, and their tests — every one supports *writing the
thesis*, none is part of the pipeline being assessed. The single exception to
verify in Phase 2: `dynamically_find_root_directory.py`, in case a shipped
script imports it.

### REWRITE — ships, but not as-is

| Path | Change |
|---|---|
| `README.md` | replace wholesale; the current one still documents the pre-2026-09 tier names and describes System B (Claude tooling) |
| every shipped `*.py` | comment pass — Phase 3 |
| `.gitignore` | strip the exemption essays that explain our tracking decisions |
| `04_SRQ4_Scenario_Experiment/scenario_setup/README.md` | strip YAML frontmatter (`applies-to`, `triggers` are Claude-rule fields) and stale folder names |

---

## Phase 2 — Verify the shipped set actually runs standalone

The manifest is a hypothesis until tested. In the export copy:

1. **Import graph** — for every shipped `.py`, resolve its imports. Any import
   reaching a dropped path is either a missing ship or a dependency to sever.
   `PATHS.py` is the main risk: it defines constants for `plans/`,
   `06_thesis_writing/`, `notebookLM/`. Those constants must be removed, not
   left resolving to absent directories.
2. **Path references** — 17 code sites name internal paths (`plans/P0035/...`,
   `writing-notes/unverified-claims-to-check.md`, `.claude/rules/...`). Each is
   a comment or a message that must lose the reference.
3. **Smoke run** — in a fresh venv from `requirements.lock`, run the lightest
   real entry point end to end. Compare its output against the tracked
   artefact. If it cannot run without Nielsen credentials, document that in the
   README as a stated precondition rather than leaving the assessor to discover it.

---

## Phase 3 — The comment pass

**This is the substantive work and the reason a skill exists.** 54 of 69
pipeline `.py` files carry at least one meta marker; `PATHS.py` alone has 49.

Full rules and worked before/after examples:
[`comment_rewrite_rules.md`](comment_rewrite_rules.md).

Summary of the four marker classes and their treatment:

| Class | Example | Treatment |
|---|---|---|
| Internal decision codes | `DEC-GRAIN`, `DEC-P0046-ANCHOR` | drop the code, **keep the reasoning** |
| Plan / finding IDs | `P0035`, `P0038 task 3`, `F63` | drop the reference; keep the fact it points at |
| Change history | "Ported from the notebook", "previously 40", "REMOVED (P0035)" | delete — describes the repo's past, not the code |
| Collaboration | "Brian 2026-08-22", "so Brian and Enrico run identical prompts" | delete the attribution; keep the decision |

Two rules govern the whole pass:

- **Preserve reasoning, delete provenance.** A comment explaining *why*
  `MIN_PERIODS` is derived rather than chosen is exactly what an assessor
  wants. The `DEC-MINPERIODS (2026-08-18)` prefix on it is not.
- **Compress where the length is itself a tell.** Several docstrings run
  60-100 lines of prose with `WHY THIS EXISTS AS A GENERATOR` banner headers.
  A master's-level file docstring is 3-8 lines: what the script does, what it
  reads, what it writes. Reasoning that survives moves to a one- or two-line
  comment at the point of use.

**Not a search-and-replace.** A regex can *find* every marker, and Phase 3
starts by generating that inventory, but each hit needs a judgement about which
half of the sentence is reasoning and which is provenance. The skill drives a
file-by-file pass with the inventory as its worklist.

---

## Phase 4 — Assemble

1. `git clone` the working repo to `../thesis-manifold-submission/`, or copy
   the tree and `rm -rf .git`
2. Apply the manifest: delete every `drop` path
3. Apply the Phase 3 rewrites
4. Write the new `README.md`
5. `git init`, one commit: `Initial commit — CBS master's thesis code`
6. Push to a fresh private repo, or hand over as a zip

## Phase 5 — Final review before handover

| Check | Command / method |
|---|---|
| No meta markers survive | `grep -rE "(DEC-[A-Z]\|P00[0-9]{2}\|\bF[0-9]{1,3}\b)" --include="*.py"` returns nothing |
| No Claude references | `grep -rniE "claude\|anthropic\|\.agents\|skill"` — expect only legitimate hits (e.g. an LLM vendor named in SRQ4 methodology) |
| No names in code | `grep -rniE "brian\|enrico"` returns nothing outside authorship in the README |
| No internal paths | `grep -rE "plans/P0\|writing-notes\|notebookLM\|user-docs"` returns nothing |
| Reads well cold | Brian opens 3 files chosen at random and reads them as an assessor would |
| Runs | Phase 2 smoke run repeated in the final tree |

The last two checks are the ones that matter. The greps are necessary and not
sufficient: they catch markers, not comments that merely *sound* machine-written.

---

## Open questions for Brian

**Q1 — the Nielsen data. This is the one that changes the deliverable.**

The engineered matrices under `_03_engineered/bymonth/` carry brand-level
monthly sales for 95 named Danish brands. They were tracked in this repo
deliberately (2026-09-08) so the VPS could pull and train. But CLAUDE.md states
the constraint plainly: *"Never commit Nielsen data. It is under a
confidentiality agreement and must not leave the local environment."*

Three options:

| Option | Assessor can | Cost |
|---|---|---|
| **A — ship no data** | read code, read results, not re-run | needs a README section stating the data is confidential and how it was obtained |
| **B — ship a synthetic sample** | run the pipeline end to end on fake data | one generator script to write; shape-faithful, values fabricated and labelled as such |
| **C — ship the real matrices** | fully reproduce | breaches the confidentiality agreement unless Manifold consents in writing |

**Recommendation: A, with B if time allows.** CBS assessors read code for
method, not to reproduce a run they have no licence for. B is a nice-to-have
that makes the code demonstrably runnable without disclosing anything.

| # | Remaining questions |
|---|---|
| Q2 | Do the trained model binaries ship (~10 MB per category), or only the metrics they produced? Under Q1-A the binaries are also derived from confidential data — likely drop. |
| Q3 | Does `05_thesis_results/` ship whole, or only the artefacts the thesis actually cites? It currently has 316 tracked files including archived and superseded runs. |
| Q4 | Is a `LICENSE` / confidentiality notice wanted at the root? |
| Q5 | Does the submission repo need `03_SRQ3_Integration_Readiness/` as an empty folder with a README explaining the scope decision, or is its absence better explained in the thesis alone? |

## Alignment with existing decisions

`DEC-P0046-SHIP-SCOPE` (recorded in CLAUDE.md) already states that tiers 01–05
ship to assessors and tiers 00 and 06 do not. The manifest above was derived
independently from a file survey and agrees with it. Where this plan goes
further: it also drops `plans/`, `user-docs/`, `.claude/`, `.agents/`, `.codex/`
and all of `utility_scripts/`, none of which that decision covers.

---

## Related

- [`comment_rewrite_rules.md`](comment_rewrite_rules.md) — the Phase 3 rules with worked examples
- [`worked_pass_step1_load_and_aggregate.md`](worked_pass_step1_load_and_aggregate.md) — completed pass over a pipeline module (2 factual defects found)
- [`worked_pass_export_appendix.md`](worked_pass_export_appendix.md) — completed pass over a generator, source **and** emitted output
- [`findings.md`](findings.md) — survey measurements
- `.claude/rules/rule-priority-hierarchy.md` — the export drops the rules that govern the working repo; this is deliberate and stated here so it is not read as an oversight
