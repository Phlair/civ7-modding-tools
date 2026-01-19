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


# Original requested types
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


# Additional high-value types
def get_constructible_classes() -> List[Dict[str, str]]:
    """Get all available constructible classes (building, wonder, improvement, etc.)."""
    return load_reference_data('constructible-classes.json')['values']


def get_unit_movement_classes() -> List[Dict[str, str]]:
    """Get all available unit movement classes (foot, mounted, naval, etc.)."""
    return load_reference_data('unit-movement-classes.json')['values']


def get_core_classes() -> List[Dict[str, str]]:
    """Get all available core unit classes (military, civilian, support)."""
    return load_reference_data('core-classes.json')['values']


def get_formation_classes() -> List[Dict[str, str]]:
    """Get all available formation classes for unit grouping."""
    return load_reference_data('formation-classes.json')['values']


def get_domains() -> List[Dict[str, str]]:
    """Get all available domains (land, sea)."""
    return load_reference_data('domains.json')['values']


def get_cost_progression_models() -> List[Dict[str, str]]:
    """Get all available cost progression models."""
    return load_reference_data('cost-progression-models.json')['values']


def get_biome_types() -> List[Dict[str, str]]:
    """Get all available biome types."""
    return load_reference_data('biome-types.json')['values']


def get_feature_types() -> List[Dict[str, str]]:
    """Get all available map feature types."""
    return load_reference_data('feature-types.json')['values']


def get_river_placements() -> List[Dict[str, str]]:
    """Get all available river placement options."""
    return load_reference_data('river-placements.json')['values']


def get_ages() -> List[Dict[str, str]]:
    """Get all available game ages."""
    return load_reference_data('ages.json')['values']


def get_military_domains() -> List[Dict[str, str]]:
    """Get all available military domain types."""
    return load_reference_data('military-domains.json')['values']


def get_promotion_classes() -> List[Dict[str, str]]:
    """Get all available unit promotion classes."""
    return load_reference_data('promotion-classes.json')['values']


def get_government_types() -> List[Dict[str, str]]:
    """Get all available government types."""
    return load_reference_data('government-types.json')['values']


def get_project_types() -> List[Dict[str, str]]:
    """Get all available city project types."""
    return load_reference_data('project-types.json')['values']


def get_belief_class_types() -> List[Dict[str, str]]:
    """Get all available belief class types."""
    return load_reference_data('belief-class-types.json')['values']


def get_difficulty_types() -> List[Dict[str, str]]:
    """Get all available difficulty levels."""
    return load_reference_data('difficulty-types.json')['values']


def get_progression_trees() -> List[Dict[str, str]]:
    """Get all available progression tree types (civics/tech trees)."""
    return load_reference_data('progression-trees.json')['values']


def get_great_work_object_types() -> List[Dict[str, str]]:
    """Get all available great work object types."""
    return load_reference_data('great-work-object-types.json')['values']


def get_resource_classes() -> List[Dict[str, str]]:
    """Get all available resource classes."""
    return load_reference_data('resource-classes.json')['values']


def get_handicap_system_types() -> List[Dict[str, str]]:
    """Get all available handicap system types."""
    return load_reference_data('handicap-system-types.json')['values']


def get_leaders() -> List[Dict[str, str]]:
    """Get all available leader types."""
    return load_reference_data('leaders.json')['values']


def get_leader_attributes() -> List[Dict[str, str]]:
    """Get all available leader personality attributes."""
    return load_reference_data('leader-attributes.json')['values']


__all__ = [
    'load_reference_data',
    # Original types
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
    # Additional types
    'get_constructible_classes',
    'get_unit_movement_classes',
    'get_core_classes',
    'get_formation_classes',
    'get_domains',
    'get_cost_progression_models',
    'get_biome_types',
    'get_feature_types',
    'get_river_placements',
    'get_ages',
    'get_military_domains',
    'get_promotion_classes',
    'get_government_types',
    'get_project_types',
    'get_belief_class_types',
    'get_difficulty_types',
    'get_progression_trees',
    'get_great_work_object_types',
    'get_resource_classes',
    'get_handicap_system_types',
    'get_leaders',
    'get_leader_attributes',
]
