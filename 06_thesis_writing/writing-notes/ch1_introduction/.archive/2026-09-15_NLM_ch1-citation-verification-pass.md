---
name: 2026-09-15_NLM_ch1-citation-verification-pass
description: PASS - NotebookLM's seventeen Chapter 1 citation checks, each re-verified against the snapshot and a fresh Zotero pull. Four real defects with paste-ready fixes, one of them a source cited for a claim it cannot support. Three proposed sources are not in the library and are not usable.
category: workflow
applies-to: [ch1_introduction]
triggers: [ch1 citations, notebooklm, citation verification, ch1 prose pass]
created: 2026_09_15-12_10
updated: 2026_09_15-12_10
snapshot: 2026-09-15_10-49_final-comment-sweep
status: prose ready to paste, awaiting human review
---

# Chapter 1 — NotebookLM citation pass, verified

Verified at `37a04f0`, fetch clean (5 ahead of `origin/main`, 0 behind).
Snapshot `2026-09-15_10-49_final-comment-sweep` — captured 10:49:25 against a
`.docx` last modified 10:44:24, so Word had not moved. Zotero exports re-pulled
**2026-09-15 10:49:34, 92 items**.

**Notes swept:** `ch1_introduction/` holds one live note,
`2026-09-14_appendix-citations-ch1.md` (reference material, no anchors, nothing
to apply). `.archive/2026-09-14_ch1-rewrite-applied.md` is already archived. **No
other session's work is dropped by this note.**

⚠ **I did not take NotebookLM's verdicts on report.** Every one of the seventeen
was re-checked against the snapshot and the library. **Four of its seventeen
changed verdict under checking** — three because it proposes sources we do not
have, one because it declared a real defect but mis-diagnosed the cause.

---

# Read this first — what actually changed

| | NotebookLM said | After checking |
|---|---|---|
| **17 items** | 6 need an edit | **4 need an edit** |
| **CIT-001** | REPLACE, add Power (2002) + Watson (2014) | ⚠ **neither is in Zotero.** Fix without them — F1 |
| **CIT-007** | REPLACE, add Shuvo et al. (2022) | ⚠ **not in Zotero — but the defect is real and worse than described.** F2 |
| **CIT-013** | REPLACE, add Ng (2017) | ✅ **apply** — F3 |
| **CIT-017** | REPLACE, keep "nine chapters" | ⚠ **its replacement text re-introduces a known error.** F4 |
| **CIT-004** | METADATA ONLY, cite 2018 **and** 2020 | ✅ **apply** — F5, both papers are already in the library |
| **CIT-006** | REPLACE, strip footnote artifact | ✅ **apply** — F6, trivial |
| **CIT-010** | FALSE / NEEDS ADAPTATION | ❌ **not a verdict.** It never read the source — see the note below |
| **CIT-012** | REPLACE | ❌ **reject.** Its replacement asserts something the paper does not measure |
| CIT-002, 003, 005, 008, 009, 011, 014, 015, 016 | KEEP | ✅ **confirmed, no action** |

---

# The library check, because three fixes depend on it

**`citations.json` is filtered by item type**, and the standing trap in
`/re-snap` is to never conclude a source is missing from that file alone. So I
checked the type distribution first and cross-read `bibtex.bib`:

```
journalArticle 49 | preprint 21 | conferencePaper 12
webpage 4 | book 3 | bookSection 2 | computerProgram 1   = 92
```

All seven types are present, so nothing is being hidden by the filter.

| Proposed by NotebookLM | In library? |
|---|---|
| Power (2002) | ❌ **no hits**, any type |
| Watson (2014) | ❌ **no hits** |
| Shuvo et al. (2022) | ❌ **no hits** |
| Sprague (1980) | ❌ **no hits** (quoted in its evidence column, not proposed) |

⚠ **This is the rule that exists because a plausible-looking reference was once
written from memory and read as verified.** Power and Watson are real, well-known
BI sources and it would be easy to add them from memory. **Do not.** If you want
them, add them to Zotero from the actual publications first, and then F1 becomes
a different and simpler edit.

---

# F1 — §1.1, the BI sentence attributes a multi-decade claim to a 2025 paper

