#!/usr/bin/env python3
"""
Build the cross-category Nielsen feature inventory.

Joins every column in every category's view tables to Nielsen's own metadata
descriptions, adds a real non-blank example value, and reports:

  1. whether the forecast target exists under a different name in any category
  2. which columns are the same measure spelled differently across categories

Outputs:
  _shared_modules/nielsen_feature_inventory.csv     (machine-readable)
  user-docs/reference/nielsen-feature-inventory.md  (reviewable)

Run:  python build_feature_inventory.py

WHY THIS IS A SCRIPT, NOT A ONE-OFF
-----------------------------------
Column availability drives what the pipeline can build, and it changes whenever
Nielsen re-delivers. Re-running this after a data refresh shows what appeared or
vanished. It reads only; it writes no pipeline data.
"""

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

from PATHS import get_category_metadata_dir, get_category_views_dir
from pipeline_config import CATEGORIES, TARGET_COL

TABLES = ("facts", "dim_product", "dim_period", "dim_market")

# Spelling variants Nielsen uses for the same concept. Normalising these is what
# surfaces alias candidates; it is NOT applied to the data.
SPELLING_NORMALISERS = ((r"_w_o_", "_wo_"), (r"_and_", "_"))


def normalise_name(column: str) -> str:
	out = column.lower()
	for pat, rep in SPELLING_NORMALISERS:
		out = re.sub(pat, rep, out)
	return re.sub(r"_+", "_", out)


def load_metadata() -> pd.DataFrame:
	frames = []
	for cat in CATEGORIES:
		f = get_category_metadata_dir(cat) / f"metadata_{cat.lower()}_columns.parquet"
		if not f.exists():
			continue
		m = pd.read_parquet(f)
		m["category"] = cat
		frames.append(m)
	meta = pd.concat(frames, ignore_index=True)
	meta["column_name"] = meta["column_name"].str.strip()
	return meta


def load_examples() -> tuple[dict, dict]:
	"""Return {(category, column): example_value} and {(category, column): dtype}."""
	examples, dtypes = {}, {}
	for cat in CATEGORIES:
		vd = get_category_views_dir(cat)
		for tbl in TABLES:
			f = vd / f"{cat.lower()}_clean_{tbl}_v.parquet"
			if not f.exists():
				continue
			df = pd.read_parquet(f)
			for col in df.columns:
				s = df[col].dropna()
				# Prefer a genuinely informative example: non-blank, non-zero.
				if s.dtype == object:
					s = s[s.astype(str).str.strip().ne("")]
				elif len(s[s != 0]):
					s = s[s != 0]
				value = s.iloc[0] if len(s) else None
				if isinstance(value, float):
					value = round(value, 4)
				examples[(cat, col)] = value
				dtypes[(cat, col)] = str(df[col].dtype)
	return examples, dtypes


def build_inventory() -> pd.DataFrame:
	meta = load_metadata()
	examples, dtypes = load_examples()

	def first_meta(col: str, field: str) -> str:
		rows = meta[meta["column_name"] == col]
		if len(rows) and rows[field].notna().any():
			return rows[field].dropna().iloc[0]
		return ""

	rows = []
	for col in sorted({c for _, c in examples}):
		present = [cat for cat in CATEGORIES if (cat, col) in examples]
		table = first_meta(col, "table_name")
		rows.append({
			"column": col,
			"table": table.split("clean_")[-1] if table else "",
			**{cat: ("Y" if cat in present else "") for cat in CATEGORIES},
			"n_cats": len(present),
			"dtype": next((dtypes[(c, col)] for c in present), ""),
			"unit": first_meta(col, "unit"),
			"example": next(
				(examples[(c, col)] for c in present if examples[(c, col)] is not None), None
			),
			"null_meaning": first_meta(col, "null_meaning"),
			"description": first_meta(col, "description"),
		})
	return pd.DataFrame(rows).sort_values(["table", "column"])


def find_alias_groups(inv: pd.DataFrame) -> list[dict]:
	"""Columns that normalise to the same name but are not universally present.

	Reports candidates only. Two columns can share every token and still mean
	OPPOSITE things -- `disp_w_o_feat` (display without feature) vs
	`feat_w_o_disp` (feature without display) -- so a match here is a prompt to
	read the descriptions, never grounds to merge automatically.
	"""
	partial = inv[inv["n_cats"] < len(CATEGORIES)].copy()
	partial["norm"] = partial["column"].map(normalise_name)

	groups = []
	for norm, grp in partial.groupby("norm"):
		cols = sorted(set(grp["column"]))
		if len(cols) < 2:
			continue
		descs = {
			" ".join(str(inv.loc[inv["column"] == c, "description"].iloc[0]).split())
			for c in cols
		}
		groups.append({
			"normalised": norm,
			"columns": cols,
			"descriptions_identical": len(descs) == 1,
		})
	return groups


def check_target_aliases(inv: pd.DataFrame) -> dict:
	"""Is the forecast target present everywhere, or aliased somewhere?"""
	pattern = r"sales|volume|units|qty|quantity|turnover|revenue|value|liter|litre|amount"
	candidates = inv[
		inv["column"].str.contains(pattern, case=False, regex=True)
		| inv["description"].str.contains(pattern, case=False, na=False, regex=True)
	]
	target_row = inv[inv["column"] == TARGET_COL]
	return {
		"target": TARGET_COL,
		"present_in_all": bool(len(target_row) and target_row["n_cats"].iloc[0] == len(CATEGORIES)),
		"candidate_count": len(candidates),
		"universal_measures": sorted(
			candidates.loc[candidates["n_cats"] == len(CATEGORIES), "column"]
		),
	}


def main() -> int:
	inv = build_inventory()
	out_csv = Path(__file__).parent / "nielsen_feature_inventory.csv"
	inv.to_csv(out_csv, index=False, encoding="utf-8")

	target = check_target_aliases(inv)
	print("=" * 78)
	print("TARGET AVAILABILITY")
	print("=" * 78)
	print(f"  target column        : {target['target']}")
	print(f"  present in all {len(CATEGORIES)}     : {target['present_in_all']}")
	print(f"  sales-like candidates: {target['candidate_count']}")
	print(f"  universal measures   : {', '.join(target['universal_measures'])}")

	print()
	print("=" * 78)
	print("ALIAS CANDIDATES (same measure, different spelling)")
	print("=" * 78)
	for g in find_alias_groups(inv):
		flag = "descriptions IDENTICAL" if g["descriptions_identical"] else "descriptions DIFFER -- read them"
		print(f"  {g['normalised']}  [{flag}]")
		for c in g["columns"]:
			marks = "".join(
				"Y" if inv.loc[inv["column"] == c, cat].iloc[0] == "Y" else "."
				for cat in CATEGORIES
			)
			print(f"      {c:<46} {marks}")

	print()
	print(f"Wrote {out_csv}  ({len(inv)} columns)")
	print("Coverage by category count:")
	print(inv.groupby("n_cats").size().rename("columns").to_string())
	return 0


if __name__ == "__main__":
	sys.exit(main())
