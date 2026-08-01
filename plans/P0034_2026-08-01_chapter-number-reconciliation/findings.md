---
pid: P0034
created: 2026-08-01 00:00:00
updated: 2026-08-01 00:00:00
---

# P0034 — Findings

## Pre-existing (grep run 2026-08-01)

### F1 — the answer to Enrico's question #2 is "yes, extensively"

Enrico asked whether the leakage fix collides with anything that hard-codes old numbers.
It does: **13 distinct locations across 4 chapter drafts**, with the same four headline
WMAPE figures repeated in **three separate tables inside ch6 alone** (lines 119–122,
153–156, 201–206), then again in ch8, ch9, and ch10.

Practical consequence: this is not a find-and-replace. The same number appears in
different framings (absolute, delta, range), so each occurrence needs its own treatment.

### F2 — the chain-grain problem is bigger than the leakage problem

Ch6's tables are structured around a **brand×month vs brand×chain** comparison, and
danskvand's *selected* configuration is brand×chain (22.0% WMAPE, line 204).

DEC-GRAIN (2026-07-12) drops the chain grain from active results, demoting it to a
documented limitation. So:

- Ch6 lines 119–122 lose a column.
- Ch6 lines 201–206 lose their "Selected granularity" column entirely.
- danskvand's headline number changes from 22.0% (chain) to 23.8% (month) — **a
  regression in the reported result**, purely from the grain decision, before any
  leakage effect.

This is a structural rewrite, and danskvand's number getting *worse* is the kind of thing
Enrico needs to sign off on knowingly. Flag it loudly.

### F3 — derived quantities are the easy thing to miss

Beyond raw figures, these are computed *from* them and will silently go stale:

- "+7.7 pp", "+4.3 pp", "+17.2 pp" ML-vs-ARIMA deltas (ch6:153–156, ch9:67)
- "test WMAPE 11.4–31.0%" range claim (ch10:21)
- "improved WMAPE by roughly 2–4 pp over untuned" (ch6:126)
- "near the ≤15% industry target" — a *qualitative* claim contingent on energidrikke
  staying at 11.4%. If the leakage fix pushes it above 15%, this sentence inverts.

F3's last item is the highest-risk single sentence in the drafts: energidrikke is both
promo-affected *and* the category carrying the thesis's strongest claim.

### F4 — V2 (mean-MAPE) is already handled in prose

Ch6 §6.5.1 (lines 109–113, 186–187) already explains that plain mean MAPE is not reported
because it diverges on low-volume categories. Enrico's V2 finding is therefore already
reflected in the writing — no prose change needed for V2, only the code-side suppression
in the S01 retrain.

### F5 — the ≤15% "industry target" is unverified, and it is load-bearing

The claim originates at `ch6-model-benchmark.md:92`:

> Target MAPE: ≤15% (industry benchmark for retail demand forecasting — cite ML-Based FMCG 2024)

The parenthetical is still a **drafting instruction** ("cite X"), not a completed citation.
From there it is restated as established fact in four places (`ch6:137`, `ch8:46`,
`ch9:18`, `ch10:21`), each time without the hedge.

Named source: Springer LNCS / INFUS 2024, *"Machine Learning-Based Demand Forecasting for
an FMCG Retailer"* (`references.md:46-47`; also `01_thesis_research/literature/scraping_log.md`
row 2). Whether that paper asserts a ≤15% MAPE benchmark is **unverified** — task 8.

Two reasons this is more than a tidiness issue:

1. It is the yardstick for the thesis's strongest empirical claim (energidrikke 11.4%
   "near the ≤15% industry target"). An unsourced yardstick makes the claim unfalsifiable.
2. P0032's leakage fix may push energidrikke above 15%, which would invert that sentence.
   Rewriting it around a threshold that has no source would compound the problem.

Cross-check `01_thesis_research/literature/gap_analysis_v4.md`, which discusses SRQ1
forecasting sources ([[ml_fmcg_demand_forecasting]], [[fmcg_demand_forecasting_methods]],
[[retail_ml_tree_ensembles_lstm]]) — if a defensible threshold exists anywhere in the
corpus, it is likely there.

### F6 — Totalbeer justification

Brian's stated reason (2026-08-01): excluded on **compute constraints** — significantly
larger than any other category, ~10M rows. Prose must state this rather than silently
dropping beer, otherwise a reader comparing Ch3's five-category framing to the results
sees an unexplained gap.

---

## Discovered during execution

<!-- append below -->