**NotebookLM is right about the defect and wrong about the remedy**, because its
remedy needs two sources we do not have.

### Anchor

**Chapter 1, Section 1.1 Background and Motivation** — the **second sentence of
the opening paragraph**. The paragraph begins *"The accelerating adoption of
artificial intelligence..."*.

Searchable, verbatim:

> "For decades, business intelligence (BI) systems have served a primarily descriptive function: they aggregate historical data into dashboards, key performance indicator reports, and trend summaries that tell managers what has happened (Rinaldi et al., 2025)."

**The sentence after it begins:**
> "While such systems have generated substantial operational value, the growing complexity of modern markets demands something more..."

### Action

REWORD — that one sentence. The rest of the paragraph stands.

#### Replace with

> "For decades, business intelligence systems have served a primarily descriptive function: they aggregate historical data into dashboards, key performance indicator reports, and trend summaries that tell managers what has happened. Recent decision-support frameworks build on that descriptive base rather than replacing it; DSS4EX, for example, wraps a time-series forecasting pipeline in an explainability layer (Rinaldi et al., 2025)."

### Note — why this shape rather than NotebookLM's

✅ **The "for decades" claim no longer carries a citation at all**, because it is
uncontroversial background that no source in our library supports as stated.
Leaving it uncited is more honest than attributing it to a 2025 paper about one
forecasting DSS.

✅ **Rinaldi moves to the claim it genuinely supports.** The library entry is
`rinaldi_dss4ex:_2025`, *"DSS4EX: A Decision Support System framework to explore
Artificial Intelligence pipelines with an application in time series
forecasting"* — which is exactly what the second half of the replacement says.

⚠ **The abbreviation "(BI)" is defined here and used later in the chapter.** I
removed it from this sentence, so **check whether "BI" appears again in Ch1
before pasting** — if it does, keep the parenthetical: *"business intelligence
(BI) systems"*. In this snapshot it does not recur in Ch1, but Ch2 §2.3 uses the
full phrase.

---

# F2 — §1.1, one Zotero item cited for two incompatible claims ⚠ THE SERIOUS ONE

**NotebookLM flagged this as a wrong-topic citation. It is worse than that, and
the fix is better than the one it proposes.**

### What I found

Chapter 1 cites `(Liu et al., 2024)` for edge and resource-constrained AI.
Chapter 2 §2.4 cites `Liu et al. (2024, "DyLAN")` for multi-agent orchestration.
**These resolve to the same library item:**

```
liu_a_2024 | preprint | "A Dynamic LLM-Powered Agent Network for
                         Task-Oriented Agent Collaboration"  (arXiv:2310.02170)
```

✅ **Ch2's use is correct** — that is what DyLAN is.
⚠ **Ch1's use is not.** A multi-agent collaboration preprint cannot support a
claim about hardware memory budgets in the edge-AI literature.

**And the source the sentence actually wants is already in the chapter next
door.** Ch2 §2.2 line 39: *"Liu et al. (2025) evaluate quantisation and
distillation for edge deployments, showing that substantial accuracy can be
preserved at sharply reduced memory footprints."* **That** is the edge-AI Liu.

→ **So the fix is a one-digit year change, not a new source.** No Shuvo needed.

### Anchor

**Chapter 1, Section 1.1** — the paragraph beginning **"Yet the practical
deployment of predictive AI systems in business settings faces a constraint..."**.
Searchable, verbatim:

> "which is why resource-efficient deployment is treated as a first-order constraint in the edge and resource-constrained AI literature (Liu et al., 2024)."

**The sentence after it begins:**
> "Ng (2017), working with four terabytes of Nielsen weekly scanner data..."

### Action

REWORD — change `2024` to `2025`. **One character.**

#### Replace with

> "which is why resource-efficient deployment is treated as a first-order constraint in the edge and resource-constrained AI literature (Liu et al., 2025)."

### ⚠ NEEDS-BRIAN — one thing I could not verify

**`Liu et al. (2025)` does not appear in `reference-list.md`**, and I could not
find a distinct 2025 Liu edge-AI entry in the 92-item pull. Ch2 cites it, so one
of two things is true:

