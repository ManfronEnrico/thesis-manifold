# Nielsen Fabric Database Schema Snapshot

**Database:** Nielsen_clean
**Snapshot Date:** 2026-04-22T14:20:45.056224
**Server:** 4xv7ztimpg6exks34r6loehyv4-ydoclh536ovebaf5eboh67x6ke.datawarehouse.fabric.microsoft.com

---

## Summary

| Type | Count |
|------|-------|
| Views (cleaned data) | 20 |
| Base Tables (raw data) | 23 |
| Metadata Tables | 9 |
| **Total** | **52** |

---

## Views (Cleaned Data — Use These for Modeling)

### csd_clean_dim_market_v
**Rows:** 28 | **Columns:** 2
**Column List:** `market_id, market_description`

### csd_clean_dim_period_v
**Rows:** 42 | **Columns:** 4
**Column List:** `period_id, period_year, period_month, date_key`

### csd_clean_dim_product_v
**Rows:** 2,057 | **Columns:** 18
**Column List:** `product_id, category, manufacturer, brand, ru_subbrand, ru_variant, packaging, size_variants, units, item_description, upc_code, type, regular_light, price_category, ru_cola_flavour, organic, private_label, corporation_ru_1`

### csd_clean_facts_v
**Rows:** 2,535,464 | **Columns:** 10
**Column List:** `market_id, period_id, product_id, sales_value, sales_in_liters, sales_units, sales_value_any_promo, sales_in_liters_any_promo, sales_units_any_promo, weighted_distribution`

### danskvand_clean_dim_market_v
**Rows:** 86 | **Columns:** 2
**Column List:** `market_id, market_description`

### danskvand_clean_dim_period_v
**Rows:** 37 | **Columns:** 4
**Column List:** `period_id, period_year, period_month, date_key`

### danskvand_clean_dim_product_v
**Rows:** 566 | **Columns:** 24
**Column List:** `product_id, sparkling_and_mineral_water, corporation_ru_1, manufacturer, brand, sub_product_class, item, upc, product_type, price_category, flavor, flavor_natural_indicator, private_label_water, packaging, rub_sweet_water, units, size_variants, organic_indicator, private_label, controlled_label, product_hierarchy_number, product_hierarchy_level, product_hierarchy_level_name, rub_total_brands`

### danskvand_clean_facts_v
**Rows:** 1,248,913 | **Columns:** 15
**Column List:** `market_id, period_id, product_id, sales_value, sales_in_liters, sales_units, numeric_distribution, numeric_distribution_reach, weighted_distribution, weighted_distribution_reach, total_weighted_distribution_points_tdp_reach, number_of_items_reach, avg_number_of_stores_selling_reach, universe_number_of_stores, avg_no_of_items_per_store_reach`

### energidrikke_clean_dim_market_v
**Rows:** 86 | **Columns:** 2
**Column List:** `market_id, market_description`

### energidrikke_clean_dim_period_v
**Rows:** 39 | **Columns:** 4
**Column List:** `period_id, period_year, period_month, date_key`

### energidrikke_clean_dim_product_v
**Rows:** 748 | **Columns:** 25
**Column List:** `product_id, category, segment, corporation_1, brand, subbrands, sugar_content, ru_variant, packaging, item, upc, ru_price_segment, rub_sizes, packaging_type, quantity, rub_flavor_variant, ecology, energy_drinks_vitamin_drinks, energy_drinks, private_label, controlled_label, product_hierarchy_number, product_hierarchy_level, product_hierarchy_level_name, manufacturer`

### energidrikke_clean_facts_v
**Rows:** 3,112,010 | **Columns:** 32
**Column List:** `market_id, period_id, product_id, sales_value, sales_in_liters, sales_units, sales_value_any_promo, sales_in_liters_any_promo, sales_units_any_promo, sales_units_any_tpr, numeric_distribution, numeric_distribution_reach, weighted_distribution, weighted_distribution_reach, total_weighted_distribution_points_tdp_reach, number_of_items_reach, avg_number_of_stores_selling_reach, universe_number_of_stores, avg_no_of_items_per_store_reach, weighted_distribution_any_promo, weighted_distribution_disp_feat, weighted_distribution_disp_wo_feat, weighted_distribution_feat_wo_disp, weighted_distribution_total_feat, weighted_distribution_any_disp, weighted_distribution_any_tpr, baseline_sales_value, baseline_sales_in_liters, baseline_sales_units, baseline_sales_value_any_promo, baseline_sales_in_liters_any_promo, baseline_sales_units_any_promo`

