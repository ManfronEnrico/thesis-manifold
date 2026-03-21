# Chapter 1 — Introduction
> Thesis Writing Agent output — BULLET POINTS ONLY (no prose)
> Last updated: 2026-03-14
> Status: DRAFT — requires human approval before prose writing

---

## 1.1 Background & Motivation

- Business intelligence (BI) systems traditionally deliver descriptive analytics — summarising what happened in the past
- Growing demand from business managers for forward-looking, actionable insights rather than historical reports
- AI-powered BI systems are evolving: from dashboards and KPI reports toward predictive and prescriptive capabilities
- Manifold AI: Danish AI company building "AI Colleagues" — an AI assistant for retail analytics currently operating at descriptive level
- Problem: transitioning to predictive decision-support requires ML forecasting infrastructure that most SME AI providers cannot afford at enterprise cloud scale
- Hard constraint driving the thesis: realistic cloud deployment budgets limit available RAM to ~8GB — ruling out large deep learning models
- Gap: no established framework exists for predictive AI decision-support that explicitly addresses this resource constraint while integrating heterogeneous data signals

---

## 1.2 Research Problem

- Descriptive analytics tells managers what happened; predictive analytics tells them what will likely happen; decision-support tells them what to do
- Current AI Colleagues system (Manifold): descriptive only — does not forecast, does not recommend
- Transition challenge: requires (1) reliable forecasting models within memory constraints, (2) integration of multiple data signals, (3) synthesis into actionable recommendations
- This thesis addresses all three challenges through a multi-agent framework

---

## 1.3 Research Questions

- **Main RQ**: How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?
- **SRQ1**: Which predictive modelling approaches provide the best balance between forecasting accuracy and computational efficiency under realistic cloud resource constraints?
- **SRQ2**: How can a multi-agent architecture coordinate predictive models and heterogeneous data signals to generate actionable managerial recommendations?
- **SRQ3**: To what extent does additional contextual information improve the predictive and decision-support capabilities of AI systems?
- **SRQ4**: How does the proposed predictive AI system compare to traditional descriptive analytics approaches used in business intelligence systems?

---

## 1.4 Delimitation

- Scope: Danish CSD (Carbonated Soft Drinks) retail market — one product category, one country
- Data: Nielsen/Prometheus sales panel + Indeks Danmark consumer survey
- Computational constraint: ≤8GB RAM (cloud deployment realistic budget)
- No deep learning models (LSTM, Transformers) — out of scope due to RAM constraint
- No real-time streaming data — monthly batch processing only
- No production deployment — framework is a research prototype evaluated on historical data

---

## 1.5 Thesis Structure

- Chapter 2: Literature Review — theoretical foundations across 5 research angles
- Chapter 3: Methodology — Design Science Research, philosophy of science, data sources
- Chapter 4: Data Assessment — Nielsen and Indeks Danmark quality and suitability
- Chapter 5: Framework Design — multi-agent architecture, design decisions
- Chapter 6: Model Benchmark — SRQ1, 5-model comparison under memory constraints
- Chapter 7: Context-Aware Decision Synthesis — SRQ2 + SRQ3, integration of consumer signals
- Chapter 8: Experimental Evaluation — SRQ4, framework vs descriptive baseline
- Chapter 9: Discussion — theoretical contribution, practical implications, limitations
- Chapter 10: Conclusion — answers to all RQs, future research

---

## CBS Compliance Notes

- ✅ RQs stated clearly in introduction (CBS requirement)
- ✅ Delimitation section required (CBS: "introduction, delimitation and research question" counts toward page limit)
- ✅ Thesis structure overview required
- ⚠️ Front page fields still to be completed (student numbers, supervisor name, programme name)
