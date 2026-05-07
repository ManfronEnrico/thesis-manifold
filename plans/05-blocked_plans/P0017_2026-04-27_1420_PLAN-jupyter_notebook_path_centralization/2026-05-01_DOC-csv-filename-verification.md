# CSV Filename Verification — All Scripts Correct

**Date**: 2026-05-01  
**Task**: Verify all preprocessing scripts load category-specific CSV files  
**Status**: ✅ VERIFIED

---

## Verification Summary

All 5 preprocessing scripts correctly reference **category-specific CSV filenames**.

### Facts Files (Step 1: load_raw)
| Script | Facts File |
|--------|-----------|
| `preprocessing_csd.py` | `csd_clean_facts_v.csv` ✅ |
| `preprocessing_danskvand.py` | `danskvand_clean_facts_v.csv` ✅ |
| `preprocessing_energidrikke.py` | `energidrikke_clean_facts_v.csv` ✅ |
| `preprocessing_rtd.py` | `rtd_clean_facts_v.csv` ✅ |
| `preprocessing_totalbeer.py` | `totalbeer_clean_facts_v.csv` ✅ |

### Dimension Files (Step 1: load_raw)
| Script | Product Dim | Period Dim | Market Dim |
|--------|------------|-----------|-----------|
| `preprocessing_csd.py` | `csd_clean_dim_product_v.csv` | `csd_clean_dim_period_v.csv` | `csd_clean_dim_market_v.csv` |
| `preprocessing_danskvand.py` | `danskvand_clean_dim_product_v.csv` | `danskvand_clean_dim_period_v.csv` | `danskvand_clean_dim_market_v.csv` |
| `preprocessing_energidrikke.py` | `energidrikke_clean_dim_product_v.csv` | `energidrikke_clean_dim_period_v.csv` | `energidrikke_clean_dim_market_v.csv` |
| `preprocessing_rtd.py` | `rtd_clean_dim_product_v.csv` | `rtd_clean_dim_period_v.csv` | `rtd_clean_dim_market_v.csv` |
| `preprocessing_totalbeer.py` | `totalbeer_clean_dim_product_v.csv` | `totalbeer_clean_dim_period_v.csv` | `totalbeer_clean_dim_market_v.csv` |

### Validation Function (validate_input_data)
All scripts validate for the **correct 4 category-specific CSV files** before processing:

**CSD validates**:
```python
required_files = [
    "csd_clean_facts_v.csv",
    "csd_clean_dim_product_v.csv",
    "csd_clean_dim_period_v.csv",
    "csd_clean_dim_market_v.csv",
]
```

**Danskvand validates**:
```python
required_files = [
    "danskvand_clean_facts_v.csv",
    "danskvand_clean_dim_product_v.csv",
    "danskvand_clean_dim_period_v.csv",
    "danskvand_clean_dim_market_v.csv",
]
```

(Same pattern for energidrikke, rtd, totalbeer)

---

## Verification Method

Used `grep` to search all 5 scripts for:
1. `read_csv.*clean_facts_v` — verified facts files are category-specific
2. `read_csv.*clean_dim_(product|market|period)` — verified all dimension files are category-specific
3. `required_files = [` — verified validation lists are correct

---

## Conclusion

✅ **All scripts correctly reference category-specific CSV filenames**

Each script will:
1. Look for `{category}_clean_facts_v.csv`
2. Look for `{category}_clean_dim_*.csv` (product, period, market)
3. Validate all 4 files exist before processing
4. Print helpful error message if any are missing

Ready to test.
