---
name: p0042-progress
description: RULE - Session log for the funded-phase sequencing plan.
category: workflow
applies-to: [srq4, notebooklm]
triggers: [resuming P0042, checking what was last done on the funded phase]
created: 2026_09_01-00_00
updated: 2026_09_01-00_00
---

# P0042 — Progress

## 2026-09-01 — cost analysis, scope freeze (gate 1, A/B/C half)

**Remote checked first:** `main` local == `origin/main` (`09bd34c`), 0 ahead / 0
behind. Enrico's last push to any branch was `enrico/local-backup` on 2026-07-13
— seven weeks ago. No incoming work to merge.

### Free checks run (no API spend)

| Check | Result |
|---|---|
| `verify_setup.py` | PASS on leakage guard, target-month alignment, feature matrices, tool payload, prompt targeting. FAIL only on `OPENAI_API_KEY` absent from shell (env, not config) — F4 |
| Model pinning audit | 30 raw responses + 27 CSV rows all `gpt-5.5-2026-04-23` @ `medium`. No drift — F3 |
| `--list-brands` | stratified picks resolve in all 4 categories — F5 |
| Cost analysis over 29 logged runs | A $0.4277 / B $0.2664 / C $0.0068 per run — F2 |
| `--dry-run` x 3 blocks | all parse; 111 runs, $11.06 est. |

### The decision

Budget ceiling set by Brian at **~$50 total**, ideally lower. The earlier
candidate designs ($84 est / ~$377 realistic for all-categories x n=10) were
rejected as unaffordable.

**Resolved by allocating inversely to per-run cost** rather than by cutting the
experiment uniformly. A_plain costs ~63x C_model, so equal-n spends the budget on
the least contested result. Frozen design in
`2026-09-01_DOC-srq4-sampling-design.md`:

| Block | Runs | Est. | Realistic |
|---|---:|---:|---:|
| 1. A floor (2 brands x 3, CSD) | 6 | $2.55 | ~$11 |
| 2. B vs C core (3 stratified x 10, CSD) | 60 | $8.20 | ~$28 |
| 3. C breadth (9 brands, 3 cats x 5) | 45 | $0.31 | ~$0.50 |
| | **111** | **$11.06** | **~$40** |

All three dry-run clean against the real harness.

### Correction made during the session

I initially advised budgeting every scenario at the 4.47x billed/estimate ratio.
**That was wrong** and would have forced an unnecessarily small experiment — the
gap is web search (A only) plus the Code Interpreter container (B only), so
C carries no surcharge. Recorded as F1.

### Decisions taken

- **DEC-STRATIFIED**: `--brand-strategy stratified`, not `volume`. Volume-ranked
  selection measures only the easiest brands. Thin-series underperformance is an
  expected, reportable finding (Brian: "we are not trying to solve world hunger,
  but to generate insights").
- **DEC-SINGLE-CATEGORY**: the full ladder runs on CSD only; `C_model` alone goes
  cross-category. Reported as a stated design choice + limitation, never as
  "we could not afford more".
- **DEC-UNEQUAL-N**: A at n=3, B/C at n=10. Justified by the 17.8pp vs 3.5pp
  effect sizes against the 63x cost ratio.

### Open before any D/E spend

`measure_e2b_cost.py` has **not** been run. D/E repeat count stays unfrozen until
it is (F6). This is the remaining half of gate 1.

### Not started

Workstream A (NotebookLM review rounds) — unchanged, still ready. Ch3/Ch4 drafts
still need uploading to notebook `03b4f55a` before A1 can run.
