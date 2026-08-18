## Brand Retention at Different MIN_PERIODS Thresholds

- How many brands survive each candidate minimum-observation threshold -- the retention curve for MIN_PERIODS.
- Thresholds are generated from the panel's own maximum span rather than the notebook's fixed 20-43 ladder, which had been written against CSD's 43-month history and produced empty rows elsewhere.
- The trade-off is explicit: a higher threshold buys longer, cleaner series at the cost of brand coverage. Look for the knee where retention falls sharply.
- Evidence only -- MIN_PERIODS is decided in step 3 (P0036 task 8).

|   Min Periods |   Brands Retained | % of Total   | Data Quality   |
|--------------:|------------------:|:-------------|:---------------|
|             5 |                62 | 91.2%        | Low            |
|            10 |                55 | 80.9%        | Low            |
|            15 |                50 | 73.5%        | Low            |
|            20 |                38 | 55.9%        | Low            |
|            25 |                34 | 50.0%        | Low            |
|            30 |                31 | 45.6%        | Medium         |
|            35 |                22 | 32.4%        | Medium         |
|            40 |                18 | 26.5%        | High           |
