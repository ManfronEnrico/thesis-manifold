---
pid: P0054
created: 2026-09-15 00:00:00
updated: 2026-09-15 00:00:00
status: in_progress
focus_detail: "Supersedes the earlier P0054 manifest. Ship list fixed by Brian 2026-09-15; export tree copied to Z:\\_dev-ssd\\thesis-manifold-submission (949 files, 976 MB). Remaining work: prune confidential artefacts, sever 3 dropped-tree dependencies, comment/docstring pass over 79 .py files, new README."
---

# Submission export — the executing plan

Supersedes the manifest in `task_plan.md`. Where the two disagree, this file
wins: the ship list here was fixed by Brian on 2026-09-15 and the earlier one
was a proposal.

**The standard, in one sentence:** a submission-ready file carries single-line
comments at the crucial parts and nothing else — no decision records, no plan
state, no essay docstrings. Excessive commentary is the clearest tell of AI
authorship, and removing it is most of the work.

---

## What ships — settled, not proposed

Ten root-level entries, and nothing else:

| Entry | Note |
|---|---|
| `01_SRQ1_Model_Training/` | data pipeline + model training |
| `02_SRQ2_Tool_Interface/` | `forecast_tool.py` |
| `04_SRQ4_Scenario_Experiment/` | scenario harness |
| `05_thesis_results/` | figures, tables, generators |
| `utility_scripts/scripts/dynamically_find_root_directory.py` | the one file kept from that tree |
| `.env.example`, `PATHS.py`, `README.md`, `requirements.lock`, `requirements.txt` | root singles |

Everything else at root is dropped: `00_thesis_context/`, `03_SRQ3_…/`,
`06_thesis_writing/`, `plans/`, `user-docs/`, `.claude/`, `.agents/`, `.codex/`,
`.archive/`, `worktrees/`, `CLAUDE.md`, `AGENTS.md`, `.claudeignore`,
`skills-lock.json`, `thesis-manifold.code-workspace`, `pyproject.toml`,
`uv.lock`, `.venv/`.

### Exclusion rules inside the shipped trees

| Rule | Reason |
|---|---|
| No `*.parquet`, no `*.jsonl` | the licensed panel itself |
| No `.archive/` at any depth | superseded by definition |
| No `__pycache__/`, no `*.pyc`, no `*.stamp` | working state |
| `*.csv` only where it carries **no literal data** | see the content test below |
| `*.json`, `*.log`, `*.md` generally fine | diagnostics and manifests, not data |
| All `*.py` under the four trees | non-negotiable — they are the artefact |

**The CSV test is content, not extension.** `step_6_final_dataset_h3.csv`
(`quantity,value` — 9 rows of counts) ships. `step_1_preview.csv` (32 columns of
raw monthly brand sales) does not.

---

## Status: the copy is done

`Z:\_dev-ssd\thesis-manifold-submission` now holds **949 files, 976 MB**,
copied with the exclusions above applied. Verified zero leaked `.parquet`,
`.jsonl`, `.archive/`, `__pycache__`, `.stamp`.

| Type | Count |
|---|---|
| `.md` | 313 |
| `.csv` | 220 |
| `.json` | 175 |
| `.svg` | 108 |
| `.py` | **79** |
| `.log` | 48 |
| `.joblib` | 2 |

Extension-level exclusion was the easy half. The three sections below are what
remains, in priority order.

---

# Phase A — Confidentiality (do first; it changes the file set)

## A1 — 33 CSVs carry literal brand data or named brands

A content scan found 33 CSVs in the export whose first rows contain real Danish
brand names. They are **not one category**, and the distinction decides each:

### A1a — LITERAL monthly sales. Delete.

These are the licensed panel in CSV clothing.

| Path | What it is |
|---|---|
| `04_SRQ4_Scenario_Experiment/agent_inputs/{CAT}/*_brand_month.csv` | 32 columns of raw monthly sales per named brand |
| `05_thesis_results/08_experimental_evaluation/scenario_inputs/CSD__*.csv` | the same series, as fed to Scenario B |
| `.../_02_preprocessing/**/step_1_preview.csv` (4) | raw panel head, all measures |

### A1b — DERIVED per-brand statistics. Brian's call.

These name brands but contain no sales history — a p-value, a lag list, a
retention count. They are the kind of aggregate the thesis already prints.

| Path | Content |
|---|---|
| `step_2_05_adf_per_brand.csv` (4) | brand, n, ADF p-values, recommendation |
| `step_2_16_acf_significant_lags.csv` (4) | brand, conf band, significant lags |
| `step_2_11_top_brands.csv` (4) | **brand + total sales** — closest to literal |
| `{cat}_series_index_h{1,3}.csv` (6) | brand, periods, **total_units**, split sizes |
| `05_model_benchmark/tables/pooled_perbrand.csv` | brand, WMAPE, mean_test_units |
| `08_experimental_evaluation/tables/25-30_per_run_record_*.csv` | brand, actual, forecast, APE |

