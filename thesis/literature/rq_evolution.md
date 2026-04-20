# RQ Evolution History
> Maintained by the Literature Review Agent
> Last updated: 2026-03-14

---

## Version 2 — Revised (2026-03-14, post ChatGPT structural revision)

### Main RQ
How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?

### Sub-RQs
- **SRQ1**: Which predictive modelling approaches provide the best balance between forecasting accuracy and computational efficiency under realistic cloud resource constraints?
- **SRQ2**: How can a multi-agent architecture coordinate predictive models and heterogeneous data signals to generate actionable managerial recommendations?
- **SRQ3**: To what extent does additional contextual information improve the predictive and decision-support capabilities of AI systems?
- **SRQ4**: How does the proposed predictive AI system compare to traditional descriptive analytics approaches used in business intelligence systems?

### What changed from v1
- Main RQ broadened: from "8GB RAM constraint" to "computational constraints in real-world environments" — more generalizable, less implementation-specific
- SRQ1: same intent, reframed as "balance between accuracy and efficiency" rather than specific memory threshold
- SRQ2: now explicitly mentions "heterogeneous data signals" — creates a clear role for Indeks Danmark alongside Nielsen
- SRQ3: entirely new — focuses on the contribution of contextual information (Indeks Danmark) to decision-support quality
- SRQ4: was SRQ3 in v1, now more explicit about "traditional descriptive analytics / BI systems" as the baseline

### Rationale
The revision shifts the thesis from a purely technical implementation toward a broader design-and-evaluation study of predictive AI decision-support systems. This strengthens academic contribution (design science), makes the Indeks Danmark dataset a first-class empirical contribution (not just secondary), and positions the comparison with descriptive analytics more explicitly.

---

## Version 1 — Initial Draft (2026-03-14)

### Main RQ
How can an AI agent transition from descriptive analytics to predictive decision-support in a resource-constrained cloud environment (8GB RAM)?

### Sub-RQs
- **SRQ1**: Which lightweight predictive models can be reliably deployed within an 8GB RAM budget without unacceptable accuracy degradation?
- **SRQ2**: How can a multi-indicator synthesis module aggregate predictions from heterogeneous models into a single, confidence-qualified managerial recommendation?
- **SRQ3**: What performance gains in predictive accuracy and decision quality does the proposed framework deliver relative to the current descriptive baseline? *(pending: Nielsen data access)*

### Status at retirement
Superseded by v2. Core intent preserved but framing broadened.

---

## RQ Consistency Status (2026-03-15)

| Location | Main RQ text | Status |
|---|---|---|
| CLAUDE.md | "How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?" | ✅ v2 canonical |
| Ch.1 skeleton | Same as CLAUDE.md | ✅ |
| Ch.10 skeleton | Was different ("To what extent can a multi-agent AI framework...") | ✅ Fixed 2026-03-15 |
| gap_analysis.md | Consistent | ✅ |

All RQ locations are now aligned on v2 canonical wording.

---

## Open RQ Questions (for Literature Review Agent)

- Does "contextual information" (SRQ3) need a more precise definition — e.g. consumer sentiment, demographic segments, macroeconomic signals? *(Current answer: feature enrichment via PCA+k-means on Indeks Danmark — this is specific enough for the empirical chapter)*
- Is "computational constraints" in the main RQ specific enough for CBS examiners, or should it reference a concrete threshold (e.g. ≤8GB)? *(Answer: keep broad in main RQ; operationalise as ≤8GB in delimitation — current structure handles this)*
- What is the standard academic term for the descriptive analytics baseline? *(Best answer from corpus: "descriptive Business Intelligence" — used in AI-enhanced BI 2025 and Design Principles ADR 2024)*
