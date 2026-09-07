---
name: p0048-inherited-context
description: STATE - Live content absorbed from P0045 (draft bullet reconstruction) and P0047 (exogenous enrichment) when both were archived on 2026-09-07. Everything still open from those plans is here.
pid: P0048
created: 2026_09_07-18_30
updated: 2026_09_07-18_30
status: inherited
---

# Inherited context — P0045 and P0047

Both plans were archived 2026-09-07. Their **writing-side** open work moved here;
their **experimental** open work moved to P0049. This file is the record of what
came across, so nothing depends on reading an archived folder.

**Division of labour after the archive:**

| Plan | Owns |
|---|---|
| **P0048** (this) | Prose, drafts, Word threads, claims verification, citations |
| **P0049** | Horizon fix, SRQ1 re-runs, funded SRQ4 scenarios |

P0049's `START_HERE.md` says explicitly: *"Don't do prose from P0049."* Respect that
boundary in both directions.

---

## PART A — from P0047 (exogenous enrichment / holiday calendar)

Folder was `.archive/P0046_2026-09-05_21-10_exogenous-enrichment-decision` (frontmatter said
P0047; the folder name never caught up). **Numbers are locked and the experiments are
finished** — 19 of 22 tasks complete.

### A.1 What shipped

Danish public-holiday calendar (Nager.Date API), three features at brand × month:
`days_in_month`, `n_holidays`, `non_holiday_days`.

**Result: helped in 7 of 12 category × model cells, mean −1.42 pp WMAPE.** Report the
per-model and per-category split, **never the mean alone** — the model-family
difference is itself the finding (Ridge 3/4 −2.49 pp; LightGBM 3/4 −2.45 pp; XGBoost
**1/4, +0.68 pp**).

**Decision 3 (2026-09-06): SHIP and report honestly**, even though the result is mostly
null. Option C was pre-registered before the answer was known; changing the reporting
rule once the result turned unfavourable would be a researcher degree of freedom. The
null is the substantive finding — seasonality in Danish beverage demand is
**trade-driven, not holiday-driven** at monthly grain.

**Rejected: splitting by model family** (holiday features for Ridge only). The SRQ1
cross-model ranking depends on every model seeing the same information.

### A.2 The three open tasks — all Brian's, all writing-side

| Was | Now | What |
|---|---|---|
| P0047 task 8 | **P0048 task 9** | Close five Word threads: ch1 15/18/20, ch2 66/69, ch3 127, ch4 177, ch5 207. Answer is "built, measured, reported" — not withdrawn |
| P0047 task 20 | superseded by 22 | Register rows now map to CV-01…CV-05 |
| P0047 task 22 | **P0048 task 10** | Run the NotebookLM claims verification |

### A.3 Claims verification — the procedure, so it is not reinvented

Briefing pack is built and ready at
`06_thesis_writing/notebookLM/04-Claims_Verification/`:
`00-MASTER-verification-brief.md`, `01-HOW-TO-RUN.md`, `NLM Review/` for output,
`Candidate Sources/` for PDFs.

**TWO notebooks, not one:**

- **A** = CV-01, CV-02 — statistical thresholds, needs statistics literature
- **B** = CV-03, CV-04, CV-05 — specific documents (Danish shop-hours law, XGBoost
  docs, Store Bededag act)

Mixing them makes a statistics question retrievable against a shop-hours law.
**If only one run is possible, do A** — CV-01 and CV-02 appear as numbers in a results
appendix.

**Do NOT upload thesis chapters.** The claim text is already quoted in the brief, and
uploading our own prose lets the notebook return our own wording as a source — the exact
failure that created CV-01.

| ID | Claim | State |
|---|---|---|
| CV-01 | VIF 5 / 10 bands | Attribution to *Hair et al. (2019)* was **invented from memory**, removed |
| CV-02 | Spearman ≥ 0.95 cluster threshold | Never had a source; a chosen parameter |
| CV-03 | Lukkeloven 2012 | Substance confirmed; statute name/year unverified |
| CV-04 | XGBoost thread mechanism | **Effect measured**; explanation unsourced |
| CV-05 | Store Bededag abolition | Effect visible in data; bill number unverified |

**Rule: if a source is not in the Zotero library, it is not a source.**
Source of truth for outcomes: `writing-notes/unverified-claims-to-check.md`.

### A.4 Reporting requirements that must survive into prose

1. The delta table, all cells, whatever the signs
2. SHAP before/after — establishes the features are **not** a month re-encoding
3. Appendix table 92 — the structural argument (Easter moves; Store Bededag)
4. Robustness checks: 5 seeds, single-feature variant, widened alpha grid
5. The **rejected** VIF reduction — trees use correlated lags productively
6. Both of Claude's over-claims, since they are corrected in the record

### A.5 Superseded numbers that must not reappear

| | superseded | **correct** |
|---|---|---|
| cells helped | 6/12 | **7/12** |
| mean delta | −0.75 pp | **−1.42 pp** |

---

## PART B — from P0045 (draft bullet reconstruction)

**6 of 11 tasks were still open.** This is genuinely unfinished work, not a closed plan.

### B.1 What it was doing

P0044's prose strip (2026-09-01) kept headings, lists and tables and dropped paragraphs
— but a thesis paragraph carries a *claim*, and the claim is planning content. Nothing
captured it on the way out, leaving `sections-drafts/*.md` as "an index of where the
argument used to be."

