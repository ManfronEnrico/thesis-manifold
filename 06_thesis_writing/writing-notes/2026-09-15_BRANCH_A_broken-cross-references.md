---
name: 2026-09-15_BRANCH_A_broken-cross-references
description: PASS - Nine broken Word cross-references that render as 0, each traced to the section it was pointing at. One is a collapsed chapter heading, not a reference. Anchored, with the repair for each.
category: workflow
applies-to: [ch1_introduction, ch3_methodology, ch4_data_assessment, ch5_model_benchmark, ch6_architecture]
triggers: [broken cross-reference, renders as 0, REF error, bookmark]
created: 2026_09_15-15_20
updated: 2026_09_15-15_20
snapshot: 2026-09-15_15-10_broken-cross-references
status: prose ready to paste, awaiting human review
---

# Nine broken cross-references, and what each pointed at

Verified at `83689d3`, fetch clean, nothing incoming. Snapshot
`2026-09-15_15-10_broken-cross-references` — 47,650 words, **3 comment threads**
(down from 10). Zotero: 93 items.

**A Word cross-reference whose target bookmark has been deleted renders as `0`.**
I swept all seventeen chapter files. **Nine are real. Everything else containing a
zero is legitimate** — see the exclusion list at the end, so nobody re-derives it.

⚠ **F1 is not a cross-reference.** It is a chapter heading that collapsed, and it
needs a different repair from the other eight.

---

# How to fix these in Word, once

**Do not type the numbers in as plain text.** A hardcoded "Chapter 8" is a
cross-reference that can never update, and this document has already renumbered
its chapters once (Ch5 and Ch6 swapped on 2026-09-08), which is what broke these
in the first place.

**For each one:** select the `0`, then **Insert → Cross-reference**, choose
*Heading* as the reference type, pick the target named below, and insert it as
*Heading number* (for a section) or the heading text (for a chapter). Then
**Ctrl+A, F9** to refresh every field in the document.

---

# F1 — ⚠ Ch1 §1.5, a collapsed chapter heading

**This is the most visible one: it breaks the chapter map on the first page a
reader uses to navigate.**

### What it looks like now

Every sibling entry reads `**Chapter N** **| Title** description...`. The
Chapter 6 entry has split into two lines, with the label replaced by a bare zero:

> **0**
>
> **| Predictive-Extension** Architecture  describes the predictive-extension architecture: the forecasting substrate, the structured forecast-tool interface and the bounded tool-using agentic layer...

### Anchor

**Chapter 1, Section 1.5 Thesis Structure**, between the **Chapter 5** entry
(*"...addresses SRQ1 through the empirical model benchmark"*) and the **Chapter 7**
entry (*"...addresses SRQ2 through the structured tool interface itself"*).

### Action

REPLACE the two lines — the `**0**` line and the `**| Predictive-Extension**
Architecture` line — with one line matching its siblings.

#### Replace with

> **Chapter 6**  **| Predictive-Extension Architecture**  describes the
> predictive-extension architecture: the forecasting substrate, the structured
> forecast-tool interface and the bounded tool-using agentic layer.

⚠ **Keep the rest of that entry's existing description** if it runs longer than
the line above — I have quoted only as far as the snapshot shows. **The repair is
the label and the line break, not the description.**

---

# F2 — Ch1 §1.3.2, the interface design reference

### Anchor

**Chapter 1, Section 1.3.2 SRQ2 – Structured Tool Interface**, first sentence
after the quoted research question:

> "SRQ2 motivates the design of a structured forecast-tool interface (0) and its realisation in a bounded tool-using agentic decision-support layer (Chapter 7)."

### Target

→ **Chapter 6, Section 6.4 — "The Structured Forecast-Tool Interface (SRQ2)"**

✅ **Confirmed:** §6.4 opens *"The interface is the mechanism by which a forecast
is exposed to the agentic layer, and is the locus of SRQ2."* That is the design;
Chapter 7 (already correctly referenced in the same sentence) is the realisation.

**After:**
> "SRQ2 motivates the design of a structured forecast-tool interface (Section 6.4)
> and its realisation in a bounded tool-using agentic decision-support layer
> (Chapter 7)."

---

# F3 — Ch3 §3.3, the beer exclusion ⚠ verify the target in Word

### Anchor

**Chapter 3, Section 3.3 Research Strategy:**

> "A fifth, beer, is present in the source and excluded, for the reasons given in 0."

### Target

→ ⚠ **Most likely the preceding paragraph of §3.3 itself.** Ch3 line 35 already
states the exclusion and its reasons, two paragraphs above this sentence.

⚠ **This is the one target I am not certain of**, because a reference pointing
two paragraphs up is unusual. **Check in Word what the original pointed at.**

**Two clean options, both better than the current state:**

**Option A — delete the reference, keep the sentence:**
> "A fifth, beer, is present in the source and excluded for the reasons given
> above."

**Option B — point at Chapter 4** if the fuller argument lives there:
> "A fifth, beer, is present in the source and excluded, for the reasons given in
> Chapter 4."

✅ **I recommend Option A.** §3.3 already carries the reasons, so a
cross-reference adds a hop for no information.

---

# F4 — Ch4 §4.1, the CSD worked example

### Anchor

**Chapter 4, Section 4.1 Overview and Data Strategy:**

