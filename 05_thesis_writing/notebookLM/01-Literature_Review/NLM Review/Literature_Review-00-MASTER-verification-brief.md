---
name: literature-review-verification-brief
description: NotebookLM briefing pack — every claim Ch1/Ch2 attribute to a downloaded paper, quoted verbatim, with the falsification test for each. Upload with the Section_A–F PDFs.
created: 2026_08_24-10_00
updated: 2026_08_25-00_00
---

# Literature Review — Source Verification Brief

> **✅ COMPLETED 2026-08-25.** NotebookLM has run this brief and returned five reports,
> filed alongside this file as `Literature_Review-Section_{A,B,C,D,F}-*.md`. **All findings
> have been applied to `ch1-introduction.md` and `ch2-literature-review.md`.** This document
> is retained as the record of what was asked; the reports are the record of what was found.
>
> **Five claims came back Contradicted**, each corrected in the chapters:
>
> | ID | Claim | What the source actually says |
> |---|---|---|
> | LR-02 | Ceran et al. use a ≤15% MAPE benchmark | They *reject* MAPE (zero-inflation) and use WRMSSE. **No 15% benchmark exists.** The thesis-wide accuracy target was withdrawn as a result — see Ch6 §6.4.3 |
> | LR-04b | M4 supports simple-beats-complex on irregular series | M4 **excluded** intermittent and low-volume series. The claim now rests on M5 |
> | LR-13 | Goodwin et al.: intervals reduce newsvendor cost | The opposite — intervals did **not** improve decisions (p=0.330) and degraded response to asymmetric loss (83.8% → 44.1%). §2.3 rebuilt around the real finding, which is a *stronger* argument for the thesis |
> | LR-27 | ANAH classifies "entity substitution, numerical imprecision, unsupported causal attribution" | Fabricated categories. The real taxonomy is No Hallucination / Contradictory / Unverifiable / No Fact |
> | LR-32 | Levi et al. validate isotonic calibration on LightGBM and XGBoost | They evaluate **only** neural networks (MLP, DenseNet). Never touch tree models |
>
> **LR-01b confirmed the fabrication.** "Bürger & Pauli (2024)" does not exist — the title
> belongs to González-Potes et al. (2026), and the Obsidian note's quoted findings were
> invented. Purged from `project-overview.md`, `gap_analysis_v4.md`, and the Obsidian note
> (replaced with a warning stub, since wikilinks point at it).
>
> **LR-31 exposed a gap the brief had not anticipated:** Kuleshov et al. is CDF recalibration,
> *not* conformal prediction — so Ch2 had no conformal literature at all while the artefact
> serves split-conformal intervals. §2.5 now carries that strand (Lei et al., 2018; Barber
> et al., 2023).
>
> **Eleven in-text citations** were corrected for authorship or year. Reference-list entries
> were updated provisionally and will regenerate from Zotero on refresh.

**For NotebookLM.** Upload the PDFs in `Section_A` through `Section_F`, then work through
this document. Every claim below is quoted from the thesis chapters as they stand on
2026-08-24, with a line reference to the source file.

Built by reading `ch1-introduction.md` and `ch2-literature-review.md` line by line — not
from an earlier summary. Where this document disagrees with the previous audit files, this
one is correct.

---

## YOUR TASK

For each claim, return a verdict in this exact form:

```
### LR-XX — <short title>
* **Source:** <paper>
* **Thesis claim:** <the quoted claim>
* **Verdict:** Supported | Partially Supported | Contradicted | Not Addressed | Cannot Verify
* **Grounded analysis:** <evidence, with page/section numbers and verbatim quotes>
* **Safest re-wording:** <if not fully Supported, the strongest claim the source DOES support>
```

Match the depth of `05_thesis_writing/notebookLM/02-Modelling Review/Modelling_Review-Section_A-conformal_prediction_verifi.md`.

**Four rules.**

1. **Quote, do not paraphrase.** A verdict of Supported needs a verbatim quotation with a page number.
2. **"Not Addressed" is a valid and useful verdict.** If the paper simply does not discuss the thing, say so — do not stretch a nearby passage to fit.
3. **Check bibliographic metadata too** — authors, year, venue, volume, pages, DOI. Several are already known wrong (see Part 4). Report every discrepancy.
4. **Attributions of the form "the authors explicitly note X" are the highest-risk claims in this document.** They assert the authors *stated* something. If the paper merely implies it, or if it is the thesis author's inference, that is a **Contradicted** verdict on the attribution even when X is true. Two such claims are marked ⚠️ ATTRIBUTION below.

**Do not attempt** to verify anything about the thesis's own results, data, or code. Nothing here requires that; every question is answerable from the PDFs alone.

---

# PART 1 — CRITICAL

Three items where a wrong answer changes the thesis argument rather than a sentence.

---

## ⚠️ LR-01 — A FABRICATED CITATION AND TWO INCOMPATIBLE SETS OF NUMBERS

**This is the most serious item in the document. Do it first.**

**Source:** `Section_E/Gonzáles_Potes_et_al-2026-Hybrid_AI_and_LLM_Enabled_Agent_Based_Real_Time_Decision_Support_Architecture_for_Industrial_Batch_Processes.pdf`

### Background — already resolved, given here so you are not misled

The repo contains a note (`01_thesis_research/literature/obisdian_paper_analysis/hybrid_ai_llm_industrial.md`) citing:

> Bürger, F., & Pauli, J. (et al.) (2024). Hybrid AI and LLM-Enabled Agent-Based Real-Time Decision Support Architecture for Industrial Batch Processes. *Engineering Applications of Artificial Intelligence*.

**That paper does not exist.** Its title is word-for-word identical to González-Potes et al. (2026), and no search located it. It is an invented author/venue pair attached to a real paper's title. **Ignore it.** González-Potes is the real source and is the PDF supplied.

### The actual problem

The non-existent paper's note carries **quantitative findings, presented as a direct quotation**, that differ completely from what Ch1 attributes to González-Potes:

| Attributed to | Numbers |
|---|---|
| "Bürger & Pauli" note, **as a verbatim quote** | CIP process duration **reduced 12–18%**; chemical consumption **down up to 20%**; **100% regulatory compliance** |
| `ch1-introduction.md:18`, on González-Potes | specification compliance **above 98%**; median LLM numerical error **below 3%** |

One real paper; two mutually exclusive quantitative profiles; one of them inside quotation marks. **At least one is fabricated.**

### VERIFY

**LR-01a — the Ch1 numbers.** Does the paper report **specification compliance above 98%** and **median LLM numerical error below 3%**? Quote the exact figures, with page and table number. If the real figures differ, give them.

**LR-01b — the quoted numbers.** Does the paper report **12–18% CIP duration reduction**, **up to 20% chemical consumption reduction**, **100% regulatory compliance**? Does the sentence *"The system reduces CIP process duration by 12–18% and chemical consumption by up to 20% relative to experienced human operators, while achieving 100% regulatory compliance"* appear anywhere, verbatim or near-verbatim? **A No here means a fabricated quotation, which must be purged from the repo.**

**LR-01c ⚠️ ATTRIBUTION — the load-bearing sentence in the whole thesis.** `ch2-literature-review.md:109` states:

> "the authors **explicitly note** that it does not address predictive forecasting over historical tabular data or the resource constraints of small-to-medium enterprise deployments."

The novelty claim rests on this. Do the authors **state this themselves** — in limitations, future work, or scope? Quote it with a page number. **If they do not say it, this is Contradicted regardless of whether the observation is true**, and must be re-worded to "the paper does not address…".

**LR-01d — is it really the closest precedent?** Confirm the domain (industrial batch process / dairy CIP), that forecasting over historical tabular data is absent, and that no SME resource constraint is considered.

**LR-01e — architecture.** Ch1 and Ch2 both claim it "carefully separates deterministic and generative components." Confirm, and describe the actual layer structure.

---

## ⚠️ LR-02 — WHICH METRIC IS CERAN'S 15%?

**Source:** `Section_A/Ceran_et_al-2024-...FULL_BOOK.pdf` — a full proceedings volume. The chapter is **LNNS Vol. 1090, chapter 11**, DOI `10.1007/978-3-031-67192-0_11`. **Locate that chapter; ignore the rest of the book.**

**Thesis claim** (`ch2-literature-review.md:31`, verbatim):

> "Ceran et al. (2024), working with a large grocery retailer, identify LightGBM as achieving strong accuracy at a low memory footprint in a real retail setting, and use **a MAPE of fifteen percent or below as a practical benchmark** for acceptable demand forecasting in their retail setting."

This 15% figure is the thesis's headline accuracy target, used in Ch1, Ch6 and Ch10. **The thesis reports WMAPE and median APE, which disagree by roughly a factor of two** — so depending on the answer, the target is met on half the categories or on none.

**VERIFY**

1. **Which metric is the 15%?** Plain MAPE, median MAPE, weighted MAPE/WMAPE, sMAPE, something else? **Quote the definition verbatim, with the formula if given.** This single fact decides whether a headline target is met or missed.
2. **At what aggregation level** — per SKU, per category, per store, or pooled? A 15% pooled figure and a 15% per-SKU figure are different targets.
3. **Is 15% their own result, or a benchmark they cite from elsewhere?** If cited, **name the original source — that is what the thesis should cite instead.**
4. **What horizon and grain?** (Thesis: H=3, brand × month.) A daily or weekly SKU-level benchmark is not comparable.
5. **Do they handle zero actuals?** If their panel has no zeros, plain MAPE is well-defined for them and undefined for the thesis — making the metric non-transferable regardless of (1).
6. **Separately confirm the memory claim:** do they report LightGBM's *memory footprint*, or is "low memory" an inference? Give the figure if present.

---

## ⚠️ LR-03 — DOES M5 SUPPORT WHAT CH1 SAYS, OR ONLY WHAT CH2 SAYS?

**Source:** `Section_A/Makridakis_et_al-2022-M5_Accuracy_Competition...pdf`

**The two chapters make different claims about the same competition, and Ch1's is far stronger:**

| Where | Claim |
|---|---|
| `ch1-introduction.md:14` | "**all top 50** performing submissions used LightGBM … achieving **more than 14% improvement** over the best statistical benchmark" |
| `ch2-literature-review.md:29` | "**many** top-performing submissions relied heavily on gradient-boosted tree models, including LightGBM" |

**VERIFY**

