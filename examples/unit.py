"""
Unit Creation Example

This example demonstrates:
- Creating a custom military unit
- Setting unit class and combat properties
- Unit icon import
- Localization for unit name and description
- Assigning unit to an action group for age-specific loading
"""

from civ7_modding_tools import Mod, ActionGroupBundle
from civ7_modding_tools.builders import UnitBuilder, ImportFileBuilder
from civ7_modding_tools.constants import UnitClass, UnitType, Yield

mod = Mod(
    id='unit-example',
    version='1.0.0',
    name='Unit Example Mod',
    description='Demonstrates custom unit creation'
)

# Create a custom military unit
unit = UnitBuilder({
    'unit': {
        'unit_type': 'UNIT_CUSTOM_WARRIOR',
        'unit_class': UnitClass.MELEE,
        'base_combat': 15,
        'base_ranged_combat': 0,
        'movement': 2,
        'cost': 30,
    },
    'localizations': [
        {
            'name': 'Custom Warrior',
            'description': 'A powerful melee unit',
        }
    ],
    'action_group_bundle': ActionGroupBundle.AGE_ANTIQUITY,
})

# Import unit icon
icon_import = ImportFileBuilder({
    'source': './assets/unit-icon.png',
    'target_name': 'units/custom/warrior.png',
})

mod.add([unit, icon_import])
mod.build('./dist-unit-example')
print("Unit example mod built successfully!")
