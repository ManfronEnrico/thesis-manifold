# Thesis Outline — Approved Structure
> Last updated: 2026-04-12 (v3 — thesis-structuring skill / /update-outline)
> Previous version: v2 — 2026-03-14 (post ChatGPT structural revision)
> Status: MINOR REVISION — page budgets reconciled against thesis-writer.md; subsection detail added; no chapter added or removed
> Change level: Minor revision — no human approval required (SKILL.md §Step 3)

---

## Identity

| Field | Value |
|---|---|
| Working title | How AI Systems Can Provide Predictive Decision-Support in Real-World Business Environments Under Computational Constraints |
| Programme | MSc Business Administration & Data Science, CBS |
| Partner | Manifold AI |
| Group | 2 students |
| Page limit | 120 standard pages (2,275 chars/page excl. spaces) |
| Deadline | 15 May 2026 |
| Language | English |

---

## Research Questions (v2 — 2026-03-14)

**Main RQ**: How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?

| | Sub-RQ | Phase |
|---|---|---|
| SRQ1 | Which predictive modelling approaches provide the best balance between forecasting accuracy and computational efficiency under realistic cloud resource constraints? | Phase 4 |
| SRQ2 | How can a multi-agent architecture coordinate predictive models and heterogeneous data signals to generate actionable managerial recommendations? | Phase 5 |
| SRQ3 | To what extent does additional contextual information improve the predictive and decision-support capabilities of AI systems? | Phase 5–6 |
| SRQ4 | How does the proposed predictive AI system compare to traditional descriptive analytics approaches used in business intelligence systems? | Phase 6 |

---

## Page Budget (authoritative — sourced from `.claude/agents/thesis-writer.md`)

> ⚠️ This table supersedes the v2 chapter budget table. Conflicts with `thesis_state.json` chapter targets noted — state.json is not authoritative for page budgets.

| # | Section | Target pages | Status | SRQ mapping |
|---|---|---|---|---|
| — | Front page + ToC + AI Declaration | ~2 | — | Excluded from char count |
| — | Abstract | 1 | bullets_draft | Counts toward 120pp |
| 1 | Introduction | **8** | PROSE DRAFT (2026-04-05) | — |
| 2 | Literature Review | **22** | bullets_draft | — |
| 3 | Methodology | **12** | bullets_draft | — |
| 4 | Data Assessment | **10** | bullets_draft / BLOCKED | — |
| 5 | Framework Design | **14** | bullets_draft | SRQ2 |
| 6 | Model Benchmark & Selection | **16** | bullets_draft / BLOCKED | SRQ1 |
| 7 | Context-Aware Decision Synthesis | **12** | bullets_draft / BLOCKED | SRQ2, SRQ3 |
| 8 | Experimental Evaluation | **10** | bullets_draft / BLOCKED | SRQ3, SRQ4 |
| 9 | Discussion | **7** | bullets_draft | — |
| 10 | Conclusion | **6** | bullets_draft | — |
| — | Bibliography | not counted | — | — |
| — | Appendices | not counted | — | — |
| | **Total body** | **120** | | 0-page buffer — budget is tight |

> ⚠️ Budget is tight. No chapter may be expanded without reducing another. Do not add sections without removing equivalent space elsewhere.

---

## Chapter Structure (v3 — with subsection detail)

### Front Matter

- **Abstract** (~1 page, counts toward limit)
  - Research context (Manifold AI, FMCG retail)
  - Research questions (Main RQ + 4 SRQs)
  - Methodology (DSR)
  - Key findings (pending data)
  - Contribution

- **AI Use Declaration** (placement TBC with supervisor — before Ch.1 or in appendix)

---

### 1. Introduction (~8 pages)
▶ Status: **PROSE DRAFT** — written 2026-04-05, requires human review before finalisation

| Subsection | Content |
|---|---|
| 1.1 Background and Motivation | FMCG analytics gap, descriptive→predictive transition, M4/M5 findings |
| 1.2 Research Problem and Gap | Manifold AI context, three unsolved challenges, gap statement |
| 1.3 Research Questions | Main RQ + SRQ1–4, each with rationale |
| 1.4 Scope and Delimitations | Danish CSD market, 8GB RAM constraint, batch mode, DSR prototype |
| 1.5 Thesis Structure | Chapter-by-chapter roadmap |

---

### 2. Literature Review (~22 pages)
▶ Status: **bullets_draft** — 37 papers integrated (Runs 1–3); pending human approval

