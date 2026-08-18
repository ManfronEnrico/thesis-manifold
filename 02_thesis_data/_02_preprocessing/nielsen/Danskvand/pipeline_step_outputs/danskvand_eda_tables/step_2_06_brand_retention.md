## Brand Retention at Different MIN_PERIODS Thresholds

- How many brands survive each candidate minimum-observation threshold -- the retention curve for MIN_PERIODS.
- Thresholds are generated from the panel's own maximum span rather than the notebook's fixed 20-43 ladder, which had been written against CSD's 43-month history and produced empty rows elsewhere.
- The trade-off is explicit: a higher threshold buys longer, cleaner series at the cost of brand coverage. Look for the knee where retention falls sharply.
- Evidence only -- MIN_PERIODS is decided in step 3 (P0036 task 8).

|   Min Periods |   Brands Retained | % of Total   | Data Quality   |
|--------------:|------------------:|:-------------|:---------------|
|             5 |                43 | 78.2%        | Low            |
|            10 |                33 | 60.0%        | Low            |
|            15 |                30 | 54.5%        | Low            |
|            20 |                28 | 50.9%        | Low            |
|            25 |                27 | 49.1%        | Low            |
|            30 |                25 | 45.5%        | Medium         |
|            35 |                22 | 40.0%        | Medium         |
|            40 |                21 | 38.2%        | High           |
