# Nielsen Feature Inventory — cross-category

> Generated 2026-08-12 (P0038 task 2 follow-up). Regenerate with
> `_shared_modules/build_feature_inventory.py`.

Every column across all four category datasets, joined to Nielsen's own
metadata descriptions, with a real non-blank example value pulled from the data.

**Why this exists.** Brian asked whether a category might carry the forecast
target under a different name, and whether columns that look category-specific
are actually the same measure spelled differently. Both questions need the
metadata, not just the column names.

## Answers

**1. Does any category lack `sales_units`, or carry it under another name?**

**No.** `sales_units`, `sales_value` and `sales_in_liters` are present *verbatim*
in all four categories. Every candidate column matching
`sales|volume|units|qty|turnover|revenue|value|liter|amount` was checked against
the metadata; no aliasing exists for the target. The `REQUIRED_MEASURES` check in
step 1 therefore never fires in practice — it is a guard against a future
dataset, not a live constraint.

**2. Are some columns the same measure under different names?**

**Yes — three confirmed alias groups**, verified by *byte-identical metadata
descriptions*, not by name similarity:

| Measure | CSD | Energidrikke | RTD | Danskvand |
|---|---|---|---|---|
| display **and** feature | `…_disp_feat` | `…_disp_feat` | `…_disp_and_feat` | — |
| display **without** feature | `…_disp_w_o_feat` | `…_disp_wo_feat` | `…_disp_wo_feat` | — |
| feature **without** display | `…_feat_w_o_disp` | `…_feat_wo_disp` | `…_feat_wo_disp` | — |

Median values agree across the spellings (0.059/0.060 · 0.039–0.081 · 0.145–0.175),
consistent with the same underlying measure.

> **Not yet unified.** These are *reported*, not silently merged. Renaming one
> spelling to another is a modelling decision — it asserts the measures are
> interchangeable across categories — and that is Brian's call, not a porting
> side effect. Open as **DEC-ALIAS**.

**Caution — one false positive.** `…_disp_w_o_feat` and `…_feat_w_o_disp` contain
the *same tokens* but mean **opposite** things (display-without-feature vs
feature-without-display). Any automated token-based matcher pairs them wrongly.
Alias detection needs the descriptions; names alone are insufficient.

## Coverage

| Present in | Columns | Meaning |
|---|---|---|
| all 4 | 35 | shared core — safe for cross-category comparison |
| 3 | 17 | usually Danskvand missing (thinnest dataset) |
| 2 | 14 | includes the alias-group spellings |
| 1 | 35 | genuinely category-unique (mostly `dim_product` attributes) |

## Facts — measures