**Recommendation: keep A1b, delete the two rows carrying absolute volume**
(`step_2_11_top_brands`, `{cat}_series_index_*`). A brand name attached to an
error rate is a result the thesis publishes anyway; a brand name attached to
`total_units = 237,169,351` is the panel. `25-30_per_run_record_*` print
`Actual` per brand and need the same judgement — they are core SRQ4 evidence,
so removing them costs more than the others.

## A2 — `04_SRQ4_Scenario_Experiment/runs/` — 37 MB, the live exposure

37 JSON files whose keys include **`prompt`** and **`answer`**. Every raw
response embeds the brand's monthly sales CSV, because that is what was pasted
into the prompt. The results tables are not the disclosure risk; these are.

Two options:

1. **Delete `runs/` entirely.** Simplest. The derived results in
   `05_thesis_results/08_experimental_evaluation/` are complete without it.
2. **Strip `prompt` and `answer` in place**, keeping the trace fields —
   `trace`, `outcome`, `ape`, `latency_s`, `tokens_*`, `cost_usd_est`,
   `deviates_from_model`, `payload_complete`.

**Recommendation: (2).** The thesis claims every forecast is traceable to a
verified tool call. That is a property of the *trace*, not the prompt text, so
stripping the two text fields preserves the auditability evidence while
removing the data. A script doing this is ~20 lines and must key on the field
names, never on file size.

## A3 — Prometheus

`prometheus_bridge.py` ships (it is the integration method, and importing it is
*designed* to fail gracefully). Two edits:

- line 8 and line 88 hardcode `Z:\_dev-ssd\prometheus\prometheus-graph-engine`.
  Replace the default with `None` + the `PROMETHEUS_ENGINE_DIR` env var, and
  the docstring path with a confidentiality placeholder.
- The docstring's `F45` architecture section describes the vendor's internal
  agent/tool structure. That is vendor IP, not our method — cut it to a
  sentence.

**Do not "tidy" the try/except around its import in `srq4_experiment.py`** —
the graceful degradation is a shipped feature.

## A4 — Model binaries

`05_model_benchmark/models/` holds 30 MB: two `.joblib`, two large `model.json`.
They are fitted on confidential data and a fitted model can leak training data.
**Recommendation: drop the binaries, keep the metrics they produced.** This also
removes most of the export's weight.

## A5 — Other brand-name carriers

94 `.json`/`.md` files mention brands. Most are EDA tables where A1b's reasoning
applies. Two need a direct look: `_00_raw/nielsen/CSD_METADATA_INDEX.json` and
`NIELSEN_METADATA_INDEX.json` (schema + possibly value samples), and
`_00_raw/nielsen/description/nielsen-prometheus_data_model.md`.

---

# Phase B — Three dependencies on dropped trees

Found by import scan; each currently breaks in the export.

## B1 — `generate_literature_table.py` hard-fails

```python
CH2 = THESIS_WRITING_DRAFTS_DIR / "literature-review.md"
...
if not CH2.is_file(): raise SystemExit(f"missing {CH2}")
```

It parses the chapter-2 draft, which does not ship. **Drop this generator** and
keep its output table — it cannot run in the export by construction.

## B2 — `PATHS.py` constants pointing at absent trees

18 lines reference dropped trees. Verified: `THESIS_WRITING_DIR`,
`THESIS_CONTEXT_DIR`, `THESIS_WRITING_NOTES_DIR`, `SRQ3_DIR` and the
notebookLM/citations/plans constants are imported by **zero** shipped files.
Only `THESIS_WRITING_DRAFTS_DIR` has a consumer, and B1 removes it.

**Remove the constants outright, do not leave them dangling.** A path resolving
to a missing directory degrades silently rather than failing — the exact trap
`path-handling.md` exists to prevent.

## B3 — `review_notes.py` / `check_reader_facing.py`

Eight shipped producers import one or both, so they ship. `check_reader_facing.py`
should additionally be **run against the export tree** at the end — it walks
whatever tree it is given and catches author names and internal paths that the
greps miss.

---

# Phase C — The comment and docstring pass

**The bulk of the work: 79 files, ~30,700 lines, 4,100 pure-comment lines.**

## C1 — Scale

62 of 79 files carry at least one internal marker:

| Class | Lines |
|---|---|
| ISO dates in comments | 269 |
| Plan IDs (`P00NN`) | 242 |
| Finding IDs (`F63`) | 194 |
| Decision codes (`DEC-…`) | 119 |
| Author names | 11 files |
| `claude` / `CLAUDE.md` | 15 files |

## C2 — Worst docstring offenders

Module docstrings, by line count. A master's-level file docstring is 3–8 lines;
these are essays with internal section banners:

| Lines | File |
|---:|---|
| 84 | `scenario_setup/prompts.py` |
| 82 | `scenario_setup/score_interval_communication.py` |
| 77 | `scenario_setup/export_scenario_inputs.py` |
| 73 | `scenario_setup/build_agent_inputs.py` |
| 68 | `scenario_setup/prometheus_bridge.py` |
| 65 | `02_SRQ2_Tool_Interface/forecast_tool.py` |
| 65 | `srq1/srq1_residual_diagnostics.py` |
| 60 | `srq1/srq1_pooled.py` |
| 58 | `scenario_setup/smoke_test.py` |
| 54 | `scenario_setup/srq4_experiment.py` |

