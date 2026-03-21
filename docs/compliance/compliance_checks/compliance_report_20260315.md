# CBS Compliance Report — All Chapter Skeletons
> Generated: 2026-03-15
> CBS Compliance Agent — Run 1 (pre-data, skeleton stage)
> Source guidelines: Thesis/Thesis Guidelines/ (Formal requirements + Bibliographies and references)

---

## Summary Table

| Chapter | Critical Issues | Warnings | Status |
|---|---|---|---|
| Front Page | 2 CRITICAL | 3 | ❌ Needs action |
| Abstract | 1 CRITICAL | 0 | ❌ MISSING |
| Ch.1 Introduction | 0 | 3 | ⚠️ Minor issues |
| Ch.2 Literature Review | 0 | 3 | ⚠️ Incomplete (expected) |
| Ch.3 Methodology | 1 CRITICAL | 3 | ❌ Risk flag |
| Ch.4 Data Assessment | 1 CRITICAL | 2 | ❌ Compliance-gated |
| Ch.5 Framework Design | 0 | 3 | ⚠️ Minor issues |
| Ch.6 Model Benchmark | 0 | 2 | ⚠️ Minor issues |
| Ch.7 Synthesis | 0 | 3 | ⚠️ Minor issues |
| Ch.8 Evaluation | 0 | 3 | ⚠️ Minor issues |
| Ch.9 Discussion | 0 | 2 | ⚠️ Minor issues |
| Ch.10 Conclusion | 1 CRITICAL | 2 | ❌ RQ inconsistency |
| **CROSS-CHAPTER** | **3 CRITICAL** | 2 | ❌ Requires immediate action |

---

## CRITICAL CROSS-CHAPTER ISSUES

### CRITICAL-01: Character Count Definition Error
**Location**: `docs/thesis/sections/frontpage.md` — Notes section
**Issue**: The front page template states: "Characters (no spaces)" for the CBS character count calculation. This contradicts CBS guidelines, which define a standard page as **2,275 characters INCLUDING spaces**.
**Impact**: If word count is based on characters excluding spaces, the thesis could exceed the 120-page limit without realising it. Excluding spaces results in a ~15–20% lower character count, meaning the actual prose would be 15–20% longer per page than the CBS calculation permits.
**Action required**: Correct all page count calculations to use characters INCLUDING spaces. Update `frontpage.md`, `CLAUDE.md`, and character count tracking.
**CBS reference**: "A standard page is max. 2,275 characters incl. spaces on average" (cbs_guidelines_notes.md, extracted from CBS formal requirements).

---

### CRITICAL-02: Abstract is missing
**Location**: No file exists for abstract skeleton
**Issue**: CBS requires the thesis to **begin** with an abstract. The abstract counts toward the total page and character limits (max 1 page). No abstract skeleton has been drafted.
**Impact**: If written late and exceeds 1 page, it will push the thesis over the 120-page limit.
**Action required**: Create `docs/thesis/sections/abstract.md` with a bullet-point skeleton immediately. The abstract should summarise: problem, method, key findings (SRQ1–4), and contribution.
**CBS reference**: "The master thesis must begin with an abstract. The abstract is a part of the assessment of your thesis and count in the total number of pages. The Abstract should be max. 1 page."

---

### CRITICAL-03: AI Use Declaration not drafted
**Location**: No chapter or section addresses the AI use declaration
**Issue**: CBS autumn 2025 rules require declaration of AI use when required by course/programme. This thesis uses Claude Sonnet 4.6 API as an architectural component (Synthesis Agent). There is no draft declaration section.
**Impact**: Missing declaration may constitute academic integrity violation.
**Action required**: Draft an AI use declaration for inclusion in the front matter (not counted in page limit if placed before abstract, or in appendices). Confirm with supervisor where CBS expects this declaration to appear.
**CBS reference**: cbs_guidelines_notes.md — "Autumn 2025 rules: must declare use of AI when required by course/programme."

---

## CHAPTER-SPECIFIC COMPLIANCE CHECKS

---

### Front Page (`frontpage.md`)

**CRITICAL-FRONT-01**: Character count formula wrong (see CRITICAL-01 above)

**CRITICAL-FRONT-02**: Danish/English title requirement unclear
- CBS requires: if enrolled in a Danish programme → thesis must have BOTH a Danish and an English title (without both, CBS cannot issue a diploma)
- If enrolled in an English programme → English title only
- Current skeleton: English title only, with no Danish equivalent
- **Action required**: Confirm programme language with CBS/supervisor. If Danish programme, a Danish title must be added.

