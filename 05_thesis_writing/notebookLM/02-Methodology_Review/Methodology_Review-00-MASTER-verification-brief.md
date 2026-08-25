---
name: methodology-review-verification-brief
description: NotebookLM briefing pack — every methodological claim Ch3 and Ch4 attribute to Saunders et al. (2023), quoted verbatim, with the falsification test for each. Upload with the 14 Saunders chapter PDFs and the two chapter drafts.
created: 2026_08_25-12_00
updated: 2026_08_25-12_00
---

# Methodology — Source Verification Brief (Saunders et al., 2023)

**For NotebookLM.** Upload the 14 `Saunders_et_al-2023-Ch_NN-*.pdf` files from
`Methdology Book Chapters/`, plus `ch3-methodology.md` and `ch4-data-assessment.md`.
Then work through this document.

**This differs from the literature-review brief in one important way.** There, thirty-six
papers each supported one or two claims, and the job was to check each claim against its
paper. Here, a *single* source supplies an entire framework that two chapters are built
on — so a misreading is not one bad sentence but a structural fault running through a
chapter. The questions are correspondingly weighted toward **whether the framework is
applied as Saunders defines it**, not only whether individual sentences are quotable.

---

## YOUR TASK

For every claim below, return:

```
### <ID> — <short title>
**Verdict:** Supported | Partially Supported | Contradicted | Not Addressed | Cannot Verify
**Source location:** <chapter, section, page>
**Verbatim quote:** "<exact words from the PDF>"
**Analysis:** <what the source actually says; where the thesis diverges>
**Safest thesis-ready wording:** <a replacement sentence, if one is needed>
```

Four rules:

1. **Quote, do not paraphrase.** A paraphrase cannot settle whether a term is used as
   Saunders defines it.
2. **"Not Addressed" is a valid and useful verdict.** If Saunders does not discuss
   something the thesis attributes to him, say so plainly — that is the finding.
3. **Terminology precision is the point here.** Saunders' terms are technical
   (*evaluative* vs *explanatory* purpose; *survey* secondary data; *mono-method
   quantitative*). A thesis using one where Saunders means another is wrong even when
   the sentence reads sensibly.
4. **Flag any claim of the form "following Saunders, X"** where Saunders offers X as one
   option among several rather than as a recommendation. Presenting a menu choice as
   methodological authority is the characteristic error of this kind of chapter.

---

## PART 1 — CRITICAL: the three claims that carry the most weight

### MR-01 — Is this research design "explanatory"?

**Thesis claim** (`ch3:§3.2`, verbatim):
> "The research design type within the CBS taxonomy is **explanatory**: the thesis is not
> merely describing what the framework does, but explaining how and why specific
> architectural choices ... produce better forecast-informed decision-support outcomes
> than a general-purpose code-as-action LLM baseline."

**Why this is critical.** Saunders lists four research purposes — exploratory,
descriptive, explanatory, evaluative. The thesis builds an artefact and measures whether
it performs better than a baseline. That is arguably **evaluative** in Saunders' sense,
or a combination, and calling it explanatory may be a category error at the top of the
methodology chapter.

**Ask NotebookLM (Ch 5, "Formulating the research design"):**
1. Quote Saunders' definitions of **explanatory** and **evaluative** research purpose
   verbatim. What distinguishes them?
2. Does Saunders discuss studies that **combine** purposes? Quote the passage.
3. Under Saunders' definitions, which purpose fits "build an artefact, then measure
   whether it outperforms a baseline on defined criteria"?
4. Does Saunders use the phrase "research design type"? If the thesis attributes a
   taxonomy to CBS rather than to Saunders, is there a Saunders equivalent it should
   align with?

---

### MR-02 — Is the "single-case embedded study" label used correctly?

**Thesis claim** (`ch3:§3.3`, verbatim):
> "The primary research strategy is a **quantitative experiment combined with a
> single-case embedded study**."
> "Manifold AI serves as the case organisation ... The **unit of analysis** is the
> predictive-extension artefact."

