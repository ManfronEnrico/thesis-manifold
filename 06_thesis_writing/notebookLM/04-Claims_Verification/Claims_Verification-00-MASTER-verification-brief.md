---
name: claims-verification-brief
description: NotebookLM briefing pack - five claims that entered the thesis WITHOUT a source. Unlike the literature and methodology runs, these have no known source to check against; the task is to find one or confirm none exists.
created: 2026_09_07-10_00
updated: 2026_09_07-10_00
---

# Claims Verification - Sourcing Brief

**For NotebookLM.** This run differs from the other three in this folder, and the
difference changes what a good answer looks like.

| Run | Starting point | Question |
|---|---|---|
| 01-Literature_Review | 36 papers, each supporting a claim | Does the paper say what we say it says? |
| 02-Methodology_Review | One framework (Saunders) two chapters rest on | Is the framework applied as its author defines it? |
| **04-Claims_Verification** | **Five claims with NO source at all** | **Does a citable source exist - and if not, say so** |

Every claim below was written into the project from memory or convention. None was
checked. One (CV-01) was written with a fabricated attribution that has since been
removed. They are quarantined here until each is either sourced or reworded.

**"No source exists" is a first-class answer.** Several of these are probably
conventions with no clean origin, and confirming that is a real result - it tells us to
reword rather than to keep hunting. Do not manufacture a citation to fill a gap.

---

## YOUR TASK

For every claim, return:

```
### <ID> - <short title>
**Verdict:** Sourced | Partially Sourced | No Source Found | Contradicted
**Source:** <full citation, or "none found">
**Verbatim quote:** "<exact words from the source>"
**Page/section:** <locator>
**Analysis:** <does the source support the claim as stated, or only a weaker version?>
**Recommended wording:** <thesis-ready sentence, with or without citation>
```

Four rules:

1. **Quote, never paraphrase.** A paraphrase cannot settle whether a threshold is a
   convention or a rule.
2. **Distinguish "widely used" from "established".** Several of these are rules of
   thumb repeated across textbooks with no traceable origin. That distinction is the
   whole point: a rule of thumb may be *reported* as one, but must not be presented as
   a standard.
3. **Prefer a primary source.** A textbook citing a threshold is weaker than the paper
   that proposed it. If only textbooks are available, say so.
4. **If the claim is true but the specifics are wrong** (e.g. right law, wrong year),
   correct the specifics and quote the correction.

---

## PART 1 - Statistical thresholds (CV-01, CV-02)

These two matter most: both are *numeric cut-offs* that appear in a results appendix.
A number presented as a standard, without a standard behind it, is the failure this
whole exercise exists to catch.

### CV-01 - VIF thresholds of 5 and 10

**The claim as it entered the project:**
> Variance Inflation Factor above 10 indicates serious multicollinearity; above 5 is a
> stricter cut-off.

**Where it entered:** `srq1_feature_diagnostics.py`, as constants with an explanatory
comment.

**Its history - read this, it is the reason this folder exists.** The comment originally
attributed these thresholds to **Hair et al. (2019), Multivariate Data Analysis**. That
attribution was written **from memory**. The source is not in the project Zotero
library, was never opened, and could not be checked. It has been removed from the code.

**What to determine:**
1. Does a citable source state a VIF threshold of 10? Of 5?
2. Is it presented as a **rule of thumb** or as a **derived criterion**?
3. Does Hair et al. actually contain this, or was the attribution wrong as well as
   unverified?
4. Is there a primary source earlier than the textbooks?

**Why it matters here:** appendix table 97 reports VIFs including several infinite
values. The caption currently asserts **no threshold at all** - deliberately. If no
source is found, that is the permanent state and the bands stay out of the prose.

---

### CV-02 - Spearman |rho| >= 0.95 as a redundancy cluster boundary

**The claim as it entered the project:**
> A Spearman rank correlation of 0.95 or above defines a redundancy cluster between
> features.

**Where it entered:** `srq1_feature_diagnostics.py::REDUNDANCY_RHO`.

**Status: this one never had a source, not even a remembered one.** It was chosen.

**What to determine:**
1. Is 0.95 used as a redundancy threshold anywhere in the feature-selection literature?
2. Is there a *conventional* value (0.9? 0.8?) that is actually attested?
3. Is threshold-based redundancy clustering itself a recognised method, or is the
   defensible framing "an arbitrary reporting parameter"?