**WARNING-FRONT-01**: Missing required front page fields
- Incomplete: Student IDs (both authors), co-author name, supervisor name, exact programme name, group number, submission date
- CBS requires ALL of these to be present on the front page
- Status: acceptable at skeleton stage; must be completed before submission

**WARNING-FRONT-02**: Confidentiality status pending
- CBS: if given access to confidential business data, thesis must be marked confidential
- Nielsen data access may require confidentiality agreement → the thesis may need to be marked confidential
- Action: resolve Nielsen data agreement before finalising front page

**WARNING-FRONT-03**: "Number of standard pages" field will need to be hand-calculated
- The front page must state the actual character count AND standard pages — these cannot be filled until the thesis is written
- The calculation must use characters INCLUDING spaces (see CRITICAL-01)

---

### Abstract — MISSING

**CRITICAL-ABSTRACT-01**: Abstract skeleton does not exist
- CBS requires: abstract, max 1 page, counts toward 120 pages, thesis must begin with it
- Language: if English programme → English abstract
- **Immediate action**: Create `docs/thesis/sections/abstract.md` with bullet skeleton:
  - Problem statement (1–2 bullets)
  - Method (1–2 bullets: DSR, multi-agent framework, 5 models, Nielsen + Indeks Danmark data)
  - Key findings (1 bullet per SRQ — TBD when data available, but structure can be drafted)
  - Contribution (1–2 bullets: 5 design principles, validated artefact)
  - Scope/limitations (1 bullet)
- Character limit: ~2,275 × 1 = 2,275 characters max (including spaces)

---

### Ch.1 Introduction

**STATUS: ✅ Structurally compliant**

CBS requirement check:
- ✅ RQs stated clearly (CBS: introduction must contain RQ)
- ✅ Delimitation section present (section 1.4 — CBS: delimitation is explicitly named as counting toward page limit)
- ✅ Thesis structure overview present (section 1.5)
- ✅ Background and motivation establishes academic and practical problem

**WARNING-CH1-01**: No citation placeholders yet
- When prose is written, all claims (e.g., "Growing demand from business managers for forward-looking insights") need citations
- APA 7 format required (in-text: Author, Year; full reference in bibliography)

**WARNING-CH1-02**: RQ stated in both CLAUDE.md and Ch.1 but minor wording difference observed
- CLAUDE.md main RQ: "How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?"
- Ch.1 main RQ: same ✅
- Ch.10 main RQ: different wording (see CRITICAL-CH10-01)

**WARNING-CH1-03**: Front page fields to complete
- Section 1.1 bullet 13 mentions "Manifold AI" — if thesis is marked confidential, check that company name can appear in the thesis or requires anonymisation

---

### Ch.2 Literature Review

**STATUS: ⚠️ Structurally incomplete (acknowledged, expected at skeleton stage)**

CBS requirement check:
- ✅ Gap statement present and explicit (section 2.6)
- ✅ Sections map to specific SRQs (each subsection labeled with SRQ mapping)
- ✅ Note on literature timeframe present (2015–2026, AI weighted 2020–2026)
- ✅ Philosophy of science correctly deferred to Ch.3

**WARNING-CH2-01**: Chapter status is "SKELETON — full bullet points require Tier 1 paper annotations to complete"
- Multiple sections reference papers by descriptor only (e.g., "Toolformer; ART; Executable Code Actions")
- These are NOT yet annotated in the paper corpus — they appear in the Ch.2 skeleton but do not have annotation files
- **Action required before prose**: all papers cited in Ch.2 must have annotation files and full APA 7 citations
- Tier 1 papers referenced in Ch.2 but not yet in corpus: Toolformer, ART, LangGraph docs, Neuro-Symbolic AI 2024, SciAgent, Model Averaging + DML, ANAH, NumeroLogic, etc.

**WARNING-CH2-02**: Section 2.1.3 cites "Measuring Reliability paper" and "AgentNoiseBench" — not in current corpus
- These are referenced in the skeleton but have no annotation files — they will need to be found and confirmed in Scraping Run 2

**WARNING-CH2-03**: Character count concern
- Target ~20 pages = ~45,500 characters (incl. spaces)
- The skeleton is comprehensive but check during prose writing that this section does not expand beyond 20 pages
- Literature reviews often run over — set a hard limit of 45,500 characters

---

### Ch.3 Methodology

**STATUS: ❌ Risk flag (DSR acceptance by CBS unconfirmed)**

CBS requirement check:
- ✅ Philosophy of science section present (CBS MANDATORY — section 3.1 covers pragmatism, ontology, epistemology)
- ✅ Research design type stated and justified (Explanatory, section 3.2)
- ✅ DSR methodology cited with foundational references (Hevner et al. 2004, Peffers et al. 2007)
- ✅ Validity and reliability section present (section 3.6 — CBS assesses this)
- ✅ Data sources documented with access status

