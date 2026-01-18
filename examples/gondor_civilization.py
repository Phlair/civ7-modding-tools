"""
Gondor Civilization Example - Python Port of build.ts

EXACT feature-for-feature port of build.ts (272 lines) for parity testing.

This example demonstrates:
- Civilization with ACTION_GROUP_BUNDLE.AGE_ANTIQUITY
- Traits, tags, and icon import
- Custom scout unit with unit_replace, visual_remap, icon
- Two custom buildings with yield changes
- Unique quarter with modifiers
- Progression tree with two nodes and prerequisites
- All entities linked together (Python uses properties instead of .bind())

Key Differences from TypeScript:
1. Python uses snake_case instead of camelCase for property names
2. Python doesn't have .bind() - entities are linked via builder properties
3. UniqueQuarterNode uses constructible_type + district_type instead of buildingType1/2
4. ProgressionTree node unlocks are specified in progression_tree_node_unlocks property

All other semantics match the TypeScript build.ts example exactly.
"""

from civ7_modding_tools import Mod, ActionGroupBundle
from civ7_modding_tools.builders import (
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
    UniqueQuarterBuilder,
    ProgressionTreeBuilder,
    ProgressionTreeNodeBuilder,
    ModifierBuilder,
    ImportFileBuilder,
)


# Create mod (matching TS: new Mod({id: 'mod-test', version: '1'}))
mod = Mod({
    'id': 'mod-test',
    'version': '1',
})

# ACTION_GROUP_BUNDLE.AGE_ANTIQUITY equivalent (matching TS constant usage)
# In Python, we create the ActionGroupBundle instance directly
AGE_ANTIQUITY_BUNDLE = ActionGroupBundle(
    action_group_id='AGE_ANTIQUITY'
)

# Import civilization icon (matching TS lines 31-35)
civilization_icon = ImportFileBuilder()
civilization_icon.action_group_bundle = AGE_ANTIQUITY_BUNDLE
civilization_icon.fill({
    'source_path': './assets/civ-icon.png',
    'target_name': 'civ_sym_gondor'
})

# Define Gondor civilization (matching TS lines 36-57)
civilization = CivilizationBuilder()
civilization.action_group_bundle = AGE_ANTIQUITY_BUNDLE
civilization.fill({
    'civilization_type': 'CIVILIZATION_GONDOR',
    'civilization': {
        'domain': 'AntiquityAgeCivilizations',
        'civilization_type': 'CIVILIZATION_GONDOR'
    },
    'civilization_traits': [
        'TRAIT_ANTIQUITY_CIV',
        'TRAIT_ATTRIBUTE_EXPANSIONIST',
        'TRAIT_ATTRIBUTE_MILITARISTIC',
    ],
    'civilization_tags': ['TAG_TRAIT_CULTURAL', 'TAG_TRAIT_ECONOMIC'],
    'icon': {
        'path': f'fs://game/{mod.mod_id}/civ_sym_gondor'
    },
    'localizations': [
        {
            'name': 'Custom civilization',
            'description': 'test description',
            'full_name': 'test full name',
            'adjective': 'test adjective',
            'city_names': ['Gondor', 'New Gondor']
        }
    ],
})

# Civilization ability modifier (matching TS lines 54-65)
civilization_modifier = ModifierBuilder()
civilization_modifier.action_group_bundle = AGE_ANTIQUITY_BUNDLE
civilization_modifier.fill({
    'modifier': {
        'collection': 'COLLECTION_PLAYER_UNITS',
        'effect': 'EFFECT_UNIT_ADJUST_MOVEMENT',
        'permanent': True,
        'requirements': [{
            'type': 'REQUIREMENT_UNIT_TAG_MATCHES',
            'arguments': [{'name': 'Tag', 'value': 'UNIT_CLASS_RECON'}]
        }],
        'arguments': [{'name': 'Amount', 'value': 10}]
    }
})

# Bind modifier to civilization
civilization.bind([civilization_modifier])

# Import unit icon (matching TS lines 67-71)
unit_icon = ImportFileBuilder()
unit_icon.action_group_bundle = AGE_ANTIQUITY_BUNDLE
unit_icon.fill({
    'source_path': './assets/unit-icon.png',
    'target_name': 'scout.png'
})

