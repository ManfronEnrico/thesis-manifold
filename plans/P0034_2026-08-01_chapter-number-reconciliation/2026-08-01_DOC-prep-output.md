---
pid: P0034
created: 2026-08-01
updated: 2026-08-01
status: draft-for-approval
---

# P0034 — Preparation Output (Tasks 2, 3+4, 5, 8)

> **Nothing in this document has been applied.** No file under `05_thesis_writing/`
> was edited. Every "proposed" block below is a *proposal* awaiting Brian/Enrico
> approval per the task-9 gate. Replacement wording is drafted so it can be judged,
> not so it can be pasted unreviewed.

---

## Task 2 — Severity triage of every inventoried figure

### Class definitions

| Class | Meaning | Action once P0032/P0033/P0035 land |
|---|---|---|
| **WILL CHANGE** | CSD / energidrikke figures — directly leakage-affected by P0032's V3 fix | Must be re-read from the new S01 output. Assume every digit moves. |
| **MUST RE-VERIFY** | danskvand / RTD — promo-zero, so *expected* stable, but S01 retrains from scratch (new splits, new seeds, new feature set after promo-column changes). Not assumable. | Re-read and confirm; only leave unchanged if byte-identical. |
| **STRUCTURAL** | Depends on the brand×chain grain that DEC-GRAIN removes. Not a number swap — the table shape changes. | Rewrite the table, then re-populate. |
| **STABLE** | Not a function of the leakage fix or the grain decision. | Spot-check only. |
| **DERIVED** | Computed *from* other figures. Goes stale silently — no grep will catch it. | Recompute after all primaries settle. Never hand-carry. |

