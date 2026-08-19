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
2. **It answers a different research question.** SRQ2 asks *how forecasting
   outputs can be exposed through a structured tool interface preserving
   reliability, uncertainty and traceability* — the unit of analysis is the
   **interface contract**, and the L0–L3 tiers vary how much structure the
   interface carries. SRQ4 asks whether *integrating dedicated models* improves
   correctness/consistency/cost against a code-as-action baseline — the unit of
   analysis is **which mechanism produces the number**, and its three scenarios
   vary what the agent can reach (nothing / data + code / trained model). One
   varies the interface; the other varies the capability behind it.

3. **It inherits the prompt-design flaw SRQ4 rejected.** Verified 2026-08-19:
   the 15 pilot rows are **15 distinct queries across 9 archetypes**, not one
   prompt repeated. Only 4 of 9 archetypes are forecasting at all
   (`point_forecast`, `range_forecast`, `confidence_interval`,
   `channel_volatility`); the rest are ranking, comparison and driver questions.
   That is the same dilution B-DEC-3 removed from SRQ4.

4. **Every pilot prompt is chain-level.** The queries name retail chains
   (`BRUGSEN`, `7_ELEVEN`, `REMA_1000`, `SPAR`), i.e. the **chain grain deleted
   by DEC-GRAIN** (2026-07-12) in favour of brand × month. Re-running the pilot
   as written would require data the project no longer produces.

**Consequence**: treat this as evidence of an earlier design, not as a partial
result to be finished. If SRQ2/SRQ3 is written up, the prompt set needs
rebuilding against the current grain and a decision on whether the archetype
spread is wanted — the *responses* here are still useful as qualitative
material about how the tiers differed.

**These CSVs are now committed.** They were previously caught by the blanket
`*.csv` rule and existed on one machine only. `.gitignore` now carries an
explicit exemption for prompt sets, because a prompt set that lives on one
machine is a silent source of drift between two people's results, and it cannot
be quoted in a methodology appendix if it is lost.

---

## `superseded_scripts_2026-08/` — archived 2026-08-19

### `srq4_tier2.py`

The 25-prompt / 5-family decision-support battery (point, interval, comparison,
ranking, seasonality) with deterministic ground-truth builders and per-family
evaluators.

**Archived for two independent reasons:**

1. **It was broken.** `--selftest` raised
   `ValueError: too many values to unpack (expected 2, got 3)` — it unpacks the
   old 2-tuple from `_brand_history`, which now also returns the target month.
   The failure predates this session and had gone unnoticed, which is itself
   evidence nothing depended on it.
2. **Its design was superseded.** B-DEC-3 (2026-08-19) replaced the
   multi-archetype prompt taxonomy with a single prediction template, because
   roughly two-thirds of such prompts involve no forecasting and dilute the
   effect being measured. Three of its five families (comparison, ranking,
   seasonality) are exactly those non-forecasting archetypes.

**Worth keeping** for its parsing and evaluation helpers — `parse_interval`,
`parse_ranklist`, `parse_yesno`, the overlap@k scorer — which are careful,
tested, and would be the starting point if a broader prompt set is ever
reinstated for SRQ2/SRQ3.

**Do not repair it in place.** The `_brand_history` signature is the smallest of
its problems.

---

## Related

- `.archive/grain_artifacts_p0035_2026-08/` — chain/region grain artefacts (repo root)
- `05_thesis_writing/notes/srq4-experiment-design-rationale.md` — why the SRQ4 prompt set replaced the archetype taxonomy
- `user-docs/handovers/2026-07-13_harness-and-srq4-decisions-handover-brian.md` — DEC-GRAIN, DEC-ARMS, the L0–L3 tier design
