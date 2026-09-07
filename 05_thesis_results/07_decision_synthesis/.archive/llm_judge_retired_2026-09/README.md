# LLM-as-Judge artefacts — retired 2026-09-06 (P0046 F8, corrected)

`judge_scores.csv`, `recommendations.csv`, `llm_summary.md`.

## Decision

**The LLM-as-Judge design was decided against.** Brian, 2026-09-06.

These files appear in the current thesis `.docx` as **Table 21** (Ch8 §8.3,
"LLM Judge Scoring Likert Scale Results", LLM 3.81 vs baseline 3.15) — but that
section is itself slated for removal. Brian's own review comments on it say so:

| Comment | Tags | On |
|---------|------|-----|
| 381 | VERIFY, OUTDATED | "On N=50 stratified test cases, GPT-4o (LLM-as-Judge…)" |
| 383 | OUTDATED, INCORRECT | "Table 21 - LLM Judge Scoring Likert Scale Results" |
| 384 | OUTDATED | (same section) |

## A correction worth recording

I initially recommended RESTORING the producers on the grounds that the thesis
cites these numbers. That reasoning was wrong: **presence in the current draft is
not evidence of intent** when the section carrying it is flagged for removal. A
citation makes an artefact load-bearing only if the citation is meant to survive.
The right question was "is this design still the plan?", and the answer was no.

## Consequence

- The producers (`srq2_agent.py`, and the judge half of `srq2_synthesis.py`) stay
  in `01_SRQ1_Model_Training/02_thesis_modelling/.archive/superseded_scripts_2026-08/`.
- Ch8 §8.3 and Table 21 come out of the `.docx` — a prose edit, tracked in
  `06_thesis_writing/writing-notes/`.
- `synthesis.csv` / `synthesis_summary.md` remain live: they back Ch7 §7.2's
  deterministic synthesis results, which is a separate, retained contribution.

Recoverable from here and from git if the design is ever revived.
