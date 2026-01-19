"""
Babylon Civilization Example - Scientific Focus

This example demonstrates:
- Civilization with ACTION_GROUP_BUNDLE.AGE_ANTIQUITY
- Scientific traits (TRAIT_SCIENTIFIC)
- Custom unit (Sabum Kibittum - unique melee unit)
- Unique building (Edubba - science/culture focused)
- Civilization ability modifier for science bonuses
- Progression tree with unique civic nodes
- Icon imports for civilization and unit
- All entities linked together using builder bindings
- Module-level localization for proper LOC_MODULE_* entries

Babylon is set up as a scientific civilization with bonuses to tech advancement
and knowledge-based yields, showcasing how to build a specialized civ around a
single core concept (Science).
"""

from civ7_modding_tools import Mod, ActionGroupBundle
from civ7_modding_tools.builders import (
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
    ProgressionTreeBuilder,
    ProgressionTreeNodeBuilder,
    ModifierBuilder,
    ImportFileBuilder,
)
from civ7_modding_tools.localizations import ModuleLocalization


# Create module-level localization for mod metadata
module_loc = ModuleLocalization(
    name="Babylon",
    description="The Babylon civilization - ancient centre of science and learning",
    authors="Firaxis Games"
)

# Create mod with rich metadata
mod = Mod({
    'id': 'babylon',
    'version': '1',
    'name': 'Babylon',  # Use plain text instead of LOC key
    'description': 'The Babylon civilization - ancient centre of science and learning',
    'authors': 'Firaxis Games',
    'affects_saved_games': True,
    'enabled_by_default': True,
    'package': 'Babylon',
    'module_localizations': module_loc,
})

# ACTION_GROUP_BUNDLE.AGE_ANTIQUITY
AGE_ANTIQUITY_BUNDLE = ActionGroupBundle(
    action_group_id='AGE_ANTIQUITY'
)

# Import civilization icon
civilization_icon = ImportFileBuilder()
civilization_icon.action_group_bundle = AGE_ANTIQUITY_BUNDLE
civilization_icon.fill({
    'source_path': './assets/babylon-civ-icon.png',
    'target_name': 'civ_sym_babylon'
})

# Define Babylon civilization with scientific traits
civilization = CivilizationBuilder()
civilization.action_group_bundle = AGE_ANTIQUITY_BUNDLE
civilization.fill({
    'civilization_type': 'CIVILIZATION_BABYLON',
    'civilization': {
        'domain': 'AntiquityAgeCivilizations',
        'civilization_type': 'CIVILIZATION_BABYLON'
    },
    'civilization_traits': [
        'TRAIT_ANTIQUITY_CIV',
        'TRAIT_ATTRIBUTE_SCIENTIFIC',
    ],
    'civilization_tags': ['TAG_TRAIT_SCIENTIFIC'],
    'icon': {
        'path': f'fs://game/{mod.mod_id}/civ_sym_babylon'
    },
    'civilization_unlocks': [
        {
            'age_type': 'AGE_EXPLORATION',
            'type': 'CIVILIZATION_PERSIA',
            'kind': 'KIND_CIVILIZATION',
            'name': 'LOC_CIVILIZATION_PERSIA_NAME',
            'description': 'LOC_CIVILIZATION_PERSIA_DESCRIPTION',
            'icon': 'CIVILIZATION_PERSIA'
        }
    ],
    'localizations': [
        {
            'name': 'Babylon',
            'description': 'Keepers of ancient wisdom and masters of the sciences.',
            'full_name': 'The Kingdom of Babylon',
            'adjective': 'Babylonian',
            'city_names': ['Babylon', 'Nippur', 'Lagash']
        }
    ],
    'loading_info_civilizations': [
        {
            'loading_image_tag': 'LOADING_BABYLON',
            'civilization_description': 'LOC_CIVILIZATION_BABYLON_DESCRIPTION'
        }
    ],
    'civilization_favored_wonders': [
        {
            'wonder_type': 'WONDER_HANGING_GARDENS'
        },
        {
            'wonder_type': 'WONDER_ORACLE'
        },
        {
            'wonder_type': 'WONDER_PYRAMIDS'
        }
    ],
    'leader_civ_priorities': [
        {
            'leader_type': 'LEADER_NEBUCHADNEZZAR_II',
            'priority': 8
        },
        {
            'leader_type': 'LEADER_HAMMURABI',
            'priority': 6
        }
    ],
})

