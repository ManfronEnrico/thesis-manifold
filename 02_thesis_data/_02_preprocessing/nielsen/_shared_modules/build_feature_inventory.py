#!/usr/bin/env python3
"""
Build the Nielsen feature inventory: one table per category, plus a
cross-category comparison.

For every column in every view table of every category, joins:
  - the ACTUAL column present in the parquet data (the source of truth for
    what exists)
  - Nielsen's own metadata, read from the raw JSONL at
    THESIS_DATA_RAW_NIELSEN_JSONL_DIR/{cat}/metadata/, surfaced as `m_data_type`
    and `m_description`
  - descriptive statistics computed from the data itself
  - a real non-blank example value

Numeric columns get min / max / mean / median / mode / std / nulls / zeros /
negatives. Text columns get the text equivalents: distinct count, mode and its
frequency, shortest and longest value, null and blank counts.

Outputs:
  user-docs/reference/nielsen-feature-inventory.md   (one table per category)
  _shared_modules/nielsen_feature_inventory.csv      (machine-readable, long form)

Run:  python build_feature_inventory.py

WHY THE JSONL AND NOT THE PARQUET METADATA
------------------------------------------
Both exist and were verified identical (266 field-sets, 0 differences,
2026-08-12). The JSONL under _00_raw/ is the delivered artifact; the parquet is
a Stage-1 conversion of it. Reading the source directly means this inventory
cannot silently inherit a conversion defect.

WHY THIS IS A SCRIPT, NOT A ONE-OFF
-----------------------------------
Column availability drives what the pipeline can build, and it changes whenever
Nielsen re-delivers. Re-running after a refresh shows what appeared or vanished.
Reads only; writes no pipeline data.
"""

import json
import re
import sys
from pathlib import Path

import pandas as pd

current = Path.cwd()
while current != current.parent:
	if (current / "CLAUDE.md").exists():
		ROOT_DIR = current
		break
	current = current.parent
else:
	raise FileNotFoundError("Could not find project root (CLAUDE.md)")

sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "02_thesis_data" / "_02_preprocessing" / "nielsen" / "_shared_modules"))

from PATHS import (
	THESIS_DATA_RAW_NIELSEN_JSONL_DIR,
	get_category_views_dir,
)
from pipeline_config import CATEGORIES, TARGET_COL

TABLES = ("facts", "dim_product", "dim_period", "dim_market")

# Spelling variants Nielsen uses for the same concept. Used ONLY to surface
# alias candidates for human review -- never applied to the data.
SPELLING_NORMALISERS = ((r"_w_o_", "_wo_"), (r"_and_", "_"))

MD_OUT = ROOT_DIR / "user-docs" / "reference" / "nielsen-feature-inventory.md"
CSV_OUT = Path(__file__).parent / "nielsen_feature_inventory.csv"


# ============================================================================
# METADATA (from the raw JSONL -- the delivered source)
# ============================================================================

def load_metadata(category: str) -> dict[str, dict]:
	"""Read metadata_{cat}_columns.jsonl -> {column_name: record}.

	Keyed on column name alone rather than (table, column): a few columns (the
	foreign keys) appear in several tables with the same meaning, and Nielsen
	documents them once per table with identical text.
	"""
	f = (
		THESIS_DATA_RAW_NIELSEN_JSONL_DIR
		/ category
		/ "metadata"
		/ f"metadata_{category.lower()}_columns.jsonl"
	)
	if not f.exists():
		raise FileNotFoundError(f"Metadata JSONL missing for {category}: {f}")

	out: dict[str, dict] = {}
	for line in f.read_text(encoding="utf-8").splitlines():
		line = line.strip()
		if not line:
			continue
		rec = json.loads(line)
		out.setdefault(str(rec["column_name"]).strip(), rec)
	return out


# ============================================================================
# STATISTICS
# ============================================================================

