---
name: 2026-09-13_18-40_BRANCH_A_cross-chapter-flow-and-connectedness
description: NOTE - Connectedness and reading flow across Chapters 1-8 read end to end against BRANCH A. Nine cross-chapter contradictions, the forward-reference map, where the argument breaks for a linear reader, and what is load-bearing versus cosmetic. Cumulative, not per-chapter.
category: reference
applies-to: [ch1_introduction, ch2_literature_review, ch3_methodology, ch4_data_assessment, ch5_model_benchmark, ch6_architecture, ch7_synthesis, ch8_experiment]
triggers: [does the thesis hang together, reading flow, cross-chapter consistency, chapter transitions, is branch a submission ready]
created: 2026_09_13-18_40
updated: 2026_09_14-09_45
snapshot: 2026-09-13_18-18_branch-a-full-review
status: findings, not prose - fixes routed per chapter. C2 STRUCK 2026-09-14, see the item.
---

# Cross-chapter flow, Chapters 1 to 8

Read end to end against snapshot `2026-09-13_18-18_branch-a-full-review`
(43,584 words), repository at `c9c0587`, Zotero re-pulled: 89 items.

**This note carries no per-chapter prose.** Where a fix belongs to one chapter
it is named and routed. What is here is only what a reader moving front to back
would notice and no single-chapter pass would catch.

---

# The verdict first

**Chapters 2 and 4 through 8 read as one document.** The argument is continuous,
the vocabulary is stable, the forward references resolve, and each chapter ends
by naming what the next one does. That is a genuinely good state and it is worth
saying plainly, because the defects below are concentrated rather than spread.

**Chapters 1 and 3 are the weak seam.** Both were written against the earlier
design and neither has been brought forward. Chapter 1 promises a thesis the
later chapters no longer deliver; Chapter 3 specifies methods the experiment did
not use. A reader who trusts the introduction meets a different study in
Chapter 5 and a third one in Chapter 8.

**The abstract is a bullet skeleton**, still carrying `[TBD - fill after
empirical results]`. It is the first page an examiner reads.

---

# Nine cross-chapter contradictions

Ordered by how much damage each does to a reader's trust, not by chapter.

## C1 — The RAM budget is 8 GB in three chapters and 4 GB in four

| Says 8 GB | Says 4 GB |
|---|---|
| Ch1 §1.1, §1.4 ("maximum of 8 gigabytes") | Ch2 §2.2 ("on the order of four gigabytes") |
| Ch9 §9.1.1, DP1, §9.2.3 | Ch3 §3.6, §3.7 ("four-gigabyte RAM budget") |
| Ch10 §10.1, §10.3 | Ch5 §5.1, §5.5.6 ("four-gigabyte sequential budget") |
| | Ch6 §6.1, §6.8 ("approximately four gigabytes") |

**This is the single most visible defect in the thesis.** The constraint is the
thesis's own headline design criterion, stated in the title of its research
question, and the document cannot agree on it. Chapter 3 even says "four" in one
sentence and the delimitation in Chapter 1 says "eight" about the same budget.

**Recommendation: four gigabytes throughout.** It is what Ch5, Ch6 and Ch7
measure against, what the architecture chapter argues from, and the stricter
claim. The Ch9 and Ch10 rewrites already say four.

→ **Routed:** Ch1 §1.1 and §1.4 need the edit. Ch9/Ch10 handled in their notes.
**NEEDS-BRIAN** for Ch1, since it also appears in the delimitation's reasoning.

---

## C2 — STRUCK. The claim was wrong.

~~Chapter 1 promises exogenous enrichment the thesis does not deliver.~~

**Corrected 2026-09-14, by Brian.** This item asserted that Ch1's closing
sentence — *"This thesis takes up that direction by incorporating exogenous
predictors into its forecasting substrate"* — promises something the thesis does
not deliver.

**That is false, and the substrate is the evidence.** Four of the eighteen model
features are exogenous in the standard sense, meaning they are known in advance
and are not functions of the target's own history:

| Feature | Source |
|---|---|
| `n_holidays` | Danish public-holiday calendar, Nager.Date |
| `days_in_month` | same |
| `non_holiday_days` | same |
| `promo_intensity` | Nielsen promotional variants, where reported |