**CRITICAL-CH3-01**: DSR acceptance by CBS unconfirmed
- The skeleton notes: "Confirm with supervisor whether DSR is accepted for this specific programme"
- CBS methodology guidance lists: Exploratory, Descriptive, Explanatory, Normative — these are research design TYPES, not methodological frameworks
- DSR is primarily an IS/IT methodology — Business Administration programmes may expect positivist or interpretivist framing
- **Action required**: Confirm with supervisor urgently — if DSR is not accepted, the entire methodology chapter needs redesign
- **Mitigation if rejected**: Frame as "Explanatory study using design-based research approach" and cite DSR as sub-framework within IS research tradition

**WARNING-CH3-02**: Confidentiality agreement timing
- Section 3.4 correctly notes "potential confidentiality agreement" for Nielsen access
- CBS requirement: must be signed BEFORE data access — currently blocked, which is correctly documented
- This is compliant with CBS requirements; maintain this blocking status until agreement is signed

**WARNING-CH3-03**: GDPR section missing from Ch.3
- Indeks Danmark contains survey respondent data (20,134 respondents, socio-demographics)
- CBS guidelines: GDPR consideration required when handling personal data
- The data was collected by Indeks Danmark (respondents consented to the survey operator), not by this thesis — likely no GDPR issue
- **Action required**: Add a 2-bullet note in Ch.3 confirming that (a) Indeks Danmark data is aggregate survey data collected with respondent consent by the survey operator, (b) no additional GDPR consent is required for secondary use, and (c) data will not leave the local environment

**WARNING-CH3-04**: Citation gaps in methodology chapter
- "Hevner et al. 2004" and "Peffers et al. 2007" are referenced but not in the current paper corpus
- These are foundational DSR papers that must be added to the corpus and cited in APA 7 format
- **Action**: add these to Scraping Run 2 / direct annotation as Tier A methodology papers

---

### Ch.4 Data Assessment

**STATUS: ❌ Compliance-gated (depends on external actions)**

CBS requirement check:
- ✅ Data sources documented
- ✅ Quality assessment methodology described
- ✅ Feature engineering plan documented
- ✅ Access blockers clearly flagged

**CRITICAL-CH4-01**: Nielsen confidentiality agreement required before data access
- CBS: "Confidentiality agreement must be signed BEFORE data access — not after"
- Current status: NOT YET OBTAINED — this is correctly flagged in the chapter
- CBS also notes: "Deadline still applies even if cooperation delays — CBS does not grant extensions for this"
- **Action required**: Contact Manifold AI now to initiate confidentiality agreement process. Do not wait until Phase 1 starts.

**WARNING-CH4-01**: Character count note says "Characters (no spaces)" — see CRITICAL-01 across chapters

**WARNING-CH4-02**: If thesis is confidential, Ch.4 must still be self-contained
- CBS: "Thesis must be self-contained — examiner must understand argumentation WITHOUT appendices"
- Applies to data chapter: cannot defer all data quality assessment to appendix
- Table 4.2.2 (schema) and 4.2.3 (coverage) are correctly kept in the main chapter

---

### Ch.5 Framework Design

**STATUS: ✅ Structurally compliant**

CBS requirement check:
- ✅ Design justified against RQs (section 5.1)
- ✅ Each architectural choice argued against 8GB constraint
- ✅ Tech stack justification table present (section 5.9)
- ✅ Memory budget summary table present (section 5.8)

**WARNING-CH5-01**: Architecture diagram required but not yet generated
- Ch.5 notes: "Agent diagram must appear in this chapter (Mermaid → export as figure)"
- CBS requirement: figures must fit within page space but do NOT count toward character count
- **Action required**: Diagram Agent must generate the system architecture figure before prose writing starts (item 3 in current task queue)

**WARNING-CH5-02**: Technical software citations needed
- LangGraph and PydanticAI referenced but not in paper corpus
- APA 7 format for software/documentation citations: Author/Organisation, Year, "Title", Version, URL
- Example: Lim, J. (2024). *LangGraph: Building stateful multi-actor applications with LLMs* (v0.1). LangChain. https://...

**WARNING-CH5-03**: "Confirm with supervisor: is a system architecture chapter standard for this programme?"
- For CBS Business Administration theses, a dedicated framework design chapter is less common than in Computer Science
- Supervisor should confirm whether Ch.5 (implementation detail level) is appropriate or should be condensed
- **Risk**: examiners from a Business Administration background may not engage deeply with system architecture — ensure the business value of each design choice is prominent

