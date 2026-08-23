---
name: source-list-for-notebooklm
description: Every paper cited in Ch1/Ch2, the specific claim each supports, and what must be verified. Download list for NotebookLM.
created: 2026_08_22-23_00
updated: 2026_08_23-21_00
---

# Source list — download these, and what to check in each

**39 sources cited in Chapter 2, plus the gaps where no source exists at all.**

For each: the claim it is cited for, and the specific thing to verify. A source that
merely "exists" is not verified — the question is always **does it say what we say it
says.**

Legend: **[PP]** peer-reviewed · **[PRE]** preprint, flagged in Ch2 · **[?]** status uncertain

---

## ⚠️ PRIORITY 0 — A CONTRADICTION IN THE MOST LOAD-BEARING CITATION

**The thesis cites two different papers for the same "closest precedent" claim.**

| Where | Cited as |
|-------|----------|
| `ch1-introduction.md` line 18 + refs | **González-Potes, A., et al. (2026).** Hybrid AI and LLM-enabled agent-based real-time decision support architecture for industrial batch processes. *AI*, 7(2), 51. |
| `ch2-literature-review.md` line 109 + refs | **González-Potes et al. (2026)** — same |
| `00_thesis_context/.../project-overview.md` line 54 | **Bürger & Pauli (2024, EAAI)** — *Hybrid AI and LLM-Enabled Agent for Industrial Batch Processes* |
| `01_thesis_research/literature/gap_analysis_v4.md` line 37 | **"González-Potes/Bürger"** — hedged, implying nobody was sure |

Different authors, different years, different journals (*AI* vs *Engineering
Applications of Artificial Intelligence*), same attributed content.

**This is the single most load-bearing citation in the thesis** — the novelty argument
is "the closest published work is this industrial-process paper, and it does not
address forecasting under SME constraints."

**VERIFY FIRST:**
1. Which paper actually exists? Two similar papers, or one misremembering of the other?
2. Whichever is real: does it report **"specification compliance rates above 98% and
   median LLM numerical errors below 3%"** (Ch1 line 18)?
3. Does it **explicitly state** it does not address predictive forecasting over
   historical tabular data, or SME resource constraints? Ch2 line 109 says "the authors
   explicitly note" this — **a strong attribution that must be checked verbatim.**
4. **Has anything closer appeared since?** A newer paper doing this in retail FMCG
   would materially weaken the gap claim.

---

## ⚠️ PRIORITY 1 — WHICH METRIC IS CERAN'S 15%?

**Blocks a headline claim in Ch1, Ch6 (§6.4.3) and Ch10.** Raised 2026-08-23 during
the §6.5 rewrite, when it became clear the answer changes the result in opposite
directions depending on the metric.

**Source:** Ceran, Özkan, Eskiocak, Mert & Yüceoğlu (2024). ML-based demand
forecasting for an FMCG retailer. INFUS 2024, LNNS 1090. Springer. *(= row A3 below.)*

**The claim it is cited for:** "a MAPE of 15% or below as a practical benchmark" —
used throughout this thesis as **the** accuracy target.

**Why it cannot be scored right now.** This thesis reports WMAPE and median APE. The
two disagree by roughly a factor of two, so the target is either half-met or missed
entirely:

| Category | Our WMAPE | Our median APE |
|---|---:|---:|
| CSD | 14.5% ✅ | 33.2% ❌ |
| energidrikke | 13.0% ✅ | 32.3% ❌ |
| danskvand | 20.5% ❌ | 38.6% ❌ |
| RTD | 31.8% ❌ | 38.1% ❌ |

- **If they mean WMAPE** — the thesis meets the target on **2 of 4** categories.
- **If they mean plain or median MAPE** — the thesis meets it on **none**, and every
  sentence claiming the target is approached or met must be rewritten.

**ASK NOTEBOOKLM:**

1. **Which metric is the 15%?** Plain MAPE, median MAPE, weighted MAPE/WMAPE, or
   something else? Quote the definition **verbatim**, including the formula if given.
2. **At what aggregation level** is it measured — per SKU, per category, per store,
   or pooled across the panel? A 15% pooled figure and a 15% per-SKU figure are very
   different targets.
3. **Is 15% their own result, or a benchmark they cite from elsewhere?** If cited,
   **the original source is what this thesis should cite**, not Ceran et al.
