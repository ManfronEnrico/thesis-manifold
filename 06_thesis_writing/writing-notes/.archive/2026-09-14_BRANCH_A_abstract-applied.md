---
name: 2026-09-14_BRANCH_A_abstract
description: NOTE - The abstract, written from Chapter 10's four SRQ answers. Replaces a bullet skeleton describing a system that was never built - a multi-agent Claude artefact, an LLM-as-judge evaluation, and a second data source that does not exist. Resolves all 8 threads. Closes S29.
category: workflow
applies-to: [abstract]
triggers: [abstract, front matter, S29, submission]
created: 2026_09_14-17_30
updated: 2026_09_14-17_30
snapshot: 2026-09-14_16-21_post-comment-pass-archive
status: prose ready to paste, awaiting human review
---

# The Abstract

Verified at `41ecb76`, fetch clean. Snapshot
`2026-09-14_16-21_post-comment-pass-archive`. Zotero: 89 items. **Eight threads:
5, 6, 7, 8, 9, 10, 11, 12 — all resolved by the single replacement below.**

**Source of every claim:** Chapter 10 §10.1, which is the thesis's only current
statement of all four SRQ answers, plus Chapter 8's measured figures. **Nothing
here is new to the document**, which is the property an abstract must have.

---

# Why this is a replacement and not an edit

**The current abstract describes a different thesis.** It is a bullet skeleton
carrying `[TBD - fill after empirical results]`, and what is written around the
placeholders is not merely unfinished but wrong:

| Current text | Reality |
|---|---|
| "multi-agent AI framework", "multi-agent system (LangGraph orchestration + 5 lightweight ML models + LLM synthesis via Claude API)" | No multi-agent system. A Python coordinator, six model families, OpenAI `gpt-5.5` |
| "Nielsen CSD panel **+ Indeks Danmark consumer survey**" | **One source.** There is no consumer survey |
| "3-level evaluation framework: ML accuracy, recommendation quality / **LLM-as-Judge**, RAM and latency" | No judge. A seven-scenario ladder, scored arithmetically |
| "SRQ3: [MAPE improvement from consumer signal enrichment — X%]" | SRQ3 is **integration readiness**. It has no MAPE |
| "Danish CSD retail" as the scope | **Four categories**, not one |
| "Validated proof-of-concept ... within ≤4GB RAM" | The budget bound **selection**, not run time — 32 MB peak |
| "calibrated, contextualised demand recommendations" | The chapter spends two sections showing the interval is **too wide to act on** |

⚠ **This is the first page an examiner reads.** Everything else in the thesis has
been corrected against Branch A; the abstract still advertises the abandoned
design.

---

# The fix

## Fix 1 — replace the entire abstract

### Anchor

**The whole section**, from the heading *"# Abstract"* through the end of
*"### Keyword list / Keywords:"*. That includes the *"## Purpose"* block, the
*"## Bullet skeleton (to be converted to prose after empirical results
available)"* heading, and all six bullet blocks.

### Action

REPLACE.

#### Replace with

> Production agentic decision-support systems in small and medium-sized
> enterprises increasingly explain what has happened but cannot anticipate what
> comes next. This thesis asks how such a system, already deployed with Danish
> retailers and consumer-goods manufacturers, can be extended with forecasting
> light enough for a small provider's resource budget, and whether a dedicated
> forecasting layer is warranted at all once a language model can write and
> execute its own forecasting code.
>
> The research follows Design Science Research (Hevner et al., 2004; Peffers et
> al., 2007), producing both an instantiation and method-level design knowledge.
> The artefact extends a production system with a benchmarked forecasting
> substrate, exposed to a tool-using agentic layer through a typed interface that
> carries a point forecast, a split-conformal prediction interval, the serving
> model's measured out-of-sample error, and the provenance needed to reconstruct
> the call. It is evaluated on a commercial scanner panel covering four Danish
> beverage categories at brand-and-month grain. The central evaluation is a
> ladder of seven scenarios over sixty-three funded runs, in which capability is
> added one variable at a time — no firm data; the firm's history in a code
> sandbox; the same data behind the typed tool; and both — with three of the
> seven executed inside the production agentic platform so that each is paired
> with its counterpart. Every scenario answers an identical question, and all
> scoring is arithmetic comparison against recorded outputs.
>
> Four findings follow. Gradient-boosted models dominate the classical and linear
> baselines across all four categories, but a five-seed sweep changes which of
> the two is selected in every category, so they are statistically
> indistinguishable here and the choice is properly an operational one; two
> categories are beaten outright by parameter-free benchmarks. The memory
> constraint bound the selection of architectures rather than run time, with
> fitting peaking at thirty-two megabytes against a four-gigabyte ceiling.
> Reliability and traceability hold at the interface and were checked, while
> uncertainty is where the result is negative and informative: the interval
> attains its coverage guarantee and is too wide to act on for a single brand,
> and three alternative calibration schemes were tested without improving
> coverage and width together. In the scenario comparison, access to the firm's
> own data is worth far more than anything above it on the ladder, moving median
> error from 502 per cent to under three; above that the dedicated model does not
> win on accuracy, but returns a forecast at roughly a fiftieth of the cost,
> twenty times faster, and identical on every repeat, on both orchestrators.
>
> The contribution is therefore a qualified one, and the qualification is the
> point. A language model given data and an execution environment is a stronger
> forecaster than the literature generally grants it, and a dedicated predictive
> layer must be justified on reproducibility, cost and auditability rather than
> on error alone. The thesis contributes a working artefact, five design
> principles for extending non-predictive agentic systems with forecasting, and
> an evaluation design that measures cost and latency beside accuracy. Its scope
> is a single organisation, one national market and four categories, with the
> scenario comparison resting on three brands within one of them; the design
> principles are derived from one design cycle rather than validated across
> contexts.
>
> **Keywords:** demand forecasting; agentic decision-support; design science
> research; large language models; prediction intervals; retail analytics