> "Carbonated soft drinks (CSD) are assessed in full in Section 0 and are where the pipeline parameters are derived, being the longest and largest of the four panels."

### Target

→ **Section 4.2 — "Carbonated Soft Drinks (CSD) – Exploratory Analysis and
Derived Parameters"**

**After:**
> "Carbonated soft drinks (CSD) are assessed in full in Section 4.2 and are where
> the pipeline parameters are derived, being the longest and largest of the four
> panels."

---

# F5 — Ch4 §4.1, the generalisation test

### Anchor

**Same paragraph as F4**, the following sentence:

> "...because they differ systematically in scale, promotional structure and series length, they are what allows 0  to test whether one pooled model generalises across categories or whether category-specific models are required."

⚠ **Note the double space after the `0`.**

### Target

→ **Chapter 5, Section 5.6.4 — "Pooled versus per-category training"**

✅ That is the section that runs exactly this test.

**After:**
> "...they are what allows Section 5.6.4 to test whether one pooled model
> generalises across categories or whether category-specific models are required."

---

# F6, F7, F8 — Ch4 §4.2, three in one sentence

### Anchor

**Chapter 4, Section 4.2**, the paragraph beginning *"CSD is presented first and
in the greatest detail."* The final two sentences:

> "All four categories are processed through the same pipeline, trained and tuned independently, and carried into both the pooled-versus-specialised comparison of 0  and the scenario experiment of 0. The three categories reported in Section 0  are full members of the design..."

⚠ **Three broken references in two sentences**, each with a double space after
the zero.

### Targets

| # | Reference | Target |
|---|---|---|
| **F6** | "pooled-versus-specialised comparison of 0" | **Section 5.6.4** |
| **F7** | "the scenario experiment of 0" | **Chapter 8** |
| **F8** | "The three categories reported in Section 0" | **Section 4.2.6** |

✅ **F8 confirmed:** §4.2.6 is *"Per-category EDA - danskvand, energidrikke,
RTD"* — exactly the three categories.

**After:**
> "All four categories are processed through the same pipeline, trained and tuned
> independently, and carried into both the pooled-versus-specialised comparison of
> Section 5.6.4 and the scenario experiment of Chapter 8. The three categories
> reported in Section 4.2.6 are full members of the design..."

---

# F9 — Ch5 §5.1, the interpretability criterion

### Anchor

**Chapter 5, Section 5.1 Rationale for model selection:**

> "The third is interpretability sufficient to support the scenario comparison in 0, where a forecast must be explained as well as produced."

### Target

→ **Chapter 8** — the scenario comparison.

**After:**
> "The third is interpretability sufficient to support the scenario comparison in
> Chapter 8, where a forecast must be explained as well as produced."

---

# F10 — Ch5 §5.8, the SRQ3 table row

### Anchor

**Chapter 5, Section 5.8 Connection to SRQs**, inside **Table 18**, the SRQ3
row:

> "| SRQ3 | Not addressed here; integration readiness is argued in 0 |"

### Target

→ **Chapter 6, Section 6.6 — "Integration Readiness (SRQ3)"**

**After:**
> "| SRQ3 | Not addressed here; integration readiness is argued in Section 6.6 |"

⚠ **A cross-reference inside a table cell still updates with F9**, but check it
after the refresh — table fields are the ones most often missed.

---

# F11 — Ch6 §6.3, the engineered predictors

### Anchor

**Chapter 6, Section 6.3 The Forecasting Substrate (SRQ1)**, final sentence:

> "The gradient-boosted models consume the engineered predictors described in 0: autoregressive lags and rolling summaries, calendar position, promotional intensity..."

### Target

→ **Chapter 4, Section 4.3 — "Feature Engineering (forecasting substrate)"**

✅ Confirmed: §4.3 is where the admissible feature set is defined.

**After:**
> "The gradient-boosted models consume the engineered predictors described in
> Section 4.3: autoregressive lags and rolling summaries, calendar position,
> promotional intensity..."

---

# What I checked and excluded — do not re-derive this

**These contain a zero and are correct.** Listed so a later sweep does not
re-open them:

| Site | Text | Why it is fine |
|---|---|---|
| Ch4 §4.3, Table 4 | `Promotional share of units (clipped 0–1)` | a numeric range |
| Ch5 §5.5, Table 7 | `median(|y−ŷ|/y) over y > 0`, `undefined where y = 0` | metric definitions |
| Ch5 §5.5.1 | *"undefined against a zero actual"* | prose about zeros |
| Ch8 §8.3 | `Runs completed9999999...` | table digits concatenated by the exporter, not prose |
| Reference list | Hastie, Ma et al., Tashman entries | page and volume numbers |
| Ch6 §6.10 | summary paragraph | no bare zero present |

**Front matter is clean.** The Table of Contents, Table of Figures, Table of
Tables and Table of Appendices carry **no** broken references.

---

# After the repair

**Ctrl+A then F9** refreshes every field in the document. Then re-snapshot and
re-run this check:

```bash
grep -nE "(^|[^0-9.,%$])0([^0-9.,%]|$)" chapters/*.md
```

✅ **The nine repaired sites should disappear; the six excluded ones above should
remain.** That is the pass condition.

⚠ **Fix these before regenerating the Table of Contents**, since a TOC built over
broken bookmarks inherits the breakage.
