---
name: 2026-09-11_experiment-state-for-ch6-prose-followup-01
description: NOTE - Three further Chapter 6 defects found while verifying the experiment-state note, including a memory budget the chapter states two different ways. Read alongside that note, not instead of it.
snapshot: 2026-09-11_15-41_ch5-applied-review
category: workflow
applies-to: [ch6-architecture]
created: 2026_09_11-18_20
updated: 2026_09_11-18_20
status: ready
---

# Three more Chapter 6 defects

**This does not replace `2026-09-11_experiment-state-for-ch6-prose.md`.** That
note's four fixes were checked against the snapshot and **all four anchors
verify** - the temperature-zero claim, the reliability sentence, both stale
cross-references, and the three-scenario description. Apply it as written.

These three are additional, found while verifying it.

---

# A. The memory budget is stated two different ways, in the same chapter

⚠ **This is the most serious of the three**, because it is internally
contradictory rather than merely stale, and Chapter 5 has already been settled
at four gigabytes.

| Where | Says |
|---|---|
| the architecture-figure caption | **4 GB** |
| Section 6.3, the substrate footprint paragraph | **four-gigabyte** ceiling |
| Section 6.8, first paragraph | **four-gigabyte** ceiling |
| **Section 6.8, the end-to-end peak sentence** | ⚠ **eight-gigabyte** budget |
| **Section 6.10 Summary** | ⚠ **eight-gigabyte** budget |
| Section 6.9 | four-gigabyte |

**Chapter 5 says four**, in both Section 5.1 and Section 5.5.6, and that was
settled deliberately. **Chapter 6 should say four everywhere.**

### Paste - Section 6.8

Replace *"The end-to-end peak of approximately 231 MB is about 2.8% of the
eight-gigabyte budget"* with:

> The end-to-end peak of approximately 231 MB is about six per cent of the
> four-gigabyte budget.

⚠ **The percentage changes too.** 231 MB against 4 GB is **5.6 per cent**, not
2.8. The old figure was computed against the eight-gigabyte number, so correcting
the budget without correcting the percentage would leave a second error behind.

### Paste - Section 6.10

Replace *"designed to operate within an eight-gigabyte budget"* with:

> designed to operate within a four-gigabyte budget

---

# B. Section 6.3's RSS figures disagree with Chapter 5's

Section 6.3 reports *"XGBoost adds about 15 MB, LightGBM about 7 MB"*, and cites
tracemalloc figures of *"Ridge 1.5 MB, LightGBM 18.7 MB, XGBoost 0.2 MB"*.

**Chapter 5, Section 5.5.6 now reports different numbers** from the same source
file, `profiling.csv`: **38.1 MB for LightGBM, 29.2 for XGBoost, 5.4 for Ridge,
1.9 for ARIMA**, all peak fit RSS.

⚠ **Two chapters citing one artefact with different numbers is the defect an
examiner is most likely to catch**, because it needs no domain knowledge to spot.

**Recommendation: cut the figures from Chapter 6 entirely** and point at Chapter
5. The architecture chapter's argument needs the *conclusion* - that the
footprint is orders of magnitude below the ceiling - not a second copy of the
measurements. Stating them once is also what stops them diverging again.

### Paste - Section 6.3, replace the whole measurement passage

> Measured peak resident memory during fitting is in the tens of megabytes for
> every model in the substrate, and the per-component figures are reported with
> the benchmark in Chapter 5. The substrate therefore operates around two orders
> of magnitude below the four-gigabyte ceiling. The binding effect of the memory
> budget is on the model-selection space, which it constrains up front by
> excluding transformer and locally hosted options, rather than on the footprint
> of the models eventually selected.

### Note - keep the argument, drop the duplicate numbers

The sentence that matters is the last one, and it survives intact. It is also
the chapter's strongest claim about the budget: the constraint did its work at
selection time, not at run time.

---

# C. "five categories" and "Chapter 6" are both wrong in the same sentence

Section 6.1's status note says the substrate is *"implemented and benchmarked
across the five categories (Chapter 6)"*.

**Two errors in six words.** The scope is **four** categories, and the substrate
chapter is **Chapter 5**, not Chapter 6.

The experiment-state note flagged the "five" and asked what it was counting.
**Answer: the dropped `totalbeer` category.** The project ran five categories
before it was dropped; the four that remain are CSD, danskvand, energidrikke and
RTD, which every results artefact confirms. **So the correct word is simply
"four".**

### Paste

> The forecasting substrate is implemented and benchmarked across the four
> categories (Chapter 5)

⚠ **The same pair of errors recurs twice more**, and the fix is the same each
time:

| Where | Says | Should say |
|---|---|---|
| Section 6.2, the layer list | "benchmarked in Chapter 6" | **Chapter 5** |
| Section 6.10 Summary | "benchmarked in Chapter 6 (SRQ1)" | **Chapter 5** |

### Note - why these are all Ch5/Ch6 swap residue

Every one of them points one chapter too high, which is the signature of the
8 September swap. **Search the chapter for "Chapter 6" once** and check each hit:
a chapter referring to itself by number is almost always this bug.

---

# Fix 4 is still blocked, but the decision has moved

The experiment-state note blocks Section 6.7 pending "a sixth and seventh rung
under active consideration". **Those were committed at 17:16 today** as
`3c37ffd`, *"scenarios F and G - data, code and the trained model together"*.

The harness now registers **seven scenarios**:

| | scenario | adds |
|---|---|---|
| A | plain LLM | - |
| B | + history and a code sandbox | what data access buys |
| C | + the trained model behind the tool | what the artefact adds |
| D | B's task on Prometheus | the production orchestrator |
| E | C's task on Prometheus | both, on production |
| **F** | **data, code and the model together** | what adding code back on top of the model does |
| **G** | **F's task on Prometheus** | the combined arm, on production |

**Stay blocked anyway.** The arms exist in code but have **no paid run behind
them**, and Section 6.7 should describe a design that has been exercised. The
commit message also records a design decision the section will need to state -
**DEC-COMBINED-INPUT**, that the model's forecast is given as one input among
several rather than as a starting point to revise, because an agent handed a
number and told it may keep it will mostly keep it, which would measure
deference rather than integration.

⚠ **What changes when it unblocks:** "baseline" is no longer the right frame for
Section 6.7. With seven rungs every arm is a comparator for the one below, which
is the deferred question the experiment-state note already raised. That decision
should be taken once, for the whole ladder, rather than per rung.
