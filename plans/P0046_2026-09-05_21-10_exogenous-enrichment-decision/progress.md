# P0047 — Progress

## Session 1 — 2026-09-05 — decision

Split out of P0043: the enrichment objection changes feature engineering, hence
training, hence every reported number, so it is not a prose fix.

Brian corrected two findings; **both weakened my case against enrichment**, and
neither was a point he had to concede.

- **F1** — I claimed the project had already tested holiday features. It had not.
  The 2026-08-18 change was a rename of a mislabelled peak-month rule.
- **F2** — The Prophet grain argument holds for holiday *windows*, not monthly
  *counts*.

**Decision: Option C, upstream of the funded runs.**
> *"exactly thats why I want to do it before we finish the experiments"*

## Session 2 — 2026-09-06 — built

### API

`nagerholidays.com/api/pro/` → 401 (commercial tier). Free tier is
`date.nager.at/api/v3/PublicHolidays/{year}/DK` (F4). Brian's BDBI exam script
used the correct host and served as the pattern for the fetch loop.

### Corrections Brian made during the build

| # | mine | correct |
|---|---|---|
| 1 | `trading_days` = weekdays − holidays | Danish retail trades weekends; `non_holiday_days = days_in_month − n_holidays` (F6) |
| 2 | Four objections to fetching during training | Three were answerable by the cache-with-timestamp I had *myself* proposed. Only the refetch-coupling point stood |
| 3 | Fetch tied to Nielsen refetch | Also needs standalone — a Nielsen pull is ~10 min minimum, ~2 h with raw |
| 4 | Asked two contract-schema questions | Not his call; decided them (F8) |

On (2) I stated the fix and then used it as an objection anyway. On (4) I asked
for a decision instead of making one after he had said to proceed.

### Built

| component | note |
|---|---|
| `_00_raw/holidays/fetch_holidays.py` | standalone + auto; per-year cache; manifest with timestamp + sha256 |
| `engineer_features.py::add_holiday_features` | `days_in_month`, `n_holidays`, `non_holiday_days` |
| `step_3_derive_params.py` | contract **v1.2**; decides + records reason |
| `step_4_engineer_features.py` | accepts v1.1 (unenriched) + v1.2; hard-fails if a promise is unmet |
| `save_all_datasets.py::_refresh_holidays` | `--force` on a Nielsen pull; never fails the Nielsen run |
| `export_holiday_appendix.py` | appendix tables 90–93 |

### Verified by running

- Fetch: 10 years cached, **15 holidays 2018–2023 → 14 from 2024** (F5)
- Features: Mar 2023 = 0 vs Mar 2024 = 3 (Easter); 2017 = NaN not 0
- Contract: covered panel → `True`; 2015-start panel → `False` with the exact fix command
- Both engineer paths: enriched emits 3 columns, unenriched emits none
- Mismatch guard raises; all 4 files compile
- **F9 bug found and fixed**: a narrow re-run shrank the manifest to 3 years while
  10 were cached — would have silently disabled enrichment

### Appendix (per P0046 provenance rules)

Tables 90–93 in `05_thesis_results/appendix/`, `.md` + `.csv` twins, all values
derived from the cache, `<!-- INTERNAL REVIEW -->` separators, output via
`PATHS.py`, root anchored on `.env.example`.

Table 92 (monthly matrix) is the anti-collinearity evidence (F7): December flat
at 4, March 0–4, April 0–5.

### Repo restructure

Mid-session the parallel session moved everything to SRQ tiers. All paths
updated; `PATHS.py` was already current. They also replaced my `parents[4]` hop
with an anchor-based root finder — a real improvement, kept.

**P-ID collision**: this plan renumbered **P0047**; the other keeps P0046
because `DEC-P0046-*` decision IDs reference it. Folder name still says P0046.

## Next session starts here

1. **Task 11 — the gate.** Re-run step 3 × 4 categories to emit v1.2 contracts.
   Until then existing v1.1 contracts keep running unenriched (correct, but the
   enrichment does nothing).
2. **Task 6** — benchmark with/without; per-category delta **whatever it is**,
   plus SHAP before/after to show it is not `month` re-encoded (F7).
3. **Task 7** — regenerate affected tables/figures.
4. **Task 12** — writing notes: reproducibility limitation (upstream revision can
   change features silently — accepted risk, must be stated), the
   `non_holiday_days` proxy caveat (F6), further exogenous sources as future work.
5. **Task 8** — close the five Word threads.

Then, and only then, P0042's funded runs.

### Open

- **School holidays**: no free API found (Brian). Out of scope by data
  availability — say so in the write-up rather than leaving it silent.
- **Both features or one?** `non_holiday_days` is an exact linear function of
  `n_holidays` given `days_in_month`. Task 6's SHAP pass decides whether all
  three earn their place; do not pre-empt it.
