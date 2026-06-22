"""
Nielsen Metadata Reference Library

Centralized access to metadata for all Nielsen categories (CSD, RTD, Energidrikke, etc.).
Load once, query efficiently without filesystem reads on every access.

This module provides:
- get_column_definition(column_name, category='CSD') → Full metadata for a column
- get_fact_columns(category='CSD') → All facts table columns with definitions
- get_dimension(dimension_name, category='CSD') → All columns in a dimension (market, period, product)
- list_categories() → Available categories
- describe_column(column_name, category='CSD') → Human-readable description

Usage:
    from METADATA import get_column_definition, get_fact_columns, get_dimension

    # Get full definition for a column
    sales_meta = get_column_definition('sales_units', category='CSD')
    print(f"{sales_meta['description']}")

    # Get all facts table columns
    facts = get_fact_columns(category='CSD')
    for col_name, meta in facts.items():
        print(f"{col_name} ({meta['type']}): {meta['description']}")

    # Get all product dimension columns
    products = get_dimension('product', category='CSD')
    print(f"Product has {len(products)} columns")
"""

import json
from pathlib import Path
from typing import Dict, Optional, List

# Lazy-load metadata on first import
_METADATA_CACHE = {}
_METADATA_PATH = Path(__file__).parent / "thesis" / "data" / "raw" / "nielsen" / "NIELSEN_METADATA_INDEX.json"


def _load_metadata(category: str = 'CSD') -> Dict:
    """Load metadata for a category (cached in memory)."""
    if category not in _METADATA_CACHE:
        try:
            with open(_METADATA_PATH.parent / f"{category.upper()}_METADATA_INDEX.json") as f:
                _METADATA_CACHE[category] = json.load(f)
        except FileNotFoundError:
            # Fallback: try CSD if category not found
            if category != 'CSD':
                return _load_metadata('CSD')
            raise FileNotFoundError(f"Metadata not found for {category}")
    return _METADATA_CACHE[category]


def get_column_definition(column_name: str, category: str = 'CSD') -> Optional[Dict]:
    """
    Get full metadata definition for a column.

    Returns:
        Dict with keys: position, type, comment, unit, null_meaning, description
        None if column not found

    Example:
        >>> meta = get_column_definition('sales_units', 'CSD')
        >>> print(meta['description'])
        'Total sales out of store expressed in consumer purchase units...'
    """
    meta = _load_metadata(category)

    # Check facts table
    if column_name in meta['facts_table']['columns']:
        return meta['facts_table']['columns'][column_name]

    # Check all dimensions
    for dim_name, dim_data in meta['dimensions'].items():
        if column_name in dim_data['columns']:
            return dim_data['columns'][column_name]

    return None


def get_fact_columns(category: str = 'CSD') -> Dict[str, Dict]:
    """
    Get all columns in the facts table with full definitions.

    Returns:
        Dict mapping column names to metadata dicts

    Example:
        >>> facts = get_fact_columns('CSD')
        >>> for col, meta in facts.items():
        ...     print(f"{col}: {meta['type']}")
    """
    meta = _load_metadata(category)
    return meta['facts_table']['columns']


def get_dimension(dimension_name: str, category: str = 'CSD') -> Dict[str, Dict]:
    """
    Get all columns in a dimension (market, period, product).

    Args:
        dimension_name: 'market', 'period', or 'product'
        category: Category code (default 'CSD')

    Returns:
        Dict mapping column names to metadata dicts

    Example:
        >>> period = get_dimension('period', 'CSD')
        >>> for col, meta in period.items():
        ...     print(f"{col}: {meta['description']}")
    """
    meta = _load_metadata(category)
    if dimension_name not in meta['dimensions']:
        raise ValueError(f"Unknown dimension: {dimension_name}. Choose: market, period, product")
    return meta['dimensions'][dimension_name]['columns']