Rebuilding them as **Claims / Warrant / Evidence / Open** skeletons.
**Ch9 is the reference implementation**, not ch1 — it was never prose-heavy so the strip
barely touched it, and it still carries its design-principles table and novelty claims.

### B.2 Open tasks, carried across

| Was | Now | What | Note |
|---|---|---|---|
| P0045 t6 | **P0048 t11** | Merge ch3-methodology | **MERGE, not rebuild** |
| P0045 t7 | **P0048 t12** | Merge ch6 + stale-numbers warning | **MERGE**; see B.4 |
| P0045 t8 | **P0048 t13** | Rebuild ch4 bullets (4 hollow) | Coordinate with the ch4 prose pass |
| P0045 t9 | **P0048 t14** | Fill ch7 + ch8 hollow sections | Ch8 design subsections are bullets (F8) |
| P0045 t10 | **P0048 t15** | Fill abstract, ai-declaration, ch10 | Smallest payoff, do last |
| P0045 t11 | **P0048 t16** | Verify wiring; re-run hollow audit | Target **22 → 0** |

### B.3 ⚠ Ch3 and ch6 are MERGE operations — rebuilding destroys content

| chapter | draft words | snapshot words | delta |
|---|---:|---:|---:|
| ch3-methodology | 5,225 | 3,258 | **+1,967** |
| ch6-model-benchmark | 3,991 | 4,727 | −736 |

Ch3's draft holds planning material that **never went into the `.docx`**. Rebuilding it
from the snapshot would destroy it. This is a materially different operation from
ch1/ch2/ch5 and must never be done on autopilot.

Corollary: word-count delta alone does not tell you what to do. Ch6 is only −736 yet has
3 hollow sections; ch3 is +1,967 yet has 10.

### B.4 Ch6's stale numbers — independent corroboration of P0048 F7

`writing-notes/2026_08_22-21_00-chapter-staleness-audit.md` records ch6 as **passing**
`check_chapter_facts.py` while every headline number in it is stale:

| Category | ch6 claims (XGBoost) | measured | drift |
|---|---:|---:|---:|
| CSD | 16.5 % | 15.2 % | −1.3 pp |
| danskvand | 23.8 % | 20.9 % | −2.9 pp |
| energidrikke | 11.4 % | 13.0 % | +1.6 pp |
| RTD | 31.0 % | **36.1 %** | **+5.1 pp** |

The checker matches stale *phrases* and has no rule for a number that used to be right.
**Two independent routes reached this** — P0045 F5 via the audit, P0048 F7 via the
result files. It goes into ch6's draft as a standing `Open` block.

⚠ **These are also pre-horizon-fix.** P0049's re-run will move them again, so record the
*mechanism* (the checker cannot see stale numbers), not just today's digits.

### B.5 The hollow-section audit

Detector: `utility_scripts/scripts/check_draft_hollow_sections.py` (verified present).

**True baseline is 22 hollow of 195**, not the 56 first reported — the original detector
wrongly counted a `##` divider whose content lives in `###` children. Phase 2 took it to
**14**. Task 16's success criterion is **22 → 0**.

**Check word-count delta as well as hollow count.** Ch2 showed 0 hollow yet was down
3,036 words — a section can carry a stub bullet and still have lost its argument.

### B.6 All 8 writing-notes were orphaned

`grep -rl <note-slug> sections-drafts/` returned **zero** for every note — ~23,200 words
of design rationale invisible from the surface meant to drive the writing. Wiring them in
is part of task 16.

### B.7 Cross-chapter contradictions the per-anchor Word comments cannot see

- **RAM bound:** ch2/ch5 say **4 GB**; ch1 and ch9 still say **8 GB**; ch5 §5.8 says
  both. P0049 task 8 owns the ch1 rewrite on the measured 4 GB bound — coordinate.
- **LLM-as-judge** is flagged `OUTDATED`/`INCORRECT` across ch3 ×9, ch7 ×7, ch8 ×10,
  ch9, ch10. Where a bullet would restate what a comment already raises, **cite the
  thread id** rather than duplicating — do not let drafts become a third place a
  decision is recorded.

### B.8 ⚠ Figure paths in the drafts are stale — deliberately not repaired

`06_thesis_writing/figures/` was re-sorted into triage subfolders:

| folder | contents | reading |
|---|---|---|
| `unsure/` | `ch2_gap_diagram` | keep-or-cut undecided |
| `update_formatting/` | `ch5_architecture_v1` | content fine, presentation not |
| `update_information/` | `ch1_research_questions_tree`, `data_flow_v1`, `ram_budget_v1`, `system_architecture_v1` | **factually stale** |

So `![...](../figures/ch5_architecture_v1.png)` in the ch5 and ch1 drafts no longer
resolves. **Left broken on purpose:** repointing at `../figures/update_formatting/...`
would encode a triage staging path as a destination, and the files move again once
triage finishes. Restore the canonical path when the figure is updated.

`ram_budget_v1` landing in `update_information/` independently corroborates B.7's RAM
contradiction — it is the figure that draws the budget, already judged out of date.

---

## What was NOT carried across

- P0047's completed experimental work (tasks 1–7, 9–19, 21) — history, in the archive.
- P0047's determinism contract — lives in `LOCKED_STATE.md`, which stays where it is and
  is referenced by P0049.
- Anything about the horizon fix, SRQ1 re-runs or funded scenarios — **P0049 owns those.**
