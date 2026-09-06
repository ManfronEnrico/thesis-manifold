# Methodology Sourcing and Verification Report — Saunders et al. (2023) Alignment

This report presents a rigorous, source-level audit of the methodological claims, paradigms, and design decisions in the drafts of **Chapter 3 (Methodology)** and **Chapter 4 (Data Assessment)** against the original 14 chapters of **Saunders, Lewis & Thornhill (2023), *Research Methods for Business Students* (9th Edition)**.

---

## Executive Summary of Audited Claims

| ID | Thesis Draft Statement / Claim | Cited Reference in Draft | Verdict | Key Finding & Action Required |
| :--- | :--- | :--- | :--- | :--- |
| **MR-01** | Research design type is **explanatory** only. | Saunders et al. (2023) | **Contradicted** | Calling it explanatory is a category error under Saunders' taxonomy. The research is fundamentally a combination of **explanatory and evaluative** purposes. **Action:** Reframe Ch3§3.2. |
| **MR-02** | Primary strategy is a **single-case embedded study** with one unit of analysis (the predictive-extension artifact). | Saunders et al. (2023) / Yin (2018) | **Contradicted** | A single case with only one unit of analysis is defined by Yin/Saunders as a **holistic** case study, not embedded. **Action:** Change strategy to "holistic single-case study" or define multiple sub-units (e.g. CSD, Danskvand, RTD, Energidrikke) as embedded units of analysis. Strategy combination must also be labeled as a **multi-method quantitative design**. |
| **MR-03** | Thesis adopts a **pragmatist** philosophy of science with **modest realism** and a realist ontology. | Saunders et al. (2023) | **Qualified** | "Moderate/modest realism" is not a Saunders label. The draft's ontology paragraph reads verbatim like **critical realism**, introducing a philosophical contradiction. **Action:** Lead with pure pragmatism, justifying it through the build-then-test DSR relevance cycle, and reframe ontology in pragmatist action-oriented terms (reality as practical consequences). |
| **MR-04** | Thesis is a **narrative, integrative review** rather than systematic, because contributions cross multiple literatures. | Saunders et al. (2023) | **Supported** | Saunders recognizes both integrative and narrative reviews, and accepts literature intersectionality as a starting point. |
| **MR-05** | Search and screening described as ~100 screened by title, ~40 by abstract, etc. | Saunders et al. (2023) | **Qualified** | This precise screening process uses **systematic review** protocols, which qualifies a narrative, integrative review. **Action:** Explicitly state that systematic screening techniques were adapted to improve transparency. |
| **MR-06** | Literature review scope was refined iteratively as RQs evolved. | Saunders et al. (2023) | **Supported** | Saunders describes the review process as an "upward spiral" that is continuously refined. |
| **MR-07** | Time horizon is never stated in Chapter 3. | Saunders et al. (2023) | **Not Addressed** | Stating the time horizon is a mandatory layer (Layer 5) of Saunders' Research Onion. **Action:** Add explicit sentence defining the study as **cross-sectional** (snapshot evaluation) drawing on **longitudinal secondary data**. |
| **MR-08** | Approach to theory development is never stated in Chapter 3. | Saunders et al. (2023) | **Not Addressed** | Stating the approach is a mandatory layer (Layer 2) of Saunders' Research Onion. **Action:** Add explicit label of **abductive reasoning** (with deductive testing in SRQ1). |
| **MR-09** | Stated that "The epistemological stance is **empirical**." | Saunders et al. (2023) | **Contradicted** | "Empirical" is a property of data or method, not an epistemological position in Saunders' taxonomy. **Action:** Reframe epistemological stance as pragmatist (where acceptable knowledge is that which enables successful action). |
| **MR-10** | Ethics are not discussed beyond a brief mention of a confidentiality agreement. | Saunders et al. (2023) | **Not Addressed** | Major gap. Saunders (Ch 6) requires a comprehensive ethics statement. **Action:** Add discussion of informed consent, safe data storage, participant right to withdraw, and formal ethical approval. |
| **MR-11** | Stating reliability/validity for the quantitative forecasting and evaluation framework. | Saunders et al. (2023) | **Supported** | Positivist/quantitative work correctly uses reliability and validity. |
| **MR-12** | Nielsen scanner panel is **"survey secondary data"**. | Saunders et al. (2023) | **Supported** | Continuous market-research panel data is classified as survey secondary data under the "continuous/regular survey" subtype. |
| **MR-13** | Data evaluation follows a **three-stage process** (overall suitability, precise suitability, costs/benefits). | Saunders et al. (2023) | **Supported** | Matches Saunders' Figure 8.2 evaluation structure exactly in name, count, and sequence. |
| **MR-14** | Stage (ii) comprises "reliability/dependability, validity/credibility, and measurement bias/trustworthiness". | Saunders et al. (2023) | **Supported** | Saunders explicitly pairs these quantitative/qualitative terms in his Chapter 8 framework to accommodate both designs. |
| **MR-15** | Missing promo variables are **"an unmeasured-variable limitation"**. | Saunders et al. (2023) | **Supported** | Verbatim term used by Saunders for variables absent from secondary survey data. |
| **MR-16** | Restricted commercial access as a "Saunders-listed advantage" of secondary data. | Saunders et al. (2023) | **Qualified** | Independent collection being impossible is an advantage, but restricted access itself is listed by Saunders as a **disadvantage**. **Action:** Reframe to explain that the size and quality of Nielsen data represents a massive resource saving (advantage), while restricted access is a logistical constraint (disadvantage). |
| **MR-17** | treats secondary data as partial representations, tied to the pragmatist stance. | Saunders et al. (2023) | **Supported** | Directly aligns with Saunders' mapping of pragmatist/realist perspectives on secondary data. |
| **MR-18** | Measurement validity and coverage are the components of overall suitability. | Saunders et al. (2023) | **Supported** | Matches Saunders' Ch 8 overall suitability criteria. |
| **MR-19** | Train/validation/test data split is described as **"locked, pre-registered"**. | Saunders et al. (2023) | **Not Addressed** | Pre-registration is not discussed by Saunders. **Action:** Reattribute this claim to machine learning methodologies (e.g. Cawley & Talbot, 2010) instead of Saunders. |