1. **Is "all top 50" accurate?** Quote the exact statement about method distribution among top performers. If the real figure is "48 of the top 50" or "the majority", give it — this is a precise, checkable, falsifiable number and must be exact.
2. **Is ">14% improvement over the best statistical benchmark"** in the paper? Quote the figure and name the benchmark it improves on.
3. Do submissions using **exogenous promotional and calendar features** outperform those using sales history alone? (Ch1 and Ch2 both claim this.)
4. **Does M5 report a global-versus-local finding** — one model pooled across series versus per-series models? Quote it if so. *(The thesis needs this; it is currently unsourced.)*
5. **Does M5 report that simple benchmarks beat sophisticated methods on irregular/intermittent series?** Quote if present. *(Also needed and unsourced — and possibly in M4 rather than M5; see LR-04.)*

---

# PART 2 — CLAIM BANK BY SECTION

One entry per downloaded paper. Each carries the verbatim thesis claim and its falsification test.

---

## SECTION A — Forecasting substrate (§2.1, §2.2 — SRQ1)

### LR-04 — M4 Competition
**Source:** `Makridakis_et_al-2020-The_M4_Competition...pdf`
**Claim** (`ch2:29`): "The M4 Competition (Makridakis et al., 2020), spanning 100,000 series and 61 methods, established that **combining models tends to outperform any single best model** and that **hybrids of statistical structure and machine learning achieve the highest accuracy**."

**Verify:** (a) both sub-claims, quoted; (b) confirm 100,000 series / 61 methods; (c) **does M4 contain the simple-beats-complex finding?** The thesis needs a source for a simple benchmark outperforming tuned ML on irregular series. **If it is in M4 rather than M5, the thesis is citing the wrong competition — say which.** (d) Ch1 additionally quotes M4 verbatim on exogenous variables as the open frontier: *"One thing that remains to be determined is the possible improvement in PF and PI performances…"* — **confirm this quotation word for word**, since it is presented as a direct quote.

### LR-05 — Ma et al. (2025), beverage forecasting
**Source:** `Ma_et_al-2025-A_Data-Driven_and_Context-Aware_Approach...pdf`
**Claim** (`ch2:31`): "machine learning models enriched with exogenous contextual features can outperform statistical baselines for high-volume, stable SKUs, **with no single model dominating across demand patterns**."
Ch1 strengthens this to "**substantially** outperform" in "a large-scale empirical study of a **private-label beverage manufacturer**."

**Verify:** (a) the no-single-model-dominates claim, quoted; (b) is the setting a private-label beverage manufacturer? (c) is "substantially" supported, or is the effect modest? (d) **do they report a sample-size or data-volume threshold** at which model choice flips? *(The thesis has found one and would extend them — worth knowing if they offer one.)*

### LR-06 — Al-Karkhi & Rzą̧dkowski (2025) — ⚠️ CITED UNDER THE WRONG AUTHORS
**Source:** `to_sort-Initial Papers/2_high/Al_Karkhi_and_Rza̧dkowski-2025-Innovative_machine_learning_approaches...pdf`
**→ MOVE THIS PDF INTO `Section_A` BEFORE UPLOADING.**

The thesis cites this as **"Nguyen, T. T. H., et al. (2025)"** (`ch2:183`) — same title, same journal (*Int. J. Innovation Studies* 9(1)), same year. **The author attribution in the thesis is wrong.**

**Claim** (`ch2:31`): "Nguyen et al. (2025), **reviewing over 120 machine learning papers** in economic forecasting and SME applications, identify **LightGBM and XGBoost as well suited to short-horizon forecasting with limited training observations**."

**Verify:** (a) **the correct author list, year, volume and DOI** — this is a reference-list correction; (b) is it a review of **over 120** papers? (c) the LightGBM/XGBoost claim, quoted; (d) does "limited observations" match ~460–1,800 rows per category over ~44 monthly periods, or do they mean something far larger?

### LR-07 — Ahrens et al., model averaging — ⚠️ YEAR AND VENUE BOTH SUSPECT
**Source:** `Ahrens_et_al-2025-Model_Averaging_and_Double_Machine_Learning.pdf`
**Claim** (`ch2:33`): "stacked averaging, and **inverse-variance weighting in particular**, can improve accuracy over individual learners; this supports combining multiple forecasts rather than relying on a single model."

**Verify:** (a) **Year: filename says 2025, thesis cites 2024 — which is correct?** (b) **Venue: thesis says *Journal of Applied Econometrics* but gives an arXiv DOI (`10.48550/arXiv.2401.01645`).** Determine whether the supplied PDF is the preprint or the published article, and give the correct full citation. (c) Is **inverse-variance weighting** singled out as claimed? (d) **Is the setting forecasting at all, or causal inference / double ML?** If the latter, the thesis is extending an econometrics result into forecasting without warrant — say so.

### LR-08 — Klee & Xia (2025), forecast stability
**Source:** `Klee_and_Xia-2025-Measuring_Time_Series_Forecast_Stability...pdf`
**Claim** (`ch2:33`): "defining stability as the **coefficient of variation of forecasts under nominally identical inputs** and finding evidence that **tree ensembles can be more stable than classical statistical models under promotional conditions**."

**Verify:** (a) **the exact definition of stability, quoted with its formula** — the thesis has implemented CV-across-seeds on this basis, so the definition must match; (b) is stability measured across *seeds*, across *retrainings*, or across *data vintages*? **These are different things and it matters.** (c) the tree-vs-classical claim; (d) **peer-review status: is this still a KDD '25 workshop preprint, or has it been published?**