| | Then |
|---|---|
| **The item is in Zotero** and the reference list is simply not yet regenerated (thread 277) | ✅ paste F2 as written |
| **The item is not in Zotero** and Ch2 §2.2 is citing something we do not have | ⚠ **that is a second, larger defect in Ch2** — and F2 must wait on it |

→ **Check `Liu 2025` in the Zotero group library directly before pasting.** I can
only see the export. This is a two-minute check and it decides between a
one-character fix and a Ch2 finding.

⚠ **Do not "solve" this by leaving the 2024.** A citation that points at the
wrong paper is worse than one that is temporarily unresolvable, because the
reference list will resolve it silently to DyLAN.

---

# F3 — §1.3.1, splitting a claim across the two sources that support its halves

**NotebookLM is right, and both sources are in the library.**

### Anchor

**Chapter 1, Section 1.3.1 SRQ1 - Models and Efficiency** — the **second
sentence** of the paragraph beginning *"SRQ1 motivates the empirical model
benchmark in Chapter 5..."*.

Searchable, verbatim:

> "Accuracy alone is insufficient for production deployment: a model with marginally lower error but higher memory use or unstable output is a worse engineering choice under a fixed memory budget (Klee & Xia, 2025)."

**The sentence after it begins:**
> "The models, metrics, and protocol are defined in Chapter 3."

### Action

REWORD — that one sentence.

#### Replace with

> "Accuracy alone is insufficient for production deployment: a model with marginally lower error but unstable output (Klee & Xia, 2025) or a larger memory footprint (Ng, 2017) is a worse engineering choice under a fixed memory budget."

### Note

✅ **Both verified in the library.** `UXPL266D` — Klee & Xia, *"Measuring Time
Series Forecast Stability for Demand Planning"*, KDD 2025 workshop. Ng (2017) is
already cited twice elsewhere in §1.1 and §1.4.

✅ **The split is substantively right, not cosmetic.** Klee & Xia measure
*stability* — the coefficient of variation of forecasts under identical inputs
varying only the seed. They do not measure memory. Ng is the memory source, and
the chapter already uses it that way.

---

# F4 — §1.5, the chapter count ⚠ DO NOT PASTE NOTEBOOKLM'S VERSION

**NotebookLM's diagnosis is correct. Its replacement text would re-introduce an
error you are already fixing.**

Its proposed replacement reads *"organised into **nine** chapters that map onto
the six core activities..."* — but the thesis has **ten** chapters, and
`2026-09-15_BRANCH_A_CONSOLIDATED-remaining-fixes.md` **F3 already fixes
`nine` → `ten`** at this exact sentence.

⚠ **Pasting NotebookLM's text verbatim would undo F3.**

### Anchor

**Chapter 1, Section 1.5 Thesis Structure** — the **opening sentence**.
Searchable, verbatim:

> "The remainder of this thesis is organised into nine chapters, each corresponding to a phase of the Design Science Research process (Peffers et al., 2007)."

**The text after it begins:**
> "**Chapter 2** **| Literature Review** reviews the literature across nine thematic sections..."

### Action

REWORD — **one sentence, two changes at once.** This supersedes F3 in the
consolidated note; apply this version instead, not both.

#### Replace with

> "The remainder of this thesis is organised into ten chapters that map onto the six activities of the Design Science Research process (Peffers et al., 2007)."

### Note — two separate defects in one sentence

| | Defect | Source |
|---|---|---|
| **1** | `nine` should be `ten` | ✅ **verified: `MANIFEST.md` lists ten numbered chapters**, and the list beneath this sentence has ten entries |
| **2** | "each corresponding to a phase" implies a 1:1 chapter-to-phase mapping | ✅ Peffers specifies **six** activities, so ten chapters cannot each be one |

✅ **The per-chapter entries beneath this sentence are already correct** (Ch5
benchmark, Ch6 architecture, Ch7 interface). Only the lead-in is wrong.

---

# F5 — §1.1, the M4 competition has two papers and we own both

**NotebookLM calls this "metadata only". It is right, and unusually the library
already supports the fix cleanly.**