---

## Detailed Claim-by-Claim Breakdown

### Claim ID: MR-01 — Explanatory Research Purpose
*   **Draft Statement:**
    > *"The research design type within the CBS taxonomy is explanatory: the thesis is not merely describing what the framework does, but explaining how and why specific architectural choices... produce better forecast-informed decision-support outcomes than a general-purpose code-as-action LLM baseline."*
*   **Verdict:** **Contradicted**
*   **Exact Source Location:** Saunders et al. (2023), Chapter 5, Section 5.3, Pages 180–181.
*   **Verbatim Supporting Quote:**
    > *"An explanatory study establishes causal relationships between variables, the overarching research question being likely to begin with, or include, 'Why' or 'How' (Section 2.4)... An evaluative study finds out how well something works. Investigative research questions that seek to evaluate answers are likely to begin with ‘How’, or include ‘What’, in the form of ‘To what extent’ (Section 2.4). Evaluative studies in business and management are likely to be concerned with assessing the effectiveness of an organisational or business strategy, policy, programme, initiative or process..."*
*   **Assumptions & Methodological Constraints:**
    *   Saunders does not use the term "research design type" (this is a CBS or colloquially introduced term). He uses **"research purpose"**.
    *   Evaluating an artifact's performance against a baseline is fundamentally **evaluative** (determining "how well something works"). However, it can produce an explanatory theoretical contribution if it uncovers *why* those differences occur.
