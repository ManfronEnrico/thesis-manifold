---
name: ch5-ch6-swap-reference-repair
description: NOTE - Every stale internal cross-reference created by the Ch5/Ch6 swap, with find/replace blocks
category: reference
applies-to: [06_thesis_writing]
triggers: [chapter reorder, cross-reference repair]
snapshot: 2026-09-08_14-05_chapter-reorder
status: ready-to-paste
created: 2026_09_08-14_20
updated: 2026_09_08-14_20
---

# Ch5 / Ch6 swap -- cross-reference repair

**The swap is done in Word.** Ch5 is now *Model Benchmark & Selection*, Ch6 is
*Predictive-Extension Architecture*. This note lists every reference the swap made
wrong, as paste-ready find/replace pairs.

## What Word already fixed, and what it did not

| | Auto-updated? |
|---|---|
| **Headings** (`## 5.1`, `## 6.3` ...) | YES -- every heading is already correct |
| **Body text** (`SS6.3.4`, `Chapter 6`, `Ch6 SS6.5.6`) | **NO** -- plain text, all stale |

So the chapter *structure* is right; only the prose pointing at it is wrong.
(`SS` above stands for the section sign used in the document.)

## Two traps before you start

**1. Do not find-and-replace the section sign + `6.` or + `5.` across the benchmark
chapter.** Three of them are **citations to Hyndman & Athanasopoulos (2021, 5.2)**,
not to a section of this thesis -- snapshot lines 17, 27 and 259. Replacing those
turns a source reference into a self-reference. Every block below is anchored to
surrounding words for exactly this reason.

**2. The snapshot filenames are now inverted and will mislead any script.**
`chapters/ch5-framework-design.md` contains **Model Benchmark**;
`chapters/ch6-model-benchmark.md` contains **Architecture**. The exporter keeps the
slug it first assigned. Go by chapter *title*, never the filename.

---

## A. Inside Ch5 (Model Benchmark) -- 20 internal refs

These are self-references inside the benchmark chapter. Its own headings are already
`5.x`, so every `6.x` reference in its body now points at the architecture chapter.

Each find-string is anchored to adjacent words, so none of them can match a citation.

| # | Find (unique fragment) | Replace |
|---|---|---|
| A1 | `4-fold expanding-window CV (§6.3.4)` | `4-fold expanding-window CV (§5.3.4)` |
| A2 | `seed sensitivity is measured separately (§6.5)` | `seed sensitivity is measured separately (§5.5)` |
| A3 | `categorisation rather than removal**  - see §6.4.4.` | `categorisation rather than removal**  - see §5.4.4.` |
| A4 | `the simple benchmarks of §6.2.0**, scored` | `the simple benchmarks of §5.2.1**, scored` |
| A5 | `own test rows (§6.5.2)` | `own test rows (§5.5.2)` |
| A6 | `different functionals (§6.4.1), each model` | `different functionals (§5.4.1), each model` |
| A7 | `as the theory in §6.4.1 predicts` | `as the theory in §5.4.1 predicts` |
| A8 | `selection bias documented in §6.3.5` | `selection bias documented in §5.3.5` |
| A9 | `The four benchmarks of §6.2.0 were run` | `The four benchmarks of §5.2.1 were run` |
| A10 | `though §6.5.9 shows the magnitudes` | `though §5.5.9 shows the magnitudes` |
| A11 | `Croston partition of §6.4.4` | `Croston partition of §5.4.4` |
| A12 | `does not exist in the cited source (§6.4.3)` | `does not exist in the cited source (§5.4.3)` |
| A13 | `the simple benchmarks of §6.5.2 alone` | `the simple benchmarks of §5.5.2 alone` |
| A14 | `optimistically biased by an unquantified amount (§6.3.5)` | `optimistically biased by an unquantified amount (§5.3.5)` |
| A15 | `fig4_ram_budget is stale and contradicts §6.5.6.` | `fig4_ram_budget is stale and contradicts §5.5.6.` |
| A16 | `§6.6 states the conclusion this supports instead.` | `§5.6 states the conclusion this supports instead.` |
| A17 | `changes with the seed in all four categories** (§6.5.7)` | `changes with the seed in all four categories** (§5.5.7)` |
| A18 | `test sizes stated in §6.3.1` | `test sizes stated in §5.3.1` |
| A19 | `the target is withdrawn (§6.4.3)` | `the target is withdrawn (§5.4.3)` |
| A20 | `whether §6.6’s combination paragraph` | `whether §5.6’s combination paragraph` |

