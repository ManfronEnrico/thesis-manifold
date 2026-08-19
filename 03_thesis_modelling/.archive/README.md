# `03_thesis_modelling/.archive/`

Superseded modelling artefacts, kept rather than deleted because they are
**evidence of how the work developed** and several are cited in plans and
handovers. Nothing here is on a live code path.

Check this README before assuming something here is safe to delete — at least
one item contains results that were never reproduced elsewhere.

---

## `notebooks_srq1_srq2_2026-08/` — archived 2026-08-19

The original Jupyter notebooks for SRQ1 (per-category and pooled model
comparison) and SRQ2/SRQ3 (the 4-tier A/B test and the forecasting registry).
Last substantive commit 2026-07-13; superseded by scripts under
`03_thesis_modelling/model_training/`.

**Why archived rather than kept live:**

- **6 of 10 reference `totalbeer`**, a fifth category dropped by DEC-GRAIN
  (2026-07-12). The thesis runs on four categories.
- `pooled_5.ipynb` is the five-category pooled model — same problem.
- They predate the H=1 → H=3 horizon decision (DEC-HORIZON), the
  `holiday_month` → `peak_month` rename, and the leakage fixes applied
  2026-08-18 (contemporaneous features, zero-run flags, split boundaries).
- Execution counts are low (4–15 executed cells of 22–68), so their stored
  outputs are partial and not a reliable record of any full run.

**Why kept:** they are the provenance of the SRQ1 model-selection argument, and
`registry_and_forecasting.ipynb` documents the original tool-registry design that
the current serving layer descends from.

**Do not re-run them.** Any number they produce will disagree with the current
pipeline, and the disagreement is expected, not a bug.

---

## `prompts_srq2_2026-08/` — archived 2026-08-19

Enrico's SRQ2/SRQ3 prompt set and human-evaluation pilot.

| File | What it is |
|------|-----------|
| `prompts_v5_final.csv` | 50 prompts across 11 archetypes, with ground-truth `actual_sales_units` |
| `human_eval_pilot_15_v3.csv` | 15 of those prompts run through four tiers (L0–L3), with LLM judge scores |

**This is not dead material, and it is not SRQ4.** Two things matter:

1. **It contains real executed results.** All 15 rows carry `L0_response` text
   and `L0_judge_v3_avg` scores. The human-score columns
   (`*_HUMAN_score_1to5`, `HUMAN_winner_*`) are empty — that validation step was
   never completed — and `L0_pred` is empty while `L3_pred` has 4 of 15. So it is
   a **partially executed pilot**, not a finished result and not an empty
   template.
2. **It answers a different research question.** The L0–L3 tiers are an SRQ2/SRQ3
   capability ladder. The SRQ4 experiment compares three *scenarios* (plain LLM /
   data + code / trained model) on a single prediction task. The 50-prompt
   archetype taxonomy was deliberately replaced for SRQ4 (B-DEC-3, 2026-08-19)
   because ~34 of the 50 involve no forecasting at all.

**These CSVs are gitignored** (`.gitignore` line 18, `*.csv`) and were never
committed, so they exist only on the machine that generated them. Losing them
loses the pilot.

**If SRQ2/SRQ3 is written up, start here** — do not regenerate the prompt set
from scratch, and do not assume the pilot needs re-running before the human
scoring step is attempted.

---

## Related

- `.archive/grain_artifacts_p0035_2026-08/` — chain/region grain artefacts (repo root)
- `05_thesis_writing/notes/srq4-experiment-design-rationale.md` — why the SRQ4 prompt set replaced the archetype taxonomy
- `user-docs/handovers/2026-07-13_harness-and-srq4-decisions-handover-brian.md` — DEC-GRAIN, DEC-ARMS, the L0–L3 tier design
