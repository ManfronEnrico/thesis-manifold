---
name: notebooklm-sections-d-k-response
description: Response to NotebookLM modelling review sections D-K — nine overstatements refuted, one docstring claim corrected by measurement, and the Ch6 rewrite requirements that follow.
category: reference
applies-to: [ch2, ch3, ch6, srq1, citation-register]
triggers: [writing Ch6, citing a benchmark/CV/HPO/SHAP/Prophet claim, justifying a feature drop or an exclusion threshold]
created: 2026_08_23-20_00
updated: 2026_08_23-20_00
---

# NotebookLM modelling review — response to Sections D–K

Eight further sections, 39 additional claims. Combined with A–C: **56 claims checked.**

**The pattern in D–K is different from A–C, and it is worth naming.** A–C found things we
had *wrong*. D–K mostly found things we would have **overstated** — nine claims where the
literature supports a weaker version of what the thesis was preparing to say. Only one
required a code-adjacent correction.

**That is the more common failure mode in a literature review, and the harder one to
self-detect**, because every one of these overstatements is a plausible-sounding sentence
built on a real source.

---

## 1. The nine overstatements, and what replaces each

| ID | The overstatement | Verdict | The defensible version |
|---|---|---|---|
| **BM-05** | "M4 proved seasonal-naïve beats tuned ML for retail beverage demand" | Contradicted as universal | M4 is 100k heterogeneous series with **no beverage category**. It establishes that *pure ML often fails to beat simple statistical baselines* — which **contextualises** our RTD result rather than proving it. |
| **CV-04** | "K-fold CV always fails for time series" | Contradicted (overstated) | Bergmeir et al. (2018) **prove** standard K-fold is valid for purely autoregressive models with uncorrelated errors. "Always fails" is mathematically false. |
| **CV-06** | "Expanding-window is mathematically mandatory for trended demand" | Contradicted (overstated) | No such proof exists. It is a **highly defensible design choice**, not a mandate. Sliding windows trade differently (adapt to breaks vs. maximise training data). |
| **HPO-07** | "50–200 trials is the established HPO convention" | Contradicted / Not Found | **Independent confirmation of what we already recorded as UNSOURCEABLE.** Practitioner folklore. Required trials grow with search-space dimensionality. |
| **HPO-08** | "Snoek et al. establish a stopping criterion on flattening curves" | Contradicted / Not Found | They use **fixed budgets** (50/100 trials or wall-time). Our plateau criterion is **our empirical design decision**, not their framework. |
| **MS-04** | Peeked-at test results are "mildly optimistic" | Qualified — **"mildly" must go** | Cawley & Talbot call the bias "of **surprising magnitude**", large enough to "conceal even the true difference between state-of-the-art and uncompetitive algorithms". Correct term: **optimistically biased to an unquantifiable degree.** |
| **TREE-02** | "ESL prescribes Ridge as the baseline every tabular model must beat" | Contradicted (overstated) | No normative rule in ESL. Ridge is a **foundational benchmark for regularised linear models**, whose merit is conditional on the data-generating process. |
| **SHAP-05** | "Lundberg & Lee prove pruning low-SHAP features improves accuracy" | Contradicted — **fabrication** | They never evaluate feature selection at all. The paper explains a **fixed** model. |
| **PRO-04/05** | "Taylor & Letham state Prophet is unsuitable for monthly data / prove it flatlines" | Contradicted / Not Found | They impose **no such restriction**. The real argument is mechanical: monthly data removes weekly seasonality and daily holiday windows — **the very features Prophet exists to exploit.** |
| **ID-04** | "Syntetos & Boylan recommend excluding highly intermittent series" | Contradicted | Their entire contribution is **specialised estimators (SBA) to forecast such series**, not discarding them. |

**Every one of these was heading into the thesis as a citation-backed sentence.**

---

## 2. The one that hit our code: SHAP-03 and the "measured cost" that was not measured

`srq1_pooled.py` justified dropping `promo_intensity` with:

> *"Measured cost of that restriction: promo_intensity ranks 11th of 13 by mean absolute
> SHAP in CSD (0.041)."*

