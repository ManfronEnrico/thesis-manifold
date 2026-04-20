#!/usr/bin/env python3
"""
Match Google Drive filenames to Zotero citation keys.

Pattern:
  GDrive: Author_et_al-Year-Title_with_underscores.pdf
  Citation Key: firstname_firstword_year

Example:
  GDrive: Avramova_et_al-2025-Overview_of_Existing_Multi_Criteria_Decision_Making_MCDM_Methods_Used_in_Industrial_Environments.pdf
  Citation Key: avramova_overview_2025
  Result: Confidence 1.00 (perfect match)

Usage:
  from scripts.gdrive_citation_matcher import match_gdrive_to_citation_key
  confidence, reason = match_gdrive_to_citation_key(gdrive_filename, citation_key)
"""
from typing import Tuple
from difflib import SequenceMatcher


def extract_gdrive_components(filename: str) -> Tuple[str, str, str]:
    """
    Extract author, year, title from Google Drive filename.

    Format: Author_et_al-Year-Title_with_underscores.pdf

    Args:
        filename: Google Drive filename

    Returns:
        Tuple of (first_author_lowercase, year, first_title_word_lowercase)
        or (None, None, None) if parsing fails
    """
    # Remove .pdf extension
    name = filename.replace('.pdf', '').replace('.PDF', '')

    # Split by hyphen: Author-Year-Title
    parts = name.split('-', 2)
    if len(parts) < 3:
        return None, None, None

    author_part = parts[0]  # e.g., "Avramova_et_al"
    year = parts[1]  # e.g., "2025"
    title_part = parts[2]  # e.g., "Overview_of_Existing_Multi_Criteria_..."

    # Extract first author (before first underscore)
    first_author = author_part.split('_')[0].lower()  # "avramova"

    # Extract first word of title (before first underscore)
    first_title_word = title_part.split('_')[0].lower()  # "overview"

    return first_author, year, first_title_word




def fuzzy_match_gdrive_to_zotero(gdrive_filename: str, zotero_item: dict) -> Tuple[float, str]:
    """Fuzzy match GDrive filename to Zotero item using string similarity.

    Used as fallback when exact matching fails. Compares title and author components.

    Args:
        gdrive_filename: Google Drive PDF filename
        zotero_item: Zotero item dict with title, creators, date fields

    Returns:
        Tuple of (confidence_score 0.5-0.9, reason)
    """
    try:
        # Extract components from GDrive filename
        gdrive_author, gdrive_year, gdrive_title_word = extract_gdrive_components(gdrive_filename)

        if not all([gdrive_author, gdrive_year, gdrive_title_word]):
            return 0.0, "Could not parse GDrive filename"

        # Extract Zotero components
        creators = zotero_item.get('creators', [])
        title = zotero_item.get('title', '')
        date_str = zotero_item.get('date', '')
        year = date_str[:4] if date_str else 'unknown'

        # Get first author from Zotero
        if creators and len(creators) > 0:
            zotero_author = creators[0].get('lastName', '').lower()
        else:
            zotero_author = 'unknown'

        # Get first word of title from Zotero
        if title:
            title_words = str(title).split()
            zotero_title_word = title_words[0].lower() if title_words else 'unknown'
        else:
            zotero_title_word = 'unknown'

        # Compare components using string similarity
        author_ratio = SequenceMatcher(None, gdrive_author, zotero_author).ratio()
        title_ratio = SequenceMatcher(None, gdrive_title_word, zotero_title_word).ratio()
        year_match = 1.0 if gdrive_year == year else 0.0

        # Weight: author 40%, title 40%, year 20%
        confidence = (author_ratio * 0.4) + (title_ratio * 0.4) + (year_match * 0.2)

        # Only return if confidence is in fuzzy range (0.5-0.9)
        if 0.5 <= confidence <= 0.9:
            reason = f"fuzzy_match: author={author_ratio:.2f} title={title_ratio:.2f} year={year_match:.2f}"
            return confidence, reason

        return 0.0, f"confidence {confidence:.2f} outside fuzzy range"

    except Exception as e:
        return 0.0, f"Error: {str(e)}"


