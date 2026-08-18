## Brand Retention at Different MIN_PERIODS Thresholds

- How many brands survive each candidate minimum-observation threshold -- the retention curve for MIN_PERIODS.
- Thresholds are generated from the panel's own maximum span rather than the notebook's fixed 20-43 ladder, which had been written against CSD's 43-month history and produced empty rows elsewhere.
- The trade-off is explicit: a higher threshold buys longer, cleaner series at the cost of brand coverage. Look for the knee where retention falls sharply.
- Evidence only -- MIN_PERIODS is decided in step 3 (P0036 task 8).

|   Min Periods |   Brands Retained | % of Total   | Data Quality   |
|--------------:|------------------:|:-------------|:---------------|
|             5 |                90 | 89.1%        | Low            |
|            10 |                81 | 80.2%        | Low            |
|            15 |                72 | 71.3%        | Low            |
|            20 |                56 | 55.4%        | Low            |
|            25 |                51 | 50.5%        | Low            |
|            30 |                46 | 45.5%        | Medium         |
|            35 |                41 | 40.6%        | Medium         |
|            40 |                34 | 33.7%        | High           |
