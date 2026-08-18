## ADF Test per Brand (top brands by volume)

- Augmented Dickey-Fuller test per brand. Null hypothesis is a unit root, i.e. non-stationarity; p < 0.05 rejects it and indicates a stationary series (Dickey & Fuller, 1979).
- Failing to reject is weak evidence -- ADF has low power on short series, and these brands have at most ~46 monthly observations. Read a non-rejection as inconclusive, not as proof of a unit root.
- Non-stationary brands are the argument for differencing or for lag features that let the model absorb the trend rather than extrapolate it.

| brand              |   n |   p_raw |   p_log |   p_diff | recommendation   |
|:-------------------|----:|--------:|--------:|---------:|:-----------------|
| RED BULL           |  43 |  0.9540 |  0.9340 |   0.0000 | log1p+diff       |
| MONSTER ENERGY     |  43 |  0.9990 |  0.9980 |   0.0450 | log1p+diff       |
| FAXE KONDI BOOSTER |  43 |  0.8570 |  0.7060 |   0.0010 | log1p+diff       |
| CULT               |  43 |  0.9970 |  0.9990 |   0.0460 | log1p+diff       |
| STATE              |  43 |  0.0000 |  0.0000 |   0.0000 | raw              |
| VITAMIN WELL       |  43 |  0.0010 |  0.0030 |   0.0060 | raw              |
| X-RAY              |  33 |  0.9990 |  0.9980 |   0.0290 | log1p+diff       |
| POWERADE           |  43 |  0.0000 |  0.0000 |   0.0000 | raw              |
| PRIME              |  39 |  0.0000 |  0.3910 |   0.1670 | raw              |
| XRAY               |  10 |  0.0890 |  0.0030 |   0.0500 | log1p            |
| NOCCO              |  43 |  0.9320 |  0.0090 |   0.0000 | log1p            |
| FAXE KONDI PRO     |  30 |  0.2710 |  0.0000 |   0.0000 | log1p            |
| ROCKSTAR           |  43 |  0.8880 |  0.9640 |   0.4680 | log1p+diff       |
| NAILED             |  17 |  0.1540 |  0.3220 |   0.1200 | log1p+diff       |
| PURE               |  16 |  0.6870 |  0.1190 |   0.0010 | log1p+diff       |
| POWERKING          |  43 |  0.7600 |  0.6670 |   0.9870 | log1p+diff       |
| STATE VITAMIN      |  43 |  0.0060 |  0.0620 |   0.0000 | raw              |
| GATORADE           |  43 |  0.0020 |  0.0250 |   0.0000 | raw              |
| SMAG               |  43 |  0.0440 |  0.8520 |   0.0040 | raw              |
| BLACK ENERGY       |  14 |  0.0000 |  0.7480 |   0.0030 | raw              |