The holiday calendar was joined onto the monthly grid, cached with a per-year
checksum, and **its contribution was measured rather than assumed**: an ablation
tuned both arms independently and found the calendar columns improved accuracy in
six of the nine category-and-model combinations tested (Ch4 §4.3).

**So Ch1's sentence is accurate as written.** The thesis took up the M4/M5
direction, incorporated the exogenous predictors the panel makes available, and
measured what they were worth.

⚠ **The Word comment threads on that paragraph are older than the holiday API.**
They predate the enrichment landing and should be resolved as **VERIFIED-OK**
rather than acted on — the objection they raise was true when written and is not
true now.

**One residual item, and it is a different point:** the same Ch1 paragraph
carries `[CITATION TO ADD: cloud-instance pricing source]` and states the RAM
ceiling as **eight** gigabytes. Both are real and both are recorded elsewhere —
the placeholder as S31, the budget as C1 and S32. **They sit in the same two
paragraphs**, so whoever edits Ch1 §1.1 should fix both in one pass rather than
opening the section twice.

→ **No Ch1 edit is required by this item.** C1 and S31 still require one.

---

## C3 — Chapter 3 specifies an LLM-as-judge protocol that does not exist

Ch3 names it four times: §3.5 (*"Scoring uses an LLM-as-judge protocol with a
separate judge model, explicit bias awareness, and a human-rated subset"*),
§3.6 twice, §3.7 by implication.

Ch7 §7.3 states the opposite, and states it as a design decision: *"No language
model judges anything... a model acting as judge would introduce
non-determinism, and with it a requirement for its own bias controls."*

**Chapter 7 is right and Chapter 3 describes a superseded design.** Your
Ch2 comment already flags it: *"As far as I know we removed the judge model
entirely."* Four `OUTDATED` threads in Ch3 say the same.

→ **Routed: Ch3 §3.5, §3.6.** Also **Ch2 §2.5**, whose final paragraph still
says the evaluation uses *"a separate judge model with bias awareness and a
human-rated subset"* — the literature review is promising the same method.

---

## C4 — "Approximately fifty prompts" against 63 runs of one prompt

Ch3 §3.5 and §3.7 both say the comparison runs on *"a common set of
approximately fifty decision-support prompts"*. Ch10 repeats it.

The design is the opposite: **one question, asked identically**, across seven
scenarios, three brands and three repeats. Consistency is measured by repetition
of an identical prompt rather than by breadth of coverage — which Ch1 §1.3
states correctly and Ch3 contradicts two chapters later.

This matters more than a number. A fifty-prompt design measures coverage; a
three-repeat design measures run-to-run variance. **They answer different
questions, and the variance result is the thesis's strongest SRQ4 finding.**

→ **Routed: Ch3 §3.5, §3.7.** Ch10 handled in its note.

---

## C5 — The chapter map in Chapter 1 §1.5 is off by one from Chapter 5 onward

Ch1 §1.5 says: Chapter 5 is the architecture, Chapter 6 the benchmark, Chapter 7
the agentic prototype, Chapter 8 the pilot evaluation, and it opens by promising
*"nine chapters"*.

The document has ten numbered chapters and the order swapped on 2026-09-08:
Ch5 is the benchmark, Ch6 the architecture.

The same stale numbering propagates **inside** other chapters:

| Location | Says | Should say |
|---|---|---|
| Ch1 §1.3, SRQ1 | "benchmark in Chapter 6" | Chapter 5 |
| Ch1 §1.3, SRQ2 | "interface (Chapter 5)" | Chapter 6 |
| Ch1 §1.3, SRQ3 | "specification (Chapter 5...)" | Chapter 6 |
| Ch2 §2.1 | "Chapter 6 encounters... the same problem" | Chapter 5 |
| Ch2 §2.5 | "Chapter 6 accordingly measures coverage" | Chapter 5 |
| Ch3 §3.5 | "RSS measurements are reported in Chapter 6" | Chapter 5 |
| Ch5 §5.7 | "integration readiness is argued in Chapter 7" | Chapter 6 |
| Ch6 §6.2 | "SRQ3, Section 5.6" | Section 6.6 |

**Ch4 is the counter-example and shows the fix.** It uses a broken-link
placeholder (`0`) where a cross-reference should be — ugly, but it means Word
owns the number. Ch6 and Ch7 mostly use prose references that are correct.

→ **Routed: Ch1, Ch2, Ch3, Ch5 §5.7, Ch6 §6.2.** Eight sites. Mechanical, and
worth doing in one pass since a wrong chapter number sends a reader to the wrong
chapter and is the error an examiner is most likely to trip over.

---

## C6 — Five categories or four

Ch3 §3.3, §3.4 and §3.6 all say **five** ("the five Nielsen categories", "five
Danish beverage categories"). Ch1 §1.4 and Ch4 say **four**, with beer
explicitly excluded and the reason given. Ch2 §2.7 says "multiple". Ch10 says
five.

Ch1's delimitation carries a further internal slip: it excludes beer, then two
paragraphs later says *"the five-category benchmark provides evidence"*.

→ **Routed: Ch3** (three sites), **Ch1 §1.4** (one site). Ch10 in its note.

---

## C7 — Chapter 2 tells the reader what the thesis has not yet done

Ch2 §2.7 lists the four contributions with status labels: *"designed; benchmark
to be built"*, *"designed; assessment planned"*, *"designed; evaluation
pending"*.

All four have landed. As written, the literature review tells an examiner the
thesis is incomplete — and your own comment says exactly this: *"I suppose the
'designed; …' parts are the current status? We must remo[ve]"*.

**This is the highest-value small fix in the document.** Four label deletions,
and the gap statement reads as a thesis rather than a proposal.

→ **Routed: Ch2 §2.7.**

---

## C8 — Chapter 5's Danskvand coverage figure exists in no artefact

Ch5 §5.5.7 prose: *"83.9 per cent against a nominal ninety, and **72.4** against
a nominal eighty"*.

Its own Table 13, ten lines above, prints **73.6**. `calibration.csv` records
73.6. The figure 72.4 appears nowhere in any results file.

→ **Routed: Ch5 §5.5.7.** One-word fix, and the anchor is quoted in full below
so it can be pasted directly.

### The Ch5 anchor, verbatim

> "danskvand fails on the other axis. It misses the coverage target at both
> levels - 83.9 per cent against a nominal ninety, and 72.4 against a nominal
> eighty - on the smallest calibration set in the study, at 174 rows."

**Action:** REWORD — replace `72.4` with `73.6`. Nothing else in the sentence
changes.

---

## C9 — Chapter 3 describes the sandbox as local

Ch3 §3.5: the baseline *"executes LLM-generated code in a sandboxed environment
(for example E2B), which is runnable locally and does not require access to the
production system."*

Ch6 §6.7 is correct: the sandbox is a hosted service created per request, which
is precisely why it costs nothing when idle — an argument Ch6 and Ch8 both use.
Your comment says it: *"E2B is not run locally either way."*

The second half of Ch3's sentence is right and worth keeping: the comparison
needs no production access. Only "runnable locally" is wrong.

→ **Routed: Ch3 §3.5.**

---

# Reading flow: where a linear reader stumbles

## The transitions that work

- **Ch4 → Ch5.** Ch4 ends on the split table and the risks; Ch5 opens on model
  selection against that data. Clean.
- **Ch5 → Ch6.** Ch5 §5.6 ends with "the served model carries its own track
  record", which is exactly what Ch6's interface section picks up.
- **Ch6 → Ch7.** Ch6 §6.4 specifies the interface and Ch7 §7.1 opens by saying
  what Ch6 did not establish. The handoff is explicit and well made.
- **Ch7 → Ch8.** Ch7 §7.7 says what Ch8 will report; Ch8 §8.1 delivers it.
- **Ch2's internal ordering.** Eight sections, each closing by naming what the
  next supplies. This is the best-structured chapter in the thesis.

## The transitions that do not

**Ch1 → Ch2.** Ch1 §1.5 promises Chapter 2 will review "eight thematic
sections" and lists them. Ch2 delivers nine (§2.1–2.9). Minor, but it is the
first promise the document makes and breaks.

**Ch3 → Ch4.** Ch3 §3.4 describes the data in 200 words; Ch4 then spends 5,292
words on the same subject. The reader cannot tell why they read the short
version first. **Recommendation:** cut Ch3 §3.4 to two sentences and a forward
reference. It currently duplicates Ch4 §4.1.1 almost claim for claim, including
the Saunders secondary-data argument, which appears in both.

**Ch7 → Ch8 on the confidence index.** Ch7 §7.4 establishes at length that the
index discriminates nothing. Ch8 never mentions it. That is defensible, but
Ch8's interval-communication criteria are scored partly on confidence being
stated, so a reader may wonder whether the degenerate index is what is being
scored. **One clause in Ch8 would close it:** the criterion records whether a
confidence was communicated, not whether the index that produced it was
informative.

## The one structural oddity

**Ch8 has two "threats to validity" tables**, numbered 21 twice. Section 8.4
ends with an old five-row table captioned *"Table 21 - Threats to Validity"*,
containing LLM-as-judge and "access to Manifold descriptive baseline" rows; then
§8.5 opens with the correct four-row table, also captioned Table 22 in italics.

The old table is a leftover and its rows are false: it names a judge protocol
and a descriptive baseline comparison that do not exist.

→ **Routed: Ch8 §8.4 — delete the old table and its caption.** This was flagged
in the Ch8 Branch A pass as F6/F7 and is still present, so it did not get
applied. Worth re-flagging to Enrico directly.

---

# What is load-bearing versus cosmetic

For triage under time pressure.

| Fix | Cost | If left |
|---|---|---|
| **Abstract is a bullet skeleton with TBDs** | 1 hour | First page an examiner reads says "fill after empirical results" |
| **C1, the 8 GB / 4 GB split** | 15 min | The headline design criterion is self-contradictory |
| **C3, the judge protocol in Ch2/Ch3** | 30 min | Methodology specifies a method the thesis argues against |
| **Ch8's duplicate Table 21** | 5 min | Two tables, same number, one false |
| **C7, Ch2's "to be built" labels** | 5 min | Literature review says the thesis is unfinished |
| **C5, chapter numbers** | 20 min | Reader sent to the wrong chapter, eight times |
| **C4, "fifty prompts"** | 10 min | Methodology describes a different experiment |
| **C6, five vs four categories** | 10 min | Simple factual inconsistency |
| **C2, the enrichment promise** | 15 min | Introduction promises what the thesis does not deliver |
| **C8, Ch5's 72.4** | 1 min | A number in no artefact, contradicting the table above it |
| **C9, "runnable locally"** | 2 min | Small, and contradicts Ch6's cost argument |
| Ch3 §3.4 duplicating Ch4 | 15 min | Redundancy in a page-limited document |
| Ch1's "nine chapters" / "eight sections" | 2 min | Cosmetic |

**Total for everything above the line: roughly three hours**, and the thesis
stops contradicting itself.

---

# What is genuinely strong, and should not be touched

Worth recording so a revision pass does not flatten it.

- **The negative results are the thesis's best feature.** The withdrawn accuracy
  target (Ch5 §5.4.3), the seed instability that dissolves the model-selection
  claim (§5.5.10), the degenerate confidence index (Ch7 §7.4), and the interval
  too wide to act on. Each is reported with what was tried. Very few master's
  theses do this, and an examiner will notice.
- **Ch5 §5.4.1's scoring-function argument.** Deriving the WMAPE choice from
  Gneiting's consistency result, then using it to *predict* the metric
  divergence the chapter goes on to measure, is the most sophisticated passage
  in the document.
- **Ch7's refusal principle** (§7.2.3), generalised from three error conditions
  into a design claim about interfaces whose consumer is a generative model.
  That is transferable design knowledge, which is what DSR asks for.
- **Ch8's decision to classify outcomes before averaging**, and to report the
  within-scenario spread beside every mean. It is what makes the chapter's
  refusal to declare a winner credible rather than evasive.
- **Ch4's treatment of the market hierarchy** (the 6.16× double-count) and of
  the thirteen lumpy brands with no test signal. Both are places where the
  honest answer is less flattering and it is given anyway.

---

# Cross-references that resolve correctly

Checked rather than assumed, since this is where a reader loses confidence
fastest. All of the following are **correct as written** and should not be
"fixed":

- Ch6 §6.3 → Chapter 5 for the benchmark ✓
- Ch6 §6.4 → Chapter 5 for conformal validation, Chapter 8 for width ✓
- Ch7 §7.4 → Chapter 5 Table 13 ✓
- Ch7 §7.7 → Chapter 8 for the comparison ✓
- Ch8 §8.2.1 → Chapter 5 for substrate accuracy ✓
- Ch8 §8.4 → Chapter 5 and Chapter 6's budget ✓
- Ch5 §5.4.4 → Syntetos et al. (2005), in Zotero ✓
- Ch2 §2.3 → Goodwin et al. (2010), in Zotero, and used consistently in Ch6, Ch7
  and Ch8 ✓

**The Goodwin thread is the best example of connectedness in the thesis.** It is
introduced in Ch2 §2.3 with the experimental result, invoked in Ch6 §6.4 as the
reason the interface carries an interval, developed in Ch7 §7.1 into the
argument that an interval alone is insufficient, operationalised in Ch7 §7.3 as
the fourth scoring criterion, and bounded in Ch8 §8.5 as the limit of what the
evaluation can claim. One source, five chapters, one continuous argument.

---

# Open items for the deferred structural list

`deferred-structural-decisions.md` uses `## S<N> - <title>` headings with a
`**Status:**` and `**Found:**` block, not table rows. **S1–S23 and S26–S28 are
in use, so the next free number is S29.** The four below are written in that
file's format and can be appended directly.

⚠ **The table-numbering collision is already S26** and must not be re-raised.
This note's C-items add to it rather than duplicating it: Chapter 9's "Table 23"
collides with Chapter 8's, so S26's scope now extends past Chapter 7.

---

## S29 - The abstract is still a bullet skeleton

**Status:** `open` - blocks submission
**Found:** 2026-09-13, cross-chapter flow pass

The abstract carries `### Key findings (TBD - fill after empirical results)` and
four bracketed placeholders, one per SRQ. It also names "Indeks Danmark consumer
survey", a second data source the thesis does not use, and a "3-level evaluation
framework" that Chapter 8 replaced with the ladder.

**Recommendation:** write it last, from Chapter 10's replacement SRQ answers,
which are now the only current statement of all four.

---

## S30 - Chapter 3 §3.4 duplicates Chapter 4 §4.1.1

**Status:** `recommended` - cut Ch3's to a forward reference
**Found:** 2026-09-13, cross-chapter flow pass

Both sections describe the same star schema, the same period counts and the same
Saunders secondary-data argument, 2,000 words apart. Chapter 4 is the fuller and
better version.

**Recommendation:** reduce Ch3 §3.4 to two sentences naming the source and the
grain, then cross-reference Chapter 4. Saves roughly 150 words in a page-limited
document and removes a place where the two can drift.

---

## S31 - Two citation placeholders remain in the running text

**Status:** `open`
**Found:** 2026-09-13, cross-chapter flow pass

| Location | Placeholder |
|---|---|
| Ch1 §1.1 | `[CITATION TO ADD: cloud-instance pricing source]` |
| Ch10 §10.3 | `[cloud-pricing citation: resolve in global references pass]` |

Both support the same claim, that GPU instances cost one to seven dollars per
hour against a fraction of that for a general-purpose instance.

**Recommendation:** the Ch10 one is deleted by that chapter's rewrite, which
makes no pricing claim. For Ch1, either add a source to Zotero or reword to the
qualitative claim Chapter 2 already makes without a citation, which is that the
difference is an order of magnitude.

---

## S32 - The 8 GB / 4 GB split across seven chapters

**Status:** `open` - **NEEDS-BRIAN**, one decision then a find-and-replace
**Found:** 2026-09-13, cross-chapter flow pass

Ch1, Ch9 and Ch10 say eight gigabytes; Ch2, Ch3, Ch5 and Ch6 say four. See C1 in
the parent note for the site list.

**Recommendation: four throughout.** It is what every measurement in the thesis
is reported against, and the stricter claim. The Ch9 and Ch10 rewrites already
use four, so only Chapter 1 remains after those are applied.