**Note for the answer:** the honest fallback is already written and acceptable - describe
it as a chosen reporting parameter and show a sensitivity check at 0.90 and 0.99. Only
displace that if a real convention exists.

---

## PART 2 - Domain fact (CV-03)

### CV-03 - Danish shop-opening law ("Lukkeloven liberalised in 2012")

**The claim as it entered the project:**
> Danish retail is open at weekends because Lukkeloven was liberalised in 2012, and many
> stores open on public holidays with reduced hours.

**Where it entered:** conversation, then `engineer_features.py::add_holiday_features`
docstring, then the enrichment writing note.

**Split this claim in two - they have different statuses:**

| Part | Status |
|---|---|
| Danish retail trades on weekends and often on public holidays | **Confirmed by the researcher** from domain knowledge. The feature design rests on this, and it is not in doubt. |
| The statute is named *Lukkeloven* and was liberalised in **2012** | **Unverified.** Both the name and the year came from Claude. |

**What to determine:**
1. What is the correct name of the Danish shop-opening-hours law?
2. When was it liberalised, and in what steps? (A staged liberalisation would make a
   single year wrong even if 2012 is one of the steps.)
3. Does it regulate public holidays differently from Sundays?

**Why it matters:** this justifies naming the feature `non_holiday_days` rather than
`selling_days` or `trading_days` - the point being that a Danish public holiday is *not*
a closed day. The reasoning survives without the statute; only the specifics need
sourcing or removal.

---

## PART 3 - Technical mechanism (CV-04)

### CV-04 - Why XGBoost is not reproducible across thread counts

**The claim as it entered the project:**
> XGBoost histogram building sums gradient statistics per thread and reduces them in
> completion order. Floating-point addition is not associative, so a different thread
> count produces a different sum, a different split, and a different tree - even with
> the seed, data and hyperparameters identical.

**Where it entered:** `srq1_benchmark.py::XGB_N_JOBS` comment; plan finding F18.

**Read the split carefully - it is unusual and it changes the task.**

| Part | Status |
|---|---|
| **The effect** | **MEASURED IN THIS PROJECT AND REPRODUCIBLE.** Holding seed, data and hyperparameters constant and varying only thread count: n_jobs 1 -> WMAPE 34.648708 (repeatable), 2 -> 34.946778, 4 -> 35.397904, 8 -> 37.297544. This evidence stands on its own and needs no citation. |
| **The explanation** | **UNSOURCED.** The non-associative-float-reduction mechanism is Claude reasoning from general knowledge. No XGBoost reference was consulted. |

**What to determine:**
1. Does XGBoost documentation address determinism and thread count?
2. Is the stated mechanism (order of parallel floating-point reduction) the documented
   cause, or is something else responsible - e.g. thread-dependent sketching or
   histogram binning?
3. Is there a known and documented setting that guarantees determinism other than
   single-threading?

**Why it matters:** the thesis reports this as a methods finding. Reporting a *measured*
effect is safe. Asserting an unverified *cause* is not - and the fix would be a single
hedged clause, so this is cheap to get right.

---

## PART 4 - Prior claim already flagged (CV-05)

### CV-05 - Store Bededag abolition

**The claim as it entered the project:**
> Store Bededag was abolished as a Danish public holiday from 2024, reducing the count
> from 15 to 14.

**Status:** the *effect* is directly visible in the fetched Nager.Date calendar - appendix
table 91 shows the count dropping, which is data, not assertion. **The bill number and
the parliamentary process are unverified.**

**What to determine:**
1. The correct legislative reference for the abolition.
2. The exact effective date.
3. Whether any transitional provision affected 2023.

**Why it matters:** this is the strongest substantive argument for the whole enrichment
- a permanent mid-panel structural break that `month` cannot represent. It deserves an
exact citation.

---

## Summary table

| ID | Claim | Kind | Fallback if no source |
|---|---|---|---|
| CV-01 | VIF 5 / 10 | Statistical threshold | Report VIFs, assert no threshold (current state) |
| CV-02 | Spearman >= 0.95 | Chosen parameter | Call it arbitrary; add sensitivity check |
| CV-03 | Lukkeloven 2012 | Domain fact | Keep "trades weekends", drop statute and year |
| CV-04 | XGBoost thread determinism | Technical mechanism | Report the measurement; hedge the cause |
| CV-05 | Store Bededag abolition | Legislative fact | Cite the calendar data; drop bill specifics |
