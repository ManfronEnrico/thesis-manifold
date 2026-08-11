---
pid: P0034
created: 2026-08-01 00:00:00
updated: 2026-08-01 17:00:00
---

# P0034 — Findings

## Pre-existing (grep run 2026-08-01)

### F1 — the answer to Enrico's question #2 is "yes, extensively"

Enrico asked whether the leakage fix collides with anything that hard-codes old numbers.
It does: **13 distinct locations across 4 chapter drafts**, with the same four headline
WMAPE figures repeated in **three separate tables inside ch6 alone** (lines 119–122,
153–156, 201–206), then again in ch8, ch9, and ch10.

Practical consequence: this is not a find-and-replace. The same number appears in
different framings (absolute, delta, range), so each occurrence needs its own treatment.

### F2 — the chain-grain problem is bigger than the leakage problem

Ch6's tables are structured around a **brand×month vs brand×chain** comparison, and
danskvand's *selected* configuration is brand×chain (22.0% WMAPE, line 204).

DEC-GRAIN (2026-07-12) drops the chain grain from active results, demoting it to a
documented limitation. So:

- Ch6 lines 119–122 lose a column.
- Ch6 lines 201–206 lose their "Selected granularity" column entirely.
- danskvand's headline number changes from 22.0% (chain) to 23.8% (month) — **a
  regression in the reported result**, purely from the grain decision, before any
  leakage effect.

This is a structural rewrite, and danskvand's number getting *worse* is the kind of thing
Enrico needs to sign off on knowingly. Flag it loudly.

### F3 — derived quantities are the easy thing to miss

Beyond raw figures, these are computed *from* them and will silently go stale:

- "+7.7 pp", "+4.3 pp", "+17.2 pp" ML-vs-ARIMA deltas (ch6:153–156, ch9:67)
- "test WMAPE 11.4–31.0%" range claim (ch10:21)
- "improved WMAPE by roughly 2–4 pp over untuned" (ch6:126)
- "near the ≤15% industry target" — a *qualitative* claim contingent on energidrikke
  staying at 11.4%. If the leakage fix pushes it above 15%, this sentence inverts.

F3's last item is the highest-risk single sentence in the drafts: energidrikke is both
promo-affected *and* the category carrying the thesis's strongest claim.

### F4 — V2 (mean-MAPE) is already handled in prose

Ch6 §6.5.1 (lines 109–113, 186–187) already explains that plain mean MAPE is not reported
because it diverges on low-volume categories. Enrico's V2 finding is therefore already
reflected in the writing — no prose change needed for V2, only the code-side suppression
in the S01 retrain.

### F5 — the ≤15% "industry target" is unverified, and it is load-bearing

The claim originates at `ch6-model-benchmark.md:92`:

> Target MAPE: ≤15% (industry benchmark for retail demand forecasting — cite ML-Based FMCG 2024)

The parenthetical is still a **drafting instruction** ("cite X"), not a completed citation.
From there it is restated as established fact in four places (`ch6:137`, `ch8:46`,
`ch9:18`, `ch10:21`), each time without the hedge.

Named source: Springer LNCS / INFUS 2024, *"Machine Learning-Based Demand Forecasting for
an FMCG Retailer"* (`references.md:46-47`; also `01_thesis_research/literature/scraping_log.md`
row 2). Whether that paper asserts a ≤15% MAPE benchmark is **unverified** — task 8.

Two reasons this is more than a tidiness issue:

1. It is the yardstick for the thesis's strongest empirical claim (energidrikke 11.4%
   "near the ≤15% industry target"). An unsourced yardstick makes the claim unfalsifiable.
2. P0032's leakage fix may push energidrikke above 15%, which would invert that sentence.
   Rewriting it around a threshold that has no source would compound the problem.

Cross-check `01_thesis_research/literature/gap_analysis_v4.md`, which discusses SRQ1
forecasting sources ([[ml_fmcg_demand_forecasting]], [[fmcg_demand_forecasting_methods]],
[[retail_ml_tree_ensembles_lstm]]) — if a defensible threshold exists anywhere in the
corpus, it is likely there.

### F6 — Totalbeer justification

Brian's stated reason (2026-08-01): excluded on **compute constraints** — significantly
larger than any other category, ~10M rows. Prose must state this rather than silently
dropping beer, otherwise a reader comparing Ch3's five-category framing to the results
sees an unexplained gap.

---

## Discovered during execution

### F7 — Ch4's stated beer-exclusion reason is factually WRONG (Brian confirmed 2026-08-01)

`ch4-data-assessment.md:11` currently reads:

> A fifth category, beer (totalbeer), was scoped out because its facts table is absent
> from the source data (**the data do not exist at source, not a size or memory
> constraint**); this is recorded as a data limitation rather than an analytical choice.

