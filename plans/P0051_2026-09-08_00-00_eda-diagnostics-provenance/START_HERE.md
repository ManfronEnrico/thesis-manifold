---
pid: P0051
created: 2026-09-08 00:00:00
updated: 2026-09-08 00:00:00
---

# START HERE — P0051

**Status: not started.** Investigation is complete; no change has been made.

## The finding in one sentence

The per-brand ADF `recommendation` column and the per-feature skewness
interpretation are computed, reported, and **read by nothing** — a single global
`log1p` is applied from a hardcoded constant, and ARIMA uses a hardcoded `d=1`.

## Read in this order

1. `findings.md` **F1-F2** — what was measured, and the per-category counts
2. `findings.md` **F3** — what the pipeline actually does instead
3. `findings.md` **F5** — the two Ch4 sentences that overstate the evidence
4. `task_plan.md` — the five phases

## Before you change anything

**This is mainly a writing task.** The uniform transform is the *better* choice on
n=46 series; do not "fix" the pipeline to consume the recommendations without
reading F3 first. The cheapest correct outcome is honest prose.

## The one free win

`_shared_modules/pipeline_config.py:218` claims ADF-per-brand results "feed
data-handling decisions". They do not. One-line fix, no dependencies.

## Coordinate with

- **P0048** owns the Ch4 prose pass — same paragraphs. Check before writing.
- **P0050** owns the EDA figures/tables these diagnostics produce.

---

## 2026-09-08 — scope widened, and one item is now time-critical

The original P0051 finding (diagnostics computed, never consumed) still holds. Two things
were added on 2026-09-08 — see **`findings-feature-reduction.md`**:

1. **The 54 → 13 reduction is traced end to end.** Three stages: contemporaneous
   exclusion (measured, sound), the hardcoded `FEATURES` list (only 1 of 21 exclusions
   individually tested), and a redundancy reduction that was tested and *rejected* on
   held-out error. Not gut feeling — but only partly written down.

2. **⚠ The holiday ablation is out of scope and `FEATURES` should be enriched.** The
   thesis asks whether trained models help an LLM forecast, not whether exogenous
   variables improve models. Holiday enrichment is adopted as a design choice consistent
   with M4/M5's exogenous-variable direction (NOT prescribed by them), not proven
   in-thesis. **This blocks the VPS training run** — see
   `P0053_.../START_HERE.md` §0.

3. **`05_thesis_results/04_data_assessment/tables/04_feature_matrix.md` states a false
   number** — "34 are model inputs". Models train on 13. The generator reads the pipeline
   manifest, which never sees the training-side list.

Chapter framing lives in
`06_thesis_writing/writing-notes/ch4_data_assessment/why-thirteen-features.md`.
