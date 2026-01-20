"""
Tester Jester Civilization _ Generated from YAML


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
    name="Tester Jester",
    authors="Phlair",
)

# Mod metadata and setup
mod = Mod({
    'id': 'tester_jester',
    'version': '0.0.1',
    'name': 'Tester Jester',
    'authors': 'Phlair',
    'enabled_by_default': True,
    'affects_saved_games': True,
    'module_localizations': MODULE_LOC,
})

# Action group
AGE_ANTIQUITY = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')

# Progression tree nodes
tester_jester_node1 = ProgressionTreeNodeBuilder()
tester_jester_node1.action_group_bundle = AGE_ANTIQUITY
tester_jester_node1.fill({
    'progression_tree_node_type': 'NODE_CIVICS_TESTER_1',
    'progression_tree_node': {
        'progression_tree_node_type': 'NODE_CIVICS_TESTER_1',
    },
    'localizations': [
        {
            'name': 'Tester Jester Foundations',
        },
    ],
})
tester_jester_node1.bind([])

tester_jester_node2 = ProgressionTreeNodeBuilder()
tester_jester_node2.action_group_bundle = AGE_ANTIQUITY
tester_jester_node2.fill({
    'progression_tree_node_type': 'NODE_CIVICS_TESTER_2',
    'progression_tree_node': {
        'progression_tree_node_type': 'NODE_CIVICS_TESTER_2',
    },
    'localizations': [
        {
            'name': 'Tester Jester Advancement',
        },
    ],
})
tester_jester_node2.bind([])

# Progression trees
progression_tree_tester_jester = ProgressionTreeBuilder()
progression_tree_tester_jester.action_group_bundle = AGE_ANTIQUITY
progression_tree_tester_jester.fill({
    'progression_tree_type': 'TREE_CIVICS_TESTER',
    'progression_tree': {
        'progression_tree_type': 'TREE_CIVICS_TESTER',
        'age_type': {
            'action_group_id': 'AGE_ANTIQUITY',
        },
    },
    'progression_tree_prereqs': [
        {
            'node': 'NODE_CIVICS_TESTER_2',
            'prereq_node': 'NODE_CIVICS_TESTER_1',
        },
    ],
    'localizations': [
        {
            'name': 'Tester Jester Civic Tree',
        },
    ],
})
progression_tree_tester_jester.bind([tester_jester_node1, tester_jester_node2])

# Civilization
tester_jester = CivilizationBuilder()
tester_jester.action_group_bundle = AGE_ANTIQUITY
tester_jester.fill({
    'civilization_type': 'CIVILIZATION_TESTER',
    'localizations': [
        {
            'name': 'Tester Jester',
            'adjective': 'Testerian',
        },
    ],
    'civilization_traits': ['TRAIT_CULTURAL'],
    'vis_art_building_cultures': ['BUILDING_CULTURE_EAS'],
    'vis_art_unit_cultures': ['CIVILIZATION_EGYPT'],
    'civilization': {
        'unique_culture_progression_tree': 'TREE_CIVICS_TESTER',
        'civilization_type': 'CIVILIZATION_TESTER',
    },
})

# Bind all entities to civilization
tester_jester.bind([progression_tree_tester_jester])

# Add all builders to mod
mod.add([
    tester_jester,
    progression_tree_tester_jester,
])

# Build mod
if __name__ == '__main__':
    mod.build('./dist_tester_jester')