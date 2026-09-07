---
pid: P0045
created: 2026-09-05 20:15:00
updated: 2026-09-05 20:15:00
---

# Findings — P0045

## F1 — The prose strip removed arguments without converting them

P0044's strip (2026-09-01) kept headings, blockquotes, lists and tables, and
dropped paragraphs. The stated rationale was that paragraphs are prose and prose
belongs in the .docx. Correct as far as it goes — but a paragraph in a thesis
carries a *claim*, and the claim is planning content. Nothing captured it on the
way out.

Measured: **56 of 222 sections (25%) are now headings with empty bodies.** Worst
is ch5 at 6/10. Ch1 §1.1 Background and Motivation, §1.2 Research Problem,
§1.4 Delimitation and §1.5 Thesis Structure are all `## heading` followed by
`---` and nothing else.

This is why the drafts feel sparse: they are not a reduced version of the
argument, they are an index of where the argument used to be.

## F2 — Ch9 shows what the drafts should look like

Ch9 was never prose-heavy, so the strip barely touched its bodies. It still has
its DP1/DP2/DP4/DP5 design-principles table, its novelty claims, its limitations
list. That is exactly the target form: claims and evidence pointers, no prose.

Use ch9 as the reference implementation, not ch1.

## F3 — Ch3 and ch6 drafts are LARGER than the snapshot; merging, not rebuilding

| chapter | draft words | snapshot words | delta |
|---|---:|---:|---:|
| ch3-methodology | 5,225 | 3,258 | **+1,967** |
| ch6-model-benchmark | 3,991 | 4,727 | -736 |
| ch2-literature-review | 3,250 | 6,286 | -3,036 |
| ch1-introduction | 1,143 | 3,084 | -1,941 |
| ch5-framework-design | 1,003 | 2,161 | -1,158 |

Ch3's draft holds planning material that never went into the .docx. Rebuilding
it from the snapshot would *destroy* content. Ch3 and ch6 need a merge pass, and
that is a materially different operation from ch1/ch2/ch5 — hence the separate
phase.

Corollary: word-count delta alone does not identify what to do. Ch6 is only
-736 yet has 3 hollow sections; ch3 is +1,967 yet has 10.

## F4 — All 8 writing-notes are orphaned

`grep -rl <note-slug> sections-drafts/` returns **zero** for every one of the
eight notes. ~23,200 words of design rationale — why the model ladder contains
what it contains, why pooled-vs-per-category was run, why LLM-as-judge was
dropped, measured SRQ4 costs — is invisible from the surface that is supposed to
drive the writing.

These are not duplicates of the prose. They answer *why*, which the .docx
mostly does not, and which is exactly what a planning surface should carry.

## F5 — The staleness audit contradicts the current drafts and nothing flags it

`2026_08_22-21_00-chapter-staleness-audit.md` records that ch6 **passes**
`check_chapter_facts.py` while every headline number in it is stale:

| Category | ch6 claims (XGBoost) | current cv_metrics.csv | drift |
|---|---:|---:|---:|
| CSD | 16.5% | 15.2% | -1.3pp |
| danskvand | 23.8% | 20.9% | -2.9pp |
| energidrikke | 11.4% | 13.0% | +1.6pp |
| RTD | 31.0% | **36.1%** | **+5.1pp** |

The checker matches stale *phrases* and has no rule for a number that used to be
right. Ch6 is almost entirely numbers.

This is the single most consequential orphaned fact in the corpus, and it is
sitting in a file no draft links to. It goes into ch6's draft as a standing
`Open` block.

## F6 — This plan and P0043's comment corpus name the same gaps

Independent evidence, same conclusions. The Word comments flag LLM-as-judge as
`OUTDATED`/`INCORRECT` in ch3 x9, ch7 x7, ch8 x10, ch9, ch10; the staleness
audit independently found LLM-as-judge as the dominant automated-checker failure
in ch3, ch7, ch8, ch9, ch10. Same for the RAM premise and exogenous enrichment.

Where a reconstructed bullet would restate something a comment already raises,
cite the thread id rather than duplicating the argument. Do not let the drafts
become a third place a decision is recorded.

## F7 — The 56-hollow figure was inflated; the real baseline was 22

My first detector split on `^#{2,3}` and treated every `##` heading as owning a body.
That is wrong for a **divider heading whose content lives in `###` children** — ch2's
four `## GOODWIN ...` blocks, ch9's `## 9.1`, ch3's phase headers. Each was counted
hollow while being correctly structured.

Corrected detector (now at `utility_scripts/scripts/check_draft_hollow_sections.py`)
skips a `##` immediately followed by a `###`. True baseline: **22 hollow of 195**, not
56 of 222.

The correction does not change the plan — ch1 (4), ch9 (4), ch3 (7), ch4 (4) are still
the hollow-bearing files, and ch5/ch2 were still genuinely empty where the plan said.
It does change two things:

- **Task 11's success criterion** is 22 → 0, not 56 → 0.
- **Word-count delta, not hollow count, is the better severity signal.** Ch2 showed only
  12 hollow on the bad detector and 0 on neither — yet it was down 3,036 words against
  the snapshot, the largest loss in the corpus. A section can carry a stub bullet and
  still have lost its argument. Task 11 should check both.

Recorded rather than quietly fixed because F1 in this file cites the 56 figure.

## F8 — Figures were re-sorted into triage folders mid-session; draft image paths are stale

`05_thesis_writing/figures/` now has three triage subfolders, created by the parallel
session (unstaged at the time of writing):

| folder | contents | reading |
|---|---|---|
| `unsure/` | `ch2_gap_diagram` | keep-or-cut undecided |
| `update_formatting/` | `ch5_architecture_v1` | content fine, presentation not |
| `update_information/` | `ch1_research_questions_tree`, `data_flow_v1`, `ram_budget_v1`, `system_architecture_v1` | **factually stale** |

Consequence: the `![...](../figures/ch5_architecture_v1.png)` and
`../figures/ch1_research_questions_tree.png` references in the ch5 and ch1 drafts no
longer resolve.

**Deliberately not repaired.** Repointing them at `../figures/update_formatting/...`
would encode a triage staging path as if it were a destination, and the files move again
the moment triage finishes. The right fix is to leave the canonical path and restore the
figure to it once updated.

`ram_budget_v1` landing in `update_information/` is independent corroboration of the RAM
contradiction: it is the figure that draws the budget, and it has already been judged
factually out of date. Ch6's draft separately carries a stale `fig4_ram_budget` flag.