**A SHAP rank is not a cost measurement.** SHAP attributes a *fixed, already-fitted*
model's output. It says nothing about what out-of-sample error does when the feature is
removed and the model **refitted** — precisely the relevance-vs-usefulness gap Guyon &
Elisseeff (2003, p. 1158) formalise and SHAP-03 flags.

**So it was measured properly** (refit with and without, on the two categories that carry
the feature):

| Category | Model | WMAPE 13 feats | WMAPE 12 feats | Δ |
|---|---|---:|---:|---:|
| CSD | XGBoost | 14.51% | 14.81% | +0.30pp |
| CSD | LightGBM | 16.20% | 16.47% | +0.27pp |
| energidrikke | XGBoost | 14.91% | 16.35% | +1.44pp |
| energidrikke | **LightGBM** | 17.39% | **16.03%** | **−1.36pp** |

**Dropping the feature HELPS on 5 of 8 model × category × metric combinations** —
including LightGBM on energidrikke, *the category where promotion data actually exists*.
Worst case is +1.44pp; the median effect is near zero and not consistently signed.

**The conclusion survives — the restriction is cheap — but the evidence for it was wrong,
and the measured version is more interesting than the SHAP rank.** It is a clean empirical
instance of SHAP-06: a well-attributed feature whose removal does not hurt, and sometimes
helps.

Docstring corrected to state the measured result and explain why the SHAP rank did not
license the claim.

---

## 3. What survived, and is now citable

| Claim | Source | Use it for |
|---|---|---|
| Four simple benchmarks (mean/naïve/seasonal-naïve/drift) with formulas | Hyndman & Athanasopoulos (2021) §5.2 | §6.2, and the requirement to beat them |
| Pure ML underperformed in M4; **hybrids won** | Makridakis et al. (2018), p. 803 | Framing RTD; **and F_ensemble's motivation** |
| Rolling-origin ≠ fixed-origin; recalibration preferred over updating | Tashman (2000), pp. 439–440 | §6.3 CV protocol |
| Temporal order matters under **non-stationarity specifically** | Cerqueira et al. (2020) | Why we don't use K-fold **here** |
| K-fold valid for stationary AR with uncorrelated errors | Bergmeir et al. (2018), Thm 1 | The honest boundary condition |
| TPE formulation | Bergstra et al. (2011), p. 2549 | The **mathematics** of our tuner |
| Optuna define-by-run, pruning, distribution | Akiba et al. (2019), p. 2623 | The **software** only — never the maths |
| Random > grid when few hyperparameters matter | Bergstra & Bengio (2012) | Why not grid search |
| **Model selection overfits a noisy criterion** | Cawley & Talbot (2010), pp. 2079, 2083 | Our nested-CV limitation |
| Ridge = RSS + L2 penalty (Eq. 3.41/3.42) | Hastie et al. (2009), pp. 61–62 | §6.2.5 |
| **Trees invariant to monotone transforms of PREDICTORS** | Hastie et al. (2009), p. 307 | **F54 — verified correct as we stated it** |
| SHAP uniqueness (local accuracy, missingness, consistency) | Lundberg & Lee (2017), p. 4, Thm 1 | §6.5 SHAP section |
| Relevance ≠ usefulness; useless-alone can be useful-together | Guyon & Elisseeff (2003), pp. 1158, 1163–4 | The `promo_intensity` result |
| Prophet additive decomposition, design intent | Taylor & Letham (2018), pp. 37–38 | §6.2.2 |
| SBA bias correction (1 − α/2); p=1.32 / CV²=0.49 quadrants | Syntetos & Boylan (2005); Syntetos et al. (2005) | **Intermittency — currently uncited entirely** |

### 3.1 F54 is verified — and we stated it correctly

TREE-05 refutes "predictor invariance explains why logging the *target* affected Ridge but
not LightGBM". **We never made that claim.** Checked every occurrence in the repo: all
of them say trees are invariant to transforming the **features**, which is TREE-03/04, both
Supported.

Worth knowing the neighbouring claim is false — **transforming the target affects LightGBM
too** (leaf means are arithmetic means; 𝔼[log Y] ≠ log 𝔼[Y]; and boosting gradients change).
Do not let the F54 write-up drift into it.

