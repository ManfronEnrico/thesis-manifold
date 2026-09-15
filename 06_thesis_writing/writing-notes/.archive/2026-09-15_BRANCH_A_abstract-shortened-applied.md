---
name: 2026-09-15_BRANCH_A_abstract-shortened
description: FOLLOW-UP - The abstract at 360 words, a quarter shorter, to fit one page. Supersedes the 480-word version. Same four paragraphs, same claims, nothing new removed from the argument.
category: workflow
applies-to: [abstract]
triggers: [abstract, front matter, S29, submission]
created: 2026_09_15-00_45
updated: 2026_09_15-00_45
snapshot: 2026-09-15_00-30_eod-final-pass
status: prose ready to paste, awaiting human review
---

# The abstract, one quarter shorter

Verified at `2b33025`, fetch clean. Snapshot `2026-09-15_00-30_eod-final-pass`.
Zotero: 92 items.

| In `2026-09-14_BRANCH_A_abstract.md` | Status |
|---|---|
| Fix 1, the replacement text | **superseded by F1 below** |
| Everything else — the anchor, the comment ledger, the figure sourcing table, the notes | **stands unchanged** |

**480 → 360 words (−25%).** The anchor, the action and all eight thread verdicts
are unchanged, so read that note for the placement and this one for the text.

---

# F1 — the shortened abstract

### Action

REPLACE, using the anchor given in the main note (the whole section, from
*"# Abstract"* through *"### Keyword list / Keywords:"*).

#### Replace with

> Production agentic decision-support systems increasingly explain what has
> happened but cannot anticipate what comes next. This thesis asks how such a
> system, deployed with Danish retailers and consumer-goods manufacturers, can be
> extended with forecasting light enough for a small provider's resource budget,
> and whether a dedicated forecasting layer is warranted once a language model can
> write and execute its own forecasting code.
>
> The research follows Design Science Research, producing an instantiation and
> method-level design knowledge. The artefact extends a production system with a
> benchmarked forecasting substrate, exposed to a tool-using agentic layer through
> a typed interface carrying a point forecast, a split-conformal prediction
> interval, the serving model's measured out-of-sample error, and the provenance
> needed to reconstruct the call. It is evaluated on a commercial scanner panel
> covering four Danish beverage categories at brand-and-month grain. The central
> evaluation is a ladder of seven scenarios over sixty-three funded runs, adding
> capability one variable at a time — no firm data; the firm's history in a code
> sandbox; the same data behind the typed tool; and both — with three scenarios
> executed inside the production platform so each is paired with its counterpart.
>
> Four findings follow. Gradient-boosted models dominate the classical and linear
> baselines, but a five-seed sweep changes which is selected in every category, so
> the choice is properly an operational one. The memory constraint bound the
> selection of architectures rather than run time, fitting peaking at thirty-two
> megabytes against a four-gigabyte ceiling. Reliability and traceability hold at
> the interface; uncertainty is where the result is negative and informative, the
> interval attaining its coverage guarantee while remaining too wide to act on for
> a single brand. In the scenario comparison, access to the firm's own data is
> worth far more than anything above it on the ladder, moving median error from
> 502 per cent to under three; above that the dedicated model does not win on
> accuracy, but returns a forecast at roughly a fiftieth of the cost, twenty times
> faster, and identical on every repeat.
>
> The contribution is therefore qualified, and the qualification is the point. A
> language model given data and an execution environment is a stronger forecaster
> than the literature generally grants it, and a dedicated predictive layer must
> be justified on reproducibility, cost and auditability rather than on error
> alone. The thesis contributes a working artefact, five design principles for
> extending non-predictive agentic systems with forecasting, and an evaluation
> design that measures cost and latency beside accuracy. Its scope is a single
> organisation, one national market and four categories, with the scenario
> comparison resting on three brands within one of them.
>
> **Keywords:** demand forecasting; agentic decision-support; design science
> research; large language models; prediction intervals; retail analytics

---

# What came out, and why each was safe

| Cut | Words | Why it survives the cut |
|---|---|---|
| The Hevner and Peffers citations | ~12 | ⚠ Both are cited in full in Ch3. Some CBS templates discourage citations in an abstract anyway — this resolves that question by removing it |
| "two categories are beaten outright by parameter-free benchmarks" | ~11 | The main note already flagged this as the most compressible sentence. The SRQ1 finding survives on the seed-sweep clause |
| "three alternative calibration schemes were tested without improving coverage and width together" | ~13 | The negative result is fully carried by "too wide to act on" |
| "Every scenario answers an identical question, and all scoring is arithmetic comparison against recorded outputs" | ~16 | Method detail, not a finding. Ch3 and Ch8 both state it |
| "on both orchestrators" | ~3 | Already implied by "three scenarios executed inside the production platform so each is paired with its counterpart" |
| "the design principles are derived from one design cycle rather than validated across contexts" | ~14 | ⚠ The weakest cut — it is a real limitation. It is stated in Ch10 §10.4 and in the scope sentence's spirit. **Restore it first if you find you have room** |
| "in small and medium-sized enterprises" | ~6 | The Danish SME framing arrives in the next clause |
| Assorted tightening | ~30 | "therefore a qualified one" → "therefore qualified", etc. |

⚠ **Nothing was cut that a later chapter contradicts.** Every remaining figure is
sourced in the main note's provenance table, and none was rounded further.

**If it still overruns**, cut the third paragraph's memory sentence — SRQ1's
resource finding is the one an examiner is least likely to check against the
abstract, and Ch5 states it three times.