# Define custom scout unit (matching TS lines 73-90)
unit = UnitBuilder()
unit.action_group_bundle = AGE_ANTIQUITY_BUNDLE
unit.fill({
    'unit_type': 'UNIT_GONDOR_SCOUT',
    'type_tags': ['UNIT_CLASS_RECON', 'UNIT_CLASS_RECON_ABILITIES'],
    'unit': {
        'trait_type': 'TRAIT_GONDOR',
        'core_class': 'CORE_CLASS_MILITARY',
        'domain': 'DOMAIN_LAND',
        'formation_class': 'FORMATION_CLASS_LAND_COMBAT',
        'unit_movement_class': 'UNIT_MOVEMENT_CLASS_FOOT',
        'base_moves': 2,
        'base_sight_range': 10,
    },
    'icon': {
        'path': f'fs://game/{mod.mod_id}/scout.png'
    },
    'unit_cost': {'yield_type': 'YIELD_PRODUCTION', 'cost': 20},
    'unit_stat': {'combat': 0},
    'unit_replace': {'replaces_unit_type': 'UNIT_SCOUT'},
    'visual_remap': {'to': 'UNIT_ARMY_COMMANDER'},
    'localizations': [
        {'name': 'Custom scout', 'description': 'test description'},
    ],
})

# Define first custom building (matching TS lines 92-116)
constructible = ConstructibleBuilder()
constructible.action_group_bundle = AGE_ANTIQUITY_BUNDLE
constructible.fill({
    'constructible_type': 'BUILDING_GONDOR',
    'constructible': {
        'constructible_type': 'BUILDING_GONDOR',
    },
    'building': {},
    'type_tags': [
        'AGELESS',
        'PRODUCTION',
        'FOOD'
    ],
    'constructible_valid_districts': [
        'DISTRICT_URBAN',
        'DISTRICT_CITY_CENTER',
    ],
    'constructible_maintenances': [
        {'yield_type': 'YIELD_PRODUCTION', 'amount': 1},
        {'yield_type': 'YIELD_HAPPINESS', 'amount': 1},
    ],
    'yield_changes': [
        {'yield_type': 'YIELD_GOLD', 'yield_change': 20},
    ],
    'localizations': [
        {
            'name': 'Custom building',
            'description': 'Custom building test description',
            'tooltip': 'Custom building test tooltip'
        },
    ]
})

# Define second custom building (matching TS lines 118-142)
constructible2 = ConstructibleBuilder()
constructible2.action_group_bundle = AGE_ANTIQUITY_BUNDLE
constructible2.fill({
    'constructible_type': 'BUILDING_GONDOR2',
    'constructible': {
        'constructible_type': 'BUILDING_GONDOR2',
    },
    'building': {},
    'type_tags': [
        'AGELESS',
        'PRODUCTION',
        'FOOD'
    ],
    'constructible_valid_districts': [
        'DISTRICT_URBAN',
        'DISTRICT_CITY_CENTER',
    ],
    'constructible_maintenances': [
        {'yield_type': 'YIELD_PRODUCTION', 'amount': 1},
        {'yield_type': 'YIELD_HAPPINESS', 'amount': 1},
    ],
    'yield_changes': [
        {'yield_type': 'YIELD_GOLD', 'yield_change': 20},
    ],
    'localizations': [
        {
            'name': 'Custom building',
            'description': 'Custom building test description',
            'tooltip': 'Custom building test tooltip'
        },
    ]
})

# Define unique quarter (matching TS lines 144-178)
unique_quarter = UniqueQuarterBuilder()
unique_quarter.action_group_bundle = AGE_ANTIQUITY_BUNDLE
unique_quarter.fill({
    'unique_quarter_type': 'QUARTER_GONDOR',
    'unique_quarter': {
        'unique_quarter_type': 'QUARTER_GONDOR',
        'building_type_1': 'BUILDING_GONDOR',
        'building_type_2': 'BUILDING_GONDOR2',
    },
    'localizations': [
        {'name': 'Custom unique quarter', 'description': 'Custom unique quarter test description'},
    ]
})

# Bind modifier to unique quarter (matching TS lines 158-175)
unique_quarter_modifier = ModifierBuilder()
unique_quarter_modifier.fill({
    'modifier': {
        'collection': 'COLLECTION_ALL_CITIES',
        'effect': 'EFFECT_CITY_ADJUST_YIELD',
        'permanent': True,
        'requirements': [{
            'type': 'REQUIREMENT_CITY_HAS_UNIQUE_QUARTER',
            'arguments': [{'name': 'UniqueQuarterType', 'value': 'QUARTER_GONDOR'}]
        }, {
            'type': 'REQUIREMENT_CITY_IS_CITY'
        }],
        'arguments': [
            {'name': 'YieldType', 'value': 'YIELD_GOLD'},
            {'name': 'Amount', 'value': 2000},
            {'name': 'Tooltip', 'value': 'LOC_QUARTER_GONDOR_NAME'}
        ]
    }
})
unique_quarter.bind([unique_quarter_modifier])