| Key | Year | Title |
|---|---|---|
| `EXNY7D4X` | **2018** | *The M4 Competition: Results, findings, conclusion and way forward* — IJF 34(4), 802–808 |
| `V58EFK8B` | **2020** | *The M4 Competition: 100,000 time series and 61 forecasting methods* — IJF 36(1), 54–74 |

✅ **Both are already correctly distinguished in `reference-list.md` lines 45 and
47.** These are not duplicates — they are two genuine papers, and this is not the
Elements-of-Statistical-Learning triplication problem from thread 277.

### Anchor

**Chapter 1, Section 1.1** — the paragraph beginning **"The broader forecasting
literature confirms this directional shift."** Searchable, verbatim:

> "The M4 Competition, the largest empirical benchmarking study in the history of the field covering 100,000 time series and 61 forecasting methods, established that combining multiple forecasting models consistently outperforms any single best model selection, and that hybrid methods blending statistical structure with machine learning achieve the highest accuracy  (Makridakis et al., 2020)."

⚠ **Note the double space before "(Makridakis"** — it is in the document and it
is what makes the string findable.

**The sentence after it begins:**
> "Its successor, the M5 Competition, focused specifically on hierarchical retail sales forecasting using real Walmart data..."

### Action

REWORD — the citation only.

#### Replace with

> "The M4 Competition, the largest empirical benchmarking study in the history of the field covering 100,000 time series and 61 forecasting methods, established that combining multiple forecasting models consistently outperforms any single best model selection, and that hybrid methods blending statistical structure with machine learning achieve the highest accuracy (Makridakis et al., 2018, 2020)."

### Note — leave Ch5 alone

✅ **Ch5 §5.1 already cites `Makridakis et al., 2018` correctly** for the M4
finding that no pure ML entry beat the statistical combination. That is the 2018
paper's result and needs no change.

⚠ **Ch2 §2.1 cites only 2020** for the same M4 claim. Consider the same edit
there for consistency — but it is outside this pass's scope and I have not
verified Ch2's sentence in context. Recorded below as a deferred item.

---

# F6 — §1.1, a footnote artifact inside a block quotation

**Trivial, and NotebookLM is right.** The quoted passage carries a stray `1`
where the source's footnote marker was scraped into the text: *"explanatory/exogenous
variables.1 This element..."*.

### Anchor

**Chapter 1, Section 1.1** — the long quotation in the paragraph beginning
*"The broader forecasting literature confirms this directional shift."* The
quotation is italicised in Word. Searchable, verbatim — the distinctive fragment:

> "expanding time series forecasting to include explanatory/exogenous variables.1 This element could be explored in future M Competitions"

### Action

REWORD — delete the `1` only. Nothing else in the quotation changes.

#### Replace with

> "expanding time series forecasting to include explanatory/exogenous variables. This element could be explored in future M Competitions"

### Note

⚠ **A direct quotation must be verbatim from the source**, and the source has no
`1` in that sentence — it has a footnote marker, which is not part of the quoted
text. Leaving it in misquotes the paper.

---

# Rejected — two items I am not applying, and why

## CIT-012 — §1.2, the Klee & Xia trade-off sentence

**NotebookLM proposes:** *"the forecasting substrate must be accurate **and
stable under promotional conditions** yet deployable within a tight computational
budget, a trade-off evaluated by Klee and Xia (2025)."*

❌ **Reject.** The inserted phrase *"under promotional conditions"* is not
something Klee & Xia measure. Their paper varies **the random seed** with data,
splits and hyperparameters held identical, and measures the coefficient of
variation of the resulting forecasts. Promotions do not enter it.

⚠ **This would replace a vague citation with a specific false one**, which is
strictly worse. NotebookLM's own evidence column quotes the paper on *"variance
in forecast outputs"* and *"changes in output which can be attributed only to
stochasticity"* — neither mentions promotions.

✅ **The existing sentence is acceptable as it stands.** If you want it tightened,
F3 already makes the accuracy-vs-stability-vs-memory split precisely, one section
later. Making it twice is redundant.

## CIT-010 — González-Potes, marked FALSE

❌ **Not a verdict, and must not be recorded as one.** Its evidence column reads
*"Source PDF excluded from active prompt selection"* — NotebookLM never read the
paper. **A source it could not open is `NOT-ADDRESSED`, not `REFUTED`**, and the
two are different: a source silent on a claim is not evidence against it.