# Civilization ability modifier - science yield bonus
civilization_modifier = ModifierBuilder()
civilization_modifier.action_group_bundle = AGE_ANTIQUITY_BUNDLE
civilization_modifier.fill({
    'modifier': {
        'collection': 'COLLECTION_ALL_CITIES',
        'effect': 'EFFECT_CITY_ADJUST_YIELD',
        'permanent': True,
        'requirements': [{
            'type': 'REQUIREMENT_CITY_IS_CITY'
        }],
        'arguments': [
            {'name': 'YieldType', 'value': 'YIELD_SCIENCE'},
            {'name': 'Amount', 'value': 100},
            {'name': 'Tooltip', 'value': 'LOC_BABYLON_SCIENCE_BONUS'}
        ]
    }
})

# Bind modifier to civilization
civilization.bind([civilization_modifier])

# Import unit icon
unit_icon = ImportFileBuilder()
unit_icon.action_group_bundle = AGE_ANTIQUITY_BUNDLE
unit_icon.fill({
    'source_path': './assets/sabum-kibittum-icon.png',
    'target_name': 'sabum_kibittum.png'
})

# Define unique unit - Sabum Kibittum (Babylonian warrior)
unit = UnitBuilder()
unit.action_group_bundle = AGE_ANTIQUITY_BUNDLE
unit.fill({
    'unit_type': 'UNIT_BABYLON_SABUM_KIBITTUM',
    'type_tags': ['UNIT_CLASS_MELEE', 'UNIT_CLASS_ANTI_CAVALRY'],
    'unit': {
        'trait_type': 'TRAIT_BABYLON',
        'core_class': 'CORE_CLASS_MILITARY',
        'domain': 'DOMAIN_LAND',
        'formation_class': 'FORMATION_CLASS_LAND_COMBAT',
        'unit_movement_class': 'UNIT_MOVEMENT_CLASS_FOOT',
        'base_moves': 2,
        'base_sight_range': 2,
    },
    'icon': {
        'path': f'fs://game/{mod.mod_id}/sabum_kibittum.png'
    },
    'unit_cost': {'yield_type': 'YIELD_PRODUCTION', 'cost': 30},
    'unit_stat': {'combat': 15},
    'unit_replace': {'replaces_unit_type': 'UNIT_WARRIOR'},
    'visual_remap': {'to': 'UNIT_WARRIOR'},
    'localizations': [
        {
            'name': 'Sabum Kibittum',
            'description': 'Elite warrior of Babylon, trained in ancient tactics.'
        },
    ],
})

# Define unique building - Edubba (House of Tablets - library)
constructible = ConstructibleBuilder()
constructible.action_group_bundle = AGE_ANTIQUITY_BUNDLE
constructible.fill({
    'constructible_type': 'BUILDING_BABYLON_EDUBBA',
    'constructible': {
        'constructible_type': 'BUILDING_BABYLON_EDUBBA',
    },
    'building': {},
    'type_tags': [
        'AGELESS',
        'SCIENCE',
        'CULTURE'
    ],
    'constructible_valid_districts': [
        'DISTRICT_URBAN',
        'DISTRICT_CITY_CENTER',
    ],
    'constructible_maintenances': [
        {'yield_type': 'YIELD_PRODUCTION', 'amount': 2},
    ],
    'yield_changes': [
        {'yield_type': 'YIELD_SCIENCE', 'yield_change': 30},
        {'yield_type': 'YIELD_CULTURE', 'yield_change': 15},
    ],
    'icon': {
        'path': f'fs://game/{mod.mod_id}/edubba.png'
    },
    'localizations': [
        {
            'name': 'Edubba',
            'description': 'House of Tablets - preserves Babylon\'s vast knowledge.',
            'tooltip': 'Increases science and culture yields.'
        },
    ]
})

