"""
Unique Quarter (District Variant) Example

This example demonstrates:
- Creating a unique district variant for a civilization
- Replacing standard districts with civilization-specific versions
- Setting district properties (cost, yields, prerequisites)
- Unique district bonuses and effects
- Icon and localization for unique districts
"""

from civ7_modding_tools import Mod, ActionGroupBundle
from civ7_modding_tools.builders import UniqueQuarterBuilder, ImportFileBuilder
from civ7_modding_tools.constants import District, Yield

mod = Mod(
    id='unique-quarter-example',
    version='1.0.0',
    name='Unique Quarter Example',
    description='Demonstrates creating civilization-specific districts'
)

# Create a unique commercial district variant
unique_market = UniqueQuarterBuilder({
    'unique_quarter': {
        'quarter_type': 'QUARTER_CUSTOM_MARKET',
        'base_district': District.COMMERCIAL_HUB,
        'cost': 120,
        'maintenance': 2,
    },
    'yields': [
        {'yield': Yield.GOLD, 'amount': 4},
        {'yield': Yield.PRODUCTION, 'amount': 2},
    ],
    'localizations': [
        {
            'name': 'Grand Bazaar',
            'description': 'Unique market for custom civilization',
        }
    ],
    'action_group_bundle': ActionGroupBundle.AGE_MEDIEVAL,
})

# Import unique quarter icon
icon_import = ImportFileBuilder({
    'source': './assets/unique-market.png',
    'target_name': 'districts/custom/grand-bazaar.png',
})

mod.add([unique_market, icon_import])
mod.build('./dist-unique-quarter-example')
print("Unique quarter example mod built successfully!")