Twenty more run 40–50 lines. The banner-header style
(`WHY THIS EXISTS`, `ROUTING`, `WHAT SRQ2 ASKS AND WHERE IT IS ANSWERED HERE`)
is the single strongest tell — no student writes `----` headings inside a
docstring.

## C3 — The target form

```python
#!/usr/bin/env python3
"""Serve forecasts from persisted models: load, predict, attach a 90% interval.

Models are fitted by train_and_persist.py; this module never trains.

Usage:
    from forecast_tool import forecast_demand
    forecast_demand("CSD", "HARBOE")
"""
```

Then **single-line comments at crucial points only** — a non-obvious threshold,
a correctness trap, a formula. Not a paragraph above every block.

## C4 — Four verdicts per comment

| Verdict | When | Action |
|---|---|---|
| KEEP | explains why the code is as it is | leave, shorten to one or two lines |
| DELABEL | good reasoning wearing an internal label | strip label, keep sentence |
| DELETE | repo history, fixed bugs, collaborator notes, dates | remove |
| **FIX** | factually wrong now — stale path, renamed file | **correct it** |

FIX matters most: a stale path is a defect an assessor trips over. Grep cannot
find these — on `train_and_persist.py` a grep-driven pass missed a docstring
describing three already-fixed bugs (read as current defects) and a `Usage:`
block naming a pre-September path, so the command an assessor copies fails.

**Read each file top to bottom. Never batch-edit with sed** — a mechanical
strip leaves dangling fragments and destroys the good comments, which is most
of them. Zero `TODO`/`FIXME` anywhere: the comment *quality* is high, the
problem is quantity and labelling.

## C5 — Known specific fixes

- `forecast_tool.py:57` cites `writing-notes/ch7_synthesis/…` — delete the
  reference, keep the finding.
- `dynamically_find_root_directory.py` — its docstring explains that the anchor
  was changed *away from* `CLAUDE.md` "because the repository is shared with
  assessors and a filename that advertises the assistant is not something to
  ship". In the export that paragraph reintroduces exactly what it avoided.
  Cut to: *"Find the repo root by searching upward for .env.example."*
- `forecast_tool.py`'s docstring documents `confidence` as degenerate across ~55
  lines. The *finding* is real and belongs in the thesis; in the module it
  becomes two lines at the point of use.

---

# Phase D — README

The current README cannot be edited into shape: it links `00_thesis_context/`,
`.claude/rules/`, `plans/`, `06_thesis_writing/` — all dropped — and has a
"Claude Code and GitHub CLI" setup section.

Five sections, nothing else: what this is (title, institution, authors, RQ +
four SRQs); what each folder does, one line; how to run it; **data availability**;
where results live.

**The reproducibility statement must be exact.** The earlier draft claim that
"`OPENAI_API_KEY` alone runs scenarios A, B and C" is **false** and must not
reach the README — those scenarios also need the withheld brand history. State
three tiers:

1. **Inspectable, not runnable:** A, B, C, F — need the licensed Nielsen panel.
2. **Not reproducible, engine withheld:** D, E, G — proprietary orchestrator.
3. **Complete and provided:** the derived results, prompts and traces.

A repo that cannot be re-run is defensible and normal for licensed commercial
data. One whose limitation the assessor *discovers* rather than reading is not.

---

# Phase E — Verification

```bash
grep -rE "(DEC-[A-Z]|P00[0-9]{2}|\bF[0-9]{1,3}\b)" --include="*.py" .
grep -rniE "brian|enrico" --include="*.py" --include="*.md" .
grep -rniE "claude|CLAUDE\.md|\.claude/" --include="*.py" --include="*.md" .
grep -rE "plans/P0|writing-notes|notebookLM|user-docs|06_thesis_writing" .
find . -name "*.parquet" -o -name "*.jsonl" -o -name "__pycache__" -o -name ".archive"
python 05_thesis_results/check_reader_facing.py
```

All empty, with two legitimate exceptions: `anthropic`/`openai` as a **named LLM
vendor** in SRQ4 methodology, and author names in the README byline.

Then the two checks no grep performs: **read three files at random as an
assessor**, and confirm the tree still imports. Finally `git init` and one
commit — never push to the existing remote.

---

## Open decisions

| # | Question | Recommendation |
|---|---|---|
| D1 | A1b derived per-brand tables — keep? | Keep, minus the two absolute-volume tables |
| D2 | `runs/` — delete or strip? | Strip `prompt`/`answer`, keep traces |
| D3 | Model binaries — ship? | Drop; keep metrics |
| D4 | `25-30_per_run_record_*` name brands with actuals | Keep — core SRQ4 evidence |
| D5 | `LICENSE` / confidentiality notice at root? | Add a short notice |