### rtd_clean_dim_market_v
**Rows:** 86 | **Columns:** 2
**Column List:** `market_id, market_description`

### rtd_clean_dim_period_v
**Rows:** 37 | **Columns:** 4
**Column List:** `period_id, period_year, period_month, date_key`

### rtd_clean_dim_product_v
**Rows:** 590 | **Columns:** 24
**Column List:** `product_id, rtd_cider, corporation_1, brand, subsegment, subbrands, ru_variant, packaging, item, upc, ru_price_segment, ru_size, quantity, ru_flavor, ru_segment, organic_indicator, rub_packaging, light_or_regular, rtd_cider_excluding_drinks_cocktails, private_label, product_hierarchy_number, product_hierarchy_level, product_hierarchy_level_name, manufacturer`

### rtd_clean_facts_v
**Rows:** 2,161,268 | **Columns:** 31
**Column List:** `market_id, period_id, product_id, sales_value, sales_in_liters, sales_units, baseline_sales_value, baseline_sales_in_liters, baseline_sales_units, baseline_sales_value_any_promo, baseline_sales_in_liters_any_promo, baseline_sales_units_any_promo, sales_value_any_promo, sales_in_liters_any_promo, sales_units_any_tpr, numeric_distribution, numeric_distribution_reach, weighted_distribution, weighted_distribution_reach, total_weighted_distribution_points_tdp_reach, number_of_items_reach, avg_number_of_stores_selling_reach, universe_number_of_stores, avg_no_of_items_per_store_reach, weighted_distribution_any_promo, weighted_distribution_disp_and_feat, weighted_distribution_disp_wo_feat, weighted_distribution_feat_wo_disp, weighted_distribution_total_feat, weighted_distribution_any_disp, weighted_distribution_any_tpr`

### totalbeer_clean_dim_market_v
**Rows:** 86 | **Columns:** 2
**Column List:** `market_id, market_description`

### totalbeer_clean_dim_period_v
**Rows:** 39 | **Columns:** 4
**Column List:** `period_id, period_year, period_month, date_key`

### totalbeer_clean_dim_product_v
**Rows:** 5,609 | **Columns:** 35
**Column List:** `product_id, category, manufacturer, brand, segment, subsegment, ru_subbrand, ru_variant, packaging_1, item, upc, ru_size, gift_box_or_calendar, beer_mixes, beer_type, size_variants, packaging_2, quantity, price_category, sub_product_class, foreign_beer, christmas_or_easter_beer, organic, alcohol_percentage, special_beer, packaging_limited_size, private_label, controlled_label, product_hierarchy_number, product_hierarchy_level, product_hierarchy_level_name, corporation_ru, rub_manufacturer_total, segment_christmas_easter_beer_ex_cl, beer_type_segment`

### totalbeer_clean_facts_v
**Rows:** 15,497,265 | **Columns:** 36
**Column List:** `market_id, period_id, product_id, sales_value, sales_in_liters, sales_units, sales_value_any_promo, sales_value_any_tpr, sales_in_liters_any_promo, sales_in_liters_any_tpr, sales_units_any_promo, sales_units_any_tpr, baseline_sales_value, baseline_sales_in_liters, baseline_sales_units, baseline_sales_value_any_promo, baseline_sales_in_liters_any_promo, baseline_sales_units_any_promo, numeric_distribution, numeric_distribution_reach, weighted_distribution, weighted_distribution_reach, total_weighted_distribution_points_tdp_reach, number_of_items_reach, avg_number_of_stores_selling_reach, universe_number_of_stores, avg_no_of_items_per_store_reach, weighted_distribution_any_promo, weighted_distribution_disp_feat, weighted_distribution_disp_w_o_feat, weighted_distribution_feat_w_o_disp, weighted_distribution_total_feat, weighted_distribution_any_disp, weighted_distribution_any_tpr, tdp_weighted_distribution_any_promo, tdp_weighted_distribution_any_tpr`

---

## Base Tables (Raw Data)