### 3.2 The M4 hybrid finding strengthens F_ensemble

BM-04: M4's winner was a **hybrid** (Smyl's ES-RNN, +9.4% over Comb), and second place was a
**combination of seven statistical methods**. Combined with D1's M4/Ahrens citations, the
literature case for `F_ensemble` is now considerably stronger than "combining tends to help".

---

## 4. Two exclusion thresholds now need the same defence

ID-04 and FM-06 (Section C) converge on one point: **the literature we cite consistently
objects to excluding difficult series rather than modelling them.** We have two exclusions:

| Exclusion | Status |
|---|---|
| Zero-actual rows from MAPE statistics | Mathematically necessary (APE undefined); now **MAPE-only**, with WMAPE and MASE reported for all |
| **≥1 unit/month volume floor** on WMAPE tables (added 2026-08-23) | **A declared design decision** — must be presented as ours, never attributed to a source |

**Neither may be attributed to Hyndman & Koehler or to Syntetos & Boylan.** Both papers
recommend better *methods* (MASE, SBA), not exclusion. Our thresholds are defensible as
stated design choices with disclosed counts — which is what both now are.

**Opportunity:** the Syntetos–Boylan–Croston quadrants (p = 1.32, CV² = 0.49) would let us
**classify** brands as smooth/intermittent/erratic/lumpy rather than apply an arbitrary
volume floor. That is a principled, citable alternative to a threshold I picked. **Worth
doing** — it converts a judgement call into a literature-grounded categorisation, and would
let the write-up report accuracy *per demand pattern*, which is a more interesting result
than a single pooled number.

---

## 5. Ch6 consequences — beyond the stale numbers

The staleness audit already flags every number in Ch6 as wrong. These sections add
**claim-level** problems the number-fixing pass would not catch:

| Ch6 location | Problem | Fix |
|---|---|---|
| §6.2.1 | Cites `auto_arima` (pmdarima) | **Not used** — implementation is `SARIMAX(order=(1,1,1))` |
| §6.2.2 | Prophet "auto-tuned via cross-validation"; lists holidays as an advantage | No Danish holiday calendar is an input; monthly grain nullifies the holiday machinery (PRO-04/06) |
| §6.2.3/4 | "Optuna ≤50 trials" | **100 trials, 4-fold expanding-window CV** |
| §6.2.5 | Ridge as "the linear baseline" | Fine — but do **not** upgrade this to "must beat" (TREE-02) |
| §6.4 metrics table | MAPE listed as the primary metric, "cite Xu 2024" | MAPE is undefined on 14–29% of rows. **WMAPE + MASE**, with Hyndman & Koehler and Gneiting |
| §6.4 | "Target MAPE ≤15%" | Ceran's metric is **still unverified** (D2). Do not claim the target is met until it is |
| §6.3.1 | `[split_date_1]` placeholders | Unfilled placeholders in a submitted chapter |
| §6.3.2 | Superseded weekly-grain block retained in comments | Delete — DEC-GRAIN locked brand × month |
| §6.5.1 | brand × chain column | **Grain removed by DEC-GRAIN/P0035.** Table structure is obsolete, not just its values |

---

## 6. Priority for the next batch

| # | Task | Why |
|---|---|---|
| 1 | **Ceran et al. (2024) — which metric for the 15% benchmark?** | Still the single highest-value open question (D2). Determines whether a headline target is met |
| 2 | **Refute G2 and G3** | The novelty claim's exposed points |
| 3 | **Verify Bürger & Pauli, and the González-Potes conflict** | PRIORITY 0 — two different papers cited for the same "closest precedent" claim |
| 4 | Have the 15 flagged preprints been published? | Free citation-quality upgrade |

## Related

- `2026_08_23-19_00-notebooklm-modelling-review-response.md` — Sections A–C
- `2026_08_22-18_00-citation-register.md` — entries updated
- `05_thesis_writing/notes/2026_08_22-21_00-chapter-staleness-audit.md` — the numbers half of the Ch6 problem