### LR-09 — Ng (2017), scanner data and memory
**Source:** `Ng-2017-Opportunities_and_Challenges...pdf`
**Claim** (`ch2:39`): "analysing **four terabytes** of Nielsen scanner data, showed that **memory can become the primary binding constraint** … at the full panel scale, in-memory analysis becomes infeasible."
Ch2 then draws a careful distinction: Ng's is a *raw-data-volume* constraint; the thesis's is a *deployment-cost* constraint.

**Verify:** (a) is it four terabytes of Nielsen scanner data? (b) does Ng identify memory as the *primary binding* constraint, or one of several? (c) **Is the thesis's reading fair to Ng?** Ch2 uses Ng to license a memory budget as "a legitimate, domain-grounded design variable" while conceding the constraint operates at a different scale. **Is that a reasonable use of the paper, or does it overreach?** Answer directly.

---

## SECTION B — Decision support and forecast-to-decision (§2.3)

### LR-10 — Elmachtoub & Grigas (2022), SPO
**Source:** `Elmachtoub_and_Grigas-2022-Smart_Predict_Then_Optimize.pdf`
**Claim** (`ch2:53`): "minimising prediction error is **not equivalent to** maximising decision quality: a prediction with small statistical error can yield a poor decision, while a less accurate prediction aligned with the decision boundary can yield a near-optimal one. They formalise a **decision-aware loss and a tractable convex surrogate**."
**Verify:** both halves; name the surrogate (SPO+?) and confirm convexity/tractability as stated.

### LR-11 — Mandi et al. (2024), decision-focused learning
**Source:** `Mandi_et_al-2024-Decision-Focused_Learning...pdf`
**Claim** (`ch2:53`): "**zero prediction loss implies zero decision loss but not the converse**, and that **no single method dominates** across decision problems."
**Verify:** the asymmetry **exactly as worded** — it is quoted precisely and the direction of implication must be right. Also confirm *JAIR* 81, 1623–1701.

### LR-12 — Pathirannehelage et al. (2025) — ⚠️ CITED AS "Herath et al. (2024)"
**Source:** `Pathirannehelage_et_al-2025-Design_Principles_for_Artificial_Intelligence-Augmented_Decision_Making...pdf`
The thesis cites this as **"Herath, S., Shrestha, Y. R., & von Krogh, G. (2024)"**, *EJIS* 34(2), 207–229. **Filename says Pathirannehelage et al., 2025.**

**Claim** (`ch2:57`): "through **action design research across three organisations**, derive a design principle of direct relevance: **AI decision-support systems must communicate uncertainty to be trusted by non-technical business users**."

**Verify:** (a) **the correct first author, full author list and year** — a reference-list correction; (b) is it action design research across **three** organisations? (c) **the uncertainty-communication principle, quoted** — this is load-bearing for SRQ2; (d) confirm *EJIS* volume/issue/pages.

### LR-13 — Goodwin et al. (2010), prediction intervals
**Source:** `Goodwin_et_al-2010-Do_Forecasts_Expressed_as_Prediction_Intervals...pdf`
**Claim** (`ch2:57`): "demonstrate experimentally that forecasts expressed as prediction intervals **reduce newsvendor cost** relative to point forecasts, **with the benefit concentrated among high-uncertainty items**."

**Verify:** (a) **Is the finding positive, negative, or mixed?** The title is a question, and the thesis reports it as a clean positive. **If the result was null or conditional, that is a significant misreport — say so plainly.** (b) is the benefit really concentrated among high-uncertainty items? (c) is the cost measure a newsvendor cost?

### LR-14 — Rinaldi et al. (2025), DSS4EX
**Source:** `Rinaldi_et_al-2025-DSS4EX...pdf`
**Claim** (`ch2:57`): "wraps time-series forecasting pipelines in an explainability layer generating natural-language explanations; their evaluation indicates that **explanatory layers can improve perceived decision quality** relative to raw model outputs."

**Verify:** (a) the perceived-decision-quality finding — **was it measured, or asserted?** (b) **CRITICAL, near-neighbour to the gap claim:** does DSS4EX expose forecasts to an **LLM agent** through a **structured tool interface**? Does it address **uncertainty**? Does it operate under **resource constraints**? **If it does all three, the thesis's novelty claim is materially weakened — say so directly.**

### LR-15 — Olszak & Bartuś (2025), AI-enhanced BI
**Source:** `Olszak_and_Bartus-2025-AI-Enhanced_Business_Intelligence...pdf`
**Claim** (`ch2:57`): "AI-enhanced business intelligence **can increase decision confidence and forecast-adoption when predictions are accompanied by explanations**."
**Verify:** (a) the claim, and whether it is **empirical or conceptual** — the thesis's hedge ("suggest") implies weak evidence; confirm which; (b) *Procedia CS* is a proceedings series — note the review rigour.

### LR-16 — Zheng et al. (2025), LLMs in supply chain
**Source:** `Zheng_et_al-2025-LLMs_in_Supply_Chain_Management...pdf`
**Claim** (`ch2:113`): "document the integration of large language models into enterprise supply-chain workflows, illustrating both the **appetite for** and the **practical friction of** embedding LLM capabilities into established operational systems."
**Verify:** both halves; is it a case study, and in what industry? Does it involve forecasting?

---

## SECTION C — LLM agents and tool use (§2.4)