def _fmt(value, digits: int = 4):
	"""Compact, stable rendering for a stat cell."""
	if value is None or (isinstance(value, float) and pd.isna(value)):
		return ""
	if isinstance(value, float):
		if value == int(value) and abs(value) < 1e15:
			return str(int(value))
		return f"{value:.{digits}g}"
	return str(value)


def example_value(series: pd.Series):
	"""A real, informative example: non-null, non-blank, and non-zero if possible."""
	s = series.dropna()
	if s.dtype == object:
		s = s[s.astype(str).str.strip().ne("")]
	elif len(s[s != 0]):
		s = s[s != 0]
	if not len(s):
		return None
	value = s.iloc[0]
	return round(value, 4) if isinstance(value, float) else value


def numeric_stats(s: pd.Series, n_rows: int) -> dict:
	v = s.dropna()
	mode = v.mode()
	return {
		"min": _fmt(v.min()) if len(v) else "",
		"max": _fmt(v.max()) if len(v) else "",
		"mean": _fmt(v.mean()) if len(v) else "",
		"median": _fmt(v.median()) if len(v) else "",
		"mode": _fmt(mode.iloc[0]) if len(mode) else "",
		"std": _fmt(v.std()) if len(v) else "",
		"distinct": f"{v.nunique():,}",
		"nulls": f"{n_rows - len(v):,}",
		"null_pct": f"{100 * (n_rows - len(v)) / n_rows:.1f}" if n_rows else "",
		"zeros": f"{int((v == 0).sum()):,}" if len(v) else "",
		"negatives": f"{int((v < 0).sum()):,}" if len(v) else "",
	}


def text_stats(s: pd.Series, n_rows: int) -> dict:
	"""Text equivalents of the numeric stats.

	min/max become shortest/longest by character length, and mean/median become
	the mean/median length -- the closest meaningful analogues for strings.
	"""
	v = s.dropna().astype(str)
	v = v[v.str.strip().ne("")]
	lengths = v.str.len()
	mode = v.mode()
	mode_val = mode.iloc[0] if len(mode) else ""
	mode_freq = int((v == mode_val).sum()) if len(mode) else 0
	return {
		"min": v.loc[lengths.idxmin()] if len(v) else "",
		"max": v.loc[lengths.idxmax()] if len(v) else "",
		"mean": f"{lengths.mean():.1f} chars" if len(v) else "",
		"median": f"{lengths.median():.0f} chars" if len(v) else "",
		"mode": mode_val,
		"std": f"{mode_freq:,}x" if len(v) else "",
		"distinct": f"{v.nunique():,}",
		"nulls": f"{n_rows - len(s.dropna()):,}",
		"null_pct": f"{100 * (n_rows - len(s.dropna())) / n_rows:.1f}" if n_rows else "",
		"zeros": "",
		"negatives": "",
	}


# ============================================================================
# INVENTORY
# ============================================================================

def build_rows() -> pd.DataFrame:
	rows = []
	for category in CATEGORIES:
		meta = load_metadata(category)
		views = get_category_views_dir(category)
		for table in TABLES:
			f = views / f"{category.lower()}_clean_{table}_v.parquet"
			if not f.exists():
				continue
			df = pd.read_parquet(f)
			n_rows = len(df)
			for col in df.columns:
				s = df[col]
				all_null = bool(s.isna().all())
				# An all-null column has no dtype pandas can infer, so it lands
				# as float64 regardless of what it holds. Trust the metadata for
				# `kind` in that case, otherwise the report claims a documented
				# string column is numeric.
				if all_null:
					is_num = str(meta.get(col, {}).get("data_type", "")).lower() in {
						"double", "int", "float", "decimal", "bigint"
					}
				else:
					is_num = pd.api.types.is_numeric_dtype(s)
				stats = numeric_stats(s, n_rows) if is_num and not all_null else text_stats(s, n_rows)
				md = meta.get(col, {})
				rows.append({
					"category": category,
					"table": table,
					"column": col,
					"kind": "numeric" if is_num else "text",
					"dtype": str(s.dtype),
					"m_data_type": md.get("data_type", ""),
					"m_unit": md.get("unit", ""),
					"m_null_meaning": md.get("null_meaning", ""),
					"m_description": md.get("description", ""),
					"has_metadata": bool(md),
					"all_null": all_null,
					# Does the stored dtype contradict the documented type? IDs
					# stored as int64 while documented `string` are the common
					# case -- harmless for joins, but it means a leading zero
					# would already have been lost at conversion time.
					"dtype_mismatch": bool(
						md
						and not all_null
						and (
							pd.api.types.is_numeric_dtype(s)
							!= (str(md.get("data_type", "")).lower() in {
								"double", "int", "float", "decimal", "bigint"
							})
						)
					),
					"n_rows": n_rows,
					"example": example_value(s),
					**stats,
				})
	return pd.DataFrame(rows)