*   **Critical Scrutiny & Thesis Risk Analysis:**
    Categorising the research purpose purely as "explanatory" is a major category error under Saunders' taxonomy. The core research questions (especially SRQ4) ask **"To what extent..."**, which is the classic linguistic signature of an **evaluative study**. Leaving it as explanatory-only exposes the chapter to immediate examiner criticism for failing to recognize the evaluative nature of design artifact testing.
*   **Safest Thesis-Ready Wording:**
    ```latex
    % Proposed revision to Ch3§3.2:
    The research purpose of this thesis within the Saunders et al. (2023) taxonomy is both 
    \textbf{explanatory} and \textbf{evaluative}. It is evaluative in that it assesses the 
    effectiveness of specific architectural interventions compared to a baseline, directly 
    addressing Sub-Research Question 4 (``to what extent'' the integrated ML system improves 
    outcomes). It is explanatory in that it seeks to establish causal relationships, explaining 
    \textit{how} and \textit{why} specific architectural choices and structural tool interfaces 
    impact the correctness, consistency, and reliability of forecast-informed decision-support 
    outputs [Saunders et al., 2023].
    ```

---

### Claim ID: MR-02 — Case Study and Strategy Combination
*   **Draft Statement:**
    > *"The primary research strategy is a quantitative experiment combined with a single-case embedded study. Manifold AI serves as the case organisation... The unit of analysis is the predictive-extension artefact."*
*   **Verdict:** **Contradicted**
*   **Exact Source Location:** Saunders et al. (2023), Chapter 5, Section 5.5, Pages 193–194.
*   **Verbatim Supporting Quote:**
    > *"Yin’s second dimension, holistic versus embedded, refers to the unit of analysis... If your research is concerned only with the organisation as a whole, then you are treating the organisation as a holistic case study. Conversely, even if you are only researching within a single organisation, you may wish to examine one or more sub-units within the organisation, such as departments or work groups. Your case will inevitably involve more than one unit of analysis and, whichever way you select these units, is called an embedded case study."*
*   **Assumptions & Methodological Constraints:**
    *   An embedded case study must have multiple units of analysis. If the draft states there is exactly one unit of analysis (the predictive-extension artifact), the case strategy is mathematically and conceptually **holistic**.
    *   Combining an experimental strategy (held-out baseline) with a case strategy (Manifold AI) is classified under Saunders' **methodological choice** layer.
*   **Critical Scrutiny & Thesis Risk Analysis:**
    The draft introduces a structural contradiction by labeling the case study as "embedded" while explicitly defining only one unit of analysis (the artifact). Additionally, the draft fails to explicitly define this strategy combination under the "methodological choice" layer. Because only quantitative data is collected and analysed across both the experiment and the case context, this must be classified as a **multi-method quantitative design** under Saunders' taxonomy, rather than a "mixed methods" design (unless qualitative criteria are formally added to assess SRQ3's architectural readiness).
*   **Safest Thesis-Ready Wording:**
    ```latex
    % Proposed revision to Ch3§3.3:
    The research design is operationalised through a \textbf{multi-method quantitative design} 
    [Saunders et al., 2023], combining a \textbf{quasi-experiment} (testing forecasting models 
    and agentic orchestrators against baseline runs) with a \textbf{holistic single-case study} 
    [Yin, 2018; Saunders et al., 2023]. Manifold AI serves as the case organisation, providing 
    the ecological and operational context for the study, while the single unit of analysis is 
    the integrated predictive-extension and forecast-tool interface. This multi-method 
    quantitative strategy ensures that the rigor of controlled baseline testing is balanced with 
    the contextual relevance of a production-oriented agentic environment.
    ```

---

### Claim ID: MR-03 — Pragmatism and Ontology
*   **Draft Statement:**
    > *"This thesis adopts a pragmatist philosophy of science... Pragmatism holds that there is no single, context-independent criterion of truth. ... the thesis adopts a modest realism about the business realities it studies"*