**A4 and A9 also fix a second, older defect.** They cite **6.2.0** -- a section number
that exists in neither numbering. The simple benchmarks are **5.2.1**
("Simple benchmarks"). This was already broken before the swap.

**Leave these three alone** -- textbook citations, not thesis sections:

> Hyndman & Athanasopoulos (2021, **§5.2**)   <- snapshot lines 17, 27, 259

---

## B. Inside Ch6 (Architecture) -- 2 internal refs

| # | Find | Replace |
|---|---|---|
| B1 | `the integration-readiness assessment (SRQ3, Section 5.6), not the evaluated implementation` | `the integration-readiness assessment (SRQ3, Section 6.6), not the evaluated implementation` |
| B2 | `it is instead the baseline against which the artefact is compared (Section 5.7).` | `it is instead the baseline against which the artefact is compared (Section 6.7).` |

Both were correct before the swap and are now off by one chapter.

---

## C. Cross-chapter references

### C1 -- Chapter 1

Three simple number changes:

| Find | Replace |
|---|---|
| `SRQ1 motivates the empirical model benchmark in Chapter 6, which evaluates` | `SRQ1 motivates the empirical model benchmark in Chapter 5, which evaluates` |
| `a structured forecast-tool interface (Chapter 5) and its realisation` | `a structured forecast-tool interface (Chapter 6) and its realisation` |
| `an integration-readiness specification (Chapter 5, assessed in Chapters 7 and 9)` | `an integration-readiness specification (Chapter 6, assessed in Chapters 7 and 9)` |

**Then the two chapter-summary paragraphs must swap wholesale, not merely renumber** --
their *content* is now in the wrong order for the reader walking down the list.

**Action:** REPLACE both paragraphs, in place, with the two below in this order.

**Find** -- the two consecutive bolded paragraphs, currently reading:

> **Chapter 5** describes the predictive-extension architecture: ...
>
> **Chapter 6** addresses SRQ1 through an empirical model benchmark, ...

**Replace with:**

> **Chapter 5** addresses SRQ1 through an empirical model benchmark, comparing lightweight forecasting models across the four categories on accuracy, memory efficiency, and stability, and testing category specialisation against pooling.
>
> **Chapter 6** describes the predictive-extension architecture: the forecasting substrate, the structured forecast-tool interface, and the bounded tool-using agentic decision-support layer, together with the integration-readiness capabilities, justified against the 8GB RAM budget. The evaluated prototype uses a lightweight Python coordinator; the production target is a LangGraph deployment.

*Keep whatever your current second paragraph says after "8GB RAM budget" -- only the
number and the ordering need to change.*

### C2 -- Chapter 2

| Find | Replace |
|---|---|
| `absolute errors instead. Chapter 6 encounters and documents the same problem` | `absolute errors instead. Chapter 5 encounters and documents the same problem` |
| `bear directly on a monthly demand panel, and Chapter 6 accordingly measures coverage` | `bear directly on a monthly demand panel, and Chapter 5 accordingly measures coverage` |

**A third ch2 hit is already correct -- do not touch it.**

> "the realised footprint of the chosen substrate is shown in **Chapter 5** to sit well within the budget"

The realised RAM footprint is reported in **5.5.6 Operational profile**, which is in
the benchmark chapter. It said "Chapter 5" before the swap for the wrong reason and is
now right for the right one. Listed here only so you do not "fix" it into being wrong.

### C3 -- Chapter 3 (4 refs, one of them easily missed)

| Find | Replace |
|---|---|
| `the RSS measurements are reported in Chapter 6.` | `the RSS measurements are reported in Chapter 5.` |

