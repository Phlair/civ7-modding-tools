"""
Custom Icon Import Example

This example demonstrates:
- Importing custom asset files (icons, images)
- Using ImportFileBuilder for visual assets
- Organizing assets into mod directories
- Icon placement for civilizations, units, buildings
"""

from civ7_modding_tools import Mod
from civ7_modding_tools.builders import ImportFileBuilder

mod = Mod(
    id='custom-icon-example',
    version='1.0.0',
    name='Custom Icon Example',
    description='Demonstrates importing custom icons and assets'
)

# Import custom civilization icon
civ_icon = ImportFileBuilder({
    'source': './assets/civilization-icon.png',
    'target_name': 'civilizations/custom/icon.png',
})

# Import custom unit icon
unit_icon = ImportFileBuilder({
    'source': './assets/unit-icon.png',
    'target_name': 'units/custom/warrior-icon.png',
})

# Import custom building/constructible icon
building_icon = ImportFileBuilder({
    'source': './assets/building-icon.png',
    'target_name': 'constructibles/custom/market.png',
})

mod.add([civ_icon, unit_icon, building_icon])
mod.build('./dist-custom-icon-example')
print("Custom icon example mod built successfully!")
