---
pid: P0051
created: 2026-09-08 00:00:00
updated: 2026-09-08 00:00:00
---

# P0051 — Progress

## 2026-09-08 — Plan created; investigation only, nothing executed

Split out of the P0050 figures/tables session. Brian asked two questions:

1. *Did we ever treat the skewness in each EDA category script based on the
   skewness values identified?*
2. *Did we apply the `adf_per_brand` recommendations (log1p+diff, log1p) to the
   datasets in the category-specific EDA?*

**The answer to both is no — computed and reported, never consumed.**

Investigation: two parallel repo-wide searches, plus a third exhaustive
`grep -ril "adfuller\|adf_"` including `worktrees/`. The negative is exhaustive,
not merely thorough. Recorded as F1-F7 in `findings.md`.

**No files were changed.** No pipeline code, no prose, no results.

### The judgement reached

This is **not a modelling defect**. Per-brand transform selection on n=46 series
would be worse than the uniform treatment actually applied — low ADF power, noise
fitting, inconsistent feature semantics. The pipeline's own note says as much,
and `step_2_eda_descriptive.py:571-573` counts the recommendations before printing
it, so the heterogeneity **was observed** and the universal transform was the
deliberate response.

It is a **prose problem**: Ch4 implies the diagnostics drove a decision they only
corroborated, and one claim (blanket differencing) is contradicted by the
chapter's own Table 3 for RTD.

### Next session starts here

1. Read `findings.md` F1-F2 (what was measured), then F5 (the two Ch4 anchors).
2. Decide (a) correct the prose / (b) wire it in / (c) stop computing it.
   F3 argues for (a).
3. `pipeline_config.py:218` is a one-line fix available immediately.
4. Coordinate with **P0048**, which owns the Ch4 prose pass — do not rewrite the
   same paragraph twice.