### LR-17 — Schick et al. (2023), Toolformer
**Source:** `Schick_et_al-2023-toolformer...pdf`
**Claim** (`ch2:71`): "a **6.7-billion-parameter** Toolformer can outperform a far larger model on downstream reasoning tasks. The implication … is that **tool delegation can partially compensate for model scale**."
**Verify:** (a) the 6.7B figure and which larger model it beat (GPT-3 175B?), on which benchmarks; (b) **the substitute-for-scale claim does real work in the gap argument** — is it the authors' framing or the thesis's extrapolation? (c) confirm NeurIPS 36 (2023).

### LR-18 — Wang, X. et al. (2024), CodeAct
**Source:** `Wang_et_al-2024-Executable_Code_Actions_Elicit_Better_LLM_Agents.pdf`
**Claim** (`ch2:73`): "executable code **can offer advantages over JSON-formatted tool calls on some agentic benchmarks**, enabling **dynamic tool composition and self-debugging**."
**Verify:** (a) the code-vs-JSON comparison — quote the magnitude and say on which benchmarks it holds **and where it does not**; (b) both mechanisms. **This is the thesis's baseline comparator (scenario B), so the characterisation must be exact.**

### LR-19 — Chen & Bibi (2026), MLAT — ⚠️ CRITICAL FOR GAP G3
**Source:** `Chen_and_Bibi-2026-Machine_Learning_as_a_Tool...pdf`
**Claim** (`ch2:120`): "an emerging strand begins to expose pre-trained statistical models as callable agent tools (Chen & Bibi, 2026); the latter, however, **exists only as small, non-peer-reviewed proofs of concept and does not address forecasting, reliability, or production constraints**."

**Verify — this is a dismissal, and dismissals are where gap claims break:**
1. Is it a **small proof of concept**, or a developed framework? Describe scale and evaluation.
2. Does it address **forecasting**? (Any time-series case?)
3. Does it address **reliability** or **uncertainty quantification**?
4. Does it address **production or resource constraints**?
5. **Peer-review status — published since?**

**Any Yes weakens gap G3. Report every Yes explicitly and prominently.**

### LR-20 — Ma, M. et al. (2024), SciAgent
**Source:** `Ma_et_al-2024-SciAgent...pdf`
**Claim** (`ch2:71`): "equipping an LLM with domain-specific tools for computation and retrieval **substantially improves precision-sensitive reasoning over a tool-free baseline**."
**Verify:** the claim and the magnitude of "substantially."

### LR-21 — Paranjape et al. (2023), ART
**Source:** `Paranjape_et_al-2023-ART...pdf`
**Claim** (`ch2:71`): "automatically decomposing a task into structured reasoning-and-tool-use steps can improve **task performance and controllability** relative to single-shot prompting."
**Verify:** both; **published since 2023?**

### LR-22 — Sapkota et al., AI Agents vs Agentic AI — ⚠️ YEAR SUSPECT
**Source:** `Sapkota_et_al-2026-AI_Agents_vs_Agentic_AI...pdf` — **filename 2026, thesis cites 2025.**
**Claim** (`ch2:75`): distinguishes "**AI Agents**, defined as modular, task-specific systems driven by a single LLM with tool use, from **Agentic AI**, characterised by multi-agent collaboration, persistent memory, and coordinated autonomy."
Ch1:18 uses a *different* wording: "systems of multiple specialised agents that coordinate, communicate, and dynamically allocate sub-tasks to achieve a common goal."

**Verify:** (a) **year, volume, article number** — *Information Fusion* 126, art. 103599; (b) **both definitions quoted verbatim** — the thesis uses this taxonomy to bound its own contribution, so the wording must be exact; (c) **do Ch1 and Ch2 describe the same construct?** Flag the divergence if not.

### LR-23 to LR-26 — Multi-agent orchestration (⚠️ THREE WRONG AUTHOR ATTRIBUTIONS)

These four are cited together (`ch2:75`) as design context, explicitly **not** part of the artefact. Verification need is **low for content, high for metadata.**

| ID | PDF (authoritative) | Thesis cites as | Claim |
|---|---|---|---|
| LR-23 | `Liu_et_al-2024-A_Dynamic_LLM_Powered_Agent_Network` | Liu, Z., et al. (**2023**), DyLAN | "dynamically activating specialist agents can outperform fixed pipelines" |
| LR-24 | `Li_et_al-2024-AutoFlow` | **Chen, Z.**, et al. (2024) ⚠️ | "structured, graph-based orchestration can be generated and optimised automatically" |
| LR-25 | `Wang_et_al-2025-ScoreFlow` | **Wu, Y.**, et al. (2025) ⚠️ | as above |
| LR-26 | `Guo_et_al-2025-Sample_Predict_then_Proceed` | **Huang, J.**, et al. (2024) ⚠️ | "self-verification sampling, in which an agent evaluates candidate outputs before committing to a tool call" |

**For each:** confirm the **correct first author and year** (filenames are authoritative — treat the thesis attribution as the error), verify the one-line claim, and report whether it has been **published since**. For LR-26 specifically: it was cited from OpenReview — **was it accepted or rejected?** A rejected paper should be reconsidered.

Ch2 also claims graph-based orchestration "**reflects best practice for multi-agent systems**." **That is a normative claim — do LR-24/LR-25 actually support it, or is it the thesis's own editorialising?**

---

## SECTION D — Reliability, uncertainty, evaluation (§2.5 — SRQ2, SRQ4)

