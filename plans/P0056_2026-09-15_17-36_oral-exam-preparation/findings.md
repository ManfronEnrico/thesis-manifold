---
name: p0056-findings
description: STATE - What the submitted thesis actually says, which plan-folder claims it supersedes, and the verified numbers any slide may quote.
pid: P0056
created: 2026_09_15-17_36
updated: 2026_09_15-18_05
---

# P0056 — Findings

## F1 — Currency, stated so a later reader knows what this was verified against

- Repo at **`83689d3`**, branch `thesis/svg-table-styling`, fetch clean, 6 ahead of `origin/main`, nothing incoming.
- Snapshot **`2026-09-15_17-43_oral-exam-prep`**; source `.docx` modified 15:40:33, SHA `0b8c197b…`, **47,299 words**, 17 level-1 chapters, 30 tables, **1** live comment.
- Zotero re-pulled the same session: **88 items**.
- **Step 3 of `/re-snap` (diff against previous snapshot) deliberately skipped.** It exists to show which proposed fixes an author applied; the thesis is submitted, so there is no pending pass. Previous snapshot was 110 minutes earlier.

## F2 — The submitted document's shape

| Ch | Subject | Words |
|---|---|---:|
| 1 | Introduction | 3,108 |
| 2 | Literature Review | 6,307 |
| 3 | Methodology | 4,110 |
| 4 | Data Assessment | 5,665 |
| 5 | Model Benchmark & Selection | 8,205 |
| 6 | Predictive-Extension Architecture | 3,317 |
| 7 | The Structured Tool Interface | 5,596 |
| 8 | Experimental Evaluation | **2,318** |
| 9 | Discussion | 3,707 |
| 10 | Conclusion | 1,663 |

**Ch8 carries the thesis contribution in the fewest words of any substantive
chapter.** That is where an examiner with limited time will push, because it is
where the claim lives and where there is least text to defend it.

## F3 — Verified headline numbers, read from the artefact not the prose

Source: `05_thesis_results/08_experimental_evaluation/tables/22_scenario_comparison.csv`
(9 runs per scenario, 63 total).

| Measure | A plain | B data+code | C model | D prod+code | E prod+model | F both | G prod+both |
|---|---:|---:|---:|---:|---:|---:|---:|
| Usable answers | **6**/9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Median APE % | 502.2 | 2.9 | 14.6 | **0.9** | 14.6 | 7.3 | 1.8 |
| Mean APE % | 662.1 | 27.9 | **13.1** | 25.0 | 13.1 | 18.3 | 15.6 |
| CV across repeats % | 26.7 | 4.1 | **0.0** | 8.1 | **0.0** | 1.7 | 3.3 |
| Replicability % | 0 | 0 | **100** | 0 | **100** | 33 | 33 |
| Cost/answer USD | 0.3798 | 0.4667 | **0.0091** | 0.7664 | 0.1994 | 0.4253 | 0.5536 |
| Response time s | 69.5 | 123.8 | **6.0** | 111.3 | 31.7 | 103.9 | 84.4 |

**Derived, computed not transcribed:** C vs B = **51.3×** cheaper
(0.4667/0.0091), **20.6×** faster (123.8/6.0). The thesis says "roughly fifty"
and "roughly twenty" — consistent.

⚠ **D is the most accurate rung on the median (0.9%), better than B (2.9%).**
The abstract and Ch10 do not foreground this. An examiner reading the appendix
table can. Be ready: the production orchestrator's *code* arm beat the
general-purpose one, which is an orchestrator effect on the code path, not a
point for the artefact. Drill this.

## F4 — Total evaluation cost, and which figure is which

Ch8 §8.3.1: **$19.60** actual (account-balance delta, the only non-estimated
figure); **$25.20** token-based estimate, a 29% overshoot; $18.46 from the
billing endpoint for an incomplete window. ≈**31 cents per run**.

Quote $19.60 as the cost. Per-scenario costs in the table above are **token
estimates and therefore upper bounds** — say so if pressed.

## F5 — ⚠ CORRECTION to P0055 F4: two claims it makes are superseded by the submitted text

P0055's `findings.md` F4 (written 2026-09-12) says Ch9 §9.1.4 states the
code-as-action baseline *"was not executed"*, and that Ch8 is a 1,384-word
skeleton with `[N] SKUs × 28 retailers × [T] weeks` placeholders and a weekly
grain. **Both were fixed before submission. Do not repeat either.**

- Ch9 §9.1.4 now reads *"executed as a ladder of seven scenarios over sixty-three funded runs"*.
- Ch8 is 2,318 words, monthly grain, no placeholders found.

**And the consequential one:** Ch9 §9.4 **already states the lag-13 defect in
full**, as *"a gap of provenance between the analytical and engineering layers
rather than of method… the same class of defect the structured interface is
designed to prevent downstream of the model."*

So the lag-12/13 issue is **an owned limitation in the submitted thesis**, not a
post-submission discovery. This reframes Phase 2 entirely: the "transparent"
variant foregrounds a limitation the thesis already makes, and the "silent"
variant merely omits a slide about text the examiner can read. **Neither variant
conceals anything.** Brian must be told this before choosing.

