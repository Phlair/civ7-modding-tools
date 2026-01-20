"""
Babylon Civilization - Generated from YAML

The Babylon civilization - ancient centre of science and learning
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
    TraditionBuilder,
)
from civ7_modding_tools.localizations import (
    ModuleLocalization,
    TraditionLocalization,
)

# Constants
CITY_NAMES = [
    'Babylon',
    'Nippur',
    'Lagash',
    'Uruk',
    'Ur',
    'Eridu',
    'Kish',
    'Sippar',
    'Borsippa',
    'Cutha',
    'Diwaniya',
    'Isin',
    'Larsa',
    'Adab',
    'Assur',
    'Susa',
    'Tyre',
    'Sidon',
    'Byblos',
    'Memphis',
    'Thebes',
    'Alexandria',
    'Athens',
    'Corinth',
    'Sparta',
    'Troy',
    'Persepolis',
    'Ecbatana',
    'Sargon',
    'Hammurabi',
]

# Module localization
MODULE_LOC = ModuleLocalization(
    name="Babylon",
    description="The Babylon civilization - ancient centre of science and learning",
    authors="Phlair",
)

# Mod metadata and setup
mod = Mod({
    'id': 'babylon',
    'version': '1',
    'name': 'Babylon',
    'description': 'The Babylon civilization - ancient centre of science and learning',
    'authors': 'Phlair',
    'affects_saved_games': True,
    'enabled_by_default': True,
    'package': 'Babylon',
    'module_localizations': MODULE_LOC,
})

# Action group
AGE_ANTIQUITY = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')

# Icon imports
civilization_icon = ImportFileBuilder()
civilization_icon.action_group_bundle = AGE_ANTIQUITY
civilization_icon.fill({
    'source_path': './assets/babylon-civ-icon.png',
    'target_name': 'civ_sym_babylon'
})

unit_icon = ImportFileBuilder()
unit_icon.action_group_bundle = AGE_ANTIQUITY
unit_icon.fill({
    'source_path': './assets/sabum-kibittum-icon.png',
    'target_name': 'sabum_kibittum.png'
})

# Modifiers
civilization_modifier = ModifierBuilder()
civilization_modifier.fill({
    'modifier': {
        'collection': 'COLLECTION_ALL_CITIES',
        'effect': 'EFFECT_CITY_ADJUST_YIELD',
        'permanent': True,
        'requirements': [
            {
                'type': 'REQUIREMENT_CITY_IS_CITY',
            },
        ],
        'arguments': [
            {
                'name': 'YieldType',
                'value': 'YIELD_SCIENCE',
            },
            {
                'name': 'Amount',
                'value': 100,
            },
            {
                'name': 'Tooltip',
                'value': 'LOC_BABYLON_SCIENCE_BONUS',
            },
        ],
    },
})

scribal_modifier = ModifierBuilder()
scribal_modifier.fill({
    'modifier_type': 'MODIFIER_TRADITION_BABYLON_SCRIBES',
    'modifier': {
        'collection': 'COLLECTION_OWNER',
        'effect': 'EFFECT_CITY_ADJUST_WORKER_YIELD',
        'arguments': [
            {
                'name': 'Tag',
                'value': 'SCIENCE',
            },
            {
                'name': 'YieldType',
                'value': 'YIELD_SCIENCE',
            },
            {
                'name': 'Amount',
                'value': 15,
            },
        ],
    },
    'localizations': [
        {
            'description': 'Scientific buildings provide +15% Science yields',
        },
    ],
})

library_modifier = ModifierBuilder()
library_modifier.fill({
    'modifier_type': 'MODIFIER_TRADITION_BABYLON_LIBRARY',
    'modifier': {
        'collection': 'COLLECTION_OWNER',
        'effect': 'EFFECT_PLAYER_ADJUST_YIELD_MODIFIER',
        'arguments': [
            {
                'name': 'YieldType',
                'value': 'YIELD_CULTURE',
            },
            {
                'name': 'Amount',
                'value': 10,
            },
        ],
    },
    'localizations': [
        {
            'description': 'Cultural and scientific heritage enhances yields',
        },
    ],
})

node1_modifier = ModifierBuilder()
node1_modifier.fill({
    'modifier': {
        'collection': 'COLLECTION_OWNER',
        'effect': 'EFFECT_CITY_ADJUST_WORKER_YIELD',
        'arguments': [
            {
                'name': 'Tag',
                'value': 'SCIENCE',
            },
            {
                'name': 'YieldType',
                'value': 'YIELD_SCIENCE',
            },
            {
                'name': 'Amount',
                'value': 15,
            },
        ],
    },
    'localizations': [
        {
            'description': 'Science buildings provide +15% yields',
        },
    ],
})

node2_modifier = ModifierBuilder()
node2_modifier.fill({
    'modifier': {
        'collection': 'COLLECTION_OWNER',
        'effect': 'EFFECT_CITY_ADJUST_WORKER_YIELD',
        'arguments': [
            {
                'name': 'Amount',
                'value': 25,
            },
        ],
    },
    'localizations': [
        {
            'description': 'Eurekas provide +25% bonus to tech progress',
        },
    ],
})

# Traditions
tradition_scribes = TraditionBuilder()
tradition_scribes.action_group_bundle = AGE_ANTIQUITY
tradition_scribes.fill({
    'tradition_type': 'TRADITION_BABYLON_SCRIBES',
    'tradition': {},
    'localizations': [
        TraditionLocalization(
            name='Scribal Tradition',
            description='Ancient Babylonian scholars preserve knowledge: +15% Science',
        )
    ],
})
tradition_scribes.bind([scribal_modifier])

tradition_library = TraditionBuilder()
tradition_library.action_group_bundle = AGE_ANTIQUITY
tradition_library.fill({
    'tradition_type': 'TRADITION_BABYLON_LIBRARY',
    'tradition': {},
    'localizations': [
        TraditionLocalization(
            name='Library of Babylon',
            description='Great repository of knowledge: +10% Culture and Science',
        )
    ],
})
tradition_library.bind([library_modifier])

# Units
unit = UnitBuilder()
unit.action_group_bundle = AGE_ANTIQUITY
unit.fill({
    'unit_type': 'UNIT_BABYLON_SABUM_KIBITTUM',
    'type_tags': ['UNIT_CLASS_MELEE'],
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
        'path': 'fs://game/${metadata.id}/sabum_kibittum.png',
    },
    'unit_cost': {
        'yield_type': 'YIELD_PRODUCTION',
        'cost': 30,
    },
    'unit_stat': {
        'combat': 15,
    },
    'unit_replace': {
        'replaces_unit_type': 'UNIT_WARRIOR',
    },
    'visual_remap': {
        'to': 'UNIT_WARRIOR',
    },
    'localizations': [
        {
            'name': 'Sabum Kibittum',
            'description': 'Elite warrior of Babylon, trained in ancient tactics.',
        },
    ],
})

# Constructibles
edubba = ConstructibleBuilder()
edubba.action_group_bundle = AGE_ANTIQUITY
edubba.fill({
    'constructible_type': 'BUILDING_BABYLON_EDUBBA',
    'constructible': {
        'cost': 1,
    },
    'building': {
        'trait_type': 'TRAIT_BABYLON',
    },
    'type_tags': ['AGELESS', 'SCIENCE', 'CULTURE'],
    'constructible_valid_districts': ['DISTRICT_URBAN', 'DISTRICT_CITY_CENTER'],
    'constructible_maintenances': [
        {
            'yield_type': 'YIELD_PRODUCTION',
            'amount': 2,
        },
    ],
    'yield_changes': [
        {
            'yield_type': 'YIELD_SCIENCE',
            'yield_change': 30,
        },
        {
            'yield_type': 'YIELD_CULTURE',
            'yield_change': 15,
        },
    ],
    'icon': {
        'path': 'fs://game/${metadata.id}/edubba.png',
    },
    'advisories': ['ADVISORY_CLASS_SCIENCE'],
    'localizations': [
        {
            'name': 'Edubba',
            'description': 'House of Tablets - preserves Babylon\'s vast knowledge.',
            'tooltip': 'Increases science and culture yields.',
        },
    ],
})

academy = ConstructibleBuilder()
academy.action_group_bundle = AGE_ANTIQUITY
academy.fill({
    'constructible_type': 'BUILDING_BABYLON_ACADEMY',
    'constructible': {
        'cost': 150,
    },
    'building': {
        'trait_type': 'TRAIT_BABYLON',
    },
    'type_tags': ['UNIQUE', 'SCIENCE'],
    'constructible_valid_districts': ['DISTRICT_URBAN'],
    'yield_changes': [
        {
            'yield_type': 'YIELD_SCIENCE',
            'yield_change': 10,
        },
    ],
    'advisories': ['ADVISORY_CLASS_SCIENCE'],
    'localizations': [
        {
            'name': 'Academy',
            'description': 'Centre of learning where knowledge is preserved and expanded.',
        },
    ],
})

ziggurat = ConstructibleBuilder()
ziggurat.action_group_bundle = AGE_ANTIQUITY
ziggurat.fill({
    'constructible_type': 'QUARTER_BABYLON_ZIGGURAT',
    'constructible': {
        'cost': 400,
    },
    'building': {
        'trait_type': 'TRAIT_BABYLON',
    },
    'type_tags': ['UNIQUE', 'CULTURE'],
    'constructible_valid_districts': ['DISTRICT_URBAN'],
    'yield_changes': [
        {
            'yield_type': 'YIELD_CULTURE',
            'yield_change': 20,
        },
    ],
    'advisories': ['ADVISORY_CLASS_CULTURE'],
    'localizations': [
        {
            'name': 'Ziggurat Complex',
            'description': 'A magnificent stepped temple complex dedicated to the gods of Babylon.',
        },
    ],
})

# Progression tree nodes
progression_tree_node = ProgressionTreeNodeBuilder()
progression_tree_node.action_group_bundle = AGE_ANTIQUITY
progression_tree_node.fill({
    'progression_tree_node_type': 'NODE_CIVICS_BABYLON1',
    'progression_tree_node': {
        'progression_tree_node_type': 'NODE_CIVICS_BABYLON1',
    },
    'progression_tree_advisories': ['ADVISORY_CLASS_SCIENCE'],
    'localizations': [
        {
            'name': 'Babylonian Learning',
        },
    ],
})
progression_tree_node.bind([node1_modifier, edubba, unit])

progression_tree_node2 = ProgressionTreeNodeBuilder()
progression_tree_node2.action_group_bundle = AGE_ANTIQUITY
progression_tree_node2.fill({
    'progression_tree_node_type': 'NODE_CIVICS_BABYLON2',
    'progression_tree_node': {
        'progression_tree_node_type': 'NODE_CIVICS_BABYLON2',
    },
    'progression_tree_advisories': ['ADVISORY_CLASS_SCIENCE'],
    'localizations': [
        {
            'name': 'Ancient Wisdom',
        },
    ],
})
progression_tree_node2.bind([node2_modifier])

# Progression trees
progression_tree = ProgressionTreeBuilder()
progression_tree.action_group_bundle = AGE_ANTIQUITY
progression_tree.fill({
    'progression_tree_type': 'TREE_CIVICS_BABYLON',
    'progression_tree': {
        'progression_tree_type': 'TREE_CIVICS_BABYLON',
        'age_type': 'AGE_ANTIQUITY',
    },
    'progression_tree_prereqs': [
        {
            'node': 'NODE_CIVICS_BABYLON2',
            'prereq_node': 'NODE_CIVICS_BABYLON1',
        },
    ],
    'localizations': [
        {
            'name': 'Babylonian Civic Tree',
        },
    ],
})
progression_tree.bind([progression_tree_node, progression_tree_node2])

# Civilization
civilization = CivilizationBuilder()
civilization.action_group_bundle = AGE_ANTIQUITY
civilization.fill({
    'civilization_type': 'CIVILIZATION_BABYLON',
    'civilization': {
        'domain': 'AntiquityAgeCivilizations',
        'civilization_type': 'CIVILIZATION_BABYLON',
        'unique_culture_progression_tree': 'TREE_CIVICS_BABYLON',
        'random_city_name_depth': 10,
    },
    'civilization_traits': ['TRAIT_ANTIQUITY_CIV', 'TRAIT_ATTRIBUTE_SCIENTIFIC'],
    'civilization_tags': ['TAG_TRAIT_SCIENTIFIC'],
    'icon': {
        'path': 'icons/civ_sym_babylon',
    },
    'civilization_unlocks': [
        {
            'age_type': 'AGE_EXPLORATION',
            'type': 'CIVILIZATION_PERSIA',
            'kind': 'KIND_CIVILIZATION',
            'name': 'LOC_CIVILIZATION_PERSIA_NAME',
            'description': 'LOC_CIVILIZATION_PERSIA_DESCRIPTION',
            'icon': 'CIVILIZATION_PERSIA',
        },
    ],
    'leader_civilization_biases': [
        {
            'leader_type': 'LEADER_XERXES',
            'bias': 2,
            'reason_type': 'LOC_UNLOCK_PLAY_AS_XERXES_BABYLON_TOOLTIP',
            'choice_type': 'LOC_CREATE_GAME_GEOGRAPHIC_CHOICE',
        },
    ],
    'start_bias_terrains': [
        {
            'terrain_type': 'TERRAIN_FLAT',
            'score': 15,
        },
        {
            'terrain_type': 'TERRAIN_NAVIGABLE_RIVER',
            'score': 20,
        },
    ],
    'start_bias_rivers': 5,
    'localizations': [
        {
            'name': 'Babylon',
            'description': 'Keepers of ancient wisdom and masters of the sciences.',
            'full_name': 'The Kingdom of Babylon',
            'adjective': 'Babylonian',
            'city_names': CITY_NAMES,
        },
        {
            'entity_id': 'CIVILIZATION_BABYLON_ABILITY',
            'name': 'Babylonian Wisdom',
            'description': 'Receive a Science bonus for every Campus and Holy Site built in Babylon cities.',
        },
        {
            'entity_id': 'BABYLON_LOADING',
            'name': 'An ancient power awakens',
            'description': 'The great libraries of Babylon hold scientific secrets.',
        },
    ],
    'loading_info_civilizations': [
        {
            'civilization_text': 'LOC_CIVILIZATION_BABYLON_DESCRIPTION',
            'subtitle': 'LOC_BABYLON_LOADING_NAME',
            'tip': 'LOC_BABYLON_LOADING_DESCRIPTION',
            'background_image_high': 'babylon/textures/1080_babylon.png',
            'background_image_low': 'babylon/textures/720_babylon.png',
            'foreground_image': 'babylon/textures/720_babylon.png',
        },
    ],
    'leader_civ_priorities': [
        {
            'leader_type': 'LEADER_XERXES',
            'priority': 8,
        },
    ],
    'ai_list_types': [
        {
            'list_type': 'Babylon Unit Biases',
        },
        {
            'list_type': 'Babylon Government Bias',
        },
        {
            'list_type': 'Babylon Constructibles Biases',
        },
        {
            'list_type': 'Babylon Yield Biases',
        },
        {
            'list_type': 'Babylon Budget Biases',
        },
    ],
    'ai_lists': [
        {
            'list_type': 'Babylon Unit Biases',
            'leader_type': 'TRAIT_BABYLON',
            'system': 'UnitBiases',
        },
        {
            'list_type': 'Babylon Government Bias',
            'leader_type': 'TRAIT_BABYLON',
            'system': 'GovernmentBiases',
        },
        {
            'list_type': 'Babylon Constructibles Biases',
            'leader_type': 'TRAIT_BABYLON',
            'system': 'ConstructibleBiases',
        },
        {
            'list_type': 'Babylon Yield Biases',
            'leader_type': 'TRAIT_BABYLON',
            'system': 'YieldBiases',
        },
        {
            'list_type': 'Babylon Budget Biases',
            'leader_type': 'TRAIT_BABYLON',
            'system': 'AiBudgetBiases',
        },
    ],
    'ai_favored_items': [
        {
            'list_type': 'Babylon Unit Biases',
            'item': 'UNIT_BABYLON_SABUM_KIBITTUM',
            'value': 50,
        },
        {
            'list_type': 'Babylon Government Bias',
            'item': 'GOVERNMENT_AUTOCRACY',
            'value': 25,
        },
        {
            'list_type': 'Babylon Constructibles Biases',
            'item': 'BUILDING_BABYLON_EDUBBA',
            'value': 200,
        },
        {
            'list_type': 'Babylon Yield Biases',
            'item': 'YIELD_SCIENCE',
            'value': 50,
        },
        {
            'list_type': 'Babylon Yield Biases',
            'item': 'YIELD_CULTURE',
            'value': 10,
        },
        {
            'list_type': 'Babylon Budget Biases',
            'item': 'AI_BUDGET_CULTURE',
            'value': 25,
        },
    ],
    'vis_art_building_cultures': ['BUILDING_CULTURE_MID', 'ANT_MUD', 'EXP_MUD', 'MOD_MUD'],
    'vis_art_unit_cultures': ['MidE'],
})

# Bind all entities to civilization
civilization.bind([unit, edubba, academy, ziggurat, progression_tree, civilization_modifier])

# Add all builders to mod
mod.add([
    civilization,
    unit,
    edubba,
    academy,
    ziggurat,
    progression_tree,
    tradition_scribes,
    tradition_library,
    civilization_icon,
    unit_icon,
])

# Build mod
if __name__ == '__main__':
    mod.build('./dist-babylon')