| Subsection | Content | Papers | SRQ |
|---|---|---|---|
| 2.1 AI Agents and LLM Orchestration | Agent paradigm, multi-agent coordination, LLM reliability | Toolformer, ART, LangGraph, DyLAN, AutoFlow, ScoreFlow, SciAgent, ANAH, AgentNoiseBench, AgentCompass, Self-Verification | Main RQ, SRQ2 |
| 2.2 Predictive Modelling for Decision-Support | Descriptive→predictive transition, ML for retail forecasting | AI-enhanced BI, AI-augmented DM, DSS4EX, Humans vs LLMs | SRQ1, SRQ4 |
| 2.3 Ensemble Methods and Model Averaging | Model combination theory, M4/M5 findings, LightGBM | Makridakis 2020, Makridakis 2022, Ahrens et al. (DML), Ma et al. 2025 | SRQ1 |
| 2.4 Multi-Criteria Decision Synthesis | MCDM frameworks, confidence scoring, prediction intervals | MCDM overview, Calibrated Regression (Kuleshov), Uncertainty (Sensors), Prediction Intervals (EJOR) | SRQ2 |
| 2.5 Resource-Constrained AI Deployment | Edge AI, SME compute, RAM profiling, stability | Edge AI survey, Klee & Xia 2025, Ng 2017, Niculescu-Mizil & Caruana | SRQ1 |
| 2.6 Gap Summary and Novelty Claim | Explicit gap statement, novelty v4 | All | All |

> Note: v2 outline listed 5 key content areas; v3 refines to 5 thematic sections + gap summary. Subsection structure consistent with existing `docs/thesis/sections/ch2-literature-review.md`.

---

### 3. Methodology (~12 pages)
▶ Status: **bullets_draft**

| Subsection | Content |
|---|---|
| 3.1 Philosophy of Science | Pragmatism, moderate realism ontology, empirical epistemology — CBS mandatory |
| 3.2 Research Design — DSR | Hevner 2004 + Peffers 2007 framework; artefact type; DSR cycles |
| 3.3 Research Strategy | Research strategy, case study context (Danish CSD market) |
| 3.4 Data Sources | Nielsen/Prometheus CSD, Indeks Danmark — access status and modality |
| 3.5 Analytical Approach | 3-level validation framework: ML accuracy, recommendation quality, agent behaviour |
| 3.6 Validity and Reliability | Internal, external, construct validity; reliability |
| 3.7 Limitations | Scope boundaries, generalisation constraints, data access risks |

---

### 4. Data Assessment (~10 pages)
▶ Status: **bullets_draft** — BLOCKED (Nielsen access + Indeks Danmark CSVs not yet obtained)

| Subsection | Content |
|---|---|
| 4.1 Nielsen/Prometheus CSD Dataset | Star schema, 28 retailers, 36 months, quality assessment |
| 4.2 Indeks Danmark Consumer Survey | 20,134 respondents, 6,364 variables, mapping to retailer demand |
| 4.3 Data Quality Assessment | Missing values, outliers, temporal coverage, forecasting suitability |
| 4.4 Feature Engineering Plan | Lag features, rolling stats, calendar, promotional flags, consumer signals |
| 4.5 Data Limitations | Access constraints, temporal resolution mismatch, generalisation limits |

---

### 5. Framework Design (~14 pages)
▶ Status: **bullets_draft** — SRQ2

| Subsection | Content |
|---|---|
| 5.1 Design Objectives | 4 design objectives, 8GB constraint, modularity principle |
| 5.2 Architectural Overview | 4-agent + Coordinator pipeline, LangGraph StateGraph, communication via typed state |
| 5.3 Coordinator | Orchestration logic, human-in-the-loop approval gates, state management |
| 5.4 Data Loader Agent | Ingestion and preprocessing of Nielsen + Indeks Danmark; memory footprint |
| 5.5 Forecasting Agent | Sequential model execution, tracemalloc profiling, SRQ1 |
| 5.6 Synthesis Agent | Ensemble logic, Claude API, temperature=0, confidence scoring; SRQ2, SRQ3 |
| 5.7 Validation Agent | 3-level evaluation framework, LLM-as-judge, comparison vs baseline; SRQ4 |
| 5.8 Memory Budget Summary | RAM budget per component, peak usage, transformer exclusion rationale |
| 5.9 Tech Stack Justification | PydanticAI + LangGraph vs alternatives; Python ecosystem choices |

---

### 6. Model Benchmark and Selection (~16 pages)
▶ Status: **bullets_draft** — BLOCKED (SRQ1, requires Nielsen data)

| Subsection | Content |
|---|---|
| 6.1 Candidate Model Overview | ARIMA, Prophet, LightGBM, XGBoost, Ridge Regression — rationale for 5 |
| 6.2 Evaluation Framework | Accuracy (MAPE, RMSE), Efficiency (RAM, runtime), Stability (CV across runs) |
| 6.3 Benchmark Results | Comparative table — 5 models × 3 dimensions |
| 6.4 Memory Profiling | tracemalloc results, peak RAM per model |
| 6.5 Model Selection Decision | Selection criterion, chosen model(s) for Synthesis Agent |

---

### 7. Context-Aware Decision Synthesis (~12 pages)
▶ Status: **bullets_draft** — BLOCKED (SRQ2 + SRQ3, requires Ch.6 output)

