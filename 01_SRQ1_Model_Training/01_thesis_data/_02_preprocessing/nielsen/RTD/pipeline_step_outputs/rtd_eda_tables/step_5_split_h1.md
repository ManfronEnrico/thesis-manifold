## Temporal split (RTD, horizon 1 month(s))

- Partitions are contiguous in time and non-overlapping: every validation month follows every training month, and every test month follows every validation month. This preserves the forecasting task, in which only the past is available at the time a prediction is made.
- Boundaries are proportional to the observed period rather than fixed dates, so the ratio holds as the panel grows and categories beginning at different dates remain comparable.
- At a 1-month horizon the test window admits 6 forecast origin(s): an origin is counted only when the month it targets falls inside the window.

| partition   |   months | period             |   rows |   brands |
|:------------|---------:|:-------------------|-------:|---------:|
| train       |       29 | 2023-03 .. 2025-07 |   2088 |       72 |
| val         |        6 | 2025-08 .. 2026-01 |    432 |       72 |
| test        |        6 | 2026-02 .. 2026-07 |    432 |       72 |