A figure can hold two classes (e.g. danskvand's 22.0% is both STRUCTURAL and MUST RE-VERIFY). Where that happens the more disruptive class is listed first.

### Triage table

| # | File:line | Current value | Class | Reason |
|---|---|---|---|---|
| 1 | `ch6:119` | CSD 16.5 / 20.8 / 39.9 | **STRUCTURAL** + WILL CHANGE | 20.8 is the brand×chain column (removed). 16.5 and 39.9 are CSD → leakage-affected. |
| 2 | `ch6:120` | danskvand 23.8 / **22.0** / 37.7 | **STRUCTURAL** + MUST RE-VERIFY | The bolded selection is the chain value. Losing chain flips the headline to 23.8 — see Task 5, this is the regression. |
| 3 | `ch6:121` | energidrikke 11.4 / 13.9 / 31.9 | **STRUCTURAL** + WILL CHANGE | 13.9 is chain (removed). 11.4 is the thesis's strongest claim and is energidrikke → leakage-affected. |
| 4 | `ch6:122` | RTD 31.0 / 38.8 / 58.8 | **STRUCTURAL** + MUST RE-VERIFY | 38.8 is chain (removed). 31.0 / 58.8 promo-zero but retrained. |
| 5 | `ch6:124` | "best in all **eight** (category × granularity) cells" | **STRUCTURAL** | 4 categories × 2 grains = 8. With chain gone it is four cells. A count embedded in prose, not a table — easy to miss. |
| 6 | `ch6:126` | "Optuna tuning improved WMAPE by roughly **2–4 pp**" | **DERIVED** + WILL CHANGE | Derived from tuned-vs-untuned deltas across all cells. Both the range endpoints and the cell population change (8 cells → 4). Recompute; do not carry. |
| 7 | `ch6:130–138` | §6.5.2 granularity-finding **prose** | **STRUCTURAL (prose, not table)** | The entire subsection's thesis is the brand×month vs brand×chain comparison. See Task 5 — this is more than a table edit. |
| 8 | `ch6:137` | "energidrikke reaches **11.4% WMAPE**, near the ≤15% industry target" | **WILL CHANGE** + **UNSOURCED** (Task 8) | Double exposure: the number moves *and* the yardstick has no source. |
| 9 | `ch6:146–147` | ARIMA: CSD 24.2, dv 33.4, ed 15.7, RTD 48.2 | WILL CHANGE (CSD/ed) + MUST RE-VERIFY (dv/RTD) | ARIMA is univariate on log sales — arguably *not* leakage-exposed via promo features. But it is refit in the S01 retrain on the corrected splits, so re-verify all four. Do not assume ARIMA is exempt. |
| 10 | `ch6:153` | CSD 16.5 / 24.2 / "ML wins (**+7.7 pp**)" | **DERIVED** + WILL CHANGE | 24.2 − 16.5. Both inputs move. |
| 11 | `ch6:154` | danskvand **22.0** / 33.4 / Prophet **16.9** / "Prophet wins" | **STRUCTURAL** + MUST RE-VERIFY | 22.0 is the chain figure. At brand×month danskvand is 23.8, so the Prophet-vs-ML gap *widens* (16.9 vs 23.8 = 6.9 pp, was 5.1 pp). The verdict "Prophet wins" survives but gets stronger — check Enrico is happy amplifying that. |
| 12 | `ch6:155` | energidrikke 11.4 / 15.7 / "ML wins (**+4.3 pp**)" | **DERIVED** + WILL CHANGE | 15.7 − 11.4. Highest-risk delta: if leakage pushes energidrikke to ~15%, this delta approaches zero and the SRQ4 verdict for the category is at risk of flipping. |
| 13 | `ch6:156` | RTD 31.0 / 48.2 / 45.4 / "ML wins (**+17.2 pp**)" | **DERIVED** + MUST RE-VERIFY | 48.2 − 31.0. Largest delta, least at risk, but still recompute. |
| 14 | `ch6:161` (in the `*Prophet` footnote, 158–162) | Prophet danskvand 16.9% | MUST RE-VERIFY | Repeated from :154. Second occurrence of the same number in a footnote — will be missed by a table-only edit. |
| 15 | `ch6:170–171` | Peak RAM: Ridge 1.5, LGB 18.7, XGB 0.2, ARIMA 0.5 MB | **STABLE** | Memory is a function of matrix size and model config, not of leakage. Caveat: the V3 fix may change the *promo feature count*, which changes matrix width — expect marginal drift, not order-of-magnitude. The load-bearing claim ("tens of MB, ≤8 GB non-binding") is robust to any plausible drift. |
| 16 | `ch6:172–173` | Latency ~1.7 s train, ~16 ms predict, LGB ~7.7 s | **STABLE** | Same reasoning. LGB's 7.7 s is tied to its tuned `n_estimators`, which *is* re-tuned — this one is the most likely of the four to move. |
| 17 | `ch6:176–178` | Coverage: CSD 90.5, RTD 88.0, dv 85.8, ed 81.0 | WILL CHANGE (CSD/ed) + MUST RE-VERIFY (dv/RTD) | Split-conformal half-width is calibrated on *validation residuals*. Leakage inflates in-sample fit → residuals were artificially small → intervals were artificially narrow. **Expect coverage to move toward nominal after the fix** — i.e. this may *improve*. Worth stating as a positive if it holds. |
| 18 | `ch6:201–206` | Final selection table (16.5 / **22.0** / 11.4 / 31.0 + "Selected granularity" column) | **STRUCTURAL** — most severe | The "Selected granularity" column ceases to exist. See Task 5. |
| 19 | `ch6:208–214` | §6.5.6 closing paragraph ("three categories forecast best at brand×month, while danskvand benefits from brand×chain… mixed-granularity selection is a deliberate methodological choice") | **STRUCTURAL (prose)** | This paragraph exists *only* to justify the mixed-grain choice. With chain removed there is no mixed-grain choice to justify. See Task 5. |
| 20 | `ch6:92` | "Target MAPE: ≤15% (industry benchmark — cite ML-Based FMCG 2024)" | **UNSOURCED** (Task 8) | Also a *metric-basis* error — see F10 below. |
| 21 | `ch8:45–46` | CSD 16.5, dv 22.0, ed **11.4** "(≈ the ≤15% industry target)", RTD 31.0 | STRUCTURAL (dv 22.0) + WILL CHANGE + UNSOURCED | Full repetition of the Ch6 headline in prose form. |
| 22 | `ch8:47–49` | ARIMA all four + Prophet 16.9 | WILL CHANGE / MUST RE-VERIFY | Third occurrence of the ARIMA set. |
| 23 | `ch8:50` | SeasonalNaive CSD 39.9, RTD 58.8 | MUST RE-VERIFY | Naive baseline should be near-invariant (no learned params) but is recomputed on the new test split. |
| 24 | `ch9:17–19` | 16.5 / 22.0 / **11.4 (near the ≤15% industry target)** / 31.0 | STRUCTURAL (22.0) + WILL CHANGE + UNSOURCED | Fourth repetition. |
| 25 | `ch9:20–23` | "finer granularity does not uniformly help… improved accuracy only for danskvand" | **STRUCTURAL (prose)** | Same problem as ch6 §6.5.2 — a finding *about* the grain comparison. If chain is demoted to a limitation, this becomes a limitation-section claim, not an SRQ1 headline finding. |
| 26 | `ch9:67–68` | "by 7.7, 4.3 and 17.2 pp" | **DERIVED** + WILL CHANGE | Second occurrence of the deltas. |
| 27 | `ch9:37` | "empirical coverage 80–98% against a 90% nominal" | **DERIVED** + MUST RE-VERIFY | A *range* over the calibration figures (item 17). Same leakage exposure, and being a range it will not be caught by grepping for individual coverage values. **Not in the original plan inventory.** |
| 28 | `ch10:21` | "test WMAPE **11.4–31.0%**; energidrikke near the ≤15% target" | **DERIVED** + WILL CHANGE + UNSOURCED | Range = min/max of the four headlines. Both endpoints move (11.4 is energidrikke = leakage; 31.0 is RTD = re-verify). |
| 29 | `ch10:23–24` | "brand×month for CSD/energidrikke/RTD, brand×chain for danskvand" | **STRUCTURAL** | Explicit grain assignment in the conclusion. Dies with DEC-GRAIN. |
| 30 | `ch10:30` | "mean 3.81 vs 3.15" (judge scores) | **STABLE** | SRQ2 LLM-judge output, unrelated to the forecasting retrain. Listed for completeness — do not touch. |
| 31 | `meeting-brief-ch1-3-2026-06-30.md:139` | CSD coverage 90.5% | **STABLE — do not edit** | Historical meeting record. Per F7's precedent, correct the chapters, not the minutes. |

### Triage summary

| Class | Count | Where the risk concentrates |
|---|---|---|
| STRUCTURAL (incl. prose) | 11 | Ch6 §6.5.1/§6.5.2/§6.5.6; Ch9 §9.1.1; Ch10 |
| WILL CHANGE | 12 | Every CSD + energidrikke figure, in 4 chapters |
| MUST RE-VERIFY | 11 | danskvand + RTD, incl. the SeasonalNaive and ARIMA sets |
| DERIVED | 7 | The deltas, the two ranges, the "2–4 pp" tuning claim |
| STABLE | 4 | RAM, latency, judge scores, the meeting brief |
| UNSOURCED | 5 | Every ≤15% mention (see Task 8) |

**Two triage items are new (not in the plan's inventory):** ch6:124 ("all eight cells") and ch9:37 ("coverage 80–98%"). Logged as **F9**.

---

## Task 3+4 — Totalbeer removal + the Ch4 factual correction

### Framing decision (proposed)

Place the **substantive justification once, in Ch3 §3.4** (data sources — where the scope of the panel is actually established), with:
- a **pointer** from Ch4 §4.1 (replacing the false "absent at source" sentence),
- a **delimitation statement** in Ch1 §1.4,
- a **limitation line** in Ch10.

Rationale: the reason is a *scoping decision about data*, so it belongs where data sources are defined. Putting it in Ch4 as the primary statement (as the plan suggested) would make it read as a data-quality finding — which is exactly the framing error F7 identifies.

**Quote the measured sizes, never "~10M rows."** The defensible number is 20.31 GB vs CSD's 11.39 GB (1.8×) and danskvand's 0.63 GB (32×).

---

### 3.1 — `ch3-methodology.md:45`

**BEFORE**
```
This thesis uses one data source: the Nielsen/Prometheus beverage scanner panel, the
core forecasting input across all five categories.
```

**AFTER (proposed)**
```
This thesis uses one data source: the Nielsen/Prometheus beverage scanner panel, the
core forecasting input across all four categories in scope.
```

*Rationale:* count swap only. "in scope" added to signal that four is a chosen subset, priming the justification that follows.

---

### 3.2 — `ch3-methodology.md:47` — the primary justification lands here

**BEFORE**
```
The Nielsen/Prometheus dataset provides longitudinal retail transaction data for five
Danish beverage categories: carbonated soft drinks (CSD), still and sparkling water
(danskvand), energy drinks (energidrikke), ready-to-drink beverages (RTD), and beer
(totalbeer). Its structure follows a star schema, ...
```

**AFTER (proposed)**
```
The Nielsen/Prometheus dataset provides longitudinal retail transaction data for
Danish beverage categories. Five categories were made available by Manifold AI;
four are carried through the empirical work: carbonated soft drinks (CSD), still and
sparkling water (danskvand), energy drinks (energidrikke), and ready-to-drink
beverages (RTD). The fifth, beer (totalbeer), was scoped out as a deliberate
methodological decision on computational grounds. Its facts table is 20.3 GB of raw
JSONL, 1.8 times the largest retained category (CSD, 11.4 GB) and roughly 32 times
the smallest (danskvand, 0.6 GB). Preprocessing it through the identical pipeline
would have consumed a disproportionate share of the compute budget for a fifth
parallel proof of concept, without altering the design of the benchmark or the
answer to any subsidiary research question. The four retained categories already
span the structural heterogeneity the benchmark is designed to test — an order of
magnitude in scale, and both promotion-rich (CSD, energidrikke) and promotion-blind
(danskvand, RTD) regimes. Excluding beer is therefore a bounded scoping choice made
under the same resource constraint that motivates the thesis, not a data
availability limitation: the beer data exist and are accessible.

Its structure follows a star schema, ...
```

*Rationale:* States the reason as an owned choice; grounds it in a measured figure; pre-empts the obvious examiner objection ("did you drop the category that would have contradicted you?") by arguing the retained four already cover the design space. The final clause explicitly closes off the false reading that Ch4 currently asserts.

---

### 3.3 — `ch4-data-assessment.md:11` — **the factual correction**

**BEFORE**
```
A fifth category, beer (totalbeer), was scoped out because its facts table is absent
from the source data (the data do not exist at source, not a size or memory
constraint); this is recorded as a data limitation rather than an analytical choice.
```

**AFTER (proposed)**
```
A fifth category, beer (totalbeer), was available but is scoped out of the empirical
work on computational grounds (Chapter 3, Section 3.4): its facts table is
approximately 20.3 GB, 1.8 times the largest retained category. This is an
analytical scoping decision, not a data limitation — the data exist and are
accessible.
```

*Rationale:* **This is a correction of a false statement, not a trim.** The current sentence asserts the file is absent at source; it is present at 20,307,167,727 bytes. Note the current text's parenthetical actively *rules out* the true reason ("not a size or memory constraint"), so a partial edit leaves a contradiction — the whole sentence must go. The polarity of the final clause also inverts: "data limitation rather than analytical choice" → "analytical choice, not a data limitation."

⚠️ **Do not retro-edit `meeting-brief-ch1-3-2026-06-30.md:40` and `:138`,** which repeat the wrong reason. They are a historical meeting record. If the wrong reason needs closing out for Enrico, do it as a note in the *next* brief, not by rewriting the old one.

---

### 3.4 — `ch1-introduction.md:64` — **the hard one. Contains an unresolved question.**

**BEFORE**
```
The thesis focuses on the Danish beverage retail market, evaluated across five Nielsen
product categories: carbonated soft drinks (CSD), still and sparkling water (danskvand),
energy drinks (energidrikke), ready-to-drink beverages (RTD), and beer (totalbeer).
[...] The five categories were selected in collaboration with Manifold AI as
representative of the FMCG challenges the system must address, including high
promotional sensitivity, seasonal demand patterns, and strong competitive dynamics,
while differing systematically in scale (brand counts range from 42 in RTD to 455 in
beer), which allows the benchmark to test whether the modelling findings generalise
across heterogeneous category structures.
```

**Two independent problems, not one:**

1. **The count.** five → four.
2. **The range is beer-anchored.** "42 in RTD to 455 in beer" uses beer as the *upper bound*. Removing beer removes the top of the range — the sentence loses its logic, not just a number.

#### 🚩 BASIS MISMATCH — flag for Brian/Enrico, do not silently resolve

Ch1 and Ch4 do not agree on what a "brand count" is:

| Source | RTD | CSD | danskvand | energidrikke | beer |
|---|---|---|---|---|---|
| **Ch1:64** (basis unstated) | **42** | — | — | — | **455** |
| **Ch4:48 / Table 4.1** — "Brands (in scope)", DVH EXCL. HD | **93** | 136 | 49 | 64 | n/a |
| **Ch4 Table 4.1** — retained ≥30 months | **42** | 77 | 24 | 27 | n/a |

**RTD = 42 appears in Ch4 as the ≥30-month *retained* count, not the in-scope count (93).** So Ch1's "42 in RTD" most plausibly sits on the **retained** basis. But 455 for beer cannot be a retained count on any plausible reading — retained counts for the worked categories top out at 77 (CSD). 455 is the scale of a *catalog* count (Ch4's catalog-SKU column runs 565–8,608, so 455 is not that either, but it is the right order of magnitude for a catalog *brand* count).

**Therefore Ch1:64 currently compares a retained count (42) against what appears to be a catalog count (455), producing a spuriously wide 10.8× range.** Removing beer does not create this problem — it *exposes* one that is already there.

**Question for Brian/Enrico — needs an answer before this sentence can be rewritten:**
> On which basis is Ch1's brand-count range stated — retained (≥30 months), in-scope, or catalog? And where did 455 come from? It is not reproducible from Table 4.1 on any of the three bases.

**Conditional drafts (pick after the basis is settled):**

*Option A — retained basis (≥30 months), consistent with RTD=42:*
```
...while differing systematically in scale (retained brand counts range from 24 in
danskvand to 77 in CSD)...
```
Range narrows from 10.8× to 3.2×. **The "differing systematically in scale" argument gets materially weaker** — this is a real cost of removing beer, not a cosmetic one. Flag to Enrico.

*Option B — in-scope basis, consistent with Ch4:48:*
```
...while differing systematically in scale (in-scope brand counts range from 49 in
danskvand to 136 in CSD)...
```
Range 2.8×. Weaker still on ratio, but the basis is the one Ch4 actually documents and defends, so it is internally consistent and auditable.

*Option C — recompute a catalog brand count for the four retained categories.* Only viable if the 455 basis can be identified and reproduced. Would preserve the widest range. **Requires a data query — out of scope for this preparation pass.**

**Recommendation:** Option B. It is the only basis Ch4 documents with a table and column definitions, so it is the only one a reader can verify. Accept the narrower ratio and lean the "heterogeneity" argument on the *promo-regime* split (promo-rich CSD/energidrikke vs promo-zero danskvand/RTD, Ch4:48), which is a stronger and better-evidenced heterogeneity claim than brand count anyway.

**Also in this sentence:** "between 37 and 42 monthly periods per category" — verify this span was not computed including beer. Table 4.1 gives 37–42 across the four retained, so it holds. No change needed.

---

### 3.5 — `ch1-introduction.md:72` (Generalisability) — **not in the F8 inventory**

**BEFORE**
```
While the five-category benchmark provides evidence on whether the modelling findings
hold across heterogeneous beverage categories, ...
```

**AFTER (proposed)**
```
While the four-category benchmark provides evidence on whether the modelling findings
hold across heterogeneous beverage categories, ...
```

*Rationale:* Count swap. **New location — logged as F9.**

---

### 3.6 — `ch1-introduction.md:84` — **not in the F8 inventory**

**BEFORE**
```
**Chapter 4** presents the data assessment, characterising the quality, structure, and
forecasting suitability of the Nielsen scanner data across the five beverage categories,
```

**AFTER (proposed)** — `five` → `four`. *New location — logged as F9.*

---

### 3.7 — `ch1-introduction.md:88`

**BEFORE**
```
**Chapter 6** addresses SRQ1 through an empirical model benchmark, comparing lightweight
forecasting models across the five categories on accuracy, memory efficiency, and stability,
```

**AFTER (proposed)** — `five` → `four`. *Count swap.*

---

### 3.8 — `ch3-methodology.md:37` and `:39` — **not in the F8 inventory**

Both carry the five-category framing:
- `:37` — "the Danish beverage retail market across the five Nielsen categories constitutes the empirical context"
- `:39` — "evaluated on the Nielsen dataset across the five Danish beverage categories at brand-times-retailer granularity"

**AFTER (proposed)** — `five` → `four` in both. *New locations — logged as F9.*

⚠️ **`ch3:39` has a second, independent problem:** it says "at brand-**times-retailer** granularity" as a *locked design decision*. That is the brand×chain grain that DEC-GRAIN removes. This line is **STRUCTURAL**, and it is stated as a pre-registered locked choice — which makes silently changing it awkward. See Task 5, §5.5. **Logged as F11.**

---

### 3.9 — `ch3-methodology.md:55` — **not in the F8 inventory**

**BEFORE**
```
Five forecasting models are evaluated across the five Nielsen beverage categories: ARIMA,
Prophet, LightGBM, XGBoost, and Ridge Regression.
```

**AFTER (proposed)**
```
Five forecasting models are evaluated across the four Nielsen beverage categories: ARIMA,
Prophet, LightGBM, XGBoost, and Ridge Regression.
```

*Rationale:* Note the collision of two "five"s in one sentence (five *models*, five *categories*). Only the second changes. A careless find-replace breaks this line. *New location — logged as F9.*

---

### 3.10 — `ch3-methodology.md:2` (frontmatter status line)

```
> Status: PROSE DRAFT — written 2026-04-12; realigned 2026-06-16 to the rescoped
> framing (5 categories; RSS profiling); ...
```

*Proposal:* leave the historical "realigned 2026-06-16 to … (5 categories)" clause intact as a change record, and **append** a new clause: `realigned 2026-08-01 to four categories (totalbeer scoped out on compute grounds, §3.4)`. Rewriting the old clause would falsify the file's own history — the same error Ch4:11 embodies.

---

### 3.11 — `ch10-conclusion.md` — limitations line (new text, no BEFORE)

*Proposal — add to the limitations enumeration:*
```
The benchmark covers four of the five Danish beverage categories in the Nielsen panel.
Beer (totalbeer) was scoped out on computational grounds (§3.4) rather than for data
reasons; whether the per-category findings extend to a category of that scale is
untested and is a direct extension of this work.
```

*Rationale:* Converts the exclusion into a stated boundary of the claim plus a future-work hook. The "rather than for data reasons" clause is doing real work here — it is the last line of defence against a reader who has seen the old Ch4 framing.

---

### Totalbeer coverage checklist

| Location | Type | Status |
|---|---|---|
| `ch1:64` | Count + **beer-anchored range** | 🚩 Blocked on basis question |
| `ch1:72` | Count | Drafted (**new, F9**) |
| `ch1:84` | Count | Drafted (**new, F9**) |
| `ch1:88` | Count | Drafted |
| `ch3:2` | Status frontmatter | Drafted (append, don't rewrite) |
| `ch3:37` | Count | Drafted (**new, F9**) |
| `ch3:39` | Count + **grain** | Drafted; grain issue → F11 |
| `ch3:45` | Count | Drafted |
| `ch3:47` | Count + **primary justification** | Drafted |
| `ch3:55` | Count (careful — two "five"s) | Drafted (**new, F9**) |
| `ch4:11` | **Factual correction** | Drafted |
| `ch10` limitations | New text | Drafted |
| `meeting-brief:40`, `:138` | Historical record | **Deliberately not edited** |

---

## Task 5 — Ch6 structural rewrite for chain-grain removal

### 5.1 The headline regression — state this first

| Category | Current headline (selected grain) | Post-DEC-GRAIN headline (month only) | Δ |
|---|---|---|---|
| CSD | 16.5% (month) | 16.5% | — |
| **danskvand** | **22.0% (chain)** | **23.8%** | **+1.8 pp worse** |
| energidrikke | 11.4% (month) | 11.4% | — |
| RTD | 31.0% (month) | 31.0% | — |

**danskvand's reported accuracy degrades by 1.8 pp purely from the grain decision, before P0032's leakage fix touches anything.** Three consequences Enrico must sign off on knowingly:

1. The **headline range in Ch10:21 widens**: 11.4–31.0% → 11.4–31.0% (unchanged, since danskvand is interior to the range). No change there — but see (2).
2. The **SRQ4 verdict for danskvand strengthens against the thesis**: Prophet 16.9% vs ML 23.8% is a 6.9 pp gap, up from 5.1 pp. The one category where a *traditional* model beats the thesis's ML approach now beats it by more.
3. **The granularity finding — the thesis's most-cited "counter-intuitive result" — is destroyed as an SRQ1 headline.** See §5.3.

### 5.2 Rewritten tables (proposed)

**§6.5.1 headline table (ch6:117–122)**

BEFORE — 4 columns:
```
| Category | brand × month (_03) | brand × chain (_04) | SeasonalNaive (chain) |
|---|---|---|---|
| CSD | **16.5%** | 20.8% | 39.9% |
| danskvand | 23.8% | **22.0%** | 37.7% |
| energidrikke | **11.4%** | 13.9% | 31.9% |
| RTD | **31.0%** | 38.8% | 58.8% |
```

AFTER — 3 columns:
```
| Category | Tuned XGBoost (brand × month) | SeasonalNaive |
|---|---|---|
| CSD | **16.5%** | 39.9% |
| danskvand | **23.8%** | 37.7% |
| energidrikke | **11.4%** | 31.9% |
| RTD | **31.0%** | 58.8% |
```

⚠️ **The SeasonalNaive column is currently labelled "(chain)".** Its four values (39.9 / 37.7 / 31.9 / 58.8) are chain-grain baselines. If chain is removed from active results, **a brand×month SeasonalNaive baseline must be recomputed** — otherwise the comparison is ML-at-month vs naive-at-chain, which is not a controlled comparison and is a genuine methodological defect, not a presentation issue. **This is a re-run requirement for P0032/P0035, not a prose edit.** Logged as **F10**.

**§6.5.6 selection table (ch6:201–206)**

BEFORE — 4 columns incl. "Selected granularity":
```
| Category | Selected model | Selected granularity | Test WMAPE |
| CSD | XGBoost | brand × month | **16.5%** |
| danskvand | XGBoost | brand × chain | **22.0%** |
| energidrikke | XGBoost | brand × month | **11.4%** |
| RTD | XGBoost | brand × month | **31.0%** |
```

AFTER — 3 columns:
```
| Category | Selected model | Test WMAPE |
| CSD | XGBoost | **16.5%** |
| danskvand | XGBoost | **23.8%** |
| energidrikke | XGBoost | **11.4%** |
| RTD | XGBoost | **31.0%** |
```

**Note what is lost:** §6.5.6's entire premise is *"the thesis selects a configuration per category."* With one model (XGBoost) and one grain (month) across all four, **there is no per-category selection left to make.** The table degenerates to "XGBoost everywhere." §6.5.6 arguably should not exist as a subsection any more — see §5.4.

### 5.3 §6.5.2 "Granularity finding" (ch6:130–138) — **cannot be table-edited; needs a decision**

Current text (paraphrased): disaggregating to chain multiplies rows ~6× but does not uniformly improve accuracy; month wins for CSD/energidrikke/RTD, chain wins for danskvand; refutes "more rows is always better."

**This subsection is 100% about the comparison DEC-GRAIN removes.** Three options:

| Option | What it does | Assessment |
|---|---|---|
| **A — Delete §6.5.2** | Cleanest structurally | ❌ **Throws away a genuine empirical finding.** The signal-to-noise result is real and was obtained; it is arguably the most interesting SRQ1 result in the chapter. Deleting it because of a presentation decision is bad research practice. |
| **B — Demote to a methodological note** | Keep §6.5.2 but reframe: chain grain was evaluated, did not improve accuracy in 3 of 4 categories, and is therefore not carried into active results; the exception (danskvand) is documented as a limitation | ✅ **Recommended.** Preserves the finding, honestly reports the danskvand exception, and *justifies* DEC-GRAIN rather than hiding it. The grain decision becomes an evidenced choice instead of an unexplained narrowing. |
| **C — Keep as-is, add a footnote** | Minimal edit | ❌ Leaves §6.5.1's table without the chain column that §6.5.2 discusses. Internally incoherent. |

**Proposed §6.5.2 rewrite under Option B:**
```
### 6.5.2 Granularity: why the chain dimension is not carried forward

A brand × retail-chain representation was evaluated alongside brand × month.
Disaggregating to the chain dimension multiplies training rows roughly sixfold but
does not uniformly improve accuracy: at the chain grain CSD degrades from 16.5% to
20.8% WMAPE, energidrikke from 11.4% to 13.9%, and RTD from 31.0% to 38.8%. Only
danskvand improves, from 23.8% to 22.0%. This refutes a naïve "more rows is always
better" assumption and is explained by the signal-to-noise trade-off of finer
granularity: more rows of noisier per-chain demand do not compensate for the loss of
a cleaner aggregate signal (see `fig2_granularity.png`).

Because the chain representation improves accuracy in only one of four categories,
and by a modest 1.8 pp, the thesis reports brand × month as the single active
representation across all categories. The danskvand result is retained as a
documented limitation: for that category a finer representation would have
delivered a slightly better forecast, and the uniform choice costs 1.8 pp WMAPE
there. The gain is not judged sufficient to warrant a mixed-representation design,
whose additional complexity would have to be carried through the tool interface,
the calibration layer, and the agentic integration for a single category.
```

*Rationale:* Turns a liability into an argued decision. Note it makes the 1.8 pp cost **explicit and owned** rather than buried — which is the defensible position, and pre-empts an examiner spotting it.

### 5.4 §6.5.6 closing paragraph (ch6:208–214) — **needs full replacement**

Current text argues: XGBoost everywhere; three categories at month, danskvand at chain; both matrices retained in the repo; "mixed-granularity selection is a deliberate methodological choice, stated as such, not an inconsistency."

**Every clause of that paragraph is now false or moot.** There is no mixed granularity to defend.

**Proposed replacement:**
```
XGBoost is the model of choice in every category, at the brand × month
representation (§6.5.2). The pipeline, feature set, and representation are identical
across categories, so the cross-category comparison is fully controlled — a stronger
position than the mixed-representation design considered and rejected in §6.5.2.
The brand × chain matrices remain in the repository (`_04`) and are reported in
§6.5.2 as evaluated-but-not-adopted, so the granularity result remains reproducible.
```

*Rationale:* Inverts the argument. The old paragraph defended mixed-grain as "deliberate, not an inconsistency" (a defensive posture). The new one claims uniform grain as a *strength* for controlled comparison — which is true and is a better argument than the one it replaces.

### 5.5 Two knock-on locations outside §6.5

- **`ch6:124`** — "XGBoost is the best model in all **eight** (category × granularity) cells." → four cells. But note: **"best in 8 of 8" is a stronger claim than "best in 4 of 4."** The chapter loses rhetorical force here. Worth stating the eight-cell result in §6.5.2's rewrite (as drafted above, which retains the chain numbers) so the evidence is not lost.
- **`ch3:39`** — states brand×retailer granularity as a **locked, pre-registered design decision**: *"These choices are documented here as locked design decisions to ensure reproducibility and to prevent retroactive revision based on observed model performance."* DEC-GRAIN is *precisely* a retroactive revision based on observed model performance. **This is the single most examiner-exposed item in the whole plan.** Logged as **F11** — see below for the recommended handling.

### 5.6 Ch9 and Ch10 knock-ons

- **`ch9:20–23`** — "a central and somewhat counter-intuitive result is that finer granularity does not uniformly help" is presented as a **headline SRQ1 finding**. Under Option B it survives, but must be reframed as a *methodological* finding that justifies the representation choice, not as a headline accuracy result. Retains its value; changes its section.
- **`ch10:23–24`** — "brand×month for CSD/energidrikke/RTD, brand×chain for danskvand" must go. Proposed: *"Category specialisation is in the model's fit, not the representation: a single brand×month representation is used throughout, after a chain-level representation was evaluated and found to help only one category (§6.5.2)."*
- **`ch9:22`** — "improved accuracy only for danskvand" — still true, keep, but it now supports the *rejection* of chain rather than describing a mixed design.

---

## Task 8 — The "≤15% industry target": **NOT FOUND**

### Verdict: **NOT FOUND — recommend cutting the claim.**

This is not "cannot verify locally." The local corpus contains an analysis note for the exact cited paper, and that note **states a different and incompatible finding**.

### Evidence

**1. The cited source's own corpus note does not contain the claim.**
`01_thesis_research/literature/obisdian_paper_analysis/ml_fmcg_demand_forecasting.md` is the analysis note for Ceran et al. (2024), *Machine Learning-Based Demand Forecasting for an FMCG Retailer* (INFUS 2024, LNNS Vol. 1090) — the paper named in ch6:92 and listed at `references.md:45–48`. Its **Key finding** (line 21) reads in full:

> *"LightGBM achieves best overall performance across categories, with 15–25% MAPE **reduction over ARIMA baselines**. Neural network models (LSTM) competitive on high-volume SKUs but less robust on low-volume/intermittent demand."*

**This is a relative improvement, not an absolute threshold.** "15–25% MAPE reduction over ARIMA" and "≤15% MAPE as an industry target" are different claims in different units. The note's **Method** section (line 18) lists MAPE/RMSE/MAE as evaluation metrics and reports no benchmark threshold. The note's **Relevance to thesis** section explicitly frames the paper's contribution as a *"magnitude benchmark — thesis should aim to demonstrate comparable or better **gains over** descriptive BI baselines"* — again, relative.

🚩 **Probable origin of the error: "15–25% MAPE reduction" was misread as "≤15% MAPE."** The 15 is the same digit in both. This is a plausible mechanical misreading at drafting time, consistent with Brian's "AI slop" suspicion.

**2. No ≤15% threshold anywhere in the literature corpus.** A regex sweep for `15\s*%|≤\s*15|15\s*percent` across all of `01_thesis_research/` returns exactly **one** hit, and it is unrelated:
- `humans_vs_llms_forecasting.md:21` — *"GPT-4 (zero-shot) achieves MAPE **within 15% of** professional human forecasters"* — a relative comparison against human forecasters, in an LLM-forecasting paper, nothing to do with a retail industry benchmark.

`gap_analysis_v4.md` returns **zero** hits for `15%`, `target MAPE`, or `threshold`. The other two SRQ1 forecasting sources flagged in F5 also fail to support it:
- `retail_hybrid_neural_forecasting.md:24` — sets **4.16% MAPE** as *"the aspirational ceiling"* and *"the state-of-the-art benchmark for the thesis to compare against."*
- `retail_ml_tree_ensembles_lstm.md:18` — reports MAPE/MAE/RMSE, no threshold.

**3. The corpus's own actual benchmark contradicts the framing.** `scraping_log.md:58` and `retail_hybrid_neural_forecasting.md:24,26` establish **4.16% MAPE** (CNN-LSTM, PLOS ONE 2024) as the corpus's *"concrete benchmark for thesis evaluation."* Against that reference point, energidrikke's 11.4% is **2.7× worse**, not "near target." The one sourced benchmark in the corpus makes the thesis's result look *weaker*, not stronger — which is very likely why an unsourced, more flattering yardstick got drafted in its place.

**4. The claim was already flagged and never resolved.** `00_thesis_context/formal-requirements/compliance_report_20260315.md:254`:
> `**WARNING-CH6-02**: MAPE target "≤15% (industry benchmark)" — citation needed`

**Open since 2026-03-15.** It also appears at `00_thesis_context/thesis-topic/project-overview.md:214` in a source-summary table (*"MAPE ≤ 15% as industry benchmark"*) attributed to the same Springer paper — i.e. the misreading propagated into the project overview too, which is likely where Ch6 picked it up. This is a **fifth** propagation site, upstream of the four chapters.

**5. Independent defect: the metric basis is wrong even if the source existed.** ch6:92 sets a target on **MAPE**. Every figure it is compared against (ch6:137, ch8:46, ch9:18, ch10:21) is **WMAPE** — and ch6:109–113 explicitly states that plain mean MAPE *"is not reported"* because it diverges on low-volume categories. **The thesis compares WMAPE numbers against a MAPE threshold.** Even a correctly sourced ≤15% MAPE benchmark would not license "energidrikke at 11.4% WMAPE is near the ≤15% target." Logged as **F10**.

### Recommendation

**Cut the ≤15% claim from all five locations.** Do not attempt to re-source it — a threshold that must be hunted for after the fact to justify a result already in hand is a p-hacking pattern, and the corpus's actual benchmark (4.16%) points the other way.

Replacement strategy, in preference order:

1. **Preferred — drop the absolute target; report relative gains, which the corpus *does* support.**
   - ch6:92 → replace the MAPE-target bullet with: *"No absolute MAPE threshold is imposed. Model performance is assessed relatively: against a SeasonalNaive baseline (learned skill), against ARIMA/Prophet traditional baselines (SRQ4), and against the published gradient-boosting-over-ARIMA improvements reported for FMCG retail panels (Ceran et al., 2024)."*
   - ch6:137 → *"energidrikke is the best-forecast category at 11.4% WMAPE, roughly a third of the SeasonalNaive baseline error (31.9%)."* — a claim the thesis's own data fully supports, needing no external yardstick.
   - ch8:46, ch9:18, ch10:21 → delete the parenthetical "(≈/near the ≤15% target)" clauses. **All three read correctly with the clause simply removed** — no rewriting needed.

2. **Fallback if an absolute anchor is wanted** — cite the sourced 4.16% CNN-LSTM ceiling and frame the thesis's result honestly as constrained-compute performance against an unconstrained-deep-learning ceiling. `retail_hybrid_neural_forecasting.md:26` already drafts this exact sentence for Ch6.

3. **Only if Brian wants to keep ≤15%** — he must read the Ceran et al. PDF directly and find a page-level quote. **My assessment: he will not find one, because the corpus note describes a relative reduction and the paper's abstract framing (per the note) is comparative throughout.** But the PDF was not read in this pass, so this is a strong inference from the note, not a reading of the primary source. If Brian wants certainty on the primary source rather than on the corpus note, checking the PDF is the way to get it.

### Why this matters more after P0032

The claim's fragility compounds. If the leakage fix pushes energidrikke from 11.4% toward or past 15%, the sentence *"near the ≤15% target"* inverts to *"misses the target"* — and the thesis would then be reporting a failure against a threshold **that has no source**. Cutting it now removes both risks at once. Doing this *before* the retrain also means the retrain's outcome cannot be accused of having influenced which yardstick was chosen.

---

## Summary of open questions for Brian / Enrico

| # | Question | Blocks |
|---|---|---|
| Q1 | **On which basis is Ch1:64's brand-count range stated, and where did "455 in beer" come from?** Not reproducible from Table 4.1 on any basis. | Ch1:64 rewrite (Task 3) |
| Q2 | Accept the narrower brand-count range (Option B, 49–136, 2.8×) and lean heterogeneity on the promo-regime split instead? | Ch1:64 rewrite |
| Q3 | **Approve Option B for §6.5.2** — keep the granularity finding, reframed as the justification for DEC-GRAIN? | Ch6 rewrite (Task 5) |
| Q4 | Knowingly accept **danskvand 22.0% → 23.8%** and the widened Prophet gap (5.1 → 6.9 pp)? | Ch6/Ch8/Ch9/Ch10 |
| Q5 | **Recompute a brand×month SeasonalNaive baseline?** Current baselines are chain-grain — an uncontrolled comparison once ML moves to month-only. Re-run requirement. | P0032/P0035 scope |
| Q6 | **Approve cutting ≤15% from all five locations** (recommendation 1)? | Ch6/Ch8/Ch9/Ch10 + project-overview.md:214 |
| Q7 | **How to handle `ch3:39`** — brand×retailer grain stated as a *locked, pre-registered* decision that DEC-GRAIN now revises on observed performance? See F11. | Ch3 rewrite |