4. **What forecast horizon and grain?** Ours is H=3 on brand × month. A daily or
   weekly SKU-level benchmark is not comparable and should not be used as our target.
5. **Do they report zero-actual handling?** If their panel has no zero actuals, plain
   MAPE is well defined for them and undefined for us (§6.4) — which would make the
   metric non-transferable regardless of the answer to (1).

**If the answer is "plain MAPE per SKU":** the honest move is to drop the ≤15% target
as a comparability claim and report against the simple benchmarks instead, which are
measured on our own data and need no cross-study metric alignment.

---

## GROUP A — Forecasting substrate (§2.1) — SRQ1

| # | Source | Status | Claim it supports | **Verify** |
|---|--------|:------:|-------------------|-----------|
| A1 | **Makridakis, Spiliotis & Assimakopoulos (2020).** The M4 competition. *IJF* 36(1), 54–74. | PP | "Combining models tends to outperform any single best model"; hybrids of statistical structure and ML achieve highest accuracy | Does M4 support the **combination** claim as stated? Also: does it support the *simple-beats-complex* finding we now need for the RTD result (seasonal-naive beats our tuned models)? **If that is in M5 rather than M4, we are citing the wrong paper.** |
| A2 | **Makridakis et al. (2022).** M5 accuracy competition. *IJF* 38(4), 1346–1364. | PP | Top submissions used gradient-boosted trees incl. LightGBM; exogenous promo/calendar features beat history-alone | Confirm both sub-claims. Also check whether M5 reports a **global vs local** (pooled vs per-series) finding — needed for register C4, currently unsourced. |
| A3 | **Ceran, Özkan, Eskiocak, Mert & Yüceoğlu (2024).** ML-based demand forecasting for an FMCG retailer. INFUS 2024, LNNS 1090. Springer. | PP | LightGBM strong accuracy at low memory; **"MAPE of 15% or below as a practical benchmark"** | **PROMOTED TO PRIORITY 1 ABOVE — see that block for the full question set.** Which metric is their 15%? Plain MAPE, median MAPE, or weighted/WMAPE? We report WMAPE and meet ≤15% on 2 of 4 categories. **On median MAPE we meet it on none (31.8–38.6%).** This one fact decides whether a headline target is met or missed. |
| A4 | **Ma, Jackson, Huang, Villegas & Macias-Aguayo (2025).** Data-driven context-aware demand forecasting in beverages. *IJLRA*. | PP | ML with exogenous features beats statistical baselines for high-volume stable SKUs; **no single model dominates** | Confirm "no single model dominates". Our evidence **corroborates strongly** and adds a sample-size threshold — check whether they offer one. |
| A5 | **Nguyen et al. (2025).** ML for economic forecasting and SME growth. *Int. J. Innovation Studies* 9(1). | PP | LightGBM/XGBoost suited to short-horizon forecasting with limited observations | Confirm the regime matches ours (~460–1,800 rows/category, ~44 monthly periods). |
| A6 | **Ahrens, Hansen, Schaffer & Wiemann (2024).** Model averaging and double machine learning. *J. Applied Econometrics*. | PP (arXiv DOI listed — check) | Stacked averaging, esp. inverse-variance weighting, improves on individual learners | Confirm. **The DOI given is an arXiv DOI** while the venue is a journal — resolve which version is cited. Relevant to disconnection D1. |
| A7 | **Klee & Xia (2025).** Measuring time series forecast stability for demand planning. KDD '25 Workshop. | **PRE** | Stability = coefficient of variation under nominally identical inputs; tree ensembles more stable than classical under promotions | Confirm the **definition** — we have now implemented CV-across-seeds on that basis. Confirm the tree-vs-classical claim. **Published since?** |
| A8 | **Ng (2017).** Lessons from analyzing terabytes of scanner data. NBER WP 23673. | PP (WP) | Memory as primary binding constraint in scanner-data analysis | Ch2 §2.2 distinguishes Ng's *raw-data-volume* constraint from our *deployment-cost* one. **Verify that reading is fair to Ng** — it is nuanced. |

**MISSING — no source cited anywhere:**