def normalise_name(column: str) -> str:
	out = column.lower()
	for pat, rep in SPELLING_NORMALISERS:
		out = re.sub(pat, rep, out)
	return re.sub(r"_+", "_", out)


def find_alias_groups(inv: pd.DataFrame) -> list[dict]:
	"""Columns normalising to one name but not present in every category.

	Candidates ONLY. Two columns can share every token and mean opposite things
	-- `disp_w_o_feat` (display without feature) vs `feat_w_o_disp` (feature
	without display) -- so a match here is a prompt to read the descriptions,
	never grounds to merge automatically.
	"""
	cov = inv.groupby("column")["category"].nunique()
	partial = [c for c, n in cov.items() if n < len(CATEGORIES)]
	desc = inv.drop_duplicates("column").set_index("column")["m_description"].to_dict()

	buckets: dict[str, list[str]] = {}
	for col in partial:
		buckets.setdefault(normalise_name(col), []).append(col)

	groups = []
	for norm, cols in sorted(buckets.items()):
		if len(cols) < 2:
			continue
		texts = {" ".join(str(desc.get(c, "")).split()) for c in cols}
		groups.append({
			"normalised": norm,
			"columns": sorted(cols),
			"descriptions_identical": len(texts) == 1,
			"owners": {c: sorted(inv.loc[inv["column"] == c, "category"].unique()) for c in cols},
		})
	return groups


# ============================================================================
# MARKDOWN
# ============================================================================

def esc(text) -> str:
	if text is None or (isinstance(text, float) and pd.isna(text)):
		return ""
	return str(text).replace("|", "\\|").replace("\n", " ").strip()


def truncate(text, limit: int) -> str:
	t = esc(text)
	return t if len(t) <= limit else t[: limit - 1] + "\u2026"


