# Train, Validation, and Test Split

> Section of **Data Assessment > Train, Validation, and Test Split**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**8 comment(s) on this section** -- INCORRECT, SOURCE, VERIFY, METACOMMENT. Detail: `comments/sections/08-ch4-data-assessment/04-train-validation-and-test-split.md`

---

The split is defined by calendar date and locked as a pre-specified design decision, applied identically across the forecasting models and across categories. No random shuffling is applied: a strict temporal split preserves the autocorrelation structure and prevents leakage of future observations into training or validation.
Because the categories differ in length, the split is expressed as contiguous chronological blocks per category (training → validation → test), with the test window placed in the most recent months relevant to Manifold AI’s planning horizon and covering at least one autumn/winter promotional cycle. The training window is required to satisfy the ARIMA minimum (~24 periods) and to contain at least two seasonal cycles for Prophet.
The per-category boundaries, taken from the locked split files (<cat>_split_dates.json), are:
| Category | Periods | Train | Valid. | Test | Train window | Validation window | Test window |
|---|---|---|---|---|---|---|---|
| CSD | 42 | 24 | 6 | 12 | 2022-10 → 2024-09 | 2024-10 → 2025-03 | 2025-04 → 2026-03 |
| danskvand | 37 | 23 | 6 | 8 | 2023-03 → 2025-01 | 2025-02 → 2025-07 | 2025-08 → 2026-03 |
| energidrikke | 39 | 25 | 6 | 8 | 2023-01 → 2025-01 | 2025-02 → 2025-07 | 2025-08 → 2026-03 |
| RTD | 37 | 23 | 6 | 8 | 2023-03 → 2025-01 | 2025-02 → 2025-07 | 2025-08 → 2026-03 |
**Table** **5** - Forward-chaining train/validation/test boundaries per category (locked, pre-registered)
CSD, the longest series, takes a 12-month test window covering a full annual cycle; the three shorter categories take an 8-month test window (a ≥40-month series would be needed for a 12-month test under the same rule). Every training window satisfies the ARIMA minimum (~24 periods; danskvand and RTD at 23 are marginally below and are flagged as a thin-data caveat in §4.6) and contains at least two seasonal cycles for Prophet. All test windows end in March 2026 and cover at least one autumn/winter promotional cycle.