### beer_clean_data
**Rows:** 1,112,372 | **Columns:** 41
**Column List:** `sales_value, sales_in_liters, sales_units, sales_value_any_promo, sales_in_liters_any_promo, sales_units_any_promo, weighted_distribution, market_description, category, manufacturer, brand, segment, subsegment, ru_subbrand, ru_variant, packaging_1, item, upc, ru_size, gift_box_or_calendar, beer_mixes, beer_type, size_variants, packaging_2, quantity, price_category, sub_product_class, foreign_beer, organic, alcohol_percentage, special_beer, packaging_limited_size, private_label, corporation_ru, rub_manufacturer_total, segment_christmas_easter_beer_ex_cl, beer_type_segment, period_year, period_month, date_key, last_server_update`

### csd_clean_data
**Rows:** 447,088 | **Columns:** 29
**Column List:** `sales_value, sales_in_liters, sales_units, sales_value_any_promo, sales_in_liters_any_promo, sales_units_any_promo, weighted_distribution, market_description, category, manufacturer, brand, ru_subbrand, ru_variant, packaging, size_variants, units, item_description, upc_code, type, regular_light, price_category, ru_cola_flavour, organic, private_label, corporation_ru_1, period_year, period_month, date_key, last_server_update`

### csd_clean_dim_market
**Rows:** 587 | **Columns:** 13
**Column List:** `market_id, market_description, market_hierarchy_level, market_hierarchy_number, market_hierarchy_name, market_hierarchy_column, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, valid_from, valid_to, change_detection_hash`

### csd_clean_dim_period
**Rows:** 152 | **Columns:** 16
**Column List:** `period_id, period_short_description, period_long_description, period_end_date, nielsen_calendar, nielsen_periodicity, period_year, period_month, date_key, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, valid_from, valid_to, change_detection_hash`

### csd_clean_dim_product
**Rows:** 49,287 | **Columns:** 30
**Column List:** `product_id, category, manufacturer, brand, ru_subbrand, ru_variant, packaging, size_variants, units, item_description, upc_code, type, regular_light, price_category, ru_cola_flavour, organic, private_label, controlled_label, product_hierarchy_number, product_hierarchy_level, product_hierarchy_level_name, packaging_excluding_controlled_label, corporation_ru_1, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, valid_from, valid_to, change_detection_hash`

### csd_clean_facts
**Rows:** 33,772,741 | **Columns:** 39
**Column List:** `market_id, period_id, product_id, sales_value, sales_in_liters, sales_units, sales_value_any_promo, sales_in_liters_any_promo, sales_units_any_promo, sales_units_any_tpr, baseline_sales_value, baseline_sales_in_liters, baseline_sales_units, baseline_sales_value_any_promo, baseline_sales_in_liters_any_promo, baseline_sales_units_any_promo, numeric_distribution, numeric_distribution_reach, weighted_distribution, weighted_distribution_reach, total_weighted_distribution_points_tdp_reach, number_of_items_reach, avg_number_of_stores_selling_reach, universe_number_of_stores, avg_no_of_items_per_store_reach, weighted_distribution_any_promo, weighted_distribution_disp_feat, weighted_distribution_disp_w_o_feat, weighted_distribution_feat_w_o_disp, weighted_distribution_total_feat, weighted_distribution_any_disp, weighted_distribution_any_tpr, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, valid_from, valid_to, change_detection_hash`

