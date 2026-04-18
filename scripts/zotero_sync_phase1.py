#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Zotero Sync Phase 1 - Read-Only Library Comparison
===================================================
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

from zotero_client import get_citations


def load_thesis_papers(papers_dir: Path) -> dict:
    papers = {}
    if not papers_dir.exists():
        print(f"Warning: papers directory not found: {papers_dir}")
        return papers
    for paper_file in papers_dir.glob("*.md"):
        try:
            content = paper_file.read_text(encoding="utf-8")
            if content.startswith("---"):
                for line in content.split("\n")[1:]:
                    if line.startswith("title:"):
                        title = line.replace("title:", "").strip().strip('"')
                        papers[title] = {"file": paper_file.name, "path": str(paper_file)}
                        break
        except Exception as e:
            print(f"Error reading {paper_file.name}: {e}")
    return papers


def generate_report(citations: list, thesis_papers: dict, output_path: Path) -> None:
    zotero_titles = {c["title"]: c for c in citations if c.get("title")}

    missing_in_thesis = [t for t in zotero_titles if t not in thesis_papers]
    missing_in_zotero = [t for t in thesis_papers if t not in zotero_titles]

    lines = [
        "# Zotero Sync Report - Phase 1",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        f"- **Zotero citation items**: {len(zotero_titles)}",
        f"- **Thesis papers**: {len(thesis_papers)}",
        f"- **In Zotero but not thesis**: {len(missing_in_thesis)}",
        f"- **In thesis but not Zotero**: {len(missing_in_zotero)}",
        "",
    ]

    if missing_in_thesis:
        lines += ["## Papers in Zotero but NOT in thesis", "", "**Candidates for addition to corpus**:", ""]
        for title in sorted(missing_in_thesis)[:20]:
            c = zotero_titles[title]
            lines += [
                f"- **{title}**",
                f"  - Authors: {c.get('authors') or 'Unknown'}",
                f"  - Year: {c.get('year') or '?'}",
                f"  - Type: {c.get('itemType')}",
                f"  - Key: {c.get('key')}",
                "",
            ]
        if len(missing_in_thesis) > 20:
            lines.append(f"... and {len(missing_in_thesis) - 20} more items")
            lines.append("")

    if missing_in_zotero:
        lines += ["## Papers in thesis but NOT in Zotero", "", "**Note**: These may be intentionally excluded.", ""]
        for title in sorted(missing_in_zotero)[:10]:
            lines += [f"- **{title}**", f"  - File: {thesis_papers[title].get('path', '?')}", ""]

    lines += ["## Next Steps", "", "1. Review the missing papers list", "2. Phase 2 (when ready): Enable bidirectional sync", "", "---", "*Phase 1 is READ-ONLY. No changes made.*"]

    output_path.write_bytes("\n".join(lines).encode("utf-8"))
    print(f"Report written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Zotero Sync Phase 1 - Read-only library comparison")
    parser.add_argument("--output", default="docs/zotero_sync_report.md", help="Output report path")
    args = parser.parse_args()

    try:
        papers_dir = Path("docs/literature/papers")
        print("Loading thesis papers...", end="", flush=True)
        thesis_papers = load_thesis_papers(papers_dir)
        print(f" OK ({len(thesis_papers)} papers)")

        print("Fetching citations from Zotero...", end="", flush=True)
        citations = get_citations()
        print(f" OK ({len(citations)} citation items)")

        print("Generating report...", end="", flush=True)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        generate_report(citations, thesis_papers, output_path)
        print(" OK")

        print("\nSync Phase 1 complete!")
        print(f"Review: {output_path}")

    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