### LR-27 — Ji et al. (2024), ANAH
**Source:** `Ji_et_al-2024-ANAH...pdf`
**Claim** (`ch2:87`): "establish a systematic taxonomy of LLM hallucination … classifying factual errors into identifiable patterns including **entity substitution, numerical imprecision, and unsupported causal attribution**."
**Verify:** are those **three named categories** actually in the taxonomy, with those names or clear equivalents? **"Numerical imprecision" matters most** — the thesis uses it to motivate validating numeric forecasts. If ANAH's categories differ, give the real list.

### LR-28 — Wang, R. et al. (2026), AgentNoiseBench
**Source:** `Wang_et_al-2026-AgentNoiseBench...pdf`
**Claim** (`ch2:87`): "tool-using agents **degrade systematically** when tool inputs contain structured noise such as **mislabelled features or formatting inconsistencies**."
**Verify:** the degradation claim and whether those specific noise types are tested. Note peer-review status (very recent).

### LR-29 — Kartik et al. (2025), AgentCompass — ⚠️ CITED AS "Sapra et al."
**Source:** `Kartik_et_al-2025-AgentCompass...pdf` — thesis cites **"Sapra, K. N., Sapra, G., Hada, R., & Pareek, N. (2025)"**.
**Claim** (`ch2:89`): "highlight **non-trivial step-level errors** in unstructured agentic workflows and find that **structured traceability mechanisms materially reduce debugging effort** when failures occur."
**Verify:** (a) **the correct author list** — reference-list correction; (b) both claims; (c) **is the debugging-effort reduction measured or asserted?** "Materially reduce" implies measurement. (d) Published since?

### LR-30 — Dong et al., AgentOps — ⚠️ YEAR SUSPECT
**Source:** `Dong_et_al-2024-AgentOps...pdf` — **filename 2024, thesis cites 2025.**
**Claim** (`ch2:89`, `ch2:111`): "specifying the artifacts — namely **execution traces, tool-call spans, prompt and guardrail registries** — that must be captured for a foundation-model agent to be auditable," positioning traceability "as relevant to emerging **compliance and auditability** expectations."
**Verify:** (a) **year**; (b) **the artifact list, quoted** — load-bearing for SRQ3's readiness criteria, so the taxonomy must be reproduced accurately; (c) do they connect it to compliance/regulatory expectations, or is that the thesis's extension? (d) Published since?

### LR-31 — Kuleshov et al. (2018), calibrated regression
**Source:** `Kuleshov_et_al-2018-Accurate_Uncertainties...pdf`
**Claim** (`ch2:91`): "**post-hoc isotonic-regression calibration** can align empirical interval coverage with stated coverage probabilities."
**Verify:** (a) the isotonic-regression method and the coverage-alignment result; (b) **CRITICAL — does this paper cover conformal prediction at all?** The thesis's artefact serves **split-conformal** intervals, and this is the closest thing Ch2 currently offers. **The two are different methods.** If Kuleshov et al. do not cover conformal prediction, confirm it plainly — it establishes that the thesis has **no source for the method it actually uses** (see Part 3). (c) Is the setting deep learning specifically, or general regression?

### LR-32 — Levi et al. (2022), calibration in regression
**Source:** `Levi_et_al-2022-Evaluating_and_Calibrating_Uncertainty...pdf`
**Claim** (`ch2:91`): "confirm isotonic regression as a **consistently effective calibration method across datasets and model families, including gradient-boosted trees such as LightGBM and XGBoost**."
**Verify:** (a) the general claim; (b) **are LightGBM and XGBoost actually among the evaluated model families?** The thesis names them specifically. **If the paper only evaluates neural networks, this is a misattribution** — say so.

### LR-33 — Mehta (2025), CLEAR — ⚠️ LOAD-BEARING PREPRINT
**Source:** `Mehta-2025-Beyond_Accuracy...pdf`
**Claim** (`ch2:93`, `ch2:111`): CLEAR proposes evaluating enterprise agentic systems across "**cost, latency, efficacy, assurance, and reliability**," reporting "preliminary evidence that **multidimensional evaluation may correlate more strongly with deployment readiness than accuracy-only evaluation**" and that "**single-run success can overstate reliability relative to multi-run consistency**."

**Verify:** (a) **do the five CLEAR dimensions match those names exactly?** SRQ4's metric design maps onto them. (b) Is the correlation-with-deployment-readiness claim **empirically supported**, and at what scale? The thesis hedges with "preliminary" — confirm how preliminary. (c) The single-run-overstates-reliability claim. (d) **Peer-reviewed since? A preprint carrying the thesis's entire evaluation framework is a structural weak point.**

### LR-34 / LR-35 — LLM-as-a-Judge (⚠️ CONDITIONAL — MAY BE OUT OF SCOPE)
**Sources:** `Gu_et_al-2024-A_Survey_on_LLM-as-a-Judge.pdf`, `Ye_et_al-2024-Justice_or_Prejudice...pdf`

**The LLM judge was dropped from the thesis design (decision B-DEC-2).** But Ch2 still cites both, and §2.5 still describes an evaluation using "a separate judge model with bias awareness."

**Verify only if time permits, in this order:**
1. **Gu et al.:** "pairwise comparison tends to be more consistent than absolute scoring"; judge reliability depends on "consistency, robustness, and alignment with human judgment."
2. **Ye et al.:** "position and self-enhancement bias"; the recommendation to "use a separate model for evaluation together with explicit bias checks." **Also: peer-review status — Ch2 flags this one as uncertain and asks for verification.**

