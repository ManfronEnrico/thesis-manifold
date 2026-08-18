## Rows per Brand Distribution

- Distribution of observation counts per brand -- how much history each brand actually has.
- Directly relevant to MIN_PERIODS: a brand with few observations cannot support lag-12 features and contributes mostly warmup rows. The threshold decision is step 3's (P0036 task 8 open); this table is its evidence.
- A long left tail means the panel is dominated by short-lived brands, which is a case for filtering rather than pooling them in.

| Statistic   |   Rows/Brand |
|:------------|-------------:|
| Min         |       1.0000 |
| Max         |      41.0000 |
| Mean        |      22.3000 |
| Median      |      20.0000 |
| Std Dev     |      17.0000 |
