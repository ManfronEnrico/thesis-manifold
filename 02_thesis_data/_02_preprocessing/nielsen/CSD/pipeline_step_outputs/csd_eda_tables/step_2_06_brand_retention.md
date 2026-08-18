## Brand Retention at Different MIN_PERIODS Thresholds

- How many brands survive each candidate minimum-observation threshold -- the retention curve for MIN_PERIODS.
- Thresholds are generated from the panel's own maximum span rather than the notebook's fixed 20-43 ladder, which had been written against CSD's 43-month history and produced empty rows elsewhere.
- The trade-off is explicit: a higher threshold buys longer, cleaner series at the cost of brand coverage. Look for the knee where retention falls sharply.
- Evidence only -- MIN_PERIODS is decided in step 3 (P0036 task 8).

|   Min Periods |   Brands Retained | % of Total   | Data Quality   |
|--------------:|------------------:|:-------------|:---------------|
|             5 |               130 | 91.5%        | Low            |
|            10 |               119 | 83.8%        | Low            |
|            15 |               106 | 74.6%        | Low            |
|            20 |                89 | 62.7%        | Low            |
|            25 |                85 | 59.9%        | Low            |
|            30 |                79 | 55.6%        | Medium         |
|            35 |                70 | 49.3%        | Medium         |
|            40 |                62 | 43.7%        | High           |
|            45 |                57 | 40.1%        | High           |