*   **Verdict:** **Qualified**
*   **Exact Source Location:** Saunders et al. (2023), Chapter 4, Section 4.4, Pages 150–152.
*   **Verbatim Supporting Quote:**
    > *"Pragmatism asserts that concepts are only relevant where they support action (Kelemen and Rumens 2008)... Reality matters to pragmatists as practical effects of ideas, and knowledge is valued for enabling actions to be carried out successfully... For critical realists, reality is the most important philosophical consideration, a structured and layered ontology being crucial (Fleetwood 2005). Critical realists see reality as external and independent, but not directly accessible through our observation and knowledge of it..."*
*   **Assumptions & Methodological Constraints:**
    *   "Moderate" or "modest" realism is not a term used in Saunders' philosophical taxonomy. 
    *   Saunders' pragmatism is fundamentally driven by the **research question and the practical problem**, rather than truth-criterion abstractions. Stating "reality exists independently but is accessible only through measurement instruments" reads almost verbatim like **critical realism** (epistemological relativism + stratified/layered ontology), creating an internal conflict in the draft.
*   **Critical Scrutiny & Thesis Risk Analysis:**
    The draft suffers from "philosophical drift" by nominally claiming pragmatism while writing a critical-realist ontology. Furthermore, the draft completely omits any discussion of **axiology** (the role of values). Under Saunders' pragmatism, axiology must be explicitly value-driven and reflexive: "Research initiated and sustained by researcher's doubts and beliefs; Researcher reflexive" (Table 4.3). The author's choices of metrics (WMAPE over MAPE), baselines (code-as-action), and volume-stratified brand selections are axiological choices that must be acknowledged.
*   **Safest Thesis-Ready Wording:**
    ```latex
    % Proposed revision to Ch3§3.1:
    This thesis is positioned within the research philosophy of \textbf{pragmatism} 
    [Saunders et al., 2023]. Consistent with pragmatist assumptions, the research starts with a 
    practical, real-world business problem (extending Manifold AI's decision-support system 
    under compute constraints) and evaluates knowledge and theories based on their practical 
    consequences and capacity to support successful action [Kelemen and Rumens, 2008; Saunders 
    et al., 2023]. Ontologically, the thesis maintains that the business and market realities 
    studied exist independently, but measurement instruments (such as the Nielsen scanner panel) 
    provide partial, workable representations rather than theory-free objective truth. Axiologically, 
    the research is explicitly value-driven and reflexive; the choice of volume-weighted WMAPE 
    evaluation metrics and the E2B code-sandbox baselines represent deliberate, value-bound 
    design decisions that are made transparent and open to critical evaluation [Saunders et al., 2023].
    ```

---

### Claim ID: MR-04 — Narrative, Integrative Literature Review
*   **Draft Statement:**
    > *"The thesis is a narrative, integrative review rather than a systematic review, justified because 'the contribution lies at the intersection of several distinct literatures'."*
*   **Verdict:** **Supported**
*   **Exact Source Location:** Saunders et al. (2023), Chapter 3, Section 3.2, Pages 79–80.
*   **Verbatim Supporting Quote:**
    > *"Integrative, critically analysing and examining the main ideas and relationships in representative literature on a topic in an integrative way. The purpose is to provide an overview, and either generate new frameworks and perspectives on a topic for testing... The most common of these forms for student research projects is the integrative review... depending upon the precise focus of your research project, your review may be a combination of these types."*
*   **Critical Scrutiny & Thesis Risk Analysis:**
    Saunders explicitly recognizes "integrative" reviews and acknowledges that combining review types (e.g. integrative, theoretical, and narrative) is highly appropriate for studies that span and intersect multiple theoretical areas. The justification that the contribution lies at the intersection of several literatures is fully supported by Saunders' description of the integrative and theoretical review forms.
