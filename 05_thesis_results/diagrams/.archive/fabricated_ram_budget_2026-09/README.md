# `ram_budget_v1` — quarantined 2026-09-06 (P0046 F12)

**Do not cite this figure.** Its seven bar values are hardcoded invented numbers,
flagged as fabricated by P0040 finding F5 and never corrected:

```
Python runtime + libraries    500 MB
LangGraph state               100 MB
Feature matrix (post-extract) 300 MB
Active ML model (worst case)  512 MB
Nielsen raw load             1000 MB
Indeks raw load               970 MB   <-- dataset never used (P0046 F6)
Synthesis state + LLM buffer  250 MB
```

The "Indeks raw load" bar is independently disqualifying: that dataset was
dropped on 2026-09-06 as never used, so the figure charts memory consumed by
data the thesis does not touch.

## Why it is here rather than deleted

The *figure* is wrong; the *question* is legitimate and the thesis needs an
answer to it. Real measurements now exist:

- `05_thesis_results/appendix/02_substrate_resource_profile.{md,csv}`
- `05_thesis_results/appendix/04_sandbox_resource_profile.{md,csv}`
- `05_thesis_results/srq1_model_performance/tables/sandbox_profiling.csv`

## To restore

Rewire `fig4_ram_budget()` in
`05_thesis_results/generate_architecture_diagrams.py` to read those appendix
tables instead of its `items` literal, drop the Indeks bar, then re-run. Until
then the function regenerates the fabrication on every run -- which is what
happened on 2026-09-06 when graphviz was installed and the generator ran for the
first time in months.
