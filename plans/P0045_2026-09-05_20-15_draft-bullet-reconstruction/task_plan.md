---
pid: P0045
created: 2026-09-05 20:15:00
updated: 2026-09-05 20:15:00
status: in_progress
focus_detail: "Rebuild sections-drafts/*.md as claim/argument bullet skeletons from the 2026-09-05_19-52 snapshot prose, and wire in the 8 disconnected writing-notes. Task 1 (survey) done; starting Ch5."
---

# P0045 — Draft bullet reconstruction

## Goal

`sections-drafts/*.md` is the planning surface for the thesis (per
`.claude/rules/writing-surface-authority.md`). The 2026-09-01 P0044 prose strip
removed paragraphs but **did not convert the arguments they carried into
bullets**. 56 of 222 sections are now hollow headings. Separately, all 8
`writing-notes/` files are referenced by **zero** drafts.

Rebuild the drafts so each section carries the *claims and arguments* the prose
makes, plus the rationale from writing-notes, without reintroducing prose.

## Scope boundary (Trust tier — do not cross)

- **No prose.** Bullets state a claim, its warrant, and its evidence pointer.
  If a bullet reads as a sentence that could be pasted into the .docx, it is
  too long. The .docx stays authoritative for prose.
- **Never edit** `docx-exported-snapshots/` — read-only mirror.
- Bullets are *derived from* but not *a copy of* the prose. A section that
  argues X because Y, evidenced by Z becomes three bullets, not a paragraph.

## Evidence: what the strip actually cost

| file | sections | hollow | % |
|---|---:|---:|---:|
| ch5-framework-design | 10 | 6 | 60% |
| ch2-literature-review | 26 | 12 | 46% |
| ch9-discussion | 13 | 6 | 46% |
| ch1-introduction | 11 | 4 | 36% |
| ch4-data-assessment | 17 | 6 | 35% |
| ai-declaration | 6 | 2 | 33% |
| abstract | 8 | 2 | 25% |
| ch3-methodology | 54 | 10 | 18% |
| ch8-evaluation | 18 | 3 | 16% |
| ch7-synthesis | 13 | 2 | 15% |
| ch6-model-benchmark | 37 | 3 | 8% |
| ch10-conclusion | 6 | 0 | 0% |
| **total** | **222** | **56** | **25%** |

Word-count delta is a weaker but corroborating signal: ch2 3,250 draft vs
6,286 snapshot; ch5 1,003 vs 2,161; ch1 1,143 vs 3,084.

**Ch3 and ch6 are the inverse case** — draft *exceeds* snapshot (ch3 5,225 vs
3,258). Those drafts hold planning content the .docx never had. Do not
overwrite; merge.

## Writing-notes: 0/8 wired in

| note | words | belongs to |
|---|---:|---|
| sample-size-and-tool-interface-rationale | 8,052 | ch4, ch5, ch6, ch7, ch8, ch10 |
| srq4-experiment-design-rationale | 2,756 | ch3, ch5, ch8, ch10 |
| srq1-model-ladder-and-baselines | 2,758 | ch5, ch6 |
| srq1-pooled-vs-per-category | 2,570 | ch6, ch8 |
| prometheus-scenarios-design-rationale | 2,153 | ch3, ch7, ch8 |
| srq1-tuning-and-validation-protocol | 2,029 | ch3, ch5 |
| srq4-first-results-and-interpretation | 1,460 | ch8, ch9, ch10 |
| chapter-staleness-audit | 1,433 | ch3–ch10 (meta) |

The staleness audit is the highest-value one and the most dangerous to ignore:
it records that **ch6 passes the automated fact-checker while every headline
number in it is wrong** (RTD off by 5.1pp). That belongs in ch6's draft as a
standing warning, not in a separate file nothing links to.

## Bullet contract

Each non-hollow section gets, in order:

```markdown
## 5.3 The Forecasting Substrate (SRQ1)

**Claims**
- Five lightweight models span the accuracy/memory frontier -- <=8GB never binds
- Per-category beats pooled on 3 of 4 categories; the exception is a finding

**Warrant**
- Standard benchmark set, not a convenience choice -> [[srq1-model-ladder-and-baselines]]
- Expanding-window CV; trial budget justified empirically, no citation exists
  -> [[srq1-tuning-and-validation-protocol]]

**Evidence**
- `04_thesis_results/srq1/cv_metrics.csv` -- current WMAPE per category
- Table 5.1 component RSS (measured)

**Open**
- RAM figure: draft says 8 GB, measured production template is 4096 MB (P0044 F22-F23)
```

Not every section needs all four headers. `Open` only where something is
genuinely unresolved.

## Phases

| # | Phase | Chapters | Status |
|---|---|---|---|
| 1 | Survey + contract | all | complete |
| 2 | Hollow-heavy rebuild | ch5, ch2, ch9, ch1 | pending |
| 3 | Merge-not-overwrite | ch3, ch6 | pending |
| 4 | Moderate rebuild | ch4, ch7, ch8 | pending |
| 5 | Short files | abstract, ai-declaration, ch10 | pending |
| 6 | Wire writing-notes + verify | all | pending |

## Sequencing rationale

Phase 2 first because those four are where content was actually lost. Phase 3
is a different operation (merge, risk of destroying planning content) and is
kept separate so it is never done on autopilot. Phase 5 last — smallest payoff.

## Related

- `.claude/rules/writing-surface-authority.md` — the rule this plan operates under
- `plans/P0043_.../` — Word comment audit; the comment corpus names many of the
  same gaps (LLM-as-judge removed but still written up, RAM premise, exogenous)
- `plans/P0044_.../findings.md` — F22-F23 RAM measurement, F6 drift evidence
- `05_thesis_writing/.archive/2026-09-01_superseded-prose/` — pre-strip prose,
  the fallback source if the snapshot is ambiguous
