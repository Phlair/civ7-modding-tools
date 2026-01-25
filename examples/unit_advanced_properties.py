"""Example: Unit with Advanced Properties

Demonstrates how to use all the newly added unit properties including:
- Tier
- Maintenance (upkeep)
- Zone of Control
- Cost Progression
- Capability Flags
- Promotion Class
- Unit Upgrades
- Unit Advisories
"""

from civ7_modding_tools import Mod
from civ7_modding_tools.builders import UnitBuilder
from civ7_modding_tools.constants import Trait

# Create a new mod
mod = Mod(
    id='advanced-unit-example',
    version='1.0.0',
    name='Advanced Unit Properties Example',
    description='Shows all new unit configuration options',
    authors='Example Author'
)

# Example 1: Tier 2 unit with maintenance and zone of control
spearman = UnitBuilder().fill({
    'unit_type': 'UNIT_EXAMPLE_SPEARMAN',
    'unit': {
        'core_class': 'CORE_CLASS_MILITARY',
        'domain': 'DOMAIN_LAND',
        'formation_class': 'FORMATION_CLASS_LAND_COMBAT',
        'unit_movement_class': 'UNIT_MOVEMENT_CLASS_FOOT',
        'base_moves': 2,
        'base_sight_range': 2,
        'tier': 2,  # Tier 2 unit
        'maintenance': 1,  # 1 gold per turn upkeep
        'zone_of_control': True,  # Blocks enemy movement
        'promotion_class': 'PROMOTION_CLASS_LAND_MELEE',
        'trait_type': Trait.MILITARY.value,
    },
    'unit_stat': {
        'combat': 25,
    },
    'unit_cost': {
        'yield_type': 'YIELD_PRODUCTION',
        'cost': 40,
    },
    'unit_upgrade': {
        'upgrade_unit': 'UNIT_EXAMPLE_PHALANX',  # Upgrades to phalanx
    },
    'unit_advisories': [{
        'advisory_class_type': 'ADVISORY_CLASS_MILITARY',
    }],
    'localizations': [{
        'name': 'Example Spearman',
        'description': 'A tier 2 melee infantry unit with zone of control',
    }],
})

# Example 2: Settler with cost progression
settler = UnitBuilder().fill({
    'unit_type': 'UNIT_EXAMPLE_SETTLER',
    'unit': {
        'core_class': 'CORE_CLASS_CIVILIAN',
        'domain': 'DOMAIN_LAND',
        'formation_class': 'FORMATION_CLASS_CIVILIAN',
        'unit_movement_class': 'UNIT_MOVEMENT_CLASS_FOOT',
        'base_moves': 3,
        'base_sight_range': 1,
        'tier': 1,
        'found_city': True,  # Can found cities
        'prereq_population': 5,  # City needs 5 population to build
        'cost_progression_model': 'COST_PROGRESSION_NUM_SETTLEMENTS',
        'cost_progression_param1': 30,  # +30 production per city founded
        'zone_of_control': False,  # Civilians don't have ZoC
    },
    'unit_cost': {
        'yield_type': 'YIELD_PRODUCTION',
        'cost': 50,
    },
    'localizations': [{
        'name': 'Example Settler',
        'description': 'Founds new cities. Cost increases with each city.',
    }],
})

# Example 3: Great Person (cannot be trained or purchased)
great_person = UnitBuilder().fill({
    'unit_type': 'UNIT_EXAMPLE_GREAT_PERSON',
    'unit': {
        'core_class': 'CORE_CLASS_CIVILIAN',
        'domain': 'DOMAIN_LAND',
        'formation_class': 'FORMATION_CLASS_CIVILIAN',
        'unit_movement_class': 'UNIT_MOVEMENT_CLASS_FOOT',
        'base_moves': 4,
        'base_sight_range': 2,
        'tier': 1,
        'can_train': False,  # Cannot be trained in cities
        'can_purchase': False,  # Cannot be purchased
        'can_earn_experience': False,  # Cannot gain promotions
        'zone_of_control': False,
    },
    'localizations': [{
        'name': 'Example Great Person',
        'description': 'A unique unit that cannot be built normally.',
    }],
})

# Example 4: Merchant unit with trade route capability
merchant = UnitBuilder().fill({
    'unit_type': 'UNIT_EXAMPLE_MERCHANT',
    'unit': {
        'core_class': 'CORE_CLASS_CIVILIAN',
        'domain': 'DOMAIN_LAND',
        'formation_class': 'FORMATION_CLASS_CIVILIAN',
        'unit_movement_class': 'UNIT_MOVEMENT_CLASS_FOOT',
        'base_moves': 3,
        'base_sight_range': 2,
        'tier': 1,
        'make_trade_route': True,  # Can establish trade routes
        'zone_of_control': False,
    },
    'unit_cost': {
        'yield_type': 'YIELD_GOLD',
        'cost': 100,
    },
    'localizations': [{
        'name': 'Example Merchant',
        'description': 'Establishes trade routes between cities.',
    }],
})

# Add all units to mod
mod.add([spearman, settler, great_person, merchant])

# Build the mod
if __name__ == '__main__':
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        print(f"Mod built successfully in {tmpdir}")
        print("\nNew unit properties demonstrated:")
        print("  ✓ tier - Unit progression tier (1-3)")
        print("  ✓ maintenance - Gold per turn upkeep")
        print("  ✓ zone_of_control - Tactical movement restriction")
        print("  ✓ cost_progression_model/param1 - Scaling costs")
        print("  ✓ can_train/can_purchase/can_earn_experience - Capability flags")
        print("  ✓ found_city - Settler capability")
        print("  ✓ make_trade_route - Merchant capability")
        print("  ✓ prereq_population - City size requirement")
        print("  ✓ promotion_class - Promotion tree assignment")
        print("  ✓ unit_upgrade - Upgrade path definition")
        print("  ✓ unit_advisories - Advisory classification")