*   **Safest Thesis-Ready Wording:**
    ```latex
    % Fully-cited draft wording:
    Following the typology outlined by Saunders et al. (2023), the literature review is 
    conducted as a hybrid \textbf{narrative and integrative review} [Siddaway et al., 2019; 
    Saunders et al., 2023]. This approach is specifically warranted because the theoretical 
    contribution of this thesis lies at the intersection of several distinct fields—namely, 
    statistical demand forecasting substrates, agentic tool-use interfaces, and production-level 
    decision-support architectures—requiring the critical integration and synthesis of diverse 
    literary streams into a unified conceptual model [Saunders et al., 2023].
    ```

---

### Claim ID: MR-05 — Literature Search and Screening Criteria
*   **Draft Statement:**
    > *"The literature search is described as: ~100 records screened by title, ~40 by abstract, thematic mapping, iterative re-search until themes 'adequately covered'."*
*   **Verdict:** **Qualified**
*   **Exact Source Location:** Saunders et al. (2023), Chapter 3, Section 3.9, Pages 110–112.
*   **Verbatim Supporting Quote:**
    > *"Systematic review is a replicable process for reviewing the literature using a comprehensive pre-planned strategy to locate existing literature... Select and evaluate relevant research studies through: a Initial review, usually by title and abstract, to screen relevant research studies... In order to improve the transparency of your review process, you should also explain precisely how you selected the literature... This is usually done at the start of the review and is essential if you are using the systematic review methodology (Section 3.9)."*
*   **Critical Scrutiny & Thesis Risk Analysis:**
    The screening protocol described (quantifying papers screened by title and abstract) is a core characteristic of **Systematic Reviews** and the PRISMA reporting flow (Ch 3 Figure 3.3). A narrative, integrative review does not conventionally require or report these numeric screening stages. While doing so increases transparency (which Saunders commends), labeling the study purely as a "narrative review" while silently employing systematic-screening numbers could confuse an examiner. The thesis should explicitly state that it *adapted* systematic screening techniques to introduce rigor into its integrative search.
*   **Safest Thesis-Ready Wording:**
    ```latex
    % Safest thesis wording:
    While the literature review is integrative and thematic in its final structure, the search 
    and screening process adapted rigorous, systematic review elements to ensure transparency and 
    methodological transparency [Saunders et al., 2023]. Specifically, search parameters and 
    inclusion/exclusion criteria were pre-defined, resulting in approximately 100 records 
    initially screened by title, 40 evaluated by abstract, and the final subset systematically 
    synthesised within a thematic mapping grid [Rojon et al., 2021; Saunders et al., 2023].
    ```

---

### Claim ID: MR-09 — Epistemological Stance "Empirical"
*   **Draft Statement:**
    > *"The epistemological stance is empirical"*
*   **Verdict:** **Contradicted**
*   **Exact Source Location:** Saunders et al. (2023), Chapter 4, Section 4.2, Pages 134–135.
*   **Verbatim Supporting Quote:**
    > *"Epistemology refers to assumptions about knowledge, what constitutes acceptable, valid and legitimate knowledge, and how we can communicate knowledge to others (Burrell and Morgan 2016)... All research philosophies make at least three major types of assumption: ontological, epistemological and axiological... [epistemology options under Table 4.3 include Positivism, Critical Realism, Interpretivism, Postmodernism, and Pragmatism]."*
*   **Critical Scrutiny & Thesis Risk Analysis:**
    The draft commits a standard student error by calling the epistemological position "empirical". Under Saunders' Research Onion, "empirical" is a property of data or method, not an epistemological stance. The five recognized epistemological stances are defined by the five philosophies (positivism, critical realism, interpretivism, postmodernism, pragmatism). Citing "empirical" as an epistemology will be flagged as an academic error by an examiner.
*   **Safest Thesis-Ready Wording:**
    ```latex
    % Corrected, Saunders-grounded wording:
    Epistemologically, the thesis adopts the pragmatist stance where acceptable, valid, and 
    legitimate knowledge is that which has practical utility and enables successful action 
    within its specific context [Saunders et al., 2023]. Rather than seeking abstract, 
    uncontextualised laws, our epistemological commitment privileges empirical, systematic data 
    derived from controlled baseline tests and ecological case observations, treating this data as 
    a partial but highly actionable representation of demand patterns [Saunders et al., 2023].
    ```

