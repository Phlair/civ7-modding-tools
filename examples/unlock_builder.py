"""
Unlock System Example

This example demonstrates:
- Creating unlock definitions for units, buildings, technologies
- Linking unlocks to progression trees/civics
- Setting unlock conditions and prerequisites
- Civilization-specific unlocks via CivilizationUnlockBuilder
- Tier progression for unlocked content
"""

from civ7_modding_tools import Mod, ActionGroupBundle
from civ7_modding_tools.builders import (
    UnlockBuilder,
    CivilizationUnlockBuilder,
)
from civ7_modding_tools.constants import UnlockType

mod = Mod(
    id='unlock-example',
    version='1.0.0',
    name='Unlock System Example',
    description='Demonstrates game progression unlock system'
)

# Create a unit unlock
unit_unlock = UnlockBuilder({
    'unlock': {
        'unlock_type': UnlockType.UNIT,
        'unlock_key': 'UNLOCK_CUSTOM_WARRIOR',
        'unit': 'UNIT_CUSTOM_WARRIOR',
    },
    'requirements': [
        {'requirement': 'REQ_TECH_BRONZE_WORKING'},
    ],
    'localizations': [
        {
            'name': 'Unlock Custom Warrior',
            'description': 'Unlocks the custom warrior unit',
        }
    ],
})

# Create a building unlock
building_unlock = UnlockBuilder({
    'unlock': {
        'unlock_type': UnlockType.BUILDING,
        'unlock_key': 'UNLOCK_CUSTOM_MARKET',
        'building': 'BUILDING_CUSTOM_MARKET',
    },
    'requirements': [
        {'requirement': 'REQ_TECH_CURRENCY'},
    ],
})

# Create civilization-specific unlocks
civ_unlocks = CivilizationUnlockBuilder({
    'civilization': 'CIVILIZATION_CUSTOM',
    'unlocks': [
        'UNLOCK_CUSTOM_WARRIOR',
        'UNLOCK_CUSTOM_MARKET',
    ],
    'action_group_bundle': ActionGroupBundle.ALWAYS,
})

mod.add([unit_unlock, building_unlock, civ_unlocks])
mod.build('./dist-unlock-example')
print("Unlock system example mod built successfully!")