def get_dimension_info(dimension_name: str, category: str = 'CSD') -> Dict:
    """
    Get dimension metadata (name, rows, description) + columns.

    Returns:
        Dict with keys: name, rows, description, columns
    """
    meta = _load_metadata(category)
    if dimension_name not in meta['dimensions']:
        raise ValueError(f"Unknown dimension: {dimension_name}")
    return meta['dimensions'][dimension_name]


def describe_column(column_name: str, category: str = 'CSD') -> str:
    """
    Get human-readable description of a column.

    Returns:
        String: full description, or "Column not found" if not in metadata

    Example:
        >>> print(describe_column('sales_units', 'CSD'))
        'Total sales out of store expressed in consumer purchase units...'
    """
    meta = get_column_definition(column_name, category)
    if meta is None:
        return f"Column '{column_name}' not found in {category} metadata"
    return meta.get('description', meta.get('comment', 'No description available'))


def list_categories() -> List[str]:
    """List available Nielsen categories with metadata indexed."""
    metadata_dir = _METADATA_PATH.parent
    categories = []
    for f in metadata_dir.glob("*_METADATA_INDEX.json"):
        cat = f.stem.replace("_METADATA_INDEX", "")
        categories.append(cat)
    return sorted(categories)


def fact_columns_by_unit(unit: str, category: str = 'CSD') -> Dict[str, str]:
    """
    Find all fact columns with a specific unit.

    Returns:
        Dict mapping column name to description

    Example:
        >>> dkk_cols = fact_columns_by_unit('DKK', 'CSD')
        >>> for col in dkk_cols:
        ...     print(col)
        'sales_value'
        'sales_value_any_promo'
        'baseline_sales_value'
        ...
    """
    facts = get_fact_columns(category)
    return {
        col: meta.get('description', '')
        for col, meta in facts.items()
        if meta.get('unit') == unit
    }


def get_nullable_columns(table_name: str, category: str = 'CSD') -> List[str]:
    """
    Get all nullable columns in a table.

    Args:
        table_name: 'facts', 'market', 'period', or 'product'
        category: Category code

    Returns:
        List of column names where NULL is possible

    Example:
        >>> nullable = get_nullable_columns('facts', 'CSD')
        >>> 'sales_units' in nullable  # This can be NULL
        True
    """
    if table_name == 'facts':
        columns = get_fact_columns(category)
    elif table_name in ['market', 'period', 'product']:
        columns = get_dimension(table_name, category)
    else:
        raise ValueError(f"Unknown table: {table_name}")

    return [
        col for col, meta in columns.items()
        if meta.get('null_meaning', '').lower() not in ['not nullable', 'never null']
    ]


if __name__ == "__main__":
    # Demo: Show metadata access
    print("=" * 80)
    print("Nielsen Metadata Reference Library — Demo")
    print("=" * 80)

    # Show available categories
    categories = list_categories()
    print(f"\n📚 Available categories: {', '.join(categories)}")

    # Demo: Facts table columns
    print(f"\n📊 Facts Table (CSD) — {len(get_fact_columns('CSD'))} columns:")
    for col, meta in list(get_fact_columns('CSD').items())[:3]:
        print(f"  • {col} ({meta['type']}, {meta['unit']})")
        print(f"    {meta['description'][:100]}...")

    # Demo: Dimension metadata
    print(f"\n🔷 Period Dimension — {len(get_dimension('period', 'CSD'))} columns:")
    period_info = get_dimension_info('period', 'CSD')
    print(f"  Range: {period_info['range']}")
    print(f"  Description: {period_info['description']}")

    # Demo: Column lookup
    print(f"\n🔍 Column Lookup: 'weighted_distribution'")
    meta = get_column_definition('weighted_distribution', 'CSD')
    if meta:
        print(f"  Type: {meta['type']}")
        print(f"  Unit: {meta['unit']}")
        print(f"  Description: {meta['description']}")

    # Demo: Nullable columns
    print(f"\n⚠️  Nullable columns in facts table:")
    nullable = get_nullable_columns('facts', 'CSD')
    print(f"  {len(nullable)} columns can be NULL")
    print(f"  Examples: {', '.join(nullable[:3])}")