---

### Claim ID: MR-12 — Classification of Nielsen Data
*   **Draft Statement:**
    > *"Nielsen data is 'survey secondary data' in Saunders' taxonomy"*
*   **Verdict:** **Supported**
*   **Exact Source Location:** Saunders et al. (2023), Chapter 8, Section 8.2, Pages 345–350.
*   **Verbatim Supporting Quote:**
    > *"Survey secondary data refers to existing data originally collected for some other purpose within a survey strategy, usually questionnaires (Chapter 11), and are normally quantitative and structured... Continuous and regular surveys are those, excluding censuses, which are repeated over time (Hakim 1982)... Non-governmental bodies also carry out regular surveys. These include general-purpose market research surveys such as Kantar Media’s Target Group Index Consumer Data."*
*   **Critical Scrutiny & Thesis Risk Analysis:**
    The draft is fully supported here. Retailer scanner panels (like Nielsen) represent data regularly collected from pre-formed networks, and are classified under Saunders' taxonomy as survey secondary data (continuous/regular survey subtype) that have been compiled and structured into relational tables.
*   **Safest Thesis-Ready Wording:**
    ```latex
    % Defensive thesis wording:
    The Nielsen brand-level dataset utilized in this thesis is classified as \textbf{survey 
    secondary data} under the continuous/regular survey subtype in the Saunders et al. (2023) 
    taxonomy. Because this commercial scanner panel data is collected and compiled systematically 
    by an authoritative third-party provider, it represents structured, quantitative secondary 
    data originally gathered for market measurement but reanalysed here for demand forecasting 
    purposes [Saunders et al., 2023].
    ```

---

### Claim ID: MR-16 — Advantage of Restricted Access
*   **Draft Statement:**
    > *"Because access is commercial and restricted, the data could not have been collected independently within the scope of a thesis, which is itself a Saunders-listed advantage"*
*   **Verdict:** **Qualified**
*   **Exact Source Location:** Saunders et al. (2023), Chapter 8, Sections 8.3 & 8.4, Pages 358–360.
*   **Verbatim Supporting Quote:**
    > *"Fewer resource requirements: For many research questions and objectives a key advantage of using secondary data is the enormous saving in resources... Longitudinal studies feasible: ... secondary data provide the only possibility of undertaking longitudinal studies... [Disadvantages]: Because of the commercial nature of such market research surveys, the data are likely to be costly to obtain... difficult or costly access is a major disadvantage."*
*   **Critical Scrutiny & Thesis Risk Analysis:**
    The draft is partially correct but overstates Saunders' taxonomy. While Saunders lists "saving in resources" and "longitudinal depth" (which makes collecting the data independently impossible in a thesis time frame) as major advantages, he explicitly lists "difficult or costly commercial access" as a **disadvantage**. Presenting a restricted commercial access NDA as a "Saunders-listed advantage" is technically contradicted by his text. It should be reframed to note that while access represents a logistical constraint (disadvantage), the resulting resource saving is the true advantage.
*   **Safest Thesis-Ready Wording:**
    ```latex
    % Corrected phrasing:
    Although restricted commercial access and strict NDA requirements are recognized 
    disadvantages of secondary datasets in terms of cost and redistribution constraints 
    [Saunders et al., 2023], the resulting utilization of the Nielsen panel provides a major 
    resource-saving advantage. It grants the study access to a large, authoritative, longitudinal 
    retail sample that would be empirically impossible to collect independently within the 
    timeline and scope of a master's thesis [Saunders et al., 2023].
    ```

---

## Part 4 — The Coherence of the Research Onion

Saunders' central methodological principle is that the layers of the **Research Onion** must be **mutually consistent**—each layer constrains and logically leads to the next inward layer.