**This is false.** Brian confirmed 2026-08-01: *"not true, it does exist, just too large."*
Verified on disk — `02_thesis_data/_00_raw/nielsen/data_jsonl/Totalbeer/views/totalbeer_clean_facts_v.jsonl`
exists at **20,307,167,727 bytes (~20.3 GB)**.

Measured facts-file sizes (raw JSONL, 2026-08-01):

| Category | Facts file | vs CSD |
|---|---|---|
| **Totalbeer** | **20.31 GB** | **1.78×** |
| CSD | 11.39 GB | 1.00× |
| Energidrikke | 3.64 GB | 0.32× |
| Danskvand | 0.63 GB | 0.06× |

Totalbeer is 1.8× the largest worked category and ~32× danskvand — a defensible
compute-constraint justification grounded in a measured number, not the plan's
approximate "~10M rows" (which was never verified and should not be quoted).

**Consequence — this widens the task-3/4 scope.** The job is no longer "remove beer from
a five-category framing." It is also a **factual correction**: Ch4:11 asserts a wrong
reason and must be rewritten, not merely trimmed. The two justifications are not
interchangeable — "absent at source" is an external data limitation; "too large to
compute" is an owned methodological scoping choice. Only the latter is true.

Note the meeting brief repeats the wrong reason twice — `meeting-brief-ch1-3-2026-06-30.md:40`
("beer (totalbeer) excluded because its facts are absent at source") and `:138`
("beer excluded because its facts are missing at source — is this acceptable?"). The brief
is a historical meeting record, so correct the chapter drafts; do not retro-edit the brief.

### F8 — inventory additions the plan's table missed

Task 1 sweep found locations absent from the task_plan inventory:

| File | Line | What |
|---|---|---|
| `ch1-introduction.md` | 64 | §1.4 Delimitation — "**five** Nielsen product categories", names beer explicitly |
| `ch1-introduction.md` | 88 | Chapter-6 forward reference — "across the **five** categories" |
| `ch3-methodology.md` | 45 | "across all **five** categories" |
| `ch3-methodology.md` | 47 | Names all five incl. "beer (totalbeer)" |
| `ch4-data-assessment.md` | 11 | The wrong-reason sentence (F7) |
| `meeting-brief-ch1-3-2026-06-30.md` | 139 | CSD coverage 90.5% (metric, not category) |

**Ch1:64 is the hardest edit and is not a count swap.** It justifies the multi-category
scope using a *beer-specific* statistic: *"brand counts range from 42 in RTD to **455 in
beer**"*. Removing beer breaks the sentence's logic, not just its number — the range's
upper bound disappears. Whoever drafts this must re-derive the range from the four
retained categories (Ch4:48 gives in-scope brand counts: CSD 136, danskvand 49,
energidrikke 64, RTD 93 → range becomes 49–136 in danskvand–CSD, on in-scope counts).
Confirm which brand-count basis Ch1 intends before rewriting; Ch1's "455 in beer" is a
catalog-style count and may not be on the same basis as Ch4's in-scope counts.

Also note `ch3-methodology.md:2` frontmatter status line still says "realigned 2026-06-16
to the rescoped framing (**5 categories**; RSS profiling)" — a status annotation, lower
priority than body prose but stale.

### F9 — inventory is still incomplete: 8 more locations found during tasks 2/3/5

Even after F8's additions, the sweep for tasks 2–5 turned up eight further locations
not in either the task_plan table or F8:

| File | Line | What | Class |
|---|---|---|---|
| `ch1-introduction.md` | 72 | "the **five**-category benchmark" (Generalisability) | count |
| `ch1-introduction.md` | 84 | "across the **five** beverage categories" (Ch4 forward ref) | count |
| `ch3-methodology.md` | 37 | "across the **five** Nielsen categories" | count |
| `ch3-methodology.md` | 39 | "across the **five** Danish beverage categories" — **and** the brand×retailer grain (see F11) | count + structural |
| `ch3-methodology.md` | 55 | "Five forecasting models … across the **five** Nielsen beverage categories" | count — ⚠️ two "five"s in one sentence, only the second changes |
| `ch6-model-benchmark.md` | 124 | "best model in all **eight** (category × granularity) cells" — 4×2 grains; becomes four | structural, in prose not a table |
| `ch9-discussion.md` | 37 | "empirical coverage **80–98%** against a 90% nominal" | derived range over the ch6:176–178 calibration figures |
| `00_thesis_context/thesis-topic/project-overview.md` | 214 | "MAPE ≤ 15% as industry benchmark", attributed to the Springer FMCG paper | **fifth ≤15% site, upstream of the chapters** |

Two lessons for whoever applies these:

1. **`ch3:55` breaks find-replace.** "Five forecasting models … across the five
   categories" — a global `five`→`four` corrupts the model count.
2. **Ranges hide their inputs.** `ch9:37`'s "80–98%" and `ch10:21`'s "11.4–31.0%" are
   derived from figures elsewhere; grepping for the component values will never surface
   them. Any future sweep must grep for range patterns (`\d+[–-]\d+%`) separately.