| Gap | What is needed |
|-----|----------------|
| **Forecast accuracy metrics** | Ch2 does not review metrics at all, yet WMAPE is the headline and WMAPE-vs-medMAPE disagreement is a recurring finding (up to 20pp). Need a definition/motivation for WMAPE and a source on MAPE's failure near zero. **Candidate: Hyndman & Koehler (2006), *IJF* 22(4) — UNVERIFIED.** Check whether they recommend MASE; if so we must justify not using it. |
| **Global vs local forecasting** | The pooled-vs-per-category crossover (~750–1000 rows) has no literature context. **Candidates: Montero-Manso & Hyndman (2021), *IJF*; M5 — UNVERIFIED.** |
| **Simple benchmarks as standard** | We added naive/seasonal-naive/drift. **Candidate: Hyndman & Athanasopoulos *FPP3* §5.2 (open access, otexts.com/fpp3) — easy to verify.** |
| **Intermittent demand as a distinct problem** | We exclude ~27–40% of brands for zero-valued test windows; need to justify as out-of-scope. **Candidates: Croston (1972); Syntetos & Boylan — UNVERIFIED.** |

---

## GROUP B — Decision support and forecast-to-decision (§2.3)

| # | Source | Status | Claim | **Verify** |
|---|--------|:------:|-------|-----------|
| B1 | **Elmachtoub & Grigas (2022).** Smart "predict, then optimize". *Management Science* 68(1). | PP | Minimising prediction error ≠ maximising decision quality | Confirm. |
| B2 | **Mandi, Kotary, Berden, Mulamba, Bucarey, Guns & Fioretto (2024).** Decision-focused learning survey. *JAIR* 81. | PP | "Zero prediction loss implies zero decision loss but not the converse"; no method dominates | Confirm the asymmetry as worded — it is quoted precisely. |
| B3 | **Herath, Shrestha & von Krogh (2024).** Design principles for AI-augmented decision making. *EJIS* 34(2). | PP | Design principles | Verify what Ch2 attributes. |
| B4 | **Olszak & Bartuś (2025).** AI-enhanced BI for decision-making. *Procedia CS* 270. | PP | Descriptive BI → forecast-informed transition | Confirm. Procedia is proceedings — check review rigour. |
| B5 | **Goodwin, Önkal & Thomson (2010).** Do forecasts expressed as prediction intervals improve production planning decisions? *EJOR* 205(1). | PP | Prediction intervals and decision quality | **Directly relevant to SRQ2.** Verify whether the finding is positive, negative or mixed — **if intervals did not help, that is important and must not be misreported.** |
| B6 | **Rinaldi, Giordano, De Stefano & Fontanella (2025).** DSS4EX. *ESWA* 269. | PP | Explainability over time-series forecasting pipelines | Verify it does **not** do what we claim is novel — a near-neighbour to the gap claim. |
| B7 | **Zheng, Almahri, Xu, Minaricova & Brintrup (2025).** LLMs in supply chain management. *IFAC-PapersOnLine* 59(10). | PP | LLMs in SCM | Verify attribution. |

---

## GROUP C — LLM agents and tool use (§2.4)

| # | Source | Status | Claim | **Verify** |
|---|--------|:------:|-------|-----------|
| C1 | **Schick et al. (2023).** Toolformer. NeurIPS 36. | PP | Agents can invoke tools; tool delegation can substitute for raw model scale | Confirm the **"substitute for scale"** claim — it does real work in the gap argument. |
| C2 | **Wang, X. et al. (2024).** Executable code actions elicit better LLM agents (CodeAct). ICML 2024. | PP | Code-as-action agents | **Foundational for scenarios B_data and D_prometheus.** |
| C3 | **Chen, E. & Bibi, Z. (2026).** MLAT: statistical ML models as callable tools in LLM agent workflows. arXiv 2602.14295. | **PRE** | Emerging work exposing pre-trained models as agent tools | **CRITICAL FOR GAP G3.** Ch2 says it "exists only as small, non-peer-reviewed proofs of concept". **If MLAT is more developed than described, G3 weakens.** Verify scope; published since? |
| C4 | **Paranjape et al. (2023).** ART. arXiv 2303.09014. | **PRE** | Tool-use orchestration | Published since? |
| C5 | **Ma, M. et al. (2024).** SciAgent. arXiv 2402.11451. | **PRE** | Orchestration patterns | Published since? |
| C6 | **Chen, Z. et al. (2024).** AutoFlow. arXiv 2407.12821. | **PRE** | Orchestration patterns | Published since? |
| C7 | **Wu, Y. et al. (2025).** ScoreFlow. arXiv 2502.04306. | **PRE** | Orchestration patterns | Published since? |
| C8 | **Liu, Z. et al. (2023).** Dynamic LLM-powered agent network. arXiv 2310.02170. | **PRE** | Agent collaboration | Published since? |
| C9 | **Huang, J. et al. (2024).** Self-verification sampling for tool use. OpenReview. | **PRE** | Tool-use self-verification | OpenReview — **accepted or rejected? If rejected, reconsider using it.** |
| C10 | **Sapkota, Roumeliotis & Karkee (2025).** AI agents vs agentic AI. *Information Fusion* 126. | PP | The Agentic AI definition used in Ch1 line 18 | Confirm the definition is quoted accurately. |

