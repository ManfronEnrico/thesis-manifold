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