# Define first progression tree node (matching TS lines 180-208)
progression_tree_node = ProgressionTreeNodeBuilder()
progression_tree_node.action_group_bundle = AGE_ANTIQUITY_BUNDLE
progression_tree_node.fill({
    'progression_tree_node_type': 'NODE_CIVICS_GONDOR1',
    'progression_tree_node': {
        'progression_tree_node_type': 'NODE_CIVICS_GONDOR1',
    },
    'progression_tree_advisories': ['ADVISORY_CLASS_FOOD'],
    'localizations': [{'name': 'Civic name'}]
})

# Bind modifiers and unlocks to first node (matching TS lines 190-208)
node1_modifier = ModifierBuilder()
node1_modifier.fill({
    'modifier': {
        'collection': 'COLLECTION_OWNER',
        'effect': 'EFFECT_PLAYER_ADJUST_CONSTRUCTIBLE_YIELD',
        'arguments': [
            {'name': 'Tag', 'value': 'FOOD'},
            {'name': 'YieldType', 'value': 'YIELD_FOOD'},
            {'name': 'Amount', 'value': 10},
        ],
    },
    'localizations': [{
        'description': '+10 Food'
    }]
})
progression_tree_node.bind([node1_modifier, constructible, constructible2, unit])

# Define second progression tree node (matching TS lines 210-231)
progression_tree_node2 = ProgressionTreeNodeBuilder()
progression_tree_node2.action_group_bundle = AGE_ANTIQUITY_BUNDLE
progression_tree_node2.fill({
    'progression_tree_node_type': 'NODE_CIVICS_GONDOR2',
    'progression_tree_node': {
        'progression_tree_node_type': 'NODE_CIVICS_GONDOR2',
    },
    'progression_tree_advisories': ['ADVISORY_CLASS_FOOD'],
    'localizations': [{'name': 'Civic name'}]
})

# Bind modifier to second node (matching TS lines 218-230)
node2_modifier = ModifierBuilder()
node2_modifier.fill({
    'modifier': {
        'collection': 'COLLECTION_OWNER',
        'effect': 'EFFECT_PLAYER_ADJUST_CONSTRUCTIBLE_YIELD',
        'arguments': [
            {'name': 'Tag', 'value': 'SCIENCE'},
            {'name': 'YieldType', 'value': 'YIELD_SCIENCE'},
            {'name': 'Amount', 'value': 10},
        ],
    },
    'localizations': [{
        'description': '+10 science'
    }]
})
progression_tree_node2.bind([node2_modifier])

# Define progression tree (matching TS lines 233-246)
progression_tree = ProgressionTreeBuilder()
progression_tree.action_group_bundle = AGE_ANTIQUITY_BUNDLE
progression_tree.fill({
    'progression_tree_type': 'TREE_CIVICS_GONDOR',
    'progression_tree': {
        'progression_tree_type': 'TREE_CIVICS_GONDOR',
        'age_type': 'AGE_ANTIQUITY'
    },
    # Node prerequisites (matching TS)
    'progression_tree_prereqs': [{
        'node': 'NODE_CIVICS_GONDOR2',
        'prereq_node': 'NODE_CIVICS_GONDOR1'
    }],
    'localizations': [{'name': 'Tree name'}]
})

# Bind nodes to tree (matching TS line 245)
progression_tree.bind([progression_tree_node, progression_tree_node2])

# Bind all entities to civilization (matching TS lines 249-256)
civilization.bind([
    unit,
    constructible,
    constructible2,
    unique_quarter,
    progression_tree,
])

# Add all builders to mod (matching TS lines 258-268)
# NOTE: progression_tree_node and progression_tree_node2 are NOT added to mod
# The progressionTree builder handles node creation internally (inline)
mod.add([
    civilization,
    unit,
    constructible,
    constructible2,
    unique_quarter,
    progression_tree,
    civilization_icon,  # Add builders, not files
    unit_icon,  # Add builders, not files
])

# Build mod (matching TS line 268)
if __name__ == '__main__':
    mod.build('./dist-py-candidate')