---

## GROUP D — Reliability, uncertainty, evaluation (§2.5) — SRQ2

| # | Source | Status | Claim | **Verify** |
|---|--------|:------:|-------|-----------|
| D1 | **Ji, Gu, Zhang, Lyu, Lin & Chen (2024).** ANAH. ACL 2024. | PP | Hallucination is measurable | Confirm. |
| D2 | **Kuleshov, Fenner & Ermon (2018).** Calibrated regression. ICML 2018. | PP | Calibration of regression uncertainty | **Closest existing source to our conformal intervals** — but it is *calibrated regression*, not conformal prediction. Verify whether it covers split-conformal at all. Probably not — see the gap below. |
| D3 | **Levi, Gispan, Giladi & Fetaya (2022).** Evaluating and calibrating uncertainty in regression. *Sensors* 22(15). | PP | Calibration evaluation | Relevant to our ≥85% coverage target. |
| D4 | **Gu, J. et al. (2024).** Survey on LLM-as-a-judge. arXiv 2411.15594. | **PRE** | Judge methodology and bias | **NO LONGER NEEDED** — judge dropped (B-DEC-2). Keep only if Ch2 uses it to justify *not* using one. |
| D5 | **Ye, J. et al. (2024).** Biases in LLM-as-a-judge. arXiv 2410.02736. | **[?]** Ch2 flags "verify" | Judge bias | **NO LONGER NEEDED** (same reason). |
| D6 | **Mehta (2025).** CLEAR: multi-dimensional evaluation of enterprise agentic AI. arXiv 2511.14136. | **PRE** | The evaluation frame SRQ4's metrics map to | **Load-bearing for SRQ4's metric design.** Verify CLEAR is as described; peer-reviewed since? **A preprint carrying our evaluation framework is a weak point.** |
| D7 | **Sapra, Sapra, Hada & Pareek (2025).** AgentCompass. arXiv 2509.14647. | **PRE** | Evaluating agentic workflows in production | Published since? |
| D8 | **Wang, R. et al. (2026).** AgentNoiseBench. arXiv 2602.11348. | **PRE** | Agent robustness under noisy tool output | Verify; very recent. |
| D9 | **Dong, Lu & Zhu (2025).** AgentOps taxonomy for observability. arXiv 2411.05285. | **PRE** | Observability/traceability requirements | **Load-bearing for SRQ3 readiness criteria.** Published since? |

**MISSING — the most serious literature gap in the thesis:**

> **CONFORMAL PREDICTION IS NOT REVIEWED ANYWHERE IN CH2**, yet every forecast the
> artefact serves carries a split-conformal 90% interval, and SRQ2's uncertainty claim
> depends on it entirely.
>
> **Candidates, all UNVERIFIED:**
> - Lei, G'Sell, Rinaldo, Tibshirani & Wasserman (2018), "Distribution-Free Predictive
>   Inference for Regression", *JASA*
> - Shafer & Vovk (2008), "A tutorial on conformal prediction", *JMLR*
> - Vovk, Gammerman & Shafer (2005), *Algorithmic Learning in a Random World*
>
> Also needed: **conformal prediction for time series / under distribution shift**,
> where exchangeability is violated. That is a genuine limitation of our application and
> better cited than asked about.
>
> **This needs a Ch2 subsection, not just a reference.**

---

## GROUP E — Production systems and integration (§2.6) — SRQ3