def match_gdrive_to_citation_key(
    gdrive_filename: str,
    citation_key: str,
) -> Tuple[float, str]:
    """
    Match Google Drive filename to Zotero citation key.

    Compares extracted components:
    - Author (first surname from GDrive, against citation key first part)
    - Year (between dashes in GDrive, against citation key last part)
    - Title word (first word after second dash in GDrive, against citation key middle part)

    Returns:
        Tuple of (confidence_score 0.0-1.0, reason)

    Confidence levels:
    - 1.0: All 3 components match (author, year, title_word)
    - 0.67: 2 components match
    - 0.33: 1 component matches
    - 0.0: No match or parse error
    """
    try:
        # Extract components from GDrive filename
        gdrive_author, gdrive_year, gdrive_title_word = extract_gdrive_components(gdrive_filename)

        if not all([gdrive_author, gdrive_year, gdrive_title_word]):
            return 0.0, "Could not parse GDrive filename"

        # Extract components from citation key
        # Format: firstname_firstword_year
        key_parts = citation_key.lower().split('_')
        if len(key_parts) < 3:
            return 0.0, "Citation key format invalid (expected: author_title_year)"

        key_author = key_parts[0].lower()
        key_title_word = key_parts[1].lower()
        key_year = key_parts[2].lower()

        # Compare components
        matches = 0
        reasons = []

        if gdrive_author == key_author:
            matches += 1
            reasons.append(f"author={gdrive_author}")
        else:
            reasons.append(f"author MISMATCH {gdrive_author} vs {key_author}")

        if gdrive_year == key_year:
            matches += 1
            reasons.append(f"year={gdrive_year}")
        else:
            reasons.append(f"year MISMATCH {gdrive_year} vs {key_year}")

        if gdrive_title_word == key_title_word:
            matches += 1
            reasons.append(f"title={gdrive_title_word}")
        else:
            reasons.append(f"title MISMATCH {gdrive_title_word} vs {key_title_word}")

        # Calculate confidence
        confidence = matches / 3.0
        reason = " | ".join(reasons)

        return confidence, reason

    except Exception as e:
        return 0.0, f"Error: {str(e)}"


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))

    from scripts.zotero_client import get_citations
    from dotenv import load_dotenv
    import os

    print("=" * 80)
    print("GDRIVE <-> CITATION KEY MATCHER TEST")
    print("=" * 80)

    print("\n[Test 1] Manual example:")
    gdrive = "Avramova_et_al-2025-Overview_of_Existing_Multi_Criteria_Decision_Making_MCDM_Methods_Used_in_Industrial_Environments.pdf"
    citkey = "avramova_overview_2025"
    conf, reason = match_gdrive_to_citation_key(gdrive, citkey)
    print(f"  GDrive: {gdrive[:70]}...")
    print(f"  Citation Key: {citkey}")
    print(f"  Confidence: {conf:.2f}")
    print(f"  Details: {reason}")

    print("\n[Test 2] Testing with real papers from Zotero:")
    try:
        env_file = Path(".env")
        load_dotenv(env_file)
        api_key = os.getenv("ZOTERO_API_KEY")
        group_id = os.getenv("ZOTERO_GROUP_ID", "6479832")

        if not api_key:
            print("  ERROR: ZOTERO_API_KEY not found in .env")
        else:
            from pyzotero import Zotero
            from scripts.zotero_client import generate_citation_key

            zot = Zotero(library_id=group_id, library_type="group", api_key=api_key)
            papers = zot.everything(zot.top(itemType="-attachment"))[:5]

            print(f"  Found {len(papers)} papers, testing citation key generation:\n")

            for i, item in enumerate(papers):
                data = item['data']
                creators = data.get('creators', [])
                title = data.get('title', '')
                date_str = data.get('date', '')
                year = date_str[:4] if date_str else 'unknown'

                gen_key = generate_citation_key(creators, title, year)
                print(f"  {i+1}. {title[:60]}...")
                print(f"     Generated key: {gen_key}")

    except Exception as e:
        print(f"  Could not test with Zotero API: {e}")

    print("\n" + "=" * 80)
