---
name: 2026-09-15_BRANCH_A_ch4-table1-sku-columns
description: FINDING - Thread 82's two figures are untraceable. Table 1's SKU columns are hand-typed, no generator emits them, and two of four rows are internally impossible. Recommends deleting both columns rather than regenerating them.
category: workflow
applies-to: [ch4_data_assessment]
triggers: [thread 82, Table 1, SKU counts, 728, 2442]
created: 2026_09_15-00_45
updated: 2026_09_15-00_45
snapshot: 2026-09-15_00-30_eod-final-pass
status: prose ready to paste, awaiting human review
---

# Thread 82 — I traced the two figures. They cannot be reconciled.

Verified at `2b33025`, fetch clean. Snapshot `2026-09-15_00-30_eod-final-pass`
(46,786 words, 29 comments in 23 threads). Zotero re-pulled: **92 items**.

**You asked me to check 728 and 2,442 against the EDA tables. I did, and the
answer is worse than "stale" — but the fix is smaller than regenerating the
row.**

---

# What the columns actually are

My earlier note guessed they might be promo-bearing and non-promo counts. **That
was wrong.** The table header in the current snapshot reads:

> | Category | Periods (max) | Brands (in scope) | Brands retained | **Catalog SKUs** | **In-scope SKUs** | Brand-month rows | In-scope fact rows |

So 728 is *Catalog SKUs* and 2,442 is *In-scope SKUs* for RTD.

---

# Three things I established

### 1 — Everything except the two SKU columns reconciles

| Cell | Value | Artefact |
|---|---|---|
| Periods | 41 | `eda/RTD/tables/step_2_01_shape.md` |
| Brands in scope | 101 | same — "Unique Brands" |
| Brands retained | 62 | `tables/03_pipeline_data_reduction.md`, H=3 row |
| Brand-month rows | 2,509 | `step_2_01_shape.md` — "Total Rows" |

✅ **Four of six figures are correct and current.** The same holds for the other
three category rows.

### 2 — No generator produces the SKU columns

```bash
grep -rln "Catalog SKU\|In-scope SKU\|in_scope_sku\|catalog_sku" --include=*.py .
# (no matches)
```

The only script mentioning SKUs at all is
`01_SRQ1_Model_Training/.../nielsen_data_assessment.py`, which **prints counts to
stdout** (`f"Row count (SKUs) : {len(df)}"`) and writes no table.

⚠ **These two columns were typed by hand into Word.** Nothing computes them, so
nothing will ever correct them. Searching the whole of `05_thesis_results/` for
`7,991` — the CSD in-scope figure — returns only coincidental substrings inside
unrelated decimals.

### 3 — Two of the four rows are internally impossible

| Category | Catalog SKUs | In-scope SKUs |
|---|---|---|
| CSD | 2,130 | **7,991** ⚠ |
| danskvand | 1,071 | 1,913 ⚠ |
| energidrikke | 1,272 | 4,083 ⚠ |
| RTD | **728** | **2,442** ⚠ |

⚠ **In-scope exceeds catalog in all four rows.** A subset cannot be larger than
the set it is drawn from. Either the two columns are transposed, or they are
counting two different things whose names no longer describe them — and with no
generator, there is no way to find out which.

**This is the detail an assessor can catch without leaving the page**, because
the column names make the contradiction self-evident.

---

# The fix

## F1 — Delete both SKU columns from Table 1

### Anchor

**Section 4.1.2 Schema and Structure.** The table immediately below the sentence
ending:

> "...are reported in **Table** **1**, all computed locally under the DVH EXCL. HD scope."

Its last row begins *"RTD | 41 | 101 | 62"*.

### Action

EDIT — remove two columns from the header and from all four body rows.

**Before (header):**
> | Category | Periods (max) | Brands (in scope) | Brands retained | Catalog SKUs | In-scope SKUs | Brand-month rows | In-scope fact rows |

**After (header):**
> | Category | Periods (max) | Brands (in scope) | Brands retained | Brand-month rows | In-scope fact rows |

**After (body):**
> | CSD | 46 | 142 | 95 | 4,209 | 223,240 |
> | danskvand | 41 | 55 | 29 | 1,225 | 27,449 |
> | energidrikke | 43 | 68 | 44 | 1,702 | 55,216 |
> | RTD | 41 | 101 | 62 | 2,509 | 49,976 |

### Also reword the sentence above it

**Before:**
> "Per-category structural counts (periods, brands, products/SKUs, brand-month rows, in-scope fact rows) are reported in **Table 1**, all computed locally under the DVH EXCL. HD scope."

**After:**
> "Per-category structural counts (periods, brands, brand-month rows and in-scope fact rows) are reported in **Table 1**, all computed locally under the DVH EXCL. HD scope."

### Note — why deleting beats regenerating

⚠ **The SKU counts are load-bearing for nothing.** The thesis models at
**brand × month** (DEC-GRAIN). No SRQ, no feature, no result depends on how many
SKUs sat behind a brand. The columns are context, and context that contradicts
itself is worse than absent context.

**Regenerating them would mean writing a new producer, at midnight, for two
numbers no argument uses.** Deleting them costs one edit and removes a visible
inconsistency.

✅ **The remaining four columns all reconcile to artefacts**, so the trimmed table
is fully defensible.

---

# Thread 82's second half

> *"Also this table might be a good candidate to move into the appendix. Or at
> the least the lengthy definitions and description."*

**That is S1–S4 in the deferred list and is not re-decided here.** ⚠ My
recommendation: **keep the trimmed six-column table in the body.** At six columns
and four rows it is now small enough to read in place, and §4.1.2's argument
refers to it directly. The appendix case was strongest when it was eight columns
wide.

→ **Resolve thread 82 as ADDRESSED once F1 is applied.**

---

# Verification

| Claim | Checked against |
|---|---|
| header names the columns "Catalog SKUs" / "In-scope SKUs" | snapshot `2026-09-15_00-30`, `ch4-data-assessment.md` line 33 |
| periods, brands, brand-month rows | `eda/{CSD,Danskvand,Energidrikke,RTD}/tables/step_2_01_shape.md` |
| brands retained | `tables/03_pipeline_data_reduction.md`, H=3 rows |
| no generator emits the SKU columns | repo-wide grep over `*.py`, no matches |
| 7,991 absent from results | grep over `05_thesis_results/`, `*.md`/`*.csv`/`*.json` |

**No new citation.** The edit removes content and adds no claim.
