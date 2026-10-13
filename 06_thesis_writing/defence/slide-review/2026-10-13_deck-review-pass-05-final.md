---
name: 2026-10-13_deck-review-pass-05-final
description: REFERENCE - Final claims check of every slide against the thesis snapshot and the repository, after the pass-04 edit round. Short; only what is still wrong or worth rehearsing.
category: reference
applies-to: [oral defence, slide deck]
triggers: [final check, claims verification, deck review]
created: 2026_10_13-22_30
updated: 2026_10_13-22_30
snapshot_deck: 2026-10-13_22-09_final_check
snapshot_thesis: 2026-10-10_16-42_deck-finalisation
supersedes: pass-04 (items you skipped count as decided and are not re-raised)
---

# Final claims check

**What was checked.** Every on-screen claim on slides 1–31 and the appendix figure
sources, against the thesis snapshot `2026-10-10_16-42_deck-finalisation`, the results
table `22_scenario_comparison.md` and the Zotero export. Deck snapshot:
`2026-10-13_22-09_final_check` (40 slides, 1 comment left, USER). Repo at `bb387c4`,
fetch clean.

**Result.** The deck is accurate. Every number on slides 20–29 matches its source.
Three wording errors remain, plus one fact on slide 4 that its source does not support.
Your skipped pass-04 items stand as decisions and are not re-raised. The two that
still matter if an examiner asks are covered in the speaker notes' Practice blocks.

---

## Your two questions from pass 04

**3.5 (slide 39 appendix figure): was that in pass 04, and did you change it?** Yes, it was
pass 04 §39.1, and no, the slide is unchanged. In plain terms: the chart on slide 39
isn't one of the thesis figures. It shows the models *before tuning*, and its title
(drawn inside the image) says *"every model beats SeasonalNaive"*. Slide 25 says the
opposite about the tuned models: 2 categories lose to benchmarks. Both are true (one
is before tuning, the other after), but an examiner flicking through the appendix only
sees the contradiction. It's an appendix slide, so it's low risk. Under your rule it
counts as ignored; if you want it gone, swap in thesis Figure 8 or delete the slide.

**3.6 (slide 25 benchmarks): did you apply it?** Half of it. The names are in, but two words are off:

| | |
|---|---|
| **Currently** | `parameter-free benchmarks: seasonal naive on RTD, Prophet on Danske` |
| **Edit** | REPLACE |
| **Should be** | `simple benchmarks: seasonal naive on RTD, Prophet on water` |

"Danske" isn't a category. The category is *danskvand* (water). And Prophet has
parameters, so "parameter-free" is wrong for it.

---

## Still wrong on screen

### F1 Slide 4: Olszak & Bartuś say cost is a barrier, not a driver

| | |
|---|---|
| **Currently** | `Cost is a key drive of AI adoption (Olszak & Bartuś, 2025)` |
| **Edit** | REWORD |
| **Should be** | `Cost is a key barrier to AI adoption (Olszak & Bartuś, 2025)` |

Their abstract: *"major barriers to this synergy include high implementation costs,
data quality issues, and a shortage of highly qualified specialists."* "Barrier" is what
the source says, and it fixes the typo ("drive") at the same time.

### F2 Slide 28: one leftover typo and a stray colon

| | |
|---|---|
| **Currently** | `7 scenarios x 3 brands x 3 repeats: = 63 runs` · `cannot be seperated` |
| **Edit** | REPLACE both |
| **Should be** | `7 scenarios × 3 brands × 3 repeats = 63 runs` · `cannot be separated` |

---

## Worth rehearsing (not slide edits)

| # | Slide | What an examiner could catch | Answer (also in that slide's Practice Notes) |
|---|---|---|---|
| R1 | 8 / 14 | **The thesis contradicts itself.** Ch2 says *"narrative, integrative review rather than a systematic review"*; Ch3 §3.2 says *"The rigor cycle is enacted through the systematic literature review in Chapter 2"*. | "Chapter 2's own description is the accurate one: a structured, iterative search, but not a systematic-review protocol. 'Systematic' in Chapter 3 is loose wording." Don't deny it. |
| R2 | 20–23 | The "Runs in" row reads as if D, E and G used a different LLM. | "All seven use the same model, GPT-5.5. What differs is the orchestrator: ours, or Manifold's production platform." (Ch3; Ch9 §9.2.3, *"with the same base model, in two independently built orchestrators"*) |
| R3 | 26 | "~50× cost difference at comparable accuracy": B's median is 2.9%, C's is 14.6%. Is that comparable? | "On the median B wins, on the mean C wins (13.1 vs 27.9). Neither dominates on accuracy, and that's the sense of 'comparable'." (Ch10 §10.2 wording) |
| R4 | 14 | "Judged against stated objectives, not novelty": the "not novelty" half isn't in the thesis. | Ch3: DSR *"judges that knowledge by whether the artefact achieves its design objectives"*. Stand on that sentence. |
| R5 | 5 | Royal Unibrew is named. The thesis never names a client. | It's public on Manifold's client-cases page, which the slide cites. Just make sure Manifold is fine with it. |
| R6 | 30 | The reference list has only the slide 4–5 URLs, not the academic sources cited on slides 8, 14 and 29 (Saunders 2023, Hevner 2004/2007, Peffers 2007, Hyndman & Athanasopoulos 2021, Goodwin et al. 2010). | Optional: add them. All six are in the thesis reference list. |

---

## Checked and correct

Every row below matches the thesis or the repo:

- **Slide 8:** 42 / 28 / 14 sources; ~100 screened, ~40 read; the Saunders attribution
- **Slide 9:** all five rows (Ch2 §2.1–2.7) and the summary line (Ch2 Fig. 2 caption)
- **Slide 10:** the RQ, verbatim
- **Slide 11:** all four bullets (Ch2 §2.7)
- **Slide 12:** SRQ1–4 (Ch1 §1.3)
- **Slide 14:**
  - pragmatism and modest realism (Ch3 §3.1)
  - single-case embedded study (Ch3 §3.3)
  - secondary data as an advantage (Ch3; Saunders)
  - expanding-window CV that never sees the test split (Ch3, Ch5 §5.4.4)
  - wMAPE primary, with median APE and MASE (Ch3)
  - exponential smoothing omitted as a limitation (Ch3, Ch5)
  - three cycles: Manifold, Ch5–8, Ch2 (Ch3, Hevner 2007)
  - the six activities (Ch3, Peffers 2007)
- **Slides 20–23:** all 56 numbers against `22_scenario_comparison.md`; gpt-5.5 confirmed in the harness
- **Slide 25:**
  - boosters beat Ridge and ARIMA in all 4 categories; the seed flips the winner in all 4 (Ch5, abstract)
  - 35 MB (34.5 in Ch5)
  - pooling wins on the 2 smallest categories (Ch5, Ch10 §10.1)
  - every figure matched the payload (Ch9)
  - 8–34× (Ch7, Ch9)
  - 3 of 7 ran in production; readiness derived from what integration required (Ch10 §10.1)
  - credentials and merge (Ch9)
  - 502% → 2.9%; combined runs invented their own weight (Ch9)
- **Slide 26:** all five principles (Ch9 §9.2.2, Ch10 §10.2); 231 MB (Ch6, Ch10 §10.3); ~50× (Ch8, Ch9, Ch10 §10.2)
- **Slide 28:** all five rows (Ch3 §3.3, Ch9 §9.4)
- **Slide 29:** all five rows (Ch9 §9.5, Ch10 §10.5, Goodwin et al. 2010)
- **Appendix 38 and 40:** thesis Figs 7 and 6
