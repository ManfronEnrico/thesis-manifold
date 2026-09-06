---
pid: P0046
created: 2026-09-05 20:40:00
updated: 2026-09-06 19:00:00
---

# P0046 — Progress Log

> Condensed 2026-09-06. Full session-by-session narrative is in git history;
> this keeps what a future session needs.

**Branch:** `thesis/draft-bullet-reconstruction` (inherited from P0045).
**Uncommitted:** ~1000 paths. Worth committing before further moves.

---

## Where things stand

Read `task_plan.md`'s STATUS QUO table first. Summary: the architecture is
settled, paths are fixed and verified, regenerability has been *tested* rather
than assumed, and one blocker remains (system graphviz).

---

## What actually happened, in order

**Session 1 (09-05)** — Traced ~70 artefacts. Found only 7-8 live producers, so
the sprawl was one script writing where it was told, not 70 independent origins.
Found the dangerous one: `fig2_granularity.png`, right folder, right name, same
date as its siblings, depicting a comparison DEC-GRAIN decided to stop making
and whose producing code P0035 deleted.

**Session 1b (09-05)** — Brian's three decisions. Two corrected me:
- I called the 18 `analysis/figures*` files unfixable. They are archived, not
  broken — a hardcoded macOS `FIGURE_DIR` and a stale scope are *edits*. Became
  per-file RESTORE-or-RETIRE.
- I held up `04_thesis_results/appendix/` as the model to copy without noticing
  it is a *production* site under the same contract. Sharpened the rule to **no
  generator writes into the writing tier**.

**Session 2 (09-06)** — Brian dropped the curation layer entirely: tier 06 holds
no artefacts at all. His reason was the sharing boundary; the stronger reason is
that it **removes the second copy**, which the manifest existed to police. I had
been building a defence against a problem I was creating.

Also reversed my own Q3 answer twice. I proposed `00_thesis_context/diagrams/`
on the grounds that "the production tree is what assessors read" — while getting
that tree's boundary wrong, since tier 00 is not shipped either. Lesson recorded:
**semantic fit is carried by the producer's location and subfolder name, not by
which tier the output lands in.**

**Session 3 (09-06)** — Brian restructured to SRQ-aligned tiers. Asked me to
update PATHS "accordingly"; probing first found **32 of 34 constants resolving to
non-existent paths**. Every pipeline script was broken, invisibly, because
`Path()` never validates and `import PATHS` still succeeded.

This is the plan's own thesis proving itself: because paths were centralised,
**one file needed repair instead of forty**, and one probe enumerated the whole
blast radius.

Brian's judgement beat mine twice more:
- *EDA split*: I proposed promoting hand-picked candidates. He split by file
  type — `.csv` stays (downstream steps consume it), `.md`/`.png` promote. Mine
  required a human decision per file before the citation sweep, i.e. backwards.
- *SRQ4 runs*: I offered fold-under-`raw/` or keep-as-is. He said runs don't
  belong in results at all. That retro-answered what I couldn't answer earlier
  ("what would `raw/` hold for SRQ1?") — nothing; `raw/` was the wrong idea.

And a correction: I wrote the ship boundary as "tiers 00-04". Tier 00 is
excluded too.

**Session 3b-3d (09-06)** — Full script sweep, then testing.

Audit went **43 flagged scripts → 10**, all 77 live scripts compile. The
`CLAUDE.md` → `.env.example` swap exposed two defects that were *not* the anchor:
`.gitignore` excluded `.env.example` (an uncommitted anchor cannot anchor a fresh
clone — the swap would have been worse than what it replaced), and every inline
finder walked from `cwd` rather than `__file__`, so any run from outside the repo
failed.

Then the shift that mattered most: **I ran the generators instead of reasoning
about them.** Three passed. Two failed on missing dependencies — and
`requirements.txt` turned out to omit `graphviz`, `matplotlib` and `statsmodels`
entirely. An assessor cloning the repo could reproduce **no** figure. Not
findable by reading the scripts.

Correction to my own first report: I initially said `shap` and `xgboost` were
undeclared. They are declared — my grep only read the first 25 lines. The real
gap was `graphviz` (undeclared *and* uninstalled), plus `matplotlib`/
`statsmodels` (undeclared, coincidentally installed).

Two confirmations from running things:
- `srq1_generate_performance_figures.py` produced 3 figures and did **not**
  recreate the zombie — P0035's removal is genuinely in the code, so archiving
  it is safe.
- `export_appendix.py`'s generated README hardcoded a producer path dead since
  the restructure: the index told readers to run a script that no longer exists.
  Now derived from `__file__`, so it cannot go stale again.

**SRQ2 is worse than Brian flagged, usefully so.** He suspected the LLM-as-Judge
files. A producer search found **zero** live producers — all five files are
orphaned, including the two 2026-08-19 synthesis outputs, because those scripts
were archived in August. The question is not "are the judge files stale" but
"can anything here be reproduced at all".

---

## Recurring errors

| Error | Note |
|-------|------|
| `grep -rn` over the repo times out at 120s | Third session running. Fix (use the Grep tool) was logged by me twice and I reached for `grep` anyway. Genuine `/errors-log` material |
| Bulk-edit scripts broke syntax twice | Block inserted inside a function; closing paren after a comment. The compile sweep caught both instantly — keep it as a gate |
| Plugin hook flags `focus_detail` frontmatter | False positive: that field is required by `workflow-planning-with-files.md`. Not stripped |

---

## Next session starts here

1. `winget install Graphviz.Graphviz`, reopen shell, re-run
   `05_thesis_results/generate_architecture_diagrams.py` → 6 diagrams.
2. Phase 3b: SRQ1 folder shape (33 loose files), SRQ2 orphan triage, EDA
   promotion (119 md + 30 png).
3. Phase 5's citation sweep unblocks both remaining orphan questions (F12, F28).