### danskvand_clean_dim_market
**Rows:** 254 | **Columns:** 13
**Column List:** `market_id, market_description, market_hierarchy_level, market_hierarchy_number, market_hierarchy_name, market_hierarchy_column, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### danskvand_clean_dim_period
**Rows:** 57 | **Columns:** 16
**Column List:** `period_id, period_short_description, period_long_description, period_end_date, nielsen_calendar, nielsen_periodicity, period_year, period_month, date_key, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### danskvand_clean_dim_product
**Rows:** 3,198 | **Columns:** 31
**Column List:** `product_id, sparkling_and_mineral_water, corporation_ru_1, manufacturer, brand, sub_product_class, item, upc, product_type, price_category, flavor, flavor_natural_indicator, private_label_water, packaging, rub_sweet_water, units, size_variants, organic_indicator, private_label, controlled_label, product_hierarchy_number, product_hierarchy_level, product_hierarchy_level_name, rub_total_brands, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### danskvand_clean_facts
**Rows:** 1,987,353 | **Columns:** 22
**Column List:** `market_id, period_id, product_id, sales_value, sales_in_liters, sales_units, numeric_distribution, numeric_distribution_reach, weighted_distribution, weighted_distribution_reach, total_weighted_distribution_points_tdp_reach, number_of_items_reach, avg_number_of_stores_selling_reach, universe_number_of_stores, avg_no_of_items_per_store_reach, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### energidrikke_clean_dim_market
**Rows:** 430 | **Columns:** 13
**Column List:** `market_id, market_description, market_hierarchy_level, market_hierarchy_number, market_hierarchy_name, market_hierarchy_column, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### energidrikke_clean_dim_period
**Rows:** 104 | **Columns:** 16
**Column List:** `period_id, period_short_description, period_long_description, period_end_date, nielsen_calendar, nielsen_periodicity, period_year, period_month, date_key, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### energidrikke_clean_dim_product
**Rows:** 11,866 | **Columns:** 32
**Column List:** `product_id, category, segment, corporation_1, brand, subbrands, sugar_content, ru_variant, packaging, item, upc, ru_price_segment, rub_sizes, packaging_type, quantity, rub_flavor_variant, ecology, energy_drinks_vitamin_drinks, energy_drinks, private_label, controlled_label, product_hierarchy_number, product_hierarchy_level, product_hierarchy_level_name, manufacturer, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### energidrikke_clean_facts
**Rows:** 9,501,956 | **Columns:** 39
**Column List:** `market_id, period_id, product_id, sales_value, sales_in_liters, sales_units, sales_value_any_promo, sales_in_liters_any_promo, sales_units_any_promo, sales_units_any_tpr, numeric_distribution, numeric_distribution_reach, weighted_distribution, weighted_distribution_reach, total_weighted_distribution_points_tdp_reach, number_of_items_reach, avg_number_of_stores_selling_reach, universe_number_of_stores, avg_no_of_items_per_store_reach, weighted_distribution_any_promo, weighted_distribution_disp_feat, weighted_distribution_disp_wo_feat, weighted_distribution_feat_wo_disp, weighted_distribution_total_feat, weighted_distribution_any_disp, weighted_distribution_any_tpr, baseline_sales_value, baseline_sales_in_liters, baseline_sales_units, baseline_sales_value_any_promo, baseline_sales_in_liters_any_promo, baseline_sales_units_any_promo, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### energydrink_clean_data
**Rows:** 554,965 | **Columns:** 32
**Column List:** `sales_value, sales_in_liters, sales_units, sales_value_any_promo, sales_in_liters_any_promo, sales_units_any_promo, weighted_distribution, market_description, segment, corporation_1, brand, subbrands, sugar_content, ru_variant, packaging, item, upc, ru_price_segment, rub_sizes, packaging_type, quantity, rub_flavor_variant, ecology, energy_drinks_vitamin_drinks, energy_drinks, private_label, manufacturer, period_year, period_month, date_key, last_server_update, category`

### rtd_clean_dim_market
**Rows:** 254 | **Columns:** 13
**Column List:** `market_id, market_description, market_hierarchy_level, market_hierarchy_number, market_hierarchy_name, market_hierarchy_column, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### rtd_clean_dim_period
**Rows:** 57 | **Columns:** 16
**Column List:** `period_id, period_short_description, period_long_description, period_end_date, nielsen_calendar, nielsen_periodicity, period_year, period_month, date_key, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### rtd_clean_dim_product
**Rows:** 5,302 | **Columns:** 31
**Column List:** `product_id, rtd_cider, corporation_1, brand, subsegment, subbrands, ru_variant, packaging, item, upc, ru_price_segment, ru_size, quantity, ru_flavor, ru_segment, organic_indicator, rub_packaging, light_or_regular, rtd_cider_excluding_drinks_cocktails, private_label, product_hierarchy_number, product_hierarchy_level, product_hierarchy_level_name, manufacturer, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### rtd_clean_facts
**Rows:** 3,603,320 | **Columns:** 38
**Column List:** `market_id, period_id, product_id, sales_value, sales_in_liters, sales_units, baseline_sales_value, baseline_sales_in_liters, baseline_sales_units, baseline_sales_value_any_promo, baseline_sales_in_liters_any_promo, baseline_sales_units_any_promo, sales_value_any_promo, sales_in_liters_any_promo, sales_units_any_tpr, numeric_distribution, numeric_distribution_reach, weighted_distribution, weighted_distribution_reach, total_weighted_distribution_points_tdp_reach, number_of_items_reach, avg_number_of_stores_selling_reach, universe_number_of_stores, avg_no_of_items_per_store_reach, weighted_distribution_any_promo, weighted_distribution_disp_and_feat, weighted_distribution_disp_wo_feat, weighted_distribution_feat_wo_disp, weighted_distribution_total_feat, weighted_distribution_any_disp, weighted_distribution_any_tpr, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### totalbeer_clean_dim_market
**Rows:** 344 | **Columns:** 13
**Column List:** `market_id, market_description, market_hierarchy_level, market_hierarchy_number, market_hierarchy_name, market_hierarchy_column, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### totalbeer_clean_dim_period
**Rows:** 94 | **Columns:** 16
**Column List:** `period_id, period_short_description, period_long_description, period_end_date, nielsen_calendar, nielsen_periodicity, period_year, period_month, date_key, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

