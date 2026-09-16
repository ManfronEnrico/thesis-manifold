---
name: 2026-09-15_APPENDIX-PASS-CONTEXT-handoff
description: HANDOFF - Verified four-surface state for the appendix pass, for a parallel session to use as context. Snapshot, repo commit, Zotero, open threads, and the traps that have already cost this project time.
category: workflow
applies-to: [00_appendices, 05_thesis_results, appendix regeneration]
triggers: [appendix pass, handoff, context for other session]
created: 2026_09_15-13_15
updated: 2026_09_15-13_15
snapshot: 2026-09-15_13-08_appendix-pass-context
status: current as of 2026-09-15 13:08
---

# Appendix pass — verified context

**Everything below was measured, not assumed.** Give this file to the appendix
session.

---

# The four surfaces

| Surface | State |
|---|---|
| **Snapshot** | `06_thesis_writing/docx-exported-snapshots/2026-09-15_13-08_appendix-pass-context/` |
| | 46,711 words, 17 chapter files, **6 comments in 6 threads** |
| **Repository** | `b2e366a`, fetch clean, **nothing incoming**, 5 commits ahead of origin |
| **Zotero** | **93 items**, pulled 13:08 |
| **Results tree** | see the table counts below |

⚠ **The `.docx` grew from 1.93 MB to 2.56 MB since 12:25** — appendix material is
being added right now. **Re-snapshot before relying on any anchor in it.**

---

# The appendix chapter is mid-rewrite — do not treat it as stale-but-stable

**`chapters/appendix.md` is now 688 words.** The previously-reported defects are
**gone, because the content itself is gone**:

| Previously | Now |
|---|---|
| prompt schema `v4-five scenarios+e37111d3daaa` | ⚠ **no schema string at all** |
| five scenario prompts, A–E, reproduced verbatim | ⚠ **no scenario prompts at all** |

✅ **This is not a regression to report — it is a rewrite in progress.** But it
means **thread 305/284's "OUTDATED" verdict is now obsolete**: there is no v4
string left to correct. The task is to write the section, not to fix it.

## The Table of Appendices has been renumbered

```
**Appendix 1** - Literature Review Design Map      138
**Appendix 2** – Star Schema Diagram (CSD Example) 141
```

⚠ **The scheme changed from `A1`/`A2` to `Appendix 1`/`Appendix 2`.** Any note or
prose still saying "Appendix A1" or "Appendix A2" is now wrong. **This directly
answers thread 98** — see below.

---

# The six open threads

| Thread | Chapter | Section | Asks |
|---|---|---|---|
| **27** | Ch1 | 1.3.4 | `APPENDIX PASS: RE-GENERATE` — Figure 1, the SRQ hierarchy tree |
| **93** | Ch4 | 4.2 | `PROSE` — new since 12:25 |
| **98** | Ch4 | 4.2.3 | fill `Appendix [N]` — the thread names the table: `step_2_05_adf_per_brand` |
| **103** | Ch4 | 4.2.5 | ⚠ `APPENDIX: Must be updated („0 figures" in documented findings)` — **new** |
| **260** | Ch8 | 8.3 | `APPENDIX PASS: Re-generate & Replace` — Table 23, the seven scenarios |
| **298** | Refs | — | dynamic Zotero reference list |

## Thread 98 is answerable right now

**Anchor**, Ch4 §4.2.3, verbatim (⚠ **note the double space before "rather"**):

> "The cost is accepted deliberately, and the per-brand results are reported in full in Appendix [N]  rather than summarised away."

→ Replace `Appendix [N]` with the number the ADF table receives under the **new**
`Appendix N` scheme. **It is the last `Appendix [N]` placeholder in the
document** — I grepped all 17 chapter files.

## Thread 103 is a real defect, not a formatting note

*"0 figures in documented findings"* against Ch4 §4.2.5 Autocorrelation. **Check
whether the ACF figures are being emitted at all** before assuming the appendix
reference is the problem.

---

# Generated table inventory

| Chapter | SVG | MD |
|---|---|---|
| 02_literature_review | 0 | 1 |
| 04_data_assessment | 3 | 7 |
| 05_model_benchmark | 7 | 27 |
| 07_decision_synthesis | 1 | 1 |
| 08_experimental_evaluation | 6 | 6 |
| 09_discussion | 0 | 0 |

⚠ **`05_model_benchmark` has 27 `.md` against 7 `.svg`.** Either most tables are
not yet rendered through the new SVG renderer, or **stale `.md` files are sitting
beside their replacements.** Worth resolving before selecting artefacts — see the
duplicate-slug warning below.

## Uncommitted work in the results tree

```
 M 04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py
 M 05_thesis_results/05_model_benchmark/tables/01_metric_dictionary.{csv,md}
 M 05_thesis_results/08_experimental_evaluation/tables/17_run_configuration.{csv,md,svg}
 M 05_thesis_results/APPENDIX_TABLES.md
 ?? 05_thesis_results/08_experimental_evaluation/abbreviated_response_example/
 ?? 05_thesis_results/08_experimental_evaluation/figures/
 ?? 05_thesis_results/render_scenario_comparison_formats.py
```

