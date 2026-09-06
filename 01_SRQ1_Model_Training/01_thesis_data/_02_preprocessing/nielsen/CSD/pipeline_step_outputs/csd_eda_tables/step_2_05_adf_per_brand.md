## ADF Test per Brand (top brands by volume)

- Augmented Dickey-Fuller test per brand. The null hypothesis is the presence of a unit root, that is, non-stationarity; a p-value below 0.05 rejects it in favour of stationarity (Dickey and Fuller, 1979).
- Failure to reject is weak evidence. The test has low power against near-unit-root alternatives in short samples, and these series span at most 46 monthly observations, so a non-rejection should be read as inconclusive rather than as evidence of a unit root.
- Non-stationary series motivate either differencing or the inclusion of lagged terms that allow the model to absorb the trend rather than extrapolate it.

| brand             |   n |   p_raw |   p_log |   p_diff | recommendation   |
|:------------------|----:|--------:|--------:|---------:|:-----------------|
| HARBOE            |  46 |  0.9950 |  0.9930 |   0.0000 | log1p+diff       |
| COCA COLA         |  46 |  0.0610 |  0.0000 |   0.0000 | log1p            |
| PEPSI             |  46 |  0.0170 |  0.0180 |   0.0020 | raw              |
| FAXE KONDI        |  46 |  0.9040 |  0.0770 |   0.0270 | log1p+diff       |
| FANTA             |  46 |  0.5680 |  0.5180 |   0.0000 | log1p+diff       |
| JOLLY             |  46 |  0.1140 |  0.0180 |   0.0000 | log1p            |
| TUBORG SQUASH     |  46 |  0.5600 |  0.8150 |   0.4710 | log1p+diff       |
| SCHWEPPES         |  46 |  0.0000 |  0.0020 |   0.0000 | raw              |
| HANCOCK           |  46 |  0.2760 |  0.3390 |   0.0000 | log1p+diff       |
| SAN PELLEGRINO    |  46 |  0.5000 |  0.3900 |   0.0000 | log1p+diff       |
| FEVER TREE        |  46 |  0.2220 |  0.0000 |   0.1630 | log1p            |
| HARBOE OTHER      |  46 |  0.0000 |  0.0000 |   0.0000 | raw              |
| EGO               |  46 |  0.8150 |  0.6150 |   0.0020 | log1p+diff       |
| SPRITE            |  46 |  0.2320 |  0.0840 |   0.0400 | log1p+diff       |
| ULUDAG            |  46 |  0.1880 |  0.2190 |   0.0000 | log1p+diff       |
| CARIBIA           |  46 |  0.8980 |  0.9010 |   0.0000 | log1p+diff       |
| FREM              |  46 |  0.6520 |  0.4160 |   0.0000 | log1p+diff       |
| THE PERFECT MIXER |  46 |  0.8670 |  1.0000 |   0.0040 | log1p+diff       |
| NORNIR            |  21 |  1.0000 |  0.0070 |   0.5340 | log1p            |
| RYNKEBY           |  19 |  0.0000 |  0.0000 |   0.0000 | raw              |
