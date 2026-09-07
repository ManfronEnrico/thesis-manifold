## Temporal split (Energidrikke, horizon 3 month(s))

- Partitions are contiguous in time and non-overlapping: every validation month follows every training month, and every test month follows every validation month. This preserves the forecasting task, in which only the past is available at the time a prediction is made.
- Boundaries are proportional to the observed period rather than fixed dates, so the ratio holds as the panel grows and categories beginning at different dates remain comparable.
- At a 3-month horizon the test window admits 5 forecast origin(s): an origin is counted only when the month it targets falls inside the window.

| partition   |   months | period             |   rows |   brands |
|:------------|---------:|:-------------------|-------:|---------:|
| train       |       30 | 2023-01 .. 2025-06 |   1320 |       44 |
| val         |        6 | 2025-07 .. 2025-12 |    264 |       44 |
| test        |        7 | 2026-01 .. 2026-07 |    308 |       44 |