# Define first progression tree node
progression_tree_node = ProgressionTreeNodeBuilder()
progression_tree_node.action_group_bundle = AGE_ANTIQUITY_BUNDLE
progression_tree_node.fill({
    'progression_tree_node_type': 'NODE_CIVICS_BABYLON1',
    'progression_tree_node': {
        'progression_tree_node_type': 'NODE_CIVICS_BABYLON1',
    },
    'progression_tree_advisories': ['ADVISORY_CLASS_SCIENCE'],
    'localizations': [{'name': 'Babylonian Learning'}]
})

# Bind modifier and buildings to first node
node1_modifier = ModifierBuilder()
node1_modifier.fill({
    'modifier': {
        'collection': 'COLLECTION_OWNER',
        'effect': 'EFFECT_PLAYER_ADJUST_YIELD_FROM_BUILDING_TAG',
        'arguments': [
            {'name': 'Tag', 'value': 'SCIENCE'},
            {'name': 'YieldType', 'value': 'YIELD_SCIENCE'},
            {'name': 'Amount', 'value': 15},
        ],
    },
    'localizations': [{
        'description': 'Science buildings provide +15% yields'
    }]
})
progression_tree_node.bind([node1_modifier, constructible, unit])

# Define second progression tree node
progression_tree_node2 = ProgressionTreeNodeBuilder()
progression_tree_node2.action_group_bundle = AGE_ANTIQUITY_BUNDLE
progression_tree_node2.fill({
    'progression_tree_node_type': 'NODE_CIVICS_BABYLON2',
    'progression_tree_node': {
        'progression_tree_node_type': 'NODE_CIVICS_BABYLON2',
    },
    'progression_tree_advisories': ['ADVISORY_CLASS_SCIENCE'],
    'localizations': [{'name': 'Ancient Wisdom'}]
})

# Bind modifier to second node
node2_modifier = ModifierBuilder()
node2_modifier.fill({
    'modifier': {
        'collection': 'COLLECTION_OWNER',
        'effect': 'EFFECT_PLAYER_ADJUST_TECH_BOOST_VALUE',
        'arguments': [
            {'name': 'Amount', 'value': 25},
        ],
    },
    'localizations': [{
        'description': 'Eurekas provide +25% bonus to tech progress'
    }]
})
progression_tree_node2.bind([node2_modifier])

# Define progression tree
progression_tree = ProgressionTreeBuilder()
progression_tree.action_group_bundle = AGE_ANTIQUITY_BUNDLE
progression_tree.fill({
    'progression_tree_type': 'TREE_CIVICS_BABYLON',
    'progression_tree': {
        'progression_tree_type': 'TREE_CIVICS_BABYLON',
        'age_type': 'AGE_ANTIQUITY'
    },
    # Node prerequisites
    'progression_tree_prereqs': [{
        'node': 'NODE_CIVICS_BABYLON2',
        'prereq_node': 'NODE_CIVICS_BABYLON1'
    }],
    'localizations': [{'name': 'Babylonian Civic Tree'}]
})

# Bind nodes to tree
progression_tree.bind([progression_tree_node, progression_tree_node2])

# Bind all entities to civilization
civilization.bind([
    unit,
    constructible,
    progression_tree,
])

# Add all builders to mod
mod.add([
    civilization,
    unit,
    constructible,
    progression_tree,
    civilization_icon,
    unit_icon,
])

# Build mod
if __name__ == '__main__':
    mod.build('./dist-babylon')