✅ **The item is in our library, twice**, which is the actual finding here:

```
69RUBISC                       | journalArticle | mdpi.com/2673-2688/7/2/51
gonzález-potes_hybrid_2026     | journalArticle | mdpi.com/2673-2688/7/2/51
```

⚠ **Same title, same URL, two keys — a genuine duplicate**, like the three
*Elements of Statistical Learning* records in thread 277. **Merge in Zotero
before generating the dynamic reference list**, or González-Potes renders twice.

**The claim itself** (98% state specification consistency, median numerical error
below 3%) **remains unverified against the source.** It is carried into the
register below rather than silently accepted — Ch1 §1.1, Ch2 §2.6 and Ch9 all
rest on it.

---

# Confirmed, no action — nine items

**Recorded so nobody re-derives them.** Each was checked against NotebookLM's
quoted evidence and the claim as the thesis states it.

| ID | Claim | Verdict |
|---|---|---|
| CIT-002 | FMCG volatility / SKU proliferation (Ma et al., 2025) | ✅ COHERENT |
| CIT-003 | No single model dominates; ML+exogenous wins on high-volume SKUs | ✅ COHERENT |
| CIT-005 | M5: top 50 all LightGBM, >14% over best statistical benchmark | ✅ COHERENT — all three figures supported |
| CIT-008 | Ng (2017), 4 TB, memory as binding constraint | ✅ COHERENT |
| CIT-009 | Sapkota et al. (2026), Agentic AI paradigm | ✅ COHERENT — 2026 matches Information Fusion vol. 126 |
| CIT-011 | Rinaldi et al. (2025), DSS4EX | ✅ COHERENT |
| CIT-014 | Ng (2017) as empirical precedent for the memory criterion | ✅ COHERENT |
| CIT-015 | Hevner et al. (2004), DSR artefact | ✅ COHERENT |
| CIT-016 | Peffers et al. (2007), DSR process | ✅ COHERENT |

---

# Chapter rename — not recommended

**You asked whether the blocks evaluate renaming. This one does not raise it, and
I do not recommend it for Chapter 1.**

*"Chapter 1 | Introduction"* with the standfirst *"A capability gap in deployed
systems"* is conventional, accurate, and the standfirst already does the work a
more specific title would. ✅ **No change.**

---

# For the registers

## `citations-added-register.md`

**No new citations are added by this pass.** F1, F3 and F5 redistribute sources
already in the library; F2 repoints one. Nothing to register — which is the
outcome the "prefer avoidance to marking" rule wants.

## Deferred / structural

| ID | Item | Recommendation |
|---|---|---|
| **new** | Ch2 §2.1 cites M4 as 2020 only, where Ch1 will now cite 2018+2020 | **Align Ch2 to `(Makridakis et al., 2018, 2020)`.** Same two library items; consistency across chapters. Verify the sentence in context first |
| **new** | `Liu et al. (2025)` cited in Ch2 §2.2 but absent from `reference-list.md` | **Blocks F2.** Check the group library directly |

## Zotero hygiene — before the dynamic list (thread 277)

⚠ **Two duplicates now known**, in addition to the three already recorded:

| Item | Keys |
|---|---|
| González-Potes et al. (2026) | `69RUBISC`, `gonzález-potes_hybrid_2026` |
| *Elements of Statistical Learning* | `4TVC5APJ`, `SPW7NXHT`, `Q4IIBE2Z` (from thread 277) |

**Merge all of these in Zotero before generating the bibliography.**

---

# What this pass did and did not establish

| | |
|---|---|
| **Verified against the library** | every citation named in all seventeen items |
| **Verified against the snapshot** | every anchor below, quoted verbatim including its double spaces |
| **NOT verified** | ⚠ whether González-Potes actually reports 98% / 3%. NotebookLM never opened it |
| **NOT verified** | ⚠ whether `Liu et al. (2025)` exists in the group library |
| **Blocked** | F2, on the Liu 2025 check above |

**Six fixes, four of them one line. F1, F3, F5 and F6 can be pasted now; F4
replaces F3 in the consolidated note; F2 waits on one Zotero lookup.**
