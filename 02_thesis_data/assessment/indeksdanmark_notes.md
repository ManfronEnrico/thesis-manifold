# Indeks Danmark Dataset Notes
> Source: Thesis/indeksdanmark_data_model-1.md + live file assessment 2026-04-13
> Last updated: 2026-04-13 — FILES DOWNLOADED AND ASSESSED
> Location: Thesis/indeksdanmark/

---

## Dataset Overview

| File | Size | Rows | Columns | Description |
|---|---|---|---|---|
| `indeksdanmark_data.csv` | 254 MB | 20,134 | 6,364 | Main survey data (all respondents) |
| `official_codebook.csv` | 1.8 MB | 6,364 | 11 | Variable documentation + survey weights |
| `indeksdanmark_metadata.csv` | 1.0 MB | 29,185 | 3 | Value label mappings (numeric → readable) |

**Data type**: All variables in main dataset are float64.  
**Status**: ✅ FILES AVAILABLE — `Thesis/indeksdanmark/`

---

## Codebook Structure (official_codebook.csv — 11 columns)

`Unnamed: 0`, `variable_name`, `variable_label`, `data_type`, `unique_values`, `missing_count`, `missing_percent`, `value_labels`, `missing_value_ranges`, `value_counts`, `weight`

The `weight` column contains the population weight for each variable. Use `VEJ_HH24` (Helårsvejning) from the main data as the row-level weight for population-representative analysis.

## Metadata Structure (indeksdanmark_metadata.csv — 3 columns)

`Variable`, `Value`, `Label` — maps numeric codes to readable labels.
Example: `STEMT_HH23` value `1.0` → "A: the Danish Social Democrats"

---

## CSD-Relevant Variables Identified

### Direct brand usage variables (missing ~76.9% — rotating module)

These variables are only asked to ~23% of respondents (~4,600 people). High missing rate is by survey design (rotating module), not data quality issue.

| Variable | Label |
|---|---|
| `K_565_03_001` | Awareness, CocaCola |
| `K_565_04_001` | Use CocaCola |
| `K_565_03_002` | Awareness, CocaCola light |
| `K_565_04_002` | Use CocaCola light |
| `K_565_03_014` | Know of CocaCola Zero Sugar |
| `K_565_04_014` | Use CocaCola Zero Sugar |
| `K_565_03_005` | Awareness, Pepsi Cola |
| `K_565_04_005` | Use Pepsi Cola |
| `K_565_03_007` | Awareness, Pepsi Max |
| `K_565_04_007` | Use Pepsi Max |
| `K_564_03_021` | Awareness, Fanta |
| `K_564_04_021` | Use Fanta |
| `K_564_03_032` | Awareness, Fanta Zero |
| `K_564_04_032` | Use Fanta Zero |
| `K_564_03_004` | Awareness, Faxe Kondi |
| `K_564_04_004` | Use Faxe Kondi |
| `K_564_03_033` | Awareness, Faxe Kondi 0 kalorier |
| `K_564_04_033` | Use Faxe Kondi 0 kalorier |
| `K_564_03_037` | Awareness, Faxe Kondi Orange |
| `K_564_04_037` | Use Faxe Kondi Orange |
| `K_564_03_011` | Awareness, Sprite |
| `K_564_04_011` | Use Sprite |
| `K_700_03_008` | Awareness, Faxe Kondi Booster |
| `K_700_04_008` | Use Faxe Kondi Booster |
| `K_600_01` | Usage, sports drink / energy drink |
| `K_600_02` | Loyalty, sports drink / energy drink |

### Retailer shopping frequency variables (missing ~33.3% — standard module)

~13,400 respondents answered these. Directly usable for consumer-to-retailer mapping.

| Variable | Label |
|---|---|
| `FORR03` | Kvickly |
| `FORR05` | Bilka |
| `FORR07` | Netto |
| `FORR11` | Føtex |
| `FORR13` | Rema 1000 |
| `FORR39` | MENY |
| `FORR23` | Spar |
| `FORR61` | Coop.dk |
| `FORR15` | Salling (province) |
| `DAGLIGVARER_1H14` | I buy daily groceries |

### Attitudinal / behavioural variables (missing 0% — all respondents)

| Variable | Label |
|---|---|
| `HOLD107` | I like to buy the supermarkets' cheap store brands when possible |
| `HOLD028` | I like to spend a little extra to get a good, wellknown brand |
| `HOLD108` | I prefer shopping in a physical store rather than online |
| `INDKOB` | Purchase influence in daily shopping |
| `AKT200` | Uses sugarfree products |
| `INT79` | Health (interest index) |
| `INT40` | Nutritional Health |

---

## Consumer-to-Retailer Mapping Strategy

The `FORR*` variables (retailer shopping frequency) are the key linkage mechanism:
- Each respondent answers how frequently they shop at each listed retailer
- Aggregate by segment → get a segment-level retailer affinity profile
- Map each Nielsen market to the corresponding `FORR*` variable
- Result: segment composition estimate per retailer → consumer demand index

Nielsen market → Indeks Danmark variable:
| Nielsen market | FORR variable |
|---|---|
| KVICKLY | FORR03 |
| BILKA | FORR05 |
| NETTO | FORR07 |
| FØTEX | FORR11 |
| REMA 1000 | FORR13 |
| MENY | FORR39 |
| SPAR | FORR23 |
| SALLING GROUP | FORR15 |

---

## Data Security Note

- Indeks Danmark contains consumer survey data with personal/behavioral attributes
- Must remain local — no external uploads
- Survey weights (`VEJ_HH24`) must be applied for population-representative analysis

---

## RAM Estimate

Loading full 254 MB CSV with pandas: ~970 MB in memory (float64, 20K × 6.4K).
**Strategy**: Load only selected CSD-relevant columns (~50 variables) → ~8 MB in memory.
Use codebook to pre-filter column list before `pd.read_csv(..., usecols=[...])`.