**Why this is critical.** Saunders (following Yin) defines *embedded* case study by
having **multiple units of analysis within one case**. The thesis names exactly one unit
of analysis — the artefact — which would make it a *holistic*, not embedded, single case.
Additionally, combining an experiment with a case study is a **multi-method** or
**mixed-method** design in Saunders' terms, and the thesis never states which.

**Ask NotebookLM (Ch 5):**
1. Quote Saunders' definition of **embedded** vs **holistic** case study. What exactly
   makes a case study embedded?
2. Given that the thesis names one unit of analysis, is "embedded" correct? If not, what
   is the correct term?
3. Quote Saunders on **combining strategies**. Is experiment + case study a recognised
   combination, and what does he call it?
4. Under Saunders' **methodological choice** layer, what is a study that uses only
   quantitative techniques across two strategies — mono-method quantitative,
   multi-method quantitative, or mixed methods? Quote the definitions.
5. Does Saunders impose conditions on case selection (typical, extreme, revelatory)?
   Does a single case chosen because it is the industry partner satisfy them, and what
   does he say about **convenience** in case selection?

---

### MR-03 — Does the pragmatism claim match Saunders' definition?

**Thesis claim** (`ch3:§3.1`, verbatim):
> "This thesis adopts a **pragmatist** philosophy of science ... Pragmatism holds that
> there is no single, context-independent criterion of truth."
> "the thesis adopts a **modest realism** about the business realities it studies"

**Why this is critical.** This is the innermost commitment of the chapter and everything
downstream is justified by coherence with it. Two specific risks: (a) Saunders'
pragmatism is characterised by **the research question driving method choice**, which is
a different emphasis from the truth-criterion framing used here; (b) "modest realism"
alongside pragmatism may be closer to Saunders' **critical realism**, and if so the
chapter may be describing one philosophy while naming another.

**Ask NotebookLM (Ch 4, "Understanding research philosophy"):**
1. Quote Saunders' full characterisation of **pragmatism** — its ontology, epistemology,
   axiology, and typical methods.
2. Quote his characterisation of **critical realism**. Is "reality exists independently
   but is known only through measurement instruments that carry their own assumptions"
   pragmatism or critical realism in his terms?
3. Does Saunders present pragmatism as primarily about **truth criteria**, or about
   **research questions driving method**? Quote.
4. Is the thesis's stated position internally coherent under Saunders' scheme, or does
   it blend two philosophies? Quote whatever he says about mixing philosophical positions.
5. Saunders discusses **axiology** (the role of values) for each philosophy. The thesis
   does not address axiology at all. What does pragmatist axiology require, and is its
   absence a gap?

---

## PART 2 — CLAIM BANK

### Ch3 — Methodology