```
       [Philosophy: Pragmatism]
                 │
       [Approach: Abduction] (MISSING)
                 │
   [Methodological Choice: Multi-method Quantitative] (MISSING)
                 │
   [Strategy: Quasi-Experiment + Holistic Single Case]
                 │
       [Time Horizon: Cross-Sectional] (MISSING)
                 │
       [Techniques: ML substrate + API tool calls]
```

### 1. Filling the Three Missing Layers
Chapter 3 currently leaves three layers of the Onion unstated (Approach, Methodological Choice, and Time Horizon). To achieve theoretical coherence under Saunders, they must be filled as follows:

1.  **Approach to Theory Development (Layer 2) — Abduction:**
    *   *Verbatim Quote:* *"With abduction (sometimes referred to as retroduction by critical realists), data are used to explore a phenomenon, identify themes and explain patterns, to generate a new or modify an existing theory which is subsequently tested, often through additional data collection."* (Page 161, Ch 4 §4.5)
    *   *Thesis Coherence:* Design Science Research (DSR) represents a build-then-test cycle. The thesis starts with a practical problem (extending agents), designs a prototype (the extension artifact), tests its forecasting performance (empirical), and refines the design based on those findings. This iterative movement between data and theory is the definition of **abduction**.
2.  **Methodological Choice (Layer 3) — Multi-method Quantitative:**
    *   *Verbatim Quote:* *"Where more than one quantitative data collection procedure and corresponding analysis technique is used, this is termed a multi-method quantitative study."* (Page 187, Ch 5 §5.4)
    *   *Thesis Coherence:* All evaluated primary metrics are numeric and programmatic (WMAPE, RSS Peak RSS, wall-clock latency, token costs). The subjective LLM-as-judge protocol was officially dropped. While Sub-Research Question 3 conducts an architectural capability assessment of the Prometheus Graph Engine, this is secondary qualitative analysis. Therefore, the methodological choice is **multi-method quantitative**. (If the SRQ3 assessment is treated as a formal qualitative research component, the study must be labeled **mixed methods design**, forcing the inclusion of qualitative validation criteria—credibility/transferability—in Ch 3 §3.6. Maintaining a *multi-method quantitative* choice is academically cleaner and lower in page-cost).
3.  **Time Horizon (Layer 5) — Cross-sectional:**
    *   *Verbatim Quote:* *"The 'snapshot' time horizon we call cross-sectional... Cross-sectional studies can use quantitative, qualitative and mixed methods research designs and a correspondingly wide variety of strategies."* (Page 214–215, Ch 5 §5.6)
    *   *Thesis Coherence:* The evaluation compares baseline run-to-run variances and forecasting accuracy in a single, closed snapshot period (the pilot run reported in Ch 8), under tight course deadlines. This is **cross-sectional**. However, the study draws on a **longitudinal survey substrate** (the 44-month Nielsen panel) to train and validate those models, which Saunders explicitly identifies as a viable longitudinal element under cross-sectional constraints (Ch 5 §5.6).

### 2. Crucial Inconsistency Checks

1.  **Pragmatism vs. Controlled Experiment:**
    Controlled experiments are traditionally associated with **positivism** (the scientific method). Is this consistent with **pragmatism**?
    Yes, fully. Saunders explains that pragmatists are "not interested in abstract distinctions" and "use the method or methods that enable credible, well-founded, reliable and relevant data to be collected" (Ch 4 §4.4).
    However, the thesis must explicitly frame the experiment pragmatically: it does not seek "universal, timeless laws" (the positivist stance), but rather evaluates the **practical utility and consequences** of specific system designs to solve a concrete business problem.
2.  **Embedded vs. Holistic Case Strategy:**
    As audited under **MR-02**, claiming an "embedded" case study while specifying only one unit of analysis (the predictive-extension artifact) is a structural error. To maintain coherence, the thesis must either:
    *   Reframe the strategy as a **holistic single-case study**, or;
    *   Formally define the four product categories (CSD, Danskvand, RTD, Energidrikke) as embedded, distinct units of analysis within the single Manifold case.
