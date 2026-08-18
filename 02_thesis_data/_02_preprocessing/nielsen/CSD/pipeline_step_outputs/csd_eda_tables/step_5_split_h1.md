## Temporal split (CSD, horizon 1 month(s))

- Partitions are contiguous in time and non-overlapping: every validation month follows every training month, and every test month follows every validation month. This preserves the forecasting task, in which only the past is available at the time a prediction is made.
- Boundaries are proportional to the observed period rather than fixed dates, so the ratio holds as the panel grows and categories beginning at different dates remain comparable.
- At a 1-month horizon the test window admits 7 forecast origin(s): an origin is counted only when the month it targets falls inside the window.

| partition   |   months | period             |   rows |   brands |
|:------------|---------:|:-------------------|-------:|---------:|
| train       |       32 | 2022-10 .. 2025-05 |   3392 |      106 |
| val         |        7 | 2025-06 .. 2025-12 |    742 |      106 |
| test        |        7 | 2026-01 .. 2026-07 |    742 |      106 |