⚠ **`export_appendix.py` carries my uncommitted edits** — see the next section.
**Do not `git checkout` that file**, it would silently restore a false claim.

---

# Two code fixes already applied, uncommitted

**In `export_appendix.py`, this session:**

| Line | Change |
|---|---|
| ~446 | `"even at temperature zero"` → `"under identical decoding settings"` |
| ~1431 | removed `("Temperature", str(tr.get("temperature", "n/a")))` — it rendered as the literal string **"None"** |

**Why:** `gpt-5.5` rejects `temperature` and `top_p` with HTTP 400.
`srq4_experiment.py:178-188` sets `TEMPERATURE = None` and states that *"Reporting
temperature 0 in the methodology would be false."* The `Decoding` row prints
*"temperature/top_p unsupported by the model; defaults used"*, which is the honest
version and is carried in every trace.

✅ **These take effect on the next regeneration.** The prose side is already
corrected in Ch3 §3.6.

⚠ **`17_run_configuration.{csv,md,svg}` is modified in the working tree** — that
is the table the second fix affects. It may already reflect it; check before
regenerating.

---

# Traps this project has already hit

**1 — Never hand-edit a generated table in Word.** It is overwritten on the next
export while leaving the document temporarily correct. Every appendix table comes
from `export_appendix.py`.

**2 — Watch for duplicate slugs from the renumbering.** Commit `37a04f0` created
`06_substrate_resource_profile` beside the existing `05_substrate_resource_profile`,
and `09_parameter_drift` beside `08_parameter_drift`. If those were renumberings
rather than additions, **the old slugs are stale duplicates** and the generator's
delete-by-identity step missed the rename. The 27-vs-7 count above may be the same
issue.

**3 — Four stale artefacts must not be cited without regenerating:**
`param_drift.csv`, `refit_vs_retune.csv`, `retune_single_cutoff.csv`,
`sandbox_profiling.csv`.

**4 — Tiers 01–05 are reader-facing.** No plan IDs, finding numbers, author names,
or paths into `06_thesis_writing/`. Enforced by:

```bash
python 05_thesis_results/check_reader_facing.py   # exit 1 on any hit
```

**5 — Figures: SVG only, landscape, white background, ratio ≤ 3.6.** No PNG twin.
See `.claude/rules/figure-generation-standards.md`.

**6 — Every number computed, never typed** — including inside `review=` blocks.
`.claude/rules/generated-artefact-provenance.md`, Correctness tier.

---

# ⚠ Zotero: 13 of 93 entries have unusable dates

**This blocks thread 298.** The bibliography is generated from exactly this data.

**Missing a year entirely (4):**

| Key | Item |
|---|---|
| `4TVC5APJ`, `SPW7NXHT`, `Q4IIBE2Z` | ⚠ **three duplicate `webpage` records** of *Elements of Statistical Learning* — will render as three separate entries |
| `HVAURH2K` | *Smart "Predict, then Optimize"* |

**Month string in the year field (9):**

| Key | Year field | Item |
|---|---|---|
| `hevner_cycles` | `01.2` | A Three Cycle View of DSR |
| `KKR3U38C` | `Augu` | XGBoost |
| `XH475DIR` | `Marc` | Saunders, Research Methods |
| `U24G3Z36` | `July` | CodeAct |
| `8CITVHH2` | `July` | Optuna |
| `AMB2F6T2` | `Janu` | Non-Determinism of ChatGPT |
| `MXN2CH3U` | `Nove` | Time Series Forecasting with LLMs |
| `chen_acgraph:_Dece` | `Dece` | ACGraph |
| `sapkota_ai_02/2` | `02/2` | AI Agents vs. Agentic AI |

⚠ **Several are load-bearing citations** — Hevner, Saunders, XGBoost and Optuna
all appear in the methodology and benchmark chapters. **Fix in Zotero, then
re-pull**, before generating the list.

⚠ **`citations.json` is filtered by `_SCHOLARLY_TYPES`.** A `computerProgram`,
`dataset` or `software` entry is silently dropped. Never conclude "not in the
library" from that file — query the API unfiltered.

---

# Live appendix notes

| Note | Purpose |
|---|---|
| `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md` | the master audit — 242 files, 36 producers |
| `00_appendices/2026-09-14_appendix-rendering-requirements.md` | rendering contract |
| `00_appendices/2026-09-14_table-format-options-and-two-findings.md` | table format options |
| `ch{1..9}/2026-09-14_appendix-citations-ch*.md` | **9 notes, none applied** — per-chapter recommendations for which artefacts to cite in-text vs appendix |

✅ **The nine citation notes are the main unapplied body of appendix work.**

---

# Before writing anything

```bash
python utility_scripts/scripts/thesis_snapshot.py --label "<your-label>"
```

⚠ **The `.docx` is being actively edited.** This snapshot is 13:08; anchors
quoted from it go stale quickly today. Submission is **2026-09-15 14:00**.
