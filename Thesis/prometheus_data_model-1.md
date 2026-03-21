The data is organized in a star schema with dimension tables and a central facts table.

**Database**: `Nielsen_clean`
**Schema**: `dbo`

| Table Type | Table Name                | Description               |
| ---------- | ------------------------- | ------------------------- |
| Dimension  | `csd_clean_dim_market_v`  | Market/retailer dimension |
| Dimension  | `csd_clean_dim_period_v`  | Time period dimension     |
| Dimension  | `csd_clean_dim_product_v` | Product dimension         |
| Fact       | `csd_clean_facts_v`       | Sales metrics fact table  |

---

## Dimension Tables

### csd_clean_dim_market_v

Market/retailer dimension table.

| Column               | Type    | Description                          | Sample Values                 |
| -------------------- | ------- | ------------------------------------ | ----------------------------- |
| `market_id`          | varchar | Primary key for the Market dimension | 1262112, 1256441, 1259957     |
| `market_description` | varchar | Market/retailer name                 | MENY, CONVENIENCE, NEMLIG.COM |

**Known market_description values** (n=28):

| market_description       |
| ------------------------ |
| 7-ELEVEN                 |
| BFI EXTRA                |
| BFI SHELL                |
| BILKA                    |
| BRUGSEN                  |
| CIRCLE K                 |
| CONVENIENCE              |
| COOP                     |
| DAGROFA                  |
| DVH EXCL. DISCOUNT/HD    |
| DVH EXCL. HD             |
| DVH/CONVENIENCE EXCL. HD |
| DVH/CONVENIENCE INCL. HD |
| FØTEX                    |
| GASOLINE/7-ELEVEN        |
| KVICKLY                  |
| MENY                     |
| MIN KØBMAND              |
| NEMLIG.COM               |
| NETTO                    |
| OK PLUS                  |
| Q8                       |
| REMA 1000                |
| SALLING GROUP            |
| SPAR                     |
| SUPERBRUGSEN             |
| TOTAL DISCOUNT           |

**Important**: Unless the user specifies a particular market, always use **DVH EXCL. HD** (Dagligvarehandel excluding hard discount) as the default, remember to explain to the user what EXCL. HD means.

**Danish Retail Landscape** (external group relationships):

- Coop Danmark: `COOP`, `BRUGSEN`, `SUPERBRUGSEN`, `KVICKLY`
- Salling Group: `SALLING GROUP`, `NETTO`, `FØTEX`, `BILKA`
- Dagrofa: `DAGROFA`, `MENY`, `SPAR`, `MIN KØBMAND`
- REITAN / REMA 1000: `REMA 1000`
- `NEMLIG.COM` is an online grocery brand

---

### csd_clean_dim_period_v

Time period dimension table (monthly periods; row count and latest month change as the database updates).

| Column         | Type    | Description                                | Sample Values       |
| -------------- | ------- | ------------------------------------------ | ------------------- |
| `period_id`    | varchar | Primary key for the Period dimension       | 40696, 40252, 40698 |
| `period_year`  | int     | Year when CSD facts were generated         | e.g., YYYY          |
| `period_month` | int     | Month (1–12) when CSD facts were generated | 1, 3, 11            |
| `date_key`     | varchar | Readable month + year format               | e.g., "Month YYYY"  |

---

### csd_clean_dim_product_v

Product dimension table. Dataset scope: **CSD only** (Carbonated Soft Drinks).

| Column             | Type    | Description                                                     | Sample Values                           |
| ------------------ | ------- | --------------------------------------------------------------- | --------------------------------------- |
| `product_id`       | varchar | Primary key for the Product dimension                           | 4722, 4947, 8397                        |
| `category`         | varchar | Product category — always "CSD"                                 | CSD                                     |
| `manufacturer`     | varchar | Manufacturer or producer                                        | VESTFYN, GLOBAL PREMIUM BRANDS          |
| `brand`            | varchar | Brand name                                                      | FANTA, PEPSI, COCA COLA                 |
| `ru_subbrand`      | varchar | Sub-brand name                                                  | FANTA LEMON, FAXE KONDI ORIGINAL        |
| `ru_variant`       | varchar | Product variant (flavor, sugar content)                         | GUARANA ANARCTICA REG                   |
| `packaging`        | varchar | Type of packaging                                               | DÅSE, GLAS, PLAST                       |
| `size_variants`    | varchar | Package size                                                    | 1.5 L, 33 CL, 75 CL                     |
| `units`            | varchar | Items per pack                                                  | 20 STK, 2 STK, 30 STK                   |
| `item_description` | varchar | Full product description                                        | FAXE KONDI SPECIEL EDITION 6\*75CL      |
| `upc_code`         | varchar | Universal Product Code (barcode)                                | 5710925015632                           |
| `type`             | varchar | Product flavor type                                             | COLA, LEMON/LIME, APPELSIN              |
| `regular_light`    | varchar | Regular or light (sugar-free)                                   | REGULAR, LIGHT                          |
| `price_category`   | varchar | Price segment                                                   | BILLIGVAND, MÆRKEVARE                   |
| `ru_cola_flavour`  | varchar | Cola flavor additions                                           | NA, FLAVOUR, NON FLAVOUR                |
| `organic`          | varchar | Organic indicator                                               | IKKE ØKOLOGISK, ØKOLOGISK               |
| `private_label`    | varchar | Retailer's own brand flag                                       | NON PRIVATE LABEL, PRIVATE LABEL        |
| `corporation_ru_1` | varchar | **Corporate group** (RU = Retail Unit in NielsenIQ terminology) | ROYAL UNIBREW, CARLSBERG, COCA COLA A/S |

**Key column**: `corporation_ru_1` identifies whether a product belongs to Royal Unibrew or a competitor.

**Note**: When searching for brands and subbrands, make sure to **capitalize the brand names** — consult sample values in the table.

---

## Fact Table

### csd_clean_facts_v

Central fact table with sales metrics

| Column                      | Type    | Description                                       | Sample Values       |
| --------------------------- | ------- | ------------------------------------------------- | ------------------- |
| `market_id`                 | varchar | Foreign key to Market dimension                   | 1262112, 1256441    |
| `period_id`                 | varchar | Foreign key to Period dimension                   | 40696, 40252        |
| `product_id`                | varchar | Foreign key to Product dimension                  | 1108, 16434         |
| `sales_value`               | float   | Sales value in Danish krone (DKK)                 | 0.0, 584.6, 10868.0 |
| `sales_in_liters`           | float   | Total sales volume in liters (L)                  | 0.0, 3819.42        |
| `sales_units`               | float   | Total number of units sold                        | 0.0, 22639.0        |
| `sales_value_any_promo`     | float   | Sales value (DKK) under any promotional activity  | 0.0, 139788.27      |
| `sales_in_liters_any_promo` | float   | Sales volume (L) under any promotion              | 0.0, 57681.24       |
| `sales_units_any_promo`     | float   | Units sold under any promotional activity         | 0.0, 1082.38        |
| `weighted_distribution`     | float   | Weighted Distribution (decimal, e.g., 0.93 = 93%) | 0.932636, 0.992521  |

---