| Subsection | Content |
|---|---|
| 7.1 Synthesis Module Architecture | 5-step pipeline: ensemble → calibration → signal enrichment → confidence → narrative |
| 7.2 Ensemble Combination Logic | Weighted combination, model averaging theory (Ahrens et al.) |
| 7.3 Indeks Danmark Signal Integration | SRQ3 — consumer segment mapping, exogenous feature design |
| 7.4 Confidence Scoring | Score composition, calibration (Kuleshov 2018), numerical confidence (0–100) |
| 7.5 Natural Language Recommendation | Claude API, structured prompt, temperature=0, output format |
| 7.6 Synthesis Agent Validation | Level 2 validation, LLM-as-judge, consistency checks (Raj et al. 2022) |

---

### 8. Experimental Evaluation (~10 pages)
▶ Status: **bullets_draft** — BLOCKED (SRQ3 + SRQ4, requires Ch.6–7 output)

| Subsection | Content |
|---|---|
| 8.1 Evaluation Design | Evaluation protocol, metrics, baseline definition |
| 8.2 Forecasting Accuracy Results | SRQ1 — MAPE/RMSE vs baseline |
| 8.3 Recommendation Quality | SRQ2 — LLM-as-judge rubric, hit rate, directional accuracy |
| 8.4 Contextual Signal Value | SRQ3 — with vs without Indeks Danmark enrichment |
| 8.5 Comparison vs Descriptive Baseline | SRQ4 — Manifold AI Colleagues vs predictive framework |
| 8.6 Threats to Validity | Internal, external, construct, reliability |

---

### 9. Discussion (~7 pages)
▶ Status: **bullets_draft**

| Subsection | Content |
|---|---|
| 9.1 Interpretation of Findings | SRQ1–4 findings interpreted in turn: model selection, synthesis quality, consumer signals, BI comparison |
| 9.2 Theoretical Contributions | DSR design knowledge; 5 generalisable design principles; IS literature contribution |
| 9.3 Practical Implications | For Manifold AI, FMCG analytics practitioners, SME AI deployment |
| 9.4 Limitations | Data constraints, generalisation, prototype vs production, LLM reliability |
| 9.5 Future Research | Dynamic agent routing, real-time streaming, other FMCG categories, other markets |

---

### 10. Conclusion (~6 pages)
▶ Status: **bullets_draft**

| Subsection | Content |
|---|---|
| 10.1 Summary of Contributions | Restate Main RQ; answer SRQ1–4 in 2–3 sentences each |
| 10.2 Theoretical Contribution | 5 DSR design principles; contribution to IS and ML literature |
| 10.3 Practical Recommendations | Specific recommendations for Manifold AI deployment |
| 10.4 Limitations Recap | Brief restatement of key limitations (data, scope, prototype status) |
| 10.5 Future Research | Concrete next steps beyond this thesis |
| 10.6 Final Statement | Closing reflection on AI-augmented decision-support at scale |

---

## Locked Decisions (confirmed 2026-03-14, unchanged)

| # | Decision |
|---|---|
| OQ1 — Granularity | **Brand × retailer** level. Default market: DVH EXCL. HD. |
| OQ2 — Models | **ARIMA, Prophet, LightGBM, XGBoost, Ridge Regression** |
| OQ3 — Indeks Danmark | **Feature enrichment**: consumer segments → retailer-level demand signals. |
| OQ4 — Metrics | MAPE/RMSE; Hit rate / directional accuracy; LLM-as-judge rubric |
| OQ5 — Baseline | Manifold AI Colleagues descriptive output or static last-period extrapolation |

---

## What Changed from v2 (2026-03-14 → 2026-04-12)

| Element | v2 | v3 |
|---|---|---|
| Ch.2 pages | 20 | **22** (thesis-writer.md authoritative) |
| Ch.5 pages | 10 | **14** (thesis-writer.md authoritative) |
| Ch.6 pages | 15 | **16** (thesis-writer.md authoritative) |
| Ch.7 pages | 15 | **12** (thesis-writer.md authoritative) |
| Ch.8 pages | 12 | **10** (thesis-writer.md authoritative) |
| Ch.9 pages | 8 | **7** (thesis-writer.md authoritative) |
| Ch.10 pages | 5 | **6** (thesis-writer.md authoritative) |
| Total | 115pp body | **120pp total** (incl. abstract + front matter) |
| Subsection detail | None | Full subsection table per chapter |
| Ch.1 status | — | PROSE DRAFT (written 2026-04-05) |
| Abstract | Not in outline | Added to front matter section |

---

## Open Items for Human Resolution

| # | Item | Priority |
|---|---|---|
| OI-01 | `thesis_state.json` records ch1-introduction as `bullets_draft` — should be `prose_draft`. Update via Coordinator. | Medium |
| OI-02 | AI Declaration placement not confirmed with supervisor. | Medium |
| OI-03 | DSR acceptance with CBS supervisor not confirmed (CRITICAL-CH3-01). | High |
| OI-04 | Budget is exactly 120pp — any expansion requires explicit trade-off. | Ongoing |
| OI-05 | thesis_state.json ch5 target = 15pp, thesis-writer.md = 14pp — minor conflict. thesis-writer.md is authoritative. | Low |
