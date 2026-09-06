# `fig2_granularity.png` — archived 2026-09-06 (P0046 F4/F17)

**The most dangerous artefact this plan found**, because it looked correct: right
folder, right name, same 2026-07-11 date as its legitimate siblings
(`fig1_model_ladder`, `fig3_forecast_overlay`).

It depicts a brand-vs-chain grain comparison that DEC-GRAIN (2026-07-12) decided
to stop making. P0035 deleted the producing code — `srq1_figures.py` still
carries the note "GRAIN NOTE (P0035, 2026-08-01): fig2_granularity.png is no
longer produced." The image outlived its producer by two months.

Verified before archiving:
- committed in git at `4c7a98b` and again in the flatten `8329881`
- **cited by zero chapters** (repo-wide search for the filename returns only
  plan docs and the two copies of `srq1_figures.py`)

Archived rather than deleted so the grain decision keeps a visual record, while
the live `figures/` folder contains only artefacts a live script produces.