---

# Notes

### Length

**Approximately 480 words**, which fits one page at CBS's formatting. ⚠ **If it
runs long in Word, cut from the third paragraph** — the SRQ1 qualification about
parameter-free benchmarks is the most compressible sentence, and the finding
survives without it.

### Every figure, and where it comes from

| Figure | Source |
|---|---|
| four categories, brand-and-month | Ch4 §4.1 |
| seven scenarios, 63 runs | Ch8 §8.3, `runs.csv` filtered to v6 |
| five-seed sweep changes the selection | Ch5 Table 15 |
| 32 MB fit against a 4 GB ceiling | `profiling.csv`, Ch5 §5.5.6 |
| three calibration schemes tested | Ch5 §5.5.7 |
| 502 per cent → under three | Ch8 §8.3, Ch10 §10.1 |
| fiftieth of the cost, twenty times faster | Ch8 §8.3 — 51.5× and 20.8× |
| five design principles | Ch10 §10.2 |

**Nothing is rounded in a direction that flatters.** "Roughly a fiftieth" is
51.5×; "twenty times faster" is 20.8×.

### What this abstract deliberately does not do

- **It does not claim the artefact wins.** The honest headline is that no
  scenario leads on every axis, and the abstract says so in its final paragraph.
  ⚠ An abstract that overstates will be contradicted by Chapter 8 twenty pages
  later, which is worse than a modest one.
- **It does not use "calibrated" loosely.** The intervals are calibrated in the
  conformal sense and uninformative in the practical one; the word is avoided.
- **It does not mention AI assistance.** That belongs in the AI Use Declaration.

### The Purpose block

⚠ *"The abstract summarises the entire thesis in one page. CBS examiners read it
first — it must communicate problem, method, findings, and contribution
clearly."* is an **instruction to the writer**, not abstract content. It is
deleted by the replacement. Thread 5 tags it `METACOMMENT`; thread 6 is a
resolved test comment.

---

# Comment ledger — all 8 threads

| Thread | Verdict |
|---|---|
| 5, the Purpose metacomment | **ADDRESSED** — deleted |
| 6, "Test Comment Resolved" | already resolved; delete the thread |
| 7, Problem | **ADDRESSED** — paragraph 1 |
| 8, Method | **ADDRESSED** — paragraph 2 |
| 9, Key findings TBD | **ADDRESSED** — paragraph 3 |
| 10, Contribution | **ADDRESSED** — paragraph 4 |
| 11, Scope note | **ADDRESSED** — folded into paragraph 4 |
| 12, Keyword list | **ADDRESSED** — six keywords supplied |

**8 of 8 addressed. S29 closes when this is pasted.**

---

# Citations

Hevner et al. (2004) and Peffers et al. (2007), both already in the library and
cited in Ch2, Ch3 and Ch10. **No new sources.**

⚠ **Check whether your programme wants citations in the abstract at all.** Some
CBS templates discourage them. If so, delete the two parenthetical citations —
the sentence reads correctly without them, since both are cited in full in
Chapter 3.