**Note for the thesis, not for NotebookLM:** if the judge is dropped, §2.5's evaluation sentence describes a design that no longer exists and must be rewritten. These two citations survive only if repurposed to justify *not* using a judge.

---

## SECTION F — Methodology (§2.8)

### LR-36 — Hevner et al. (2004)
**Source:** `Hevner_et_al-2004-Design_Science_in_Information_Systems_Research.pdf`
**Claim** (`ch2:135`): "distinguishing the construction of a working artefact from the behavioural study of existing systems, and articulating guidelines that require an artefact to be **both demonstrably useful in a relevant problem context and a source of generalisable knowledge** beyond its specific instantiation."
**Verify:** the design-vs-behavioural distinction and the dual usefulness/generalisability requirement. Low risk; confirm *MISQ* 28(1), 75–105.

### LR-37 — Peffers et al. (2007)
**Source:** `Peffers_et_al-2007-A_Design_Science_Research_Methodology...pdf`
**Claim** (`ch2:135`): the six-step process — "**problem identification, objective definition, design and development, demonstration, evaluation, and communication**."
**Verify:** **are these the six steps, in this order, with these names?** The thesis structures its chapters on them. Confirm *JMIS* 24(3), 45–77.

---

# PART 3 — WHAT CANNOT BE VERIFIED IN THIS BATCH

Not oversights. Recorded so they are not silently lost.

## 3a. Cited in Ch2 but NOT downloaded — a second download round is needed

Found by reading Ch2's reference list; **absent from the earlier plan files entirely**:

| Source | Cited for | §  |
|---|---|---|
| **Liu, S., Guo, B., Yu, Z., et al. (2025).** On accelerating edge AI. arXiv 2501.15014 [PRE] | quantisation/distillation preserve accuracy at reduced memory | 2.2 |
| **Semerikov et al. (2025).** Edge intelligence unleashed. *J. Edge Computing* 4(2) | compressed LLMs still need 1–4 GB | 2.2 |
| **Ouyang et al. (2025).** LLM code non-determinism | ½–¾ of code-gen tasks yield no two identical outputs | 2.5 |
| **Atıl et al. (2025).** Non-determinism at temperature zero | persists at temp 0; agreement-rate metrics | 2.5 |
| **Schwartz et al. (2020).** Green AI | computational cost as a first-class criterion | 2.5 |
| **Chen et al. (2024).** Inference cost | order-of-magnitude cost differences across LLMs | 2.5 |
| **Saunders, Lewis & Thornhill (2023).** *Research Methods for Business Students* (9th ed.) | narrative vs systematic review justification | 2.0 |

**Ouyang and Atıl matter most** — they carry SRQ4's *consistency* dimension, a primary evaluation metric, and both are preprints.

## 3b. Methods used but cited nowhere

Used by the thesis; absent from every chapter's references. **These need finding, not verifying.**

| Method used | Candidate source |
|---|---|
| TPE sampler | Bergstra, Bardenet, Bengio & Kégl (2011), NeurIPS |
| Random > grid search | Bergstra & Bengio (2012), *JMLR* 13 |
| Optuna | Akiba et al. (2019), KDD |
| Rolling-origin CV | Hyndman & Athanasopoulos *FPP3* §5.10; Tashman (2000) |
| Model-selection optimism | Cawley & Talbot (2010), *JMLR* |
| Ridge as tabular baseline | Hastie, Tibshirani & Friedman, *ESL* ch. 3 |
| SHAP | Lundberg & Lee (2017), NeurIPS |
| Prophet's design regime | Taylor & Letham (2018) |
| Simple benchmarks as standard | Hyndman & Athanasopoulos *FPP3* §5.2 |
| Intermittent demand | Croston (1972); Syntetos & Boylan (2005) |
| Forecast accuracy metrics | Hyndman & Koehler (2006), *IJF* 22(4) |
| Global vs local models | Montero-Manso & Hyndman (2021), *IJF* |
| **Conformal prediction** | **Lei et al. (2018); Barber et al. (2023) — already verified in the Modelling Review, Section A** |

## 3c. Two literature gaps needing new Ch2 subsections

1. **Conformal prediction is not reviewed anywhere in Ch2**, yet every served forecast carries a split-conformal interval and SRQ2's uncertainty claim depends on it entirely. The sources are already verified (Modelling Review Section A) — **they need writing into Ch2, not researching.**
2. **Forecast-accuracy metrics are not reviewed at all**, yet WMAPE is the headline metric and the WMAPE-vs-medMAPE disagreement (up to 20pp) is a recurring finding.

## 3d. Optional — leftover PDFs, reconsider for inclusion

Not cited in any chapter. Most trace to the abandoned multi-agent/MCDM framing and are correctly dropped: `Abdulla & Baryannis` (supplier selection), `Colelough & Regli` (neuro-symbolic), `Avramova` (MCDM), `Chen ACGraph`, `Nava Martinez` (heart-attack prediction).

**Four are worth a second look, because each would strengthen a currently weak spot:**