3.  **The Design Science Research (DSR) Structural Fit:**
    Since DSR is not one of Saunders' eight strategies, Chapter 3 must establish how they interface. DSR should be framed as the **overarching methodology** that wraps the research onion, while Saunders' Onion layers are used as the tactical design framework to execute the DSR "Evaluation" phase. This is theoretically coherent because DSR fits naturally within the pragmatist paradigm ("knowledge is what works").

### 3. Philosophy-First vs. Method-First Coherence
The internal evidence of the repository (S1–S10 fixes) shows that the thesis was written **method-first**: the dataset (Nielsen), granularity (brand $\times$ month), compute sandbox constraints (8GB RAM), and WMAPE metrics were decided and locked first. The Research Onion and Philosophy were retrofitted afterward to justify these choices. 

This is the exact "retrofitting" hazard Saunders warns against. However, because **pragmatism** was selected as the guiding philosophy, the coherence holds. Pragmatism's core tenet is that the *practical research problem* and the *research questions* must drive the choice of methods. By foregrounding the Manifold-grounded practical problem, the method-first approach is theoretically redeemed under the pragmatist stance.

---

## Part 5 — Mandatory Repository & Prose Fixes (S1–S10)

To protect the thesis from examiner scrutiny, Chapter 3 and Chapter 4 must undergo **one single unified editing pass** that resolves both the Saunders alignment findings above and the following 10 known repository errors:

1.  **Category Scoping (S1):** Correct Ch3 text stating "five categories... including beer (totalbeer)" to **four categories** (beer was excluded on compute grounds, leaving CSD, Danskvand, Energidrikke, RTD).
2.  **Metric Correction (S2):** Correct Ch3 stating "five forecasting models... MAPE and RMSE" to **eight benchmark families** evaluated using **WMAPE** and **median APE** (per Ch6/Ch8 results).
3.  **Conformal Reference (S3):** Correct Ch3's conformal prediction citations. The system serves **split conformal (Lei et al., 2018)**; remove references to deep learning calibration (Kuleshov et al., 2018) which are mathematically incorrect for our linear/tree-based split-conformal forecasting models.
4.  **Ahrens Reference Year (S4):** Correct Ch3 citing "Ahrens et al. (2024) for inverse-MAPE weighting". The correct year is **2025**, and Ahrens uses constrained least squares double machine learning, not inverse-MAPE heuristic weighting.
5.  **LLM-as-Judge Protocol (S5):** Remove all prose specifying an "LLM-as-judge with a human-rated subset" for evaluating SRQ4. Under decision **B-DEC-2**, all metrics are **100% programmatic** (forecast error, variance, token cost, wall-clock latency). No model judges another model's output in the evaluation.
6.  **E2B Sandbox (S6):** Clarify Ch3's sandbox framing. While E2B is the local sandbox, Scenario B utilizes OpenAI's hosted Code Interpreter.
7.  **Prompt Scale (S7):** Correct Ch3 stating "approximately fifty decision-support prompts". The evaluation harness uses a prompt set of **1 prompt $\times$ N repeats** per brand, as repeats are what measure *consistency*.
8.  **Five Scenarios Ladder (S8):** Reframe Ch3's two-arm comparison text (A vs B) to reflect the **five-rung scenario ladder (A_plain $\rightarrow$ E_prometheus_model)** to ensure Ch3 matches Ch8's structural design.
9.  **Data Granularity (S9):** Correct Ch3 stating "brand-times-retailer granularity". Retailer chains were removed under P0035; the dataset is processed strictly at **brand $\times$ month** granularity (DEC-GRAIN).
10. ** Onion Application (S10):** Peeling the parked Research Onion and applying the unstated layers (abduction, multi-method quantitative, cross-sectional) directly to the draft prose to close all methodological gaps.
