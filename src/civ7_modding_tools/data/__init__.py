"""
Reference data files for Civilization VII modding configuration values.

This package provides JSON files documenting all valid options for modding
attributes like BuildingCulture, TerrainType, YieldType, etc., extracted
from official game data and community mod examples.

All files are in kebab-case naming convention.
"""

import json
from pathlib import Path
from typing import Any, Dict, List


# Module directory
_DATA_DIR = Path(__file__).parent


def load_reference_data(filename: str) -> Dict[str, Any]:
    """
    Load a reference JSON data file.

    Args:
        filename: Name of the JSON file (e.g., 'yield-types.json')

    Returns:
        Parsed JSON data as dictionary

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is invalid JSON
    """
    file_path = _DATA_DIR / filename
    with open(file_path) as f:
        return json.load(f)


def get_yield_types() -> List[Dict[str, str]]:
    """Get all available yield types."""
    return load_reference_data('yield-types.json')['values']


def get_district_types() -> List[Dict[str, str]]:
    """Get all available district types."""
    return load_reference_data('district-types.json')['values']


def get_terrain_types() -> List[Dict[str, str]]:
    """Get all available terrain types."""
    return load_reference_data('terrain-types.json')['values']


def get_building_cultures() -> List[Dict[str, Any]]:
    """Get all available building cultures with civilization context."""
    return load_reference_data('building-cultures.json')['values']


def get_unit_cultures() -> List[Dict[str, Any]]:
    """Get all available unit cultures with civilization context."""
    return load_reference_data('unit-cultures.json')['values']


def get_effects() -> List[Dict[str, str]]:
    """Get all available game effects."""
    return load_reference_data('effects.json')['values']


def get_requirements() -> List[Dict[str, str]]:
    """Get all available requirement types."""
    return load_reference_data('requirement-types.json')['values']


def get_collections() -> List[Dict[str, str]]:
    """Get all available collection types (modifier scopes)."""
    return load_reference_data('collection-types.json')['values']


def get_advisory_class_types() -> List[Dict[str, str]]:
    """Get all available advisory class types."""
    return load_reference_data('advisory-class-types.json')['values']


def get_tags() -> List[Dict[str, str]]:
    """Get all available tags with their categories."""
    return load_reference_data('tags.json')['values']


def get_civilization_domains() -> List[Dict[str, str]]:
    """Get all available civilization UI domain groupings."""
    return load_reference_data('civilization-domains.json')['values']


__all__ = [
    'load_reference_data',
    'get_yield_types',
    'get_district_types',
    'get_terrain_types',
    'get_building_cultures',
    'get_unit_cultures',
    'get_effects',
    'get_requirements',
    'get_collections',
    'get_advisory_class_types',
    'get_tags',
    'get_civilization_domains',
]