| PDF | Why reconsider |
|---|---|
| `Raj_et_al-2023-Measuring_Reliability_of_LLMs_through_Semantic_Consistency` | §2.5's consistency dimension rests on **two preprints** (Ouyang, Atıl). A 2023 peer-reviewed consistency paper would materially strengthen it. |
| `Gabellini_et_al-2025-...cost_aware_custom_loss...3PL_supply_chain_forecasting` | Peer-reviewed, supply-chain, decision-aware loss — a domain-closer anchor for §2.3 than SPO/DFL alone. |
| `UNSURE/Mehdiyev_et_al-2024-Quantifying_and_explaining_ML_uncertainty...` | §2.5 has no uncertainty-quantification source matching the method actually used. |
| `UNSURE/Sharma-2024-Unlocking_Business_Potential_in_FMCG_with_Predictive_Analytics` | Direct domain match (FMCG predictive analytics); check quality before adopting. |

---

# PART 4 — BIBLIOGRAPHIC CORRECTIONS ALREADY IDENTIFIED

From filename metadata (authoritative — the PDFs were retrieved from publisher pages via Zotero). **Confirm each from the PDF itself and return a corrected reference list.**

| # | Thesis cites | Filename says | Nature |
|---|---|---|---|
| LR-06 | Nguyen, T. T. H., et al. (2025) | **Al-Karkhi & Rzą̧dkowski (2025)** | wrong authors |
| LR-07 | Ahrens et al. (**2024**), *J. Applied Econometrics* + arXiv DOI | **2025** | wrong year; venue/DOI mismatch |
| LR-12 | Herath, Shrestha & von Krogh (**2024**) | **Pathirannehelage et al. (2025)** | wrong authors + year |
| LR-22 | Sapkota et al. (**2025**) | **2026** | wrong year |
| LR-23 | Liu, Z., et al. (**2023**) | **2024** | wrong year |
| LR-24 | **Chen, Z.**, et al. (2024), AutoFlow | **Li et al. (2024)** | wrong authors |
| LR-25 | **Wu, Y.**, et al. (2025), ScoreFlow | **Wang et al. (2025)** | wrong authors |
| LR-26 | **Huang, J.**, et al. (2024) | **Guo et al. (2025)** | wrong authors + year |
| LR-29 | **Sapra et al.** (2025), AgentCompass | **Kartik et al. (2025)** | wrong authors |
| LR-30 | Dong et al. (**2025**), AgentOps | **2024** | wrong year |

**Ten of ~40 references carry an error.** In-text citations are what matter first (Zotero regenerates the reference list on refresh), so the fixes are: `(Nguyen et al., 2025)` → `(Al-Karkhi & Rzą̧dkowski, 2025)`, `(Herath et al., 2024)` → `(Pathirannehelage et al., 2025)`, `(Chen et al., 2024, AutoFlow)` → `(Li et al., 2024)`, `(Wu et al., 2025, ScoreFlow)` → `(Wang et al., 2025)`, `(Huang et al., 2024)` → `(Guo et al., 2025)`, `(Sapra et al., 2025)` → `(Kartik et al., 2025)`, plus four year corrections.

---

# PART 5 — REPO FIXES (NOT NOTEBOOKLM TASKS)

Found while reading the chapters. Listed for tracking; **none has been actioned.**

| # | Issue | Location |
|---|---|---|
| R1 | **Bürger & Pauli (2024) is a fabricated citation.** Correct to González-Potes et al. (2026). | `00_thesis_context/thesis-topic/2026_08_22-19_00-project-overview.md:54`; `01_thesis_research/literature/gap_analysis_v4.md:37` |
| R2 | **The Obsidian note carries an apparently fabricated verbatim quote** (12–18% CIP, 20% chemical, 100% compliance) under fabricated authorship. Add a warning header or delete — **do not cite from it** pending LR-01b. | `01_thesis_research/literature/obisdian_paper_analysis/hybrid_ai_llm_industrial.md` |
| R3 | **"the five beverage categories"** — there are four. Two occurrences. | `ch1-introduction.md:42` |
| R4 | **Unresolved `[CITATION TO ADD: cloud-instance pricing source]`** — and Ch2's banner claims "0 CITATION NEEDED flags remain," which is false across the pair. | `ch1-introduction.md:16` |
| R5 | **Ch1 and Ch2 disagree on M5.** Ch1: "all top 50 … >14% improvement." Ch2: "many top-performing." Reconcile to whatever LR-03 establishes. | `ch1:14` vs `ch2:29` |
| R6 | **Ch2 §2.5 still describes an evaluation using "a separate judge model with bias awareness"** — the judge was dropped (B-DEC-2). | `ch2-literature-review.md:93` |
| R7 | **Ch2 claims 39 cited sources; the reference list has 40 entries.** Recount after the corrections above. | `ch2:15`, `ch2:167+` |
| R8 | **Ch2 §2.1 promises the SRQ1 benchmark evaluates "accuracy, computational efficiency, and stability."** Stability has since been measured (`stability.csv`) — Ch2's forward reference is now satisfiable and should point at the result. | `ch2:33` |

---

## Priority order

1. **LR-01** — fabricated citation + contradictory numbers + the "explicitly note" attribution
2. **LR-02** — Ceran's metric (decides a headline target)
3. **LR-03** — M5 "all top 50" and ">14%"
4. **LR-19** — Chen & Bibi / gap G3
5. **LR-14** — DSS4EX as a near-neighbour to the gap claim
6. **LR-13** — Goodwin: is the prediction-interval result actually positive?
7. **LR-33** — CLEAR, carrying SRQ4's evaluation framework
8. **Part 4** — the ten bibliographic corrections (fast, mechanical, high examiner-visibility)
9. Everything else in LR-04 to LR-37