| ID | Thesis claim | Location | Falsification test |
|---|---|---|---|
| MR-04 | The thesis is a **narrative, integrative review** rather than a systematic review, justified because "the contribution lies at the intersection of several distinct literatures" | `ch2:16` | Does Saunders (Ch 3) recognise "narrative/integrative review" as a legitimate type? Quote his review typology. Is intersectionality of literatures a reason he accepts? |
| MR-05 | The literature search is described as: ~100 records screened by title, ~40 by abstract, thematic mapping, iterative re-search until themes "adequately covered" | `ch2:16` | Does this satisfy Saunders' criteria for a **critical** literature review (Ch 3)? What does he require that this does not state — search strings, databases, inclusion/exclusion criteria, date ranges? |
| MR-06 | Literature review scope was refined as RQs evolved, "in the iterative manner characteristic of a literature review (Saunders et al., 2023)" | `ch2:14` | Does Saunders describe the review as iterative in this way? Quote. Does he warn about scope refinement *after* seeing results (a distinct risk)? |
| MR-07 | Time horizon is never stated in Ch3 | `ch3` (absent) | Saunders' onion layer 5 requires cross-sectional or longitudinal. Forecasting on a 37–42-month panel — which is it in his terms? Is a study that *analyses* longitudinal data but collects it at one point cross-sectional? Quote his definitions. |
| MR-08 | Approach to theory development is never stated in Ch3 | `ch3` (absent) | Saunders' onion layer 2 requires deduction, induction, or abduction. Which fits DSR — building an artefact then evaluating it? Quote his definition of **abduction** specifically. |
| MR-09 | "The epistemological stance is **empirical**" | `ch3:§3.1` | Is "empirical" an epistemological position in Saunders' scheme, or a property of method? Quote his epistemology options. |
| MR-10 | Ethics is not discussed in Ch3 beyond a confidentiality agreement mention | `ch3:§3.3` | What does Saunders (Ch 6) require in a research ethics statement? Which of his required elements are absent — informed consent, data storage, anonymisation, right to withdraw, ethical approval? |
| MR-11 | Validity/reliability are addressed in `§3.6` | `ch3:§3.6` | Does Saunders apply **reliability/validity** to quantitative work and **dependability/credibility/transferability** to qualitative? Which vocabulary is correct for this thesis, and is it used consistently? |

### Ch4 — Data assessment (the most Saunders-dependent chapter)

| ID | Thesis claim | Location | Falsification test |
|---|---|---|---|
| MR-12 | Nielsen data is **"survey secondary data"** in Saunders' taxonomy | `ch4:23` | Quote Saunders' (Ch 8) secondary-data taxonomy in full. Is a **commercial scanner panel** survey data, or does it fall under documentary/multiple-source? This label drives the whole chapter — get the quote exact. |
| MR-13 | The chapter follows a **three-stage evaluation**: (i) overall suitability, (ii) precise suitability, (iii) costs/benefits | `ch4:15` | Is this Saunders' actual structure? Quote his stages verbatim and confirm the names, order, and count. Does he have a stage the thesis omits? |
| MR-14 | Stage (ii) comprises "reliability/dependability, validity/credibility, and measurement bias/trustworthiness" | `ch4:15` | Are these Saunders' precise-suitability criteria, or has the thesis merged his quantitative and qualitative vocabularies? Quote. |
| MR-15 | Missing promo variables for danskvand/RTD are "an **unmeasured-variable limitation** in Saunders' terms" | `ch4:48` | Does Saunders use the term "unmeasured variable"? Quote his discussion of variables absent from secondary data and the term he actually uses. |
| MR-16 | "Because access is commercial and restricted, the data could not have been collected independently within the scope of a thesis, which is itself a **Saunders-listed advantage**" | `ch4:23` | Quote Saunders' list of secondary-data advantages. Is "could not be collected independently" among them, or is the thesis inventing an advantage? |
| MR-17 | Data are "treated as a partial but workable representation ... rather than a theory-free objective record", tied to the pragmatist stance | `ch4:13` | Does Saunders connect secondary-data evaluation to philosophical stance? Or is this coherence claim the thesis's own? Verdict "Not Addressed" is likely and is fine. |
| MR-18 | Measurement validity and coverage are the two components of overall suitability | `ch4:15,48` | Quote Saunders on **measurement validity** for secondary data. Does he include coverage under overall suitability or elsewhere? |
| MR-19 | Train/validation/test split is described as **"locked, pre-registered"** | `ch4:15` | Does Saunders discuss pre-registration? If not addressed, where does the thesis's justification for this actually come from — and should it cite a different source? |

---

## PART 3 — WHAT THIS BATCH CANNOT SETTLE

State these as out of scope rather than guessing:

1. **DSR itself is not in Saunders.** Hevner and Peffers are the DSR sources; Saunders
   does not cover design science. If asked whether Saunders endorses DSR, the answer is
   Not Addressed. **But do answer this:** does Saunders' Ch 5 strategy list have a slot
   DSR could occupy, or is DSR genuinely outside his framework? That determines whether
   Ch3 must justify departing from Saunders explicitly.
