"""Phase 2 example: Building a complete mod with multiple civilizations, units, and buildings."""

from civ7_modding_tools import Mod
from civ7_modding_tools.builders import (
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
)


def main():
    """Create a sample mod with a custom civilization."""
    
    # Initialize the mod
    mod = Mod(
        mod_id="rome-expansion",
        version="1.0.0",
        name="Roman Empire Expansion",
        description="Adds a custom Roman civilization with unique units and buildings",
        authors="Civ7 Modding Tools",
    )
    
    # Create Roman civilization
    rome_civ = CivilizationBuilder().fill({
        "civilization_type": "CIVILIZATION_ROME_CUSTOM",
        "civilization": {
            "base_tourism": 2,
            "base_loyalty": 5,
            "legacy_modifier": True,
        },
        "civilization_traits": [
            "TRAIT_ECONOMIC",
            "TRAIT_DIPLOMATIC",
        ],
        "city_names": [
            "Rome",
            "Milan",
            "Venice",
            "Florence",
            "Naples",
            "Palermo",
            "Genoa",
            "Bologna",
            "Ravenna",
            "Siena",
        ],
    })
    mod.add(rome_civ)
    
    # Create Roman Legion unit
    legion = UnitBuilder().fill({
        "unit_type": "UNIT_ROMAN_LEGION",
        "unit": {
            "unit_class": "UNIT_CLASS_MELEE",
            "unit_movement_class": "UNIT_MOVEMENT_CLASS_LAND",
            "combat": 28,
            "ranged_combat": 0,
            "range": 0,
            "movement": 2,
            "era_type": "ERA_CLASSICAL",
        },
        "unit_costs": [
            {
                "yield_type": "YIELD_PRODUCTION",
                "amount": 65,
            },
        ],
    })
    mod.add(legion)
    
    # Create Roman Archer unit
    archer = UnitBuilder().fill({
        "unit_type": "UNIT_ROMAN_ARCHER",
        "unit": {
            "unit_class": "UNIT_CLASS_RANGED",
            "unit_movement_class": "UNIT_MOVEMENT_CLASS_LAND",
            "combat": 18,
            "ranged_combat": 32,
            "range": 2,
            "movement": 2,
            "era_type": "ERA_CLASSICAL",
        },
        "unit_costs": [
            {
                "yield_type": "YIELD_PRODUCTION",
                "amount": 50,
            },
        ],
    })
    mod.add(archer)
    
    # Create Roman Forum building
    forum = ConstructibleBuilder().fill({
        "constructible_type": "BUILDING_ROMAN_FORUM",
        "constructible": {
            "cost": 150,
            "maintenance": 2,
            "district_type": "DISTRICT_COMMERCIAL_HUB",
            "era_type": "ERA_CLASSICAL",
        },
        "yield_changes": [
            {
                "yield_type": "YIELD_GOLD",
                "amount": 4,
            },
            {
                "yield_type": "YIELD_CULTURE",
                "amount": 2,
            },
        ],
    })
    mod.add(forum)
    
    # Create Roman Temple building
    temple = ConstructibleBuilder().fill({
        "constructible_type": "BUILDING_ROMAN_TEMPLE",
        "constructible": {
            "cost": 120,
            "maintenance": 1,
            "district_type": "DISTRICT_HOLY_SITE",
            "era_type": "ERA_CLASSICAL",
        },
        "yield_changes": [
            {
                "yield_type": "YIELD_FAITH",
                "amount": 3,
            },
            {
                "yield_type": "YIELD_CULTURE",
                "amount": 1,
            },
        ],
    })
    mod.add(temple)
    
    # Create Roman Aqueduct improvement
    aqueduct = ConstructibleBuilder().fill({
        "constructible_type": "IMPROVEMENT_ROMAN_AQUEDUCT",
        "constructible": {
            "cost": 80,
            "maintenance": 1,
            "improvement": True,
            "era_type": "ERA_CLASSICAL",
        },
        "yield_changes": [
            {
                "yield_type": "YIELD_PRODUCTION",
                "amount": 2,
            },
        ],
    })
    mod.add(aqueduct)
    
    # Generate mod files to ./dist
    print("Building mod: Roman Empire Expansion")
    mod.build("./dist", clear=True)
    print("✓ Mod built successfully!")
    print("✓ Output: ./dist/")
    print(f"✓ Files: {len(mod.builders)} builders → {sum(len(b.build()) for b in mod.builders)} output files")


if __name__ == "__main__":
    main()