def render_markdown(inv: pd.DataFrame, groups: list[dict]) -> str:
	L: list[str] = []
	A = L.append

	A("# Nielsen Feature Inventory")
	A("")
	A("> Generated by `_shared_modules/build_feature_inventory.py`. Do not edit by hand.")
	A("> Re-run after any Nielsen re-delivery to see what appeared or vanished.")
	A("")
	A("Every column in every view table, per category, joined to Nielsen's own")
	A("metadata (read from the raw JSONL under `_00_raw/.../metadata/`) and to")
	A("statistics computed from the data itself.")
	A("")
	A("**Column meanings**")
	A("")
	A("| Field | Meaning |")
	A("|---|---|")
	A("| `m_data_type`, `m_description` | From Nielsen's metadata JSONL (`m_` = metadata-sourced) |")
	A("| `dtype` | The actual pandas dtype in the parquet |")
	A("| min / max | Numeric: smallest and largest. Text: shortest and longest value |")
	A("| mean / median | Numeric: as usual. Text: mean and median character length |")
	A("| mode | Most frequent value; for text, `freq` gives its count |")
	A("| nulls | Count and percentage of missing values |")
	A("| neg | Count of negative values (numeric only) |")
	A("| example | A real non-null, non-blank, non-zero value from the data |")
	A("")

	# ---- summary
	A("## Summary")
	A("")
	A("| Category | Columns | Facts | Product | Period | Market | Fact rows |")
	A("|---|---|---|---|---|---|---|")
	for cat in CATEGORIES:
		sub = inv[inv["category"] == cat]
		counts = sub["table"].value_counts()
		fact_rows = sub.loc[sub["table"] == "facts", "n_rows"]
		A(
			f"| {cat} | {len(sub)} | {counts.get('facts', 0)} | "
			f"{counts.get('dim_product', 0)} | {counts.get('dim_period', 0)} | "
			f"{counts.get('dim_market', 0)} | {int(fact_rows.iloc[0]):,} |"
			if len(fact_rows) else
			f"| {cat} | {len(sub)} | {counts.get('facts', 0)} | "
			f"{counts.get('dim_product', 0)} | {counts.get('dim_period', 0)} | "
			f"{counts.get('dim_market', 0)} | — |"
		)
	A("")

	# ---- target availability
	tgt = inv[inv["column"] == TARGET_COL]
	A(f"### Forecast target (`{TARGET_COL}`)")
	A("")
	A(f"Present in **{tgt['category'].nunique()} of {len(CATEGORIES)}** categories.")
	A("")
	A("| Category | min | max | mean | median | nulls | neg | example |")
	A("|---|---|---|---|---|---|---|---|")
	for _, r in tgt.sort_values("category").iterrows():
		A(
			f"| {r['category']} | {r['min']} | {r['max']} | {r['mean']} | "
			f"{r['median']} | {r['nulls']} ({r['null_pct']}%) | {r['negatives']} | {_fmt(r['example'])} |"
		)
	A("")

	# ---- alias candidates
	A("### Cross-category alias candidates")
	A("")
	A("Columns whose names normalise to the same string but which are not present")
	A("in every category. **Candidates for review, not merged.**")
	A("")
	A("> **Warning:** `…_disp_w_o_feat` and `…_feat_w_o_disp` contain the same tokens")
	A("> but mean opposite things (display-without-feature vs feature-without-display).")
	A("> Never match aliases on tokens alone — read `m_description`.")
	A("")
	if groups:
		A("| Normalised | Columns | Present in | Descriptions identical |")
		A("|---|---|---|---|")
		for g in groups:
			cols = "<br>".join(f"`{c}`" for c in g["columns"])
			owners = "<br>".join(", ".join(g["owners"][c]) for c in g["columns"])
			A(f"| `{g['normalised']}` | {cols} | {owners} | {'yes' if g['descriptions_identical'] else '**no — read them**'} |")
	else:
		A("_None found._")
	A("")

	# ---- coverage matrix
	A("### Column coverage across categories")
	A("")
	pivot = (
		inv.assign(present="Y")
		.pivot_table(index="column", columns="category", values="present", aggfunc="first")
		.reindex(columns=list(CATEGORIES))
		.fillna("·")
	)
	pivot["n"] = (pivot == "Y").sum(axis=1)
	A("| Column | " + " | ".join(CATEGORIES) + " | n |")
	A("|---" * (len(CATEGORIES) + 2) + "|")
	for col, r in pivot.sort_values(["n", "column"], ascending=[False, True]).iterrows():
		A(f"| `{col}` | " + " | ".join(str(r[c]) for c in CATEGORIES) + f" | {r['n']} |")
	A("")

	# ---- per-category tables
	for cat in CATEGORIES:
		A(f"## {cat}")
		A("")
		sub = inv[inv["category"] == cat]
		for table in TABLES:
			part = sub[sub["table"] == table]
			if part.empty:
				continue
			n_rows = int(part["n_rows"].iloc[0])
			A(f"### {cat} — `{cat.lower()}_clean_{table}_v` ({len(part)} columns, {n_rows:,} rows)")
			A("")
			A("| Column | kind | m_data_type | unit | min | max | mean | median | mode | distinct | nulls | neg | example | m_description |")
			A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
			for _, r in part.sort_values("column").iterrows():
				A(
					f"| `{r['column']}` | {r['kind']} | {esc(r['m_data_type'])} | {esc(r['m_unit'])} | "
					f"{truncate(r['min'], 22)} | {truncate(r['max'], 22)} | {esc(r['mean'])} | "
					f"{esc(r['median'])} | {truncate(r['mode'], 22)} | {r['distinct']} | "
					f"{r['nulls']} ({r['null_pct']}%) | {r['negatives']} | "
					f"{truncate(_fmt(r['example']), 20)} | {truncate(r['m_description'], 220)} |"
				)
			A("")

	# ---- data-quality flags
	mismatch = inv[inv["dtype_mismatch"]].drop_duplicates(["category", "table", "column"])
	empty = inv[inv["all_null"]].drop_duplicates(["category", "table", "column"])

	if len(mismatch) or len(empty):
		A("## Data-quality flags")
		A("")

	if len(mismatch):
		A("### Stored dtype contradicts the documented type")
		A("")
		A("Mostly foreign keys documented as `string` but stored as integers. Harmless")
		A("for joining (both sides converted consistently), but it means a leading zero")
		A("would already have been lost during Stage-1 conversion.")
		A("")
		A("| Category | Table | Column | m_data_type | stored dtype |")
		A("|---|---|---|---|---|")
		for _, r in mismatch.sort_values(["category", "table", "column"]).iterrows():
			A(f"| {r['category']} | {r['table']} | `{r['column']}` | {esc(r['m_data_type'])} | `{r['dtype']}` |")
		A("")

	if len(empty):
		A("### Columns that are 100% NULL")
		A("")
		A("Documented by Nielsen but never populated. Several carry an explicit")
		A("`null_meaning` acknowledging this as a known upstream issue.")
		A("")
		A("| Category | Table | Column | m_null_meaning |")
		A("|---|---|---|---|")
		for _, r in empty.sort_values(["category", "table", "column"]).iterrows():
			A(f"| {r['category']} | {r['table']} | `{r['column']}` | {truncate(r['m_null_meaning'], 90)} |")
		A("")

	# ---- gaps
	missing = inv[~inv["has_metadata"]]
	if len(missing):
		A("## Columns with no metadata entry")
		A("")
		A("Present in the data but absent from the metadata JSONL.")
		A("")
		A("| Category | Table | Column | example |")
		A("|---|---|---|---|")
		for _, r in missing.sort_values(["category", "table", "column"]).iterrows():
			A(f"| {r['category']} | {r['table']} | `{r['column']}` | {truncate(_fmt(r['example']), 24)} |")
		A("")

	return "\n".join(L) + "\n"


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
	inv = build_rows()
	groups = find_alias_groups(inv)

	CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
	inv.to_csv(CSV_OUT, index=False, encoding="utf-8")

	MD_OUT.parent.mkdir(parents=True, exist_ok=True)
	MD_OUT.write_text(render_markdown(inv, groups), encoding="utf-8", newline="\n")

	print("=" * 78)
	print("FEATURE INVENTORY")
	print("=" * 78)
	for cat in CATEGORIES:
		sub = inv[inv["category"] == cat]
		print(f"  {cat:<14} {len(sub):>3} columns   "
			  f"{(sub['kind'] == 'numeric').sum():>2} numeric  "
			  f"{(sub['kind'] == 'text').sum():>2} text  "
			  f"{(~sub['has_metadata']).sum():>2} without metadata")

	tgt = inv[inv["column"] == TARGET_COL]
	print()
	print(f"  target {TARGET_COL!r}: present in {tgt['category'].nunique()}/{len(CATEGORIES)} "
		  f"({', '.join(sorted(tgt['category']))})")

	print()
	print(f"  alias candidates: {len(groups)}")
	for g in groups:
		flag = "identical" if g["descriptions_identical"] else "DIFFER"
		print(f"    {g['normalised']}  [{flag}]")
		for c in g["columns"]:
			print(f"        {c:<46} {', '.join(g['owners'][c])}")

	print()
	print(f"  Wrote {MD_OUT}")
	print(f"  Wrote {CSV_OUT}")
	return 0


if __name__ == "__main__":
	sys.exit(main())