2. **CBS-specific requirements.** Where the thesis says "the CBS taxonomy" or "CBS case
   study guidelines", Saunders cannot confirm these. Flag them for separate checking
   against CBS documentation.
3. **Whether the supervisor accepts DSR** (open item OI-03 in Ch3) is an institutional
   question, not a source question.

---

## PART 4 — THE QUESTION I MOST WANT ANSWERED

Beyond claim-checking: **is the Ch3 onion coherent?**

Saunders' central argument is that the six layers must be *mutually consistent* —
philosophy constrains approach, which constrains methodological choice, which constrains
strategy, and so on inward. Ch3 currently states philosophy (pragmatism), strategy
(experiment + case study), and techniques, but **leaves layers 2, 3 and 5 unstated**.

**Read Ch3 as a whole against Saunders Ch 4–5 and answer:**

1. Fill in the three missing layers as Saunders would require, given what Ch3 *does*
   state. Quote the definitions you rely on.
2. Is there any **inconsistency** between the stated layers? Specifically: is a
   controlled experiment with a held-constant baseline compatible with pragmatism, or is
   it a more positivist move that the philosophy section would then need to accommodate?
3. Saunders warns against choosing a philosophy to fit a method already selected. Does
   Ch3 read as philosophy-first or method-first, on the internal evidence?

---

## PART 5 — REPO FIXES ALREADY KNOWN (not NotebookLM tasks)

Recorded so they are not lost; **none has been actioned**, and none needs the PDFs:

| # | Fix | Location |
|---|---|---|
| S1 | "five categories" → four (beer scoped out; Ch4 already says four) | `ch3:§3.3`, `§3.4`, `§3.5` — several occurrences |
| S2 | "five forecasting models ... MAPE and RMSE" contradicts Ch6, which reports WMAPE + median APE across eight benchmarks | `ch3:§3.5 SRQ1` |
| S3 | Prediction intervals attributed to **Kuleshov et al. (2018)** — the same conformal error just corrected in Ch2. The artefact serves **split conformal** (Lei et al., 2018) | `ch3:§3.5 SRQ2` |
| S4 | "inverse-MAPE weighting in the spirit of **Ahrens et al. (2024)**" — year is 2025, and Ahrens uses constrained least squares, not inverse-variance/inverse-MAPE | `ch3:§3.5 SRQ2` |
| S5 | **LLM-as-judge protocol is specified here** but was dropped (B-DEC-2); every SRQ4 metric is programmatic | `ch3:§3.5 SRQ4` — this is P0040 task 22 |
| S6 | **E2B** named as the sandbox; Scenario B now uses OpenAI's hosted Code Interpreter | `ch3:§3.5 SRQ4` |
| S7 | "approximately fifty decision-support prompts" — confirm against the actual scenario harness before it becomes a claim | `ch3:§3.5 SRQ4` |
| S8 | Two-scenario framing (A vs B) predates the five-scenario ladder A_plain → E_prometheus_model | `ch3:§3.3`, `§3.5` |
| S9 | "brand-times-retailer granularity" contradicts DEC-GRAIN (brand × month); the chain grain was removed by P0035 | `ch3:§3.3` |
| S10 | Saunders' research onion is marked "parked for application at writing time" in the Ch3 header — this brief is the trigger to apply it | `ch3:5` |

---

## PRIORITY ORDER

1. **MR-01, MR-02, MR-03** — the three structural labels. If any is wrong, the fix is
   architectural, not a sentence edit.
2. **Part 4** — the coherence read. This is the highest-value output of the whole run.
3. **MR-12, MR-13, MR-14** — Ch4's framework spine.
4. **MR-07, MR-08** — the missing onion layers, which an examiner will look for.
5. Everything else.