---

### Ch.6 Model Benchmark

**STATUS: ✅ Structurally compliant (results pending data)**

CBS requirement check:
- ✅ Five models described with justifications
- ✅ Evaluation metrics defined with rationale
- ✅ Experimental setup documented
- ✅ Connection to SRQs explicit

**WARNING-CH6-01**: Results section is empty (data-dependent — acknowledged)
- This is acceptable at skeleton stage
- CBS assessment will require actual numbers — plan to complete section 6.5 as the FIRST section filled in once data access is obtained

**WARNING-CH6-02**: MAPE target "≤15% (industry benchmark)" — citation needed
- Section 6.4 states this target but cites "cite ML-Based FMCG 2024" — this must be the Springer LNCS 2024 paper (ml_fmcg_demand_forecasting.md) OR the MDPI Applied Sciences 2024 paper
- Verify which paper supports the 15% MAPE claim specifically

---

### Ch.7 Synthesis (SRQ2 + SRQ3)

**STATUS: ✅ Structurally strong**

CBS requirement check:
- ✅ SRQ2 operationalised (5-step pipeline maps to the SRQ)
- ✅ LLM prompt templates documented (strong — CBS examiners will appreciate this transparency)
- ✅ Confidence score formula explicit
- ✅ Evaluation protocol documented (LLM-as-Judge)

