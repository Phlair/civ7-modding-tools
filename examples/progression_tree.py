"""
Progression Tree (Civics) Example

This example demonstrates:
- Creating a progression tree (civics tree)
- Defining tree nodes with different civic types
- Setting era/age requirements
- Linking nodes together
- Adding effects and modifiers to civics
- Unlocks for units, buildings, etc.
"""

from civ7_modding_tools import Mod, ActionGroupBundle
from civ7_modding_tools.builders import (
    ProgressionTreeBuilder,
    ProgressionTreeNodeBuilder,
)
from civ7_modding_tools.constants import Effect, Yield

mod = Mod(
    id='progression-tree-example',
    version='1.0.0',
    name='Progression Tree Example',
    description='Demonstrates custom civics tree creation'
)

# Create a progression tree (civics)
tree = ProgressionTreeBuilder({
    'progression_tree': {
        'tree_type': 'TREE_CUSTOM_CIVICS',
        'name': 'Custom Civics Tree',
    },
    'nodes': [
        {
            'node_type': 'NODE_FOUNDATIONAL',
            'era': 'ERA_ANTIQUITY',
            'effects': [
                {'effect': Effect.UNIT_ADJUST_MOVEMENT, 'value': 1}
            ],
        },
        {
            'node_type': 'NODE_ADVANCED',
            'era': 'ERA_CLASSICAL',
            'unlocks': ['UNIT_CUSTOM_WARRIOR'],
            'effects': [
                {'effect': Effect.YIELD_ADJUST, 'yield': Yield.SCIENCE, 'value': 5}
            ],
        },
    ],
    'action_group_bundle': ActionGroupBundle.ALWAYS,
})

mod.add(tree)
mod.build('./dist-progression-tree-example')
print("Progression tree example mod built successfully!")
