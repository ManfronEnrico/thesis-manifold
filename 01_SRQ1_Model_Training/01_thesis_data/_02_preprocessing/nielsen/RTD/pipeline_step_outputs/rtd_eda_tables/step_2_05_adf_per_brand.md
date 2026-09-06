## ADF Test per Brand (top brands by volume)

- Augmented Dickey-Fuller test per brand. The null hypothesis is the presence of a unit root, that is, non-stationarity; a p-value below 0.05 rejects it in favour of stationarity (Dickey and Fuller, 1979).
- Failure to reject is weak evidence. The test has low power against near-unit-root alternatives in short samples, and these series span at most 46 monthly observations, so a non-rejection should be read as inconclusive rather than as evidence of a unit root.
- Non-stationary series motivate either differencing or the inclusion of lagged terms that allow the model to absorb the trend rather than extrapolate it.

| brand                |   n |   p_raw |   p_log |   p_diff | recommendation   |
|:---------------------|----:|--------:|--------:|---------:|:-----------------|
| BREEZER              |  41 |  0.2390 |  0.0000 |   0.0360 | log1p            |
| SHAKER               |  41 |  0.8770 |  0.7280 |   0.0140 | log1p+diff       |
| SMIRNOFF ICE/TWISTED |  41 |  0.0000 |  0.0000 |   0.0460 | raw              |
| SOMERSBY             |  41 |  0.4940 |  0.0000 |   0.0000 | log1p            |
| MOKAÏ                |  41 |  0.6910 |  0.9770 |   0.0350 | log1p+diff       |
| READY TO DRINK       |  41 |  0.0000 |  0.0000 |   0.0010 | raw              |
| IMPRESS              |  41 |  0.0080 |  0.9220 |   0.0000 | raw              |
| TANQUERAY            |  41 |  0.0000 |  0.8500 |   0.0510 | raw              |
| CULT MODJO           |  22 |  0.4550 |  0.9760 |   0.0110 | log1p+diff       |
| PUNCH! CLUB          |  38 |  0.1010 |  0.0440 |   0.1360 | log1p            |
| NOHRLUND             |  41 |  0.2320 |  1.0000 |   0.0010 | log1p+diff       |
| BUZZBALLZ            |  41 |  0.0180 |  0.0330 |   0.1710 | raw              |
| MIKROPOLIS COCKTAILS |  41 |  0.1970 |  0.6670 |   0.0120 | log1p+diff       |
| ISH                  |  14 |  0.3890 |  0.2150 |   0.0000 | log1p+diff       |
| THE COCKTAIL FACTORY |  41 |  0.0000 |  0.9990 |   0.5290 | raw              |
| MAGNERS              |  41 |  0.8780 |  0.5300 |   0.0060 | log1p+diff       |
| SPRITZ               |  30 |  0.0000 |  0.0110 |   0.0070 | raw              |
| REKORDERLIG          |  41 |  0.2240 |  0.3040 |   0.0010 | log1p+diff       |
| SIR. JAMES 101       |  41 |  0.0060 |  0.2920 |   0.0000 | raw              |
