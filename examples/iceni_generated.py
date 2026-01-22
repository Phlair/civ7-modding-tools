"""
Phlair's Iceni Civilization - Generated from YAML

Adds the Iceni Civilization
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

# Module localization
MODULE_LOC = ModuleLocalization(
    name="Iceni",
    description="Adds the Iceni Civilization",
)

# Mod metadata and setup
mod = Mod({
    'id': 'iceni',
    'name': 'Phlair\'s Iceni',
    'authors': 'Phlair',
    'description': 'Adds the Iceni Civilization',
    'package': 'Iceni',
    'module_localizations': MODULE_LOC,
})

# Action group
Antiquity = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')

# Progression tree nodes
iceni_node1 = ProgressionTreeNodeBuilder()
iceni_node1.action_group_bundle = Antiquity
iceni_node1.fill({
    'progression_tree_node_type': 'NODE_CIVICS_ICENI_1',
    'progression_tree_node': {
        'progression_tree_node_type': 'NODE_CIVICS_ICENI_1',
    },
    'localizations': [
        {
            'name': 'Iceni Foundations',
        },
    ],
})
iceni_node1.bind([])

iceni_node2 = ProgressionTreeNodeBuilder()
iceni_node2.action_group_bundle = Antiquity
iceni_node2.fill({
    'progression_tree_node_type': 'NODE_CIVICS_ICENI_2',
    'progression_tree_node': {
        'progression_tree_node_type': 'NODE_CIVICS_ICENI_2',
    },
    'localizations': [
        {
            'name': 'Iceni Advancement',
        },
    ],
})
iceni_node2.bind([])

# Progression trees
progression_tree_iceni = ProgressionTreeBuilder()
progression_tree_iceni.action_group_bundle = Antiquity
progression_tree_iceni.fill({
    'progression_tree_type': 'TREE_CIVICS_ICENI',
    'progression_tree': {
        'progression_tree_type': 'TREE_CIVICS_ICENI',
        'age_type': 'AGE_ANTIQUITY',
    },
    'progression_tree_prereqs': [
        {
            'node': 'NODE_CIVICS_ICENI_2',
            'prereq_node': 'NODE_CIVICS_ICENI_1',
        },
    ],
    'localizations': [
        {
            'name': 'Iceni Civic Tree',
        },
    ],
})
progression_tree_iceni.bind([iceni_node1, iceni_node2])

# Civilization
civilization = CivilizationBuilder()
civilization.action_group_bundle = Antiquity
civilization.fill({
    'civilization_type': 'CIVILIZATION_ICENI',
    'localizations': [
        {
            'name': 'Iceni',
            'adjective': 'Iceni',
            'description': 'The Iceni were an ancient tribe of eastern Britain during the Iron Age and early Roman era. Their territory included present-day Norfolk and parts of Suffolk and Cambridgeshire, and bordered the area of the Corieltauvi to the west, and the Catuvellauni and Trinovantes to the south.',
            'city_names': ['Venta Icenorum', 'Brettenham', 'Durolipons', 'Ixworth', 'Narford', 'Thetford', 'Snettisham', 'Toftrees', 'Wilton', 'Camvorritum'],
        },
    ],
    'civilization_traits': ['TRAIT_ANTIQUITY_CIV', 'TRAIT_ATTRIBUTE_ECONOMIC', 'TRAIT_ATTRIBUTE_MILITARISTIC'],
    'vis_art_building_cultures': ['BUILDING_CULTURE_NAM'],
    'building_culture_base': 'MUD',
    'vis_art_unit_cultures': ['Euro'],
    'start_bias_rivers': 7,
    'start_bias_terrains': [
        {
            'terrain_type': 'TERRAIN_FLAT',
            'score': 8,
        },
    ],
    'civilization_unlocks': [],
    'civilization': {
        'unique_culture_progression_tree': 'TREE_CIVICS_ICENI',
    },
    'icon': {
        'path': 'icons/civ_sym_iceni',
    },
})

# Bind all entities to civilization
civilization.bind([progression_tree_iceni])

# Add all builders to mod
mod.add([
    civilization,
    iceni_node1,
    iceni_node2,
    progression_tree_iceni,
])

# Build mod
if __name__ == '__main__':
    mod.build(f'./dist-{mod.mod_id}')