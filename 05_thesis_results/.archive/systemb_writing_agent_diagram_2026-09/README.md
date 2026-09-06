# `generate_systemB_diagram.py` — archived 2026-09-06 (P0046 F26)

Renders a multi-agent **thesis writing** system: Thesis Coordinator, Planner
Agent, Writing Agent ("Bullet points only (never prose)"), Critic Agent, Outline
Agent, APA Citation Agent, Thesis Writer Agent.

## Why archived

That system was never built. It is not the SRQ2 structured tool interface, and
not the SRQ4 scenario harness — the two artefacts the thesis actually presents.
A repo-wide search for its output filename `system_b_overview` returned three
files: this script, its byte-identical shadow copy, and the P0046 plan. **No
chapter cites it.**

Leaving it in a shipped tier would invite a defence question about an artefact
that does not exist.

## History

- Lived at `05_thesis_writing/figures/generate_systemB_diagram.py`, writing into
  the writing tier — which DEC-P0046-SINGLE-HOME forbids.
- 2026-09-06: relocated to `05_thesis_results/`, repointed at
  `THESIS_RESULTS_DIAGRAMS_DIR`, staleness warning added.
- 2026-09-06: archived here once the keep/adapt/delete call was made.

The shadow copy is at `.archive/shadow_scripts_2026-09/`.

## If you want it back

It runs as-is: `python generate_systemB_diagram.py` writes
`system_b_overview.{svg,png}` to the diagrams directory. Nothing is broken about
it — it is simply about the wrong system.