RSS memory profiling is reported in **5.5.6 Operational profile** -- the benchmark
chapter. (This is a *fourth* ch3 reference, easily missed: it sits at the tail of a long
sentence about `psutil` vs `tracemalloc`, not near any other chapter pointer.)

**One clause needs its word order flipped, not its numbers:**

**Find:**
> `constitutes the core contribution of Chapters 5 and 6, where the predictive-extension architecture is specified and the forecasting model`

**Replace:**
> `constitutes the core contribution of Chapters 5 and 6, where the forecasting models are benchmarked and the predictive-extension architecture is specified`

The clause names the two contributions in sequence, so the sequence must flip even
though the chapter numbers do not.

**And one needs nothing:** `"across Chapters 5 through 8"` -- a span is unaffected by
a swap inside it.

### C4 -- Chapter 4

| Find | Replace |
|---|---|
| `The exact extraction interface used by the pipeline is documented in Chapter 5;` | `The exact extraction interface used by the pipeline is documented in Chapter 6;` |
| `Benchmarking (Chapter 6) is conducted on the brand` | `Benchmarking (Chapter 5) is conducted on the brand` |

Two further `Chapter 6` hits in ch4 sit inside text that `ch4-pass.md` already
replaces. **Apply `ch4-pass.md` first**, then these -- otherwise you edit a sentence
that is about to be replaced anyway.

### C5 -- Chapters 8 and 9

| Find | Replace |
|---|---|
| `On the selected per-category configuration (Ch6 §6.5.6), tuned XGBoost` | `On the selected per-category configuration (Ch5 §5.5.6), tuned XGBoost` |
| `separately (§8.3.2 / Ch6 §6.5.4: ensemble conformal coverage` | `separately (§8.3.2 / Ch5 §5.5.4: ensemble conformal coverage` |
| `motivates the per-category representation choice (Ch6 §6.5.6)` | `motivates the per-category representation choice (Ch5 §5.5.6)` |

---

## D. The SRQ3 table row -- three occurrences, one judgement call

An identical "Connection to SRQs" table row appears in **three chapters**:

| Chapter | Snapshot line |
|---|---|
| Ch5 Model Benchmark, "Connection to SRQs" | 396 |
| Ch7 Decision Synthesis | 135 |
| Ch8 Experimental Evaluation | 152 |

All three read:

> `| SRQ3 | Not addressed here; integration readiness is addressed in Ch3 and Ch5 |`

**Integration readiness is §6.6, in the architecture chapter** -- which after the swap is
**Ch6**, not Ch5. So all three rows are now wrong, and the one inside Ch5 is additionally
self-contradictory: it sits in the benchmark chapter while pointing at it.

**Replace in all three** (identical string, so a single find-all is safe here -- it occurs
nowhere else):

> **Find:** `integration readiness is addressed in Ch3 and Ch5`
> **Replace:** `integration readiness is addressed in Ch3 and Ch6`

---

## E. Repo-side edits (not Word)

Per P0048's execution recipe, outside the `.docx` and **not yet done**:

1. `PATHS.py:175` -- swap `"architecture"` and `"model_benchmark"` in `CHAPTER_SLUGS`
2. `05_thesis_results/05_architecture/` -> `06_architecture/` and
   `06_model_benchmark/` -> `05_model_benchmark/` (**together** -- they collide otherwise)
3. Six diagram stems `ch5_*` <-> `ch6_*`, plus their string literals in
   `generate_architecture_diagrams.py` (~lines 360, 448, 533, 886, 968)
4. Re-resolve image links in `sections-drafts/ch5-framework-design.md`

This note covers the prose only.

---

## Verification after pasting

Re-run the snapshot, then:

```bash
cd 06_thesis_writing/docx-exported-snapshots/<newest>/chapters
grep -nE "6\.[0-9]" ch5-framework-design.md | grep -i "hyndman\|§"   # only the 3 citations
grep -n "Section 5\." ch6-model-benchmark.md                          # expect none
grep -n "Ch6 §6" *.md                                                 # expect none
```