The inventory should now be treated as *probably* complete but not provably so — three
independent passes each found new locations.

### F10 — the ≤15% claim has TWO independent defects, and NOT FOUND is the verdict

**Defect 1 — no source (task 8 verdict: NOT FOUND, not "cannot verify").**
The corpus note for the exact cited paper —
`01_thesis_research/literature/obisdian_paper_analysis/ml_fmcg_demand_forecasting.md:21`
(Ceran et al. 2024, INFUS/Springer, = `references.md:45-48`) — states:

> "LightGBM achieves best overall performance across categories, with **15–25% MAPE
> reduction over ARIMA baselines**."

That is a **relative improvement**, not an absolute threshold. The likely mechanism of
the error is a misreading of *"15–25% MAPE reduction"* as *"≤15% MAPE"* — same digit,
different unit. A regex sweep of all of `01_thesis_research/` for `15\s*%|≤\s*15` returns
exactly one hit and it is unrelated (`humans_vs_llms_forecasting.md:21`, GPT-4 "within
15% of professional human forecasters"). `gap_analysis_v4.md` has zero hits.

The corpus's *actual* sourced benchmark points the other way: `retail_hybrid_neural_forecasting.md:24`
sets **4.16% MAPE** (CNN-LSTM, PLOS ONE 2024) as "the aspirational ceiling" and "the
state-of-the-art benchmark for the thesis to compare against." Against that, energidrikke's
11.4% is 2.7× worse — which is plausibly *why* a more flattering unsourced yardstick got
drafted instead.

This was already flagged and never closed:
`00_thesis_context/formal-requirements/compliance_report_20260315.md:254` —
`WARNING-CH6-02: MAPE target "≤15% (industry benchmark)" — citation needed`. **Open
since 2026-03-15.**

**Defect 2 — metric-basis mismatch, independent of sourcing.**
`ch6:92` states the target on **MAPE**. Every figure compared against it (`ch6:137`,
`ch8:46`, `ch9:18`, `ch10:21`) is **WMAPE**. And `ch6:109–113` explicitly says plain mean
MAPE "is *not* reported" because it diverges on low-volume categories. So the thesis
compares WMAPE values against a MAPE threshold. **Even a correctly sourced ≤15% MAPE
benchmark would not license the sentence.** This defect survives any re-sourcing effort
and is on its own sufficient reason to cut the claim.

**Recommendation: cut from all five sites** (ch6:92, ch6:137, ch8:46, ch9:18, ch10:21 —
plus `project-overview.md:214` per F9) and replace with relative framing the data already
supports (e.g. energidrikke 11.4% vs SeasonalNaive 31.9%). Re-sourcing a threshold after
the result is in hand is a p-hacking pattern; cutting it before the P0032 retrain also
means the retrain outcome cannot be said to have influenced the choice of yardstick.

### F11 — DEC-GRAIN collides with a pre-registration claim in Ch3 (highest examiner exposure)

`ch3-methodology.md:39` states the brand×retailer granularity as a **locked design
decision**:

> "The unit of analysis is the predictive-extension artefact, evaluated on the Nielsen
> dataset across the five Danish beverage categories **at brand-times-retailer
> granularity**. … These choices are documented here as **locked design decisions to
> ensure reproducibility and to prevent retroactive revision based on observed model
> performance**."

DEC-GRAIN drops the chain (retailer) grain from active results **because of observed
model performance** — it improved accuracy in only one of four categories. That is,
verbatim, the thing the sentence promises will not happen.

This is not fixable by editing `ch3:39` to say "brand × month" and moving on. Doing so
would silently rewrite a pre-registration to match the outcome, which is the more serious
version of the same problem, and Ch4 §4.1's split is elsewhere described as
"locked, pre-registered."

Three defensible handlings, in order of preference:

1. **Report the revision openly.** Keep `ch3:39`'s locked-decision language, and add that
   the granularity choice was subsequently revised on evidence, with the revision and its
   1.8 pp cost for danskvand reported in Ch6 §6.5.2 and carried as a limitation. An
   openly reported protocol deviation is standard and defensible; a concealed one is not.
2. **Narrow the pre-registration claim** to what genuinely was locked before results
   (the train/val/test split, the market scope, the ≥30-month filter) and explicitly
   exclude the representation choice from the locked set, noting it was an evaluated
   design dimension rather than a fixed parameter.
3. Rewrite `ch3:39` to brand×month with no acknowledgement. **Not recommended** — this is
   the same class of error as Ch4:11 (F7): a statement made to fit the current story
   rather than the record.

Note this is structurally identical to F7: in both cases the drafts assert something
tidier than what happened. Worth checking whether other "locked"/"pre-registered" claims
in Ch3/Ch4 survive contact with what was actually done.

<!-- append below -->