**WARNING-CH7-01**: LLM prompt templates as primary research instruments
- The system prompt and user prompt in section 7.3 are research instruments — they define HOW the synthesis works
- CBS convention: primary instruments (questionnaires, interview guides) are typically in appendices, but referenced in the main chapter
- Recommendation: keep abbreviated prompt in Ch.7; put full versioned prompt in appendix (appendices don't count toward page limit)

**WARNING-CH7-02**: N=50 LLM-as-Judge sample — statistical adequacy
- Section 7.6 acknowledges the N=50 concern
- For Likert-scale data (1–5), N=50 provides limited statistical power for parametric tests
- **Action**: in the prose, justify N=50 by reference to comparable LLM evaluation literature OR increase to N=80–100 if API cost allows (~$0.25–$0.50 at current estimates)

**WARNING-CH7-03**: Temperature=0 reproducibility claim
- Section 7.2.2 states "Temperature: 0 (deterministic for reproducibility)"
- Note: temperature=0 is near-deterministic but not fully — Claude API documentation does not guarantee exact reproducibility across model updates
- **Action**: add a note that synthesis outputs are logged and reproducibility is bounded by model versioning; log model version alongside every synthesis output

---

### Ch.8 Evaluation

**STATUS: ✅ Methodologically rigorous skeleton**

CBS requirement check:
- ✅ Three-level evaluation framework documented
- ✅ Threats to validity table present (CBS assessment dimension)
- ✅ Connection to all 4 SRQs explicit
- ✅ Statistical tests identified (Diebold-Mariano)

**WARNING-CH8-01**: Human baseline comparison (N=20) depends on Manifold AI cooperation
- Section 8.3.3 requires a Manifold AI team member or category manager to produce manual recommendations
- This is external cooperation — CBS notes: "Deadline still applies even if cooperation delays"
- **Action**: contact Manifold AI early to schedule this evaluation; do not leave it until the last week

**WARNING-CH8-02**: Diebold-Mariano test implementation
- DM test is cited (section 8.2.2) but implementation note is absent
- For retail demand forecasting, DM test requires equal forecast horizon and same loss function — document this in the final chapter

**WARNING-CH8-03**: Empty results sections (data-dependent — acknowledged)
- All subsections titled "Expected results" are placeholders
- CBS examiners will assess whether the hypotheses are well-founded and whether the actual results are accurately interpreted — ensure hypotheses are based on literature, not guesses

---

### Ch.9 Discussion

**STATUS: ⚠️ Structurally appropriate but content-light (expected at skeleton stage)**

CBS requirement check:
- ✅ Interprets findings per SRQ (sections 9.1.1–9.1.4)
- ✅ Theoretical contributions section present (9.2)
- ✅ Practical implications present (9.3)
- ✅ Limitations section present (9.4 — CBS MANDATORY)
- ✅ Future research present (9.5)

**WARNING-CH9-01**: Design principles table missing
- Section 9.2.1 notes "Recommend design principles table for DSR framing" — this is strongly recommended
- A table of 5 design principles (from Ch.10 skeleton) structured as `{problem class, design principle, rationale, evidence from this thesis}` is the canonical DSR contribution format
- **Action**: draft the 5-principle table now (content in Ch.10 skeleton section 10.2) and add to Ch.9 skeleton

**WARNING-CH9-02**: Most content is placeholder ("Discuss…", "Connect to…")
- This is expected at bullet skeleton stage
- CBS Compliance Agent will need to re-run compliance once actual findings are available
- Re-run compliance check once data is available (Phase 2 compliance check)

---

### Ch.10 Conclusion

**STATUS: ❌ RQ version inconsistency**

CBS requirement check:
- ✅ Answers each SRQ (structure in place)
- ✅ 5 design principles listed
- ✅ Practical recommendations present
- ✅ Limitations recap present

**CRITICAL-CH10-01**: Main RQ wording inconsistency
- CLAUDE.md main RQ (v2, 2026-03-14): *"How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?"*
- Ch.10 section 10.1 main RQ: *"To what extent can a multi-agent AI framework combining LLM orchestration with lightweight ML ensemble forecasting improve demand forecast accuracy and decision quality for FMCG retailers operating under real-world computational constraints?"*
- These are DIFFERENT research questions — different framing ("How can AI systems be designed..." vs "To what extent can a multi-agent AI framework..."), different scope
- The "How" version is a design question (DSR-compatible); the "To what extent" version is an evaluative question (better for explanatory study)
- **Action required**: align with supervisor and co-author on the FINAL main RQ; update both CLAUDE.md and all chapter references to use the same wording consistently

**WARNING-CH10-01**: Executive summary before Ch.1
- Section "outstanding decisions" mentions: "whether to include a one-page executive summary before Ch.1"
- CBS: only the abstract is mandatory before the body — executive summaries are not a CBS convention for master theses; omit unless supervisor specifically recommends it

**WARNING-CH10-02**: Design principle 3 needs citation refinement
- "Consumer signal integration principle" cites "survey-derived consumer segments are a viable proxy where transaction loyalty data is unavailable"
- The prediction_intervals_planning.md (EJOR 2010) and customer_segmentation_sales_prediction.md (2023) are the relevant citations
- Ensure this principle is grounded in the thesis's own empirical findings (Ch.8 results), not stated as a prior claim

---

## PRIORITY ACTION LIST

### Immediate (before next session):
1. **Fix character count definition** in `frontpage.md`: change "Characters (no spaces)" to "Characters (including spaces)" — CBS standard is 2,275 chars INCL. spaces
2. **Create abstract skeleton** in `docs/thesis/sections/abstract.md`
3. **Draft AI use declaration** — confirm with supervisor where it should appear

### Before prose writing begins:
4. **Confirm DSR acceptance** with CBS supervisor — risk flag for Ch.3
5. **Align main RQ wording** across CLAUDE.md, Ch.1, and Ch.10 — critical for assessment coherence
6. **Confirm programme language** (Danish vs English) — affects title requirements (Danish + English required for Danish programme)
7. **Initiate Nielsen confidentiality agreement** with Manifold AI — CBS compliance-gated
8. **Add design principles table** to Ch.9 skeleton (content already in Ch.10)

### Before submission:
9. **All papers cited in APA 7 format** — currently all by descriptor
10. **Add GDPR note** to Ch.3 (Indeks Danmark secondary use)
11. **Add architecture diagram** to Ch.5 (Diagram Agent output)
12. **Tier 1 paper annotations required** to complete Ch.2 (Toolformer, ART, LangGraph, etc.)
13. **Re-run compliance check** once data is available and results sections are populated

---

## Page Budget Check

| Chapter | Target pages | Target characters (incl. spaces) |
|---|---|---|
| Abstract | 1 | 2,275 |
| Ch.1 Introduction | 8 | 18,200 |
| Ch.2 Literature Review | 20 | 45,500 |
| Ch.3 Methodology | 12 | 27,300 |
| Ch.4 Data Assessment | 9 | 20,475 |
| Ch.5 Framework Design | 15 | 34,125 |
| Ch.6 Model Benchmark | 15 | 34,125 |
| Ch.7 Synthesis | 12 | 27,300 |
| Ch.8 Evaluation | 15 | 34,125 |
| Ch.9 Discussion | 8 | 18,200 |
| Ch.10 Conclusion | 5 | 11,375 |
| **TOTAL** | **120 pages** | **273,000 characters** |

✅ **WITHIN BUDGET**: Ch.4 reduced from 10 to 9 pages (2026-03-15). Total is exactly 120 pages.
Note: the abstract (1 page) counts, but the front page, bibliography, and appendices do NOT count.

---

*Report generated by CBS Compliance Agent — 2026-03-15*
*Next check: after empirical results are available (Phase 2 compliance)*