| Column | C D E R | Unit | Example | Description |
|---|---|---|---|---|
| `avg_no_of_items_per_store_reach` | Y Y Y Y | items | 36.1111 | Average number of items (SKUs) a brand/manufacturer/segment has per store, computed across sto… |
| `avg_number_of_stores_selling_reach` | Y Y Y Y | stores | 18.0 | Average number of stores in the universe that sold the product at any point during the period.… |
| `number_of_items_reach` | Y Y Y Y | items | 650.0 | Number of distinct UPC items (SKUs) within the selected product group that were sold at any po… |
| `numeric_distribution` | Y Y Y Y | fraction … | 1.0 | Average WEEKLY percentage of stores where the product was sold for the chosen period, stored a… |
| `numeric_distribution_reach` | Y Y Y Y | fraction … | 1.0 | Percentage of stores that sold the selected product at ANY point during the entire selected pe… |
| `sales_in_liters` | Y Y Y Y | liters | 7540.3459 | Total sales out of store expressed in litres. Includes both promo and non-promo volume. NULL =… |
| `sales_units` | Y Y Y Y | units | 2513.4486 | Total sales out of store expressed in consumer purchase units (individual packs / bottles / ca… |
| `sales_value` | Y Y Y Y | DKK | 16990.9294 | Total sales out of store expressed in Danish Krone (DKK). Consumer retail price including VAT … |
| `total_weighted_distribution_points_tdp_reach` | Y Y Y Y | decimal (… | 36.7202 | Total Distribution Points (TDP). Sum of weighted distribution across all items within a brand/… |
| `universe_number_of_stores` | Y Y Y Y | stores | 2726.75 | Total number of physical stores in the selected market universe. Market-level attribute, NOT p… |
| `weighted_distribution` | Y Y Y Y | fraction … | 1.0 | Average WEEKLY percentage of total CATEGORY TURNOVER (value sales) accounted for by stores tha… |
| `weighted_distribution_reach` | Y Y Y Y | fraction … | 1.0 | Percentage of total category turnover accounted for by stores that sold the selected product a… |
| `baseline_sales_in_liters` | Y · Y Y | liters | 90122.7822 | Modeled volume in litres that would have occurred without promotions. Same baseline-model logi… |
| `baseline_sales_in_liters_any_promo` | Y · Y Y | liters | 14060.8082 | Baseline volume in litres for the promoted portion. NULL = not modeled. |
| `baseline_sales_units` | Y · Y Y | units | 106118.9303 | Modeled units that would have occurred without promotions. NULL = not modeled. |
| `baseline_sales_units_any_promo` | Y · Y Y | units | 12912.3344 | Baseline units for the promoted portion. NULL = not modeled. |
| `baseline_sales_value` | Y · Y Y | DKK | 535345.2878 | Modeled value sales (DKK) that would have occurred in the absence of any promotions, calculate… |
| `baseline_sales_value_any_promo` | Y · Y Y | DKK | 74660.4241 | Baseline value sales (DKK) attributed specifically to the promoted portion. Used together with… |
| `sales_in_liters_any_promo` | Y · Y Y | liters | 83215.2318 | Volume in litres sold on any type of promotion. Subset of sales_in_liters. NULL = promo not tr… |
| `sales_units_any_tpr` | Y · Y Y | units | 195272.0553 | Units sold specifically on Temporary Price Reduction (TPR). TPR is a subset of 'any promo'. NU… |
| `sales_value_any_promo` | Y · Y Y | DKK | 463188.3853 | Value of sales (DKK) made on any type of promotion (TPR, display, feature, or any combination)… |
| `weighted_distribution_any_disp` | Y · Y Y | fraction … | 0.3995 | Percentage of category turnover (fraction 0-1) accounted for by stores that sold the product o… |
| `weighted_distribution_any_promo` | Y · Y Y | fraction … | 0.6895 | Percentage of category turnover (fraction 0-1) accounted for by stores that sold the product O… |
| `weighted_distribution_any_tpr` | Y · Y Y | fraction … | 0.6597 | Percentage of category turnover (fraction 0-1) accounted for by stores that sold the product o… |
| `weighted_distribution_total_feat` | Y · Y Y | fraction … | 0.3286 | Percentage of category turnover (fraction 0-1) accounted for by stores that promoted the produ… |
| `sales_units_any_promo` | Y · Y · | units | 197333.6973 | Units sold on any type of promotion. Subset of sales_units. NULL = promo not tracked. Not appl… |
| `weighted_distribution_disp_feat` | Y · Y · | fraction … | 0.1895 | Percentage of category turnover (fraction 0-1) accounted for by stores that sold the product w… |
| `weighted_distribution_disp_wo_feat` | · · Y Y | fraction … | 0.0773 | Percentage of category turnover (fraction 0-1) accounted for by stores that sold the product w… |
| `weighted_distribution_feat_wo_disp` | · · Y Y | fraction … | 0.9545 | Percentage of category turnover (fraction 0-1) accounted for by stores that sold the product w… |
| `weighted_distribution_disp_and_feat` | · · · Y | fraction … | 0.0277 | Percentage of category turnover (fraction 0-1) accounted for by stores that sold the product w… |
| `weighted_distribution_disp_w_o_feat` | Y · · · | fraction … | 0.3013 | Percentage of category turnover (fraction 0-1) accounted for by stores that sold the product w… |
| `weighted_distribution_feat_w_o_disp` | Y · · · | fraction … | 0.3286 | Percentage of category turnover (fraction 0-1) accounted for by stores that sold the product w… |

## Product dimension

| Column | C D E R | Unit | Example | Description |
|---|---|---|---|---|
| `brand` | Y Y Y Y |  | LEMONITA | Brand name as classified by Nielsen. The brand level sits below manufacturer and above sub-bra… |
| `manufacturer` | Y Y Y Y |  | MEGAFOOD APS | Manufacturer of the product as classified by Nielsen. One level below the corporation grouping… |
| `packaging` | Y Y Y Y |  | DÅSE | Packaging description for the product (e.g. 'CAN', 'PET', 'GLASS'). Captures the primary conta… |
| `private_label` | Y Y Y Y |  | NON PRIVATE LAB… | Flag indicating whether the product is a retailer private label (e.g. Coop's 365, REMA 1000 ow… |
| `product_hierarchy_level` | Y Y Y Y |  | 10 | Depth level of the product in the hierarchy. Level 1 = category total, Level 2 = manufacturer/… |
| `product_hierarchy_level_name` | Y Y Y Y |  | UPC | Human-readable name of the hierarchy level. Values vary by category: CSD uses 'CSD', 'MANUFACT… |
| `product_hierarchy_number` | Y Y Y Y |  | 1 | Dedup key within a hierarchy level. At level 1 (category) there are typically multiple rows re… |
| `product_id` | Y Y Y Y |  | 130714 | Foreign key to the Product dimension. Joins facts to product metadata. Never NULL. |
| `controlled_label` | Y Y Y · |  |  | Flag indicating whether the product is a controlled label — a brand owned by a retailer but ma… |
| `item` | · Y Y Y |  | ACTIVE O2 PEACH… | Item description — the canonical Nielsen item label, typically combining brand + variant + siz… |
| `ru_variant` | Y · Y Y |  | LEMONITA LEMON … | Royal Unibrew internal variant grouping. Below sub-brand in the RU-defined product hierarchy. … |
| `upc` | · Y Y Y |  | 4005906005193 | Universal Product Code / barcode of the SKU. Lowest level of the product hierarchy (one row pe… |
| `category` | Y · Y · |  | CSD | Top-level category label for this dataset: 'CSD' (Carbonated Soft Drinks). All rows in this da… |
| `corporation_1` | · · Y Y |  | CARLSBERG | Top-level corporate grouping (energidrikke/RTD datasets). Same concept as corporation_ru_1 (CS… |
| `corporation_ru_1` | Y Y · · |  |  | Top-level corporate grouping. Groups brands under their parent corporation as defined by RU/Ni… |
| `organic_indicator` | · Y · Y |  | IKKE ØKOLOGISK | Flag indicating whether the product is certified organic. Values are typically 'YES'/'NO' or c… |
| `price_category` | Y Y · · |  | MÆRKEVARE | Nielsen price tier classification (e.g. 'PREMIUM', 'STANDARD', 'ECONOMY'). Groups products by … |
| `quantity` | · · Y Y |  | 24 STK | Quantity descriptor for the multipack (e.g. number of consumer units in the pack). Stored as t… |
| `ru_price_segment` | · · Y Y |  | MÆRKEVARER | Royal Unibrew internal price segment classification. RU-defined price tier used for internal p… |
| `size_variants` | Y Y · · |  | 33 CL | Product size variant description (e.g. '33CL', '50CL', '6X33CL'). Only populated at lower hier… |
| `subbrands` | · · Y Y |  | MONSTER ENERGY | Sub-brand grouping below brand in the product hierarchy. Distinguishes brand extensions and li… |
| `units` | Y Y · · |  | 1 STK | Number of consumer units per multipack (e.g. '1', '6', '24'). Stored as text. |
| `ecology` | · · Y · |  | IKKE ØKOLOGISK | Ecology / organic indicator for the product (energy drinks dataset). Identifies products marke… |
| `energy_drinks` | · · Y · |  |  | Subset flag identifying products that are pure energy drinks (excludes vitamin drinks and spor… |
| `energy_drinks_vitamin_drinks` | · · Y · |  | ENERGIDRIKKE + … | Subset flag identifying products that are either energy drinks or vitamin drinks (excludes spo… |
| `flavor` | · Y · · |  | ØVRIG SMAG | Flavor variant of the product (e.g. 'CITRUS', 'BERRY', 'COLA'). Category-specific values. |
| `flavor_natural_indicator` | · Y · · |  | FLAVOR | Combined flavor + natural-flavor indicator. Identifies whether the flavoring is natural and wh… |
| `item_description` | Y · · · |  | LEMONITA LEMON … | Item description — the canonical Nielsen item label, typically combining brand + variant + siz… |
| `light_or_regular` | · · · Y |  | REG | Sugar content classification: regular (full sugar) vs. light/diet/zero (RTD dataset). |
| `organic` | Y · · · |  | IKKE ØKOLOGISK | Flag indicating whether the product is certified organic. Values are typically 'YES'/'NO' or c… |
| `packaging_excluding_controlled_label` | Y · · · |  | 1STK DÅSER | Packaging classification computed with controlled-label products excluded. Useful for clean pa… |
| `packaging_type` | · · Y · |  | DÅSE | Packaging type classification (e.g. 'CAN', 'PET BOTTLE', 'GLASS BOTTLE'). Captures container m… |
| `private_label_water` | · Y · · |  | OTHER | Flag indicating whether the sparkling/mineral water product is a retailer private label rather… |
| `product_type` | · Y · · |  | KILDEVAND M/SMAG | Product type classification within the category. Category-specific values. |
| `regular_light` | Y · · · |  | REGULAR | Sugar content classification: regular (full sugar) vs. light/diet/zero. CSD-specific. |
| `rtd_cider` | · · · Y |  | RTD / CIDER | Top-level classification for the RTD dataset, distinguishing RTD (ready-to-drink) cocktails fr… |
| `rtd_cider_excluding_drinks_cocktails` | · · · Y |  | RTD/CIDER ex DR… | RTD/cider classification with the DRINKS/COCKTAILS subsegment excluded. Useful for analyzing p… |
| `ru_cola_flavour` | Y · · · |  |  | Royal Unibrew internal classification of cola flavor variants (e.g. 'REGULAR COLA', 'CHERRY CO… |
| `ru_flavor` | · · · Y |  | LIME | Royal Unibrew internal flavor classification (RTD dataset). RU-defined flavor grouping. |
| `ru_segment` | · · · Y |  | ALKOHOLSODAVAND | Royal Unibrew internal segment classification (RTD dataset). RU-defined segmentation that may … |
| `ru_size` | · · · Y |  | 101- | Royal Unibrew internal size grouping (RTD / beer). Buckets pack sizes into RU-defined ranges. |
| `ru_subbrand` | Y · · · |  | LEMONITA LEMON | Royal Unibrew internal sub-brand grouping. RU-defined classification used for internal reporti… |
| `rub_flavor_variant` | · · Y · |  | ENERGI SMAG | Royal Unibrew flavor variant grouping (RUB = Royal Unibrew internal classification). |
| `rub_packaging` | · · · Y |  | GLAS | Royal Unibrew internal packaging grouping (RUB = Royal Unibrew internal classification). |
| `rub_sizes` | · · Y · |  | 41-60 CL | Royal Unibrew internal size grouping (energy drinks). Buckets pack sizes into RU-defined range… |
| `rub_sweet_water` | · Y · · |  | REGULAR WATER | Royal Unibrew internal grouping for sweetened/flavored water products (RUB = Royal Unibrew int… |
| `rub_total_brands` | · Y · · |  | OTHERS | Royal Unibrew internal grouping aggregating brand totals (water dataset). Used to roll up RU-r… |
| `segment` | · · Y · |  | ENERGIDRIK | Product segment classification within the category. Hierarchically broader than subsegment. Ex… |
| `sparkling_and_mineral_water` | · Y · · |  | DANSKVAND OG KI… | Top-level classification for the water dataset, distinguishing sparkling water from mineral wa… |
| `sub_product_class` | · Y · · |  | KILDEVAND | Sub-classification within the broader product class. Category-specific intermediate level betw… |
| `subsegment` | · · · Y |  | RTD | Finer segmentation below segment in the product hierarchy. Hierarchical CHILD of segment (e.g.… |
| `sugar_content` | · · Y · |  | ALM. | Sugar content classification for the product (e.g. 'REGULAR', 'SUGAR FREE', 'LOW SUGAR'). Ener… |
| `type` | Y · · · |  | LEMON/LIME | Product type classification within the category. Category-specific values; see the row's categ… |
| `upc_code` | Y · · · |  | 5706920102095 | Universal Product Code / barcode of the SKU. Lowest level of the product hierarchy (one row pe… |

## Period dimension

| Column | C D E R | Unit | Example | Description |
|---|---|---|---|---|
| `date_key` | Y Y Y Y |  | January 2026 | Combination of month and year as a single label (e.g. 'January 2026') for the CSD facts row. |
| `nielsen_calendar` | Y Y Y Y |  | 12F_445 | Nielsen calendar identifier (e.g. monthly calendar). Indicates which Nielsen periodicity calen… |
| `nielsen_periodicity` | Y Y Y Y |  | Months | Periodicity label / display folder used by Nielsen to group periods (e.g. monthly). Used for o… |
| `period_end_date` | Y Y Y Y |  | 2026-01-25 | The last calendar day of the measurement period. Nielsen Denmark uses monthly periods built on… |
| `period_id` | Y Y Y Y |  | 43679 | Foreign key to the Period dimension. Joins facts to period metadata. Never NULL. |
| `period_long_description` | Y Y Y Y |  | Jan 26 - 4 w/e … | Nielsen's original long label for the period as delivered. Human readable. |
| `period_month` | Y Y Y Y | months | 1 | Calendar month number 1-12 when the CSD facts row was generated. |
| `period_short_description` | Y Y Y Y |  | Jan 26 - 4 w/e … | Nielsen's original short label for the period as delivered (e.g. 'Jan 26'). Raw value preserve… |
| `period_year` | Y Y Y Y | years | 2026 | Calendar year (integer, e.g. 2026) when the CSD facts row was generated. Derived from period_e… |

## Market dimension

| Column | C D E R | Unit | Example | Description |
|---|---|---|---|---|
| `market_description` | Y Y Y Y |  | FØTEX FOOD | Human-readable name of the Nielsen market (retail chain, channel, or aggregate universe), e.g.… |
| `market_hierarchy_column` | Y Y Y Y |  |  | Internal Nielsen reference indicating which hierarchy column this market belongs to. Technical… |
| `market_hierarchy_level` | Y Y Y Y |  |  | Depth level of this market in Nielsen's Denmark retail hierarchy tree. Level 1 = top aggregate… |
| `market_hierarchy_name` | Y Y Y Y |  |  | Human-readable name of the hierarchy level (e.g. 'Total Grocery', 'Retail Chain', 'Channel'). … |
| `market_hierarchy_number` | Y Y Y Y |  |  | Numeric identifier for the market's position within its hierarchy level. Combined with market_… |
| `market_id` | Y Y Y Y |  | 2195816 | Foreign key to the Market dimension. Joins facts to market metadata. Never NULL. |

## Data-quality notes

**Negative values exist in every category** (~0.01–0.06% of rows) in the sales
measures — returns and Nielsen restatements. Step 1's positive-sales filter
(`sales_units > 0`) removes them at row level before aggregation.

RTD additionally carries small negatives in the `weighted_distribution*` family
(min −0.17), which are documented as fractions in 0–1. These survive the sales
filter because it only tests `sales_units`. Flagged for step 2 EDA — they are
rare, but they mean a distribution feature can be negative.

`Danskvand` is by far the thinnest dataset: no promo/baseline/display family at
all, which is why it lands at 15 panel columns vs 31–32 for the others.

## Legend

`C D E R` = CSD · Danskvand · Energidrikke · RTD. `Y` present, `·` absent.