Lesson, and it is the one `plan-verification-discipline.md` already states: a
plan folder records intent at a moment. The submitted `.docx` is ground truth.

## F6 — Gaps in the inherited defence file, for Phase 4

`anticipated-assessor-questions.md` is strong (~25 questions, measured answers,
explicit concessions). Its **U1–U3 are now answerable** — they were blocked on
"the funded run", which has since run (63 runs). Those three rows are stale and
read as open questions when they are closed.

Questions it does **not** yet cover, all askable from the submitted text:

1. **Why is D more accurate than B?** (F3) — an orchestrator effect on the code path, unaddressed.
2. **Why does Ch8 devote 2,318 words to the thesis's own contribution?** (F2)
3. **Two categories are beaten by a parameter-free seasonal naive / Prophet** (Ch9 §9.1.1, Ch10). The thesis reports this well; the defence needs a crisp 20-second version.
4. **The thesis cites ~2 figures against 87 generated SVGs and ~317 result files.** Why is so little shown?
5. **DSR with one cycle** — design principles are *derived, not validated*. Ch10 §10.4 concedes it; expect a methodology examiner to press.
6. **"Bounded tool-using agent, not a multi-agent system"** (Ch9 §9.2.1, citing Sapkota et al.) — a framing correction the thesis makes about itself. Invites "so what is agentic about it?"

## F9 — ⚠ The submitted thesis reports two different peak-memory figures for the same models

Found 2026-09-15 while verifying SRQ1 numbers for the deck. **Both are in the
submitted document, forty pages apart.**

| Model | Ch9 §9.1.1 | Ch6 Table 20 | `15_substrate_resource_profile.md` |
|---|---:|---:|---:|
| XGBoost | **34.5** MB | **31.9** MB | 34.5 MB |
| LightGBM | **17.9** MB | **14.9** MB | 17.9 MB |
| Ridge | — | 1.6 MB | 1.5 MB |

Ch7 §7.6 adds a third framing: *"the fitting path peaks between 1.6 and 31.9
megabytes"* — i.e. it follows Ch6's pair, not Ch9's.

The artefact on disk agrees with **Ch9** (34.5 / 17.9). Ch6's Table 20 is dated
2026-09-11 and carries the Ridge figure 1.6 against the artefact's 1.5, so it
appears to be a separate, slightly earlier measurement run that was never
reconciled.

**Neither figure changes any conclusion** — the argument is a hundredfold margin
against a 4096 MB ceiling, and 34.5 vs 31.9 is 0.84% vs 0.78% of budget. But if
an examiner puts the two tables side by side, the answer must be ready and must
not be improvised. **Drill it (Phase 4), do not put it on a slide.**

The honest answer: two profiling runs at different dates, the later one
regenerated after the 18-feature retraining; the results artefact carries the
current figures; the discrepancy is within run-to-run variation of a memory
measurement and is immaterial against a ceiling three orders of magnitude above
it. Do **not** claim the difference is meaningful, and do not claim it was noticed
before submission.

## F10 — Zotero export integrity confirmed after the crash

`bibtex.bib` (157,324 B) and `citations.json` (167,113 B) both written 17:44.
**88 entries; exactly 1 has no `year`** — which is precisely what crashed the
sample-print loop. Exports are complete and current. The defect is one line
(`item["year"]` → `item.get("year")`) and is not this plan's work.

⚠ Carried forward from `deferred-structural-decisions.md` S16 and still open at
submission: the BibTeX exporter writes `author = {Hyndman Rob J., Athanasopoulos
George}` where BibTeX needs ` and ` as separator. **Harmless if Word's own
citation manager built the reference list; a Trust-tier defect if the `.bib`
did.** If an examiner asks how the bibliography was produced, know the answer.

## F7 — Reusable assets found (do not rebuild)

| Asset | Path |
|---|---|
| ~25 examiner Q&A with evidence | `06_thesis_writing/writing-notes/anticipated-assessor-questions.md` |
| 22 line-numbered forecasting defects + textbook citations | `plans/P0055_*/findings.md` |
| Scenario ladder figure | `05_thesis_results/07_decision_synthesis/figures/ch7_scenarios_v2.svg` |
| Layered architecture | `05_thesis_results/06_architecture/figures/ch6_layered_architecture_v2.svg` |
| Tool interface | `05_thesis_results/06_architecture/figures/ch6_tool_interface_v1.svg` |
| RQ tree | `05_thesis_results/01_introduction/figures/ch1_research_questions_tree_v2.svg` |
| Scenario comparison as styled SVG | `05_thesis_results/08_experimental_evaluation/tables/22_scenario_comparison.svg` |
| 87 SVGs total | `05_thesis_results/**/figures|tables/*.svg` |

**The deck reuses these.** Making new charts would both waste effort and risk
numbers that disagree with the submitted document.

## F8 — The one live Word comment

Thread **279**, Ch8 §8.3, tagged `APPENDIX`, opened by Brian 2026-09-15 10:33 on
*"The seven scenarios on sixty-three runs"*: "APPENDIX PASS: Re-genearte &
Replace". Unresolved at submission. Cosmetic/appendix-regeneration intent, not a
factual defect — but confirm with Brian whether Table 24 in the submitted
document is the regenerated one.
