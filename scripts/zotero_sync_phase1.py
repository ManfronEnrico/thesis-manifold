#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Zotero Sync Phase 1 - Read-Only Library Comparison
===================================================
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Any

from pyzotero import Zotero
from dotenv import load_dotenv


def load_env() -> dict:
    """Load Zotero credentials from .env file."""
    env_path = Path.cwd() / ".env"
    load_dotenv(env_path)
    
    required = ["ZOTERO_USER_ID", "ZOTERO_API_KEY"]
    env_vars = {}
    for key in required:
        val = os.environ.get(key)
        if not val:
            raise ValueError(f"Missing environment variable: {key}")
        env_vars[key] = val
    
    return env_vars


def load_thesis_papers(papers_dir: Path) -> dict:
    """Load thesis paper records from docs/literature/papers/*.md files."""
    papers = {}
    
    if not papers_dir.exists():
        print(f"Warning: papers directory not found: {papers_dir}")
        return papers
    
    for paper_file in papers_dir.glob("*.md"):
        try:
            content = paper_file.read_text(encoding='utf-8')
            if content.startswith("---"):
                lines = content.split("
")
                for line in lines[1:]:
                    if line.startswith("title:"):
                        title = line.replace('title:', '').strip().strip('"')
                        papers[title] = {
                            "file": paper_file.name,
                            "path": str(paper_file),
                        }
                        break
        except Exception as e:
            print(f"Error reading {paper_file.name}: {e}")
    
    return papers


def fetch_zotero_items(zot: Zotero) -> list:
    """Fetch all items from Zotero library."""
    print(f"Fetching items from Zotero...", end="", flush=True)
    items = zot.everything(zot.items(limit=100))
    print(f" OK ({len(items)} items)")
    return items


def get_item_title(item: dict) -> str:
    """Safely extract title from Zotero item."""
    try:
        return item["data"].get("title", None)
    except (KeyError, TypeError):
        return None


def generate_report(zotero_items: list, thesis_papers: dict, output_path: Path) -> None:
    """Generate sync report and write to file."""
    
    # Build Zotero titles map
    zotero_titles = {}
    items_without_title = 0
    
    for item in zotero_items:
        title = get_item_title(item)
        if title:
            zotero_titles[title] = item
        else:
            items_without_title += 1
    
    # Find missing items
    missing_in_thesis = [
        title for title in zotero_titles.keys()
        if title not in thesis_papers
    ]
    
    missing_in_zotero = [
        title for title in thesis_papers.keys()
        if title not in zotero_titles
    ]
    
    # Generate report
    lines = [
        "# Zotero Sync Report - Phase 1",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        f"- **Zotero library items (with title)**: {len(zotero_titles)}",
        f"- **Zotero items (without title)**: {items_without_title}",
        f"- **Thesis papers**: {len(thesis_papers)}",
        f"- **Missing in thesis**: {len(missing_in_thesis)}",
        f"- **Missing in Zotero**: {len(missing_in_zotero)}",
        "",
    ]
    
    if missing_in_thesis:
        lines.extend([
            "## Papers in Zotero but NOT in thesis",
            "",
            "**Candidates for addition to corpus**:",
            "",
        ])
        for title in sorted(missing_in_thesis)[:20]:
            item = zotero_titles[title]
            authors = item["data"].get("creators", [])
            author_str = ", ".join(
                f"{a.get('lastName', '')} {a.get('firstName', '')}"
                for a in authors
            ).strip() or "Unknown"
            year = item["data"].get("year", "?")
            lines.append(f"- **{title}**")
            lines.append(f"  - Authors: {author_str}")
            lines.append(f"  - Year: {year}")
            lines.append(f"  - Key: {item['key']}")
            lines.append("")
        
        if len(missing_in_thesis) > 20:
            lines.append(f"... and {len(missing_in_thesis) - 20} more items")
            lines.append("")
    
    if missing_in_zotero:
        lines.extend([
            "## Papers in thesis but NOT in Zotero",
            "",
            "**Note**: These may be intentionally excluded.",
            "",
        ])
        for title in sorted(missing_in_zotero)[:10]:
            path = thesis_papers[title].get("path", "?")
            lines.append(f"- **{title}**")
            lines.append(f"  - File: {path}")
            lines.append("")
    
    lines.extend([
        "## Next Steps",
        "",
        "1. Review the missing papers list",
        "2. Decide which papers to add to thesis corpus",
        "3. Phase 2 (when ready): Enable bidirectional sync",
        "",
        "---",
        "*Phase 1 is READ-ONLY. No changes made.*",
    ])
    
    report_text = "
".join(lines)
    output_path.write_bytes(report_text.encode('utf-8'))
    print(f"Report written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Zotero Sync Phase 1 - Read-only library comparison"
    )
    parser.add_argument(
        "--output",
        default="docs/zotero_sync_report.md",
        help="Output report path",
    )
    
    args = parser.parse_args()
    
    try:
        print("Loading Zotero credentials...", end="", flush=True)
        env = load_env()
        print(" OK")
        
        print("Connecting to Zotero...", end="", flush=True)
        zot = Zotero(
            library_id=env["ZOTERO_USER_ID"],
            library_type="user",
            api_key=env["ZOTERO_API_KEY"],
        )
        print(" OK")
        
        papers_dir = Path("docs/literature/papers")
        print(f"Loading thesis papers...", end="", flush=True)
        thesis_papers = load_thesis_papers(papers_dir)
        print(f" OK ({len(thesis_papers)} papers)")
        
        zotero_items = fetch_zotero_items(zot)
        
        print(f"Generating report...", end="", flush=True)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        generate_report(zotero_items, thesis_papers, output_path)
        print(" OK")
        
        print("
Sync Phase 1 complete!")
        print(f"Review: {output_path}")
        
    except Exception as e:
        print(f"
ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