### totalbeer_clean_dim_product
**Rows:** 62,752 | **Columns:** 42
**Column List:** `product_id, category, manufacturer, brand, segment, subsegment, ru_subbrand, ru_variant, packaging_1, item, upc, ru_size, gift_box_or_calendar, beer_mixes, beer_type, size_variants, packaging_2, quantity, price_category, sub_product_class, foreign_beer, christmas_or_easter_beer, organic, alcohol_percentage, special_beer, packaging_limited_size, private_label, controlled_label, product_hierarchy_number, product_hierarchy_level, product_hierarchy_level_name, corporation_ru, rub_manufacturer_total, segment_christmas_easter_beer_ex_cl, beer_type_segment, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, valid_from, valid_to, change_detection_hash`

### totalbeer_clean_facts
**Rows:** 39,320,290 | **Columns:** 43
**Column List:** `market_id, period_id, product_id, sales_value, sales_in_liters, sales_units, sales_value_any_promo, sales_value_any_tpr, sales_in_liters_any_promo, sales_in_liters_any_tpr, sales_units_any_promo, sales_units_any_tpr, baseline_sales_value, baseline_sales_in_liters, baseline_sales_units, baseline_sales_value_any_promo, baseline_sales_in_liters_any_promo, baseline_sales_units_any_promo, numeric_distribution, numeric_distribution_reach, weighted_distribution, weighted_distribution_reach, total_weighted_distribution_points_tdp_reach, number_of_items_reach, avg_number_of_stores_selling_reach, universe_number_of_stores, avg_no_of_items_per_store_reach, weighted_distribution_any_promo, weighted_distribution_disp_feat, weighted_distribution_disp_w_o_feat, weighted_distribution_feat_w_o_disp, weighted_distribution_total_feat, weighted_distribution_any_disp, weighted_distribution_any_tpr, tdp_weighted_distribution_any_promo, tdp_weighted_distribution_any_tpr, valid_from, valid_to, folder_name, last_server_update, pipeline_run_at, pipeline_run_id, change_detection_hash`

---

## Metadata Tables

### metadata_csd_clean_dim_market
**Rows:** 2 | **Columns:** 4
**Column List:** `position, column_name, data_type, comment`

### metadata_csd_clean_dim_period
**Rows:** 4 | **Columns:** 4
**Column List:** `position, column_name, data_type, comment`

### metadata_csd_clean_dim_product
**Rows:** 18 | **Columns:** 4
**Column List:** `position, column_name, data_type, comment`

### metadata_csd_clean_facts
**Rows:** 10 | **Columns:** 4
**Column List:** `position, column_name, data_type, comment`

### metadata_csd_columns
**Rows:** 70 | **Columns:** 7
**Column List:** `table_name, position, column_name, data_type, unit, null_meaning, description`

### metadata_danskvand_columns
**Rows:** 54 | **Columns:** 7
**Column List:** `table_name, position, column_name, data_type, unit, null_meaning, description`

### metadata_energidrikke_columns
**Rows:** 72 | **Columns:** 7
**Column List:** `table_name, position, column_name, data_type, unit, null_meaning, description`

### metadata_rtd_columns
**Rows:** 70 | **Columns:** 7
**Column List:** `table_name, position, column_name, data_type, unit, null_meaning, description`

### metadata_totalbeer_columns
**Rows:** 86 | **Columns:** 7
**Column List:** `table_name, position, column_name, data_type, unit, null_meaning, description`