| # | Source | Status | Claim | **Verify** |
|---|--------|:------:|-------|-----------|
| E1 | **González-Potes et al. (2026)** *(or Bürger & Pauli 2024 — see PRIORITY 0)* | PP | Closest published exemplar; >98% spec compliance, <3% median numerical error; authors "explicitly note" it does not address forecasting or SME constraints | **See PRIORITY 0 — resolve the identity contradiction first.** |
| E2 | **Dong, Lu & Zhu (2025).** AgentOps taxonomy. | **PRE** | Observability capabilities for production agents | See D9. |

---

## GROUP F — Methodology (§2.8)

| # | Source | Status | Claim | **Verify** |
|---|--------|:------:|-------|-----------|
| F1 | **Hevner, March, Park & Ram (2004).** *MIS Quarterly* 28(1). | PP | DSR paradigm | Standard, low risk. |
| F2 | **Peffers, Tuunanen, Rothenberger & Chatterjee (2007).** *JMIS* 24(3). | PP | DSR process model | Standard, low risk. |
| F3 | **Saunders, Lewis & Thornhill (2023).** *Research Methods for Business Students* (9th ed.). | PP | Research-design scaffold; narrative vs systematic review | Confirm the narrative-review justification (Ch2 §2.0) is supported. |

---

## GROUP G — Methods used but cited NOWHERE

All are used by the thesis; none appears in any chapter's references.

| Method used | Candidate source | Status |
|-------------|------------------|--------|
| TPE hyperparameter sampler | Bergstra, Bardenet, Bengio & Kégl (2011), NeurIPS | UNVERIFIED |
| Random > grid search | Bergstra & Bengio (2012), *JMLR* 13 | UNVERIFIED |
| Optuna | Akiba, Sano, Yanase, Ohta & Koyama (2019), KDD | UNVERIFIED |
| Rolling-origin / time-series CV | Hyndman & Athanasopoulos *FPP3* §5.10; Tashman (2000) *IJF* 16(4) | UNVERIFIED |
| Model-selection optimism | Cawley & Talbot (2010), *JMLR* | UNVERIFIED |
| Ridge as tabular baseline | Hastie, Tibshirani & Friedman, *ESL* ch. 3 | UNVERIFIED |
| SHAP | Lundberg & Lee (2017), NeurIPS | UNVERIFIED |
| Importance ≠ selection | *(none identified)* | UNSOURCED |
| Prophet's intended data regime | Taylor & Letham (2018), "Forecasting at scale" | UNVERIFIED |
| Log transforms / tree invariance to monotone transforms | *(none identified)* | UNSOURCED |

---

## GROUP H — Open areas where citations would strengthen the thesis

| Area | Why | Search direction |
|------|-----|------------------|
| Do LLMs forecast time series well? | Scenario A assumes not; literature would justify it | "LLMs as zero-shot time series forecasters" |
| Context length and LLM performance | Directly relevant to the context-depth experiment | "lost in the middle"; long-context degradation |
| Communicating forecast uncertainty to decision-makers | SRQ2's core concern; Goodwin (B5) is the only current source | forecast uncertainty communication; DSS |
| Retail/FMCG forecasting practice | Domain grounding | Nielsen scanner-data studies |
| Model deployment footprint trade-offs | SRQ1's memory leg | efficient ML deployment; model size vs accuracy |

---

## Download priority

1. **González-Potes (2026) AND Bürger & Pauli (2024)** — resolve PRIORITY 0
2. **Ceran et al. (2024)** — the 15% metric question (A3)
3. **Chen & Bibi (2026) MLAT** — gap G3's exposure (C3)
4. **Conformal prediction** — Lei et al. (2018) / Shafer & Vovk (2008)
5. **Hyndman & Koehler (2006)** — accuracy metrics
6. **Montero-Manso & Hyndman (2021)** — global vs local
7. **Klee & Xia (2025)** — the stability definition we implemented (A7)
8. **Mehta (2025) CLEAR** — SRQ4's metric framework, currently a preprint (D6)
9. **M4 (2020) and M5 (2022)** — incl. the simple-beats-complex claim
10. Everything else in Groups A–F

## Summary

| Category | Count |
|----------|------:|
| Peer-reviewed, cited in Ch2 | 24 |
| Preprints, cited in Ch2 | 15 |
| **Contradictory citation (PRIORITY 0)** | **1** |
| Methods used but never cited (Group G) | 10 |
| Literature gaps needing a new Ch2 section | 2 (conformal, metrics) |
| Open areas (Group H) | 5 |
